// D4: match ranking, runs in the browser. Rules in docs/arquitetura.md ("Regras de ranking").
import type { Level, Profile, Project, UserProfile, Way } from "./types";


// Ways to help that need no technical skill in common with the project.
const NON_CODE: Way[] = ["triage", "refinement", "documentation", "translation"];

const LEVEL_BONUS: Record<Level, Partial<Record<Profile, number>>> = {
  beginner: { open_door: 4, needs_hands: 1 },
  intermediate: { open_door: 2, needs_hands: 3, guardian: 1 },
  experienced: { guardian: 4, needs_hands: 3, open_door: 1 },
};

// languageIds: ids from skills.json with kind "language". If the person picked languages, the project must use one of them.
// For beginners, only ready projects: newcomers getting accepted, outside PRs with a real chance,
// an active project with a contribution guide (computed in build.py, beginner_checks).
export function welcoming(p: Project): boolean {
  return p.beginner.ready;
}

export function rankProjects(projects: Project[], profile: UserProfile, languageIds: ReadonlySet<string> = new Set()): Project[] {
  const wanted = new Set(profile.skills);
  const wantedLangs = profile.skills.filter((s) => languageIds.has(s));
  const ways = new Set(profile.ways);
  const nonCodeOnly = ways.size > 0 && [...ways].every((w) => NON_CODE.includes(w));

  const scored: { p: Project; score: number }[] = [];
  for (const p of projects) {
    if (p.profile === "stable") continue;
    // a guardian needs experienced, trusted people: not a door for someone just starting
    if (p.profile === "guardian" && profile.level === "beginner") continue;
    if (profile.level === "beginner" && !welcoming(p)) continue;
    if (ways.size > 0 && !p.needs.some((w) => ways.has(w))) continue;
    const common = p.skills.filter((s) => wanted.has(s)).length;
    if (wanted.size > 0 && common === 0 && !nonCodeOnly) continue;
    if (wantedLangs.length > 0 && !nonCodeOnly && !wantedLangs.some((l) => p.skills.includes(l))) continue;

    let score = common * 5 + (LEVEL_BONUS[profile.level][p.profile] ?? 0);
    if (profile.level === "beginner" && p.newcomer_open > 0) score += 2;
    score += p.needs.filter((w) => ways.has(w)).length;
    scored.push({ p, score });
  }
  return scored
    // tie-break: newcomers getting accepted, then acceptance rate (openness alone misleads in a 1-person project)
    .sort(
      (a, b) =>
        b.score - a.score ||
        (b.p.debuts_12m ?? -1) - (a.p.debuts_12m ?? -1) ||
        (b.p.acceptance ?? -1) - (a.p.acceptance ?? -1) ||
        b.p.stars - a.p.stars,
    )
    .map((x) => x.p);
}
