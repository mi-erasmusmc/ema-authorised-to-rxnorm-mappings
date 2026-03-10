#!/usr/bin/env python3
"""
One-shot import of spanish_mappings.tsv into per-product mapping.tsv files.

Matching: authorisationnumber → nro_definitivo
  - Periods and commas are stripped (used as thousands separators, e.g. 61,892 → 61892)
  - Tries raw value first, then normalised

Rules:
  - Exact duplicate rows (same authorisationnumber + concept_id) are deduplicated.
  - A cod_nacion that already has a concept_id set is left untouched.
  - A cod_nacion with no existing mapping gets the matched concept written in.
  - If a nro_definitivo maps to multiple cod_nacion (known CIMA data issue), all
    unmapped ones receive the concept — flag these for review.

Run once after link_ema_mappings.py has seeded initial mapping.tsv files.
"""

import csv
import sys
from collections import defaultdict
from pathlib import Path

SPAIN_DIR = Path(__file__).parent
SOURCE_FILE = SPAIN_DIR / "spanish_mappings.tsv"
PRODUCTS_DIR = SPAIN_DIR / "products"

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


def normalize_auth(num: str) -> str:
    """Remove periods and commas used as thousands separators."""
    return num.replace(".", "").replace(",", "")


def load_source_mappings(source_file: Path) -> dict[str, dict]:
    """Load spanish_mappings.tsv, deduplicate, return dict keyed by normalized auth number.

    Where multiple rows share the same auth number (all identical concept_id after dedup),
    only one is kept.
    """
    seen: set[tuple] = set()
    by_norm: dict[str, dict] = {}
    duplicates = 0

    with open(source_file, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            num = row["authorisationnumber"].strip()
            concept_id = row["concept_id"].strip()
            key = (num, concept_id)
            if key in seen:
                duplicates += 1
                continue
            seen.add(key)
            norm = normalize_auth(num)
            # Prefer raw match, fall back to normalized
            by_norm[num] = row   # raw
            by_norm[norm] = row  # normalized (may overwrite raw if same)

    print(f"  {len(seen)} unique source rows ({duplicates} exact duplicates dropped)",
          file=sys.stderr)
    return by_norm


def load_folder_mappings(mapping_file: Path) -> dict[str, dict]:
    """Load existing mapping.tsv keyed by cod_nacion."""
    if not mapping_file.exists():
        return {}
    with open(mapping_file, newline="", encoding="utf-8") as f:
        return {row["cod_nacion"]: row for row in csv.DictReader(f, delimiter="\t")
                if row.get("cod_nacion")}


def write_mapping(mapping_file: Path, rows: dict[str, dict]) -> None:
    with open(mapping_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=MAPPING_COLUMNS, delimiter="\t",
                                extrasaction="ignore")
        writer.writeheader()
        writer.writerows(sorted(rows.values(), key=lambda r: r["cod_nacion"]))


def main():
    if not SOURCE_FILE.exists():
        print(f"ERROR: {SOURCE_FILE} not found", file=sys.stderr)
        sys.exit(1)

    print(f"Loading {SOURCE_FILE} ...", file=sys.stderr)
    source = load_source_mappings(SOURCE_FILE)

    # Build nro_definitivo → [(cod_nacion, nro)] from all data.tsv files
    nro_to_rows: dict[str, list[tuple[str, str, Path]]] = defaultdict(list)
    for data_tsv in sorted(PRODUCTS_DIR.glob("*/data.tsv")):
        with open(data_tsv, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f, delimiter="\t"):
                cod = row["cod_nacion"].strip()
                nro = row["nro_definitivo"].strip()
                if cod and nro:
                    nro_to_rows[nro].append((cod, nro, data_tsv.parent))
                    norm = normalize_auth(nro)
                    if norm != nro:
                        nro_to_rows[norm].append((cod, nro, data_tsv.parent))

    # Process each matched source row
    # Accumulate changes per folder
    folder_updates: dict[Path, dict[str, dict]] = defaultdict(dict)

    matched_nros = 0
    skipped_already_mapped = 0
    flagged_multi_cod = 0

    with open(SOURCE_FILE, newline="", encoding="utf-8") as _f:
        _all_nums = list(dict.fromkeys(
            row["authorisationnumber"].strip()
            for row in csv.DictReader(_f, delimiter="\t")
        ))

    for raw_num in _all_nums:
        norm = normalize_auth(raw_num)
        source_row = source.get(raw_num) or source.get(norm)
        if source_row is None:
            continue

        matches = nro_to_rows.get(raw_num) or nro_to_rows.get(norm)
        if not matches:
            continue

        matched_nros += 1
        if len(matches) > 1:
            flagged_multi_cod += 1

        for cod, nro, folder in matches:
            folder_updates[folder][cod] = {
                "cod_nacion": cod,
                "nro_definitivo": nro,
                "concept_id": source_row["concept_id"].strip(),
                "concept_name": source_row["concept_name"].strip(),
                "concept_code": source_row["concept_code"].strip(),
                "mapping_type": source_row.get("mapping_typ", "").strip(),
                "comment": "",
                "suggestion": "",
                "last_updated_date": "",
            }

    # Merge with existing mapping.tsv — existing concept_id wins
    total_added = 0
    total_skipped = 0

    for folder, new_rows in sorted(folder_updates.items()):
        mapping_file = folder / "mapping.tsv"
        existing = load_folder_mappings(mapping_file)

        added = 0
        for cod, new_row in new_rows.items():
            if cod in existing and existing[cod].get("concept_id", "").strip():
                total_skipped += 1
                skipped_already_mapped += 1
                continue
            existing[cod] = new_row
            added += 1
            total_added += 1

        if added:
            write_mapping(mapping_file, existing)
            print(f"  {folder.name}: +{added} added", file=sys.stderr)

    print(f"\nDone.", file=sys.stderr)
    print(f"  Source auth numbers matched to CIMA nro_definitivo: {matched_nros}",
          file=sys.stderr)
    print(f"  Auth numbers with multiple cod_nacion (review recommended): {flagged_multi_cod}",
          file=sys.stderr)
    print(f"  Rows added to mapping.tsv files: {total_added}", file=sys.stderr)
    print(f"  Rows skipped (already had mapping): {skipped_already_mapped}", file=sys.stderr)


if __name__ == "__main__":
    main()
