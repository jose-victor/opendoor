<img src="web/public/logo.svg" alt="Logo do OpenDoor: o Tux saindo por uma porta" width="160">

# OpenDoor

**Portas de entrada para contribuir com open source.** Você diz o que sabe e o OpenDoor mostra onde e como você pode ajudar: em qual projeto, que tipo de ajuda ele precisa e por onde começar.

Projeto do [Hacktoberfest Hack Day São José dos Campos](https://www.mlh.com/events/hacktoberfest-hack-day-sao-jose-dos-campos-x-github-community-sjc) (31/10/2026), concorrendo em *Best Open-Source AI Project* e *Best Use of Gemma 4*.

## Por quê
"Abra um projeto que você usa e veja no que pode contribuir" é um conselho genérico demais, e a barreira para começar é grande. Enquanto isso, pacotes pequenos dos quais metade da internet depende são mantidos por uma ou duas pessoas (event-stream, xz-utils, chalk/debug...).

Mas entrar não é sair abrindo PR sem entender o projeto: muitos projetos estão recebendo PRs que resolvem um problema e criam outros. O OpenDoor guia por um caminho responsável: escolher **um** projeto, observar, conversar com a comunidade, entender o código e começar por testes ou docs (ver [docs/visao.md](docs/visao.md#filosofia-contribuir-com-responsabilidade)).

O OpenDoor mapeia o ecossistema, mede a saúde e a abertura de cada projeto e casa isso com o perfil de quem quer contribuir.

## Como funciona
1. **Mapa:** grafo de dependências do npm, PyPI e Go (deps.dev), mais uma lista de apps mainstream e de IA que vivem no GitHub.
2. **Saúde, de 2018 até hoje:** issues, PRs, revisões, merges e commits por mês, com quem fez cada papel; OpenSSF Scorecard; issues para iniciantes.
3. **Perfil de cada projeto:** *Guardião*, *Porta aberta*, *Precisa de mãos* ou *Estável* (ver [docs/visao.md](docs/visao.md)).
4. **Pronto para iniciante:** só ganha o selo o projeto em que os dados mostram gente nova conseguindo entrar (estreias, aceite de quem é novo, PRs de fora aceitos recentemente, tempo de resposta e guia de contribuição). Ver [docs/arquitetura.md](docs/arquitetura.md).
5. **IA aberta (Gemma 4), offline:** lê a política de contribuição de cada projeto (aceita IA? com aviso? proíbe?), sugere onde ajudar e escreve o guia "por onde começar". Tudo é gerado antes e fica salvo; o site não chama o modelo na hora.

## Dados e IA

Em 31/10/2026, às 15h, o banco tinha:
- **973 repositórios**: os de 1.351 pacotes críticos de npm (950), PyPI (225) e Go (176), mais apps mainstream e de IA;
- **958 projetos no site**, dos quais 346 aceitam contribuição e **30 estão prontos para iniciante**;
- **39.100 linhas mensais** e **523.716 registros de participação**;
- **1.190 arquivos** de contribuição e de política de IA.

Os 104 repos grandes têm contagens mensais completas mais uma amostra de PRs. Todos os números são recalculáveis a partir do cache bruto.

O achado central é que atividade não é sinônimo de abertura: um projeto pode receber muitos PRs
e continuar mantendo poucas pessoas externas. Por isso, o OpenDoor mede PRs aceitos de quem não é
mantenedor, mantenedores ativos, issues para iniciantes, commits, revisões e Scorecard de segurança.

**O Gemma 4 (`gemma-4-26b-a4b-it`) trabalha em três pontos:**
1. **Oportunidades (offline):** `pipeline/opportunities.py` lê o guia de contribuição de cada projeto e sugere onde ajudar quando o projeto não diz. Exemplo no React: "traduzir a documentação oficial para o português brasileiro".
2. **Política de IA (offline):** `pipeline/classify_ai_policy.py` classifica se o projeto aceita IA, pede aviso ou proíbe, sempre com uma citação literal do arquivo.
3. **Guia "por onde começar" (offline):** `pipeline/guides.py` escreve, uma vez por projeto, o resumo e os passos por forma de ajuda. O site combina o guia com o perfil da pessoa, sem chamar o modelo. Os passos começam por observar e conversar, nunca por "abra um PR".

A rota `/api/explain` (modelo ao vivo, hoje `gemini-3.5-flash-lite`) continua disponível, mas o site não a usa: o grupo preferiu que tudo fosse gerado antes e ficasse salvo. A avaliação dela está em `eval/explain.md`.

`pipeline/llm.py` fala com o modelo pela Gemini API (`GEMINI_MODEL`, padrão `gemini-3.5-flash-lite`) ou pelo Ollama local. Os dados publicados hoje foram gerados com o Gemma 4.

## Roteiro da demo — 2 minutos

1. **0:00–0:15 — Problema:** “Contribuir com open source parece procurar uma porta sem saber qual está aberta.”
2. **0:15–0:35 — Escala:** mostrar que o OpenDoor combina pacotes críticos, aplicativos mainstream e dados históricos.
3. **0:35–0:55 — Perfil:** apresentar habilidade, nível e forma de contribuição escolhidos pela pessoa.
4. **0:55–1:20 — Resultados:** abrir um projeto e destacar perfil, abertura, mantenedores, issues para iniciantes e Scorecard.
5. **1:20–1:45 — Gemma:** mostrar as oportunidades sugeridas pela IA e a política de IA com a citação literal (por exemplo, o OBS proíbe: "must be human written"); depois, clicar em "por onde começar" para ver a explicação ao vivo.
6. **1:45–2:00 — Responsabilidade:** mostrar os primeiros passos de observar, conversar e começar por docs, testes ou triagem.
7. Fechar com a frase: “OpenDoor não manda fazer um PR; ajuda a entrar de maneira responsável.”

## English

OpenDoor is an open-source contribution recommender for people with limited time and experience.
It maps dependencies and GitHub activity, measures project openness and maintenance health, and
matches those signals with a contributor's skills, experience and preferred type of help.

The project uses data collected from deps.dev, GitHub and OpenSSF Scorecard. The static Next.js
site loads generated JSON, while the Gemma integration is designed to run on the server through
the `/api/explain` route. Gemma 4 suggests contribution opportunities, classifies each project's AI policy
with a literal quote as evidence, and explains live why a project fits and how to start responsibly.
`pipeline/llm.py` supports the Gemini API and a local Ollama backend.

The demo should emphasize responsible contribution: observe the roadmap, read contribution
guidelines, join discussions, understand the code and prefer low-risk starts such as documentation,
tests or issue triage.

## Estado da demo

- **Dados coletados:** 973 repositórios e 958 projetos no site, 30 prontos para iniciante (números completos em "Dados e IA").
- **Gabarito de políticas:** 28 repositórios rotulados à mão, com as 4 categorias (13 silent, 7 accepts_with_disclosure, 5 accepts e 3 forbids).
- **Gemma:** oportunidades, política de IA (966 de 975 repos classificados) e guias gerados offline. A rota ao vivo `/api/explain` foi avaliada em `eval/explain.md` (9 de 9 respostas válidas, de 30 a 45 s cada).
- **Acurácia do classificador (K3):** ainda sem o script oficial. Na auditoria de 31/10, 22 de 24 rótulos do gabarito já classificados bateram.

## Começando
Requisitos: Python 3.11+ (só biblioteca padrão) e o [GitHub CLI](https://cli.github.com/) logado (`gh auth login`), que fornece o token da API.

O banco já vem pronto em `data/ecosystem.db` (SQLite). Para explorar:

```bash
sqlite3 data/ecosystem.db ".tables"
python pipeline/collect.py stats
```

Para coletar de novo ou atualizar (cada etapa retoma de onde parou):

```bash
python pipeline/collect.py graph --system npm   # grafo de dependências (npm, pypi ou go)
python pipeline/collect.py apps        # apps mainstream (lista APPS em collect.py)
python pipeline/collect.py repos       # foto atual + arquivos de política
python pipeline/collect.py activity    # PRs/issues por mês desde 2018
python pipeline/collect.py commits     # commits por mês, quantos entraram direto sem PR
python pipeline/collect.py labels      # issues para iniciantes
python pipeline/collect.py topics      # topics do GitHub (habilidades)
python pipeline/collect.py security    # OpenSSF Scorecard + alertas
python pipeline/collect.py large       # repos grandes: contagens mensais + amostra de pessoas
python pipeline/collect.py reaggregate # recalcula agregações do cache bruto, sem API
python pipeline/build.py               # gera web/public/data/*.json para o site
python pipeline/opportunities.py       # Gemma sugere oportunidades (offline, com cache); rode o build.py de novo depois
python pipeline/classify_ai_policy.py  # Gemma classifica a política de IA (offline, com cache); rode o build.py de novo depois
python pipeline/guides.py              # guia "por onde começar" de cada projeto (offline, com cache); rode o build.py de novo depois
python pipeline/collect.py selftest    # testes da agregação
```

## Site (`web/`)
**No ar:** https://opendoor-fawn.vercel.app

Next.js 16 (App Router) na Vercel. Os dados vêm de `web/public/data/`, gerados por `python pipeline/build.py`.

```bash
cd web
cp ../.env.example .env.local   # preencha GEMINI_API_KEY
npm install
npm run dev                     # http://localhost:3000
```

## Estrutura
| Caminho | O quê |
|---|---|
| `pipeline/collect.py` | coletor (um arquivo, sem dependências) |
| `pipeline/build.py` | gera `web/public/data/*.json` a partir do banco: habilidades, perfil, oportunidades |
| `pipeline/skills.py` | vocabulário de habilidades e regras de detecção |
| `pipeline/opportunities.py` | Gemma 4 sugere oportunidades de contribuição (offline, em cache no banco) |
| `pipeline/classify_ai_policy.py` | Gemma 4 classifica a política de IA de cada repo, com evidência literal (offline, em cache em `ai_policy`) |
| `pipeline/guides.py` | guia "por onde começar" de cada projeto, escrito uma vez pelo modelo e combinado com o perfil no site (`web/lib/guide.ts`) |
| `pipeline/llm.py` | cliente mínimo do Gemma (Gemini API ou Ollama) |
| `web/` | site Next.js: páginas, `/api/explain`, `lib/types.ts` (tipos do contrato) |
| `data/ecosystem.db` | banco SQLite com tudo que foi coletado |
| `eval/` | `gabarito.csv` (política de IA rotulada à mão) e `explain.md` (avaliação das respostas do Gemma) |
| `docs/dados.md` | dicionário de dados e consultas de exemplo |
| `docs/tarefas.md` | **tarefas em aberto (cada uma vira uma issue)** |
| `docs/arquitetura.md` | contratos: formato do JSON, tipos, API do Gemma |
| `CONTRIBUTING.md` | como o time trabalha: issues, branches, PRs |
| `docs/visao.md` | visão do produto e os 4 perfis de projeto |
| `docs/evento-e-competicao.md` | regras do evento, categorias, Gemma 4 |
| `docs/ideias.md` | ideias anotadas fora do escopo |
| `AGENTS.md` / `CLAUDE.md` | instruções para agentes de código |

## Contribuindo (time)
Leia o [CONTRIBUTING.md](CONTRIBUTING.md): pegue uma issue, comente "comecei" e trabalhe numa branch. Não commite segredos (chave da Gemini API vai no `.env`, que está no `.gitignore`).

## Licença
GPL-3.0, ver [LICENSE](LICENSE).
