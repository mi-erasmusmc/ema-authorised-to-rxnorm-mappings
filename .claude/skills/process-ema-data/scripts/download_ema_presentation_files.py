#!/usr/bin/env python3
"""
Download EMA medicines report and authorised presentations PDFs.

1. Downloads the medicines report Excel file from EMA
2. Converts it to TSV for processing
3. Creates folders for each EMA product number
4. Downloads Authorised Presentations PDFs with naming: emaprodcutnumber_name-of-medicine_date_last_updated.pdf
   (date is from the Authorised Presentations section on the medicine page)
"""

import argparse
import requests
import re
import csv
import time
import sys
import os
import subprocess
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

try:
    import pandas as pd
except ImportError:
    print("pandas is required. Install with: pip install pandas openpyxl")
    sys.exit(1)


def _gitroot():
    return subprocess.check_output(
        ["git", "rev-parse", "--show-toplevel"], text=True
    ).strip()


# Constants
EXCEL_URL = "https://www.ema.europa.eu/en/documents/report/medicines-output-medicines-report_en.xlsx"
GIT_ROOT = _gitroot()
EMA_DIR = os.path.join(GIT_ROOT, "data", "ema")
EXCEL_FILENAME = "medicines_output_medicines_report_en.xlsx"
TSV_FILENAME = "medicines_report.tsv"
PDF_BASE_DIR = "products"
PROGRESS_FILE = "download_progress.csv"


def get_session_with_retries():
    """Create a requests session with retry logic"""
    session = requests.Session()
    retry_strategy = Retry(
        total=5,
        backoff_factor=2,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        respect_retry_after_header=False
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def download_excel_file(session, output_dir="."):
    """Download the EMA medicines report Excel file"""
    output_path = os.path.join(output_dir, EXCEL_FILENAME)
    print(f"Downloading Excel file from {EXCEL_URL}...")

    try:
        response = session.get(EXCEL_URL, timeout=60)
        response.raise_for_status()

        with open(output_path, 'wb') as f:
            f.write(response.content)

        print(f"Downloaded: {output_path}")
        return output_path
    except Exception as e:
        print(f"Error downloading Excel file: {e}", file=sys.stderr)
        return None


def convert_excel_to_tsv(excel_path, output_dir="."):
    """Convert EMA Excel file to TSV format"""
    tsv_path = os.path.join(output_dir, TSV_FILENAME)
    print(f"Converting Excel to TSV...")

    try:
        # Read Excel with row 8 (0-indexed) as header
        df = pd.read_excel(excel_path, header=8)

        # Clean column names (remove newlines, strip whitespace)
        df.columns = [str(col).strip().replace('\n', ' ') if pd.notna(col) else f'Column_{i}'
                      for i, col in enumerate(df.columns)]

        print(f"Columns found: {list(df.columns)}")

        # Sort by EMA product number for stable diffs
        if 'EMA product number' in df.columns:
            df = df.sort_values('EMA product number', ignore_index=True)

        # Write to TSV
        df.to_csv(tsv_path, sep='\t', index=False, encoding='utf-8')

        print(f"Converted to TSV: {tsv_path}")
        print(f"Total records: {len(df)}")
        return tsv_path, df
    except Exception as e:
        print(f"Error converting Excel to TSV: {e}", file=sys.stderr)
        return None, None


def sanitize_filename(name):
    """Sanitize a string to be safe for use in filenames"""
    # Replace spaces and special characters with underscores
    name = re.sub(r'[^\w\-]', '_', name)
    # Remove consecutive underscores
    name = re.sub(r'_+', '_', name)
    # Remove leading/trailing underscores
    name = name.strip('_')
    return name.lower()


def extract_product_number(ema_product_number):
    """Extract the numeric product number from EMA product number (e.g., 'EMEA/H/C/003970' -> '003970')"""
    # Remove EMEA/H/C/ or similar prefixes
    match = re.search(r'EMEA/[HV]/C/(\d+)', ema_product_number, re.IGNORECASE)
    if match:
        return match.group(1)
    # Fallback: just sanitize the whole thing
    return sanitize_filename(ema_product_number)


def parse_date(date_str):
    """Parse a date string and return a datetime object, or None if parsing fails"""
    if not date_str:
        return None

    # Try different date formats
    date_formats = [
        "%d/%m/%Y",  # 14/01/2026
        "%Y-%m-%d",  # 2026-01-14
        "%d-%m-%Y",  # 14-01-2026
    ]

    for fmt in date_formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue

    return None


def format_date_for_filename(date_str):
    """Format a date string for use in filename (YYYY-MM-DD format)"""
    dt = parse_date(date_str)
    if dt:
        return dt.strftime("%Y-%m-%d")
    # If all parsing fails, sanitize the original string
    return sanitize_filename(date_str) if date_str else "unknown_date"


def get_authorised_presentations_pdf_and_date(page_url, session):
    """
    Fetch a medicine page and extract:
    - The Authorised Presentations PDF link
    - The Last updated date for the Authorised Presentations section
    """
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = session.get(page_url, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            pdf_link = None
            last_updated = None

            # Find all links that might be authorised presentations PDFs
            # Collect all candidates, then prefer English version
            pdf_candidates = []
            for link in soup.find_all('a', href=True):
                href = link['href']

                # Look for authorised-presentations PDF
                if 'authorised-presentations' in href and href.endswith('.pdf'):
                    pdf_candidates.append((link, href))

            # Prefer English version (_en.pdf), otherwise take first available
            pdf_link = None
            selected_link = None
            for link, href in pdf_candidates:
                if href.endswith('_en.pdf'):
                    pdf_link = urljoin(page_url, href)
                    selected_link = link
                    break

            # Fallback to first candidate if no English version found
            if not pdf_link and pdf_candidates:
                selected_link, href = pdf_candidates[0]
                pdf_link = urljoin(page_url, href)

            if pdf_link and selected_link:
                # Try to find the last updated date near this link
                # Walk up parent elements to find date information
                for parent in selected_link.parents:
                    if parent.name in ['div', 'li', 'article', 'section', 'details']:
                        text = parent.get_text()
                        # Look for "Last updated: DD/MM/YYYY" pattern, fallback to "First published"
                        date_match = re.search(r'Last updated[:\s]+(\d{1,2}/\d{1,2}/\d{4})', text)
                        if date_match:
                            last_updated = date_match.group(1)
                            break
                        date_match = re.search(r'First published[:\s]+(\d{1,2}/\d{1,2}/\d{4})', text)
                        if date_match:
                            last_updated = date_match.group(1)
                            break

            # If we didn't find date near the link, search page text for authorised presentations context
            if pdf_link and not last_updated:
                page_text = soup.get_text()
                # Look for last updated specifically in Authorised presentations context, fallback to First published
                patterns = [
                    r'[Aa]uthorised presentations.*?Last updated[:\s]+(\d{1,2}/\d{1,2}/\d{4})',
                    r'[Aa]ll [Aa]uthorised presentations.*?Last updated[:\s]+(\d{1,2}/\d{1,2}/\d{4})',
                    r'[Aa]uthorised presentations.*?First published[:\s]+(\d{1,2}/\d{1,2}/\d{4})',
                    r'[Aa]ll [Aa]uthorised presentations.*?First published[:\s]+(\d{1,2}/\d{1,2}/\d{4})',
                ]
                for pattern in patterns:
                    match = re.search(pattern, page_text, re.IGNORECASE | re.DOTALL)
                    if match:
                        last_updated = match.group(1)
                        break

            return pdf_link, last_updated

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                wait_time = (attempt + 1) * 10
                print(f"Rate limited, waiting {wait_time}s...", end=' ')
                time.sleep(wait_time)
                continue
            else:
                print(f"HTTP error: {e}", file=sys.stderr)
                return None, None
        except Exception as e:
            print(f"Error fetching page {page_url}: {e}", file=sys.stderr)
            return None, None

    print(f"Failed after {max_retries} retries", file=sys.stderr)
    return None, None


def download_pdf(pdf_url, output_path, session):
    """Download a PDF file to the specified path"""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = session.get(pdf_url, timeout=60)
            response.raise_for_status()

            with open(output_path, 'wb') as f:
                f.write(response.content)

            return True
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                wait_time = (attempt + 1) * 10
                print(f"Rate limited on PDF, waiting {wait_time}s...", end=' ')
                time.sleep(wait_time)
                continue
            else:
                print(f"HTTP error downloading PDF: {e}", file=sys.stderr)
                return False
        except Exception as e:
            print(f"Error downloading PDF {pdf_url}: {e}", file=sys.stderr)
            return False

    return False


def load_progress(progress_file):
    """Load already processed items from progress file"""
    processed = {}
    if os.path.exists(progress_file):
        with open(progress_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                processed[row['ema_product_number']] = row
    return processed


def save_progress(progress_file, results):
    """Save current progress to file"""
    if not results:
        return
    with open(progress_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['ema_product_number', 'medicine_name', 'medicine_url', 'pdf_url',
                      'last_updated', 'pdf_filename', 'status']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)


def process_medicines(df, output_dir=".", session=None, since_date=None):
    """Process medicines from dataframe: create folders and download PDFs

    Args:
        df: DataFrame with medicine data
        output_dir: Directory for output files
        session: requests session
        since_date: Only download files updated on or after this date (datetime object)
    """
    if session is None:
        session = get_session_with_retries()

    if since_date:
        print(f"Filtering to files updated on or after: {since_date.strftime('%Y-%m-%d')}")

    pdf_base_dir = os.path.join(output_dir, PDF_BASE_DIR)
    progress_file = os.path.join(output_dir, PROGRESS_FILE)

    # Create base directory
    if not os.path.exists(pdf_base_dir):
        os.makedirs(pdf_base_dir)
        print(f"Created directory: {pdf_base_dir}")

    # Load existing progress
    results_dict = load_progress(progress_file)

    # Get unique EMA product numbers (to avoid processing the same product multiple times)
    # Column names may vary, so we try to find the right columns
    product_col = None
    name_col = None
    url_col = None
    category_col = None
    first_published_col = None
    last_updated_col = None

    for col in df.columns:
        col_lower = col.lower()
        if 'ema product number' in col_lower:
            product_col = col
        elif 'name of medicine' in col_lower:
            name_col = col
        elif 'medicine url' in col_lower:
            url_col = col
        elif col_lower == 'category':
            category_col = col
        elif 'first published' in col_lower:
            first_published_col = col
        elif 'last updated' in col_lower:
            last_updated_col = col

    if not all([product_col, name_col, url_col]):
        print(f"Error: Could not find required columns.", file=sys.stderr)
        print(f"Available columns: {list(df.columns)}", file=sys.stderr)
        return

    # Filter to only Human medicines
    if category_col:
        df_filtered = df[df[category_col].str.strip().str.lower() == 'human']
        print(f"Filtered to Human medicines: {len(df_filtered)} records (from {len(df)} total)")
    else:
        print("Warning: Category column not found, processing all medicines")
        df_filtered = df

    # Get unique products
    unique_products = df_filtered.drop_duplicates(subset=[product_col])

    # Pre-filter by date if since_date is provided and date columns exist
    if since_date and (first_published_col or last_updated_col):
        def is_recent(row):
            """Check if row has any date on or after since_date"""
            for col in [first_published_col, last_updated_col]:
                if col and pd.notna(row.get(col)):
                    dt = parse_date(str(row[col]))
                    if dt and dt >= since_date:
                        return True
            return False

        before_filter = len(unique_products)
        unique_products = unique_products[unique_products.apply(is_recent, axis=1)]
        after_filter = len(unique_products)
        print(f"Filtered by date (>= {since_date.strftime('%Y-%m-%d')}): {after_filter} products (skipped {before_filter - after_filter} older products)")

    total = len(unique_products)
    already_processed = len(results_dict)

    print(f"Processing {total} unique products (already completed: {already_processed})...")
    print(f"PDFs will be saved to: {pdf_base_dir}/")

    skipped_count = 0
    downloaded_count = 0
    no_pdf_count = 0
    failed_count = 0

    try:
        for idx, (_, row) in enumerate(unique_products.iterrows(), 1):
            ema_product_number = str(row[product_col]).strip()
            medicine_name = str(row[name_col]).strip()
            medicine_url = str(row[url_col]).strip()

            # Skip if already processed
            if ema_product_number in results_dict:
                skipped_count += 1
                continue

            # Create folder for this product
            folder_name = extract_product_number(ema_product_number)
            product_folder = os.path.join(pdf_base_dir, folder_name)
            if not os.path.exists(product_folder):
                os.makedirs(product_folder)

            # Get PDF link and last updated date from the product page
            pdf_url, last_updated = get_authorised_presentations_pdf_and_date(medicine_url, session)

            if not pdf_url:
                print(f"  No PDF: {medicine_name} ({ema_product_number})")
                no_pdf_count += 1
                results_dict[ema_product_number] = {
                    'ema_product_number': ema_product_number,
                    'medicine_name': medicine_name,
                    'medicine_url': medicine_url,
                    'pdf_url': '',
                    'last_updated': '',
                    'pdf_filename': '',
                    'status': 'no_pdf_found'
                }
            elif since_date and last_updated:
                # Check if the file was updated before the cutoff date
                file_date = parse_date(last_updated)
                if file_date and file_date < since_date:
                    skipped_count += 1
                    results_dict[ema_product_number] = {
                        'ema_product_number': ema_product_number,
                        'medicine_name': medicine_name,
                        'medicine_url': medicine_url,
                        'pdf_url': pdf_url,
                        'last_updated': last_updated,
                        'pdf_filename': '',
                        'status': 'skipped_before_date'
                    }
                    time.sleep(2)  # Still be nice to server even when skipping
                    continue
            if pdf_url:
                # Format the PDF filename
                sanitized_product = extract_product_number(ema_product_number)
                sanitized_name = sanitize_filename(medicine_name)
                formatted_date = format_date_for_filename(last_updated) if last_updated else "unknown_date"

                pdf_filename = f"{sanitized_product}_{sanitized_name}_{formatted_date}.pdf"
                pdf_path = os.path.join(product_folder, pdf_filename)

                # Download the PDF
                success = download_pdf(pdf_url, pdf_path, session)

                if success:
                    downloaded_count += 1
                    print(f"  Downloaded: {pdf_filename}")
                    results_dict[ema_product_number] = {
                        'ema_product_number': ema_product_number,
                        'medicine_name': medicine_name,
                        'medicine_url': medicine_url,
                        'pdf_url': pdf_url,
                        'last_updated': last_updated or '',
                        'pdf_filename': pdf_filename,
                        'status': 'success'
                    }
                else:
                    failed_count += 1
                    print(f"  Failed: {medicine_name} ({ema_product_number})")
                    results_dict[ema_product_number] = {
                        'ema_product_number': ema_product_number,
                        'medicine_name': medicine_name,
                        'medicine_url': medicine_url,
                        'pdf_url': pdf_url,
                        'last_updated': last_updated or '',
                        'pdf_filename': '',
                        'status': 'download_failed'
                    }

            # Save progress every 10 items
            if idx % 10 == 0:
                save_progress(progress_file, list(results_dict.values()))

            # Be nice to the server - delay between requests
            time.sleep(5)

    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Saving progress...")
        save_progress(progress_file, list(results_dict.values()))
        print(f"Progress saved to {progress_file}")
        sys.exit(1)

    # Save final progress
    save_progress(progress_file, list(results_dict.values()))

    # Print compact summary
    parts = [f"Downloaded {downloaded_count} new PDFs"]
    parts.append(f"{total} products checked")
    if skipped_count:
        parts.append(f"{skipped_count} skipped")
    if no_pdf_count:
        parts.append(f"{no_pdf_count} no PDF")
    if failed_count:
        parts.append(f"{failed_count} failed")
    print(f"\n{parts[0]} ({', '.join(parts[1:])})")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Download EMA medicines report and authorised presentations PDFs."
    )
    parser.add_argument(
        '--since',
        type=str,
        help='Only download files updated on or after this date (YYYY-MM-DD format)'
    )
    args = parser.parse_args()

    # Parse the since date if provided
    since_date = None
    if args.since:
        since_date = parse_date(args.since)
        if not since_date:
            print(f"Error: Invalid date format '{args.since}'. Use YYYY-MM-DD.", file=sys.stderr)
            sys.exit(1)

    output_dir = EMA_DIR

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


if __name__ == '__main__':
    main()
