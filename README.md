<img src="web/public/logo.svg" alt="OpenDoor logo: Tux walking out through a door" width="160">

# OpenDoor

*[Português](README.pt-BR.md)*

**Entry points for contributing to open source.** Tell OpenDoor what you know and it shows where and how you can help: which project, what kind of help it needs and where to start.

**Live:** https://opendoor-fawn.vercel.app (the site is in Portuguese for now; an English version is planned in #50)

OpenDoor was born at [Hacktoberfest Hack Day São José dos Campos](https://www.mlh.com/events/hacktoberfest-hack-day-sao-jose-dos-campos-x-github-community-sjc) (October 31, 2026), where it won the local round. It is now a community project, and contributions are welcome.

## Why
"Open a project you use and see how you can contribute" is too generic, and the barrier to getting started is high. Meanwhile, small packages that half the internet depends on are maintained by one or two people (event-stream, xz-utils, chalk/debug...).

But getting in is not about opening PRs without understanding the project: many projects receive PRs that fix one problem and create others. OpenDoor guides people along a responsible path: pick **one** project, watch, talk to the community, understand the code and start with tests or docs (see the [product vision](docs/vision.md#philosophy-contribute-responsibly)).

OpenDoor maps the ecosystem, measures the health and openness of each project and matches that with the profile of the person who wants to contribute.

## How it works
1. **Map:** dependency graph of npm, PyPI and Go (deps.dev), plus a list of mainstream and AI apps that live on GitHub.
2. **Health, from 2018 to today:** issues, PRs, reviews, merges and commits per month, with who played each role; OpenSSF Scorecard; beginner issues.
3. **Project profile:** *Guardian*, *Open door*, *Needs hands* or *Stable* (see the [product vision](docs/vision.md)).
4. **Ready for beginners:** only projects where the data shows newcomers actually getting in earn the badge (first-time contributors, acceptance of newcomers' PRs, recent outside PRs merged, response time and a contribution guide). See [docs/architecture.md](docs/architecture.md).
5. **AI, offline:** a language model reads each project's contribution policy (does it accept AI? with disclosure? does it forbid it?), suggests where to help and writes the "where to start" guide. Everything is generated ahead of time and stored; the site never calls the model live.

## Data and AI

On October 31, 2026, the database had:
- **973 repositories**: those of 1,351 critical npm (950), PyPI (225) and Go (176) packages, plus mainstream and AI apps;
- **958 projects on the site**, of which 346 accept contributions and **30 are ready for beginners**;
- **39,100 monthly rows** and **523,716 participation records**;
- **1,190 files** of contribution guides and AI policies.

The 104 large repos have complete monthly counts plus a sample of PRs. Every number can be recomputed from the raw cache.

The central finding is that activity is not openness: a project can receive many PRs and still keep few outside contributors. That is why OpenDoor measures PRs merged from non-maintainers, active maintainers, beginner issues, commits, reviews and the security Scorecard.

**The language model works in three places, always offline and cached in the database:**
1. **Opportunities:** `pipeline/opportunities.py` reads each project's contribution guide and suggests where to help when the project does not say. Example for React: "translate the official documentation into Brazilian Portuguese".
2. **AI policy:** `pipeline/classify_ai_policy.py` classifies whether the project accepts AI, asks for disclosure or forbids it, always with a literal quote from the file.
3. **"Where to start" guide:** `pipeline/guides.py` writes, once per project, a summary and steps for each way to help. The site combines the guide with the person's profile without calling the model. Steps start with watching and talking, never with "open a PR".

`pipeline/llm.py` talks to the model through the Gemini API (`GEMINI_MODEL`, default `gemini-3.5-flash-lite`) or a local Ollama. The data published today was generated with Gemma 4. The `/api/explain` route (live model) is still in the code, but the site does not use it; its future is discussed in #68.

## Getting started
Requirements: Python 3.11+ (standard library only). To collect data you also need the [GitHub CLI](https://cli.github.com/) logged in (`gh auth login`), which provides the API token.

The database (SQLite) is not in git: each collection is published as a [GitHub Release](https://github.com/jose-victor/opendoor/releases) tagged `data-YYYY-MM-DD`. To download and explore it:

```bash
python pipeline/collect.py fetch-db          # -> data/ecosystem.db (add --raw for the raw API cache, needed by build.py's review times)
sqlite3 data/ecosystem.db ".tables"
python pipeline/collect.py stats
```

To collect again or update (each step resumes where it stopped):

```bash
python pipeline/collect.py graph --system npm   # dependency graph (npm, pypi or go)
python pipeline/collect.py apps        # mainstream apps (APPS list in collect.py)
python pipeline/collect.py repos       # current snapshot + policy files
python pipeline/collect.py activity    # PRs/issues per month since 2018
python pipeline/collect.py commits     # commits per month, how many landed directly without a PR
python pipeline/collect.py labels      # beginner issues
python pipeline/collect.py topics      # GitHub topics (skills)
python pipeline/collect.py security    # OpenSSF Scorecard + advisories
python pipeline/collect.py large       # large repos: monthly counts + sample of people
python pipeline/collect.py reaggregate # recompute aggregations from the raw cache, no API
python pipeline/build.py               # generate web/public/data/*.json for the site
python pipeline/opportunities.py       # opportunities suggested by the model (cached); run build.py again afterwards
python pipeline/classify_ai_policy.py  # AI policy (cached); run build.py again afterwards
python pipeline/guides.py              # "where to start" guide (cached); run build.py again afterwards
python pipeline/collect.py selftest    # aggregation tests
```

## Website (`web/`)
Next.js 16 (App Router) on Vercel. Data comes from `web/public/data/`, generated by `python pipeline/build.py`.

```bash
cd web
cp ../.env.example .env.local   # GEMINI_API_KEY is only needed for /api/explain
npm install
npm run dev                     # http://localhost:3000
```

## Layout
| Path | What |
|---|---|
| `pipeline/collect.py` | collector (one file, no dependencies) |
| `pipeline/build.py` | generates `web/public/data/*.json` from the database: skills, profile, opportunities |
| `pipeline/skills.py` | skill vocabulary and detection rules |
| `pipeline/opportunities.py` | contribution opportunities suggested by the model (cached in the database) |
| `pipeline/classify_ai_policy.py` | each repo's AI policy, with literal evidence (cached in `ai_policy`) |
| `pipeline/guides.py` | "where to start" guide for each project, combined with the profile on the site (`web/lib/guide.ts`) |
| `pipeline/llm.py` | minimal model client (Gemini API or Ollama) |
| `web/` | Next.js site: pages, `/api/explain`, `lib/types.ts` (contract types) |
| `data/ecosystem.db` | SQLite database with everything collected (not in git; `collect.py fetch-db`) |
| `eval/` | `gabarito.csv` (hand-labeled AI policies) and `explain.md` (evaluation of model answers) |
| `docs/vision.md` | product vision and the 4 project profiles |
| `docs/architecture.md` | contracts: JSON format, types, API |
| `docs/data.md` | data dictionary and example queries |
| `AGENTS.md` / `CLAUDE.md` | instructions for coding agents |

## Contributing
Read [CONTRIBUTING.md](CONTRIBUTING.md). Planned work lives in the [issues labeled `roadmap`](https://github.com/jose-victor/opendoor/issues?q=is%3Aopen+label%3Aroadmap), and questions and ideas go to [Discussions](https://github.com/jose-victor/opendoor/discussions). This project follows a [Code of Conduct](CODE_OF_CONDUCT.md). Found a vulnerability? See [SECURITY.md](SECURITY.md).

## License
GPL-3.0, see [LICENSE](LICENSE).
