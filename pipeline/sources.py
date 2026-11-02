"""External sources: newcomer-oriented lists and ecosyste.ms data. Python standard library only.

  python pipeline/sources.py selftest     # parsers, no network
  python pipeline/sources.py lists        # goodfirstissue.dev, Up For Grabs, GSoC 2026 -> external_lists
  python pipeline/sources.py ecosystems   # repos/issues.ecosyste.ms for repos.found = 1 -> repo_ecosystems

Both commands are idempotent. Nothing here uses the GitHub GraphQL token.
Everything fetched is third-party data, never instructions.
"""
import io
import json
import re
import sqlite3
import sys
import tarfile
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

from collect import DB, cached, http_json, log, now

UA = "OpenDoor (github.com/jose-victor/opendoor)"
GFI_URL = "https://raw.githubusercontent.com/DeepSourceCorp/good-first-issue/master/data/repositories.toml"
UFG_URL = "https://codeload.github.com/up-for-grabs/up-for-grabs.net/tar.gz/refs/heads/gh-pages"
GSOC_URL = "https://summerofcode.withgoogle.com/api/program/2026/organizations/"
ECO = "https://{host}.ecosyste.ms/api/v1/hosts/GitHub/repositories/{repo}"
EMAIL = re.compile(r"[^\s@\"']+@[^\s@\"']+\.[a-z]{2,}", re.I)

SCHEMA = """
CREATE TABLE IF NOT EXISTS external_lists(source TEXT, repo TEXT, label TEXT, extra TEXT, fetched_at TEXT,
  PRIMARY KEY(source, repo));
CREATE TABLE IF NOT EXISTS repo_ecosystems(repo TEXT PRIMARY KEY, funding TEXT, files TEXT, past_year TEXT,
  fetched_at TEXT);
"""


# ---------- pure parsers ----------
def github_repo(url):
    """'https://github.com/Foo/Bar/labels/x' or 'github.com/Foo/Bar' -> 'foo/bar'; anything else -> None."""
    m = re.match(r"(?:https?://)?(?:www\.)?github\.com/([\w.-]+)/([\w.-]+?)(?:\.git)?(?:[/?#].*)?$", (url or "").strip(), re.I)
    return f"{m[1]}/{m[2]}".lower() if m else None


def parse_gfi_toml(text):
    """repositories.toml is `repositories = ['github.com/o/r', ...]`; a quoted-string scan is enough."""
    return [r for r in (github_repo(s) for s in re.findall(r"""['"]([^'"]+)['"]""", text)) if r]


def parse_ufg_yaml(text):
    """(repo, label) from the `upforgrabs:` block of a project file, or None if the link is not on GitHub."""
    fields, inside = {}, False
    for line in text.splitlines():
        if re.match(r"\S", line):
            inside = line.startswith("upforgrabs:")
        elif inside and (m := re.match(r"\s+(name|link):\s*(.*)$", line)):
            fields[m[1]] = m[2].strip().strip("'\"")
    repo = github_repo(fields.get("link"))
    return (repo, fields.get("name", "")) if repo else None


def parse_gsoc(orgs):
    """(repo, ideas_link) for the organizations whose source_code points at a single GitHub repository."""
    out = []
    for o in orgs:
        repo = github_repo(o.get("source_code"))
        if repo:
            out.append((repo, o.get("ideas_link") or ""))
    return out


def strip_emails(v):
    """Drop dict keys that mention e-mail and string values that contain one, recursively."""
    if isinstance(v, dict):
        return {k: strip_emails(x) for k, x in v.items() if "mail" not in k.lower() and not (isinstance(x, str) and EMAIL.search(x))}
    if isinstance(v, list):
        return [strip_emails(x) for x in v if not (isinstance(x, str) and EMAIL.search(x))]
    return v


def selftest():
    assert github_repo("https://github.com/Foo/Bar/") == "foo/bar"
    assert github_repo("https://gitlab.com/a/b") is None
    assert github_repo("https://github.com/foo") is None
    assert github_repo("github.com/Foo/Bar.git") == "foo/bar"
    assert parse_gfi_toml("repositories = [\n  'github.com/a/b',\n  \"https://github.com/C/D\",\n  'gitlab.com/x/y',\n]") == ["a/b", "c/d"]
    ufg = "name: x\nupforgrabs:\n  name: good first issue\n  link: https://github.com/a/b/labels/good%20first%20issue\nstats:\n  name: no\n"
    assert parse_ufg_yaml(ufg) == ("a/b", "good first issue")
    assert parse_ufg_yaml("upforgrabs:\n  name: x\n  link: 'https://gitlab.com/a/b/issues'\n") is None
    assert parse_ufg_yaml("name: no block\n") is None
    assert parse_gsoc([{"source_code": "https://github.com/A/b", "ideas_link": "u"}, {"source_code": "https://github.com/org"}]) == [("a/b", "u")]
    assert strip_emails({"a": {"email": "x", "n": 1}, "b": "me@x.org", "c": ["u@v.io", "ok"]}) == {"a": {"n": 1}, "c": ["ok"]}
    log("selftest ok")


# ---------- lists ----------
def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def ufg_projects():
    with tarfile.open(fileobj=io.BytesIO(get(UFG_URL)), mode="r:gz") as tar:
        for m in tar.getmembers():
            if m.isfile() and "/_data/projects/" in m.name and m.name.endswith(".yml"):
                yield tar.extractfile(m).read().decode("utf-8", "replace")


def cmd_lists(db):
    sources = {
        "goodfirstissue_dev": lambda: [(r, None, None) for r in parse_gfi_toml(get(GFI_URL).decode())],
        "up_for_grabs": lambda: [(r, label, None) for r, label in filter(None, map(parse_ufg_yaml, ufg_projects()))],
        "gsoc_2026": lambda: [(r, None, json.dumps({"ideas_link": ideas})) for r, ideas in parse_gsoc(json.loads(get(GSOC_URL)))],
    }
    for source, load in sources.items():
        try:
            rows = load()
        except Exception as e:  # GSoC's endpoint is undocumented: log and keep the previous rows
            log(f"{source}: skipped ({e})")
            continue
        with db:
            db.execute("DELETE FROM external_lists WHERE source = ?", (source,))
            db.executemany("INSERT OR REPLACE INTO external_lists VALUES(?,?,?,?,?)", [(source, r, l, x, now()) for r, l, x in rows])
        log(f"{source}: {len(rows)} repos")


# ---------- ecosystems ----------
def fetch_eco(repo):
    def one(host):
        q = urllib.parse.quote(repo, safe="")
        # sanitize before the raw cache: the cache must not hold e-mails either
        return cached("ecosystems", f"{host}|{repo}", lambda: strip_emails(http_json(ECO.format(host=host, repo=q), headers={"User-Agent": UA})))
    return repo, one("repos"), one("issues")


def cmd_ecosystems(db, workers=4):
    done = {r[0] for r in db.execute("SELECT repo FROM repo_ecosystems")}
    todo = [r[0] for r in db.execute("SELECT repo FROM repos WHERE found = 1 ORDER BY repo") if r[0] not in done]
    log(f"{len(todo)} repos to fetch")
    with ThreadPoolExecutor(workers) as ex:
        for i, (repo, rp, iss) in enumerate(ex.map(fetch_eco, todo), 1):
            meta = (rp or {}).get("metadata") or {}
            past = {k: v for k, v in (iss or {}).items() if k.startswith("past_year") or k == "last_synced_at"}
            with db:  # a repo unknown to ecosyste.ms still gets a row, so it is not asked again
                db.execute("INSERT OR REPLACE INTO repo_ecosystems VALUES(?,?,?,?,?)",
                           (repo, json.dumps(meta.get("funding")), json.dumps(meta.get("files")), json.dumps(past) if iss else None, now()))
            if i % 100 == 0:
                log(f"  {i}/{len(todo)}")


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "selftest":
        return selftest()
    if cmd not in ("lists", "ecosystems"):
        sys.exit(__doc__)
    db = sqlite3.connect(DB, timeout=60)
    db.executescript(SCHEMA)
    {"lists": cmd_lists, "ecosystems": cmd_ecosystems}[cmd](db)


if __name__ == "__main__":
    main()
