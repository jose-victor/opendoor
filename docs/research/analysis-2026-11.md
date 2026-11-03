# First analysis of the Tier 1 signals (November 2026)

Issue #107. Sections 1–6: the collection of 2026-10-31 (last closed month 2026-09), `repo_signals` from `pipeline/signals.py` (branch `jose/106-signals`, recomputed on 2026-11-02 with the corrected definitions: closed PRs stop waiting at their close, insiders are behavioral only, `as_of` = last closed month), `web/public/data/projects.json` as committed on 2026-11-02, `external_lists` and `repo_ecosystems`. Design this feeds: `docs/deep-analysis.md` (#86).

`as_of` labels: **2026-09** = window of the 12 months ending with September 2026 (current). **2025-09** = the same window one year earlier (T, the backtest). Signals at 2025-09 pair with `conversion` at 2026-09: outsiders whose first merged PR fell between 2024-10 and 2025-09, and whether they came back within 12 months.

## Summary

Updated after the collection of 2026-11-02 (section 7). Numbers come from that collection unless marked otherwise.

1. **Coverage grew, but most projects still can't be rated on welcome.** Of 957 projects, 133 (13.9%) have `conversion`, up from 93, and 280 (29.3%) have the insider-response signals, up from 180. The rest: 111 sampled, 34 with no PR since 2018, 565 with fewer than 10 outside PRs. Correction to the first run: its 216 "no PR" projects had simply never been collected.
2. **Past conversion is the only predictor that holds.** Year over year it gives +0.33 [+0.11, +0.54], n 89 (+0.45 on the first data). `conversion@T ≥ 0.1` lifts next year's mean by +0.091 [+0.035, +0.148].
3. **Demand per active maintainer predicts lower conversion, on both datasets.** −0.30 [−0.46, −0.12], n 124, falling across terciles: 0.28 → 0.22 → 0.18 pooled.
4. **Insider response time and no-response share do not predict conversion** (+0.06, −0.03, CIs around 0). Keep them as product rules: a newcomer who never hears back learns nothing.
5. **Neither today's badge nor a v1 rule beats chance at T.** Badge +0.004 [−0.069, +0.085]; v1 +0.026; v1 without past conversion −0.002. The data defends the null rules (insufficient, nobody active, no team response), not a good/ok split.
6. **Redundancy.**
   - Response days ≈ today's review median (+0.88).
   - No-response share ≈ inverse of acceptance (−0.72).
   - Reviewer diversity ≈ active maintainers (+0.68).
   - Demand ≈ debuts (+0.78).

   New information: conversion, `active_maintainers` (131 projects with every insider on a break) and the insider-only no-response share.
7. **A fast answer can be a fast "no".** `pallets/jinja` answers in a median of 0.0 days but merged 0 of 116 PRs in 2026, so response must be read with acceptance. The reverse also happens: bot-merged Kubernetes repos look 100% open and are badged ready, while no human insider ever answers (no-resp 1.00).
8. **The `guide` fix worked, and it alone made 14 projects ready.** Passes went 247 → 443, with 0 mismatches against ecosyste.ms left.
   - Trust 8 of the 14.
   - Tag 2 "poucos dados".
   - Drop the badge on 4: `aio-libs/yarl`, `aio-libs/frozenlist`, `pyca/pyopenssl`, `privatenumber/get-tsconfig`.

   The new labels changed nothing.
9. **Use assignableUsers as insiders for "who answers / maintains", not for "who debuted".** It is today's list, and successful newcomers become members. Keep the backtest behavioral, and in huge orgs count only assignable logins who acted.
10. **Entry paths for experienced people:** review 55 projects, triage 105, successor 93. Drop `outsider_insider_gap` (48 projects). Maintainers of other repos are 10.6% of conversion cohorts and inflate it.

Scripts: [`analysis.py`](analysis-2026-11/analysis.py) (all tables; `python3 analysis.py <worktree> <now> <T> > out.md`, stdlib only, DB opened `mode=ro`), [`after.py`](analysis-2026-11/after.py) (section 7) and [`cases.sql`](analysis-2026-11/cases.sql). Sections 1–6 are the first run on the data of 2026-10-31 (labels 2026-09 / 2025-09), quoted from [`out-2026-10-31.md`](analysis-2026-11/out-2026-10-31.md). Section 7 is the re-run on the collection of 2026-11-02 (labels 2026-10 / 2025-10), from [`out.md`](analysis-2026-11/out.md) and [`after.out`](analysis-2026-11/after.out). Every number below was printed by one of them. "Script section N" in the Pending list refers to the script's printed sections, not this report's.

---

## 1. Coverage

Denominator: the 958 projects in `projects.json`. `repo_signals` has 650 repos, but 11 of those are non-canonical duplicates (old names) that are not on the site.

| Stage | Projects | What happens |
|---|---|---|
| Computed (full collection, raw file) | 639 | signals exist; a value needs the minimum n |
| Full, no raw activity file | 216 | not collected yet (`activity_fetched_at` NULL; see the correction in section 7); 207 have PRs in the new data |
| Sampled (large) | 102 | not computed (76 `open_door`, 23 `stable`, 3 `guardian`; 0 ready) |
| Truncated | 1 | not computed |

Per signal at 2026-09 (the 639 computed projects):

| Signal | min n | n = 0 | 0 < n < min | has value | % of 958 | has value @2025-09 |
|---|---|---|---|---|---|---|
| conversion | 5 debuts | 331 | 215 | 93 | 9.7% | 102 |
| first_insider_response_days | 10 outside PRs | 196 | 263 | 180 | 18.8% | 122 |
| no_insider_response_share | 10 | 196 | 263 | 180 | 18.8% | 122 |
| outsider_insider_gap | 10 (smaller side) | 518 | 85 | 36 | 3.8% | 23 |
| reviewer_diversity | 10 | 196 | 263 | 180 | 18.8% | 122 |
| active_maintainers | 1 insider | 160 | 0 | 479 | 50.0% | 480 |
| demand_per_maintainer | 1 active | 275 | 0 | 364 | 38.0% | 360 |

`demand_per_maintainer` NULL mixes two cases. In 115 projects it is NULL because nobody is active (`active_maintainers = 0`); in 160 there is no insider at all. Read it together with `active_maintainers`.

Who drops out, by outside PRs in 12 months (computed projects):

| Outside PRs 12m | Projects | open_door | stable | guardian | needs_hands | ready | has conversion |
|---|---|---|---|---|---|---|---|
| 0 | 196 | 0 | 149 | 47 | 0 | 0 | 0 |
| 1–9 | 263 | 20 | 171 | 72 | 0 | 1 | 7 |
| 10–29 | 92 | 40 | 32 | 17 | 3 | 9 | 22 |
| 30–99 | 62 | 34 | 15 | 10 | 3 | 14 | 41 |
| 100+ | 26 | 16 | 6 | 4 | 0 | 5 | 23 |

Conversion cohort size: 0 in 331 projects, 1–4 in 215, 5–9 in 45, 10–29 in 39, 30+ in 9. Almost half of the rated projects (45 of 93) rest on 5–9 people.

External lists: 35 projects appear in goodfirstissue.dev, Up For Grabs or GSoC 2026. 31 of them are sampled, 2 have no PRs, 2 are computed. Only 1 has conversion and none is ready. The lists cannot validate the rating today; they are seeds (as `data-sources.md` concluded).

CONTRIBUTING, today's `guide` check against `repo_ecosystems.files.contributing` (924 projects with a record):

| | ecosyste.ms has it | ecosyste.ms does not |
|---|---|---|
| guide check passes | 239 | 3 |
| guide check fails | 37 | 645 |

The file ecosyste.ms sees in the 37 mismatches:

| File | Projects |
|---|---|
| `CONTRIBUTING.rst` | 14 |
| `docs/contributing.md` | 7 |
| `docs/contributing.rst` | 4 |
| `.github/contributing.md` | 4 |
| `docs/contributing/guidelines.rst` | 3 |
| `contributing.md` | 3 |
| `CONTRIBUTING.txt` | 1 |
| `CONTRIBUTING` | 1 |

Most of the bug is on **our side**. `build.py` only reads `repo_files` paths matching `%CONTRIBUTING.md`, and the collector does not fetch the `.rst`/`.txt` or `docs/` variants. Org-level files (the community-files fix) are a separate gap.

55 projects fail **only** the `guide` check, e.g. `h3js/h3`, `pypa/build`, `fsspec/filesystem_spec`, `agronholm/anyio`, `sindresorhus/type-fest`. 8 of them have a contributing file according to ecosyste.ms.

**What the site should say for each group** (copy in section 5.2):

| Group | Projects | Proposed state |
|---|---|---|
| Not collected yet | 216 (34 after the new collection, all with really 0 PRs) | "dados insuficientes" + the reason. Not a bad rating. |
| Sampled | 102 | "dados insuficientes" until the per-author debut search exists (deep-analysis §4) |
| 1–9 outside PRs | 263 | show the raw count ("3 de 5 PRs de fora tiveram resposta do time") marked "poucos dados", no rating |
| 0 outside PRs | 196 | "ninguém de fora mandou PR no último ano" |

## 2. Distributions and redundancy

Quantiles (projects with a value):

| Signal | as_of | n | p10 | p25 | p50 | p75 | p90 | mean |
|---|---|---|---|---|---|---|---|---|
| conversion | 2026-09 | 93 | 0.00 | 0.10 | 0.20 | 0.31 | 0.50 | 0.23 |
| conversion | 2025-09 | 102 | 0.00 | 0.11 | 0.18 | 0.28 | 0.40 | 0.21 |
| first_insider_response_days | 2026-09 | 180 | 0.20 | 1.08 | 6.00 | 22.52 | 46.62 | 18.92 |
| first_insider_response_days | 2025-09 | 122 | 0.11 | 0.60 | 3.15 | 25.48 | 63.78 | 21.74 |
| no_insider_response_share | 2026-09 | 180 | 0.07 | 0.17 | 0.31 | 0.61 | 0.88 | 0.40 |
| no_insider_response_share | 2025-09 | 122 | 0.06 | 0.10 | 0.23 | 0.44 | 0.68 | 0.30 |
| outsider_insider_gap | 2026-09 | 36 | −0.36 | −0.07 | 0.08 | 0.29 | 0.48 | 0.08 |
| reviewer_diversity | 2026-09 | 180 | 0 | 1 | 1 | 2 | 3 | 1.57 |
| active_maintainers | 2026-09 | 479 | 0 | 1 | 1 | 1 | 3 | 1.26 |
| active_maintainers | 2025-09 | 480 | 0 | 0.75 | 1 | 1 | 2 | 1.19 |
| demand_per_maintainer | 2026-09 | 364 | 0.07 | 0.17 | 0.75 | 2.10 | 5.91 | 2.32 |
| demand_per_maintainer | 2025-09 | 360 | 0.08 | 0.22 | 0.67 | 1.93 | 4.32 | 1.61 |

- `reviewer_diversity` counts: 0 → 38, 1 → 77, 2 → 29, 3 → 19, 4 → 11, 5+ → 6. So 115 of 180 have at most one insider reviewing outside PRs.
- `active_maintainers` counts: 0 → 115, 1 → 258, 2 → 49, 3+ → 57. A single active person is the norm.
- No-response share median 0.23 → 0.31 between windows, but over different project sets (122 vs 180): not a trend.

Spearman, pairwise complete (rho, n). Rows: signals at 2026-09. Columns: today's numbers from `projects.json`.

| | openness | acceptance | debuts_12m | review median | stale share | maintainers_24m | newcomer_open | ready |
|---|---|---|---|---|---|---|---|---|
| conversion | +0.03 (90) | **+0.34** (89) | −0.15 (93) | −0.06 (92) | +0.02 (92) | +0.26 (93) | −0.05 (93) | +0.03 (93) |
| resp_days | −0.02 (163) | −0.49 (180) | −0.26 (180) | **+0.85** (180) | +0.71 (180) | +0.05 (180) | +0.29 (180) | −0.21 (180) |
| no_resp | −0.13 (163) | **−0.76** (180) | −0.36 (180) | +0.68 (180) | **+0.77** (180) | −0.06 (180) | +0.22 (180) | −0.20 (180) |
| gap | +0.05 (36) | −0.39 (36) | −0.16 (36) | +0.11 (36) | +0.17 (36) | −0.07 (36) | −0.18 (36) | −0.10 (36) |
| rev_div | +0.23 (163) | +0.39 (180) | +0.52 (180) | −0.25 (180) | −0.11 (180) | **+0.65** (180) | +0.13 (180) | +0.30 (180) |
| active | +0.08 (285) | +0.27 (238) | +0.50 (479) | −0.17 (263) | −0.07 (263) | **+0.61** (479) | +0.16 (479) | +0.28 (479) |
| demand | +0.41 (259) | −0.16 (211) | **+0.76** (364) | −0.09 (229) | +0.14 (229) | +0.22 (364) | +0.28 (364) | +0.25 (364) |

Among the signals: resp_days vs no_resp +0.76 (180); rev_div vs active +0.67 (177); conversion vs demand −0.41 (91); conversion vs every other signal at most |0.24|.

Median of each signal by today's profile and badge (value, n):

| Group | Projects | conversion | resp_days | no_resp | rev_div | active | demand |
|---|---|---|---|---|---|---|---|
| open_door | 187 | 0.20 (51) | 4.2 (90) | 0.24 (90) | 2 (90) | 2 (110) | 1.90 (100) |
| stable | 612 | 0.14 (26) | 10.4 (53) | 0.53 (53) | 1 (53) | 1 (213) | 0.42 (149) |
| guardian | 153 | 0.20 (14) | 6.1 (31) | 0.29 (31) | 1 (31) | 1 (150) | 0.33 (109) |
| needs_hands | 6 | 0.19 (2) | 17.3 (6) | 0.41 (6) | 1 (6) | 1 (6) | 3.29 (6) |
| ready | 30 | 0.20 (21) | 2.5 (28) | 0.21 (28) | 2 (28) | 2 (29) | 2.58 (29) |
| not ready | 928 | 0.20 (72) | 7.7 (152) | 0.35 (152) | 1 (152) | 1 (450) | 0.58 (335) |

Today's review median against the insider-only response: rho +0.85 (180). The insider median is 7+ days slower in 45 projects and 30+ days slower in 13. Today's `review_of` counts any review by someone other than the author (bots and other outsiders included), and any merge or close, even a close by the author.

**Reading:**

| Signal | Adds information? | Why |
|---|---|---|
| conversion | **yes** | at most +0.34 with any of today's numbers; it is the outcome itself |
| no_insider_response_share | **yes, keep this one** | −0.76 with acceptance, but it says something acceptance does not ("nunca tiveram resposta"), and it is easy to explain |
| first_insider_response_days | mostly repeats | +0.85 with today's review median and +0.76 with no_resp; keep it only as the replacement for today's review median (45 projects move 7+ days) |
| reviewer_diversity | little | +0.65 with maintainers_24m, +0.67 with active; useful only at 0/1 (single gatekeeper) |
| active_maintainers | **yes** | 115 projects with 0 active are invisible today (`maintainers_24m` counts them as maintained) |
| demand_per_maintainer | **yes, for experienced** | +0.76 with debuts (volume), but its use is "need", which no number on the site covers today |
| outsider_insider_gap | no (too sparse) | 36 projects |
| openness (today's) | hide | +0.03 with conversion; redundant with acceptance on the page |

## 3. Backtest

Setup: signals at T = 2025-09 use only data before 2025-10-01. Outcome: `conversion` at 2026-09. 93 projects have the outcome; pooled over them, 1,355 people debuted and 0.22 came back.

Today's badge was also **rebuilt at T** from `participation`, with every window capped at 2025-09 (`debuts`, `acceptance`, `active` as in `build.py`). Two parts could not be rebuilt and were substituted:

- `response` became `first_insider_response_days@T ≤ 14` and `no_insider_response_share@T ≤ 0.25`, because `review_of` has no time cap;
- `guide` keeps today's value, a small leak.

23 of 856 full projects are ready at T. Of today's 30 ready projects, 18 were also ready at T and 12 only today; 5 were ready at T but are not now.

Spearman with conversion@2026-09, 95% bootstrap CI (1,000 resamples):

| Predictor | n | rho | 95% CI |
|---|---|---|---|
| **Noise ceiling: conversion@T (prior cohort)** | 66 | **+0.45** | [+0.19, +0.64] |
| first_insider_response_days@T | 83 | −0.05 | [−0.26, +0.18] |
| no_insider_response_share@T | 83 | −0.08 | [−0.29, +0.14] |
| outsider_insider_gap@T | 19 | −0.33 | [−0.77, +0.22] |
| reviewer_diversity@T | 83 | +0.22 | [+0.00, +0.41] |
| active_maintainers@T | 93 | +0.11 | [−0.11, +0.31] |
| **demand_per_maintainer@T** | 90 | **−0.27** | [−0.46, −0.07] |
| debuts_12m@T (coupled: equals the cohort) | 93 | −0.13 | [−0.35, +0.09] |
| newcomer acceptance@T (debuts / tried) | 92 | +0.20 | [−0.03, +0.43] |
| outside merges last 3 months@T | 93 | +0.12 | [−0.11, +0.32] |
| badge@T checks passed (0–5) | 93 | +0.10 | [−0.12, +0.31] |
| badge@T ready | 93 | +0.06 | [−0.12, +0.23] |
| today's ready (**concurrent, not a backtest**) | 93 | +0.03 | [−0.17, +0.21] |
| today's acceptance (concurrent, **coupled**) | 89 | +0.34 | [+0.13, +0.53] |
| today's openness (concurrent) | 90 | +0.03 | [−0.18, +0.25] |
| today's review median (concurrent) | 92 | −0.06 | [−0.28, +0.16] |

Conversion@2026-09 by tercile at T. Each cell: mean of repo rates / pooled rate (came back ÷ debuted), then repos and people.

| Predictor @T | Low tercile | Mid | High |
|---|---|---|---|
| no_insider_response_share | 0.00–0.11: 0.22 / 0.21 (27 repos, 409 people) | 0.11–0.29: 0.26 / 0.24 (28, 564) | 0.29–0.70: 0.18 / 0.16 (28, 311) |
| first_insider_response_days | 0–0.8 d: 0.21 / 0.23 (27, 478) | 0.9–6.8 d: 0.28 / 0.24 (28, 460) | 7.1–98.4 d: 0.18 / 0.16 (28, 346) |
| reviewer_diversity | 0–1: 0.22 / 0.19 (27, 324) | 1–2: 0.17 / 0.19 (28, 420) | 2–15: 0.28 / 0.25 (28, 540) |
| active_maintainers | 0–1: 0.24 / 0.22 (31, 310) | 1–2: 0.16 / 0.18 (31, 467) | 2–25: 0.30 / 0.25 (31, 578) |
| demand_per_maintainer | 0.03–2.00: 0.32 / 0.29 (30, 391) | 2.08–4.50: 0.17 / 0.18 (30, 346) | 4.50–20.25: 0.18 / 0.19 (30, 599) |
| conversion (prior cohort) | 0.00–0.12: 0.12 / 0.14 (22, 311) | 0.12–0.22: 0.23 / 0.23 (22, 309) | 0.23–0.80: 0.27 / 0.25 (22, 446) |
| newcomer acceptance | 0.10–0.58: 0.21 / 0.19 (30, 329) | 0.59–0.79: 0.19 / 0.22 (31, 490) | 0.79–1.00: 0.28 / 0.23 (31, 526) |
| debuts_12m (cohort size) | 3–6: 0.29 / 0.31 (31, 178) | 7–14: 0.23 / 0.23 (31, 302) | 14–124: 0.19 / 0.20 (31, 875) |

Groups:

| Grouping | Group | Repos | Mean conv | Pooled | People |
|---|---|---|---|---|---|
| today's ready (concurrent) | yes / no | 21 / 72 | 0.24 / 0.23 | 0.24 / 0.21 | 421 / 934 |
| badge@T ready | yes / no | 21 / 72 | 0.25 / 0.23 | 0.23 / 0.22 | 421 / 934 |
| today's profile (concurrent) | open_door / stable / guardian | 51 / 26 / 14 | 0.26 / 0.20 / 0.21 | 0.23 / 0.19 / 0.20 | 898 / 270 / 156 |
| badge@T check `response` | pass / fail | 50 / 43 | 0.24 / 0.22 | 0.23 / 0.21 | 883 / 472 |
| badge@T check `active` | pass / fail | 68 / 25 | 0.24 / 0.22 | 0.22 / 0.21 | 1,147 / 208 |
| badge@T check `guide` (today's value) | pass / fail | 40 / 53 | 0.24 / 0.23 | 0.23 / 0.21 | 633 / 722 |

Mean conversion, flagged minus the rest (bootstrap 95% CI):

| Flag | Repos | Flagged | Difference | 95% CI |
|---|---|---|---|---|
| badge@T ready | 93 | 21 | +0.025 | [−0.053, +0.106] |
| v1 beginner `good` @T (section 5.1) | 93 | 35 | +0.058 | [−0.014, +0.134] |
| same rule **without** its `conversion ≥ 0.1` clause | 93 | 40 | +0.030 | [−0.044, +0.105] |
| `conversion@T ≥ 0.1` alone | 66 | 51 | **+0.137** | [+0.074, +0.199] |
| today's ready (concurrent) | 93 | 21 | +0.016 | [−0.060, +0.102] |

**Reading, honestly:**

- **Today's badge vs conversion is not a clean backtest.** Its windows (2025-10 to 2026-09) are the same months as the cohort's follow-up, so it describes the same period instead of predicting it. Even so, it separates nothing (+0.016).
- **What signal there is comes from past conversion.** Removing the conversion clause from the v1 rule halves its gap (+0.058 → +0.030). Past conversion alone is the only flag whose CI stays clear of 0.
- **Selection bias.** Conversion exists only where 5+ people debuted, so the backtest ranks open projects against each other. It **cannot** validate a "bad" cut, because closed projects have no cohort. "Bad" and "dados insuficientes" have to come from the coverage and null rules (section 1), not from conversion.
- **Mechanical coupling.** "Came back" means another merged PR or a review. Today's acceptance and debuts are counted over months that include those returns, so today's +0.34 for acceptance is partly the outcome measured early. `debuts_12m@T` *is* the cohort size: bigger cohorts convert less (pooled 0.31 → 0.20), which reads as small-n noise plus big, busy projects, not as a signal.
- **Cross-repo insiders.** Insiders are per repo. Of the 1,328 cohort people in a participation rebuild, 121 (9.1%) were already a merger or direct committer in another of our repos before T; 19 (1.4%) in a repo of the same owner. Where this is 30%+ of the cohort: `pypa/build` 3 of 5, `pillarjs/router` 2 of 6, `jshttp/cookie` 5 of 13, `jshttp/mime-db` 5 of 15, `pypa/packaging` 5 of 15, `browserslist/browserslist` 3 of 9, and 4 more. This inflates conversion, the backtest outcome included.
- **Demand cuts the other way.** More demand per maintainer comes with less conversion: −0.27, with the low tercile at 0.29 pooled against 0.18–0.19 for the other two. One reading: overloaded maintainers do not mentor. It is a lead, not a rule, given the number of tests; do not let demand raise a beginner rating.
- **Response time does not show up in conversion** in this sample. Only the top tercile drops: no-response above 0.29, or insider median above 7 days, gives pooled 0.16 against 0.21–0.24. That matches the methodology's caveat that there is no strong causal evidence for latency. Keep the response thresholds as product choices: a newcomer who never hears back learns nothing.
- **Small n.** At p = 0.2, a 95% interval is ±0.35 with 5 people, ±0.25 with 10, ±0.18 with 20 and ±0.11 with 50.

**What would make it stronger:**

1. **Several T's.** Roll T monthly from 2024-09 to 2025-09 and pool the 13 overlapping cohorts, counting each person once per T, with a cluster-aware CI.
2. **A person-level model.** Fit a logistic model on the 1,355 debuts, with the project's signals as features, instead of 93 repo rates.
3. **Shrink small cohorts** toward the pooled 0.22, e.g. `(back + 0.22·k) / (n + k)` with k = 10, so 0/5 does not read as 0.
4. **Add the sampled projects** (per-author debut search). They are where most newcomer lists point: 31 of the 35 listed projects.
5. **Collect issue comments** (who answered, and when). The first-response-on-issues and "prior interaction" signals need them, and the literature ranks those above PR latency.
6. **An org-level insider class**, so a maintainer from a sibling repo is not counted as a debut who came back.

## 4. Cases where the new signals tell a different story

Columns: today's `profile`, `ready`, `acceptance` (outside PRs accepted, 12m), today's review median (days) | new: conversion (cohort n), insider response median (days), no-insider-response share (outside PRs n), reviewer_diversity, active_maintainers, demand per active maintainer per month.

| Project | Today | New signals | Story |
|---|---|---|---|
| `motdotla/dotenv` | open_door, **ready**, acc 0.21, review 7 d | conv 0.10 (10), insider 7.8 d, no-resp **0.65** (92), rev_div 1, active 1, demand 10.08 | Badge says ready, but two thirds of outside PRs never hear from the maintainer, and 1 of 10 debuts came back. v1 rates it `bad` for beginners. |
| `websocket-client/websocket-client` | open_door, **ready** | insider 12.8 d, no-resp **0.73** (11), rev_div 1 | Ready on 4 debuts; most outside PRs have no insider answer. |
| `tornadoweb/tornado` | needs_hands, **ready**, acc 0.30 | conv 0.13 (15), insider 24.1 d, no-resp 0.44 (57), rev_div 1, demand 7.33 | One reviewer with 7 new items per month: a review path for experienced people rather than a beginner door. |
| `pallets/jinja` | stable, acc **0.00** | conv **0.00** (22), insider **0.0 d**, no-resp 0.15 (118), demand 12.58 | Answers at once, merges nothing: 116 PRs opened in 2026, 0 merged (`cases.sql`). A response signal alone would call this a good door. Same pattern: `pallets/flask`, `pallets/itsdangerous`. |
| `unjs/ofetch` | stable, acc 0.08, review **1 d** | conv 0.20 (5), insider **91.1 d**, no-resp **0.88** (77), rev_div 1, demand 8.08 | Today's review median looks great; the insider-only one is 3 months. |
| `pillarjs/router` | stable, acc 0.00, 0 debuts | conv **0.71** (7), insider 204.8 d, no-resp 1.00 (15) | Two of the cohort are express maintainers, so part of this "came back" is insiders from next door. The door is shut today. |
| `pypa/build` | **stable**, not ready (fails only `guide`) | conv **0.40** (5), insider 0.2 d, no-resp 0.09 (33), rev_div 3, active 3 | Responsive, but the broken `guide` check hides it. Its conversion is inflated: 3 of 5 debuts already maintain other repos. |
| `h3js/h3` | open_door, not ready (fails only `guide`) | conv 0.30 (40), insider 0.4 d, no-resp 0.14 (213), rev_div **1**, demand **24.17** | Good for beginners (v1 `good`), and a clear review path: one reviewer, 24 new items per month. |
| `ipython/ipykernel` | open_door, **ready**, acc 0.79 | conv **0.00** (5), insider 2.7 d, no-resp 0.21 (38), rev_div 4, active 5 | Everything looks right, but 0 of 5 came back. With n = 5 that is within noise (±0.35): show "poucos dados", do not downgrade. |
| `ajv-validator/ajv` | guardian, acc 0.02 | active **0**, insider 97.3 d, no-resp 0.92 (51) | Every insider is on a break while outside PRs keep coming. A "successor" path for experienced people, not a door for anyone else. |
| `huggingface/huggingface.js` | open_door, ready | conv 0.27 (130), no-resp 0.38 (441), rev_div **21** | The opposite of a gatekeeper: 21 insiders review, and conversion is solid on a large cohort. A good reference case. |

## 5. Hypotheses

### 5.1 Candidate thresholds (v1), per level

2026-09 quantiles: no-response median 0.31, p75 0.61; insider response median 6.0 d, p75 22.5 d; demand p25 0.17, p75 2.10. The day cut-offs below (14 and 30) are product choices, looser than the p75: the backtest shows no dose-response for latency. Rules are checked in order; the first that matches wins.

| Level | `insufficient` (dados insuficientes) | `bad` | `good` | `ok` |
|---|---|---|---|---|
| beginner | sampled/truncated; no PRs since 2018; <10 outside PRs | guardian; 0 active maintainers; no-resp > 0.5 or insider median > 30 d | today's `debuts`, `acceptance` and `active` checks pass; no-resp ≤ 0.3; insider median ≤ 14 d; conversion ≥ 0.1 or unknown | the rest |
| intermediate | same | 0 active; no-resp > 0.6 | no-resp ≤ 0.3, insider median ≤ 14 d, outside acceptance ≥ 0.3 | the rest |
| experienced | sampled/truncated; no PRs; no insider; 0 active and 0 outside PRs | no-resp > 0.6, or outside acceptance < 0.1 | demand ≥ p75 (2.10), no-resp ≤ 0.5, acceptance ≥ 0.2 | the rest, including 0 active + outside PRs ("successor wanted") |

`guide` is dropped from `good` until the path bug (section 1) and the community-files fix are in: it is broken, and conversion is 0.23 vs 0.21 pooled with and without it. It stays on the page as a tip.

Result over the 958 projects:

| Level | good | ok | bad | insufficient |
|---|---|---|---|---|
| beginner | 44 | 49 | 272 (150 guardian, 74 no one active, 48 unanswered) | 593 |
| intermediate | 63 | 68 | 154 | 673 |
| experienced | 50 | 345 (73 successor) | 42 | 521 |

Checks:

- **Backtest of the beginner rule at T** (signals@2025-09 and the badge rebuilt at T):

  | Rating | Repos | Pooled conversion | People |
  |---|---|---|---|
  | good | 35 | 0.24 | 712 |
  | ok | 25 | 0.14 | 338 |
  | bad | 25 | 0.21 | 255 |
  | insufficient | 8 | 0.44 | 50 |

  The good-minus-rest gap, +0.058, has a CI that crosses 0, and ok < bad. The scale is not validated yet.
- **Same-period sanity check (circular, because conversion is an input):** beginner good 25 repos → 0.29 pooled; ok 26 → 0.19; bad 38 → 0.19.
- **Today's 30 ready projects under v1:** 17 good, 9 ok, 2 bad (`motdotla/dotenv`, `websocket-client`), 2 insufficient.
- **v1 beginner good by today's profile:** 38 open_door, 5 stable (e.g. `pypa/build`), 1 needs_hands, 0 guardian.
- **Experienced good, highest demand:** `pydantic/httpx2`, `h3js/h3`, `kludex/starlette`, `agronholm/anyio`, `fsspec/filesystem_spec`, `sindresorhus/type-fest`, `shikijs/shiki`. A demand-only rule would also have rated `pallets/jinja`, `pallets/flask` and `textualize/rich` good; requiring acceptance ≥ 0.2 removes them.

These are hypotheses to calibrate, not results. Today the data can defend the **null rules** ("dados insuficientes", "ninguém ativo", "sem resposta do time"), because they come from coverage and counts, not from conversion. The data cannot yet tell `good` from `ok`.

### 5.2 What the project page should show

Five numbers replace the current `BigNumbers` set on the project page; the card keeps 3. Each number shows the count behind it.

| # | Number | Suggested copy (pt-BR) | When n is small | Source |
|---|---|---|---|---|
| 1 | conversion | "**4 de 13** pessoas que estrearam entre out/2024 e set/2025 voltaram a contribuir em até 1 ano" | n < 5: "poucas estreias para medir"; n 5–19: show the counts, no %, plus "poucos dados" | `conversion` |
| 2 | no-response share | "**65%** dos PRs de quem é de fora nunca tiveram resposta de alguém do time" | n < 10: "3 de 5 PRs de fora tiveram resposta do time (poucos dados)" | `no_insider_response_share` |
| 3 | insider response median | "metade dos PRs de fora tem a 1ª resposta do time em até **N dias**" (replaces "até o 1º retorno") | same as #2 | `first_insider_response_days` |
| 4 | newcomer acceptance | "**13 de 30** pessoas novas que abriram PR tiveram aceito" (already in the badge text) | < 5 tried: "poucas pessoas novas tentaram" | today's `acceptance` check |
| 5 | active maintainers and reviewers | "**1 pessoa** do time ativa agora (de 3 nos últimos 2 anos) · **1 pessoa** revisa os PRs de fora" | active = 0: "ninguém do time agiu recentemente" | `active_maintainers`, `reviewer_diversity`, `maintainers_24m` |

For the experienced level, add "cerca de **N** issues e PRs novos por mês para cada pessoa ativa" (`demand_per_maintainer`).

Next to #2 and #3, when acceptance is below 0.1, add: "o time responde, mas quase nada de fora é aceito" (the `pallets/jinja` case).

**Uncertainty:**

- Show counts ("4 de 13") rather than percentages whenever n < 20.
- Add a "poucos dados" tag when n < 10 (PRs) or n < 20 (cohort).
- If conversion is shown as a rate, use the shrunk value (section 3, point 3).
- Never color a number red on n < 10.

**"Dados insuficientes" texts, one per reason:**

- Large repo: "Projeto grande: ainda não medimos quem estreia aqui."
- No PRs: "Não vimos PRs nem commits neste projeto desde 2018."
- < 10 outside PRs: "Poucos PRs de gente de fora no último ano (N) para avaliar a resposta."
- 0 outside PRs: "Ninguém de fora mandou PR no último ano."

**What to hide:**

| Hide | Why |
|---|---|
| `openness` | +0.03 with conversion; next to acceptance it confuses (it is not a measure of the door) |
| `outsider_insider_gap` | 36 projects |
| "PRs de fora parados há 30+ dias" | +0.77 with no-response share, which says the same thing in plainer words |
| today's review median | replaced by #3; it counts bots, other outsiders and the author's own close as answers |
| the scorecard number | keep the link only; it is not about the door |

### 5.3 Entry paths per level the data supports

| Level | Path (`Way`) | Rule (2026-09) | Projects | Example |
|---|---|---|---|---|
| beginner | `code` on newcomer issues | v1 beginner `good` and `newcomer_open` > 0 | 11 (before the new labels) | `fsspec/filesystem_spec` (4 open), `joblib/joblib` (4) |
| beginner/intermediate | `code`, "people come back here" | conversion ≥ 0.3 and no-resp ≤ 0.3 | 12 | `h3js/h3`, `agronholm/anyio`, `python/typing_extensions` |
| experienced | `review` | reviewer_diversity ≤ 1, demand ≥ p75 (2.10), no-resp ≤ 0.5 | 41 | `h3js/h3`, `kludex/starlette`, `sindresorhus/type-fest` |
| experienced | `triage` | demand ≥ p75 and 1–2 active maintainers | 79 | `agronholm/anyio`, `tornadoweb/tornado` |
| experienced | successor (maintenance) | 0 active maintainers, outside PRs still arriving | 73 | `ajv-validator/ajv`, `npm/node-semver` |

- **Review** needs a reviewer who still merges. That is why it requires no-resp ≤ 0.5, the same idea as `build.py` asking for a PR merged in the last 3 months.
- **Successor** should go only to `experienced`, and only next to the dependents count, so the site does not send beginners to an abandoned project.

## 6. Limits

| Question | Why we cannot answer it now | Collection that would |
|---|---|---|
| Who answers issues, and how fast | the raw cache has no comment authors or times | issue comments (deep-analysis §4, new collection) |
| Did newcomers talk before their first PR | same | issue/PR comments per author |
| Do GFI labels work (resolved by a newcomer) | no labels or linked PRs in the cache; newcomer labels incomplete | labels + `closedByPullRequestsReferences` |
| Large projects (102, 31 of the 35 listed) | no per-person debuts | per-author debut search |
| Insiders without merges (private org members) | signals are behavioral only; `repo_assignable` has 2 repos (`microsoft/tslib` 15, `isaacs/inherits` 1) and is not read by `signals.py` | the `people`/assignableUsers step for all repos, then a decision on using it in `run` |
| Cross-repo insiders counted as outsiders | insiders are per repo; 9.1% of the cohort maintain another of our repos (1.4% same owner) | an org/ecosystem-level insider class |
| Abandoned PRs: who went quiet | no event order | timeline events for stale outside PRs |
| Does response time *cause* staying | observational data, one T | several T's + person-level model; still not causal |
| Does the rating help OpenDoor users | no outcome from the site | track debuts of people who came via OpenDoor (opt-in) |

## 7. After the new collection (2026-11-02)

**What ran.** The collection `data-2026-11-02` (data up to October 2026) ran in an integration tree with #108–#112. It added:

- 218 newly collected repos (all Go repos among them);
- `repo_community` (org-level CONTRIBUTING through GraphQL);
- `repo_people` and `repo_assignable` (973 repos, 22,328 assignable logins, 0 capped);
- refreshed `repo_labels`, with the 3 new labels;
- recomputed `repo_signals`, with labels **2026-10** (current) and **2025-10** (T).

Measured effects of the collection itself are in [`analysis-2026-11/collection-2026-11-02.md`](analysis-2026-11/collection-2026-11-02.md). The tables below come from [`analysis.py`](analysis-2026-11/analysis.py) run as `analysis.py <int-tree> 2026-10 2025-10` (output [`out.md`](analysis-2026-11/out.md); sections 1–6 quote [`out-2026-10-31.md`](analysis-2026-11/out-2026-10-31.md)), and from [`after.py`](analysis-2026-11/after.py) (output [`after.out`](analysis-2026-11/after.out); its second argument is the pre-collection `projects.json` saved by the collection run).

**Correction to section 1.** The 216 "no raw file" projects were **never collected** (`activity_fetched_at` NULL, no `repo_monthly` rows). They were not projects without PRs: 207 of them have PRs in the new data. The "Não vimos PRs nem commits" copy in 5.2 applies only to the 34 projects that really have 0 PRs since 2018.

### 7.1 Coverage and distributions, before and after

| | 2026-10-31 data (as_of 2026-09) | 2026-11-02 data (as_of 2026-10) |
|---|---|---|
| projects / computed / sampled | 958 / 639 / 102 | 957 / 845 / 111 |
| conversion has value | 93 (9.7%) | **133 (13.9%)** |
| response signals have value | 180 (18.8%) | **280 (29.3%)** |
| outsider_insider_gap has value | 36 | 48 |
| active_maintainers = 0 | 115 | 131 |
| no_insider_response_share median | 0.31 | **0.42** |
| first_insider_response_days median | 6.0 d | 9.2 d |
| demand_per_maintainer p75 | 2.10 | 2.69 |
| beginner `ready` (site) | 30 | 57 (43 in the pre-collection build of this tree) |

The no-response median rose because the new projects (Go, Kubernetes) merge through bots. With behavioral insiders, nobody there counts as an insider who answers (section 7.3). Redundancy is unchanged:

| Pair | Before | After |
|---|---|---|
| resp_days vs today's review median | +0.85 | +0.88 (280) |
| no_resp vs acceptance | −0.76 | −0.72 (280) |
| rev_div vs active | +0.67 | +0.68 (274) |
| demand vs debuts | +0.76 | +0.78 (504) |
| conversion vs acceptance | +0.34 | +0.26 (129) |

### 7.2 Do the backtest conclusions hold? (133 repos, 1,832 people, pooled 0.22)

| Predictor @T vs conversion@now | 2026-10-31 data | 2026-11-02 data |
|---|---|---|
| noise ceiling: conversion@T | +0.45 [+0.19, +0.64], n 66 | +0.33 [+0.11, +0.54], n 89 |
| demand_per_maintainer@T | −0.27 [−0.46, −0.07], n 90 | **−0.30 [−0.46, −0.12]**, n 124 |
| reviewer_diversity@T | +0.22 [+0.00, +0.41] | +0.19 [+0.00, +0.37] |
| first_insider_response_days@T | −0.05 [−0.26, +0.18] | +0.06 [−0.12, +0.25] |
| no_insider_response_share@T | −0.08 [−0.29, +0.14] | −0.03 [−0.23, +0.15] |
| active_maintainers@T | +0.11 | +0.04 [−0.15, +0.23] |
| debuts_12m@T (coupled) | −0.13 | −0.22 [−0.39, −0.05] |
| today's acceptance (concurrent, coupled) | +0.34 | +0.26 [+0.09, +0.42] |

| Flag, mean conversion flagged minus rest | 2026-10-31 data | 2026-11-02 data |
|---|---|---|
| `conversion@T ≥ 0.1` alone | +0.137 [+0.074, +0.199] | **+0.091 [+0.035, +0.148]** (89 repos, 64 flagged) |
| badge@T ready | +0.025 [−0.053, +0.106] | +0.004 [−0.069, +0.085] (133, 33) |
| v1 beginner `good` @T | +0.058 [−0.014, +0.134] | +0.026 [−0.041, +0.092] (133, 43) |
| v1 without its conversion clause | +0.030 [−0.044, +0.105] | −0.002 [−0.065, +0.064] (133, 52) |
| today's ready (concurrent) | +0.016 | +0.020 [−0.046, +0.090] (133, 35) |

Demand by tercile at T: 0.28 / 0.22 / 0.18 pooled (518 / 476 / 778 people).

v1 beginner rule at T, by rating:

| Rating | Repos | Pooled conversion |
|---|---|---|
| good | 43 | 0.25 |
| ok | 42 | 0.18 |
| bad | 31 | 0.22 |
| insufficient | 17 | 0.32 |

**They hold, with more data:**

- **Past conversion still predicts conversion.** It is still the only flag clear of 0.
- **Demand per maintainer predicts lower conversion.** This is now the most stable signal against conversion: CI clear of 0 on both datasets, and the dose-response by tercile is monotonic.
- **Insider response time and no-response share still do not predict conversion.**
- **Neither today's badge nor v1 beats chance.** Both separate projects less than before, and v1 without past conversion is exactly 0. "Bad" still cannot be validated by conversion, because bad projects have no cohort (section 3).
- **Cross-repo insiders inflate conversion more than before.** They now make up 10.6% of the cohort (190 of 1,789; 1.8% same owner), up from 9.1%. In `kubernetes-sigs/structured-merge-diff`, 10 of the 11 cohort people are mergers elsewhere.

### 7.3 What the three fixes changed

| Fix | Effect | Reading |
|---|---|---|
| Org-level + non-`.md` CONTRIBUTING (#103) | `guide` passes 247 → 443 (196 flips, all False→True). ecosyste.ms-has-it-but-check-fails went 37 → **0**. 155 projects pass with a file ecosyste.ms does not see (inherited from the org's `.github`) | The bug in section 1 is fixed. 75 projects still fail **only** `guide`, and ecosyste.ms finds no contributing file in any of them: they really have none |
| New labels (`beginner-friendly`, `starter`, `low-hanging-fruit`) | 2,995 → 2,994 open newcomer issues, 177 → 178 repos; 3 repos changed | No effect on this set. Keep the labels for new repos; nothing to recalibrate |
| assignableUsers (#108) | 458 assignable logins in 164 repos count as outsiders today, with 4,112 merged PRs in 12 months. Openness falls 0.14 on average in the 105 affected full repos (42 by 0.10+) | Big effect where merges go through bots (see below) |

All 14 newly ready projects flipped on `guide` alone. 7 profiles moved to `open_door` (6 from `stable`, 1 from `needs_hands`): `aio-libs/multidict`, `fastify/fast-uri`, `kludex/python-multipart`, `pyca/pyopenssl`, `sindresorhus/type-fest`, `tox-dev/python-discovery`, `webpack/minimizer-webpack-plugin`. In each case the ready rule promoted the profile.

**Kubernetes shows the insider problem at its worst.** Merges there go through a bot, so with behavioral insiders the projects have **0 maintainers**. Every human PR becomes an "outside" PR, and no human insider ever answers.

| Project | Site today | Insider signals | Assignable |
|---|---|---|---|
| `kubernetes/kube-openapi` | `open_door`, **ready**, openness 1.00, acceptance 0.59 | no-resp **1.00** (75), rev_div 0, active n/a, conversion 0.00 (6) | 644 logins |
| `kubernetes-sigs/structured-merge-diff` | `open_door`, **ready**, openness 1.00, acceptance 0.80 | no-resp **1.00** (35), rev_div 0, conversion 0.455 (11), 10 of 11 already mergers elsewhere | 450 |
| `kubernetes/klog` | `open_door`, openness 1.00 | no-resp 0.917 (12) | 633 |
| `kubernetes/utils` | `open_door`, openness 0.71 | no-resp 0.90 (20) | 650 |

Two of the 57 ready badges are false positives of this kind; v1 rates both `bad` for beginners. With assignable as insider, openness would drop to 0.14 and 0.04 (collection report).

**Mastodon** (sampled, so no signals): 20 assignable logins. One of them has 257 merged PRs in 12 months and never merges. The behavioral outsider share on the sample drops from 0.25 to 0.09 if assignable logins count as insiders.

### 7.4 Recommendation: should the insider rule include assignableUsers?

**Yes for "who answers / who reviews / who maintains". No for "who debuted".**

1. **Use assignable logins as insiders in `run`** for these signals:
   - `first_insider_response_days`, `no_insider_response_share`, `reviewer_diversity`, `active_maintainers`, `demand_per_maintainer`;
   - in `build.py`, for openness and `maintainers_24m`.

   It fixes the bot-merged projects (Kubernetes), the "member who never merges" (Mastodon) and the 458 hidden insiders.
2. **Do not use today's list to remove debuts or to define the conversion cohort.** It is today's list: a newcomer who did well becomes a member later (Kubernetes promotes contributors to org members after a few PRs), so excluding them would erase exactly the successes we count. 88 of the 1,789 people in the conversion cohort (4.9%) are assignable today, and so are 114 of the 3,587 debuts of the last 12 months in full repos (84 repos). That share is small, which also shows how often debuts later get access.
3. **The backtest must stay behavioral** (as `signals.py` does now). For a past T, use assignable only if a snapshot from before T exists; start keeping one per monthly collection (`repo_assignable` with `fetched_at`).
4. **Huge orgs.** Kubernetes lists 437–774 assignable logins per repo, which is the whole org. As insiders, that is right for "did a human insider answer", but it makes `active_maintainers` and `demand_per_maintainer` meaningless. Count only assignable logins who **acted** in the repo (reviewed, merged or closed) in 24 months.

### 7.5 The 14 newly ready projects: which to trust

All 14 flipped on `guide` only (10 of them through an inherited org-level CONTRIBUTING). Columns: debuts in 12 months (how many are assignable today), outside acceptance, conversion (cohort n), insider response median, no-response share (outside PRs n), reviewer_diversity, v1 beginner rating.

| Project | Debuts (assign.) | Acc. | Conv (n) | Resp d | No-resp (n) | Rev | v1 | Verdict |
|---|---|---|---|---|---|---|---|---|
| `sindresorhus/type-fest` | 19 (0) | 0.32 | 0.27 (37) | 0.5 | 0.19 (93) | 2 | good | **trust**: large cohort, fast answers, 5 open newcomer issues |
| `pypa/packaging` | 30 (4) | 0.62 | 0.29 (14) | 1.1 | 0.22 (209) | 4 | good | **trust**, but 6 of its 14 cohort people maintain other repos: conversion is inflated |
| `aio-libs/multidict` | 13 (2) | 0.70 | – (4) | 10.4 | 0.12 (43) | 4 | good | **trust** |
| `expressjs/body-parser` | 9 (2) | 0.65 | – (4) | 1.4 | 0.23 (26) | 3 | good | **trust** |
| `fastify/fast-uri` | 4 (1) | 0.54 | – (1) | 3.9 | 0.00 (13) | 4 | good | **trust**, few debuts |
| `antfu-collective/package-manager-detector` | 9 (1) | 0.56 | 0.25 (12) | 5.7 | 0.22 (18) | 2 | good | **trust** |
| `aio-libs/propcache` | 7 (1) | 0.92 | 0.57 (7) | 0.7 | 0.00 (12) | 3 | good | **trust, "poucos dados"** (12 PRs, cohort 7) |
| `kludex/python-multipart` | 6 (0) | 0.46 | – (2) | 11.4 | 0.11 (28) | 1 | good | **trust, with a caveat**: one reviewer and one active maintainer |
| `tox-dev/python-discovery` | 9 (0) | 0.89 | – (0) | 0.1 | 0.00 (18) | 1 | good | plausible, "poucos dados": one reviewer, no cohort yet |
| `webpack/minimizer-webpack-plugin` | 3 (1) | 0.25 | – (1) | 2.1 | 0.17 (12) | 1 | good | plausible, "poucos dados": 3 debuts, 12 outside PRs, one reviewer |
| `pyca/pyopenssl` | 6 (0) | 0.50 | – (4) | 0.1 | **0.43** (14) | 3 | ok | **don't badge**: 43% of outside PRs never get an insider answer |
| `aio-libs/frozenlist` | 6 (1) | 0.39 | – (4) | **25.3** | **0.50** (18) | 2 | ok | **don't badge**: half of outside PRs never get an insider answer, median 25 days |
| `aio-libs/yarl` | 15 (3) | 0.42 | 0.20 (10) | **35.8** | **0.45** (65) | 4 | bad | **don't badge** |
| `privatenumber/get-tsconfig` | 7 (0) | 1.00 | – (1) | – | – (9) | – | insufficient | **don't badge**: 9 outside PRs, too few to read the response |

So: 8 to trust, 2 plausible with a "poucos dados" tag, 4 that the badge should not carry. The badge alone cannot tell them apart, because it shares the `guide` and `response` checks with all of them. The no-response share against insiders is what separates them.

Across all 57 ready projects under v1: 32 good, 15 ok, 7 bad, 3 insufficient.

- The 7 bad: `aio-libs/yarl`, `bytedance/sonic` (no-resp 0.60), `google/brotli` (0.52), `kubernetes-sigs/structured-merge-diff` (1.00), `kubernetes/kube-openapi` (1.00), `motdotla/dotenv`, `pyparsing/pyparsing`.
- The 3 insufficient: `jaredwray/cacheable`, `narwhals-dev/narwhals` (sampled), `privatenumber/get-tsconfig`.

### 7.6 v1 counts on the new data

| Level | good | ok | bad | insufficient |
|---|---|---|---|---|
| beginner | 62 | 74 | 304 (133 guardian, 88 nobody active, 83 unanswered) | 517 (371 <10 outside PRs, 112 large, 34 no PRs) |
| intermediate | 84 | 97 | 189 | 587 |
| experienced | 69 | 450 (93 successor) | 72 | 366 |

Entry paths (rules in 5.3, p75 demand now 2.69):

| Path | Before | After |
|---|---|---|
| review | 41 | 55 |
| triage | 79 | 105 |
| successor | 73 | 93 |
| "people come back" | 12 | 18 |
| beginner code on newcomer issues | 11 | 17 |

New examples: `prometheus/client_golang` (20 open newcomer issues), `valyala/fasthttp` (14), `yaml/go-yaml`.

## Pending: after the new collection

**Status (2026-11-02):** steps 1–3 below ran in the integration collection; results in section 7. In step 1, #103 (`repo_community`) supersedes the `%CONTRIBUTING.md` pattern fix. Step 2 now has a recommendation (7.4) instead of a re-run. Step 4 is still pending.

Built but not run yet: the community-files fix (org-level CONTRIBUTING through GraphQL), the `people`/assignableUsers step, and the new newcomer labels (`beginner-friendly`, `starter`, `low-hanging-fruit`). Re-run `analysis.py <worktree> <now> <T>` after each step, in this order.

1. **Community files.** Run `collect.py` (files step), then `python pipeline/build.py`. Also fix the `%CONTRIBUTING.md` pattern in `build.py`, or the 37 mismatches will remain. Then re-run:
   - script section 1: the CONTRIBUTING vs ecosyste.ms table, the mismatch file list and the "only failing check is `guide`" list (today 55);
   - script section 3: the row "badge@T check guide";
   - script section 6: the v1 counts. Then decide whether `guide` goes back into beginner `good`.
2. **`people` / assignableUsers.** Today `signals.py` uses behavioral insiders only, in both windows. If `run` starts reading `repo_assignable`, then after `python pipeline/signals.py run` re-run:
   - script section 1: the per-signal coverage table (the insider set grows, the outside-PR n shrinks);
   - script section 2: quantiles, the Spearman table and the review-median vs insider-response line;
   - script section 4: the case candidates (check `huggingface/huggingface.js` and `microsoft/tslib`);
   - script sections 5 and 6: the entry-path and v1 counts;
   - script section 7: the cross-repo insider share.

   Keep the backtest behavioral, or it leaks the future. Before re-running, keep a copy of today's rows (`CREATE TABLE repo_signals_2026_11 AS SELECT * FROM repo_signals` in a scratch copy of the DB) so they can be compared per project.
3. **New labels.** Run `collect.py` (labels step), then `build.py`. Re-run:
   - script section 2: the `newcomer_open` column;
   - the last two lines the script prints, i.e. the entry-path lists (beginner `code` on newcomer issues: today 11).
4. **Next monthly collection (2026-10).** `python pipeline/signals.py backtest` adds T = 2025-10. Re-run script sections 3 and 7, and pool both T's (point 1 of "What would make it stronger").
