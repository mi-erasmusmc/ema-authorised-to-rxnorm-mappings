#!/usr/bin/env python3
"""
Download EMA medicines report and authorised presentations PDFs.

1. Downloads the medicines report Excel file from EMA
2. Converts it to TSV for processing
3. Loads document URLs and dates from EMA’s official bulk document index
4. Downloads missing/updated PDFs as <product_number>_<medicine_name>_<document_date>.pdf
   without requesting individual medicine pages.
"""

import argparse
import requests
import re
import csv
import time
import sys
import os
import subprocess
import math
from pathlib import Path
from datetime import datetime
from email.utils import parsedate_to_datetime
from zoneinfo import ZoneInfo
from urllib.parse import urlsplit
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
DOCUMENTS_URL = "https://www.ema.europa.eu/en/documents/report/documents-output-epar_documents_json-report_en.json"
DEFAULT_REQUEST_INTERVAL = 10
MAX_RATE_LIMIT_RETRIES = 3
MAX_RETRY_WAIT = 300


class EMARateLimitError(Exception):
    """Stop when a rate limit cannot be handled within the retry budget."""

    @classmethod
    def from_response(cls, response):
        retry_after = response.headers.get('Retry-After')
        detail = f'Retry-After: {retry_after}' if retry_after else 'No Retry-After header supplied'
        return cls(f'EMA returned HTTP 429 for {response.url}; {detail}. Stop and retry later.')


def positive_seconds(value):
    seconds = float(value)
    if not math.isfinite(seconds) or seconds <= 0:
        raise argparse.ArgumentTypeError('request interval must be a positive finite number')
    return seconds


def parse_retry_after(value):
    """Accept HTTP dates and numeric seconds, including EMA's decimal values."""
    if not value:
        return None
    try:
        seconds = float(value)
        return seconds if math.isfinite(seconds) and seconds >= 0 else None
    except ValueError:
        try:
            date = parsedate_to_datetime(value)
            if date.tzinfo is None:
                return None
            return max(0, date.timestamp() - time.time())
        except (ValueError, TypeError, OverflowError):
            return None


class PacedHTTPAdapter(HTTPAdapter):
    """Space every HTTP send, including redirects, across the shared session."""

    def __init__(self, request_interval, **kwargs):
        super().__init__(**kwargs)
        self.request_interval = positive_seconds(request_interval)
        self.last_response_at = None

    def send(self, request, **kwargs):
        interval = self.request_interval
        for attempt in range(MAX_RATE_LIMIT_RETRIES + 1):
            if self.last_response_at is not None:
                remaining = interval - (time.monotonic() - self.last_response_at)
                if remaining > 0:
                    print(f'Waiting {remaining:.1f}s before next EMA request...', flush=True)
                    time.sleep(remaining)
            try:
                response = super().send(request, **kwargs)
            finally:
                self.last_response_at = time.monotonic()
            if response.status_code != 429 or request.method not in ('GET', 'HEAD'):
                return response
            delay = parse_retry_after(response.headers.get('Retry-After'))
            if (delay is None or delay > MAX_RETRY_WAIT
                    or attempt == MAX_RATE_LIMIT_RETRIES):
                return response
            interval = max(self.request_interval, delay)
            print(f'EMA returned HTTP 429; Retry-After: {response.headers["Retry-After"]}. '
                  f'Retrying in at least {interval:g}s '
                  f'({attempt + 1}/{MAX_RATE_LIMIT_RETRIES}).', flush=True)
            response.close()


def get_session_with_retries(request_interval=DEFAULT_REQUEST_INTERVAL):
    """Create a paced session with bounded, server-directed HTTP 429 retries."""
    session = requests.Session()
    retry_strategy = Retry(
        total=0,
        respect_retry_after_header=False
    )
    adapter = PacedHTTPAdapter(request_interval, max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def download_excel_file(session, output_dir="."):
    """Download the EMA medicines report Excel file"""
    output_path = os.path.join(output_dir, EXCEL_FILENAME)
    print(f"Downloading Excel file from {EXCEL_URL}...")

    try:
        response = session.get(EXCEL_URL, timeout=60)
        if response.status_code == 429:
            raise EMARateLimitError.from_response(response)
        response.raise_for_status()

        temporary_path = output_path + '.part'
        with open(temporary_path, 'wb') as f:
            f.write(response.content)
        os.replace(temporary_path, output_path)

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
        df.to_csv(tsv_path + '.tmp', sep='\t', index=False, encoding='utf-8')
        os.replace(tsv_path + '.tmp', tsv_path)

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


def build_presentation_index(payload):
    """Index the official bulk feed by product, using document-specific dates."""
    if not isinstance(payload, dict) or not isinstance(payload.get('data'), list):
        raise ValueError('Invalid EMA document feed: expected a data list')
    records = payload['data']
    if payload.get('meta', {}).get('total_records') != len(records):
        raise ValueError('Incomplete EMA document feed: record count does not match metadata')
    index = {}
    for record in records:
        if record.get('type') != 'all-authorised-presentations':
            continue
        product = record.get('ema_product_number', '')
        if not re.fullmatch(r'EMEA/H/C/\d+', product):
            continue
        url = record.get('document_url', '')
        # EMA has valid English download URLs ending in .pdf-0. The feed's
        # language path, rather than a file extension, identifies English.
        if not urlsplit(url).path.startswith('/en/'):
            url = record.get('translations', {}).get('en', '')
        if not url:
            raise ValueError(f'No English presentation URL in document feed for {product}')
        revision = record.get('last_updated_date') or record.get('first_published_date')
        if not revision:
            raise ValueError(f'No presentation date in document feed for {product}')
        # The page dates used by existing filenames are Amsterdam calendar dates.
        timestamp = datetime.fromisoformat(revision.replace('Z', '+00:00'))
        if timestamp.tzinfo is not None:
            timestamp = timestamp.astimezone(ZoneInfo('Europe/Amsterdam'))
        document = dict(record, document_url=url, document_updated=revision,
                        date=timestamp.strftime('%Y-%m-%d'))
        previous = index.get(product)
        if previous is None or (document['date'], revision, url) > (
                previous['date'], previous['document_updated'], previous['document_url']):
            index[product] = document
    if not index:
        raise ValueError('EMA document feed contains no human authorised presentations')
    return index


def download_presentation_index(session):
    print(f'Downloading bulk document index from {DOCUMENTS_URL}...', flush=True)
    response = session.get(DOCUMENTS_URL, timeout=120)
    if response.status_code == 429:
        raise EMARateLimitError.from_response(response)
    response.raise_for_status()
    index = build_presentation_index(response.json())
    print(f'Indexed presentations for {len(index)} human products; no medicine-page requests needed.')
    return index


def is_complete_pdf(path):
    """Reject empty, truncated and non-PDF downloads before trusting a filename."""
    try:
        with open(path, 'rb') as f:
            if f.read(5) != b'%PDF-':
                return False
            f.seek(0, os.SEEK_END)
            f.seek(max(0, f.tell() - 1024))
            return b'%%EOF' in f.read()
    except OSError:
        return False


def download_pdf(pdf_url, output_path, session):
    """Publish only complete PDF downloads; preserve an existing file on failure."""
    try:
        response = session.get(pdf_url, timeout=60)
        if response.status_code == 429:
            raise EMARateLimitError.from_response(response)
        response.raise_for_status()
        temporary_path = str(output_path) + '.part'
        with open(temporary_path, 'wb') as f:
            f.write(response.content)
        if not is_complete_pdf(temporary_path):
            raise ValueError('Response is not a complete PDF')
        os.replace(temporary_path, output_path)
        return True
    except EMARateLimitError:
        raise
    except (requests.RequestException, OSError, ValueError) as error:
        print(f'Error downloading PDF {pdf_url}: {error}', file=sys.stderr)
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
    temporary_path = str(progress_file) + '.tmp'
    with open(temporary_path, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['ema_product_number', 'medicine_name', 'medicine_url', 'pdf_url',
                      'last_updated', 'pdf_filename', 'status', 'document_updated']
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(results)
    os.replace(temporary_path, progress_file)


def find_current_pdf(product_folder, product_number, document_date):
    """Accept a complete local PDF for this document date or a newer revision.

    The bulk feed is refreshed twice daily, so a newer local file can legitimately
    precede the feed. Medicine names can change without changing the document.
    """
    for path in sorted(Path(product_folder).glob(f'{product_number}_*.pdf'), reverse=True):
        match = re.search(r'_(\d{4}-\d{2}-\d{2})\.pdf$', path.name)
        if match and parse_date(match.group(1)) and match.group(1) >= document_date:
            if is_complete_pdf(path):
                return path
    return None


def process_medicines(df, output_dir=".", session=None, since_date=None, presentation_index=None,
                      dry_run=False):
    """Compare local PDFs with the bulk document feed and download missing revisions."""
    if session is None:
        session = get_session_with_retries()
    if presentation_index is None:
        presentation_index = download_presentation_index(session)
    required = {'EMA product number', 'Name of medicine', 'Medicine URL', 'Category'}
    if not required.issubset(df.columns):
        raise ValueError(f'Medicine report is missing required columns: {sorted(required - set(df.columns))}')
    products = df[df['Category'].str.strip().str.lower() == 'human'].drop_duplicates(
        subset=['EMA product number'])
    pdf_base_dir = Path(output_dir) / PDF_BASE_DIR
    progress_file = Path(output_dir) / PROGRESS_FILE
    results = load_progress(progress_file)
    pending = []
    current = absent = excluded = 0
    for _, row in products.iterrows():
        product = str(row['EMA product number']).strip()
        medicine_name = str(row['Name of medicine']).strip()
        medicine_url = str(row['Medicine URL']).strip()
        number = extract_product_number(product)
        document = presentation_index.get(product)
        record = dict(ema_product_number=product, medicine_name=medicine_name,
                      medicine_url=medicine_url, pdf_url='', last_updated='',
                      pdf_filename='', status='no_pdf_in_index', document_updated='')
        if document is None:
            absent += 1
            results[product] = record
            continue
        document_date = document['date']
        record.update(pdf_url=document['document_url'], last_updated=document_date,
                      document_updated=document['document_updated'])
        if since_date and parse_date(document_date) < since_date:
            excluded += 1
            continue
        folder = pdf_base_dir / number
        existing = find_current_pdf(folder, number, document_date)
        previous = results.get(product, {})
        previous_revision = previous.get('document_updated', '')
        if (existing and existing.name.endswith(f'_{document_date}.pdf')
                and previous.get('pdf_filename') == existing.name
                and previous_revision and previous_revision < document['document_updated']):
            # Filenames only carry a calendar date; saved timestamps also detect
            # a second publication on that same day once a baseline is known.
            existing = None
        if existing:
            current += 1
            record.update(pdf_filename=existing.name, status='success')
            results[product] = record
            continue
        filename = f'{number}_{sanitize_filename(medicine_name)}_{document_date}.pdf'
        # A queued target is not a completed revision. Preserve the last
        # completed timestamp until replacement succeeds, including same-day
        # updates whose target filename already exists.
        record.update(pdf_filename=filename, status='pending',
                      document_updated=previous_revision)
        results[product] = record
        pending.append((document_date, product, folder / filename, record))

    # Persist the complete queue before any download, so interruption loses no work.
    if not dry_run:
        save_progress(progress_file, list(results.values()))
    print(f'Local audit: {current} current, {len(pending)} missing/outdated, '
          f'{absent} with no PDF in the index, {excluded} excluded by --since.')
    if dry_run:
        print('Dry run: no PDFs downloaded and progress unchanged.')
        return dict(downloaded=0, failed=0, pending=len(pending), current=current)

    downloaded = failed = 0
    # Newest updates first; the product ID makes ties deterministic across restarts.
    pending.sort(key=lambda item: (item[0], item[1]), reverse=True)
    try:
        for _, product, pdf_path, record in pending:
            pdf_path.parent.mkdir(parents=True, exist_ok=True)
            if download_pdf(record['pdf_url'], pdf_path, session):
                record['status'] = 'success'
                record['document_updated'] = presentation_index[product]['document_updated']
                downloaded += 1
                print(f'  Downloaded: {pdf_path.name}', flush=True)
            else:
                record['status'] = 'download_failed'
                failed += 1
                print(f'  Failed: {product}', file=sys.stderr)
            save_progress(progress_file, list(results.values()))
    except (EMARateLimitError, KeyboardInterrupt):
        save_progress(progress_file, list(results.values()))
        raise
    remaining = len(pending) - downloaded
    print(f'Downloaded {downloaded} PDFs; {failed} failed; {remaining} still pending. '
          'Medicine pages requested: 0.')
    if remaining:
        print('Update incomplete: rerun to resume pending downloads.')
    else:
        print('All presentation PDFs listed in the index are up to date.')
    return dict(downloaded=downloaded, failed=failed, pending=remaining, current=current)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Download EMA medicines report and authorised presentations PDFs."
    )
    parser.add_argument(
        '--request-interval', type=positive_seconds, default=DEFAULT_REQUEST_INTERVAL,
        help=f'Minimum seconds between HTTP requests (default: {DEFAULT_REQUEST_INTERVAL})',
    )
    parser.add_argument(
        '--since',
        type=str,
        help='Only download presentation documents dated on or after this date (YYYY-MM-DD)'
    )
    parser.add_argument('--dry-run', action='store_true', help='Audit local PDFs without downloading them')
    args = parser.parse_args()
    # Parse the since date if provided
    since_date = None
    if args.since:
        since_date = parse_date(args.since)
        if not since_date:
            print(f"Error: Invalid date format '{args.since}'. Use YYYY-MM-DD.", file=sys.stderr)
            sys.exit(1)

    output_dir = EMA_DIR

    session = get_session_with_retries(request_interval=args.request_interval)

    excel_path = download_excel_file(session, output_dir)
    if not excel_path:
        print("Failed to download Excel file. Exiting.", file=sys.stderr)
        sys.exit(1)

    tsv_path, df = convert_excel_to_tsv(excel_path, output_dir)
    if df is None:
        print("Failed to convert Excel to TSV. Exiting.", file=sys.stderr)
        sys.exit(1)

    process_medicines(df, output_dir, session, since_date=since_date, dry_run=args.dry_run)


if __name__ == '__main__':
    try:
        main()
    except (EMARateLimitError, requests.RequestException, ValueError) as error:
        print(f"Update stopped: {error}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("Update interrupted; rerun to resume.", file=sys.stderr)
        sys.exit(1)
