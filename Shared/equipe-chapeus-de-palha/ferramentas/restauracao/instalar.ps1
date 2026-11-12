# Reconstroi o ambiente de restauracao do zero (nesta pasta). Pode ser rodado de novo sem problema.
# Requisitos: Windows, GPU NVIDIA com driver recente (opcional: sem GPU roda em CPU, bem mais devagar), `uv` e `sh` (Git for Windows), internet.
# Uso (em ferramentas\restauracao):  powershell -ExecutionPolicy Bypass -File instalar.ps1
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
$py = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'

# 1. Python 3.11 isolado e venv (o Python do sistema 3.14 nao serve: PyTorch 2.1 e MediaPipe 0.10 pedem <= 3.11/3.12).
uv python install 3.11
if (-not (Test-Path $py)) { uv venv --python 3.11 .venv }

# 2. PyTorch 2.1.2 com CUDA 11.8 (funciona na RTX 3050 e e o par testado com onnxruntime-gpu 1.17.1).
uv pip install --python $py torch==2.1.2 --index-url https://download.pytorch.org/whl/cu118

# 3. Demais bibliotecas, nas versoes testadas.
uv pip install --python $py numpy==1.26.4 opencv-contrib-python-headless==4.9.0.80 pillow onnxruntime-gpu==1.17.1 `
  absl-py attrs flatbuffers "protobuf>=4.25.3,<5" matplotlib
# MediaPipe sem as dependencias automaticas (ele puxaria o opencv completo e pacotes que nao usamos).
uv pip install --python $py mediapipe==0.10.14 --no-deps

# 4. Pesos dos modelos (pasta modelos\), cada um da fonte oficial; ver LICENCAS.md.
sh baixar-modelos.sh

# 5. Confere tudo: versoes, GPU, pesos (strict), LaMa em CUDA, detector de rostos. Grava modelos\SHA256.txt na 1a vez.
& $py verificar_ambiente.py
