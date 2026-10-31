"use client";
// S1: o que a pessoa sabe, o nível e como quer ajudar. O estado é um UserProfile (docs/arquitetura.md).
import { LEVEL_LABELS, WAY_LABELS } from "@/lib/labels";
import { LEVELS, WAYS, type Skill, type UserProfile } from "@/lib/types";

function Chip({ on, onClick, children, title }: { on: boolean; onClick: () => void; children: React.ReactNode; title?: string }) {
  return (
    <button
      type="button"
      aria-pressed={on}
      title={title}
      onClick={onClick}
      className={`rounded-full px-2.5 py-1 text-[13px] transition-colors focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-1 focus-visible:outline-emerald-600 ${
        on ? "bg-emerald-600 text-white" : "border border-line bg-card text-foreground/85 hover:border-foreground/30"
      }`}
    >
      {children}
    </button>
  );
}

function Group({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <fieldset className="space-y-2">
      <legend className="text-sm font-semibold">{label}</legend>
      <div className="flex flex-wrap gap-1.5">{children}</div>
    </fieldset>
  );
}

export default function FilterPanel({ skills, profile, onChange }: { skills: Skill[]; profile: UserProfile; onChange: (p: UserProfile) => void }) {
  const toggle = <T,>(list: T[], v: T) => (list.includes(v) ? list.filter((x) => x !== v) : [...list, v]);
  const chips = (kind: Skill["kind"]) =>
    skills
      .filter((s) => s.kind === kind)
      .map((s) => (
        <Chip key={s.id} on={profile.skills.includes(s.id)} onClick={() => onChange({ ...profile, skills: toggle(profile.skills, s.id) })}>
          {s.label}
        </Chip>
      ));
  const areasOn = skills.filter((s) => s.kind === "area" && profile.skills.includes(s.id)).length;

  return (
    <section aria-label="Seu perfil" className="space-y-5">
      <Group label="Seu nível">
        <div className="flex w-full rounded-full border border-line bg-card p-0.5">
          {LEVELS.map((l) => (
            <button
              key={l}
              type="button"
              aria-pressed={profile.level === l}
              onClick={() => onChange({ ...profile, level: l })}
              className={`flex-1 rounded-full px-2 py-1 text-[13px] focus-visible:outline focus-visible:outline-2 focus-visible:outline-emerald-600 ${
                profile.level === l ? "bg-foreground text-background" : "text-foreground/75 hover:text-foreground"
              }`}
            >
              {LEVEL_LABELS[l]}
            </button>
          ))}
        </div>
      </Group>
      <Group label="Linguagens que você usa">{chips("linguagem")}</Group>
      <details className="group space-y-2" open={areasOn > 0}>
        <summary className="cursor-pointer list-none text-sm font-semibold">
          Áreas de interesse <span className="font-normal text-muted">{areasOn ? `(${areasOn} marcadas)` : "(opcional)"}</span>
          <span className="ml-1 inline-block text-muted transition-transform group-open:rotate-90">›</span>
        </summary>
        <div className="flex flex-wrap gap-1.5 pt-2">{chips("area")}</div>
      </details>
      <Group label="Como quer ajudar">
        {WAYS.map((w) => (
          <Chip key={w} on={profile.ways.includes(w)} title={WAY_LABELS[w].hint} onClick={() => onChange({ ...profile, ways: toggle(profile.ways, w) })}>
            {WAY_LABELS[w].label}
          </Chip>
        ))}
      </Group>
    </section>
  );
}
