#!/usr/bin/env python3
"""
Audit a Spain product folder and report what needs mapping work.

Usage:
    python3 .claude/skills/map-spain-drugs/audit_folder.py data/spain/products/<folder>/
    python3 .claude/skills/map-spain-drugs/audit_folder.py data/spain/products/<folder>/ --details
    python3 .claude/skills/map-spain-drugs/audit_folder.py data/spain/products/<folder>/ --details --issue MISSING

Default output is summary-first:
    - one summary line with issue counts
    - grouped pattern counts by issue type

Use --details to print tab-separated rows grouped by issue type.
Use --issue to limit details to one issue type when drilling down.

Issue types:
    MISSING           - cod_nacion in data.tsv with no row in mapping.tsv
    NO_TYPE           - mapping row with empty mapping_type
    NO_CONCEPT        - mapping row with empty concept_id
    BROAD             - mapping row with mapping_type=BROAD (for review)
    STALE_MAPPING     - mapping row whose cod_nacion no longer exists in data.tsv
    NRO_MISMATCH      - mapping row whose nro_definitivo disagrees with data.tsv
    DUPLICATE_DATA    - duplicate cod_nacion in data.tsv
    DUPLICATE_MAPPING - duplicate cod_nacion in mapping.tsv
    REVIEW_VOLUME     - likely single-use injectable mapped to a concentration-only concept
"""

import argparse
import csv
import re
import sys
from collections import Counter
from pathlib import Path

DETAIL_HEADER = [
    "issue",
    "cod_nacion",
    "nro_definitivo",
    "des_dcp",
    "concept_id",
    "concept_name",
    "mapping_type",
]


def load_tsv(path):
    with open(path, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def clean(value):
    if value is None:
        return ""
    return str(value).strip()


def duplicate_values(rows, key):
    counts = Counter(clean(row.get(key, "")) for row in rows if clean(row.get(key, "")))
    return sorted(value for value, count in counts.items() if count > 1)


def extract_ml(text):
    match = re.search(r"(\d+(?:[.,]\d+)?)\s*ml\b", text, flags=re.IGNORECASE)
    if not match:
        return None
    return match.group(1).replace(",", ".")


def needs_volume_review(data_row, concept_name):
    des_dcp = clean(data_row.get("des_dcp", ""))
    unit = clean(data_row.get("unidad_contenido", "")).lower()
    form = clean(data_row.get("forma_farmaceutica", "")).lower()
    volume = extract_ml(des_dcp)
    if not volume:
        return False
    if "inye" not in unit and "inyect" not in form:
        return False
    concept_lower = clean(concept_name).lower()
    if "injection" not in concept_lower:
        return False
    if "mg/ml" not in concept_lower:
        return False
    return not concept_lower.startswith(f"{volume} ml ")


def make_issue(issue, cod, nro_definitivo, des_dcp, concept_id, concept_name, mapping_type):
    return {
        "issue": clean(issue),
        "cod_nacion": clean(cod),
        "nro_definitivo": clean(nro_definitivo),
        "des_dcp": clean(des_dcp),
        "concept_id": clean(concept_id),
        "concept_name": clean(concept_name),
        "mapping_type": clean(mapping_type),
    }


def print_summary(folder_name, issues):
    counts = Counter(issue["issue"] for issue in issues)
    summary_parts = [f"{count} {issue}" for issue, count in sorted(counts.items())]
    print(f"# {folder_name}: {', '.join(summary_parts)}")
    print()

    grouped = {}
    for issue in issues:
        issue_type = issue["issue"]
        label = issue["des_dcp"] or issue["concept_name"] or issue["cod_nacion"]
        grouped.setdefault(issue_type, Counter())[label] += 1

    for issue_type in sorted(grouped):
        print(f"[{issue_type}]")
        for label, count in grouped[issue_type].most_common():
            print(f"{count}\t{label}")
        print()


def print_details(issues, issue_filter=None):
    filtered = [
        issue for issue in issues
        if issue_filter is None or issue["issue"] == issue_filter
    ]
    if not filtered:
        if issue_filter:
            print(f"OK - no {issue_filter} issues found")
        else:
            print("OK - no issues found")
        return

    print("\t".join(DETAIL_HEADER))
    for issue in sorted(filtered, key=lambda item: (item["issue"], item["cod_nacion"])):
        print("\t".join(issue[column] for column in DETAIL_HEADER))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help="Spain product folder to audit")
    parser.add_argument(
        "--details",
        action="store_true",
        help="Print row-level TSV instead of summary-first output",
    )
    parser.add_argument(
        "--issue",
        help="Limit --details output to one issue type such as MISSING or BROAD",
    )
    args = parser.parse_args()
    if args.issue:
        args.issue = args.issue.strip().upper()
    return args


def main():
    args = parse_args()
    folder = Path(args.folder)
    data_path = folder / "data.tsv"
    mapping_path = folder / "mapping.tsv"

    if not data_path.exists():
        print(f"ERROR: {data_path} not found", file=sys.stderr)
        sys.exit(1)

    data_rows = load_tsv(data_path)
    data_by_cod = {clean(row["cod_nacion"]): row for row in data_rows}
    duplicate_data_cods = duplicate_values(data_rows, "cod_nacion")

    mapped_cods = set()
    mapping_rows = []
    if mapping_path.exists():
        mapping_rows = load_tsv(mapping_path)
        mapped_cods = {clean(row.get("cod_nacion", "")) for row in mapping_rows}
    duplicate_mapping_cods = duplicate_values(mapping_rows, "cod_nacion")

    issues = []

    for cod in duplicate_data_cods:
        issues.append(make_issue("DUPLICATE_DATA", cod, "", "", "", "", ""))

    for cod in duplicate_mapping_cods:
        issues.append(make_issue("DUPLICATE_MAPPING", cod, "", "", "", "", ""))

    for cod, row in data_by_cod.items():
        if cod not in mapped_cods:
            issues.append(
                make_issue(
                    "MISSING",
                    cod,
                    row.get("nro_definitivo", ""),
                    row.get("des_dcp", ""),
                    "",
                    "",
                    "",
                )
            )

    for row in mapping_rows:
        cod = clean(row.get("cod_nacion", ""))
        data_row = data_by_cod.get(cod, {})
        des_dcp = clean(data_row.get("des_dcp", ""))
        concept = clean(row.get("concept_name", ""))
        mapping_type = clean(row.get("mapping_type", ""))
        concept_id = clean(row.get("concept_id", ""))
        source_nro = clean(data_row.get("nro_definitivo", ""))
        mapped_nro = clean(row.get("nro_definitivo", ""))

        if cod not in data_by_cod:
            issues.append(make_issue("STALE_MAPPING", cod, mapped_nro, "", concept_id, concept, mapping_type))
            continue

        if source_nro and mapped_nro and source_nro != mapped_nro:
            issues.append(make_issue("NRO_MISMATCH", cod, mapped_nro, des_dcp, concept_id, concept, mapping_type))

        if not concept_id:
            issues.append(make_issue("NO_CONCEPT", cod, mapped_nro, des_dcp, concept_id, concept, mapping_type))
        elif not mapping_type:
            issues.append(make_issue("NO_TYPE", cod, mapped_nro, des_dcp, concept_id, concept, mapping_type))
        elif mapping_type == "BROAD":
            issues.append(make_issue("BROAD", cod, mapped_nro, des_dcp, concept_id, concept, mapping_type))
        elif mapping_type == "EXACT" and needs_volume_review(data_row, concept):
            issues.append(make_issue("REVIEW_VOLUME", cod, mapped_nro, des_dcp, concept_id, concept, mapping_type))

    if not issues:
        print("OK - no issues found")
        return

    if args.details:
        print_details(issues, issue_filter=args.issue)
        return

    print_summary(folder.name, issues)


if __name__ == "__main__":
    main()
