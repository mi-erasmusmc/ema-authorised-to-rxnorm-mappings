#!/usr/bin/env python3
"""
Split prescripcion.tsv into per-ingredient product folders.

Output structure:
  products/{slug}/data.tsv

Folder name is the des_dcsa value slugified:
  - lowercased
  - accents stripped
  - spaces → underscore
  - special chars sanitised for filesystem safety
"""

import csv
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

PRODUCTS_DIR = Path(__file__).parent / "products"
INPUT_TSV = Path(__file__).parent / "prescripcion.tsv"

# Columns written to each data.tsv — urls and redundant fields dropped.
# PDFs are fetched on demand via fetch_pdf.py using nro_definitivo.
DATA_COLUMNS = [
    "cod_nacion",           # national code (primary key)
    "nro_definitivo",       # product number — used to derive PDF urls
    "des_nomco",            # commercial name
    "des_dcp",              # clinical product: name + dose + form (normalised)
    "des_dosific",          # dosage string
    "envase",               # container type
    "contenido",            # quantity
    "unidad_contenido",     # unit
    "principios_activos",   # pipe-separated "NAME DOSE UNIT" per ingredient
    "vias_administracion",  # pipe-separated route names
    "forma_farmaceutica",   # pharmaceutical form
    "nro_pactiv",           # number of active ingredients
    "atc",                  # ATC code + description, e.g. "J01CR02 - Amoxicilina..."
    "laboratorio_titular",  # MAH
    "fecha_autorizacion",   # authorisation date
    "sw_comercializado",    # currently marketed (0/1)
    "fec_comer",            # date first marketed
    "situacion_registro",   # Autorizado / Anulado / Suspenso
    "fecha_situacion_registro",
    "sw_receta",            # prescription required
    "sw_base_a_plantas",    # herbal (may lack RxNorm concept)
    "biosimilar",           # biosimilar (maps differently to originator)
    "radiofarmaco",         # radiopharmaceutical (specialist RxNorm handling)
]


def slugify(text: str) -> str:
    # Normalise unicode and strip combining characters (accents)
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = text.lower()
    # Replace + with _plus_ for readability, keep it filesystem-safe
    text = text.replace("+", "+")  # keep + as-is, it's valid in dir names
    # Replace slashes and other unsafe chars
    text = re.sub(r'[/\\:*?"<>|]', "_", text)
    # Collapse runs of spaces/underscores
    text = re.sub(r"[ ]+", "_", text)
    text = re.sub(r"_+", "_", text)
    text = text.strip("_")
    return text


def main():
    if not INPUT_TSV.exists():
        print(f"ERROR: {INPUT_TSV} not found. Run download_aemps.py first.", file=sys.stderr)
        sys.exit(1)

    print(f"Reading {INPUT_TSV} ...", file=sys.stderr)
    with open(INPUT_TSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        fieldnames = reader.fieldnames
        groups = defaultdict(list)
        for row in reader:
            # Merge cod_atc + des_atc into a single column.
            # des_atc already contains the code as prefix ("J01CR02 - Description")
            # so we just use des_atc directly and drop the redundant cod_atc column.
            row["atc"] = row.get("des_atc", "") or row.get("cod_atc", "")
            groups[row["des_dcsa"]].append(row)

    print(f"Found {len(groups)} ingredient groups across {sum(len(v) for v in groups.values())} rows", file=sys.stderr)

    PRODUCTS_DIR.mkdir(exist_ok=True)
    for des_dcsa, rows in sorted(groups.items(), key=lambda x: x[0]):
        slug = slugify(des_dcsa) if des_dcsa else "_unknown"
        folder = PRODUCTS_DIR / slug
        folder.mkdir(exist_ok=True)

        out_path = folder / "data.tsv"
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=DATA_COLUMNS, delimiter="\t", extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)

    print(f"Done. Written to {PRODUCTS_DIR}/", file=sys.stderr)
    print(f"  {len(groups)} folders, e.g.:", file=sys.stderr)
    for slug in list(sorted(slugify(k) for k in groups))[:8]:
        print(f"    products/{slug}/", file=sys.stderr)


if __name__ == "__main__":
    main()
