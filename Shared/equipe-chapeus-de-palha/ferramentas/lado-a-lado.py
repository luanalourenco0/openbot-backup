"""Comparativo de restauração: original | restaurada | mapa de diferenças.

Uso:
    python lado-a-lado.py ORIGINAL RESTAURADA SAIDA.png [--zoom X,Y,L,A]

--zoom recorta a mesma região das duas imagens (frações de 0 a 1: x, y, largura, altura),
para ampliar um rosto. Ex.: --zoom 0.35,0.10,0.30,0.35

O mapa de diferenças mostra onde a estrutura mudou (claro = mudou mais). Riscos removidos
aparecem como traços finos; mudança em olhos, boca ou contorno do rosto é sinal de alerta.
O script também avisa se a proporção da imagem mudou (mudança de enquadramento).
Só usa Pillow. Não envia nada para a internet.
"""
import argparse
import sys

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageOps

ALTURA = 900
MARGEM = 16
FAIXA_TITULO = 40


def abrir(caminho):
    img = Image.open(caminho)
    img = ImageOps.exif_transpose(img)
    return img.convert("RGB")


def recortar(img, zoom):
    if not zoom:
        return img
    x, y, l, a = zoom
    w, h = img.size
    return img.crop((int(x * w), int(y * h), int((x + l) * w), int((y + a) * h)))


def na_altura(img, altura):
    w, h = img.size
    return img.resize((max(1, round(w * altura / h)), altura), Image.LANCZOS)


def _pixels(img):
    # getdata() foi descontinuado no Pillow 13; get_flattened_data() substitui.
    leitor = getattr(img, "get_flattened_data", None) or img.getdata
    return list(leitor())


def casar_tons(ref, img):
    """Ajusta brilho e contraste de img aos de ref (ajuste linear por mínimos quadrados).

    A restauração corrige desbotamento e contraste; isso não deve aparecer como "mudança".
    Áreas pequenas que mudaram (risco, rosto alterado) pesam pouco no ajuste e continuam visíveis.
    """
    amostra = (200, max(1, round(200 * ref.height / ref.width)))
    xs = _pixels(img.resize(amostra))
    ys = _pixels(ref.resize(amostra))
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    var = sum((x - mx) ** 2 for x in xs) / n
    if var < 1e-6:
        return img
    k = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / n / var
    c = my - k * mx
    return img.point([max(0, min(255, round(k * v + c))) for v in range(256)])


def mapa_diferenca(a, b):
    # Tons casados (ignora correção de cor/contraste), desfoque leve para ignorar grão
    # e escala fixa para não inflar ruído.
    ga = a.convert("L")
    gb = casar_tons(ga, b.convert("L"))
    ga = ga.filter(ImageFilter.GaussianBlur(2))
    gb = gb.filter(ImageFilter.GaussianBlur(2))
    dif = ImageChops.difference(ga, gb).point(lambda v: min(255, v * 3))
    return ImageOps.colorize(dif, black="#000000", white="#ff3b30")


def ler_zoom(texto):
    try:
        partes = [float(p) for p in texto.split(",")]
    except ValueError:
        raise argparse.ArgumentTypeError("--zoom precisa de 4 números: X,Y,L,A")
    if len(partes) != 4 or not all(0 <= p <= 1 for p in partes):
        raise argparse.ArgumentTypeError("--zoom precisa de 4 frações entre 0 e 1: X,Y,L,A")
    if partes[2] == 0 or partes[3] == 0 or partes[0] + partes[2] > 1 or partes[1] + partes[3] > 1:
        raise argparse.ArgumentTypeError("--zoom vazio ou fora da imagem")
    return partes


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("original")
    p.add_argument("restaurada")
    p.add_argument("saida")
    p.add_argument("--zoom", type=ler_zoom, default=None)
    args = p.parse_args(argv)

    orig = abrir(args.original)
    rest = abrir(args.restaurada)

    pr_o = orig.width / orig.height
    pr_r = rest.width / rest.height
    alerta = abs(pr_o - pr_r) / pr_o > 0.02
    if alerta:
        print(f"ALERTA: a proporção mudou ({pr_o:.3f} -> {pr_r:.3f}). Possível mudança de enquadramento.")

    a = na_altura(recortar(orig, args.zoom), ALTURA)
    b = recortar(rest, args.zoom).resize(a.size, Image.LANCZOS)
    d = mapa_diferenca(a, b)

    paineis = [("Original", a), ("Restaurada", b), ("Diferencas (claro = mudou)", d)]
    largura = sum(img.width for _, img in paineis) + MARGEM * (len(paineis) + 1)
    altura = ALTURA + FAIXA_TITULO + MARGEM * 2
    tela = Image.new("RGB", (largura, altura), "white")
    desenho = ImageDraw.Draw(tela)

    x = MARGEM
    for titulo, img in paineis:
        desenho.text((x, MARGEM), titulo, fill="black")
        tela.paste(img, (x, MARGEM + FAIXA_TITULO))
        x += img.width + MARGEM
    if alerta:
        desenho.text((MARGEM, MARGEM + FAIXA_TITULO // 2), "ALERTA: proporcao mudou", fill="red")

    tela.save(args.saida)
    print(f"Salvo: {args.saida}")
    return 1 if alerta else 0


if __name__ == "__main__":
    sys.exit(main())
