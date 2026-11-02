# Integração de memória entre ferramentas

Objetivo: todo agente, em qualquer ferramenta, ter o mesmo contexto do projeto sem ninguém repetir o que já foi decidido.

## Princípio

Esta pasta, `C:\Users\Lourenco_Filho\OpenBot\Shared\equipe-chapeus-de-palha\`, é a fonte única. Cada ferramenta recebe só um ponteiro fino para ela, sem cópias que fiquem desatualizadas.

## O que o OpenBot tem na máquina (verificado só por listagem)

- `C:\Users\Lourenco_Filho\OpenBot\Agents`: onde ficam os workspaces dos agentes. Estava vazia.
- `C:\Users\Lourenco_Filho\OpenBot\Shared`: pasta compartilhada. Esta equipe mora aqui.
- `C:\Users\Lourenco_Filho\AppData\Roaming\OpenBot`: dados do app, incluindo o banco `openbot.db`. Não mexer.

Ainda não sei como o OpenBot guarda a memória e as conversas de cada agente, nem se ele carrega a pasta `Shared` sozinho.

Verificado na tela em 2026-10-31: as configurações do canal `equipe` têm os campos Nome, Título e Instruções do canal, uma seção **Memórias** ("os agentes de equipe salvam o que aprenderam aqui", com opção de adicionar memória manualmente), uma seção Rotinas e a lista de membros. O Luffy aparece com uma coroa na lista de membros, que parece indicar o líder. A memória do OpenBot é por canal, dentro do app. Nada foi adicionado a ela.

## Estado por ferramenta

| Ferramenta | Como lê o contexto | Estado |
|---|---|---|
| Agentes do OpenBot | Instruções de cada agente mandam ler o `AGENTS.md` desta pasta | Escrito; falta criar os agentes no app |
| Codex (como provedor ou direto) | `AGENTS.md` do diretório de trabalho; basta um ponteiro de uma linha para esta pasta | Pendente, depois de criar o primeiro agente |
| Claude Code (como provedor ou direto) | `CLAUDE.md` do diretório de trabalho, com `@` para o `AGENTS.md` desta pasta | Pendente, depois de criar o primeiro agente |
| Antigravity | A confirmar qual arquivo de regras do projeto ele lê | Pendente |

## Próximos passos

1. Criar o primeiro agente no OpenBot e ver em qual diretório ele trabalha e o que ele carrega sozinho.
2. Colocar nesse diretório um ponteiro de uma linha para o `AGENTS.md` desta pasta, só se o agente não a carregar sozinho.
3. Ver na documentação do Antigravity quais arquivos de regras e de contexto ele carrega.
4. Qualquer mudança em configuração global de uma ferramenta passa pelo OK do Luan.

## Regras da memória compartilhada

- Um fato por linha, curto, com data quando for decisão.
- Nada de segredos, tokens ou senhas.
- Dados pessoais (currículo, perfil, conversas) ficam em `privado\`, fora daqui.
- Só o Luffy e o Luan editam `contexto\`. Os outros agentes sugerem a alteração a eles.
- Contexto curto custa menos tokens em toda sessão. Se um arquivo crescer, divida e deixe um ponteiro.
