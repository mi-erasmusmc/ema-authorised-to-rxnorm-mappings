#!/usr/bin/env python3
"""
Report EMA-linked duplicate nro_definitivo values in Spain source data.

Usage:
    python3 .claude/skills/map-spain-drugs/scripts/find_duplicate_nros.py
    python3 .claude/skills/map-spain-drugs/scripts/find_duplicate_nros.py --folder adalimumab
"""

import argparse
import csv
import sys
from collections import defaultdict
from pathlib import Path


def load_rows(path):
    with open(path, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def build_ema_nros(path):
    ema_nros = set()
    for row in load_rows(path):
        ma_number = row.get("ma_number", "").strip()
        if ma_number.startswith("EU"):
            ema_nros.add(ma_number[2:].replace("/", ""))
    return ema_nros


def iter_spain_rows(products_root, folder_name=None):
    folders = [products_root / folder_name] if folder_name else sorted(products_root.iterdir())
    for folder in folders:
        if not folder.is_dir():
            continue
        data_path = folder / "data.tsv"
        if not data_path.exists():
            continue
        for row in load_rows(data_path):
            row["_folder"] = folder.name
            yield row


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", help="Limit the report to one ingredient folder")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[4]
    ema_path = repo_root / "ema-to-rxnorm.tsv"
    products_root = repo_root / "data" / "spain" / "products"

    if not ema_path.exists():
        print(f"ERROR: {ema_path} not found", file=sys.stderr)
        return 1
    if not products_root.exists():
        print(f"ERROR: {products_root} not found", file=sys.stderr)
        return 1
    if args.folder and not (products_root / args.folder).exists():
        print(f"ERROR: {products_root / args.folder} not found", file=sys.stderr)
        return 1

    ema_nros = build_ema_nros(ema_path)
    grouped = defaultdict(list)
    for row in iter_spain_rows(products_root, args.folder):
        nro = row.get("nro_definitivo", "").strip()
        if nro and nro in ema_nros:
            grouped[nro].append(row)

    duplicates = {nro: rows for nro, rows in grouped.items() if len(rows) > 1}
    if not duplicates:
        print("OK - no duplicate EMA-linked nro_definitivo values found")
        return 0

    print("nro_definitivo\tfolder\tcod_nacion\tdes_dosific\tdes_dcp")
    for nro in sorted(duplicates):
        for row in sorted(duplicates[nro], key=lambda item: (item["_folder"], item.get("cod_nacion", ""))):
            print(
                "\t".join(
                    [
                        nro,
                        row["_folder"],
                        row.get("cod_nacion", "").strip(),
                        row.get("des_dosific", "").strip(),
                        row.get("des_dcp", "").strip(),
                    ]
                )
            )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
