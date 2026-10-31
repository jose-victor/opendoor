"use client";
// S2: uma porta de entrada. O que é o projeto (em pt-BR, do guia), um fato que importa, onde ajudar e por onde começar.
import Link from "next/link";
import { WAY_LABELS } from "@/lib/labels";
import type { Project, UserProfile } from "@/lib/types";
import { AiBadge, ProfileBadge, keyFact } from "./ProjectBits";
import StartBox from "./StartBox";

export default function DoorCard({ project, profile }: { project: Project; profile: UserProfile }) {
  const [owner, name] = project.repo.split("/");
  const about = project.guide?.summary ?? project.description;

  return (
    <article className="flex flex-col gap-4 rounded-xl border border-line bg-card p-5 sm:p-6">
      <header className="flex flex-wrap items-start justify-between gap-x-4 gap-y-2">
        <div className="min-w-0">
          <Link href={`/p/${project.repo}`} className="group block">
            <h3 className="break-words text-xl font-semibold leading-tight group-hover:underline">{name}</h3>
            <span className="text-xs text-muted">{owner}</span>
          </Link>
        </div>
        <div className="flex items-center gap-2">
          <AiBadge project={project} />
          <ProfileBadge project={project} />
        </div>
      </header>

      {about && <p className="max-w-prose text-[15px] leading-relaxed">{about}</p>}

      <p className="text-sm text-muted">{keyFact(project)}</p>

      {project.needs.length > 0 && (
        <div className="flex flex-wrap items-center gap-1.5">
          <span className="mr-1 text-xs text-muted">Onde ajudar:</span>
          {project.needs.map((w) => (
            <span
              key={w}
              className={`rounded-full px-2.5 py-0.5 text-xs ${
                profile.ways.includes(w)
                  ? "bg-emerald-600 text-white"
                  : "border border-line text-foreground/80"
              }`}
            >
              {WAY_LABELS[w].label}
            </span>
          ))}
        </div>
      )}

      <div className="flex flex-col gap-3 border-t border-line pt-4">
        <StartBox project={project} profile={profile} />
        <Link href={`/p/${project.repo}`} className="self-start text-xs text-muted underline-offset-2 hover:underline">
          Ver números, histórico e política de IA →
        </Link>
      </div>
    </article>
  );
}
