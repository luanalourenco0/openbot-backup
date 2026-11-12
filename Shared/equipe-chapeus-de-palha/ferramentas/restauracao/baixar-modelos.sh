#!/bin/sh
# Baixa os pesos para a pasta modelos\ (cada arquivo da fonte oficial). Uso: sh baixar-modelos.sh
cd "$(dirname "$0")/modelos" || exit 1
get() { [ -s "$2" ] && echo "ja existe: $2" || curl -L --fail --retry 3 -sS -o "$2" "$1" && echo "ok: $2"; }
get https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth GFPGANv1.4.pth
get https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth RealESRGAN_x4plus.pth
get https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth RealESRGAN_x2plus.pth
get https://huggingface.co/Carve/LaMa-ONNX/resolve/main/lama_fp32.onnx lama_fp32.onnx
get https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task face_landmarker.task
get https://huggingface.co/piddnad/DDColor-models/resolve/main/ddcolor_paper_tiny.pth ddcolor_paper_tiny.pth
