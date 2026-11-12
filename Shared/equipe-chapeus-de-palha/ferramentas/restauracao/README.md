# Fluxo local de restauração de fotos (`restaurar.py`)

Restauração de fotos antigas **100% local**, em etapas separadas e auditáveis, seguindo a regra do serviço (`agentes\kaya.md`): **restaurar, nunca recriar**. Nenhuma foto de cliente sai desta máquina.

## Requisitos e ambiente

- **Hardware testado:** Windows 10/11, NVIDIA GeForce RTX 3050 6 GB Laptop GPU, 8 GB de RAM (usa CUDA por padrão e CPU como plano B com `--cpu`).
- **Python isolado:** `3.11.18` em `.venv\` (criado via `uv`). O Python 3.14 do sistema não é usado porque PyTorch 2.1 (`cu118`), ONNX Runtime GPU 1.17.1 e MediaPipe 0.10.14 exigem Python 3.11/3.12.
- **Pacotes sem restrição não comercial:** apenas os arquivos de arquitetura limpa (`GFPGANv1Clean`, `RRDBNet`, `DDColor`) foram copiados em `vendor\` com suas licenças (`Apache-2.0` e `BSD-3`), sem instalar `gfpgan`, `basicsr`, `realesrgan`, `facexlib` nem `CodeFormer`. Detalhes completos e SHA256 dos pesos em [`LICENCAS.md`](./LICENCAS.md).

## Instalação / Reconstrução do zero

Em `C:\Users\Lourenco_Filho\OpenBot\Shared\equipe-chapeus-de-palha\ferramentas\restauracao`:

```powershell
powershell -ExecutionPolicy Bypass -File instalar.ps1
```

Para apenas conferir se o ambiente, a GPU e os 6 pesos estão íntegros:

```powershell
.venv\Scripts\python.exe verificar_ambiente.py
```

## Uso

```powershell
.venv\Scripts\python.exe restaurar.py <original> <pasta_saida> [--rosto 0.0-1.0] [--escala 2|4] [--cor] [--mascara arquivo.png]
```

### Opções principais

| Opção | Padrão | Descrição |
|---|---|---|
| `--rosto 0.0-1.0` | `0.5` | Opacidade do rosto restaurado pelo GFPGAN v1.4 sobre o passo 2. Com `--rosto 0`, a etapa 3 não roda. **Nota:** em rostos já nítidos ou com sardas/pintas, prefira `--rosto 0` ou `0.3` para não suavizar a pele. |
| `--escala 2\|4` | `2` | Ampliação com Real-ESRGAN (`x2plus` ou `x4plus`) em blocos (*tiles*) de 256 px em FP16 na GPU. |
| `--cor` | desligado | Colorização opcional com DDColor (`ddcolor_paper_tiny`, Apache-2.0). Só altera os canais de cor (`a, b` do Lab), preservando 100% da luminância (`L`) da foto. Só roda em fotos monocromáticas/sépia e registra aviso no relatório de que a cor é interpretação. |
| `--cor-intensidade` | `0.8` | Escala da saturação do DDColor (`0.8` deixa tons mais discretos). |
| `--mascara ARQ.png` | nenhum | Máscara manual em PNG (branco = área danificada para o LaMa preencher). Soma-se à máscara automática (ou substitui se usado com `--sem-auto`). |
| `--sem-auto` | desligado | Desliga a detecção automática de riscos e usa apenas `--mascara`. |
| `--max-mascara PCT` | `12.0` | Trava de segurança: se a máscara automática passar de `12%` da imagem, ela não é aplicada e um aviso é gravado. |
| `--limite-original` | `0.40` | Limite mínimo de identidade comparando `original -> resultado final`. |
| `--limite-etapa` | `0.60` | Limite mínimo de identidade em cada transição entre etapas seguidas (`etapa N -> etapa N+1`). |
| `--cpu` | desligado | Força execução em CPU (plano B). |

## Arquivos gerados em `<pasta_saida>`

1. `01_ajuste.png` — **Etapa 1 (OpenCV):** ajuste de níveis (percentis 0,5%–99,5%), remoção de amarelado/sépia (neutralização para cinza em fotos monocromáticas ou balanço de branco suave em fotos coloridas), contraste local suave (`CLAHE` `clipLimit=1.6` misturado a 60%) e redução leve de ruído (`fastNlMeansDenoising` proporcional ao ruído estimado pelo método de Immerkaer). Não redesenha nada.
2. `02_mascara.png` e `02_riscos.png` — **Etapa 2 (LaMa):** detecção morfológica conservadora de riscos finos (claros e escuros) e pontos isolados de poeira, com máscara de proteção sobre olhos, sobrancelhas, nariz e lábios. O LaMa (`lama_fp32.onnx`) preenche **somente** os pixels brancos da máscara; fora dela, os pixels são idênticos aos de `01_ajuste.png`.
3. `03_rosto.png` — **Etapa 3 (GFPGAN v1.4, se `--rosto > 0`):** alinha cada rosto detectado, transfere apenas o detalhe de luminância de alta frequência (mantendo o tom de baixa frequência e a cor da foto) e cola com máscara oval suave na opacidade `--rosto`.
4. `04_resolucao_2x.png` (ou `4x`) — **Etapa 4 (Real-ESRGAN):** super-resolução em blocos de 256 px.
5. `05_cor.png` — **Etapa 5 (DDColor, só com `--cor`):** colorização mantendo a luminância intacta.
6. `resultado.png` — Cópia da última etapa ativa.
7. `relatorio.json` — **Etapa 6 (Identidade e auditoria):** nota de cada rosto (original vs. cada etapa e transição entre etapas seguidas), status (`APROVADO`, `REPROVADO` ou `SEM_ROSTO_DETECTADO`), área da máscara, parâmetros, versões, hashes SHA256 dos modelos e tempos por etapa. Se reprovar, o script termina com código de saída `2`.
8. `lado_a_lado.png` e `lado_a_lado_rosto.png` — **Etapa 7:** executa `..\lado-a-lado.py` gerando o quadro `Original | Restaurada | Diferenças` da foto inteira e do recorte ampliado no rosto principal.

## Como funciona a checagem de identidade e por que os limites são `0.40` e `0.60`

Modelos de reconhecimento facial como InsightFace/ArcFace têm pesos restritos a pesquisa não comercial e não entram. A verificação usa apenas:
- **Geometria (`nota_geometria`):** 106 pontos dos traços centrais (olhos, sobrancelhas, nariz e lábios) do MediaPipe Face Landmarker, medidos sobre um recorte normalizado de 640 px e alinhados por semelhança (Umeyama: escala, rotação e translação). Os pontos da borda da mandíbula/bochecha não entram porque oscilam com o contraste do fundo em fotos de perfil. O erro quadrático médio (RMS) é dividido pela distância entre os olhos e convertido em nota de `0` a `1` por `1 / (1 + (erro / 0.045)^2)`.
- **Estrutura (`ssim_estrutura`):** SSIM do rosto alinhado em 192×192 px (tons de cinza com brilho/contraste casados) dentro de uma elipse central.
- **Nota final:** `min(nota_geometria, ssim_estrutura)`.

### Calibração (`teste\calibracao.py` -> `teste\calibracao.json`)

Testei três grupos nas fotos de teste:
- **Pessoas diferentes (`outra`, 6 pares):** notas entre `0.040` e `0.186` (mediana `0.117`).
- **Mesma pessoa com degradações que não mudam identidade (`preserva`, 18 casos: desfoque, JPEG Q30, ruído, contraste, redução de resolução):** notas de `0.253` a `0.996` (mediana `0.839`). Em rostos muito pequenos (~74 px na `foto2`), perda severa de resolução (`x0.35`) desloca os pontos em ~7% da distância entre os olhos (`0.253`).
- **Deformação sintética de olhos e boca (`deslocado`, 2% a 10% da distância entre os olhos):** em rosto frontal (`foto1`), deslocar 4% cai para `0.597` e 10% cai para `0.450`; em perfil (`foto3`), 2%–10% caem para `0.214`–`0.397`.

Por isso usamos **dois limites simultâneos**:
1. **`--limite-original 0.40` (`original -> resultado`):** separa com folga outra pessoa (`<= 0.186`) e pega deformações fortes (`<= 0.450`), permitindo que a remoção de riscos e o ganho de contraste melhorem a leitura do rosto em relação ao original danificado.
2. **`--limite-etapa 0.60` (`etapa N -> etapa N+1`):** exige que nenhuma etapa isolada (especialmente o GFPGAN na etapa 3 ou o Real-ESRGAN na etapa 4) desloque a geometria ou a estrutura do rosto além do limiar onde começam deformações de ~4% (`0.597`).

## Bateria de testes (`teste\`)

Fontes e licenças das 3 fotos de domínio público em [`teste\FONTES.md`](./teste/FONTES.md). Tabelas completas em [`teste\RESULTADOS_tabelas.md`](./teste/RESULTADOS_tabelas.md). Para rodar novamente:

```powershell
powershell -ExecutionPolicy Bypass -File teste\rodar_testes.ps1
.venv\Scripts\python.exe teste\resumir.py
```
