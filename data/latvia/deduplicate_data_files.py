#!/usr/bin/env python3
"""
After running organize_products.py, each product folder may have a new dated data file
alongside the previous one. This script compares them and keeps only one:
  - If equal:   delete the newer file (no change, old date preserved)
  - If changed: delete the older file (keep the update)

Prints a summary of changed, unchanged, and new (no prior file) folders.
"""

import sys
from pathlib import Path

PRODUCTS_DIR = Path(__file__).parent / "products"


def data_files(folder: Path) -> list[Path]:
    """Return dated data_*.tsv files sorted oldest first."""
    return sorted(folder.glob("data_*.tsv"))


def main():
    changed = []
    unchanged = []
    new = []

    for folder in sorted(PRODUCTS_DIR.rglob("data_*.tsv")):
        # rglob gives individual files; we want to process each product folder once
        pass

    product_folders = sorted(
        {f.parent for f in PRODUCTS_DIR.rglob("data_*.tsv")}
    )

    for folder in product_folders:
        files = data_files(folder)
        if len(files) < 2:
            if len(files) == 1:
                new.append(folder)
            continue

        # Compare the two most recent files (handles edge case of 3+ files gracefully)
        older, newer = files[-2], files[-1]
        if older.read_bytes() == newer.read_bytes():
            newer.unlink()
            unchanged.append(folder)
        else:
            older.unlink()
            changed.append(folder)

    print(f"Changed:   {len(changed)}")
    print(f"Unchanged: {len(unchanged)}")
    print(f"New:       {len(new)}")

    if changed:
        print("\nChanged folders:")
        for f in changed:
            print(f"  {f.relative_to(PRODUCTS_DIR.parent.parent)}")

    if new:
        print("\nNew folders:")
        for f in new:
            print(f"  {f.relative_to(PRODUCTS_DIR.parent.parent)}")


if __name__ == "__main__":
    main()
