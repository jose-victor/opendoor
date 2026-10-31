// D4: ranking do match, roda no navegador. Regras em docs/arquitetura.md ("Regras de ranking").
import type { Level, Profile, Project, UserProfile, Way } from "./types";

// Poucas portas, não uma lista infinita (docs/visao.md).
export const MAX_DOORS = 5;

// Formas de ajudar que não exigem habilidade técnica em comum com o projeto.
const NON_CODE: Way[] = ["triagem", "refinamento", "documentacao", "traducao"];

const LEVEL_BONUS: Record<Level, Partial<Record<Profile, number>>> = {
  iniciante: { porta_aberta: 4, precisa_de_maos: 1 },
  intermediario: { porta_aberta: 2, precisa_de_maos: 3, guardiao: 1 },
  experiente: { guardiao: 4, precisa_de_maos: 3, porta_aberta: 1 },
};

// languageIds: ids de skills.json com kind "linguagem". Se a pessoa marcou linguagens, o projeto precisa usar uma delas.
// Acolhe quem está começando: issues marcadas para iniciantes ou 25%+ dos PRs aceitos vindos de fora.
export function welcoming(p: Project): boolean {
  return p.newcomer_open > 0 || (p.openness ?? 0) >= 0.25;
}

export function rankProjects(projects: Project[], profile: UserProfile, languageIds: ReadonlySet<string> = new Set()): Project[] {
  const wanted = new Set(profile.skills);
  const wantedLangs = profile.skills.filter((s) => languageIds.has(s));
  const ways = new Set(profile.ways);
  const nonCodeOnly = ways.size > 0 && [...ways].every((w) => NON_CODE.includes(w));

  const scored: { p: Project; score: number }[] = [];
  for (const p of projects) {
    if (p.profile === "estavel") continue;
    // guardião pede gente experiente e de confiança: não é porta para quem está começando
    if (p.profile === "guardiao" && profile.level === "iniciante") continue;
    if (profile.level === "iniciante" && !welcoming(p)) continue;
    if (ways.size > 0 && !p.needs.some((w) => ways.has(w))) continue;
    const common = p.skills.filter((s) => wanted.has(s)).length;
    if (wanted.size > 0 && common === 0 && !nonCodeOnly) continue;
    if (wantedLangs.length > 0 && !nonCodeOnly && !wantedLangs.some((l) => p.skills.includes(l))) continue;

    let score = common * 5 + (LEVEL_BONUS[profile.level][p.profile] ?? 0);
    if (profile.level === "iniciante" && p.newcomer_open > 0) score += 2;
    score += p.needs.filter((w) => ways.has(w)).length;
    scored.push({ p, score });
  }
  return scored
    .sort((a, b) => b.score - a.score || (b.p.openness ?? 0) - (a.p.openness ?? 0) || b.p.stars - a.p.stars)
    .slice(0, MAX_DOORS)
    .map((x) => x.p);
}
