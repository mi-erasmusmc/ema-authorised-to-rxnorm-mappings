#!/usr/bin/env python3
"""
Audit all Spain product folders and report issues across the entire registry.

Usage:
    python3 .claude/skills/map-spain-drugs/audit_all.py
    python3 .claude/skills/map-spain-drugs/audit_all.py --issue BROAD
    python3 .claude/skills/map-spain-drugs/audit_all.py --issue MISSING --details
    python3 .claude/skills/map-spain-drugs/audit_all.py --issue MISSING --min-count 3

Default output (no --issue):
    One summary line per folder with any issues, showing counts by type.
    Sorted by total issue count descending.

With --issue ISSUE_TYPE:
    Only folders that have that issue type are shown.
    Sorted by count for that issue type descending.

With --details:
    Print full tab-separated rows for each matching folder (same format as
    audit_folder.py --details --issue), separated by a folder header line.

Issue types:
    MISSING               - cod_nacion in data.tsv with no row in mapping.tsv
    NO_TYPE               - mapping row with empty mapping_type
    NO_CONCEPT            - mapping row with empty concept_id
    BROAD                 - mapping row with mapping_type=BROAD (for review)
    STALE_MAPPING         - mapping row whose cod_nacion no longer exists in data.tsv
    NRO_MISMATCH          - mapping row whose nro_definitivo disagrees with data.tsv
    DUPLICATE_DATA        - duplicate cod_nacion in data.tsv
    DUPLICATE_MAPPING     - duplicate cod_nacion in mapping.tsv
    REVIEW_VOLUME         - likely single-use injectable mapped to a concentration-only concept
    INCONSISTENT_CONCEPT  - EXACT rows with same clinical signature but different concept_ids
    INVALID               - mapping.tsv fails structural validation (bad date, invalid suggestion, etc.)
"""

import argparse
import sys
from collections import Counter
from pathlib import Path

# Allow importing from the same directory as this script and the map-drugs skill
sys.path.insert(0, str(Path(__file__).parent))

from audit_folder import (  # noqa: E402
    DETAIL_HEADER,
    audit_folder,
    print_details,
)


ISSUE_TYPES = [
    "MISSING",
    "NO_CONCEPT",
    "NO_TYPE",
    "BROAD",
    "STALE_MAPPING",
    "NRO_MISMATCH",
    "DUPLICATE_DATA",
    "DUPLICATE_MAPPING",
    "REVIEW_VOLUME",
    "INCONSISTENT_CONCEPT",
    "INVALID",
]


def discover_folders(products_dir: Path):
    return sorted(p for p in products_dir.iterdir() if p.is_dir() and (p / "data.tsv").exists())


def parse_args():
    script_dir = Path(__file__).parent
    default_products = script_dir.parent.parent.parent / "data" / "spain" / "products"

    parser = argparse.ArgumentParser(
        description="Audit all Spain product folders.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--products-dir",
        default=str(default_products),
        help="Path to data/spain/products/ (auto-detected by default)",
    )
    parser.add_argument(
        "--issue",
        help=(
            "Filter to folders with this issue type. "
            f"One of: {', '.join(ISSUE_TYPES)}"
        ),
    )
    parser.add_argument(
        "--details",
        action="store_true",
        help="Print row-level TSV for matching folders (requires --issue)",
    )
    parser.add_argument(
        "--min-count",
        type=int,
        default=1,
        metavar="N",
        help="Only show folders with at least N occurrences of the issue (default: 1)",
    )
    args = parser.parse_args()
    if args.issue:
        args.issue = args.issue.strip().upper()
    if args.details and not args.issue:
        parser.error("--details requires --issue")
    return args


def format_summary_line(folder_name: str, counts: Counter) -> str:
    parts = [f"{counts[t]} {t}" for t in ISSUE_TYPES if counts[t] > 0]
    return f"{folder_name}\t{', '.join(parts)}"


def main():
    args = parse_args()
    products_dir = Path(args.products_dir)

    if not products_dir.is_dir():
        print(f"ERROR: {products_dir} not found", file=sys.stderr)
        sys.exit(1)

    folders = discover_folders(products_dir)

    # Collect issues for all folders
    folder_issues = {}
    for folder in folders:
        issues = audit_folder(folder)
        if issues:
            folder_issues[folder] = issues

    if not folder_issues:
        print("OK - no issues found across all folders")
        return

    if args.issue:
        # Filter to folders with the requested issue type at or above min-count
        matching = [
            (folder, issues)
            for folder, issues in folder_issues.items()
            if sum(1 for i in issues if i["issue"] == args.issue) >= args.min_count
        ]
        matching.sort(
            key=lambda item: -sum(1 for i in item[1] if i["issue"] == args.issue)
        )

        if not matching:
            print(f"OK - no {args.issue} issues found (min-count={args.min_count})")
            return

        total = sum(
            sum(1 for i in issues if i["issue"] == args.issue)
            for _, issues in matching
        )
        print(f"# {args.issue}: {total} occurrences in {len(matching)} folders\n")

        if args.details:
            print("\t".join(["folder"] + DETAIL_HEADER))
            for folder, issues in matching:
                filtered = [i for i in issues if i["issue"] == args.issue]
                for issue in sorted(filtered, key=lambda x: x["cod_nacion"]):
                    row = [folder.name] + [issue[col] for col in DETAIL_HEADER]
                    print("\t".join(row))
        else:
            for folder, issues in matching:
                count = sum(1 for i in issues if i["issue"] == args.issue)
                print(f"{count}\t{folder.name}")

    else:
        # Full summary: all folders with issues, sorted by total issue count
        ranked = sorted(folder_issues.items(), key=lambda item: -len(item[1]))
        total_issues = sum(len(issues) for issues in folder_issues.values())
        print(f"# {len(folder_issues)} folders with issues, {total_issues} total\n")
        for folder, issues in ranked:
            counts = Counter(i["issue"] for i in issues)
            print(format_summary_line(folder.name, counts))


if __name__ == "__main__":
    main()
