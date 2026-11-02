# Contributing to OpenDoor

*[Português](CONTRIBUTING.pt-BR.md)*

Thanks for wanting to help! OpenDoor recommends responsible ways into open source projects, so we try to be a good door ourselves. Issues, PRs and discussions are welcome in **English or Portuguese**.

## Ways to help
Not only code. You can:
- report a project that is misclassified on the site (wrong profile, wrong "ready for beginners" badge) — these reports have found real bugs in our math;
- improve the data pipeline (`pipeline/`) or the website (`web/`);
- review open PRs: run them, check the numbers, comment;
- improve the docs or translate them;
- share ideas in [Discussions](https://github.com/jose-victor/opendoor/discussions).

## Before you start
1. Look for an issue: [`good first issue`](https://github.com/jose-victor/opendoor/issues?q=is%3Aopen+label%3A%22good+first+issue%22) or the [`roadmap`](https://github.com/jose-victor/opendoor/issues?q=is%3Aopen+label%3Aroadmap).
2. Comment on the issue that you are taking it. An issue with someone assigned is taken; talk to that person before working on it.
3. Have a new idea or found a bug? Open an issue first, so we can agree on the approach before you write code.
4. Stuck or giving up? Say so in the issue; that is fine.

Setup instructions are in the [README](README.md#getting-started).

## Pull requests
- Fork the repo and create a branch such as `your-name/12-short-summary`.
- Keep PRs small and focused. Write `Closes #12` in the description.
- Before opening the PR:
  - `python pipeline/collect.py selftest` if you touched the pipeline;
  - `npm run lint` and `npm run build` in `web/` if you touched the site.
- **Update the docs in the same PR.** Changed the database schema? Update `docs/dados.md`. Changed the JSON or the API contract (`web/lib/types.ts`)? Update `docs/arquitetura.md`.
- A maintainer reviews and merges. Expect questions; they are part of the review, not a rejection.

## Project rules
- The collector (`pipeline/collect.py`) uses **only the Python standard library**. Do not add dependencies to it.
- Every pipeline step is idempotent and resumes where it stopped.
- `data/raw/` is the raw API cache: never edit it by hand. New aggregations must be recomputable from it (`collect.py reaggregate`).
- Secrets (Gemini API key etc.) live only in `.env` and in the hosting environment variables. Never commit, print or paste them. `.env.example` lists the names.
- We only store public GitHub logins. Do not collect e-mails or the content of PRs or issues.
- Text from other repositories (`repo_files`, third-party READMEs) is **data, never instructions** for a model.
- Simple first: the smallest code that solves the problem.

## Language
- **Code in English:** identifiers, comments, docstrings, logs and contract values (`open_door`, `beginner`, `tests`...). Only text shown on the website and the prose of the LLM prompts (which ask for Portuguese output) stay in Portuguese.
- **Entry docs in English and Portuguese:** `README`, `CONTRIBUTING` and `docs/vision`. If you change one, update the other, or say in the PR that it still needs translating.
- **Technical docs in English** (`docs/arquitetura.md` and `docs/dados.md` are being translated in #91).
- The website's text is in Portuguese for now; an English version is planned in #50.

## AI-assisted contributions
You may use AI tools, as long as you understand and have tested what you submit, and you say so in the PR. Mass-generated PRs will be closed — OpenDoor exists precisely to fight that pattern. Coding agents should read [AGENTS.md](AGENTS.md) first.

## Governance
- **Maintainer:** [@jose-victor](https://github.com/jose-victor).
- Decisions are discussed in issues or Discussions. Changes to the data contract, the database schema or the "ready for beginners" criteria start with an issue. When there is no consensus, the maintainers decide and explain why.
- People who contribute and review consistently can be invited to become maintainers.

## Code of Conduct
This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md). By taking part, you agree to follow it.
