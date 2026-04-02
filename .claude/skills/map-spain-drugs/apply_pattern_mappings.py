#!/usr/bin/env python3
"""
Apply Spain mapping decisions by presentation pattern.

Reads mapping decisions from stdin as TSV keyed by pattern fields, then expands
those decisions to all matching cod_nacion rows. This is the Spain equivalent of
Latvia's apply_pattern_mappings.py.

Usage:
    python3 .claude/skills/map-spain-drugs/apply_pattern_mappings.py \
        data/spain/products/<folder>/mapping.tsv <<'EOF'
    des_dcp	vias_administracion	forma_farmaceutica	sw_generico	des_dosific	unidad_contenido	concept_id	concept_name	concept_code	mapping_type	comment	suggestion
    ATORVASTATINA 10 MG COMPRIMIDOS	ORAL	COMPRIMIDO	1	10 mg	comprimidos	617312	atorvastatin 10 MG Oral Tablet	370584	EXACT
    EOF

Flags:
    --only-missing    Only fill rows with no concept_id and no mapping_type
    --backfill-dates  Fill today's date on existing rows with empty last_updated_date
"""

import csv
import sys
from datetime import date
from io import StringIO
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "map-drugs"))
from helpers import clean, fail, load_tsv, pattern_key, write_tsv  # noqa: E402

PATTERN_COLUMNS = [
    "des_dcp",
    "vias_administracion",
    "forma_farmaceutica",
    "sw_generico",
    "des_dosific",
    "unidad_contenido",
]

MAPPING_COLUMNS = [
    "cod_nacion",
    "nro_definitivo",
    "concept_id",
    "concept_name",
    "concept_code",
    "mapping_type",
    "comment",
    "suggestion",
    "last_updated_date",
]


def validate_input_rows(rows):
    for index, row in enumerate(rows, start=2):
        missing = [col for col in PATTERN_COLUMNS if col not in row]
        if missing:
            fail(f"stdin row {index} is missing required pattern columns: {', '.join(missing)}")
        mapping_type = clean(row.get("mapping_type", ""))
        if not mapping_type:
            fail(f"stdin row {index} is missing mapping_type")
        if mapping_type in {"BROAD", "NO_MAPPING"} and not clean(row.get("suggestion", "")):
            fail(f"stdin row {index} requires suggestion for mapping_type={mapping_type}")


def main():
    args = sys.argv[1:]
    only_missing = "--only-missing" in args
    backfill = "--backfill-dates" in args
    positional = [arg for arg in args if not arg.startswith("--")]

    if not positional:
        fail(f"Usage: {sys.argv[0]} <mapping.tsv> [--only-missing] [--backfill-dates]")

    mapping_path = Path(positional[0])
    folder = mapping_path.parent
    data_path = folder / "data.tsv"
    today = date.today().isoformat()

    if not data_path.exists():
        fail(f"{data_path} not found")

    existing_rows = load_tsv(mapping_path) if mapping_path.exists() else []

    if backfill:
        changed = 0
        for row in existing_rows:
            if not clean(row.get("last_updated_date", "")):
                row["last_updated_date"] = today
                changed += 1
        write_tsv(mapping_path, existing_rows, MAPPING_COLUMNS)
        print(f"Backfilled dates on {changed} rows -> {mapping_path}")
        return

    stdin_data = sys.stdin.read().strip()
    if not stdin_data:
        fail("no input on stdin")

    updates = list(csv.DictReader(StringIO(stdin_data), delimiter="\t"))
    validate_input_rows(updates)

    updates_by_pattern = {}
    for row in updates:
        key = pattern_key(row, PATTERN_COLUMNS)
        if key in updates_by_pattern:
            fail(f"stdin contains duplicate pattern row for {key}")
        if not clean(row.get("last_updated_date", "")):
            row["last_updated_date"] = today
        updates_by_pattern[key] = row

    data_rows = load_tsv(data_path)
    existing_by_id = {clean(row.get("cod_nacion", "")): row for row in existing_rows}

    matched_ids = set()
    data_patterns = {pattern_key(row, PATTERN_COLUMNS) for row in data_rows}

    for data_row in data_rows:
        key = pattern_key(data_row, PATTERN_COLUMNS)
        if key not in updates_by_pattern:
            continue
        cod = clean(data_row.get("cod_nacion", ""))
        current = existing_by_id.get(cod, {"cod_nacion": cod})
        if only_missing and (clean(current.get("concept_id", "")) or clean(current.get("mapping_type", ""))):
            continue

        update = updates_by_pattern[key]
        for column in MAPPING_COLUMNS:
            if column == "cod_nacion":
                current[column] = cod
            elif column == "nro_definitivo":
                current[column] = clean(current.get("nro_definitivo", "")) or clean(data_row.get("nro_definitivo", ""))
            else:
                current[column] = clean(update.get(column, ""))
        existing_by_id[cod] = current
        matched_ids.add(cod)

    if not matched_ids:
        fail("stdin patterns did not match any data rows")

    for key in updates_by_pattern:
        if key not in data_patterns:
            fail(f"stdin pattern did not exist in data: {key}")

    # Merge: preserve data.tsv ordering, keep existing unmapped rows
    merged_rows = []
    seen_ids = set()
    for data_row in data_rows:
        cod = clean(data_row.get("cod_nacion", ""))
        row = existing_by_id.get(cod)
        if row is None:
            continue
        if cod in seen_ids:
            fail(f"duplicate cod_nacion after merge: {cod}")
        seen_ids.add(cod)
        merged_rows.append({col: clean(row.get(col, "")) for col in MAPPING_COLUMNS})

    # Append any existing mapping rows not in data (stale but preserved)
    for row in existing_rows:
        cod = clean(row.get("cod_nacion", ""))
        if cod not in seen_ids:
            seen_ids.add(cod)
            merged_rows.append({col: clean(row.get(col, "")) for col in MAPPING_COLUMNS})

    write_tsv(mapping_path, merged_rows, MAPPING_COLUMNS)
    print(f"Applied {len(updates)} pattern rows -> {len(matched_ids)} cod_nacion rows in {mapping_path}")


if __name__ == "__main__":
    main()
