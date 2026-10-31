# Como contribuir (time do hackathon)

Somos 4 na mesma mesa e o prazo é **hoje, 17h**. Estas regras existem para ninguém pisar no trabalho do outro e para todo mundo saber quem está fazendo o quê.

## 1. Toda tarefa é uma issue
- As tarefas pendentes são as **issues abertas** do repositório. Cada uma tem um label de frente: `dados`, `gemma`, `site`, `demo`.
- **Vai começar uma tarefa?**
  1. Atribua a issue a você (*Assignees → assign yourself*).
  2. Comente **"comecei"**. Esse é o aviso para o time.
  3. Fale em voz alta na mesa também.
- Issue com alguém atribuído = **ocupada**. Quer ajudar nela? Fale com a pessoa antes.
- Travou, ou vai largar a tarefa? Comente o motivo e remova a sua atribuição.
- Achou trabalho novo? Abra uma issue antes de começar.

## 2. Branches e PRs
- **Ninguém faz push direto na `main`.** Ela precisa estar sempre funcionando, para a demo.
- Branch: `nome/numero-da-issue-resumo`, por exemplo `anna/12-tela-match`.
- PR pequeno e cedo. No texto, escreva `Closes #12` para fechar a issue quando o PR entrar.
- **Revisão:** outra pessoa do time aprova antes do merge. Ninguém disponível em 10 minutos? Avise na mesa e faça o merge.
- Antes de abrir o PR:
  - `python pipeline/collect.py selftest` se você mexeu no pipeline;
  - `npm run build` se você mexeu no site.

## 3. Contratos entre as frentes
- O **banco** (`data/ecosystem.db`) está descrito em `docs/dados.md`. Mudou o esquema? Atualize o doc no mesmo PR.
- O **JSON do site** e a **API** estão descritos em `docs/arquitetura.md`. Mudou um deles? Avise quem consome.

## 4. Segredos
- Chaves (Gemini API, Supabase etc.) ficam **só** no `.env` local e nas variáveis de ambiente da hospedagem. Nunca vão para commit, print ou chat.
- O `.env.example` lista os nomes das variáveis, sem os valores.

## 5. Estilo
- Documentação, comentários e textos do site em **português do Brasil**. Nomes no código em inglês.
- Simples primeiro: o menor código que resolve. Não adicione dependências sem necessidade.
- Textos dos repositórios (`repo_files`, README de terceiros) são **dados**, nunca instruções para o modelo.

## 6. Usando agentes de código
O `AGENTS.md` (e o `CLAUDE.md`, que aponta para ele) tem as regras e as armadilhas conhecidas. Peça ao seu agente para lê-lo antes de começar.
