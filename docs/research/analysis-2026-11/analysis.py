#!/usr/bin/env python3
"""Analysis for issue #107. Stdlib only. Reads the DB read-only and web/public/data/projects.json.
Prints markdown tables (every number in the report comes from here).

  python3 analysis.py /home/jose/Documentos/Projetos/hacktoberfest-t5 > out.md
"""
import json
import random
import sqlite3
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(sys.argv[1])
# as_of labels of repo_signals: the collection window and the backtest window (pass them if the labels change)
NOW, TT = (sys.argv[2], sys.argv[3]) if len(sys.argv) > 3 else ("2026-09", "2025-09")
DB = (ROOT / "data" / "ecosystem.db").resolve()
db = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
RAW = DB.parent / "raw" / "github_activity"
projects = {p["repo"]: p for p in json.load(open(ROOT / "web/public/data/projects.json"))}
raw_files = {p.name[:-len(".json.gz")].replace("__", "/", 1).lower() for p in RAW.glob("*.json.gz")}
repos = {r[0]: dict(mode=r[1], trunc=r[2], open_issues=r[3], open_prs=r[4]) for r in db.execute(
    "SELECT repo, collection_mode, activity_truncated, open_issues, open_prs FROM repos")}

SIG = ["conversion", "first_insider_response_days", "no_insider_response_share", "outsider_insider_gap",
       "reviewer_diversity", "active_maintainers", "demand_per_maintainer"]
MIN = {"conversion": 5, "first_insider_response_days": 10, "no_insider_response_share": 10, "outsider_insider_gap": 10,
       "reviewer_diversity": 10, "active_maintainers": 1, "demand_per_maintainer": 1}
S = defaultdict(dict)  # S[as_of][(repo, signal)] = (value, n)
for repo, sig, as_of, v, n in db.execute("SELECT repo, signal, as_of, value, n FROM repo_signals"):
    S[as_of][(repo, sig)] = (v, n)


def sv(repo, sig, as_of=NOW):
    return S[as_of].get((repo, sig), (None, None))[0]


def sn(repo, sig, as_of=NOW):
    return S[as_of].get((repo, sig), (None, None))[1]


# ---------- stats helpers ----------
def ranks(xs):
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0] * len(xs)
    i = 0
    while i < len(xs):
        j = i
        while j + 1 < len(xs) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        for k in range(i, j + 1):
            r[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return r


def pearson(a, b):
    ma, mb = statistics.fmean(a), statistics.fmean(b)
    num = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    den = (sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b)) ** 0.5
    return num / den if den else float("nan")


def spearman(a, b):
    return pearson(ranks(a), ranks(b))


assert ranks([10, 20, 20, 30]) == [1, 2.5, 2.5, 4]
assert abs(spearman([1, 2, 3, 4], [10, 20, 30, 40]) - 1) < 1e-9 and abs(spearman([1, 2, 3], [3, 2, 1]) + 1) < 1e-9


def boot_ci(a, b, reps=1000, seed=107):
    rnd = random.Random(seed)
    out = []
    idx = range(len(a))
    for _ in range(reps):
        s = [rnd.choice(idx) for _ in idx]
        x, y = [a[i] for i in s], [b[i] for i in s]
        if len(set(x)) > 1 and len(set(y)) > 1:
            out.append(spearman(x, y))
    out.sort()
    return out[int(0.025 * len(out))], out[int(0.975 * len(out)) - 1]


def pairs(keys, fa, fb):
    a, b = [], []
    for k in keys:
        x, y = fa(k), fb(k)
        if x is not None and y is not None:
            a.append(float(x)); b.append(float(y))
    return a, b


def q(vals, ps=(0.1, 0.25, 0.5, 0.75, 0.9)):
    v = sorted(vals)
    def at(p):
        pos = p * (len(v) - 1)
        lo = int(pos)
        return v[lo] + (v[min(lo + 1, len(v) - 1)] - v[lo]) * (pos - lo)
    return [at(p) for p in ps]


def f(x, d=2):
    if x is None:
        return "-"
    if isinstance(x, float):
        return f"{x:.{d}f}"
    return str(x)


def table(head, rows):
    print("| " + " | ".join(head) + " |")
    print("|" + "---|" * len(head))
    for r in rows:
        print("| " + " | ".join(f(c) for c in r) + " |")
    print()


# ---------- today's numbers from projects.json ----------
def today(repo, key):
    p = projects[repo]
    if key == "review_median_days":
        return p["review"]["median_days"] if p["review"] else None
    if key == "review_stale_share":
        return round(p["review"]["stale_open"] / p["review"]["prs"], 3) if p["review"] else None
    if key == "ready":
        return int(p["beginner"]["ready"])
    if key == "debuts_12m":
        return p["debuts_12m"]
    return p[key]


TODAY = ["openness", "acceptance", "debuts_12m", "review_median_days", "review_stale_share", "maintainers_24m",
         "newcomer_open", "ready"]
P = sorted(projects)

# ================= 1. Coverage =================
print("## 1. Coverage\n")
print(f"projects.json: {len(P)} projects; repo_signals repos: {len({r for r, _ in S[NOW]})}; "
      f"non-canonical repos in repo_signals but not in projects.json: "
      f"{len({r for r, _ in S[NOW]} - set(P))}\n")


def stage(repo):
    r = repos[repo]
    if r["mode"] == "sampled":
        return "sampled (large)"
    if r["trunc"]:
        return "truncated"
    if repo not in raw_files:
        return "full, no raw activity file"
    if (repo, "conversion") not in S[NOW]:
        return "full, raw file, not computed"
    return "computed"


st = Counter(stage(r) for r in P)
table(["Stage", "Projects"], sorted(st.items(), key=lambda x: -x[1]))

# what are the "no raw file" ones?
noraw = [r for r in P if stage(r) == "full, no raw activity file"]
last12 = dict(db.execute("SELECT repo, SUM(prs_opened) FROM repo_monthly WHERE month >= '2025-10' GROUP BY repo"))
all_prs = dict(db.execute("SELECT repo, SUM(prs_opened) FROM repo_monthly GROUP BY repo"))
print("No raw file, PRs opened (repo_monthly):")
table(["Group", "Projects"], [
    ["0 PRs ever since 2018", sum(1 for r in noraw if not all_prs.get(r))],
    ["PRs ever but 0 in last 12 months", sum(1 for r in noraw if all_prs.get(r) and not last12.get(r))],
    ["1+ PRs in last 12 months", sum(1 for r in noraw if last12.get(r))],
])
print("No raw file, by profile:", dict(Counter(projects[r]["profile"] for r in noraw)), "\n")

rows = []
comp = [r for r in P if stage(r) == "computed"]
for s in SIG:
    n0 = sum(1 for r in comp if sn(r, s) == 0)
    low = sum(1 for r in comp if sv(r, s) is None and (sn(r, s) or 0) > 0)
    has = sum(1 for r in comp if sv(r, s) is not None)
    has25 = sum(1 for r in comp if sv(r, s, TT) is not None)
    rows.append([s, MIN[s], len(comp), n0, low, has, f"{has / len(P):.1%}", has25])
print("Per signal at 2026-09 among the computed projects (denominator for % = all 958 projects):")
table(["Signal", "min n", "computed", "n = 0", "0 < n < min", "has value", "% of 958", "has value @2025-09"], rows)

# who drops from the response signals (no outside PRs)
print("Computed projects by outside PRs in 12 months (n of first_insider_response_days) and profile:")
bands = [("0", lambda n: n == 0), ("1-9", lambda n: 1 <= n <= 9), ("10-29", lambda n: 10 <= n <= 29),
         ("30-99", lambda n: 30 <= n <= 99), ("100+", lambda n: n >= 100)]
rows = []
for name, fn in bands:
    g = [r for r in comp if fn(sn(r, "first_insider_response_days") or 0)]
    c = Counter(projects[r]["profile"] for r in g)
    rows.append([name, len(g), c["open_door"], c["stable"], c["guardian"], c["needs_hands"],
                 sum(projects[r]["beginner"]["ready"] for r in g),
                 sum(1 for r in g if sv(r, "conversion") is not None)])
table(["outside PRs 12m", "projects", "open_door", "stable", "guardian", "needs_hands", "ready", "has conversion"], rows)

print("Conversion cohort size (n) among computed projects at 2026-09:")
rows = []
for name, fn in [("0", lambda n: n == 0), ("1-4", lambda n: 1 <= n <= 4), ("5-9", lambda n: 5 <= n <= 9),
                 ("10-29", lambda n: 10 <= n <= 29), ("30+", lambda n: n >= 30)]:
    rows.append([name, sum(1 for r in comp if fn(sn(r, "conversion") or 0))])
table(["cohort n", "projects"], rows)

samp = [r for r in P if stage(r) == "sampled (large)"]
print("Sampled projects by profile:", dict(Counter(projects[r]["profile"] for r in samp)),
      "| ready:", sum(projects[r]["beginner"]["ready"] for r in samp), "\n")

# external lists and ecosystems
ext = defaultdict(set)
for src, repo in db.execute("SELECT source, repo FROM external_lists"):
    ext[repo.lower()].add(src)
inl = [r for r in P if r in ext]
print(f"Projects in an external newcomer list: {len(inl)}; by stage: {dict(Counter(stage(r) for r in inl))}; "
      f"with conversion@2026-09: {sum(1 for r in inl if sv(r, 'conversion') is not None)}; "
      f"ready: {sum(projects[r]['beginner']['ready'] for r in inl)}\n")
eco = {}
for repo, files in db.execute("SELECT repo, files FROM repo_ecosystems"):
    try:
        eco[repo] = json.loads(files) if files else None
    except ValueError:
        eco[repo] = None
guide_ok = {r: next(c["ok"] for c in projects[r]["beginner"]["checks"] if c["key"] == "guide") for r in P}
eco_contrib = {r: bool(eco.get(r) and eco[r].get("contributing")) for r in P if eco.get(r)}
print("CONTRIBUTING: today's guide check vs ecosyste.ms files.contributing (projects with an ecosyste.ms record):")
table(["", "eco has", "eco missing"], [
    ["guide check ok", sum(1 for r, e in eco_contrib.items() if e and guide_ok[r]), sum(1 for r, e in eco_contrib.items() if not e and guide_ok[r])],
    ["guide check fails", sum(1 for r, e in eco_contrib.items() if e and not guide_ok[r]), sum(1 for r, e in eco_contrib.items() if not e and not guide_ok[r])],
])
fails_only_guide = [r for r in P if not projects[r]["beginner"]["ready"]
                    and [c["key"] for c in projects[r]["beginner"]["checks"] if not c["ok"]] == ["guide"]]
print(f"Projects whose only failing beginner check is `guide`: {len(fails_only_guide)} "
      f"(of them eco sees a CONTRIBUTING: {sum(1 for r in fails_only_guide if eco_contrib.get(r))}): {fails_only_guide}\n")

# ================= 2. Distributions =================
print("## 2. Distributions\n")
rows = []
for s in SIG:
    for as_of in (NOW, TT):
        vals = [v for (r, sg), (v, n) in S[as_of].items() if sg == s and v is not None and r in projects]
        rows.append([s, as_of, len(vals), *q(vals), statistics.fmean(vals)])
table(["Signal", "as_of", "n repos", "p10", "p25", "p50", "p75", "p90", "mean"], rows)
rd = Counter(int(sv(r, "reviewer_diversity")) for r in comp if sv(r, "reviewer_diversity") is not None)
print("demand_per_maintainer NULL split: active_maintainers = 0:", sum(1 for r in comp if sv(r, "demand_per_maintainer") is None and sv(r, "active_maintainers") == 0),
      "| no insider at all:", sum(1 for r in comp if sv(r, "demand_per_maintainer") is None and sv(r, "active_maintainers") is None), "\n")
print("reviewer_diversity@2026-09 counts:", sorted(rd.items()), "\n")
am = Counter(int(sv(r, "active_maintainers")) for r in comp if sv(r, "active_maintainers") is not None)
print("active_maintainers@2026-09 counts:", sorted(am.items()), "\n")
print("active_maintainers = 0 but insiders > 0 @2026-09:",
      sum(1 for r in comp if sv(r, "active_maintainers") == 0), "\n")

# Spearman matrix
print("Spearman, pairwise complete, signals @2026-09 and today's numbers (rho / n):\n")
COLS = [s for s in SIG] + TODAY
get = {s: (lambda s: lambda r: sv(r, s))(s) for s in SIG}
get.update({k: (lambda k: lambda r: today(r, k))(k) for k in TODAY})
short = {"conversion": "conv", "first_insider_response_days": "resp_days", "no_insider_response_share": "no_resp",
         "outsider_insider_gap": "gap", "reviewer_diversity": "rev_div", "active_maintainers": "active",
         "demand_per_maintainer": "demand", "openness": "open", "acceptance": "accept", "debuts_12m": "debuts",
         "review_median_days": "rev_med", "review_stale_share": "stale", "maintainers_24m": "maint24",
         "newcomer_open": "gfi_open", "ready": "ready"}
rows = []
for a in SIG:
    row = [short[a]]
    for b in COLS:
        if a == b:
            row.append("·"); continue
        x, y = pairs(P, get[a], get[b])
        row.append(f"{spearman(x, y):+.2f} ({len(x)})" if len(x) >= 10 and len(set(x)) > 1 and len(set(y)) > 1 else f"- ({len(x)})")
    rows.append(row)
table(["", *[short[c] for c in COLS]], rows)

print("Median of each signal @2026-09 by today's profile (value / n):")
rows = []
for prof in ("open_door", "stable", "guardian", "needs_hands"):
    row = [prof, sum(1 for r in P if projects[r]["profile"] == prof)]
    for s in SIG:
        vals = [sv(r, s) for r in P if projects[r]["profile"] == prof and sv(r, s) is not None]
        row.append(f"{statistics.median(vals):.2f} ({len(vals)})" if vals else "- (0)")
    rows.append(row)
for ready in (True, False):
    row = [f"ready={ready}", sum(1 for r in P if projects[r]["beginner"]["ready"] == ready)]
    for s in SIG:
        vals = [sv(r, s) for r in P if projects[r]["beginner"]["ready"] == ready and sv(r, s) is not None]
        row.append(f"{statistics.median(vals):.2f} ({len(vals)})" if vals else "- (0)")
    rows.append(row)
table(["group", "projects", *[short[s] for s in SIG]], rows)

# review_of vs insider response
x, y = pairs(P, lambda r: today(r, "review_median_days"), lambda r: sv(r, "first_insider_response_days"))
diff = [(r, today(r, "review_median_days"), sv(r, "first_insider_response_days"), sv(r, "no_insider_response_share"),
         sn(r, "first_insider_response_days")) for r in P
        if today(r, "review_median_days") is not None and sv(r, "first_insider_response_days") is not None]
print(f"review.median_days (any non-author reviewer) vs first_insider_response_days: rho {spearman(x, y):+.2f}, n {len(x)}; "
      f"insider median > today's by 7+ days: {sum(1 for d in diff if d[2] - d[1] >= 7)}; by 30+ days: {sum(1 for d in diff if d[2] - d[1] >= 30)}\n")

# ================= 3. Backtest =================
print("## 3. Backtest\n")
conv_out = lambda r: sv(r, "conversion", NOW)
x, y = pairs(P, lambda r: sv(r, "conversion", TT), conv_out)
lo, hi = boot_ci(x, y)
print(f"Noise ceiling: conversion@2025-09 vs conversion@2026-09: rho {spearman(x, y):+.2f} [{lo:+.2f}, {hi:+.2f}], n {len(x)}\n")

# badge at 2025-10 rebuilt from participation, every window capped at 2025-09 (no leak)
BOTS = "'github-actions','dependabot','dependabot-preview','renovate','greenkeeper','pre-commit-ci','mergify','allcontributors','web-flow','copilot','imgbot','snyk-bot'"
HUMAN = f"is_bot = 0 AND login NOT LIKE '%bot' AND login NOT IN ({BOTS})"
PH = HUMAN.replace("is_bot", "p.is_bot").replace("login NOT", "p.login NOT")
T_LAST, C24, C12, C3 = "2025-09", "2023-10", "2024-10", "2025-07"
M = (f"SELECT repo, login FROM participation WHERE {HUMAN} AND month >= '{C24}' AND month <= '{T_LAST}' "
     "AND role IN ('pr_merger','direct_committer') GROUP BY repo, login "
     "HAVING SUM(role='pr_merger') > 0 OR SUM(CASE WHEN role='direct_committer' THEN n ELSE 0 END) >= 3")
F = (f"SELECT repo, login, MIN(month) first FROM participation WHERE role='merged_pr_author' AND {HUMAN} "
     f"AND month <= '{T_LAST}' GROUP BY repo, login")
deb25 = dict(db.execute(f"WITH m AS ({M}), f AS ({F}) SELECT f.repo, COUNT(*) FROM f LEFT JOIN m ON m.repo=f.repo "
                        f"AND m.login=f.login WHERE m.login IS NULL AND f.first >= '{C12}' GROUP BY f.repo"))
tried25 = dict(db.execute(
    f"WITH m AS ({M}), f AS ({F}) SELECT p.repo, COUNT(DISTINCT p.login) FROM participation p "
    "LEFT JOIN m ON m.repo=p.repo AND m.login=p.login LEFT JOIN f ON f.repo=p.repo AND f.login=p.login "
    f"WHERE p.role='pr_author' AND {PH} AND p.month >= '{C12}' AND p.month <= '{T_LAST}' AND m.login IS NULL "
    f"AND (f.first IS NULL OR f.first >= '{C12}') GROUP BY p.repo"))
rec25 = dict(db.execute(
    f"WITH m AS ({M}) SELECT p.repo, SUM(p.n) FROM participation p LEFT JOIN m ON m.repo=p.repo AND m.login=p.login "
    f"WHERE p.role='merged_pr_author' AND m.login IS NULL AND {PH} AND p.month >= '{C3}' AND p.month <= '{T_LAST}' "
    "GROUP BY p.repo"))


def badge25(r):
    """Today's 5 checks at T=2025-10. guide = today's value; response = insider median <= 14 days and
    no-insider-response share <= 0.25 (substitutes review_of, which has no time cap)."""
    if repos[r]["mode"] == "sampled":
        return None
    d = deb25.get(r, 0)
    t = max(tried25.get(r, 0), d)
    rate = d / t if t >= 5 else None
    resp_d, resp_s = sv(r, "first_insider_response_days", TT), sv(r, "no_insider_response_share", TT)
    checks = dict(debuts=d >= 2, acceptance=rate is not None and rate >= 0.25, active=rec25.get(r, 0) >= 2,
                  response=resp_d is not None and resp_d <= 14 and resp_s <= 0.25, guide=guide_ok[r])
    return checks


B25 = {r: badge25(r) for r in P}
newrate25 = lambda r: (deb25.get(r, 0) / max(tried25.get(r, 0), deb25.get(r, 0))) if max(tried25.get(r, 0), deb25.get(r, 0)) >= 5 else None

PRED = [("first_insider_response_days@T", lambda r: sv(r, "first_insider_response_days", TT)),
        ("no_insider_response_share@T", lambda r: sv(r, "no_insider_response_share", TT)),
        ("outsider_insider_gap@T", lambda r: sv(r, "outsider_insider_gap", TT)),
        ("reviewer_diversity@T", lambda r: sv(r, "reviewer_diversity", TT)),
        ("active_maintainers@T", lambda r: sv(r, "active_maintainers", TT)),
        ("demand_per_maintainer@T", lambda r: sv(r, "demand_per_maintainer", TT)),
        ("conversion@T (prior cohort)", lambda r: sv(r, "conversion", TT)),
        ("debuts_12m@T (= cohort size, coupled)", lambda r: deb25.get(r, 0) if B25[r] else None),
        ("newcomer acceptance@T (debuts/tried, 5+ tried)", newrate25),
        ("outside merges last 3m@T", lambda r: rec25.get(r, 0) if B25[r] else None),
        ("badge@T checks passed (0-5)", lambda r: sum(B25[r].values()) if B25[r] else None),
        ("badge@T ready (0/1)", lambda r: int(all(B25[r].values())) if B25[r] else None),
        ("TODAY ready (concurrent, not a backtest)", lambda r: today(r, "ready")),
        ("TODAY openness (concurrent)", lambda r: today(r, "openness")),
        ("TODAY acceptance (concurrent)", lambda r: today(r, "acceptance")),
        ("TODAY review_median_days (concurrent)", lambda r: today(r, "review_median_days"))]
rows = []
for name, fn in PRED:
    x, y = pairs(P, fn, conv_out)
    if len(x) >= 10 and len(set(x)) > 1:
        lo, hi = boot_ci(x, y)
        rows.append([name, len(x), f"{spearman(x, y):+.2f}", f"[{lo:+.2f}, {hi:+.2f}]"])
    else:
        rows.append([name, len(x), "-", "-"])
print("Spearman with conversion@2026-09 (cohort debuted 2024-10..2025-09, followed 12 months), 95% bootstrap CI (1000):")
table(["Predictor", "n", "rho", "95% CI"], rows)

conv_back = lambda r: round(sv(r, "conversion") * sn(r, "conversion"))


def terciles(fn, name):
    ks = [r for r in P if fn(r) is not None and conv_out(r) is not None]
    ks.sort(key=fn)
    out = []
    k = len(ks)
    for i, lab in enumerate(("low", "mid", "high")):
        g = ks[i * k // 3:(i + 1) * k // 3]
        if not g:
            continue
        vals = [fn(r) for r in g]
        pooled = sum(conv_back(r) for r in g) / sum(sn(r, "conversion") for r in g)
        out.append([name, lab, len(g), f"{min(vals):.2f}–{max(vals):.2f}",
                    f"{statistics.fmean(conv_out(r) for r in g):.2f}", f"{pooled:.2f}",
                    sum(sn(r, "conversion") for r in g)])
    return out


rows = []
for name, fn in PRED[:11]:
    rows += terciles(fn, name)
print("Conversion@2026-09 by tercile of each predictor (mean of repo rates; pooled = sum came back / sum cohort):")
table(["Predictor", "tercile", "repos", "range", "mean conv", "pooled conv", "cohort people"], rows)


def groups(fn, labels, name):
    rows = []
    for lab in labels:
        g = [r for r in P if fn(r) == lab and conv_out(r) is not None]
        if g:
            rows.append([name, lab, len(g), f"{statistics.fmean(conv_out(r) for r in g):.2f}",
                         f"{sum(conv_back(r) for r in g) / sum(sn(r, 'conversion') for r in g):.2f}",
                         sum(sn(r, 'conversion') for r in g)])
    return rows


rows = groups(lambda r: today(r, "ready"), [1, 0], "TODAY ready (concurrent)")
rows += groups(lambda r: int(all(B25[r].values())) if B25[r] else None, [1, 0], "badge@T ready")
rows += groups(lambda r: projects[r]["profile"], ["open_door", "stable", "guardian", "needs_hands"], "TODAY profile (concurrent)")
for key in ("debuts", "acceptance", "active", "response", "guide"):
    rows += groups(lambda r, key=key: (int(B25[r][key]) if B25[r] else None), [1, 0], f"badge@T check {key}")
print("Conversion@2026-09 by badge / profile group:")
table(["Grouping", "group", "repos", "mean conv", "pooled conv", "cohort people"], rows)
print("badge@T ready overall:", Counter(int(all(b.values())) for b in B25.values() if b), "| today ready vs badge@T ready (both, today only, T only):",
      sum(1 for r in P if B25[r] and all(B25[r].values()) and today(r, 'ready')),
      sum(1 for r in P if B25[r] and not all(B25[r].values()) and today(r, 'ready')),
      sum(1 for r in P if B25[r] and all(B25[r].values()) and not today(r, 'ready')), "\n")

# ================= 4. Cases =================
print("## 4. Case candidates\n")
cols = ["repo", "profile", "ready", "open", "accept", "debuts", "rev_med", "conv(n)", "resp_days", "no_resp(n)",
        "rev_div", "active", "demand", "gap"]


def caserow(r):
    p = projects[r]
    return [r, p["profile"], int(p["beginner"]["ready"]), p["openness"], p["acceptance"], p["debuts_12m"],
            today(r, "review_median_days"), f"{f(sv(r, 'conversion'))} ({sn(r, 'conversion')})",
            sv(r, "first_insider_response_days"), f"{f(sv(r, 'no_insider_response_share'))} ({sn(r, 'no_insider_response_share')})",
            sv(r, "reviewer_diversity"), sv(r, "active_maintainers"), sv(r, "demand_per_maintainer"),
            sv(r, "outsider_insider_gap")]


def show(title, cond, key=None, lim=12):
    ks = [r for r in P if cond(r)]
    if key:
        ks.sort(key=key)
    print(f"**{title}** ({len(ks)})\n")
    table(cols, [caserow(r) for r in ks[:lim]])


g = lambda r, s: sv(r, s)
show("ready but >= 30% of outside PRs never got an insider response", lambda r: today(r, "ready") and (g(r, "no_insider_response_share") or 0) >= 0.3,
     key=lambda r: -g(r, "no_insider_response_share"))
show("ready, conversion known", lambda r: today(r, "ready") and g(r, "conversion") is not None, key=lambda r: g(r, "conversion"))
show("stable/guardian with conversion >= 0.4", lambda r: projects[r]["profile"] in ("stable", "guardian") and (g(r, "conversion") or 0) >= 0.4,
     key=lambda r: -g(r, "conversion"))
show("open_door with no_insider_response_share >= 0.4", lambda r: projects[r]["profile"] == "open_door" and (g(r, "no_insider_response_share") or 0) >= 0.4,
     key=lambda r: -g(r, "no_insider_response_share"))
show("today's review fast (<= 3 days) but insider median >= 14 days", lambda r: today(r, "review_median_days") is not None and today(r, "review_median_days") <= 3
     and (g(r, "first_insider_response_days") or 0) >= 14, key=lambda r: -g(r, "first_insider_response_days"))
show("reviewer_diversity = 1 and demand >= 5/month per active maintainer", lambda r: g(r, "reviewer_diversity") == 1 and (g(r, "demand_per_maintainer") or 0) >= 5,
     key=lambda r: -g(r, "demand_per_maintainer"))
show("active_maintainers = 0 (everyone on a break) but outside PRs keep coming (10+)", lambda r: g(r, "active_maintainers") == 0 and (sn(r, "first_insider_response_days") or 0) >= 10)
show("open_door with conversion <= 0.15", lambda r: projects[r]["profile"] == "open_door" and g(r, "conversion") is not None and g(r, "conversion") <= 0.15,
     key=lambda r: g(r, "conversion"))

# ================= 5. Entry-path support =================
print("## 5. Entry-path counts (2026-09)\n")
hd = [r for r in comp if g(r, "demand_per_maintainer") is not None]
d75 = q([g(r, "demand_per_maintainer") for r in hd])[3]
rows = [
    ["review: reviewer_diversity <= 1, demand >= p75, and someone answers (no_resp <= 0.5)",
     sum(1 for r in comp if g(r, "reviewer_diversity") is not None and g(r, "reviewer_diversity") <= 1 and (g(r, "demand_per_maintainer") or 0) >= d75 and g(r, "no_insider_response_share") <= 0.5)],
    ["triage: demand >= p75 and active_maintainers 1-2", sum(1 for r in comp if (g(r, "demand_per_maintainer") or 0) >= d75 and g(r, "active_maintainers") in (1, 2))],
    ["successor: active_maintainers = 0, insiders > 0, demand > 0 issues/PRs", sum(1 for r in comp if g(r, "active_maintainers") == 0 and (sn(r, "first_insider_response_days") or 0) > 0)],
    ["code for beginners: conversion >= 0.3 and no_resp <= 0.3", sum(1 for r in comp if (g(r, "conversion") or 0) >= 0.3 and g(r, "no_insider_response_share") is not None and g(r, "no_insider_response_share") <= 0.3)],
]
print(f"demand p75 = {d75:.2f}\n")
table(["Path rule", "projects"], rows)

# ================= 6. Candidate rules (v1) =================
print("## 6. Candidate rules v1: counts\n")
D75, D25 = q([g(r, "demand_per_maintainer") for r in hd])[3], q([g(r, "demand_per_maintainer") for r in hd])[1]


def chk(r, key):
    return next(c["ok"] for c in projects[r]["beginner"]["checks"] if c["key"] == key)


def rate(r, level, T=False):
    """v1 rules. T=True: the beginner rule at 2025-10 (signals@2025-09, badge checks rebuilt at T; profile and
    guardian are today's), for the backtest."""
    st_ = stage(r)
    if T:
        g_ = lambda r, s: sv(r, s, TT)
        chk_ = lambda r, k: B25[r][k]
    else:
        g_, chk_ = g, chk
    if st_ in ("sampled (large)", "truncated"):
        return "insufficient", "large/truncated repo"
    if st_ == "full, no raw activity file":
        return "insufficient", "no PRs since 2018"
    act, nr, rdays = g_(r, "active_maintainers"), g_(r, "no_insider_response_share"), g_(r, "first_insider_response_days")
    conv, dem = g_(r, "conversion"), g_(r, "demand_per_maintainer")
    out_n = sn(r, "first_insider_response_days", TT if T else NOW) or 0
    acc = projects[r]["acceptance"]
    if level == "beginner":
        if projects[r]["profile"] == "guardian":
            return "bad", "guardian"
        if act == 0:
            return "bad", "nobody active"
        if nr is None:
            return "insufficient", "<10 outside PRs"
        if nr > 0.5 or rdays > 30:
            return "bad", "outside PRs go unanswered"
        if (chk_(r, "debuts") and chk_(r, "acceptance") and chk_(r, "active") and nr <= 0.3 and rdays <= 14
                and (conv is None or conv >= 0.1)):
            return "good", "all pass"
        return "ok", "partial"
    if level == "intermediate":
        if act == 0:
            return "bad", "nobody active"
        if nr is None:
            return "insufficient", "<10 outside PRs"
        if nr > 0.6:
            return "bad", "outside PRs go unanswered"
        if nr <= 0.3 and rdays <= 14 and (projects[r]["acceptance"] or 0) >= 0.3:
            return "good", "door works"
        return "ok", "partial"
    # experienced
    if act == 0:
        return ("ok", "successor wanted") if out_n > 0 else ("insufficient", "no activity to read")
    if dem is None:
        return "insufficient", "no maintainer"
    if nr is not None and (nr > 0.6 or (acc is not None and acc < 0.1)):
        return "bad", "door closed despite activity"
    if dem >= D75 and nr is not None and nr <= 0.5 and (acc or 0) >= 0.2:
        return "good", "high demand, door works"
    return "ok", "low or average demand"


print(f"demand p25 = {D25:.2f}, p75 = {D75:.2f}\n")
rows = []
for level in ("beginner", "intermediate", "experienced"):
    c = Counter(rate(r, level)[0] for r in P)
    rows.append([level, c["good"], c["ok"], c["bad"], c["insufficient"]])
table(["Level", "good", "ok", "bad", "insufficient"], rows)
for level in ("beginner", "intermediate", "experienced"):
    c = Counter(rate(r, level) for r in P)
    print(f"{level} reasons:", sorted(((k[0], k[1], v) for k, v in c.items()), key=lambda x: (x[0], -x[2])), "\n")
rows = []
for level in ("beginner", "intermediate", "experienced"):
    for lab in ("good", "ok", "bad", "insufficient"):
        gg = [r for r in P if rate(r, level)[0] == lab and conv_out(r) is not None]
        if gg:
            rows.append([level, lab, len(gg), f"{statistics.fmean(conv_out(r) for r in gg):.2f}",
                         f"{sum(conv_back(r) for r in gg) / sum(sn(r, 'conversion') for r in gg):.2f}", sum(sn(r, 'conversion') for r in gg)])
print("Sanity only (concurrent, same window as the rules): conversion@2026-09 by v1 rating:")
table(["Level", "rating", "repos", "mean conv", "pooled conv", "cohort people"], rows)
rows = []
for lab in ("good", "ok", "bad", "insufficient"):
    gg = [r for r in P if rate(r, "beginner", T=True)[0] == lab and conv_out(r) is not None]
    if gg:
        rows.append(["beginner @T=2025-10", lab, len(gg), f"{statistics.fmean(conv_out(r) for r in gg):.2f}",
                     f"{sum(conv_back(r) for r in gg) / sum(sn(r, 'conversion') for r in gg):.2f}", sum(sn(r, 'conversion') for r in gg)])
print("Backtest of the v1 beginner rule: rated with data before 2025-10, outcome conversion@2026-09:")
table(["Level", "rating", "repos", "mean conv", "pooled conv", "cohort people"], rows)
print("Today's ready=True (30) under v1 beginner:", dict(Counter(rate(r, "beginner")[0] for r in P if today(r, "ready"))))
print("Today's profile x v1 beginner:")
table(["profile", "good", "ok", "bad", "insufficient"],
      [[p_, *[sum(1 for r in P if projects[r]["profile"] == p_ and rate(r, "beginner")[0] == lab) for lab in ("good", "ok", "bad", "insufficient")]]
       for p_ in ("open_door", "stable", "guardian", "needs_hands")])
print("v1 beginner good:", [r for r in P if rate(r, "beginner")[0] == "good"], "\n")
print("today ready but v1 beginner not good:", [(r, rate(r, "beginner")) for r in P if today(r, "ready") and rate(r, "beginner")[0] != "good"], "\n")
print("v1 experienced good (top demand):", sorted([(g(r, "demand_per_maintainer"), r) for r in P if rate(r, "experienced")[0] == "good"], reverse=True)[:15], "\n")
# small-n binomial noise: 95% half-width of a proportion at p = 0.2
for n_ in (5, 10, 20, 50):
    print(f"conversion half-width at p=0.2, n={n_}: ±{1.96 * (0.2 * 0.8 / n_) ** 0.5:.2f}")
print()
# response includes closes: how many answered PRs got only a close (no review, no merge) is not in repo_signals;
# count projects where insiders close fast but merge nothing from outside
print("Fast insider response (<= 2 days) but outside acceptance today < 0.1:",
      [(r, g(r, "first_insider_response_days"), projects[r]["acceptance"]) for r in P
       if g(r, "first_insider_response_days") is not None and g(r, "first_insider_response_days") <= 2 and (projects[r]["acceptance"] or 0) < 0.1])


def diff_ci(flag, reps=1000, seed=107):
    """Mean conversion of flagged repos minus the rest, with a bootstrap 95% CI (repos resampled)."""
    ks = [r for r in P if flag(r) is not None and conv_out(r) is not None]
    rnd = random.Random(seed)
    def d(sample):
        a = [conv_out(r) for r in sample if flag(r)]
        b = [conv_out(r) for r in sample if not flag(r)]
        return statistics.fmean(a) - statistics.fmean(b) if a and b else None
    out = sorted(x for x in (d([rnd.choice(ks) for _ in ks]) for _ in range(reps)) if x is not None)
    return len(ks), sum(1 for r in ks if flag(r)), d(ks), out[int(0.025 * len(out))], out[int(0.975 * len(out)) - 1]


rows = []
for name, fl in [("badge@T ready", lambda r: all(B25[r].values()) if B25[r] else None),
                 ("v1 beginner good @T", lambda r: rate(r, "beginner", T=True)[0] == "good"),
                 ("TODAY ready (concurrent)", lambda r: bool(today(r, "ready")))]:
    n_, k_, d_, lo, hi = diff_ci(fl)
    rows.append([name, n_, k_, f"{d_:+.3f}", f"[{lo:+.3f}, {hi:+.3f}]"])
print("Mean conversion@2026-09, flagged minus rest (bootstrap 95% CI):")
table(["Flag", "repos", "flagged", "diff", "95% CI"], rows)
print()
print("code for beginners list (conv >= 0.3, no_resp <= 0.3):", [r for r in comp if (g(r, "conversion") or 0) >= 0.3 and g(r, "no_insider_response_share") is not None and g(r, "no_insider_response_share") <= 0.3])
print("v1 beginner good with newcomer_open > 0:", [(r, projects[r]["newcomer_open"]) for r in P if rate(r, "beginner")[0] == "good" and projects[r]["newcomer_open"] > 0])

# ================= 7. Robustness checks (advisor review) =================
print("\n## 7. Robustness\n")
# (a) cross-repo insiders inside the conversion cohort (cohort rebuilt from participation, months <= 2025-09)
cohort = db.execute(
    f"WITH m AS ({M}), f AS ({F}) SELECT f.repo, f.login FROM f LEFT JOIN m ON m.repo=f.repo AND m.login=f.login "
    f"WHERE m.login IS NULL AND f.first >= '{C12}'").fetchall()
cohort = [(r, l) for r, l in cohort if conv_out(r) is not None]
ins_any = defaultdict(set)
for repo_, login_ in db.execute(f"SELECT DISTINCT repo, login FROM participation WHERE {HUMAN} AND month <= '{T_LAST}' "
                                "AND role IN ('pr_merger','direct_committer')"):
    ins_any[login_].add(repo_)
other_any = [(r, l) for r, l in cohort if ins_any[l] - {r}]
other_owner = [(r, l) for r, l in cohort if any(x.split('/')[0] == r.split('/')[0] for x in ins_any[l] - {r})]
print(f"Cohort (participation rebuild, projects with conversion): {len(cohort)} people; merger/direct committer in another "
      f"repo before 2025-10: {len(other_any)} ({len(other_any) / len(cohort):.1%}); same owner: {len(other_owner)} ({len(other_owner) / len(cohort):.1%})")
for r in ("pillarjs/router", "h3js/h3", "pypa/build", "celery/kombu", "jshttp/content-disposition"):
    c = [l for rr, l in cohort if rr == r]
    print(f"  {r}: cohort {len(c)}, insider elsewhere {sum(1 for l in c if ins_any[l] - {r})}: {[(l, sorted(ins_any[l] - {r})[:3]) for l in c if ins_any[l] - {r}]}")
by_repo = defaultdict(lambda: [0, 0])
for r, l in cohort:
    by_repo[r][0] += 1; by_repo[r][1] += bool(ins_any[l] - {r})
print("Repos where 30%+ of the cohort is an insider elsewhere:", sorted((r, v[1], v[0]) for r, v in by_repo.items() if v[1] >= 0.3 * v[0]))
# (b) ablation: v1 beginner rule at T without the conversion clause
_orig = sv
def rate_noconv(r):
    lab, why = rate(r, "beginner", T=True)
    if lab == "ok" and why == "partial":
        # re-check good without the conversion clause
        nr, rdays = sv(r, "no_insider_response_share", TT), sv(r, "first_insider_response_days", TT)
        if B25[r]["debuts"] and B25[r]["acceptance"] and B25[r]["active"] and nr <= 0.3 and rdays <= 14:
            return "good"
    return lab
n_, k_, d_, lo, hi = diff_ci(lambda r: rate_noconv(r) == "good")
print(f"\nv1 beginner good @T WITHOUT the conversion clause: repos {n_}, flagged {k_}, diff {d_:+.3f} [{lo:+.3f}, {hi:+.3f}]")
n_, k_, d_, lo, hi = diff_ci(lambda r: (sv(r, "conversion", TT) or 0) >= 0.1 if sv(r, "conversion", TT) is not None else None)
print(f"conversion@T >= 0.1 alone (repos with conversion@T): repos {n_}, flagged {k_}, diff {d_:+.3f} [{lo:+.3f}, {hi:+.3f}]")
# (c) the 216 no-PR projects: any commits in the last 24 months?
c24 = dict(db.execute("SELECT repo, SUM(commits) FROM commit_monthly WHERE month >= '2024-10' GROUP BY repo"))
d24 = dict(db.execute("SELECT repo, SUM(direct_commits) FROM commit_monthly WHERE month >= '2024-10' GROUP BY repo"))
print(f"\nNo-PR projects (216): commits in last 24 months > 0: {sum(1 for r in noraw if (c24.get(r) or 0) > 0)}; "
      f"direct commits > 0: {sum(1 for r in noraw if (d24.get(r) or 0) > 0)}; no commit row: {sum(1 for r in noraw if r not in c24)}")
# (d) the 37 guide mismatches: what file does ecosyste.ms see?
mis = [r for r, e in eco_contrib.items() if e and not guide_ok[r]]
print("\nGuide mismatches, ecosyste.ms contributing path:", Counter(eco[r]["contributing"] for r in mis).most_common())
