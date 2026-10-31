"use client";
// "Por onde começar?": tudo vem pronto e salvo (G1). O guia do projeto, gerado antes, é combinado com o
// perfil sem chamar modelo nenhum. Sem guia salvo, os passos saem das oportunidades.
import { useState } from "react";
import { aiPolicyNote, composeGuide, guideFor } from "@/lib/guide";
import { WAY_LABELS } from "@/lib/labels";
import type { Project, UserProfile } from "@/lib/types";

export default function StartBox({ project, profile, startOpen = false }: { project: Project; profile: UserProfile; startOpen?: boolean }) {
  const [open, setOpen] = useState(startOpen);

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

  const g = composeGuide(guideFor(project), profile);
  const alerts = [aiPolicyNote(project), g.heads_up].filter(Boolean) as string[];
  return (
    <div className="space-y-3">
      <ol className="space-y-2">
        {g.steps.map((s, i) => (
          <li key={s.text} className="grid grid-cols-[1.5rem_1fr] gap-2 text-sm leading-relaxed">
            <span className="mt-0.5 flex h-5 w-5 items-center justify-center rounded-full bg-emerald-600/15 text-xs font-semibold tabular-nums text-emerald-700 dark:text-emerald-400">
              {i + 1}
            </span>
            <span>
              {s.text}
              {s.way && <span className="ml-1.5 text-xs text-muted">· {WAY_LABELS[s.way].label}</span>}
            </span>
          </li>
        ))}
      </ol>
      {alerts.map((a) => (
        <p key={a} className="rounded-md bg-amber-500/10 px-3 py-2 text-sm text-amber-900 dark:text-amber-200">
          {a}
        </p>
      ))}
      <p className="text-xs text-muted">
        {project.guide ? "Guia gerado com IA a partir do guia de contribuição e dos dados do projeto." : "Passos montados a partir dos dados do projeto."} Confira no
        projeto antes de agir.
      </p>
    </div>
  );
}
