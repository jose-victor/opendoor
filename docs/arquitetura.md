# Arquitetura e contratos

Este arquivo é o **contrato entre as frentes**. Se você precisa mudar algo aqui, avise o time antes, porque outra pessoa depende disso.

## Visão geral
```
PIPELINE (Python, roda antes, na máquina de alguém)          SITE (Next.js na Vercel)
pipeline/collect.py ──> data/ecosystem.db                    web/
                             │                                ├─ app/page.tsx          home + filtros + resultados
   pipeline/classify_ai_policy.py (Gemma) ──> ai_policy       ├─ app/p/[...repo]/      página do projeto
   pipeline/skills.py ──> project_skills                      ├─ app/api/explain/      Gemma ao vivo (servidor)
                             │                                ├─ lib/types.ts          tipos deste contrato
pipeline/build.py ──> web/public/data/projects.json ─────────>├─ lib/match.ts          ranking no navegador
                      web/public/data/skills.json  ─────────> └─ lib/gemma.ts          cliente Gemini API (só servidor)
```
- **Os dados dos projetos são estáticos.** São gerados pelo pipeline e versionados em `web/public/data/`.
- **O match roda no navegador**, em cima do `projects.json`.
- **Só o `/api/explain` chama o modelo ao vivo.** A chave fica na Vercel, nunca no navegador.
- **Fora de hoje:** Supabase, quando vierem o cadastro de projetos e os perfis salvos.

## `web/public/data/skills.json`: vocabulário fixo dos filtros
```ts
type Skill = {
  id: string;           // "react", "typescript", "docs", "testes"...
  label: string;        // "React"
  kind: "linguagem" | "framework" | "ferramenta" | "area";  // area = não é código: docs, tradução, design, segurança...
};
```
Nenhuma outra parte inventa ids: tudo referencia este arquivo.

## `web/public/data/projects.json`: lista de `Project`
```ts
type Profile = "guardiao" | "porta_aberta" | "precisa_de_maos" | "estavel";
type AiPolicy = {
  classification: "accepts" | "accepts_with_disclosure" | "forbids" | "silent" | "unknown";
  evidence: string;      // frase literal do arquivo, "" se silent/unknown
  source_file: string;
};
type YearStats = {
  prs_opened: number; prs_merged: number; issues_opened: number; issues_closed: number;
  commits: number;
  direct_commits: number | null;  // null em repos grandes
  people: number | null;          // pessoas distintas (não-bot) no ano; null em repos grandes
};
// Formas de contribuir (docs/visao.md). Mesma lista para o projeto (o que precisa) e para a pessoa (o que quer fazer).
type Way = "codigo" | "triagem" | "revisao" | "refinamento" | "documentacao" | "traducao" | "seguranca" | "testes";
type Project = {
  repo: string;               // "debug-js/debug" (minúsculas)
  needs: Way[];               // formas de ajuda que o projeto mais precisa, da mais para a menos urgente
  url: string;                // "https://github.com/debug-js/debug"
  tags: ("npm-graph" | "mainstream-app")[];
  description: string | null;
  language: string | null;
  license: string | null;
  stars: number;
  dependents: number | null;  // só npm-graph
  profile: Profile;
  skills: string[];           // ids de skills.json
  openness: number | null;    // 0..1, fatia de PRs aceitos de quem não é mantenedor (12 meses); null = poucos dados
  maintainers_24m: number;    // pessoas que fizeram merge ou commit direto (24 meses, não-bot)
  newcomer_open: number;      // issues abertas para iniciantes
  scorecard: number | null;   // OpenSSF 0..10
  ai_policy: AiPolicy;
  collection: "completo" | "contagem+amostra";  // grandes: contagens mensais completas + amostra de pessoas (12 meses)
  coverage_since: string;     // "2018-01" ou mês a partir do qual os dados estão completos
  years: Record<string, YearStats>;  // "2018".."2026"
};
```

## `POST /api/explain`
Entrada (o navegador manda **só o repo e o perfil**; o servidor busca o projeto no `projects.json` e não confia em dados de projeto vindos do cliente):
```ts
type UserProfile = {
  skills: string[];                                       // ids de skills.json
  level: "iniciante" | "intermediario" | "experiente";
  ways: Way[];                                            // como a pessoa quer ajudar; vazio = qualquer forma
};
type ExplainRequest = { repo: string; profile: UserProfile };
```
Saída:
```ts
type ExplainResponse =
  | { ok: true; why: string; first_steps: string[]; heads_up: string | null; model: string }
  | { ok: false; error: "rate_limited" | "not_found" | "bad_request" | "model_error"; message: string };
```
- `why`: 2–3 frases, em português, sobre por que o projeto combina com o perfil.
- `first_steps`: de 3 a 5 passos concretos, seguindo a filosofia de `docs/visao.md`: começam por observar o projeto (roadmap, issues, discussões) e conversar com a comunidade; para iniciantes, a primeira contribuição sugerida é de testes, docs ou triagem. Nunca "abra um PR" como primeiro passo.
- `heads_up`: um alerta, por exemplo a política de IA do projeto ou "mantido por 1 pessoa, seja paciente".
- Com erro, o site mostra a `message` e continua funcionando.

## Variáveis de ambiente (`.env.example`)
| Nome | Onde | Para quê |
|---|---|---|
| `GEMINI_API_KEY` | Vercel e pipeline | Gemini API (Gemma 4) |
| `GEMMA_MODEL` | Vercel e pipeline | padrão `gemma-4-26b-a4b-it` |
| `LLM_BACKEND` | pipeline | `gemini` ou `ollama` (local) |
| `OLLAMA_MODEL` | pipeline | ex.: `gemma4:e4b` |

## Regras de ranking (`web/lib/match.ts`)
Implementação do José. Resumo para quem consome:
- **Formas de contribuir:** se a pessoa marcou formas (`ways`), o projeto precisa ter pelo menos uma delas em `needs`. Formas que não são código (triagem, docs, tradução) **não exigem** habilidade técnica em comum.
- **Habilidades:** pontua quantas habilidades marcadas o projeto tem.
- **Nível:** iniciante favorece `porta_aberta` com `newcomer_open > 0`; experiente favorece `guardiao` e `precisa_de_maos`.
- **Exclusões:** `estavel` não aparece.
- **Empate:** desempata por `openness`.
