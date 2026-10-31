"use client";
// S3: página do projeto. O que é, por que é uma porta, por onde começar, onde ajudar, política de IA e histórico.
import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { BigNumbers, NewcomerLink, ProfileBand, RecentActivity, ScorecardLink } from "@/components/ProjectBits";
import StartBox from "@/components/StartBox";
import { LEVEL_LABELS, WAY_LABELS } from "@/lib/labels";
import { EMPTY_PROFILE, loadProfile } from "@/lib/profile-store";
import type { Opportunity, Project, UserProfile } from "@/lib/types";

const SOURCE: Record<Opportunity["source"], { label: string; className: string }> = {
  projeto: { label: "o projeto pede", className: "bg-emerald-500/10 text-emerald-700 dark:text-emerald-400" },
  dados: { label: "os números mostram", className: "bg-sky-500/10 text-sky-700 dark:text-sky-400" },
  gemma: { label: "sugestão da IA", className: "bg-violet-500/10 text-violet-700 dark:text-violet-400" },
};

const AI_TONE: Record<Project["ai_policy"]["classification"], { title: string; className: string }> = {
  accepts: { title: "Aceita contribuições feitas com ajuda de IA", className: "border-emerald-500/40 bg-emerald-500/5" },
  accepts_with_disclosure: { title: "Aceita IA, mas pede que você avise quando usar", className: "border-amber-500/40 bg-amber-500/5" },
  forbids: { title: "Não aceita contribuições feitas com IA", className: "border-red-500/40 bg-red-500/5" },
  silent: { title: "O guia de contribuição não fala de IA", className: "border-line" },
  unknown: { title: "Ainda não classificada. Leia o guia de contribuição antes de usar IA.", className: "border-line" },
};

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="space-y-4 rounded-xl border border-line bg-card p-5 sm:p-6">
      <h2 className="text-lg font-semibold">{title}</h2>
      {children}
    </section>
  );
}

function YearsChart({ project }: { project: Project }) {
  const rows = Object.entries(project.years);
  const max = Math.max(1, ...rows.map(([, y]) => y.prs_opened));
  return (
    <figure className="space-y-2">
      <figcaption className="flex flex-wrap gap-4 text-sm text-muted">
        <span>
          <span className="mr-1.5 inline-block h-2.5 w-3 rounded-sm bg-zinc-400/50 align-middle" />
          PRs abertos
        </span>
        <span>
          <span className="mr-1.5 inline-block h-2.5 w-3 rounded-sm bg-emerald-500 align-middle" />
          PRs aceitos
        </span>
      </figcaption>
      <div className="space-y-1.5">
        {rows.map(([year, y]) => (
          <div key={year} className="grid grid-cols-[3rem_1fr_6.5rem] items-center gap-2 text-xs tabular-nums">
            <span className="text-muted">{year === "2026" ? "2026*" : year}</span>
            <div className="relative h-4 rounded-sm bg-foreground/5">
              <div className="absolute inset-y-0 left-0 rounded-sm bg-zinc-400/50" style={{ width: `${(y.prs_opened / max) * 100}%` }} />
              <div className="absolute inset-y-0 left-0 rounded-sm bg-emerald-500" style={{ width: `${(y.prs_merged / max) * 100}%` }} />
            </div>
            <span className="text-right text-muted">
              {y.prs_opened.toLocaleString("pt-BR")} / {y.prs_merged.toLocaleString("pt-BR")}
            </span>
          </div>
        ))}
      </div>
      <p className="text-xs text-muted">* 2026 até setembro (só meses fechados). Dados desde {project.coverage_since}.</p>
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

  if (project === undefined) return <main className="mx-auto max-w-3xl px-4 py-8 text-muted">Carregando…</main>;
  if (project === null)
    return (
      <main className="mx-auto max-w-3xl space-y-3 px-4 py-8">
        <p>O projeto {repo} não está no OpenDoor.</p>
        <Link href="/" className="underline">
          Voltar para as portas
        </Link>
      </main>
    );

  const [owner, name] = project.repo.split("/");
  const policy = project.ai_policy;
  const ai = AI_TONE[policy.classification];

  return (
    <main className="mx-auto w-full max-w-3xl space-y-5 px-4 py-8 sm:py-12">
      <Link href="/" className="text-sm text-muted hover:underline">
        ← Voltar para as portas
      </Link>

      <header className="overflow-hidden rounded-xl border border-line bg-card">
        <ProfileBand project={project} />
        <div className="space-y-5 p-5 sm:p-6">
          <div>
            <h1 className="break-words text-3xl font-semibold leading-tight tracking-tight">{name}</h1>
            <p className="text-sm text-muted">
              {owner} · ★ {project.stars.toLocaleString("pt-BR")} ·{" "}
              <a href={project.url} className="underline underline-offset-2">
                abrir no GitHub
              </a>
            </p>
          </div>
          {project.guide ? (
            <p className="text-lg leading-relaxed">{project.guide.summary}</p>
          ) : (
            project.description && <p className="text-lg leading-relaxed">{project.description}</p>
          )}
          <BigNumbers project={project} full />
          <ScorecardLink project={project} />
        </div>
      </header>

      <Section title="Por onde começar">
        <p className="text-sm text-muted">
          Para quem é {LEVEL_LABELS[profile.level].toLowerCase()}
          {profile.ways.length > 0 && ` e quer ajudar com ${profile.ways.map((w) => WAY_LABELS[w].label.toLowerCase()).join(", ")}`}. Mude o perfil na
          página inicial.
        </p>
        <StartBox project={project} profile={profile} startOpen />
        <NewcomerLink project={project} />
      </Section>

      {project.recent && (
        <Section title="Atividade nos últimos 3 meses">
          <RecentActivity project={project} />
        </Section>
      )}

      <Section title="Onde o projeto precisa de ajuda">
        {project.opportunities.length === 0 ? (
          <p className="text-sm text-muted">O projeto não pede ajuda e os dados não mostram uma necessidade clara.</p>
        ) : (
          <ul className="divide-y divide-line">
            {project.opportunities.map((o) => (
              <li key={o.way + o.note} className="grid gap-1 py-2.5 first:pt-0 last:pb-0 sm:grid-cols-[11rem_1fr] sm:gap-3">
                <span className="text-sm font-semibold">{WAY_LABELS[o.way].label}</span>
                <span className="text-sm leading-relaxed">
                  {o.note}{" "}
                  <span className={`ml-1 whitespace-nowrap rounded-full px-2 py-px text-[11px] font-medium ${SOURCE[o.source].className}`}>{SOURCE[o.source].label}</span>
                </span>
              </li>
            ))}
          </ul>
        )}
      </Section>

      <Section title="Política de IA">
        <div className={`space-y-2 rounded-lg border p-4 ${ai.className}`}>
          <p className="font-medium">{ai.title}</p>
          {policy.evidence && (
            <blockquote className="text-sm italic leading-relaxed text-muted">
              “{policy.evidence}”<span className="ml-2 not-italic">({policy.source_file})</span>
            </blockquote>
          )}
        </div>
      </Section>

      {Object.keys(project.years).length > 0 && (
        <Section title="PRs abertos e aceitos por ano">
          <YearsChart project={project} />
        </Section>
      )}
    </main>
  );
}
