// G1: builds "por onde começar" from the project's saved guide and the profile. No model: same input, same output.
import type { Guide, Project, UserProfile, Way } from "./types";

// For beginners: low-risk contributions first (docs/vision.md).
const BEGINNER_FIRST: Way[] = ["tests", "documentation", "triage", "translation", "refinement"];
const MAX_WAYS = 2;

export type GuideStep = { text: string; way?: Way };

export function composeGuide(guide: Guide, profile: UserProfile): { summary: string; steps: GuideStep[]; heads_up: string | null; ways: Way[] } {
  const available = Object.keys(guide.steps_by_way) as Way[];
  const chosen = profile.ways.filter((w) => available.includes(w));
  const fallback = profile.level === "beginner" ? BEGINNER_FIRST.filter((w) => available.includes(w)) : available;
  const ways = (chosen.length ? chosen : fallback.length ? fallback : available).slice(0, MAX_WAYS);
  const steps: GuideStep[] = [
    ...guide.common_steps.slice(0, 2).map((text) => ({ text })),
    ...ways.flatMap((way) => (guide.steps_by_way[way] ?? []).slice(0, 2).map((text) => ({ text, way }))),
  ];
  return { summary: guide.summary, steps, heads_up: guide.heads_up, ways };
}

// Project without a saved guide yet: steps built from the opportunities, also without a model.
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

// The AI policy warning comes from the classified data (with the quote), not from generated text.
export function aiPolicyNote(p: Project): string | null {
  const { classification, evidence } = p.ai_policy;
  const quote = evidence ? ` O projeto diz: “${evidence}”` : "";
  if (classification === "forbids") return `Este projeto não aceita contribuições feitas com IA.${quote}`;
  if (classification === "accepts_with_disclosure") return `Este projeto pede que você avise quando usar IA.${quote}`;
  return null;
}
