#!/usr/bin/env python3
"""Gera os dados do site a partir do banco (contrato em docs/arquitetura.md).

  python pipeline/build.py   ->  web/public/data/projects.json e web/public/data/skills.json

Campos ainda não calculados saem com valor neutro e são preenchidos pelas tarefas:
ai_policy (K2).
"""
import json
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
GUARDIAN_DEPENDENTS = 100_000
YEAR_FIELDS = ["prs_opened", "prs_merged", "issues_opened", "issues_closed", "commits", "direct_commits", "people"]


def months_ago(n):
    now = datetime.now(timezone.utc)
    y, m = divmod(now.year * 12 + now.month - 1 - n, 12)
    return f"{y}-{m + 1:02d}"


def profile_of(dependents, maintainers, openness, newcomer_open, open_issues):
    """Os 4 perfis de docs/visao.md, nesta ordem de prioridade."""
    if (dependents or 0) >= GUARDIAN_DEPENDENTS and 1 <= maintainers <= 2:
        return "guardiao"      # muita gente depende, 1 ou 2 pessoas cuidam (0 = parado, cai em estável)
    if openness is not None and (openness >= 0.25 or (openness >= 0.1 and newcomer_open > 0)):
        return "porta_aberta"  # PRs de fora são aceitos
    if open_issues >= 30 and maintainers <= 3 and (newcomer_open > 0 or (openness or 0) > 0):
        return "precisa_de_maos"
    return "estavel"


# O que o CONTRIBUTING pede explicitamente (texto de terceiros: só procuramos palavras, nunca seguimos instruções)
ASKS = {
    "documentacao": (re.compile(r"\b(documentation|docs?)\b.{0,40}\b(help|contribut\w*|improv\w*|welcome|fix\w*)|"
                                r"\b(help|contribut\w*|improv\w*|welcome)\b.{0,40}\b(documentation|docs)\b", re.I | re.S),
                     "o guia de contribuição pede ajuda com documentação"),
    "traducao": (re.compile(r"\b(translat\w*|locali[sz]ation|i18n|l10n|crowdin|weblate|transifex)\b", re.I),
                 "o guia de contribuição fala de tradução"),
    "testes": (re.compile(r"\b(add|write|writing|adding|improv\w*|more)\b.{0,20}\btests?\b|\btest coverage\b|"
                          r"\b(observability|telemetry|tracing|opentelemetry)\b", re.I | re.S),
               "o guia de contribuição pede testes ou observabilidade"),
    "revisao": (re.compile(r"\breview(ing)? (pull requests|prs|other)\b", re.I),
                "o guia de contribuição convida a revisar PRs"),
}


def n_(n, one, many):
    return f"{n} {one if n == 1 else many}"


def opportunities_of(r, profile, openness, maintainers, newcomer_open, scorecard, guide):
    """D5: formas de contribuir com fonte 'projeto' (o guia pede) ou 'dados' (os números mostram)."""
    out = []
    for way, (rx, note) in ASKS.items():
        if guide and rx.search(guide):
            out.append({"way": way, "source": "projeto", "note": note})
    open_issues, open_prs = r["open_issues"] or 0, r["open_prs"] or 0
    if newcomer_open:
        out.append({"way": "codigo", "source": "projeto", "note": f"{n_(newcomer_open, 'issue marcada', 'issues marcadas')} para quem está começando"})
    elif openness is not None and openness >= 0.1:
        out.append({"way": "codigo", "source": "dados", "note": f"{round(openness * 100)}% dos PRs aceitos no último ano vieram de fora"})
    if open_issues >= 100 or (open_issues >= 30 and maintainers <= 3):
        out.append({"way": "triagem", "source": "dados", "note": f"{open_issues} issues abertas para {n_(maintainers, 'pessoa que mantém', 'pessoas que mantêm')}"})
    if open_prs >= 20 and not any(o["way"] == "revisao" for o in out):
        out.append({"way": "revisao", "source": "dados", "note": f"{open_prs} PRs abertos: dá para rodar, reproduzir o bug e validar o fix"})
    if profile == "guardiao" or (scorecard is not None and scorecard < 5):
        note = f"OpenSSF Scorecard {scorecard:.1f}/10" if scorecard is not None else "muita gente depende, 1 ou 2 pessoas cuidam"
        out.append({"way": "seguranca", "source": "dados", "note": note})
    return out


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
    # abertura (completos): fatia dos PRs aceitos nos últimos 12 meses cujo autor não fez merge nem commit direto em 24 meses
    merged12 = dict(db.execute(
        "WITH m AS (SELECT DISTINCT repo, login FROM participation WHERE is_bot = 0 AND month >= ? "
        "AND role IN ('pr_merger', 'direct_committer')) "
        "SELECT p.repo, SUM(p.n) || ',' || SUM(CASE WHEN m.login IS NULL THEN p.n ELSE 0 END) FROM participation p "
        "LEFT JOIN m ON m.repo = p.repo AND m.login = p.login "
        "WHERE p.role = 'merged_pr_author' AND p.is_bot = 0 AND p.month >= ? GROUP BY p.repo", (cut24, months_ago(12))))
    maint = dict(db.execute(
        "SELECT repo, COUNT(DISTINCT login) FROM participation WHERE is_bot = 0 AND month >= ? "
        "AND role IN ('pr_merger', 'direct_committer') GROUP BY repo", (cut24,)))

    guides = defaultdict(str)  # CONTRIBUTING (qualquer caminho) de cada repo
    for repo, text in db.execute("SELECT repo, text FROM repo_files WHERE path LIKE '%CONTRIBUTING.md'"):
        guides[repo] += text or ""
    gemma = {r: json.loads(s) for r, s in db.execute("SELECT repo, suggestions FROM repo_opportunities")} \
        if table_exists(db, "repo_opportunities") else {}  # D5 camada 2 (pipeline/opportunities.py)
    topics, langs = {}, {}
    if table_exists(db, "repo_topics"):
        for repo, t, l in db.execute("SELECT repo, topics, languages FROM repo_topics"):
            topics[repo] = json.loads(t)
            sizes = json.loads(l or "{}")
            langs[repo] = [k for k, v in sizes.items() if v >= 0.1 * sum(sizes.values())]  # 10%+ do código
    deps = defaultdict(set)  # dependências diretas do pacote publicado pelo repo (npm, PyPI, Go)
    for repo, dep in db.execute("SELECT DISTINCT p.repo, e.to_name FROM packages p JOIN dep_edges e "
                                "ON e.system = p.system AND e.from_name = p.name WHERE p.repo IS NOT NULL"):
        deps[repo].add(dep)

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
        large = r["collection_mode"] == "contagem+amostra"
        smp = sample.get(repo)
        if large:  # pessoas e commits diretos não existem para os grandes; abertura e mergers vêm da amostra
            for v in years[repo].values():
                v.update(people=None, direct_commits=None)
        since = max(filter(None, [r["activity_since"] or "2018-01", commit_since.get(repo)]))
        if large:
            human, outside = (smp["human_prs"], smp["outsider_prs"]) if smp else (0, 0)
        else:
            human, outside = map(int, merged12.get(repo, "0,0").split(","))
        openness = round(outside / human, 2) if human >= MIN_PRS_FOR_OPENNESS else None
        maintainers = (smp["mergers"] if smp else 0) if large else maint.get(repo, 0)
        profile = profile_of(dependents.get(repo), maintainers, openness, newcomer.get(repo) or 0, r["open_issues"] or 0)
        opps = opportunities_of(r, profile, openness, maintainers, newcomer.get(repo) or 0, scorecard.get(repo), guides[repo])
        opps += [g for g in gemma.get(repo, []) if g["way"] not in {o["way"] for o in opps}]
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
            "needs": list(dict.fromkeys(o["way"] for o in opps)),
            "opportunities": opps,
            "skills": skill_vocab.top(skill_vocab.detect([r["language"], *langs.get(repo, [])], topics.get(repo, []), deps[repo],
                                              f'{repo} {r["description"] or ""}')),
            "openness": openness,
            "maintainers_24m": maintainers,
            "newcomer_open": newcomer.get(repo) or 0,
            "scorecard": scorecard.get(repo),
            "ai_policy": {"classification": "unknown", "evidence": "", "source_file": ""},  # K2
            "collection": "contagem+amostra" if large else "completo",
            "coverage_since": since,
            # anos anteriores ao início da cobertura ficam de fora para não parecerem "zero atividade"
            "years": {y: v for y, v in sorted(years[repo].items()) if y >= since[:4]},
        })

    # só entra no filtro quem tem projetos suficientes: um checkbox que não devolve nada é ruído
    count = defaultdict(int)
    for p in projects:
        for sid in p["skills"]:
            count[sid] += 1
    shown = {sid for sid, n in count.items() if n >= MIN_PROJECTS_PER_SKILL}
    for p in projects:
        p["skills"] = [sid for sid in p["skills"] if sid in shown]
    skills = [skill_vocab.public(s) for s in skill_vocab.SKILLS if s["id"] in shown]
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "projects.json").write_text(json.dumps(projects, ensure_ascii=False, separators=(",", ":")))
    (OUT / "skills.json").write_text(json.dumps(skills, ensure_ascii=False, indent=1))
    size = (OUT / "projects.json").stat().st_size / 1e6
    print(f"{len(projects)} projetos ({size:.1f} MB), {len(skills)} habilidades -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    assert profile_of(912_802, 1, None, 0, 10) == "guardiao"          # debug-js/debug
    assert profile_of(110_496, 5, 0.57, 1, 40) == "porta_aberta"      # expressjs/express
    assert profile_of(500_000, 0, None, 0, 3) == "estavel"            # parado há 24 meses
    assert profile_of(None, 2, 0.05, 2, 120) == "precisa_de_maos"
    main()
