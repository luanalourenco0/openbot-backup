# Projeto: bot do X (@luanzeraAI)

Status: ativo
Atualizado em: 2026-11-02
Dono: Luan. Condutor: Luffy. Executa: Brook.
Regras de delegação e entrega: `contexto\fluxo-de-projetos.md`.

## Objetivo

Rascunhos de tweets e threads no jeito do Luan, 1 a 2 por dia, com fila, contador de caracteres, divisão em thread e log. O Luan posta à mão. Sem API, sem chave e sem custo. Detalhes em `x-bot\README.md`.

## Pronto quando

O Luan posta no X, à mão, ao menos um rascunho escrito pelo Brook com a voz dele, e o ciclo (rascunho, aprovado, publicado) aparece no log.

## Etapas

| # | Etapa | Responsável | Status | Evidência |
|---|---|---|---|---|
| 1 | Plano (opções de acesso ao X, custo e risco) | Claude Code | feito | decisão de 2026-11-01 em `contexto\decisoes.md` |
| 2 | Bot v0.1 (fila, contagem, thread, log) | Claude Code | feito | 19 testes passando, `x-bot\test\` |
| 3 | Agente Brook criado no app | Claude Code | feito | `agentes\brook.md`; Codex, GPT-6 Luna (o app mostra Luna; o Luan decidiu deixar em 2026-11-02), esforço Médio |
| 4 | Amostras de voz | Claude Code, a pedido do Luan | feito em 2026-11-05; autoria confirmada pelo Luan | `x-bot\voz\amostras.md` e `x-bot\voz\guia.md` |
| 5 | Primeiros rascunhos pelo Brook | Brook | pendente | |
| 6 | Revisão do código | Zoro | pendente | |
| 7 | Brook no canal `#equipe` | Luan ou Claude Code | pendente | |
| 8 | Primeiro post feito à mão | Luan | pendente | |
| 9 | Publicação pela API | | fora do escopo | sem verba; exige novo plano e OK |

## Agora

Aguardando: o Luan mandar as amostras de voz (o Luan disse que envia quando tiver uma amostragem boa). Para os 3 primeiros rascunhos o Brook também precisa de 3 tópicos, tom ou objetivo por tópico, temas a evitar, exemplos de tweets que o Luan gosta ou não, e correções de formato (lista do Brook em 2026-11-02; com poucas amostras ele já começa).

## Próximo passo

O Luan manda os posts ao Brook. Até lá o bot fica pronto e parado.

## Aguardando OK do Luan

Nada no momento.

## Decisões do projeto

- 2026-11-01: sem verba para a API do X (paga por uso). O Premium do Luan não substitui a API. Sem `.env` e sem chaves.
- 2026-11-02: sem 20 posts, o Luan começa com poucos e vai mandando; o Brook ajusta o tom pelas correções.
- 2026-11-02: o Brook salva sozinho em `x-bot\voz\amostras.md` os posts que o Luan mandar no chat como sendo dele. Frase do Luan: "Sim, pode salvar". Regra em `agentes\brook.md`.

## Não verificado

- Se o agendamento do compositor do X está disponível na conta do Luan.
- Se o Premium aceita posts longos pela interface (`limite` em `x-bot\config.json`).
- A contagem de caracteres é uma aproximação do contador do X.
- Regras do X para contas automatizadas (a página não foi encontrada).
