# Probe: `assignableUsers` vs public members

Run on 2026-11-02 with one throwaway script. `assignableUsers` = people with write access plus org members with read access, so it includes private org members that `authorAssociation` and the public members list miss.

| Repo | assignableUsers | Pages | GraphQL points | Public members (REST) |
|---|---|---|---|---|
| mastodon/mastodon | 20 | 1 | 1 | 9 |
| tailwindlabs/tailwindcss | 4 | 1 | 1 | 0 |
| microsoft/vscode | 85 | 1 | 1 | >= 1000 (REST count stopped at 10 pages) |
| expressjs/express | 20 | 1 | 1 | 38 |

- Cost: 1 point per page of 100, so 4 points in total. No repo needed more than one page; the 20-page cap (`ASSIGNABLE_MAX_PAGES`, 2,000 logins) was not reached and no repo was capped.
- Mastodon: 20 assignable against 9 public members, confirming the private-member gap.
- Public members can exceed assignable (express: 38 vs 20; vscode: >= 1000 vs 85): public membership does not imply repo access, so the two numbers are different signals. Orgs with tens of thousands of public members make the REST count capped at 1,000.
