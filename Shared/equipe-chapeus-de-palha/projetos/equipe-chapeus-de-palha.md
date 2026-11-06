# Projeto: a própria equipe Chapéus de Palha

Status: ativo
Atualizado em: 2026-11-02
Dono: Luan. Condutor: Luffy.
Regras de delegação e entrega: `contexto\fluxo-de-projetos.md`.

## Objetivo

Uma equipe de agentes no OpenBot, cada um no modelo certo para o seu papel, com os planos que o Luan já paga e sem estourar os limites. Este arquivo concentra as pendências da equipe que não pertencem a outro projeto.

## Pronto quando

Os agentes recebem pedidos pelo Luffy, entregam no formato combinado, o registro mostra cada OK com a frase do Luan, e o uso de tokens foi medido por uma semana.

## Etapas

| # | Etapa | Responsável | Status | Evidência |
|---|---|---|---|---|
| 1 | OpenBot instalado, OpenMausBot removido | Claude Code | feito | `contexto\decisoes.md` |
| 2 | 10 agentes e canal `equipe` | Claude Code | feito | `GUIA-OPENBOT.md`; Brook criado em 2026-11-02 e ainda fora do canal |
| 3 | Composio com Instagram conectado | Luan | feito | `GUIA-OPENBOT.md` |
| 4 | Workflow "Instagram v2 (PUBLICA)" com Aprovação | Claude Code | feito, publicação real ainda não testada | `GUIA-OPENBOT.md` |
| 5 | Fluxo de projetos e delegação | Claude Code | feito em 2026-11-02 | `contexto\fluxo-de-projetos.md` |
| 6 | Resumo novo do Luffy no app e agentes em pastas | Claude Code | feito em 2026-11-02 | Comando (Luffy), Engineering (Nami, Franky, Zoro, Usopp), Redes Sociais (Sanji, Robin, Brook), Apoio (Chopper, Jinbe); o canal One Piece ficou sem pasta |
| 7 | Teste do fluxo novo com um pedido real | Luffy | pendente | |

## Agora

O fluxo está em arquivos e o resumo novo do Luffy já está no app. Aguardando: o primeiro projeto real conduzido pelo Luffy com o modelo novo.

## Próximo passo

O Luan faz um pedido ao Luffy e confere se ele usa os campos de delegação e o arquivo de projeto.

## Pendências da equipe

- Permissões somente leitura do Chopper e do Zoro: o app não tem esse nível (só "Espaço de trabalho", "Perguntar antes" e "Acesso completo"). Hoje vale a regra escrita.
- Brook: entrar no canal `#equipe`.
- Skill `equipe-chapeus-de-palha` (em `~\.agents\skills\`) e `exportacao\briefing-chatgpt-codex.md` ainda listam nove agentes, sem o Brook.
- Robin: o Luan preencher as preferências de vaga (`agentes\robin.md`) e os itens [CONFIRMAR] do currículo; resumo da marca para o Sanji.
- Jinbe: teste de delegação pelo Luffy.
- Sanji: fontes Google do HyperFrames e teste real de publicação pelo Composio (só com um post aprovado pelo Luan).
- Composio: a segunda conexão do Instagram, "initiated", pode ser apagada.
- Memória: integrar o OpenBot, o Codex e o Antigravity (`contexto\integracao-memoria.md`).
- Tokens: medir o uso antes e depois da economia, em um projeto, por uma semana.
- Backup da pasta `Shared`.
- Modelo de prompt de vídeo para o Sanji.
- Confirmar se o Codex enxerga a skill `equipe-chapeus-de-palha`.

## Decisões do projeto

- 2026-11-02: agentes organizados em pastas no app (o OpenBot chama de "pasta" o que o Luan chamou de seção): Comando, Engineering, Redes Sociais e Apoio. Sem pasta por projeto: os agentes atendem vários projetos e o estado deles fica em `projetos\`. Pasta "Carreira" só se o Luan pedir.
- 2026-11-02: projetos ganham arquivo em `projetos\`; o registro fica com uma linha por OK; OK dado direto a um agente vem com a frase exata no relatório do agente; só o Workflow com Aprovação publica por ferramenta. Pedido do Luan: "Faça todas".
