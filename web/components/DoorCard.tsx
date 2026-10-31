"use client";
// S2: uma porta de entrada. Perfil, política de IA, habilidades em comum, saúde, 2 oportunidades e o Gemma.
import Link from "next/link";
import type { Project, Skill, UserProfile } from "@/lib/types";
import ExplainBox from "./ExplainBox";
import { AiBadge, OpportunityItem, ProfileBadge, Stats } from "./ProjectBits";

export default function DoorCard({ project, profile, skills }: { project: Project; profile: UserProfile; skills: Skill[] }) {
  const common = skills.filter((s) => profile.skills.includes(s.id) && project.skills.includes(s.id));
  // primeiro as oportunidades nas formas que a pessoa marcou
  const opps = [...project.opportunities]
    .sort((a, b) => Number(profile.ways.includes(b.way)) - Number(profile.ways.includes(a.way)))
    .slice(0, 2);

  return (
    <article className="space-y-3 rounded-lg border border-zinc-200 bg-white p-4 dark:border-zinc-800 dark:bg-zinc-950 sm:p-5">
      <header className="flex flex-wrap items-center gap-x-3 gap-y-1">
        <Link href={`/p/${project.repo}`} className="min-w-0 break-words text-base font-semibold hover:underline">
          {project.repo}
        </Link>
        <ProfileBadge project={project} />
        <AiBadge project={project} />
        <span className="ml-auto text-xs tabular-nums text-zinc-500">★ {project.stars.toLocaleString("pt-BR")}</span>
      </header>
      {project.description && <p className="text-sm text-zinc-600 dark:text-zinc-400">{project.description}</p>}
      {common.length > 0 && (
        <div className="flex flex-wrap gap-1.5">
          {common.map((s) => (
            <span key={s.id} className="rounded bg-emerald-50 px-1.5 py-0.5 text-xs text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300">
              {s.label}
            </span>
          ))}
        </div>
      )}
      <Stats project={project} />
      {opps.length > 0 && <ul className="space-y-1.5">{opps.map((o) => <OpportunityItem key={o.way} o={o} />)}</ul>}
      <div className="flex flex-col gap-3 pt-1">
        <ExplainBox repo={project.repo} profile={profile} compact />
        <Link href={`/p/${project.repo}`} className="text-sm text-zinc-600 underline-offset-2 hover:underline dark:text-zinc-400">
          Ver o projeto inteiro →
        </Link>
      </div>
    </article>
  );
}
