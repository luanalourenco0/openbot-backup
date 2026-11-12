# Fluxo de projetos e delegação

Criado em 2026-11-02, a pedido do Luan ("Faça todas"). Vale para todos os agentes. O resumo está no `AGENTS.md`.

## Pedido ou projeto

- **Pedido:** uma ação, um agente, resolvido no mesmo dia. Vai só para o `registro-aprovacoes.md`.
- **Projeto:** mais de um passo, mais de um agente ou mais de um dia. Ganha um arquivo em `projetos\<nome>.md`, a partir de `projetos\_modelo.md`. O Luffy cria e mantém; o Luan também pode editar.
- O arquivo do projeto é o **estado vivo**: etapa atual, quem executa, quem aguarda quem, próximo passo. O registro guarda só decisões e OKs, uma linha cada, citando o projeto.
- Quando o Luan perguntar "onde estamos", o Luffy lê só os projetos com status ativo, não o histórico.
- Projeto encerrado vira "concluído" e o Luffy deixa de lê-lo.

## Delegação (Luffy para o agente)

Mensagem curta, com estes campos:

1. **Projeto:** nome do arquivo em `projetos\`, ou "pedido avulso".
2. **Objetivo:** uma frase.
3. **Pronto quando:** o critério verificável.
4. **Contexto:** os arquivos ou pastas necessários, nada além. Cite sempre pelo nome: o agente não lê tudo sozinho nem recebe a conversa ou as memórias de outro agente. Vale também depois de trocar de modelo ou de um tempo parado, porque o modelo novo não recebe a conversa inteira.
5. **Não fazer:** o que está fora do escopo.
6. **Entrega:** formato e onde salvar.
7. **Depende de OK do Luan?** Sim ou não, e qual ação.

## Entrega (agente para o Luffy)

1. **Status:** feito, parcial ou bloqueado.
2. **O que foi feito.**
3. **Evidência:** `arquivo:linha`, saída de comando ou caminho do arquivo gerado.
4. **O que não foi verificado.**
5. **Bloqueio ou pergunta:** no máximo uma.
6. **Próximo passo sugerido.**
7. **OKs que o Luan deu direto a você:** a frase exata e a hora. Se não houve, escreva "nenhum".

## Documentos de trabalho

- **Um dono por documento principal.** Só um agente atualiza o relatório ou texto principal. Os outros entregam pesquisa ou revisão em arquivos separados, para ninguém sobrescrever o trabalho do outro. Se o dono não estiver claro, pergunte ao Luffy. As regras próprias do `contexto\` e dos projetos continuam valendo.
- **Nova versão com data.** Ao revisar um relatório ou texto importante, salve um arquivo novo com a data, mantenha o anterior e liste o que mudou. Isso não vale para código (o git cuida), registros, listas e arquivos de estado vivo, nem aprova nada: a aprovação continua sendo do Luan.

## Quem passa o bastão

O agente não delega ao seguinte por conta própria: devolve ao Luffy, que encadeia e registra. O Luan pode falar direto com qualquer agente quando quiser.

Cadeias fixas:

- **Código:** Nami (plano, se não for trivial), OK do Luan ao plano, Franky implementa em branch própria, Zoro revisa, Usopp testa quando houver app, Luan decide o merge. Quem escreve não revisa.
- **Conteúdo para publicar:** segue o envelope de autonomia do `AGENTS.md`. Sanji publica sozinho dentro das regras; Brook e Robin publicam depois de um OK no lote (ver "Publicar").
- **Pesquisa:** Chopper ou Jinbe (ver "Leitura") devolvem o resumo a quem pediu.
- **Prospecção e restauração (Vendas):** Vivi acha o cliente e rascunha a abordagem, o Luan dá o OK por envio e, até decidir outra coisa, posta ele mesmo à mão; a Vivi registra em `prospeccao\`. Cliente fechado manda as fotos: Kaya restaura, Zoro revisa traço por traço (reserva: Jinbe; a Kaya nunca revisa a própria restauração), o Luan aprova o lado a lado e só então a entrega vai ao cliente. Detalhes: `agentes\vivi.md` e `agentes\kaya.md`.

## OKs do Luan

- Um OK vale só para a ação em que foi dado. Um OK a um lote de redes sociais vale para o lote inteiro.
- Publicação dentro do envelope não gera linha em `registro-aprovacoes.md` nem pede a frase do Luan: fica no log de quem publicou (`projetos\instagram-publicados.md`, fila do `x-bot\`, arquivo de posts da Robin). O registro guarda uma linha por decisão; detalhe de execução vai para o arquivo do projeto.
- Quando o Luan der um OK direto a um agente, o agente cola a frase exata e a hora no relatório. O Luffy não enxerga esse chat: ele confia no relato, copia a frase no registro com a marca "visto no relato do <agente>" e segue, sem mandar parar e sem perguntar ao Luan. Hora faltando vira "hora não informada" e não bloqueia nada.
- O Luffy só pergunta ao Luan quando o relato não traz a frase, ou quando a frase não cobre a ação feita (outro alvo, outro canal, mais itens do que o pedido). Aí o registro diz "a confirmar", ele pergunta uma vez e deixa parado só o que depende da resposta.

## Publicar

Dentro do envelope de autonomia do `AGENTS.md`, publicar não pede aprovação por etapa. A candidatura da Robin entra no envelope: um OK no lote e ela envia pelo navegador. Fora dele (mensagem a terceiros, post fora das regras), o que publica ou envia por ferramenta roda dentro de um Workflow com nó de Aprovação. Testado em 2026-10-31: a Aprovação bloqueia o fluxo até o Luan decidir, e Rejeitar encerra a execução.

- **Sanji:** lote avulso no Workflow "Instagram: lote autônomo (sem aprovação)". O que fica fora das regras usa o "Instagram v2 (PUBLICA): publicar com aprovação".
- **Brook:** o Luan dá um OK na fila da semana; a rotina diária publica pelo navegador, um post por execução.
- **Robin:** o Luan dá um OK no pacote de posts; ela posta pelo navegador, onde o LinkedIn está logado.

## Leitura: Chopper ou Jinbe

- **Chopper (Claude Haiku):** busca pontual e curta em arquivos locais ("onde está X", "o que diz este trecho").
- **Jinbe (Gemini):** o que é grande ou externo: web, PDFs, vídeos, repositórios inteiros, pesquisa de empresas, vagas e tendências.
- Com o plano Claude perto do limite, a leitura local também vai para o Jinbe.

## Reescrever ou planejar

O Luffy reescreve o pedido em uma frase com critério de pronto. Ele não faz plano. Plano em passos, com riscos e pontos de OK, é da Nami.
