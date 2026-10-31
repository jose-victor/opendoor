"use client";
// S3: página do projeto. Tudo do card, mais todas as oportunidades, a política de IA com a citação e o histórico.
import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import ExplainBox from "@/components/ExplainBox";
import { AiBadge, OpportunityItem, ProfileBadge, Stats } from "@/components/ProjectBits";
import { AI_LABELS, LEVEL_LABELS, PROFILE_LABELS, WAY_LABELS } from "@/lib/labels";
import { EMPTY_PROFILE, loadProfile } from "@/lib/profile-store";
import type { Project, UserProfile } from "@/lib/types";

function YearsChart({ project }: { project: Project }) {
  const rows = Object.entries(project.years);
  const max = Math.max(1, ...rows.map(([, y]) => y.prs_opened));
  return (
    <figure className="space-y-2">
      <figcaption className="text-sm text-zinc-600 dark:text-zinc-400">
        PRs abertos <span className="inline-block h-2 w-3 rounded-sm bg-zinc-300 align-middle dark:bg-zinc-600" /> e aceitos{" "}
        <span className="inline-block h-2 w-3 rounded-sm bg-emerald-600 align-middle" /> por ano
      </figcaption>
      <div className="space-y-1">
        {rows.map(([year, y]) => (
          <div key={year} className="grid grid-cols-[3rem_1fr_7.5rem] items-center gap-2 text-xs tabular-nums">
            <span className="text-zinc-500">{year === "2026" ? "2026*" : year}</span>
            <div className="relative h-4 rounded-sm bg-zinc-100 dark:bg-zinc-900">
              <div className="absolute inset-y-0 left-0 rounded-sm bg-zinc-300 dark:bg-zinc-600" style={{ width: `${(y.prs_opened / max) * 100}%` }} />
              <div className="absolute inset-y-0 left-0 rounded-sm bg-emerald-600" style={{ width: `${(y.prs_merged / max) * 100}%` }} />
            </div>
            <span className="text-right text-zinc-600 dark:text-zinc-400">
              {y.prs_opened.toLocaleString("pt-BR")} / {y.prs_merged.toLocaleString("pt-BR")}
            </span>
          </div>
        ))}
      </div>
      <p className="text-xs text-zinc-500">* 2026 até setembro (só meses fechados). Dados desde {project.coverage_since}.</p>
    </figure>
  );
}

export default function ProjectView() {
  const params = useParams<{ repo: string[] }>();
  const repo = params.repo.map(decodeURIComponent).join("/").toLowerCase();
  const [project, setProject] = useState<Project | null | undefined>(undefined);
  const [profile, setProfile] = useState<UserProfile>(EMPTY_PROFILE);

  useEffect(() => {
    setProfile(loadProfile());
    fetch("/data/projects.json")
      .then((r) => r.json())
      .then((all: Project[]) => setProject(all.find((p) => p.repo === repo) ?? null))
      .catch(() => setProject(null));
  }, [repo]);

  if (project === undefined) return <main className="mx-auto max-w-3xl px-4 py-8">Carregando…</main>;
  if (project === null)
    return (
      <main className="mx-auto max-w-3xl space-y-3 px-4 py-8">
        <p>O projeto {repo} não está no OpenDoor.</p>
        <Link href="/" className="underline">
          Voltar para as portas
        </Link>
      </main>
    );

  const policy = project.ai_policy;
  const ai = AI_LABELS[policy.classification];

  return (
    <main className="mx-auto w-full max-w-3xl space-y-8 px-4 py-8 sm:py-12">
      <Link href="/" className="text-sm text-zinc-600 hover:underline dark:text-zinc-400">
        ← Voltar para as portas
      </Link>

      <header className="space-y-3">
        <div className="flex flex-wrap items-center gap-x-3 gap-y-1">
          <h1 className="min-w-0 break-words text-2xl font-bold tracking-tight">{project.repo}</h1>
          <ProfileBadge project={project} />
          <AiBadge project={project} />
        </div>
        {project.description && <p className="text-zinc-600 dark:text-zinc-400">{project.description}</p>}
        <p className="text-sm text-zinc-600 dark:text-zinc-400">
          {PROFILE_LABELS[project.profile].label}: {PROFILE_LABELS[project.profile].hint}.{" "}
          <a href={project.url} className="underline">
            Abrir no GitHub
          </a>
        </p>
        <Stats project={project} />
      </header>

      <section className="space-y-3">
        <h2 className="text-lg font-semibold">Por onde começar</h2>
        <p className="text-sm text-zinc-500">
          Para o perfil {LEVEL_LABELS[profile.level].toLowerCase()}
          {profile.skills.length > 0 && ` em ${profile.skills.join(", ")}`}
          {profile.ways.length > 0 && `, ajudando com ${profile.ways.map((w) => WAY_LABELS[w].label.toLowerCase()).join(", ")}`}. Mude o perfil na
          página inicial.
        </p>
        <ExplainBox repo={project.repo} profile={profile} />
      </section>

      <section className="space-y-3">
        <h2 className="text-lg font-semibold">Onde o projeto precisa de ajuda</h2>
        {project.opportunities.length === 0 ? (
          <p className="text-sm text-zinc-500">O projeto não pede ajuda e os dados não mostram uma necessidade clara.</p>
        ) : (
          <ul className="space-y-2">
            {project.opportunities.map((o) => (
              <OpportunityItem key={o.way + o.note} o={o} />
            ))}
          </ul>
        )}
      </section>

      <section className="space-y-2">
        <h2 className="text-lg font-semibold">Política de IA</h2>
        {ai ? (
          <>
            <p className={`text-sm font-medium ${ai.className}`}>{ai.label}</p>
            {policy.evidence && (
              <blockquote className="border-l-4 border-zinc-300 pl-3 text-sm italic text-zinc-700 dark:border-zinc-700 dark:text-zinc-300">
                “{policy.evidence}”
                <footer className="mt-1 text-xs not-italic text-zinc-500">{policy.source_file}</footer>
              </blockquote>
            )}
          </>
        ) : (
          <p className="text-sm text-zinc-500">Ainda não classificada. Leia o CONTRIBUTING do projeto antes de usar IA.</p>
        )}
      </section>

      {Object.keys(project.years).length > 0 && (
        <section className="space-y-3">
          <h2 className="text-lg font-semibold">Atividade</h2>
          <YearsChart project={project} />
        </section>
      )}
    </main>
  );
}
