#!/usr/bin/env python3
"""
Merge mapping updates into a mapping.tsv file.

Reads new/updated rows from stdin as TSV (same columns as mapping.tsv).
- Existing cod_nacion: updated in place (preserves row order)
- New cod_nacion: appended at the end

Usage:
    python3 .claude/skills/map-spain-drugs/apply_mappings.py data/spain/products/<folder>/mapping.tsv <<'EOF'
    cod_nacion	nro_definitivo	concept_id	concept_name	concept_code	mapping_type	comment	suggestion
    12345	72707	617312	atorvastatin 10 MG Oral Tablet	370584	EXACT
    EOF

    last_updated_date is set to today automatically if not supplied.

Flags:
    --backfill-dates    Fill today's date on all existing rows with empty last_updated_date.
                        No stdin required when using this flag.
"""

import csv
import sys
from datetime import date
from io import StringIO
from pathlib import Path

COLUMNS = [
    "cod_nacion", "nro_definitivo", "concept_id", "concept_name",
    "concept_code", "mapping_type", "comment", "suggestion", "last_updated_date",
]


def load_tsv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def write_tsv(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def fail(message):
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(1)


def validate_columns(rows, label):
    for index, row in enumerate(rows, start=2):
        missing = [column for column in ("cod_nacion", "nro_definitivo") if column not in row]
        if missing:
            fail(f"{label} row {index} is missing required columns: {', '.join(missing)}")


def find_duplicates(rows, key):
    seen = set()
    duplicates = set()
    for row in rows:
        value = row.get(key, "").strip()
        if not value:
            continue
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return sorted(duplicates)


def main():
    args = sys.argv[1:]
    backfill = "--backfill-dates" in args
    positional = [a for a in args if not a.startswith("--")]

    if not positional:
        print(f"Usage: {sys.argv[0]} <mapping.tsv> [--backfill-dates]", file=sys.stderr)
        sys.exit(1)

    mapping_path = Path(positional[0])
    today = date.today().isoformat()

    if backfill:
        if not mapping_path.exists():
            fail(f"{mapping_path} not found")
        rows = load_tsv(mapping_path)
        validate_columns(rows, "mapping.tsv")
        n = 0
        for row in rows:
            if not row.get("last_updated_date", "").strip():
                row["last_updated_date"] = today
                n += 1
        write_tsv(mapping_path, rows)
        print(f"Backfilled dates on {n} rows → {mapping_path}")
        return

    # Read updates from stdin
    stdin_data = sys.stdin.read().strip()
    if not stdin_data:
        fail("no input on stdin")

    updates = list(csv.DictReader(StringIO(stdin_data), delimiter="\t"))
    validate_columns(updates, "stdin")
    duplicate_update_cods = find_duplicates(updates, "cod_nacion")
    if duplicate_update_cods:
        fail(f"stdin contains duplicate cod_nacion values: {', '.join(duplicate_update_cods)}")
    for r in updates:
        if not r.get("last_updated_date", "").strip():
            r["last_updated_date"] = today
    updates_by_cod = {r["cod_nacion"]: r for r in updates}

    # Load existing mapping (or start fresh)
    existing = load_tsv(mapping_path) if mapping_path.exists() else []
    validate_columns(existing, "mapping.tsv")
    duplicate_existing_cods = find_duplicates(existing, "cod_nacion")
    if duplicate_existing_cods:
        fail(f"mapping.tsv contains duplicate cod_nacion values: {', '.join(duplicate_existing_cods)}")
    existing_cods = {r["cod_nacion"] for r in existing}

    # Apply updates in place
    merged = []
    for row in existing:
        cod = row["cod_nacion"]
        if cod in updates_by_cod:
            merged.append(updates_by_cod.pop(cod))
        else:
            merged.append(row)

    # Append new rows (not in existing)
    for row in updates:
        if row["cod_nacion"] in updates_by_cod:
            merged.append(updates_by_cod.pop(row["cod_nacion"]))

    write_tsv(mapping_path, merged)

    n_updated = sum(1 for r in updates if r["cod_nacion"] in existing_cods)
    n_added = len(updates) - n_updated
    print(f"Applied {len(updates)} rows: {n_updated} updated, {n_added} added → {mapping_path}")


if __name__ == "__main__":
    main()
