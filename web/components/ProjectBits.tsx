// Peças comuns ao card (S2) e à página do projeto (S3): selo de IA, faixa do perfil e números.
import { AI_LABELS, PROFILE_LABELS, PROFILE_TONE } from "@/lib/labels";
import type { Project } from "@/lib/types";

export function AiBadge({ project }: { project: Project }) {
  const a = AI_LABELS[project.ai_policy.classification];
  if (!a) return null;
  const quote = project.ai_policy.evidence ? `"${project.ai_policy.evidence}" (${project.ai_policy.source_file})` : undefined;
  return (
    <span title={quote} className={`rounded-full border border-current/25 px-2 py-0.5 text-xs font-medium ${a.className}`}>
      {a.label}
    </span>
  );
}

// Mesmos labels que a coleta conta (NEWCOMER_LABELS em pipeline/collect.py); na busca do GitHub, a vírgula é "ou".
const NEWCOMER_LABELS = ["good first issue", "good-first-issue", "first-timers-only", "beginner", "easy", "help wanted"];

export function NewcomerLink({ project }: { project: Project }) {
  if (project.newcomer_open <= 0) return null;
  const q = `is:issue is:open label:${NEWCOMER_LABELS.map((l) => `"${l}"`).join(",")}`;
  return (
    <a
      href={`${project.url}/issues?q=${encodeURIComponent(q)}`}
      target="_blank"
      rel="noreferrer"
      className="self-start text-sm font-medium text-emerald-700 underline-offset-2 hover:underline dark:text-emerald-400"
    >
      Ver {project.newcomer_open === 1 ? "a issue marcada" : `as ${project.newcomer_open} issues marcadas`} para iniciantes no GitHub ↗
    </a>
  );
}

export function fmt(n: number) {
  return n >= 1000 ? `${(n / 1000).toFixed(n >= 10_000 ? 0 : 1).replace(".", ",")} mil` : String(n);
}

// Por que esta porta: o número que explica o perfil, em uma frase.
export function doorReason(p: Project): string {
  const pct = p.openness === null ? null : `${Math.round(p.openness * 100)}% dos PRs aceitos vêm de fora`;
  const people = p.maintainers_24m === 1 ? "1 pessoa mantém" : `${p.maintainers_24m} pessoas mantêm`;
  const newcomer = p.newcomer_open > 0 ? (p.newcomer_open === 1 ? "1 issue para iniciantes" : `${p.newcomer_open} issues para iniciantes`) : null;
  const parts =
    p.profile === "guardiao"
      ? [p.dependents ? `${fmt(p.dependents)} pacotes dependem dele` : null, people]
      : p.profile === "precisa_de_maos"
        ? [`muito trabalho acumulado e ${people}`, pct]
        : p.profile === "porta_aberta"
          ? [pct, newcomer]
          : [PROFILE_LABELS[p.profile].hint];
  return parts.filter(Boolean).join(" · ");
}

export function ProfileBand({ project }: { project: Project }) {
  const tone = PROFILE_TONE[project.profile];
  return (
    <div className={`flex flex-wrap items-center gap-x-2 gap-y-0.5 px-5 py-2 text-xs sm:px-6 ${tone.soft} ${tone.text}`}>
      <span className={`h-2 w-2 rounded-full ${tone.dot}`} />
      <span className="font-semibold">{PROFILE_LABELS[project.profile].label}</span>
      <span className="opacity-90">· {doorReason(project)}</span>
    </div>
  );
}

// Números grandes na cor do perfil. "full" mostra todos (página do projeto); senão, os 3 que mais dizem.
export function BigNumbers({ project: p, full = false }: { project: Project; full?: boolean }) {
  const tone = PROFILE_TONE[p.profile];
  const all: [string, string, boolean][] = [
    [p.dependents ? fmt(p.dependents) : "—", "pacotes dependem dele", p.profile === "guardiao"],
    [p.openness === null ? "—" : `${Math.round(p.openness * 100)}%`, "dos PRs aceitos vêm de fora", true],
    [String(p.maintainers_24m), p.maintainers_24m === 1 ? "pessoa mantém" : "pessoas mantêm", true],
    [String(p.newcomer_open), "issues para iniciantes", p.profile !== "guardiao"],
    [p.scorecard === null ? "—" : `${p.scorecard.toFixed(1).replace(".", ",")}`, "Scorecard de segurança (0 a 10)", false],
  ];
  const items = full ? all.filter(([v]) => v !== "—") : all.filter(([, , show]) => show).slice(0, 3);
  return (
    <dl className={`grid gap-3 ${full ? "grid-cols-2 sm:grid-cols-5" : "grid-cols-3"}`}>
      {items.map(([value, what]) => (
        <div key={what} className="min-w-0">
          <dt className="sr-only">{what}</dt>
          <dd className={`font-display text-2xl font-semibold tabular-nums leading-none ${tone.text}`}>{value}</dd>
          <span className="mt-1 block text-xs leading-snug text-muted">{what}</span>
        </div>
      ))}
    </dl>
  );
}
