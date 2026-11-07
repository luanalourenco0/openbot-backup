# Projeto: Prospecção + Restauração de Fotos

Status: ativo (fase 1 feita, aguardando criação dos agentes no app)
Atualizado em: 2026-11-06
Dono: Luan. Condutor: Luffy.
Regras de delegação e entrega: `contexto\fluxo-de-projetos.md`.
Origem: post @condzxyz (restauração de foto antiga com IA, ~R$ 100) + recurso de prospecção local do OpenBot (post @OpenBot_, 06/11).

## Objetivo

Criar a seção de Prospecção da equipe (serve para qualquer serviço) e um agente que restaura fotos antigas sem alterar a pessoa, com a restauração como primeiro serviço a vender no Facebook e no Reddit.

## Pronto quando

3 restaurações de fotos da família do Luan aprovadas sem alteração de traços (fase 2) e a primeira venda ou 10 grupos testados no Facebook (fase 4).

## Etapas

| # | Etapa | Responsável | Status | Evidência |
|---|---|---|---|---|
| 0 | Aprovar o plano | Luan | feito | registro-aprovacoes.md, 2026-11-06 |
| 1 | Criar estrutura, fichas dos agentes e ferramenta lado a lado | Claude Code | feito | `prospeccao\`, `agentes\vivi.md`, `agentes\kaya.md`, `ferramentas\lado-a-lado.py` |
| 1b | Revisão independente dos textos | Zoro | planejado | |
| 1c | Criar Vivi e Kaya no app OpenBot | Claude Code | feito | Criadas em 2026-11-06 ~14h55: Vivi (Gemini 3.8 Flash, esforço médio) e Kaya (GPT-6.1 Terra, esforço médio). Limite do ChatGPT esgotado, renova em 07/11 às 23h28: a Kaya só responde depois disso |
| 2 | Teste da Kaya com 3–5 fotos antigas da família do Luan | Kaya + Zoro + Luan | planejado | `privado\restauracao\teste-*` |
| 3 | Portfólio antes/depois (só fotos da família, com OK) | Sanji rascunha | planejado | |
| 4 | Prospecção Facebook, campanha de Natal | Vivi + Luan posta | planejado | `prospeccao\leads.md` |
| 5 | Reddit (volume/portfólio) + parceiros B2B | Vivi | planejado | |

## Agora

Fase 1 feita. Aguardando: revisão do Zoro e criação dos dois agentes no app.

## Próximo passo

Decisão do Luan (2026-11-06): a operação começa quando a cota do ChatGPT renovar (07/11, 23h28). Nesse dia:
1. Luan confere se a aprovação automática da Vivi e da Kaya está desligada.
2. Kaya: fase 2, com 3 a 5 fotos antigas da família em `privado\restauracao\teste-*`.
3. Vivi: em paralelo, primeira busca no Facebook (pedidos explícitos + 10 grupos avaliados), só leitura e rascunhos, para a campanha de Natal.

## Aguardando OK do Luan

- Conferir no app se a aprovação automática da Vivi e da Kaya está desligada (no Tio Patinhas ela veio ligada).
- Fotos da família para o teste da fase 2 (Kaya funciona a partir de 07/11, 23h28).

## Para o Luffy registrar (registro-aprovacoes.md)

| 2026-11-06 | Criar a seção de Prospecção e os agentes Vivi (prospecção) e Kaya (restauração de fotos): arquivos, fichas e `ferramentas\lado-a-lado.py`. Projeto: `projetos\plano-prospeccao-restauracao.md` | Claude Code | Sim, plano novo; criar agentes no app pede OK próprio | "Ajustando esses pontos, pode seguir." e, para criar no app, "Você que vai criar." (Luan no chat com o Claude Code, 2026-11-06) | Arquivos em `prospeccao\`, `agentes\vivi.md`, `agentes\kaya.md`, `privado\restauracao\LEIA.md`; ferramenta testada com imagens sintéticas. Agentes ainda não criados no app; revisão do Zoro pendente | preparado |

## Decisões do projeto

- 2026-11-06: prospecção sem limite de cidade. Venda digital para o Brasil todo; quadro impresso só onde houver gráfica parceira (começa pelo Alto Tietê).
- 2026-11-06: Reddit é canal de volume e portfólio, não de margem (Luan ciente).
- 2026-11-06: Vivi (prospecção) no Gemini 3.8 Flash, assinatura Gemini Pro. Reserva: Codex Terra 6.1, se o Gemini não conseguir usar o navegador logado no Facebook/Reddit dentro do OpenBot.
- 2026-11-06: Kaya (restauração) no Codex Terra 6.1 com a geração/edição de imagem da OpenAI (assinatura GPT Plus). Reserva: o Nano Banana mais recente disponível no Gemini Pro. Higgsfield fora por enquanto.
- 2026-11-06: privacidade aprovada: fotos de clientes em `privado\restauracao\`, apagadas 30 dias após a entrega; portfólio só com autorização escrita do cliente.
- 2026-11-06: quem prospecta não restaura, e quem restaura não revisa a própria restauração (revisor: Zoro; reserva: Jinbe).

## Preços

| Serviço | BRL | USD (exterior) |
|---|---|---|
| Restauração simples | R$ 100 | US$ 20 |
| Dano pesado (rasgo, mancha, parte faltando) | R$ 150–200 | US$ 35–45 |
| Colorização (adicional) | + R$ 40 | + US$ 10 |
| Quadro impresso | custo da gráfica + margem | não oferecer (só digital) |

Detalhes da oferta: `prospeccao\servicos\restauracao-fotos.md`. Canais: `prospeccao\canais\`.
