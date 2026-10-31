// G1: monta o "por onde começar" a partir do guia salvo do projeto e do perfil. Sem modelo: mesma entrada, mesma saída.
import type { Guide, Project, UserProfile, Way } from "./types";

// Para quem começa: contribuições de baixo risco primeiro (docs/visao.md).
const BEGINNER_FIRST: Way[] = ["testes", "documentacao", "triagem", "traducao", "refinamento"];
const MAX_WAYS = 2;

export type GuideStep = { text: string; way?: Way };

export function composeGuide(guide: Guide, profile: UserProfile): { summary: string; steps: GuideStep[]; heads_up: string | null; ways: Way[] } {
  const available = Object.keys(guide.steps_by_way) as Way[];
  const chosen = profile.ways.filter((w) => available.includes(w));
  const fallback = profile.level === "iniciante" ? BEGINNER_FIRST.filter((w) => available.includes(w)) : available;
  const ways = (chosen.length ? chosen : fallback.length ? fallback : available).slice(0, MAX_WAYS);
  const steps: GuideStep[] = [
    ...guide.common_steps.slice(0, 2).map((text) => ({ text })),
    ...ways.flatMap((way) => (guide.steps_by_way[way] ?? []).slice(0, 2).map((text) => ({ text, way }))),
  ];
  return { summary: guide.summary, steps, heads_up: guide.heads_up, ways };
}

// Projeto ainda sem guia salvo: passos montados a partir das oportunidades, também sem modelo.
export function guideFor(p: Project): Guide {
  if (p.guide) return p.guide;
  const steps_by_way: Partial<Record<Way, string[]>> = {};
  for (const o of p.opportunities) steps_by_way[o.way] = [...(steps_by_way[o.way] ?? []), o.note.charAt(0).toUpperCase() + o.note.slice(1) + (/[.!?]$/.test(o.note) ? "" : ".")];
  return {
    summary: p.description ?? "",
    common_steps: ["Leia o README e o guia de contribuição (CONTRIBUTING).", "Acompanhe as issues e as discussões abertas antes de propor algo."],
    steps_by_way,
    heads_up: null,
  };
}

// Alerta da política de IA vem do dado classificado (com a citação), não do texto gerado.
export function aiPolicyNote(p: Project): string | null {
  const { classification, evidence } = p.ai_policy;
  const quote = evidence ? ` O projeto diz: “${evidence}”` : "";
  if (classification === "forbids") return `Este projeto não aceita contribuições feitas com IA.${quote}`;
  if (classification === "accepts_with_disclosure") return `Este projeto pede que você avise quando usar IA.${quote}`;
  return null;
}
