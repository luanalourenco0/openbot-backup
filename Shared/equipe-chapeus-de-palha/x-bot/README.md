# x-bot: fila de rascunhos para o X (@luanzeraAI)

Versão 0.1, 2026-11-01. **Não publica nada e não fala com o X.** O Brook (agente do OpenBot) escreve rascunhos no jeito do Luan, o script organiza a fila e valida o tamanho, e o Luan posta à mão (ou agenda no próprio X). Sem API, sem chave, sem `.env`, sem custo.

Por que sem API: em 2026 a API do X é paga por uso (post simples US$ 0,015, post com link US$ 0,20, fonte: docs.x.com). A publicação automática fica para quando houver verba; a fila já guarda os rascunhos no formato que ela vai precisar.

## Fluxo

1. O Brook cria rascunhos: `node src\cli.mjs novo --arquivo rascunho.txt`.
2. O Luan lê (`mostrar <id>`) e aprova (`aprovar <id>`) ou pede ajuste.
3. O Luan copia do `mostrar <id>` e posta no X (ou agenda no compositor do X; confira no X se o agendamento está disponível na sua conta).
4. O Luan marca `publicado <id> --url <link do post>`.
5. Tudo fica registrado em `logs\x-bot.jsonl` (data e hora, evento, id; nunca o texto nem credenciais).

## Comandos

Rode dentro desta pasta (`x-bot`). Precisa só do Node 22 ou mais novo.

| Comando | O que faz |
|---|---|
| `node src\cli.mjs novo --texto "..."` | Cria um rascunho. Também aceita `--arquivo caminho.txt` ou texto por stdin. Uma linha só com `===` separa os tweets de uma thread. |
| `node src\cli.mjs listar [pasta]` | Lista rascunhos, aprovados, publicados ou erros. |
| `node src\cli.mjs validar [id]` | Mostra o contador (peso/limite) de cada tweet. Sem id, confere todos os rascunhos. |
| `node src\cli.mjs mostrar <id>` | Texto pronto para colar, tweet por tweet, com contador. |
| `node src\cli.mjs aprovar <id>` | Move para aprovados. Se o rascunho é um texto só e passa de 280, divide em thread numerada "(1/3)". |
| `node src\cli.mjs publicado <id> [--url ...]` | Marca como publicado. Só funciona para rascunho aprovado. |
| `node src\cli.mjs erro <id> <motivo>` | Move para erros e guarda o motivo. |

Dica no PowerShell: para texto com acento, prefira `--arquivo` (UTF-8) a mandar por pipe, porque o PowerShell 5.1 pode estragar os acentos no pipe.

## Estrutura

```
x-bot/
  config.json        conta, limite de caracteres (280) e fuso
  voz/amostras.md    posts do Luan, para o Brook imitar o tom
  fila/              rascunhos, aprovados, publicados, erros (criadas sob demanda)
  logs/x-bot.jsonl   um evento por linha (fora do git)
  src/               cli, contagem, divisão em thread, fila, log
  test/              testes (npm test ou node --test)
```

Um rascunho é um `.md` com cabeçalho (`id`, `status`, datas) e os tweets separados por `===`.

## Voz (`voz\amostras.md`)

O arquivo guarda só as amostras, para o Brook imitar o tom: de 20 a 30 posts do Luan, um por bloco, separados por uma linha com `---`. Escolha os que soam mais como o Luan, não os que mais viralizaram. Abaixo dos posts, se quiser, acrescente palavras e expressões que ele usa muito e o que ele nunca escreveria.

Enquanto houver só o título no arquivo, ele está vazio: o Brook não inventa uma voz e pede as amostras. Com poucos posts ele já começa e ajusta o tom pelas correções do Luan.

## Regras

- Nenhum post sai sem o OK do Luan no texto ou na fila (decisão de 2026-11-08; ver `agentes\brook.md`). `aprovar` só roda nos rascunhos cobertos por esse OK.
- O script não fala com o X. Quem publica e lê a conta é o Brook, pelo navegador. Sem curtir, seguir, retuitar ou DM sem pedido.
- Contagem: link vale 23, emoji vale 2, acento vale 1. É uma aproximação do contador do X; confira no X se o tweet estiver no limite. Se a conta Premium aceitar posts longos, suba `limite` em `config.json`.
- Divisão automática só vale para rascunho de uma parte. Uma thread escrita pelo Brook não é reescrita: se um tweet passar do limite, `aprovar` recusa e explica.

## Quando entrar a API (depois, com verba e OK do Luan)

Um módulo novo lê os aprovados e posta com OAuth 1.0a, com `.env` fora desta pasta, dry-run por padrão, espera em erro 429 (no máximo 3 tentativas) e sem tentar de novo após timeout. Isso é um novo trabalho, com plano e aprovação próprios.

## Testes

`node --test` dentro desta pasta. Cobrem contagem, divisão em thread, fluxo da fila, log em ordem, recusa de id malformado e a trava que impede marcar como publicado sem aprovação.
