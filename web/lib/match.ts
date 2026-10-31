// D4 (José): ranking do match. Versão provisória: filtra por habilidade em comum e ordena por estrelas.
import type { Project, UserProfile } from "./types";

export function rankProjects(projects: Project[], profile: UserProfile): Project[] {
  const wanted = new Set(profile.skills);
  return projects
    .filter((p) => p.profile !== "estavel")
    .filter((p) => wanted.size === 0 || p.skills.some((s) => wanted.has(s)))
    .sort((a, b) => b.stars - a.stars);
}
