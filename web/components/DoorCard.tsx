"use client";
// S2: uma porta de entrada. O que é o projeto (em pt-BR, do guia salvo), 3 números, onde ajudar e por onde começar.
import Link from "next/link";
import { WAY_LABELS } from "@/lib/labels";
import type { Project, UserProfile } from "@/lib/types";
import { AiBadge, BigNumbers, NewcomerLink, ProfileBand, RecentActivity } from "./ProjectBits";
import StartBox from "./StartBox";

export default function DoorCard({ project, profile }: { project: Project; profile: UserProfile }) {
  const [owner, name] = project.repo.split("/");
  const about = project.guide?.summary ?? project.description;

  return (
    <article className="overflow-hidden rounded-xl border border-line bg-card">
      <ProfileBand project={project} />

      <div className="flex flex-col gap-4 p-5 sm:p-6">
        <header className="flex flex-wrap items-start justify-between gap-x-4 gap-y-1">
          <Link href={`/p/${project.repo}`} target="_blank" rel="noreferrer" className="group min-w-0">
            <h3 className="break-words text-xl font-semibold leading-tight group-hover:underline">{name}</h3>
            <span className="text-xs text-muted">
              {owner} · ★ {project.stars.toLocaleString("pt-BR")}
            </span>
          </Link>
          <AiBadge project={project} />
        </header>

        {about && <p className="max-w-prose text-[15px] leading-relaxed">{about}</p>}

        <BigNumbers project={project} />
        <RecentActivity project={project} compact />

        {project.needs.length > 0 && (
          <div className="flex flex-wrap items-center gap-1.5">
            <span className="mr-1 text-xs text-muted" title="Em verde, as formas de ajudar que você marcou e que o projeto precisa">
              Onde ajudar{profile.ways.some((w) => project.needs.includes(w)) ? " (em verde, o que você marcou)" : ""}:
            </span>
            {[...project.needs].sort((a, b) => Number(profile.ways.includes(b)) - Number(profile.ways.includes(a))).map((w) => (
              <span
                key={w}
                className={`rounded-full px-2.5 py-0.5 text-xs ${profile.ways.includes(w) ? "bg-emerald-600 text-white" : "border border-line text-foreground/80"}`}
              >
                {WAY_LABELS[w].label}
              </span>
            ))}
          </div>
        )}

        <div className="flex flex-col gap-3 border-t border-line pt-4">
          <StartBox project={project} profile={profile} />
          <NewcomerLink project={project} />
          <Link href={`/p/${project.repo}`} target="_blank" rel="noreferrer" className="self-start text-xs text-muted underline-offset-2 hover:underline">
            Ver histórico, todas as oportunidades e política de IA →
          </Link>
        </div>
      </div>
    </article>
  );
}
