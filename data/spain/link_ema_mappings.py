#!/usr/bin/env python3
"""
Link EMA mappings to Spain product folders — incremental.

Matches ema-to-rxnorm.tsv ma_number → nro_definitivo by:
  - removing the "EU" prefix and all "/" from ma_number
  - e.g. EU/1/20/1476/001 → 1201476001

Behaviour on each run:
  - Existing rows in mapping.tsv are PRESERVED (manual edits survive reruns).
  - New cod_nacion values (added to source data) are auto-mapped and appended.
  - Stale cod_nacion values (removed from source data) are pruned.

To reset a row to auto-mapping, delete it from mapping.tsv and rerun.
"""

import csv
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
EMA_RXNORM = REPO_ROOT / "ema-to-rxnorm.tsv"
PRODUCTS_DIR = Path(__file__).parent / "products"

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


def normalize_ma_number(ma_number: str) -> str:
    """EU/1/20/1476/001 → 1201476001"""
    s = ma_number.strip()
    if s.startswith("EU"):
        s = s[2:]
    return s.replace("/", "")


def load_existing_mapping(mapping_file: Path) -> dict[str, dict]:
    """Load existing mapping.tsv keyed by cod_nacion."""
    if not mapping_file.exists():
        return {}
    with open(mapping_file, newline="", encoding="utf-8") as f:
        return {
            row["cod_nacion"]: row
            for row in csv.DictReader(f, delimiter="\t")
            if row.get("cod_nacion")
        }


def main():
    if not EMA_RXNORM.exists():
        print(f"ERROR: {EMA_RXNORM} not found", file=sys.stderr)
        sys.exit(1)

    # Build lookup: normalized_ma → first matching EMA mapping row
    print(f"Reading {EMA_RXNORM} ...", file=sys.stderr)
    ema_by_norm: dict[str, dict] = {}
    with open(EMA_RXNORM, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            norm = normalize_ma_number(row["ma_number"])
            if norm not in ema_by_norm:
                ema_by_norm[norm] = row

    print(f"  Loaded {len(ema_by_norm)} EMA mappings", file=sys.stderr)

    total_added = 0
    total_pruned = 0
    total_preserved = 0

    for data_tsv in sorted(PRODUCTS_DIR.glob("*/data.tsv")):
        folder = data_tsv.parent
        mapping_file = folder / "mapping.tsv"

        # Load current source rows: cod_nacion → nro_definitivo
        source: dict[str, str] = {}
        with open(data_tsv, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f, delimiter="\t"):
                cod = row["cod_nacion"].strip()
                nro = row["nro_definitivo"].strip()
                if cod:
                    source[cod] = nro

        # Load existing mapping rows (preserved across reruns)
        existing = load_existing_mapping(mapping_file)

        # Prune stale rows
        pruned = [cod for cod in existing if cod not in source]
        for cod in pruned:
            del existing[cod]

        # Add new rows via EMA auto-match
        added = 0
        for cod, nro in source.items():
            if cod in existing:
                continue  # already mapped (auto or manual) — leave untouched
            ema_row = ema_by_norm.get(nro)
            if ema_row is None:
                continue
            existing[cod] = {
                "cod_nacion": cod,
                "nro_definitivo": nro,
                "concept_id": ema_row["concept_id"],
                "concept_name": ema_row["concept_name"],
                "concept_code": ema_row["concept_code"],
                "mapping_type": ema_row["mapping_type"],
                "comment": ema_row.get("comment", ""),
                "suggestion": ema_row.get("suggestion", ""),
                "last_updated_date": ema_row.get("last_updated_date", ""),
            }
            added += 1

        if not existing:
            continue

        # Write back sorted by cod_nacion
        with open(mapping_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=MAPPING_COLUMNS, delimiter="\t",
                                    extrasaction="ignore")
            writer.writeheader()
            writer.writerows(sorted(existing.values(), key=lambda r: r["cod_nacion"]))

        preserved = len(existing) - added
        if added or pruned:
            print(f"  {folder.name}: +{added} added, -{len(pruned)} pruned, {preserved} preserved",
                  file=sys.stderr)

        total_added += added
        total_pruned += len(pruned)
        total_preserved += preserved

    print(f"\nDone. +{total_added} added, -{total_pruned} pruned, {total_preserved} preserved.",
          file=sys.stderr)


if __name__ == "__main__":
    main()
