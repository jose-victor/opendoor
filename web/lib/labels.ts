// Rótulos do site (tabela "Formas de contribuir" em docs/arquitetura.md). Os ids vêm de lib/types.ts.
import type { AiPolicy, Level, Profile, Way } from "./types";

export const LEVEL_LABELS: Record<Level, string> = {
  iniciante: "Iniciante",
  intermediario: "Intermediário",
  experiente: "Experiente",
};

export const WAY_LABELS: Record<Way, { label: string; hint: string }> = {
  codigo: { label: "Código", hint: "correções e funcionalidades pequenas, de preferência good first issues" },
  triagem: { label: "Triagem e suporte", hint: "reproduzir bugs relatados, achar duplicadas, responder dúvidas" },
  revisao: { label: "Revisão de PRs", hint: "rodar o PR, reproduzir o bug e validar o fix" },
  refinamento: { label: "Refinamento de issues", hint: "passos de reprodução e critério de pronto" },
  documentacao: { label: "Documentação", hint: "docs, exemplos e tutoriais" },
  traducao: { label: "Tradução", hint: "tradução e localização" },
  seguranca: { label: "Segurança", hint: "dependências, alertas e práticas do OpenSSF Scorecard" },
  testes: { label: "Testes e observabilidade", hint: "regressão, cobertura, logs e métricas" },
};

// Cores por papel: verde = porta aberta, âmbar = precisa de mãos, roxo = guardião.
export const PROFILE_LABELS: Record<Profile, { label: string; hint: string; className: string }> = {
  porta_aberta: {
    label: "Porta aberta",
    hint: "recebe bem quem é de fora: boa parte do que entra vem de fora e PRs de fora costumam ser aceitos",
    className: "bg-emerald-50 text-emerald-800 ring-emerald-600/20 dark:bg-emerald-950 dark:text-emerald-300 dark:ring-emerald-400/30",
  },
  precisa_de_maos: {
    label: "Precisa de mãos",
    hint: "sobrecarregado: muito trabalho para 1 a 3 pessoas; triagem e revisão aliviam quem mantém",
    className: "bg-amber-50 text-amber-800 ring-amber-600/20 dark:bg-amber-950 dark:text-amber-300 dark:ring-amber-400/30",
  },
  guardiao: {
    label: "Guardião",
    hint: "muita gente depende, 1 ou 2 pessoas cuidam",
    className: "bg-violet-50 text-violet-800 ring-violet-600/20 dark:bg-violet-950 dark:text-violet-300 dark:ring-violet-400/30",
  },
  estavel: {
    label: "Estável",
    hint: "hoje aceita pouco de quem é de fora, ou está parado",
    className: "bg-zinc-100 text-zinc-700 ring-zinc-500/20 dark:bg-zinc-800 dark:text-zinc-300 dark:ring-zinc-400/30",
  },
};

// Cor de cada perfil, usada no selo, nos números e na faixa do card.
export const PROFILE_TONE: Record<Profile, { text: string; soft: string; dot: string }> = {
  porta_aberta: { text: "text-emerald-700 dark:text-emerald-400", soft: "bg-emerald-500/10", dot: "bg-emerald-500" },
  precisa_de_maos: { text: "text-amber-700 dark:text-amber-400", soft: "bg-amber-500/10", dot: "bg-amber-500" },
  guardiao: { text: "text-violet-700 dark:text-violet-400", soft: "bg-violet-500/10", dot: "bg-violet-500" },
  estavel: { text: "text-zinc-600 dark:text-zinc-400", soft: "bg-zinc-500/10", dot: "bg-zinc-400" },
};

export const AI_LABELS: Record<AiPolicy["classification"], { label: string; className: string } | null> = {
  accepts: { label: "Aceita IA", className: "text-emerald-700 dark:text-emerald-400" },
  accepts_with_disclosure: { label: "IA com aviso", className: "text-amber-700 dark:text-amber-400" },
  forbids: { label: "Proíbe IA", className: "text-red-700 dark:text-red-400" },
  silent: { label: "Sem regra de IA", className: "text-zinc-500" },
  unknown: null, // ainda não classificado: não mostra nada
};
