"use client";
// S1: o que a pessoa sabe, o nível e como quer ajudar. O estado é um UserProfile (docs/arquitetura.md).
import { LEVEL_LABELS, WAY_LABELS } from "@/lib/labels";
import { LEVELS, WAYS, type Skill, type UserProfile, type Way } from "@/lib/types";

function Chip({ on, onClick, children, title }: { on: boolean; onClick: () => void; children: React.ReactNode; title?: string }) {
  return (
    <button
      type="button"
      aria-pressed={on}
      title={title}
      onClick={onClick}
      className={`rounded-full border px-3 py-1 text-sm transition-colors focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-1 focus-visible:outline-emerald-600 ${
        on
          ? "border-emerald-600 bg-emerald-600 text-white"
          : "border-zinc-300 bg-white text-zinc-800 hover:border-zinc-400 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-200 dark:hover:border-zinc-500"
      }`}
    >
      {children}
    </button>
  );
}

function Row({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="grid gap-2 sm:grid-cols-[9rem_1fr] sm:items-start">
      <span className="pt-1 text-xs font-semibold uppercase tracking-wide text-zinc-500">{label}</span>
      <div className="flex flex-wrap gap-2">{children}</div>
    </div>
  );
}

export default function FilterPanel({ skills, profile, onChange }: { skills: Skill[]; profile: UserProfile; onChange: (p: UserProfile) => void }) {
  const toggle = <T,>(list: T[], v: T) => (list.includes(v) ? list.filter((x) => x !== v) : [...list, v]);
  const skillChips = (kind: Skill["kind"]) =>
    skills
      .filter((s) => s.kind === kind)
      .map((s) => (
        <Chip key={s.id} on={profile.skills.includes(s.id)} onClick={() => onChange({ ...profile, skills: toggle(profile.skills, s.id) })}>
          {s.label}
        </Chip>
      ));

  return (
    <section aria-label="Seu perfil" className="space-y-4 rounded-lg border border-zinc-200 bg-white p-4 dark:border-zinc-800 dark:bg-zinc-950 sm:p-5">
      <Row label="Linguagens">{skillChips("linguagem")}</Row>
      <Row label="Áreas">{skillChips("area")}</Row>
      <Row label="Nível">
        {LEVELS.map((l) => (
          <Chip key={l} on={profile.level === l} onClick={() => onChange({ ...profile, level: l })}>
            {LEVEL_LABELS[l]}
          </Chip>
        ))}
      </Row>
      <Row label="Como quer ajudar">
        {WAYS.map((w: Way) => (
          <Chip key={w} on={profile.ways.includes(w)} title={WAY_LABELS[w].hint} onClick={() => onChange({ ...profile, ways: toggle(profile.ways, w) })}>
            {WAY_LABELS[w].label}
          </Chip>
        ))}
      </Row>
    </section>
  );
}
