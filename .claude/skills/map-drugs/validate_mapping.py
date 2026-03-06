#!/usr/bin/env python3
"""Validate mapping.tsv files for correct structure and data types.

Usage:
    python3 skills/map-ema-drugs/validate_mapping.py <path_to_mapping.tsv> [...]

Validates:
- last_updated_date is YYYY-MM-DD formatted and not null
- concept_id is a number or empty
- mapping_type is EXACT, BROAD, or empty

Exit code 0 if all files pass, 1 if any errors found.
"""

import csv
import re
import sys

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
VALID_MAPPING_TYPES = {"EXACT", "BROAD", ""}

VALID_ID_COLUMNS = {"ma_number", "product_id"}
REQUIRED_COLUMNS = [
    "concept_id", "concept_name", "concept_code",
    "mapping_type", "comment", "suggestion", "last_updated_date",
]


def validate_file(path: str) -> list[str]:
    errors = []
    try:
        with open(path, newline="") as f:
            reader = csv.DictReader(f, delimiter="\t")
            fields = reader.fieldnames or []

            # Check ID column (first column)
            if not fields or fields[0] not in VALID_ID_COLUMNS:
                errors.append(
                    f"  First column must be one of {sorted(VALID_ID_COLUMNS)}, "
                    f"got '{fields[0] if fields else '(empty)'}'"
                )
                return errors

            # Check required columns are present
            missing = [c for c in REQUIRED_COLUMNS if c not in fields]
            if missing:
                errors.append(f"  Missing required columns: {missing}")
                return errors

            expected = [fields[0]] + REQUIRED_COLUMNS
            if fields != expected:
                errors.append(
                    f"  Column order mismatch: expected {expected}, "
                    f"got {fields}"
                )
                return errors

            for i, row in enumerate(reader, start=2):
                line = f"line {i}"

                # last_updated_date: required, YYYY-MM-DD
                date = row.get("last_updated_date", "").strip()
                if not date:
                    errors.append(f"  {line}: last_updated_date is empty")
                elif not DATE_RE.match(date):
                    errors.append(
                        f"  {line}: last_updated_date '{date}' is not YYYY-MM-DD"
                    )

                # concept_id: number or empty
                cid = row.get("concept_id", "").strip()
                if cid and not cid.isdigit():
                    errors.append(
                        f"  {line}: concept_id '{cid}' is not a number"
                    )

                # mapping_type: EXACT, BROAD, or empty
                mt = row.get("mapping_type", "").strip()
                if mt not in VALID_MAPPING_TYPES:
                    errors.append(
                        f"  {line}: mapping_type '{mt}' is not EXACT, BROAD, or empty"
                    )

                # BROAD mappings require a suggestion
                suggestion = row.get("suggestion", "").strip()
                if mt == "BROAD" and not suggestion:
                    errors.append(
                        f"  {line}: BROAD mappings require suggestion"
                    )

    except FileNotFoundError:
        errors.append(f"  File not found: {path}")
    except Exception as e:
        errors.append(f"  Error reading file: {e}")

    return errors


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <mapping.tsv> [...]", file=sys.stderr)
        sys.exit(2)

    has_errors = False
    for path in sys.argv[1:]:
        errors = validate_file(path)
        if errors:
            has_errors = True
            print(f"FAIL {path}")
            for e in errors:
                print(e)
        else:
            print(f"OK   {path}")

    sys.exit(1 if has_errors else 0)


if __name__ == "__main__":
    main()
