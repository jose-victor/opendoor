# Architecture and contracts

This file is the **contract between the parts** of OpenDoor. If you need to change something here, open an issue first, because other parts depend on it.

## Overview
```
PIPELINE (Python, runs ahead of time, on someone's machine)  SITE (Next.js on Vercel)
pipeline/collect.py ──> data/ecosystem.db                    web/
                             │                                ├─ app/page.tsx          home + filters + results
   pipeline/classify_ai_policy.py (LLM) ──> ai_policy         ├─ app/p/[...repo]/      project page
   pipeline/skills.py ──> (build.py)                          ├─ app/api/explain/      live LLM (server)
                             │                                ├─ lib/types.ts          types of this contract
pipeline/build.py ──> web/public/data/projects.json ─────────>├─ lib/match.ts          ranking in the browser
                      web/public/data/skills.json  ─────────> └─ lib/gemini.ts          Gemini API client (server only)
```
- **Project data is static.** The pipeline generates it and it is versioned in `web/public/data/`.
- **The match runs in the browser**, on top of `projects.json`.
- **Only `/api/explain` calls the model live.** The key stays on Vercel, never in the browser.
- **Not yet:** a database for maintainers registering projects and saved profiles (#69).

## `web/public/data/skills.json`: fixed vocabulary of the filters
```ts
type Skill = {
  id: string;           // "typescript", "frontend", "ai", "testing"...
  label: string;        // "Frontend web" (UI text, in Portuguese)
  kind: "language" | "framework" | "tool" | "area";  // area = not code: docs, translation, design, security...
};
```
No other part invents ids: everything refers to this file.

**Only languages and areas get here** (20 today: 8 languages and 12 areas). A project counts **every language with 10% or more of the code**, not only the main one (OBS is C and C++). `pipeline/skills.py` detects 62 fine-grained skills, but each framework or tool has a `parent` and counts as its parent area (React becomes `frontend`, Flask becomes `backend`, PyTorch becomes `ai`). On top of that, `build.py` only publishes a skill that shows up in **5 projects or more**, so no filter returns nothing. That is why C#, Java and Kotlin are left out for now. `Project.skills` uses the same ids.

## `web/public/data/projects.json`: list of `Project`
```ts
type Profile = "guardian" | "open_door" | "needs_hands" | "stable";
type AiPolicy = {
  classification: "accepts" | "accepts_with_disclosure" | "forbids" | "silent" | "unknown";
  evidence: string;      // literal sentence from the file, "" when silent/unknown
  source_file: string;
};
type YearStats = {
  prs_opened: number; prs_merged: number; issues_opened: number; issues_closed: number;
  commits: number;
  direct_commits: number | null;  // null for large repos
  people: number | null;          // distinct people (not bots) in the year; null for large repos
};
// Ways to contribute (docs/vision.md). Same list for the project (what it needs) and the person (what they want to do).
type Way = "code" | "triage" | "review" | "refinement" | "documentation" | "translation" | "security" | "tests";
type Project = {
  repo: string;               // "debug-js/debug" (lowercase)
  needs: Way[];               // ways to help, in the order of opportunities (no repeats)
  opportunities: Opportunity[]; // why it needs each way; see "Opportunities" below
  guide: Guide | null;        // saved "where to start" guide; see "Project guide" below
  url: string;                // "https://github.com/debug-js/debug"
  tags: ("npm-graph" | "pypi-graph" | "go-graph" | "mainstream-app")[];  // which graph it came from, or the hand-made app list
  description: string | null;
  language: string | null;
  license: string | null;
  stars: number;
  dependents: number | null;  // packages that depend on it; null for mainstream apps (they don't come from a graph)
  profile: Profile;
  skills: string[];           // ids from skills.json
  openness: number | null;    // 0..1: of what landed in 12 months (merged PRs + direct commits), the share from outsiders; null = too little data
  maintainers_24m: number;    // people who merged, or made 3+ direct commits, in 24 months (no bots)
  recent: Recent | null;      // issues and PRs of the last 3 closed months
  acceptance: number | null;  // of the PRs outsiders opened in 12 months, the share merged; null = fewer than 5
  debuts_12m: number | null;  // outsiders whose first PR was merged in the last 12 months; null for large repos
  beginner: Beginner;         // ready for beginners, with the evidence
  review: { median_days: number; stale_open: number; prs: number } | null; // first response to outside PRs (12 months)
  newcomer_open: number;      // open issues for newcomers
  scorecard: number | null;   // OpenSSF 0..10
  ai_policy: AiPolicy;
  collection: "full" | "sampled";  // sampled = large repo: complete monthly counts + sample of people (12 months)
  coverage_since: string;     // "2018-01", or the month from which data is complete
  years: Record<string, YearStats>;  // "2018".."2026"
};
```

## `POST /api/explain`
Input (the browser sends **only the repo and the profile**; the server looks the project up in `projects.json` and does not trust project data coming from the client):
```ts
type UserProfile = {
  skills: string[];                                       // ids from skills.json
  level: "beginner" | "intermediate" | "experienced";
  ways: Way[];                                            // how the person wants to help; empty = any way
};
type ExplainRequest = { repo: string; profile: UserProfile };
```
Output:
```ts
type ExplainResponse =
  | { ok: true; why: string; first_steps: string[]; heads_up: string | null; model: string }
  | { ok: false; error: "rate_limited" | "not_found" | "bad_request" | "model_error"; message: string };
```
- `why`: 2–3 sentences, in Portuguese, on why the project fits the profile.
- `first_steps`: 3 to 5 concrete steps, following `docs/vision.md`: they start with watching the project (roadmap, issues, discussions) and talking to the community; for beginners, the first suggested contribution is tests, docs or triage. Never "open a PR" as the first step.
- `heads_up`: a warning, for example the project's AI policy or "maintained by one person, be patient".
- On error, the site shows `message` and keeps working.
- **Implementation** (`lib/gemini.ts`):
  - uses the `@google/genai` SDK and the `GEMINI_MODEL` model (default `gemini-3.5-flash-lite`);
  - **does not use `responseSchema`**, because it hangs with Gemma 4;
  - 60 s timeout;
  - the prompt gets the profile, the project's `opportunities` and its AI policy;
  - an answer in the wrong format becomes `model_error`, never invented text;
  - each answer takes 30 to 45 s, so the site shows a loading state.
  The evaluation of 3 profiles × 3 projects is in `eval/explain.md`.
- The site does not use this route today; its future is discussed in #68.

## Environment variables (`.env.example`)
| Name | Where | What for |
|---|---|---|
| `GEMINI_API_KEY` | Vercel and pipeline | Gemini API |
| `GEMINI_MODEL` | Vercel and pipeline | default `gemini-3.5-flash-lite` |
| `LLM_BACKEND` | pipeline | `gemini` or `ollama` (local) |
| `OLLAMA_MODEL` | pipeline | required with `LLM_BACKEND=ollama` (no default) |
| `OLLAMA_URL` | pipeline | default `http://localhost:11434` |

The pipeline client (`pipeline/llm.py`) reads the root `.env` and runs with `python pipeline/llm.py "your prompt"`. The default backend is `gemini`; for a local model, use `LLM_BACKEND=ollama`.

## How `build.py` computes the profile
In order of priority (`profile_of` in `pipeline/build.py`):
1. **`guardian`:** 100,000 dependents or more, and 1 or 2 people merged or committed directly in 24 months.
2. **`open_door`:** `openness` of 0.25 or more (or 0.1 or more with "good first issue"/"help wanted" issues) **and** an acceptance rate (`acceptance`) of 0.2 or more, when known. Projects **ready for beginners** (see below) also get in, even with low openness caused by many maintainer commits (the postcss case).
3. **`needs_hands`:** 30 open issues or more, 1 to 3 active maintainers, 10% or more of what lands coming from outsiders, an acceptance rate of 0.2 or more (when known) **and at least 1 PR merged in the last 3 months**. The October 31 audit showed that 9 of 19 "needs hands" projects had not merged a PR in 3 months: they were dead ends, not doors.
4. **`stable`:** everything else, including packages with no active maintainer in 24 months.

**Ready for beginners (`beginner`)** is the site's most important promise, so it is the strictest. All 5 checks must pass (`beginner_checks` in `build.py`), and each one goes into the JSON with the text of its evidence:
1. **Debuts (`debuts`):** 2 or more outsiders had their **first** PR merged in the last 12 months (`debuts_12m`).
2. **Acceptance of newcomers, per person (`acceptance`):** of the people who opened a PR in 12 months and had never had one merged before, 25% or more succeeded (needs at least 5 newcomers). Example: redux, 24 of 28. Counting per person, and only newcomers, avoids two mistakes: a long-time contributor without merge rights inflated the rate (in sharp-libvips, kleisauke had 29 of 29), and so did a bot with a human-looking name (`github-actions`).
3. **Active for newcomers (`active`):** 2 or more PRs from **outsiders** merged in the last 3 closed months. Internal merges and bots do not count: nbformat was "active" only because of internal PRs.
4. **Response (`response`):** half of the outside PRs get a first response (review by someone else, merge or close) **within 14 days**, and at most **25%** of them are stale, waiting more than 30 days without review (`review`, computed from the raw cache of the `activity` step). Feedback from a person with a lot of open source experience: a PR waiting a long time without review is not a good door. sqlparse had 13 debuts, but 25 days to the first response and 41 of 107 PRs stale, so it was dropped.
5. **Guide (`guide`):** there is a CONTRIBUTING file.

Large repos do not pass: we only have a recent sample of their PRs, and cannot tell who debuted. Guardians never get the badge (critical, with 1 or 2 people looking after them). On November 2 (data up to October 2026) there were 43 ready projects, and those are exactly what a beginner sees. In the "X of Y newcomers" count, someone who opened a PR before the window and debuted inside it also counts as "tried". A ready project with no opportunity gets the note "N people had their first PR merged here last year". And `open_door` requires at least 1 debut in the year when debuts are known: if nobody new got in for 12 months, the door is not open to newcomers.

**Bots:** besides `is_bot`, logins ending in `bot` and a list of known bots with human-looking names (`github-actions`, `dependabot`, `renovate`, `pre-commit-ci`, `mergify`, `allcontributors`, `copilot`...) are left out.

**Acceptance rate (`acceptance`):** of the PRs outsiders opened in 12 months, the share merged, with a minimum of 5 outside PRs. Openness says where what landed came from; the acceptance rate says the chance that an outside PR gets in. Flask has openness 0.11 and accepts 4%; Express has 0.52 and accepts 8%; Tornado accepts 30%.

**Insiders and outsiders:**
- **Maintainer (insider):** someone who merged a PR in 24 months, or made 3 or more direct commits on the main branch. A single commit does not count, because a third-party commit applied by hand stays under the author's name. Bots are left out, including those with human-looking names such as `antfubot` (filter `login NOT LIKE '%bot'`).
- **`openness`:** of what landed in the project in 12 months (merged PRs + direct commits by maintainers), the share that came from outsiders. Needs 5 changes or more; below that it is `null`. It used to count only PRs, and sharp showed 100% outsiders; counting the maintainer's 177 direct commits, it is 17%.
- **Large repos:** openness counts only PRs (we don't have their direct commits), so it can come out too high for a project whose team makes many commits without PRs (tdesktop: 0.98). They use the same rule on the sample of merged PRs (whoever merged is an insider). GitHub's `authorAssociation` is only used when that participation data is missing, because people who are private members of the organization show up as `CONTRIBUTOR`. For Mastodon, that gave 100% outsiders, while the right value is 25%. If `authorAssociation` gives 95% outsiders or more, the value becomes `null` (that was Tailwind's case).
- **Coverage:** without collected direct commits (`commit_coverage`), the openness of a fully collected repo becomes `null`, because it would come out inflated (csstree showed 100%, and the real value is ~33%). For large repos whose participation covers less than 12 months, openness and maintainers come from the sample (`repo_sample`).
- **Duplicates:** repos that changed owner (`facebook/react` → `react/react`) show up once, with the current name.
- **`recent`:** sum of `repo_monthly` over the last 3 closed months. Example: debug had 18 PRs opened and none merged from July to September.

Distribution on November 2, after the first monthly update: 570 stable, 149 guardians, 233 open doors and 5 that need hands.

## Ways to contribute (`Way`): label on the site and what it covers
| id | Label on the site (pt-BR) | Covers |
|---|---|---|
| `code` | Código | small fixes and features, preferably "good first issue" issues |
| `triage` | Triagem e suporte | reproduce reported bugs, ask for information, find duplicates, answer community questions |
| `review` | Revisão de PRs | run the PR locally, reproduce the bug and check that the fix works |
| `refinement` | Refinamento de issues | turn vague issues into issues with reproduction steps and a definition of done |
| `documentation` | Documentação | docs, examples, tutorials |
| `translation` | Tradução | translation and localization |
| `security` | Segurança | dependencies and advisories, OpenSSF Scorecard practices, auditing |
| `tests` | Testes e observabilidade | regression tests, coverage, logs, metrics, tracing |

The model prompt (`pipeline/opportunities.py`) uses these same descriptions. Accessibility, design/UX, packaging and performance are planned in #66, because they change the contract.

## Project guide: `guide`
```ts
type Guide = {
  summary: string;                               // what the project is and where it needs help, in Portuguese
  common_steps: string[];                        // watch and talk
  steps_by_way: Partial<Record<Way, string[]>>;  // 2 or 3 steps per way to help (only those in needs)
  heads_up: string | null;
};
```
- **Generated once per project:** `pipeline/guides.py` has the model read the contribution guide or the README, the opportunities, the numbers and the AI policy. The answer is stored in `project_guides`. Run the script **after** `classify_ai_policy.py`, so the warning can cite the policy. The published guides were generated with Gemma 4.
- **On the site, without a model:** `web/lib/guide.ts` (`composeGuide`) joins the common steps with the steps of up to 2 ways to help:
  - the ones the person picked;
  - if they picked none and are a beginner, tests, docs and triage first;
  - otherwise, the project's own.
  It is deterministic: same input, same output, and it answers instantly.
- **Nothing is generated live.** The site does not call the model. A project with no saved guide gets steps built from its `opportunities` (`guideFor`). The AI policy warning comes from the classified data, with the quote (`aiPolicyNote`).
- **On the site, AI content is labeled** ("gerado com IA", "sugestão da IA"), without advertising the model. OpenDoor is for the community, and the model is a means.

## Opportunities: `needs` and `opportunities`
```ts
type Opportunity = { way: Way; source: "project" | "data" | "gemini"; note: string };
```
Each project lists the ways to help and the reason (`note`, in Portuguese), in this order:
1. **`project`:** the contribution guide **mentions** documentation, translation, tests or review (it is a regex; the UI says "the guide mentions", not "the project asks"), or there are "good first issue"/"help wanted" issues. Translation is dropped when the guide says it does not accept it ("we do not merge … translations", the tdesktop case). We only look for words in the text, never follow its instructions.
2. **`data`:** the numbers show it:
   - `code`: 10% or more of merged PRs come from outsiders;
   - `triage`: 100 open issues or more, or 30 or more with up to 3 maintainers;
   - `review`: 20 open PRs or more (note: run it, reproduce the bug and check the fix);
   - `security`: guardian, or Scorecard below 5.
3. **`gemini`:** an LLM suggestion (the current data came from Gemma 4), generated **offline** by `pipeline/opportunities.py`. It reads the contribution guide or the README and the numbers, and only suggests ways not already on the list. The result is cached in `repo_opportunities`. **On the site, show it as an "AI suggestion", not as a fact.**

Every project that shows up in the match (profile other than `stable`) has at least one opportunity.

## Ranking rules (`web/lib/match.ts`)
`rankProjects(projects, profile, languageIds)` returns **every project that qualifies**, from best to worst match. On the home page, a search (name, owner, description and summary, ignoring accents) and a bar filter the list by profile, AI policy and "good first issue / help wanted"; it can be sorted by match, openness, newcomer issues or stars (`components/ResultsBar.tsx`). The list shows 20 projects at a time. `languageIds` are the ids from `skills.json` with `kind: "language"`; the home page already loads that file and passes the set.
- **Exclusions:**
  - `stable` never shows up;
  - `guardian` does not show up for beginners;
  - for beginners, only projects **ready for beginners** (`beginner.ready`; see above);
  - `needs` only holds what the guide mentions or the numbers show; model suggestions appear on the project page, but do not put the project in the ways-to-help filter;
  - if the person picked ways (`ways`), the project must have at least one of them in `needs`;
  - if the person picked skills, the project must have at least one in common;
  - if they picked languages, the project must use one of them.
- **Exception:** someone who picked only non-code ways (triage, refinement, documentation, translation) **does not need** a skill or language in common.
- **Score:**
  - 5 per skill in common;
  - level bonus: beginner favors `open_door`, plus 2 if `newcomer_open > 0`; intermediate favors `needs_hands`; experienced favors `guardian`;
  - plus 1 per way to contribute in common.
- **Ties:** broken by debuts in the last year, then by acceptance rate, then by stars. Openness alone is misleading for a one-person project.
