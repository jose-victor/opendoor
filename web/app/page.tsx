"use client";
// Home: S1 (filtros, na coluna da esquerda) + S2 (portas). O match roda no navegador (lib/match.ts).
import { useEffect, useMemo, useState } from "react";
import DoorCard from "@/components/DoorCard";
import FilterPanel from "@/components/FilterPanel";
import { rankProjects } from "@/lib/match";
import { loadProfile, saveProfile } from "@/lib/profile-store";
import type { Project, Skill, UserProfile } from "@/lib/types";

const EXAMPLE: UserProfile = { skills: ["javascript", "frontend"], level: "iniciante", ways: ["documentacao", "testes"] };

export default function Home() {
  const [projects, setProjects] = useState<Project[] | null>(null);
  const [skills, setSkills] = useState<Skill[]>([]);
  const [profile, setProfile] = useState<UserProfile>(EXAMPLE);

  useEffect(() => {
    const saved = loadProfile();
    if (saved.skills.length || saved.ways.length) setProfile(saved);
    else saveProfile(EXAMPLE); // a página do projeto usa o mesmo perfil de exemplo
    Promise.all([fetch("/data/projects.json").then((r) => r.json()), fetch("/data/skills.json").then((r) => r.json())])
      .then(([p, s]) => {
        setProjects(p);
        setSkills(s);
      })
      .catch(() => setProjects([]));
  }, []);

  function change(p: UserProfile) {
    setProfile(p);
    saveProfile(p);
  }

  const languages = useMemo(() => new Set(skills.filter((s) => s.kind === "linguagem").map((s) => s.id)), [skills]);
  const doors = useMemo(() => (projects ? rankProjects(projects, profile, languages) : []), [projects, profile, languages]);
  const total = projects?.filter((p) => p.profile !== "estavel").length ?? 0;

  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-8 sm:px-6 sm:py-12">
      <header className="mb-10 max-w-3xl space-y-4">
        <p className="text-sm font-semibold text-emerald-700 dark:text-emerald-400">OpenDoor</p>
        <h1 className="text-4xl font-semibold leading-[1.05] tracking-tight sm:text-5xl">Uma porta de entrada no open source, do seu tamanho.</h1>
        <p className="text-lg leading-relaxed text-muted">
          Conte o que você sabe e como quer ajudar. A gente mostra poucos projetos que precisam exatamente disso e por onde começar:
          primeiro observar e conversar, depois contribuir.
        </p>
      </header>

      <div className="grid gap-8 md:grid-cols-[17rem_1fr] md:gap-10">
        <aside className="md:sticky md:top-6 md:self-start">
          <FilterPanel skills={skills} profile={profile} onChange={change} />
        </aside>

        <main className="min-w-0 space-y-4">
          {projects === null ? (
            <p className="text-muted">Carregando os projetos…</p>
          ) : (
            <>
              <h2 className="text-sm text-muted">
                {doors.length > 0 ? (
                  <>
                    <span className="font-semibold text-foreground">{doors.length === 1 ? "1 porta" : `${doors.length} portas`} para você</span>, entre{" "}
                    {total} projetos que pedem ajuda
                  </>
                ) : (
                  "Nenhuma porta com essa combinação"
                )}
              </h2>
              {doors.length === 0 && (
                <p className="rounded-xl border border-dashed border-line p-5 text-sm text-muted">
                  Tente marcar menos linguagens ou outra forma de ajudar. Quem escolhe só documentação, tradução ou triagem não precisa ter uma
                  linguagem em comum com o projeto.
                </p>
              )}
              {doors.map((p) => (
                <DoorCard key={p.repo} project={p} profile={profile} />
              ))}
            </>
          )}
        </main>
      </div>

      <footer className="mt-16 border-t border-line pt-5 text-xs text-muted">
        Dados de deps.dev, GitHub e OpenSSF Scorecard. Resumos e guias gerados com IA (Gemma 4, um modelo aberto) a partir dos guias de
        contribuição de cada projeto. Código aberto (GPL-3.0) em{" "}
        <a className="underline" href="https://github.com/jose-victor/opendoor">
          github.com/jose-victor/opendoor
        </a>
        .
      </footer>
    </div>
  );
}
