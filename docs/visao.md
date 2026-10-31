# Visão do produto

*Registrada em 31/10/2026, a partir da conversa do José.*

## O problema
A recomendação comum, "abra um projeto que você usa e veja no que pode contribuir" (dita numa palestra do evento), é genérica. A barreira para começar é grande.

## A ideia
Uma plataforma em que a pessoa diz o que sabe e o que já fez, e recebe **portas de entrada** em projetos open source: em qual projeto, que tipo de ajuda ele precisa e por onde começar.

A longo prazo vira um marketplace ou rede social para ajudar projetos open source: mantenedores também **cadastram os próprios projetos** para pedir ajuda.

## Duas vertentes de projetos
1. **Críticos e "underground":** pacotes pequenos com muitos dependentes (blast radius enorme, casos como event-stream, xz-utils e chalk/debug).
2. **Mainstream:** apps de usuário final que vivem no GitHub (OBS, Godot, Audacity, Jellyfin...).

## Quatro perfis de projeto (o tipo de ajuda que cada um precisa)
| Perfil | Sinal nos dados | Contribuição | Para quem |
|---|---|---|---|
| Guardião | muitos dependentes, 1 pessoa faz tudo, commits diretos, Scorecard baixo | revisão de segurança, co-manutenção, financiamento | experientes e de confiança |
| Porta aberta | PRs de gente de fora mergeados nos últimos 12 meses, issues para iniciantes, alguém revisando | código, docs, testes, primeira contribuição | qualquer pessoa |
| Precisa de mãos | muitas issues abertas, poucos mantenedores ativos, aceita PR de fora | triagem, correções, revisão | intermediários |
| Estável/fechado | sem PR de fora e sem pedido de ajuda | pouca coisa | não é alvo |

**Indicador-chave de abertura:** a fatia de PRs mergeados de quem não é mantenedor.

## Formas de contribuir (não é só código)
Cada projeto precisa de tipos diferentes de ajuda, e cada pessoa pode oferecer tipos diferentes. O match cruza as duas coisas.

| Forma | Sinal de que o projeto precisa |
|---|---|
| Código | issues abertas com label de bug/feature, PRs de fora sendo aceitos |
| Triagem de issues | muitas issues abertas sem label e sem resposta |
| Revisão de PRs | PRs abertos esperando, poucos revisores ativos |
| Refinamento de issues | issues vagas: sem passos de reprodução, sem label, sem critério de pronto |
| Documentação | label de docs, README/CONTRIBUTING fracos ou ausentes |
| Tradução / localização | arquivos de i18n, label de tradução |
| Segurança | Scorecard baixo, perfil guardião, commits diretos sem revisão |
| Testes | label de testes, pouca cobertura (quando dá para saber) |

## Fora do MVP de hoje
- Cadastro de projetos pelos mantenedores (marketplace/rede social).
- Monitor de inserções maliciosas (ver `ideias.md`).
- Coletores para GitLab, Gerrit e Gitea (GIMP, LibreOffice, Blender, Firefox).
