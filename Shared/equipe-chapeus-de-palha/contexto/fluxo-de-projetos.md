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
- **Conteúdo para publicar:** Sanji, Robin ou Brook escrevem o rascunho, o Luan aprova cada peça, e só então ela é publicada (ver "Publicar").
- **Pesquisa:** Chopper ou Jinbe (ver "Leitura") devolvem o resumo a quem pediu.

## OKs do Luan

- Um OK vale só para a ação em que foi dado.
- Quando o Luan der um OK direto a um agente, o agente cola a frase exata e a hora no relatório. O Luffy copia no registro com a marca "visto no relato do <agente>".
- Sem a frase exata, o registro diz "a confirmar", e o Luffy pergunta ao Luan antes de liberar a próxima ação que dependa desse OK.

## Publicar

Tudo que publica ou envia por ferramenta (post, mensagem, candidatura) roda dentro de um Workflow com nó de Aprovação. Testado em 2026-10-31: a Aprovação bloqueia o fluxo até o Luan decidir, e Rejeitar encerra a execução. A regra escrita nas instruções do agente é o segundo cinto, não o primeiro.

Hoje só o Sanji publica por ferramenta (Instagram, pelo Composio), no Workflow "Instagram v2 (PUBLICA): publicar com aprovação". A Robin não publica: o Luan posta à mão. O Brook lê a conta @luanzeraAI pelo navegador do OpenBot e só posta com permissão a cada post, pelo Workflow com Aprovação (ainda não existe; até lá não posta). Se a Robin ganhar uma ferramenta de publicar, o Workflow com Aprovação é criado antes de a ferramenta ser usada.

## Leitura: Chopper ou Jinbe

- **Chopper (Claude Haiku):** busca pontual e curta em arquivos locais ("onde está X", "o que diz este trecho").
- **Jinbe (Gemini):** o que é grande ou externo: web, PDFs, vídeos, repositórios inteiros, pesquisa de empresas, vagas e tendências.
- Com o plano Claude perto do limite, a leitura local também vai para o Jinbe.

## Reescrever ou planejar

O Luffy reescreve o pedido em uma frase com critério de pronto. Ele não faz plano. Plano em passos, com riscos e pontos de OK, é da Nami.
