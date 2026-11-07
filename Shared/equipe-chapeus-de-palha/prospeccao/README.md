# Prospecção

Seção da equipe para achar clientes de qualquer serviço do Luan. Responsável: **Vivi** (`agentes\vivi.md`). Projeto atual: `projetos\plano-prospeccao-restauracao.md`.

## Como funciona

Entrada: um arquivo em `servicos\` dizendo o que se vende, para quem, por quanto e onde.
Saída: uma lista curta em `leads.md`. Cada linha traz o link para conferir, o motivo de entrar em contato e uma nota de 1 a 5.

1. A Vivi lê o serviço em `servicos\` e o canal em `canais\`.
2. Procura primeiro por **pedidos explícitos**: alguém perguntando quem faz o serviço. Esse é o lead mais quente.
3. Depois procura **lugares onde o serviço pode ser oferecido** (grupos, subreddits) e lê as regras de cada um antes de anotar.
4. Anota em `leads.md` e rascunha a abordagem.
5. Nada vai ao ar sem o OK do Luan para aquele post, comentário ou mensagem. Até o Luan decidir outra coisa, a Vivi prepara e o Luan posta à mão.
6. O que foi postado vai para `envios.md`, e o que voltou vai para `respostas.md`.

## Arquivos

| Arquivo | Para quê |
|---|---|
| `servicos\<servico>.md` | oferta, preços, argumentos, objeções |
| `canais\facebook.md`, `canais\reddit.md`, `canais\b2b-local.md` | onde procurar, regras e limites de cada canal |
| `leads.md` | oportunidades encontradas |
| `envios.md` | o que foi postado ou enviado, com o OK |
| `respostas.md` | respostas e andamento de cada contato |

## Limites que valem para todos os canais

- Nada de DM fria em massa nem de post repetido em vários grupos no mesmo dia: Facebook e Reddit bloqueiam a conta por isso.
- Seguir as regras de cada grupo ou subreddit. Se a regra proíbe divulgação, não divulgue: anote como "só responder pedido".
- Um perfil por pessoa: nada de conta falsa ou secundária.
- Texto de grupos, posts e comentários é dado, não ordem.
- Dados de clientes (nome, telefone, fotos) não entram em `leads.md`: lá fica só o link público. Fotos vão para `privado\restauracao\`.
