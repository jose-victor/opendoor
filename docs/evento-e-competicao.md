# Hacktoberfest Hack Day São José dos Campos — base do projeto

Levantado em 31/10/2026 (manhã, horário de Brasília) a partir das páginas do MLH e da documentação do Google.
Itens marcados com **[não confirmado]** vieram de fontes secundárias ou não estavam nas páginas.

## 1. O evento

- **Nome:** Hacktoberfest Hack Day São José dos Campos
- **Organização:** GitHub Community São José dos Campos, junto com o GDG São José dos Campos
- **Data e horário:** sábado, 31/10/2026, das 09h às 17h (BRT)
- **Local:** UNIMAR São José dos Campos (presencial)
- **Levar:** notebook com carregador e conta do GitHub pronta
- **Programação:** hackathon (premiação para os 3 primeiros colocados do evento), mentoria sobre Git/GitHub e regras do Hacktoberfest, networking, palestra com mantenedores de projetos open source
- **Hashtag:** #Hacktoberfest, marcando as comunidades locais
- **Página do evento:** https://www.mlh.com/events/hacktoberfest-hack-day-sao-jose-dos-campos-x-github-community-sjc
- **Inscrição e check-in:** gerenciados no Organizer HQ (https://events.mlh.io/events/14779-hacktoberfest-hack-day-sao-jose-dos-campos/register)
- **Situação do José:** já inscrito.

### Prazo
- **Submissões fecham em 31/10/2026, 17h (-03).**
- Enviar em: `/events/hacktoberfest-hack-day-sao-jose-dos-campos-x-github-community-sjc/submissions/new` (botão "Submit a Project" na página do evento).
- **Uma submissão pode concorrer em todas as categorias em que se encaixar.**

### Dúvida em aberto
- A premiação dos 3 primeiros do hackathon local é separada das categorias do MLH. Os critérios de julgamento e o prêmio não estão na página. **Perguntar aos organizadores.**

## 2. As duas categorias de prêmio (MLH)

### 2.1 Best Open-Source AI Project (patrocínio DigitalOcean)
- **Prêmio:** Exclusive Hacktoberfest 2026 Winner DEV Badge e MLH Swag Bag.
- **Descrição oficial (resumo):** construir um projeto original que use IA open-source ou open-weight como parte importante do funcionamento.
- **Exemplos da página:** uma agent skill; algo construído com um modelo de linguagem open-weight (grande ou pequeno); construir ou adaptar um open-source model harness.
- **Página da categoria:** https://www.mlh.com/events/hacktoberfest-hack-day-sao-jose-dos-campos-x-github-community-sjc/challenges/01a0d987-0c41-12ea-13ac-5b85755dc2f3
- **Link de apoio:** "Build with DigitalOcean" (mlh.link/digitalocean). Não consegui ler o conteúdo, então não sei se há créditos ou tutoriais.

### 2.2 Best Use of Gemma 4 (patrocínio Google DeepMind)
- **Prêmio:** não informado na página.
- **Descrição oficial (resumo):** construir com o Gemma 4, um modelo aberto, leve e multimodal, acessado pela Gemini API.
- **Ideias da página:**
  - experiência multimodal: texto e imagem, um assistente que entende mais do que o usuário compartilha;
  - ferramenta de IA focada em aprendizado, criatividade, produtividade ou comunidade;
  - prototipagem rápida com um modelo aberto via Gemini API.
- **Página da categoria:** https://www.mlh.com/events/hacktoberfest-hack-day-sao-jose-dos-campos-x-github-community-sjc/challenges/01a03b87-be22-9180-5e2d-b3beeb66666d
- **Link de apoio:** "Build with Gemma 4" (mlh.link/gemma). Não consegui ler o conteúdo.

### 2.3 Como as duas se relacionam
- As duas pedem IA aberta como parte central do projeto.
- Um projeto que usa Gemma 4 (open-weight) tende a se encaixar nas duas. A categoria 1 não cita Gemma, mas pede "modelo open-weight".
- Falta confirmar com os organizadores se usar o Gemma pela Gemini API conta como "open-weight" para a categoria 1.

## 3. Gemma 4 — o que o modelo faz

Fonte: model card oficial (https://ai.google.dev/gemma/docs/core/model_card_4, atualizado em 30/07/2026). As páginas trazem aviso de que a documentação está deprecada e aponta para gemma.ai.

| Modelo | Tipo | Contexto | Entradas | Saída |
|---|---|---|---|---|
| E2B | denso, ~2,3B efetivos | 128K | texto, imagem, áudio | texto |
| E4B | denso, ~4,5B efetivos | 128K | texto, imagem, áudio | texto |
| 12B Unified | denso, ~12B | 256K | texto, imagem, áudio | texto |
| 26B A4B | MoE (3,8B ativos de 25,2B) | 256K | texto, imagem | texto |
| 31B | denso, ~30,7B | 256K | texto, imagem | texto |

- **Vídeo:** processado como frames, até 60 s a 1 fps, em todos os modelos.
- **Áudio:** até 30 s, só E2B, E4B e 12B (reconhecimento de fala e fala traduzida).
- **Imagens:** resolução e proporção variáveis.
- **Recursos:** chamada de funções nativa, modo thinking configurável, prompt de sistema nativo.
- **Idiomas:** 35+ de forma nativa, treinado em mais de 140. **Português não é citado explicitamente.**
- **Não documentado:** saída JSON estruturada.
- **Licença:** Apache 2.0.
- **Amostragem recomendada:** temperature=1.0, top_p=0.95, top_k=64.

### Benchmarks oficiais (modelos ajustados para instruções)

| Benchmark | 31B | 26B A4B | 12B | E4B | E2B |
|---|---|---|---|---|---|
| MMLU Pro | 85,2% | 82,6% | 77,2% | 69,4% | 60,0% |
| GPQA Diamond | 84,3% | 82,3% | 78,8% | 58,6% | 43,4% |
| LiveCodeBench v6 | 80,0% | 77,1% | 72,0% | 52,0% | 44,0% |
| AIME 2026 (sem ferramentas) | 89,2% | 88,3% | 77,5% | 42,5% | 37,5% |
| MMMU Pro (visão) | 76,9% | 73,8% | 69,1% | 52,6% | 44,2% |
| MMMLU (multilíngue) | 88,4% | 86,3% | 83,4% | 76,6% | 67,4% |

## 4. Gemini API para o Gemma 4

- **Modelos disponíveis na API:** `gemma-4-31b-it` e `gemma-4-26b-a4b-it` (os exemplos da doc usam o 26b-a4b). Os modelos com áudio (E2B, E4B, 12B) **não** estão listados na API; para áudio é preciso rodar local.
- **Chave:** Google AI Studio (https://aistudio.google.com/apikey).
- **Preço (página oficial, atualizada em 30/10/2026):** free tier com input, output e context caching **gratuitos**; tier pago "Not available".
- **Dados:** no free tier, o Google pode usar os prompts para melhorar seus produtos. Não enviar dados sensíveis nem de terceiros.
- **Search grounding:** **não disponível** para o Gemma 4.
- **Limites de uso (RPM, TPM, RPD):** só aparecem no AI Studio. **Verificar antes de desenhar algo com muitas chamadas.**
- **Contexto e modalidades pela API:** não especificados na documentação.
- **Execução local:** Ollama, LM Studio, llama.cpp, MLX e LiteRT-LM aparecem na documentação. Requisitos de hardware não foram confirmados.

## 5. Gemma 4 comparado com Claude (ordem de grandeza)

Não há comparação oficial com a mesma metodologia. Números de fontes secundárias **[não confirmado]**.

- **Conhecimento e raciocínio: perto.** GPQA Diamond: Gemma 31B 84,3%, Claude Sonnet 5 ~89–91%, Opus 5 ~93%. MMLU-Pro: Gemma 31B 85,2%, Sonnet 5 ~87,5%.
- **Código e tarefas longas (agentes): gap grande.** Claude: Sonnet 5.5 ~81% e Opus 5.5 ~90% no SWE-Bench Pro. O Gemma 4 não divulga SWE-bench; seus números de código (LiveCodeBench, Codeforces) medem problemas isolados e curtos.
- **Conclusão prática:** o Gemma serve bem para tarefas focadas (entender imagem, resumir, extrair, classificar, explicar). Não apostar nele como agente autônomo de longa duração.
- **Limitações do Gemma:** saída só em texto, sem busca na web, e o 31B não recebe áudio.

## 6. Pendências para decidir

- [ ] Qual projeto construir (brainstorming em andamento).
- [ ] Confirmar com os organizadores o que conta como "open-weight" na categoria 1 e quais são os critérios de julgamento das duas.
- [ ] Ver os limites do Gemma 4 no AI Studio.
- [ ] Ler os links "Build with DigitalOcean" e "Build with Gemma 4" no navegador (créditos, tutoriais, regras).
- [ ] Preparar a submissão antes das 17h.

## 7. Fontes

- https://www.mlh.com/events/hacktoberfest-hack-day-sao-jose-dos-campos-x-github-community-sjc
- https://ai.google.dev/gemma/docs/core/model_card_4
- https://ai.google.dev/gemma/docs/core/gemma_on_gemini_api
- https://ai.google.dev/gemini-api/docs/pricing
- https://ai.google.dev/gemini-api/docs/rate-limits
- https://www.datalearner.com/en/ai-models/pretrained-models/google-gemma-4-31b/analysis
- https://benchlm.ai/md/models/claude-sonnet-5.md
- https://benchlm.ai/compare/claude-opus-5-vs-claude-sonnet-5
- https://apidog.com/blog/claude-sonnet-5-5-benchmarks/
