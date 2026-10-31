// G1: monta o "por onde começar" a partir do guia salvo do projeto e do perfil. Sem modelo: mesma entrada, mesma saída.
import type { Guide, UserProfile, Way } from "./types";

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
