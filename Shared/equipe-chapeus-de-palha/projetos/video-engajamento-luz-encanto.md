# Projeto: vídeo de engajamento do Instagram Luz & Encanto

Status: ativo
Atualizado em: 2026-11-02
Dono: Luan. Condutor: Luffy. Executa: Sanji.
Regras de delegação e entrega: `contexto\fluxo-de-projetos.md`.

## Objetivo

Um vídeo para o Instagram Luz & Encanto focado em engajamento (compartilhamentos e novos seguidores), usando a memória do projeto "Instagram mãe cimento" no Codex e a skill `hyperframes`. Narração e imagens conforme o Sanji decidir; criar o vídeo e gerar imagens está autorizado.

## Pronto quando

O Luan aprova uma versão do vídeo. Publicar é outra decisão, com OK próprio e dentro do Workflow com Aprovação.

## Etapas

| # | Etapa | Responsável | Status | Evidência |
|---|---|---|---|---|
| 1 | Encaminhar o pedido e registrar | Luffy | feito | registro de 2026-11-01 |
| 2 | Achar o contexto do projeto no Codex | Sanji | feito | `contexto\projetos-e-memorias.md` |
| 3 | HyperFrames disponível por `npx` | Sanji | feito | `npx --yes hyperframes@0.8.221 --version` retornou 0.8.221 |
| 4 | Versão v1 (foto real, 12 s) | Sanji | reprovada pelo Luan | `luz-encanto.mp4` |
| 5 | Versão v2 (três fotos reais, movimento e trocas de cena) | Sanji | aguardava avaliação | `luz-encanto-motion-v2.mp4` |
| 6 | Conceito "O detalhe muda tudo" (ilustração animada, sem fotos nem áudio) | Sanji | aguardava avaliação | `detalhe-loop.mp4` |
| 7 | Versão v3 (escrita animada, cenário ilustrado em etapas) | Sanji | preparada | `detalhe-motion-v3.mp4` |
| 8 | Avaliação do Luan | Luan | pendente | |
| 9 | Publicação | Sanji, via Workflow com Aprovação | não autorizada | |

Os arquivos ficam em `agents\agent-03dd6eb7-f445-404d-911e-310af56b0a42\luz-video\`, dentro da pasta do OpenBot.

## Agora

A v3 está pronta (12 s, sem áudio nem fotos; quadros revisados, duração e decodificação conferidas). Aguardando: a avaliação do Luan.

## Próximo passo

O Luan aprova, pede mudanças ou reprova a v3.

## Aguardando OK do Luan

- Avaliação da v3.
- Publicação (nada foi publicado nem agendado).
- Confirmar os três OKs que o Sanji relatou e o Luffy não viu (ver "Decisões do projeto").

## Decisões do projeto

- 2026-11-01: criar o vídeo e gerar imagens autorizados. Frase do Luan: "Peça pro Sanji verificar a memória ... gerar um vídeo pela skill hyperframes ... caso ele precisse gerar imagens, também está autorizado".
- 2026-11-01: o Luan disse ter respondido direto no chat do Sanji a três autorizações: instalação do HyperFrames, uso de fontes Google e download do componente `panel-reveal`. Frases relatadas pelo Sanji, não vistas pelo Luffy: HyperFrames "Sim, autorizo" (01/11, 12h03); fontes "Autorizar e continuar" e `panel-reveal` "Autorizar download" (horários exatos não confirmados, perguntas feitas às 12h08 e 12h36 de 01/11). A confirmar.
- Publicação: não autorizada.

## Histórico

- O pedido foi enviado ao Sanji em 2026-11-01 (entrega em fila).
- 1ª resposta do Sanji: bloqueado, CLI do HyperFrames ausente, pediu OK de instalação.
- 2ª resposta: parcial. O `npx --yes hyperframes@0.8.221 --version` retornou 0.8.221 e o projeto inicial ficou em `luz-video`.
- 3ª mensagem: o Sanji afirmou que o Luan autorizou `hyperframes@0.8.221` via `npx --yes` e seguiu sem novo OK.
- 4ª mensagem: bloqueado. A composição de 12 s usa foto real. O HyperFrames baixou fontes Google fora do escopo (EB Garamond e Inter, cache de 2.157.544 bytes). O Sanji interrompeu e aguardou a decisão do Luan.
- 5ª mensagem: rascunho vertical de 12 s renderizado em `luz-encanto.mp4` (ffprobe: 12 s, 360 quadros; FFmpeg decodificou sem erro; reprodução em player não conferida). Sem narração, sem imagens geradas, sem publicação. O Luan reprovou a v1.
- 6ª mensagem: v2 com três fotos reais, movimento e trocas de cena, 12 s em 9:16, em `luz-encanto-motion-v2.mp4`; duração e decodificação verificadas; sem áudio.
- 7ª mensagem: conceito "O detalhe muda tudo", ilustração animada, 12 s, sem fotos nem áudio, em `detalhe-loop.mp4`; FFmpeg decodificou sem erro e o ffprobe confirmou a duração.
- 8ª mensagem: nova versão após pedido do Luan, `detalhe-motion-v3.mp4`, com escrita animada e cenário ilustrado em etapas, 12 s, sem áudio nem fotos; quadros revisados, duração e decodificação conferidas. Nada publicado nem agendado.
