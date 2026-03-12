#!/usr/bin/env python3
"""
Audit a Spain product folder and report what needs mapping work.

Usage:
    python3 .claude/skills/map-spain-drugs/audit_folder.py data/spain/products/<folder>/

Output (tab-separated rows grouped by issue type):
    MISSING     - cod_nacion in data.tsv with no row in mapping.tsv
    NO_TYPE     - mapping row with empty mapping_type
    NO_CONCEPT  - mapping row with empty concept_id
    BROAD       - mapping row with mapping_type=BROAD (for review)
"""

import csv
import sys
from pathlib import Path


def load_tsv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <product-folder>", file=sys.stderr)
        sys.exit(1)

    folder = Path(sys.argv[1])
    data_path = folder / "data.tsv"
    mapping_path = folder / "mapping.tsv"

    if not data_path.exists():
        print(f"ERROR: {data_path} not found", file=sys.stderr)
        sys.exit(1)

    data_rows = load_tsv(data_path)
    data_by_cod = {r["cod_nacion"]: r for r in data_rows}

    mapped_cods = set()
    mapping_rows = []
    if mapping_path.exists():
        mapping_rows = load_tsv(mapping_path)
        mapped_cods = {r["cod_nacion"] for r in mapping_rows}

    issues = []

    # MISSING: in data.tsv but not in mapping.tsv
    for cod, row in data_by_cod.items():
        if cod not in mapped_cods:
            issues.append(("MISSING", cod, row["nro_definitivo"], row["des_dcp"], "", "", ""))

    # NO_TYPE / NO_CONCEPT / BROAD: issues in existing mapping rows
    for row in mapping_rows:
        cod = row["cod_nacion"]
        data_row = data_by_cod.get(cod, {})
        des_dcp = data_row.get("des_dcp", "")
        concept = row.get("concept_name", "")
        mapping_type = row.get("mapping_type", "").strip()
        concept_id = row.get("concept_id", "").strip()

        if not concept_id:
            issues.append(("NO_CONCEPT", cod, row["nro_definitivo"], des_dcp, concept_id, concept, mapping_type))
        elif not mapping_type:
            issues.append(("NO_TYPE", cod, row["nro_definitivo"], des_dcp, concept_id, concept, mapping_type))
        elif mapping_type == "BROAD":
            issues.append(("BROAD", cod, row["nro_definitivo"], des_dcp, concept_id, concept, mapping_type))

    if not issues:
        print("OK - no issues found")
        return

    # Print summary
    from collections import Counter
    counts = Counter(i[0] for i in issues)
    summary_parts = [f"{v} {k}" for k, v in sorted(counts.items())]
    print(f"# {folder.name}: {', '.join(summary_parts)}")
    print()

    # Print issues grouped by type
    header = ["issue", "cod_nacion", "nro_definitivo", "des_dcp", "concept_id", "concept_name", "mapping_type"]
    print("\t".join(header))
    for issue in sorted(issues, key=lambda x: (x[0], x[1])):
        print("\t".join(issue))


if __name__ == "__main__":
    main()
