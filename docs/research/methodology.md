# Evidence base for OpenDoor's project scoring methodology

Research date: 2026-11-02. Scope: academic and community work on onboarding newcomers to OSS, how contributor roles are detected, how governance is inferred, sustainability, and CHAOSS metrics. The aim is to back the future "agent gathers evidence, rules decide the score" system.

**How to read this.** Each finding gives the **claim**, the **signal for OpenDoor**, the **computation** (with a flag for whether it needs **TEXT**, meaning issue, PR or comment bodies, which OpenDoor avoids storing today; **META** means metadata only: logins, timestamps, states, labels, review events), and the **source**.

**Confidence** shows how closely I read each source:
- **[read]**: I read the abstract or page directly.
- **[secondary]**: I saw only search snippets or summaries.

Do not quote numbers marked [secondary] without opening the PDF.

**What OpenDoor already does** (from `docs/architecture.md`):
- It classifies insiders and outsiders by merges and direct commits.
- It measures openness and per-person newcomer acceptance.
- It computes debuts in 12 months, outside PRs merged in the last 3 months, a 14-day first-response median, a stale share above 30 days, and whether a CONTRIBUTING file exists.

Most of these line up well with the literature. The gaps are mostly about **retention after the first PR**, **who** responds, **concentration and bus factor**, **maintainer load**, and the **quality of the interaction**.

---

## 1. Barriers to newcomers (why projects lose them)

### 1.1 Five barrier categories (Steinmacher et al.)
- **Claim.** A systematic review groups newcomer barriers into five categories:
  - finding a way to start;
  - social interaction (no response, delayed or impolite answers);
  - newcomers' own knowledge;
  - documentation problems;
  - technical hurdles in the code and setup.

  The journal version screened 291 studies and coded the barriers with grounded theory.
- **Signal.** Use the categories as a **checklist of evidence the agent must look for**:
  - **Finding a way to start:** GFI or help-wanted labels; issues that point to files.
  - **Social:** first-response latency and tone.
  - **Docs:** CONTRIBUTING, a dev-setup section, an architecture doc.
  - **Technical setup:** a devcontainer or Docker setup, a Makefile, the test command, CI that runs on forks.
- **Computation.** Mostly META plus repo files. Tone of answers needs TEXT.
- **Source.**
  - Steinmacher, Silva, Gerosa, Redmiles, "A systematic literature review on the barriers faced by newcomers to open source software projects", IST 59 (2015) 67–85. https://experts.nau.edu/en/publications/a-systematic-literature-review-on-the-barriers-faced-by-newcomers/
  - IFIP 2014 version: https://link.springer.com/content/pdf/10.1007/978-3-642-55128-4_21.pdf
- **Confidence.** [secondary] for the counts. The five categories match two sources.

### 1.2 Who answers, and how, matters more than whether someone answers
- **Claim.** In the CHASE 2013 study, whether a newcomer left depended on **who** answered the first message and **what kind** of answer it was. Simply getting an answer did not emerge as a factor.
- **Signal.** Count a first response only if it comes from an **insider** (maintainer or reviewer), not a bot or another outsider. OpenDoor already counts review by "someone else", so tighten that to **someone else who is an insider**.
- **Computation.** META, by joining the responder login to the maintainer set.
- **Source.** Steinmacher, Wiese, Chaves, Gerosa, "Why do newcomers abandon open source software projects?", CHASE 2013. https://www.ime.usp.br/~gerosa/papers/CHASE2013.pdf
- **Confidence.** [secondary]

### 1.3 Most barriers are social; mentors face barriers too
- **Claim.** Interviews with mentors found 44 barriers: 19 that affect mentors, 34 that affect newcomers, and 9 that affect both. 66% of them are social.
- **Signal.** "Is there capacity to mentor?" is a property of the project. A project with one overloaded maintainer cannot mentor, even if it is welcoming.
- **Computation.** Infer it from maintainer load (see §5).
- **Source.** Balali, Steinmacher, Annamalai, Sarma, Gerosa, "Newcomers' Barriers… Is That All? An Analysis of Mentors' and Newcomers' Barriers in OSS Projects", CSCW Journal 27 (2018). https://web.engr.oregonstate.edu/~sarmaa/wp-content/uploads/2020/08/Balali2018_Article_NewcomersBarriersIsThatAllAnAn.pdf
- **Confidence.** [secondary]

### 1.4 Onboarding guidelines
- **Claim.** The barrier research, an onboarding portal (FLOSScoach) and interviews were turned into practical onboarding guidelines for communities and for newcomers.
- **Signal.** This is a **source for the agent's checklist** of project-side onboarding practices.
- **Source.** Steinmacher, Treude, Gerosa, "Let Me In: Guidelines for the Successful Onboarding of Newcomers to Open Source Projects", IEEE Software 36(4), 2019. https://www.ime.usp.br/~gerosa/papers/08254320.pdf
- **Confidence.** [secondary]. I did not extract the guideline list, so read the PDF before encoding it.

### 1.5 What potential contributors look at
- **Claim.** Interviews plus a regression on about 10,000 npm packages found that people look at:
  - how the README is structured;
  - recent activity;
  - the number of contributors;
  - how recent the commits are;
  - maintainer friendliness in discussions;
  - popularity.

  Many important attributes have **no easily observable signal**, and some signals are both attractive and unattractive. Politeness mattered for new contributors in general, but **not for first-time GitHub contributors**.
- **Signal.** This backs OpenDoor's purpose: it makes visible the signals that are not observable today, such as debuts, acceptance of newcomers and latency. It also warns that a busy project can be both attractive and hard to enter.
- **Source.** Qiu, Li, Padala, Sarma, Vasilescu, "The Signals that Potential Contributors Look for When Choosing Open-source Projects", PACM HCI (CSCW) 2019. https://cmustrudel.github.io/papers/cscw19signals.pdf
- **Confidence.** [secondary]

---

## 2. Good first issues (GFI) and mentoring

### 2.1 Many GFIs are never solved by newcomers
- **Claim.** Of 9,368 GFIs in 816 projects, almost half were never solved by newcomers.
- **Signal.** A GFI label is **not** evidence of an open door on its own. Measure **GFI effectiveness**: the share of closed GFIs whose linked or closing PR came from a newcomer, meaning a person whose first merged PR in this repo it was.
- **Computation.** META:
  - issue labels;
  - the `closedByPullRequestsReferences` or timeline events;
  - the PR author;
  - whether this was the author's first merged PR here.
- **Source.** Tan, Zhou, Sun, "A First Look at Good First Issues on GitHub", ESEC/FSE 2020. https://bohrium.dp.tech/paper/arxiv/63b3f1f790e50fcafde9ee63
- **Confidence.** [secondary]. Many search results agree on the numbers.

### 2.2 Mentoring on GFIs
- **Claim.** Across 48,402 GFIs in 964 repositories:
  - about 70% had an expert involved, usually one expert with two comments;
  - the median time to the first expert comment was 8.5 hours after the newcomer's comment;
  - expert involvement was **positively** associated with the newcomer succeeding, but **negatively** with retention.

  The paper describes four mentoring structures: centralized, decentralized, collaborative and distributed.
- **Signal.**
  - **Mentoring presence:** the share of GFI or newcomer threads where an insider commented.
  - **Expert latency:** the median time from a newcomer's comment or PR to the first insider comment.
- **Computation.** META: comment author and timestamp only, no body needed. The negative retention result is a caution: do not reward heavy hand-holding as if it meant "sticky".
- **Source.** Tan, Chen, Wu, Zhou, Zhang, "Is It Enough to Recommend Tasks to Newcomers? Understanding Mentoring on Good First Issues", ICSE 2023. https://arxiv.org/abs/2302.05058
- **Confidence.** [read] (abstract)

### 2.3 GFI labeling is declining and newcomer merge rates are falling (2021–2025)
- **Claim.** Across 37 popular repositories (406,826 issues), the share of GFI-labeled issues fell significantly starting in January 2024. Newcomer engagement with GFIs stayed at about 27%. The merge rate of newcomer GFI PRs fell from **61.9% to 42.2%**. PR description length and code size did not predict the merge.
- **Signal.**
  - Use **time-windowed** newcomer acceptance. OpenDoor's 12-month window is good. Also show the trend, because rates from 2023 are stale.
  - Do not penalize a project for having no GFI label if newcomers still debut there.
- **Source.** Hoshikawa, Tanaka, Shimari, Kula, Matsumoto, "A Longitudinal Analysis of Good First Issue Practices and Newcomer Pull Requests in Popular OSS Projects", arXiv 2604.27532 (2026). https://arxiv.org/abs/2604.27532
- **Confidence.** [read] (abstract). This is a preprint, and the paper itself says causality is not established.

### 2.4 Characteristics of the first issue and long-term retention
- **Claim.** Interaction traits are more strongly associated with newcomer retention than the issue's own attributes. Higher retention potential came with:
  - a reporter of moderate experience;
  - **moderate** discussion intensity;
  - participation by project members;
  - neutral or slightly negative sentiment.
- **Signal.** Insider participation in newcomers' threads and the comment count per thread, both META. Sentiment needs TEXT, which can be computed on the fly and thrown away.
- **Source.** Hao, Xu, Gao, Zhang, "The First Issue Matters: Linking Task-Level Characteristics to Long-Term Newcomer Retention in OSS", arXiv 2603.27136 (2026). https://arxiv.org/abs/2603.27136
- **Confidence.** [read] (abstract). This is a preprint, and the retention definition was not visible.

### 2.5 Early experience predicts long-term contributors
- **Claim.** A newcomer's willingness and the project's macro-climate and micro-climate are associated with the odds of becoming a long-term contributor (Mozilla and Gnome issue trackers).
- **Signal.** This supports measuring **conversion**: of the people who debuted in year Y, how many contributed again within the next 6 to 12 months.
- **Source.** Zhou & Mockus, "What make long term contributors: Willingness and opportunity in OSS community", ICSE 2012. https://researchr.org/publication/ZhouM12-1
- **Confidence.** [secondary]

---

## 3. PR acceptance for outsiders

### 3.1 Integrators judge quality first
- **Claim.** A survey of 749 integrators found that technical quality, tests and following project conventions dominate acceptance. Common reasons for rejection were technical quality (85%), test failures (55%) and not following conventions (48%).
- **Signal.** The guide should tell newcomers which conventions and tests apply. The agent can extract these from CONTRIBUTING and CI config. This is a source for "entry paths", not for the score.
- **Source.** Gousios, Zaidman, Storey, van Deursen, "Work Practices and Challenges in Pull-Based Development: The Integrator's Perspective", ICSE 2015. https://repository.tudelft.nl/record/uuid:09847ac7-e5e8-4c09-b8b1-291f82c2f34c
- **Confidence.** [secondary]. The percentages come from summaries.

### 3.2 Few factors explain PR decisions, and the top one is insider versus outsider
- **Claim.** 3.35 million PRs, 95 features and 11,230 projects, with mixed-effects models. **Whether the integrator is the same person as the submitter** is the most important factor. Factor effects depend on context: CI failures matter only when CI is used, and how "hot" the touched area is matters early in a project's life.
- **Signal.** The raw acceptance rate mixes in insiders' self-merges. OpenDoor is right to compute **outsider-only** acceptance. Keep self-merges out of every "acceptance" signal.
- **Source.** Zhang, Yu, Gousios, Rastogi, "Pull Request Decisions Explained: An Empirical Overview", IEEE TSE 49(2), 2023. https://arxiv.org/abs/2105.13970
- **Confidence.** [secondary]

### 3.3 Social and technical signals both matter, and long discussions predict rejection for non-members
- **Claim.** Social signals (for example, an earlier connection to the project) and technical ones are both strongly associated with acceptance. The FSE companion paper found that non-member PRs were more likely to be rejected after a long discussion.
- **Signal.** **Prior interaction before the PR** helps acceptance. The entry path "comment on an issue first, then open a PR" has evidence behind it, and this matches OpenDoor's "watch and talk first" philosophy.
- **Computation.** META: did the PR author comment or open an issue in the repo before their first PR?
- **Source.**
  - Tsay, Dabbish, Herbsleb, "Influence of social and technical factors for evaluating contribution in GitHub", ICSE 2014. https://par.nsf.gov/servlets/purl/10038370
  - "Let's talk about it", FSE 2014: https://bibtex.github.io/FSE-2014-TsayDH.html
- **Confidence.** [secondary]

### 3.4 Volunteers versus employees in company-owned OSS
- **Claim.** In company-owned projects, volunteers had **26x more rejections** than employees and waited about 11 days on average for a patch to be processed, against about 2 days for employees.
- **Signal.** For corporate-backed repos, measure the **outsider/insider gap**: the difference in acceptance and latency between outsiders and insiders. A big gap means a door that is "open on paper".
- **Computation.** META. OpenDoor already has both groups.
- **Source.** Pinto, Dias, Steinmacher, "Who Gets a Patch Accepted First? Comparing the Contributions of Employees and Volunteers", CHASE 2018. https://researchr.org/publication/0001DS18
- **Confidence.** [secondary] (abstract figures)

### 3.5 Gender and identifiability
- **Claim.** Overall, women's PRs were accepted more often. But among **outsiders whose gender is identifiable** from the profile, men's acceptance was higher. The study and its charts were criticized.
- **Signal.** OpenDoor should **not** infer gender. Treat this as evidence that outsiders face bias, and that a project's measured acceptance can hide differences between subgroups. Low priority for the score.
- **Source.** Terrell et al., "Gender differences and bias in open source: pull request acceptance of women versus men", PeerJ CS 3:e111 (2017). https://peerj.com/articles/cs-111.html
- **Confidence.** [secondary]

### 3.6 Abandoned PRs
- **Claim.** A manual study of 321 abandoned PRs plus a survey of 710 developers found 12 reasons. Key ones were **integrators not responding** and **the contributor running out of time**. Most contributors abandon without explanation.
- **Signal.** Measure the **abandonment rate of outside PRs**: PRs closed unmerged, or left open, where the last event was a request or comment from the reviewer and there was no reply. This splits "the project is slow" from "contributors give up".
- **Computation.** META: the order of review events and authors.
- **Source.**
  - Li, Yu et al., "Are You Still Working on This? An Empirical Study on Pull Request Abandonment", TSE / ICSE 2022 journal-first. https://yuyue.github.io/res/paper/abPR-icse2022-jf.pdf
  - Khatoonabadi et al., "On Wasted Contributions", arXiv 2110.15447. https://arxiv.org/abs/2110.15447
- **Confidence.** [secondary]

---

## 4. Responsiveness, bots and AI

### 4.1 Bots skew time to first response
- **Claim.** 111,094 closed PRs in 10 projects. Bots often give the first response, and their timing is significantly different from humans'. Longer waits for the first **human** response go with:
  - a low PR success rate;
  - heavy team workload;
  - a newly created project.
- **Signal.** Measure the first response as the **first human insider response**. Workload predicts latency, so use both together in maintainer-load rules.
- **Source.** Hasan, Macedo, Tian, Adams, Ding, "Understanding the Time to First Response in GitHub Pull Requests", MSR 2023. https://conf.researchr.org/details/msr-2023/msr-2023-technical-papers/18/Understanding-the-Time-to-First-Response-In-GitHub-Pull-Requests
- **Confidence.** [read] (abstract)

### 4.2 First response and coming back
- **Claim.** 2.77 million first-contribution PRs. Most first responses were positive but slow. Negative responses were mostly constructive (50.7%) or critical (37.7%). Having interaction at all correlates with future contributions. Predicting future contributions was only modest (F1 0.62).
- **Signal.** Evidence that **any human interaction on the first PR** goes with return. The evidence on **latency** in particular is weaker than folklore suggests.
- **Source.** Assavakamhaenghan et al., "Does the First Response Matter for Future Contributions? A Study of First Contributions", arXiv 2104.02933. https://arxiv.org/abs/2104.02933
- **Confidence.** [read] (abstract)
- **Honest note.** I did **not** find a strong peer-reviewed causal result that "faster first response leads to higher newcomer retention". A non-peer-reviewed practitioner analysis (Multitudes) found similar first-PR wait times for newcomers who stayed and those who left. OpenDoor's 14-day threshold is defensible as a usability floor for newcomers, not as a calibrated predictor.

### 4.3 Bots: maintainers gain, newcomers pay
- **Claim.**
  - Code-review bots go with more merged PRs, fewer unmerged ones and **less communication**.
  - Maintainers report newcomer dropout, and bots that "impersonate" maintainers frustrate contributors.
  - Interviews show that bot noise and long feedback lists can push newcomers to abandon their PR.
- **Signal.** Measure **bot density on newcomer PRs**: the number of bot comments before the first human comment. Treat high bot density with no human response as a negative.
- **Computation.** META (`is_bot`, comment author).
- **Source.**
  - Wessel et al., "Quality Gatekeepers: Investigating the Effects of Code Review Bots on Pull Request Activities", EMSE 2022. https://research.tudelft.nl/en/publications/quality-gatekeepers-investigating-the-effects-of-code-review-bots
  - Wessel et al., "Don't Disturb Me: Challenges of Interacting with Software Bots on OSS", CSCW 2021. https://arxiv.org/pdf/2103.13950
  - Wessel et al., "What to Expect from Code Review Bots on GitHub?", SBES 2020. https://sol.sbc.org.br/index.php/sbes/article/view/17041
- **Confidence.** [secondary]

### 4.4 AI-generated contributions
- **Claim.**
  - The Linux Foundation Research survey (234 respondents, sponsored by Red Hat) estimates that about 25% of incoming PRs are low-quality AI-assisted ones (31% in large projects).
  - 64% of maintainers of large projects say review cycles got longer.
  - Only 35% of projects have a formal policy on generative AI.

  Empirical papers on agent PRs: Claude Code PRs were accepted 83.8% of the time against 91.0% for human PRs, in 157 projects (arXiv 2509.14745). Acceptance varies widely by agent, from 0.45 for Copilot to 0.83 for Codex (AIDev dataset, arXiv 2602.02345).
- **Signal.**
  - The AI policy (OpenDoor already classifies it) is a first-class gate.
  - In 2024–2026, a falling acceptance ratio may mean the project is **defending itself against spam**, not that it is unwelcoming (see §8).
- **Sources.**
  - https://www.linuxfoundation.org/blog/navigating-open-source-software-development-in-the-generative-ai-era-balancing-velocity-and-community-health
  - https://arxiv.org/abs/2509.14745
  - https://arxiv.org/pdf/2602.02345
- **Confidence.** [secondary]. The LF figures are estimates from respondents, not measured counts.

---

## 5. Who is an insider, a newcomer, casual or core

### 5.1 Onion model, core and periphery, and the 80% heuristic
- **Claim.**
  - The onion model has a small core surrounded by layers of peripheral contributors (Crowston & Howison).
  - The common count-based operational rule: the core is the smallest set of developers who make **80%** of commits (after Mockus et al. 2002 on Apache).
  - Joblin et al. (ICSE 2017) compared count-based and network-based classifications against a survey of 166 developers. **Network metrics** (high degree, low clustering in the communication network) agreed better with how developers see themselves. Count metrics such as commit counts were less consistent.
- **Signal.** Use a **two-signal core definition**: (a) people with merge or commit rights, as OpenDoor does now, and (b) an 80% share of reviews plus merges. Disagreement between (a) and (b) is informative. For example, many committers but 1 person doing 80% of reviews means a review bottleneck.
- **Computation.** META (review and merge authors; the co-commenting network between issues and PRs).
- **Sources.**
  - Crowston et al.: https://crowston.syr.edu/sites/default/files/CoreAndPeripheryInFreeLibre.pdf
  - Joblin, Apel, Hunsen, Mauerer, "Classifying Developers into Core and Peripheral: An Empirical Study on Count and Network Metrics", ICSE 2017: https://arxiv.org/abs/1604.00830
- **Confidence.** [secondary] for the 80% origin. [read] (abstract) for Joblin.

### 5.2 Casual contributors are common
- **Claim.** Casual contributors (those with a single contribution) are about **49% of contributors but 1.73% of commits**. Both they and the maintainers see more benefit than harm in them. Lack of time is the main reason they do not stay.
- **Signal.** "Casual-friendly" is a valid door, especially for the "experienced but new to this project" profile.
  - **Casual share:** the share of merged outside PRs from one-time authors.
  - **Conversion:** the share of one-time authors who come back within 12 months.
- **Source.** Pinto, Steinmacher, Gerosa, "More Common Than You Think: An In-depth Study of Casual Contributors", SANER 2016. https://bibtex.github.io/SANER-2016-PintoSG.html
- **Confidence.** [secondary]

### 5.3 External contribution
- **Claim.** A study of 89 top-starred projects and their forks looked at how external (non-collaborator) contributions are distributed.
- **Signal.** This is prior art for OpenDoor's openness metric.
- **Source.** Padhye, Mani, Sinha, "A study of external community contribution to open-source projects on GitHub", MSR 2014. https://bibtex.github.io/MSR-2014-PadhyeMS.html
- **Confidence.** [secondary]. I did not retrieve the findings.

### 5.4 Company affiliation inference
- **Claim.**
  - The commit email domain is the standard proxy. The MSR 2020 enterprise dataset found 17,264 enterprise projects through domains filtered with blocklists and heuristics, with **89%** accuracy in a manual check.
  - It breaks with gmail.com, `users.noreply.github.com`, personal emails and companies with several domains.
  - OpenSSF Scorecard "Contributors" uses the **`company` field of the GitHub profile** on the last 30 commits, and needs at least 3 distinct companies, each with at least 5 commits.
  - OpenStack's Stackalytics keeps a hand-curated domain → company map.
- **Signal.** **Affiliation concentration**: whether insiders share an org or company. This feeds the "elephant factor" (§7.2) and the corporate-gap check (§3.4).
- **Computation.**
  - META: profile `company`, public org memberships, the commit email domain. Commit emails are already in git metadata, but the AGENTS.md rule says **not to collect e-mails**.
  - Extract the domain only, and only in memory, or use profile `company` and orgs instead.
- **Sources.**
  - Spinellis et al., "A Dataset of Enterprise-Driven Open Source Software", MSR 2020: https://www.spinellis.gr/pubs/conf/2020-MSR-enterprise-oss/html/indoss.pdf
  - Scorecard checks: https://github.com/ossf/scorecard/blob/main/docs/checks.md
- **Confidence.** [read] for Scorecard. [secondary] for MSR 2020.

### 5.5 GitHub data pitfalls
- **Claim.**
  - Most GitHub repos are personal or inactive.
  - About 40% of PRs that were in fact merged do **not appear as merged**, because they were integrated by rebase, squash or cherry-pick outside the UI.
  - About half of users have no public activity.
- **Signal.**
  - "Closed unmerged" overcounts rejections in repos that merge by hand. Detect a hand merge by a commit that references `#PR` or shares the same patch.
  - OpenDoor's note on direct commits ("a third-party commit applied by hand keeps the author's name") is consistent with this.
- **Source.** Kalliamvakou et al., "The Promises and Perils of Mining GitHub", MSR 2014 / EMSE. https://repository.tudelft.nl/record/uuid:d9115632-cfdd-4211-bc88-9fb27952f6a6
- **Confidence.** [secondary]. The 40% figure is from the extended version and depends on its time period.

---

## 6. Retention, disengagement and the long-term contributor

### 6.1 Why people leave
- **Claim.** The most common reason for leaving completely is a job transition: graduating, changing employer or changing role. Higher activity and more popular projects lower the risk. Mostly-office-hours contributors had about 2.2x the risk.
- **Signal.** Contributors who work mostly in office hours are likely paid. A core made of paid, office-hours contributors is fragile when the employer changes priorities. This is a soft context signal from commit timestamps (META).
- **Source.** Miller, Widder, Kästner, Vasilescu, "Why Do People Give Up FLOSSing? A Study of Contributor Disengagement in Open Source", OSS 2019. https://cmustrudel.github.io/papers/miller19dropout.pdf
- **Confidence.** [secondary]

### 6.2 Core developers take breaks
- **Claim.**
  - All core developers took at least 1 break, and about 45% fully disengaged for 1 year or more.
  - After a pause, the chance of returning is about 35–55%. After a break of 1 year or more, it is about 21–26%.
  - Breaks are detected against each developer's **own contribution rhythm**.
- **Signal.** **Maintainer absence**: an insider is "on break" if their current gap is larger than their usual gap, for example the 90th percentile of their inter-activity gaps. This is better than a fixed 24-month window, and it tells "1 maintainer, active" apart from "1 maintainer, on a 10-month break".
- **Computation.** META (activity timestamps per login).
- **Source.** Calefato, Gerosa, Iaffaldano, Lanubile, Steinmacher, "Will You Come Back to Contribute? Investigating the Inactivity of OSS Core Developers in GitHub", EMSE 27(3), 2022. https://arxiv.org/abs/2103.04656
- **Confidence.** [read] (abstract)

### 6.3 Social capital and diversity
- **Claim.** Social capital (team familiarity, and the variety of expertise in the team) prolongs engagement. Women are more likely to leave, but less likely to leave in teams with diverse expertise.
- **Signal.** This argues for recommending projects where a newcomer can **interact with several insiders**, not only one. In other words: the reviewer diversity on outside PRs, measured as the number of distinct insiders who review outside PRs.
- **Source.** Qiu, Nolte, Brown, Serebrenik, Vasilescu, "Going Farther Together: The Impact of Social Capital on Sustained Participation in Open Source", ICSE 2019. https://aserebre.win.tue.nl/ICSE2019.pdf
- **Related.** Vasilescu et al., "Gender and Tenure Diversity in GitHub Teams", CHI 2015: gender and tenure diversity positively predict productivity. https://www.cs.ucdavis.edu/~filkov/papers/chi15.pdf
- **Confidence.** [secondary]

### 6.4 Magnet and sticky
- **Claim.** Project typology by:
  - **magnet**: the share of new contributors in a period, relative to all contributors;
  - **sticky**: the share of last period's contributors who stay active this period.

  Projects with low magnet and low sticky decline.
- **Signal.** This is the most direct published operationalization of "does this project attract and keep people". OpenDoor's "debuts" is half of magnet, and it has no sticky yet.
- **Computation.** META, per year, over the contributor set: PR authors, plus commit authors where available.
- **Source.** Yamashita, Kamei, McIntosh, Hassan, Ubayashi, "Magnet or Sticky? Measuring Project Characteristics from the Perspective of Developer Attraction and Retention", JIP 24(2), 2016. https://sail.cs.queensu.ca/data/pdfs/2016_MagnetOrSticky_MeasuringProjectCharacteristicsFromThePerspectiveOfDeveloperAttractionAndRetention.pdf
- **Confidence.** [secondary]. Check the exact formulas in the PDF.

---

## 7. Governance and concentration

### 7.1 Truck factor (Avelino et al.) and how the algorithms compare
- **Claim.**
  - The truck factor is the minimum number of developers who would have to leave before the project stalls.
  - File authorship comes from **Degree of Authorship (DOA)**, which combines first authorship, the number of the author's own changes, and changes by others, on a log scale.
  - A developer "owns" a file if their normalized DOA is above 0.75 and the absolute DOA is at least 3.2 (thresholds from the paper; check them).
  - A greedy loop removes the top author until more than 50% of the files have no author.

  In 133 popular apps, 46% had TF=1 and 28% had TF=2. Comparing 3 algorithms against an oracle built from 35 projects' maintainers, **AVL** (Avelino) was the most accurate, with a best coverage threshold of 50%. A public implementation exists.
- **Signal.** **Truck factor** of the codebase. It complements OpenDoor's "1–2 people merged" (a review-process concentration) with knowledge concentration.
- **Computation.** It needs **git history per file**: a clone, or the commits API with file lists. It is expensive for large repos, as noted by arXiv 2412.00313. It uses neither TEXT nor emails beyond the author identity (which can be the GitHub login).
- **Sources.**
  - Avelino, Passos, Hora, Valente, "A Novel Approach for Estimating Truck Factors", ICPC 2016: https://arxiv.org/abs/1604.06766
  - Preprint: https://peerj.com/preprints/1233v2/
  - Ferreira, Valente, Ferreira, "A Comparison of Three Algorithms for Computing Truck Factors", ICPC 2017: https://homepages.dcc.ufmg.br/~mtov/pub/2017-icpc.pdf
  - Implementation: https://github.com/aserg-ufmg/truck-factor
- **Confidence.** [secondary] for the DOA thresholds; check them. The headline numbers are confirmed across sources.

### 7.2 Abandonment and survival
- **Claim.**
  - Of 1,932 popular projects, 315 (16%) went through a TF-developer detachment, meaning all truck-factor developers left.
  - **41%** of those survived, usually by attracting **one** new TF developer (86%).
  - Those who took over were mostly motivated by using the software themselves. Their barriers were lack of time and **difficulty getting push access**.
- **Signal.** This is a direct basis for the **"guardian / needs successor"** entry path for experienced people. Detect it with a TF of 1 plus that developer's absence (§6.2) plus continued demand from users (incoming issues).
- **Source.** Avelino, Constantinou, Valente, Serebrenik, "On the abandonment and survival of open source projects: An empirical investigation", ESEM 2019. https://arxiv.org/abs/1906.08058
- **Confidence.** [secondary]. The numbers agree across 2 sources.

### 7.3 CHAOSS concentration metrics
- **Contributor Absence Factor** (formerly "Bus Factor"):
  - **Definition:** the smallest number of contributors who make up **50%** of total contributions.
  - **Computation:** sort contributors by contribution count, then add them up until the running total is above 50%.
  - The contribution type is configurable: commits, issues, comments.
  - Caveats: it does not say how to handle bots, ties or merged identities, and the result depends on the contribution type.
  - Source: https://chaoss.community/kb/metric-bus-factor/ [read]
- **Elephant Factor:**
  - **Definition:** the smallest number of **companies** whose employees make a chosen share (50% in the example) of commits.
  - CHAOSS **does not specify how affiliation is assigned**.
  - The threshold should scale with the number of organizations.
  - Source: https://chaoss.community/kb/metric-elephant-factor/ [read]
- **Inclusive Leadership:**
  - Asks: "How well is a project and community set up for diverse leadership?"
  - It is a **qualitative checklist**: term limits for leaders, documented roles, emeritus paths, accountability, disclosed inactivity, equal recognition of technical and non-technical work.
  - Filters include maintainers, people with merge rights, org members, and contacts listed in project documents.
  - It is mostly answerable by an LLM reading GOVERNANCE.md, MAINTAINERS and CODEOWNERS.
  - Source: https://chaoss.community/kb/metric-inclusive-leadership/ [read]
- **Signal.**
  - The agent reads GOVERNANCE.md, MAINTAINERS, OWNERS and CODEOWNERS, and extracts:
    - the documented roles;
    - whether there is a path from contributor to committer;
    - who owns which directories.
  - Rules then check consistency with behavior: do the listed owners actually review?
  - CODEOWNERS gives a **per-directory reviewer map**, which is useful for entry paths ("PRs under `docs/` are reviewed by @x, who reviews in a median of N days").
  - I found no academic study validating CODEOWNERS as a signal. This is my inference.

### 7.4 OpenSSF Scorecard checks (already partly used)
- **Maintained:**
  - Highest score: at least 1 commit per week over 90 days.
  - Partial credit: issue activity by collaborators, members or owners.
  - Archived: the lowest score.
- **Code-Review:**
  - Looks at about the last 30 commits.
  - Counts as reviewed: an approval, or a merger different from the committer.
  - Bot reviews do not count.
- **Contributors:** see §5.4.
- **Source.** https://github.com/ossf/scorecard/blob/main/docs/checks.md [read]

---

## 8. "Would this project benefit from more contributors?" Demand and sustainability

### 8.1 Unmaintained detection
- **Claim.** An ML model on GitHub metadata (commits, forks, issues, PRs) for each period reached 80% precision and 96% recall when checked against developers. 16% of 2,927 active projects became unmaintained within 1 year.
- **Signal.** A **level-of-maintenance score** to exclude dead ends. OpenDoor's "≥1 merged PR in 3 months" for needs-hands is a crude version of it. The paper's features are cheap to compute.
- **Source.** Coelho, Valente, Milen, Silva, "Is this GitHub Project Maintained? Measuring the Level of Maintenance Activity of Open-Source Projects", IST 2020. https://arxiv.org/abs/2003.04755
- **Confidence.** [secondary]

### 8.2 Ecosystem position and the labor pool
- **Claim.** In PyPI, position in the dependency network significantly affects how long a project stays active (Cox survival models). Labor-pool factors add considerable explanatory power beyond project-level factors.
- **Signal.** Dependents (OpenDoor already has deps.dev) are a **sustainability-risk modifier**: a project with many dependents and a shrinking contributor pool needs help.
- **Source.** Valiev, Vasilescu, Herbsleb, "Ecosystem-Level Determinants of Sustained Activity in Open-Source Projects: A Case Study of the PyPI Ecosystem", ESEC/FSE 2018. https://cmustrudel.github.io/papers/fse18sustainability.pdf
- **Confidence.** [secondary]

### 8.3 Maintainer stress and toxicity
- **Claim.** Maintainers report high stress from frequent, sometimes aggressive demands. Toxic conversations demotivate people and cause burnout. The paper is a vision paper that proposes a toxicity classifier.
- **Signal.** **Demand pressure**: new issues per active maintainer per month. Optionally, a toxicity rate on comments, which needs TEXT. Compute it on the fly and store only the rate.
- **Source.** Raman, Cao, Tsvetkov, Kästner, Vasilescu, "Stress and Burnout in Open Source", ICSE NIER 2020. https://cmustrudel.github.io/papers/raman20toxicity.pdf
- **Confidence.** [secondary]

### 8.4 Demand signals from CHAOSS
- **Time to First Response:**
  - The time from when an item that needs attention is created to the first response.
  - **Exclude bots.** It can be filtered by responder role (for example, maintainers only).
  - It does not say how to handle items that never get a response, or replies that are not substantive.
  - Source: https://chaoss.community/kb/metric-time-to-first-response/ [read]
- **Change Request Acceptance Ratio:**
  - Merged divided by closed-without-merge. Open requests are excluded.
  - It can be filtered by **origin: fork versus branch**. Fork PRs usually come from outsiders, so this is a cheap insider/outsider proxy.
  - Do not compare it across projects as if the values were equivalent.
  - Source: https://chaoss.community/kb/metric-change-request-acceptance-ratio/ [read]
- **Issue Age:** the time from opening to closing, or to the end of the period. Report the mean or median of open issues. It can be filtered by label. Source: https://chaoss.community/kb/metric-issue-age/ [read]
- **Newcomer Experience:**
  - Quantitative parts: whether first-time contributors come back, and whether new contributors close issues.
  - The rest is surveys.
  - It gives no formula or benchmark.
  - Source: https://chaoss.community/kb/metric-newcomer-experience/ [read]
- **New Contributors, Occasional Contributors, Inactive Contributors:**
  - Counts of first contributions.
  - Counts of irregular contributors, with thresholds for minimum contributions and maximum gap.
  - Counts of contributors whose gap is longer than a chosen interval.
  - Sources: https://chaoss.community/kb/metric-occasional-contributors/ and https://chaoss.community/metric-inactive-contributors/ [secondary]
- **Signal for "needs more contributors".** Combine these:
  - growing open-issue backlog and issue age;
  - few active insiders (absence-aware);
  - outside PRs still being merged, so the door works;
  - stale review queue.

  "Needs hands" means demand is high **and** the door works. If demand is high and the door does not work, it is a dead end, which OpenDoor already learned in the October 31 audit.

---

## 9. Pitfalls and critiques

1. **Bots and agents break identity-based metrics.** New-contributor counts, acceptance ratio, response time and bus factor all assume that one account is one human who spent real effort. AI triage makes first responses look instant. A departed maintainer whose token still auto-merges looks active. A falling acceptance ratio may mean maintainers are reviewing properly against cheap PRs. Bot detection by label or name misses agents that post through personal tokens. Source: Andrew Nesbitt, "CHAOSS metrics in 2026" (blog, not peer-reviewed). https://nesbitt.io/2026/05/27/chaoss-metrics-in-2026.html [read]
2. **Gaming and fake popularity.**
   - StarScout flagged about 4.5 million suspected fake stars and 15,835 repos (2019–2024), with a 2-order-of-magnitude rise in 2024.
   - Fake stars give only a short-lived boost.
   - Do not use stars as a quality signal.
   - Source: He et al., "4.5 Million (Suspected) Fake Stars in GitHub", arXiv 2412.13459. https://arxiv.org/abs/2412.13459 [secondary]
3. **Incentive-driven spam.**
   - In Hacktoberfest 2020, at least 4% of participant PRs were marked invalid or spam.
   - That led to opt-in through the `hacktoberfest` topic, and spam labels.
   - Spikes in outside-PR volume in October are not demand.
   - A "spam"/"invalid" label rate is a useful filter.
   - Sources: https://www.theregister.com/2020/10/01/digitalocean_hacktoberfest_pull_request_spam/ and https://developerrelations.com/case-studies/overcoming-hacktoberfest-spam [secondary, news]
4. **Hidden merges.** About 40% of PRs that were merged show as unmerged (Kalliamvakou). Acceptance rates are biased low in repos that merge by rebase or cherry-pick.
5. **Bias toward large repos.**
   - Ratios are not comparable across projects (CHAOSS's own caveat).
   - The Elephant factor threshold should scale with the number of organizations.
   - The truck factor is expensive and noisy in monorepos.
   - Survival and abandonment studies are run on popular repos.
   - OpenDoor's sampled mode for large repos is the right instinct. Show "insufficient data", do not show a low score.
6. **Count versus network core definitions disagree** (Joblin 2017). Firefox showed low agreement between methods. Treat "core" as uncertain and use more than one definition.
7. **Correlation, not causation.** Almost all findings here are observational: GFI, response time, mentoring. Only the 2026 first-issue paper claims causal inference, and it is a preprint. Thresholds such as 14 days, 25% or 2 debuts are **choices for the product**, not empirical cutoffs. Calibrate them against OpenDoor's own outcome data: for example, do the debuts of a badged project come back?
8. **The current `authorAssociation`.** This is already documented in AGENTS.md, and the literature uses the same proxy with the same flaw.
9. **Privacy.**
   - Every CHAOSS page warns about GDPR and terms of service. OpenDoor's rule (no e-mails, no content) is stricter than common practice.
   - Affiliation from email domains clashes with it. Use profile `company` and orgs.
   - Never infer gender.

---

## 10. Ranked: the ~10 most useful signals and methods for OpenDoor

| # | Signal / method | Computation | Rationale |
|---|---|---|---|
| 1 | **Newcomer conversion (sticky).** Of the people who debuted in a 12-month window, the share who contribute again within the next 6–12 months. Yamashita magnet/sticky; Zhou & Mockus; CHAOSS Newcomer Experience. | META | OpenDoor measures entry (debuts) but not whether newcomers **stay**. Staying is the outcome the whole literature cares about, and it is the best ground truth for calibrating the other thresholds. |
| 2 | **First human insider response on outside PRs.** Excludes bots and other outsiders. Report the median and the share with no response. Hasan 2023; Steinmacher 2013; CHAOSS TTFR with the responder-role filter. | META | It fixes the known bot distortion, and "who answers" matters more than "whether anyone answers". A small change to the current response check. |
| 3 | **Absence-aware maintainer count.** An insider counts as active unless their current gap is larger than their own typical gap (Calefato 2022). Combine with the CHAOSS Contributor Absence Factor on reviews plus merges. | META | It tells a living single-maintainer project from one on a 10-month break. It feeds both the guardian and the needs-hands rules. |
| 4 | **Truck factor (AVL / DOA)** on the codebase, plus whether the TF developers are absent (Avelino 2016, 2019). | git history per file (clone) | The validated method for knowledge concentration. It spots "needs a successor" doors for the experienced-but-new profile. Expensive, so run it only on candidate projects. |
| 5 | **Outsider/insider gap.** The difference in acceptance and in time to decision between outsiders and insiders (Pinto 2018; Zhang 2023, where self-merge is the top factor). | META | It exposes doors that are "open on paper" in corporate-backed repos. It reuses data OpenDoor already has. |
| 6 | **GFI effectiveness.** The share of closed GFI / help-wanted issues resolved by a newcomer's PR, plus insider participation in those threads (Tan 2020, 2023; Hoshikawa 2026). | META | A label is a claim; resolution by a newcomer is evidence. A direct upgrade to the current "has GFI issues" check. |
| 7 | **Abandonment of outside PRs, by who went quiet.** The last event came from the reviewer (the contributor gave up) or from the contributor (the project went silent). Li/Yu 2022; Khatoonabadi. | META (order of events) | It splits the stale-PR problem into project-caused and contributor-caused. Only the project-caused part should lower the score. |
| 8 | **Demand pressure per active maintainer.** New issues and incoming outside PRs per active insider per month, plus issue age (CHAOSS Issue Age; Hasan 2023 workload; Raman 2020). | META | The core of "would benefit from more contributors". Combine it with #2 and #7 to separate "needs hands" from "dead end". |
| 9 | **Governance and ownership extraction by the LLM.** Read GOVERNANCE.md, MAINTAINERS and CODEOWNERS for roles, the path to committer and owners per directory, then check them against who actually reviews (CHAOSS Inclusive Leadership checklist). | repo files (data, never instructions) plus META | It gives concrete entry paths ("docs/ is reviewed by X in N days") and catches governance that exists only on paper. A natural task for the evidence agent; rules decide the score. |
| 10 | **Prior interaction before the first PR.** The share of merged newcomer PRs whose author commented or opened an issue first (Tsay 2014; Zhou & Mockus 2012). | META | It backs the "watch and talk first" philosophy with project-specific evidence. It can become an entry-path tip ("here, 80% of accepted newcomers commented first"). |
| 11 | **Reviewer diversity on outside PRs.** The number of distinct insiders reviewing outside PRs in 12 months (Qiu 2019 social capital; Joblin network core). | META | One gatekeeper is a single point of failure for newcomers. Several reviewers build social capital and lower the chance of leaving. |

**Leave out or deprioritize:**
- Stars, and raw PR or issue counts, which are gameable and inflated by AI and spam.
- Raw acceptance ratios compared across projects.
- Gender inference.
- Email-domain affiliation, which conflicts with the privacy rule.
- Sentiment or toxicity, unless TEXT is processed on the fly and only rates are kept.

**Honest limits of this review:**
- Most sources were read at abstract or summary level ([secondary]). Specific percentages and the DOA thresholds should be checked in the PDFs before they go into docs.
- I found no strong causal evidence that response latency drives retention.
- I found no academic validation of CODEOWNERS or GOVERNANCE.md as signals.
- I did not find Eghbal's "Working in Public" typology (federations, clubs, toys, stadiums) in a primary source during this search, so it is not cited, although it is conceptually relevant.
