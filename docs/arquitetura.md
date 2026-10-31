# Arquitetura e contratos

Este arquivo é o **contrato entre as frentes**. Se você precisa mudar algo aqui, avise o time antes, porque outra pessoa depende disso.

## Visão geral
```
PIPELINE (Python, roda antes, na máquina de alguém)          SITE (Next.js na Vercel)
pipeline/collect.py ──> data/ecosystem.db                    web/
                             │                                ├─ app/page.tsx          home + filtros + resultados
   pipeline/classify_ai_policy.py (Gemma) ──> ai_policy       ├─ app/p/[...repo]/      página do projeto
   pipeline/skills.py ──> (build.py)                          ├─ app/api/explain/      Gemma ao vivo (servidor)
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
  id: string;           // "typescript", "frontend", "ia", "testes"...
  label: string;        // "Frontend web"
  kind: "linguagem" | "framework" | "ferramenta" | "area";  // area = não é código: docs, tradução, design, segurança...
};
```
Nenhuma outra parte inventa ids: tudo referencia este arquivo.

**Só linguagens e áreas chegam aqui** (hoje 20: 8 linguagens e 12 áreas). Um projeto conta com **todas as linguagens que têm 10% ou mais do código**, não só a principal (o OBS é C e C++). O `pipeline/skills.py` detecta 62 habilidades finas, mas cada framework ou ferramenta tem um `parent` e conta como a área-mãe (React vira `frontend`, Flask vira `backend`, PyTorch vira `ia`). Além disso, o `build.py` só publica a habilidade que aparece em **5 projetos ou mais**, para nenhum filtro devolver vazio. Por isso C#, Java e Kotlin ficam de fora por enquanto. O `Project.skills` usa os mesmos ids.

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
  needs: Way[];               // formas de ajuda, na ordem de opportunities (sem repetir)
  opportunities: Opportunity[]; // por que precisa de cada forma; ver "Oportunidades (D5)" abaixo
  guide: Guide | null;        // guia "por onde começar" salvo; ver "Guia por projeto (G1)" abaixo
  url: string;                // "https://github.com/debug-js/debug"
  tags: ("npm-graph" | "pypi-graph" | "go-graph" | "mainstream-app")[];  // de qual grafo veio, ou app da lista à mão
  description: string | null;
  language: string | null;
  license: string | null;
  stars: number;
  dependents: number | null;  // pacotes que dependem dele; null em apps mainstream (não vêm de grafo)
  profile: Profile;
  skills: string[];           // ids de skills.json
  openness: number | null;    // 0..1, do que entrou em 12 meses (PRs aceitos + commits diretos), a fatia de quem é de fora; null = poucos dados
  maintainers_24m: number;    // pessoas que fizeram merge, ou 3+ commits diretos, em 24 meses (sem bots)
  recent: Recent | null;      // issues e PRs dos 3 últimos meses fechados
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
- **Implementação** (`lib/gemma.ts`, A1/A2, Anna):
  - usa o SDK `@google/genai` e o modelo `GEMMA_MODEL` (padrão `gemma-4-26b-a4b-it`);
  - **não usa `responseSchema`**, porque ele trava com o Gemma 4;
  - timeout de 60 s;
  - o prompt recebe o perfil, as `opportunities` e a política de IA do projeto;
  - uma resposta fora do formato vira `model_error`, nunca um texto inventado;
  - cada resposta leva de 30 a 45 s, então o site mostra um estado de carregamento.
  A avaliação de 3 perfis × 3 projetos está em `eval/explain.md`.
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
| `OLLAMA_URL` | pipeline | padrão `http://localhost:11434` |

O cliente do pipeline (`pipeline/llm.py`) lê o `.env` da raiz e roda com `python pipeline/llm.py "seu prompt"`. O backend padrão é `gemini`; para o Gemma local, use `LLM_BACKEND=ollama`.

## Como o `build.py` calcula o perfil (D3)
Em ordem de prioridade (`profile_of` em `pipeline/build.py`):
1. **`guardiao`:** 100 mil dependentes ou mais, e 1 ou 2 pessoas fizeram merge ou commit direto em 24 meses.
2. **`porta_aberta`:** `openness` de 0,25 ou mais (ou de 0,1 ou mais com issues "good first issue"/"help wanted") **e** taxa de aceite (`acceptance`) de 0,2 ou mais, quando conhecida. Também entra quem está **pronto para iniciante** (ver abaixo), mesmo com a abertura baixa por causa de muitos commits do mantenedor (caso do postcss).
3. **`precisa_de_maos`:** 30 issues abertas ou mais, de 1 a 3 mantenedores ativos, 10% ou mais do que entra vindo de fora, taxa de aceite de 0,2 ou mais (quando conhecida) **e pelo menos 1 PR aceito nos 3 últimos meses**. A auditoria de 31/10 mostrou que 9 de 19 "precisa de mãos" não aceitavam nenhum PR havia 3 meses: eram becos, não portas.
4. **`estavel`:** o resto, incluindo pacotes sem nenhum mantenedor ativo em 24 meses.

**Pronto para iniciante (`beginner`)** é a promessa mais importante do site, então é a mais exigente. As 4 verificações precisam passar (`beginner_checks` no `build.py`), e cada uma vai para o JSON com o texto da prova:
1. **Estreias:** 2 ou mais pessoas de fora tiveram o **primeiro** PR aceito nos últimos 12 meses (`debuts_12m`).
2. **Aceite de gente nova (por pessoa):** das pessoas que abriram PR em 12 meses e nunca tinham tido um aceito antes, 25% ou mais conseguiram (precisa de pelo menos 5 pessoas novas). Exemplo: redux, 24 de 28. Contar por pessoa, e só gente nova, evita dois enganos: um colaborador antigo sem permissão de merge inflava a taxa (no sharp-libvips, o kleisauke tinha 29 de 29), e um bot com nome de gente (`github-actions`) também.
3. **Vivo:** 3 ou mais PRs aceitos nos 3 últimos meses fechados.
4. **Guia:** existe um CONTRIBUTING.

Repos grandes não passam: deles só temos uma amostra recente de PRs, e não dá para saber quem estreou. Em 31/10 eram 44 projetos prontos. E porta aberta exige pelo menos 1 estreia no ano quando sabemos as estreias: se ninguém novo entrou em 12 meses, a porta não está aberta para quem chega.

**Bots:** além de `is_bot`, ficam de fora os logins que terminam em `bot` e uma lista de bots conhecidos com nome de gente (`github-actions`, `dependabot`, `renovate`, `pre-commit-ci`, `mergify`, `allcontributors`, `copilot`...).

**Taxa de aceite (`acceptance`)**: dos PRs que gente de fora abriu em 12 meses, a fatia aceita, com mínimo de 5 PRs de fora. A "abertura" diz de onde veio o que entrou; a taxa de aceite diz a chance de um PR de fora entrar. O Flask tem abertura 0,11 e aceita 4%; o Express tem 0,52 e aceita 8%; o Tornado aceita 30%.

**Quem é de dentro e de fora:**
- **Mantenedor (de dentro):** quem fez merge de um PR em 24 meses, ou fez 3 ou mais commits diretos na branch principal. Um commit isolado não conta, porque o commit de terceiro aplicado à mão fica no nome do autor. Bots ficam de fora, inclusive os com nome de gente, como `antfubot` (filtro `login NOT LIKE '%bot'`).
- **`openness`:** do que entrou no projeto em 12 meses (PRs aceitos + commits diretos de quem mantém), a fatia que veio de quem é de fora. Precisa de 5 mudanças ou mais; abaixo disso é `null`. Antes contava só PRs, e o sharp aparecia com 100% de fora; contando os 177 commits diretos do mantenedor, são 17%.
- **Repos grandes:** usam a mesma regra sobre a amostra de PRs aceitos (quem fez merge é de dentro). O `authorAssociation` do GitHub só entra quando não há essa participação, porque quem participa da organização de forma privada aparece como `CONTRIBUTOR`. No Mastodon, isso dava 100% de fora, e o certo é 25%. Se o `authorAssociation` dá 95% ou mais de fora, o valor vira `null` (era o caso do Tailwind).
- **Cobertura:** sem os commits diretos coletados (`commit_coverage`), a abertura de um repo completo vira `null`, porque sairia inflada (o csstree aparecia com 100%, e o real é ~33%). Nos grandes cuja participação cobre menos de 12 meses, abertura e mantenedores vêm da amostra (`repo_sample`).
- **Duplicatas:** repos que mudaram de dono (`facebook/react` → `react/react`) aparecem uma vez só, com o nome atual.
- **`recent`:** soma de `repo_monthly` nos 3 últimos meses fechados. Exemplo: o debug teve 18 PRs abertos e nenhum aceito de julho a setembro.

Distribuição em 31/10 às 14h, com a coleta da rodada 3 ainda rodando: 580 estáveis, 168 guardiões, 199 portas abertas e 14 que precisam de mãos.

## Formas de contribuir (`Way`): rótulo sugerido e o que inclui
| id | Rótulo no site | Inclui |
|---|---|---|
| `codigo` | Código | correções e funcionalidades pequenas, de preferência issues "good first issue" |
| `triagem` | Triagem e suporte | reproduzir bugs relatados, pedir informações, achar duplicadas, responder dúvidas da comunidade |
| `revisao` | Revisão de PRs | rodar o PR localmente, reproduzir o bug e validar se o fix resolve |
| `refinamento` | Refinamento de issues | issues vagas viram issues com passos de reprodução e critério de pronto |
| `documentacao` | Documentação | docs, exemplos, tutoriais |
| `traducao` | Tradução | tradução e localização |
| `seguranca` | Segurança | dependências e alertas, práticas do OpenSSF Scorecard, auditoria |
| `testes` | Testes e observabilidade | testes de regressão, cobertura, logs, métricas, tracing |

O prompt do Gemma (`pipeline/opportunities.py`) usa essas mesmas descrições. Acessibilidade, design/UX, empacotamento e performance ficaram para depois de hoje, porque mudariam o contrato.

## Guia por projeto (G1): `guide`
```ts
type Guide = {
  summary: string;                               // o que é o projeto e onde precisa de ajuda, em pt-BR
  common_steps: string[];                        // observar e conversar
  steps_by_way: Partial<Record<Way, string[]>>;  // 2 ou 3 passos por forma de ajuda (só as de needs)
  heads_up: string | null;
};
```
- **Geração, uma vez por projeto:** `pipeline/guides.py` faz o modelo (Gemma 4) ler o guia de contribuição ou o README, as oportunidades, os números e a política de IA. A resposta fica em `project_guides`. Rode o script **depois** do `classify_ai_policy.py`, para o alerta citar a política.
- **No site, sem modelo:** `web/lib/guide.ts` (`composeGuide`) junta os passos comuns com os passos de até 2 formas de ajuda:
  - as que a pessoa marcou;
  - se ela não marcou nenhuma e é iniciante, testes, docs e triagem primeiro;
  - senão, as do projeto.
  É determinístico: mesma entrada, mesma saída, e responde na hora.
- **Nada é gerado na hora.** O site não chama o modelo. Um projeto sem guia salvo recebe passos montados a partir das `opportunities` (`guideFor`). O alerta de política de IA vem do dado classificado, com a citação (`aiPolicyNote`). A rota `/api/explain` continua disponível para quem quiser a explicação ao vivo, mas a interface não a usa (decisão do grupo).
- **No site, o conteúdo da IA é sinalizado** ("gerado com IA", "sugestão da IA"), sem propaganda do modelo. O OpenDoor é para a comunidade, e o modelo é um meio.

## Oportunidades (D5): `needs` e `opportunities`
```ts
type Opportunity = { way: Way; source: "projeto" | "dados" | "gemma"; note: string };
```
Cada projeto lista as formas de ajuda e o motivo (`note`, em pt-BR), nesta ordem:
1. **`projeto`:** o guia de contribuição **menciona** documentação, tradução, testes ou revisão (é uma regex; a interface diz "o guia menciona", não "o projeto pede"), ou há issues com "good first issue"/"help wanted". A tradução sai quando o guia diz que não aceita ("we do not merge … translations", caso do tdesktop). Só procuramos palavras no texto, nunca seguimos instruções dele.
2. **`dados`:** os números mostram:
   - `codigo`: 10% ou mais dos PRs aceitos vêm de fora;
   - `triagem`: 100 issues abertas ou mais, ou 30 ou mais com até 3 mantenedores;
   - `revisao`: 20 PRs abertos ou mais (nota: rodar, reproduzir o bug e validar o fix);
   - `seguranca`: guardião ou Scorecard abaixo de 5.
3. **`gemma`:** sugestão do Gemma 4, gerada **offline** por `pipeline/opportunities.py`. Ele lê o guia de contribuição ou o README e os números, e só sugere formas que ainda não estão na lista. O resultado fica em cache em `repo_opportunities`. **No site, mostrar como "sugestão da IA", não como fato.**

Todo projeto que aparece no match (perfil diferente de `estavel`) tem pelo menos uma oportunidade.

## Regras de ranking (`web/lib/match.ts`)
`rankProjects(projects, profile, languageIds)` devolve **todos os projetos que se enquadram**, do que mais combina para o que menos combina. Isso foi uma decisão do grupo: antes eram no máximo 5. Na home, uma busca (nome, dono, descrição e resumo, sem diferenciar acentos) e uma barra filtram a lista por perfil, política de IA e "good first issue / help wanted"; dá para ordenar por combinação, abertura, issues para iniciantes ou estrelas (`components/ResultsBar.tsx`). A lista mostra 20 projetos por vez. O `languageIds` são os ids de `skills.json` com `kind: "linguagem"`; o S1 já carrega esse arquivo e passa o conjunto.
- **Exclusões:**
  - `estavel` nunca aparece;
  - `guardiao` não aparece para iniciante;
  - para iniciante, só projetos **prontos para iniciante** (`beginner.ready`; ver acima);
  - `needs` só tem o que o guia menciona ou os números mostram; as sugestões do Gemma aparecem na página, mas não colocam o projeto no filtro de formas de ajuda;
  - se a pessoa marcou formas (`ways`), o projeto precisa ter pelo menos uma delas em `needs`;
  - se a pessoa marcou habilidades, o projeto precisa ter pelo menos uma em comum;
  - se ela marcou linguagens, o projeto precisa usar uma delas.
- **Exceção:** quem marcou só formas que não são código (triagem, refinamento, documentação, tradução) **não precisa** ter habilidade nem linguagem em comum.
- **Pontuação:**
  - 5 por habilidade em comum;
  - bônus do nível: iniciante favorece `porta_aberta`, mais 2 se `newcomer_open > 0`; intermediário favorece `precisa_de_maos`; experiente favorece `guardiao`;
  - mais 1 por forma de contribuir em comum.
- **Empate:** desempata por estreias no último ano, depois pela taxa de aceite e depois pelas estrelas. A abertura sozinha engana em projeto de uma pessoa só.
