"use client";
// "Por onde começar?": mostra na hora o guia salvo do projeto (G1, sem chamar o modelo).
// A versão ao vivo (ExplainBox) fica como opção, e é o caminho quando o projeto ainda não tem guia.
import { useState } from "react";
import { composeGuide } from "@/lib/guide";
import { WAY_LABELS } from "@/lib/labels";
import type { Project, UserProfile } from "@/lib/types";
import ExplainBox from "./ExplainBox";

export default function StartBox({ project, profile, startOpen = false }: { project: Project; profile: UserProfile; startOpen?: boolean }) {
  const [open, setOpen] = useState(startOpen);
  const [live, setLive] = useState(false);

  if (!project.guide) return <ExplainBox repo={project.repo} profile={profile} />;

  if (!open) {
    return (
      <button
        onClick={() => setOpen(true)}
        className="self-start rounded-full bg-foreground px-4 py-2 text-sm font-medium text-background hover:opacity-85 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-emerald-600"
      >
        Por onde começar?
      </button>
    );
  }

  const g = composeGuide(project.guide, profile);
  return (
    <div className="space-y-3">
      <ol className="space-y-2">
        {g.steps.map((s, i) => (
          <li key={s.text} className="grid grid-cols-[1.5rem_1fr] gap-2 text-sm leading-relaxed">
            <span className="mt-0.5 flex h-5 w-5 items-center justify-center rounded-full bg-emerald-600/10 text-xs font-semibold tabular-nums text-emerald-700 dark:text-emerald-400">
              {i + 1}
            </span>
            <span>
              {s.text}
              {s.way && <span className="ml-1.5 text-xs text-muted">· {WAY_LABELS[s.way].label}</span>}
            </span>
          </li>
        ))}
      </ol>
      {g.heads_up && <p className="rounded-md bg-amber-500/10 px-3 py-2 text-sm text-amber-900 dark:text-amber-200">{g.heads_up}</p>}
      <p className="text-xs text-muted">Guia gerado com IA a partir do guia de contribuição e dos dados do projeto. Confira no projeto antes de agir.</p>
      {live ? (
        <ExplainBox repo={project.repo} profile={profile} autoStart />
      ) : (
        <button onClick={() => setLive(true)} className="text-xs font-medium text-emerald-700 underline-offset-2 hover:underline dark:text-emerald-400">
          Personalizar para o meu perfil (leva uns 40 s)
        </button>
      )}
    </div>
  );
}
