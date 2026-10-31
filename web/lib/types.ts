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

// D5: por que o projeto precisa dessa forma de ajuda. "projeto" = o guia de contribuição pede;
// "dados" = os números mostram; "gemma" = sugestão da IA (mostrar como sugestão, não como fato).
export type Opportunity = { way: Way; source: "projeto" | "dados" | "gemma"; note: string };

// G1: guia "por onde começar" escrito pelo Gemma uma vez por projeto (pipeline/guides.py).
// O site combina com o perfil em lib/guide.ts, sem chamar o modelo. null = ainda não gerado.
export type Guide = {
  summary: string;                               // o que é o projeto e onde precisa de ajuda, em pt-BR
  common_steps: string[];                        // observar e conversar
  steps_by_way: Partial<Record<Way, string[]>>;  // 2 ou 3 passos por forma de ajuda
  heads_up: string | null;
};

// Atividade dos 3 últimos meses fechados (since/until = "AAAA-MM"): o projeto responde ou acumula?
export type Recent = { since: string; until: string; issues_opened: number; issues_closed: number; prs_opened: number; prs_merged: number };

// Pronto para iniciante: as 4 verificações precisam passar (estreias, aceite, vivo, guia). Ver docs/arquitetura.md.
export type Beginner = { ready: boolean; checks: { key: "estreias" | "aceite" | "vivo" | "resposta" | "guia"; ok: boolean; text: string }[] };

// Retorno aos PRs de gente de fora abertos em 12 meses (cache bruto da activity; null sem dados ou com menos de 5 PRs).
export type Review = { median_days: number; stale_open: number; prs: number };

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
  recent: Recent | null;      // últimos 3 meses fechados
  acceptance: number | null;  // dos PRs que gente de fora abriu em 12 meses, a fatia aceita; null = menos de 5
  debuts_12m: number | null;  // pessoas de fora com o primeiro PR aceito nos últimos 12 meses; null nos repos grandes
  beginner: Beginner;         // pronto para iniciante, com as provas
  review: Review | null;      // dias até o 1º retorno (mediana) e PRs parados há 30+ dias sem revisão
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
