#!/usr/bin/env python
"""Máscara e recomposição com relatório de mudanças fora da área.

Arquivo novo; não altera restaurar.py nem o original. Só usa cv2, numpy e
Pillow (já presentes no .venv da ferramenta). Roda 100% local.

Dois comandos:

  mascara   Cria uma máscara dos pontos brancos (manchas claras) numa região
            do fundo (--roi x0,y0,x1,y1 em frações 0-1 da imagem).
  compor    Recompõe SÓ a área da máscara de uma imagem "gerada" (ex.: saída
            da IA) sobre o original e mede o que mudou fora da máscara.

Uso:
  python mascara_compor.py mascara ORIGINAL SAIDA_DIR --roi 0,0,1,0.25
  python mascara_compor.py compor  ORIGINAL GERADA MASCARA SAIDA_DIR [--dilatar 2] [--suavizar 0]

SAIDA_DIR tem de ser uma pasta NOVA (se já existir, o script recusa e não grava nada).

Convenção da máscara: branco = área que pode ser substituída; preto = intocada.
"""
import argparse
import hashlib
import json
import os
import sys
from datetime import datetime
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageOps

SAIDAS_COMPOR = ["composto.png", "mascara_usada.png", "suporte_booleano.png",
                 "diff_fora_mascara_gerada_bruta.png", "relatorio.json", "relatorio.md"]
LIMIAR_DIFF = 8 # diferença (0-255, pior canal) para contar um pixel como "mudou"


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def ler_rgb(p: Path) -> np.ndarray:
    # exif_transpose: respeita a rotação gravada na foto, igual ao que o usuário vê
    with Image.open(p) as im:
        return np.asarray(ImageOps.exif_transpose(im).convert("RGB"))


def salvar(p: Path, arr: np.ndarray) -> None:
    Image.fromarray(arr).save(p)


def preparar_saida(entradas, saida_dir: Path, nomes) -> None:
    """Exige pasta de saída NOVA e garante que nenhum arquivo de saída é uma entrada.

    - A pasta não pode existir (nem como link quebrado): nada pré-existente é sobrescrito.
    - Cada arquivo de saída, resolvido, não pode coincidir com nenhuma entrada.
    - Só então a pasta é criada (exist_ok=False).
    """
    if os.path.lexists(saida_dir):
        sys.exit(f"ERRO: a pasta de saída '{saida_dir}' já existe. Informe uma pasta NOVA (nada é sobrescrito).")
    prospectiva = saida_dir.parent.resolve() / saida_dir.name
    ents = {e.resolve() for e in entradas}
    for n in nomes:
        if (prospectiva / n).resolve() in ents:
            sys.exit(f"ERRO: o arquivo de saída '{n}' coincide com uma entrada. Use outra pasta de saída.")
    saida_dir.mkdir(parents=True, exist_ok=False)
    # reconfere com a pasta já criada (pega link simbólico/junção no caminho)
    for n in nomes:
        alvo = (saida_dir / n).resolve()
        if alvo in ents or any(alvo.exists() and e.exists() and os.path.samefile(alvo, e) for e in entradas):
            sys.exit(f"ERRO: o arquivo de saída '{n}' aponta para uma entrada. Nada foi gravado.")


def criar_mascara(orig: np.ndarray, roi, percentil: float, dilatar: int) -> np.ndarray:
    """Pontos claros pequenos (top-hat) dentro da ROI -> máscara 0/255."""
    h, w = orig.shape[:2]
    x0, y0, x1, y1 = (int(roi[0] * w), int(roi[1] * h), int(roi[2] * w), int(roi[3] * h))
    cinza = cv2.cvtColor(orig, cv2.COLOR_RGB2GRAY)
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
    tophat = cv2.morphologyEx(cinza, cv2.MORPH_TOPHAT, k)
    regiao = tophat[y0:y1, x0:x1]
    corte = max(np.percentile(regiao, percentil), 12)
    m = np.zeros((h, w), np.uint8)
    m[y0:y1, x0:x1] = (regiao >= corte).astype(np.uint8) * 255
    if dilatar > 0:
        m = cv2.dilate(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * dilatar + 1,) * 2))
    return m


def estimar_deslocamento(a: np.ndarray, b: np.ndarray):
    """Deslocamento global (dx, dy) em px entre duas imagens por correlação de fase."""
    ga = cv2.cvtColor(a, cv2.COLOR_RGB2GRAY).astype(np.float32)
    gb = cv2.cvtColor(b, cv2.COLOR_RGB2GRAY).astype(np.float32)
    (dx, dy), resp = cv2.phaseCorrelate(ga, gb, cv2.createHanningWindow(ga.shape[::-1], cv2.CV_32F))
    return float(dx), float(dy), float(resp)


def metricas_fora(a: np.ndarray, b: np.ndarray, fora: np.ndarray) -> dict:
    """Diferença por pixel entre a e b, só nos pixels onde 'fora' é True."""
    d = np.abs(a.astype(np.int16) - b.astype(np.int16)).max(axis=2)  # pior canal por pixel
    dv = d[fora]
    n = int(dv.size)
    mse = float(((a.astype(np.float64) - b.astype(np.float64))[fora] ** 2).mean()) if n else 0.0
    psnr = None if mse == 0 else round(float(10 * np.log10(255.0 ** 2 / mse)), 2)
    return {
        "pixels_avaliados": n,
        "pixels_diferentes": int((dv > 0).sum()),
        "pct_diferentes": round(100 * float((dv > 0).mean()), 4) if n else 0.0,
        f"pct_mudou_mais_que_{LIMIAR_DIFF}": round(100 * float((dv > LIMIAR_DIFF).mean()), 4) if n else 0.0,
        "diff_media": round(float(dv.mean()), 4) if n else 0.0,
        "diff_p99": float(np.percentile(dv, 99)) if n else 0.0,
        "diff_max": int(dv.max()) if n else 0,
        "psnr_db": psnr,  # None = sem diferença (infinito)
    }


def mapa_calor(a, b, fora) -> np.ndarray:
    d = np.abs(a.astype(np.int16) - b.astype(np.int16)).max(axis=2)
    d = np.clip(d.astype(np.float32) * 4, 0, 255).astype(np.uint8)  # ganho 4x
    cal = cv2.cvtColor(cv2.applyColorMap(d, cv2.COLORMAP_INFERNO), cv2.COLOR_BGR2RGB)
    cal[~fora] = 0  # dentro da máscara: preto (não conta)
    return cal


def cmd_mascara(a):
    orig_p, saida = Path(a.original), Path(a.saida)
    roi = [float(x) for x in a.roi.split(",")]
    if len(roi) != 4 or not (0 <= roi[0] < roi[2] <= 1 and 0 <= roi[1] < roi[3] <= 1):
        sys.exit("ERRO: --roi deve ser x0,y0,x1,y1 em frações 0-1, com x0<x1 e y0<y1.")
    preparar_saida([orig_p], saida, ["mascara.png", "mascara_previa.png"])
    hash_antes = sha256(orig_p)
    orig = ler_rgb(orig_p)
    m = criar_mascara(orig, roi, a.percentil, a.dilatar)
    salvar(saida / "mascara.png", m)
    prev = orig.copy()
    prev[m > 0] = (255, 0, 0)
    salvar(saida / "mascara_previa.png", prev)
    print(f"mascara.png: {int((m > 0).sum())} px ({100 * (m > 0).mean():.3f}% da imagem) em {saida}")
    if sha256(orig_p) != hash_antes:  # conferido depois de TODAS as gravações
        sys.exit("ERRO GRAVE: o original mudou durante a execução.")


def cmd_compor(a):
    orig_p, ger_p, msk_p, saida = Path(a.original), Path(a.gerada), Path(a.mascara), Path(a.saida)
    preparar_saida([orig_p, ger_p, msk_p], saida, SAIDAS_COMPOR)
    hash_antes = sha256(orig_p)

    orig, ger = ler_rgb(orig_p), ler_rgb(ger_p)
    h, w = orig.shape[:2]
    gh, gw = ger.shape[:2]
    with Image.open(msk_p) as im:
        msk = np.asarray(ImageOps.exif_transpose(im).convert("L"))
    if msk.shape != (h, w):
        sys.exit(f"ERRO: máscara {msk.shape[1]}x{msk.shape[0]} difere do original {w}x{h}. Gere-a com o comando 'mascara'.")

    # 1) resolução e enquadramento da imagem gerada
    mesmo_tamanho = (gw, gh) == (w, h)
    prop_orig, prop_ger = w / h, gw / gh
    ger_alinhada = ger if mesmo_tamanho else cv2.resize(ger, (w, h), interpolation=cv2.INTER_LANCZOS4)
    aviso = []
    if not mesmo_tamanho:
        aviso.append(f"Gerada tem {gw}x{gh}, original {w}x{h}: a gerada foi reamostrada (Lanczos) para comparar/compor. "
                     "Isso suaviza a textura da área colada, e parte da diferença medida vem da reamostragem.")
    if abs(prop_orig - prop_ger) / prop_orig > 0.005:
        aviso.append(f"Proporção mudou ({prop_orig:.4f} -> {prop_ger:.4f}): houve recorte/enquadramento diferente; "
                     "esticar para o tamanho original desalinha a imagem.")

    # 2) máscara efetiva (dilatação + suavização opcional de borda)
    binaria = (msk >= 128).astype(np.uint8)
    if a.dilatar > 0:
        binaria = cv2.dilate(binaria, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * a.dilatar + 1,) * 2))
    alfa = binaria.astype(np.float32)
    if a.suavizar > 0:
        alfa = np.clip(cv2.GaussianBlur(alfa, (0, 0), a.suavizar), 0, 1)
    dentro = alfa > 0          # onde a recomposição pode mexer
    fora = ~dentro             # onde o composto TEM que ser idêntico ao original

    # 3) recomposição
    a3 = alfa[..., None]
    comp = np.rint(ger_alinhada.astype(np.float32) * a3 + orig.astype(np.float32) * (1 - a3)).astype(np.uint8)

    # 4) medidas
    dx, dy, resp = estimar_deslocamento(orig, ger_alinhada)
    bruto = metricas_fora(orig, ger_alinhada, fora)   # o que a gerada mudou fora da máscara
    final = metricas_fora(orig, comp, fora)           # o que sobrou depois de recompor (deve ser 0)
    area = {"pixels": int(dentro.sum()), "pct_da_imagem": round(100 * float(dentro.mean()), 4)}

    salvar(saida / "composto.png", comp)
    salvar(saida / "mascara_usada.png", (alfa * 255).astype(np.uint8))  # alfa de mistura (com suavização, tem tons de cinza)
    # suporte booleano EXATO usado nas medidas: 255 onde alfa>0 (pode mexer), 0 onde o composto é idêntico ao original
    salvar(saida / "suporte_booleano.png", dentro.astype(np.uint8) * 255)
    salvar(saida / "diff_fora_mascara_gerada_bruta.png", mapa_calor(orig, ger_alinhada, fora))

    identico = final["pixels_diferentes"] == 0
    hash_depois = sha256(orig_p)
    rel = {
        "gerado_em": datetime.now().isoformat(timespec="seconds"),
        "entradas": {"original": str(orig_p), "gerada": str(ger_p), "mascara": str(msk_p)},
        "parametros": {"dilatar_px": a.dilatar, "suavizar_sigma": a.suavizar, "limiar_diff": LIMIAR_DIFF},
        "resolucao": {"original": [w, h], "gerada": [gw, gh], "mesmo_tamanho": mesmo_tamanho,
                      "proporcao_original": round(prop_orig, 5), "proporcao_gerada": round(prop_ger, 5)},
        "enquadramento": {"deslocamento_px_dx": round(dx, 3), "deslocamento_px_dy": round(dy, 3),
                          "confianca_0a1": round(resp, 3),
                          "obs": "correlação de fase da imagem inteira, gerada (reamostrada) vs original; ~0 = alinhada"},
        "area_da_mascara": area,
        "fora_da_mascara_gerada_bruta": bruto,
        "fora_da_mascara_composto_final": final,
        "composto_identico_fora_da_mascara": identico,
        "original_intacto": {"sha256": hash_antes, "igual_apos_execucao": hash_antes == hash_depois},
        "avisos": aviso,
    }
    (saida / "relatorio.json").write_text(json.dumps(rel, ensure_ascii=False, indent=2), encoding="utf-8")

    md = [
        "# Relatório de recomposição por máscara", "",
        f"- Original: `{orig_p.name}` {w}x{h} | Gerada: `{ger_p.name}` {gw}x{gh}",
        f"- Área da máscara: {area['pixels']} px ({area['pct_da_imagem']}% da imagem)",
        f"- Deslocamento de enquadramento (gerada vs original): dx={dx:.2f}px dy={dy:.2f}px (confiança {resp:.2f})",
        f"- Proporção: original {prop_orig:.4f} | gerada {prop_ger:.4f}", "",
        "## O que a gerada mudou FORA da máscara (antes de recompor)",
        f"- Pixels diferentes: {bruto['pct_diferentes']}% | mudou mais que {LIMIAR_DIFF}: {bruto[f'pct_mudou_mais_que_{LIMIAR_DIFF}']}%",
        f"- Diferença média {bruto['diff_media']} | p99 {bruto['diff_p99']} | máx {bruto['diff_max']} | PSNR {bruto['psnr_db']} dB", "",
        "## Composto final fora da máscara (deve ser idêntico)",
        f"- Pixels diferentes: {final['pixels_diferentes']} -> **{'IDÊNTICO' if identico else 'DIVERGE'}**",
        f"- Original intacto após a execução (SHA-256): {hash_antes == hash_depois}", "",
    ]
    if aviso:
        md += ["## Avisos"] + [f"- {x}" for x in aviso] + [""]
    md += ["## Arquivos",
           "- `composto.png`, `diff_fora_mascara_gerada_bruta.png` (mapa de calor 4x), `relatorio.json`",
           "- `mascara_usada.png`: alfa de mistura (com `--suavizar` tem tons de cinza)",
           "- `suporte_booleano.png`: suporte exato medido (255 = onde pode mudar; 0 = tem de ser idêntico)"]
    (saida / "relatorio.md").write_text("\n".join(md), encoding="utf-8")

    # conferência FINAL, depois de todas as gravações (inclui relatorio.md): o original não pode ter mudado
    ok_final = sha256(orig_p) == hash_antes
    rel["original_intacto"]["igual_apos_todas_as_gravacoes"] = ok_final
    (saida / "relatorio.json").write_text(json.dumps(rel, ensure_ascii=False, indent=2), encoding="utf-8")
    md.append(f"- Original intacto após TODAS as gravações (SHA-256): {ok_final}")
    (saida / "relatorio.md").write_text("\n".join(md), encoding="utf-8")
    ok_final = ok_final and sha256(orig_p) == hash_antes  # e de novo após reescrever os relatórios
    print("\n".join(md))
    if not identico or not ok_final:
        sys.exit(2)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("mascara", help="cria máscara dos pontos claros numa região")
    m.add_argument("original"); m.add_argument("saida")
    m.add_argument("--roi", default="0,0,1,0.25", help="x0,y0,x1,y1 em frações (padrão: topo 25%%)")
    m.add_argument("--percentil", type=float, default=99.0, help="sensibilidade (maior = menos pontos)")
    m.add_argument("--dilatar", type=int, default=2)
    m.set_defaults(f=cmd_mascara)
    c = sub.add_parser("compor", help="recompõe a área da máscara sobre o original e mede o resto")
    c.add_argument("original"); c.add_argument("gerada"); c.add_argument("mascara"); c.add_argument("saida")
    c.add_argument("--dilatar", type=int, default=2, help="expande a máscara em px (cobre a borda das manchas)")
    c.add_argument("--suavizar", type=float, default=0.0, help="sigma de suavização da borda (0 = borda dura)")
    c.set_defaults(f=cmd_compor)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
