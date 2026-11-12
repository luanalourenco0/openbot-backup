# Projeto: equipe de agentes Chapéus de Palha

Atualizado em 2026-11-11.

## Objetivo

Uma equipe de agentes de IA, com tema de One Piece, rodando no OpenBot com os planos que o Luan já paga, cada agente no modelo certo para o seu papel e sem estourar os limites.

## Estado atual

- OpenBot 0.56.0 instalado e configurado. Há 15 agentes (lista e modelos no `AGENTS.md`) e o canal One Piece, chamado de `#equipe` nestes documentos, com o Luffy como líder. Em 2026-11-11 o Luan colocou no canal Vivi, Kaya, Tio Patinhas, Bot Builder, Kureha e Bon Clay. Agentes novos do dia: Kureha (Instagram da Katia, `projetos\instagram-katia.md`) e Bon Clay (edição de vídeo, `editor-video\`), ambos aguardando OK do Luan. Restauração de fotos (`ferramentas\restauracao\`, Franky): reprovada para venda por cor escura e checagem de identidade pouco confiável (revisões do Zoro e da Kaya, 2026-11-11); Kaya ainda não integrada.
- OpenMausBot foi desinstalado por completo.
- CLIs instaladas: `claude` e `codex`. O Gemini roda pelo runtime do Antigravity (1.4.5) dentro do OpenBot. Grok, OpenCode, Cursor, Cline e Pi não estão instalados.
- Planos: Claude Pro (limite semanal apertado desde 2026-10-31) e ChatGPT Plus. O Luan informou em 2026-11-02 que o limite do ChatGPT foi resetado; o Luffy não verificou.
- As instruções completas dos agentes estão em `agentes\`; o app recebe um resumo de até 2.000 caracteres que aponta para elas.
- **Estado dos projetos e pendências da equipe: `projetos\`.** Pedido de um passo é uma linha no registro; projeto tem arquivo próprio. Regras em `contexto\fluxo-de-projetos.md`. Pendências da própria equipe: `projetos\equipe-chapeus-de-palha.md`.
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
- O Sanji tem acesso total ao Instagram e à conta Meta. Publica sozinho dentro das regras de `agentes\sanji.md` (decisão de 2026-11-08).
- No X (@luanzeraAI), o Brook monta a fila e, com um OK na fila, publica pelo navegador do OpenBot. Risco de suspensão apontado pela Nami e aceito pelo Luan em 2026-11-08.
- Na LinkedIn, a Robin posta pelo navegador depois do OK do Luan no pacote de posts.
- Redes Sociais têm autonomia para reduzir a fricção manual: ver o envelope no `AGENTS.md`.
- Respostas em português do Brasil.
