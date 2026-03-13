#!/usr/bin/env python3
"""Validate mapping.tsv files for correct structure and data types.

Usage:
    python3 .claude/skills/map-drugs/validate_mapping.py <path_to_mapping.tsv> [...]

Validates:
- last_updated_date is YYYY-MM-DD formatted and not null
- concept_id is a number or empty
- mapping_type is EXACT, BROAD, or empty
- suggestion is not identical to concept_name
- suggestion is not a stray YYYY-MM-DD value
- suggestion does not contain pipe-delimited pseudo-records
- non-empty suggestions contain a recognized RxNorm dose form

Exit code 0 if all files pass, 1 if any errors found.
"""

import csv
import json
from pathlib import Path
import re
import sys

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
VALID_MAPPING_TYPES = {"EXACT", "BROAD", ""}

VALID_ID_COLUMNS = {"ma_number", "product_id", "cod_nacion"}
# Extra columns that follow the first ID column for certain formats
EXTRA_ID_COLUMNS = {"cod_nacion": ["nro_definitivo"]}
REQUIRED_COLUMNS = [
    "concept_id", "concept_name", "concept_code",
    "mapping_type", "comment", "suggestion", "last_updated_date",
]
DOSE_FORM_LOOKUP_PATH = Path(__file__).with_name("dose_form_lookup.json")


def load_dose_forms() -> list[str]:
    with DOSE_FORM_LOOKUP_PATH.open() as f:
        data = json.load(f)
    names = [item["name"].strip() for item in data if item.get("name")]
    # Match more specific dose forms first.
    return sorted(names, key=len, reverse=True)


VALID_DOSE_FORMS = load_dose_forms()


def suggestion_has_valid_dose_form(suggestion: str) -> bool:
    lower_suggestion = suggestion.casefold()
    return any(dose_form.casefold() in lower_suggestion for dose_form in VALID_DOSE_FORMS)


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

            extra = EXTRA_ID_COLUMNS.get(fields[0], [])
            expected = [fields[0]] + extra + REQUIRED_COLUMNS
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
                concept_name = row.get("concept_name", "").strip()
                suggestion = row.get("suggestion", "").strip()
                if mt == "BROAD" and not suggestion:
                    errors.append(
                        f"  {line}: BROAD mappings require suggestion"
                    )
                if suggestion:
                    if suggestion == concept_name:
                        errors.append(
                            f"  {line}: suggestion must not equal concept_name"
                        )
                    if DATE_RE.fullmatch(suggestion):
                        errors.append(
                            f"  {line}: suggestion must not be a date"
                        )
                    if "|" in suggestion:
                        errors.append(
                            f"  {line}: suggestion must not contain pipe-delimited data"
                        )
                    if not suggestion_has_valid_dose_form(suggestion):
                        errors.append(
                            f"  {line}: suggestion must contain a valid dose form from dose_form_lookup.json"
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
