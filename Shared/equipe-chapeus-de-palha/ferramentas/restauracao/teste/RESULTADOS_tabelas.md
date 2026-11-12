# Tabelas geradas dos relatorio.json (teste\resumir.py)

## Tempo e mascara

| Foto | --rosto | Entrada | 1 ajuste | 2 riscos (LaMa) | 3 rosto | 4 resolucao 2x | Rostos+identidade | Total | Mascara (% da imagem) |
|---|---|---|---|---|---|---|---|---|---|
| foto1_rapaz_quepe | 0 | 1920x2681 | 2.88 s | 54.84 s | pulada | 16.9 s | 3.88 s | 85.63 s | 0.088% |
| foto1_rapaz_quepe | 0.5 | 1920x2681 | 2.3 s | 52.53 s | 3.28 s | 16.48 s | 3.88 s | 83.47 s | 0.088% |
| foto1_rapaz_quepe | 1.0 | 1920x2681 | 2.27 s | 52.16 s | 2.69 s | 16.37 s | 3.66 s | 81.87 s | 0.088% |
| foto2_homem_riscos | 0 | 467x629 | 0.52 s | 49.27 s | pulada | 2.64 s | 3.13 s | 57.25 s | 1.979% |
| foto2_homem_riscos | 0.5 | 467x629 | 0.46 s | 47.93 s | 2.8 s | 1.96 s | 3.39 s | 58.16 s | 1.979% |
| foto2_homem_riscos | 1.0 | 467x629 | 0.47 s | 47.7 s | 2.06 s | 2.07 s | 3.51 s | 57.4 s | 1.979% |
| foto3_senhora_manchas | 0 | 1920x2473 | 1.66 s | 58.42 s | pulada | 14.9 s | 4.62 s | 84.4 s | 1.506% |
| foto3_senhora_manchas | 0.5 | 1920x2473 | 1.42 s | 58.44 s | 2.23 s | 14.88 s | 5.3 s | 87.14 s | 1.506% |
| foto3_senhora_manchas | 1.0 | 1920x2473 | 1.67 s | 58.59 s | 2.03 s | 15.09 s | 5.95 s | 88.64 s | 1.506% |

## Identidade (rosto principal, comparado com o original e pior transicao entre etapas)

| Foto | --rosto | Etapa 1 | Etapa 2 | Etapa 3 | Final (04) | Erro geom. (final) | SSIM (final) | Pior transicao | Status |
|---|---|---|---|---|---|---|---|---|---|
| foto1_rapaz_quepe | 0 | 0.971 | 0.973 | - | 0.98 | 0.0051 | 0.98 | 0.971 | APROVADO (orig>=0.4, etapa>=0.6) |
| foto1_rapaz_quepe | 0.5 | 0.971 | 0.973 | 0.989 | 0.974 | 0.0073 | 0.974 | 0.971 | APROVADO (orig>=0.4, etapa>=0.6) |
| foto1_rapaz_quepe | 1.0 | 0.971 | 0.973 | 0.984 | 0.978 | 0.0056 | 0.978 | 0.971 | APROVADO (orig>=0.4, etapa>=0.6) |
| foto2_homem_riscos | 0 | 0.661 | 0.708 | - | 0.746 | 0.0263 | 0.911 | 0.621 | APROVADO (orig>=0.4, etapa>=0.6) |
| foto2_homem_riscos | 0.5 | 0.661 | 0.708 | 0.717 | 0.696 | 0.0298 | 0.865 | 0.661 | APROVADO (orig>=0.4, etapa>=0.6) |
| foto2_homem_riscos | 1.0 | 0.661 | 0.708 | 0.64 | 0.613 | 0.0357 | 0.837 | 0.661 | APROVADO (orig>=0.4, etapa>=0.6) |
| foto3_senhora_manchas | 0 | 0.932 | 0.861 | - | 0.757 | 0.0255 | 0.954 | 0.617 | APROVADO (orig>=0.4, etapa>=0.6) |
| foto3_senhora_manchas | 0.5 | 0.932 | 0.863 | 0.82 | 0.701 | 0.0294 | 0.941 | 0.758 | APROVADO (orig>=0.4, etapa>=0.6) |
| foto3_senhora_manchas | 1.0 | 0.932 | 0.861 | 0.813 | 0.681 | 0.0308 | 0.965 | 0.719 | APROVADO (orig>=0.4, etapa>=0.6) |

## Avisos registrados

