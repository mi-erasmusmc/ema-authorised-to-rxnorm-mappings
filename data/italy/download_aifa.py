#!/usr/bin/env python3
"""
Download AIFA Italian medicines register and convert to TSV.

Sources:
  https://drive.aifa.gov.it/farmaci/confezioni_fornitura.csv  — main pack register
  https://drive.aifa.gov.it/farmaci/PA_confezioni.csv         — active ingredient strengths

Output: confezioni.tsv — one row per pack, semicolon CSV converted to tab-separated,
with principio_attivo/quantita/unita_misura joined from PA_confezioni.
"""

import csv
import ssl
import sys
import urllib.request
from pathlib import Path

URL_CONFEZIONI = "https://drive.aifa.gov.it/farmaci/confezioni_fornitura.csv"
URL_PA = "https://drive.aifa.gov.it/farmaci/PA_confezioni.csv"
OUT_TSV = Path(__file__).parent / "confezioni.tsv"

COLUMNS = [
    "codice_aic",
    "cod_farmaco",
    "cod_confezione",
    "denominazione",
    "descrizione",
    "codice_ditta",
    "ragione_sociale",
    "stato_amministrativo",
    "tipo_procedura",
    "forma",
    "codice_atc",
    "pa_associati",
    "principio_attivo",
    "quantita",
    "unita_misura",
    "fornitura",
    "link_fi",
    "link_rcp",
]


def fetch(url: str) -> bytes:
    print(f"Downloading {url} ...", file=sys.stderr)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    data = urllib.request.urlopen(url, timeout=60, context=ctx).read()
    print(f"  {len(data):,} bytes", file=sys.stderr)
    return data


def parse_csv(data: bytes) -> list[dict]:
    text = data.decode("utf-8", errors="replace")
    reader = csv.DictReader(text.splitlines(), delimiter=";")
    return list(reader)


def main():
    raw_confezioni = fetch(URL_CONFEZIONI)
    raw_pa = fetch(URL_PA)

    print("Parsing...", file=sys.stderr)
    confezioni = parse_csv(raw_confezioni)
    pa_rows = parse_csv(raw_pa)

    # Build AIC → aggregated PA entries (multiple rows per AIC for combo/homeopathic products)
    pa_by_aic: dict[str, list[dict]] = {}
    for row in pa_rows:
        aic = row.get("CODICE_AIC", "").strip().strip('"')
        pa_by_aic.setdefault(aic, []).append(row)

    print(f"  {len(confezioni):,} packs, {len(pa_by_aic):,} AIC PA entries", file=sys.stderr)

    def agg_pa(entries: list[dict]) -> tuple[str, str, str]:
        """Aggregate multiple PA rows into pipe-joined principio_attivo, quantita, unita_misura."""
        pas, qtys, units = [], [], []
        for e in entries:
            pa = e.get("PRINCIPIO_ATTIVO", "").strip()
            qty = e.get("QUANTITA", "").strip()
            unit = e.get("UNITA_MISURA", "").strip()
            pas.append(pa if pa != "N.D." else "")
            qtys.append(qty if qty not in ("0.0", "0") else "")
            units.append(unit if unit != "N.D." else "")
        return "|".join(pas), "|".join(qtys), "|".join(units)

    with open(OUT_TSV, "w", newline="", encoding="utf-8") as fout:
        writer = csv.DictWriter(fout, fieldnames=COLUMNS, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        skipped = 0
        for row in confezioni:
            if row.get("TIPO_PROCEDURA", "").strip().strip('"') == "Omeopatico":
                skipped += 1
                continue
            aic = row.get("CODICE_AIC", "").strip().strip('"')
            pa_entries = pa_by_aic.get(aic, [])
            pa_val, qty, unit = agg_pa(pa_entries) if pa_entries else ("", "", "")
            writer.writerow({
                "codice_aic":        aic,
                "cod_farmaco":       row.get("COD_FARMACO", "").strip().strip('"'),
                "cod_confezione":    row.get("COD_CONFEZIONE", "").strip().strip('"'),
                "denominazione":     row.get("DENOMINAZIONE", "").strip().strip('"'),
                "descrizione":       row.get("DESCRIZIONE", "").strip().strip('"'),
                "codice_ditta":      str(row.get("CODICE_DITTA", "")).strip().strip('"'),
                "ragione_sociale":   row.get("RAGIONE_SOCIALE", "").strip().strip('"'),
                "stato_amministrativo": row.get("STATO_AMMINISTRATIVO", "").strip().strip('"'),
                "tipo_procedura":    row.get("TIPO_PROCEDURA", "").strip().strip('"'),
                "forma":             row.get("FORMA", "").strip().strip('"'),
                "codice_atc":        row.get("CODICE_ATC", "").strip().strip('"'),
                "pa_associati":      row.get("PA_ASSOCIATI", "").strip().strip('"'),
                "principio_attivo":  pa_val,
                "quantita":          qty,
                "unita_misura":      unit,
                "fornitura":         row.get("FORNITURA", "").strip().strip('"'),
                "link_fi":           row.get("LINK_FI", "").strip().strip('"'),
                "link_rcp":          row.get("LINK_RCP", "").strip().strip('"'),
            })

    print(f"  Skipped {skipped:,} homeopathic rows", file=sys.stderr)
    print(f"Done. Written to {OUT_TSV}", file=sys.stderr)


if __name__ == "__main__":
    main()
