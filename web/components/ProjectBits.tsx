// Peças comuns ao card (S2) e à página do projeto (S3): selos, números de saúde e oportunidades.
import { AI_LABELS, PROFILE_LABELS, WAY_LABELS } from "@/lib/labels";
import type { Opportunity, Project } from "@/lib/types";

export function ProfileBadge({ project }: { project: Project }) {
  const p = PROFILE_LABELS[project.profile];
  return (
    <span title={p.hint} className={`inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium ring-1 ring-inset ${p.className}`}>
      {p.label}
    </span>
  );
}

export function AiBadge({ project }: { project: Project }) {
  const a = AI_LABELS[project.ai_policy.classification];
  if (!a) return null;
  const quote = project.ai_policy.evidence ? `"${project.ai_policy.evidence}" (${project.ai_policy.source_file})` : undefined;
  return (
    <span title={quote} className={`text-xs font-medium ${a.className}`}>
      {a.label}
    </span>
  );
}

function fmt(n: number) {
  return n >= 1000 ? `${(n / 1000).toFixed(n >= 10_000 ? 0 : 1).replace(".", ",")} mil` : String(n);
}

export function Stats({ project }: { project: Project }) {
  const items: [string, string][] = [
    ["mantêm (24 meses)", String(project.maintainers_24m)],
    ["PRs aceitos de fora", project.openness === null ? "—" : `${Math.round(project.openness * 100)}%`],
    ["issues para iniciantes", String(project.newcomer_open)],
    ["Scorecard", project.scorecard === null ? "—" : `${project.scorecard.toFixed(1).replace(".", ",")}/10`],
  ];
  if (project.dependents) items.push(["dependentes", fmt(project.dependents)]);
  return (
    <dl className="flex flex-wrap gap-x-5 gap-y-1 text-xs text-zinc-500 dark:text-zinc-400">
      {items.map(([k, v]) => (
        <div key={k} className="flex items-baseline gap-1">
          <dt className="sr-only">{k}</dt>
          <dd className="font-semibold tabular-nums text-zinc-800 dark:text-zinc-200">{v}</dd>
          <span aria-hidden>{k}</span>
        </div>
      ))}
    </dl>
  );
}

export function OpportunityItem({ o }: { o: Opportunity }) {
  return (
    <li className="flex gap-2 text-sm leading-snug">
      <span className="shrink-0 font-medium">{WAY_LABELS[o.way].label}:</span>
      <span className="text-zinc-700 dark:text-zinc-300">
        {o.note}
        {o.source === "gemma" && (
          <span className="ml-1.5 rounded bg-sky-50 px-1 py-px text-[11px] font-medium text-sky-700 dark:bg-sky-950 dark:text-sky-300">sugestão da IA</span>
        )}
        {o.source === "projeto" && <span className="ml-1.5 text-[11px] text-zinc-400">o projeto pede</span>}
      </span>
    </li>
  );
}
