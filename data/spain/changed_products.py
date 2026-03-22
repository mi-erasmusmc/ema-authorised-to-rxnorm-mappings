#!/usr/bin/env python3
"""
List product folders whose data.tsv has changed since the last git commit.

Detects both modified and newly created (untracked) data.tsv files so that
new ingredient folders are included alongside updated ones.

Usage:
    python3 data/spain/changed_products.py
    python3 data/spain/changed_products.py --paths   # absolute paths (default: relative)
    python3 data/spain/changed_products.py --null    # NUL-separated output (for xargs -0)
"""

import argparse
import subprocess
import sys
from pathlib import Path

PRODUCTS_DIR = Path(__file__).parent / "products"


def git_changed_data_tsvs() -> list[Path]:
    """Return paths of data.tsv files that are modified or untracked in the working tree."""
    root = Path(
        subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
    )

    # Modified (staged or unstaged) vs HEAD
    modified = subprocess.check_output(
        ["git", "diff", "--name-only", "HEAD", "--", "data/spain/products/*/data.tsv"],
        text=True,
    ).splitlines()

    # Also catch staged-only changes (in case user ran git add)
    staged = subprocess.check_output(
        ["git", "diff", "--name-only", "--cached", "--", "data/spain/products/*/data.tsv"],
        text=True,
    ).splitlines()

    # Untracked (new product folders)
    status = subprocess.check_output(
        ["git", "status", "--porcelain", "--", "data/spain/products/"],
        text=True,
    ).splitlines()
    untracked = [
        line[3:]
        for line in status
        if line.startswith("?? ") and line.endswith("data.tsv")
    ]

    seen = set()
    result = []
    for rel in modified + staged + untracked:
        p = (root / rel).resolve()
        if p not in seen and p.exists():
            seen.add(p)
            result.append(p)

    return sorted(result)


def main():
    parser = argparse.ArgumentParser(description="List Spain product folders with changed data.tsv")
    parser.add_argument("--paths", action="store_true", help="Print full absolute paths (default)")
    parser.add_argument("--null", "-0", action="store_true", help="Separate output with NUL instead of newline")
    args = parser.parse_args()

    changed = git_changed_data_tsvs()

    if not changed:
        print("No changed data.tsv files found.", file=sys.stderr)
        sys.exit(0)

    sep = "\0" if args.null else "\n"
    folders = [str(p.parent) for p in changed]
    print(sep.join(folders), end=sep if args.null else "\n")


if __name__ == "__main__":
    main()
