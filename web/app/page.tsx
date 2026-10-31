"use client";
// Home. S1 (filtros) e S2 (lista) entram aqui; hoje mostra só os dados reais para validar o esqueleto.
import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { rankProjects } from "@/lib/match";
import type { Project, UserProfile } from "@/lib/types";

export default function Home() {
  const [projects, setProjects] = useState<Project[] | null>(null);
  // S1 (Pablo): o painel de filtros controla este perfil.
  const [profile] = useState<UserProfile>({ skills: [], level: "iniciante", ways: [] });

  useEffect(() => {
    fetch("/data/projects.json")
      .then((r) => r.json())
      .then(setProjects)
      .catch(() => setProjects([]));
  }, []);

  const ranked = useMemo(() => (projects ? rankProjects(projects, profile) : []), [projects, profile]);

  return (
    <main className="mx-auto max-w-4xl p-6">
      <h1 className="text-3xl font-bold">OpenDoor</h1>
      <p className="mt-2 text-zinc-500">Portas de entrada para contribuir com open source.</p>

      {/* S1: painel de filtros (habilidades, nível, formas de contribuir) */}

      {projects === null ? (
        <p className="mt-6">Carregando…</p>
      ) : (
        <>
          <p className="mt-6 text-sm text-zinc-500">{ranked.length} projetos</p>
          {/* S2: trocar esta lista simples pelos cards */}
          <ul className="mt-2 space-y-1">
            {ranked.slice(0, 30).map((p) => (
              <li key={p.repo}>
                <Link className="underline" href={`/p/${p.repo}`}>
                  {p.repo}
                </Link>{" "}
                <span className="text-sm text-zinc-500">★ {p.stars}</span>
              </li>
            ))}
          </ul>
        </>
      )}
    </main>
  );
}
