# A3: qualidade das respostas do Gemma (3 perfis × 3 projetos)

Rodado em 31/10/2026 contra `POST /api/explain` local (`gemma-4-26b-a4b-it`, sem `responseSchema`). As respostas completas estão em `explain-3x3.json`.

| Projeto | Nível | Habilidades | Formas | Tempo | OK | 1º passo | "Abra um PR" no 1º passo? |
|---|---|---|---|---|---|---|---|
| debug-js/debug | iniciante | javascript | — | 30s | sim | Explore o repositório e a documentação para entender como a biblioteca… | não |
| expressjs/express | intermediario | javascript, backend | revisao | 47s | sim | Estude a documentação de contribuição e o guia de estilo do projeto pa… | não |
| godotengine/godot | experiente | cpp | codigo, testes | 31s | sim | Explore o roadmap e as discussões recentes no repositório para entende… | não |
| debug-js/debug | experiente | javascript, seguranca | seguranca | 31s | sim | Analise o repositório e os detalhes do relatório OpenSSF Scorecard par… | não |
| expressjs/express | iniciante | javascript | documentacao | 44s | sim | Explore o repositório e leia a documentação atual para entender o padr… | não |
| godotengine/godot | iniciante | cpp | traducao | 33s | sim | Leia o guia de contribuição oficial para entender o fluxo de tradução … | não |
| debug-js/debug | intermediario | javascript, testes | testes | 29s | sim | Explore o repositório e entenda a estrutura de testes atual para garan… | não |
| expressjs/express | experiente | javascript, backend | seguranca | 32s | sim | Explore o histórico de discussões e o roadmap do repositório para ente… | não |
| godotengine/godot | intermediario | cpp, multimidia | triagem | 33s | sim | Leia o guia de contribuição do Godot para entender os padrões de quali… | não |

**Conclusões**
- **9 de 9** respostas válidas, em pt-BR e específicas do projeto, citando números reais: "60 issues abertas", "147 PRs abertos", o Scorecard do debug.
- O primeiro passo é sempre observar ou ler o guia. Nenhuma resposta começa por abrir PR, como pede `docs/visao.md`.
- Os alertas fazem sentido: debug com um mantenedor só, Godot com 13 mil issues.
- Depois da rodada, o prompt passou a não citar a política de IA quando ela é `unknown` ou `silent`. Antes ele alertava "política desconhecida", o que era ruído.
- **Latência: de 29 a 47 s.** O site precisa de um estado de carregamento claro (S2/S3).
