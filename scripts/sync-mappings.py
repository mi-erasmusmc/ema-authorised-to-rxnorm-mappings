#!/usr/bin/env python3
"""
Sync mapping data between EMA and Latvia TSV files.
When ma_number = product_id and one has a value while the other is null,
update the product's mapping.tsv file with the non-null value.
"""

import csv
import sys
import subprocess
from pathlib import Path
from datetime import date
from typing import Dict, Optional, List

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

def find_product_mapping_file(base_path: Path, product_id: str, is_latvia: bool = False, ema_product_number: str = '') -> Optional[Path]:
    """Find the mapping.tsv file for a given product ID in the product folders."""
    # For EMA: data/ema/products/{product_number}/mapping.tsv (product_number from ema_product_number e.g. EMEA/H/C/000071 -> 000071)
    # For Latvia: data/latvia/products/{ingredient}/{brand_name}/mapping.tsv (need to search within files)

    if not is_latvia:
        # EMA: folder is named by the numeric product ID from ema_product_number
        folder_name = ema_product_number.rsplit('/', 1)[-1] if ema_product_number else ''
        if folder_name:
            mapping_file = base_path / folder_name / 'mapping.tsv'
            if mapping_file.exists():
                return mapping_file
        return None
    else:
        # Latvia: search through all mapping.tsv files to find one containing this product_id
        for mapping_file in base_path.rglob('*/*/mapping.tsv'):
            try:
                rows = read_tsv(mapping_file)
                for row in rows:
                    if row.get('product_id') == product_id:
                        return mapping_file
            except Exception:
                continue
        return None

def update_mapping_file(mapping_file: Path, product_id: str, updates: Dict[str, str], source: str):
    """Update a product's mapping.tsv file with new values."""
    if not mapping_file.exists():
        print(f"  ⚠️  Mapping file not found: {mapping_file}")
        return

    rows = read_tsv(mapping_file)
    if not rows:
        print(f"  ⚠️  No rows in mapping file: {mapping_file}")
        return

    # Get fieldnames from existing file
    with open(mapping_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        fieldnames = reader.fieldnames

    # Find the row matching the product_id (first column could be ma_number or product_id)
    id_field = fieldnames[0]  # 'ma_number' or 'product_id'

    updated = False
    for row in rows:
        if row.get(id_field) == product_id:
            changes = []
            for field, value in updates.items():
                if field in fieldnames and is_empty(row.get(field)) and not is_empty(value):
                    row[field] = value
                    changes.append(f"{field}={value}")
                    updated = True

            if changes:
                row['last_updated_date'] = str(date.today())
                print(f"  ✓ Updated {mapping_file.relative_to(Path.cwd())}")
                print(f"    {', '.join(changes)}")

    if updated:
        write_tsv(mapping_file, rows, fieldnames)

    return updated

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
    ema_products = workspace / 'data' / 'ema' / 'products'
    latvia_products = workspace / 'data' / 'latvia' / 'products'

    print("Reading TSV files...")
    ema_rows = read_tsv(ema_file)
    latvia_rows = read_tsv(latvia_file)

    # Create lookup dictionaries by ID
    ema_by_id = {row['ma_number']: row for row in ema_rows}
    latvia_by_id = {row['product_id']: row for row in latvia_rows}

    # Find common IDs - check both product_id and inter_code for Latvia
    print("Finding common products...")
    matches = []

    # Match EMA ma_number with Latvia product_id or inter_code
    for ema_id, ema_row in ema_by_id.items():
        # Check if EMA ma_number matches Latvia product_id
        if ema_id in latvia_by_id:
            matches.append((ema_id, ema_id, ema_row, latvia_by_id[ema_id]))
        else:
            # Check if EMA ma_number matches Latvia inter_code
            for latvia_id, latvia_row in latvia_by_id.items():
                if latvia_row.get('inter_code') == ema_id:
                    matches.append((ema_id, latvia_id, ema_row, latvia_row))
                    break

    print(f"Found {len(matches)} products in both EMA and Latvia files\n")

    if not matches:
        print("No common products found. Exiting.")
        return

    updates_count = 0

    for ema_id, latvia_id, ema_row, latvia_row in matches:
        # Check for fields to sync from Latvia to EMA
        ema_updates = {}
        for field in SYNC_FIELDS:
            ema_val = ema_row.get(field)
            latvia_val = latvia_row.get(field)

            if is_empty(ema_val) and not is_empty(latvia_val):
                ema_updates[field] = latvia_val

        # Check for fields to sync from EMA to Latvia
        latvia_updates = {}
        for field in SYNC_FIELDS:
            ema_val = ema_row.get(field)
            latvia_val = latvia_row.get(field)

            if is_empty(latvia_val) and not is_empty(ema_val):
                latvia_updates[field] = ema_val

        # Update EMA mapping file if needed
        if ema_updates:
            print(f"Product {ema_id}: Syncing from Latvia → EMA")
            ema_mapping_file = find_product_mapping_file(ema_products, ema_id, is_latvia=False, ema_product_number=ema_row.get('ema_product_number', ''))
            if ema_mapping_file:
                if update_mapping_file(ema_mapping_file, ema_id, ema_updates, 'Latvia'):
                    updates_count += 1
            else:
                print(f"  ⚠️  EMA product folder not found: {ema_id}")

        # Update Latvia mapping file if needed
        if latvia_updates:
            print(f"Product {latvia_id} (EMA: {ema_id}): Syncing from EMA → Latvia")
            latvia_mapping_file = find_product_mapping_file(latvia_products, latvia_id, is_latvia=True)
            if latvia_mapping_file:
                if update_mapping_file(latvia_mapping_file, latvia_id, latvia_updates, 'EMA'):
                    updates_count += 1
            else:
                print(f"  ⚠️  Latvia product folder not found: {latvia_id}")

    print(f"\n✓ Sync complete. Updated {updates_count} mapping files.")

if __name__ == '__main__':
    main()
