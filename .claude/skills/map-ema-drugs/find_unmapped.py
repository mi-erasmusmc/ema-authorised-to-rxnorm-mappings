#!/usr/bin/env python3
"""List EMA product folders that have parsed data but no mapping.tsv."""

import subprocess
from pathlib import Path


def _gitroot():
    return Path(subprocess.check_output(
        ["git", "rev-parse", "--show-toplevel"], text=True
    ).strip())


def main():
    pdf_dir = _gitroot() / "data" / "ema" / "products"
    unmapped = []

    for folder in sorted(pdf_dir.iterdir()):
        if not folder.is_dir() or folder.name.startswith("."):
            continue
        has_parsed = any(folder.glob("parsed_data*.tsv"))
        has_mapping = (folder / "mapping.tsv").exists()
        if has_parsed and not has_mapping:
            unmapped.append(folder.name)

    if not unmapped:
        print("All parsed products have mapping.tsv.")
    else:
        print(f"{len(unmapped)} products need mapping:")
        for name in unmapped:
            print(name)


if __name__ == "__main__":
    main()
