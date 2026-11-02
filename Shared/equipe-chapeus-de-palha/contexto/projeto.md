# Projeto: equipe de agentes Chapéus de Palha

Atualizado em 2026-10-31.

## Objetivo

Uma equipe de agentes de IA, com tema de One Piece, rodando no OpenBot com os planos que o Luan já paga, cada agente no modelo certo para o seu papel e sem estourar os limites.

## Estado atual

- OpenBot 0.56.0 está instalado e foi aberto: a configuração inicial foi concluída. Os 8 agentes e o canal `equipe` foram criados em 2026-10-31 (modelos e esforço em `GUIA-OPENBOT.md`). O líder do canal ainda não foi definido.
- OpenMausBot foi desinstalado por completo.
- CLIs instaladas: `claude` e `codex`. Gemini, Grok, OpenCode, Cursor, Cline e Pi não estão instalados.
- Planos: Claude Pro (restam 13% do limite semanal em 2026-10-31 às 15h13, segundo o OpenBot; renova em 1º de novembro às 16h) e ChatGPT Plus, com o limite esgotado até 4 de nov., 6h57, segundo o aviso do OpenBot. Os agentes do Codex não respondem até lá. O Luan informou (2026-10-31) que ganha um reset do Codex na noite de hoje; os testes dos agentes do Codex e do fluxo "TESTE sem publicar" são para depois desse reset.
- As instruções dos 8 agentes estão em `agentes\`, prontas para colar no app.
- Existe uma cópia anterior para Claude Code e Codex em `ambiente-claude\equipe-chapeus-de-palha\`, só para teste. Um rascunho ainda mais antigo, `protocolo-luffy-orquestrador.md`, é do OpenMausBot e não vale.

## Modelos OpenAI (documentação da API, 2026-10-31)

| Modelo | Entrada / saída por milhão de tokens | Uso |
|---|---|---|
| GPT-6 Luna | US$ 0,10 / 0,50 | Tarefas simples em grande volume |
| GPT-6.1 Terra | US$ 1 / 5 | Raciocínio visual, uso de computador, escrita natural |
| GPT-6.1 Sol | US$ 2 / 10 | Equilíbrio entre custo e inteligência |
| GPT-6 Astra | US$ 10 / 50 | O mais capaz; só sob pedido do Luan |

Rodar o Astra com frequência pode esgotar o limite semanal do Plus em um ou dois dias. O quanto de cada modelo o Plus libera não foi confirmado em fonte oficial.

## Preferências do Luan

- Luffy é o chefe de gabinete e porta de entrada, mas o Luan pode falar direto com qualquer agente.
- Luffy no Haiku 5.5, com escalada para o Sonnet 5.5 se errar o encaminhamento com frequência.
- O Sanji tem acesso total ao Instagram e à conta Meta. Post só depois do OK do Luan, a cada post.
- Respostas em português do Brasil.

## Pendências

- Definir o líder do canal `equipe` e ajustar permissões (Chopper e Zoro somente leitura).
- Luan entrar nas contas Meta e LinkedIn no navegador do OpenBot.
- Luan preencher as preferências de vaga da Robin (`agentes\robin.md`).
- Integrar a memória do OpenBot, o Codex e o Antigravity (ver `contexto\integracao-memoria.md`).
- Medir o uso de tokens antes e depois da economia, em um projeto, por uma semana.
