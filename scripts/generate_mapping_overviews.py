#!/usr/bin/env python3
"""Regenerate combined ema-to-rxnorm.tsv and/or latvia-to-rxnorm.tsv from individual mapping.tsv files.

Usage:
    python3 scripts/generate_mapping_overviews.py          # regenerate both
    python3 scripts/generate_mapping_overviews.py ema       # regenerate EMA only
    python3 scripts/generate_mapping_overviews.py latvia    # regenerate Latvia only
"""

import argparse
import csv
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path


def _gitroot():
    return Path(subprocess.check_output(
        ["git", "rev-parse", "--show-toplevel"], text=True
    ).strip())


GIT_ROOT = _gitroot()

# ---------------------------------------------------------------------------
# EMA
# ---------------------------------------------------------------------------

EMA_DIR = GIT_ROOT / "data" / "ema"

EMA_PARSED_COLUMNS = [
    "ma_number",
    "ema_product_number",
    "strength",
    "pharmaceutical_form",
    "route_of_administration",
    "packaging",
    "content",
    "pack_size",
    "product_name",
]

EMA_MAPPING_COLUMNS = [
    "concept_id",
    "concept_name",
    "concept_code",
    "mapping_type",
    "comment",
    "suggestion",
    "last_updated_date",
]

EMA_RXNORM_COLUMNS = [
    "ma_number",
    "concept_id",
    "concept_name",
    "concept_code",
    "mapping_type",
    "ema_active_substance",
    "pdf_strength",
    "pdf_pharmaceutical_form",
    "pdf_route_of_administration",
    "pdf_packaging",
    "pdf_content",
    "pdf_pack_size",
    "pdf_product_name",
    "ema_name_of_medicine",
    "ema_product_number",
    "ema_atc_code",
    "comment",
    "suggestion",
    "last_updated_date",
]


def _load_medicines_report(report_file):
    """Load medicines_report.tsv into a dict keyed by EMA product number."""
    report = {}
    with open(report_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            product_number = row.get("EMA product number", "")
            if product_number:
                report[product_number] = {
                    "active_substance": row.get("Active substance", ""),
                    "name_of_medicine": row.get("Name of medicine", ""),
                    "atc_code": row.get("ATC code (human)", ""),
                }
    return report


def _load_ema_mappings(ema_pdfs_dir):
    """Load all EMA mapping.tsv files into a dict keyed by ma_number."""
    mappings = {}
    for folder in sorted(ema_pdfs_dir.iterdir()):
        if not folder.is_dir():
            continue
        mapping_file = folder / "mapping.tsv"
        if not mapping_file.exists():
            continue
        with open(mapping_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t")
            for row in reader:
                ma = row.get("ma_number", "")
                if ma:
                    mappings[ma] = {col: row.get(col, "") for col in EMA_MAPPING_COLUMNS}
    return mappings


def regenerate_ema():
    """Regenerate ema-to-rxnorm.tsv from per-product parsed_data and mapping files."""
    ema_pdfs_dir = EMA_DIR / "products"

    mappings = _load_ema_mappings(ema_pdfs_dir)
    empty_mapping = {col: "" for col in EMA_MAPPING_COLUMNS}

    medicines_report = _load_medicines_report(EMA_DIR / "medicines_report.tsv")
    empty_report = {"active_substance": "", "name_of_medicine": "", "atc_code": ""}

    rxnorm_file = GIT_ROOT / "ema-to-rxnorm.tsv"

    all_rows = []

    for folder in sorted(ema_pdfs_dir.iterdir()):
        if not folder.is_dir():
            continue

        tsv_file = folder / "parsed_data.tsv"
        if not tsv_file.exists():
            tsv_files = list(folder.glob("parsed_data_*.tsv"))
            if tsv_files:
                tsv_file = tsv_files[0]
            else:
                continue

        with open(tsv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t")
            for row in reader:
                filtered_row = {col: row.get(col, "") for col in EMA_PARSED_COLUMNS}
                ma = filtered_row["ma_number"]
                mapping_row = mappings.get(ma, empty_mapping)
                filtered_row.update(mapping_row)
                report = medicines_report.get(filtered_row["ema_product_number"], empty_report)
                all_rows.append({
                    "ma_number": ma,
                    "concept_id": filtered_row["concept_id"],
                    "concept_name": filtered_row["concept_name"],
                    "concept_code": filtered_row["concept_code"],
                    "mapping_type": filtered_row["mapping_type"],
                    "ema_active_substance": report["active_substance"],
                    "pdf_strength": filtered_row["strength"],
                    "pdf_pharmaceutical_form": filtered_row["pharmaceutical_form"],
                    "pdf_route_of_administration": filtered_row["route_of_administration"],
                    "pdf_packaging": filtered_row["packaging"],
                    "pdf_content": filtered_row["content"],
                    "pdf_pack_size": filtered_row["pack_size"],
                    "pdf_product_name": filtered_row["product_name"],
                    "ema_name_of_medicine": report["name_of_medicine"],
                    "ema_product_number": filtered_row["ema_product_number"],
                    "ema_atc_code": report["atc_code"],
                    "comment": filtered_row["comment"],
                    "suggestion": filtered_row["suggestion"],
                    "last_updated_date": filtered_row["last_updated_date"],
                })

    with open(rxnorm_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=EMA_RXNORM_COLUMNS, delimiter="\t")
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"EMA: Generated {len(all_rows)} rows into {rxnorm_file}")


# ---------------------------------------------------------------------------
# Latvia
# ---------------------------------------------------------------------------

LATVIA_DIR = GIT_ROOT / "data" / "latvia"

LATVIA_MAPPING_COLUMNS = [
    "concept_id",
    "concept_name",
    "concept_code",
    "mapping_type",
    "comment",
    "suggestion",
    "last_updated_date",
]

LATVIA_PRODUCT_COLUMNS = [
    "product_id",
    "original_name",
    "short_name",
    "active_substance",
    "strength",
    "pharmaceutical_form",
    "product_strength",
    "package_en",
    "package_size",
    "authorisation_no",
    "date_of_authorisation",
    "inter_code",
    "atc_code",
    "marketing_authorisation_holder",
    "manufacturer",
    "status",
]

LATVIA_RXNORM_COLUMNS = [
    "product_id",
    "inter_code",
    "concept_id",
    "concept_name",
    "concept_code",
    "mapping_type",
    "active_substance",
    "strength",
    "pharmaceutical_form",
    "product_strength",
    "package_en",
    "package_size",
    "original_name",
    "short_name",
    "authorisation_no",
    "atc_code",
    "marketing_authorisation_holder",
    "comment",
    "suggestion",
    "last_updated_date",
]


def _load_human_products(json_file):
    """Load HumanProducts.json into a dict keyed by product_id."""
    with open(json_file, "r", encoding="utf-8-sig") as f:
        products = json.load(f)
    return {p["product_id"]: p for p in products}


def _load_latvia_mappings(products_dir):
    """Load all Latvia mapping.tsv files from the products directory tree."""
    mappings = {}
    for mapping_file in sorted(products_dir.rglob("mapping.tsv")):
        with open(mapping_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t")
            for row in reader:
                pid = row.get("product_id", "").strip()
                if pid:
                    mappings[pid] = {col: row.get(col, "").strip() for col in LATVIA_MAPPING_COLUMNS}
    return mappings


def regenerate_latvia():
    """Regenerate latvia-to-rxnorm.tsv from per-product mapping files and HumanProducts.json."""
    products_dir = LATVIA_DIR / "products"
    json_file = LATVIA_DIR / "HumanProducts.json"

    print("Loading HumanProducts.json...")
    products = _load_human_products(json_file)
    print(f"  Loaded {len(products)} products")

    print("Loading Latvia mapping.tsv files...")
    mappings = _load_latvia_mappings(products_dir)
    print(f"  Loaded {len(mappings)} mappings")

    rxnorm_file = GIT_ROOT / "latvia-to-rxnorm.tsv"
    all_rows = []

    for pid, mapping in sorted(mappings.items()):
        product = products.get(pid, {})
        row = {col: product.get(col, "") for col in LATVIA_PRODUCT_COLUMNS}
        row["product_id"] = pid
        row.update(mapping)
        all_rows.append({col: row.get(col, "") for col in LATVIA_RXNORM_COLUMNS})

    with open(rxnorm_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=LATVIA_RXNORM_COLUMNS, delimiter="\t")
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"Latvia: Generated {len(all_rows)} rows into {rxnorm_file}")

    mapped = sum(1 for r in all_rows if r["concept_id"])
    unmapped = len(all_rows) - mapped
    print(f"  Mapped: {mapped}, Unmapped: {unmapped}")

    missing_product = sum(1 for r in all_rows if not r["original_name"])
    print(f"  Missing product info (not in HumanProducts.json): {missing_product}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Regenerate combined RxNorm mapping TSV files from individual mapping.tsv files."
    )
    parser.add_argument(
        "source",
        nargs="?",
        choices=["ema", "latvia"],
        help="Regenerate only EMA or Latvia (default: both)",
    )
    args = parser.parse_args()

    if args.source == "ema":
        regenerate_ema()
    elif args.source == "latvia":
        regenerate_latvia()
    else:
        regenerate_ema()
        print()
        regenerate_latvia()


if __name__ == "__main__":
    main()
