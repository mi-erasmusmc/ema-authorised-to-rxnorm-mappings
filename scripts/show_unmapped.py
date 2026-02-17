#!/usr/bin/env python3
"""Show unmapped Latvia products grouped by unique presentation identity.

Usage:
    python3 scripts/show_unmapped.py data/latvia/products/<substance>/

Outputs a compact summary for mapping decisions — one line per unique
(original_name, strength, pharmaceutical_form, product_strength, package) group.
"""

import csv
import glob
import os
import re
import sys
from collections import defaultdict


def normalize_package(package_en, package_size):
    """Normalize package description to ignore size-only differences."""
    # Strip the N<number> suffix and size — these don't affect concept choice
    pkg = re.sub(r',?\s*N\d+\s*$', '', package_en).strip()
    return pkg


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/show_unmapped.py <substance_dir> [...]")
        sys.exit(1)

    for substance_dir in sys.argv[1:]:
        substance_dir = substance_dir.rstrip("/")
        substance = os.path.basename(substance_dir)
        print(f"\n=== {substance} ===")

        # Group by the identity key that determines concept choice
        groups = defaultdict(list)
        total_unmapped = 0
        total_mapped = 0

        for mapping_file in sorted(glob.glob(os.path.join(substance_dir, "*/mapping.tsv"))):
            product = os.path.basename(os.path.dirname(mapping_file))
            product_data = {}

            data_files = glob.glob(os.path.join(os.path.dirname(mapping_file), "data_*.tsv"))
            if data_files:
                with open(sorted(data_files)[-1]) as f:
                    for row in csv.DictReader(f, delimiter="\t"):
                        product_data[row["product_id"]] = row

            with open(mapping_file) as f:
                for row in csv.DictReader(f, delimiter="\t"):
                    if row.get("concept_id"):
                        total_mapped += 1
                    else:
                        total_unmapped += 1
                        pid = row["product_id"]
                        pdata = product_data.get(pid, {})
                        pkg = normalize_package(
                            pdata.get("package_en", ""),
                            pdata.get("package_size", ""),
                        )
                        key = (
                            (pdata.get("original_name") or "").strip(),
                            (pdata.get("strength") or "").strip(),
                            (pdata.get("pharmaceutical_form") or "").strip(),
                            (pdata.get("product_strength") or "").strip(),
                            pkg,
                        )
                        groups[key].append((product, pid))

        if not groups:
            print(f"  All mapped ({total_mapped} rows)")
            continue

        print(f"  {total_unmapped} unmapped / {total_mapped + total_unmapped} total\n")

        for (name, strength, form, prod_strength, pkg), items in sorted(groups.items()):
            products = sorted(set(p for p, _ in items))
            pids = [pid for _, pid in items]

            print(f"  [{len(items)} rows] {name}")
            print(f"    strength: {strength} | form: {form} | product_strength: {prod_strength}")
            if pkg:
                print(f"    package: {pkg}")
            print(f"    products: {', '.join(products)}")
            if len(pids) > 2:
                print(f"    IDs: {pids[0]}..{pids[-1]}  ({len(pids)})")
            else:
                print(f"    IDs: {', '.join(pids)}")
            print()


if __name__ == "__main__":
    main()
