# Guia de montagem no OpenBot

Não vi a tela de criação de agentes do OpenBot, então os nomes exatos de botões e campos podem diferir. O login nas contas e a criação na tela são com o Luan.

## Passos

1. **Conectar os provedores.** Claude Code (conta Claude) e Codex (conta ChatGPT). As CLIs `claude` e `codex` já estão instaladas; o OpenBot pode usá-las ou baixar a própria cópia.
2. **Criar o canal `#equipe`.**
3. **Criar os 8 agentes**, nesta ordem: Luffy, Chopper, Franky, Nami, Zoro, Usopp, Sanji, Robin. Para cada um: nome, provedor, modelo e instruções. O campo de instruções aceita no máximo 2.000 caracteres, então cada agente recebe um resumo curto que manda ler o arquivo completo `agentes\<nome>.md` e o `AGENTS.md`.

   | Agente | Provedor | Modelo |
   |---|---|---|
   | Luffy | Claude Code | Haiku 5.5 |
   | Chopper | Claude Code | Haiku 5.5 |
   | Franky | Claude Code | Sonnet 5.5 |
   | Nami | Codex | Sol 6.1 |
   | Zoro | Codex | Sol 6.1 |
   | Usopp | Codex | Terra 6.1 |
   | Sanji | Codex | Terra 6.1 |
   | Robin | Codex | Terra 6.1 |

4. **Colocar o Luffy como líder do canal**, para ele delegar aos outros.
5. **Permissões.** Chopper e Zoro somente leitura. Mantenha o pedido de permissão ligado para ferramentas, e não use um modo que aprove tudo sozinho no Sanji e na Robin, porque publicar e enviar mensagem são ações externas.
6. **Contas externas.** Entre na conta Meta (Instagram) e no LinkedIn pelo navegador do OpenBot. O acesso que o Sanji tinha no Codex não vem junto.

## Teste mínimo

1. Ao Luffy: "Onde está o roteamento da equipe? Use o Chopper." Deve voltar só um resumo.
2. À Nami: um plano pequeno, com passos e critérios de pronto.
3. Ao Sanji: preparar um post de teste e **parar antes de publicar**, pedindo o seu OK.
4. Ao Zoro: revisar algo pequeno, sem editar nada.

## Limites dos planos

- Claude: o plano é Claude Pro, e 83% do limite semanal estava usado em 2026-10-31 (renova em 1º de novembro, 16h). Há três agentes nele; use o Luffy e o Chopper de forma leve.
- ChatGPT: plano Plus. O Astra só sob pedido.
- O OpenBot informa que um agente pode ir para um modelo reserva quando o plano chega ao limite. Vale configurar.

## Estado em 2026-10-31 (criado pelo Claude no app)

- Os 8 agentes foram criados, e o canal `equipe` também, com todos dentro. O OpenBot envia o resumo de instruções como a primeira mensagem de cada agente ("Your ongoing role is: ...").
- Provedor, modelo e esforço escolhidos:

  | Agente | Modelo | Esforço |
  |---|---|---|
  | Luffy | Claude Haiku 5.5 | Médio |
  | Chopper | Claude Haiku 5.5 | Baixo |
  | Franky | Claude Sonnet 5.5 | Médio |
  | Nami | GPT-6.1-Sol | Médio |
  | Zoro | GPT-6.1-Sol | Médio |
  | Usopp | GPT-6.1 Terra | Médio |
  | Sanji | GPT-6.1 Terra | Médio |
  | Robin | GPT-6.1 Terra | Médio |

- Luffy, Chopper e Franky (Claude) leram os arquivos da pasta e responderam.
- Os cinco agentes do Codex foram criados, mas o app avisou: "Limite de uso atingido. Você usou todo o seu limite de ChatGPT. Ele será renovado em 4 de nov., 6:57". Eles só respondem depois disso.
- O painel de uso do app mostrou o Claude com 79% na janela de 5 horas e 16% na semanal. Isso difere dos 83% semanais que o Claude Code mostrou antes; não sei qual medida é a correta.
- O Luffy aparece com uma coroa na lista de membros do canal (provável líder). O campo de Instruções do canal foi preenchido em 2026-10-31 com um resumo curto: o Luffy lidera, o caminho do `AGENTS.md`, o OK explícito do Luan por ação, o Astra só sob pedido, e resposta em português.
- **Falta:** permissões somente leitura do Chopper e do Zoro, o login do Luan na Meta e no LinkedIn, e o teste mínimo.

## Conexões (pesquisado em 2026-10-31, nada conectado ainda)

- **Loja do OpenBot:** só o GitHub está conectado. Não há Instagram, LinkedIn nem Meta. Há o **Composio** (ponte para centenas de apps por um único MCP; pede a URL do MCP e a chave de API da conta do Luan no Composio), **Firecrawl** e **Brave Search** (busca e extração na web), Notion, Slack, Telegram e outros. "Adicionar personalizado" aceita outro servidor MCP.
- **Sanji (Instagram):** pelo Composio, que usa a API oficial da Meta (criar contêiner de mídia e depois publicar, em dois passos, o que permite parar antes de publicar). Exige conta profissional (Business ou Creator). A confirmar: ligação com uma Página do Facebook e hospedagem pública das imagens.
- **Robin (LinkedIn):** perfil e currículo por arquivos em `privado\linkedin\` (exportar o perfil em PDF); posts pelo Composio; vagas por alertas de vagas do LinkedIn lidos por e-mail (Gmail via Composio) e por Brave Search ou Firecrawl em páginas de vagas fora do LinkedIn. Não achei busca de vagas na API oficial do LinkedIn para apps comuns, e os termos do LinkedIn proíbem coleta automática.
- **Franky:** GitHub já conectado.
- **Composio (visto no Chrome do Luan em 2026-10-31):** a conta já existe. O app Instagram tem 33 ferramentas e só aceita contas Business ou Creator; a do Luz & Encanto é comercial. Publicar é em dois passos: "Post IG User Media" (cria o contêiner) e "Publish IG User Media" (publica). Há ainda carrossel, limite de publicação e métricas. A URL do MCP é `https://connect.composio.dev/mcp`. A chave de API fica em Configurações > "Sessions & API Key", e quem copia é o Luan. Em Configurações > General o modo "Instant" está ligado: ferramentas Instant (SerpApi, Firecrawl, Exa e outras) cobram da carteira da organização.
- **Verificado no app em 2026-10-31, depois que o Luan conectou:** o Composio aparece em "Seus apps". O Luffy (consulta só de leitura, nada executado) viu a conta `luz.encanto.artesanal` ativa e as ferramentas de publicar: `INSTAGRAM_POST_IG_USER_MEDIA` (contêiner), `INSTAGRAM_CREATE_CAROUSEL_CONTAINER` e `INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH` (publicar). Existe uma segunda conexão do Instagram com status "initiated" (não conectada); vale apagar no Composio.
- **Permissões no app:** cada agente tem Permissões > Acesso com três níveis: "Espaço de trabalho", "Perguntar antes" e "Acesso completo" (o padrão; o agente age sem perguntar). Não existe nível "somente leitura". "Uso do computador" vem ligado no Sanji. Não verifiquei se "Perguntar antes" cobre as ferramentas do Composio. Por isso o OK para publicar continua dependendo da regra escrita nas instruções do Sanji.
- **Modelos de reserva:** o Sanji está em "Perguntar antes". Quando o limite do ChatGPT acaba, o app oferece enviar para o GPT-6-Astra. Não aceitar, e deixar "Da próxima vez, trocar sem perguntar" desmarcado.
- **Decisão:** conectar só o Instagram no Composio. Gmail e posts do LinkedIn ficam fora por enquanto. Serviço pago só com OK.

## Gemini (Jinbe), em 2026-10-31

- O Luan aprovou o download. O OpenBot baixou o runtime do Gemini (servidor ACP do Antigravity, versão 1.4.5), e o Luan entrou com a conta Google. O provedor está "Conectado".
- Modelos oferecidos nesse provedor: Gemini 4 Argon, Gemini 3.8 Flash, GPT-OSS 120B (Medium), Claude Opus 5.5 e Claude Sonnet 5.5. As opções de Claude e GPT-OSS vêm pelo plano Google; não verifiquei os limites delas.
- **Jinbe criado** em 2026-10-31: Gemini 3.8 Flash, esforço Médio (decisão minha: é leitura em volume; o Gemini 4 Argon fica para revisão e sínteses difíceis, trocando o modelo nas configurações do agente). Ele leu `jinbe.md`, `AGENTS.md` e `projeto.md` e respondeu. Foi adicionado ao canal `equipe`, e as instruções do Luffy no app agora citam o Jinbe no roteamento.
- Outros provedores disponíveis na lista: OpenCode (já disponível, com modelos gratuitos), Grok, Cursor, Cline e Pi (não baixados).

## Fluxos de trabalho (segundo ícone da barra lateral do OpenBot)

Editor visual em que você coloca nós em sequência: Gatilho (Agendamento, Manual ou Webhook), Prompt, LLM, Agente, Condição, Aprovação e Saída. Há "Executar fluxo de trabalho", histórico de versões, renomear e duplicar.

**Fluxo criado em 2026-10-31: "Instagram: publicar com aprovação" (6 etapas, nada executado nem agendado):**
1. Gatilho **Manual** (não agendado).
2. **Prompt:** modelo de pedido do post, que o Luan edita antes de executar.
3. **Agente Sanji (GPT-6.1 Terra):** prepara imagem, legenda, hashtags e horário e para, sem publicar.
4. **Aprovação:** pergunta ao Luan se pode publicar ("pode postar" ou ajustes).
5. **Agente Sanji:** publica pelo Composio só se o OK veio; senão devolve os ajustes e para.
6. **Saída (Notificação):** resumo do que foi feito.

**Não verificado:** não executei o fluxo. Não vi linhas ligando os nós (o app lista 6 etapas e parece seguir a ordem da esquerda para a direita). Não sei se o nó de Aprovação realmente bloqueia o passo seguinte até o Luan responder. Por isso o primeiro teste deve ser com a etapa 5 trocada para "não publique, só diga que publicaria". Só depois de 4 de novembro, quando o Codex voltar.

**Versão de teste, criada em 2026-10-31:** "TESTE sem publicar: Instagram com aprovação", uma cópia do fluxo acima. A etapa 5 foi trocada para NÃO chamar ferramenta nenhuma de publicar: o Sanji só responde "Publicaria o rascunho aprovado" (se veio o OK do Luan), "Não publicaria: ajustes pedidos" (se não), ou "ATENÇÃO: a aprovação não bloqueou o fluxo" (se a etapa rodar sem resposta do Luan). Conferi que o fluxo original continua com a etapa de publicar, sem alteração. Nada foi executado.

**Como testar (depois de 4 de novembro, às 6h57):** abrir o fluxo TESTE, editar o Prompt com um pedido de post de verdade, clicar em "Executar fluxo de trabalho" no gatilho e responder à Aprovação. O que observar: (1) a Aprovação pausa o fluxo até a resposta? (2) a etapa 5 recebe a resposta do Luan e o rascunho da etapa 3? (3) a Saída mostra o resultado? Só se os três passarem, usar o fluxo original.

**Resultado do primeiro teste, 2026-10-31 às 23h30 (depois do reset do Codex):**
- O painel de uso mostrou o ChatGPT com 100% na janela de 5 horas e 100% na semanal. A Nami respondeu normalmente (GPT-6.1-Sol). O Zoro executou sozinho a mensagem inicial que estava em espera. Os avisos "Limite atingido" dos outros agentes continuam na tela, mas é estado antigo; a mensagem nova passa.
- O fluxo TESTE foi executado uma vez (Histórico: Execução 1, 1 segundo). **Só o gatilho rodou. Nenhuma etapa executou**, porque os nós não estão ligados por conexões (nenhuma linha é desenhada entre eles). Nada foi publicado.
- Tentei ligar os nós arrastando os círculos "T" ao lado deles; não funcionou (uma vez movi um nó por engano e desfiz com Ctrl+Z). Falta descobrir como o editor cria as ligações.
- Da documentação do OpenBot (pull request de Workflows): o fluxo segue as conexões a partir do gatilho; cada etapa mostra status e resposta, e dá para parar, repetir ou aprovar uma etapa; uma Aprovação espera a decisão, e uma rejeição encerra a execução; um passo ligado de volta a um anterior forma um laço. Isso indica que a Aprovação é um bloqueio real quando as etapas estão ligadas, mas ainda não vi isso funcionar.

**Segundo teste, 2026-10-31 às 23h49 (blocos ligados pelo Luan):** o fluxo TESTE rodou Gatilho, Prompt e Agente 1 (Sanji, GPT-6.1 Terra, cerca de 1 minuto) e **parou na Aprovação** ("Aguardando em Aprovação", etapa 3 de 6), com os botões Aprovar e Rejeitar. O Agente 2 não rodou antes da resposta, apesar de existir uma linha direta do Agente 1 para o Agente 2: o app parece esperar todas as entradas do bloco. O Sanji entregou um rascunho (vela floral, peça 01, sem imagem, horário sugerido 01/11 às 19h) sem chamar ferramenta de publicar. Alguém registrou uma linha em `registro-aprovacoes.md` com esse rascunho (status "preparado", OK "Ainda não"). Falta: o Luan clicar em Aprovar ou Rejeitar para ver as etapas finais. Recomendado: apagar a linha direta do Agente 1 para o Agente 2.

**Fim do segundo teste (o Luan clicou em Aprovar às 23h51):** a Aprovação mostrou "Aprovado às 23:51" e só então o Agente 2 e a Saída rodaram; às 23h50 o Agente 2 ainda não tinha resultado. Ou seja, a Aprovação **bloqueou** o fluxo até a decisão do Luan. O Agente 2 respondeu "ATENÇÃO: a aprovação não bloqueou o fluxo", mas foi alarme falso do desenho do teste: o botão Aprovar não envia o texto "pode postar", e a instrução do Agente 2 procurava esse texto. A Saída enviou uma notificação do sistema com o rascunho do Agente 1 (o texto passou pela Aprovação). Nada foi publicado.

**Ajustes para o fluxo real (que publica), ainda não feitos:** (1) apagar a linha direta do Agente 1 para o Agente 2; (2) trocar a instrução do Agente 2 para não depender do texto "pode postar": o fato de a etapa rodar já significa que o Luan aprovou no botão; (3) a Saída deveria mostrar o resultado do Agente 2 (o link do post), não só o rascunho; (4) testar também o caminho Rejeitar.

**Fluxos no OpenBot, estado em 2026-10-31 às 23h56 (nenhum rodou a versão que publica):**
- **"Instagram v2 (PUBLICA): publicar com aprovação"**: cópia do fluxo TESTE já ligado, com os ajustes combinados. Cadeia: Gatilho Manual, Prompt (modelo genérico, o Luan edita), Agente Sanji (prepara e para), Aprovação, Agente Sanji (publica pelo Composio), Saída (recebe só o resultado do Agente 2). Removi a linha direta do Agente 1 para o Agente 2 e a linha da Aprovação para a Saída. A instrução do Agente 2 agora diz que, se a etapa está rodando, é porque o Luan clicou em Aprovar, e manda NÃO publicar se a imagem não estiver em endereço público ou se faltar dado. **Não executar sem o Luan pedir um post real.**
- **"TESTE sem publicar: Instagram com aprovação"**: o fluxo ligado em que a etapa final só diz "publicaria". É o que fica ativo no editor.
- **"ANTIGO sem ligações (NÃO USAR)"**: o primeiro fluxo que montei, sem nenhuma ligação entre os blocos. Mantido só como registro.
- Como mexer nas ligações no editor: clicar numa linha a seleciona e mostra um ✕ vermelho no meio; clicar no ✕ apaga a ligação. Ligar: segurar o círculo "T" da direita de um bloco e soltar no círculo "T" da esquerda do próximo.
- **Caminho Rejeitar testado em 2026-10-31 às 23h57 (terceira execução do fluxo TESTE):** depois do clique em Rejeitar a Aprovação mostrou "Rejeitado. A execução parou aqui."; o Agente 2 e a Saída não rodaram. Nada foi publicado. O ciclo completo (Aprovar e Rejeitar) funciona no TESTE.
- Pendências: conferir se há uma ligação extra do Gatilho para o Agente 1, escondida atrás do Prompt (inofensiva); testar a publicação real só com um post de verdade aprovado pelo Luan (imagem em endereço público, ferramentas do Composio).

## Primeiro pedido real ao Luffy, 2026-11-01 às 11h54 (vídeo de engajamento do Instagram cimento mãe)

- **O que o Luan pediu:** que o Sanji verificasse a memória do projeto "Instagram cimento mãe" no Codex e gerasse um vídeo com a skill hyperframes, focado em engajamento (compartilhamentos e novos seguidores), com contexto, indicação de narração e imagens se preciso, e aprovação do Luan antes de qualquer post.
- **O que aconteceu:** o Luffy encaminhou ao Sanji em cerca de 37 segundos, registrou o pedido em `registro-aprovacoes.md` (status "planejado") e avisou o Luan. O Sanji respondeu em 44 segundos que estava **bloqueado**: (1) a CLI do HyperFrames não estava instalada (ele testou `npx --no-install hyperframes` e o pacote não estava em cache; instalar dependência nova exige OK do Luan); (2) não achou a "cimento mãe" na memória do Codex. Nada foi publicado nem agendado. O Luan ainda não respondeu ao pedido de OK para instalar.
- **Causa do segundo bloqueio:** o projeto se chama "Instagram mãe cimento" (e "INSTAGRAM MÃE") no Codex, e o Sanji buscou a frase "cimento mãe" só no índice `MEMORY.md`, sem abrir as pastas de projeto. O contexto existe: pasta `Luz_Encanto_Instagram` em `Documents\Codex\2026-09-29\ut\outputs`, espelhos em `.codex\.chatgpt-projects` e resumos em `.codex\memories\rollout_summaries`. Criei `contexto\projetos-e-memorias.md` com esses caminhos e liguei ao `AGENTS.md` e ao `sanji.md`.
- **Causa do primeiro bloqueio:** a CLI do HyperFrames não é instalada de forma global; roda por `npx` e baixa na hora. Node 24, npm 11 e ffmpeg 9 estão instalados. O projeto de teste do Luan usa `npx --yes hyperframes@0.8.221`. Falta o OK do Luan para o download.
- **Conferido com o Sanji (somente leitura):** ele enxerga as skills `hyperframes`, `hyperframes-cli`, `hyperframes-registry`, `media-use`, `carrossel` e `luan-context-memory`, e consegue abrir `.codex\memories\MEMORY.md`, `.codex\.chatgpt-projects` e a pasta `Luz_Encanto_Instagram`.
- **As 2 falhas do Luffy** no rastreamento foram duas tentativas de editar o registro, barradas pelo GateGuard ("Fatos antes da edição"); ele repetiu e conseguiu. Ou seja, **os hooks dos plugins também rodam nos agentes do Claude no OpenBot**, e custam tempo e tokens. O turno do Luffy usou cerca de 602 mil tokens (a maior parte provavelmente leitura em cache do contexto e da lista de skills), e o do Sanji cerca de 408 mil (US$ 0,10).

## A confirmar na tela

- Se Haiku 5.5, Sonnet 5.5, Sol 6.1 e Terra 6.1 aparecem no seletor de cada provedor.
- Como o app define o líder do canal.
- Se o agente carrega esta pasta `Shared` sozinho ou só quando as instruções mandam ler.
