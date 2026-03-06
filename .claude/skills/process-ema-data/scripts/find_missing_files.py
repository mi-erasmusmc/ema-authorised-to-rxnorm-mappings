#!/usr/bin/env python3
"""Find folders with missing PDF/TSV/mapping/ema-info files in products."""

import subprocess
from pathlib import Path


def _gitroot():
    return Path(subprocess.check_output(
        ["git", "rev-parse", "--show-toplevel"], text=True
    ).strip())


GIT_ROOT = _gitroot()
EMA_DIR = GIT_ROOT / "data" / "ema"
SKIP_DIRS = {".claude"}


def find_missing_files():
    pdf_dir = EMA_DIR / "products"

    if not pdf_dir.exists():
        print(f"Directory not found: {pdf_dir}")
        return

    headers = ["Folder", "PDF", "parsed_data.tsv", "mapping.tsv", "ema-info.txt"]
    rows = []

    for folder in sorted(pdf_dir.iterdir()):
        if not folder.is_dir() or folder.name in SKIP_DIRS:
            continue

        has_pdf = len(list(folder.glob("*.pdf"))) > 0
        has_parsed = len(list(folder.glob("parsed_data*.tsv"))) > 0
        has_mapping = (folder / "mapping.tsv").exists()
        has_ema_info = (folder / "ema-info.txt").exists()

        missing = [not has_pdf, not has_parsed, not has_mapping, not has_ema_info]
        if any(missing):
            rows.append([
                folder.name,
                "x" if not has_pdf else "",
                "x" if not has_parsed else "",
                "x" if not has_mapping else "",
                "x" if not has_ema_info else "",
            ])

    if not rows:
        print("All folders have all required files.")
        return

    col_widths = [max(len(h), max(len(r[i]) for r in rows)) for i, h in enumerate(headers)]
    header_line = "  ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
    sep_line = "  ".join("-" * col_widths[i] for i in range(len(headers)))

    print(header_line)
    print(sep_line)
    for row in rows:
        print("  ".join(row[i].ljust(col_widths[i]) for i in range(len(headers))))
    print(sep_line)
    print(f"{len(rows)} folders with missing files")


if __name__ == "__main__":
    find_missing_files()
