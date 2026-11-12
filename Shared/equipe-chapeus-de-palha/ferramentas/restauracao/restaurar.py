#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Restauracao local de fotos antigas, sem redesenhar a foto.

Uso:
    python restaurar.py <original> <pasta_saida> [--rosto 0.0-1.0] [--escala 2|4] [--cor] [--mascara arquivo.png]
                        [--sem-auto] [--limite-identidade N] [--cpu]

Etapas (cada uma salva separada em <pasta_saida>):
  1. 01_ajuste.png      OpenCV: niveis, tom/amarelado, contraste local suave (CLAHE), ruido leve. Nao redesenha.
  2. 02_riscos.png      LaMa so dentro da mascara (02_mascara.png). Fora da mascara os pixels sao os do passo 1.
  3. 03_rosto.png       GFPGAN v1.4 mesclado sobre o rosto do passo 2 com opacidade --rosto (0 = etapa nao roda).
  4. 04_resolucao_Nx.png  Real-ESRGAN 2x ou 4x.
  5. 05_cor.png         Colorizacao (so com --cor; so se houver modelo de licenca comercial).
  6. relatorio.json     Identidade rosto a rosto (original x resultado), area da mascara, parametros, versoes, tempos.
  7. lado_a_lado.png    Roda ..\\lado-a-lado.py: original | resultado | mapa de diferencas.

Tudo roda local: nenhuma foto sai desta maquina. Veja README.md e LICENCAS.md.
"""
import argparse
import gc
import hashlib
import json
import math
import platform
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageOps

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
MODELOS = AQUI / "modelos"
LADO_A_LADO = AQUI.parent / "lado-a-lado.py"

VERSAO = "0.1.0"
# Limites de identidade e escala da nota geometrica: calibrados em teste\calibracao.py (ver README.md). Valores provisorios ate la.
LIMITE_ORIGINAL = 0.40   # original -> resultado: folgado, porque o original tem riscos que a restauracao remove
LIMITE_ETAPA = 0.60      # cada etapa contra a anterior: rigoroso, isola o efeito de cada etapa
E0_GEOMETRIA = 0.045
METODO_IDENTIDADE = ("nota = min(geometria, estrutura). geometria: erro RMS dos 106 pontos dos tracos centrais (olhos, sobrancelhas, "
                     "nariz e labios) do MediaPipe Face Landmarker apos alinhamento por semelhanca, dividido pela distancia entre os "
                     "olhos, convertido por 1/(1+(erro/E0)^2). estrutura: SSIM do rosto alinhado (192 px, cinza, tons casados) dentro "
                     "de uma elipse central. Nenhum modelo de reconhecimento facial e usado (os mais comuns sao nao comerciais).")

# Deteccao de riscos: limiar = mediana + K_MAD * MAD do residual (abertura/fechamento); comprimento minimo de risco = fracao do lado menor.
K_MAD = 6.0
LIMIAR_MIN = 18.0
COMP_MIN_FRAC = 0.05
K_TEXTURA = 4.0  # o limiar por pixel nunca fica abaixo de K_TEXTURA x a mediana local do residual

# Modelo de 5 pontos do rosto FFHQ para recortes de 512 px (olho E, olho D, ponta do nariz, canto E e D da boca).
TEMPLATE_512 = np.array([[192.98138, 239.94708], [318.90277, 240.1936], [256.63416, 314.01935],
                         [201.26117, 371.41043], [313.08905, 371.15118]], dtype=np.float32)

# Indices do MediaPipe Face Mesh (478 pontos: 468 do rosto + 10 da iris).
OLHO_E = [33, 246, 161, 160, 159, 158, 157, 173, 133, 155, 154, 153, 145, 144, 163, 7]
OLHO_D = [362, 398, 384, 385, 386, 387, 388, 466, 263, 249, 390, 373, 374, 380, 381, 382]
SOBRANCELHA_E = [70, 63, 105, 66, 107, 55, 65, 52, 53, 46]
SOBRANCELHA_D = [300, 293, 334, 296, 336, 285, 295, 282, 283, 276]
LABIOS = [61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 308, 324, 318, 402, 317, 14, 87, 178, 88, 95, 185, 40, 39,
          37, 0, 267, 269, 270, 409, 415, 310, 311, 312, 13, 82, 81, 80, 191, 78]
NARIZ = [6, 168, 98, 327, 129, 358, 49, 279, 2, 1, 4, 5, 195, 197]
PONTOS_TRACOS = sorted(set(OLHO_E + OLHO_D + SOBRANCELHA_E + SOBRANCELHA_D + LABIOS + NARIZ))


def log(msg):
    print(msg, flush=True)


# ----------------------------------------------------------------------------- entrada e saida

def carregar_imagem(caminho):
    """Le qualquer imagem comum e devolve BGR uint8 (corrige a rotacao do EXIF; descarta transparencia)."""
    img = Image.open(caminho)
    img = ImageOps.exif_transpose(img)
    if img.mode in ("I;16", "I;16B", "I;16L", "I"):
        arr = np.asarray(img, dtype=np.float32)
        arr = arr / max(float(arr.max()), 1.0) * 255.0
        img = Image.fromarray(arr.astype(np.uint8))
    img = img.convert("RGB")
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)


def salvar_png(caminho, bgr):
    ok, buf = cv2.imencode(".png", bgr)
    if not ok:
        raise RuntimeError(f"nao consegui codificar {caminho}")
    buf.tofile(str(caminho))


def ler_mascara(caminho, forma):
    m = np.asarray(ImageOps.exif_transpose(Image.open(caminho)).convert("L"))
    if m.shape != forma:
        m = cv2.resize(m, (forma[1], forma[0]), interpolation=cv2.INTER_NEAREST)
    return ((m > 127).astype(np.uint8)) * 255


class Cronometro:
    def __init__(self):
        self.tempos = {}

    def medir(self, nome):
        outer = self

        class _Ctx:
            def __enter__(self_):
                self_.t = time.perf_counter()
                return self_

            def __exit__(self_, *exc):
                outer.tempos[nome] = round(time.perf_counter() - self_.t, 2)

        return _Ctx()


# ----------------------------------------------------------------------------- etapa 1: ajuste basico

def eh_monocromatica(bgr):
    lab = cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB).astype(np.float32)
    a, b = lab[..., 1] - 128.0, lab[..., 2] - 128.0
    croma = np.hypot(a, b)
    peso = croma > 3.0
    if peso.sum() < 200:
        return True
    p95 = float(np.percentile(croma, 95))
    ang = np.arctan2(b[peso], a[peso])
    concentracao = float(abs(np.mean(np.exp(1j * ang))))
    return p95 < 40.0 and concentracao > 0.85


def estimar_ruido(gray):
    """Metodo de Immerkaer: desvio padrao do ruido sem depender de bordas."""
    h, w = gray.shape
    n = np.array([[1, -2, 1], [-2, 4, -2], [1, -2, 1]], dtype=np.float32)
    s = cv2.filter2D(gray.astype(np.float32), -1, n)[1:-1, 1:-1]
    return float(math.sqrt(math.pi / 2.0) * np.abs(s).sum() / (6.0 * (w - 2) * (h - 2)))


def ajuste_basico(bgr, mono):
    info = {"monocromatica": bool(mono)}
    lab = cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB)
    L = lab[..., 0].astype(np.float32)
    lo, hi = np.percentile(L, (0.5, 99.5))
    ganho = float(min(255.0 / max(hi - lo, 1.0), 2.0))
    L = np.clip((L - lo) * ganho, 0, 255)
    info["niveis"] = {"p0_5": round(float(lo), 1), "p99_5": round(float(hi), 1), "ganho": round(ganho, 3)}

    L8 = L.astype(np.uint8)
    clahe = cv2.createCLAHE(clipLimit=1.6, tileGridSize=(8, 8))
    L = 0.6 * clahe.apply(L8).astype(np.float32) + 0.4 * L.astype(np.float32)
    info["clahe"] = {"clipLimit": 1.6, "grade": [8, 8], "mistura": 0.6}

    sigma = estimar_ruido(L8)
    h = float(np.clip(0.8 * sigma, 1.5, 5.0))
    Ld = cv2.fastNlMeansDenoising(np.clip(L, 0, 255).astype(np.uint8), None, h=h, templateWindowSize=7, searchWindowSize=21)
    info["ruido"] = {"sigma_estimado": round(sigma, 2), "h_nlm": round(h, 2)}

    if mono:
        out = cv2.cvtColor(Ld, cv2.COLOR_GRAY2BGR)
        info["cor"] = "convertida para tons de cinza neutros (remove o amarelado/sepia)"
    else:
        a = lab[..., 1].astype(np.float32)
        b = lab[..., 2].astype(np.float32)
        meio = (lab[..., 0] > 60) & (lab[..., 0] < 200)
        if meio.sum() > 100:
            da = float(np.clip(np.median(a[meio]) - 128.0, -25, 25))
            db = float(np.clip(np.median(b[meio]) - 128.0, -25, 25))
        else:
            da = db = 0.0
        a = cv2.GaussianBlur(a - 0.8 * da, (0, 0), 1.0)
        b = cv2.GaussianBlur(b - 0.8 * db, (0, 0), 1.0)
        merged = cv2.merge([Ld, np.clip(a, 0, 255).astype(np.uint8), np.clip(b, 0, 255).astype(np.uint8)])
        out = cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)
        info["cor"] = {"balanco_branco_deslocamento_a": round(-0.8 * da, 2), "balanco_branco_deslocamento_b": round(-0.8 * db, 2)}
    return out, info


# ----------------------------------------------------------------------------- rostos (MediaPipe)

class Rostos:
    """Detecta rostos e os 478 pontos com o MediaPipe Face Landmarker (Apache-2.0), em varias janelas."""

    def __init__(self):
        import mediapipe as mp
        from mediapipe.tasks import python as mpt
        from mediapipe.tasks.python import vision
        self.mp = mp
        self.det = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(
            base_options=mpt.BaseOptions(model_asset_path=str(MODELOS / "face_landmarker.task")),
            num_faces=25, min_face_detection_confidence=0.3, min_face_presence_confidence=0.3))

    def _janela(self, rgb):
        img = self.mp.Image(image_format=self.mp.ImageFormat.SRGB, data=np.ascontiguousarray(rgb))
        res = self.det.detect(img)
        h, w = rgb.shape[:2]
        return [np.array([[p.x * w, p.y * h] for p in lm], dtype=np.float32) for lm in res.face_landmarks]

    def detectar(self, bgr, fracs=(0.6, 0.35, 0.22)):
        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        h, w = rgb.shape[:2]
        escala_busca = 1.0
        rgb_b = rgb
        if max(h, w) > 2000:
            escala_busca = 2000.0 / max(h, w)
            rgb_b = cv2.resize(rgb, None, fx=escala_busca, fy=escala_busca, interpolation=cv2.INTER_AREA)
        hb, wb = rgb_b.shape[:2]
        brutos = [pts / escala_busca for pts in self._janela(rgb_b)]
        s = min(hb, wb)
        if s < 600:
            f = 640.0 / s
            for pts in self._janela(cv2.resize(rgb_b, None, fx=f, fy=f, interpolation=cv2.INTER_CUBIC)):
                brutos.append(pts / (f * escala_busca))
        for frac in fracs:
            W = max(int(s * frac), 64)
            passo = max(int(W * 0.5), 1)
            ys = list(range(0, max(hb - W, 0) + 1, passo))
            xs = list(range(0, max(wb - W, 0) + 1, passo))
            if ys[-1] != max(hb - W, 0):
                ys.append(max(hb - W, 0))
            if xs[-1] != max(wb - W, 0):
                xs.append(max(wb - W, 0))
            for y0 in ys:
                for x0 in xs:
                    crop = rgb_b[y0:y0 + W, x0:x0 + W]
                    f = 1.0
                    if W != 640:
                        f = 640.0 / W
                        interp = cv2.INTER_CUBIC if f > 1.0 else cv2.INTER_AREA
                        crop = cv2.resize(crop, None, fx=f, fy=f, interpolation=interp)
                    for pts in self._janela(crop):
                        brutos.append((pts / f + np.array([x0, y0], dtype=np.float32)) / escala_busca)
        return [self._refinar(rgb, c) for c in self._deduplicar(brutos, exigir_votos=True)]

    def _refinar(self, rgb, cara, exigir_sucesso=False):
        """Recorta o rosto com folga e redimensiona para 640 px antes de medir os 478 pontos.
        Garante que rostos de qualquer resolucao (ex.: antes e depois do Real-ESRGAN 2x/4x) sejam medidos na mesma escala."""
        bb = cara["bbox"]
        larg, alt = float(bb[2] - bb[0]), float(bb[3] - bb[1])
        h, w = rgb.shape[:2]
        cx, cy = (bb[0] + bb[2]) / 2.0, (bb[1] + bb[3]) / 2.0
        for mult in (2.0, 3.2, 4.2):
            lado = max(larg, alt) * mult
            x0, y0 = int(max(cx - lado / 2, 0)), int(max(cy - lado / 2, 0))
            x1, y1 = int(min(cx + lado / 2, w)), int(min(cy + lado / 2, h))
            crop = rgb[y0:y1, x0:x1]
            if crop.shape[0] < 16 or crop.shape[1] < 16:
                continue
            f = 640.0 / max(crop.shape[:2])
            interp = cv2.INTER_AREA if f < 1.0 else cv2.INTER_CUBIC
            melhor, iou_m = None, 0.0
            for pts in self._janela(cv2.resize(crop, None, fx=f, fy=f, interpolation=interp)):
                p2 = pts / f + np.array([x0, y0], dtype=np.float32)
                v = iou(self._bbox(p2), bb)
                if v > iou_m:
                    melhor, iou_m = p2, v
            if melhor is not None and iou_m >= 0.45:
                novo = dict(cara)
                novo["pts"], novo["bbox"] = melhor, self._bbox(melhor)
                return novo
        return None if exigir_sucesso else cara

    def medir_em(self, bgr, rostos_ref, shape_ref):
        """Remede em `bgr` cada rosto de `rostos_ref` (escalando a bbox de `shape_ref` para `bgr.shape`)."""
        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        hr, wr = shape_ref[:2]
        h, w = rgb.shape[:2]
        esc = np.array([w / wr, h / hr, w / wr, h / hr], dtype=np.float32)
        esc_pts = np.array([w / wr, h / hr], dtype=np.float32)
        out = []
        for r in rostos_ref:
            alvo = {"bbox": r["bbox"] * esc, "pts": r["pts"] * esc_pts, "votos": r.get("votos", 2)}
            medido = self._refinar(rgb, alvo, exigir_sucesso=True)
            if medido is not None:
                out.append(medido)
        return out

    @staticmethod
    def _bbox(pts):
        return np.array([pts[:, 0].min(), pts[:, 1].min(), pts[:, 0].max(), pts[:, 1].max()], dtype=np.float32)

    def _deduplicar(self, lista, exigir_votos):
        """Agrupa deteccoes do mesmo rosto e tira a mediana dos pontos das janelas que concordam.
        'votos' = em quantas janelas/escalas ele apareceu. Em imagens com varias janelas um 'rosto' achado so uma vez
        costuma ser textura (roupa, parede) e e descartado."""
        itens = []
        for pts in lista:
            bb = self._bbox(pts)
            if (bb[2] - bb[0]) < 20 or (bb[3] - bb[1]) < 20:
                continue
            itens.append({"pts": pts, "bbox": bb})
        itens.sort(key=lambda d: -(d["bbox"][2] - d["bbox"][0]) * (d["bbox"][3] - d["bbox"][1]))
        mantidos = []
        for d in itens:
            if all(iou(d["bbox"], m["bbox"]) < 0.3 for m in mantidos):
                grupo = [it["pts"] for it in itens if iou(d["bbox"], it["bbox"]) >= 0.3]
                pts_med = np.median(np.stack(grupo, axis=0), axis=0).astype(np.float32)
                mantidos.append({"pts": pts_med, "bbox": self._bbox(pts_med), "votos": len(grupo)})
        if exigir_votos:
            mantidos = [d for d in mantidos if d["votos"] >= 2]
        mantidos.sort(key=lambda d: d["bbox"][0])
        return mantidos

    def fechar(self):
        self.det.close()


def iou(a, b):
    x0, y0 = max(a[0], b[0]), max(a[1], b[1])
    x1, y1 = min(a[2], b[2]), min(a[3], b[3])
    inter = max(0.0, x1 - x0) * max(0.0, y1 - y0)
    ua = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
    return float(inter / ua) if ua > 0 else 0.0


def cinco_pontos(pts):
    olho_e = pts[OLHO_E].mean(axis=0)
    olho_d = pts[OLHO_D].mean(axis=0)
    olhos = sorted([olho_e, olho_d], key=lambda p: p[0])
    boca = sorted([pts[61], pts[291]], key=lambda p: p[0])
    return np.array([olhos[0], olhos[1], pts[1], boca[0], boca[1]], dtype=np.float32)


def distancia_olhos(pts):
    return float(np.linalg.norm(pts[OLHO_E].mean(axis=0) - pts[OLHO_D].mean(axis=0)))


def _preencher(forma, grupos, pts, dilatar):
    m = np.zeros(forma, np.uint8)
    for g in grupos:
        hull = cv2.convexHull(pts[g].astype(np.int32))
        cv2.fillConvexPoly(m, hull, 255)
    if dilatar > 0:
        m = cv2.dilate(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * dilatar + 1, 2 * dilatar + 1)))
    return m


def mascara_protecao(rostos, forma):
    """Olhos, sobrancelhas, labios e nariz: nunca entram na mascara automatica de riscos."""
    m = np.zeros(forma, np.uint8)
    for r in rostos:
        pts = r["pts"][:468]
        larg = r["bbox"][2] - r["bbox"][0]
        d = max(2, int(0.05 * larg))
        m |= _preencher(forma, [OLHO_E + SOBRANCELHA_E, OLHO_D + SOBRANCELHA_D, LABIOS, NARIZ], pts, d)
    return m


def mascara_oval(rostos, forma):
    m = np.zeros(forma, np.uint8)
    for r in rostos:
        hull = cv2.convexHull(r["pts"][:468].astype(np.int32))
        cv2.fillConvexPoly(m, hull, 255)
    return m


# ----------------------------------------------------------------------------- etapa 2: riscos (mascara + LaMa)

def detectar_riscos(gray, rostos, max_pct):
    """Mascara automatica de riscos finos (claros e escuros) e poeira. Conservadora de proposito:
    fora dos rostos aceita linhas finas e longas e pontos pequenos isolados; dentro dos rostos so aceita linhas
    longas e retas (risco), nunca pontos (podem ser pintas) e nunca olhos, sobrancelhas, labios ou nariz."""
    h, w = gray.shape
    m = min(h, w)
    g = cv2.GaussianBlur(gray, (0, 0), 0.8)
    k = int(max(5, round(m / 150.0))) | 1
    ell = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k))
    claro = cv2.subtract(g, cv2.morphologyEx(g, cv2.MORPH_OPEN, ell))
    escuro = cv2.subtract(cv2.morphologyEx(g, cv2.MORPH_CLOSE, ell), g)
    res = np.maximum(claro, escuro)
    med = float(np.median(res))
    mad = float(np.median(np.abs(res.astype(np.float32) - med))) + 1e-3
    limiar = max(LIMIAR_MIN, med + K_MAD * 1.4826 * mad)
    # textura local: mediana do residual numa janela grande. Em tecido, cabelo e grao o residual e alto em toda parte,
    # entao o limiar sobe ali; em fundo liso (onde riscos e poeira aparecem) ele fica no minimo.
    peq = cv2.resize(res, None, fx=0.25, fy=0.25, interpolation=cv2.INTER_AREA)
    loc = cv2.resize(cv2.medianBlur(peq, 31), (w, h), interpolation=cv2.INTER_LINEAR).astype(np.float32)
    cand = (res.astype(np.float32) > np.maximum(limiar, K_TEXTURA * loc)).astype(np.uint8)
    cand = cv2.morphologyEx(cand, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
    gb = cv2.GaussianBlur(gray, (0, 0), max(1.5, k / 3.0)).astype(np.float32)
    grad = (np.hypot(cv2.Sobel(gb, cv2.CV_32F, 1, 0), cv2.Sobel(gb, cv2.CV_32F, 0, 1)) / 8.0)

    prot = mascara_protecao(rostos, (h, w)) > 0
    oval = mascara_oval(rostos, (h, w)) > 0
    larg_rosto = max([r["bbox"][2] - r["bbox"][0] for r in rostos], default=0.0)

    n, rot, st, _ = cv2.connectedComponentsWithStats(cand, connectivity=8)
    area_poeira = max(20.0, 0.8 * (0.02 * m) ** 2)
    comp_min = max(20.0, COMP_MIN_FRAC * m)
    mask = np.zeros((h, w), np.uint8)
    motivos = {"aceito_linha": 0, "aceito_poeira": 0, "pequeno": 0, "no_rosto_protegido": 0, "no_rosto_nao_linha": 0,
               "textura_ao_redor": 0, "junto_de_borda_grande": 0, "nem_linha_nem_poeira": 0}
    for i in range(1, n):
        x, y, bw, bh, area = (int(v) for v in st[i])
        if area < 3:
            motivos["pequeno"] += 1
            continue
        comp = (rot[y:y + bh, x:x + bw] == i).astype(np.uint8)
        pad = 8
        y0, y1 = max(y - pad, 0), min(y + bh + pad, h)
        x0, x1 = max(x - pad, 0), min(x + bw + pad, w)
        comp_g = np.zeros((y1 - y0, x1 - x0), np.uint8)
        comp_g[(y - y0):(y - y0 + bh), (x - x0):(x - x0 + bw)] = comp
        cont = float(res[y:y + bh, x:x + bw][comp > 0].mean())
        no_oval = bool(oval[y:y + bh, x:x + bw][comp > 0].mean() > 0.5)
        toca_prot = bool(prot[y0:y1, x0:x1][cv2.dilate(comp_g, np.ones((5, 5), np.uint8)) > 0].any())
        if toca_prot:
            motivos["no_rosto_protegido"] += 1
            continue
        pts = cv2.findNonZero(comp_g)
        (_, _), (rw, rh), _ = cv2.minAreaRect(pts)
        longo, curto = max(rw, rh), max(min(rw, rh), 1.0)
        esq = cv2.ximgproc.thinning(comp_g * 255)
        comp_len = float(max(np.count_nonzero(esq), 1))
        larg_media = area / comp_len
        reta = longo / comp_len
        eh_linha = comp_len >= comp_min and larg_media <= (0.012 * m + 3) and (longo / curto >= 6 or comp_len >= 2.5 * comp_min)
        anel = cv2.dilate(comp_g, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))) - cv2.dilate(comp_g, np.ones((5, 5), np.uint8))
        vals = g[y0:y1, x0:x1][anel > 0]
        anel_dp = float(vals.std()) if vals.size else 99.0
        grad_med = float(grad[y0:y1, x0:x1][comp_g > 0].mean())
        if grad_med > 0.12 * cont + 3.0:
            motivos["junto_de_borda_grande"] += 1
            continue
        if no_oval:
            if not (eh_linha and comp_len >= 0.35 * larg_rosto and reta >= 0.75 and cont >= 2.5 * (anel_dp + 2.0)):
                motivos["no_rosto_nao_linha"] += 1
                continue
            mask[y0:y1, x0:x1] |= comp_g
            motivos["aceito_linha"] += 1
            continue
        if eh_linha:
            if cont >= 2.5 * (anel_dp + 2.0):
                mask[y0:y1, x0:x1] |= comp_g
                motivos["aceito_linha"] += 1
            else:
                motivos["textura_ao_redor"] += 1
        elif area <= area_poeira:
            if cont >= 3.5 * (anel_dp + 2.0):
                mask[y0:y1, x0:x1] |= comp_g
                motivos["aceito_poeira"] += 1
            else:
                motivos["textura_ao_redor"] += 1
        else:
            motivos["nem_linha_nem_poeira"] += 1
    r = max(1, int(round(m / 600.0)) + 1)
    mask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))) * 255
    mask = (mask > 0).astype(np.uint8) * 255
    pct = 100.0 * float((mask > 0).sum()) / (h * w)
    stats = {"limiar": round(limiar, 1), "kernel_morfologico": k, "componentes_candidatos": int(n - 1), "motivos": motivos,
             "dilatacao_px": r}
    if pct > max_pct:
        stats["aviso"] = (f"mascara automatica ocupou {pct:.1f}% da imagem (limite {max_pct:.0f}%): NAO aplicada. "
                          "Use --mascara com uma mascara manual.")
        return np.zeros((h, w), np.uint8), stats
    return mask, stats


class LaMa:
    """LaMa big-lama em ONNX (Carve/LaMa-ONNX, Apache-2.0), entrada fixa de 512x512."""
    _cache = {}

    def __init__(self, usar_gpu):
        if usar_gpu not in LaMa._cache:
            import onnxruntime as ort
            disp = ort.get_available_providers()
            prov = ["CUDAExecutionProvider", "CPUExecutionProvider"] if (usar_gpu and "CUDAExecutionProvider" in disp) else ["CPUExecutionProvider"]
            LaMa._cache[usar_gpu] = ort.InferenceSession(str(MODELOS / "lama_fp32.onnx"), providers=prov)
        self.sess = LaMa._cache[usar_gpu]
        self.provedor = self.sess.get_providers()[0]

    def __call__(self, rgb512, mask512):
        x = (rgb512.astype(np.float32) / 255.0).transpose(2, 0, 1)[None]
        m = (mask512 > 0).astype(np.float32)[None, None]
        out = self.sess.run(None, {"image": x, "mask": m})[0][0]
        if float(out.max()) <= 1.5:
            out = out * 255.0
        return np.clip(out.transpose(1, 2, 0), 0, 255).astype(np.uint8)


def inpaint_lama(bgr, mask, lama):
    """Preenche so os pixels da mascara. Fora dela a saida e identica a entrada."""
    h, w = bgr.shape[:2]
    S, BLK = 512, 384
    ph, pw = max(S - h, 0), max(S - w, 0)
    if ph or pw:
        modo = "reflect" if (ph < h and pw < w) else "edge"
        img_p = np.pad(bgr, ((0, ph), (0, pw), (0, 0)), mode=modo)
        msk_p = np.pad(mask, ((0, ph), (0, pw)), mode="constant")
    else:
        img_p, msk_p = bgr, mask
    H, W = img_p.shape[:2]
    out = bgr.copy()
    janelas = 0
    for by0 in range(0, h, BLK):
        for bx0 in range(0, w, BLK):
            by1, bx1 = min(by0 + BLK, h), min(bx0 + BLK, w)
            blk = mask[by0:by1, bx0:bx1]
            if not blk.any():
                continue
            cy, cx = (by0 + by1) // 2, (bx0 + bx1) // 2
            wy0 = int(np.clip(cy - S // 2, 0, H - S))
            wx0 = int(np.clip(cx - S // 2, 0, W - S))
            win = img_p[wy0:wy0 + S, wx0:wx0 + S]
            wm = msk_p[wy0:wy0 + S, wx0:wx0 + S]
            res = lama(cv2.cvtColor(win, cv2.COLOR_BGR2RGB), wm)
            res = cv2.cvtColor(res, cv2.COLOR_RGB2BGR)
            sub = res[(by0 - wy0):(by1 - wy0), (bx0 - wx0):(bx1 - wx0)]
            alvo = out[by0:by1, bx0:bx1]
            alvo[blk > 0] = sub[blk > 0]
            janelas += 1
    return out, janelas


# ----------------------------------------------------------------------------- etapa 3: rosto (GFPGAN)

def carregar_gfpgan(dispositivo):
    import torch
    from vendor.gfpganv1_clean_arch import GFPGANv1Clean
    net = GFPGANv1Clean(out_size=512, num_style_feat=512, channel_multiplier=2, decoder_load_path=None, fix_decoder=False,
                        num_mlp=8, input_is_latent=True, different_w=True, narrow=1, sft_half=True)
    net.load_state_dict(torch.load(MODELOS / "GFPGANv1.4.pth", map_location="cpu", weights_only=True)["params_ema"], strict=True)
    return net.eval().to(dispositivo)


def restaurar_recorte(net, recorte_bgr, dispositivo):
    import torch
    rgb = recorte_bgr[..., ::-1].astype(np.float32) / 255.0
    t = torch.from_numpy(rgb.transpose(2, 0, 1)).unsqueeze(0).to(dispositivo)
    t = (t - 0.5) / 0.5
    with torch.no_grad():
        saida = net(t, return_rgb=False, randomize_noise=False)[0]
    s = saida.squeeze(0).float().clamp_(-1, 1).cpu().numpy()
    return ((s.transpose(1, 2, 0) + 1.0) / 2.0 * 255.0).round().astype(np.uint8)[..., ::-1].copy()


def mascara_oval_512():
    m = np.zeros((512, 512), np.float32)
    cv2.ellipse(m, (256, 268), (172, 208), 0, 0, 360, 1.0, -1)
    return cv2.GaussianBlur(m, (0, 0), 16)


def recorte_alinhado(bgr, M, tamanho=512, borda=(135, 133, 132)):
    """Recorta o rosto alinhado (matriz M: imagem -> recorte). Reduz antes se o rosto for muito maior que o recorte."""
    s = math.hypot(M[0, 0], M[1, 0])
    if s < 0.6:
        f = float(min(1.0, max(s * 1.5, 0.05)))
        pequeno = cv2.resize(bgr, None, fx=f, fy=f, interpolation=cv2.INTER_AREA)
        M2 = M.copy()
        M2[:, :2] = M[:, :2] / f
        return cv2.warpAffine(pequeno, M2, (tamanho, tamanho), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=borda)
    return cv2.warpAffine(bgr, M, (tamanho, tamanho), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=borda)


def preparar_rosto(orig512, rest512, mono):
    """Mantem o brilho de baixa frequencia e a cor da foto; usa do GFPGAN so o detalhe fino (luminancia)."""
    lo = cv2.cvtColor(orig512, cv2.COLOR_BGR2LAB)
    lr = cv2.cvtColor(rest512, cv2.COLOR_BGR2LAB)
    Lo, Lr = lo[..., 0].astype(np.float32), lr[..., 0].astype(np.float32)
    L = Lr - cv2.GaussianBlur(Lr, (0, 0), 8) + cv2.GaussianBlur(Lo, (0, 0), 8)
    L = np.clip(L, 0, 255).astype(np.uint8)
    if mono:
        a = b = np.full_like(L, 128)
    else:
        a, b = lo[..., 1], lo[..., 2]
    return cv2.cvtColor(cv2.merge([L, a, b]), cv2.COLOR_LAB2BGR)


def colar_rosto(base, preparado512, M, alfa, mascara512):
    h, w = base.shape[:2]
    Minv = cv2.invertAffineTransform(M)
    cantos = np.array([[[0, 0], [512, 0], [512, 512], [0, 512]]], dtype=np.float32)
    p = cv2.transform(cantos, Minv)[0]
    x0, y0 = int(max(0, math.floor(p[:, 0].min()) - 2)), int(max(0, math.floor(p[:, 1].min()) - 2))
    x1, y1 = int(min(w, math.ceil(p[:, 0].max()) + 2)), int(min(h, math.ceil(p[:, 1].max()) + 2))
    if x1 <= x0 or y1 <= y0:
        return base
    Mr = Minv.copy()
    Mr[0, 2] -= x0
    Mr[1, 2] -= y0
    tam = (x1 - x0, y1 - y0)
    rest = cv2.warpAffine(preparado512, Mr, tam, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    msk = cv2.warpAffine(mascara512, Mr, tam, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    a = (msk * float(alfa))[..., None]
    roi = base[y0:y1, x0:x1].astype(np.float32)
    base[y0:y1, x0:x1] = np.clip(roi * (1.0 - a) + rest.astype(np.float32) * a, 0, 255).astype(np.uint8)
    return base


def etapa_rosto(bgr, rostos, alfa, mono, dispositivo):
    net = carregar_gfpgan(dispositivo)
    saida = bgr.copy()
    mascara = mascara_oval_512()
    n = 0
    for r in rostos:
        p5 = cinco_pontos(r["pts"])
        M = cv2.estimateAffinePartial2D(p5, TEMPLATE_512, method=cv2.LMEDS)[0]
        if M is None:
            continue
        orig512 = recorte_alinhado(bgr, M)
        rest512 = restaurar_recorte(net, orig512, dispositivo)
        saida = colar_rosto(saida, preparar_rosto(orig512, rest512, mono), M, alfa, mascara)
        n += 1
    del net
    return saida, n


# ----------------------------------------------------------------------------- etapa 4: resolucao (Real-ESRGAN)

def ampliar(bgr, escala, dispositivo, usar_half):
    import torch
    from vendor.rrdbnet_arch import RRDBNet
    net = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=escala)
    net.load_state_dict(torch.load(MODELOS / f"RealESRGAN_x{escala}plus.pth", map_location="cpu", weights_only=True)["params_ema"], strict=True)
    net = net.eval().to(dispositivo)
    if usar_half:
        net = net.half()
    h, w = bgr.shape[:2]
    out = np.zeros((h * escala, w * escala, 3), np.uint8)
    tile, pad = 256, 16
    for y in range(0, h, tile):
        for x in range(0, w, tile):
            y0, y1 = max(y - pad, 0), min(y + tile + pad, h)
            x0, x1 = max(x - pad, 0), min(x + tile + pad, w)
            patch = bgr[y0:y1, x0:x1]
            ph, pw = patch.shape[:2]
            if ph % 2 or pw % 2:
                patch = np.pad(patch, ((0, ph % 2), (0, pw % 2), (0, 0)), mode="reflect" if min(ph, pw) > 1 else "edge")
            rgb = patch[..., ::-1].astype(np.float32) / 255.0
            t = torch.from_numpy(rgb.transpose(2, 0, 1)).unsqueeze(0).to(dispositivo)
            if usar_half:
                t = t.half()
            with torch.no_grad():
                o = net(t)
            o = o.squeeze(0).float().clamp_(0, 1).cpu().numpy().transpose(1, 2, 0)
            o = (o * 255.0).round().astype(np.uint8)[..., ::-1]
            o = o[:ph * escala, :pw * escala]
            oy0, ox0 = (y - y0) * escala, (x - x0) * escala
            ty, tx = min(tile, h - y), min(tile, w - x)
            out[y * escala:(y + ty) * escala, x * escala:(x + tx) * escala] = o[oy0:oy0 + ty * escala, ox0:ox0 + tx * escala]
    del net
    return out


# ----------------------------------------------------------------------------- etapa 5: cor (opcional)

def colorizar(bgr, dispositivo, mono, intensidade):
    """Colorizacao com DDColor tiny (Apache-2.0). So gera os canais de cor (a, b do Lab); a luminancia (L) da foto
    e mantida como esta. Devolve (imagem ou None, aviso)."""
    arq = MODELOS / "ddcolor_paper_tiny.pth"
    if not mono:
        return None, "a foto ja e colorida: colorizacao nao aplicada"
    if not arq.is_file():
        return None, "colorizacao indisponivel: falta modelos\\ddcolor_paper_tiny.pth (rode baixar-modelos.sh)"
    import torch
    from vendor.ddcolor.ddcolor_arch import DDColor
    modelo = DDColor(encoder_name="convnext-t", decoder_name="MultiScaleColorDecoder", input_size=[512, 512],
                     num_output_channels=2, last_norm="Spectral", do_normalize=False, num_queries=100, num_scales=3, dec_layers=9)
    sd = torch.load(arq, map_location="cpu", weights_only=True)
    sd = sd["params"] if isinstance(sd, dict) and "params" in sd else sd
    res = modelo.load_state_dict(sd, strict=False)
    modelo = modelo.eval().to(dispositivo)
    h, w = bgr.shape[:2]
    peq = cv2.resize(bgr, (512, 512), interpolation=cv2.INTER_AREA).astype(np.float32) / 255.0
    L = cv2.cvtColor(peq, cv2.COLOR_BGR2Lab)[:, :, :1]
    cinza = cv2.cvtColor(np.concatenate([L, np.zeros_like(L), np.zeros_like(L)], axis=-1), cv2.COLOR_LAB2RGB)
    t = torch.from_numpy(cinza.transpose(2, 0, 1)).float().unsqueeze(0).to(dispositivo)
    with torch.no_grad():
        ab = modelo(t).float().cpu()[0].numpy().transpose(1, 2, 0) * float(intensidade)
    del modelo
    ab8 = np.clip(np.round(cv2.resize(ab.astype(np.float32), (w, h), interpolation=cv2.INTER_CUBIC) + 128.0), 0, 255).astype(np.uint8)
    lab8 = cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB)
    lab8[..., 1:] = ab8
    aviso = ("a cor e interpretacao do modelo DDColor (tiny, intensidade %.2f), nao a cor real da foto; avisar o cliente. "
             "pesos fora do esperado: %d ausentes, %d inesperados" % (intensidade, len(res.missing_keys), len(res.unexpected_keys)))
    return cv2.cvtColor(lab8, cv2.COLOR_LAB2BGR), aviso


# ----------------------------------------------------------------------------- etapa 6: identidade

def umeyama(src, dst):
    """Transformacao por semelhanca (escala, rotacao, translacao) que leva src em dst."""
    mu_s, mu_d = src.mean(0), dst.mean(0)
    s0, d0 = src - mu_s, dst - mu_d
    cov = d0.T @ s0 / len(src)
    U, D, Vt = np.linalg.svd(cov)
    S = np.eye(2)
    if np.linalg.det(U) * np.linalg.det(Vt) < 0:
        S[1, 1] = -1
    R = U @ S @ Vt
    var_s = (s0 ** 2).sum() / len(src)
    c = float((D * np.diag(S)).sum() / var_s) if var_s > 0 else 1.0
    t = mu_d - c * R @ mu_s
    return c, R, t


def erro_geometrico(pts_o, pts_r):
    po, pr = pts_o[PONTOS_TRACOS], pts_r[PONTOS_TRACOS]
    c, R, t = umeyama(pr, po)
    pr2 = (c * (R @ pr.T)).T + t
    erro = np.sqrt(((pr2 - po) ** 2).sum(axis=1).mean()) / max(distancia_olhos(pts_o), 1e-6)
    return float(erro)


def _ssim_mapa(a, b):
    a, b = a.astype(np.float32), b.astype(np.float32)
    C1, C2 = (0.01 * 255) ** 2, (0.03 * 255) ** 2
    g = lambda x: cv2.GaussianBlur(x, (11, 11), 1.5)
    mu_a, mu_b = g(a), g(b)
    saa, sbb, sab = g(a * a) - mu_a ** 2, g(b * b) - mu_b ** 2, g(a * b) - mu_a * mu_b
    return ((2 * mu_a * mu_b + C1) * (2 * sab + C2)) / ((mu_a ** 2 + mu_b ** 2 + C1) * (saa + sbb + C2))


def _recorte_canonico(bgr, pts, tam=192):
    tmpl = TEMPLATE_512 * (tam / 512.0)
    M = cv2.estimateAffinePartial2D(cinco_pontos(pts), tmpl, method=cv2.LMEDS)[0]
    if M is None:
        return None
    s = math.hypot(M[0, 0], M[1, 0])
    if s < 0.5:
        f = float(max(s * 1.5, 0.05))
        bgr = cv2.resize(bgr, None, fx=f, fy=f, interpolation=cv2.INTER_AREA)
        M = M.copy()
        M[:, :2] = M[:, :2] / f
    c = cv2.warpAffine(bgr, M, (tam, tam), flags=cv2.INTER_AREA, borderMode=cv2.BORDER_REPLICATE)
    g = cv2.cvtColor(c, cv2.COLOR_BGR2GRAY)
    return cv2.GaussianBlur(g, (0, 0), 1.5)


def estrutura_rosto(bgr_o, pts_o, bgr_r, pts_r):
    a = _recorte_canonico(bgr_o, pts_o)
    b = _recorte_canonico(bgr_r, pts_r)
    if a is None or b is None:
        return 0.0
    tam = a.shape[0]
    elipse = np.zeros((tam, tam), np.uint8)
    cv2.ellipse(elipse, (tam // 2, int(tam * 0.52)), (int(tam * 0.34), int(tam * 0.40)), 0, 0, 360, 255, -1)
    sel = elipse > 0
    x, y = b[sel].astype(np.float64), a[sel].astype(np.float64)
    var = x.var()
    if var < 1e-6:
        return 0.0
    k = float(((x - x.mean()) * (y - y.mean())).mean() / var)
    b2 = np.clip(k * b.astype(np.float32) + float(y.mean() - k * x.mean()), 0, 255)
    return float(np.clip(_ssim_mapa(a, b2)[sel].mean(), 0.0, 1.0))


def nota_geometria(erro, e0=E0_GEOMETRIA):
    return float(1.0 / (1.0 + (erro / e0) ** 2))


def comparar_rostos(bgr_o, rostos_o, bgr_r, rostos_r, limite):
    """Casa cada rosto do original com o rosto na mesma posicao relativa do resultado e da a nota."""
    ho, wo = bgr_o.shape[:2]
    hr, wr = bgr_r.shape[:2]
    norm_o = np.array([wo, ho, wo, ho], np.float32)
    norm_r = np.array([wr, hr, wr, hr], np.float32)
    saida = []
    for i, ro in enumerate(rostos_o):
        bo = ro["bbox"] / norm_o
        melhor, iou_m = None, 0.0
        for rr in rostos_r:
            v = iou(bo, rr["bbox"] / norm_r)
            if v > iou_m:
                melhor, iou_m = rr, v
        item = {"rosto": i + 1, "bbox_original_px": [round(float(v), 1) for v in ro["bbox"]], "votos_deteccao": int(ro.get("votos", 1))}
        if melhor is None or iou_m < 0.3:
            item.update({"detectado_no_resultado": False, "nota": 0.0, "status": "REPROVADO",
                         "motivo": "rosto nao encontrado no resultado"})
        else:
            erro = erro_geometrico(ro["pts"], melhor["pts"])
            ng = nota_geometria(erro)
            ne = estrutura_rosto(bgr_o, ro["pts"], bgr_r, melhor["pts"])
            nota = min(ng, ne)
            item.update({"detectado_no_resultado": True, "erro_geometrico_norm": round(erro, 4),
                         "nota_geometria": round(ng, 3), "ssim_estrutura": round(ne, 3), "nota": round(nota, 3),
                         "status": "APROVADO" if nota >= limite else "REPROVADO"})
        saida.append(item)
    return saida


# ----------------------------------------------------------------------------- relatorio e principal

def sha256_modelos():
    arq = MODELOS / "SHA256.txt"
    d = {}
    if arq.exists():
        for linha in arq.read_text(encoding="utf-8").splitlines():
            partes = linha.split(None, 1)
            if len(partes) == 2:
                d[partes[1].strip()] = partes[0]
    return d


def ambiente():
    import onnxruntime
    import mediapipe
    import torch
    amb = {"python": platform.python_version(), "sistema": platform.platform(), "numpy": np.__version__, "opencv": cv2.__version__,
           "pillow": Image.__version__, "torch": torch.__version__, "cuda_torch": torch.version.cuda,
           "onnxruntime": onnxruntime.__version__, "mediapipe": mediapipe.__version__, "script": VERSAO}
    amb["gpu"] = torch.cuda.get_device_name(0) if torch.cuda.is_available() else None
    return amb


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("original")
    p.add_argument("saida", help="pasta de saida (criada se nao existir)")
    p.add_argument("--rosto", type=float, default=0.5, help="opacidade do rosto restaurado (GFPGAN), 0.0 a 1.0; 0 pula a etapa. Padrao 0.5")
    p.add_argument("--escala", type=int, choices=(2, 4), default=2, help="Real-ESRGAN 2x ou 4x. Padrao 2")
    p.add_argument("--cor", action="store_true", help="colorizar com DDColor (so fotos preto e branco/sepia; a cor e interpretacao)")
    p.add_argument("--cor-intensidade", type=float, default=0.8, help="escala da cor do DDColor, 0.0 a 1.0+. Padrao 0.8 (mais discreta)")
    p.add_argument("--mascara", help="PNG com a mascara manual (branco = reparar); soma-se a automatica")
    p.add_argument("--sem-auto", action="store_true", help="nao detectar riscos automaticamente (usa so --mascara)")
    p.add_argument("--max-mascara", type=float, default=12.0, help="se a mascara automatica passar desse %% da imagem, nao e aplicada")
    p.add_argument("--limite-original", type=float, default=LIMITE_ORIGINAL, help="nota minima original -> resultado (folgado)")
    p.add_argument("--limite-etapa", type=float, default=LIMITE_ETAPA, help="nota minima de cada etapa contra a anterior (rigoroso)")
    p.add_argument("--cpu", action="store_true", help="nao usar a GPU")
    args = p.parse_args(argv)
    if not 0.0 <= args.rosto <= 1.0:
        p.error("--rosto precisa estar entre 0.0 e 1.0")
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    import torch  # primeiro: carrega as DLLs CUDA/cuDNN que o onnxruntime tambem usa
    usar_gpu = torch.cuda.is_available() and not args.cpu
    disp = torch.device("cuda" if usar_gpu else "cpu")

    origem = Path(args.original)
    pasta = Path(args.saida)
    pasta.mkdir(parents=True, exist_ok=True)
    cron, avisos = Cronometro(), []
    t_total = time.perf_counter()
    orig_disco = carregar_imagem(origem)
    h_disco, w_disco = orig_disco.shape[:2]
    log(f"Entrada: {origem.name} ({w_disco}x{h_disco}) | dispositivo: {'GPU (CUDA)' if usar_gpu else 'CPU'}")
    rel = {"versao": VERSAO, "data": datetime.now().replace(microsecond=0).isoformat(),
           "entrada": {"arquivo": origem.name, "largura": w_disco, "altura": h_disco},
           "parametros": {"rosto": args.rosto, "escala": args.escala, "cor": args.cor, "mascara_manual": bool(args.mascara),
                          "sem_auto": args.sem_auto, "max_mascara_pct": args.max_mascara, "dispositivo": "cuda" if usar_gpu else "cpu"},
           "etapas": {}, "avisos": avisos}

    rostos_cls = Rostos()
    orig = orig_disco
    rotacao_interna = 0
    with cron.medir("deteccao_rostos_original"):
        rostos_orig = rostos_cls.detectar(orig)
        if len(rostos_orig) <= 5:
            for ang, cod_rot in ((-90, cv2.ROTATE_90_COUNTERCLOCKWISE), (90, cv2.ROTATE_90_CLOCKWISE)):
                cand_img = cv2.rotate(orig_disco, cod_rot)
                cand_r = rostos_cls.detectar(cand_img, fracs=(0.6, 0.35))
                if len(cand_r) >= max(4, len(rostos_orig) * 2):
                    orig = cand_img
                    rotacao_interna = ang
                    rostos_orig = rostos_cls.detectar(orig)
                    avisos.append(f"foto detectada deitada: processada em pe (rotacao interna {ang} graus) e salva na orientacao original (+ resultado_em_pe.png)")
                    break
    h0, w0 = orig.shape[:2]
    if rotacao_interna:
        rel["entrada"]["rotacao_interna_graus"] = rotacao_interna
    log(f"Rostos detectados no original: {len(rostos_orig)}" + (f" (rotacao interna {rotacao_interna} graus)" if rotacao_interna else ""))

    def para_disco(img):
        if rotacao_interna == -90:
            return cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        if rotacao_interna == 90:
            return cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        return img

    # 1. ajuste basico
    with cron.medir("1_ajuste"):
        mono = eh_monocromatica(orig)
        e1, info1 = ajuste_basico(orig, mono)
    salvar_png(pasta / "01_ajuste.png", para_disco(e1))
    rel["etapas"]["1_ajuste"] = info1
    etapas = {"01_ajuste": e1}
    log(f"[1] ajuste basico: ok ({cron.tempos['1_ajuste']}s) | monocromatica={mono}")

    # rostos na imagem ajustada (melhor contraste) servem a mascara e ao GFPGAN; se achou rosto que faltou no original desbotado, completa rostos_orig
    with cron.medir("deteccao_rostos_ajustada"):
        rostos_adj = rostos_cls.detectar(e1)
        rgb_orig = cv2.cvtColor(orig, cv2.COLOR_BGR2RGB)
        for ra in rostos_adj:
            if all(iou(ra["bbox"], ro["bbox"]) < 0.3 for ro in rostos_orig):
                med_o = rostos_cls._refinar(rgb_orig, ra, exigir_sucesso=True)
                rostos_orig.append(med_o if med_o is not None else dict(ra))
        rostos_orig.sort(key=lambda d: d["bbox"][0])
        rgb_e1 = cv2.cvtColor(e1, cv2.COLOR_BGR2RGB)
        for ro in rostos_orig:
            if all(iou(ro["bbox"], ra["bbox"]) < 0.3 for ra in rostos_adj):
                med_1 = rostos_cls._refinar(rgb_e1, ro, exigir_sucesso=True)
                rostos_adj.append(med_1 if med_1 is not None else dict(ro))
        rostos_adj.sort(key=lambda d: d["bbox"][0])
    rostos_cls.fechar()

    # 2. riscos
    with cron.medir("2_riscos"):
        gray = cv2.cvtColor(e1, cv2.COLOR_BGR2GRAY)
        if args.sem_auto:
            auto, st = np.zeros((h0, w0), np.uint8), {"auto": "desligada (--sem-auto)"}
        else:
            auto, st = detectar_riscos(gray, rostos_adj, args.max_mascara)
        if "aviso" in st:
            avisos.append(st["aviso"])
        mascara = auto.copy()
        if args.mascara:
            m_usr = ler_mascara(args.mascara, (h_disco, w_disco))
            if rotacao_interna == -90:
                m_usr = cv2.rotate(m_usr, cv2.ROTATE_90_COUNTERCLOCKWISE)
            elif rotacao_interna == 90:
                m_usr = cv2.rotate(m_usr, cv2.ROTATE_90_CLOCKWISE)
            mascara = np.maximum(mascara, m_usr)
        e2, janelas, provedor = e1, 0, None
        if mascara.any():
            lama = LaMa(usar_gpu)
            provedor = lama.provedor
            e2, janelas = inpaint_lama(e1, mascara, lama)
            del lama
            gc.collect()
    salvar_png(pasta / "02_mascara.png", para_disco(mascara))
    salvar_png(pasta / "02_riscos.png", para_disco(e2))
    area_px = int((mascara > 0).sum())
    rel["etapas"]["2_riscos"] = {"area_mascara_px": area_px, "area_mascara_pct": round(100.0 * area_px / (h0 * w0), 3),
                                 "deteccao_automatica": st, "janelas_lama": janelas, "provedor_lama": provedor}
    etapas["02_riscos"] = e2
    log(f"[2] riscos: mascara {100.0 * area_px / (h0 * w0):.2f}% da imagem, {janelas} janelas LaMa ({cron.tempos['2_riscos']}s)")

    # 3. rosto
    atual = e2
    if args.rosto > 0 and rostos_adj:
        with cron.medir("3_rosto"):
            e3, n = etapa_rosto(e2, rostos_adj, args.rosto, mono, disp)
            if usar_gpu:
                torch.cuda.empty_cache()
        salvar_png(pasta / "03_rosto.png", para_disco(e3))
        rel["etapas"]["3_rosto"] = {"rostos_restaurados": n, "opacidade": args.rosto}
        etapas["03_rosto"] = e3
        atual = e3
        log(f"[3] rosto: {n} rosto(s) com opacidade {args.rosto} ({cron.tempos['3_rosto']}s)")
    elif args.rosto > 0:
        avisos.append("nenhum rosto detectado: etapa 3 (GFPGAN) nao aplicada")
        rel["etapas"]["3_rosto"] = {"rostos_restaurados": 0, "motivo": "nenhum rosto detectado"}
        log("[3] rosto: nenhum rosto detectado, etapa pulada")
    else:
        rel["etapas"]["3_rosto"] = {"pulada": "--rosto 0"}
        log("[3] rosto: pulada (--rosto 0)")

    # 4. resolucao
    with cron.medir("4_resolucao"):
        e4 = ampliar(atual, args.escala, disp, usar_gpu)
        if usar_gpu:
            torch.cuda.empty_cache()
    nome4 = f"04_resolucao_{args.escala}x"
    e4_disco = para_disco(e4)
    salvar_png(pasta / f"{nome4}.png", e4_disco)
    etapas[nome4] = e4
    rel["etapas"]["4_resolucao"] = {"escala": args.escala, "saida": [int(e4_disco.shape[1]), int(e4_disco.shape[0])]}
    log(f"[4] resolucao {args.escala}x: {e4_disco.shape[1]}x{e4_disco.shape[0]} ({cron.tempos['4_resolucao']}s)")
    final, nome_final = e4, nome4

    # 5. cor
    if args.cor:
        with cron.medir("5_cor"):
            e5, aviso = colorizar(final, disp, mono, args.cor_intensidade)
            if usar_gpu:
                torch.cuda.empty_cache()
        avisos.append(aviso)
        if e5 is None:
            rel["etapas"]["5_cor"] = {"pulada": aviso}
            log(f"[5] cor: pulada ({aviso})")
        else:
            salvar_png(pasta / "05_cor.png", para_disco(e5))
            etapas["05_cor"] = e5
            final, nome_final = e5, "05_cor"
            rel["etapas"]["5_cor"] = {"ok": True, "modelo": "DDColor paper_tiny", "intensidade": args.cor_intensidade}
            log(f"[5] cor: ok ({cron.tempos['5_cor']}s)")

    salvar_png(pasta / "resultado.png", para_disco(final))
    if rotacao_interna:
        salvar_png(pasta / "resultado_em_pe.png", final)

    # 6. identidade: (a) original contra cada etapa, com limite folgado (o original tem riscos que a restauracao remove de
    #    proposito); (b) cada etapa contra a anterior, com limite rigoroso (isola o efeito de cada etapa, em especial o GFPGAN).
    with cron.medir("6_identidade"):
        det = Rostos()
        deteccoes = {"original": rostos_orig}
        for nome, img in etapas.items():
            deteccoes[nome] = det.medir_em(img, rostos_orig, orig.shape) if rostos_orig else []
        det.fechar()
        por_etapa = {nome: comparar_rostos(orig, rostos_orig, img, deteccoes[nome], args.limite_original) for nome, img in etapas.items()}
        sequencia = [("original", orig)] + list(etapas.items())
        transicoes = {}
        for (na, ia), (nb, ib) in zip(sequencia[:-1], sequencia[1:]):
            transicoes[f"{na} -> {nb}"] = comparar_rostos(ia, deteccoes[na], ib, deteccoes[nb], args.limite_etapa)
    notas_final = por_etapa[nome_final]
    reprovados = []
    if not rostos_orig:
        status = "SEM_ROSTO_DETECTADO"
        avisos.append("nenhum rosto detectado no original: identidade nao verificada (revisao humana)")
    else:
        reprovados = [f"original -> {nome_final} (rosto {r['rosto']})" for r in notas_final if r["status"] == "REPROVADO"]
        for k, v in transicoes.items():
            reprovados += [f"{k} (rosto {r['rosto']})" for r in v if r["status"] == "REPROVADO"]
        status = "REPROVADO" if reprovados else "APROVADO"
    rel["identidade"] = {"metodo": METODO_IDENTIDADE, "limite_original": args.limite_original, "limite_etapa": args.limite_etapa,
                         "status_geral": status, "reprovado_em": reprovados, "rostos": notas_final,
                         "por_etapa": {k: [{"rosto": r["rosto"], "nota": r["nota"]} for r in v] for k, v in por_etapa.items()},
                         "transicoes": {k: v for k, v in transicoes.items()}}
    pior = min([r["nota"] for v in transicoes.values() for r in v] or [0.0])
    log(f"[6] identidade: {status} | original->final: {[r['nota'] for r in notas_final]} (limite {args.limite_original}) | "
        f"pior transicao: {pior} (limite {args.limite_etapa})")

    # 7. lado a lado
    with cron.medir("7_lado_a_lado"):
        saidas_lado = []
        try:
            cmd = [sys.executable, str(LADO_A_LADO), str(origem), str(pasta / "resultado.png"), str(pasta / "lado_a_lado.png")]
            r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
            saidas_lado.append("lado_a_lado.png")
            if r.returncode not in (0, 1):
                avisos.append("lado-a-lado.py falhou: " + (r.stderr or r.stdout)[-300:])
            if rostos_orig:
                bb = max(rostos_orig, key=lambda d: (d["bbox"][2] - d["bbox"][0]) * (d["bbox"][3] - d["bbox"][1]))["bbox"]
                lw, lh = bb[2] - bb[0], bb[3] - bb[1]
                x0_u, y0_u = max(bb[0] - 0.4 * lw, 0) / w0, max(bb[1] - 0.4 * lh, 0) / h0
                x1_u, y1_u = min(bb[2] + 0.4 * lw, w0) / w0, min(bb[3] + 0.4 * lh, h0) / h0
                if rotacao_interna == -90:
                    x0, x1, y0, y1 = 1.0 - y1_u, 1.0 - y0_u, x0_u, x1_u
                elif rotacao_interna == 90:
                    x0, x1, y0, y1 = y0_u, y1_u, 1.0 - x1_u, 1.0 - x0_u
                else:
                    x0, x1, y0, y1 = x0_u, x1_u, y0_u, y1_u
                zoom = f"{x0:.4f},{y0:.4f},{x1 - x0:.4f},{y1 - y0:.4f}"
                cmd2 = cmd[:-1] + [str(pasta / "lado_a_lado_rosto.png"), "--zoom", zoom]
                subprocess.run(cmd2, capture_output=True, text=True, encoding="utf-8")
                saidas_lado.append("lado_a_lado_rosto.png")
        except Exception as exc:  # noqa: BLE001
            avisos.append(f"lado a lado nao gerado: {exc}")
    rel["etapas"]["7_lado_a_lado"] = {"arquivos": saidas_lado}

    rel["tempos_s"] = cron.tempos
    rel["tempo_total_s"] = round(time.perf_counter() - t_total, 2)
    rel["arquivos_saida"] = sorted(f.name for f in pasta.iterdir())
    rel["ambiente"] = ambiente()
    rel["modelos_sha256"] = sha256_modelos()
    (pasta / "relatorio.json").write_text(json.dumps(rel, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"Pronto em {rel['tempo_total_s']}s. Saida: {pasta}")
    return 0 if status != "REPROVADO" else 2


if __name__ == "__main__":
    sys.exit(main())
