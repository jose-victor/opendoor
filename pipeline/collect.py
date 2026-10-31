#!/usr/bin/env python3
"""Coletor do ecossistema open source (npm, PyPI e Go; escolha com --system).

Cada etapa pode ser re-executada: ela pula o que já está no banco e retoma de onde parou.

  python pipeline/collect.py graph --system npm|pypi|go  # grafo de um ecossistema
  python pipeline/collect.py graph                 # deps.dev: árvore de dependências das sementes -> seeds, packages, dep_edges
  python pipeline/collect.py repos                 # GitHub: foto atual + arquivos de política -> repos, repo_files
  python pipeline/collect.py activity [--limit N]  # GitHub: quem abriu/revisou/mergeou/fechou, por mês desde 2018
  python pipeline/collect.py commits [--limit N]   # GitHub: commits por mês e quantos entraram direto, sem PR
  python pipeline/collect.py labels                # GitHub: issues abertas marcadas para iniciantes / help wanted
  python pipeline/collect.py security              # deps.dev: OpenSSF Scorecard + alertas de vulnerabilidade
  python pipeline/collect.py apps                  # vertente 2: marca e fotografa os apps mainstream (lista APPS)
  python pipeline/collect.py large [--workers N]  # repos grandes: contagens mensais + amostra de pessoas
  python pipeline/collect.py reaggregate           # recalcula as agregações a partir do cache bruto, sem API
  python pipeline/collect.py stats                 # resumo do banco
  python pipeline/collect.py selftest              # checa a agregação mensal
"""
import argparse
import concurrent.futures as cf
import gzip
import json
import sqlite3
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # raiz do repositório
DATA = ROOT / "data"
RAW = DATA / "raw"
DB = DATA / "ecosystem.db"
SYSTEM = "npm"
SINCE = "2018-01"
MAX_PAGES = 30  # por tipo (PR/issue) e repo: até 3000 itens; acima disso o repo fica marcado como truncado
SEEDS_BY_SYSTEM = {
    "npm": [
        # backend, build, testes, CLI, banco, desktop, automação
        "express", "next", "react-dom", "vue", "@angular/core", "vite", "webpack", "eslint", "jest", "mocha",
        "axios", "socket.io", "mongoose", "pg", "nodemon", "yargs", "electron", "puppeteer", "sharp",
        "@babel/core", "typescript", "prettier", "jsonwebtoken", "dotenv", "winston",
        # web frontend
        "react-router", "@reduxjs/toolkit", "@tanstack/react-query", "tailwindcss", "@mui/material",
        "styled-components", "react-hook-form", "zod", "svelte", "astro", "@storybook/react", "framer-motion",
        # IA
        "ai", "openai", "@langchain/core", "@huggingface/transformers",
    ],
    "pypi": [
        # web
        "django", "flask", "fastapi", "requests", "httpx", "celery", "sqlalchemy", "pydantic", "scrapy",
        # dados, IA, ferramentas
        "pandas", "scikit-learn", "transformers", "langchain", "llama-index", "huggingface-hub", "openai",
        "matplotlib", "jupyterlab", "streamlit", "pytest", "poetry",
    ],
    "go": [
        "github.com/gin-gonic/gin", "github.com/gofiber/fiber/v2", "github.com/labstack/echo/v4",
        "github.com/go-chi/chi/v5", "github.com/spf13/cobra", "github.com/charmbracelet/bubbletea",
        "github.com/stretchr/testify", "gorm.io/gorm", "go.uber.org/zap", "k8s.io/client-go",
        "github.com/prometheus/client_golang", "github.com/ollama/ollama",
    ],
}
# vertente 2: apps mainstream que vivem de verdade no GitHub (issues e PRs lá). Fora: GIMP, LibreOffice,
# Blender, Firefox, Krita, Inkscape, que só têm espelho aqui e parecem abandonados se medidos pelo GitHub.
APPS = [
    "obsproject/obs-studio", "audacity/audacity", "godotengine/godot", "freecad/freecad", "musescore/musescore",
    "jellyfin/jellyfin", "home-assistant/core", "bitwarden/clients", "laurent22/joplin", "darktable-org/darktable",
    "keepassxreboot/keepassxc", "qbittorrent/qbittorrent", "flameshot-org/flameshot", "ankitects/anki", "mpv-player/mpv",
    "xbmc/xbmc", "mltframework/shotcut", "nextcloud/server", "mastodon/mastodon", "logseq/logseq",
    "appflowy-io/appflowy", "signalapp/signal-desktop", "telegramdesktop/tdesktop", "zed-industries/zed",
    "microsoft/vscode",
    # IA
    "ollama/ollama", "ggml-org/llama.cpp", "open-webui/open-webui", "comfyanonymous/comfyui",
]
POLICY_FILES = [
    "CONTRIBUTING.md", ".github/CONTRIBUTING.md", "docs/CONTRIBUTING.md", "AI_POLICY.md", ".github/AI_POLICY.md",
    "AGENTS.md", "CLAUDE.md", ".github/copilot-instructions.md", "README.md",
]

SCHEMA = """
CREATE TABLE IF NOT EXISTS repo_tags(repo TEXT, tag TEXT, PRIMARY KEY(repo, tag));
CREATE TABLE IF NOT EXISTS seeds(system TEXT, name TEXT, version TEXT, PRIMARY KEY(system, name));
CREATE TABLE IF NOT EXISTS packages(system TEXT, name TEXT, version TEXT, repo TEXT, dependents INT,
  direct_dependents INT, fetched_at TEXT, PRIMARY KEY(system, name));
CREATE TABLE IF NOT EXISTS dep_edges(system TEXT, seed TEXT, from_name TEXT, to_name TEXT,
  PRIMARY KEY(system, seed, from_name, to_name));
CREATE TABLE IF NOT EXISTS repos(repo TEXT PRIMARY KEY, found INT, description TEXT, language TEXT, license TEXT,
  created_at TEXT, pushed_at TEXT, archived INT, stars INT, forks INT, open_issues INT, total_issues INT,
  open_prs INT, total_prs INT, fetched_at TEXT,
  activity_since TEXT, activity_truncated INT, activity_fetched_at TEXT);
CREATE TABLE IF NOT EXISTS repo_files(repo TEXT, path TEXT, oid TEXT, text TEXT, fetched_at TEXT,
  PRIMARY KEY(repo, path));
CREATE TABLE IF NOT EXISTS repo_monthly(repo TEXT, month TEXT, issues_opened INT, issues_closed INT,
  issues_closed_completed INT, issues_closed_not_planned INT, prs_opened INT, prs_merged INT,
  prs_closed_unmerged INT, reviews INT, PRIMARY KEY(repo, month));
CREATE TABLE IF NOT EXISTS participation(repo TEXT, month TEXT, role TEXT, login TEXT, is_bot INT, n INT,
  PRIMARY KEY(repo, month, role, login));
"""
MONTHLY_FIELDS = ["issues_opened", "issues_closed", "issues_closed_completed", "issues_closed_not_planned",
                  "prs_opened", "prs_merged", "prs_closed_unmerged", "reviews"]


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def log(*a):
    print(*a, flush=True)


def http_json(url, data=None, headers=None, tries=6):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, data=data, headers={"User-Agent": "hacktoberfest-ecosystem", **(headers or {})})
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            if e.code in (403, 429, 500, 502, 503, 504) and i < tries - 1:
                wait = int(e.headers.get("Retry-After") or 0) or 5 * 2 ** i
                log(f"  HTTP {e.code}, esperando {wait}s: {url[:80]}")
                time.sleep(wait)
                continue
            raise
        except (urllib.error.URLError, TimeoutError):
            if i < tries - 1:
                time.sleep(2 * 2 ** i)
                continue
            raise


def cached(kind, key, fetch):
    p = RAW / kind / (urllib.parse.quote(key, safe="") + ".json")
    if p.exists():
        return json.loads(p.read_text())
    value = fetch()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value))
    return value


# ---------- deps.dev ----------
DD = "https://api.deps.dev"


def q(s):
    return urllib.parse.quote(s, safe="")


def dd_default_version(name):
    d = cached("depsdev_pkg", name, lambda: http_json(f"{DD}/v3/systems/{SYSTEM}/packages/{q(name)}"))
    vs = [v["versionKey"]["version"] for v in (d or {}).get("versions", []) if v.get("isDefault")]
    return vs[0] if vs else None


def dd(kind, name, ver, suffix="", api="v3"):
    return cached(kind, f"{name}@{ver}", lambda: http_json(
        f"{DD}/{api}/systems/{SYSTEM}/packages/{q(name)}/versions/{q(ver)}{suffix}"))


def norm_repo(project_id):
    # deps.dev usa "github.com/Owner/Name"; o resto do coletor usa "owner/name"
    if not project_id or not project_id.lower().startswith("github.com/"):
        return None
    parts = project_id.split("/")
    return f"{parts[1]}/{parts[2]}".lower() if len(parts) >= 3 else None


def requirements(name, ver):
    """Dependências declaradas (package.json / go.mod / metadados PyPI), sem resolver a árvore."""
    d = (dd("depsdev_reqs", name, ver, ":requirements", api="v3alpha") or {}).get(SYSTEM) or {}
    if SYSTEM == "go":
        return [x["name"] for x in d.get("directDependencies", [])]
    if SYSTEM == "pypi":  # extras opcionais ("extra == ...") não contam
        return [x["projectName"].lower() for x in d.get("dependencies", []) if "extra" not in x.get("environmentMarker", "")]
    return [x["name"] for x in (d.get("dependencies") or {}).get("dependencies", [])]


def requirements_graph(seed, ver, depth=2):
    """Grafo descendo `depth` níveis pelas dependências declaradas: plano B quando o deps.dev não resolve a árvore
    (Go, e pacotes npm como eslint/electron), e o caminho padrão no PyPI, onde a árvore resolvida é rasa."""
    nodes, edges, frontier = {seed: ver}, [], [(seed, ver)]
    for _ in range(depth):
        nxt = []
        for name, v in frontier:
            for dep in requirements(name, v):
                edges.append((name, dep))
                if dep not in nodes:
                    nodes[dep] = dd_default_version(dep)
                    if nodes[dep]:
                        nxt.append((dep, nodes[dep]))
        frontier = nxt
    return {n: v for n, v in nodes.items() if v}, edges


def cmd_graph(db, args):
    versions = {}
    for seed in SEEDS_BY_SYSTEM[SYSTEM]:
        ver = dd_default_version(seed)
        if not ver:
            log("sem versão no deps.dev:", seed)
            continue
        db.execute("INSERT OR REPLACE INTO seeds VALUES(?,?,?)", (SYSTEM, seed, ver))
        g = (dd("depsdev_deps", seed, ver, ":dependencies") if SYSTEM == "npm" else None) or {"nodes": [], "edges": []}
        if len(g["nodes"]) <= 1:
            found, edges = requirements_graph(seed, ver)
            for n, v in found.items():
                versions.setdefault(n, v)
            db.executemany("INSERT OR IGNORE INTO dep_edges VALUES(?,?,?,?)", [(SYSTEM, seed, a, b) for a, b in edges])
            log(f"semente {seed}@{ver}: {len(found)} pacotes (dependências declaradas, 2 níveis)")
            db.commit()
            continue
        nodes = g["nodes"]
        for n in nodes:
            versions.setdefault(n["versionKey"]["name"], n["versionKey"]["version"])
        for e in g.get("edges", []):
            db.execute("INSERT OR IGNORE INTO dep_edges VALUES(?,?,?,?)", (
                SYSTEM, seed, nodes[e["fromNode"]]["versionKey"]["name"], nodes[e["toNode"]]["versionKey"]["name"]))
        log(f"semente {seed}@{ver}: {len(nodes)} pacotes")
        db.commit()  # por semente, para não segurar o banco durante as chamadas seguintes
    db.commit()
    done = {r[0] for r in db.execute("SELECT name FROM packages WHERE system=?", (SYSTEM,))}
    todo = [(n, v) for n, v in versions.items() if n not in done]
    log(f"{len(versions)} pacotes no grafo, {len(todo)} a detalhar")

    def info(nv):
        name, ver = nv
        vi = dd("depsdev_ver", name, ver) or {}
        repo = next((p["projectKey"]["id"] for p in vi.get("relatedProjects", [])
                     if p.get("relationType") == "SOURCE_REPO"), None)
        dep = dd("depsdev_dependents", name, ver, ":dependents", api="v3alpha") or {}
        return name, ver, norm_repo(repo), dep.get("dependentCount"), dep.get("directDependentCount")

    with cf.ThreadPoolExecutor(8) as ex:
        for i, row in enumerate(ex.map(info, todo), 1):
            with db:  # grava um por vez: segurar a transação durante as chamadas ao deps.dev trava as outras etapas
                db.execute("INSERT OR REPLACE INTO packages VALUES(?,?,?,?,?,?,?)", (SYSTEM, *row, now()))
            if i % 100 == 0:
                log(f"  {i}/{len(todo)} pacotes")
    db.commit()


# ---------- GitHub ----------
_token = None


def gh(query, variables=None):
    global _token
    _token = _token or subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, check=True).stdout.strip()
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    for i in range(6):
        d = http_json("https://api.github.com/graphql", body, {"Authorization": f"bearer {_token}"})
        errs = (d or {}).get("errors") or []
        if any(e.get("type") == "RATE_LIMITED" for e in errs) or d is None:
            log(f"  GraphQL limitado, esperando {60 * (i + 1)}s")
            time.sleep(60 * (i + 1))
            continue
        rl = (d.get("data") or {}).get("rateLimit")
        if rl and rl["remaining"] < 100:
            reset = datetime.strptime(rl["resetAt"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
            wait = max(0, (reset - datetime.now(timezone.utc)).total_seconds()) + 5
            log(f"  cota GraphQL baixa ({rl['remaining']}), esperando {wait:.0f}s")
            time.sleep(wait)
        return d
    raise RuntimeError("GraphQL falhou depois de várias tentativas")


REPO_FIELDS = """nameWithOwner description primaryLanguage{name} licenseInfo{spdxId} createdAt pushedAt isArchived
 stargazerCount forkCount openIssues: issues(states:OPEN){totalCount} allIssues: issues{totalCount}
 openPRs: pullRequests(states:OPEN){totalCount} allPRs: pullRequests{totalCount}"""


def cmd_apps(db, args):
    """Vertente 2: marca os apps mainstream e tira a foto deles (depois: activity, commits, labels, security)."""
    with db:
        db.executemany("INSERT OR IGNORE INTO repo_tags VALUES(?, 'mainstream-app')", [(r,) for r in APPS])
        db.execute("INSERT OR IGNORE INTO repo_tags SELECT DISTINCT repo, system || '-graph' FROM packages WHERE repo IS NOT NULL")
    cmd_repos(db, args)


def cmd_repos(db, args):
    todo = [r[0] for r in db.execute(
        "SELECT DISTINCT x.repo FROM (SELECT repo FROM packages WHERE repo IS NOT NULL UNION SELECT repo FROM repo_tags) x "
        "LEFT JOIN repos r ON r.repo = x.repo WHERE r.repo IS NULL")]
    log(f"{len(todo)} repositórios a fotografar")
    files = " ".join(f'f{j}: object(expression:"HEAD:{path}"){{... on Blob{{oid text}}}}'
                     for j, path in enumerate(POLICY_FILES))
    for start in range(0, len(todo), 10):
        batch = todo[start:start + 10]
        parts = [f'r{i}: repository(owner:{json.dumps(r.split("/")[0])}, name:{json.dumps(r.split("/")[1])}){{{REPO_FIELDS} {files}}}'
                 for i, r in enumerate(batch)]
        d = gh("query{ rateLimit{remaining resetAt} " + " ".join(parts) + " }")
        data = d.get("data") or {}
        for i, repo in enumerate(batch):
            x = data.get(f"r{i}")
            if not x:
                db.execute("INSERT OR REPLACE INTO repos(repo, found, fetched_at) VALUES(?,0,?)", (repo, now()))
                continue
            db.execute("INSERT OR REPLACE INTO repos(repo, found, description, language, license, created_at, pushed_at, "
                       "archived, stars, forks, open_issues, total_issues, open_prs, total_prs, fetched_at) "
                       "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (
                repo, 1, x["description"], (x["primaryLanguage"] or {}).get("name"),
                (x["licenseInfo"] or {}).get("spdxId"), x["createdAt"], x["pushedAt"], int(x["isArchived"]),
                x["stargazerCount"], x["forkCount"], x["openIssues"]["totalCount"], x["allIssues"]["totalCount"],
                x["openPRs"]["totalCount"], x["allPRs"]["totalCount"], now()))
            for j, path in enumerate(POLICY_FILES):
                blob = x.get(f"f{j}")
                if blob and blob.get("text") is not None:
                    db.execute("INSERT OR REPLACE INTO repo_files VALUES(?,?,?,?,?)",
                               (repo, path, blob["oid"], blob["text"], now()))
        db.commit()
        log(f"  {min(start + 10, len(todo))}/{len(todo)} repositórios")


PERSON = "login __typename"
PR_QUERY = """query($o:String!,$n:String!,$c:String){ rateLimit{remaining resetAt} repository(owner:$o,name:$n){
 pullRequests(first:100, after:$c, orderBy:{field:CREATED_AT, direction:DESC}){ pageInfo{hasNextPage endCursor}
  nodes{ createdAt closedAt mergedAt state author{%s} mergedBy{%s}
   reviews(first:30){ nodes{ author{%s} submittedAt } }
   closeEvt: timelineItems(itemTypes:[CLOSED_EVENT], last:1){ nodes{ ... on ClosedEvent{ actor{%s} } } } } } } }""" % ((PERSON,) * 4)
ISSUE_QUERY = """query($o:String!,$n:String!,$c:String){ rateLimit{remaining resetAt} repository(owner:$o,name:$n){
 issues(first:100, after:$c, orderBy:{field:CREATED_AT, direction:DESC}){ pageInfo{hasNextPage endCursor}
  nodes{ createdAt closedAt closed stateReason author{%s}
   closeEvt: timelineItems(itemTypes:[CLOSED_EVENT], last:1){ nodes{ ... on ClosedEvent{ actor{%s} } } } } } } }""" % ((PERSON,) * 2)


def fetch_items(repo, query, key):
    owner, name = repo.split("/")
    items, cursor, truncated = [], None, False
    for page in range(MAX_PAGES):
        d = gh(query, {"o": owner, "n": name, "c": cursor})
        conn = (((d.get("data") or {}).get("repository") or {}).get(key)) or {"nodes": [], "pageInfo": {}}
        items += conn["nodes"]
        if not conn["nodes"] or conn["nodes"][-1]["createdAt"][:7] < SINCE or not conn["pageInfo"].get("hasNextPage"):
            break
        cursor = conn["pageInfo"]["endCursor"]
    else:
        truncated = True
    return items, truncated


def is_bot(actor):
    actor = actor or {}
    return actor.get("__typename") == "Bot" or (actor.get("login") or "").endswith("[bot]")


def aggregate(prs, issues, since, until):
    """Conta eventos por mês (since <= mês < until) e quem fez cada papel.

    shortcut: só itens criados a partir de `since` entram, então um PR/issue aberto antes de 2018 e
    fechado depois não é contado no fechamento; a diferença é pequena e some nos anos recentes.
    """
    monthly, part = defaultdict(Counter), Counter()

    def add(ts, field, role, actor):
        month = ts[:7] if ts else None
        if not month or not (since <= month < until):
            return
        if field:
            monthly[month][field] += 1
        login = (actor or {}).get("login") or "ghost"  # "ghost" = conta apagada
        part[(month, role, login, int(is_bot(actor)))] += 1

    for pr in prs:
        add(pr["createdAt"], "prs_opened", "pr_author", pr["author"])
        if pr["mergedAt"]:
            add(pr["mergedAt"], "prs_merged", "pr_merger", pr["mergedBy"])
            add(pr["mergedAt"], None, "merged_pr_author", pr["author"])  # de quem era o PR aceito (mede abertura)
        elif pr["state"] == "CLOSED":
            ev = pr["closeEvt"]["nodes"]
            add(pr["closedAt"], "prs_closed_unmerged", "pr_closer", ev[0]["actor"] if ev else None)
        author, seen = (pr["author"] or {}).get("login"), set()
        for r in pr["reviews"]["nodes"]:
            login = (r["author"] or {}).get("login")
            if login == author or login in seen:  # cada revisor conta 1x por PR; autor respondendo não é revisão
                continue
            seen.add(login)
            add(r["submittedAt"], "reviews", "pr_reviewer", r["author"])
    for it in issues:
        add(it["createdAt"], "issues_opened", "issue_author", it["author"])
        if it["closed"] and it["closedAt"]:
            ev = it["closeEvt"]["nodes"]
            add(it["closedAt"], "issues_closed", "issue_closer", ev[0]["actor"] if ev else None)
            reason = {"COMPLETED": "issues_closed_completed", "NOT_PLANNED": "issues_closed_not_planned"}.get(it["stateReason"])
            if reason and since <= it["closedAt"][:7] < until:
                monthly[it["closedAt"][:7]][reason] += 1
    return monthly, part


def activity_for(repo):
    prs, t1 = fetch_items(repo, PR_QUERY, "pullRequests")
    issues, t2 = fetch_items(repo, ISSUE_QUERY, "issues")
    p = RAW / "github_activity" / (repo.replace("/", "__") + ".json.gz")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(gzip.compress(json.dumps({"fetched_at": now(), "prs": prs, "issues": issues}).encode()))
    since = SINCE
    if t1 or t2:  # truncado: só vale a partir do mês seguinte ao item mais antigo que coube
        oldest = max(x[-1]["createdAt"][:7] for x, t in ((prs, t1), (issues, t2)) if t and x)
        y, m = map(int, oldest.split("-"))
        since = f"{y + m // 12}-{m % 12 + 1:02d}"
    until = datetime.now(timezone.utc).strftime("%Y-%m")  # mês corrente fica de fora: só meses fechados
    monthly, part = aggregate(prs, issues, since, until)
    return repo, since, int(t1 or t2), monthly, part, len(prs), len(issues)


def write_activity(db, repo, since, trunc, monthly, part, fetched_at):
    with db:
        db.execute("DELETE FROM repo_monthly WHERE repo=?", (repo,))
        db.execute("DELETE FROM participation WHERE repo=? AND role NOT IN (?,?)", (repo, *COMMIT_ROLES))
        db.executemany(f"INSERT INTO repo_monthly VALUES(?,?,{','.join('?' * len(MONTHLY_FIELDS))})",
                       [(repo, mo, *(c[f] for f in MONTHLY_FIELDS)) for mo, c in monthly.items()])
        db.executemany("INSERT INTO participation VALUES(?,?,?,?,?,?)",
                       [(repo, mo, role, login, bot, n) for (mo, role, login, bot), n in part.items()])
        db.execute("UPDATE repos SET activity_since=?, activity_truncated=?, activity_fetched_at=? WHERE repo=?",
                   (since, trunc, fetched_at, repo))


def cmd_reaggregate(db, args):
    """Recalcula repo_monthly e participation a partir de data/raw/github_activity, sem chamar a API."""
    rows = db.execute("SELECT repo, activity_since, activity_truncated, activity_fetched_at FROM repos "
                      "WHERE activity_fetched_at IS NOT NULL AND collection_mode IS NULL").fetchall()  # grandes: etapa large
    for repo, since, trunc, fetched_at in rows:
        raw = json.loads(gzip.decompress((RAW / "github_activity" / (repo.replace("/", "__") + ".json.gz")).read_bytes()))
        monthly, part = aggregate(raw["prs"], raw["issues"], since, raw["fetched_at"][:7])
        write_activity(db, repo, since, trunc, monthly, part, fetched_at)
    log(f"{len(rows)} repositórios recalculados")


def cmd_activity(db, args):
    # prioridade: repos de pacotes com mais dependentes (os "críticos")
    todo = [r[0] for r in db.execute(
        "SELECT r.repo FROM repos r LEFT JOIN packages p ON p.repo = r.repo WHERE r.found = 1 AND r.activity_fetched_at IS NULL "
        "GROUP BY r.repo ORDER BY MAX(COALESCE(p.dependents, 0)) DESC LIMIT ?", (args.limit,))]
    log(f"{len(todo)} repositórios para coletar atividade")
    with cf.ThreadPoolExecutor(args.workers) as ex:
        futures = [ex.submit(activity_for, r) for r in todo]
        for i, fut in enumerate(cf.as_completed(futures), 1):
            try:
                repo, since, trunc, monthly, part, n_pr, n_is = fut.result()
            except Exception as e:
                log(f"  ERRO: {e}")
                continue
            write_activity(db, repo, since, trunc, monthly, part, now())
            log(f"  [{i}/{len(todo)}] {repo}: {n_pr} PRs, {n_is} issues desde {since}{' (truncado)' if trunc else ''}")


COMMIT_ROLES = ("committer", "direct_committer")
COMMIT_QUERY = """query($o:String!,$n:String!,$c:String,$since:GitTimestamp!){ rateLimit{remaining resetAt}
 repository(owner:$o,name:$n){ defaultBranchRef{ target{ ... on Commit{
  history(first:100, after:$c, since:$since){ pageInfo{hasNextPage endCursor}
   nodes{ committedDate author{ user{login} name } associatedPullRequests(first:1){ totalCount } } } } } } } }"""


def aggregate_commits(commits, since, until):
    """Commits por mês no branch principal; "direto" = commit sem PR associado (entrou sem passar por revisão)."""
    monthly, part = defaultdict(Counter), Counter()
    for c in commits:
        month = c["committedDate"][:7]
        if not (since <= month < until):
            continue
        a = c["author"] or {}
        login = (a.get("user") or {}).get("login") or f"~{a.get('name') or 'desconhecido'}"  # "~" = sem conta no GitHub
        bot = int(login.endswith("[bot]") or (a.get("name") or "").endswith("[bot]"))
        direct = c["associatedPullRequests"]["totalCount"] == 0
        monthly[month]["commits"] += 1
        part[(month, "committer", login, bot)] += 1
        if direct:
            monthly[month]["direct_commits"] += 1
            part[(month, "direct_committer", login, bot)] += 1
    return monthly, part


def commits_for(repo):
    owner, name = repo.split("/")
    commits, cursor, truncated = [], None, False
    for page in range(MAX_PAGES):
        d = gh(COMMIT_QUERY, {"o": owner, "n": name, "c": cursor, "since": f"{SINCE}-01T00:00:00Z"})
        ref = ((d.get("data") or {}).get("repository") or {}).get("defaultBranchRef") or {}
        hist = (ref.get("target") or {}).get("history") or {"nodes": [], "pageInfo": {}}
        commits += hist["nodes"]
        if not hist["pageInfo"].get("hasNextPage"):
            break
        cursor = hist["pageInfo"]["endCursor"]
    else:
        truncated = True
    since = SINCE
    if truncated and commits:  # só vale a partir do mês seguinte ao commit mais antigo que coube
        y, m = map(int, commits[-1]["committedDate"][:7].split("-"))
        since = f"{y + m // 12}-{m % 12 + 1:02d}"
    monthly, part = aggregate_commits(commits, since, datetime.now(timezone.utc).strftime("%Y-%m"))
    return repo, since, int(truncated), monthly, part, len(commits)


def cmd_commits(db, args):
    db.executescript("""
    CREATE TABLE IF NOT EXISTS commit_monthly(repo TEXT, month TEXT, commits INT, direct_commits INT, PRIMARY KEY(repo, month));
    CREATE TABLE IF NOT EXISTS commit_coverage(repo TEXT PRIMARY KEY, since TEXT, truncated INT, fetched_at TEXT);""")
    # só repos com activity pronta: a etapa activity apaga e regrava a participation do repo
    todo = [r[0] for r in db.execute(
        "SELECT r.repo FROM repos r LEFT JOIN packages p ON p.repo = r.repo LEFT JOIN commit_coverage c ON c.repo = r.repo "
        "WHERE r.activity_fetched_at IS NOT NULL AND c.repo IS NULL "
        "GROUP BY r.repo ORDER BY MAX(COALESCE(p.dependents, 0)) DESC LIMIT ?", (args.limit,))]
    log(f"{len(todo)} repositórios para coletar commits")
    with cf.ThreadPoolExecutor(args.workers) as ex:
        futures = [ex.submit(commits_for, r) for r in todo]
        for i, fut in enumerate(cf.as_completed(futures), 1):
            try:
                repo, since, trunc, monthly, part, n = fut.result()
            except Exception as e:
                log(f"  ERRO: {e}")
                continue
            with db:
                db.execute("DELETE FROM commit_monthly WHERE repo=?", (repo,))
                db.execute("DELETE FROM participation WHERE repo=? AND role IN (?,?)", (repo, *COMMIT_ROLES))
                db.executemany("INSERT INTO commit_monthly VALUES(?,?,?,?)",
                               [(repo, mo, c["commits"], c["direct_commits"]) for mo, c in monthly.items()])
                # a mesma pessoa pode vir como usuária e como bot no mesmo mês: uma linha só por chave
                rows = {}
                for (mo, role, login, bot), k in part.items():
                    b, total = rows.get((mo, role, login), (0, 0))
                    rows[(mo, role, login)] = (max(b, bot), total + k)
                db.executemany("INSERT INTO participation VALUES(?,?,?,?,?,?)",
                               [(repo, mo, role, login, b, k) for (mo, role, login), (b, k) in rows.items()])
                db.execute("INSERT OR REPLACE INTO commit_coverage VALUES(?,?,?,?)", (repo, since, trunc, now()))
            log(f"  [{i}/{len(todo)}] {repo}: {n} commits desde {since}{' (truncado)' if trunc else ''}")


LARGE_ITEMS = 6000  # acima disso (issues + PRs no total) o repo é "grande": contagem + amostra, não cópia
OUTSIDER = {"CONTRIBUTOR", "FIRST_TIME_CONTRIBUTOR", "FIRST_TIMER", "NONE"}
FIRST_TIMER = {"FIRST_TIME_CONTRIBUTOR", "FIRST_TIMER"}
COUNT_QUERIES = {  # campo de repo_monthly -> filtro da busca
    "issues_opened": "is:issue created:{r}", "issues_closed": "is:issue closed:{r}",
    "prs_opened": "is:pr created:{r}", "prs_merged": "is:pr merged:{r}",
}
SAMPLE_QUERY = """query($q:String!,$c:String){ rateLimit{remaining resetAt}
 search(type:ISSUE, first:100, after:$c, query:$q){ pageInfo{hasNextPage endCursor}
  nodes{ ... on PullRequest{ authorAssociation author{login __typename} mergedBy{login __typename} } } } }"""


def month_range(since, until):
    y, m = map(int, since.split("-"))
    while f"{y}-{m:02d}" < until:
        nxt = (y + m // 12, m % 12 + 1)
        yield f"{y}-{m:02d}", f"{y}-{m:02d}-01", f"{nxt[0]}-{nxt[1]:02d}-01"
        y, m = nxt


def large_for(repo, created):
    owner, name = repo.split("/")
    until = datetime.now(timezone.utc).strftime("%Y-%m")
    since = max(SINCE, created[:7])
    months = list(month_range(since, until))
    counts = defaultdict(dict)
    # 1) contagens mensais pela busca: só o total, sem baixar itens (~30 contagens por chamada)
    jobs = [(mo, f, q.format(r=f"{a}..{b}")) for mo, a, b in months for f, q in COUNT_QUERIES.items()]
    for start in range(0, len(jobs), 30):
        chunk = jobs[start:start + 30]
        parts = [f'a{i}: search(type:ISSUE, first:0, query:{json.dumps(f"repo:{repo} {q}")}){{issueCount}}'
                 for i, (_, _, q) in enumerate(chunk)]
        data = gh("query{ rateLimit{remaining resetAt} " + " ".join(parts) + " }").get("data") or {}
        for i, (mo, f, _) in enumerate(chunk):
            counts[mo][f] = (data.get(f"a{i}") or {}).get("issueCount")
    # 2) commits por mês no branch principal: também só o total
    commits = {}
    for start in range(0, len(months), 36):
        chunk = months[start:start + 36]
        parts = [f'c{i}: history(since:"{a}T00:00:00Z", until:"{b}T00:00:00Z"){{totalCount}}' for i, (_, a, b) in enumerate(chunk)]
        q = (f'query{{ rateLimit{{remaining resetAt}} repository(owner:{json.dumps(owner)}, name:{json.dumps(name)}){{'
             f' defaultBranchRef{{ target{{ ... on Commit{{ {" ".join(parts)} }} }} }} }} }}')
        target = ((((gh(q).get("data") or {}).get("repository") or {}).get("defaultBranchRef") or {}).get("target") or {})
        for i, (mo, _, _) in enumerate(chunk):
            commits[mo] = (target.get(f"c{i}") or {}).get("totalCount")
    # 3) amostra de pessoas: até 300 PRs aceitos nos últimos 12 meses, com a relação do autor com o projeto
    window = list(month_range("2000-01", until))[-12][0]
    prs, cursor = [], None
    for _ in range(3):
        d = gh(SAMPLE_QUERY, {"q": f"repo:{repo} is:pr is:merged merged:>={window}-01 sort:created-desc", "c": cursor})
        s = (d.get("data") or {}).get("search") or {"nodes": [], "pageInfo": {}}
        prs += [n for n in s["nodes"] if n]
        if not s["pageInfo"].get("hasNextPage"):
            break
        cursor = s["pageInfo"]["endCursor"]
    humans = [p for p in prs if not is_bot(p.get("author"))]
    sample = (window, len(prs), len(humans), sum(p["authorAssociation"] in OUTSIDER for p in humans),
              sum(p["authorAssociation"] in FIRST_TIMER for p in humans),
              len({(p.get("mergedBy") or {}).get("login") for p in prs if p.get("mergedBy") and not is_bot(p["mergedBy"])}),
              len({(p.get("author") or {}).get("login") for p in humans}))
    return repo, since, counts, commits, sample


def cmd_large(db, args):
    """Repos grandes: contagens mensais completas (busca) + amostra de pessoas, em vez de copiar cada item."""
    db.execute("""CREATE TABLE IF NOT EXISTS repo_sample(repo TEXT PRIMARY KEY, window_start TEXT, prs INT, human_prs INT,
      outsider_prs INT, first_timer_prs INT, mergers INT, authors INT, fetched_at TEXT)""")
    todo = db.execute(
        "SELECT r.repo, r.created_at FROM repos r LEFT JOIN commit_coverage c ON c.repo = r.repo "
        "WHERE r.found = 1 AND COALESCE(r.collection_mode, '') != 'contagem+amostra' AND "
        "(r.activity_truncated = 1 OR c.truncated = 1 OR COALESCE(r.total_issues, 0) + COALESCE(r.total_prs, 0) > ?)",
        (LARGE_ITEMS,)).fetchall()
    log(f"{len(todo)} repositórios grandes")
    with cf.ThreadPoolExecutor(args.workers) as ex:
        futures = [ex.submit(large_for, r, c) for r, c in todo]
        for i, fut in enumerate(cf.as_completed(futures), 1):
            try:
                repo, since, counts, commits, sample = fut.result()
            except Exception as e:
                log(f"  ERRO: {e}")
                continue
            with db:
                # campos que só a cópia item a item dá (fechadas sem merge, revisões, commits diretos) ficam NULL
                db.execute("DELETE FROM repo_monthly WHERE repo=?", (repo,))
                db.executemany("INSERT INTO repo_monthly(repo, month, issues_opened, issues_closed, prs_opened, prs_merged) "
                               "VALUES(?,?,?,?,?,?)", [(repo, mo, c.get("issues_opened"), c.get("issues_closed"),
                                                         c.get("prs_opened"), c.get("prs_merged")) for mo, c in counts.items()])
                db.execute("DELETE FROM commit_monthly WHERE repo=?", (repo,))
                db.executemany("INSERT INTO commit_monthly VALUES(?,?,?,NULL)", [(repo, mo, n) for mo, n in commits.items()])
                db.execute("INSERT OR REPLACE INTO repo_sample VALUES(?,?,?,?,?,?,?,?,?)", (repo, *sample, now()))
                db.execute("UPDATE repos SET collection_mode='contagem+amostra', activity_since=?, activity_truncated=0, "
                           "activity_fetched_at=COALESCE(activity_fetched_at, ?) WHERE repo=?", (since, now(), repo))  # activity pula
                db.execute("INSERT OR REPLACE INTO commit_coverage VALUES(?,?,0,?)", (repo, since, now()))
            _, n, h, out, ft, mg, au = sample
            log(f"  [{i}/{len(todo)}] {repo}: {len(counts)} meses; amostra {n} PRs aceitos, "
                f"{out}/{h} de fora, {ft} estreias, {mg} fazem merge")


NEWCOMER_LABELS = '"good first issue","good-first-issue","first-timers-only","beginner","easy","help wanted"'


def cmd_labels(db, args):
    """Porta de entrada: quantas issues abertas estão marcadas para quem quer começar a contribuir."""
    db.execute("CREATE TABLE IF NOT EXISTS repo_labels(repo TEXT PRIMARY KEY, newcomer_open INT, fetched_at TEXT)")
    todo = [r[0] for r in db.execute(
        "SELECT r.repo FROM repos r LEFT JOIN repo_labels l ON l.repo = r.repo WHERE r.found = 1 AND l.repo IS NULL")]
    for start in range(0, len(todo), 20):
        batch = todo[start:start + 20]
        parts = [f'a{i}: search(type:ISSUE, first:0, query:{json.dumps(f"repo:{r} is:issue is:open label:{NEWCOMER_LABELS}")}){{issueCount}}'
                 for i, r in enumerate(batch)]
        data = gh("query{ rateLimit{remaining resetAt} " + " ".join(parts) + " }").get("data") or {}
        with db:
            db.executemany("INSERT OR REPLACE INTO repo_labels VALUES(?,?,?)",
                           [(r, (data.get(f"a{i}") or {}).get("issueCount"), now()) for i, r in enumerate(batch)])
        log(f"  {min(start + 20, len(todo))}/{len(todo)} repositórios")


def cmd_topics(db, args):
    """Topics e linguagens (com bytes) de cada repositório (D2: entram na detecção de habilidades)."""
    db.execute("CREATE TABLE IF NOT EXISTS repo_topics(repo TEXT PRIMARY KEY, topics TEXT, fetched_at TEXT)")
    if "languages" not in {r[1] for r in db.execute("PRAGMA table_info(repo_topics)")}:
        db.execute("ALTER TABLE repo_topics ADD COLUMN languages TEXT")  # {"C++": bytes, ...}
    todo = [r[0] for r in db.execute(
        "SELECT r.repo FROM repos r LEFT JOIN repo_topics t ON t.repo = r.repo "
        "WHERE r.found = 1 AND (t.repo IS NULL OR t.languages IS NULL)")]
    for start in range(0, len(todo), 50):
        batch = todo[start:start + 50]
        parts = [f'r{i}: repository(owner:{json.dumps(r.split("/")[0])}, name:{json.dumps(r.split("/")[1])})'
                 '{repositoryTopics(first:30){nodes{topic{name}}} '
                 'languages(first:10, orderBy:{field:SIZE, direction:DESC}){edges{size node{name}}}}' for i, r in enumerate(batch)]
        data = gh("query{ rateLimit{remaining resetAt} " + " ".join(parts) + " }").get("data") or {}
        with db:
            db.executemany("INSERT OR REPLACE INTO repo_topics(repo, topics, fetched_at, languages) VALUES(?,?,?,?)", [
                (r, json.dumps([n["topic"]["name"] for n in x["repositoryTopics"]["nodes"]]), now(),
                 json.dumps({e["node"]["name"]: e["size"] for e in x["languages"]["edges"]}))
                for i, r in enumerate(batch) if (x := data.get(f"r{i}"))])
        log(f"  {min(start + 50, len(todo))}/{len(todo)} repositórios")


def cmd_security(db, args):
    """deps.dev: OpenSSF Scorecard de cada repo + alertas de vulnerabilidade da versão atual de cada pacote."""
    db.executescript("""
    CREATE TABLE IF NOT EXISTS repo_scorecard(repo TEXT PRIMARY KEY, overall REAL, date TEXT, fetched_at TEXT);
    CREATE TABLE IF NOT EXISTS scorecard_checks(repo TEXT, check_name TEXT, score INT, reason TEXT,
      PRIMARY KEY(repo, check_name));
    CREATE TABLE IF NOT EXISTS package_advisories(system TEXT, name TEXT, version TEXT, advisory TEXT,
      PRIMARY KEY(system, name, version, advisory));""")
    repos = [r[0] for r in db.execute("SELECT repo FROM repos WHERE found = 1")]
    proj = lambda r: cached("depsdev_project", r, lambda: http_json(f"{DD}/v3/projects/{q('github.com/' + r)}"))
    with cf.ThreadPoolExecutor(8) as ex:
        results = list(zip(repos, ex.map(proj, repos)))
    # shortcut: alertas só da versão atual (default) de cada pacote, não o histórico; vem do cache da etapa graph
    advisories = []
    for name, ver in db.execute("SELECT name, version FROM packages WHERE system = ?", (SYSTEM,)).fetchall():
        for a in (dd("depsdev_ver", name, ver) or {}).get("advisoryKeys", []):
            advisories.append((SYSTEM, name, ver, a["id"]))
    with db:  # grava tudo de uma vez para não segurar o banco enquanto a etapa activity escreve
        for repo, p in results:
            sc = (p or {}).get("scorecard")
            if not sc:
                continue
            db.execute("INSERT OR REPLACE INTO repo_scorecard VALUES(?,?,?,?)", (repo, sc.get("overallScore"), sc.get("date"), now()))
            db.executemany("INSERT OR REPLACE INTO scorecard_checks VALUES(?,?,?,?)",
                           [(repo, c["name"], c.get("score"), c.get("reason")) for c in sc.get("checks", [])])
        db.executemany("INSERT OR IGNORE INTO package_advisories VALUES(?,?,?,?)", advisories)
    log(f"scorecard: {sum(1 for _, p in results if (p or {}).get('scorecard'))}/{len(repos)} repos; "
        f"alertas: {len(advisories)} em {len({a[1] for a in advisories})} pacotes")


def cmd_stats(db, args):
    for t in ["seeds", "packages", "dep_edges", "repos", "repo_files", "repo_monthly", "participation"]:
        log(f"{t:14} {db.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0]}")
    log("repos com atividade:", db.execute("SELECT COUNT(*) FROM repos WHERE activity_fetched_at IS NOT NULL").fetchone()[0])
    log("pacotes sem repo no GitHub:", db.execute("SELECT COUNT(*) FROM packages WHERE repo IS NULL").fetchone()[0])


def cmd_selftest(db, args):
    u = {"login": "ana", "__typename": "User"}
    b = {"login": "dependabot", "__typename": "Bot"}
    m = {"login": "rui", "__typename": "User"}
    prs = [
        {"createdAt": "2025-01-10T00:00:00Z", "closedAt": "2025-02-01T00:00:00Z", "mergedAt": "2025-02-01T00:00:00Z",
         "state": "MERGED", "author": u, "mergedBy": m,
         "reviews": {"nodes": [{"author": m, "submittedAt": "2025-01-20T00:00:00Z"},
                               {"author": m, "submittedAt": "2025-01-21T00:00:00Z"},
                               {"author": u, "submittedAt": "2025-01-22T00:00:00Z"}]},
         "closeEvt": {"nodes": [{"actor": m}]}},
        {"createdAt": "2025-01-11T00:00:00Z", "closedAt": "2025-01-12T00:00:00Z", "mergedAt": None,
         "state": "CLOSED", "author": b, "mergedBy": None, "reviews": {"nodes": []}, "closeEvt": {"nodes": [{"actor": m}]}},
        {"createdAt": "2017-12-01T00:00:00Z", "closedAt": None, "mergedAt": None, "state": "OPEN",
         "author": u, "mergedBy": None, "reviews": {"nodes": []}, "closeEvt": {"nodes": []}},
    ]
    issues = [{"createdAt": "2025-03-01T00:00:00Z", "closedAt": "2025-03-05T00:00:00Z", "closed": True,
               "stateReason": "NOT_PLANNED", "author": None, "closeEvt": {"nodes": [{"actor": m}]}}]
    monthly, part = aggregate(prs, issues, "2018-01", "2025-03")
    assert monthly["2025-01"] == Counter(prs_opened=2, reviews=1, prs_closed_unmerged=1), monthly["2025-01"]
    assert monthly["2025-02"] == Counter(prs_merged=1), monthly["2025-02"]
    assert "2025-03" not in monthly and "2017-12" not in monthly  # mês corrente e antes de 2018 ficam de fora
    assert part[("2025-01", "pr_author", "dependabot", 1)] == 1
    assert part[("2025-02", "merged_pr_author", "ana", 0)] == 1 and monthly["2025-02"]["prs_merged"] == 1
    assert part[("2025-01", "pr_reviewer", "rui", 0)] == 1 and ("2025-01", "pr_reviewer", "ana", 0) not in part
    monthly, part = aggregate([], issues, "2018-01", "2025-04")
    assert monthly["2025-03"] == Counter(issues_opened=1, issues_closed=1, issues_closed_not_planned=1)
    assert part[("2025-03", "issue_author", "ghost", 0)] == 1
    commits = [
        {"committedDate": "2025-01-05T00:00:00Z", "author": {"user": {"login": "rui"}, "name": "Rui"}, "associatedPullRequests": {"totalCount": 0}},
        {"committedDate": "2025-01-06T00:00:00Z", "author": {"user": None, "name": "Fulano"}, "associatedPullRequests": {"totalCount": 1}},
        {"committedDate": "2025-02-01T00:00:00Z", "author": {"user": {"login": "renovate[bot]"}, "name": "renovate[bot]"}, "associatedPullRequests": {"totalCount": 0}},
    ]
    monthly, part = aggregate_commits(commits, "2018-01", "2025-02")
    assert monthly["2025-01"] == Counter(commits=2, direct_commits=1) and "2025-02" not in monthly
    assert part[("2025-01", "direct_committer", "rui", 0)] == 1 and part[("2025-01", "committer", "~Fulano", 0)] == 1
    assert aggregate_commits(commits, "2018-01", "2025-03")[1][("2025-02", "direct_committer", "renovate[bot]", 1)] == 1
    assert [m[0] for m in month_range("2025-11", "2026-02")] == ["2025-11", "2025-12", "2026-01"]
    assert list(month_range("2025-12", "2026-01")) == [("2025-12", "2025-12-01", "2026-01-01")]
    log("selftest ok")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["graph", "repos", "activity", "commits", "labels", "topics", "security", "apps", "reaggregate", "large", "stats", "selftest"])
    ap.add_argument("--limit", type=int, default=300, help="activity: quantos repos (os com mais dependentes primeiro)")
    ap.add_argument("--workers", type=int, default=4, help="activity: repos em paralelo")
    ap.add_argument("--system", default="npm", choices=sorted(SEEDS_BY_SYSTEM), help="graph/security: ecossistema do deps.dev")
    args = ap.parse_args()
    global SYSTEM
    SYSTEM = args.system
    DATA.mkdir(exist_ok=True)
    db = sqlite3.connect(DB, timeout=60)
    db.executescript(SCHEMA)
    if "collection_mode" not in {r[1] for r in db.execute("PRAGMA table_info(repos)")}:
        db.execute("ALTER TABLE repos ADD COLUMN collection_mode TEXT")  # NULL = completo; 'contagem+amostra' = grande
    globals()[f"cmd_{args.cmd}"](db, args)


if __name__ == "__main__":
    sys.exit(main())
