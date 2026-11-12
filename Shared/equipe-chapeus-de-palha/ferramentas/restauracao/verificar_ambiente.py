"""Confere se o ambiente de restauracao esta pronto: versoes, GPU, pesos e modelos.

Uso (dentro de ferramentas\\restauracao):  .venv\\Scripts\\python.exe verificar_ambiente.py
Grava modelos\\SHA256.txt (um hash por arquivo de peso) na primeira execucao.
Nao envia nada para a internet.
"""
import hashlib
import platform
import sys
import time
from pathlib import Path

AQUI = Path(__file__).resolve().parent
MODELOS = AQUI / "modelos"
sys.path.insert(0, str(AQUI))

PESOS = ["GFPGANv1.4.pth", "RealESRGAN_x2plus.pth", "RealESRGAN_x4plus.pth", "lama_fp32.onnx", "face_landmarker.task", "ddcolor_paper_tiny.pth"]


def sha256(caminho):
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def main():
    ok = True
    import torch  # importar o torch primeiro: ele carrega as DLLs CUDA/cuDNN que o onnxruntime tambem usa

    import cv2
    import numpy
    import onnxruntime as ort
    import PIL
    import mediapipe as mp

    print(f"python {platform.python_version()} | torch {torch.__version__} (CUDA {torch.version.cuda}) | numpy {numpy.__version__}"
          f" | opencv {cv2.__version__} | pillow {PIL.__version__} | onnxruntime {ort.__version__} | mediapipe {mp.__version__}")
    if torch.cuda.is_available():
        p = torch.cuda.get_device_properties(0)
        print(f"GPU: {p.name}, {p.total_memory / 2**30:.1f} GB")
    else:
        print("GPU: nao encontrada (vai rodar em CPU, bem mais devagar)")

    hashes = {}
    arq_hash = MODELOS / "SHA256.txt"
    for nome in PESOS:
        c = MODELOS / nome
        if not c.is_file():
            print(f"FALTA: {c}  (rode: sh baixar-modelos.sh)")
            ok = False
            continue
        hashes[nome] = sha256(c)
    if hashes and not arq_hash.exists():
        arq_hash.write_text("".join(f"{h}  {n}\n" for n, h in hashes.items()), encoding="utf-8")
        print(f"Gravado {arq_hash}")

    if ok:
        from vendor.gfpganv1_clean_arch import GFPGANv1Clean
        from vendor.rrdbnet_arch import RRDBNet

        t = time.perf_counter()
        g = GFPGANv1Clean(out_size=512, num_style_feat=512, channel_multiplier=2, decoder_load_path=None, fix_decoder=False,
                          num_mlp=8, input_is_latent=True, different_w=True, narrow=1, sft_half=True)
        g.load_state_dict(torch.load(MODELOS / "GFPGANv1.4.pth", map_location="cpu", weights_only=True)["params_ema"], strict=True)
        print(f"GFPGAN v1.4: pesos carregados (strict) em {time.perf_counter() - t:.1f}s")
        for esc in (2, 4):
            r = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=esc)
            r.load_state_dict(torch.load(MODELOS / f"RealESRGAN_x{esc}plus.pth", map_location="cpu", weights_only=True)["params_ema"], strict=True)
            print(f"Real-ESRGAN x{esc}plus: pesos carregados (strict)")

        provedores = [p for p in ("CUDAExecutionProvider", "CPUExecutionProvider") if p in ort.get_available_providers()]
        sess = ort.InferenceSession(str(MODELOS / "lama_fp32.onnx"), providers=provedores)
        print("LaMa (ONNX): provedor em uso =", sess.get_providers()[0],
              "| entradas:", [(i.name, i.shape) for i in sess.get_inputs()], "| saidas:", [(o.name, o.shape) for o in sess.get_outputs()])

        from mediapipe.tasks import python as mpt
        from mediapipe.tasks.python import vision
        det = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(
            base_options=mpt.BaseOptions(model_asset_path=str(MODELOS / "face_landmarker.task")), num_faces=5))
        print("MediaPipe Face Landmarker: carregado")
        det.close()

        from vendor.ddcolor.ddcolor_arch import DDColor
        dd = DDColor(encoder_name="convnext-t", decoder_name="MultiScaleColorDecoder", input_size=[512, 512],
                     num_output_channels=2, last_norm="Spectral", do_normalize=False, num_queries=100, num_scales=3, dec_layers=9)
        sd_dd = torch.load(MODELOS / "ddcolor_paper_tiny.pth", map_location="cpu", weights_only=True)
        sd_dd = sd_dd["params"] if isinstance(sd_dd, dict) and "params" in sd_dd else sd_dd
        dd.load_state_dict(sd_dd, strict=False)
        print("DDColor paper_tiny: pesos carregados")
    print("AMBIENTE OK" if ok else "AMBIENTE INCOMPLETO")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
