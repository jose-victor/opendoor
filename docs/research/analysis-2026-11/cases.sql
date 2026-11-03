-- run with: sqlite3 -readonly data/ecosystem.db < cases.sql
-- pallets/jinja: PRs opened vs merged per year, and merges by month since 2025-06
SELECT substr(month,1,4) year, SUM(prs_opened), SUM(prs_merged) FROM repo_monthly
WHERE repo='pallets/jinja' AND month>='2024-01' GROUP BY 1;
SELECT month, COUNT(*) FROM participation WHERE repo='pallets/jinja' AND role='pr_merger' AND month>='2025-06' GROUP BY 1;
