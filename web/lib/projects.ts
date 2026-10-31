// Só para o servidor: os dados entram no bundle da função, então não dependem de buscar arquivo em produção.
import data from "@/public/data/projects.json";
import type { Project } from "./types";

const projects = data as Project[];
const byRepo = new Map(projects.map((p) => [p.repo, p]));

export function getProject(repo: string): Project | undefined {
  return byRepo.get(repo.toLowerCase());
}
