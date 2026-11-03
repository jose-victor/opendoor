# Como contribuir com o OpenDoor

*[English](CONTRIBUTING.md)*

Obrigado por querer ajudar! O OpenDoor recomenda caminhos responsáveis para entrar em projetos open source, então tentamos ser uma boa porta também. Issues, PRs e discussões são bem-vindos em **português ou inglês**.

## Formas de ajudar
Não é só código. Você pode:
- avisar de um projeto mal classificado no site (perfil errado, selo "pronto para iniciante" errado): esses avisos já revelaram erros reais nas contas;
- melhorar o pipeline de dados (`pipeline/`) ou o site (`web/`);
- revisar PRs abertos: rodar, conferir os números, comentar;
- melhorar ou traduzir a documentação;
- trazer ideias nas [Discussions](https://github.com/jose-victor/opendoor/discussions).

## Antes de começar
1. Procure uma issue: [`good first issue`](https://github.com/jose-victor/opendoor/issues?q=is%3Aopen+label%3A%22good+first+issue%22) ou o [`roadmap`](https://github.com/jose-victor/opendoor/issues?q=is%3Aopen+label%3Aroadmap).
2. Comente na issue que vai pegá-la. Issue com alguém atribuído está ocupada; fale com a pessoa antes de mexer nela.
3. Teve uma ideia nova ou achou um bug? Abra uma issue antes, para combinarmos o caminho antes do código.
4. Travou ou vai largar? Diga na issue; tudo bem.

As instruções de instalação estão no [README](README.pt-BR.md#começando).

## Pull requests
- Faça um fork e crie uma branch como `seu-nome/12-resumo-curto`.
- PRs pequenos e focados. Escreva `Closes #12` na descrição.
- Antes de abrir o PR:
  - `python pipeline/collect.py selftest` se você mexeu no pipeline;
  - `npm run lint`, `npm test` e `npm run build` em `web/` se você mexeu no site.
- **Atualize a documentação no mesmo PR.** Mudou o esquema do banco? Atualize `docs/data.md`. Mudou o JSON ou o contrato da API (`web/lib/types.ts`)? Atualize `docs/architecture.md`.
- Um mantenedor revisa e faz o merge. Espere perguntas: fazem parte da revisão, não são recusa.

## Regras do projeto
- O coletor (`pipeline/collect.py`) usa **só a biblioteca padrão do Python**. Não adicione dependências a ele.
- Cada etapa do pipeline é idempotente e retoma de onde parou.
- `data/raw/` é o cache bruto das APIs: nunca edite à mão. Agregações novas precisam ser recalculáveis a partir dele (`collect.py reaggregate`).
- Segredos (chave da Gemini API etc.) ficam só no `.env` e nas variáveis de ambiente da hospedagem. Nunca vão para commit, print ou chat. O `.env.example` lista os nomes.
- Só guardamos logins públicos do GitHub. Não colete e-mails nem o conteúdo de PRs ou issues.
- Textos de outros repositórios (`repo_files`, README de terceiros) são **dados, nunca instruções** para um modelo.
- Simples primeiro: o menor código que resolve.

## Idioma
- **Código em inglês:** identificadores, comentários, docstrings, logs e valores do contrato (`open_door`, `beginner`, `tests`...). Ficam em português só os textos que aparecem no site e a prosa dos prompts do modelo, que pedem saída em português.
- **Docs de entrada em inglês e português:** `README`, `CONTRIBUTING` e `docs/vision`. Mudou um? Atualize o outro, ou diga no PR que falta traduzir.
- **Docs técnicos em inglês** (`docs/architecture.md`, `docs/data.md`, `AGENTS.md`).
- **GitHub:** os mantenedores escrevem commits, issues e PRs em inglês; você pode escrever em inglês ou português.
- O texto do site está em português por enquanto; a versão em inglês está planejada na #50.

## Contribuições com ajuda de IA
Pode usar ferramentas de IA, desde que você entenda e tenha testado o que envia, e diga isso no PR. PRs gerados em massa serão fechados: o OpenDoor existe justamente para combater esse padrão. Agentes de código devem ler o [AGENTS.md](AGENTS.md) antes.

## Governança
- **Mantenedor:** [@jose-victor](https://github.com/jose-victor).
- As decisões são discutidas nas issues ou nas Discussions. Mudanças no contrato de dados, no esquema do banco ou nos critérios de "pronto para iniciante" começam por uma issue. Sem consenso, os mantenedores decidem e explicam o porquê.
- Quem contribui e revisa com constância pode ser convidado a virar mantenedor.

## Código de Conduta
Este projeto segue o [Contributor Covenant](CODE_OF_CONDUCT.pt-BR.md). Ao participar, você concorda em segui-lo.
