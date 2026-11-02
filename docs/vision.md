# Product vision

*[Português](vision.pt-BR.md)*

## The problem
The usual advice, "open a project you use and see how you can contribute" (heard at a talk during Hacktoberfest Hack Day SJC 2026, where OpenDoor was born), is too generic. The barrier to getting started is high.

## The idea
A platform where people say what they know and what they have done, and get **entry points** into open source projects: which project, what kind of help it needs and where to start.

In the long run it becomes a marketplace or social network that helps open source projects: maintainers also **register their own projects** to ask for help.

## Philosophy: contribute responsibly
Contributing is not opening PRs on someone else's project without understanding what is going on. At a GDG talk during the same event, the speaker told how projects like Node.js and Meteor received many PRs that fixed one problem and created several others. Our data shows the same trend: **opened** PRs exploded (in VS Code, from 117 a month in 2018 to 2,695 in 2026), far more than **merged** ones.

OpenDoor walks people through the path the talk recommends:
1. Pick **one** project you like.
2. Watch the roadmap and the priorities.
3. Join the discussions and the community.
4. Talk to a maintainer, when possible.
5. Understand the code before changing it.
6. Start with tests or documentation.

What this changes in the product:
- **Doors (AI-written guide):** the first steps start with watching and talking. "Open a PR" is never the first step.
- **Match:** shows every project that fits, from best to worst match, with filters (profile, AI policy, beginner issues). For beginners, only welcoming projects are shown, and low-risk entries (tests, docs, triage) come first.
- **AI policy up front:** using AI on a project that asks for disclosure, or forbids it, is the kind of contribution that causes trouble.
- **Never** encourage mass-generated PRs.

## Two kinds of projects
1. **Critical and "underground":** small packages with many dependents (huge blast radius, as in event-stream, xz-utils and chalk/debug).
2. **Mainstream:** end-user apps that live on GitHub (OBS, Godot, Audacity, Jellyfin...).

## Four project profiles (the kind of help each one needs)
| Profile | Signal in the data | Contribution | For whom |
|---|---|---|---|
| Guardian | many dependents, one person does everything, direct commits, low Scorecard | security review, co-maintenance, funding | experienced and trusted people |
| Open door | outside PRs merged in the last 12 months, beginner issues, someone reviewing | code, docs, tests, first contribution | anyone |
| Needs hands | many open issues, few active maintainers, accepts outside PRs | triage, fixes, review | intermediate |
| Stable/closed | no outside PRs and no call for help | little to do | not a target |

**Key openness indicator:** the share of merged PRs from people who are not maintainers.

## Ways to contribute (not only code)
Each project needs different kinds of help, and each person can offer different kinds. The match crosses both.

| Way | Signal that the project needs it |
|---|---|
| Code | "good first issue" and similar issues, outside PRs being accepted |
| Triage and support (reproduce reported bugs, answer questions) | many open issues for few maintainers |
| PR review (run it, reproduce the bug and validate the fix) | open PRs waiting, few active reviewers |
| Issue refinement | vague issues: no reproduction steps, no label, no definition of done |
| Documentation | docs label, weak or missing README/CONTRIBUTING |
| Translation / localization | i18n files, translation label |
| Security | low Scorecard, guardian profile, direct commits without review |
| Tests and observability (regression, coverage, logs, metrics) | the guide asks for tests or observability, low coverage |

When a project does not list what it needs, a language model suggests opportunities (labeled as AI suggestions). Details in `docs/architecture.md`.

## Not yet (on the roadmap)
Future work lives in the [issues labeled `roadmap`](https://github.com/jose-victor/opendoor/issues?q=is%3Aopen+label%3Aroadmap). Some examples:
- Maintainers registering their projects (marketplace/social network): #69.
- Malicious-insertion monitor: #70.
- More ways to contribute (accessibility, design/UX, packaging and performance): #66.
- Collectors for GitLab, Gerrit and Gitea (GIMP, LibreOffice, Blender, Firefox): #71.
