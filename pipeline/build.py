#!/usr/bin/env python3
"""Builds the site's data from the database (contract in docs/arquitetura.md).

  python pipeline/build.py   ->  web/public/data/projects.json and web/public/data/skills.json

Run these first (cached, only what's missing): pipeline/opportunities.py (LLM suggestions),
pipeline/classify_ai_policy.py (AI policy) and pipeline/guides.py (per-project guide);
without them, those fields come out neutral.
"""
import gzip
import json
import statistics
import re
import sqlite3
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import skills as skill_vocab

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "ecosystem.db"
OUT = ROOT / "web" / "public" / "data"
MIN_PROJECTS_PER_SKILL = 5
MIN_PRS_FOR_OPENNESS = 5
MIN_ACCEPTANCE = 0.2
MIN_NEW_PEOPLE = 5  # new people who opened a PR in 12 months, for the per-person rate to count  # flask accepted 4% of outside PRs in 12 months; tornado, 30%
GUARDIAN_DEPENDENTS = 100_000
YEAR_FIELDS = ["prs_opened", "prs_merged", "issues_opened", "issues_closed", "commits", "direct_commits", "people"]


def months_ago(n):
    now = datetime.now(timezone.utc)
    y, m = divmod(now.year * 12 + now.month - 1 - n, 12)
    return f"{y}-{m + 1:02d}"


def profile_of(dependents, maintainers, openness, newcomer_open, open_issues, acceptance=None, recent_merged=None):
    """The 4 profiles from docs/vision.md, in this order of priority.

    acceptance: of the PRs outsiders opened in 12 months, the share accepted (None = fewer than 5 outside PRs).
    recent_merged: PRs accepted in the last 3 closed months (None = no data).
    """
    if (dependents or 0) >= GUARDIAN_DEPENDENTS and 1 <= maintainers <= 2:
        return "guardian"      # many depend on it, 1 or 2 people maintain it (0 = stalled, falls into stable)
    accepts = acceptance is None or acceptance >= MIN_ACCEPTANCE  # when known, an outside PR must have a real chance
    if accepts and openness is not None and (openness >= 0.25 or (openness >= 0.1 and newcomer_open > 0)):
        return "open_door"
    # needs hands: really accepts outsiders and still merges PRs (not a dead end)
    outsiders = openness >= 0.1 if openness is not None else newcomer_open > 0
    if open_issues >= 30 and 1 <= maintainers <= 3 and outsiders and accepts and (recent_merged or 0) > 0:
        return "needs_hands"
    return "stable"


# What CONTRIBUTING explicitly asks for (third-party text: we only look for words, never follow instructions)
ASKS = {
    "documentation": (re.compile(r"\b(documentation|docs?)\b.{0,40}\b(help|contribut\w*|improv\w*|welcome|fix\w*)|"
                                 r"\b(help|contribut\w*|improv\w*|welcome)\b.{0,40}\b(documentation|docs)\b", re.I | re.S),
                      "o guia de contribuição menciona documentação"),
    "translation": (re.compile(r"\b(translat\w*|locali[sz]ation|i18n|l10n|crowdin|weblate|transifex)\b", re.I),
                    "o guia de contribuição menciona tradução"),
    "tests": (re.compile(r"\b(add|write|writing|adding|improv\w*|more)\b.{0,20}\btests?\b|\btest coverage\b|"
                         r"\b(observability|telemetry|tracing|opentelemetry)\b", re.I | re.S),
              "o guia de contribuição menciona testes ou observabilidade"),
    "review": (re.compile(r"\breview(ing)? (pull requests|prs|other)\b", re.I),
               "o guia de contribuição menciona revisar PRs"),
}
# "we don't merge translations" (tdesktop), "don't send translation PRs" (Signal)
NO_TRANSLATION = re.compile(r"\b(do not|don't|not|no|never|won't)\b[^.\n]{0,120}\btranslat\w*|\btranslat\w*[^.\n]{0,40}\b(elsewhere|not accepted|are not merged)\b", re.I)


def n_(n, one, many):
    return f"{n} {one if n == 1 else many}"


def opportunities_of(r, profile, openness, maintainers, newcomer_open, scorecard, guide, recent_merged=None):
    """D5: ways to contribute with source 'project' (the guide mentions it) or 'data' (the numbers show it)."""
    out = []
    for way, (rx, note) in ASKS.items():
        if guide and rx.search(guide) and not (way == "translation" and NO_TRANSLATION.search(guide)):
            out.append({"way": way, "source": "project", "note": note})
    open_issues, open_prs = r["open_issues"] or 0, r["open_prs"] or 0
    if newcomer_open:
        out.append({"way": "code", "source": "project", "note": f"{n_(newcomer_open, 'issue aberta', 'issues abertas')} com \"good first issue\", \"help wanted\" ou parecido"})
    elif openness is not None and openness >= 0.1:
        out.append({"way": "code", "source": "data", "note": f"{round(openness * 100)}% dos PRs aceitos no último ano vieram de fora"})
    if open_issues >= 100 or (open_issues >= 30 and maintainers <= 3):
        out.append({"way": "triage", "source": "data", "note": f"{open_issues} issues abertas para {n_(maintainers, 'pessoa que mantém', 'pessoas que mantêm')}"})
    # reviewing only helps if someone merges: with no PR merged in the last 3 months, open PRs are stuck
    if open_prs >= 20 and (recent_merged or 0) > 0 and not any(o["way"] == "review" for o in out):
        out.append({"way": "review", "source": "data", "note": f"{open_prs} PRs abertos: dá para rodar, reproduzir o bug e validar o fix"})
    if profile == "guardian" or (scorecard is not None and scorecard < 5):
        note = f"OpenSSF Scorecard {scorecard:.1f}/10" if scorecard is not None else "muita gente depende, 1 ou 2 pessoas cuidam"
        out.append({"way": "security", "source": "data", "note": note})
    return out


def beginner_checks(debuts, tried, outside_recent, has_guide, review=None):
    """Beginner-ready: the data shows new people are managing to get in. All 4 must pass.

    debuts: outsiders whose 1st PR was accepted in 12 months; tried: new people who opened a PR in 12 months.
    """
    if debuts is not None:
        tried = max(tried or 0, debuts)  # whoever opened the PR before the window and debuted inside it also tried ("20 de 19")
    rate = debuts / tried if debuts is not None and tried and tried >= MIN_NEW_PEOPLE else None
    checks = [
        ("debuts", (debuts or 0) >= 2,
         f"{n_(debuts, 'pessoa teve', 'pessoas tiveram')} o 1º PR aceito no último ano" if debuts is not None
         else "sem dados de estreias (repo grande: só temos uma amostra recente de PRs)"),
        ("acceptance", rate is not None and rate >= 0.25,
         f"{debuts} de {tried} pessoas novas que abriram PR tiveram aceito" if rate is not None
         else f"poucas pessoas novas tentaram ({tried or 0}) para medir"),
        # active for newcomers: outside PRs accepted now (internal and bot merges don't count; nbformat)
        ("active", outside_recent >= 2, f"{n_(outside_recent, 'PR de gente de fora aceito', 'PRs de gente de fora aceitos')} nos últimos 3 meses"),
        # newcomers need feedback: half of outside PRs answered within 14 days and at most 25% stale
        ("response", review is not None and review["median_days"] <= 14 and review["stale_open"] <= 0.25 * review["prs"],
         (("metade dos PRs de fora tem retorno no mesmo dia" if review["median_days"] == 0 else
           f"metade dos PRs de fora tem retorno em até {review['median_days']} {'dia' if review['median_days'] == 1 else 'dias'}")
          + (f"; {review['stale_open']} de {review['prs']} estão parados há mais de 30 dias sem revisão" if review["stale_open"] else ""))
         if review is not None else "sem dados de tempo de resposta"),
        ("guide", has_guide, "tem guia de contribuição (CONTRIBUTING)" if has_guide else "não tem guia de contribuição (CONTRIBUTING)"),
    ]
    return {"ready": all(ok for _, ok, _ in checks), "checks": [{"key": k, "ok": ok, "text": t} for k, ok, t in checks]}


def review_of(path, maintainers, bots, now):
    """Feedback on outside PRs opened in 12 months, from the activity step's raw cache.

    First feedback = first review by someone else, merge or close. A PR with no feedback counts with the time
    it has waited so far. Stale = open for more than 30 days with no review.
    """
    parse = lambda t: datetime.strptime(t, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    waits, stale = [], 0
    for pr in json.load(gzip.open(path))["prs"]:
        author = pr.get("author") or {}
        login = author.get("login") or ""
        if author.get("__typename") == "Bot" or login.endswith("bot") or login in bots or login in maintainers:
            continue
        created = parse(pr["createdAt"])
        if (now - created).days > 365:
            continue
        times = [parse(r["submittedAt"]) for r in (pr.get("reviews") or {}).get("nodes", [])
                 if r.get("submittedAt") and (r.get("author") or {}).get("login") != login]
        times += [parse(t) for t in (pr.get("mergedAt"), pr.get("closedAt")) if t]
        first = min(times) if times else None
        waits.append(((first or now) - created).days)
        stale += pr["state"] == "OPEN" and first is None and (now - created).days > 30
    if len(waits) < MIN_PRS_FOR_OPENNESS:
        return None
    return {"median_days": int(statistics.median(waits)), "stale_open": stale, "prs": len(waits)}


def table_exists(db, name):
    return db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (name,)).fetchone() is not None


def main():
    db = sqlite3.connect(DB, timeout=60)
    db.row_factory = sqlite3.Row
    cut24 = months_ago(24)

    tags = defaultdict(list)
    for r in db.execute("SELECT repo, tag FROM repo_tags ORDER BY tag"):
        tags[r["repo"]].append(r["tag"])
    ai_policy = {
        r["repo"]: {
            "classification": r["classification"],
            "evidence": r["evidence"],
            "source_file": r["source_file"],
        }
        for r in db.execute("SELECT repo, classification, evidence, source_file FROM ai_policy")
    } if table_exists(db, "ai_policy") else {}
    dependents = dict(db.execute("SELECT repo, MAX(dependents) FROM packages WHERE repo IS NOT NULL GROUP BY repo"))
    scorecard = dict(db.execute("SELECT repo, overall FROM repo_scorecard")) if table_exists(db, "repo_scorecard") else {}
    newcomer = dict(db.execute("SELECT repo, newcomer_open FROM repo_labels")) if table_exists(db, "repo_labels") else {}
    sample = {r["repo"]: r for r in db.execute("SELECT * FROM repo_sample")} if table_exists(db, "repo_sample") else {}
    commit_since = dict(db.execute("SELECT repo, since FROM commit_coverage")) if table_exists(db, "commit_coverage") else {}
    # Openness: of what went into the project in the last 12 months (merged PRs + maintainers' direct commits),
    # the share that came from people who neither merge nor commit directly. Applies to every repo with participation;
    # for large ones it comes from the PR sample (no direct commits). GitHub's authorAssociation is misleading
    # (a member with private org membership shows up as CONTRIBUTOR), so it's only used without participation.
    cut12 = months_ago(12)
    bots = "'github-actions','dependabot','dependabot-preview','renovate','greenkeeper','pre-commit-ci','mergify','allcontributors','web-flow','copilot','imgbot','snyk-bot'"
    human = f"is_bot = 0 AND login NOT LIKE '%bot' AND login NOT IN ({bots})"  # bots with human-like names (antfubot, prombot) don't set is_bot
    # maintainer: merged, or made 3+ direct commits in 24 months (a third-party commit applied by hand keeps the author's name)
    maintainers_sql = (f"SELECT repo, login FROM participation WHERE {human} AND month >= ? "
                       "AND role IN ('pr_merger', 'direct_committer') GROUP BY repo, login "
                       "HAVING SUM(role = 'pr_merger') > 0 OR SUM(CASE WHEN role = 'direct_committer' THEN n ELSE 0 END) >= 3")
    merged12 = {r: (m, o) for r, m, o in db.execute(
        f"WITH m AS ({maintainers_sql}) "
        "SELECT p.repo, SUM(p.n), SUM(CASE WHEN m.login IS NULL THEN p.n ELSE 0 END) FROM participation p "
        "LEFT JOIN m ON m.repo = p.repo AND m.login = p.login "
        f"WHERE p.role = 'merged_pr_author' AND p.is_bot = 0 AND p.login NOT LIKE '%bot' AND p.login NOT IN ({bots}) AND p.month >= ? GROUP BY p.repo",
        (cut24, cut12))}
    direct12 = dict(db.execute(f"SELECT repo, SUM(n) FROM participation WHERE role = 'direct_committer' AND {human} "
                               "AND month >= ? GROUP BY repo", (cut12,)))
    maint = dict(db.execute(f"SELECT repo, COUNT(*) FROM ({maintainers_sql}) GROUP BY repo", (cut24,)))
    # Acceptance rate: of the PRs outsiders opened in 12 months, how many were accepted (needs 5+ outside PRs).
    acceptance = {r: round(min(1, m / a), 2) for r, a, m in db.execute(
        f"WITH m AS ({maintainers_sql}) SELECT p.repo, SUM(CASE WHEN p.role = 'pr_author' THEN p.n ELSE 0 END), "
        "SUM(CASE WHEN p.role = 'merged_pr_author' THEN p.n ELSE 0 END) FROM participation p "
        "LEFT JOIN m ON m.repo = p.repo AND m.login = p.login WHERE m.login IS NULL AND p.is_bot = 0 "
        f"AND p.login NOT LIKE '%bot' AND p.login NOT IN ({bots}) AND p.month >= ? AND p.role IN ('pr_author', 'merged_pr_author') GROUP BY p.repo",
        (cut24, cut12)) if a >= MIN_PRS_FOR_OPENNESS}
    # Debuts: outsiders whose first accepted PR (in the collected history) was in the last 12 months.
    # Newcomer acceptance, per person: of the outsiders who opened a PR in 12 months and never had one
    # accepted before, how many did (= debuts). A long-time contributor without merge rights (kleisauke on
    # sharp-libvips, 29 of 29) doesn't count: for newcomers, the question is "can new people get in?".
    tried_new = dict(db.execute(
        f"WITH m AS ({maintainers_sql}), f AS (SELECT repo, login, MIN(month) first FROM participation "
        f"WHERE role = 'merged_pr_author' AND {human} GROUP BY repo, login) "
        f"SELECT p.repo, COUNT(DISTINCT p.login) FROM participation p LEFT JOIN m ON m.repo = p.repo AND m.login = p.login "
        "LEFT JOIN f ON f.repo = p.repo AND f.login = p.login "
        f"WHERE p.role = 'pr_author' AND p.{human.replace(' AND login', ' AND p.login')} AND p.month >= ? AND m.login IS NULL "
        "AND (f.first IS NULL OR f.first >= ?) GROUP BY p.repo", (cut24, cut12, cut12)))
    debuts = dict(db.execute(
        f"WITH m AS ({maintainers_sql}), f AS (SELECT repo, login, MIN(month) first FROM participation "
        f"WHERE role = 'merged_pr_author' AND {human} GROUP BY repo, login) "
        "SELECT f.repo, COUNT(*) FROM f LEFT JOIN m ON m.repo = f.repo AND m.login = f.login "
        "WHERE m.login IS NULL AND f.first >= ? GROUP BY f.repo", (cut24, cut12)))
    # For large repos, participation only comes from the recent sample; if it covers less than 12 months, the sample wins.
    part_from = dict(db.execute("SELECT repo, MIN(month) FROM participation WHERE role = 'merged_pr_author' GROUP BY repo"))
    # Repos that changed owner appear twice (facebook/react and react/react): keep the one with more collected months.
    # shortcut: old names GitHub redirects (checked by hand); with equal data, the current name wins.
    # Better: store the nameWithOwner returned by the API in the repos step.
    old_names = {"facebook/react", "facebook/jest", "dcodeio/protobuf.js"}
    keep = {}
    for repo, key, n in db.execute("SELECT r.repo, r.created_at || '|' || r.stars, COUNT(m.month) FROM repos r "
                                   "LEFT JOIN repo_monthly m ON m.repo = r.repo WHERE r.found = 1 GROUP BY r.repo"):
        if key not in keep or n > keep[key][1] or (n == keep[key][1] and keep[key][0] in old_names):
            keep[key] = (repo, n)
    canonical = {repo for repo, _ in keep.values()}

    guides = defaultdict(str)  # each repo's CONTRIBUTING (any path)
    for repo, text in db.execute("SELECT repo, text FROM repo_files WHERE path LIKE '%CONTRIBUTING.md'"):
        guides[repo] += text or ""
    ai_opps = {r: json.loads(s) for r, s in db.execute("SELECT repo, suggestions FROM repo_opportunities")} \
        if table_exists(db, "repo_opportunities") else {}  # D5 layer 2 (pipeline/opportunities.py)
    guide_of = {r: json.loads(g) for r, g in db.execute("SELECT repo, guide FROM project_guides")} \
        if table_exists(db, "project_guides") else {}  # G1 (pipeline/guides.py)
    topics, langs = {}, {}
    if table_exists(db, "repo_topics"):
        for repo, t, l in db.execute("SELECT repo, topics, languages FROM repo_topics"):
            topics[repo] = json.loads(t)
            sizes = json.loads(l or "{}")
            langs[repo] = [k for k, v in sizes.items() if v >= 0.1 * sum(sizes.values())]  # 10%+ of the code
    deps = defaultdict(set)  # direct dependencies of the package the repo publishes (npm, PyPI, Go)
    for repo, dep in db.execute("SELECT DISTINCT p.repo, e.to_name FROM packages p JOIN dep_edges e "
                                "ON e.system = p.system AND e.from_name = p.name WHERE p.repo IS NOT NULL"):
        deps[repo].add(dep)

    # Recent activity: the last 3 closed months (data is monthly; the current month is left out).
    last = db.execute("SELECT MAX(month) FROM repo_monthly").fetchone()[0]
    recent_from = months_ago(3) if last is None else f"{int(last[:4]) - (int(last[5:]) <= 2)}-{(int(last[5:]) - 3) % 12 + 1:02d}"
    recent = {r[0]: dict(since=recent_from, until=last, issues_opened=r[1], issues_closed=r[2], prs_opened=r[3], prs_merged=r[4])
              for r in db.execute("SELECT repo, SUM(issues_opened), SUM(issues_closed), SUM(prs_opened), SUM(prs_merged) "
                                  "FROM repo_monthly WHERE month >= ? GROUP BY repo", (recent_from,))}

    outside_recent = dict(db.execute(
        f"WITH m AS ({maintainers_sql}) SELECT p.repo, SUM(p.n) FROM participation p "
        "LEFT JOIN m ON m.repo = p.repo AND m.login = p.login WHERE p.role = 'merged_pr_author' AND m.login IS NULL "
        f"AND p.{human.replace(' AND login', ' AND p.login')} AND p.month >= ? GROUP BY p.repo", (cut24, recent_from)))

    # Time to first feedback on outside PRs (only repos with the activity raw cache).
    maintainer_sets = defaultdict(set)
    for repo, login in db.execute(maintainers_sql, (cut24,)):
        maintainer_sets[repo].add(login)
    raw = Path(DB).parent / "raw" / "github_activity"
    known_bots = {b.strip("'") for b in bots.split(",")}
    reviews = {}
    for path in raw.glob("*.json.gz"):
        repo = path.name[:-len(".json.gz")].replace("__", "/", 1).lower()
        reviews[repo] = review_of(path, maintainer_sets[repo], known_bots, datetime.now(timezone.utc))

    years = defaultdict(lambda: defaultdict(lambda: dict.fromkeys(YEAR_FIELDS, 0)))
    for r in db.execute("SELECT repo, substr(month, 1, 4) y, SUM(prs_opened) po, SUM(prs_merged) pm, "
                        "SUM(issues_opened) io, SUM(issues_closed) ic FROM repo_monthly GROUP BY repo, y"):
        years[r["repo"]][r["y"]].update(prs_opened=r["po"], prs_merged=r["pm"], issues_opened=r["io"], issues_closed=r["ic"])
    if table_exists(db, "commit_monthly"):
        for r in db.execute("SELECT repo, substr(month, 1, 4) y, SUM(commits) c, SUM(direct_commits) d "
                            "FROM commit_monthly GROUP BY repo, y"):
            years[r["repo"]][r["y"]].update(commits=r["c"], direct_commits=r["d"])
    for r in db.execute("SELECT repo, substr(month, 1, 4) y, COUNT(DISTINCT login) n FROM participation "
                        "WHERE is_bot = 0 GROUP BY repo, y"):
        years[r["repo"]][r["y"]]["people"] = r["n"]

    projects = []
    for r in db.execute("SELECT * FROM repos WHERE found = 1 AND (archived = 0 OR archived IS NULL) ORDER BY repo"):
        repo = r["repo"]
        if repo not in canonical:
            continue
        large = r["collection_mode"] == "sampled"
        smp = sample.get(repo)
        if large:  # people and direct commits don't exist for large repos; openness and mergers come from the sample
            for v in years[repo].values():
                v.update(people=None, direct_commits=None)
        since = max(filter(None, [r["activity_since"] or "2018-01", commit_since.get(repo)]))
        partial = large and (part_from.get(repo) or "9999") > cut12  # sample covering less than 12 months
        if repo in merged12 and not large and repo not in commit_since:
            total, outside = 0, 0  # without direct commits, openness would be inflated (csstree: 100% vs ~33% real)
        elif repo in merged12 and not partial:
            merged, outside = merged12[repo]
            total = merged + (direct12.get(repo) or 0)
        elif large and smp and smp["outsider_prs"] < 0.95 * smp["human_prs"]:
            # shortcut: authorAssociation says CONTRIBUTOR for members with private membership; 95%+ "outside" is that
            # symptom (Tailwind) and becomes "no data". Better: collect the sample's mergedBy into participation.
            total, outside = smp["human_prs"], smp["outsider_prs"]
        else:
            total, outside = 0, 0
        openness = round(outside / total, 2) if total >= MIN_PRS_FOR_OPENNESS else None
        maintainers = (smp["mergers"] if smp else 0) if partial else (maint.get(repo) or ((smp["mergers"] if smp else 0) if large else 0))
        acc = None if partial else acceptance.get(repo)
        rec = recent.get(repo)
        rec_merged = rec["prs_merged"] if rec else 0
        profile = profile_of(dependents.get(repo), maintainers, openness, newcomer.get(repo) or 0, r["open_issues"] or 0,
                             acc, rec_merged)
        deb = None if large else debuts.get(repo, 0)
        review = reviews.get(repo)
        beginner = beginner_checks(deb, tried_new.get(repo, 0), outside_recent.get(repo) or 0, bool(guides.get(repo)), review)
        if profile == "guardian":
            beginner["ready"] = False  # critical and maintained by 1 or 2 people: not a place to learn
        if profile == "open_door" and deb == 0:
            profile = "stable"  # nobody new got in for 12 months: not an open door for newcomers (sharp-libvips)
        if beginner["ready"] and profile == "stable":
            profile = "open_door"  # postcss: low openness (many maintainer commits), but welcomes newcomers well
        opps = opportunities_of(r, profile, openness, maintainers, newcomer.get(repo) or 0, scorecard.get(repo), guides[repo],
                                rec_merged)
        if beginner["ready"] and not any(o["way"] == "code" for o in opps):
            opps.append({"way": "code", "source": "data", "note": f"{n_(deb, 'pessoa teve', 'pessoas tiveram')} o 1º PR aceito aqui no último ano"})
        facts = list(dict.fromkeys(o["way"] for o in opps))  # needs: only what the guide mentions or the numbers show
        opps += [{**g, "source": "gemini"} for g in ai_opps.get(repo, []) if g["way"] not in facts]  # the DB cache stores the old source
        projects.append({
            "repo": repo,
            "url": f"https://github.com/{repo}",
            "tags": tags.get(repo, []),
            "description": r["description"],
            "language": r["language"],
            "license": r["license"],
            "stars": r["stars"] or 0,
            "dependents": dependents.get(repo),
            "profile": profile,
            "needs": facts,
            "opportunities": opps,
            "guide": guide_of.get(repo),
            "skills": skill_vocab.top(skill_vocab.detect([r["language"], *langs.get(repo, [])], topics.get(repo, []), deps[repo],
                                              f'{repo} {r["description"] or ""}')),
            "openness": openness,
            "acceptance": acc,
            "debuts_12m": None if large else debuts.get(repo, 0),
            "beginner": beginner,
            "review": review,
            "recent": recent.get(repo),
            "maintainers_24m": maintainers,
            "newcomer_open": newcomer.get(repo) or 0,
            "scorecard": scorecard.get(repo),
            "ai_policy": ai_policy.get(repo, {"classification": "unknown", "evidence": "", "source_file": ""}),
            "collection": "sampled" if large else "full",
            "coverage_since": since,
            # years before coverage starts are left out so they don't look like "zero activity"
            "years": {y: v for y, v in sorted(years[repo].items()) if y >= since[:4]},
        })

    # only skills with enough projects go into the filter: a checkbox that returns nothing is noise
    count = defaultdict(int)
    for p in projects:
        for sid in p["skills"]:
            count[sid] += 1
    shown = {sid for sid, n in count.items() if n >= MIN_PROJECTS_PER_SKILL}
    for p in projects:
        p["skills"] = [sid for sid in p["skills"] if sid in shown]
    skills = [skill_vocab.public(s) for s in skill_vocab.SKILLS if s["id"] in shown]
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "projects.json").write_text(
        json.dumps(projects, ensure_ascii=False, separators=(",", ":")), encoding="utf-8"
    )
    (OUT / "skills.json").write_text(
        json.dumps(skills, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    size = (OUT / "projects.json").stat().st_size / 1e6
    print(f"{len(projects)} projects ({size:.1f} MB), {len(skills)} skills -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    assert profile_of(912_802, 1, None, 0, 10) == "guardian"          # debug-js/debug
    assert profile_of(110_496, 5, 0.57, 1, 40) == "open_door"         # expressjs/express
    assert profile_of(500_000, 0, None, 0, 3) == "stable"             # stalled for 24 months
    assert profile_of(None, 2, 0.15, 0, 120, 0.3, 4) == "needs_hands"
    assert profile_of(None, 2, 0.15, 0, 120, 0.3, 0) == "stable"            # no PR merged in 3 months: dead end
    assert profile_of(None, 5, 0.42, 3, 300, 0.04, 20) == "stable"          # flask: 4% of outside PRs accepted
    assert profile_of(None, 1, 0.04, 0, 900) == "stable"              # open-webui: almost nothing from outside gets in
    ok_review = {"median_days": 3, "stale_open": 2, "prs": 50}
    assert beginner_checks(13, 30, 9, True, ok_review)["ready"]           # 13 of 30 new people got in
    assert not beginner_checks(13, 30, 9, True, {"median_days": 24, "stale_open": 41, "prs": 107})["ready"]  # sqlparse
    assert not beginner_checks(13, 30, 1, True, ok_review)["ready"]                  # only 1 outside PR accepted in 3 months (nbformat)
    assert "20 de 20" in beginner_checks(20, 19, 9, True, ok_review)["checks"][1]["text"]  # never "20 de 19"
    assert not beginner_checks(None, 30, 40, True)["ready"]               # large repo: no debut data
    assert not beginner_checks(6, 150, 20, True)["ready"]                 # 6 of 150: 4%
    assert not beginner_checks(0, 1, 30, True)["ready"]                   # sharp-libvips: 0 of 1
    main()
