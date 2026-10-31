# Ideias anotadas (fora do escopo atual)

## Monitor de mudanças em pacotes pequenos e críticos
*Anotada em 31/10/2026. Outro projeto: não seguir agora.*

Pacotes pequenos com muitos dependentes têm um raio de impacto enorme: uma mudança maliciosa chega a milhões de projetos (casos como event-stream, xz-utils e o comprometimento de chalk/debug em 2025).

A ideia é um sistema que acompanha commits e releases desses projetos e procura inserções suspeitas: código ofuscado, scripts de instalação novos, chamadas de rede inesperadas, troca de mantenedor, commits diretos sem revisão.

Pode aproveitar a base deste projeto, que já tem o grafo, os dependentes e quem faz merge e commit em cada projeto.
