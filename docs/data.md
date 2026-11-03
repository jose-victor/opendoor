# Data dictionary — `data/ecosystem.db`

## Getting and publishing the data
The database is not in git. Each collection is published as a GitHub Release tagged `data-YYYY-MM-DD`, with two files:
- `ecosystem.db.gz`: this database;
- `raw.tar.gz`: the raw API cache (`data/raw/`), so the aggregations can be recomputed (`collect.py reaggregate`) and `build.py` can compute review times.

```bash
python pipeline/collect.py fetch-db --raw    # the release named in data/RELEASE -> data/ecosystem.db and data/raw/
```
`fetch-db` refuses to overwrite an existing database unless you pass `--force`, and only replaces it after an integrity check.

### Monthly update
Once a month, after the month closes, a maintainer updates and publishes the data:
```bash
python pipeline/collect.py fetch-db --raw     # start from the current release (skip if data/ is up to date)
python pipeline/collect.py update             # refresh snapshots; fetch only what changed since the last run (1 to 2 h)
python pipeline/build.py                      # regenerate web/public/data/; compare with the published numbers
sqlite3 data/ecosystem.db VACUUM
cp data/ecosystem.db data/publish.db && sqlite3 data/publish.db "DROP TABLE IF EXISTS repo_assignable; VACUUM"  # who has access stays local
gzip -9c data/publish.db > data/ecosystem.db.gz && tar czf data/raw.tar.gz -C data raw
gh release create data-YYYY-MM-DD data/ecosystem.db.gz data/raw.tar.gz --latest=false \
  --title "Data: collection of YYYY-MM-DD" --notes "What changed in this collection."
echo data-YYYY-MM-DD > data/RELEASE           # commit it together with web/public/data/ in one PR
```
- `update` refreshes the snapshots (`repos`, then `community`, `people`, `labels`, `topics`) and fetches only PRs, issues and commits changed since the last run. Repos never collected get their full history. A repo already collected keeps its collection mode (full or sampled).
- It does not refresh the dependency graph (`graph`); run that now and then, followed by `repos` and `update`.
- CI downloads the release named in `data/RELEASE` and checks that `build.py` reproduces the committed JSON. Publishing a new release does not affect `main` until the PR that bumps `data/RELEASE` merges.
- Before publishing, compare the build with the published data (profiles, beginner badges). A large jump usually means a collection problem, not a real change.

## Conventions
A repository is always identified as `owner/name` in lowercase. Months use the `YYYY-MM` format, closed months only, starting at `2018-01`.

## Map
| Table | Contents |
|---|---|
| `repo_tags(repo, tag)` | where the repo came from: `npm-graph`, `pypi-graph` or `go-graph` (dependency graph of each ecosystem), or `mainstream-app` (hand-made list) |
| `seeds(system, name, version)` | seed packages of the graph |
| `packages(system, name, version, repo, dependents, direct_dependents)` — `system`: `npm`, `pypi` or `go` | each package in the graph; `dependents` = how many packages depend on it (deps.dev) |
| `dep_edges(system, seed, from_name, to_name)` | who depends on whom, per seed |

## Current snapshot
| Table | Contents |
|---|---|
| `repos` | description, language, license, creation, last push, archived, stars, forks, open and total issues/PRs; `found=0` = no longer exists |
| `repo_files(repo, path, oid, text)` | CONTRIBUTING, AGENTS, CLAUDE, AI_POLICY, copilot-instructions, README. `oid` changes when the file changes |
| `ai_policy(repo, classification, evidence, source_file, model, classified_at)` | AI policy classification from the texts in `repo_files`; `evidence` is literal, `source_file` and `evidence` are empty when no rule is confirmed, and `model` is null when the regex filter makes the model unnecessary |
| `repo_labels(repo, newcomer_open)` | open issues labeled "good first issue", "help wanted" and similar. After changing `NEWCOMER_LABELS`, take effect with `DELETE FROM repo_labels;` then `collect.py labels` |
| `repo_community(repo, contributing_url, contributing_inherited, code_of_conduct, issue_templates, pr_templates, security_policy_url, discussions, funding, fetched_at)` | community health from GitHub (`collect.py community`). `contributing_url` is whatever file GitHub resolves (any supported name or extension, in the repo, `docs/`, `.github/`, or the owner's `.github` repo). `contributing_inherited = 1` when it comes from the owner's `.github` repo. When the `repos` step found no CONTRIBUTING for the repo, `community` stores GitHub's body in `repo_files` (`oid` NULL) with the path from the URL: `<path>` for the repo's own file (e.g. `docs/contributing.rst`), `<owner>/.github/<path>` for an inherited one. Readers match `LIKE '%CONTRIBUTING%'` (case-insensitive); the `guide` check also passes when `contributing_url` is set. `issue_templates`, `pr_templates`, `discussions` are 0/1; `funding` is a JSON list of `{platform, url}` |
| `project_guides(repo, model, guide)` | "where to start" guide for each project (JSON of `Guide`; `steps_by_way` keys are `Way` ids), generated by `pipeline/guides.py`; each repo is asked once |
| `repo_opportunities(repo, model, suggestions)` | model suggestions (JSON list of `Opportunity`, with `way` as a `Way` id; the stored `source` is the old `"gemma"`, and `build.py` publishes it as `"gemini"`), generated by `pipeline/opportunities.py`; each repo is asked once |
| `repo_topics(repo, topics, languages)` | GitHub topics (JSON list) and languages with bytes (`{"C++": 639…}`); `topics` step, used in skill detection |
| `repo_scorecard(repo, overall, date)` / `scorecard_checks(repo, check_name, score, reason)` | OpenSSF Scorecard (0–10) and each check (Maintained, Code-Review, Branch-Protection...) |
| `package_advisories(system, name, version, advisory)` | vulnerability advisories for the current version |
| `external_lists(source, repo, label, extra, fetched_at)` | repos on newcomer-oriented lists, from `pipeline/sources.py lists`. `source`: `goodfirstissue_dev`, `up_for_grabs`, `gsoc_2026`. `repo` is lowercase `owner/name`; `label` is the project's own newcomer label (Up For Grabs only); `extra` is JSON (GSoC: `ideas_link`). Organizations that list only an org page are skipped |
| `repo_ecosystems(repo, funding, files, past_year, fetched_at)` | ecosyste.ms data for repos with `found = 1`, from `pipeline/sources.py ecosystems`. `funding` and `files` (JSON) come from `repos.ecosyste.ms` `metadata`; `past_year` (JSON) keeps the `past_year_*` fields of `issues.ecosyste.ms` (author associations, bot PRs, time to close...). Fields that mention e-mails are dropped. All NULL = unknown to ecosyste.ms. Raw responses in `data/raw/ecosystems/` |

## Monthly activity
| Table | Contents |
|---|---|
| `repo_monthly(repo, month, ...)` | issues opened/closed (completed or "not planned"), PRs opened/merged/closed without merge, reviews |
| `commit_monthly(repo, month, commits, direct_commits)` | commits on the main branch; `direct_commits` = no associated PR (landed without review) |
| `participation(repo, month, role, login, is_bot, n)` | **who played each role**, how many times in the month |
| `repo_assignable(repo, login)` | who GitHub lets be assigned on the repo (`assignableUsers`: write access plus some org members with read access; not every org member, e.g. microsoft/vscode has 85 assignable vs 1,000+ public members); sees private org members that `authorAssociation` misses. Up to 2,000 logins per repo. **Never published**: the release copy drops this table (see Monthly update), because it reveals private org membership |
| `repo_people(repo, assignable, capped, public_members, fetched_at)` | one row per repo: logins count, `capped` = hit the 20-page cap, `public_members` = public org members count (REST, max 1,000; `NULL` when the owner is a user) |

Roles in `participation.role`:
- `pr_author`, `pr_reviewer` (1 per PR, not counting the author), `pr_merger`, `pr_closer` (closed without merge);
- `merged_pr_author` (author of a merged PR, in the month of the merge);
- `issue_author`, `issue_closer`;
- `committer`, `direct_committer`.

Special logins: `ghost` = deleted account; `~Name` = commit author without a GitHub account.

## Signals (`pipeline/signals.py`)
`repo_signals(repo, signal, as_of, value, n)`: Tier 1 signals (design in `docs/deep-analysis.md`, section 5), computed offline from the activity raw cache for fully collected repos (`collection_mode` NULL, `activity_truncated = 0`). `as_of` (`YYYY-MM`) is the last closed month, as in `build.py` and `repo_monthly`: windows end at the first day of the **next** month, exclusive, and nothing from that day on is read. `run` writes every signal at the last closed month; `backtest` writes every signal 12 months earlier (T) plus `conversion` at T + 12. A repo whose raw cache was fetched before the window end is skipped (logged as stale). `n` is the sample behind the value; `value` is NULL when `n` is below the minimum.

Insiders at the window end: merged a PR or made 3+ direct commits in the 24 months before it (the `build.py` rule). Behavioral only, in `run` and `backtest` alike; variants that also use `repo_assignable` come later, under separate signal names. Outside PR = author is neither an insider nor a bot (`Bot` type, login ending in `bot` in any case, or the known list in `build.py`).

| `signal` | `value` | `n` (minimum) |
|---|---|---|
| `conversion` | of outsiders whose first merged PR fell in the 12 months that end 12 months before the window end (outsider = not an insider at the start of those 12 months, so a debut who becomes a maintainer later still counts), the share with another merged PR or a review on someone else's PR within 12 months of it | cohort (5) |
| `first_insider_response_days` | median days from an outside PR's creation (12 months) to the first insider review, merge or close (not a bot); unanswered PRs count the time waited until they were closed, or until the window end if still open | outside PRs (10) |
| `no_insider_response_share` | share of those PRs with no insider review, merge or close before the window end (closed without one still counts) | outside PRs (10) |
| `outsider_insider_gap` | insider acceptance minus outsider acceptance, PRs created in 12 months and decided before the window end; self-merged insider PRs left out | smaller side (10) |
| `reviewer_diversity` | distinct insiders who reviewed outside PRs of the 12 months (reviews only) | outside PRs (10) |
| `active_maintainers` | insiders not on a break: acted in the last 90 days, or the gap since their last action is within the 90th percentile of their own gaps (5+ gaps). Actions: merges, reviews, PR and issue closes, and `direct_committer` months from `participation` (dated the 15th); at most one action per day | insiders (1) |
| `demand_per_maintainer` | (new issues not by bots + new outside PRs) per month over 12 months, divided by `active_maintainers` | active maintainers (1) |

Retention backtest: pair the signals at T with `conversion` at T + 12 (the `run` row), whose cohort debuted in the 12 months before T and is followed up after it.

## Large repositories (`repos.collection_mode = 'sampled'`)
Above 6,000 issues + PRs we do not copy item by item (`collection_mode` is NULL for fully collected repos):
- `repo_monthly`: only `issues_opened`, `issues_closed`, `prs_opened` and `prs_merged`, which are **complete counts since 2018** from GitHub search. The other fields are NULL.
- `commit_monthly`: `commits` is complete; `direct_commits` is NULL.
- `repo_sample(repo, window_start, prs, human_prs, outsider_prs, first_timer_prs, mergers, authors)`: a sample of up to 300 PRs merged in the last 12 months. `outsider_prs` = the author is not a member, owner or collaborator (`authorAssociation`). `first_timer_prs` is almost always 0, because the association is today's: after the merge, the newcomer becomes a contributor.
- `participation` for these repos is partial (only the most recent period) and must not be used for yearly series.

## Coverage (read before comparing years)
- `repos.activity_since` / `repos.activity_truncated`: from when PRs and issues are complete. Huge repositories keep only the 3,000 most recent items per type.
- `commit_coverage(repo, since, truncated)`: the same for commits.
- Items opened before 2018 and closed after are not counted as closed.
- **Stars per year do not exist** (GitHub closed the list of who starred). Only the current total in `repos.stars`.

## Example queries

**Openness: share of merged PRs that came from non-maintainers (last 12 months)**
```sql
WITH win AS (SELECT * FROM participation WHERE month >= strftime('%Y-%m', 'now', '-12 months') AND is_bot = 0),
mergers AS (SELECT DISTINCT repo, login FROM participation WHERE role = 'pr_merger')
SELECT w.repo,
       SUM(w.n) AS merged_prs,
       SUM(CASE WHEN m.login IS NULL THEN w.n ELSE 0 END) AS from_outsiders,
       ROUND(1.0 * SUM(CASE WHEN m.login IS NULL THEN w.n ELSE 0 END) / SUM(w.n), 2) AS openness
FROM win w LEFT JOIN mergers m ON m.repo = w.repo AND m.login = w.login
JOIN repos r ON r.repo = w.repo AND r.collection_mode IS NULL  -- large repos: use repo_sample
WHERE w.role = 'merged_pr_author'
GROUP BY w.repo HAVING merged_prs >= 5 ORDER BY openness DESC;
```

**Guardians: widely used, a single person, direct commits**
```sql
WITH dep AS (SELECT repo, MAX(dependents) AS dependents FROM packages GROUP BY repo),
people AS (SELECT repo, COUNT(DISTINCT login) AS maintainers FROM participation
           WHERE role IN ('pr_merger', 'direct_committer') AND is_bot = 0
             AND month >= strftime('%Y-%m', 'now', '-24 months') GROUP BY repo)
SELECT d.repo, d.dependents, p.maintainers, s.overall AS scorecard
FROM dep d JOIN people p USING (repo) LEFT JOIN repo_scorecard s USING (repo)
WHERE p.maintainers <= 1 ORDER BY d.dependents DESC LIMIT 20;
```

**A project's health over the years**
```sql
SELECT substr(month, 1, 4) AS year, SUM(prs_opened) AS prs, SUM(prs_merged) AS merged, SUM(issues_opened) AS issues
FROM repo_monthly WHERE repo = 'expressjs/express' GROUP BY year;
```
