// A1 (Anna): cliente da Gemini API (Gemma 4). Só roda no servidor: usa process.env.GEMINI_API_KEY.
// Contrato da saída: ExplainResponse em lib/types.ts e docs/arquitetura.md.
import type { ExplainResponse, Project, UserProfile } from "./types";

export async function explain(project: Project, profile: UserProfile): Promise<ExplainResponse> {
  void project;
  void profile;
  throw new Error("explain() ainda não implementado (issue A1)");
}
