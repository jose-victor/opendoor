// O perfil marcado na home também vale na página do projeto (S3). Fica só no navegador desta pessoa.
import type { UserProfile } from "./types";

const KEY = "opendoor:profile";
export const EMPTY_PROFILE: UserProfile = { skills: [], level: "iniciante", ways: [] };

export function loadProfile(): UserProfile {
  try {
    const p = JSON.parse(sessionStorage.getItem(KEY) ?? "null");
    if (p && Array.isArray(p.skills) && Array.isArray(p.ways) && typeof p.level === "string") return p;
  } catch {}
  return EMPTY_PROFILE;
}

export function saveProfile(p: UserProfile) {
  try {
    sessionStorage.setItem(KEY, JSON.stringify(p));
  } catch {}
}
