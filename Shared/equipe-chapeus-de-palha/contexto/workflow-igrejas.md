# Workflow "Igrejas Mogi: mensagem ao Instagram com aprovação"

Estado em 2026-11-03. Montado pelo Claude Code a pedido do Luan. Detalhes e histórico de testes: `projetos\pedido-workflow-lista-alvos.md`. Projeto: `projetos\igrejas-mogi-velas.md`.

## O que o Workflow faz (uma igreja por execução)

1. **Gatilho (Webhook).** Quem inicia a execução é o script `ferramentas\executar-workflow-igrejas.ps1`, que a Sanji roda por PowerShell quando o Luan pedir. O Luan também pode clicar em "Executar agora" no nó do Gatilho.
2. **Etapa 1 (Sanji, GPT-6.1 Terra).** Lê `projetos\igrejas-alvos.md`, pega a primeira linha `pendente`, abre o perfil, **segue o perfil** se aparecer "Seguir", abre o direct e roda `ferramentas\colar-texto-instagram.js`, que cola e confere a caixa contra o texto aprovado. Não envia. Problema no alvo não derruba a etapa: vai escrito no campo "Problema" do resultado.
3. **Aprovação.** O OpenBot notifica o Luan. Ele decide só na tela do Workflow, sem abrir o navegador: o resultado da Etapa 1 mostra igreja, @, conferência automática e problema, e o cartão mostra o texto com os parágrafos e os botões Aprovar e Rejeitar.
4. **Etapa 2 (Sanji).** Só roda depois de Aprovar. Não envia se houver "Problema", se o perfil não bater ou se a conversa já tiver a mensagem. Roda o mesmo script (se o rascunho sumiu, ele cola de novo) e só envia com `identico: true`. Envia uma vez, confirma o balão, marca a linha como `enviado` em `projetos\igrejas-alvos.md` e anota o envio em `projetos\igrejas-envios.md`. Sem confirmação do balão, a linha fica `pendente` e o fluxo avisa.
5. **Saída.** Notificação com o resultado.

## O que já está autorizado e o que não está

- Autorizado pelo Luan (2026-11-03, no chat com o Claude Code): seguir o perfil da igreja-alvo na Etapa 1, uma vez por igreja, e o gatilho por Webhook. Não peça outro OK só para seguir o perfil-alvo.
- Continua exigindo o OK do Luan: cada envio, que ele dá clicando em Aprovar na tela do Workflow. A Sanji e o Luffy não aprovam por ele e não enviam fora do Workflow.
- O Luan não precisa dar OK extra para você iniciar a execução quando ele pedir "rode o Workflow para a próxima igreja".
- Fora do Workflow: não siga, não curta, não comente e não abra outros perfis.

## Para a Sanji

- Para iniciar: `powershell -NoProfile -File "C:\Users\Lourenco_Filho\OpenBot\Shared\equipe-chapeus-de-palha\ferramentas\executar-workflow-igrejas.ps1"`. Resposta HTTP 202 = execução iniciada. 401 = assinatura; 400 = corpo.
- Depois de iniciar, responda em uma linha que a execução começou e ENCERRE a resposta. Não confira nada e não deixe pergunta aberta: enquanto a sua conversa estiver ocupada, a Etapa 1 fica parada na fila (foi o que travou a execução nº 20).
- Para saber em que pé está: `python "C:\Users\Lourenco_Filho\OpenBot\Shared\equipe-chapeus-de-palha\ferramentas\status-workflow-igrejas.py"`. Mostra as últimas execuções, o estado e o resultado da Etapa 1. Use em vez de perguntar ao Luan.
- O script de início recusa abrir outra execução enquanto houver uma em andamento ou esperando aprovação. Não contorne.
- O segredo do Webhook está em `C:\Users\Lourenco_Filho\OpenBot\Secrets\webhook-igrejas-mogi.secret`. Nunca imprima, copie nem registre.
- `MODO TESTE` no nó Prompt: `não` para envio real; `sim` só em teste (alvo @luanzera.02, não segue, não envia, não mexe na lista). Não troque sem o Luan pedir.

## Para o Luffy

- O registro de cada envio real fica em `projetos\igrejas-envios.md`, escrito pela Etapa 2. Copie de lá para o `registro-aprovacoes.md` (que só você e o Luan editam). Não trate como "sem OK" um envio que passou pelo nó de Aprovação: o OK é o clique do Luan na tela.
- Respostas das igrejas: `projetos\igrejas-respostas.md`. O Luan avisa ou manda print, e você registra.
- Envios já feitos: Catedral Diocesana Sant'Ana, 2026-11-03 13h57 (execução nº 15); Santuário Sagrado Coração de Jesus, 2026-11-03 14h42 (execução nº 18); Paróquia Nossa Senhora do Carmo, 2026-11-03 15h55 (execução nº 24). Em 2026-11-04 o Luan pediu um novo lote de 10 igrejas, já em `projetos\igrejas-alvos.md` na ordem de prioridade (linhas 4 a 13). Sem linha `pendente`, uma execução devolve "SEM ALVO PENDENTE".

## Pontos fracos conhecidos

- A Sanji precisa copiar o script de colagem para a ferramenta, e uma cópia já saiu com erro de sintaxe (execução nº 22; nada foi enviado). O script foi encurtado, e as etapas repetem até 3 vezes em erro de cópia.
- Fila da Sanji: os nós do Workflow usam a mesma conversa do chat da Sanji. Se ela estiver ocupada ou com pergunta aberta, a execução espera sem avisar. Ver "Para a Sanji".
- O botão "Enviar mensagem" do Instagram pode ficar carregando (execução nº 20). A Etapa 1 tenta até 3 vezes e depois escreve em "Problema".
- Se o texto aprovado mudar, três lugares precisam mudar juntos: `projetos\texto-aprovado-igrejas.txt`, `ferramentas\colar-texto-instagram.js` (gerado, com a soma de conferência) e o cartão de Aprovação. Peça ao Claude Code.
- O Instagram pode bloquear o primeiro contato ou não mostrar o botão Mensagem em alguns perfis. Nesses casos o fluxo para e avisa; a linha continua `pendente`.
- Perfil privado: o pedido de seguir fica "Solicitado" e o fluxo para. Não foi testado.
