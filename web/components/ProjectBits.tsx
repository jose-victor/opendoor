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
      Ver {project.newcomer_open === 1 ? "a issue" : `as ${project.newcomer_open} issues`} &quot;good first issue&quot; ou &quot;help wanted&quot; no GitHub ↗
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
  const newcomer = p.newcomer_open > 0 ? `${p.newcomer_open} ${p.newcomer_open === 1 ? "issue" : "issues"} good first issue/help wanted` : null;
  const acc = p.acceptance === null ? null : `aceita ${Math.round(p.acceptance * 100)}% dos PRs de fora`;
  const debuts = p.debuts_12m ? `${p.debuts_12m} ${p.debuts_12m === 1 ? "estreia" : "estreias"} no último ano` : null;
  const parts =
    p.profile === "guardiao"
      ? [p.dependents ? `${fmt(p.dependents)} pacotes dependem dele` : null, people]
      : p.profile === "precisa_de_maos"
        ? [`muito trabalho acumulado e ${people}`, acc ?? pct]
        : p.profile === "porta_aberta"
          ? [acc ?? pct, debuts ?? newcomer]
          : [PROFILE_LABELS[p.profile].hint];
  return parts.filter(Boolean).join(" · ");
}

export function ProfileBand({ project }: { project: Project }) {
  const tone = PROFILE_TONE[project.profile];
  // pronto para iniciante vem primeiro: é a promessa mais importante do site, e mostra as provas
  const proof = project.beginner.ready ? project.beginner.checks.filter((c) => c.key === "estreias" || c.key === "aceite").map((c) => c.text) : null;
  return (
    <div className={`flex flex-wrap items-center gap-x-2 gap-y-0.5 px-5 py-2 text-xs sm:px-6 ${tone.soft} ${tone.text}`}>
      <span className={`h-2 w-2 rounded-full ${tone.dot}`} />
      <span className="cursor-help font-semibold underline decoration-dotted underline-offset-2" title={PROFILE_LABELS[project.profile].hint}>
        {PROFILE_LABELS[project.profile].label}
      </span>
      {proof ? (
        <>
          <span className="rounded-full bg-emerald-600 px-2 py-px font-semibold text-white">✓ Pronto para iniciante</span>
          <span className="opacity-90">{proof.join(" · ")}</span>
        </>
      ) : (
        <span className="opacity-90">· {doorReason(project)}</span>
      )}
    </div>
  );
}

// As 4 verificações de "pronto para iniciante", com ✓ ou ✗ e o número de cada uma.
export function BeginnerChecks({ project }: { project: Project }) {
  const b = project.beginner;
  return (
    <div className="space-y-3">
      <p className={`font-medium ${b.ready ? "text-emerald-700 dark:text-emerald-400" : "text-muted"}`}>
        {b.ready
          ? "Sim: os dados mostram que gente nova está conseguindo contribuir aqui."
          : project.profile === "guardiao"
            ? "Não: é um projeto crítico, mantido por 1 ou 2 pessoas. É melhor para quem já tem experiência."
            : "Ainda não dá para garantir. Veja o que falta:"}
      </p>
      <ul className="space-y-1.5">
        {b.checks.map((c) => (
          <li key={c.key} className="flex gap-2 text-sm">
            <span aria-hidden className={c.ok ? "text-emerald-600" : "text-red-500"}>
              {c.ok ? "✓" : "✗"}
            </span>
            <span className={c.ok ? "" : "text-muted"}>{c.text}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

// Números grandes na cor do perfil. "full" mostra todos (página do projeto); senão, os 3 que mais dizem.
export function BigNumbers({ project: p, full = false }: { project: Project; full?: boolean }) {
  const tone = PROFILE_TONE[p.profile];
  const pct = (x: number | null) => (x === null ? "—" : `${Math.round(x * 100)}%`);
  const all: [string, string, boolean][] = [
    [p.dependents ? fmt(p.dependents) : "—", "pacotes dependem dele", p.profile === "guardiao"],
    [pct(p.acceptance), "dos PRs de quem é de fora são aceitos (12 meses)", true],
    [pct(p.openness), "do que entrou no último ano veio de fora", full],
    [String(p.maintainers_24m), p.maintainers_24m === 1 ? "pessoa mantém" : "pessoas mantêm", true],
    [p.debuts_12m === null ? "—" : String(p.debuts_12m), "pessoas novas tiveram o 1º PR aceito no ano", full],
    [String(p.newcomer_open), "issues good first issue / help wanted", p.profile !== "guardiao"],
    [p.scorecard === null ? "—" : `${p.scorecard.toFixed(1).replace(".", ",")}`, "Scorecard de segurança (0 a 10)", false],
  ];
  const items = full ? all.filter(([v]) => v !== "—") : all.filter(([, , show]) => show).slice(0, 3);
  return (
    <dl className={`grid gap-3 ${full ? "grid-cols-2 sm:grid-cols-3" : "grid-cols-3"}`}>
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

// Atividade dos 3 últimos meses fechados: dá para ver se o projeto responde ou se o trabalho acumula.
const MONTHS = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"];
const monthName = (m: string) => `${MONTHS[Number(m.slice(5)) - 1]}/${m.slice(2, 4)}`;

export function RecentActivity({ project, compact = false }: { project: Project; compact?: boolean }) {
  const r = project.recent;
  if (!r) return null;
  const period = `${monthName(r.since)} a ${monthName(r.until)}`;
  if (compact)
    return (
      <p className="text-xs text-muted">
        <span className="font-medium text-foreground/80">Nos últimos 3 meses:</span> {r.issues_opened} issues abertas e {r.issues_closed} fechadas ·{" "}
        {r.prs_opened} PRs abertos e {r.prs_merged} aceitos
      </p>
    );
  const pairs: [string, number, string, number][] = [
    ["issues abertas", r.issues_opened, "fechadas", r.issues_closed],
    ["PRs abertos", r.prs_opened, "aceitos", r.prs_merged],
  ];
  return (
    <div className="space-y-3">
      <p className="text-sm text-muted">De {period}, os meses fechados mais recentes.</p>
      {pairs.map(([a, x, b, y]) => {
        const max = Math.max(1, x, y);
        return (
          <div key={a} className="grid grid-cols-[1fr_auto] items-center gap-x-3 gap-y-1 text-sm">
            <div className="h-2.5 rounded-full bg-zinc-400/50" style={{ width: `${(x / max) * 100}%` }} />
            <span className="tabular-nums">
              <b>{x}</b> {a}
            </span>
            <div className="h-2.5 rounded-full bg-emerald-500" style={{ width: `${(y / max) * 100}%`, minWidth: y ? undefined : "2px" }} />
            <span className="tabular-nums">
              <b>{y}</b> {b}
            </span>
          </div>
        );
      })}
    </div>
  );
}

export function ScorecardLink({ project }: { project: Project }) {
  if (project.scorecard === null) return null;
  return (
    <a
      href={`https://scorecard.dev/viewer/?uri=github.com/${project.repo}`}
      target="_blank"
      rel="noreferrer"
      className="text-sm text-muted underline underline-offset-2 hover:text-foreground"
    >
      Ver o relatório completo do OpenSSF Scorecard ↗
    </a>
  );
}
