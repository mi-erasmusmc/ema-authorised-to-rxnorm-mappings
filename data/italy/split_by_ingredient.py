#!/usr/bin/env python3
"""
Split confezioni.tsv into per-ingredient product folders.

Output structure:
  products/{slug}/data.tsv

Folder name is the pa_associati value slugified:
  - lowercased
  - accents stripped
  - "/" (combo separator) → "_+_"
  - spaces → underscore
  - unsafe filesystem chars sanitised
"""

import csv
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

PRODUCTS_DIR = Path(__file__).parent / "products"
INPUT_TSV = Path(__file__).parent / "confezioni.tsv"

DATA_COLUMNS = [
    "codice_aic",           # unique pack identifier (primary key)
    "cod_farmaco",          # product-level ID (shared across pack sizes)
    "denominazione",        # brand name
    "descrizione",          # pack description: strength, form, size
    "pa_associati",         # active ingredient names (/-separated for combos)
    "principio_attivo",     # ingredient names from PA_confezioni (may differ)
    "quantita",             # strength quantity
    "unita_misura",         # strength unit
    "forma",                # pharmaceutical form
    "codice_atc",           # ATC code
    "ragione_sociale",      # MAH / company name
    "stato_amministrativo", # authorisation status
    "tipo_procedura",       # procedure type (Centralizzata = EMA, etc.)
    "fornitura",            # dispensing class
]


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = text.lower()
    text = text.replace("/", " + ")
    text = re.sub(r'[\\:*?"<>|]', "_", text)
    text = re.sub(r"[ ]+", "_", text)
    text = re.sub(r"_+", "_", text)
    text = text.strip("_")
    # macOS/Linux filename limit is 255 bytes; truncate conservatively
    if len(text.encode()) > 200:
        text = text[:200].rsplit("_", 1)[0]
    return text


def main():
    if not INPUT_TSV.exists():
        print(f"ERROR: {INPUT_TSV} not found. Run download_aifa.py first.", file=sys.stderr)
        sys.exit(1)

    print(f"Reading {INPUT_TSV} ...", file=sys.stderr)
    with open(INPUT_TSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        groups: dict[str, list[dict]] = defaultdict(list)
        for row in reader:
            groups[row["pa_associati"]].append(row)

    print(f"Found {len(groups)} ingredient groups across {sum(len(v) for v in groups.values())} rows", file=sys.stderr)

    PRODUCTS_DIR.mkdir(exist_ok=True)
    for pa, rows in sorted(groups.items(), key=lambda x: x[0]):
        slug = slugify(pa) if pa else "_unknown"
        folder = PRODUCTS_DIR / slug
        folder.mkdir(exist_ok=True)

        out_path = folder / "data.tsv"
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=DATA_COLUMNS, delimiter="\t", extrasaction="ignore")
            writer.writeheader()
            for row in rows:
                writer.writerow(row)

    print(f"Done. Written to {PRODUCTS_DIR}/", file=sys.stderr)
    print(f"  {len(groups)} folders", file=sys.stderr)


if __name__ == "__main__":
    main()
