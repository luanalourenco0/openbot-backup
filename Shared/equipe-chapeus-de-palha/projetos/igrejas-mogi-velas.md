# Projeto: igrejas católicas de Mogi das Cruzes e velas votivas (Luz & Encanto)

Status: ativo
Atualizado em: 2026-11-03
Dono: Luan. Condutor: Luffy.
Regras de delegação e entrega: `contexto\fluxo-de-projetos.md`.

## Objetivo

Listar as igrejas católicas de Mogi das Cruzes (SP) que têm Instagram; depois, com OK do Luan, contatar cada uma pelo Instagram do Luz & Encanto para saber se há lojinha, livraria ou lembranças e propor deixar velas votivas à mostra, com percentual sobre as vendas geradas.

## Pronto quando

1. Lista com nome, endereço, bairro, perfil do Instagram (link), fonte e data de verificação de cada igreja, e a marca "sem Instagram" ou "não verificado" quando for o caso.
2. Luan aprova o texto da proposta e o percentual.
3. Cada mensagem enviada tem OK próprio do Luan, e a resposta de cada igreja é registrada.

## Etapas

| # | Etapa | Responsável | Status | Evidência |
|---|---|---|---|---|
| 1 | Levantar igrejas católicas de Mogi das Cruzes com Instagram (só perfis públicos, sem seguir nem enviar mensagem) | Jinbe | feito (33 com Instagram, 9 sem ou não verificado) | `pesquisa\igrejas-mogi-das-cruzes.md` |
| 2 | Revisar a lista e tirar duplicatas e perfis que não são da igreja | Chopper | planejado | |
| 3 | Luan define o percentual, o texto da mensagem e o que pode ou não oferecer | Luan | planejado | |
| 4 | Sanji rascunha as mensagens (uma por igreja, sem pressão de venda) | Sanji | planejado | |
| 5 | Luan aprova cada mensagem; só então Sanji envia pelo Instagram Luz & Encanto (Workflow com Aprovação) | Sanji, Luan | primeiro lote feito (3 envios: 13h57, 14h42, 15h55) | `projetos\igrejas-envios.md`; `registro-aprovacoes.md` |
| 6 | Registrar respostas e vendas por igreja | Sanji, Luffy | planejado | |

## Agora

Etapa 1 feita (Jinbe). Texto e 3 alvos aprovados. Primeiro lote enviado em 2026-11-03, com aprovação do Luan na tela do Workflow para cada envio: Catedral Sant'Ana (13h57, nº 15), Santuário Sagrado Coração de Jesus (14h42, nº 18) e Paróquia Nossa Senhora do Carmo (15h55, nº 24). Não há mais linha `pendente` em `projetos\igrejas-alvos.md`.

## Próximo passo

Segundo lote: em 2026-11-04 o Luan pediu as 10 igrejas "mais contatáveis e com maior chance de aceitar a parceria". Elas estão em `projetos\igrejas-alvos.md`, linhas 4 a 13, e cada envio continua com aprovação na tela do Workflow. Acompanhar as respostas em `projetos\igrejas-respostas.md`. Em paralelo, a margem por vela vem da mãe do Luan, para checar o percentual antes de negociar.

## Aguardando OK do Luan

- Tabela de preços e margem por vela, vindas da mãe do Luan (ela controla). Na pasta de trabalho do Luz & Encanto (`Documents\Codex\2026-09-29\ut\outputs\Luz_Encanto_Instagram\00_Projeto\Estado_do_Projeto.json`) o preço ainda estava "aguardando informação posterior" em 2026-09-30; se a mãe já definiu, o Luan confirma o valor atual.
- Percentual sobre as vendas que será oferecido às igrejas (o Luan decide; o Luffy não sugere número).
- Estratégia aprovada pelo Luan em 2026-11-02: primeira mensagem sem número, perguntar à igreja como ela trata esse tipo de parceria; testar com 2 ou 3 igrejas; só então negociar o percentual dentro de piso e teto definidos pelo Luan.
- Texto da primeira mensagem e a regra de que cada mensagem tem OK próprio.
- Envio das mensagens pelo Instagram Luz & Encanto (publicar ou enviar mensagem em nome do Luan exige OK por ação).

## Decisões do projeto

- 2026-11-02: primeiro passo é só levantamento público; nenhum contato com igreja antes do OK do Luan para cada mensagem.
- 2026-11-02: o percentual de comissão é decisão do Luan, não do Luffy.
- 2026-11-02: a Paróquia Cristo Rei fica fora da lista; a Kátia fala direto com o padre.
- 2026-11-02: o primeiro contato é sem preço e sem percentual, reconhecendo como funcionam as parcerias com a igreja. Luan decide enviar manualmente por enquanto; a Sanji só rascunha. Configurar a Sanji para responder sozinha depende de OK novo e de um Workflow com Aprovação.
- 2026-11-02: texto-modelo aprovado pelo Luan ("Aprovo"), usando só "velas oratórias" (não "votivas"). Ainda não enviado. Cada igreja precisa de OK próprio para o envio: texto: "Olá! Somos a Luz & Encanto e trabalhamos com velas e decoração artesanal de cimento. Entre elas estão velas oratórias. 🕯️ Gostaríamos de saber se a igreja tem lojinha, livraria ou espaço para lembranças e como costuma tratar parcerias desse tipo. Seria possível conversarmos sobre deixar velas oratórias à mostra nesse espaço? Agradecemos pela atenção! Kátia Ribeiro, responsável pelo Luz & Encanto".
- 2026-11-02: as mensagens são assinadas por Kátia Ribeiro, responsável pelo Luz & Encanto (pessoa real, de acordo, OK registrado). Sem bairro nem dados pessoais além do nome.
- 2026-11-03: primeiro lote de 3 igrejas enviado, cada envio com aprovação do Luan por clique em Aprovar na tela do Workflow (execuções nº 15, 18 e 24). Registro em `registro-aprovacoes.md`.
- 2026-11-03: o Luan autorizou a Sanji a seguir o perfil-alvo na Etapa 1, uma vez por igreja, sem novo OK para isso. Nada além do perfil-alvo.
- 2026-11-03: regra da Sanji: depois de iniciar o Workflow, responde em uma linha e encerra, sem pergunta aberta. Estado da execução: `ferramentas\status-workflow-igrejas.py`.
- 2026-11-03: nenhuma resposta de igreja vira nova mensagem sem OK do Luan.

## Workflow de envio (criado pelo Claude Code em 2026-11-02, não executado)

- Nome no app: "Igrejas Mogi: mensagem ao Instagram com aprovação (1 igreja por execução)". Pedido do Luan: "Leia toda a conversa com Luffy sobre novos planos para o instagram Luz & Encanto e crie o fluxo de trabalho que ele n conseguiu fazer por favor". Duplicado do "Instagram v2 (PUBLICA)", que já tinha as ligações certas.
- Fluxo: Gatilho manual + Prompt (igreja, @perfil e texto aprovado) → Agente 1 (Sanji) abre o perfil e o direct no navegador do OpenBot, digita o texto e NÃO envia → Aprovação (o Luan vê perfil, link e texto digitado) → Agente 2 (Sanji) clica em Enviar uma única vez → Saída (notificação). Ligações conferidas no banco do app: o Agente 2 só recebe entrada da Aprovação.
- Como usar: no nó Prompt, o Luan edita as linhas "Igreja", "Instagram" e "Cidade", clica em Executar fluxo de trabalho e aprova ou rejeita. Uma execução por igreja; cada "Aprovar" é o OK daquela mensagem. Alvos aprovados: Catedral Sant'Ana, Santuário Sagrado Coração de Jesus e Nossa Senhora do Carmo (Centro).
- Prova de que a Aprovação bloqueia (banco do app, Workflow "TESTE sem publicar", 01/11): na execução 2 a Aprovação esperou cerca de 100 s e, ao aprovar, o Agente 2 rodou; na execução 3 o Luan rejeitou, o status ficou "stopped" e o Agente 2 não rodou. O alerta "a aprovação não bloqueou o fluxo" daquele teste foi falso alarme: a Aprovação só repassa o rascunho e o Agente 2 não vê "pode postar".
- Não provado: o envio pelo navegador dentro do Workflow (a sessão do navegador durante a execução, o Enter do direct que envia, bloqueio do Instagram a primeiro contato). A primeira execução deve ser com 1 igreja e o Luan acompanhando.
- O Workflow "TESTE aprovação bloqueia (sem envio)" que a Sanji disse ter criado não existe no app (a lista tinha só 3 Workflows). O "ANTIGO..." e o "TESTE sem publicar..." podem ser excluídos, só com OK do Luan.
- Pela API do Instagram não dá para iniciar a primeira conversa. Nada foi enviado. Cada envio precisa de OK próprio.

## Histórico

- 2026-11-02: Luan pediu o projeto. Luffy criou o arquivo a partir de `projetos\_modelo.md`.
