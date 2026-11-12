"""Transcreve um video ou audio com tempo por palavra (faster-whisper).

Uso:
    python transcrever.py <arquivo> [--modelo small] [--idioma pt]

Gera, ao lado do arquivo: <nome>.palavras.json (cada palavra com inicio e fim)
e <nome>.srt (legenda por frase).

O audio e decodificado pelo FFmpeg e passado ao Whisper como array, porque
o faster-whisper 1.2.1 nao funciona com o av 19 desta maquina (testado em 2026-11-11).
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from faster_whisper import WhisperModel


def tempo_srt(s: float) -> str:
    ms = int(round(s * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    seg, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{seg:02},{ms:03}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("arquivo")
    ap.add_argument("--modelo", default="small")
    ap.add_argument("--idioma", default="pt")
    a = ap.parse_args()

    entrada = Path(a.arquivo).resolve()
    if not entrada.is_file():
        print(f"Arquivo nao encontrado: {entrada}", file=sys.stderr)
        return 1

    bruto = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(entrada), "-f", "f32le", "-ac", "1", "-ar", "16000", "-"],
        capture_output=True,
        check=True,
    ).stdout
    audio = np.frombuffer(bruto, np.float32)

    modelo = WhisperModel(a.modelo, device="cpu", compute_type="int8")
    segmentos, _ = modelo.transcribe(audio, language=a.idioma, word_timestamps=True)

    palavras, linhas_srt = [], []
    for i, s in enumerate(segmentos, 1):
        linhas_srt += [str(i), f"{tempo_srt(s.start)} --> {tempo_srt(s.end)}", s.text.strip(), ""]
        for w in s.words or []:
            palavras.append({"palavra": w.word.strip(), "inicio": round(float(w.start), 3), "fim": round(float(w.end), 3)})

    base = entrada.with_suffix("")
    Path(f"{base}.palavras.json").write_text(json.dumps(palavras, ensure_ascii=False, indent=1), encoding="utf-8")
    Path(f"{base}.srt").write_text("\n".join(linhas_srt), encoding="utf-8")
    print(f"OK: {len(palavras)} palavras -> {base}.palavras.json e {base}.srt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
