#!/usr/bin/env python3
"""Gera os dados do site a partir do banco (contrato em docs/arquitetura.md).

  python pipeline/build.py   ->  web/public/data/projects.json e web/public/data/skills.json

Campos ainda não calculados saem com valor neutro e são preenchidos pelas tarefas:
skills (D2), profile/openness (D3), needs (D5), ai_policy (K2).
"""
import json
import re
import sqlite3
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "ecosystem.db"
OUT = ROOT / "web" / "public" / "data"
YEAR_FIELDS = ["prs_opened", "prs_merged", "issues_opened", "issues_closed", "commits", "direct_commits", "people"]


def months_ago(n):
    now = datetime.now(timezone.utc)
    y, m = divmod(now.year * 12 + now.month - 1 - n, 12)
    return f"{y}-{m + 1:02d}"


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def table_exists(db, name):
    return db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (name,)).fetchone() is not None


def main():
    db = sqlite3.connect(DB, timeout=60)
    db.row_factory = sqlite3.Row
    cut24 = months_ago(24)

    tags = defaultdict(list)
    for r in db.execute("SELECT repo, tag FROM repo_tags ORDER BY tag"):
        tags[r["repo"]].append(r["tag"])
    dependents = dict(db.execute("SELECT repo, MAX(dependents) FROM packages WHERE repo IS NOT NULL GROUP BY repo"))
    scorecard = dict(db.execute("SELECT repo, overall FROM repo_scorecard")) if table_exists(db, "repo_scorecard") else {}
    newcomer = dict(db.execute("SELECT repo, newcomer_open FROM repo_labels")) if table_exists(db, "repo_labels") else {}
    sample = {r["repo"]: r for r in db.execute("SELECT * FROM repo_sample")} if table_exists(db, "repo_sample") else {}
    commit_since = dict(db.execute("SELECT repo, since FROM commit_coverage")) if table_exists(db, "commit_coverage") else {}
    maint = dict(db.execute(
        "SELECT repo, COUNT(DISTINCT login) FROM participation WHERE is_bot = 0 AND month >= ? "
        "AND role IN ('pr_merger', 'direct_committer') GROUP BY repo", (cut24,)))

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

    projects, languages = [], set()
    for r in db.execute("SELECT * FROM repos WHERE found = 1 AND (archived = 0 OR archived IS NULL) ORDER BY repo"):
        repo = r["repo"]
        large = r["collection_mode"] == "contagem+amostra"
        smp = sample.get(repo)
        if large:  # pessoas e commits diretos não existem para os grandes; abertura e mergers vêm da amostra
            for v in years[repo].values():
                v.update(people=None, direct_commits=None)
        since = max(filter(None, [r["activity_since"] or "2018-01", commit_since.get(repo)]))
        if r["language"]:
            languages.add(r["language"])
        projects.append({
            "repo": repo,
            "url": f"https://github.com/{repo}",
            "tags": tags.get(repo, []),
            "description": r["description"],
            "language": r["language"],
            "license": r["license"],
            "stars": r["stars"] or 0,
            "dependents": dependents.get(repo),
            "profile": "precisa_de_maos",  # D3
            "needs": [],                    # D5
            "skills": [],                   # D2
            "openness": round(smp["outsider_prs"] / smp["human_prs"], 2) if large and smp and smp["human_prs"] >= 5 else None,  # D3: completos
            "maintainers_24m": (smp["mergers"] if smp else 0) if large else maint.get(repo, 0),
            "newcomer_open": newcomer.get(repo) or 0,
            "scorecard": scorecard.get(repo),
            "ai_policy": {"classification": "unknown", "evidence": "", "source_file": ""},  # K2
            "collection": "contagem+amostra" if large else "completo",
            "coverage_since": since,
            # anos anteriores ao início da cobertura ficam de fora para não parecerem "zero atividade"
            "years": {y: v for y, v in sorted(years[repo].items()) if y >= since[:4]},
        })

    skills = [{"id": slug(l), "label": l, "kind": "linguagem"} for l in sorted(languages)]  # D1 amplia
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "projects.json").write_text(json.dumps(projects, ensure_ascii=False, separators=(",", ":")))
    (OUT / "skills.json").write_text(json.dumps(skills, ensure_ascii=False, indent=1))
    size = (OUT / "projects.json").stat().st_size / 1e6
    print(f"{len(projects)} projetos ({size:.1f} MB), {len(skills)} habilidades -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
