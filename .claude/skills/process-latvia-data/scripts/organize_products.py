#!/usr/bin/env python3
import csv
import json
import os
import re
import subprocess
from datetime import date


def _gitroot():
    return subprocess.check_output(
        ["git", "rev-parse", "--show-toplevel"], text=True
    ).strip()


GIT_ROOT = _gitroot()
LATVIA_DIR = os.path.join(GIT_ROOT, "data", "latvia")
DATA_FILE = os.path.join(LATVIA_DIR, "HumanProducts.json")
OUTPUT_DIR = os.path.join(LATVIA_DIR, "products")

TSV_FIELDS = [
    "product_id",
    "original_name",
    "authorisation_no",
    "date_of_authorisation",
    "inter_code",
    "strength",
    "pharmaceutical_form",
    "product_strength",
    "package_en",
    "package_size",
]

INFO_FIELDS = [
    "short_name",
    "active_substance",
    "marketing_authorisation_holder",
    "manufacturer",
    "atc_code",
    "package_leaflet",
    "summary_of_product_characteristics",
]


def sanitize_folder_name(name):
    """Lowercase, replace whitespace with _, truncate to 96 chars."""
    name = name.strip().lower()
    name = re.sub(r"\s+", "_", name)
    name = re.sub(r'[<>:"/\\|?*]', "", name)
    return name[:96]


def main():
    with open(DATA_FILE, encoding="utf-8-sig") as f:
        products = json.load(f)

    # Group by (substance_slug, name_slug) so case variants merge into the same folder.
    # e.g. "Torasemide HEXAL" and "Torasemide Hexal" both → "torasemide_hexal"
    grouped = {}  # {(substance_slug, name_slug): [products]}
    for product in products:
        substance = product.get("active_substance", "unknown")
        short_name = product.get("short_name", "unknown")
        key = (sanitize_folder_name(substance), sanitize_folder_name(short_name))
        grouped.setdefault(key, []).append(product)

    today = date.today().isoformat()

    for (substance_slug, name_slug), items in sorted(grouped.items()):
        substance_folder = os.path.join(OUTPUT_DIR, substance_slug)
        os.makedirs(substance_folder, exist_ok=True)

        name_folder = os.path.join(substance_folder, name_slug)
        os.makedirs(name_folder, exist_ok=True)

        # Check info fields are consistent across all products in group
        first = items[0]
        for field in INFO_FIELDS:
            values = set(item.get(field, "") for item in items)
            if len(values) > 1:
                print(f"WARNING: '{field}' differs in {substance_slug} / {name_slug}: {values}")

        info_path = os.path.join(name_folder, "info.txt")
        with open(info_path, "w", encoding="utf-8") as f:
            for field in INFO_FIELDS:
                f.write(f"{field}: {first.get(field, '')}\n")

        # Write dated TSV with selected columns
        tsv_path = os.path.join(name_folder, f"data_{today}.tsv")
        with open(tsv_path, "w", newline="", encoding="utf-8") as tsv_file:
            writer = csv.DictWriter(
                tsv_file, fieldnames=TSV_FIELDS, delimiter="\t", extrasaction="ignore"
            )
            writer.writeheader()
            writer.writerows(items)

    print(f"Done. Processed {len(products)} products into {len(grouped)} folders across {len(set(k[0] for k in grouped))} active substances.")


if __name__ == "__main__":
    main()
