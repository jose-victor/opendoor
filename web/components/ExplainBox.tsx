"use client";
// "Por onde começar?": chama o Gemma 4 em /api/explain. Usado no card (S2) e na página do projeto (S3).
import { useEffect, useState } from "react";
import type { ExplainResponse, UserProfile } from "@/lib/types";

// Mesma pergunta não chama o modelo de novo (cada resposta leva de 30 a 45 s).
const cache = new Map<string, ExplainResponse>();

const WAITING = [
  "O Gemma está lendo o guia de contribuição…",
  "Cruzando o seu perfil com o que o projeto precisa…",
  "Montando os primeiros passos…",
  "Quase lá. O Gemma leva de 30 a 45 segundos.",
];

export default function ExplainBox({ repo, profile, compact = false }: { repo: string; profile: UserProfile; compact?: boolean }) {
  const key = JSON.stringify([repo, profile]);
  const [answer, setAnswer] = useState<ExplainResponse | null>(() => cache.get(key) ?? null);
  const [loading, setLoading] = useState(false);
  const [seconds, setSeconds] = useState(0);

  useEffect(() => setAnswer(cache.get(key) ?? null), [key]);
  useEffect(() => {
    if (!loading) return;
    const t = setInterval(() => setSeconds((s) => s + 1), 1000);
    return () => clearInterval(t);
  }, [loading]);

  async function ask() {
    setLoading(true);
    setSeconds(0);
    try {
      const res = await fetch("/api/explain", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ repo, profile }),
      });
      const data: ExplainResponse = await res.json();
      if (data.ok) cache.set(key, data);
      setAnswer(data);
    } catch {
      setAnswer({ ok: false, error: "model_error", message: "Sem conexão com o servidor. Tente de novo." });
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return (
      <div className="flex items-center gap-3 rounded-md border border-dashed border-zinc-300 p-3 text-sm text-zinc-600 dark:border-zinc-700 dark:text-zinc-400" role="status">
        <span className="h-2 w-2 animate-pulse rounded-full bg-emerald-500" />
        <span>{WAITING[Math.min(Math.floor(seconds / 10), WAITING.length - 1)]}</span>
        <span className="ml-auto tabular-nums text-zinc-400">{seconds}s</span>
      </div>
    );
  }

  if (!answer) {
    return (
      <button
        onClick={ask}
        className="w-full self-start rounded-md bg-emerald-600 px-4 py-2 text-sm font-medium text-white hover:bg-emerald-700 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-emerald-600 sm:w-auto"
      >
        Por onde começar?
      </button>
    );
  }

  if (!answer.ok) {
    return (
      <div className="flex flex-wrap items-center gap-3 rounded-md bg-red-50 p-3 text-sm text-red-800 dark:bg-red-950 dark:text-red-300">
        <span>{answer.message}</span>
        <button onClick={ask} className="font-medium underline">
          Tentar de novo
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-3 rounded-md bg-zinc-50 p-4 text-sm dark:bg-zinc-900">
      <p className="leading-relaxed">{answer.why}</p>
      <ol className={`list-decimal space-y-1 pl-5 leading-relaxed ${compact ? "" : "text-[15px]"}`}>
        {answer.first_steps.map((s) => (
          <li key={s}>{s}</li>
        ))}
      </ol>
      {answer.heads_up && (
        <p className="rounded border-l-4 border-amber-500 bg-amber-50 p-2 text-amber-900 dark:bg-amber-950 dark:text-amber-200">{answer.heads_up}</p>
      )}
      <p className="text-xs text-zinc-500">Gerado por {answer.model}. Confira no projeto antes de agir.</p>
    </div>
  );
}
