#!/usr/bin/env python3
"""List PDFs in products sorted by the date in the filename, newest first."""

import re
import subprocess
from pathlib import Path


def _gitroot():
    return Path(subprocess.check_output(
        ["git", "rev-parse", "--show-toplevel"], text=True
    ).strip())


GIT_ROOT = _gitroot()
EMA_DIR = GIT_ROOT / "data" / "ema"


def extract_date_from_filename(filename):
    """Extract YYYY-MM-DD date from end of filename."""
    match = re.search(r'(\d{4}-\d{2}-\d{2})\.pdf$', filename)
    return match.group(1) if match else None


def list_pdfs_by_date():
    pdf_dir = EMA_DIR / "products"

    if not pdf_dir.exists():
        print(f"Directory not found: {pdf_dir}")
        return

    pdfs_with_dates = []

    for pdf_path in pdf_dir.rglob("*.pdf"):
        date = extract_date_from_filename(pdf_path.name)
        if date:
            pdfs_with_dates.append((date, pdf_path))

    # Sort by date descending (newest first)
    pdfs_with_dates.sort(key=lambda x: x[0], reverse=True)

    for date, pdf_path in pdfs_with_dates:
        print(f"{date}  {pdf_path.name}")


if __name__ == "__main__":
    list_pdfs_by_date()
