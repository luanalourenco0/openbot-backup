"""Junta os relatorio.json da bateria de testes em tabelas Markdown (teste\\RESULTADOS_tabelas.md).

Uso (em ferramentas\\restauracao):  .venv\\Scripts\\python.exe teste\\resumir.py
"""
import json
import statistics
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
FOTOS = [
    "foto1_rapaz_quepe",
    "foto2_homem_riscos",
    "foto3_senhora_manchas",
    "AdaStoddard_1914",
    "Amos_Strunk_1911",
    "Dandridge_McRae",
    "Soldier_with_girl",
    "5pulklegionow1929",
]
ROSTOS = ["0", "0.5", "1.0"]


def carregar(foto, r):
    p = BASE / foto / f"rosto_{r}" / "relatorio.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def fmt_lista(vals):
    vals = [v for v in vals if isinstance(v, (int, float))]
    if not vals:
        return "-"
    if len(vals) <= 4:
        return " / ".join(str(v) for v in vals)
    return f"{len(vals)} rostos (min {min(vals)}, med {round(statistics.median(vals), 3)}, max {max(vals)})"


def main():
    L = ["# Tabelas geradas dos relatorio.json (teste\\resumir.py)", ""]
    L += ["## Tempo e mascara", "",
          "| Foto | --rosto | Entrada | 1 ajuste | 2 riscos (LaMa) | 3 rosto | 4 resolucao 2x | Rostos+identidade | Total | Mascara (% da imagem) |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for f in FOTOS:
        for r in ROSTOS:
            d = carregar(f, r)
            if not d:
                L.append(f"| {f} | {r} | (nao rodou) | | | | | | | |")
                continue
            t = d["tempos_s"]
            e = d["entrada"]
            L.append("| {f} | {r} | {w}x{h} | {a} s | {b} s | {c} | {dd} s | {ee} s | {tot} s | {m}% |".format(
                f=f, r=r, w=e["largura"], h=e["altura"], a=t.get("1_ajuste"), b=t.get("2_riscos"),
                c=(f"{t['3_rosto']} s" if "3_rosto" in t else "pulada"), dd=t.get("4_resolucao"),
                ee=round(t.get("deteccao_rostos_original", 0) + t.get("deteccao_rostos_ajustada", 0) + t.get("6_identidade", 0), 2),
                tot=d["tempo_total_s"], m=d["etapas"]["2_riscos"]["area_mascara_pct"]))
    L += ["", "## Identidade (comparado com o original e pior transicao entre etapas)", "",
          "| Foto | --rosto | Etapa 1 | Etapa 2 | Etapa 3 | Final (04) | Erro geom. (final) | SSIM (final) | Pior transicao | Status |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for f in FOTOS:
        for r in ROSTOS:
            d = carregar(f, r)
            if not d:
                continue
            idn = d["identidade"]
            pe = idn["por_etapa"]

            def nota(chave):
                if chave not in pe or not pe[chave]:
                    return "-"
                return fmt_lista([x["nota"] for x in pe[chave]])
            rost = idn["rostos"]
            eg = fmt_lista([x.get("erro_geometrico_norm") for x in rost if "erro_geometrico_norm" in x])
            ss = fmt_lista([x.get("ssim_estrutura") for x in rost if "ssim_estrutura" in x])
            fin = fmt_lista([x["nota"] for x in rost])
            lim_orig = idn.get("limite_original", idn.get("limite", 0.4))
            lim_etapa = idn.get("limite_etapa", 0.6)
            trans = idn.get("transicoes", {})
            pior_t = min([r["nota"] for v in trans.values() for r in v] or ["-"])
            L.append(f"| {f} | {r} | {nota('01_ajuste')} | {nota('02_riscos')} | {nota('03_rosto')} | {fin} | {eg} | {ss} | {pior_t} | {idn['status_geral']} (orig>={lim_orig}, etapa>={lim_etapa}) |")
    L += ["", "## Avisos registrados", ""]
    for f in FOTOS:
        for r in ROSTOS:
            d = carregar(f, r)
            if d and d.get("avisos"):
                for a in d["avisos"]:
                    L.append(f"- {f} --rosto {r}: {a}")
    (BASE / "RESULTADOS_tabelas.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    sys.exit(main())
