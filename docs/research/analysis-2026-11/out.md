## 1. Coverage

projects.json: 958 projects; repo_signals repos: 650; non-canonical repos in repo_signals but not in projects.json: 11

| Stage | Projects |
|---|---|
| computed | 639 |
| full, no raw activity file | 216 |
| sampled (large) | 102 |
| truncated | 1 |

No raw file, PRs opened (repo_monthly):
| Group | Projects |
|---|---|
| 0 PRs ever since 2018 | 216 |
| PRs ever but 0 in last 12 months | 0 |
| 1+ PRs in last 12 months | 0 |

No raw file, by profile: {'stable': 216} 

Per signal at 2026-09 among the computed projects (denominator for % = all 958 projects):
| Signal | min n | computed | n = 0 | 0 < n < min | has value | % of 958 | has value @2025-09 |
|---|---|---|---|---|---|---|---|
| conversion | 5 | 639 | 331 | 215 | 93 | 9.7% | 102 |
| first_insider_response_days | 10 | 639 | 196 | 263 | 180 | 18.8% | 122 |
| no_insider_response_share | 10 | 639 | 196 | 263 | 180 | 18.8% | 122 |
| outsider_insider_gap | 10 | 639 | 518 | 85 | 36 | 3.8% | 23 |
| reviewer_diversity | 10 | 639 | 196 | 263 | 180 | 18.8% | 122 |
| active_maintainers | 1 | 639 | 160 | 0 | 479 | 50.0% | 480 |
| demand_per_maintainer | 1 | 639 | 275 | 0 | 364 | 38.0% | 360 |

Computed projects by outside PRs in 12 months (n of first_insider_response_days) and profile:
| outside PRs 12m | projects | open_door | stable | guardian | needs_hands | ready | has conversion |
|---|---|---|---|---|---|---|---|
| 0 | 196 | 0 | 149 | 47 | 0 | 0 | 0 |
| 1-9 | 263 | 20 | 171 | 72 | 0 | 1 | 7 |
| 10-29 | 92 | 40 | 32 | 17 | 3 | 9 | 22 |
| 30-99 | 62 | 34 | 15 | 10 | 3 | 14 | 41 |
| 100+ | 26 | 16 | 6 | 4 | 0 | 5 | 23 |

Conversion cohort size (n) among computed projects at 2026-09:
| cohort n | projects |
|---|---|
| 0 | 331 |
| 1-4 | 215 |
| 5-9 | 45 |
| 10-29 | 39 |
| 30+ | 9 |

Sampled projects by profile: {'open_door': 76, 'stable': 23, 'guardian': 3} | ready: 0 

Projects in an external newcomer list: 35; by stage: {'sampled (large)': 31, 'full, no raw activity file': 2, 'computed': 2}; with conversion@2026-09: 1; ready: 0

CONTRIBUTING: today's guide check vs ecosyste.ms files.contributing (projects with an ecosyste.ms record):
|  | eco has | eco missing |
|---|---|---|
| guide check ok | 239 | 3 |
| guide check fails | 37 | 645 |

Projects whose only failing beginner check is `guide`: 55 (of them eco sees a CONTRIBUTING: 8): ['agronholm/anyio', 'ai/nanoid', 'aio-libs/frozenlist', 'aio-libs/multidict', 'aio-libs/propcache', 'aio-libs/yarl', 'antfu-collective/package-manager-detector', 'brianc/node-postgres', 'browserslist/browserslist', 'browserslist/update-db', 'celery/billiard', 'celery/kombu', 'celery/py-amqp', 'certifi/python-certifi', 'eslint/js', 'expressjs/body-parser', 'fastify/fast-uri', 'fsspec/filesystem_spec', 'guybedford/es-module-lexer', 'h3js/crossws', 'h3js/h3', 'horejsek/python-fastjsonschema', 'immerjs/immer', 'jd/tenacity', 'joblib/joblib', 'joblib/threadpoolctl', 'jshttp/content-disposition', 'juliangruber/brace-expansion', 'jupyter-server/jupyter_server', 'jupyterlab/jupyter-builder', 'kaelzhang/node-ignore', 'ljharb/qs', 'lxml/lxml', 'mrabarnett/mrab-regex', 'msgpack/msgpack-python', 'nucleic/kiwi', 'pillarjs/path-to-regexp', 'pyca/pyopenssl', 'pypa/build', 'pypa/packaging', 'pytest-dev/pluggy', 'python-cffi/cffi', 'python-poetry/tomlkit', 'rich-harris/magic-string', 'rolldown/plugins', 'scrapy/cssselect', 'sindresorhus/p-limit', 'sindresorhus/type-fest', 'standard-schema/standard-schema', 'sveltejs/devalue', 'tinylibs/tinyexec', 'unjs/magicast', 'unjs/radix3', 'webpack/enhanced-resolve', 'whitequark/ipaddr.js']

## 2. Distributions

| Signal | as_of | n repos | p10 | p25 | p50 | p75 | p90 | mean |
|---|---|---|---|---|---|---|---|---|
| conversion | 2026-09 | 93 | 0.00 | 0.10 | 0.20 | 0.31 | 0.50 | 0.23 |
| conversion | 2025-09 | 102 | 0.00 | 0.11 | 0.18 | 0.28 | 0.40 | 0.21 |
| first_insider_response_days | 2026-09 | 180 | 0.20 | 1.08 | 6.00 | 22.52 | 46.62 | 18.92 |
| first_insider_response_days | 2025-09 | 122 | 0.11 | 0.60 | 3.15 | 25.48 | 63.78 | 21.74 |
| no_insider_response_share | 2026-09 | 180 | 0.07 | 0.17 | 0.31 | 0.61 | 0.88 | 0.40 |
| no_insider_response_share | 2025-09 | 122 | 0.06 | 0.10 | 0.23 | 0.44 | 0.68 | 0.30 |
| outsider_insider_gap | 2026-09 | 36 | -0.36 | -0.07 | 0.08 | 0.29 | 0.48 | 0.08 |
| outsider_insider_gap | 2025-09 | 23 | -0.44 | -0.06 | 0.01 | 0.18 | 0.33 | 0.02 |
| reviewer_diversity | 2026-09 | 180 | 0.00 | 1.00 | 1.00 | 2.00 | 3.00 | 1.57 |
| reviewer_diversity | 2025-09 | 122 | 1.00 | 1.00 | 1.00 | 2.00 | 3.00 | 1.80 |
| active_maintainers | 2026-09 | 479 | 0.00 | 1.00 | 1.00 | 1.00 | 3.00 | 1.26 |
| active_maintainers | 2025-09 | 480 | 0.00 | 0.75 | 1.00 | 1.00 | 2.00 | 1.19 |
| demand_per_maintainer | 2026-09 | 364 | 0.07 | 0.17 | 0.75 | 2.10 | 5.91 | 2.32 |
| demand_per_maintainer | 2025-09 | 360 | 0.08 | 0.22 | 0.67 | 1.93 | 4.32 | 1.61 |

demand_per_maintainer NULL split: active_maintainers = 0: 115 | no insider at all: 160 

reviewer_diversity@2026-09 counts: [(0, 38), (1, 77), (2, 29), (3, 19), (4, 11), (5, 4), (6, 1), (21, 1)] 

active_maintainers@2026-09 counts: [(0, 115), (1, 258), (2, 49), (3, 28), (4, 17), (5, 4), (6, 3), (7, 2), (9, 1), (15, 1), (21, 1)] 

active_maintainers = 0 but insiders > 0 @2026-09: 115 

Spearman, pairwise complete, signals @2026-09 and today's numbers (rho / n):

|  | conv | resp_days | no_resp | gap | rev_div | active | demand | open | accept | debuts | rev_med | stale | maint24 | gfi_open | ready |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| conv | · | -0.13 (86) | -0.09 (86) | -0.24 (27) | +0.16 (86) | +0.20 (93) | -0.41 (91) | +0.03 (90) | +0.34 (89) | -0.15 (93) | -0.06 (92) | +0.02 (92) | +0.26 (93) | -0.05 (93) | +0.03 (93) |
| resp_days | -0.13 (86) | · | +0.76 (180) | -0.29 (36) | -0.22 (180) | -0.06 (177) | -0.02 (167) | -0.02 (163) | -0.49 (180) | -0.26 (180) | +0.85 (180) | +0.71 (180) | +0.05 (180) | +0.29 (180) | -0.21 (180) |
| no_resp | -0.09 (86) | +0.76 (180) | · | -0.04 (36) | -0.28 (180) | -0.17 (177) | +0.15 (167) | -0.13 (163) | -0.76 (180) | -0.36 (180) | +0.68 (180) | +0.77 (180) | -0.06 (180) | +0.22 (180) | -0.20 (180) |
| gap | -0.24 (27) | -0.29 (36) | -0.04 (36) | · | -0.07 (36) | -0.01 (36) | -0.03 (36) | +0.05 (36) | -0.39 (36) | -0.16 (36) | +0.11 (36) | +0.17 (36) | -0.07 (36) | -0.18 (36) | -0.10 (36) |
| rev_div | +0.16 (86) | -0.22 (180) | -0.28 (180) | -0.07 (36) | · | +0.67 (177) | -0.14 (167) | +0.23 (163) | +0.39 (180) | +0.52 (180) | -0.25 (180) | -0.11 (180) | +0.65 (180) | +0.13 (180) | +0.30 (180) |
| active | +0.20 (93) | -0.06 (177) | -0.17 (177) | -0.01 (36) | +0.67 (177) | · | +0.12 (364) | +0.08 (285) | +0.27 (238) | +0.50 (479) | -0.17 (263) | -0.07 (263) | +0.61 (479) | +0.16 (479) | +0.28 (479) |
| demand | -0.41 (91) | -0.02 (167) | +0.15 (167) | -0.03 (36) | -0.14 (167) | +0.12 (364) | · | +0.41 (259) | -0.16 (211) | +0.76 (364) | -0.09 (229) | +0.14 (229) | +0.22 (364) | +0.28 (364) | +0.25 (364) |

Median of each signal @2026-09 by today's profile (value / n):
| group | projects | conv | resp_days | no_resp | gap | rev_div | active | demand |
|---|---|---|---|---|---|---|---|---|
| open_door | 187 | 0.20 (51) | 4.15 (90) | 0.24 (90) | 0.03 (27) | 2.00 (90) | 2.00 (110) | 1.90 (100) |
| stable | 612 | 0.14 (26) | 10.40 (53) | 0.53 (53) | 0.19 (8) | 1.00 (53) | 1.00 (213) | 0.42 (149) |
| guardian | 153 | 0.20 (14) | 6.10 (31) | 0.29 (31) | 0.54 (1) | 1.00 (31) | 1.00 (150) | 0.33 (109) |
| needs_hands | 6 | 0.19 (2) | 17.30 (6) | 0.41 (6) | - (0) | 1.00 (6) | 1.00 (6) | 3.29 (6) |
| ready=True | 30 | 0.20 (21) | 2.45 (28) | 0.21 (28) | 0.04 (14) | 2.00 (28) | 2.00 (29) | 2.58 (29) |
| ready=False | 928 | 0.20 (72) | 7.70 (152) | 0.35 (152) | 0.16 (22) | 1.00 (152) | 1.00 (450) | 0.58 (335) |

review.median_days (any non-author reviewer) vs first_insider_response_days: rho +0.85, n 180; insider median > today's by 7+ days: 45; by 30+ days: 13

## 3. Backtest

Noise ceiling: conversion@2025-09 vs conversion@2026-09: rho +0.45 [+0.19, +0.64], n 66

Spearman with conversion@2026-09 (cohort debuted 2024-10..2025-09, followed 12 months), 95% bootstrap CI (1000):
| Predictor | n | rho | 95% CI |
|---|---|---|---|
| first_insider_response_days@T | 83 | -0.05 | [-0.26, +0.18] |
| no_insider_response_share@T | 83 | -0.08 | [-0.29, +0.14] |
| outsider_insider_gap@T | 19 | -0.33 | [-0.77, +0.22] |
| reviewer_diversity@T | 83 | +0.22 | [+0.00, +0.41] |
| active_maintainers@T | 93 | +0.11 | [-0.11, +0.31] |
| demand_per_maintainer@T | 90 | -0.27 | [-0.46, -0.07] |
| conversion@T (prior cohort) | 66 | +0.45 | [+0.19, +0.64] |
| debuts_12m@T (= cohort size, coupled) | 93 | -0.13 | [-0.35, +0.09] |
| newcomer acceptance@T (debuts/tried, 5+ tried) | 92 | +0.20 | [-0.03, +0.43] |
| outside merges last 3m@T | 93 | +0.12 | [-0.11, +0.32] |
| badge@T checks passed (0-5) | 93 | +0.10 | [-0.12, +0.31] |
| badge@T ready (0/1) | 93 | +0.06 | [-0.12, +0.23] |
| TODAY ready (concurrent, not a backtest) | 93 | +0.03 | [-0.17, +0.21] |
| TODAY openness (concurrent) | 90 | +0.03 | [-0.18, +0.25] |
| TODAY acceptance (concurrent) | 89 | +0.34 | [+0.13, +0.53] |
| TODAY review_median_days (concurrent) | 92 | -0.06 | [-0.28, +0.16] |

Conversion@2026-09 by tercile of each predictor (mean of repo rates; pooled = sum came back / sum cohort):
| Predictor | tercile | repos | range | mean conv | pooled conv | cohort people |
|---|---|---|---|---|---|---|
| first_insider_response_days@T | low | 27 | 0.00–0.80 | 0.21 | 0.23 | 478 |
| first_insider_response_days@T | mid | 28 | 0.90–6.80 | 0.28 | 0.24 | 460 |
| first_insider_response_days@T | high | 28 | 7.10–98.40 | 0.18 | 0.16 | 346 |
| no_insider_response_share@T | low | 27 | 0.00–0.11 | 0.22 | 0.21 | 409 |
| no_insider_response_share@T | mid | 28 | 0.11–0.29 | 0.26 | 0.24 | 564 |
| no_insider_response_share@T | high | 28 | 0.29–0.70 | 0.18 | 0.16 | 311 |
| outsider_insider_gap@T | low | 6 | -0.79–-0.05 | 0.26 | 0.25 | 221 |
| outsider_insider_gap@T | mid | 6 | -0.03–0.11 | 0.23 | 0.23 | 116 |
| outsider_insider_gap@T | high | 7 | 0.14–0.30 | 0.18 | 0.15 | 97 |
| reviewer_diversity@T | low | 27 | 0.00–1.00 | 0.22 | 0.19 | 324 |
| reviewer_diversity@T | mid | 28 | 1.00–2.00 | 0.17 | 0.19 | 420 |
| reviewer_diversity@T | high | 28 | 2.00–15.00 | 0.28 | 0.25 | 540 |
| active_maintainers@T | low | 31 | 0.00–1.00 | 0.24 | 0.22 | 310 |
| active_maintainers@T | mid | 31 | 1.00–2.00 | 0.16 | 0.18 | 467 |
| active_maintainers@T | high | 31 | 2.00–25.00 | 0.30 | 0.25 | 578 |
| demand_per_maintainer@T | low | 30 | 0.03–2.00 | 0.32 | 0.29 | 391 |
| demand_per_maintainer@T | mid | 30 | 2.08–4.50 | 0.17 | 0.18 | 346 |
| demand_per_maintainer@T | high | 30 | 4.50–20.25 | 0.18 | 0.19 | 599 |
| conversion@T (prior cohort) | low | 22 | 0.00–0.12 | 0.12 | 0.14 | 311 |
| conversion@T (prior cohort) | mid | 22 | 0.12–0.22 | 0.23 | 0.23 | 309 |
| conversion@T (prior cohort) | high | 22 | 0.23–0.80 | 0.27 | 0.25 | 446 |
| debuts_12m@T (= cohort size, coupled) | low | 31 | 3.00–6.00 | 0.29 | 0.31 | 178 |
| debuts_12m@T (= cohort size, coupled) | mid | 31 | 7.00–14.00 | 0.23 | 0.23 | 302 |
| debuts_12m@T (= cohort size, coupled) | high | 31 | 14.00–124.00 | 0.19 | 0.20 | 875 |
| newcomer acceptance@T (debuts/tried, 5+ tried) | low | 30 | 0.10–0.58 | 0.21 | 0.19 | 329 |
| newcomer acceptance@T (debuts/tried, 5+ tried) | mid | 31 | 0.59–0.79 | 0.19 | 0.22 | 490 |
| newcomer acceptance@T (debuts/tried, 5+ tried) | high | 31 | 0.79–1.00 | 0.28 | 0.23 | 526 |
| outside merges last 3m@T | low | 31 | 0.00–2.00 | 0.24 | 0.23 | 260 |
| outside merges last 3m@T | mid | 31 | 2.00–7.00 | 0.21 | 0.18 | 313 |
| outside merges last 3m@T | high | 31 | 7.00–55.00 | 0.25 | 0.23 | 782 |
| badge@T checks passed (0-5) | low | 31 | 2.00–3.00 | 0.24 | 0.21 | 320 |
| badge@T checks passed (0-5) | mid | 31 | 3.00–4.00 | 0.22 | 0.23 | 457 |
| badge@T checks passed (0-5) | high | 31 | 4.00–5.00 | 0.23 | 0.22 | 578 |

Conversion@2026-09 by badge / profile group:
| Grouping | group | repos | mean conv | pooled conv | cohort people |
|---|---|---|---|---|---|
| TODAY ready (concurrent) | 1 | 21 | 0.24 | 0.24 | 421 |
| TODAY ready (concurrent) | 0 | 72 | 0.23 | 0.21 | 934 |
| badge@T ready | 1 | 21 | 0.25 | 0.23 | 421 |
| badge@T ready | 0 | 72 | 0.23 | 0.22 | 934 |
| TODAY profile (concurrent) | open_door | 51 | 0.26 | 0.23 | 898 |
| TODAY profile (concurrent) | stable | 26 | 0.20 | 0.19 | 270 |
| TODAY profile (concurrent) | guardian | 14 | 0.21 | 0.20 | 156 |
| TODAY profile (concurrent) | needs_hands | 2 | 0.19 | 0.19 | 31 |
| badge@T check debuts | 1 | 93 | 0.23 | 0.22 | 1355 |
| badge@T check acceptance | 1 | 90 | 0.23 | 0.22 | 1322 |
| badge@T check acceptance | 0 | 3 | 0.23 | 0.21 | 33 |
| badge@T check active | 1 | 68 | 0.24 | 0.22 | 1147 |
| badge@T check active | 0 | 25 | 0.22 | 0.21 | 208 |
| badge@T check response | 1 | 50 | 0.24 | 0.23 | 883 |
| badge@T check response | 0 | 43 | 0.22 | 0.21 | 472 |
| badge@T check guide | 1 | 40 | 0.24 | 0.23 | 633 |
| badge@T check guide | 0 | 53 | 0.23 | 0.21 | 722 |

badge@T ready overall: Counter({0: 833, 1: 23}) | today ready vs badge@T ready (both, today only, T only): 18 12 5 

## 4. Case candidates

**ready but >= 30% of outside PRs never got an insider response** (10)

| repo | profile | ready | open | accept | debuts | rev_med | conv(n) | resp_days | no_resp(n) | rev_div | active | demand | gap |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| websocket-client/websocket-client | open_door | 1 | 0.21 | 0.36 | 4 | 9 | - (3) | 12.80 | 0.73 (11) | 1.00 | 1.00 | 2.00 | - |
| motdotla/dotenv | open_door | 1 | 0.12 | 0.21 | 18 | 7 | 0.10 (10) | 7.80 | 0.65 (92) | 1.00 | 1.00 | 10.08 | - |
| google/brotli | open_door | 1 | 0.56 | 0.32 | 14 | 9 | 0.31 (13) | 7.90 | 0.49 (63) | 1.00 | 1.00 | 8.50 | - |
| tornadoweb/tornado | needs_hands | 1 | 0.21 | 0.30 | 13 | 13 | 0.13 (15) | 24.10 | 0.44 (57) | 1.00 | 1.00 | 7.33 | - |
| huggingface/huggingface.js | open_door | 1 | 0.30 | 0.44 | 149 | 0 | 0.27 (130) | 1.70 | 0.38 (441) | 21.00 | 21.00 | 2.04 | -0.01 |
| prometheus/client_python | open_door | 1 | 0.85 | 0.56 | 16 | 8 | 0.19 (16) | 6.10 | 0.38 (50) | 1.00 | 2.00 | 2.67 | - |
| pydantic/httpx2 | open_door | 1 | 0.30 | 0.58 | 25 | 0 | - (0) | 2.80 | 0.36 (105) | 1.00 | 2.00 | 42.75 | -0.66 |
| protobufjs/protobuf.js | open_door | 1 | 0.11 | 0.44 | 13 | 0 | - (4) | 4.60 | 0.32 (37) | 2.00 | 2.00 | 3.17 | - |
| vega/altair | open_door | 1 | 0.26 | 0.62 | 21 | 5 | 0.17 (6) | 2.20 | 0.31 (55) | 4.00 | 4.00 | 2.19 | -0.06 |
| kpdecker/jsdiff | open_door | 1 | 0.16 | 0.50 | 4 | 2 | - (3) | 2.30 | 0.30 (10) | 1.00 | 1.00 | 2.58 | - |

**ready, conversion known** (21)

| repo | profile | ready | open | accept | debuts | rev_med | conv(n) | resp_days | no_resp(n) | rev_div | active | demand | gap |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ipython/ipykernel | open_door | 1 | 0.39 | 0.79 | 16 | 3 | 0.00 (5) | 2.70 | 0.21 (38) | 4.00 | 5.00 | 1.13 | -0.06 |
| jaredwray/cacheable | open_door | 1 | 0.02 | 0.86 | 6 | 0 | 0.08 (26) | - | - (7) | - | 1.00 | 3.58 | - |
| nltk/nltk | open_door | 1 | 0.36 | 0.65 | 44 | 0 | 0.08 (13) | 5.80 | 0.15 (208) | 3.00 | 4.00 | 5.88 | 0.05 |
| motdotla/dotenv | open_door | 1 | 0.12 | 0.21 | 18 | 7 | 0.10 (10) | 7.80 | 0.65 (92) | 1.00 | 1.00 | 10.08 | - |
| reduxjs/redux-toolkit | open_door | 1 | 0.42 | 0.58 | 32 | 3 | 0.10 (20) | 3.60 | 0.22 (106) | 4.00 | 5.00 | 3.65 | 0.24 |
| tornadoweb/tornado | needs_hands | 1 | 0.21 | 0.30 | 13 | 13 | 0.13 (15) | 24.10 | 0.44 (57) | 1.00 | 1.00 | 7.33 | - |
| postcss/postcss | open_door | 1 | 0.21 | 0.69 | 22 | 0 | 0.15 (13) | 0.10 | 0.12 (51) | 1.00 | 1.00 | 6.50 | - |
| vega/altair | open_door | 1 | 0.26 | 0.62 | 21 | 5 | 0.17 (6) | 2.20 | 0.31 (55) | 4.00 | 4.00 | 2.19 | -0.06 |
| microsoft/debugpy | open_door | 1 | 0.54 | 0.85 | 13 | 0 | 0.19 (16) | 0.00 | 0.03 (33) | 2.00 | 3.00 | 1.92 | - |
| prometheus/client_python | open_door | 1 | 0.85 | 0.56 | 16 | 8 | 0.19 (16) | 6.10 | 0.38 (50) | 1.00 | 2.00 | 2.67 | - |
| nodejs/node-addon-api | open_door | 1 | 0.50 | 1 | 5 | 1 | 0.20 (5) | 1.10 | 0.08 (12) | 2.00 | 2.00 | 1.17 | - |
| styled-components/styled-components | open_door | 1 | 0.07 | 0.63 | 9 | 0 | 0.20 (10) | 9.50 | 0.21 (19) | 1.00 | 1.00 | 6.58 | -0.65 |

**stable/guardian with conversion >= 0.4** (7)

| repo | profile | ready | open | accept | debuts | rev_med | conv(n) | resp_days | no_resp(n) | rev_div | active | demand | gap |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pillarjs/router | stable | 0 | - | 0.00 | 0 | 24 | 0.71 (7) | 204.80 | 1.00 (15) | 0.00 | 2.00 | 0.79 | - |
| mongodb-js/devtools-shared | stable | 0 | 0.05 | 0.35 | 4 | 0 | 0.70 (10) | 4.80 | 0.55 (20) | 3.00 | 15.00 | 0.12 | -0.05 |
| expressjs/serve-static | guardian | 0 | 0.50 | 0.38 | 0 | 14 | 0.60 (5) | - | - (8) | - | 0.00 | - | - |
| langchain-ai/agent-protocol | stable | 0 | 0.00 | - | 0 | 26 | 0.57 (7) | - | - (4) | - | 4.00 | 0.15 | - |
| aio-libs/aiohappyeyeballs | stable | 0 | 0.07 | - | 0 | - | 0.40 (5) | - | - (2) | - | 2.00 | 0.33 | - |
| pypa/build | stable | 0 | 0.14 | 0.64 | 15 | 0 | 0.40 (5) | 0.20 | 0.09 (33) | 3.00 | 3.00 | 1.86 | 0.11 |
| pyparsing/pyparsing | stable | 0 | 0.09 | 0.46 | 13 | 15 | 0.40 (5) | 8.60 | 0.44 (39) | 1.00 | 1.00 | 4.50 | - |

**open_door with no_insider_response_share >= 0.4** (27)

| repo | profile | ready | open | accept | debuts | rev_med | conv(n) | resp_days | no_resp(n) | rev_div | active | demand | gap |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| omnilib/aiosqlite | open_door | 0 | 0.57 | 0.36 | 4 | 25 | - (2) | 36.80 | 0.91 (11) | 0.00 | 0.00 | - | - |
| svg/svgo | open_door | 0 | 0.12 | 0.20 | 1 | 45 | 0.29 (7) | 46.60 | 0.89 (35) | 1.00 | 3.00 | 1.75 | - |
| csstree/csstree | open_door | 0 | 0.33 | 0.35 | 3 | 61 | 0.80 (5) | 68.10 | 0.88 (17) | 0.00 | 1.00 | 2.50 | - |
| prismjs/prism | open_door | 0 | 0.17 | 0.24 | 6 | 39 | - (4) | 78.80 | 0.79 (34) | 2.00 | 2.00 | 2.88 | - |
| cloudpipe/cloudpickle | open_door | 0 | 0.57 | 0.31 | 3 | 19 | - (3) | 12.00 | 0.77 (13) | 2.00 | 2.00 | 1.04 | - |
| websocket-client/websocket-client | open_door | 1 | 0.21 | 0.36 | 4 | 9 | - (3) | 12.80 | 0.73 (11) | 1.00 | 1.00 | 2.00 | - |
| tqdm/tqdm | open_door | 0 | 0.48 | 0.21 | 20 | 18 | - (1) | 24.60 | 0.71 (105) | 1.00 | 1.00 | 12.42 | - |
| micromatch/picomatch | open_door | 0 | 0.31 | 0.27 | 8 | 23 | - (1) | 18.40 | 0.70 (37) | 0.00 | 4.00 | 1.04 | - |
| prompt-toolkit/python-prompt-toolkit | open_door | 0 | 0.68 | 0.28 | 11 | 24 | 0.20 (5) | 19.80 | 0.69 (54) | 1.00 | 1.00 | 6.67 | - |
| google/flatbuffers | open_door | 0 | 0.69 | 0.32 | 53 | 20 | 0.20 (30) | 30.10 | 0.67 (332) | 5.00 | 2.00 | 20.00 | -0.13 |
| popperjs/popper-core | open_door | 0 | 0.35 | 0.45 | 12 | 17 | 0.21 (14) | 32.30 | 0.66 (38) | 2.00 | 2.00 | 2.83 | - |
| motdotla/dotenv | open_door | 1 | 0.12 | 0.21 | 18 | 7 | 0.10 (10) | 7.80 | 0.65 (92) | 1.00 | 1.00 | 10.08 | - |

**today's review fast (<= 3 days) but insider median >= 14 days** (5)

| repo | profile | ready | open | accept | debuts | rev_med | conv(n) | resp_days | no_resp(n) | rev_div | active | demand | gap |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unjs/ofetch | stable | 0 | 0.27 | 0.08 | 3 | 1 | 0.20 (5) | 91.10 | 0.88 (77) | 1.00 | 1.00 | 8.08 | - |
| stefankoegl/python-json-patch | stable | 0 | - | 0.00 | 0 | 0 | - (0) | 36.30 | 1.00 (13) | 0.00 | - | - | - |
| unjs/destr | stable | 0 | - | 0.00 | 0 | 0 | - (2) | 36.20 | 0.71 (17) | 0.00 | 1.00 | 1.67 | - |
| pillarjs/send | stable | 0 | 0.71 | 0.29 | 0 | 1 | - (2) | 24.40 | 0.41 (17) | 2.00 | 1.00 | 1.58 | - |
| standard-schema/standard-schema | open_door | 0 | 0.77 | 0.76 | 27 | 1 | 0.14 (63) | 20.30 | 0.22 (49) | 2.00 | 2.00 | 2.46 | - |

**reviewer_diversity = 1 and demand >= 5/month per active maintainer** (27)

| repo | profile | ready | open | accept | debuts | rev_med | conv(n) | resp_days | no_resp(n) | rev_div | active | demand | gap |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pydantic/httpx2 | open_door | 1 | 0.30 | 0.58 | 25 | 0 | - (0) | 2.80 | 0.36 (105) | 1.00 | 2.00 | 42.75 | -0.66 |
| h3js/h3 | open_door | 0 | 0.33 | 0.68 | 44 | 0 | 0.30 (40) | 0.40 | 0.14 (213) | 1.00 | 1.00 | 24.17 | - |
| textualize/rich | stable | 0 | 0.22 | 0.07 | 12 | 1 | 0.00 (8) | 10.40 | 0.56 (181) | 1.00 | 1.00 | 23.17 | - |
| kludex/starlette | open_door | 0 | 0.31 | 0.25 | 44 | 0 | 0.17 (29) | 3.10 | 0.23 (242) | 1.00 | 1.00 | 22.75 | -0.26 |
| agronholm/anyio | guardian | 0 | 0.48 | 0.48 | 48 | 0 | 0.33 (9) | 1.00 | 0.28 (192) | 1.00 | 1.00 | 22.67 | - |
| fsspec/filesystem_spec | open_door | 0 | 0.86 | 0.83 | 74 | 1 | 0.20 (41) | 1.80 | 0.12 (185) | 1.00 | 1.00 | 21.00 | - |
| sindresorhus/type-fest | guardian | 0 | 0.72 | 0.56 | 21 | 0 | 0.28 (36) | 1.30 | 0.32 (176) | 1.00 | 1.00 | 20.83 | - |
| shikijs/shiki | open_door | 1 | 0.47 | 0.38 | 48 | 2 | 0.24 (50) | 2.60 | 0.30 (172) | 1.00 | 1.00 | 18.92 | - |
| pallets/jinja | stable | 0 | - | 0.00 | 0 | 0 | 0.00 (22) | 0.00 | 0.15 (118) | 1.00 | 1.00 | 12.58 | - |
| tqdm/tqdm | open_door | 0 | 0.48 | 0.21 | 20 | 18 | - (1) | 24.60 | 0.71 (105) | 1.00 | 1.00 | 12.42 | - |
| python-poetry/tomlkit | open_door | 0 | 0.83 | 0.56 | 20 | 3 | 0.20 (5) | 4.60 | 0.36 (103) | 1.00 | 1.00 | 12.00 | - |
| openai/tiktoken | stable | 0 | 0.23 | 0.04 | 3 | 40 | - (4) | 76.70 | 0.86 (79) | 1.00 | 1.00 | 11.50 | - |

**active_maintainers = 0 (everyone on a break) but outside PRs keep coming (10+)** (10)

| repo | profile | ready | open | accept | debuts | rev_med | conv(n) | resp_days | no_resp(n) | rev_div | active | demand | gap |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ajv-validator/ajv | guardian | 0 | 0.10 | 0.02 | 1 | 103 | - (1) | 97.30 | 0.92 (51) | 0.00 | 0.00 | - | - |
| auth0/node-jsonwebtoken | stable | 0 | 0.00 | 0.00 | 0 | 100 | - (0) | 146.90 | 1.00 (25) | 0.00 | 0.00 | - | - |
| istanbuljs/istanbuljs | stable | 0 | - | 0.00 | 0 | 98 | - (3) | 96.60 | 1.00 (18) | 0.00 | 0.00 | - | - |
| jshttp/mime-types | open_door | 0 | 0.91 | 0.50 | 3 | 0 | - (3) | 1.40 | 0.50 (20) | 2.00 | 0.00 | - | - |
| npm/node-semver | open_door | 0 | 0.62 | 0.27 | 7 | 16 | - (3) | 9.60 | 0.62 (37) | 2.00 | 0.00 | - | - |
| omnilib/aiosqlite | open_door | 0 | 0.57 | 0.36 | 4 | 25 | - (2) | 36.80 | 0.91 (11) | 0.00 | 0.00 | - | - |
| python-hyper/h11 | guardian | 0 | - | 0.00 | 0 | 28 | - (2) | 50.00 | 1.00 (15) | 0.00 | 0.00 | - | - |
| sinonjs/fake-timers | open_door | 0 | 0.13 | 0.47 | 7 | 21 | - (4) | 18.20 | 0.47 (15) | 1.00 | 0.00 | - | - |
| styled-components/css-to-react-native | open_door | 0 | 1.00 | 0.79 | 1 | 0 | - (1) | 0.40 | 0.14 (14) | 1.00 | 0.00 | - | - |
| tartley/colorama | stable | 0 | - | 0.06 | 1 | 33 | - (1) | 35.80 | 0.94 (16) | 0.00 | 0.00 | - | - |

**open_door with conversion <= 0.15** (11)

| repo | profile | ready | open | accept | debuts | rev_med | conv(n) | resp_days | no_resp(n) | rev_div | active | demand | gap |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| django/asgiref | open_door | 0 | 0.67 | 0.47 | 12 | 22 | 0.00 (8) | 41.20 | 0.42 (43) | 2.00 | 1.00 | 4.92 | - |
| immerjs/immer | open_door | 0 | 0.43 | 0.59 | 14 | 11 | 0.00 (8) | 18.90 | 0.29 (38) | 2.00 | 2.00 | 2.29 | - |
| ipython/ipykernel | open_door | 1 | 0.39 | 0.79 | 16 | 3 | 0.00 (5) | 2.70 | 0.21 (38) | 4.00 | 5.00 | 1.13 | -0.06 |
| jaredwray/cacheable | open_door | 1 | 0.02 | 0.86 | 6 | 0 | 0.08 (26) | - | - (7) | - | 1.00 | 3.58 | - |
| nltk/nltk | open_door | 1 | 0.36 | 0.65 | 44 | 0 | 0.08 (13) | 5.80 | 0.15 (208) | 3.00 | 4.00 | 5.88 | 0.05 |
| huggingface/safetensors | open_door | 0 | 0.27 | 0.21 | 11 | 20 | 0.09 (23) | 29.70 | 0.62 (76) | 4.00 | 3.00 | 3.47 | - |
| joblib/joblib | open_door | 0 | 0.49 | 0.49 | 14 | 2 | 0.10 (10) | 5.90 | 0.29 (49) | 4.00 | 6.00 | 1.17 | 0.22 |
| motdotla/dotenv | open_door | 1 | 0.12 | 0.21 | 18 | 7 | 0.10 (10) | 7.80 | 0.65 (92) | 1.00 | 1.00 | 10.08 | - |
| reduxjs/redux-toolkit | open_door | 1 | 0.42 | 0.58 | 32 | 3 | 0.10 (20) | 3.60 | 0.22 (106) | 4.00 | 5.00 | 3.65 | 0.24 |
| urllib3/urllib3 | open_door | 0 | 0.47 | 0.21 | 34 | 5 | 0.13 (15) | 10.50 | 0.54 (267) | 3.00 | 4.00 | 6.77 | 0.50 |
| standard-schema/standard-schema | open_door | 0 | 0.77 | 0.76 | 27 | 1 | 0.14 (63) | 20.30 | 0.22 (49) | 2.00 | 2.00 | 2.46 | - |

## 5. Entry-path counts (2026-09)

demand p75 = 2.10

| Path rule | projects |
|---|---|
| review: reviewer_diversity <= 1, demand >= p75, and someone answers (no_resp <= 0.5) | 41 |
| triage: demand >= p75 and active_maintainers 1-2 | 79 |
| successor: active_maintainers = 0, insiders > 0, demand > 0 issues/PRs | 73 |
| code for beginners: conversion >= 0.3 and no_resp <= 0.3 | 12 |

## 6. Candidate rules v1: counts

demand p25 = 0.17, p75 = 2.10

| Level | good | ok | bad | insufficient |
|---|---|---|---|---|
| beginner | 44 | 49 | 272 | 593 |
| intermediate | 63 | 68 | 154 | 673 |
| experienced | 50 | 345 | 42 | 521 |

beginner reasons: [('bad', 'guardian', 150), ('bad', 'nobody active', 74), ('bad', 'outside PRs go unanswered', 48), ('good', 'all pass', 44), ('insufficient', '<10 outside PRs', 274), ('insufficient', 'no PRs since 2018', 216), ('insufficient', 'large/truncated repo', 103), ('ok', 'partial', 49)] 

intermediate reasons: [('bad', 'nobody active', 115), ('bad', 'outside PRs go unanswered', 39), ('good', 'door works', 63), ('insufficient', '<10 outside PRs', 354), ('insufficient', 'no PRs since 2018', 216), ('insufficient', 'large/truncated repo', 103), ('ok', 'partial', 68)] 

experienced reasons: [('bad', 'door closed despite activity', 42), ('good', 'high demand, door works', 50), ('insufficient', 'no PRs since 2018', 216), ('insufficient', 'no maintainer', 160), ('insufficient', 'large/truncated repo', 103), ('insufficient', 'no activity to read', 42), ('ok', 'low or average demand', 272), ('ok', 'successor wanted', 73)] 

Sanity only (concurrent, same window as the rules): conversion@2026-09 by v1 rating:
| Level | rating | repos | mean conv | pooled conv | cohort people |
|---|---|---|---|---|---|
| beginner | good | 25 | 0.32 | 0.29 | 375 |
| beginner | ok | 26 | 0.18 | 0.19 | 540 |
| beginner | bad | 38 | 0.20 | 0.19 | 396 |
| beginner | insufficient | 4 | 0.35 | 0.23 | 44 |
| intermediate | good | 33 | 0.29 | 0.27 | 448 |
| intermediate | ok | 37 | 0.17 | 0.19 | 694 |
| intermediate | bad | 18 | 0.24 | 0.21 | 163 |
| intermediate | insufficient | 5 | 0.28 | 0.20 | 50 |
| experienced | good | 33 | 0.21 | 0.21 | 587 |
| experienced | ok | 41 | 0.27 | 0.25 | 570 |
| experienced | bad | 19 | 0.19 | 0.16 | 198 |

Backtest of the v1 beginner rule: rated with data before 2025-10, outcome conversion@2026-09:
| Level | rating | repos | mean conv | pooled conv | cohort people |
|---|---|---|---|---|---|
| beginner @T=2025-10 | good | 35 | 0.27 | 0.24 | 712 |
| beginner @T=2025-10 | ok | 25 | 0.14 | 0.14 | 338 |
| beginner @T=2025-10 | bad | 25 | 0.23 | 0.21 | 255 |
| beginner @T=2025-10 | insufficient | 8 | 0.39 | 0.44 | 50 |

Today's ready=True (30) under v1 beginner: {'good': 17, 'ok': 9, 'insufficient': 2, 'bad': 2}
Today's profile x v1 beginner:
| profile | good | ok | bad | insufficient |
|---|---|---|---|---|
| open_door | 38 | 26 | 31 | 92 |
| stable | 5 | 20 | 89 | 498 |
| guardian | 0 | 0 | 150 | 3 |
| needs_hands | 1 | 3 | 2 | 0 |

v1 beginner good: ['aio-libs/multidict', 'aio-libs/propcache', 'bombshell-dev/clack', 'celery/billiard', 'celery/kombu', 'celery/py-amqp', 'eslint/rewrite', 'fastify/fast-uri', 'fonttools/fonttools', 'fsspec/filesystem_spec', 'h3js/crossws', 'h3js/h3', 'joblib/joblib', 'joblib/threadpoolctl', 'jshttp/content-disposition', 'jupyterlab/jupyter-builder', 'kaelzhang/node-ignore', 'kpdecker/jsdiff', 'lxml/lxml', 'mdn/data', 'microsoft/debugpy', 'mltframework/shotcut', 'mongodb/js-bson', 'mrabarnett/mrab-regex', 'msgpack/msgpack-python', 'nodejs/node-addon-api', 'postcss/postcss', 'psf/cachecontrol', 'pypa/build', 'pypa/packaging', 'pytest-dev/pluggy', 'python-cffi/cffi', 'python/typing_extensions', 'reduxjs/redux', 'reduxjs/redux-toolkit', 'rich-harris/magic-string', 'shikijs/shiki', 'styled-components/styled-components', 'sveltejs/devalue', 'tinylibs/tinyexec', 'tox-dev/platformdirs', 'unjs/magicast', 'unjs/radix3', 'webpack/enhanced-resolve'] 

today ready but v1 beginner not good: [('google/brotli', ('ok', 'partial')), ('huggingface/huggingface.js', ('ok', 'partial')), ('ipython/ipykernel', ('ok', 'partial')), ('jaredwray/cacheable', ('insufficient', '<10 outside PRs')), ('motdotla/dotenv', ('bad', 'outside PRs go unanswered')), ('narwhals-dev/narwhals', ('insufficient', 'large/truncated repo')), ('nltk/nltk', ('ok', 'partial')), ('prometheus/client_python', ('ok', 'partial')), ('protobufjs/protobuf.js', ('ok', 'partial')), ('pydantic/httpx2', ('ok', 'partial')), ('tornadoweb/tornado', ('ok', 'partial')), ('vega/altair', ('ok', 'partial')), ('websocket-client/websocket-client', ('bad', 'outside PRs go unanswered'))] 

v1 experienced good (top demand): [(42.75, 'pydantic/httpx2'), (24.17, 'h3js/h3'), (22.75, 'kludex/starlette'), (22.67, 'agronholm/anyio'), (21.0, 'fsspec/filesystem_spec'), (20.83, 'sindresorhus/type-fest'), (18.92, 'shikijs/shiki'), (13.0, 'celery/kombu'), (12.0, 'python-poetry/tomlkit'), (9.33, 'socketio/socket.io'), (8.5, 'google/brotli'), (7.33, 'tornadoweb/tornado'), (6.58, 'styled-components/styled-components'), (6.5, 'postcss/postcss'), (5.96, 'mltframework/shotcut')] 

conversion half-width at p=0.2, n=5: ±0.35
conversion half-width at p=0.2, n=10: ±0.25
conversion half-width at p=0.2, n=20: ±0.18
conversion half-width at p=0.2, n=50: ±0.11

Fast insider response (<= 2 days) but outside acceptance today < 0.1: [('pallets/flask', 0.0, 0.04), ('pallets/itsdangerous', 0.0, 0.0), ('pallets/jinja', 0.0, 0.0)]
Mean conversion@2026-09, flagged minus rest (bootstrap 95% CI):
| Flag | repos | flagged | diff | 95% CI |
|---|---|---|---|---|
| badge@T ready | 93 | 21 | +0.025 | [-0.053, +0.106] |
| v1 beginner good @T | 93 | 35 | +0.058 | [-0.014, +0.134] |
| TODAY ready (concurrent) | 93 | 21 | +0.016 | [-0.060, +0.102] |


code for beginners list (conv >= 0.3, no_resp <= 0.3): ['acornjs/acorn', 'agronholm/anyio', 'aio-libs/propcache', 'bombshell-dev/clack', 'eslint/rewrite', 'h3js/crossws', 'h3js/h3', 'mdn/data', 'pypa/build', 'python-cffi/cffi', 'python/typing_extensions', 'tinylibs/tinyexec']
v1 beginner good with newcomer_open > 0: [('aio-libs/multidict', 1), ('bombshell-dev/clack', 1), ('fonttools/fonttools', 1), ('fsspec/filesystem_spec', 4), ('joblib/joblib', 4), ('joblib/threadpoolctl', 2), ('jshttp/content-disposition', 1), ('mdn/data', 2), ('pytest-dev/pluggy', 1), ('reduxjs/redux-toolkit', 1), ('shikijs/shiki', 1)]

## 7. Robustness

Cohort (participation rebuild, projects with conversion): 1328 people; merger/direct committer in another repo before 2025-10: 121 (9.1%); same owner: 19 (1.4%)
  pillarjs/router: cohort 6, insider elsewhere 2: [('Phillip9587', ['expressjs/body-parser', 'expressjs/express', 'jshttp/on-finished']), ('bjohansebas', ['expressjs/express', 'pillarjs/iconv-lite', 'stream-utils/raw-body'])]
  h3js/h3: cohort 39, insider elsewhere 2: [('patak-cat', ['vitejs/vite']), ('septatrix', ['python/typing_extensions'])]
  pypa/build: cohort 5, insider elsewhere 3: [('DimitriPapadopoulos', ['babel/babel', 'jaraco/jaraco.classes', 'jaraco/jaraco.context']), ('jayaddison', ['pallets/flask']), ('mgorny', ['pydantic/httpx2', 'pypa/distlib'])]
  celery/kombu: cohort 22, insider elsewhere 1: [('emmanuel-ferdman', ['pydantic/httpx2'])]
  jshttp/content-disposition: cohort 0, insider elsewhere 0: []
Repos where 30%+ of the cohort is an insider elsewhere: [('annotated-types/annotated-types', 2, 6), ('browserslist/browserslist', 3, 9), ('expressjs/serve-static', 2, 5), ('jshttp/cookie', 5, 13), ('jshttp/mime-db', 5, 15), ('pallets/markupsafe', 2, 5), ('pillarjs/router', 2, 6), ('pypa/build', 3, 5), ('pypa/packaging', 5, 15), ('tinylibs/tinyexec', 2, 6)]

v1 beginner good @T WITHOUT the conversion clause: repos 93, flagged 40, diff +0.030 [-0.044, +0.105]
conversion@T >= 0.1 alone (repos with conversion@T): repos 66, flagged 51, diff +0.137 [+0.074, +0.199]

No-PR projects (216): commits in last 24 months > 0: 0; direct commits > 0: 0; no commit row: 216

Guide mismatches, ecosyste.ms contributing path: [('CONTRIBUTING.rst', 14), ('docs/contributing.md', 7), ('docs/contributing.rst', 4), ('.github/contributing.md', 4), ('docs/contributing/guidelines.rst', 3), ('contributing.md', 3), ('CONTRIBUTING.txt', 1), ('CONTRIBUTING', 1)]
