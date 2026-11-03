# OpenDoor integration collection, 2026-11-02

Working files (logs, points per step, `measure.py`, `queries.sql`, raw numbers) stayed in the collector's local session and are not in the repo; every number below was copied from them.

## Integration tree
- Worktree `/home/jose/Documentos/Projetos/hacktoberfest-int`, branch `local/integration-data` (not pushed), based on
  origin/jose/100-monthly-update, then merged 103, 104, 105, 106, and 103 again (ebbe696, the guide fix).
- Conflicts: `collect.py` (NEWCOMER_LABELS kept 103's 9-label list on top of #100's `update_large`; selftest asserts union,
  with 103's new `contributing_file` assert replacing the old `inherited_contributing` one; `main()` choices include
  `people`, `community`, `update`), `AGENTS.md` (command list union), `web/public/data/projects.json` (kept #100's).
- Local commits on top: `cmd_update` now runs `(cmd_repos, cmd_community, cmd_people, cmd_labels, cmd_topics)`;
  **`COMMUNITY_BATCH = 10`** in `cmd_community` (see problem 1). Patch: `integration-resolution.diff` (305 lines).
- Self-tests: collect, signals and sources all print `selftest ok` (also after the second 103 merge).
- Data: `data/` is tracked (holds `data/RELEASE` = data-2026-11-02), so `data/ecosystem.db` and `data/raw` are symlinks
  into `/home/jose/Documentos/Projetos/hacktoberfest-data2` (fetch-db ran first, files moved after: its atomic
  `replace()` and tar's `data` filter would break on pre-made symlinks). Note: the `data/raw` symlink shows as untracked
  (`.gitignore` has `data/raw/`, which matches only directories); never add it.
- Release stats: 975 repos (973 found), repo_monthly 50,259, participation 672,530.

## Problems found
1. **`community` with 50 repos per query times out**: GitHub answered 502/504 on every retry of the first batch
   (resolving CONTRIBUTING bodies is heavy). The failed attempt still cost 22 points. With 10 per batch it ran cleanly
   (98 queries, 22 points, no HTTP errors). **Branch 103 needs this fix** (the commit is ba496fc on the local branch).
2. The 3 new newcomer labels (`beginner-friendly`, `starter`, `low-hanging-fruit`) changed almost nothing; see Labels.
   A GraphQL check of label names (50 repos x 3 `labels(query:)`) also hit 502s and was stopped (6 points); not verified
   whether those labels exist in the set at all.

## GraphQL points
| step | before | after | spent |
|---|---|---|---|
| community, 1st attempt (batch 50, 502/504, stopped) | 4158 | 4136 | 22 |
| community (batch 10) | 4136 | 4114 | 22 |
| labels (after `DELETE FROM repo_labels`) | 4114 | 4100 | 14 |
| people --limit 5000 (quota reset mid-run) | 4100 | 4758 after reset | ~1,094 (1 per 100-login page: SUM(max(1, ceil(assignable/100))) = 1,094) |
| label-name check (stopped, 502s) | 4758 | 4752 | 6 |
| sources lists/ecosystems, signals, build | - | - | 0 |
| **total** | | | **~1,158** |
People also used REST (core quota) for public members.

## Community / CONTRIBUTING
- repo_community: 973 rows; 451 with a `contributing_url`; **162 inherited from the org `.github` repo**.
- 197 repos have a resolved contributing file that was not in `repo_files` before (rst, docs/, .github/, org-level).
- code of conduct 404, issue templates 126, discussions 193.

## Build effect (projects.json before vs after; 957 projects both)
- `guide` check: **196 flips, all False -> True** (247 -> 443 ok).
- `beginner.ready`: **14 flips False -> True** (43 -> 57): aio-libs/frozenlist, aio-libs/multidict, aio-libs/propcache,
  aio-libs/yarl, antfu-collective/package-manager-detector, expressjs/body-parser, fastify/fast-uri,
  kludex/python-multipart, privatenumber/get-tsconfig, pyca/pyopenssl, pypa/packaging, sindresorhus/type-fest,
  tox-dev/python-discovery, webpack/minimizer-webpack-plugin.
- profile flips: 7 (6 stable -> open_door, 1 needs_hands -> open_door), the ready rule promoting them.
- `git diff --stat web/public/data`: only `projects.json` (one-line file). Not committed.

## Labels
- Before (release DB, fetched today 19:46): 973 rows, 2,995 open newcomer issues, 177 repos > 0.
- After (9 labels): 973 rows, 2,994 issues, 178 repos > 0. Only 3 repos changed (apache/arrow 41 -> 40,
  gorakhargosh/watchdog 2 -> 1, pyca/pyopenssl 0 -> 1). The new labels add ~nothing for this repo set.

## People
- repo_people: **973/973 repos**, 22,328 assignable logins in total, **0 capped** (max 20 pages), public members known
  for 545 owners (the rest are users or None).

## Assignable users the behavioral rule calls outsiders
Rule (build.py): insider = merged a PR or made 3+ direct commits in 24 months. Counted: logins with merged PRs in the
last 12 months who are not insiders by that rule but are in `repo_assignable`.
- **164 repos**, **458 logins**, **4,112 merged PRs** in 12 months that today count as "from outside".

Top 20 by logins (openness = build.py value; the "if" column only for full repos, where openness comes from participation):

| repo | logins | their merged PRs (12m) | openness now | openness if assignable = insider | drop |
|---|---|---|---|---|---|
| godotengine/godot | 44 | 529 | 0.49 (sample) | - | ~0.54 on sample |
| freecad/freecad | 29 | 663 | 0.54 (sample) | - | ~0.43 |
| huggingface/huggingface_hub | 25 | 53 | 0.24 | - | ~0.06 |
| nextcloud/server | 13 | 38 | 0.56 | - | ~0.07 |
| open-telemetry/opentelemetry-python | 12 | 104 | 0.62 | - | ~0.27 |
| vuejs/core | 12 | 67 | 0.34 | - | ~0.08 |
| darktable-org/darktable | 11 | 631 | 0.63 | - | ~0.44 |
| obsproject/obs-studio | 11 | 62 | 0.47 | - | ~0.19 |
| pypa/packaging | 10 | 22 | 0.35 | 0.29 | 0.06 |
| vercel/workflow | 10 | 15 | 0.49 | - | ~0.02 |
| vitejs/vite | 10 | 162 | 0.47 | - | ~0.19 |
| kubernetes/kube-openapi | 9 | 38 | 1.00 | 0.14 | 0.86 |
| agronholm/anyio | 8 | 43 | 0.53 | 0.34 | 0.19 |
| kubernetes-sigs/structured-merge-diff | 8 | 27 | 1.00 | 0.04 | 0.96 |
| huggingface/huggingface.js | 7 | 9 | 0.30 | 0.29 | 0.01 |
| jellyfin/jellyfin | 6 | 40 | 0.19 | - | ~0.06 |
| webpack/webpack | 6 | 322 | 0.28 | - | ~0.24 |
| musescore/musescore | 5 | 29 | 0.25 | - | ~0.02 |
| prometheus/client_golang | 5 | 12 | 0.65 | 0.54 | 0.11 |
| swc-project/swc | 5 | 163 | 0.37 | - | ~0.29 |

"-" rows are sampled (large) repos: their openness comes from `repo_sample` (authorAssociation), not participation, so
the "~" drop is the share of the sampled merged PRs (12m) by those logins, i.e. how much the behavioral outsider share
on the sample would fall. Note the two measures disagree a lot for sampled repos (godot: 0.49 by authorAssociation
vs 0.91 behavioral on the sample).

- Full repos with an openness value affected: **105**; mean drop **0.14**; **42 drop by 0.10 or more**. Largest:
  structured-merge-diff 1.00 -> 0.04, kube-openapi 1.00 -> 0.14, kubernetes/klog 1.00 -> 0.25, pillarjs/send 0.71 -> 0.00,
  kubernetes/utils 0.71 -> 0.07, nodejs/cjs-module-lexer 0.77 -> 0.14, expressjs/serve-static 0.62 -> 0.12,
  seek-oss/capsize 0.57 -> 0.08 (Kubernetes repos merge through bots, so humans never show as mergers).
- Sampled repos affected: 43, mean drop ~0.10 on the sample share.
- **Mastodon** (sampled, openness `null` because 207/208 of the authorAssociation sample say "outside"): 20 assignable,
  0 capped, 9 public members. 1 assignable behavioral outsider, with **257 merged PRs** in 12 months (never
  merges). Behavioral outsider share on the sample: 388/1,530 = 0.25 -> 131/1,530 = **0.09** if assignable = insider.

## Other steps
- sources lists: goodfirstissue.dev 830 repos (30 in our set), Up For Grabs 1,319 (17), GSoC 2026 62 (3).
- sources ecosystems: 973 repo_ecosystems rows.
- signals run/backtest: ok (e.g. no_insider_response_share 281 repos, median 0.425; backtest as_of 2025-10 and 2026-10,
  859 repos each).
