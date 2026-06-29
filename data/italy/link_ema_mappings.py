#!/usr/bin/env python3
"""
Auto-populate Italy product folder mapping.tsv files by linking to EMA mappings.

Strategy:
  1. Build a lookup: normalised brand name → EMA product folder (from medicines_report.tsv)
  2. For each Italy product folder that contains Procedura Centralizzata packs,
     look up the brand name in the EMA lookup.
  3. Load that EMA product's mapping.tsv.
  4. If ALL EMA presentations map to the same RxNorm concept, apply that concept
     to all Italy packs (EXACT). This handles single-concept products cleanly.
  5. Write mapping.tsv — incremental: existing manual rows are preserved.

Run:
  python3 data/italy/link_ema_mappings.py
  python3 data/italy/link_ema_mappings.py --dry-run   # preview only
"""

import csv
import re
import sys
from datetime import date
from pathlib import Path

EMA_DATA_DIR = Path(__file__).resolve().parent.parent / "ema" / "products"
EMA_REPORT = Path(__file__).resolve().parent.parent / "ema" / "medicines_report.tsv"
ITALY_PRODUCTS_DIR = Path(__file__).parent / "products"

TODAY = date.today().isoformat()

MAPPING_COLUMNS = [
    "codice_aic", "cod_farmaco",
    "concept_id", "concept_name", "concept_code",
    "mapping_type", "comment", "suggestion", "last_updated_date",
]


# ── helpers ──────────────────────────────────────────────────────────────────

def norm_name(name: str) -> str:
    """Normalise a brand name for fuzzy matching."""
    name = name.lower().strip()
    name = re.sub(r"[^a-z0-9]", "", name)
    return name


def load_tsv(path: Path) -> tuple[list[str], list[dict]]:
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        return list(reader.fieldnames or []), list(reader)


def write_tsv(path: Path, columns: list[str], rows: list[dict]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns, delimiter="\t",
                                extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


# ── EMA data loading ──────────────────────────────────────────────────────────

def build_ema_name_lookup() -> dict[str, str]:
    """Return {normalised_brand_name: ema_folder_id} from medicines_report.tsv."""
    if not EMA_REPORT.exists():
        print(f"WARNING: {EMA_REPORT} not found — no EMA linking possible", file=sys.stderr)
        return {}
    _, rows = load_tsv(EMA_REPORT)
    lookup: dict[str, str] = {}
    for row in rows:
        name = row.get("Name of medicine", "").strip()
        prod_num = row.get("EMA product number", "").strip()
        if not name or not prod_num:
            continue
        # EMEA/H/C/000074 → 000074
        m = re.search(r"/(\d+)$", prod_num)
        if m:
            lookup[norm_name(name)] = m.group(1).zfill(6)
    return lookup


def load_ema_product_mapping(folder_id: str) -> list[dict]:
    mapping_path = EMA_DATA_DIR / folder_id / "mapping.tsv"
    if not mapping_path.exists():
        return []
    _, rows = load_tsv(mapping_path)
    return rows


def single_concept(ema_rows: list[dict]) -> dict | None:
    """Return the shared concept if all mapped rows agree on concept_id, else None."""
    mapped = [r for r in ema_rows if r.get("concept_id", "").strip()
              and r.get("mapping_type", "").strip() not in ("NO_MAPPING", "")]
    if not mapped:
        return None
    concept_ids = {r["concept_id"].strip() for r in mapped}
    if len(concept_ids) != 1:
        return None
    r = mapped[0]
    return {
        "concept_id":   r["concept_id"].strip(),
        "concept_name": r.get("concept_name", "").strip(),
        "concept_code": r.get("concept_code", "").strip(),
        "mapping_type": r.get("mapping_type", "EXACT").strip(),
    }


# ── main ─────────────────────────────────────────────────────────────────────

def main():
    dry_run = "--dry-run" in sys.argv

    print("Building EMA name lookup...", file=sys.stderr)
    ema_lookup = build_ema_name_lookup()
    print(f"  {len(ema_lookup)} EMA products indexed", file=sys.stderr)

    folders = sorted(ITALY_PRODUCTS_DIR.iterdir())
    stats = {"folders": 0, "linked": 0, "new_rows": 0, "skipped_ambiguous": 0, "skipped_no_match": 0}

    for folder in folders:
        data_path = folder / "data.tsv"
        if not data_path.exists():
            continue
        stats["folders"] += 1

        _, data_rows = load_tsv(data_path)

        # Find Procedura Centralizzata packs
        central_rows = [r for r in data_rows if r.get("tipo_procedura", "") == "Procedura Centralizzata"]
        if not central_rows:
            continue

        # Get the brand name (denominazione) — use the first one found
        brand = central_rows[0].get("denominazione", "").strip()
        ema_folder_id = ema_lookup.get(norm_name(brand))
        if not ema_folder_id:
            stats["skipped_no_match"] += 1
            continue

        ema_rows = load_ema_product_mapping(ema_folder_id)
        concept = single_concept(ema_rows)
        if not concept:
            stats["skipped_ambiguous"] += 1
            continue

        # Load existing mapping (to preserve manual edits)
        mapping_path = folder / "mapping.tsv"
        existing: dict[str, dict] = {}
        if mapping_path.exists():
            _, existing_rows = load_tsv(mapping_path)
            existing = {r["codice_aic"]: r for r in existing_rows if r.get("codice_aic")}

        # Build updated mapping — all packs in the folder (not just Centralizzata)
        added = 0
        for row in data_rows:
            aic = row.get("codice_aic", "").strip()
            if not aic:
                continue
            if aic in existing:
                continue  # preserve existing row
            existing[aic] = {
                "codice_aic":       aic,
                "cod_farmaco":      row.get("cod_farmaco", "").strip(),
                "concept_id":       concept["concept_id"],
                "concept_name":     concept["concept_name"],
                "concept_code":     concept["concept_code"],
                "mapping_type":     concept["mapping_type"],
                "comment":          f"auto-linked from EMA {ema_folder_id}",
                "suggestion":       "",
                "last_updated_date": TODAY,
            }
            added += 1

        if added == 0:
            continue

        stats["linked"] += 1
        stats["new_rows"] += added

        out_rows = sorted(existing.values(), key=lambda r: r.get("codice_aic", ""))
        if dry_run:
            print(f"  [dry-run] {folder.name}: {added} rows → EMA {ema_folder_id} {concept['concept_name'][:60]}")
        else:
            write_tsv(mapping_path, MAPPING_COLUMNS, out_rows)

    print(
        f"\nDone. Folders scanned: {stats['folders']}, "
        f"linked: {stats['linked']}, "
        f"new rows: {stats['new_rows']}, "
        f"no EMA match: {stats['skipped_no_match']}, "
        f"ambiguous concepts: {stats['skipped_ambiguous']}",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
