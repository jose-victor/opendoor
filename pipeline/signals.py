#!/usr/bin/env python3
"""Tier 1 signals from the activity raw cache (design: docs/deep-analysis.md, section 5).

  python pipeline/signals.py selftest   # assert-based checks on hand-built PRs, no database
  python pipeline/signals.py run        # every signal at the collection month -> repo_signals
  python pipeline/signals.py backtest   # also every signal 12 months earlier (T); conversion at T+12 is the outcome

Offline: reads data/raw/github_activity/*.json.gz and the participation table, no API calls.
as_of = first day of the month after the last closed month (like build.py, windows end at the collection, not
today). Windows end at as_of, exclusive, and nothing at or after as_of is read, so a backtest at T only sees
data before T.
"""
import gzip
import json
import sqlite3
import statistics
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone

from build import BOTS, DB, months_ago, table_exists

RAW = DB.parent / "raw" / "github_activity"
YEAR = timedelta(days=365)


def ts(t):
    return datetime.strptime(t, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc) if t else None


def shift(d, months):
    y, m = divmod(d.year * 12 + d.month - 1 + months, 12)
    return d.replace(year=y, month=m + 1)


def days(delta):
    return delta.total_seconds() / 86400


def login(actor):
    return (actor or {}).get("login") or ""


def is_bot(actor):
    name = login(actor)
    return (actor or {}).get("__typename") == "Bot" or name.endswith(("bot", "[bot]")) or name in BOTS


def closer(item):
    nodes = (item.get("closeEvt") or {}).get("nodes") or [{}]
    return login(nodes[-1].get("actor"))


def reviews(pr):
    return [r for r in (pr.get("reviews") or {}).get("nodes") or [] if r.get("submittedAt")]


def outside(prs, insiders, start, end):
    """Outside PRs created in [start, end): the author is a person (not a bot, not deleted) and not an insider."""
    return [pr for pr in prs if login(pr.get("author")) and not is_bot(pr.get("author"))
            and login(pr.get("author")) not in insiders and start <= ts(pr["createdAt"]) < end]


def first_response(pr, insiders, as_of):
    """First review, merge or close by an insider before as_of (not a bot, not the author); None if none."""
    author = login(pr.get("author"))
    ok = lambda actor: login(actor) in insiders and login(actor) != author and not is_bot(actor)
    times = [ts(r["submittedAt"]) for r in reviews(pr) if ok(r.get("author"))]
    if pr.get("mergedAt"):
        if ok(pr.get("mergedBy")):
            times.append(ts(pr["mergedAt"]))
    elif pr.get("closedAt") and ok({"login": closer(pr)}):
        times.append(ts(pr["closedAt"]))
    return min((t for t in times if t < as_of), default=None)


def _responses(prs, insiders, as_of):
    """(days waited, answered) per outside PR created in the 12 months before as_of; unanswered wait until as_of."""
    out = []
    for pr in outside(prs, insiders, shift(as_of, -12), as_of):
        first = first_response(pr, insiders, as_of)
        out.append((days((first or as_of) - ts(pr["createdAt"])), first is not None))
    return out


def conversion(prs, insiders, as_of):
    """Of outsiders whose first merged PR fell in [as_of-24, as_of-12) months, the share with another merged PR or a
    review on someone else's PR within the 12 months after it. Pass the insiders as of the cohort's end (as_of-12),
    so a debut who later became a maintainer still counts as an outsider who came back."""
    merged, reviewed = defaultdict(list), defaultdict(list)
    for pr in prs:
        author = pr.get("author")
        if pr.get("mergedAt") and ts(pr["mergedAt"]) < as_of and login(author) and not is_bot(author):
            merged[login(author)].append(ts(pr["mergedAt"]))
        for r in reviews(pr):
            if login(r.get("author")) and login(r.get("author")) != login(author) and not is_bot(r.get("author")):
                reviewed[login(r.get("author"))].append(ts(r["submittedAt"]))
    start, end = shift(as_of, -24), shift(as_of, -12)
    back = n = 0
    for who, times in merged.items():
        times.sort()
        debut = times[0]
        if who in insiders or not start <= debut < end:
            continue
        n += 1
        back += any(debut < t <= debut + YEAR and t < as_of for t in times[1:] + reviewed[who])
    return (round(back / n, 3) if n >= 5 else None, n)


def first_insider_response_days(prs, insiders, as_of):
    """Median days from an outside PR's creation to the first insider review, merge or close (window: 12 months)."""
    r = _responses(prs, insiders, as_of)
    return (round(statistics.median(w for w, _ in r), 1) if len(r) >= 10 else None, len(r))


def no_insider_response_share(prs, insiders, as_of):
    """Share of outside PRs of the 12 months with no insider review, merge or close before as_of."""
    r = _responses(prs, insiders, as_of)
    return (round(sum(not answered for _, answered in r) / len(r), 3) if len(r) >= 10 else None, len(r))


def outsider_insider_gap(prs, insiders, as_of):
    """Insider acceptance minus outsider acceptance, PRs created in 12 months and decided before as_of.
    Self-merged insider PRs are left out (they say nothing about the door). n = the smaller side."""
    ins, out = [], []
    start = shift(as_of, -12)
    for pr in prs:
        author = pr.get("author")
        if not login(author) or is_bot(author) or not start <= ts(pr["createdAt"]) < as_of:
            continue
        merged = bool(pr.get("mergedAt")) and ts(pr["mergedAt"]) < as_of
        if not merged and not (pr.get("closedAt") and ts(pr["closedAt"]) < as_of):
            continue  # still open at as_of
        if login(author) not in insiders:
            out.append(merged)
        elif not (merged and login(pr.get("mergedBy")) == login(author)):
            ins.append(merged)
    n = min(len(ins), len(out))
    return (round(sum(ins) / len(ins) - sum(out) / len(out), 3) if n >= 10 else None, n)


def reviewer_diversity(prs, insiders, as_of):
    """Distinct insiders who reviewed outside PRs created in the 12 months (reviews only, not merges)."""
    window = outside(prs, insiders, shift(as_of, -12), as_of)
    who = {login(r.get("author")) for pr in window for r in reviews(pr)
           if login(r.get("author")) in insiders and not is_bot(r.get("author")) and ts(r["submittedAt"]) < as_of}
    return (len(who) if len(window) >= 10 else None, len(window))


def active_maintainers(prs, insiders, as_of, issues=()):
    """Insiders not on a break: the gap since their last action (merge, review, PR or issue close) is within the
    90th percentile of their own gaps, or 90 days with fewer than 5 gaps (Calefato 2022). n = insiders."""
    acts = defaultdict(list)
    for item in [*prs, *issues]:
        for r in reviews(item):
            acts[login(r.get("author"))].append(ts(r["submittedAt"]))
        if item.get("mergedAt"):
            acts[login(item.get("mergedBy"))].append(ts(item["mergedAt"]))
        elif item.get("closedAt"):
            acts[closer(item)].append(ts(item["closedAt"]))
    active = 0
    for who in insiders:
        # shortcut: direct commits are not in the activity cache, so a maintainer who only pushes counts as
        # inactive (tiny packages); upgrade when commit authors/times per login are cached.
        times = sorted(t for t in acts.get(who, ()) if t < as_of)
        if not times:
            continue
        gaps = [days(b - a) for a, b in zip(times, times[1:])]
        usual = statistics.quantiles(gaps, n=10, method="inclusive")[-1] if len(gaps) >= 5 else 90
        active += days(as_of - times[-1]) <= usual
    return (active if insiders else None, len(insiders))


def demand_per_maintainer(prs, insiders, as_of, issues=()):
    """New issues (not by bots) + new outside PRs per month over the 12 months, per active maintainer.
    n = active maintainers; None when there is none."""
    start = shift(as_of, -12)
    new = len(outside(prs, insiders, start, as_of)) + sum(
        1 for i in issues if not is_bot(i.get("author")) and start <= ts(i["createdAt"]) < as_of)
    active, _ = active_maintainers(prs, insiders, as_of, issues)
    return (round(new / 12 / active, 2) if active else None, active or 0)


SIGNALS = [first_insider_response_days, no_insider_response_share, outsider_insider_gap, reviewer_diversity,
           active_maintainers, demand_per_maintainer]


def insiders(db, repo, as_of):
    """Insiders at as_of: build.py's maintainer rule (merged a PR, or 3+ direct commits, in the 24 months before as_of),
    plus repo_assignable (write access, today's list) when that table exists. Bots excluded."""
    last = shift(as_of, -1).strftime("%Y-%m")
    logins = [r[0] for r in db.execute(
        "SELECT login FROM participation WHERE repo = ? AND is_bot = 0 AND month >= ? AND month <= ? "
        "AND role IN ('pr_merger', 'direct_committer') GROUP BY login "
        "HAVING SUM(role = 'pr_merger') > 0 OR SUM(CASE WHEN role = 'direct_committer' THEN n ELSE 0 END) >= 3",
        (repo, months_ago(24, last), last))]
    if table_exists(db, "repo_assignable"):
        logins += [r[0] for r in db.execute("SELECT login FROM repo_assignable WHERE repo = ?", (repo,))]
    return {l for l in logins if not is_bot({"login": l})}


def compute(db, as_of):
    """Every signal for fully collected repos at as_of, one transaction per repo."""
    files = {p.name[:-len(".json.gz")].replace("__", "/", 1).lower(): p for p in RAW.glob("*.json.gz")}
    key = as_of.strftime("%Y-%m")
    # truncated repos miss their older PRs, so debuts and maintainer gaps would be wrong
    repos = [r[0] for r in db.execute("SELECT repo FROM repos WHERE found = 1 AND collection_mode IS NULL "
                                      "AND activity_truncated = 0 ORDER BY repo") if r[0] in files]
    for repo in repos:
        raw = json.load(gzip.open(files[repo]))
        prs, issues, ins = raw["prs"], raw["issues"], insiders(db, repo, as_of)
        rows = {"conversion": conversion(prs, insiders(db, repo, shift(as_of, -12)), as_of)}
        for fn in SIGNALS:
            rows[fn.__name__] = fn(prs, ins, as_of, issues) if fn in (active_maintainers, demand_per_maintainer) \
                else fn(prs, ins, as_of)
        with db:
            db.executemany("INSERT OR REPLACE INTO repo_signals VALUES (?, ?, ?, ?, ?)",
                           [(repo, s, key, v, n) for s, (v, n) in rows.items()])
    print(f"as_of {key}: {len(repos)} repos")
    for s in ["conversion"] + [fn.__name__ for fn in SIGNALS]:
        vals = [v for (v,) in db.execute("SELECT value FROM repo_signals WHERE signal = ? AND as_of = ? "
                                         "AND value IS NOT NULL", (s, key))]
        print(f"  {s:30} {len(vals):4} repos  median {statistics.median(vals) if vals else '-'}")


def selftest():
    d = lambda s: f"{s}T00:00:00Z"
    user = lambda name: {"login": name, "__typename": "User"}
    bot = lambda name: {"login": name, "__typename": "Bot"}

    def pr(author, created, merged=None, by=None, closed=None, closed_by=None, revs=()):
        return {"createdAt": d(created), "author": author if isinstance(author, dict) else user(author),
                "mergedAt": d(merged) if merged else None, "mergedBy": user(by) if by else None,
                "closedAt": d(merged or closed) if (merged or closed) else None,
                "closeEvt": {"nodes": [{"actor": user(by or closed_by)}] if (by or closed_by) else []},
                "reviews": {"nodes": [{"author": a if isinstance(a, dict) else user(a), "submittedAt": d(t)} for a, t in revs]}}

    as_of = datetime(2026, 10, 1, tzinfo=timezone.utc)
    ins = {"maint", "renovate-bot"}  # a bot sneaking into the insiders must still be ignored
    # 10 outside PRs answered only by a bot or by their author: none answered, all waited until as_of
    prs = [pr(f"out{i}", "2026-09-01", revs=[(bot("renovate-bot"), "2026-09-02"), (f"out{i}", "2026-09-02")])
           for i in range(10)]
    assert no_insider_response_share(prs, ins, as_of) == (1.0, 10)
    assert first_insider_response_days(prs, ins, as_of) == (30.0, 10)
    # insider review after 2 days; merge after as_of does not count (backtest sees only the past)
    prs = [pr(f"out{i}", "2026-09-01", revs=[("maint", "2026-09-03")]) for i in range(10)]
    prs.append(pr("late", "2026-09-01", merged="2026-10-05", by="maint"))
    assert first_insider_response_days(prs, ins, as_of) == (2.0, 11)
    assert no_insider_response_share(prs, ins, as_of) == (round(1 / 11, 3), 11)
    # a close by the author is not a response; a close by an insider is
    assert first_response(pr("x", "2026-09-01", closed="2026-09-02", closed_by="x"), ins, as_of) is None
    assert first_response(pr("x", "2026-09-01", closed="2026-09-04", closed_by="maint"), ins, as_of) == ts(d("2026-09-04"))
    # below the minimum n
    assert first_insider_response_days(prs[:9], ins, as_of) == (None, 9)
    assert reviewer_diversity(prs[:9], ins, as_of) == (None, 9)
    assert reviewer_diversity(prs, ins, as_of) == (1, 11)
    # conversion: cohort = first merge in [2024-10, 2025-10); 3 of 5 come back within 12 months
    prs = [pr("a", "2025-01-01", merged="2025-01-02", by="maint"), pr("a", "2025-06-01", merged="2025-06-02", by="maint"),
           pr("b", "2025-02-01", merged="2025-02-02", by="maint"), pr("maint", "2025-08-01", revs=[("b", "2025-08-03")]),
           pr("c", "2025-03-01", merged="2025-03-02", by="maint"), pr("c", "2026-06-01", merged="2026-06-02", by="maint"),
           pr("e", "2025-04-01", merged="2025-04-02", by="maint"),  # never back
           pr("f", "2025-05-01", merged="2025-05-02", by="maint"), pr("f", "2025-06-01", merged="2025-06-02", by="f"),  # later a maintainer
           pr("old", "2023-01-01", merged="2023-01-02", by="maint"), pr("old", "2025-03-01", merged="2025-03-02", by="maint"),
           pr("maint", "2025-01-01", merged="2025-01-02", by="maint"), pr("maint", "2025-02-01", merged="2025-02-02", by="maint")]
    assert conversion(prs, {"maint"}, as_of) == (0.6, 5)  # c came back after 15 months: not converted
    assert conversion(prs[:9], {"maint"}, as_of) == (0.6, 5)
    assert conversion(prs[:7], {"maint"}, as_of) == (None, 4)
    # gap: insiders accept 10/10 (self-merges excluded), outsiders 5/10
    prs = ([pr("maint", "2026-01-01", merged="2026-01-02", by="other") for _ in range(10)]
           + [pr("maint", "2026-01-01", merged="2026-01-02", by="maint") for _ in range(10)]
           + [pr(f"o{i}", "2026-01-01", merged="2026-01-02", by="maint") for i in range(5)]
           + [pr(f"p{i}", "2026-01-01", closed="2026-01-02", closed_by="maint") for i in range(5)]
           + [pr("q", "2026-09-20")])  # still open: not decided
    assert outsider_insider_gap(prs, {"maint", "other"}, as_of) == (0.5, 10)
    assert outsider_insider_gap(prs[10:], {"maint", "other"}, as_of) == (None, 0)
    # active maintainers: weekly reviewer gone for 10 months is on a break; a weekly one seen 3 days ago is not;
    # one with 2 actions 30 days ago falls back to 90 days
    weekly = lambda who, last: [pr("o", "2020-01-01", revs=[(who, (last - timedelta(weeks=k)).strftime("%Y-%m-%d"))])
                                for k in range(10)]
    prs = weekly("gone", datetime(2025, 12, 1)) + weekly("here", datetime(2026, 9, 28)) \
        + [pr("o", "2020-01-01", revs=[("rare", "2026-08-31"), ("rare", "2026-07-01")])]
    trio = {"gone", "here", "rare"}
    assert active_maintainers(prs, trio, as_of) == (2, 3)
    assert active_maintainers(prs, {"gone"}, as_of) == (0, 1)
    assert active_maintainers(prs, set(), as_of) == (None, 0)
    # demand: 20 new issues (2 by bots ignored) + 4 outside PRs over 12 months, 2 active maintainers -> 24/12/2
    issues = [{"createdAt": d("2026-03-01"), "author": user("u")}] * 20 + [{"createdAt": d("2026-03-01"), "author": bot("x")}] * 2
    prs += [pr(f"o{i}", "2026-05-01") for i in range(4)]
    assert demand_per_maintainer(prs, trio, as_of, issues) == (round(24 / 12 / 2, 2), 2)
    assert demand_per_maintainer(prs, {"gone"}, as_of, issues) == (None, 0)


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "run"
    if cmd not in ("selftest", "run", "backtest"):
        raise SystemExit(__doc__)
    selftest()
    if cmd == "selftest":
        print("selftest ok")
        return
    db = sqlite3.connect(DB, timeout=60)
    db.execute("CREATE TABLE IF NOT EXISTS repo_signals(repo TEXT, signal TEXT, as_of TEXT, value REAL, n INT, "
               "PRIMARY KEY(repo, signal, as_of))")
    last = db.execute("SELECT MAX(month) FROM repo_monthly").fetchone()[0]
    as_of = shift(datetime.strptime(last, "%Y-%m").replace(tzinfo=timezone.utc), 1)
    for when in ([shift(as_of, -12)] if cmd == "backtest" else []) + [as_of]:
        compute(db, when)


if __name__ == "__main__":
    main()
