// Tipos do contrato (docs/arquitetura.md). Mudou algo aqui? Mude o doc e avise o time.

export type Skill = {
  id: string;
  label: string;
  kind: "linguagem" | "framework" | "ferramenta" | "area";
};

export type Profile = "guardiao" | "porta_aberta" | "precisa_de_maos" | "estavel";

export type Way =
  | "codigo"
  | "triagem"
  | "revisao"
  | "refinamento"
  | "documentacao"
  | "traducao"
  | "seguranca"
  | "testes";

export type AiPolicy = {
  classification: "accepts" | "accepts_with_disclosure" | "forbids" | "silent" | "unknown";
  evidence: string;
  source_file: string;
};

export type YearStats = {
  prs_opened: number;
  prs_merged: number;
  issues_opened: number;
  issues_closed: number;
  commits: number;
  direct_commits: number | null; // null em repos grandes (contagem+amostra)
  people: number | null;         // null em repos grandes (contagem+amostra)
};

export type Project = {
  repo: string;
  url: string;
  tags: ("npm-graph" | "mainstream-app")[];
  description: string | null;
  language: string | null;
  license: string | null;
  stars: number;
  dependents: number | null;
  profile: Profile;
  needs: Way[];
  skills: string[];
  openness: number | null;
  maintainers_24m: number;
  newcomer_open: number;
  scorecard: number | null;
  ai_policy: AiPolicy;
  collection: "completo" | "contagem+amostra";
  coverage_since: string;
  years: Record<string, YearStats>;
};

export type Level = "iniciante" | "intermediario" | "experiente";

export type UserProfile = {
  skills: string[];
  level: Level;
  ways: Way[];
};

export type ExplainRequest = { repo: string; profile: UserProfile };

export type ExplainResponse =
  | { ok: true; why: string; first_steps: string[]; heads_up: string | null; model: string }
  | { ok: false; error: "rate_limited" | "not_found" | "bad_request" | "model_error"; message: string };

export const LEVELS: Level[] = ["iniciante", "intermediario", "experiente"];
export const WAYS: Way[] = ["codigo", "triagem", "revisao", "refinamento", "documentacao", "traducao", "seguranca", "testes"];
