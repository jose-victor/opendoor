// The profile picked on the home page also applies on the project page (S3). It stays only in this person's browser.
import { LEVELS, WAYS, type UserProfile, type Way } from "./types";

const KEY = "opendoor:profile";
export const EMPTY_PROFILE: UserProfile = { skills: [], level: "beginner", ways: [] };

export function loadProfile(): UserProfile {
  try {
    const p = JSON.parse(sessionStorage.getItem(KEY) ?? "null");
    // a profile saved before the English rename may carry old values: keep only the current ones
    if (p && Array.isArray(p.skills) && Array.isArray(p.ways))
      return {
        skills: p.skills,
        level: LEVELS.includes(p.level) ? p.level : EMPTY_PROFILE.level,
        ways: p.ways.filter((w: Way) => WAYS.includes(w)),
      };
  } catch {}
  return EMPTY_PROFILE;
}

export function saveProfile(p: UserProfile) {
  try {
    sessionStorage.setItem(KEY, JSON.stringify(p));
  } catch {}
}
