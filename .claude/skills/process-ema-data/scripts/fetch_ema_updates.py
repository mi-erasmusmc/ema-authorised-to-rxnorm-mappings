#!/usr/bin/env python3
"""Fetch new EMA data: check local PDFs, download updates, generate metadata.

Chains four steps into one command:
1. Compare each product's local PDFs with EMA's bulk document index
2. Download missing/updated Authorised Presentations PDFs
3. Generate ema-info.txt metadata for any new product folders
4. Combine all parsed TSV files into overview files
"""

import argparse
import sys
import os
import requests

# Add scripts directory to path so we can import sibling modules
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GIT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(SCRIPT_DIR))))
sys.path.insert(0, SCRIPT_DIR)
sys.path.insert(0, os.path.join(GIT_ROOT, "scripts"))

from download_ema_presentation_files import (
    DEFAULT_REQUEST_INTERVAL,
    positive_seconds,
    EMARateLimitError,
    get_session_with_retries,
    download_excel_file,
    convert_excel_to_tsv,
    process_medicines,
    parse_date,
    EMA_DIR as DOWNLOAD_EMA_DIR,
)
from generate_ema_info import main as generate_ema_info_main
from generate_mapping_overviews import regenerate_ema


def main():
    parser = argparse.ArgumentParser(
        description="Fetch new EMA data: check local PDFs, download updates, generate metadata."
    )
    parser.add_argument(
        "--since",
        type=str,
        help="Only download presentation documents dated on or after this date (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--request-interval", type=positive_seconds, default=DEFAULT_REQUEST_INTERVAL,
        help=f"Minimum seconds between HTTP requests (default: {DEFAULT_REQUEST_INTERVAL})",
    )
    parser.add_argument("--dry-run", action="store_true", help="Audit local PDFs without downloading them")
    args = parser.parse_args()

    # Step 1: Apply a date cutoff only when explicitly requested
    if args.since:
        since_str = args.since
        since_date = parse_date(since_str)
        if not since_date:
            print(f"Error: Invalid date format '{since_str}'. Use YYYY-MM-DD.", file=sys.stderr)
            sys.exit(1)
        print(f"Using provided date cutoff: {since_str}")
    else:
        since_date = None
        print("Checking local PDFs against EMA’s bulk document index.")

    # Step 2: Download new/updated PDFs
    output_dir = DOWNLOAD_EMA_DIR
    session = get_session_with_retries(request_interval=args.request_interval)

    excel_path = download_excel_file(session, output_dir)
    if not excel_path:
        print("Failed to download Excel file. Exiting.", file=sys.stderr)
        sys.exit(1)

    tsv_path, df = convert_excel_to_tsv(excel_path, output_dir)
    if df is None:
        print("Failed to convert Excel to TSV. Exiting.", file=sys.stderr)
        sys.exit(1)

    result = process_medicines(df, output_dir, session, since_date=since_date,
                               dry_run=args.dry_run)
    if args.dry_run:
        return

    # Step 3: Generate ema-info.txt metadata
    print("\nGenerating ema-info.txt files...")
    generate_ema_info_main()

    # Step 4: Combine all parsed TSV files into overview files
    print("\nCombining parsed data...")
    regenerate_ema()

    print(f"\nUpdate pass finished; {result['pending']} PDF downloads remain pending.")
    if result["failed"]:
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except (EMARateLimitError, requests.RequestException, ValueError) as error:
        print(f"Update stopped: {error}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("Update interrupted; rerun to resume.", file=sys.stderr)
        sys.exit(1)
