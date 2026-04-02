#!/usr/bin/env python3
"""
Apply Latvia mapping decisions by presentation pattern.

Reads mapping decisions from stdin as TSV keyed by the default pattern fields used by
list_folder_patterns.py, then expands those decisions to all matching product_id rows.

Usage:
    python3 .claude/skills/map-latvia-drugs/apply_pattern_mappings.py \
        data/latvia/products/<substance>/<product>/mapping.tsv <<'EOF'
    original_name	strength	pharmaceutical_form	product_strength	concept_id	concept_name	concept_code	mapping_type	comment	suggestion
    CarvedilolHexal 6.25 mg tablets	6.25 mg	Tablet	6,25 mg	19022749	carvedilol 6.25 MG Oral Tablet	200031	EXACT
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
from helpers import clean, fail, find_dated_file, load_tsv, pattern_key, write_tsv  # noqa: E402

PATTERN_COLUMNS = [
    "original_name",
    "strength",
    "pharmaceutical_form",
    "product_strength",
]

MAPPING_COLUMNS = [
    "product_id",
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
        missing = [column for column in PATTERN_COLUMNS if column not in row]
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
    data_path = find_dated_file(folder)
    today = date.today().isoformat()

    if not data_path:
        fail(f"no data_*.tsv found in {folder}")

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
    existing_by_id = {clean(row.get("product_id", "")): row for row in existing_rows}

    matched_ids = set()
    data_patterns = {pattern_key(row, PATTERN_COLUMNS) for row in data_rows}

    for data_row in data_rows:
        key = pattern_key(data_row, PATTERN_COLUMNS)
        if key not in updates_by_pattern:
            continue
        product_id = clean(data_row.get("product_id", ""))
        current = existing_by_id.get(product_id, {"product_id": product_id})
        if only_missing and (clean(current.get("concept_id", "")) or clean(current.get("mapping_type", ""))):
            continue

        update = updates_by_pattern[key]
        for column in MAPPING_COLUMNS:
            if column == "product_id":
                current[column] = product_id
            else:
                current[column] = clean(update.get(column, ""))
        existing_by_id[product_id] = current
        matched_ids.add(product_id)

    if not matched_ids:
        fail("stdin patterns did not match any data rows")

    for key in updates_by_pattern:
        if key not in data_patterns:
            fail(f"stdin pattern did not exist in data: {key}")

    merged_rows = []
    seen_ids = set()
    for data_row in data_rows:
        product_id = clean(data_row.get("product_id", ""))
        row = existing_by_id.get(product_id)
        if row is None:
            continue
        if product_id in seen_ids:
            fail(f"duplicate product_id after merge: {product_id}")
        seen_ids.add(product_id)
        merged_rows.append({column: clean(row.get(column, "")) for column in MAPPING_COLUMNS})

    write_tsv(mapping_path, merged_rows, MAPPING_COLUMNS)
    print(f"Applied {len(updates)} pattern rows -> {len(matched_ids)} product rows in {mapping_path}")


if __name__ == "__main__":
    main()
