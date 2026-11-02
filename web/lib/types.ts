// Contract types (docs/arquitetura.md). Changed something here? Update the doc and tell the team.

export type Skill = {
  id: string;
  label: string;
  kind: "language" | "framework" | "tool" | "area";
};

export type Profile = "guardian" | "open_door" | "needs_hands" | "stable";

export type Way =
  | "code"
  | "triage"
  | "review"
  | "refinement"
  | "documentation"
  | "translation"
  | "security"
  | "tests";

export type AiPolicy = {
  classification: "accepts" | "accepts_with_disclosure" | "forbids" | "silent" | "unknown";
  evidence: string;
  source_file: string;
};

// D5: why the project needs this way of helping. "project" = the contribution guide asks for it;
// "data" = the numbers show it; "gemini" = AI suggestion (show it as a suggestion, not as fact).
export type Opportunity = { way: Way; source: "project" | "data" | "gemini"; note: string };

// G1: "por onde começar" guide written by the LLM once per project (pipeline/guides.py).
// The site combines it with the profile in lib/guide.ts, without calling the model. null = not generated yet.
export type Guide = {
  summary: string;                               // what the project is and where it needs help, in pt-BR
  common_steps: string[];                        // observe and talk
  steps_by_way: Partial<Record<Way, string[]>>;  // 2 or 3 steps per way of helping
  heads_up: string | null;
};

// Activity in the last 3 closed months (since/until = "YYYY-MM"): does the project respond or pile up?
export type Recent = { since: string; until: string; issues_opened: number; issues_closed: number; prs_opened: number; prs_merged: number };

// Beginner-ready: the 4 checks must pass (debuts, acceptance, active, guide). See docs/arquitetura.md.
export type Beginner = { ready: boolean; checks: { key: "debuts" | "acceptance" | "active" | "response" | "guide"; ok: boolean; text: string }[] };

// Response to outside PRs opened in 12 months (raw activity cache; null without data or with fewer than 5 PRs).
export type Review = { median_days: number; stale_open: number; prs: number };

export type YearStats = {
  prs_opened: number;
  prs_merged: number;
  issues_opened: number;
  issues_closed: number;
  commits: number;
  direct_commits: number | null; // null in large repos (sampled)
  people: number | null;         // null in large repos (sampled)
};

export type Project = {
  repo: string;
  url: string;
  tags: ("npm-graph" | "pypi-graph" | "go-graph" | "mainstream-app")[];
  description: string | null;
  language: string | null;
  license: string | null;
  stars: number;
  dependents: number | null;
  profile: Profile;
  needs: Way[];
  opportunities: Opportunity[];
  guide: Guide | null;
  recent: Recent | null;      // last 3 closed months
  acceptance: number | null;  // share accepted of the PRs outsiders opened in 12 months; null = fewer than 5
  debuts_12m: number | null;  // outsiders whose first PR was accepted in the last 12 months; null in large repos
  beginner: Beginner;         // beginner-ready, with the evidence
  review: Review | null;      // days to first response (median) and PRs stuck 30+ days without review
  skills: string[];
  openness: number | null;
  maintainers_24m: number;
  newcomer_open: number;
  scorecard: number | null;
  ai_policy: AiPolicy;
  collection: "full" | "sampled";
  coverage_since: string;
  years: Record<string, YearStats>;
};

export type Level = "beginner" | "intermediate" | "experienced";

export type UserProfile = {
  skills: string[];
  level: Level;
  ways: Way[];
};

export type ExplainRequest = { repo: string; profile: UserProfile };

export type ExplainResponse =
  | { ok: true; why: string; first_steps: string[]; heads_up: string | null; model: string }
  | { ok: false; error: "rate_limited" | "not_found" | "bad_request" | "model_error"; message: string };

export const LEVELS: Level[] = ["beginner", "intermediate", "experienced"];
export const WAYS: Way[] = ["code", "triage", "review", "refinement", "documentation", "translation", "security", "tests"];
