"use client";
// S3 (Kaiky): página do projeto. Hoje mostra o básico e testa o /api/explain de ponta a ponta.
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import type { ExplainResponse, Project } from "@/lib/types";

export default function ProjectView() {
  const params = useParams<{ repo: string[] }>();
  const repo = params.repo.join("/").toLowerCase();
  const [project, setProject] = useState<Project | null | undefined>(undefined);
  const [answer, setAnswer] = useState<ExplainResponse | null>(null);

  useEffect(() => {
    fetch("/data/projects.json")
      .then((r) => r.json())
      .then((all: Project[]) => setProject(all.find((p) => p.repo === repo) ?? null));
  }, [repo]);

  async function askGemma() {
    // S3: usar o perfil que a pessoa marcou nos filtros (S1).
    const res = await fetch("/api/explain", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ repo, profile: { skills: [], level: "iniciante", ways: [] } }),
    });
    setAnswer(await res.json());
  }

  if (project === undefined) return <main className="p-6">Carregando…</main>;
  if (project === null) return <main className="p-6">Projeto não encontrado.</main>;

  return (
    <main className="mx-auto max-w-3xl p-6">
      <h1 className="text-2xl font-bold">
        <a className="underline" href={project.url}>
          {project.repo}
        </a>
      </h1>
      <p className="mt-2">{project.description}</p>
      {/* S3: gráfico por ano (project.years), perfil, política de IA com evidência */}
      <button className="mt-6 rounded bg-black px-4 py-2 text-white" onClick={askGemma}>
        Como eu começo aqui?
      </button>
      {answer && (
        <pre className="mt-4 whitespace-pre-wrap rounded bg-zinc-100 p-4 text-sm text-black">
          {JSON.stringify(answer, null, 2)}
        </pre>
      )}
    </main>
  );
}
