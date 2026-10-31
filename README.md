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
4. **IA aberta (Gemma 4):** lê a política de contribuição de cada projeto (aceita IA? com aviso? proíbe?) e explica por que um projeto combina com você.

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
| `pipeline/llm.py` | cliente mínimo do Gemma (Gemini API ou Ollama) |
| `web/` | site Next.js: páginas, `/api/explain`, `lib/types.ts` (tipos do contrato) |
| `data/ecosystem.db` | banco SQLite com tudo que foi coletado |
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
