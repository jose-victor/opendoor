# OpenDoor research: existing platforms and concrete data signals

Date: 2026-11-02. Scope: issues #83 (study similar platforms) and #86 (the deep-analysis agent). Everything marked **[verified]** was checked during this research, either by an API call or by reading the primary page. **[secondhand]** means a blog or search summary. **[unverified]** means from memory or not confirmed. "OpenDoor has it" refers to `docs/data.md` and `pipeline/build.py` as of commit 508bca4.

---

## 0. Actionable findings to fix first

1. **The `guide` beginner check misses CONTRIBUTING files that are inherited from the org.** [verified] `build.py` sets `has_guide` from `repo_files` rows with path `LIKE '%CONTRIBUTING.md'`. `collect.py` `POLICY_FILES` only looks inside the repo (`CONTRIBUTING.md`, `.github/`, `docs/`). GitHub resolves community files from the org's `.github` repo too. For `expressjs/express`, the published JSON says *"não tem guia de contribuição (CONTRIBUTING)"*, but:
   - GraphQL `repository{ contributingGuidelines{ url body } }` returns `https://github.com/expressjs/.github/blob/master/CONTRIBUTING.md`;
   - REST `GET /repos/expressjs/express/community/profile` has `files.contributing` set (health_percentage 87).

   Fix: read `contributingGuidelines{body}` in the existing `files` batch. It costs about 0 extra points, since it is one more field on a query already sent. The same fallback applies to `codeOfConduct`, `issueTemplates`, `pullRequestTemplates` and `securityPolicyUrl`. **How many repos this affects is unknown:** the local `data/` is empty. Run `collect.py fetch-db --raw` and diff against `contributingGuidelines` to count them.
2. **Misleading text for sampled repos.** [verified, minor] In `beginner_checks`, when `debuts is None` (large repos), the acceptance check prints *"poucas pessoas novas tentaram (289) para medir"* for express. That reads as "few tried" next to a big number. The real reason is "no debut data for large repos".
3. **An insider signal that sees private org members exists: `assignableUsers`.** [verified with a probe] For `mastodon/mastodon`, `orgs/mastodon/public_members` returns 9 logins. `repository.assignableUsers` returns 20: all 9 public ones plus 11 more (for example `ClearlyClaire`, `mjankowski`, `oneiros`). Those are almost certainly private members or collaborators. This is the exact case architecture.md says broke `authorAssociation` (Mastodon 100% outsiders vs ~25% real). GitHub docs say you can assign "anyone with write permissions to the repository, and organization members with read permissions to the repository" ([docs](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/assigning-issues-and-pull-requests-to-other-github-users)). **Caveat:** for huge orgs (microsoft, google), "org members with read" can include thousands of employees. That is still "insider" for OpenDoor's purpose, but it is a large paginated list (100 per page, about 1 point per page). Test it on Tailwind and on a big-org repo before relying on it.

---

## 1. Platforms

| Platform | What it does | Signals / curation | Alive? | Borrow / integrate |
|---|---|---|---|---|
| **goodfirstissue.dev** (DeepSource) | Lists open labeled issues from a curated repo list | Maintainers submit a form. README criteria: "At least 3 open issues with beginner-friendly labels", "At least 10 contributors", README with setup, CONTRIBUTING, "recent commits", OSI license ([README](https://github.com/DeepSourceCorp/good-first-issue)). The code (`gfi/populate.py`) is simpler: skips archived repos and repos pushed >90 days ago, needs ≥1 labeled issue and a detected language. Labels (`data/labels.json`): good first issue, good-first-issue, beginner, beginner-friendly, easy, first-timers-only, starter, help wanted, low-hanging-fruit | Yes, last push 2026-03 [verified] | `data/repositories.toml` = **830 curated repos** [verified], a ready seed list. Adding `beginner-friendly`, `starter` and `low-hanging-fruit` to `NEWCOMER_LABELS` is a one-line change. No API, but static JSON is generated |
| **goodfirstissue.org** (a different site) | Independent GFI index | Reads issues only from repos with a commit in the last 180 days. Skips repos that have >1,000 open issues **and** <100 stars. Treats `good first issue`, `help wanted` and `hacktoberfest` as "discovery signals, not guarantees" ([about](https://goodfirstissue.org/about)) | Yes | Its "signals, not guarantees" framing matches OpenDoor's "what the project does vs says". No API mentioned |
| **Up For Grabs** | Curated list of projects with a "grab" label | One YAML file per project in `_data/projects/` (name, desc, site, tags, `upforgrabs.{name,link}`). `stats` are filled by tooling from the GitHub API ([list-a-project.md](https://github.com/up-for-grabs/up-for-grabs.net/blob/gh-pages/docs/list-a-project.md)) | Yes, pushed today [verified] | **1,414 project files** (git tree count) [verified]. Each gives the project's *own* newcomer label name, which beats guessing labels. A seed source for #83 |
| **CodeTriage** | Emails subscribers one open issue per day to triage. Also has "doc methods" (undocumented methods to document, e.g. [codetriage.com/doc_methods/…](https://www.codetriage.com/doc_methods/899446698)) | Subscription + issues fetched from GitHub. No public scoring described ([repo](https://github.com/codetriage/CodeTriage)) | Yes, pushed 2026-10 | A model for OpenDoor's `triage` way: "one issue a day" as a habit. No public API |
| **First Timers Only** | Advocacy (Hanselman, Kent C. Dodds) for a `first-timers-only` label with very detailed, hand-held issues. The First Timers app turns `first-timers-*` branches into issues ([site](https://www.firsttimersonly.com/)) | No list or scoring. Links to Up For Grabs, goodfirstissue.dev and CodeTriage | Site up | The **issue-quality rubric** (small, steps described, maintainer commits to mentor) is a good LLM-evidence checklist for "is this GFI actually good?" |
| **GitHub GFI / `/contribute` / topics** | `github.com/<o>/<r>/contribute` lists approachable issues. Labels drive surfacing ([docs](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/encouraging-helpful-contributions-to-your-project-with-labels)) | **Dated (2020) blog:** ~300 curated label synonyms + an ML classifier on title/body only. Weak supervision: positives = labeled, or closed by a first-timer's PR, or closed by a tiny PR. Ranked by confidence with an age penalty; precision over recall ([blog](https://github.blog/2020-01-22-how-we-built-good-first-issues/)) | Feature exists. Current internals unknown | Borrow the **weak-label idea**: "issues closed by a first-timer's PR" and "closed by a one-file PR" are computable from data OpenDoor already caches (PR → closing issue). No API for `/contribute` |
| **Hacktoberfest** | October event. Repo opts in with the `hacktoberfest` topic. PR counts if merged, approved, or labeled `hacktoberfest-accepted`. `spam`/`invalid` labels exclude it. Accepted PRs wait a review window (7 or 14 days depending on source) | **[secondhand]**: the official participation page returned 404; sources are e.g. [DigitalOcean 2025](https://www.digitalocean.com/blog/how-to-participate-hacktoberfest-2025), [WP Tavern on opt-in](https://wptavern.com/hacktoberfest-adds-gitlab-support-updates-participation-requirements-to-combat-open-source-project-spam) | Yes (2025 edition) | Signals: `hacktoberfest` topic (OpenDoor already stores topics), `hacktoberfest-accepted` and `spam`/`invalid` label counts. A high spam-label ratio is a "this project is flooded" signal |
| **GSoC** | Annual paid mentorship. Orgs publish idea lists | Google selects orgs (185 in 2026 per [blog](https://opensource.googleblog.com/2026/02/introducing-the-185-organizations-for-gsoc-2026.html)) | Yes | **Undocumented JSON endpoint** `https://summerofcode.withgoogle.com/api/program/2026/organizations/` returns 183 orgs with `source_code`, `ideas_link`, `contributor_guidance_url`, `tech_tags`, `topic_tags` [verified 200]. Not documented, so it may change. A "mentored program" badge plus a link to the ideas page |
| **Outreachy** | Paid internships for underrepresented people, two cohorts a year | Communities apply and mentors are vetted | Yes | No documented machine-readable feed found (project pages are HTML) |
| **LFX Mentorship** | LF-run mentorship terms ([docs](https://docs.linuxfoundation.org/lfx/mentorship)) | Projects post programs | Yes | No documented public API found |
| **OpenSauced** | Contributor and repo insights (contributor lottery factor, "pizza" commit engine) | — | **Discontinued**: `open-sauced/app` archived 2025-03. The README says the team "now supports the LFX" after joining the Linux Foundation ([repo](https://github.com/open-sauced/app)). Hanselminutes, Dec 2024: "just joined the Linux Foundation" | Nothing to integrate. Its ideas live on in LFX Insights |
| **CHAOSS: Augur → CollectOSS; GrimoireLab** | Metric definitions + collectors/dashboards | Metrics such as New Contributors ("only consider their first contribution", [def](https://chaoss.community/metric-new-contributors/)), Time to First Response (filter bots, [def](https://github.com/chaoss/wg-common/blob/main/focus-areas/time/time-to-first-response.md)), Issue Response Time split by new vs long-time contributor ([def](https://chaoss.community/metric-issue-response-time/)). **Starter Project Health model** = Time to First Response, Change Request Closure Ratio, Bus Factor ("smallest number of people that make 50% of contributions"), Release Frequency ([model](https://chaoss.community/?p=4897)) | Augur archived 2026-07 and moved out of CHAOSS, replaced by **CollectOSS** ([chaoss/augur](https://github.com/chaoss/augur), [CollectOSS](https://github.com/chaoss/CollectOSS/)). GrimoireLab active (pushed 2026-10) | Use as **vocabulary and validation** for OpenDoor's rules (`response` ≈ TTFR, `acceptance` ≈ CR acceptance, add bus factor 50%). Heavy self-hosted stacks: don't run them |
| **LFX Insights** | Health Score 0–100 for >15k repos (GitHub, GitLab, Gerrit) | Published rubric ([health score](https://insights.linuxfoundation.org/docs/metrics/health-score/)). **Maintainer Health 40**: responsiveness (median human response to new issues/PRs: 15 pts <24 h … 0 ≥3 mo), bus factor (5+ active maintainers = 18), org diversity (3+ orgs = 7). **Security 35**: open vulns, SECURITY.md/branch protection/required reviews/status checks, Scorecard, dependency health. *The listed sub-maxima add up to 30, not 35, which is a doc inconsistency.* **Activity 25**: release cadence, commits in 6 months, issue close ratio + median time to close, PR merge ratio + median time to merge. Bands: 85+ Excellent … <30 Critical | Yes, relaunched 2025 ([CNCF](https://www.cncf.io/blog/2025/10/22/lfx-insights-a-new-way-to-understand-open-source-projects/)) | **Borrow the scoring style**: explicit thresholds → points → bands is the "rules decide" pattern #86 wants. Affiliation is inferred and not shown per person for privacy (per an [OpenStack thread](https://lists.openstack.org/archives/list/openstack-discuss@lists.openstack.org/thread/L63X443VSEOSTOQNG57GEDYSF3BX744L)). No documented public API found (third parties mention badge endpoints) [unverified] |
| **ecosyste.ms** | Open APIs for repos, packages, issues, commits | See below. Each record has `last_synced_at` | Very active (pushed 2026-10-30) | **Best integration candidate.** Free JSON, no key needed for light use. Rate limits and license: check [ecosyste.ms](https://ecosyste.ms) [unverified] |
| **Libraries.io** | Package discovery + SourceRank | SourceRank combines code, community, distribution, documentation and usage factors (README, license, semver, recent release, dependents, stars, contributors…) **[unverified, from memory; docs fetch failed]**, see [docs](https://docs.libraries.io/overview.html). API needs a key, ~60 req/min [unverified] | Repo active (2026-10-29) | Overlaps with deps.dev + ecosyste.ms. Low priority |
| **OpenSSF Scorecard** | Security checks 0–10 | Already used (`repo_scorecard`, `scorecard_checks`) | Active | Check scores like `Code-Review`, `Branch-Protection` and `Maintained` can feed "is it organized" for free |
| **New: GFI-Bot** (PKU, FSE'22 demo / ICSE'22) | ML GFI recommender + GitHub App ([repo](https://github.com/osslab-pku/gfi-bot)) | Issue + reporter + repo features | Pushed 2026-04, pre-alpha, 57 stars | Its feature list is a good reference for what predicts GFI success. Not worth depending on |
| **New: DeepWiki** (Cognition) | Replace `github.com` with `deepwiki.com` in a repo URL to get an AI wiki of the codebase with Q&A and line citations. Has an MCP server [secondhand: [apidog](https://apidog.com/blog/deepwiki)] | LLM over code | Active | A possible **tool for the #86 agent** ("which module handles X"). Third-party, so treat output as evidence to verify. Link it from the project page instead of re-generating code maps |
| **New: awesome-for-beginners / first-contributions** | Hand lists (91k stars) / practice repo (56k stars) | Manual curation | Active | Seed list (awesome-for-beginners). first-contributions is the classic "practice PR" step for absolute beginners |

### ecosyste.ms fields (verified on `expressjs/express`)
- `issues.ecosyste.ms/api/v1/hosts/GitHub/repositories/{owner}%2F{repo}`: `past_year_pull_request_author_associations_count` (`{NONE: 373, CONTRIBUTOR: 99, MEMBER: 45}`), `past_year_avg_time_to_close_pull_request`, `past_year_merged_pull_requests_count`, `past_year_bot_pull_requests_count`, `past_year_pull_request_authors` (login → count), `maintainers` / `active_maintainers` (method undocumented), label counts, avg comments per issue/PR. **Caveats:** averages, not medians. Associations are today's. "Maintainers" is undefined.
- `repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/{o}%2F{r}`: `metadata.files` detects **readme, contributing, code_of_conduct, codeowners, security, governance, roadmap, maintainers, support, dco, cla, agents, claude, gemini, cursor, copilot**… plus `metadata.funding` (e.g. `open_collective: express`) and `commit_stats.dds`. It reported `contributing: null` for express (it also misses the org-level file).
- `commits.ecosyste.ms/...`: `committers[]` with **name, email, login, count**, `past_year_committers`, `dds`. **Privacy:** this exposes e-mails. AGENTS.md forbids collecting them, so use them only transiently (see §3).

Use: a cheap cross-check of OpenDoor's numbers, and a source for `funding` (#65) and governance files, with no GitHub points spent.

---

## 2. Signal catalog (public GitHub + free sources)

Cost notes: GraphQL costs about 1 point per query below ~100 nodes. Aliased batches (as `collect.py` already does) cost 1 point per batch for counts. Points measured here: a query with 2 searches + a repo block + a user block cost **1 point** [verified]. REST calls use the separate 5,000/h core limit. "Text?" = whether you must read issue/PR/comment bodies. "Has" = OpenDoor already collects it.

### A. How open is it to outsiders?
| Signal | Source / field | Cost | Has | Text? |
|---|---|---|---|---|
| Share of landed changes from outsiders | `participation` (merged_pr_author vs pr_merger/direct_committer) | — | Yes (`openness`) | No |
| Outside PR acceptance, newcomer acceptance, debuts | raw `activity` cache | — | Yes | No |
| First response to outside PRs, stale share | raw cache reviews/close events | — | Yes (`review`) | No |
| First response to **outside issues** | `issues{ timelineItems(itemTypes:[ISSUE_COMMENT, LABELED_EVENT, CLOSED_EVENT], first:1){ ... createdAt actor/author{login} } }` | ~1 pt per 100 issues | **No** | No: only timestamps and author login of the first comment. The body is not needed |
| Review rounds before merge | `pullRequest.reviews{ state submittedAt }` count of `CHANGES_REQUESTED` | already fetched (first:30) | Partly (reviews stored without state) | No |
| Outsider PR closed-unmerged by maintainer within N days ("rejected fast") | close events | — | Derivable | No |
| Spam/invalid label ratio (AI-slop pressure) | `search(repo:X is:pr label:spam OR label:invalid)` `issueCount` | 1 pt per batch | No | No |
| Account age of new PR authors (agent / sockpuppet filter, per [Nesbitt 2026](https://nesbitt.io/2026/05/27/chaoss-metrics-in-2026.html)) | `user{ createdAt }` | 1 pt per ~100 users aliased | No | No |
| AI policy | `repo_files` + `ai_policy` | — | Yes | Yes, but it is repo policy text, not issue/PR content |

### B. Is it organized / what structure?
| Signal | Source / field | Cost | Has | Text? |
|---|---|---|---|---|
| Community files incl. org-inherited | GraphQL `contributingGuidelines{url body}`, `codeOfConduct{key}`, `issueTemplates{name}`, `pullRequestTemplates{filename}`, `securityPolicyUrl`, `hasDiscussionsEnabled`, `fundingLinks{platform url}`; REST `/community/profile` (`health_percentage`) | ~0 (extra fields) | Partly, and misses org defaults (§0.1) | No |
| CODEOWNERS / MAINTAINERS / GOVERNANCE / OWNERS / ROADMAP | `object(expression:"HEAD:.github/CODEOWNERS"){...on Blob{text}}`, same for `MAINTAINERS*`, `GOVERNANCE.md`, `OWNERS` (k8s), `ROADMAP.md`; or ecosyste.ms `metadata.files`. `GET /repos/{o}/{r}/codeowners/errors` validates it | ~0 in the files batch | No | No (repo files) |
| Label taxonomy (area/, kind/, priority/, triage state) | `repository.labels(first:100){name}` | ~1 pt | No (only the newcomer count) | No |
| Share of issues labeled / with milestone / triaged in N days | `issues{ labels{totalCount} milestone{title} }` | ~1 pt per 100 | No | No |
| Projects / milestones in use | `repository.projectsV2{totalCount}`, `milestones(states:OPEN){totalCount}` | ~0 | No | No |
| Review practice | Scorecard `Code-Review`, `Branch-Protection`; `direct_commits` | — | Yes | No |
| Release cadence | `releases(first:20){publishedAt}` / ecosyste.ms tags | ~1 | No | No |
| Bus factor (CHAOSS 50%) | `participation` | — | Derivable | No |

### C. Would it benefit from more people, and where?
| Signal | Source | Cost | Has | Text? |
|---|---|---|---|---|
| Open issues / PRs vs active maintainers | `repos`, `participation` | — | Yes (`triage`, `review` opportunities) | No |
| **Free** newcomer issues: labeled, no assignee, no open linked PR | `issues(states:OPEN, labels:[...]){ assignees{totalCount} timelineItems(itemTypes:[CROSS_REFERENCED_EVENT, CONNECTED_EVENT]){ nodes{ ...on CrossReferencedEvent{ willCloseTarget source{...on PullRequest{state}} } } } }` | ~1 pt per 100 [verified query shape] | No (only `newcomer_open` count) | No |
| Stale newcomer issues (age, last update) | `createdAt`, `updatedAt` | same | No | No |
| Docs/tests need | labels `documentation`/`tests`; Scorecard; presence of a `tests/` dir in the tree | ~1 | Partly (regex on CONTRIBUTING) | No |
| Translation need | i18n dirs (`locales/`, `*.po`), Weblate/Crowdin config (`crowdin.yml`) in the tree | ~1 | No | No |
| "Vague issue" share (refinement way) | issues without labels; template usage | ~1 per 100 | No | **Yes** for real quality. Computable transiently: have the LLM read the body, store only a boolean/score + issue number + URL |
| Weak-labeled GFIs (issues closed by a first-timer's PR, or by a 1-file PR) | PR `closingIssuesReferences`, `changedFiles`, author debut | ~1 per 100 PRs | Partly (debut data) | No |

### D. Who are the contributors?
| Signal | Source | Cost | Has | Text? |
|---|---|---|---|---|
| Insider by behavior (merged in 24m / ≥3 direct commits) | `participation` | — | Yes | No |
| Insider by permission (incl. private org members) | `assignableUsers` (§0.3) | 1 pt / 100 users | No | No |
| Public org members | REST `GET /orgs/{org}/public_members`; `user.organizations` (public only) | core REST | No | No |
| Collaborators list | `GET /repos/{o}/{r}/collaborators` → **403 "Must have push access"** [verified] | — | Unavailable | — |
| Profile `company` | `user{ company }` (free text, often null, e.g. `dougwilson` null) | 1 pt / ~100 | No | No (profile field, public) |
| Commit e-mail domain | GraphQL `commit.author.email` / ecosyste.ms `committers[].email` | ~1 per 100 commits | No | No, but **e-mail** (see §3) |
| Newcomer vs returning | first PR / first merged PR per login (see §3) | — | Yes for full repos (since 2018) | No |
| Bots / agents | `__typename == Bot`, login suffix, known list; account age | — | Yes (bots) | No |

### E. How easy is the first contribution?
| Signal | Source | Cost | Has | Text? |
|---|---|---|---|---|
| Setup docs present | README/CONTRIBUTING (`repo_files`) | — | Yes | Repo text (allowed) |
| Dev container | `object(expression:"HEAD:.devcontainer/devcontainer.json")`, `.devcontainer.json`; REST `GET /repos/{o}/{r}/codespaces/devcontainers` (returned `.devcontainer/devcontainer.json` for microsoft/vscode, needs an authenticated token) [verified] | ~0 / 1 REST | No | No |
| Gitpod | `.gitpod.yml`. **Deprecated:** Gitpod became Ona (Sep 2025), Classic PAYG ended 2025-10-15, `.gitpod.yml` replaced by devcontainer.json ([Ona](https://ona.com/stories/gitpod-classic-payg-sunset)). Treat as a legacy signal | ~0 | No | No |
| Reproducible toolchain | `Dockerfile`, `docker-compose.yml`, `flake.nix`, `devbox.json`, `.tool-versions`, `mise.toml`, `.nvmrc`, `.python-version`, `rust-toolchain.toml`, `go.mod` | ~0 (root tree listing: `object(expression:"HEAD:"){...on Tree{entries{name type}}}`) | No | No |
| Task runner + test command | `Makefile` targets (`test`, `setup`, `dev`), `justfile`, `Taskfile.yml`, `package.json` `scripts.test`, `tox.ini`/`noxfile.py`, `pyproject` `[tool.pytest]` | ~0 per file | No | No (repo files) |
| CI test steps | `.github/workflows/*.yml` `run:` lines (express has `ci.yml`, `legacy.yml`…) [verified] | ~0 per file | No | No |
| **Does the default branch build?** | REST `GET /repos/{o}/{r}/actions/runs?branch=<default>&per_page=50`: `conclusion`, `run_started_at`, `updated_at` → pass rate and **duration as a setup-time proxy** [verified: express 609 runs, ~1 min] | 1 REST | No | No |
| First-PR CI friction | fork PRs need workflow approval from a maintainer ([docs](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/approve-runs-from-forks)). The "first-time contributor" definition for this is not on that page | — | No | No |
| Repo size / languages | `diskUsage`, `languages` | ~0 | Partly (languages) | No |

---

## 3. Outsider vs insider, and "first-time contributor"

**`authorAssociation` is current state, proven by a probe.** [verified] Enum (introspection): `OWNER`, `MEMBER` ("member of the organization"), `COLLABORATOR`, `CONTRIBUTOR` ("has previously committed to the repository"), `FIRST_TIME_CONTRIBUTOR`, `FIRST_TIMER` ("has not previously committed to GitHub"), `MANNEQUIN`, `NONE`. Probe: `bjohansebas`'s **earliest** PR in express (#5814, 2024-08) reports `authorAssociation: MEMBER` today. So historical first-timer status cannot come from this field. It also misses private membership: architecture.md records private org members showing up as `CONTRIBUTOR` (the Mastodon case).

**Insider options, best first:**
1. **Behavior** (current OpenDoor rule: merged in 24m or ≥3 direct commits). Robust and needs no permissions. It misses insiders who never merge (triage-only staff, private members without merge rights).
2. **`assignableUsers`** (write access + org members with read). It sees private members (Mastodon: 20 vs 9 public) [verified]. The risk is very large lists in big orgs.
3. **CODEOWNERS / MAINTAINERS / OWNERS / GOVERNANCE files**: declared maintainers. Logins in CODEOWNERS (`@user`, `@org/team`; teams can't be expanded without org access).
4. **`orgs/{org}/public_members`, `user.organizations`**: public only, so a lower bound.
5. **Affiliation (company) for #59 "who is from the company"**: `user.company` (free text such as `@google`, often null) + **commit e-mail domain**. Privacy-preserving recipe: fetch the e-mail, map the domain → org label in memory (drop `gmail.com`, `users.noreply.github.com` and similar), store only `(repo, login, org_label)` or just the aggregate share. **Never store the address.** Note that this still means "collecting" it transiently, so it needs a maintainer decision against the AGENTS.md rule.

**First-time contributor options:**
1. **Full repos:** already done from the raw cache (first merged PR since 2018). Gap: someone whose first PR was before 2018 looks like a debut. Mitigate with option 2 for the few logins flagged as debuts.
2. **Per-author search:** `search(type:ISSUE, first:1, query:"repo:o/r is:pr is:merged author:LOGIN sort:created-asc")` returns the earliest merged PR. Aliased in batches, it cost 1 point for 2 searches here [verified]. This is the fix for **sampled (large) repos**: for each author in `repo_sample`, check whether their earliest merged PR falls in the window. Limits: search returns at most 1,000 results per query (fine with `first:1`) and has **secondary rate limits** on search. Exact numbers for GraphQL search are [unverified], so batch ~20 per query like `cmd_labels`.
3. Commit-based: `history(author:{id})` for the earliest commit, for direct-commit projects.
4. ecosyste.ms `past_year_pull_request_authors` vs all-time `pull_request_authors`: an author present only in the past year counts as new. Cheap, but it uses ecosyste.ms's sync window [unverified accuracy].
5. Agent filter: drop accounts created shortly before their first PR, or show them separately (Nesbitt's point that one identity ≠ one person in 2026).

---

## 4. Ease of local setup without running untrusted code locally

**Static (zero risk, cheap):** fetch the root tree + a fixed list of files in the existing `files` batch: devcontainer.json, Dockerfile/compose, Makefile/justfile/Taskfile, package.json `scripts`, tox/nox/pyproject, toolchain pins, `.github/workflows/*.yml`. Rules (not the LLM) can score:
- *one-command env* (devcontainer, or compose + Makefile `setup`);
- *declared test command* (scripts.test / make test / tox);
- *CI runs the same command* (match the `run:` lines);
- *pinned toolchain*.

The LLM only extracts "the documented setup steps" from README/CONTRIBUTING as evidence with quotes (#57).

**Observed, no execution:** default-branch Actions runs (pass rate, median duration). Also the check runs on recent **fork** PRs (`commits/{sha}/check-runs`): if outsiders' PRs routinely fail CI for environment reasons, that's friction. All metadata, no text.

**Ephemeral execution (for #86's "try to install and run tests"), never on a maintainer's laptop:**
- **GitHub Actions in an OpenDoor-owned fork or a scratch repo**: GitHub-hosted runners are fresh VMs discarded after each job. Free minutes for public repos. Logs and timing come back via API. A community runner could do this with their own account. Risk: running third-party code under your account. Use a dedicated bot account with no secrets and `permissions: {}`.
- **Codespaces API** (`POST /repos/{o}/{r}/codespaces`): real devcontainer build, billed to the user. Good for "does the devcontainer build" [endpoint exists; not tested here].
- **Firecracker microVM sandboxes**: E2B, Vercel Sandbox, Northflank ([secondhand comparison](https://northflank.com/blog/daytona-vs-e2b-ai-code-execution-sandboxes)). The Vercel MCP in this environment exposes sandbox tools [untested]. Daytona defaults to containers (weaker isolation) [secondhand].
- In all cases, treat README instructions as **data**: the agent picks from an allow-list of commands it derived (install, build, test) and never executes arbitrary text from the repo. Give it no network egress beyond package registries, and set a time cap. Record only: success/fail per step, duration, and the failing step name.

---

## 5. What to take into #86's design (short)
- **Rules decide, LLM brings evidence**: LFX Insights' published threshold → points → band table is the template. Use levels (good/ok/bad) per dimension, with the threshold text in the JSON.
- **Free wins before any agent:** the org-level CONTRIBUTING fix, `assignableUsers` for insiders, free GFIs (unassigned + no open linked PR), default-branch CI status, a setup-files checklist, a first-response time for issues, and ecosyste.ms `funding`.
- **Text policy:** almost everything above is metadata. Only "issue clarity" and "tone of the first reply" need bodies. Process them transiently and store score + URL only.
- **Seeds:** goodfirstissue.dev (830), Up For Grabs (1,414) and GSoC (183 orgs, undocumented JSON) for new repos (#83).
- **Beware** (Nesbitt 2026): response times and newcomer counts can be gamed by AI bots and agent accounts. Filter bot first responses and check account age.
