<img src="web/public/logo.svg" alt="Logo do OpenDoor: o Tux saindo por uma porta" width="160">

# OpenDoor

*[English](README.md)*

**Portas de entrada para contribuir com open source.** Você diz o que sabe e o OpenDoor mostra onde e como você pode ajudar: em qual projeto, que tipo de ajuda ele precisa e por onde começar.

**No ar:** https://opendoor-fawn.vercel.app

O OpenDoor nasceu no [Hacktoberfest Hack Day São José dos Campos](https://www.mlh.com/events/hacktoberfest-hack-day-sao-jose-dos-campos-x-github-community-sjc) (31/10/2026), onde venceu a etapa local. Agora é um projeto da comunidade, e contribuições são bem-vindas.

## Por quê
"Abra um projeto que você usa e veja no que pode contribuir" é um conselho genérico demais, e a barreira para começar é grande. Enquanto isso, pacotes pequenos dos quais metade da internet depende são mantidos por uma ou duas pessoas (event-stream, xz-utils, chalk/debug...).

Mas entrar não é sair abrindo PR sem entender o projeto: muitos projetos estão recebendo PRs que resolvem um problema e criam outros. O OpenDoor guia por um caminho responsável: escolher **um** projeto, observar, conversar com a comunidade, entender o código e começar por testes ou docs (ver a [visão do produto](docs/vision.pt-BR.md#filosofia-contribuir-com-responsabilidade)).

O OpenDoor mapeia o ecossistema, mede a saúde e a abertura de cada projeto e casa isso com o perfil de quem quer contribuir.

## Como funciona
1. **Mapa:** grafo de dependências do npm, PyPI e Go (deps.dev), mais uma lista de apps mainstream e de IA que vivem no GitHub.
2. **Saúde, de 2018 até hoje:** issues, PRs, revisões, merges e commits por mês, com quem fez cada papel; OpenSSF Scorecard; issues para iniciantes.
3. **Perfil de cada projeto:** *Guardião*, *Porta aberta*, *Precisa de mãos* ou *Estável* (ver a [visão do produto](docs/vision.pt-BR.md)).
4. **Pronto para iniciante:** só ganha o selo o projeto em que os dados mostram gente nova conseguindo entrar (estreias, aceite de quem é novo, PRs de fora aceitos recentemente, tempo de resposta e guia de contribuição). Ver [docs/arquitetura.md](docs/arquitetura.md).
5. **IA, offline:** um modelo de linguagem lê a política de contribuição de cada projeto (aceita IA? com aviso? proíbe?), sugere onde ajudar e escreve o guia "por onde começar". Tudo é gerado antes e fica salvo; o site não chama o modelo na hora.

## Dados e IA

Em 31/10/2026, o banco tinha:
- **973 repositórios**: os de 1.351 pacotes críticos de npm (950), PyPI (225) e Go (176), mais apps mainstream e de IA;
- **958 projetos no site**, dos quais 346 aceitam contribuição e **30 estão prontos para iniciante**;
- **39.100 linhas mensais** e **523.716 registros de participação**;
- **1.190 arquivos** de contribuição e de política de IA.

Os 104 repos grandes têm contagens mensais completas mais uma amostra de PRs. Todos os números são recalculáveis a partir do cache bruto.

O achado central é que atividade não é sinônimo de abertura: um projeto pode receber muitos PRs e continuar mantendo poucas pessoas externas. Por isso, o OpenDoor mede PRs aceitos de quem não é mantenedor, mantenedores ativos, issues para iniciantes, commits, revisões e Scorecard de segurança.

**O modelo de linguagem trabalha em três pontos, sempre offline e com cache no banco:**
1. **Oportunidades:** `pipeline/opportunities.py` lê o guia de contribuição de cada projeto e sugere onde ajudar quando o projeto não diz. Exemplo no React: "traduzir a documentação oficial para o português brasileiro".
2. **Política de IA:** `pipeline/classify_ai_policy.py` classifica se o projeto aceita IA, pede aviso ou proíbe, sempre com uma citação literal do arquivo.
3. **Guia "por onde começar":** `pipeline/guides.py` escreve, uma vez por projeto, o resumo e os passos por forma de ajuda. O site combina o guia com o perfil da pessoa, sem chamar o modelo. Os passos começam por observar e conversar, nunca por "abra um PR".

`pipeline/llm.py` fala com o modelo pela Gemini API (`GEMINI_MODEL`, padrão `gemini-3.5-flash-lite`) ou por um Ollama local. Os dados publicados hoje foram gerados com o Gemma 4. A rota `/api/explain` (modelo ao vivo) continua no código, mas o site não a usa; o futuro dela está na #68.

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
python pipeline/opportunities.py       # oportunidades sugeridas pelo modelo (com cache); rode o build.py de novo depois
python pipeline/classify_ai_policy.py  # política de IA (com cache); rode o build.py de novo depois
python pipeline/guides.py              # guia "por onde começar" (com cache); rode o build.py de novo depois
python pipeline/collect.py selftest    # testes da agregação
```

## Site (`web/`)
Next.js 16 (App Router) na Vercel. Os dados vêm de `web/public/data/`, gerados por `python pipeline/build.py`.

```bash
cd web
cp ../.env.example .env.local   # GEMINI_API_KEY só é necessária para /api/explain
npm install
npm run dev                     # http://localhost:3000
```

## Estrutura
| Caminho | O quê |
|---|---|
| `pipeline/collect.py` | coletor (um arquivo, sem dependências) |
| `pipeline/build.py` | gera `web/public/data/*.json` a partir do banco: habilidades, perfil, oportunidades |
| `pipeline/skills.py` | vocabulário de habilidades e regras de detecção |
| `pipeline/opportunities.py` | oportunidades de contribuição sugeridas pelo modelo (em cache no banco) |
| `pipeline/classify_ai_policy.py` | política de IA de cada repo, com evidência literal (em cache em `ai_policy`) |
| `pipeline/guides.py` | guia "por onde começar" de cada projeto, combinado com o perfil no site (`web/lib/guide.ts`) |
| `pipeline/llm.py` | cliente mínimo do modelo (Gemini API ou Ollama) |
| `web/` | site Next.js: páginas, `/api/explain`, `lib/types.ts` (tipos do contrato) |
| `data/ecosystem.db` | banco SQLite com tudo que foi coletado |
| `eval/` | `gabarito.csv` (política de IA rotulada à mão) e `explain.md` (avaliação das respostas do modelo) |
| `docs/vision.pt-BR.md` | visão do produto e os 4 perfis de projeto |
| `docs/arquitetura.md` | contratos: formato do JSON, tipos, API |
| `docs/dados.md` | dicionário de dados e consultas de exemplo |
| `AGENTS.md` / `CLAUDE.md` | instruções para agentes de código |

## Contribuindo
Leia o [CONTRIBUTING.pt-BR.md](CONTRIBUTING.pt-BR.md). O trabalho planejado está nas [issues com label `roadmap`](https://github.com/jose-victor/opendoor/issues?q=is%3Aopen+label%3Aroadmap), e dúvidas e ideias vão para as [Discussions](https://github.com/jose-victor/opendoor/discussions). Este projeto segue um [Código de Conduta](CODE_OF_CONDUCT.pt-BR.md). Achou uma vulnerabilidade? Veja o [SECURITY.md](SECURITY.md).

## Licença
GPL-3.0, ver [LICENSE](LICENSE).
