// Server only: the data goes into the function bundle, so it doesn't depend on fetching a file in production.
import data from "@/public/data/projects.json";
import type { Project } from "./types";

const projects = data as Project[];
const byRepo = new Map(projects.map((p) => [p.repo, p]));

export function getProject(repo: string): Project | undefined {
  return byRepo.get(repo.toLowerCase());
}
