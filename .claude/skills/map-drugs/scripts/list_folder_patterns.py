#!/usr/bin/env python3
"""
Summarize repeated presentation patterns in a product folder.

This is a read-only helper intended to reduce context load before concept search.
It auto-detects the data source (Spain, Latvia) from the folder path and uses
the appropriate grouping fields and ID column.

Usage:
    python3 .claude/skills/map-drugs/scripts/list_folder_patterns.py data/spain/products/<folder>/
    python3 .claude/skills/map-drugs/scripts/list_folder_patterns.py data/latvia/products/<substance>/<product>/
    python3 .claude/skills/map-drugs/scripts/list_folder_patterns.py <folder>/ --missing-only
    python3 .claude/skills/map-drugs/scripts/list_folder_patterns.py <folder>/ --package-aware
    python3 .claude/skills/map-drugs/scripts/list_folder_patterns.py <folder>/ --full
"""

import argparse
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from helpers import clean, fail, find_dated_file, load_tsv, normalize_latvia_package, pattern_key  # noqa: E402


# -- Source configurations -----------------------------------------------------

SPAIN_CONFIG = {
    "id_col": "cod_nacion",
    "data_file": "data.tsv",
    "default_fields": [
        "des_dcp",
        "vias_administracion",
        "forma_farmaceutica",
        "sw_generico",
        "des_dosific",
        "unidad_contenido",
    ],
    "full_fields": [
        "des_dcp",
        "vias_administracion",
        "forma_farmaceutica",
        "sw_generico",
        "des_dosific",
        "unidad_contenido",
        "envase",
        "contenido",
        "principios_activos",
        "laboratorio_titular",
    ],
    "display_name": lambda folder: folder.name,
    "mapped_filter": lambda row: True,
}

LATVIA_CONFIG = {
    "id_col": "product_id",
    "data_file": None,  # use find_dated_file
    "default_fields": [
        "original_name",
        "strength",
        "pharmaceutical_form",
        "product_strength",
    ],
    "package_fields": [
        "original_name",
        "strength",
        "pharmaceutical_form",
        "product_strength",
        "package_en",
    ],
    "full_fields": [
        "original_name",
        "strength",
        "pharmaceutical_form",
        "product_strength",
        "package_en",
        "package_size",
        "authorisation_no",
    ],
    "display_name": lambda folder: f"{folder.parent.name}/{folder.name}",
    "mapped_filter": lambda row: clean(row.get("concept_id", "")) or clean(row.get("mapping_type", "")),
}


def detect_source(folder):
    """Detect data source from folder path."""
    resolved = folder.resolve()
    parts = resolved.parts
    if "spain" in parts:
        return SPAIN_CONFIG
    if "latvia" in parts:
        return LATVIA_CONFIG
    fail(f"Cannot detect source from path: {folder}. Expected 'spain' or 'latvia' in path.")


def find_data_path(folder, config):
    """Return the data file path for the folder."""
    if config["data_file"]:
        path = folder / config["data_file"]
        if not path.exists():
            fail(f"{path} not found")
        return path
    path = find_dated_file(folder)
    if not path:
        fail(f"no data_*.tsv found in {folder}")
    return path


def parse_args():
    parser = argparse.ArgumentParser(
        description="Summarize repeated presentation patterns in a product folder.",
    )
    parser.add_argument("folder", help="Product folder path")
    parser.add_argument(
        "--missing-only",
        action="store_true",
        help="Only summarize rows not yet mapped in mapping.tsv",
    )
    parser.add_argument(
        "--package-aware",
        action="store_true",
        help="For Latvia folders, include package_en in the grouping key while still collapsing pack-size variants",
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Include extra fields (packaging, holder, etc.) in the grouping key",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    folder = Path(args.folder)
    config = detect_source(folder)

    data_path = find_data_path(folder, config)
    mapping_path = folder / "mapping.tsv"

    if args.full:
        fields = config["full_fields"]
    elif args.package_aware:
        fields = config.get("package_fields", config["default_fields"])
    else:
        fields = config["default_fields"]
    id_col = config["id_col"]
    data_rows = load_tsv(data_path)

    mapped_ids = set()
    if mapping_path.exists():
        mapped_ids = {
            clean(row.get(id_col, ""))
            for row in load_tsv(mapping_path)
            if config["mapped_filter"](row)
        }

    selected_rows = []
    for row in data_rows:
        row_id = clean(row.get(id_col, ""))
        if args.missing_only and row_id in mapped_ids:
            continue
        selected_rows.append(row)

    if not selected_rows:
        print("OK - no matching rows found")
        return

    def build_key(row):
        normalized = dict(row)
        if args.package_aware and "latvia" in folder.resolve().parts and "package_en" in fields:
            normalized["package_en"] = normalize_latvia_package(row.get("package_en", ""))
        return pattern_key(normalized, fields)

    grouped = Counter(build_key(row) for row in selected_rows)
    examples = defaultdict(list)
    for row in selected_rows:
        key = build_key(row)
        if len(examples[key]) < 3:
            examples[key].append(clean(row.get(id_col, "")))

    display_name = config["display_name"](folder)
    print(f"# {display_name}: {len(selected_rows)} rows, {len(grouped)} patterns")
    print()
    print(f"count\texample_{id_col}s\t" + "\t".join(fields))

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
