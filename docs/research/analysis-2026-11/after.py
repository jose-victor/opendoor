"""Part 2 of #107: effects of the new collection. Read-only.
python3 after.py <int-tree> <before-projects.json> <now-label>"""
import json, sqlite3, sys
from collections import Counter
from pathlib import Path
ROOT, BEFORE, NOW = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
db = sqlite3.connect(f"file:{(ROOT / 'data/ecosystem.db').resolve()}?mode=ro", uri=True)
new = {p["repo"]: p for p in json.load(open(ROOT / "web/public/data/projects.json"))}
old = {p["repo"]: p for p in json.load(open(BEFORE))}
both = sorted(set(new) & set(old))
print("projects before/after/both:", len(old), len(new), len(both))
print("ready before/after:", sum(old[r]["beginner"]["ready"] for r in both), sum(new[r]["beginner"]["ready"] for r in both))
flip = [r for r in both if new[r]["beginner"]["ready"] and not old[r]["beginner"]["ready"]]
lost = [r for r in both if old[r]["beginner"]["ready"] and not new[r]["beginner"]["ready"]]
print("newly ready:", len(flip), "| lost ready:", lost)
sig = {}
for repo, s, v, n in db.execute("SELECT repo, signal, value, n FROM repo_signals WHERE as_of = ?", (NOW,)):
    sig[(repo, s)] = (v, n)
v = lambda r, s: sig.get((r, s), (None, None))
BOTS = "'github-actions','dependabot','dependabot-preview','renovate','greenkeeper','pre-commit-ci','mergify','allcontributors','web-flow','copilot','imgbot','snyk-bot'"
HUMAN = f"is_bot = 0 AND login NOT LIKE '%bot' AND login NOT IN ({BOTS})"
last = db.execute("SELECT MAX(month) FROM repo_monthly").fetchone()[0]
def back(m, k):
    y, mo = divmod(int(m[:4]) * 12 + int(m[5:]) - 1 - k, 12)
    return f"{y}-{mo + 1:02d}"
c24, c12 = back(last, 23), back(last, 11)
M = (f"SELECT repo, login FROM participation WHERE {HUMAN} AND month >= '{c24}' AND role IN ('pr_merger','direct_committer') "
     "GROUP BY repo, login HAVING SUM(role='pr_merger') > 0 OR SUM(CASE WHEN role='direct_committer' THEN n ELSE 0 END) >= 3")
F = f"SELECT repo, login, MIN(month) first FROM participation WHERE role='merged_pr_author' AND {HUMAN} GROUP BY repo, login"
assign = {(r, l.lower()) for r, l in db.execute("SELECT repo, login FROM repo_assignable")}
debuts = db.execute(f"WITH m AS ({M}), f AS ({F}) SELECT f.repo, f.login FROM f LEFT JOIN m ON m.repo=f.repo AND m.login=f.login "
                    f"WHERE m.login IS NULL AND f.first >= '{c12}'").fetchall()
deb_by = Counter(r for r, l in debuts); deb_as = Counter(r for r, l in debuts if (r, l.lower()) in assign)
print(f"\nDebuts (12m, build.py rule) that are assignable today: {sum(deb_as.values())} of {len(debuts)} "
      f"in {len(deb_as)} repos")
cols = ["repo", "profile old→new", "guide old→new", "debuts (assignable)", "acceptance", "conv (n)", "insider resp d",
        "no-resp (n)", "rev_div", "active", "newcomer_open", "contributing"]
comm = {r: (u, inh) for r, u, inh in db.execute("SELECT repo, contributing_url, contributing_inherited FROM repo_community")} \
    if db.execute("SELECT 1 FROM pragma_table_info('repo_community') WHERE name='contributing_inherited'").fetchone() else {}
print("\nrepo_community columns:", [c[1] for c in db.execute("PRAGMA table_info(repo_community)")])
def g(r, k): return next(c["ok"] for c in r["beginner"]["checks"] if c["key"] == k)
print("\n| " + " | ".join(cols) + " |\n|" + "---|" * len(cols))
for r in flip:
    o, n_ = old[r], new[r]
    cv, cn = v(r, "conversion"); nr, nn = v(r, "no_insider_response_share")
    print(f"| `{r}` | {o['profile']}→{n_['profile']} | {int(g(o,'guide'))}→{int(g(n_,'guide'))} | {deb_by.get(r,0)} ({deb_as.get(r,0)}) | "
          f"{n_['acceptance']} | {cv if cv is None else round(cv,2)} ({cn}) | {v(r,'first_insider_response_days')[0]} | "
          f"{nr} ({nn}) | {v(r,'reviewer_diversity')[0]} | {v(r,'active_maintainers')[0]} | {n_['newcomer_open']} | "
          f"{'inherited' if comm.get(r, (0, 0))[1] else ('own' if comm.get(r, (None,))[0] else '-')} |")
# which checks flipped for the newly ready
print("\nChecks that flipped False->True among the newly ready:",
      Counter(k for r in flip for k in ("debuts", "acceptance", "active", "response", "guide") if g(new[r], k) and not g(old[r], k)))
# profile flips
pf = [(r, old[r]["profile"], new[r]["profile"]) for r in both if old[r]["profile"] != new[r]["profile"]]
print("profile flips:", pf)
full = {r for (r,) in db.execute("SELECT repo FROM repos WHERE collection_mode IS NULL AND activity_truncated = 0")}
dfull = [(r, l) for r, l in debuts if r in full]
print(f"\nFull repos only: debuts 12m {len(dfull)}, assignable today {sum(1 for r, l in dfull if (r, l.lower()) in assign)} "
      f"in {len({r for r, l in dfull if (r, l.lower()) in assign})} repos")
# conversion cohort at T (participation rebuild, first merge in the 12 months to T, not insider at T) that is assignable today
T = back(last, 12)
MT = M.replace(f"month >= '{c24}'", f"month >= '{back(T, 23)}' AND month <= '{T}'")
FT = F.replace("GROUP BY", f"AND month <= '{T}' GROUP BY")
coh = [(r, l) for r, l in db.execute(f"WITH m AS ({MT}), f AS ({FT}) SELECT f.repo, f.login FROM f LEFT JOIN m ON m.repo=f.repo "
       f"AND m.login=f.login WHERE m.login IS NULL AND f.first >= '{back(T, 11)}'") if r in full and v(r, 'conversion')[0] is not None]
print(f"T={T}: cohort people in repos with conversion: {len(coh)}; assignable today: {sum(1 for r, l in coh if (r, l.lower()) in assign)}")
