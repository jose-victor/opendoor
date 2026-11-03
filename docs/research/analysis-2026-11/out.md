## 1. Coverage

projects.json: 957 projects; repo_signals repos: 859; non-canonical repos in repo_signals but not in projects.json: 14

| Stage | Projects |
|---|---|
| computed | 845 |
| sampled (large) | 111 |
| truncated | 1 |

No raw file, PRs opened (repo_monthly):
| Group | Projects |
|---|---|
| 0 PRs ever since 2018 | 0 |
| PRs ever but 0 in last 12 months | 0 |
| 1+ PRs in last 12 months | 0 |

Computed projects with 0 PRs since 2018 (repo_monthly): 34
No raw file, by profile: {} 

Per signal at 2026-09 among the computed projects (denominator for % = all projects):
| Signal | min n | computed | n = 0 | 0 < n < min | has value | % of all projects | has value @T |
|---|---|---|---|---|---|---|---|
| conversion | 5 | 845 | 410 | 302 | 133 | 13.9% | 149 |
| first_insider_response_days | 10 | 845 | 207 | 358 | 280 | 29.3% | 172 |
| no_insider_response_share | 10 | 845 | 207 | 358 | 280 | 29.3% | 172 |
| outsider_insider_gap | 10 | 845 | 650 | 147 | 48 | 5.0% | 27 |
| reviewer_diversity | 10 | 845 | 207 | 358 | 280 | 29.3% | 172 |
| active_maintainers | 1 | 845 | 210 | 0 | 635 | 66.4% | 633 |
| demand_per_maintainer | 1 | 845 | 341 | 0 | 504 | 52.7% | 476 |

Computed projects by outside PRs in 12 months (n of first_insider_response_days) and profile:
| outside PRs 12m | projects | open_door | stable | guardian | needs_hands | ready | has conversion |
|---|---|---|---|---|---|---|---|
| 0 | 207 | 0 | 172 | 35 | 0 | 0 | 0 |
| 1-9 | 358 | 24 | 259 | 74 | 1 | 2 | 13 |
| 10-29 | 142 | 61 | 60 | 21 | 0 | 19 | 27 |
| 30-99 | 94 | 51 | 28 | 13 | 2 | 25 | 53 |
| 100+ | 44 | 23 | 17 | 3 | 1 | 10 | 40 |

Conversion cohort size (n) among computed projects at 2026-09:
| cohort n | projects |
|---|---|
| 0 | 410 |
| 1-4 | 302 |
| 5-9 | 65 |
| 10-29 | 57 |
| 30+ | 11 |

Sampled projects by profile: {'open_door': 80, 'stable': 28, 'guardian': 3} | ready: 0 

Projects in an external newcomer list: 35; by stage: {'sampled (large)': 32, 'computed': 3}; with conversion@now: 0; ready: 0

CONTRIBUTING: today's guide check vs ecosyste.ms files.contributing (projects with an ecosyste.ms record):
|  | eco has | eco missing |
|---|---|---|
| guide check ok | 276 | 155 |
| guide check fails | 0 | 492 |

Projects whose only failing beginner check is `guide`: 75 (of them eco sees a CONTRIBUTING: 0): ['agnivade/levenshtein', 'agronholm/exceptiongroup', 'ai/nanoid', 'annotated-types/annotated-types', 'brianc/node-postgres', 'browserslist/browserslist', 'browserslist/update-db', 'caolan/async', 'celery/billiard', 'celery/kombu', 'celery/py-amqp', 'certifi/python-certifi', 'click-contrib/click-repl', 'dpranke/pyjson5', 'fb55/domutils', 'fb55/entities', 'fsspec/filesystem_spec', 'gabriel-vasile/mimetype', 'gorakhargosh/watchdog', 'grahamdumpleton/wrapt', 'guybedford/es-module-lexer', 'h3js/crossws', 'h3js/h3', 'horejsek/python-fastjsonschema', 'immerjs/immer', 'ipython/matplotlib-inline', 'jd/tenacity', 'joblib/joblib', 'joblib/threadpoolctl', 'jshttp/content-disposition', 'jshttp/type-is', 'juliangruber/brace-expansion', 'jupyterlab/jupyter-builder', 'kaelzhang/node-ignore', 'kjd/idna', 'klauspost/compress', 'labstack/echo', 'ledongthuc/pdf', 'lxml/lxml', 'mattn/go-runewidth', 'mattn/go-sqlite3', 'mrabarnett/mrab-regex', 'msgpack/msgpack-python', 'nucleic/kiwi', 'olekukonko/tablewriter', 'pillarjs/path-to-regexp', 'pydantic/jiter', 'pypa/build', 'pypa/distlib', 'pytest-dev/iniconfig', 'pytest-dev/pluggy', 'python-cffi/cffi', 'python-poetry/tomlkit', 'python-websockets/websockets', 'rexxars/eventsource-parser', 'rich-harris/magic-string', 'rolldown/plugins', 'scrapy/cssselect', 'scrapy/itemadapter', 'scrapy/itemloaders', 'scrapy/parsel', 'scrapy/protego', 'scrapy/w3lib', 'spf13/pflag', 'stefankoegl/python-json-patch', 'sveltejs/devalue', 'sveltejs/esrap', 'tinylib/msgp', 'tinylibs/tinyexec', 'tree-sitter/tree-sitter-php', 'unjs/magicast', 'unjs/radix3', 'valyala/fasthttp', 'websockets/ws', 'whitequark/ipaddr.js']

## 2. Distributions

| Signal | as_of | n repos | p10 | p25 | p50 | p75 | p90 | mean |
|---|---|---|---|---|---|---|---|---|
| conversion | 2026-10 | 133 | 0.00 | 0.12 | 0.20 | 0.33 | 0.50 | 0.24 |
| conversion | 2025-10 | 149 | 0.00 | 0.09 | 0.20 | 0.30 | 0.46 | 0.22 |
| first_insider_response_days | 2026-10 | 280 | 0.39 | 1.40 | 9.20 | 25.38 | 61.71 | 21.04 |
| first_insider_response_days | 2025-10 | 172 | 0.20 | 0.70 | 3.20 | 21.15 | 76.41 | 21.95 |
| no_insider_response_share | 2026-10 | 280 | 0.07 | 0.19 | 0.42 | 0.72 | 0.95 | 0.46 |
| no_insider_response_share | 2025-10 | 172 | 0.06 | 0.11 | 0.24 | 0.46 | 0.74 | 0.32 |
| outsider_insider_gap | 2026-10 | 48 | -0.31 | -0.03 | 0.14 | 0.34 | 0.50 | 0.12 |
| outsider_insider_gap | 2025-10 | 27 | -0.16 | -0.10 | -0.04 | 0.17 | 0.32 | 0.01 |
| reviewer_diversity | 2026-10 | 280 | 0.00 | 1.00 | 1.00 | 2.00 | 3.10 | 1.53 |
| reviewer_diversity | 2025-10 | 172 | 1.00 | 1.00 | 1.00 | 3.00 | 4.00 | 1.93 |
| active_maintainers | 2026-10 | 635 | 0.00 | 1.00 | 1.00 | 1.00 | 3.00 | 1.39 |
| active_maintainers | 2025-10 | 633 | 0.00 | 1.00 | 1.00 | 1.00 | 3.00 | 1.26 |
| demand_per_maintainer | 2026-10 | 504 | 0.08 | 0.25 | 0.90 | 2.69 | 6.31 | 2.62 |
| demand_per_maintainer | 2025-10 | 476 | 0.08 | 0.25 | 0.62 | 1.83 | 4.17 | 1.65 |

demand_per_maintainer NULL split: active_maintainers = 0: 131 | no insider at all: 210 

reviewer_diversity@now counts: [(0, 69), (1, 112), (2, 44), (3, 27), (4, 15), (5, 7), (6, 5), (22, 1)] 

active_maintainers@now counts: [(0, 131), (1, 346), (2, 78), (3, 36), (4, 19), (5, 8), (6, 5), (7, 3), (8, 1), (9, 4), (10, 1), (13, 1), (19, 1), (22, 1)] 

active_maintainers = 0 but insiders > 0 @now: 131 

Spearman, pairwise complete, signals @now and today's numbers (rho / n):

|  | conv | resp_days | no_resp | gap | rev_div | active | demand | open | accept | debuts | rev_med | stale | maint24 | gfi_open | ready |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| conv | · | -0.13 (120) | -0.10 (120) | -0.19 (33) | +0.18 (120) | +0.20 (131) | -0.38 (126) | -0.10 (126) | +0.26 (129) | -0.17 (133) | -0.13 (129) | -0.06 (129) | +0.21 (133) | -0.11 (133) | +0.08 (133) |
| resp_days | -0.13 (120) | · | +0.77 (280) | -0.15 (48) | -0.23 (280) | -0.14 (274) | -0.05 (244) | -0.02 (244) | -0.60 (280) | -0.35 (280) | +0.88 (280) | +0.76 (280) | +0.06 (280) | +0.21 (280) | -0.28 (280) |
| no_resp | -0.10 (120) | +0.77 (280) | · | +0.11 (48) | -0.31 (280) | -0.22 (274) | +0.02 (244) | +0.05 (244) | -0.72 (280) | -0.44 (280) | +0.72 (280) | +0.80 (280) | -0.07 (280) | +0.23 (280) | -0.26 (280) |
| gap | -0.19 (33) | -0.15 (48) | +0.11 (48) | · | -0.08 (48) | -0.11 (48) | -0.08 (48) | +0.04 (48) | -0.46 (48) | -0.22 (48) | +0.15 (48) | +0.13 (48) | -0.21 (48) | +0.00 (48) | -0.32 (48) |
| rev_div | +0.18 (120) | -0.23 (280) | -0.31 (280) | -0.08 (48) | · | +0.68 (274) | -0.09 (244) | +0.18 (244) | +0.36 (280) | +0.51 (280) | -0.24 (280) | -0.11 (280) | +0.67 (280) | +0.14 (280) | +0.33 (280) |
| active | +0.20 (131) | -0.14 (274) | -0.22 (274) | -0.11 (48) | +0.68 (274) | · | +0.09 (504) | +0.08 (403) | +0.26 (369) | +0.50 (635) | -0.17 (370) | -0.16 (370) | +0.64 (635) | +0.18 (635) | +0.31 (635) |
| demand | -0.38 (126) | -0.05 (244) | +0.02 (244) | -0.08 (48) | -0.09 (244) | +0.09 (504) | · | +0.47 (373) | -0.06 (322) | +0.78 (504) | -0.06 (323) | +0.12 (323) | +0.21 (504) | +0.28 (504) | +0.26 (504) |

Median of each signal @now by today's profile (value / n):
| group | projects | conv | resp_days | no_resp | gap | rev_div | active | demand |
|---|---|---|---|---|---|---|---|---|
| open_door | 240 | 0.20 (73) | 5.00 (135) | 0.28 (135) | 0.12 (34) | 1.00 (135) | 1.00 (157) | 2.06 (149) |
| stable | 564 | 0.17 (46) | 23.50 (105) | 0.72 (105) | 0.15 (13) | 1.00 (105) | 1.00 (328) | 0.50 (246) |
| guardian | 149 | 0.16 (12) | 5.30 (37) | 0.28 (37) | 0.59 (1) | 1.00 (37) | 1.00 (146) | 0.42 (105) |
| needs_hands | 4 | 0.22 (2) | 18.60 (3) | 0.45 (3) | - (0) | 1.00 (3) | 1.00 (4) | 7.12 (4) |
| ready=True | 57 | 0.23 (35) | 3.65 (54) | 0.24 (54) | 0.08 (24) | 2.00 (54) | 2.00 (54) | 3.08 (54) |
| ready=False | 900 | 0.20 (98) | 12.50 (226) | 0.50 (226) | 0.27 (24) | 1.00 (226) | 1.00 (581) | 0.75 (450) |

review.median_days (any non-author reviewer) vs first_insider_response_days: rho +0.88, n 280; insider median > today's by 7+ days: 57; by 30+ days: 8

## 3. Backtest

Noise ceiling: conversion@T vs conversion@now: rho +0.33 [+0.11, +0.54], n 89

Spearman with conversion@now (cohort debuted 2024-11..2025-10, followed 12 months), 95% bootstrap CI (1000):
| Predictor | n | rho | 95% CI |
|---|---|---|---|
| first_insider_response_days@T | 114 | +0.06 | [-0.12, +0.25] |
| no_insider_response_share@T | 114 | -0.03 | [-0.23, +0.15] |
| outsider_insider_gap@T | 24 | -0.36 | [-0.69, +0.03] |
| reviewer_diversity@T | 114 | +0.19 | [+0.00, +0.37] |
| active_maintainers@T | 132 | +0.04 | [-0.15, +0.23] |
| demand_per_maintainer@T | 124 | -0.30 | [-0.46, -0.12] |
| conversion@T (prior cohort) | 89 | +0.33 | [+0.11, +0.54] |
| debuts_12m@T (= cohort size, coupled) | 133 | -0.22 | [-0.39, -0.05] |
| newcomer acceptance@T (debuts/tried, 5+ tried) | 131 | +0.17 | [-0.01, +0.35] |
| outside merges last 3m@T | 133 | +0.09 | [-0.08, +0.27] |
| badge@T checks passed (0-5) | 133 | +0.02 | [-0.16, +0.21] |
| badge@T ready (0/1) | 133 | +0.02 | [-0.15, +0.19] |
| TODAY ready (concurrent, not a backtest) | 133 | +0.08 | [-0.09, +0.23] |
| TODAY openness (concurrent) | 126 | -0.10 | [-0.27, +0.08] |
| TODAY acceptance (concurrent) | 129 | +0.26 | [+0.09, +0.42] |
| TODAY review_median_days (concurrent) | 129 | -0.13 | [-0.30, +0.04] |

Conversion@now by tercile of each predictor (mean of repo rates; pooled = sum came back / sum cohort):
| Predictor | tercile | repos | range | mean conv | pooled conv | cohort people |
|---|---|---|---|---|---|---|
| first_insider_response_days@T | low | 38 | 0.00–0.90 | 0.19 | 0.21 | 593 |
| first_insider_response_days@T | mid | 38 | 1.00–6.40 | 0.27 | 0.24 | 626 |
| first_insider_response_days@T | high | 38 | 6.90–122.10 | 0.23 | 0.20 | 506 |
| no_insider_response_share@T | low | 38 | 0.00–0.13 | 0.22 | 0.23 | 533 |
| no_insider_response_share@T | mid | 38 | 0.14–0.31 | 0.25 | 0.24 | 691 |
| no_insider_response_share@T | high | 38 | 0.31–1.00 | 0.22 | 0.19 | 501 |
| outsider_insider_gap@T | low | 8 | -0.25–-0.10 | 0.35 | 0.28 | 239 |
| outsider_insider_gap@T | mid | 8 | -0.06–0.02 | 0.32 | 0.34 | 135 |
| outsider_insider_gap@T | high | 8 | 0.04–0.38 | 0.20 | 0.18 | 131 |
| reviewer_diversity@T | low | 38 | 0.00–1.00 | 0.22 | 0.20 | 455 |
| reviewer_diversity@T | mid | 38 | 1.00–3.00 | 0.20 | 0.18 | 533 |
| reviewer_diversity@T | high | 38 | 3.00–15.00 | 0.28 | 0.26 | 737 |
| active_maintainers@T | low | 44 | 0.00–1.00 | 0.25 | 0.23 | 518 |
| active_maintainers@T | mid | 44 | 1.00–2.00 | 0.21 | 0.20 | 538 |
| active_maintainers@T | high | 44 | 2.00–21.00 | 0.28 | 0.24 | 770 |
| demand_per_maintainer@T | low | 41 | 0.01–1.71 | 0.32 | 0.28 | 518 |
| demand_per_maintainer@T | mid | 41 | 1.75–4.17 | 0.22 | 0.22 | 476 |
| demand_per_maintainer@T | high | 42 | 4.17–26.17 | 0.17 | 0.18 | 778 |
| conversion@T (prior cohort) | low | 29 | 0.00–0.11 | 0.15 | 0.15 | 409 |
| conversion@T (prior cohort) | mid | 30 | 0.12–0.25 | 0.21 | 0.20 | 470 |
| conversion@T (prior cohort) | high | 30 | 0.25–1.00 | 0.26 | 0.25 | 540 |
| debuts_12m@T (= cohort size, coupled) | low | 44 | 1.00–6.00 | 0.32 | 0.33 | 250 |
| debuts_12m@T (= cohort size, coupled) | mid | 44 | 6.00–13.00 | 0.22 | 0.22 | 415 |
| debuts_12m@T (= cohort size, coupled) | high | 45 | 14.00–133.00 | 0.20 | 0.20 | 1167 |
| newcomer acceptance@T (debuts/tried, 5+ tried) | low | 43 | 0.11–0.56 | 0.21 | 0.19 | 555 |
| newcomer acceptance@T (debuts/tried, 5+ tried) | mid | 44 | 0.57–0.81 | 0.22 | 0.23 | 715 |
| newcomer acceptance@T (debuts/tried, 5+ tried) | high | 44 | 0.81–1.00 | 0.27 | 0.23 | 549 |
| outside merges last 3m@T | low | 44 | 0.00–2.00 | 0.24 | 0.21 | 370 |
| outside merges last 3m@T | mid | 44 | 2.00–5.00 | 0.25 | 0.21 | 454 |
| outside merges last 3m@T | high | 45 | 5.00–55.00 | 0.24 | 0.24 | 1008 |
| badge@T checks passed (0-5) | low | 44 | 0.00–3.00 | 0.25 | 0.21 | 389 |
| badge@T checks passed (0-5) | mid | 44 | 3.00–4.00 | 0.23 | 0.22 | 615 |
| badge@T checks passed (0-5) | high | 45 | 4.00–5.00 | 0.25 | 0.24 | 828 |

Conversion@now by badge / profile group:
| Grouping | group | repos | mean conv | pooled conv | cohort people |
|---|---|---|---|---|---|
| TODAY ready (concurrent) | 1 | 35 | 0.26 | 0.25 | 663 |
| TODAY ready (concurrent) | 0 | 98 | 0.24 | 0.21 | 1169 |
| badge@T ready | 1 | 33 | 0.25 | 0.25 | 664 |
| badge@T ready | 0 | 100 | 0.24 | 0.21 | 1168 |
| TODAY profile (concurrent) | open_door | 73 | 0.25 | 0.24 | 1220 |
| TODAY profile (concurrent) | stable | 46 | 0.24 | 0.20 | 483 |
| TODAY profile (concurrent) | guardian | 12 | 0.23 | 0.20 | 101 |
| TODAY profile (concurrent) | needs_hands | 2 | 0.22 | 0.21 | 28 |
| badge@T check debuts | 1 | 132 | 0.24 | 0.22 | 1827 |
| badge@T check debuts | 0 | 1 | 1.00 | 1.00 | 5 |
| badge@T check acceptance | 1 | 126 | 0.24 | 0.22 | 1753 |
| badge@T check acceptance | 0 | 7 | 0.38 | 0.24 | 79 |
| badge@T check active | 1 | 97 | 0.24 | 0.23 | 1534 |
| badge@T check active | 0 | 36 | 0.25 | 0.21 | 298 |
| badge@T check response | 1 | 64 | 0.24 | 0.23 | 1057 |
| badge@T check response | 0 | 69 | 0.25 | 0.21 | 775 |
| badge@T check guide | 1 | 80 | 0.24 | 0.22 | 1270 |
| badge@T check guide | 0 | 53 | 0.25 | 0.22 | 562 |

badge@T ready overall: Counter({0: 809, 1: 37}) | today ready vs badge@T ready (both, today only, T only): 24 33 13 

## 4. Case candidates

**ready but >= 30% of outside PRs never got an insider response** (21)

| repo | profile | ready | open | accept | debuts | rev_med | conv(n) | resp_days | no_resp(n) | rev_div | active | demand | gap |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| kubernetes-sigs/structured-merge-diff | open_door | 1 | 1.00 | 0.80 | 4 | 0 | 0.46 (11) | 4.20 | 1.00 (35) | 0.00 | - | - | - |
| kubernetes/kube-openapi | open_door | 1 | 1.00 | 0.59 | 7 | 1 | 0.00 (6) | 2.00 | 1.00 (75) | 0.00 | - | - | - |
| pyparsing/pyparsing | open_door | 1 | 0.09 | 0.28 | 13 | 12 | 0.40 (5) | 17.30 | 0.66 (65) | 1.00 | 1.00 | 6.83 | - |
| motdotla/dotenv | open_door | 1 | 0.15 | 0.28 | 26 | 7 | 0.10 (10) | 7.70 | 0.61 (99) | 1.00 | 1.00 | 10.33 | - |
| bytedance/sonic | open_door | 1 | 0.34 | 0.27 | 8 | 6 | 0.17 (12) | 6.70 | 0.60 (48) | 2.00 | 2.00 | 3.67 | 0.13 |
| google/brotli | open_door | 1 | 0.61 | 0.31 | 17 | 10 | 0.29 (14) | 9.20 | 0.52 (75) | 1.00 | 1.00 | 9.75 | - |
| aio-libs/frozenlist | open_door | 1 | 0.37 | 0.39 | 6 | 0 | - (4) | 25.30 | 0.50 (18) | 2.00 | 3.00 | 0.78 | - |
| prometheus/common | open_door | 1 | 0.33 | 0.35 | 12 | 11 | 0.09 (11) | 14.00 | 0.49 (57) | 6.00 | 9.00 | 0.61 | 0.35 |
| vega/altair | open_door | 1 | 0.27 | 0.46 | 21 | 6 | 0.12 (8) | 7.10 | 0.47 (76) | 4.00 | 3.00 | 3.42 | 0.04 |
| huggingface/huggingface.js | open_door | 1 | 0.30 | 0.38 | 151 | 0 | 0.26 (137) | 3.30 | 0.45 (525) | 22.00 | 22.00 | 2.30 | -0.01 |
| tornadoweb/tornado | needs_hands | 1 | 0.22 | 0.32 | 26 | 14 | 0.13 (15) | 15.60 | 0.45 (100) | 1.00 | 1.00 | 11.08 | - |
| mongodb/js-bson | open_door | 1 | 0.26 | 0.38 | 5 | 12 | - (1) | 10.70 | 0.45 (29) | 5.00 | 6.00 | 0.40 | 0.20 |

**ready, conversion known** (35)

| repo | profile | ready | open | accept | debuts | rev_med | conv(n) | resp_days | no_resp(n) | rev_div | active | demand | gap |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ipython/ipykernel | open_door | 1 | 0.48 | 0.74 | 16 | 3 | 0.00 (8) | 3.70 | 0.20 (39) | 5.00 | 5.00 | 1.03 | - |
| kubernetes/kube-openapi | open_door | 1 | 1.00 | 0.59 | 7 | 1 | 0.00 (6) | 2.00 | 1.00 (75) | 0.00 | - | - | - |
| jaredwray/cacheable | open_door | 1 | 0.02 | 0.88 | 7 | 0 | 0.09 (23) | - | - (8) | - | 1.00 | 3.83 | - |
| go-playground/validator | open_door | 1 | 0.82 | 0.56 | 44 | 3 | 0.09 (33) | 6.90 | 0.31 (99) | 3.00 | 3.00 | 3.83 | - |
| prometheus/common | open_door | 1 | 0.33 | 0.35 | 12 | 11 | 0.09 (11) | 14.00 | 0.49 (57) | 6.00 | 9.00 | 0.61 | 0.35 |
| motdotla/dotenv | open_door | 1 | 0.15 | 0.28 | 26 | 7 | 0.10 (10) | 7.70 | 0.61 (99) | 1.00 | 1.00 | 10.33 | - |
| vega/altair | open_door | 1 | 0.27 | 0.46 | 21 | 6 | 0.12 (8) | 7.10 | 0.47 (76) | 4.00 | 3.00 | 3.42 | 0.04 |
| reduxjs/redux-toolkit | open_door | 1 | 0.42 | 0.48 | 27 | 3 | 0.13 (23) | 3.60 | 0.28 (113) | 4.00 | 5.00 | 3.67 | 0.25 |
| tornadoweb/tornado | needs_hands | 1 | 0.22 | 0.32 | 26 | 14 | 0.13 (15) | 15.60 | 0.45 (100) | 1.00 | 1.00 | 11.08 | - |
| nltk/nltk | open_door | 1 | 0.32 | 0.68 | 49 | 0 | 0.14 (14) | 5.80 | 0.14 (206) | 3.00 | 4.00 | 5.79 | 0.06 |
| postcss/postcss | open_door | 1 | 0.24 | 0.64 | 28 | 0 | 0.15 (13) | 0.20 | 0.16 (67) | 1.00 | 1.00 | 8.08 | - |
| bytedance/sonic | open_door | 1 | 0.34 | 0.27 | 8 | 6 | 0.17 (12) | 6.70 | 0.60 (48) | 2.00 | 2.00 | 3.67 | 0.13 |

**stable/guardian with conversion >= 0.4** (14)

| repo | profile | ready | open | accept | debuts | rev_med | conv(n) | resp_days | no_resp(n) | rev_div | active | demand | gap |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| mongodb-js/mongodb-connection-string-url | stable | 0 | 0.08 | - | 1 | - | 1.00 (5) | - | - (2) | - | 6.00 | 0.03 | - |
| mongodb-js/devtools-shared | stable | 0 | 0.04 | 0.55 | 3 | 0 | 0.75 (8) | 3.60 | 0.27 (11) | 3.00 | 19.00 | 0.06 | - |
| charmbracelet/lipgloss | stable | 0 | 0.43 | 0.14 | 8 | 20 | 0.67 (6) | 21.90 | 0.72 (111) | 4.00 | 4.00 | 2.83 | - |
| expressjs/serve-static | guardian | 0 | 0.62 | 0.56 | 1 | 14 | 0.60 (5) | - | - (9) | - | 1.00 | 0.75 | - |
| masci/banks | stable | 0 | 0.22 | - | 2 | - | 0.60 (5) | - | - (4) | - | 1.00 | 0.50 | - |
| langchain-ai/agent-protocol | stable | 0 | 0.00 | - | 0 | - | 0.57 (7) | - | - (4) | - | 7.00 | 0.08 | - |
| huggingface/xet-core | stable | 0 | 0.04 | 0.26 | 8 | 1 | 0.55 (11) | 4.00 | 0.37 (43) | 4.00 | 10.00 | 0.94 | -0.24 |
| agronholm/anyio | guardian | 0 | 0.53 | 0.49 | 63 | 0 | 0.40 (10) | 1.40 | 0.27 (244) | 1.00 | 1.00 | 27.17 | - |
| aio-libs/aiohappyeyeballs | stable | 0 | 0.07 | - | 0 | - | 0.40 (5) | - | - (3) | - | 2.00 | 0.38 | - |
| andfoy/pywinpty | stable | 0 | 0.11 | 0.80 | 3 | 2 | 0.40 (5) | - | - (5) | - | 1.00 | 1.17 | - |
| expressjs/cors | guardian | 0 | 0.62 | 0.14 | 4 | 115 | 0.40 (5) | 113.20 | 0.83 (35) | 2.00 | 1.00 | 3.33 | - |
| pypa/build | stable | 0 | 0.18 | 0.59 | 23 | 0 | 0.40 (5) | 0.30 | 0.15 (54) | 3.00 | 3.00 | 2.47 | 0.12 |

**open_door with no_insider_response_share >= 0.4** (48)

| repo | profile | ready | open | accept | debuts | rev_med | conv(n) | resp_days | no_resp(n) | rev_div | active | demand | gap |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| kubernetes-sigs/structured-merge-diff | open_door | 1 | 1.00 | 0.80 | 4 | 0 | 0.46 (11) | 4.20 | 1.00 (35) | 0.00 | - | - | - |
| kubernetes/kube-openapi | open_door | 1 | 1.00 | 0.59 | 7 | 1 | 0.00 (6) | 2.00 | 1.00 (75) | 0.00 | - | - | - |
| omnilib/aiosqlite | open_door | 0 | 0.57 | 0.20 | 4 | 27 | - (2) | 25.60 | 0.95 (20) | 0.00 | 0.00 | - | - |
| kubernetes/klog | open_door | 0 | 1.00 | 0.67 | 2 | 4 | - (2) | 16.60 | 0.92 (12) | 0.00 | 1.00 | 1.33 | - |
| csstree/csstree | open_door | 0 | 0.33 | 0.27 | 3 | 63 | 0.80 (5) | 61.80 | 0.91 (22) | 0.00 | 1.00 | 3.00 | - |
| kubernetes/utils | open_door | 0 | 0.71 | 0.50 | 3 | 3 | - (4) | 5.20 | 0.90 (20) | 1.00 | 1.00 | 1.92 | - |
| gin-gonic/gin | open_door | 0 | 0.78 | 0.21 | 46 | 23 | 0.19 (37) | 39.20 | 0.81 (324) | 1.00 | 1.00 | 31.33 | - |
| google/flatbuffers | open_door | 0 | 0.67 | 0.22 | 50 | 22 | 0.24 (33) | 21.60 | 0.78 (458) | 5.00 | 3.00 | 16.64 | 0.12 |
| pillarjs/router | open_door | 0 | 0.67 | 0.40 | 4 | 67 | - (4) | 87.20 | 0.73 (15) | 2.00 | 4.00 | 0.48 | - |
| ipython/traitlets | open_door | 0 | 0.12 | 0.21 | 4 | 36 | - (2) | 36.00 | 0.71 (24) | 0.00 | 2.00 | 1.21 | - |
| arsenetar/send2trash | open_door | 0 | 0.40 | 0.31 | 2 | 5 | - (1) | 11.60 | 0.69 (13) | 1.00 | 1.00 | 1.67 | - |
| popperjs/popper-core | open_door | 0 | 0.37 | 0.40 | 17 | 17 | 0.23 (13) | 22.20 | 0.67 (55) | 2.00 | 2.00 | 3.62 | - |

**today's review fast (<= 3 days) but insider median >= 14 days** (9)

| repo | profile | ready | open | accept | debuts | rev_med | conv(n) | resp_days | no_resp(n) | rev_div | active | demand | gap |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| unjs/ofetch | stable | 0 | - | 0.04 | 2 | 2 | - (4) | 112.10 | 0.91 (80) | 0.00 | 0.00 | - | - |
| openai/openai-python | stable | 0 | 0.15 | 0.08 | 43 | 0 | 0.10 (29) | 67.60 | 0.38 (658) | 6.00 | 9.00 | 7.81 | 0.04 |
| pillarjs/send | guardian | 0 | 0.71 | 0.31 | 0 | 1 | - (2) | 61.70 | 0.62 (16) | 1.00 | 0.00 | - | - |
| unjs/destr | stable | 0 | - | 0.00 | 0 | 0 | - (2) | 53.40 | 0.67 (18) | 0.00 | 1.00 | 1.75 | - |
| unjs/radix3 | stable | 0 | 0.04 | 0.31 | 3 | 0 | - (4) | 28.50 | 0.23 (13) | 1.00 | 2.00 | 1.33 | 0.48 |
| aio-libs/frozenlist | open_door | 1 | 0.37 | 0.39 | 6 | 0 | - (4) | 25.30 | 0.50 (18) | 2.00 | 3.00 | 0.78 | - |
| fb55/css-select | stable | 0 | 0.00 | 0.00 | 0 | 0 | - (1) | 19.20 | 0.92 (12) | 0.00 | 1.00 | 1.83 | - |
| micromatch/braces | guardian | 0 | - | 0.00 | 0 | 2 | - (3) | 17.40 | 1.00 (14) | 0.00 | 0.00 | - | - |
| aio-libs/async-lru | open_door | 0 | 0.38 | 0.50 | 3 | 3 | - (3) | 15.50 | 0.50 (18) | 2.00 | 2.00 | 0.88 | - |

**reviewer_diversity = 1 and demand >= 5/month per active maintainer** (39)

| repo | profile | ready | open | accept | debuts | rev_med | conv(n) | resp_days | no_resp(n) | rev_div | active | demand | gap |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pydantic/httpx2 | open_door | 1 | 0.30 | 0.56 | 30 | 0 | - (0) | 6.50 | 0.37 (118) | 1.00 | 2.00 | 43.71 | -0.58 |
| fsspec/filesystem_spec | open_door | 0 | 0.92 | 0.73 | 118 | 1 | 0.17 (36) | 2.10 | 0.21 (364) | 1.00 | 1.00 | 37.00 | - |
| kludex/starlette | open_door | 0 | 0.31 | 0.20 | 54 | 0 | 0.16 (31) | 2.50 | 0.20 (339) | 1.00 | 1.00 | 31.42 | -0.12 |
| gin-gonic/gin | open_door | 0 | 0.78 | 0.21 | 46 | 23 | 0.19 (37) | 39.20 | 0.81 (324) | 1.00 | 1.00 | 31.33 | - |
| h3js/h3 | open_door | 0 | 0.39 | 0.65 | 53 | 0 | 0.35 (40) | 0.80 | 0.18 (249) | 1.00 | 1.00 | 28.08 | - |
| agronholm/anyio | guardian | 0 | 0.53 | 0.49 | 63 | 0 | 0.40 (10) | 1.40 | 0.27 (244) | 1.00 | 1.00 | 27.17 | - |
| valyala/fasthttp | open_door | 0 | 0.68 | 0.80 | 50 | 0 | 0.21 (14) | 1.70 | 0.09 (210) | 1.00 | 1.00 | 24.83 | - |
| textualize/rich | stable | 0 | 0.22 | 0.06 | 11 | 1 | 0.00 (9) | 8.70 | 0.58 (174) | 1.00 | 1.00 | 23.00 | - |
| shikijs/shiki | open_door | 1 | 0.49 | 0.38 | 52 | 2 | 0.23 (51) | 4.40 | 0.31 (179) | 1.00 | 1.00 | 19.92 | - |
| tqdm/tqdm | stable | 0 | 0.48 | 0.14 | 20 | 18 | - (0) | 28.70 | 0.80 (152) | 1.00 | 1.00 | 16.58 | - |
| python-poetry/tomlkit | open_door | 0 | 0.85 | 0.55 | 40 | 2 | 0.20 (5) | 9.40 | 0.35 (149) | 1.00 | 1.00 | 16.50 | - |
| bruits/satteri | open_door | 1 | 0.15 | 0.80 | 19 | 0 | - (0) | 0.50 | 0.14 (64) | 1.00 | 1.00 | 14.67 | - |

**active_maintainers = 0 (everyone on a break) but outside PRs keep coming (10+)** (30)

| repo | profile | ready | open | accept | debuts | rev_med | conv(n) | resp_days | no_resp(n) | rev_div | active | demand | gap |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ajv-validator/ajv | guardian | 0 | 0.10 | 0.02 | 1 | 101 | - (1) | 110.60 | 0.93 (60) | 0.00 | 0.00 | - | - |
| auth0/node-jsonwebtoken | stable | 0 | 0.00 | 0.00 | 0 | 113 | - (0) | 131.40 | 1.00 (29) | 0.00 | 0.00 | - | - |
| fatih/color | stable | 0 | - | 0.12 | 3 | 29 | - (2) | 39.30 | 0.92 (24) | 0.00 | 0.00 | - | - |
| form-data/form-data | stable | 0 | - | 0.00 | 0 | 134 | - (3) | 132.30 | 0.90 (10) | 1.00 | 0.00 | - | - |
| goccy/go-yaml | stable | 0 | 0.85 | 0.11 | 6 | 40 | 0.22 (18) | 58.70 | 0.93 (98) | 1.00 | 0.00 | - | - |
| google/uuid | stable | 0 | - | 0.00 | 0 | 113 | - (1) | 111.50 | 1.00 (19) | 0.00 | 0.00 | - | - |
| gorilla/websocket | stable | 0 | - | 0.00 | 0 | 63 | - (1) | 61.60 | 1.00 (21) | 0.00 | 0.00 | - | - |
| h2non/filetype.py | stable | 0 | - | 0.00 | 0 | 11 | - (1) | 21.80 | 1.00 (22) | 0.00 | 0.00 | - | - |
| istanbuljs/istanbuljs | stable | 0 | - | 0.00 | 0 | 99 | - (3) | 121.40 | 1.00 (18) | 0.00 | 0.00 | - | - |
| jinzhu/now | stable | 0 | - | 0.00 | 0 | 31 | - (2) | 29.40 | 1.00 (11) | 0.00 | 0.00 | - | - |
| josdejong/workerpool | stable | 0 | 0.19 | 0.30 | 0 | 6 | - (3) | 6.20 | 0.70 (10) | 1.00 | 0.00 | - | - |
| jshttp/mime-types | open_door | 0 | 0.91 | 0.50 | 3 | 0 | - (3) | 1.40 | 0.50 (20) | 2.00 | 0.00 | - | - |

**open_door with conversion <= 0.15** (18)

| repo | profile | ready | open | accept | debuts | rev_med | conv(n) | resp_days | no_resp(n) | rev_div | active | demand | gap |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| immerjs/immer | open_door | 0 | 0.64 | 0.68 | 29 | 10 | 0.00 (8) | 12.20 | 0.19 (64) | 2.00 | 2.00 | 3.50 | - |
| ipython/ipykernel | open_door | 1 | 0.48 | 0.74 | 16 | 3 | 0.00 (8) | 3.70 | 0.20 (39) | 5.00 | 5.00 | 1.03 | - |
| kubernetes/kube-openapi | open_door | 1 | 1.00 | 0.59 | 7 | 1 | 0.00 (6) | 2.00 | 1.00 (75) | 0.00 | - | - | - |
| pypa/trove-classifiers | open_door | 0 | 1.00 | 0.39 | 7 | 25 | 0.00 (11) | 24.50 | 0.64 (28) | 2.00 | 2.00 | 1.54 | - |
| seek-oss/capsize | open_door | 0 | 0.57 | 1 | 1 | 0 | 0.00 (5) | 0.00 | 0.00 (21) | 2.00 | 1.00 | 1.92 | - |
| klauspost/compress | open_door | 0 | 0.66 | 0.78 | 32 | 0 | 0.08 (12) | 0.70 | 0.13 (98) | 1.00 | 1.00 | 10.50 | - |
| jaredwray/cacheable | open_door | 1 | 0.02 | 0.88 | 7 | 0 | 0.09 (23) | - | - (8) | - | 1.00 | 3.83 | - |
| go-playground/validator | open_door | 1 | 0.82 | 0.56 | 44 | 3 | 0.09 (33) | 6.90 | 0.31 (99) | 3.00 | 3.00 | 3.83 | - |
| prometheus/common | open_door | 1 | 0.33 | 0.35 | 12 | 11 | 0.09 (11) | 14.00 | 0.49 (57) | 6.00 | 9.00 | 0.61 | 0.35 |
| joblib/joblib | open_door | 0 | 0.54 | 0.37 | 17 | 2 | 0.10 (10) | 3.90 | 0.33 (90) | 4.00 | 6.00 | 1.89 | 0.32 |
| motdotla/dotenv | open_door | 1 | 0.15 | 0.28 | 26 | 7 | 0.10 (10) | 7.70 | 0.61 (99) | 1.00 | 1.00 | 10.33 | - |
| vega/altair | open_door | 1 | 0.27 | 0.46 | 21 | 6 | 0.12 (8) | 7.10 | 0.47 (76) | 4.00 | 3.00 | 3.42 | 0.04 |

## 5. Entry-path counts (now)

demand p75 = 2.69

| Path rule | projects |
|---|---|
| review: reviewer_diversity <= 1, demand >= p75, and someone answers (no_resp <= 0.5) | 55 |
| triage: demand >= p75 and active_maintainers 1-2 | 105 |
| successor: active_maintainers = 0, insiders > 0, demand > 0 issues/PRs | 93 |
| code for beginners: conversion >= 0.3 and no_resp <= 0.3 | 18 |

## 6. Candidate rules v1: counts

demand p25 = 0.25, p75 = 2.69

| Level | good | ok | bad | insufficient |
|---|---|---|---|---|
| beginner | 62 | 74 | 304 | 517 |
| intermediate | 84 | 97 | 189 | 587 |
| experienced | 69 | 450 | 72 | 366 |

beginner reasons: [('bad', 'guardian', 133), ('bad', 'nobody active', 88), ('bad', 'outside PRs go unanswered', 83), ('good', 'all pass', 62), ('insufficient', '<10 outside PRs', 371), ('insufficient', 'large/truncated repo', 112), ('insufficient', 'no PRs since 2018', 34), ('ok', 'partial', 74)] 

intermediate reasons: [('bad', 'nobody active', 120), ('bad', 'outside PRs go unanswered', 69), ('good', 'door works', 84), ('insufficient', '<10 outside PRs', 441), ('insufficient', 'large/truncated repo', 112), ('insufficient', 'no PRs since 2018', 34), ('ok', 'partial', 97)] 

experienced reasons: [('bad', 'door closed despite activity', 72), ('good', 'high demand, door works', 69), ('insufficient', 'no maintainer', 193), ('insufficient', 'large/truncated repo', 112), ('insufficient', 'no PRs since 2018', 34), ('insufficient', 'no activity to read', 27), ('ok', 'low or average demand', 357), ('ok', 'successor wanted', 93)] 

Sanity only (concurrent, same window as the rules): conversion@now by v1 rating:
| Level | rating | repos | mean conv | pooled conv | cohort people |
|---|---|---|---|---|---|
| beginner | good | 33 | 0.33 | 0.31 | 464 |
| beginner | ok | 37 | 0.18 | 0.19 | 695 |
| beginner | bad | 53 | 0.21 | 0.19 | 600 |
| beginner | insufficient | 10 | 0.37 | 0.30 | 73 |
| intermediate | good | 46 | 0.29 | 0.29 | 564 |
| intermediate | ok | 43 | 0.18 | 0.19 | 820 |
| intermediate | bad | 32 | 0.22 | 0.19 | 365 |
| intermediate | insufficient | 12 | 0.36 | 0.30 | 83 |
| experienced | good | 42 | 0.23 | 0.23 | 701 |
| experienced | ok | 60 | 0.28 | 0.25 | 732 |
| experienced | bad | 29 | 0.19 | 0.15 | 382 |
| experienced | insufficient | 2 | 0.23 | 0.29 | 17 |

Backtest of the v1 beginner rule: rated with data before 2025-10, outcome conversion@now:
| Level | rating | repos | mean conv | pooled conv | cohort people |
|---|---|---|---|---|---|
| beginner @T=2025-10 | good | 43 | 0.26 | 0.25 | 805 |
| beginner @T=2025-10 | ok | 42 | 0.19 | 0.18 | 649 |
| beginner @T=2025-10 | bad | 31 | 0.25 | 0.22 | 281 |
| beginner @T=2025-10 | insufficient | 17 | 0.32 | 0.32 | 97 |

Today's ready=True (30) under v1 beginner: {'ok': 15, 'good': 32, 'bad': 7, 'insufficient': 3}
Today's profile x v1 beginner:
| profile | good | ok | bad | insufficient |
|---|---|---|---|---|
| open_door | 56 | 45 | 37 | 102 |
| stable | 6 | 27 | 133 | 398 |
| guardian | 0 | 0 | 133 | 16 |
| needs_hands | 0 | 2 | 1 | 1 |

v1 beginner good: ['agronholm/exceptiongroup', 'aio-libs/multidict', 'aio-libs/propcache', 'antfu-collective/package-manager-detector', 'bombshell-dev/clack', 'bruits/satteri', 'celery/billiard', 'celery/kombu', 'celery/py-amqp', 'dpranke/pyjson5', 'eslint/rewrite', 'expressjs/body-parser', 'fastify/fast-uri', 'fsspec/filesystem_spec', 'gorakhargosh/watchdog', 'grahamdumpleton/wrapt', 'h3js/crossws', 'h3js/h3', 'joblib/threadpoolctl', 'jshttp/content-disposition', 'jupyterlab/jupyter-builder', 'kaelzhang/node-ignore', 'kludex/python-multipart', 'lxml/lxml', 'mdn/data', 'microsoft/debugpy', 'mltframework/shotcut', 'molecule-man/go-brrr', 'mongodb/mongo-go-driver', 'nltk/nltk', 'nucleic/kiwi', 'olekukonko/tablewriter', 'postcss/postcss', 'prometheus/client_golang', 'prometheus/procfs', 'psf/cachecontrol', 'pypa/build', 'pypa/distlib', 'pypa/packaging', 'pytest-dev/pluggy', 'python-cffi/cffi', 'python/typing_extensions', 'reduxjs/redux', 'reduxjs/redux-toolkit', 'rich-harris/magic-string', 'rolldown/plugins', 'scrapy/cssselect', 'scrapy/w3lib', 'sindresorhus/type-fest', 'stefankoegl/python-json-patch', 'stretchr/objx', 'styled-components/styled-components', 'sveltejs/esrap', 'tinylib/msgp', 'tinylibs/tinyexec', 'tox-dev/filelock', 'tox-dev/platformdirs', 'tox-dev/python-discovery', 'valyala/fasthttp', 'webpack/minimizer-webpack-plugin', 'yaml/go-yaml', 'zopefoundation/zope.interface'] 

today ready but v1 beginner not good: [('aio-libs/frozenlist', ('ok', 'partial')), ('aio-libs/yarl', ('bad', 'outside PRs go unanswered')), ('bytedance/sonic', ('bad', 'outside PRs go unanswered')), ('fonttools/fonttools', ('ok', 'partial')), ('go-playground/validator', ('ok', 'partial')), ('google/brotli', ('bad', 'outside PRs go unanswered')), ('huggingface/huggingface.js', ('ok', 'partial')), ('ipython/ipykernel', ('ok', 'partial')), ('jaredwray/cacheable', ('insufficient', '<10 outside PRs')), ('kpdecker/jsdiff', ('ok', 'partial')), ('kubernetes-sigs/structured-merge-diff', ('bad', 'outside PRs go unanswered')), ('kubernetes/kube-openapi', ('bad', 'outside PRs go unanswered')), ('mongodb/js-bson', ('ok', 'partial')), ('motdotla/dotenv', ('bad', 'outside PRs go unanswered')), ('narwhals-dev/narwhals', ('insufficient', 'large/truncated repo')), ('privatenumber/get-tsconfig', ('insufficient', '<10 outside PRs')), ('prometheus/client_python', ('ok', 'partial')), ('prometheus/common', ('ok', 'partial')), ('pyca/pyopenssl', ('ok', 'partial')), ('pydantic/httpx2', ('ok', 'partial')), ('pyparsing/pyparsing', ('bad', 'outside PRs go unanswered')), ('shikijs/shiki', ('ok', 'partial')), ('tornadoweb/tornado', ('ok', 'partial')), ('vega/altair', ('ok', 'partial')), ('websocket-client/websocket-client', ('ok', 'partial'))] 

v1 experienced good (top demand): [(43.71, 'pydantic/httpx2'), (37.0, 'fsspec/filesystem_spec'), (31.42, 'kludex/starlette'), (28.08, 'h3js/h3'), (27.17, 'agronholm/anyio'), (24.83, 'valyala/fasthttp'), (19.92, 'shikijs/shiki'), (18.0, 'celery/kombu'), (16.5, 'python-poetry/tomlkit'), (14.67, 'bruits/satteri'), (14.17, 'gorakhargosh/watchdog'), (13.17, 'tox-dev/filelock'), (11.08, 'tornadoweb/tornado'), (10.5, 'klauspost/compress'), (9.92, 'socketio/socket.io')] 

conversion half-width at p=0.2, n=5: ±0.35
conversion half-width at p=0.2, n=10: ±0.25
conversion half-width at p=0.2, n=20: ±0.18
conversion half-width at p=0.2, n=50: ±0.11

Fast insider response (<= 2 days) but outside acceptance today < 0.1: [('pallets/flask', 0.0, 0.04), ('pallets/itsdangerous', 0.0, 0.0), ('pallets/jinja', 0.0, 0.0)]
Mean conversion@now, flagged minus rest (bootstrap 95% CI):
| Flag | repos | flagged | diff | 95% CI |
|---|---|---|---|---|
| badge@T ready | 133 | 33 | +0.004 | [-0.069, +0.085] |
| v1 beginner good @T | 133 | 43 | +0.026 | [-0.041, +0.092] |
| TODAY ready (concurrent) | 133 | 35 | +0.020 | [-0.046, +0.090] |


code for beginners list (conv >= 0.3, no_resp <= 0.3): ['acornjs/acorn', 'agronholm/anyio', 'aio-libs/propcache', 'bombshell-dev/clack', 'eslint/rewrite', 'h3js/crossws', 'h3js/h3', 'lxml/lxml', 'mongodb-js/devtools-shared', 'prometheus/client_golang', 'pypa/build', 'python-cffi/cffi', 'python/typing_extensions', 'sveltejs/acorn-typescript', 'sveltejs/esrap', 'tinylib/msgp', 'tinylibs/tinyexec', 'yaml/go-yaml']
v1 beginner good with newcomer_open > 0: [('aio-libs/multidict', 1), ('bombshell-dev/clack', 1), ('expressjs/body-parser', 1), ('fsspec/filesystem_spec', 4), ('gorakhargosh/watchdog', 1), ('joblib/threadpoolctl', 2), ('jshttp/content-disposition', 1), ('mdn/data', 2), ('nltk/nltk', 9), ('nucleic/kiwi', 1), ('prometheus/client_golang', 20), ('pytest-dev/pluggy', 1), ('reduxjs/redux-toolkit', 1), ('sindresorhus/type-fest', 5), ('tinylib/msgp', 1), ('valyala/fasthttp', 14), ('webpack/minimizer-webpack-plugin', 1)]

## 7. Robustness

Cohort (participation rebuild, projects with conversion): 1789 people; merger/direct committer in another repo before 2025-10: 190 (10.6%); same owner: 33 (1.8%)
  pillarjs/router: cohort 0, insider elsewhere 0: []
  h3js/h3: cohort 39, insider elsewhere 2: [('patak-cat', ['vitejs/vite']), ('septatrix', ['python/typing_extensions'])]
  pypa/build: cohort 5, insider elsewhere 3: [('DimitriPapadopoulos', ['babel/babel', 'jaraco/jaraco.classes', 'jaraco/jaraco.context']), ('jayaddison', ['dulwich/dulwich', 'pallets/flask']), ('mgorny', ['dulwich/dulwich', 'pydantic/httpx2', 'pypa/distlib'])]
  celery/kombu: cohort 20, insider elsewhere 1: [('emmanuel-ferdman', ['dulwich/dulwich', 'pydantic/httpx2'])]
  jshttp/content-disposition: cohort 0, insider elsewhere 0: []
Repos where 30%+ of the cohort is an insider elsewhere: [('browserslist/browserslist', 3, 8), ('expressjs/serve-static', 2, 5), ('fxamacker/cbor', 2, 5), ('jshttp/mime-db', 5, 15), ('jupyter/jupyter_core', 2, 6), ('kubernetes-sigs/structured-merge-diff', 10, 11), ('kubernetes/kube-openapi', 3, 6), ('mongodb-js/mongodb-connection-string-url', 1, 1), ('pypa/build', 3, 5), ('pypa/packaging', 6, 14), ('sveltejs/acorn-typescript', 2, 4), ('tinylibs/tinyexec', 2, 5), ('unjs/unifont', 2, 6)]

v1 beginner good @T WITHOUT the conversion clause: repos 133, flagged 52, diff -0.002 [-0.065, +0.064]
conversion@T >= 0.1 alone (repos with conversion@T): repos 89, flagged 64, diff +0.091 [+0.035, +0.148]

No-PR projects: commits in last 24 months > 0: 0; direct commits > 0: 0; no commit row: 0

Guide mismatches, ecosyste.ms contributing path: []
