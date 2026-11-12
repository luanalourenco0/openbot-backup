# Editor de vídeo

Responsável: Bon Clay (`agentes\bon-clay.md`). Referência do método: Matheus Gobbi, "Editar vídeo com o Claude" (matheusgobbi.com/edit, 2026-11-10).

## Pastas

| Pasta | Para quê |
|---|---|
| `videos-brutos\` | gravações do Luan (uma subpasta por vídeo) |
| `referencias\<perfil>\` | vídeos de criadores que o Luan gosta, só para estudo; nunca entram no vídeo final |
| `guias\<perfil>.md` | guia de estilo de cada perfil (hoje: `luan.md`) |
| `projetos\<data>-<tema>\` | storyboard, transcrição e composição de cada vídeo |
| `exportacao\` | vídeo final aprovado |
| `ferramentas\` | scripts da equipe (`transcrever.py`) |

## Ferramentas (testadas em 2026-11-11)

| Ferramenta | Como chamar | Observação |
|---|---|---|
| FFmpeg 9.0.2 | `ffmpeg` / `ffprobe` | cortes, áudio, junção, exportação |
| faster-whisper 1.2.1 | `python ferramentas\transcrever.py <arquivo>` | gera `.palavras.json` (tempo por palavra) e `.srt`. Modelo `small` em CPU |
| yt-dlp 2026.10.26 | `python -m yt_dlp <link> -o referencias\<perfil>\%(title)s.%(ext)s` | só para baixar referência que o Luan mandou |
| HyperFrames 0.8.221 | `npx -y hyperframes@0.8.221 ...` | motion graphics; skills `hyperframes`, `hyperframes-cli`, `hyperframes-registry` |

## Fluxo de um vídeo

1. O Luan põe a gravação em `videos-brutos\` e diz o perfil e a rede.
2. Bon Clay transcreve, monta o storyboard em `projetos\<data>-<tema>\storyboard.md` (cena, trecho da fala, o que aparece na tela, duração) e para.
3. O Luan pede ajustes; cada ajuste que vale para os próximos vídeos entra no guia do perfil.
4. Com o "aprovado" do Luan no storyboard, Bon Clay gera o vídeo em `exportacao\`, confere os quadros e entrega.
5. Publicar é do agente da rede (Brook no X, Robin no LinkedIn), pelo envelope de cada um.
