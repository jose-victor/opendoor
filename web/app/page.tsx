"use client";
// Home: S1 (filtros, na coluna da esquerda) + S2 (portas). O match roda no navegador (lib/match.ts).
import Image from "next/image";
import { useEffect, useMemo, useState } from "react";
import DoorCard from "@/components/DoorCard";
import FilterPanel from "@/components/FilterPanel";
import ResultsBar, {
  NO_FILTER,
  SortSelect,
  applyFilter,
  type ResultFilter,
} from "@/components/ResultsBar";
import { rankProjects } from "@/lib/match";
import { loadProfile, saveProfile } from "@/lib/profile-store";
import type { Profile, Project, Skill, UserProfile } from "@/lib/types";

const PAGE = 20;

const EXAMPLE: UserProfile = {
  skills: ["javascript", "frontend"],
  level: "iniciante",
  ways: ["documentacao", "testes"],
};

export default function Home() {
  const [projects, setProjects] = useState<Project[] | null>(null);
  const [skills, setSkills] = useState<Skill[]>([]);
  const [profile, setProfile] = useState<UserProfile>(EXAMPLE);
  const [filter, setFilter] = useState<ResultFilter>(NO_FILTER);
  const [shown, setShown] = useState(PAGE);

  useEffect(() => {
    const saved = loadProfile();
    if (saved.skills.length || saved.ways.length) setProfile(saved);
    else saveProfile(EXAMPLE); // a página do projeto usa o mesmo perfil de exemplo
    Promise.all([
      fetch("/data/projects.json").then((r) => r.json()),
      fetch("/data/skills.json").then((r) => r.json()),
    ])
      .then(([p, s]) => {
        setProjects(p);
        setSkills(s);
      })
      .catch(() => setProjects([]));
  }, []);

  function change(p: UserProfile) {
    setProfile(p);
    saveProfile(p);
    setShown(PAGE);
  }

  const languages = useMemo(
    () =>
      new Set(skills.filter((s) => s.kind === "linguagem").map((s) => s.id)),
    [skills],
  );
  const doors = useMemo(
    () => (projects ? rankProjects(projects, profile, languages) : []),
    [projects, profile, languages],
  );
  const total = projects?.filter((p) => p.profile !== "estavel").length ?? 0;
  const list = useMemo(() => applyFilter(doors, filter), [doors, filter]);
  const counts = useMemo(() => {
    const c = {
      porta_aberta: 0,
      precisa_de_maos: 0,
      guardiao: 0,
      estavel: 0,
    } as Record<Profile, number>;
    for (const p of doors) c[p.profile]++;
    return c;
  }, [doors]);

  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-8 sm:px-6 sm:py-12">
      <nav className="mb-12 flex items-center justify-between border-b border-line pb-4">
        <span className="flex items-center gap-3.5">
          <Image src="/logo.svg" alt="" width={56} height={56} className="rounded-xl" priority />
          <span className="text-2xl font-semibold tracking-tight" style={{ fontFamily: "var(--font-unbounded), var(--font-geist-sans), sans-serif" }}>
            OpenDoor
          </span>
        </span>
        <a href="https://github.com/jose-victor/opendoor" className="text-sm text-muted hover:text-foreground">
          Código aberto no GitHub ↗
        </a>
      </nav>

      <header className="mb-12 max-w-5xl space-y-4">
        <h1 className="text-4xl font-semibold leading-[1.05] tracking-tight sm:text-5xl">
          Uma <span className="text-emerald-600 dark:text-emerald-400">Porta Aberta</span> para você contribuir{" "}
          <br className="hidden md:block" />
          no mundo Open Source
        </h1>
        <p className="text-lg leading-relaxed text-foreground/85">
          Quer contribuir pra um projeto Open Source e não sabe como?{" "}
          <br className="hidden sm:block" />
          Descubra quais os projetos ideais para você iniciar nessa jornada!
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
              <div className="flex items-start justify-between gap-3">
                <h2 className="min-w-0 flex-1 pt-1 text-sm text-muted">
                  {doors.length > 0 ? (
                    <>
                      <span className="font-semibold text-foreground">
                        {doors.length === 1
                          ? "1 projeto combina"
                          : `${doors.length} projetos combinam`}{" "}
                        com você
                      </span>
                      , entre {total} que aceitam contribuição
                      {list.length !== doors.length &&
                        ` · ${list.length} com os filtros`}
                    </>
                  ) : (
                    "Nenhum projeto com essa combinação"
                  )}
                </h2>
                {doors.length > 1 && (
                  <SortSelect
                    filter={filter}
                    onChange={(f) => {
                      setFilter(f);
                      setShown(PAGE);
                    }}
                  />
                )}
              </div>
              {doors.length > 0 && (
                <ResultsBar
                  filter={filter}
                  counts={counts}
                  newcomerCount={doors.filter((p) => p.newcomer_open > 0).length}
                  onChange={(f) => {
                    setFilter(f);
                    setShown(PAGE);
                  }}
                />
              )}
              {doors.length === 0 && (
                <p className="rounded-xl border border-dashed border-line p-5 text-sm text-muted">
                  Tente marcar menos linguagens ou outra forma de ajudar. Quem
                  escolhe só documentação, tradução ou triagem não precisa ter
                  uma linguagem em comum com o projeto.
                </p>
              )}
              {doors.length > 0 && list.length === 0 && (
                <p className="rounded-xl border border-dashed border-line p-5 text-sm text-muted">
                  Nenhum projeto com essa busca ou esses filtros. Tente outro termo ou limpe os filtros.
                </p>
              )}
              {list.slice(0, shown).map((p) => (
                <DoorCard key={p.repo} project={p} profile={profile} />
              ))}
              {list.length > shown && (
                <button
                  onClick={() => setShown((n) => n + PAGE)}
                  className="w-full rounded-xl border border-line bg-card py-3 text-sm font-medium hover:bg-foreground/5"
                >
                  Mostrar mais {Math.min(PAGE, list.length - shown)} de{" "}
                  {list.length - shown}
                </button>
              )}
            </>
          )}
        </main>
      </div>

      <footer className="mt-16 border-t border-line pt-5 text-xs text-muted">
        Dados de deps.dev, GitHub e OpenSSF Scorecard. Resumos e guias gerados
        com IA (Gemma 4, um modelo aberto) a partir dos guias de contribuição de
        cada projeto. Código aberto (GPL-3.0) em{" "}
        <a className="underline" href="https://github.com/jose-victor/opendoor">
          github.com/jose-victor/opendoor
        </a>
        .
      </footer>
    </div>
  );
}
