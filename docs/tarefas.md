# Tarefas

Cada tarefa abaixo vira **uma issue**. Fluxo em `CONTRIBUTING.md`: atribuir a issue a si mesmo, comentar "comecei", trabalhar numa branch, abrir o PR com `Closes #N`. Contratos (formatos, tipos, API) em `docs/arquitetura.md`. **Siga o contrato; não invente formato.**

Nomes são sugestão. Tamanho: P (até 30 min), M (até 1h).

Prazo: **congelar às 16h**, submeter às **16h30**.

## Ordem
```
Fase 0 (esqueleto, bloqueia o site)   E1 ─ E2 ─ E3
Em paralelo desde já                  K1 → K2 → K3 (depende de P1)
                                      P1 (gabarito)
                                      A1 → A2 → A3 (A2 depende de E1)
Depois do esqueleto                   D1 → D2 → D3 → D5 → D4
Dados (em paralelo)                   D6 (repos grandes), D7 (PyPI, Go, web e IA)
                                      S1, S2, S3 → I1 (integração)
```

---

## Fase 0: Esqueleto — José

### E1. Criar `web/` e publicar na Vercel (M) — ✅ PR #23, no ar em https://opendoor-fawn.vercel.app
- ✅ Vercel conectada ao GitHub (pasta raiz `web/`): a `main` faz deploy sozinha e **cada PR ganha um preview**. `GEMINI_API_KEY` e `GEMMA_MODEL` configuradas.
- Next.js (App Router, TypeScript), com as pastas e arquivos vazios de `docs/arquitetura.md`. `lib/types.ts` com os tipos do contrato.
- Projeto na Vercel ligado ao repositório. `GEMINI_API_KEY` configurada lá.
- **Pronto quando:** a URL da Vercel abre uma página e `npm run build` passa.

### E2. `build.py` v0 com dados reais (M) — ✅ PR #23
- Gera `web/public/data/projects.json` a partir do banco, já no formato do contrato. Campos ainda não calculados vêm com valor neutro: `skills: []`, `profile: "precisa_de_maos"`, `ai_policy.classification: "unknown"`.
- Gera um `skills.json` inicial.
- **Pronto quando:** o JSON tem todos os projetos e passa na checagem de tipos do site.

### E3. Stub de `/api/explain` (P) — ✅ PR #23
- A rota valida a entrada e devolve uma resposta **fixa** no formato do contrato. Assim o site pode ser construído sem esperar o Gemma.
- **Pronto quando:** `curl -X POST /api/explain -d '{"repo":"debug-js/debug","profile":{"skills":["javascript"],"level":"iniciante"}}'` devolve `ok: true`.

---

## Dados — José

### D1. Vocabulário de habilidades (P) — ✅ PR #33
- `pipeline/skills.py`: lista de ~40 habilidades (`id`, `label`, `kind`) e, para cada uma, as regras de detecção: nomes de dependências npm, linguagens do GitHub, *topics*.
- Feito: 62 habilidades (15 linguagens, 20 frameworks, 9 ferramentas, 18 áreas, incluindo IA/ML e dados). As regras de dependência valem para npm, PyPI e Go; `skills.detect(language, topics, deps, texto)` já está pronta para a D2. Selftest: `python pipeline/skills.py`.
- **Pronto quando:** `skills.json` é gerado a partir dessa lista.

### D2. Habilidades de cada projeto (M)
- Detectar pelas dependências (já coletadas), pela linguagem e pelos *topics* (nova coleta, barata). Grava `project_skills(repo, skill, source)`.
- ✅ Feito (PR #33): etapa `collect.py topics` (`repo_topics`) e detecção no `build.py` (sem tabela `project_skills`: é recalculada a cada build). Após a conversa sobre a UX, o site mostra só **19 filtros** (linguagens e áreas, com 5+ projetos cada; ver `docs/arquitetura.md`). Resultado: 99,7% dos projetos com 1+ habilidade e 64% com 2+. Os outros são bibliotecas utilitárias minúsculas, em que a linguagem é a resposta honesta. Depois, cada projeto passou a contar com todas as linguagens que têm 10% ou mais do código, e 212 projetos ficaram com 2 linguagens ou mais. O critério de 90% com 2+ era para o vocabulário fino e foi trocado por "todo filtro tem 5+ projetos".
- **Pronto quando:** pelo menos 90% dos projetos têm 2 ou mais habilidades.

### D3. Perfil e métricas (M) — ✅ PR da #6
- Calcular `profile`, `openness`, `maintainers_24m` e `years` no `build.py`, com as regras de `docs/visao.md`. Teste com assert em 3 projetos conhecidos.
- **Pronto quando:** `debug-js/debug` sai como `guardiao` e algum projeto com PRs de fora sai como `porta_aberta`.
- Feito: as regras estão em `docs/arquitetura.md` e os asserts rodam com `python pipeline/build.py`. O debug sai guardião; Express, React, VS Code, Godot e llama.cpp saem porta aberta.

### D6. Repos grandes: contagem + amostra (M) — issue #25, PR #24 ✅ coleta dos 104 grandes concluída (os dados entram no PR de dados finais)
- Repos com mais de 6 mil issues + PRs (53) ganham contagens mensais completas desde 2018 pela busca, mais uma amostra de até 300 PRs aceitos dos últimos 12 meses (abertura e quem faz merge). Etapa `collect.py large`.
- **Atenção, A1 e S3:** nesses repos, `years[ano].people` e `direct_commits` são `null`.

### D7. Novos ecossistemas: PyPI e Go, mais web e IA (M) — issue #27 ✅ código (PR #28); ⏳ dados em coleta
- `collect.py --system npm|pypi|go`. Sementes de web (React, TypeScript, Tailwind...), dados e IA (pandas, transformers, LangChain, Ollama...). Apps de IA no GitHub (Ollama, llama.cpp, Open WebUI, ComfyUI).
- Go e alguns pacotes npm não têm árvore resolvida no deps.dev: o grafo desce 2 níveis pelas dependências declaradas.

### D5. Formas de contribuir por projeto (`needs`) (M) — ✅ PR da #22
- Calcular `needs` com os sinais de `docs/visao.md`: issues sem label nem resposta → triagem; PRs abertos esperando revisão → revisão; Scorecard baixo / guardião → segurança; label ou arquivos de docs/i18n → documentação/tradução. Pode precisar de uma coleta extra, barata: labels das issues abertas e PRs abertos sem revisão.
- **Pronto quando:** todo projeto tem pelo menos uma forma em `needs`, e a ordem faz sentido em 5 projetos conferidos à mão.
- Feito, em duas camadas (ideia do José). (1) O que o guia de contribuição pede (fonte `projeto`), mais os sinais dos números (fonte `dados`), no `build.py`. (2) Sugestões do Gemma 4 para o que o projeto não lista (fonte `gemma`), offline, com `pipeline/opportunities.py`. Campo novo no contrato: `opportunities`. Todo projeto que aparece no match (não estável) tem pelo menos uma oportunidade. Conferidos à mão: express, debug, vscode, godot, obs.

### D4. `match.ts` (M) — ✅ PR da #7 (regras em `docs/arquitetura.md`)
- Ranking no navegador (regras em `docs/arquitetura.md`), mais um teste com 3 perfis.
- **Pronto quando:** o teste passa.

---

## Gemma offline (pipeline) — Kaiky

### K1. Cliente do Gemma no pipeline (P) — ✅ PR #29
- Trazer o `llm.py` do esqueleto do Kaiky para `pipeline/llm.py`, com caminhos baseados em `Path(__file__)` e configuração vinda das variáveis de `docs/arquitetura.md`.
- **Pronto quando:** `python pipeline/llm.py "responda só OK"` responde, com `LLM_BACKEND=gemini`. Ollama é plano B.

### K2. Classificador de política de IA (M) — ✅ PR #40 (Kaiky; revisão do Claude)
- Trazer o `classify_ai_policy.py` do Kaiky. **Ler os textos da tabela `repo_files`**, sem baixar de novo. Gravar `ai_policy(repo, classification, evidence, source_file, model, classified_at)`.
- Manter: o filtro por regex antes de chamar o modelo e o descarte quando a evidência não está no texto.
- O texto dos arquivos é dado de terceiros: o prompt precisa dizer que é conteúdo a analisar, não instruções.
- **Pronto quando:** a tabela está preenchida para todos os repositórios e o script imprime a contagem por categoria.
- Feito. Na revisão entraram:
  - `try` por repo: um erro do modelo não derruba a rodada, e o repo fica para a próxima execução;
  - 3 threads;
  - extração do JSON com regex;
  - comparação da evidência ignorando Markdown (o OBS agora sai `forbids`);
  - `llm.py` corrigido pelo #37.
- 157 repos passam do filtro e vão ao modelo. Teste: Godot, OBS, acorn, Prettier, yargs, FreeCAD e llama.cpp batem com o gabarito.

### K3. Acurácia contra o gabarito (P) — depende de P1
- `pipeline/evaluate.py` lê `eval/gabarito.csv` e compara com a tabela `ai_policy`.
- **Pronto quando:** imprime "acertou X de Y" e o número vai para o README.

---

## Gemma ao vivo (site) — Anna

### A1. `web/lib/gemma.ts` (M) — ✅ PR #41 (Anna; revisão do Claude)
- ⚠️ Gemma 4 pela API: use só as partes **sem** `thought: true` (o raciocínio vem junto); não use `thinkingLevel: "minimal"` (erro 500); cada chamada leva de 10 a 15 s.
- Função `explain(project: Project, profile: UserProfile): Promise<ExplainResponse>`, que chama a Gemini API com o modelo `GEMMA_MODEL` (SDK `@google/genai`).
- O prompt em português usa **só** os dados do `Project` (habilidades, perfil, política de IA com a evidência, issues para iniciantes, mantenedores) e pede JSON no formato `why` / `first_steps` / `heads_up`.
- Dá para começar antes do E1, num arquivo solto testado com `npx tsx`.
- **Pronto quando:** roda com 1 projeto de exemplo e devolve o formato do contrato.

### A2. Ligar `/api/explain` ao Gemma (P) — ✅ PR #41
- Trocar a resposta fixa do stub pela `explain()`. Buscar o projeto no `projects.json` pelo `repo`.
- Erros: 429 da API vira `rate_limited`; repo desconhecido vira `not_found`; resposta fora do formato vira `model_error`.
- **Pronto quando:** o `curl` do E3 devolve um texto real e um repo inexistente devolve `not_found`.

### A3. Qualidade das respostas (P) — ✅ `eval/explain.md` (9 de 9 válidas, nenhuma começa por PR)
- Testar 3 perfis (iniciante em JS, experiente em segurança, alguém de docs) em 3 projetos (um guardião, um porta aberta, um app mainstream). Ajustar o prompt.
- **Pronto quando:** as 9 respostas estão coladas na issue e nenhuma inventa algo que não está nos dados.

---

## Site (telas) — Pablo / Kaiky (depois do K2)
Todas dependem do E1 e usam o `projects.json` do E2.

### S1. Painel de filtros (M) — ✅ feito em grupo (José, Anna, Kaiky, Pablo e Claude)
- Checkboxes das habilidades de `skills.json`, agrupadas por `kind`, a escolha de nível e **as formas de contribuir** (código, triagem, revisão, documentação, tradução, segurança...). O estado vira um `UserProfile`.
- **Pronto quando:** marcar e desmarcar atualiza o `UserProfile`.

### S2. Lista de resultados (M) — ✅ feito em grupo
- Cards com repo, descrição, perfil (selo), habilidades em comum, política de IA e issues para iniciantes. A ordem vem do `match.ts` (D4); até ele ficar pronto, ordene por estrelas.
- **Pronto quando:** filtrar por React mostra só projetos com React.

### S3. Página do projeto `/p/dono/nome` (M) — ✅ feito em grupo
- Dados do projeto, gráfico simples por ano (PRs, issues, pessoas), política de IA com a evidência citada, e o botão "Como eu começo aqui?", que chama `/api/explain` com o perfil atual.
- **Pronto quando:** o botão mostra a resposta do stub (E3) e depois a real (A2).
- **Como ficou:**
  - Uma página só, com filtros em chips (Linguagens, Áreas, Nível, Como quer ajudar) e de 3 a 5 portas embaixo.
  - O card mostra perfil, política de IA, habilidades em comum, números de saúde e 2 oportunidades (a "sugestão da IA" marcada).
  - O botão "Por onde começar?" chama o Gemma ali mesmo, com carregamento e contador, e guarda a resposta para não repetir a chamada.
  - A página do projeto traz todas as oportunidades, a política de IA com a citação, o gráfico de PRs abertos contra aceitos por ano e a mesma caixa do Gemma.
  - O perfil marcado na home vale na página do projeto (`sessionStorage`).
  - Na revisão em grupo (José, Anna, Kaiky e Pablo), a home virou duas colunas: filtros à esquerda e portas à direita. O card ficou mais leve: resumo em pt-BR do guia, uma frase com o número que explica o perfil e "onde ajudar" em etiquetas. O site não faz propaganda do modelo. Na segunda rodada:
    - a faixa colorida do card diz **por que** a porta apareceu;
    - entraram 3 números grandes na cor do perfil;
    - a página do projeto foi reorganizada em seções;
    - surgiu um link para as issues "good first issue" (e labels parecidos) no GitHub;
    - nada é gerado na hora: o guia é salvo antes.
  - Na terceira rodada:
    - lista com todos os projetos que combinam, com filtros e ordenação;
    - atividade dos últimos 3 meses;
    - link para o relatório do OpenSSF Scorecard;
    - abertura e mantenedores recalculados (commits diretos contam; o rótulo do GitHub deixou de ser a fonte principal nos repos grandes).
  - Depois da auditoria dos dados (subagente, 31/10):
    - critério "pronto para iniciante" com 4 provas (estreias, aceite, vivo, guia);
    - taxa de aceite de PRs de fora;
    - "precisa de mãos" sem becos;
    - "o guia menciona" no lugar de "o projeto pede";
    - sugestões do Gemma fora do filtro;
    - duplicatas removidas;
    - filtros da lista refeitos.
    As propostas para depois do hackathon estão na seção "Depois de hoje".
  - Na reavaliação, o veredito foi "dá para congelar" depois de 4 ajustes, que já entraram:
    - guardiões sem o selo;
    - a conta "X de Y" sem X maior que Y;
    - "vivo" medido por PRs de gente de fora;
    - nota de código nos projetos prontos.
    Resultado: 38 projetos prontos para iniciante (os que o iniciante vê), com precisão estimada de 85 a 90%.
  - Feedback de uma pessoa experiente em open source, no evento: entrou o **tempo até o primeiro retorno** em PRs de fora e a contagem de **PRs parados** (30+ dias sem revisão), no card, na página e como 5º critério de iniciante. Ficaram 30 prontos.
  - Componentes em `web/components/` e rótulos em `web/lib/labels.ts`.

---

## Demo — Pablo

### P1. Gabarito da política de IA (M) — ✅ PR #39 (Pablo; revisão do Claude)
- Rotular 25 repositórios em `eval/gabarito.csv` lendo os arquivos. Consulta: `SELECT repo, path FROM repo_files WHERE path != 'README.md'`.
- Comece pelos que têm `AI_POLICY.md`, `AGENTS.md`, `CLAUDE.md` ou `copilot-instructions.md`. Inclua uns 5 sem nada (`silent`).
- **Pronto quando:** 25 linhas, e pelo menos 3 categorias aparecem.
- Feito: 28 repos (13 `silent`, 7 `accepts_with_disclosure`, 5 `accepts`, 3 `forbids`). Na revisão, 5 rótulos foram corrigidos conferindo o texto em `repo_files` (OBS e acorn proíbem; Godot pede aviso; Prettier e sharp aceitam). Também entraram pyzmq, TanStack Query e llama.cpp.

### P2. README final e roteiro da demo (M)
- README em pt-BR e inglês: problema, como funciona, onde entra o Gemma (local e API), números (o achado do slide e a acurácia do K3).
- Roteiro de 2 minutos para o vídeo.

### P3. Vídeo, PR real e submissão (M), às 16h
- Gravar a demo. Abrir um PR de verdade num projeto que o OpenDoor recomendou. Submeter no MLH nas duas categorias.

---

## Integração — José

### I1. Integração final (M), às 15h
- Gerar o `projects.json` final (skills + perfil + ai_policy), fazer o deploy, testar o fluxo inteiro e congelar a `main` às 16h.

---

## Depois de hoje
- **Necessidades mais específicas** (auditoria de 31/10):
  - coletar todos os labels de cada repo e separar "good first issue" livre e recente de "help wanted";
  - medir o tempo até a primeira resposta e os PRs de fora parados (do cache bruto);
  - segurança por verificação do Scorecard (`scorecard_checks`, já coletado);
  - detectar a infraestrutura de tradução (crowdin, weblate, `locales/`);
  - prompt do Gemma ancorado em labels e PRs parados;
  - um gabarito de necessidades rotulado à mão;
  - estreias também nos repos grandes;
  - guardar o `nameWithOwner` da API para resolver redirecionamentos.
  - o CONTRIBUTING em outros caminhos (`.rst`, `docs/`, `.github` da organização, variações de caixa): 77 projetos caem no selo de iniciante só por isso;
  - `authorAssociation` no cache, para saber quem é funcionário da empresa;
  - atividade dos repos Go (só 4 de 151 cobertos);
  - estreias nos repos grandes que têm histórico desde 2022 (axios, babel, jest, mocha, sharp, zod...);
  - exigir que o repo tenha mais de 24 meses para valer o selo (num repo novo, todo mundo "estreia").
- **G1. Guia de contribuição de cada projeto** (issue #21). **Parte feita hoje**, ideia do José: o guia "por onde começar" escrito uma vez por projeto pelo modelo (`pipeline/guides.py`) e combinado com o perfil sem chamar o modelo (`web/lib/guide.ts`). Validado numa amostra de 6 projetos. **Fica para depois:** ambiente, regras do projeto (DCO, estilo de commit), quem revisa e quanto tempo leva.

As issues no GitHub têm o código da tarefa no título (`[E1]`, `[K2]`...), e as dependências já apontam para o número da issue.
