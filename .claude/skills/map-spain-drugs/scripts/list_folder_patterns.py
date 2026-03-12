#!/usr/bin/env python3
"""
Summarize repeated presentation patterns in a Spain product folder.

This is a read-only helper intended to reduce context load before concept search.
It groups rows conservatively so route, form, generic status, and pack context stay visible.

Usage:
    python3 .claude/skills/map-spain-drugs/scripts/list_folder_patterns.py data/spain/products/<folder>/
    python3 .claude/skills/map-spain-drugs/scripts/list_folder_patterns.py data/spain/products/<folder>/ --missing-only
    python3 .claude/skills/map-spain-drugs/scripts/list_folder_patterns.py data/spain/products/<folder>/ --full
"""

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path


DEFAULT_FIELDS = [
    "des_dcp",
    "vias_administracion",
    "forma_farmaceutica",
    "sw_generico",
    "des_dosific",
    "unidad_contenido",
]

FULL_FIELDS = DEFAULT_FIELDS + [
    "envase",
    "contenido",
    "principios_activos",
    "laboratorio_titular",
]


def load_tsv(path):
    with open(path, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def clean(value):
    if value is None:
        return ""
    return str(value).strip()


def pattern_key(row, fields):
    return tuple(clean(row.get(field, "")) for field in fields)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help="Spain product folder")
    parser.add_argument(
        "--missing-only",
        action="store_true",
        help="Only summarize cod_nacion values not yet present in mapping.tsv",
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Include extra pack and holder fields in the grouping key",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    folder = Path(args.folder)
    data_path = folder / "data.tsv"
    mapping_path = folder / "mapping.tsv"

    if not data_path.exists():
        raise SystemExit(f"ERROR: {data_path} not found")

    fields = FULL_FIELDS if args.full else DEFAULT_FIELDS
    data_rows = load_tsv(data_path)

    mapped_cods = set()
    if mapping_path.exists():
        mapped_cods = {
            clean(row.get("cod_nacion", ""))
            for row in load_tsv(mapping_path)
        }

    selected_rows = []
    for row in data_rows:
        cod = clean(row.get("cod_nacion", ""))
        if args.missing_only and cod in mapped_cods:
            continue
        selected_rows.append(row)

    if not selected_rows:
        print("OK - no matching rows found")
        return

    grouped = Counter(pattern_key(row, fields) for row in selected_rows)
    examples = defaultdict(list)
    for row in selected_rows:
        key = pattern_key(row, fields)
        if len(examples[key]) < 3:
            examples[key].append(clean(row.get("cod_nacion", "")))

    print(f"# {folder.name}: {len(selected_rows)} rows, {len(grouped)} patterns")
    print()
    print("count\texample_cods\t" + "\t".join(fields))

    for key, count in grouped.most_common():
        print(
            "\t".join(
                [
                    str(count),
                    ",".join(examples[key]),
                    *key,
                ]
            )
        )


if __name__ == "__main__":
    main()
