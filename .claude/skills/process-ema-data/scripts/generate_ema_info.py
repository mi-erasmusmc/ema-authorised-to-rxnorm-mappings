#!/usr/bin/env python3
"""Generate ema-info.txt files in each products subfolder from medicines_report.tsv."""

import csv
import os
import subprocess


def _gitroot():
    return subprocess.check_output(
        ["git", "rev-parse", "--show-toplevel"], text=True
    ).strip()


GIT_ROOT = _gitroot()
EMA_DIR = os.path.join(GIT_ROOT, "data", "ema")
TSV_PATH = os.path.join(EMA_DIR, "medicines_report.tsv")
PDF_DIR = os.path.join(EMA_DIR, "products")

FIELDS = [
    "EMA product number",
    "Name of medicine",
    "Medicine status",
    "International non-proprietary name (INN) / common name",
    "Active substance",
    "Therapeutic area (MeSH)",
    "ATC code (human)",
    "Pharmacotherapeutic group (human)",
    "Therapeutic indication",
    "Biosimilar",
    "Generic or hybrid",
    "Medicine URL",
]


def main():
    # Read TSV and build lookup by product number suffix
    products = {}
    with open(TSV_PATH, "r") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            if row.get("Category") != "Human":
                continue
            ema_num = row["EMA product number"]
            suffix = ema_num.split("/")[-1] if "/" in ema_num else ema_num
            products[suffix] = row

    created = 0
    missing = 0
    for folder in sorted(os.listdir(PDF_DIR)):
        folder_path = os.path.join(PDF_DIR, folder)
        if not os.path.isdir(folder_path) or folder.startswith("."):
            continue
        if folder in products:
            row = products[folder]
            def _get(field):
                val = row.get(field, "")
                if field == "Active substance" and not val:
                    val = row.get("International non-proprietary name (INN) / common name", "")
                return val
            lines = [f"{field}: {_get(field)}" for field in FIELDS]
            with open(os.path.join(folder_path, "ema-info.txt"), "w") as out:
                out.write("\n".join(lines) + "\n")
            created += 1
        else:
            missing += 1
            print(f"No TSV match for folder: {folder}")

    print(f"\nCreated {created} ema-info.txt files, {missing} folders had no match")


if __name__ == "__main__":
    main()
