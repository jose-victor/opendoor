"use client";
// Home: S1 (filtros) + S2 (portas). O match roda no navegador (lib/match.ts).
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
    <main className="mx-auto w-full max-w-4xl space-y-6 px-4 py-8 sm:py-12">
      <header className="space-y-2">
        <h1 className="text-3xl font-bold tracking-tight">OpenDoor</h1>
        <p className="max-w-2xl text-zinc-600 dark:text-zinc-400">
          Diga o que você sabe e como quer ajudar. Mostramos poucas portas de entrada em projetos open source, e o Gemma 4 explica por onde
          começar, com calma: observar e conversar antes de abrir um PR.
        </p>
      </header>

      <FilterPanel skills={skills} profile={profile} onChange={change} />

      {projects === null ? (
        <p className="text-zinc-500">Carregando os projetos…</p>
      ) : (
        <section aria-label="Portas para você" className="space-y-4">
          <h2 className="text-sm text-zinc-500">
            {doors.length > 0 ? (
              <>
                <span className="font-semibold text-zinc-900 dark:text-zinc-100">{doors.length} portas para você</span>, entre {total} projetos que
                pedem ajuda
              </>
            ) : (
              "Nenhuma porta com essa combinação."
            )}
          </h2>
          {doors.length === 0 && (
            <p className="rounded-lg border border-dashed border-zinc-300 p-4 text-sm text-zinc-600 dark:border-zinc-700 dark:text-zinc-400">
              Tente marcar menos linguagens ou outra forma de ajudar. Quem escolhe só documentação, tradução ou triagem não precisa ter uma
              linguagem em comum com o projeto.
            </p>
          )}
          {doors.map((p) => (
            <DoorCard key={p.repo} project={p} profile={profile} skills={skills} />
          ))}
        </section>
      )}

      <footer className="border-t border-zinc-200 pt-4 text-xs text-zinc-500 dark:border-zinc-800">
        Dados de deps.dev, GitHub e OpenSSF Scorecard. Código aberto (GPL-3.0) em{" "}
        <a className="underline" href="https://github.com/jose-victor/opendoor">
          github.com/jose-victor/opendoor
        </a>
        .
      </footer>
    </main>
  );
}
