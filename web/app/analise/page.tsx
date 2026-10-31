// Análise do Ecossistema: tudo calculado no build a partir de projects.json, então acompanha os dados regenerados.
import Link from "next/link";
import type { Metadata } from "next";
import data from "@/public/data/projects.json";
import { AI_LABELS, PROFILE_LABELS, PROFILE_TONE } from "@/lib/labels";
import type { AiPolicy, Profile, Project } from "@/lib/types";

export const metadata: Metadata = { title: "Análise do Ecossistema · OpenDoor" };

const projects = data as Project[];
const fmt = (n: number) => n.toLocaleString("pt-BR");
const pct = (a: number, b: number) => (b ? `${Math.round((100 * a) / b)}%` : "—");

function count<T extends string>(items: T[]): [T, number][] {
  const c = new Map<T, number>();
  for (const i of items) c.set(i, (c.get(i) ?? 0) + 1);
  return [...c].sort((a, b) => b[1] - a[1]);
}

function median(xs: number[]): number {
  const s = [...xs].sort((a, b) => a - b);
  const m = Math.floor(s.length / 2);
  return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2;
}

const ECOS: Record<string, string> = {
  "npm-graph": "npm",
  "pypi-graph": "PyPI",
  "go-graph": "Go",
  "mainstream-app": "Apps mainstream e de IA",
};
const PROFILE_ORDER: Profile[] = ["estavel", "porta_aberta", "guardiao", "precisa_de_maos"];
const CHECKS = [
  { key: "guia", label: "Guia de contribuição", rule: "tem CONTRIBUTING (ou equivalente)" },
  { key: "vivo", label: "Vivo para quem chega", rule: "2 ou mais PRs de gente de fora aceitos nos últimos 3 meses (merges internos e de bots não contam)" },
  { key: "estreias", label: "Estreias", rule: "2 ou mais pessoas tiveram o 1º PR aceito no último ano" },
  { key: "aceite", label: "Aceite de quem é novo", rule: "25% ou mais das pessoas novas que abriram PR tiveram aceito (com pelo menos 5 tentativas)" },
  { key: "resposta", label: "Resposta", rule: "metade dos PRs de fora recebe retorno em até 14 dias e no máximo 25% estão parados" },
] as const;

function Bar({ value, max, label, right, tone = "bg-emerald-500" }: { value: number; max: number; label: React.ReactNode; right: string; tone?: string }) {
  return (
    <div className="grid grid-cols-[minmax(0,10rem)_1fr_auto] items-center gap-3 text-sm">
      <span className="truncate">{label}</span>
      <span className="h-2.5 rounded-full bg-zinc-500/10">
        <span className={`block h-full rounded-full ${tone}`} style={{ width: `${max ? (100 * value) / max : 0}%` }} />
      </span>
      <span className="tabular-nums text-muted">{right}</span>
    </div>
  );
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="space-y-4 rounded-2xl border border-line p-5 sm:p-6">
      <h2 className="text-xl font-semibold">{title}</h2>
      {children}
    </section>
  );
}

export default function Analise() {
  const total = projects.length;
  const ecos = count(projects.flatMap((p) => p.tags).filter((t) => t in ECOS));
  const langs = count(projects.map((p) => p.language ?? "sem linguagem")).slice(0, 8);
  const large = projects.filter((p) => p.collection === "contagem+amostra").length;
  const profiles = count(projects.map((p) => p.profile));
  const open = projects.filter((p) => p.profile !== "estavel");
  const until = projects.find((p) => p.recent)?.recent?.until;

  // PRs por ano, somando todos os projetos
  const years = new Map<string, { opened: number; merged: number }>();
  for (const p of projects)
    for (const [y, v] of Object.entries(p.years ?? {})) {
      const t = years.get(y) ?? { opened: 0, merged: 0 };
      t.opened += v.prs_opened ?? 0;
      t.merged += v.prs_merged ?? 0;
      years.set(y, t);
    }
  const yearRows = [...years].sort();
  const lastYear = yearRows.at(-1)?.[0];
  const maxOpened = Math.max(...yearRows.map(([, v]) => v.opened));

  const critical = projects
    .filter((p) => (p.dependents ?? 0) >= 1000 && p.maintainers_24m !== null && p.maintainers_24m <= 2)
    .sort((a, b) => (b.dependents ?? 0) - (a.dependents ?? 0));
  const openness = projects.map((p) => p.openness).filter((x): x is number => x !== null);
  const scores = projects.map((p) => p.scorecard).filter((x): x is number => x !== null);
  const ai = count(projects.map((p) => (p.ai_policy?.classification ?? "unknown") as AiPolicy["classification"]));
  const withNewcomer = projects.filter((p) => p.newcomer_open > 0);
  const active = projects
    .filter((p) => p.recent)
    .sort((a, b) => b.recent!.prs_merged - a.recent!.prs_merged)
    .slice(0, 10);

  const ready = projects.filter((p) => p.beginner.ready).sort((a, b) => b.stars - a.stars);
  const passes = (p: Project, key: string) => p.beginner.checks.some((c) => c.key === key && c.ok);
  let funnel = open;
  const funnelRows = CHECKS.map((c) => {
    funnel = funnel.filter((p) => passes(p, c.key));
    return { ...c, n: funnel.length };
  });

  return (
    <div className="mx-auto w-full max-w-4xl space-y-8 px-4 py-8 sm:px-6 sm:py-12">
      <Link href="/" className="text-sm text-muted hover:underline">
        ← Voltar para as portas
      </Link>
      <header className="space-y-3">
        <h1 className="text-4xl font-semibold tracking-tight">Análise do Ecossistema</h1>
        <p className="text-lg leading-relaxed text-foreground/85">
          O que os dados de {fmt(total)} projetos open source mostram sobre quem mantém, quem entra e onde há espaço para
          gente nova. Esta página é recalculada sempre que os dados são atualizados.
        </p>
      </header>

      <Section title="O que analisamos">
        <p className="text-sm text-muted">
          Os repositórios dos pacotes mais usados do npm, PyPI e Go (grafo de dependências do deps.dev), mais apps
          mainstream e de IA que vivem no GitHub. Issues, PRs, merges, revisões e commits mês a mês desde 2018-01
          {until ? `, até ${until}` : ""} (só meses fechados), OpenSSF Scorecard e os guias de contribuição.
        </p>
        <div className="space-y-2">
          {ecos.map(([t, n]) => (
            <Bar key={t} label={ECOS[t]} value={n} max={total} right={fmt(n)} />
          ))}
        </div>
        <p className="text-sm text-muted">
          Linguagens: {langs.map(([l, n]) => `${l} (${fmt(n)})`).join(", ")}. {fmt(total - large)} projetos têm coleta
          completa; os {fmt(large)} maiores (mais de 6 mil issues + PRs) têm contagens completas e uma amostra recente de PRs.
        </p>
      </Section>

      <Section title="Perfis">
        <p className="text-sm text-muted">
          Cada projeto ganha um perfil pelos números. {fmt(open.length)} de {fmt(total)} ({pct(open.length, total)}) aceitam
          contribuição de quem é de fora; os outros estão estáveis ou fechados.
        </p>
        <div className="space-y-3">
          {PROFILE_ORDER.map((k) => {
            const n = profiles.find(([p]) => p === k)?.[1] ?? 0;
            return (
              <div key={k} className="space-y-1">
                <Bar label={PROFILE_LABELS[k].label} value={n} max={total} right={fmt(n)} tone={PROFILE_TONE[k].dot} />
                <p className="text-xs text-muted">{PROFILE_LABELS[k].hint}</p>
              </div>
            );
          })}
        </div>
      </Section>

      <Section title="PRs abertos e aceitos por ano">
        <p className="text-sm text-muted">Soma de todos os projetos. A barra clara é o que foi aberto; a escura, o que foi aceito.</p>
        <div className="space-y-2">
          {yearRows.map(([y, v]) => (
            <div key={y} className="grid grid-cols-[3.5rem_1fr_auto] items-center gap-3 text-sm">
              <span className="tabular-nums">{y}{y === lastYear ? "*" : ""}</span>
              <span className="relative h-3 rounded-full bg-zinc-500/10">
                <span className="absolute inset-y-0 left-0 rounded-full bg-emerald-500/30" style={{ width: `${(100 * v.opened) / maxOpened}%` }} />
                <span className="absolute inset-y-0 left-0 rounded-full bg-emerald-600" style={{ width: `${(100 * v.merged) / maxOpened}%` }} />
              </span>
              <span className="tabular-nums text-muted">
                {fmt(v.opened)} / {fmt(v.merged)} · {pct(v.merged, v.opened)} aceitos
              </span>
            </div>
          ))}
        </div>
        <p className="text-xs text-muted">* {lastYear} só até o último mês fechado.</p>
      </Section>

      <Section title="Muita gente depende, poucas pessoas cuidam">
        <p className="text-sm text-muted">
          {fmt(critical.length)} projetos têm 1.000 pacotes dependentes ou mais e no máximo 2 pessoas mantendo nos últimos
          24 meses. Os maiores:
        </p>
        <ul className="space-y-1 text-sm">
          {critical.slice(0, 8).map((p) => (
            <li key={p.repo} className="flex justify-between gap-3">
              <Link href={`/p/${p.repo}`} className="truncate hover:underline">{p.repo}</Link>
              <span className="shrink-0 tabular-nums text-muted">
                {fmt(p.dependents ?? 0)} dependentes · {p.maintainers_24m} {p.maintainers_24m === 1 ? "pessoa" : "pessoas"}
              </span>
            </li>
          ))}
        </ul>
      </Section>

      <Section title="Abertura, segurança e IA">
        <ul className="space-y-2 text-sm">
          <li>
            <b>Abertura:</b> em {fmt(openness.length)} projetos com dados suficientes, a mediana é{" "}
            {Math.round(100 * median(openness))}% dos PRs aceitos vindos de fora; {fmt(openness.filter((x) => x >= 0.5).length)}{" "}
            passam de metade.
          </li>
          <li>
            <b>Segurança:</b> o OpenSSF Scorecard mediano é {median(scores).toLocaleString("pt-BR", { maximumFractionDigits: 1 })} de 10
            ({fmt(scores.length)} projetos avaliados); {fmt(scores.filter((x) => x < 5).length)} ficam abaixo de 5.
          </li>
          <li>
            <b>Para iniciantes:</b> {fmt(withNewcomer.length)} projetos têm issues marcadas como good first issue ou help
            wanted, {fmt(withNewcomer.reduce((s, p) => s + p.newcomer_open, 0))} no total.
          </li>
        </ul>
        <div className="space-y-2">
          <p className="text-sm font-medium">Política de IA no guia de contribuição</p>
          {ai.map(([k, n]) => (
            <Bar key={k} label={AI_LABELS[k]?.label ?? "Ainda não classificado"} value={n} max={total} right={fmt(n)} tone="bg-violet-500" />
          ))}
        </div>
      </Section>

      <Section title="Mais ativos nos últimos 3 meses">
        <div className="space-y-2">
          {active.map((p) => (
            <Bar
              key={p.repo}
              label={<Link href={`/p/${p.repo}`} className="hover:underline">{p.repo}</Link>}
              value={p.recent!.prs_merged}
              max={active[0].recent!.prs_merged}
              right={`${fmt(p.recent!.prs_merged)} PRs aceitos`}
            />
          ))}
        </div>
        <p className="text-xs text-muted">Atividade não é abertura: muitos dos mais ativos aceitam pouco de quem é de fora.</p>
      </Section>

      <Section title={`Prontos para iniciante: ${ready.length}`}>
        <p className="text-sm text-muted">
          Só ganha o selo o projeto em que os dados mostram gente nova conseguindo entrar. As 5 checagens precisam passar:
        </p>
        <ol className="list-decimal space-y-1 pl-5 text-sm">
          {CHECKS.map((c) => (
            <li key={c.key}><b>{c.label}:</b> {c.rule}.</li>
          ))}
        </ol>
        <p className="text-sm text-muted">
          Guardiões ficam de fora (crítico e com 1 ou 2 pessoas cuidando não é lugar para aprender), e os repositórios
          grandes também: só temos uma amostra dos PRs deles, então não dá para contar estreias. Entre os{" "}
          {fmt(open.length)} que aceitam contribuição, quantos passam em cada checagem, uma depois da outra:
        </p>
        <div className="space-y-2">
          {funnelRows.map((r) => (
            <Bar key={r.key} label={r.label} value={r.n} max={open.length} right={fmt(r.n)} />
          ))}
        </div>
        <ul className="grid gap-x-6 gap-y-1 text-sm sm:grid-cols-2">
          {ready.map((p) => (
            <li key={p.repo} className="flex justify-between gap-3">
              <Link href={`/p/${p.repo}`} className="truncate hover:underline">{p.repo}</Link>
              <span className="shrink-0 tabular-nums text-muted">{p.language} · ★ {fmt(p.stars)}</span>
            </li>
          ))}
        </ul>
      </Section>
    </div>
  );
}
