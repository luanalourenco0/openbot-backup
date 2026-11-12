"""Calibra o limite de identidade do restaurar.py com tres tipos de controle:

  preserva  - a mesma pessoa com degradacoes realistas (desfoque, JPEG, ruido, contraste, perda de resolucao). Deve APROVAR.
  deslocado - a mesma foto com olhos e boca deslocados por fracoes da distancia entre os olhos (imita um rosto "redesenhado").
  outra     - rostos de pessoas diferentes (fotos de teste cruzadas). Deve REPROVAR.

Uso (em ferramentas\\restauracao):  .venv\\Scripts\\python.exe teste\\calibracao.py
Grava teste\\calibracao.json. Nao envia nada para a internet.
"""
import itertools
import json
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AQUI))
import cv2  # noqa: E402
import numpy as np  # noqa: E402
import restaurar as R  # noqa: E402

FOTOS = ["foto1_rapaz_quepe", "foto2_homem_riscos", "foto3_senhora_manchas"]


def maior(rostos):
    return max(rostos, key=lambda d: (d["bbox"][2] - d["bbox"][0]) * (d["bbox"][3] - d["bbox"][1]))


def jpeg(img, q):
    ok, b = cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, q])
    return cv2.imdecode(b, 1)


def ruido(img, s):
    rng = np.random.default_rng(1)
    return np.clip(img.astype(np.float32) + rng.normal(0, s, img.shape), 0, 255).astype(np.uint8)


def perda_res(img, f):
    h, w = img.shape[:2]
    p = cv2.resize(img, (max(int(w * f), 8), max(int(h * f), 8)), interpolation=cv2.INTER_AREA)
    return cv2.resize(p, (w, h), interpolation=cv2.INTER_CUBIC)


def degradacoes(img):
    return {
        "desfoque_sigma2": cv2.GaussianBlur(img, (0, 0), 2.0),
        "jpeg_q30": jpeg(img, 30),
        "ruido_sigma8": ruido(img, 8),
        "contraste_0.8_brilho+20": np.clip(img.astype(np.float32) * 0.8 + 20, 0, 255).astype(np.uint8),
        "resolucao_x0.5": perda_res(img, 0.5),
        "resolucao_x0.35": perda_res(img, 0.35),
    }


def deslocar(img, pts, frac, dist_olhos):
    """Gaussiana de deslocamento: boca desce e olhos sobem 'frac' x distancia entre os olhos (imita redesenho do rosto)."""
    h, w = img.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    dx = np.zeros((h, w), np.float32)
    dy = np.zeros((h, w), np.float32)
    sig = 0.35 * dist_olhos
    fontes = [(pts[R.LABIOS].mean(axis=0), +frac * dist_olhos),
              (pts[R.OLHO_E].mean(axis=0), -frac * dist_olhos),
              (pts[R.OLHO_D].mean(axis=0), -frac * dist_olhos)]
    for (cx, cy), d in fontes:
        g = np.exp(-(((xx - cx) ** 2 + (yy - cy) ** 2) / (2 * sig ** 2)))
        dy += d * g
    return cv2.remap(img, xx, yy - dy, interpolation=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)


def pontuar(orig, ro, img2, rr):
    erro = R.erro_geometrico(ro["pts"], rr["pts"])
    ng = R.nota_geometria(erro)
    ne = R.estrutura_rosto(orig, ro["pts"], img2, rr["pts"])
    return {"erro_geometrico_norm": round(erro, 4), "nota_geometria": round(ng, 3), "ssim_estrutura": round(ne, 3),
            "nota": round(min(ng, ne), 3)}


def main():
    det = R.Rostos()
    fotos = {}
    for n in FOTOS:
        img = R.carregar_imagem(AQUI / "teste" / f"{n}.jpg")
        rs = det.detectar(img)
        if rs:
            fotos[n] = (img, maior(rs))
    saida = {"preserva": [], "deslocado": [], "outra": []}

    for n, (img, ro) in fotos.items():
        h, w = img.shape[:2]
        for nome, deg in degradacoes(img).items():
            rs = det.detectar(deg)
            casado = None
            for rr in rs:
                if R.iou(ro["bbox"] / np.array([w, h, w, h]), rr["bbox"] / np.array([w, h, w, h])) >= 0.3:
                    casado = rr
            if casado is None:
                saida["preserva"].append({"foto": n, "caso": nome, "nota": 0.0, "obs": "rosto nao detectado"})
            else:
                saida["preserva"].append({"foto": n, "caso": nome, **pontuar(img, ro, deg, casado)})
        dist = R.distancia_olhos(ro["pts"])
        for frac in (0.02, 0.04, 0.06, 0.10):
            des = deslocar(img, ro["pts"], frac, dist)
            rs = det.detectar(des)
            casado = None
            for rr in rs:
                if R.iou(ro["bbox"] / np.array([w, h, w, h]), rr["bbox"] / np.array([w, h, w, h])) >= 0.3:
                    casado = rr
            if casado is None:
                saida["deslocado"].append({"foto": n, "caso": f"olhos e boca {int(frac * 100)}% da dist. entre olhos", "nota": 0.0,
                                           "obs": "rosto nao detectado"})
            else:
                saida["deslocado"].append({"foto": n, "caso": f"olhos e boca {int(frac * 100)}% da dist. entre olhos",
                                           **pontuar(img, ro, des, casado)})

    for (na, (ia, ra)), (nb, (ib, rb)) in itertools.permutations(fotos.items(), 2):
        saida["outra"].append({"foto": f"{na} x {nb}", "caso": "rostos de pessoas diferentes", **pontuar(ia, ra, ib, rb)})
    det.fechar()

    def notas(chave):
        return [c["nota"] for c in saida[chave]]

    resumo = {}
    for k in saida:
        v = notas(k)
        resumo[k] = {"n": len(v), "min": round(min(v), 3), "mediana": round(float(np.median(v)), 3), "max": round(max(v), 3)}
    saida["resumo"] = resumo
    pos_min = resumo["preserva"]["min"]
    neg_max = max(resumo["outra"]["max"], 0.0)
    saida["proposta_limite"] = {"minimo_dos_casos_que_preservam": pos_min, "maximo_dos_casos_de_outra_pessoa": neg_max,
                               "ponto_medio": round((pos_min + neg_max) / 2, 3)}
    (AQUI / "teste" / "calibracao.json").write_text(json.dumps(saida, ensure_ascii=False, indent=2), encoding="utf-8")
    for k in ("preserva", "deslocado", "outra"):
        print(f"--- {k}: {resumo[k]}")
        for c in saida[k]:
            print("  ", c.get("foto"), "|", c.get("caso"), "| erro", c.get("erro_geometrico_norm"), "| geom", c.get("nota_geometria"),
                  "| ssim", c.get("ssim_estrutura"), "| nota", c["nota"], c.get("obs", ""))
    print("proposta:", saida["proposta_limite"])


if __name__ == "__main__":
    main()
