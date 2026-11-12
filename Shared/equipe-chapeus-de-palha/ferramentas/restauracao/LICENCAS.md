# Licenças do fluxo de restauração

Verificado em 2026-11-11 por Franky, nas fontes citadas abaixo (repositórios, *model cards*, metadados dos pacotes). **Não sou advogado e esta tabela não é parecer jurídico.**
Regra do serviço: o serviço é vendido, então só entra o que permite uso comercial, **código e pesos**.

## Resumo

- **Código e pesos: todos os componentes usados têm licença publicada que permite uso comercial** (Apache-2.0, BSD-3, MIT, PSF).
- **Fora de propósito:** CodeFormer (licença não comercial), InsightFace/ArcFace (pesos não comerciais), as partes do GFPGAN sob licença NVIDIA e DFDNet (não comerciais) e o `facexlib` com seus pesos de parsing (treinados em CelebAMask-HQ, de pesquisa).
- **Risco residual, que precisa de decisão do Luan (ver a seção "Risco residual"):** três redes (GFPGAN, LaMa, Real-ESRGAN) foram treinadas em conjuntos de dados cujos termos são de pesquisa ou não comerciais, embora os autores publiquem os pesos sob licença permissiva. Não dá para eliminar isso por código.
- **Cor (DDColor):** incluído (opcional, só com `--cor`) usando `ddcolor_paper_tiny` sob licença Apache-2.0 (ver "Colorização").

## Código

| Componente | Versão | Uso | Licença declarada | Como verifiquei |
|---|---|---|---|---|
| Python (build do `uv`) | 3.11.18 | interpretador do venv (o do sistema é 3.14) | PSF | padrão do CPython; não li o arquivo da distribuição |
| PyTorch | 2.1.2+cu118 | GFPGAN e Real-ESRGAN | BSD-3 | metadados do pacote |
| NumPy 1.26.4, Pillow 13.0.0, matplotlib 3.11.2 | | imagens; matplotlib é exigido pelo MediaPipe | BSD / MIT-CMU / PSF | metadados dos pacotes |
| OpenCV (`opencv-contrib-python-headless`) | 4.9.0.80 | ajuste, máscara, alinhamento | Apache-2.0 | metadados; README do `opencv-python`: sem algoritmos não livres (SURF etc.); os *wheels* trazem FFmpeg LGPL 2.1 (sem Qt na versão *headless* do Windows) |
| ONNX Runtime GPU | 1.17.1 | roda o LaMa | MIT | metadados e API do GitHub |
| MediaPipe | 0.10.14 | detecção de rostos e pontos | Apache-2.0 | metadados e API do GitHub |
| GFPGAN, arquitetura "clean" | 2 arquivos copiados em `vendor\` | roda o GFPGAN v1.4 | Apache-2.0 (`vendor\LICENSE-GFPGAN.txt`) | `LICENSE` do repositório. **Exceções do próprio arquivo de licença:** StyleGAN2 da NVIDIA e DFDNet (CC BY-NC-SA). Conferi que os dois arquivos copiados (`gfpganv1_clean_arch.py`, `stylegan2_clean_arch.py`) **não importam** `upfirdn2d` nem `fused_act` (os módulos da NVIDIA) e não citam o DFDNet. O arquivo `gfpganv1_arch.py` (que importa os módulos da NVIDIA) **não é usado** |
| BasicSR, `rrdbnet_arch.py` | 1 arquivo copiado | arquitetura do Real-ESRGAN | Apache-2.0 (texto dentro do `vendor\LICENSE-GFPGAN.txt`, seção BasicSR; API do GitHub confirma Apache-2.0) | cabeçalho de modificação nos arquivos |
| `vendor\basicsr_min.py` | meu | substitui o pacote `basicsr` (registro e 3 funções) | derivado do BasicSR (Apache-2.0) | o próprio arquivo explica a modificação |
| DDColor (`vendor\ddcolor\`) | 7 arquivos copiados | arquitetura do DDColor (`--cor`) | Apache-2.0 (`vendor\LICENSE-DDColor.txt`) | `LICENSE` do repositório `piddnad/DDColor`; troquei imports de `basicsr`/`timm` por módulos locais |
| Real-ESRGAN (licença) | | só o texto de licença e os pesos | BSD-3 (`vendor\LICENSE-RealESRGAN.txt`) | `LICENSE` do repositório |
| Demais dependências instaladas (requests, urllib3, protobuf, absl-py, attrs, flatbuffers, sympy, networkx, jinja2, fsspec, filelock, packaging, certifi, etc.) | ver `uv pip list` | apoio | MIT, BSD, Apache-2.0, PSF; `certifi` é MPL-2.0 (nível de arquivo, sem efeito aqui) | campo `License` dos metadados de cada pacote |
| CUDA e cuDNN | embutidos no *wheel* do PyTorch | GPU | licença da NVIDIA para esses binários | **não li o texto** (uso interno nesta máquina; reler antes de distribuir o venv) |

Os pacotes `gfpgan`, `basicsr`, `realesrgan` e `facexlib` **não foram instalados**: só os 3 arquivos acima foram copiados, com atribuição, para evitar importar os módulos sob licença não comercial.

## Pesos dos modelos (pasta `modelos\`)

Para reproduzir: `sh baixar-modelos.sh`. O SHA256 de cada arquivo está em `modelos\SHA256.txt` e no `relatorio.json` de cada execução.

| Arquivo | Fonte | SHA256 | Licença declarada | Dados de treino (ponto de atenção) |
|---|---|---|---|---|
| `GFPGANv1.4.pth` | https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth | `e2cd4703ab14f4d01fd1383a8a8b266f9a5833dacee8e6a79d3bf21a1b6be5ad` | Apache-2.0 (README e LICENSE do GFPGAN) | **FFHQ** (conjunto da NVIDIA): imagens individuais CC BY, **CC BY-NC**, domínio público e outras; a NVIDIA pede contato para uso comercial do conjunto e diz que ele não deve ser usado para desenvolver reconhecimento facial |
| `RealESRGAN_x2plus.pth`, `RealESRGAN_x4plus.pth` | https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth e .../v0.1.0/RealESRGAN_x4plus.pth | x2: `49fafd45f8fd7aa8d31ab2a22d14d91b536c34494a5cfe31eb5d89c2fa266abb`; x4: `4fa0d38905f75ac06eb49a7951b426670021be3018265fd191d2125df9d682f1` | BSD-3 (repositório) | treinados em DF2K (DIV2K + Flickr2K) e OST; **a página do DIV2K diz "somente para pesquisa acadêmica"** |
| `lama_fp32.onnx` | https://huggingface.co/Carve/LaMa-ONNX (porte em ONNX do *big-lama*) | `1faef5301d78db7dda502fe59966957ec4b79dd64e16f03ed96913c7a4eb68d6` | Apache-2.0 (ficha do Hugging Face do porte e do `smartywu/big-lama`; repositório `advimman/lama` Apache-2.0) | treinado em **Places2/Places-Challenge**, que o site do MIT descreve em termos de uso para pesquisa |
| `face_landmarker.task` | https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task | `64184e229b263107bc2b804c6625db1341ff2bb731874b0bcc2fe6544e0bc9ff` | **Apache-2.0**, conforme os *model cards* do Face Mesh V2, do BlazeFace (short range) e do Blendshape V2 (os três dizem "LICENSED UNDER Apache License, Version 2.0") | imagens de celular capturadas pela própria Google, sem conjunto de dados público de pesquisa |
| `ddcolor_paper_tiny.pth` | https://huggingface.co/piddnad/DDColor-models/resolve/main/ddcolor_paper_tiny.pth | `81dd643904f4664c3718513e3320ae3db0c567f0d3e18398606659adee7bfc17` | Apache-2.0 (ficha do Hugging Face `piddnad/DDColor-models` e repositório `piddnad/DDColor`) | treinado em **ImageNet** (termos de pesquisa acadêmica) |

Formato dos pesos: `.pth` carregados com `torch.load(weights_only=True)` (não executa código arbitrário), `.onnx` e `.task` (TFLite).

## Excluídos por causa da licença

| Item | Por quê |
|---|---|
| CodeFormer | licença não comercial (S-Lab). Pedido do Bot Builder: não entra |
| InsightFace / ArcFace (verificação de identidade) | pesos publicados só para pesquisa não comercial. A checagem de identidade usa só geometria (MediaPipe) e estrutura (SSIM), sem modelo de reconhecimento facial |
| `facexlib` (RetinaFace e modelos de *parsing*) | o código é MIT, mas os pesos de *parsing* vêm de CelebAMask-HQ (pesquisa) e o RetinaFace de WIDER FACE; troquei por MediaPipe |
| GFPGAN original (`gfpganv1_arch.py`), StyleGAN2 da NVIDIA, DFDNet | licença NVIDIA e CC BY-NC-SA, citadas no próprio `LICENSE` do GFPGAN |
| Pacotes `gfpgan`, `basicsr`, `realesrgan` | puxariam os módulos acima; só copiei os arquivos necessários |

## Colorização (`--cor`)

Usa o **DDColor** (`ddcolor_paper_tiny.pth`): código no GitHub com Apache-2.0 (`vendor\ddcolor\`, `vendor\LICENSE-DDColor.txt`) e pesos no Hugging Face com Apache-2.0 (`piddnad/DDColor-models`). Só altera os canais de cor (`a` e `b` do espaço Lab) e mantém 100% da luminância (`L`) da foto restaurada, sem redesenhar traços. Como foi treinado em ImageNet (termos de pesquisa), entra no mesmo ponto de atenção de dados de treino abaixo. Sempre registra aviso no relatório lembrando que a cor é interpretação.

## Risco residual (decisão do Luan)

As licenças **publicadas** dos pesos permitem uso comercial. Mas GFPGAN (FFHQ), LaMa (Places) e Real-ESRGAN (DIV2K/Flickr2K) foram treinados em conjuntos de dados cujos termos falam em pesquisa ou uso não comercial. É um ponto discutido de forma aberta na comunidade de IA, sem resposta simples, e **eu não tenho como resolver isso por código nem afirmar que é seguro**.
Opções: (1) aceitar o risco, como o Luan já deu a entender ao aprovar o fluxo; (2) pedir parecer de um advogado antes de vender em escala; (3) contatar os autores/NVIDIA; (4) restringir a etapa de rosto, que é a de maior risco, mantendo `--rosto 0` como padrão do serviço (o `--rosto 0` pula o GFPGAN; LaMa e Real-ESRGAN continuam entrando).

## Atribuições a manter

Ao entregar o venv ou o código a terceiros, manter `vendor\LICENSE-GFPGAN.txt`, `vendor\LICENSE-RealESRGAN.txt` e `vendor\LICENSE-DDColor.txt` e os cabeçalhos de modificação dos arquivos copiados. Apache-2.0 e BSD-3 exigem manter os avisos de direitos autorais e de modificação.

## Fotos de teste do Wikimedia Commons (categoria "Damaged photographs")

Conferidas nas páginas individuais e via API do Wikimedia Commons (`action=query&prop=imageinfo&iiprop=url|size|extmetadata`) em 2026-11-11. Todas foram baixadas no arquivo **original** (não miniatura).

| Papel no teste | Arquivo local (`teste\`) | Página no Wikimedia Commons | Origem, autor e data | Licença na página | Dimensões originais e SHA256 | Dano visível |
|---|---|---|---|---|---|---|
| 1. Retrato em close (pedido) | `AdaStoddard_1914.jpg` | https://commons.wikimedia.org/wiki/File:AdaStoddard.1914.jpg | Recorte do jornal *The Arizona Republican* (1914-02-15), p. 7 ("Mrs. Ada Stoddard, Who Will Leave Soon for Work in China"). Autor desconhecido | **Public domain** (`PD-US`, publicado nos EUA antes de 1931) | 1110×1502 px (471.385 B) — `7c2df765383674c4f7d636758029fb18e3ed1a90a4ff61c39763a450a1b56733` | Rasgo/vinco branco vertical no centro e retícula grossa de impressão de jornal (perfil de 90°; o detector facial não acha rosto por causa da retícula e do perfil estrito) |
| 1b. Retrato em close fotográfico (complementar da mesma categoria) | `Amos_Strunk_1911.jpg` | https://commons.wikimedia.org/wiki/File:(Amos_Strunk,_Philadelphia,_AL_(baseball))_LOC_2162649383.jpg | Bain News Service, 1911; Library of Congress (`LC-B2-2191-5`, negativo de vidro) | **No known copyright restrictions** (`No restrictions`, Flickr Commons / Library of Congress) | 1024×738 px (69.841 B) — `a1b4143a9040f2bc64c21dabb23a262a0888f069c9443c3be08578a7f51f501d` | Riscos escuros horizontais, pontos de poeira no rosto e descascamento de emulsão na borda inferior (incluído porque `AdaStoddard.1914.jpg` é recorte reticulado de jornal em perfil, onde o MediaPipe não detecta rosto) |
| 2. Retrato de corpo | `Dandridge_McRae.jpg` | https://commons.wikimedia.org/wiki/File:Dandridge_McRae,_in_prewar_militia_uniform.jpg | Autor desconhecido, c. 1860; acervo do Prairie Grove Battlefield State Park (Arkansas) | **Public domain** (`PD-US`, anterior a 1931) | 1390×1924 px (806.802 B) — `98c7073b464cb8443f13c5dc7d6c72e6ad4a7c5ab55c78f9aef3056e4ffe92ea` | Riscos brancos finos, poeira espalhada e mancha escura na bochecha esquerda |
| 3. Duas pessoas | `Soldier_with_girl.jpg` | https://commons.wikimedia.org/wiki/File:A_soldier_with_a_girl,_n.d._(11791515195).jpg | Alexander Galloway (1876–1945), negativo de vidro; Coalfields Local History Association Inc. / Newcastle Region Library | **Public domain** / **No known copyright restrictions** (Austrália pré-1955 e Flickr Commons) | 2796×3803 px (5.822.352 B) — `b02d0f6ba8128b9a62e75dc6e7515acd7971bceefdbb39f82f572b6e85e60aee` | Emulsão craquelada e descascada nas bordas, riscos sobre a testa do soldado e nas pernas |
| 4. Grupo com rostos pequenos | `5pulklegionow1929.jpg` | https://commons.wikimedia.org/wiki/File:5pulklegionow1929.jpg | Autor desconhecido, 1929 (Szkoła podoficerska 5 Pułku Legionów, Polônia) | **Public domain** (`PD-Poland` / `PD-anon-70-EU`, publicada em 1929 sem autor identificado) | 3190×1830 px (1.135.362 B) — `23d1ebb57eb4d73556813e6eef44f55730de9f50a86f15f2bd2d452e2d66c32f` | Amarelado/sépia, manchas na faixa inferior, riscos finos no muro de tijolos e cerca de 85 rostos pequenos (~45–60 px cada) |
| Lote inicial (3 fotos) | `foto1_rapaz_quepe.jpg`, `foto2_homem_riscos.jpg`, `foto3_senhora_manchas.jpg` | ver `teste\FONTES.md` | Library of Congress, Bibliothèque de Toulouse e Midpointe Library System / DPLA | **Public domain** / **No restrictions** | ver `teste\FONTES.md` | `foto1` já limpa por voluntário (controle); `foto2` com riscos severos; `foto3` com manchas e rabisco |

> **Nota sobre as fotos reais da família do Luan:** `foto1-original.jpg` e `foto2-original.jpg` ficam exclusivamente em `C:\Users\Lourenco_Filho\OpenBot\Shared\equipe-chapeus-de-palha\privado\restauracao\teste-familia\` e seus resultados em `teste-familia\metodo-novo\`, processadas 100% localmente sem envio a nenhum serviço externo.

## O que não verifiquei

- O texto integral das licenças de cada dependência transitiva (confiei nos metadados do pacote).
- Os termos do CUDA/cuDNN embutidos no PyTorch.
- Os termos atuais dos conjuntos de dados além do que as páginas citadas dizem (FFHQ, DIV2K, Places).
- Patentes.
