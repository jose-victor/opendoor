# Dicionário de dados — `data/ecosystem.db`

Repositório sempre identificado como `dono/nome` em minúsculas. Meses no formato `AAAA-MM`, só meses fechados, a partir de `2018-01`.

## Mapa
| Tabela | Conteúdo |
|---|---|
| `repo_tags(repo, tag)` | de onde o repo veio: `npm-graph`, `pypi-graph` ou `go-graph` (grafo de dependências de cada ecossistema) ou `mainstream-app` (lista feita à mão) |
| `seeds(system, name, version)` | pacotes-semente do grafo |
| `packages(system, name, version, repo, dependents, direct_dependents)` — `system`: `npm`, `pypi` ou `go` | cada pacote do grafo; `dependents` = quantos pacotes dependem dele (deps.dev) |
| `dep_edges(system, seed, from_name, to_name)` | quem depende de quem, por semente |

## Foto atual
| Tabela | Conteúdo |
|---|---|
| `repos` | descrição, linguagem, licença, criação, último push, arquivado, estrelas, forks, issues/PRs abertos e totais; `found=0` = não existe mais |
| `repo_files(repo, path, oid, text)` | CONTRIBUTING, AGENTS, CLAUDE, AI_POLICY, copilot-instructions, README. `oid` muda quando o arquivo muda |
| `repo_labels(repo, newcomer_open)` | issues abertas com "good first issue", "help wanted" e parecidas |
| `repo_scorecard(repo, overall, date)` / `scorecard_checks(repo, check_name, score, reason)` | OpenSSF Scorecard (0–10) e cada verificação (Maintained, Code-Review, Branch-Protection...) |
| `package_advisories(system, name, version, advisory)` | alertas de vulnerabilidade da versão atual |

## Atividade mensal
| Tabela | Conteúdo |
|---|---|
| `repo_monthly(repo, month, ...)` | issues abertas/fechadas (concluídas ou "não planejadas"), PRs abertos/mergeados/fechados sem merge, revisões |
| `commit_monthly(repo, month, commits, direct_commits)` | commits no branch principal; `direct_commits` = sem PR associado (entrou sem revisão) |
| `participation(repo, month, role, login, is_bot, n)` | **quem fez cada papel**, quantas vezes no mês |

Papéis em `participation.role`:
- `pr_author`, `pr_reviewer` (1 por PR, sem contar o autor), `pr_merger`, `pr_closer` (fechou sem merge);
- `merged_pr_author` (autor de um PR que foi aceito, no mês do merge);
- `issue_author`, `issue_closer`;
- `committer`, `direct_committer`.

Logins especiais: `ghost` = conta apagada; `~Nome` = autor de commit sem conta no GitHub.

## Repositórios grandes (`repos.collection_mode = 'contagem+amostra'`)
Acima de 6 mil issues + PRs não copiamos item a item:
- `repo_monthly`: só `issues_opened`, `issues_closed`, `prs_opened` e `prs_merged`, que são **contagens completas desde 2018** pela busca do GitHub. Os outros campos ficam NULL.
- `commit_monthly`: `commits` completo; `direct_commits` NULL.
- `repo_sample(repo, window_start, prs, human_prs, outsider_prs, first_timer_prs, mergers, authors)`: amostra de até 300 PRs aceitos nos últimos 12 meses. `outsider_prs` = autor não é membro, dono nem colaborador (`authorAssociation`). `first_timer_prs` quase sempre dá 0, porque a associação é a de hoje: depois do merge, quem estreou vira contribuidor.
- `participation` desses repos é parcial (só o período mais recente) e não deve ser usada para séries anuais.

## Cobertura (leia antes de comparar anos)
- `repos.activity_since` / `repos.activity_truncated`: a partir de quando PRs e issues estão completos. Repositórios gigantes guardam só os 3 mil itens mais recentes por tipo.
- `commit_coverage(repo, since, truncated)`: o mesmo para commits.
- Itens abertos antes de 2018 e fechados depois não entram na contagem de fechamentos.
- **Estrelas por ano não existem** (o GitHub fechou a lista de quem deu estrela). Só o total atual em `repos.stars`.

## Consultas de exemplo

**Abertura: fatia de PRs aceitos que vieram de quem não é mantenedor (últimos 12 meses)**
```sql
WITH win AS (SELECT * FROM participation WHERE month >= strftime('%Y-%m', 'now', '-12 months') AND is_bot = 0),
mergers AS (SELECT DISTINCT repo, login FROM participation WHERE role = 'pr_merger')
SELECT w.repo,
       SUM(w.n) AS prs_aceitos,
       SUM(CASE WHEN m.login IS NULL THEN w.n ELSE 0 END) AS de_fora,
       ROUND(1.0 * SUM(CASE WHEN m.login IS NULL THEN w.n ELSE 0 END) / SUM(w.n), 2) AS abertura
FROM win w LEFT JOIN mergers m ON m.repo = w.repo AND m.login = w.login
WHERE w.role = 'merged_pr_author'
GROUP BY w.repo HAVING prs_aceitos >= 5 ORDER BY abertura DESC;
```

**Guardiões: muito usados, uma pessoa só, commits diretos**
```sql
WITH dep AS (SELECT repo, MAX(dependents) AS dependents FROM packages GROUP BY repo),
people AS (SELECT repo, COUNT(DISTINCT login) AS mantenedores FROM participation
           WHERE role IN ('pr_merger', 'direct_committer') AND is_bot = 0
             AND month >= strftime('%Y-%m', 'now', '-24 months') GROUP BY repo)
SELECT d.repo, d.dependents, p.mantenedores, s.overall AS scorecard
FROM dep d JOIN people p USING (repo) LEFT JOIN repo_scorecard s USING (repo)
WHERE p.mantenedores <= 1 ORDER BY d.dependents DESC LIMIT 20;
```

**Saúde de um projeto ao longo dos anos**
```sql
SELECT substr(month, 1, 4) AS ano, SUM(prs_opened) AS prs, SUM(prs_merged) AS aceitos, SUM(issues_opened) AS issues
FROM repo_monthly WHERE repo = 'expressjs/express' GROUP BY ano;
```
