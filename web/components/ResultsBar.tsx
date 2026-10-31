"use client";
// Filtros e ordem da lista de resultados (em cima das portas). Só recortam o que o match já achou.
import { AI_LABELS, PROFILE_LABELS, PROFILE_TONE } from "@/lib/labels";
import type { AiPolicy, Profile, Project } from "@/lib/types";

export type Sort = "match" | "openness" | "newcomer" | "stars";
export type ResultFilter = {
  profiles: Profile[];
  ai: AiPolicy["classification"] | "any";
  newcomerOnly: boolean;
  sort: Sort;
  q: string; // busca no nome, no dono, na descrição e no resumo
};
export const NO_FILTER: ResultFilter = {
  profiles: [],
  ai: "any",
  newcomerOnly: false,
  sort: "match",
  q: "",
};

// minúsculas e sem acento: "traducao" acha "tradução"
const norm = (s: string) =>
  s
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase();

const SORTS: Record<Sort, string> = {
  match: "Melhor combinação",
  openness: "Mais aberto a quem é de fora",
  newcomer: "Mais good first issue / help wanted",
  stars: "Mais estrelas",
};
const SHOWN_PROFILES: Profile[] = [
  "porta_aberta",
  "precisa_de_maos",
  "guardiao",
];

export function applyFilter(list: Project[], f: ResultFilter): Project[] {
  const terms = norm(f.q).split(/\s+/).filter(Boolean);
  const out = list.filter(
    (p) =>
      terms.every((t) =>
        norm(
          `${p.repo} ${p.description ?? ""} ${p.guide?.summary ?? ""}`,
        ).includes(t),
      ) &&
      (f.profiles.length === 0 || f.profiles.includes(p.profile)) &&
      (f.ai === "any" || p.ai_policy.classification === f.ai) &&
      (!f.newcomerOnly || p.newcomer_open > 0),
  );
  if (f.sort === "openness")
    out.sort((a, b) => (b.openness ?? -1) - (a.openness ?? -1));
  if (f.sort === "newcomer")
    out.sort((a, b) => b.newcomer_open - a.newcomer_open);
  if (f.sort === "stars") out.sort((a, b) => b.stars - a.stars);
  return out; // "match": mantém a ordem do rankProjects
}

const chip = (on: boolean) =>
  `flex items-center gap-1.5 rounded-full border px-3 py-1 transition-colors focus-visible:outline focus-visible:outline-2 focus-visible:outline-emerald-600 ${
    on
      ? "border-foreground bg-foreground text-background"
      : "border-line bg-card hover:border-foreground/40"
  }`;

export function SortSelect({
  filter,
  onChange,
}: {
  filter: ResultFilter;
  onChange: (f: ResultFilter) => void;
}) {
  return (
    <label className="flex shrink-0 items-center gap-2 text-sm text-muted">
      Ordenar por
      <select
        id="sort"
        value={filter.sort}
        onChange={(e) => onChange({ ...filter, sort: e.target.value as Sort })}
        className="rounded-full border border-line bg-card px-3 py-1 text-foreground"
      >
        {(Object.keys(SORTS) as Sort[]).map((s) => (
          <option key={s} value={s}>
            {SORTS[s]}
          </option>
        ))}
      </select>
    </label>
  );
}

export default function ResultsBar({
  filter,
  onChange,
  counts,
  newcomerCount,
}: {
  filter: ResultFilter;
  onChange: (f: ResultFilter) => void;
  counts: Record<Profile, number>;
  newcomerCount: number; // quantos da lista têm issue "good first issue"/"help wanted" aberta
}) {
  const toggle = (p: Profile) =>
    onChange({
      ...filter,
      profiles: filter.profiles.includes(p)
        ? filter.profiles.filter((x) => x !== p)
        : [...filter.profiles, p],
    });
  return (
    <div className="space-y-3">
      <input
        id="search"
        type="search"
        value={filter.q}
        onChange={(e) => onChange({ ...filter, q: e.target.value })}
        placeholder="Buscar pelo nome ou pela descrição do projeto"
        aria-label="Buscar projetos"
        className="w-full rounded-full border border-line bg-card px-4 py-2 text-sm placeholder:text-muted focus-visible:outline focus-visible:outline-2 focus-visible:outline-emerald-600"
      />
      <div
        className="flex flex-wrap items-center gap-2 text-[13px]"
        role="group"
        aria-label="Filtrar a lista"
      >
        <span className="mr-1 text-muted">Filtrar:</span>
        {SHOWN_PROFILES.filter((p) => counts[p] > 0).map((p) => (
          <button
            key={p}
            type="button"
            aria-pressed={filter.profiles.includes(p)}
            onClick={() => toggle(p)}
            className={chip(filter.profiles.includes(p))}
          >
            <span className={`h-2 w-2 rounded-full ${PROFILE_TONE[p].dot}`} />
            {PROFILE_LABELS[p].label}
            <span className="tabular-nums opacity-70">{counts[p]}</span>
          </button>
        ))}
        <button
          type="button"
          aria-pressed={filter.newcomerOnly}
          onClick={() =>
            onChange({ ...filter, newcomerOnly: !filter.newcomerOnly })
          }
          className={chip(filter.newcomerOnly)}
          title="Só projetos com issues abertas marcadas como good first issue ou help wanted"
        >
          {filter.newcomerOnly ? "✓ " : ""}Com good first issue
          <span className="tabular-nums opacity-70">{newcomerCount}</span>
        </button>
        <select
          id="ai-filter"
          aria-label="Política de IA"
          value={filter.ai}
          onChange={(e) =>
            onChange({ ...filter, ai: e.target.value as ResultFilter["ai"] })
          }
          className={chip(filter.ai !== "any")}
        >
          <option value="any">Qualquer política de IA</option>
          {(
            ["accepts", "accepts_with_disclosure", "forbids", "silent"] as const
          ).map((c) => (
            <option key={c} value={c}>
              {AI_LABELS[c]!.label}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
}
