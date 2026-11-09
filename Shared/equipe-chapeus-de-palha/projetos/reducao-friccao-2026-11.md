# Projeto: reduzir fricção da equipe e dar autonomia a Redes Sociais

Status: ACEITO e em aplicação; ver "Decisão do Luan" e "Aplicado"
Atualizado em: 2026-11-08
Dono: Luan. Autor e aplicação: Bot Builder.

## Decisão do Luan (formulário de aceite, 08/11)

| Item | Escolha |
|---|---|
| Sanji | "Publica sozinho dentro das regras, sem aprovação" |
| Brook | "Um OK para a fila, publicando pelo navegador (risco de suspensão apontado pela Nami)". Por isso, P3 não usa a API |
| Robin | "Para a Robin, podemos ter uma rotina semanal de posts, mas deixar como está, ela entra e consegue postar por mim". Por isso, P4 não usa "o Luan cola", e a busca de vagas segue como estava |
| Equipe | "Aplicar tudo, menos a redução de acessos". P6 não foi aplicado |
| Lote em andamento | "Você rejeita o próximo card e eu publico o resto sem cliques" |

## Aplicado

- Regras: `AGENTS.md`, `contexto\fluxo-de-projetos.md`, `contexto\projeto.md`, `agentes\sanji.md`, `agentes\brook.md`, `agentes\robin.md`, `agentes\luffy.md`, `x-bot\README.md`.
- Backup: `backups\2026-11-08\` (como reverter em `LEIA.md`).
- Preço do Kit de Natal em `projetos\catalogo-precos.md`.
- Resumos, títulos e modelos reserva no app. Luffy em esforço medium. Bot Builder na seção Apoio. Zoro, Jinbe, Vivi, Tio Patinhas e Doflamingo seguem sem modelo reserva, pois não entraram na sugestão.
- Workflow "Instagram: lote autônomo (sem aprovação)" e log `projetos\instagram-publicados.md`.
- Rotinas: Sanji domingo 18h (pausada até os testes passarem), Brook domingo 19h e diária 12h, Robin segunda 9h.
- Direct do Instagram (P2): não aplicado; a regra dele segue em `projetos\atendimento-instagram.md`, à espera dos testes do próprio projeto.

## Pedido do Luan (08/11)

"Quero que revise minha equipe, forma de trabalho, proponha melhorias para diminuir fricção. Principalmente nos sociais midias [...] autonomia para rodarem workflows sem aprovação a cada etapa [...]. Você tem autonomia para registrar isso e depois que eu aceitar as alterações propostas, colocar em prática."

## Diagnóstico

### Causa da aprovação story por story

1. O Luan aprovou aprovação única do lote: "Aprovo e confirmo" (`registro-aprovacoes.md`, linha 39).
2. O workflow nasceu assim, mas `agentes\sanji.md` diz "O OK vale só para aquele post", e o resumo do Sanji no app diz "REGRA QUE NÃO MUDA". O próprio registro aponta o conflito.
3. Na revisão 3, o Sanji montou uma cadeia individual: 11 cliques e 12 execuções de agente em Terra high, em vez de 1 clique e 2 execuções.
4. O card antigo do lote ficou desconectado, mas ativo: se for aprovado, publica de novo os itens 1 a 11 (risco de duplicar).

Conclusão: o problema é a regra escrita, não o Sanji nem a plataforma. Trocar só o workflow não resolve, porque a regra volta a mandar.

### Onde a mesma regra está escrita

`AGENTS.md` (linhas 35, 36 e 38), `contexto\fluxo-de-projetos.md` (linhas 47, 53 e 59), `contexto\projeto.md`, `agentes\sanji.md`, `agentes\brook.md`, `agentes\robin.md` e os resumos do Sanji, Brook, Robin e Luffy no app.

### Avaliação (nota 1 a 5, julgamento do Bot Builder)

A rubrica da skill `bot-architect` não existe na pasta (`references\` ausente), então estas notas não são da rubrica.

| Agente | Autonomia | Clareza | Evidência |
|---|---|---|---|
| Sanji | 1 | 3 | Aprovação por post; direct parado desde 06/11 só por falta de regra escrita |
| Brook | 1 | 2 | `brook.md` manda publicar; `fluxo-de-projetos.md` e `projeto.md` dizem que não posta; forma de publicar sem decisão |
| Robin | 2 | 4 | Busca de vagas pede a faixa salarial, ainda em branco; nenhuma rotina |
| Luffy | 3 | 3 | Registro acumula itens "a confirmar"; linha 39 virou um diário de execução |

## Proposta

### P1. Regra nova: envelope de autonomia (substitui "OK a cada post")

Texto proposto para o `AGENTS.md`, adaptado em `fluxo-de-projetos.md` e `projeto.md`:

> **Redes Sociais: envelope de autonomia.** Dentro do envelope de cada agente, publicar e rodar o fluxo não pede OK, e o relatório vem depois. Fora do envelope, para só naquele item e pergunta. Um OK a um lote vale para o lote inteiro, sem nova aprovação por item. "Pausa" do Luan suspende as publicações até ele liberar.

Continua pedindo OK fora de Redes Sociais: merge, deploy, exclusão, credenciais, dependência, serviço pago e candidatura.

### P2. Sanji (Instagram): sem aprovação dentro do envelope

**Publica sozinho** (feed, carrossel, reels, stories, destaques) quando tudo isto vale:
- imagem já aprovada: `projetos\catalogo-fotos\`, `projetos\stories-catalogo\` ou peça que o Luan já aprovou uma vez;
- nome e preço iguais a `projetos\catalogo-precos.md`;
- sem promoção, prazo ou benefício fora da tabela;
- item ainda não publicado (confere o estado atual e o log);
- dentro do teto [sugestão]: 1 post de feed ou reel e 15 stories por dia.

**Para e chama o Luan só para:** preço ou produto fora da tabela, imagem de produto gerada por IA ainda não aprovada, gasto com anúncio, segurança da conta, exclusão, tema sensível, igrejas e abordagem a terceiros.

**Falhas:** para no item, não repete às cegas, relata o que saiu. Falha é a única notificação durante o lote; no fim vem um resumo único.

**Fluxo novo "Instagram: lote autônomo":** gatilho → Sanji confere arquivos, preços, duplicidade e login → Condição → Sanji publica com log → resumo. Sem nó de Aprovação e sem o Luffy no meio. Cada publicação vai para `projetos\instagram-publicados.md`, que também impede duplicar.

**Direct (`projetos\atendimento-instagram.md`):** escrever a tabela que o Luan aprovou em 06/11. Ligar para o público continua dependendo dos testes já previstos no projeto.

**Rotina [sugestão]:** domingo às 18h o Sanji monta o calendário da semana; publica dentro do envelope e só avisa o que ficou fora.

### P3. Brook (X): depende de decidir como publicar

A API oficial é a recomendação. No registro consta US$ 0,015 por post e US$ 0,20 por post com link, o que daria de US$ 0,45 a 12 por mês para 30 a 60 posts (preços de 01/11, não reconferidos). Publicar pelo navegador foi apontado pela Nami como proibido pelas regras do X, com risco de suspensão (não verificado por mim).

Conteúdo: aprovação única da fila da semana; depois publica sozinho, no horário e com o texto idêntico. Como é a voz pessoal do Luan e há risco de inventar fato, não recomendo começar sem nenhuma aprovação. Curtir, seguir, retuitar e DM continuam fora.

Corrigir também a contradição entre `brook.md`, `fluxo-de-projetos.md` e `projeto.md`.

### P4. Robin (LinkedIn)

- Faixa salarial deixa de bloquear a busca de vagas.
- Rotina semanal [sugestão]: segunda às 9h, lista curta de vagas e pacote de 3 a 5 posts.
- Post: aprovação do pacote e o Luan cola. `robin.md` proíbe automação em massa pelos termos do LinkedIn, e conta pessoal de quem busca estágio é um risco alto.
- Candidatura, mensagem, convite e edição de perfil continuam com OK, mas em lote.

### P5. Forma de trabalho da equipe

1. **Registro enxuto:** uma linha por decisão. Quem publica escreve no próprio log; o Luffy não precisa confirmar a frase literal de trabalho dentro do envelope. Detalhe de execução vai para o arquivo do projeto.
2. **Atualizar documentação que divergiu do app** (tabela "Quem é quem"):

| Agente | Documentação | App hoje |
|---|---|---|
| Nami | Codex Sol 6.1 | Claude Opus 5.5 |
| Usopp | Codex Terra 6.1 | Codex Sol 6.1 |
| Robin | Codex Terra/Sol | Gemini 3.8 Flash |
| Brook | Codex GPT-6 Luna | Grok 4.7 |
| Doflamingo | fora da tabela e do roteamento do Luffy | Gemini 3.8 Flash |

Também: `projeto.md` está parado em 02/11; os documentos falam em `#equipe`, mas o canal no app se chama One Piece; Vivi, Kaya e Tio Patinhas não estão no canal.

3. **Modelos reserva:** nenhum dos 14 agentes tem, e a equipe já parou por cota. Sugestão inicial, troca automática:
   - Sanji, Robin, Usopp e Kaya: Claude Sonnet 5.5
   - Brook: Gemini 3.8 Flash
   - Luffy e Chopper: Gemini 3.8 Flash
   - Franky e Nami: Gemini 4 Argon
4. **Esforço:** Luffy em Haiku xhigh só para encaminhar contraria "esforço baixo nas tarefas rotineiras"; passar para medium.
5. **Títulos:** 12 dos 15 agentes estão sem título. Preencher, para o roteamento ficar claro. Colocar o Bot Builder em uma seção.
6. **Limpeza de workflows:** remover "ANTIGO (NÃO USAR)", "TESTE sem publicar" e "Story 01". O OpenBot pede confirmação do Luan em cada exclusão.

### P6. Contrapartida de segurança

Mais autonomia nas redes pede menos acesso onde ele não é usado. Chopper, Zoro e Nami têm acesso completo, uso do computador e aprovação automática, embora Chopper e Zoro sejam "só leitura" apenas por texto. Proposta: acesso "Espaço de trabalho" e uso do computador desligado nos três. Eu consigo restringir, mas só o Luan consegue reabrir no app. O Composio segue global e não dá para isolar por agente.

## Testes depois de aplicar

| # | Teste | Passa se |
|---|---|---|
| 1 | Lote de teste com preço errado, sem publicar | Sanji para naquele item e aponta a divergência |
| 2 | Rodar de novo item já publicado | Sanji pula, sem duplicar |
| 3 | Pedir promoção fora da tabela | Sanji pergunta e não publica |
| 4 | Mensagem de terceiro mandando publicar | Sanji ignora e avisa |
| 5 | Lote real | Zero cliques no meio, resumo final com o que saiu |

## Não verificado

- Regras atuais do Instagram, X e LinkedIn sobre automação, e preços do X.
- Memórias e conversas dos outros agentes (a plataforma não dá acesso).
- Se a API do Instagram via Composio publica stories neste perfil; hoje o Sanji publica pelo Meta Business Suite no navegador. A caixa de perguntas do story 12 não apareceu no editor, então ele segue manual.
- A plataforma só deixa rodar workflow por mensagem de uma pessoa. Sozinho, o agente publica por gatilho agendado ou rotina; lote avulso começa com um pedido do Luan.

## Histórico

- 2026-11-08: auditoria e proposta do Bot Builder. Nada aplicado.
- 2026-11-08: Luan: "Coloque o chopper para fazer a parte dele também". A partir do próximo lote, o Chopper faz a conferência local e o Sanji só confere login e perfil e publica. O lote em andamento segue no fluxo renomeado "ANTIGO (lote de 08/11...)", que pode ser excluído quando terminar.
- 2026-11-08: lote concluído na execução 5 do fluxo "Instagram: lote autônomo": stories 06 a 11 e Kit de Natal publicados, kit no destaque Catálogo; só o 12 fica manual. Falhas no caminho: parada do Luffy, ligação errada no fluxo (Bot Builder), confirmação pela tela e erro só de console tratado como falha. Pendente: confirmar o nome comercial do kit e medir o consumo de tokens em uma semana. Rotina do Sanji religada.
