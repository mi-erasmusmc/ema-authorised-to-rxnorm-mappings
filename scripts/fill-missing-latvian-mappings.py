#!/usr/bin/env python3
"""
For a Latvia product folder, join data and mapping TSVs, group rows by
(original_name, strength, pharmaceutical_form, product_strength,
 REPLACE(package_en, package_size, ''))
and where one row is unmapped but another in the same group is mapped,
copy the mapping. If two rows in the same group have conflicting mappings,
print an error.
"""

import csv
import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import Dict, List, Optional


def read_tsv(filepath: Path) -> List[Dict]:
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        return list(reader)


def write_tsv(filepath: Path, rows: List[Dict], fieldnames: List[str]):
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='\t', extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)


def is_empty(value: Optional[str]) -> bool:
    return value is None or value.strip() == ''


def normalize_package(package_en: str, package_size: str) -> str:
    """REPLACE(package_en, package_size, '') — strip the package size number from the description."""
    if package_size:
        return package_en.replace(package_size, '')
    return package_en


def row_key(data_row: Dict) -> tuple:
    """Grouping key ignoring package size differences."""
    return (
        (data_row.get('original_name') or '').strip(),
        (data_row.get('strength') or '').strip(),
        (data_row.get('pharmaceutical_form') or '').strip(),
        (data_row.get('product_strength') or '').strip(),
        normalize_package(
            data_row.get('package_en') or '',
            data_row.get('package_size') or '',
        ),
    )


def find_data_tsv(folder: Path) -> Optional[Path]:
    candidates = sorted(folder.glob('data_*.tsv'))
    return candidates[-1] if candidates else None


def process_folder(folder: Path):
    folder = folder.resolve()

    data_file = find_data_tsv(folder)
    mapping_file = folder / 'mapping.tsv'

    if not data_file or not data_file.exists():
        print(f"No data TSV found in {folder}")
        return
    if not mapping_file.exists():
        print(f"No mapping.tsv found in {folder}")
        return

    data_rows = read_tsv(data_file)
    mapping_rows = read_tsv(mapping_file)

    # Build mapping lookup by product_id
    mapping_by_id: Dict[str, Dict] = {r['product_id']: r for r in mapping_rows}
    mapping_fieldnames = list(mapping_rows[0].keys()) if mapping_rows else [
        'product_id', 'concept_id', 'concept_name', 'concept_code',
        'mapping_type', 'comment', 'suggestion', 'last_updated_date'
    ]

    # Group data rows by normalized key
    groups: Dict[tuple, List[Dict]] = {}
    for data_row in data_rows:
        key = row_key(data_row)
        groups.setdefault(key, []).append(data_row)

    updated = False

    for key, group in groups.items():
        if len(group) < 2:
            continue  # Nothing to compare

        # Attach mapping info to each row in group
        annotated = []
        for data_row in group:
            pid = data_row['product_id']
            m = mapping_by_id.get(pid, {})
            annotated.append((pid, data_row, m))

        mapped = [(pid, d, m) for pid, d, m in annotated if not is_empty(m.get('concept_id'))]
        unmapped = [(pid, d, m) for pid, d, m in annotated if is_empty(m.get('concept_id'))]

        if not unmapped:
            continue  # All mapped — check for conflicts among mapped
        if not mapped:
            continue  # None mapped — nothing to copy

        # Check for conflicts among the mapped rows
        concept_ids = {m.get('concept_id') for _, _, m in mapped}
        if len(concept_ids) > 1:
            print(f"\n❌ CONFLICT in {folder.name}:")
            for pid, _, m in mapped:
                print(f"   {pid}: {m.get('concept_id')} — {m.get('concept_name')}")
            print(f"   Key: {key}")
            continue

        # Single consistent mapping — copy to unmapped rows
        source_pid, _, source_mapping = mapped[0]
        fields_to_copy = ['concept_id', 'concept_name', 'concept_code', 'mapping_type', 'comment', 'suggestion']

        for pid, _, _ in unmapped:
            if pid not in mapping_by_id:
                mapping_by_id[pid] = {'product_id': pid}
            target = mapping_by_id[pid]
            for f in fields_to_copy:
                if not is_empty(source_mapping.get(f)):
                    target[f] = source_mapping[f]
            target['last_updated_date'] = str(date.today())
            print(f"  ✓ {pid} ← {source_pid}: {source_mapping.get('concept_name')}")
            updated = True

    if updated:
        # Rebuild mapping rows in original order, adding any new entries
        seen = set()
        out_rows = []
        for m in mapping_rows:
            pid = m['product_id']
            seen.add(pid)
            out_rows.append(mapping_by_id.get(pid, m))
        # Add any product_ids that were in data but not in original mapping
        for data_row in data_rows:
            pid = data_row['product_id']
            if pid not in seen and pid in mapping_by_id:
                out_rows.append(mapping_by_id[pid])
        write_tsv(mapping_file, out_rows, mapping_fieldnames)
        print(f"\n✓ Wrote {mapping_file}")


def get_git_root() -> Path:
    try:
        root = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], text=True).strip()
        return Path(root)
    except subprocess.CalledProcessError:
        print("Error: Not in a git repository")
        sys.exit(1)


def main():
    if len(sys.argv) >= 2:
        folders = [Path(arg) for arg in sys.argv[1:]]
    else:
        git_root = get_git_root()
        latvia_products = git_root / 'data' / 'latvia' / 'products'
        folders = sorted(latvia_products.glob('*/*/'))

    for folder in folders:
        if not folder.is_dir():
            print(f"Not a directory: {folder}")
            continue
        process_folder(folder)


if __name__ == '__main__':
    main()
