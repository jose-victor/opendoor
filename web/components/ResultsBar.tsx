"use client";
// Filtros e ordem da lista de resultados (em cima das portas). Só recortam o que o match já achou.
import { AI_LABELS, PROFILE_LABELS, PROFILE_TONE } from "@/lib/labels";
import type { AiPolicy, Profile, Project } from "@/lib/types";

export type Sort = "match" | "openness" | "newcomer" | "stars";
export type ResultFilter = { profiles: Profile[]; ai: AiPolicy["classification"] | "any"; newcomerOnly: boolean; sort: Sort };
export const NO_FILTER: ResultFilter = { profiles: [], ai: "any", newcomerOnly: false, sort: "match" };

const SORTS: Record<Sort, string> = { match: "Melhor combinação", openness: "Mais aberto a quem é de fora", newcomer: "Mais issues para iniciantes", stars: "Mais estrelas" };
const SHOWN_PROFILES: Profile[] = ["porta_aberta", "precisa_de_maos", "guardiao"];

export function applyFilter(list: Project[], f: ResultFilter): Project[] {
  const out = list.filter(
    (p) =>
      (f.profiles.length === 0 || f.profiles.includes(p.profile)) &&
      (f.ai === "any" || p.ai_policy.classification === f.ai) &&
      (!f.newcomerOnly || p.newcomer_open > 0),
  );
  if (f.sort === "openness") out.sort((a, b) => (b.openness ?? -1) - (a.openness ?? -1));
  if (f.sort === "newcomer") out.sort((a, b) => b.newcomer_open - a.newcomer_open);
  if (f.sort === "stars") out.sort((a, b) => b.stars - a.stars);
  return out; // "match": mantém a ordem do rankProjects
}

export default function ResultsBar({ filter, onChange, counts }: { filter: ResultFilter; onChange: (f: ResultFilter) => void; counts: Record<Profile, number> }) {
  const toggle = (p: Profile) => onChange({ ...filter, profiles: filter.profiles.includes(p) ? filter.profiles.filter((x) => x !== p) : [...filter.profiles, p] });
  return (
    <div className="flex flex-wrap items-center gap-2 rounded-xl border border-line bg-card px-3 py-2.5 text-[13px]">
      {SHOWN_PROFILES.map((p) => {
        const on = filter.profiles.includes(p);
        const tone = PROFILE_TONE[p];
        return (
          <button
            key={p}
            type="button"
            aria-pressed={on}
            onClick={() => toggle(p)}
            className={`flex items-center gap-1.5 rounded-full px-2.5 py-1 ${on ? `${tone.soft} ${tone.text} font-semibold ring-1 ring-current/30` : "text-foreground/80 hover:bg-foreground/5"}`}
          >
            <span className={`h-2 w-2 rounded-full ${tone.dot}`} />
            {PROFILE_LABELS[p].label}
            <span className="tabular-nums text-muted">{counts[p]}</span>
          </button>
        );
      })}
      <label className="flex items-center gap-1.5 rounded-full px-2.5 py-1 hover:bg-foreground/5">
        <input id="newcomer-only" type="checkbox" checked={filter.newcomerOnly} onChange={(e) => onChange({ ...filter, newcomerOnly: e.target.checked })} className="accent-emerald-600" />
        Só com issues para iniciantes
      </label>
      <div className="ml-auto flex flex-wrap items-center gap-2">
        <select
          id="ai-filter"
          aria-label="Política de IA"
          value={filter.ai}
          onChange={(e) => onChange({ ...filter, ai: e.target.value as ResultFilter["ai"] })}
          className="rounded-full border border-line bg-card px-2.5 py-1"
        >
          <option value="any">Qualquer política de IA</option>
          {(["accepts", "accepts_with_disclosure", "forbids", "silent"] as const).map((c) => (
            <option key={c} value={c}>
              {AI_LABELS[c]!.label}
            </option>
          ))}
        </select>
        <select
          id="sort"
          aria-label="Ordenar"
          value={filter.sort}
          onChange={(e) => onChange({ ...filter, sort: e.target.value as Sort })}
          className="rounded-full border border-line bg-card px-2.5 py-1"
        >
          {(Object.keys(SORTS) as Sort[]).map((s) => (
            <option key={s} value={s}>
              {SORTS[s]}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
}
