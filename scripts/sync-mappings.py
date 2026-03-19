#!/usr/bin/env python3
"""
Sync mapping data from EMA to Latvia TSV files.
EMA is the single source of truth: when ma_number matches a Latvia product_id or inter_code,
overwrite the Latvia mapping with the EMA values.
"""

import csv
import sys
import subprocess
from pathlib import Path
from datetime import date
from typing import Dict, List

# Fields to sync between EMA and Latvia
SYNC_FIELDS = ['concept_id', 'concept_name', 'concept_code', 'mapping_type', 'comment', 'suggestion']

def read_tsv(filepath: Path) -> List[Dict]:
    """Read TSV file into list of dictionaries."""
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        return list(reader)

def write_tsv(filepath: Path, rows: List[Dict], fieldnames: List[str]):
    """Write list of dictionaries to TSV file."""
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
        writer.writerows(rows)

def is_empty(value: Optional[str]) -> bool:
    """Check if a value is None or empty string."""
    return value is None or value == ''

def build_latvia_file_index(base_path: Path) -> Dict[str, Path]:
    """Scan all Latvia mapping files once and return {product_id: mapping_file} index."""
    index = {}
    for mapping_file in base_path.rglob('*/*/mapping.tsv'):
        try:
            rows = read_tsv(mapping_file)
            for row in rows:
                pid = row.get('product_id')
                if pid:
                    index[pid] = mapping_file
        except Exception:
            continue
    return index

def apply_updates_to_file(mapping_file: Path, updates_by_id: Dict[str, Dict[str, str]]):
    """Apply multiple product updates to a single mapping file in one read/write pass."""
    rows = read_tsv(mapping_file)
    if not rows:
        print(f"  ⚠️  No rows in mapping file: {mapping_file}")
        return 0

    with open(mapping_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        fieldnames = reader.fieldnames

    id_field = fieldnames[0]
    today = str(date.today())
    file_updated = False

    for row in rows:
        pid = row.get(id_field)
        if pid not in updates_by_id:
            continue
        updates = updates_by_id[pid]
        changes = []
        for field, value in updates.items():
            if field in fieldnames and not is_empty(value) and row.get(field) != value:
                row[field] = value
                changes.append(f"{field}={value}")
        if changes:
            row['last_updated_date'] = today
            print(f"  ✓ Updated {mapping_file.relative_to(Path.cwd())} [{pid}]")
            print(f"    {', '.join(changes)}")
            file_updated = True

    if file_updated:
        write_tsv(mapping_file, rows, fieldnames)
    return file_updated

def main():
    # Get git root directory
    try:
        git_root = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'],
                                          text=True).strip()
        workspace = Path(git_root)
    except subprocess.CalledProcessError:
        print("Error: Not in a git repository")
        sys.exit(1)

    ema_file = workspace / 'ema-to-rxnorm.tsv'
    latvia_file = workspace / 'latvia-to-rxnorm.tsv'
    latvia_products = workspace / 'data' / 'latvia' / 'products'

    print("Reading TSV files...")
    ema_rows = read_tsv(ema_file)
    latvia_rows = read_tsv(latvia_file)

    # Build lookup indexes
    ema_by_id = {row['ma_number']: row for row in ema_rows}
    latvia_by_id = {row['product_id']: row for row in latvia_rows}
    # Build inter_code -> product_id index to avoid O(N²) scan
    latvia_by_inter_code = {
        row['inter_code']: row['product_id']
        for row in latvia_rows
        if row.get('inter_code')
    }

    # Find common IDs - check both product_id and inter_code for Latvia
    print("Finding common products...")
    matches = []
    for ema_id, ema_row in ema_by_id.items():
        if ema_id in latvia_by_id:
            matches.append((ema_id, ema_id, ema_row, latvia_by_id[ema_id]))
        elif ema_id in latvia_by_inter_code:
            latvia_id = latvia_by_inter_code[ema_id]
            matches.append((ema_id, latvia_id, ema_row, latvia_by_id[latvia_id]))

    print(f"Found {len(matches)} products in both EMA and Latvia files")

    if not matches:
        print("No common products found. Exiting.")
        return

    # Build Latvia file index in one pass (instead of re-scanning per product)
    print("Indexing Latvia mapping files...")
    latvia_file_index = build_latvia_file_index(latvia_products)

    # Group updates by mapping file to minimise reads/writes
    updates_by_file: Dict[Path, Dict[str, Dict[str, str]]] = {}
    missing = []

    for ema_id, latvia_id, ema_row, latvia_row in matches:
        latvia_updates = {
            field: ema_row[field]
            for field in SYNC_FIELDS
            if not is_empty(ema_row.get(field))
        }
        if not latvia_updates:
            continue
        mapping_file = latvia_file_index.get(latvia_id)
        if not mapping_file:
            missing.append(latvia_id)
            continue
        updates_by_file.setdefault(mapping_file, {})[latvia_id] = latvia_updates

    print(f"\nApplying updates to {len(updates_by_file)} mapping file(s)...\n")
    updates_count = 0
    for mapping_file, updates_by_id in updates_by_file.items():
        if apply_updates_to_file(mapping_file, updates_by_id):
            updates_count += 1

    for latvia_id in missing:
        print(f"  ⚠️  Latvia product folder not found: {latvia_id}")

    print(f"\n✓ Sync complete. Updated {updates_count} mapping files.")

if __name__ == '__main__':
    main()
