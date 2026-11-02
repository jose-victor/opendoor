# Data sources: what we can pull, and how much it overlaps with OpenDoor

Date: 2026-11-02. Follow-up of #83. It deepens `platforms-and-signals.md` (sections 1 and 5) with real downloads and overlap numbers; it does not repeat the platform descriptions. Numbers come from `pipeline/sources.py` run against the published database (975 repos, 973 with `repos.found = 1`). Reproduce with `python pipeline/sources.py lists` and `python pipeline/sources.py ecosystems`; tables are `external_lists` and `repo_ecosystems` (see `docs/data.md`).

## 1. Platform by platform

"Pull" = can a script fetch it, how, and what it costs. Nothing below uses the GitHub GraphQL token.

| Platform | What we use | Pull | Freshness | License / terms |
|---|---|---|---|---|
| goodfirstissue.dev (DeepSource) | `data/repositories.toml`: 830 repos, as `'github.com/owner/name'` strings | One raw file from raw.githubusercontent.com. Implemented (`lists`) | Last push 2026-03-02, so the list is aging | Repo is MIT. Site terms not found |
| Up For Grabs | `_data/projects/*.yml`: 1,412 files, 1,320 on GitHub (92 point elsewhere, mostly GitLab/Bitbucket/own sites). Gives the project's own newcomer label (`good first issue` 497, `help wanted` 298, `up-for-grabs` 243, `up for grabs` 74...) | One tarball from codeload.github.com (~1 request instead of 1,400). Implemented (`lists`) | Pushed daily; per-project `stats.last-updated` is filled by their tooling, entries are not pruned fast | Repo license is `NOASSERTION` (custom file). Each project file is the project's own listing |
| GSoC 2026 | `https://summerofcode.withgoogle.com/api/program/2026/organizations/`: 183 orgs, 151 with a GitHub `source_code`, only 62 of those point at a single repo (89 are org pages). Also `ideas_link` (all 183), `contributor_guidance_url` | One JSON call. Implemented (`lists`), skipped with a log line if it fails. Undocumented, can change | Yearly | No terms found for the endpoint. Treat as best effort |
| ecosyste.ms (`repos.`, `issues.`) | `metadata.files` (readme, contributing, code_of_conduct, codeowners, security, governance, agents, claude, cursor, copilot...), `metadata.funding`, and `past_year_*` issue/PR stats | REST JSON, no key. 973 repos x 2 calls took about 6 minutes with 4 workers and a polite `User-Agent`; no 429 happened. Responses carry `x-ratelimit-limit: 5000` per hour per IP (anonymous tier). Implemented (`ecosystems`) | `last_synced_at` is per repo: median 2026-11-02 01:24, but the oldest of 952 is 2023-11-05, so check it before trusting a number | The API docs say contact them for higher limits. The data license is not stated on the pages I read: **unverified**, check before redistributing the raw JSON. The service code is AGPL-3.0 |
| goodfirstissue.org | Nothing to pull (no list or API found) | Only scraping | n/a | n/a |
| CodeTriage | Subscription-based, no public list | None | n/a | n/a |
| First Timers Only | Advocacy site; no data | None | n/a | n/a |
| GitHub `/contribute` | No API | None | n/a | n/a |
| Hacktoberfest | The `hacktoberfest` topic is already in `repo_topics`: 36 of our 975 repos have it | Free, already collected | Per repo | n/a |
| Outreachy, LFX Mentorship | HTML project pages only (no feed found, as in `platforms-and-signals.md`) | Scraping only; not worth it for the gain | n/a | n/a |
| OpenSauced | Discontinued (archived 2025-03) | None | n/a | n/a |
| LFX Insights, Libraries.io | No documented public API (LFX); key needed (Libraries.io); both overlap with ecosyste.ms + deps.dev | Skipped | n/a | n/a |
| OpenSSF Scorecard, deps.dev | Already collected | Done | Per run | n/a |

## 2. Overlap with our repos

Our set is built from dependency graphs (npm, PyPI, Go) and a list of mainstream apps, so it favors widely used libraries. The newcomer lists favor projects that asked to be listed. The result is that they barely meet.

| List | Listed repos (GitHub, single repo) | Already in our 975 | Not yet in our database |
|---|---|---|---|
| goodfirstissue.dev | 830 | 30 (3.6%) | 800 |
| Up For Grabs | 1,319 (one repo is listed twice) | 17 (1.3%) | 1,302 |
| GSoC 2026 | 62 | 3 (4.8%) | 59 |
| Union | 2,094 distinct | 36 | 2,058 |

- 114 repos are in at least two lists, so the lists agree with each other more (5%) than with us.
- No listed repo that we have is `found = 0`.
- GSoC at **owner level** is better: 151 GSoC organizations have a GitHub owner, and 12 of our repos live under 5 of those owners. For GSoC, the owner is the useful key, not the repo.
- Reading: the lists are **seeds for new repos** (#83), about 2,000 candidates we have never looked at, not a way to validate or enrich what we already have. As enrichment they touch 36 repos (3.7%). The Up For Grabs `label` is the one field with direct use: it tells us the project's own newcomer label for the 17 repos in common and for any repo we add later (`repo_labels` today only counts a fixed label list).
- Not done here: checking which of the 2,058 still pass the pipeline's filters (archived, no recent push). goodfirstissue.dev's own README says it filters on recent activity, Up For Grabs does not, so expect more dead entries there.

## 3. ecosyste.ms: what it adds

Result of the run: 973 repos stored, 963 with an `issues` record, 934 with `repos` metadata (the rest are unknown to ecosyste.ms).

- **Funding:** 465 repos have a funding block (508 none). Platforms: GitHub Sponsors 373, Open Collective 240, custom 183, Tidelift 147, Patreon 88, Buy Me a Coffee 87, Ko-fi 76, Liberapay 69. This is the data #65 wanted, at no GitHub cost.
- **Files detected:** CONTRIBUTING 279, SECURITY 289, CODE_OF_CONDUCT 143, CODEOWNERS 73, AGENTS 103, CLAUDE 54, copilot 19, cursor 6, GOVERNANCE 6.
  - Against our own `repo_files`: CONTRIBUTING agrees on 242 repos; ecosyste.ms finds 37 we miss, we find 12 it misses. Reason on their side (checked for expressjs/express in the earlier research): it only reads files inside the repo, as we do, so the 37 are likely paths we do not scan (for example `docs/` or `.github/` variants), not org-level files. Not verified per repo.
  - AGENTS/CLAUDE: we have all 113 that ecosyste.ms sees, plus 12 more.
- **Past-year PR stats:** see the cross-check below. Averages instead of medians, and "today's" author association (the same limit as in AGENTS.md).

## 4. Cross-check: our outside PR counts vs ecosyste.ms

Method. 20 repos spaced evenly (by PR volume) across the 172 full-collection repos with at least 20 non-bot PRs in the window. Window for us: PRs opened in the 12 closed months 2025-10 to 2026-09. "Ours outside" = `pr_author` PRs by non-bot logins that were not a PR merger or direct committer in the previous 24 months (the behavior rule in `build.py`). ecosyste.ms: `past_year_pull_request_author_associations_count`; "outside" = NONE + CONTRIBUTOR + FIRST_TIME_CONTRIBUTOR + FIRST_TIMER + MANNEQUIN; "minus bots" subtracts `past_year_bot_pull_requests_count`, because bots are counted in the associations.

| Repo | Ours, all non-bot | Ours outside | Eco total | Eco outside | Eco bot PRs | Eco outside minus bots |
|---|---|---|---|---|---|---|
| `huggingface/huggingface.js` | 675 | 442 | 509 | 412 | 41 | 371 |
| `urllib3/urllib3` | 328 | 268 | 411 | 347 | 38 | 309 |
| `fsspec/filesystem_spec` | 209 | 185 | 330 | 314 | 0 | 314 |
| `sindresorhus/type-fest` | 183 | 114 | 120 | 81 | 0 | 81 |
| `dubzzz/pure-rand` | 140 | 0 | 101 | 64 | 64 | 0 |
| `dateutil/dateutil` | 125 | 105 | 171 | 139 | 0 | 139 |
| `python-poetry/tomlkit` | 109 | 104 | 174 | 174 | 27 | 147 |
| `yargs/yargs` | 84 | 70 | 111 | 95 | 14 | 81 |
| `mltframework/shotcut` | 71 | 30 | 47 | 25 | 0 | 25 |
| `mongodb/js-bson` | 64 | 18 | 90 | 83 | 36 | 47 |
| `microsoft/debugpy` | 58 | 33 | 51 | 50 | 7 | 43 |
| `fastify/fast-uri` | 53 | 12 | 69 | 26 | 14 | 12 |
| `eemeli/yaml` | 49 | 31 | 48 | 39 | 0 | 39 |
| `7rulnik/source-map-js` | 43 | 2 | 3 | 3 | 0 | 3 |
| `expressjs/cors` | 40 | 35 | 47 | 39 | 11 | 28 |
| `zeromq/pyzmq` | 39 | 27 | 60 | 52 | 26 | 26 |
| `lovell/sharp-libvips` | 35 | 30 | 125 | 90 | 89 | 1 |
| `jsdom/whatwg-url` | 30 | 7 | 40 | 11 | 5 | 6 |
| `jshttp/cookie` | 28 | 16 | 31 | 18 | 3 | 15 |
| `emotion-js/emotion` | 25 | 22 | 25 | 21 | 0 | 21 |

Summary: the median ratio (eco outside minus bots / ours outside) is 1.0, and 10 of the 19 repos with a non-zero count are within +-25%. Where they differ:

1. **Bots are inside ecosyste.ms's associations.** `pure-rand` (64 of 64 outside are bots) and `sharp-libvips` (89 of 90) look wildly open until bots are removed. Subtracting the bot count fixes both. Our `is_bot` flag and theirs are not the same list (for example `sharp-libvips`: 74 vs 89), so a small gap remains.
2. **Insider definition.** We use behavior (merged or committed in 24 months). They use today's `authorAssociation`. This matters most where the maintainers have `MEMBER`, `OWNER` or `COLLABORATOR` today but also contributed as outsiders before (`fastify/fast-uri`: ours 12 outside of 53, theirs 26 outside; `mongodb/js-bson`, `jsdom/whatwg-url`). These cases are consistent with the known limit that association is the current state, but I did not trace individual PRs.
3. **Window and sync.** Ours ends at the last closed month (2025-10 to 2026-09); theirs is a rolling year up to `last_synced_at` (mostly 2026-11-01/02, so about one month newer). This explains a few percent, not the large gaps.
4. **Unexplained.** `source-map-js` (ours 43 PRs, 2 outside; theirs 3 total), `fsspec` and `sharp-libvips` (their total is 330 and 125 vs our non-bot 209 and 35 plus 74 bots). I did not find the cause. Candidates: a burst of PRs from one sync boundary, a different PR type filter, or ecosyste.ms counting only PRs it has fully synced. Do not use ecosyste.ms counts as ground truth for these.

Conclusion: ecosyste.ms is good as a **cheap sanity check and for funding/files**, not as a replacement for `participation`, because its insider rule cannot be changed, it mixes bots into associations, and its freshness varies per repo.

## 5. Recommendations

1. Keep the three lists as **seeds** (#83): add the unseen repos behind a filter (not archived, pushed in the last year) rather than all 2,058. Start with the 114 repos present in two or more lists.
2. Use the Up For Grabs `label` to extend `NEWCOMER_LABELS` per project.
3. Use `repo_ecosystems.funding` for #65 and `files` to cross-check the community-file checks; compare the 37 CONTRIBUTING mismatches before changing `POLICY_FILES`.
4. Do not wire ecosyste.ms PR counts into the score. If used, show them as a second opinion and always subtract bots.
5. Refresh `lists` before each monthly update (3 requests); refresh `ecosystems` only for new repos, since the command skips repos already stored (delete rows to re-fetch; the raw cache in `data/raw/ecosystems/` must be deleted too).
