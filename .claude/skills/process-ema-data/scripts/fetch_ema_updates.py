#!/usr/bin/env python3
"""Fetch new EMA data: detect latest PDF date, download updates, generate metadata.

Chains four steps into one command:
1. Find the most recent PDF date in products/
2. Download new/updated Authorised Presentations PDFs (--since that date)
3. Generate ema-info.txt metadata for any new product folders
4. Combine all parsed TSV files into overview files
"""

import argparse
import sys
import os

# Add scripts directory to path so we can import sibling modules
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GIT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(SCRIPT_DIR))))
sys.path.insert(0, SCRIPT_DIR)
sys.path.insert(0, os.path.join(GIT_ROOT, "scripts"))

from list_pdfs_by_date import extract_date_from_filename, EMA_DIR
from download_ema_presentation_files import (
    get_session_with_retries,
    download_excel_file,
    convert_excel_to_tsv,
    process_medicines,
    parse_date,
    EMA_DIR as DOWNLOAD_EMA_DIR,
)
from generate_ema_info import main as generate_ema_info_main
from generate_mapping_overviews import regenerate_ema
from pathlib import Path


def find_latest_pdf_date():
    """Find the most recent PDF date from filenames in products/."""
    pdf_dir = EMA_DIR / "products"
    if not pdf_dir.exists():
        return None

    latest = None
    for pdf_path in pdf_dir.rglob("*.pdf"):
        date = extract_date_from_filename(pdf_path.name)
        if date and (latest is None or date > latest):
            latest = date
    return latest


def main():
    parser = argparse.ArgumentParser(
        description="Fetch new EMA data: detect latest date, download updates, generate metadata."
    )
    parser.add_argument(
        "--since",
        type=str,
        help="Override auto-detected date cutoff (YYYY-MM-DD format)",
    )
    args = parser.parse_args()

    # Step 1: Determine the since date
    if args.since:
        since_str = args.since
        since_date = parse_date(since_str)
        if not since_date:
            print(f"Error: Invalid date format '{since_str}'. Use YYYY-MM-DD.", file=sys.stderr)
            sys.exit(1)
        print(f"Using provided date cutoff: {since_str}")
    else:
        since_str = find_latest_pdf_date()
        if since_str:
            since_date = parse_date(since_str)
            print(f"Auto-detected latest PDF date: {since_str}")
        else:
            since_date = None
            print("No existing PDFs found, downloading all.")

    # Step 2: Download new/updated PDFs
    output_dir = DOWNLOAD_EMA_DIR
    session = get_session_with_retries()

    excel_path = download_excel_file(session, output_dir)
    if not excel_path:
        print("Failed to download Excel file. Exiting.", file=sys.stderr)
        sys.exit(1)

    tsv_path, df = convert_excel_to_tsv(excel_path, output_dir)
    if df is None:
        print("Failed to convert Excel to TSV. Exiting.", file=sys.stderr)
        sys.exit(1)

    process_medicines(df, output_dir, session, since_date=since_date)

    # Step 3: Generate ema-info.txt metadata
    print("\nGenerating ema-info.txt files...")
    generate_ema_info_main()

    # Step 4: Combine all parsed TSV files into overview files
    print("\nCombining parsed data...")
    regenerate_ema()

    print("\nDone.")


if __name__ == "__main__":
    main()
