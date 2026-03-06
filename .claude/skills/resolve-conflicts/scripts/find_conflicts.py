#!/usr/bin/env python3
"""Find conflicting mappings between ema-to-rxnorm.tsv and latvia-to-rxnorm.tsv.

Groups conflicts by EMA product folder so they can be resolved one folder at a time.
"""
import csv
import os
import subprocess
import sys
from collections import defaultdict

GIT_ROOT = subprocess.check_output(
    ["git", "rev-parse", "--show-toplevel"], text=True
).strip()

EMA_TSV = os.path.join(GIT_ROOT, "ema-to-rxnorm.tsv")
LATVIA_TSV = os.path.join(GIT_ROOT, "latvia-to-rxnorm.tsv")
EMA_DATA_DIR = os.path.join(GIT_ROOT, "data", "ema", "products")
LATVIA_DATA_DIR = os.path.join(GIT_ROOT, "data", "latvia", "products")


def read_ema():
    rows = {}
    with open(EMA_TSV, "r") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            rows.setdefault(row["ma_number"], []).append(row)
    return rows


def read_latvia():
    rows = {}
    with open(LATVIA_TSV, "r") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            rows.setdefault(row["product_id"], []).append(row)
    return rows


def ema_folder_num(ema_product_number):
    """EMEA/H/C/XXXXXX -> XXXXXX"""
    return ema_product_number.split("/")[-1] if ema_product_number else None


def build_latvia_folder_index():
    index = {}
    for substance in os.listdir(LATVIA_DATA_DIR):
        substance_dir = os.path.join(LATVIA_DATA_DIR, substance)
        if not os.path.isdir(substance_dir):
            continue
        for product in os.listdir(substance_dir):
            mapping_path = os.path.join(substance_dir, product, "mapping.tsv")
            if os.path.isfile(mapping_path):
                with open(mapping_path, "r") as f:
                    for row in csv.DictReader(f, delimiter="\t"):
                        pid = row.get("product_id", "")
                        if pid:
                            index[pid] = os.path.join(substance_dir, product)
    return index


def main():
    limit = None
    if len(sys.argv) > 1:
        limit = int(sys.argv[1])

    ema_rows = read_ema()
    latvia_rows = read_latvia()

    # Concept sets per ma_number
    ema_concepts = {}
    for ma, rows in ema_rows.items():
        cids = {r["concept_id"] for r in rows if r["concept_id"]}
        if cids:
            ema_concepts[ma] = cids

    latvia_concepts = {}
    for pid, rows in latvia_rows.items():
        cids = {r["concept_id"] for r in rows if r["concept_id"]}
        if cids:
            latvia_concepts[pid] = cids

    common = set(ema_concepts) & set(latvia_concepts)
    conflict_ids = sorted(k for k in common if ema_concepts[k] != latvia_concepts[k])

    # Group by EMA folder number
    groups = defaultdict(list)
    for ma in conflict_ids:
        ema_num = ema_rows[ma][0].get("ema_product_number", "")
        folder = ema_folder_num(ema_num) or "UNKNOWN"
        groups[folder].append(ma)

    print(f"Common IDs with mappings: {len(common)}")
    print(f"Conflicting ma_numbers: {len(conflict_ids)}")
    print(f"Conflicting EMA folders: {len(groups)}")

    if not groups:
        return

    print("Building Latvia folder index...", file=sys.stderr)
    latvia_index = build_latvia_folder_index()

    sorted_folders = sorted(groups.keys())
    if limit:
        sorted_folders = sorted_folders[:limit]

    for folder in sorted_folders:
        ma_numbers = groups[folder]
        first_ema = ema_rows[ma_numbers[0]][0]
        product_name = first_ema.get("ema_name_of_medicine", "")
        ema_path = os.path.join(EMA_DATA_DIR, folder)

        # Collect unique Latvia folders for this group
        latvia_folders = sorted({latvia_index[ma] for ma in ma_numbers if ma in latvia_index})

        # Collect distinct concept pairs across all ma_numbers in this group
        ema_cids = set()
        latvia_cids = set()
        for ma in ma_numbers:
            ema_cids |= ema_concepts[ma]
            latvia_cids |= latvia_concepts[ma]

        print(f"\n{product_name}")
        print(f"  {len(ma_numbers)} conflicting MA numbers")
        print(f"  EMA folder:     {ema_path}")
        for lf in latvia_folders:
            print(f"  Latvia folder:  {lf}")


if __name__ == "__main__":
    main()
