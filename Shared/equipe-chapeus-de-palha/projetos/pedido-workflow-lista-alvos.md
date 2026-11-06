# Pedido ao Claude Code: Workflow com lista de alvos

Autorizado pelo Luan em 2026-11-02 ("OK, quero que faça o pedido"). Projeto: `projetos\igrejas-mogi-velas.md`.

## Objetivo

Trocar a edição manual de Igreja, @ e Cidade por uma lista. O Workflow "Igrejas Mogi: mensagem ao Instagram com aprovação" passa a ler `projetos\igrejas-alvos.md`, pegar a primeira linha com status `pendente` e preparar a mensagem.

## Pronto quando

1. O Workflow lê a lista e pega só a primeira linha `pendente`.
2. A Etapa 1 (preparar, sem enviar) abre o perfil daquela linha e digita o texto aprovado no direct, sem apertar Enter.
3. O nó de Aprovação mostra o nome da igreja, o @ e o texto. Só isso passa para a Etapa 2.
4. Rejeitar encerra o fluxo e não altera a lista.
5. Aprovar faz a Etapa 2 enviar uma vez e confirmar o envio. Só então a linha vira `enviado`. Se não houver confirmação, a linha continua `pendente` e o fluxo para e avisa.
6. Testes: primeiro a rejeição, com o alvo de teste (@luanzera.02, perfil pessoal), usando um modo teste que pula a checagem de igreja e de cidade. Nenhuma linha da lista muda durante o teste.

## Ajuste pedido pelo Luan (2026-11-03)

- O texto digitado na Etapa 1 precisa manter os parágrafos do texto aprovado, usando Shift+Enter entre eles. Não pode sair numa linha só.
- Enter sozinho não pode ser apertado, porque envia a mensagem.
- Antes do envio real, o bloco da tela de aprovação precisa mostrar os parágrafos iguais ao texto aprovado.
- Teste de aprovação em modo teste: conferir que os parágrafos aparecem no bloco e que, ao aprovar, a Etapa 2 não envia nada.

## Ajuste 2 pedido pelo Luan (2026-11-03): seguir o perfil-alvo

- Execução real nº 7 (Catedral Sant'Ana) falhou na Etapa 1: o perfil não mostrou o botão Mensagem. Nada foi digitado nem enviado.
- O Luan autorizou que o fluxo siga a página da igreja com quem vamos falar, antes de abrir o direct. Vale só para o perfil-alvo da linha, uma vez, e fica registrado no bloco da Etapa 1 ("Seguindo o perfil"). Em modo teste não segue ninguém.
- Isso muda a regra "não seguir": seguir acontece na Etapa 1, ANTES da Aprovação. Rejeitar depois não desfaz o seguir.
- Perfil privado com pedido "Solicitado": o fluxo para e avisa; o direct só abre quando aceitarem.

## Ajuste 3 (2026-11-03): o Luan cola o texto

- Execuções 8 a 10: a digitação com parágrafos pela Sanji falhou 3 vezes (caixa substituiu o texto; faltou linha em branco; quebra não confirmada). Nada foi enviado.
- Decisão (Luan: "Pode ser"): a Etapa 1 abre o direct e PARA, sem digitar. O Luan cola o texto aprovado (`projetos\texto-aprovado-igrejas.txt`, com parágrafos), sem Enter, e só então aprova. A Etapa 2 confere perfil e texto na caixa antes de enviar.

## Ajuste 4 (2026-11-03): a Sanji cola o texto (automação completa)

- A Etapa 1 passou a colar o texto aprovado de uma vez, lendo `projetos\texto-aprovado-igrejas.txt`, com 3 métodos e plano B (caixa vazia, o Luan cola).
- Execução nº 12 (modo teste): os 3 métodos falharam, porque a Sanji não usou o PowerShell para a área de transferência. Execução nº 13 (modo teste, @luanzera.02): colou com o método 2 (evento de colar por script), 4 parágrafos corretos, NADA ENVIADO, lista idêntica. Rejeitada ao final.
- Falta: envio real com a Etapa 2 (conferência, balão, marcação `enviado`). O Luan está sem pressa.

## Resultado do primeiro envio real (2026-11-03)

- Execução nº 15, Catedral Sant'Ana (linha 1): Etapa 1 colou o texto (método 2) com conferência final; o Luan conferiu o direct, aprovou ("Tudo certo agora. Aprovo"); a Etapa 2 enviou às 13h57, confirmou o balão e marcou a linha 1 como `enviado`. Execuções 14 e anteriores: nada enviado.
- Próximo alvo `pendente`: linha 2 (Santuário Sagrado Coração de Jesus). Cada envio precisa de aprovação própria.

## Ajuste 5 (2026-11-03): gatilho Webhook (autorizado pelo Luan)

- O gatilho do Workflow passou de Manual para Webhook ("Pode fazer o Webhook, vamos acabar com toda fricção manual dessa etapa").
- Endpoint: `https://signal.openbot.run/v1/webhooks/cc987657-42b9-4e81-8e64-6f5d69fe71d5`. Cabeçalhos `x-openbot-timestamp`, `x-openbot-delivery-id`, `x-openbot-signature` = `sha256=` + HMAC-SHA256 de `timestamp.deliveryId.corpo` com o segredo. Corpo aceito: `{"type":"openbot.test"}`.
- O segredo está em `C:\Users\Lourenco_Filho\OpenBot\Secrets\webhook-igrejas-mogi.secret` (fora da pasta compartilhada da equipe, só o usuário lê). Nunca imprimir nem copiar.
- Script para a Sanji: `ferramentas\executar-workflow-igrejas.ps1`. Inicia uma execução, que pega a primeira linha `pendente`, prepara o direct e PARA na Aprovação. A aprovação do envio continua sendo do Luan, na tela do OpenBot.
- Testes (modo teste, @luanzera.02): execuções nº 16 (chamada direta) e nº 17 (script), origem webhook, ambas chegaram à Aprovação e foram rejeitadas. Nada enviado; lista inalterada.

## Ajuste 6 (2026-11-03): aprovar sem alternar de tela

- Pedido do Luan: "Mantenha a aprovação e rejeição, mas faça com que consiga fazer essa fase sem ficar tendo que alternar a tela entre workflow e navegador do openbot".
- Execução nº 19 (linha 3, real) falhou na colagem, antes da Aprovação, e ninguém foi avisado. Nada enviado; a linha 3 continua `pendente`. A causa exata não foi apurada: os detalhes das ferramentas não ficam no registro. O perfil @paroquiansracarmo foi seguido nessa execução, segundo o relatório da Etapa 1.
- Colagem por script fixo: `ferramentas\colar-texto-instagram.js`, só com caracteres ASCII, compara a caixa com uma soma do texto aprovado e tenta até 3 vezes. Nunca envia.
- A Etapa 1 não falha mais por problema no alvo ou na colagem: o motivo vai para o campo "Problema" e o fluxo chega à Aprovação.
- O cartão de Aprovação mostra o texto com os parágrafos. A Etapa 2 confere de novo, cola de novo se preciso, não envia em duplicidade e só envia com `identico: true`.
- `ferramentas\status-workflow-igrejas.py` mostra o estado das execuções. O script de início recusa abrir uma segunda execução.
- Removido o nó de aviso criado antes: a notificação nativa do OpenBot já avisa na Aprovação.
- Testes em modo teste, @luanzera.02: nº 20 (direct não abriu; Problema apareceu no cartão; rejeitada) e nº 21 (Conferência IDÊNTICO; aprovada; Etapa 2 `identico: true`, `tentativas: 0`, MODO TESTE: NÃO ENVIADO; lista com o mesmo hash).
- Execução nº 22 (linha 3, real): o Luan aprovou, a Etapa 2 deu erro de sintaxe na conferência e NÃO enviou; a linha ficou `pendente`. Causa provável, não provada: erro da Sanji ao copiar o script. Correção: script mais curto, repetição em erro de cópia e Etapa 2 sempre devolve resultado. Execução nº 23 (modo teste): passou, `identico: true`, nada enviado.
- Execução nº 24 (linha 3, real): o Luan aprovou na tela; a Etapa 2 relatou ENVIADO às 15h55, balão confirmado. A linha 3 está `enviado` e a anotação em `igrejas-envios.md` foi feita sozinha; o nº da execução nessa linha foi preenchido depois pelo Claude Code.
- Não testado: o bloqueio de duplicidade. Na conta de teste ficou um rascunho na caixa do direct de @luanzera.02, não enviado.

## Não fazer

- Não enviar sem aprovação por mensagem. Cada envio tem a sua aprovação.
- Não mudar o texto aprovado. Ele está no Prompt, palavra por palavra.
- Não usar o Brook nos nós de Agente. Os dois nós usam a Sanji com GPT-6.1 Terra, como no GUIA-OPENBOT.md.
- Não excluir o Workflow de teste nem a lista sem OK do Luan.
- Não usar a conta da igreja fora do direct.

## Contexto

- Lista: `projetos\igrejas-alvos.md`
- Texto aprovado: ver `projetos\igrejas-mogi-velas.md`, seção "Decisões do projeto".
- Histórico de teste: `projetos\igrejas-mogi-velas.md`, seção "Para retomar o Workflow".

## Entrega

Status, o que mudou no Workflow, evidência de cada rodada (print do histórico com aprovação e rejeição) e o que não foi testado. Responder ao Luffy, que registra.
