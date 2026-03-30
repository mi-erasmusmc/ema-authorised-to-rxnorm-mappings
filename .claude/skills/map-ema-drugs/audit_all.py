#!/usr/bin/env python3
"""
Audit all EMA product folders and report issues across the entire registry.

Usage:
    python3 .claude/skills/map-ema-drugs/audit_all.py
    python3 .claude/skills/map-ema-drugs/audit_all.py --issue STALE_MAPPING
    python3 .claude/skills/map-ema-drugs/audit_all.py --issue MISSING --details
    python3 .claude/skills/map-ema-drugs/audit_all.py --issue BROAD --min-count 2

Default output (no --issue):
    One summary line per folder with any issues, showing counts by type.
    Sorted by total issue count descending.

With --issue ISSUE_TYPE:
    Only folders with that issue type are shown.
    Sorted by count for that issue type descending.

With --details:
    Print full tab-separated rows for each matching folder.
    Requires --issue.

Issue types:
    NO_MAPPING        - folder has parsed data but no mapping.tsv at all, OR
                        mapping row with mapping_type=NO_MAPPING missing suggestion
    NO_DATE           - parsed_data file has no date (parsed_data.tsv instead of parsed_data_dateXX.tsv)
    MISSING           - ma_number in parsed_data with no row in mapping.tsv
    STALE_MAPPING     - mapping row whose ma_number no longer exists in parsed_data
    NO_CONCEPT        - mapping row with empty concept_id
    NO_TYPE           - mapping row with concept_id but empty mapping_type
    BROAD             - mapping row with mapping_type=BROAD missing suggestion
    DUPLICATE_DATA    - duplicate ma_number in parsed_data
    DUPLICATE_MAPPING - duplicate ma_number in mapping.tsv
    INVALID           - mapping.tsv fails structural validation
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "map-drugs"))
import audit_core as core  # noqa: E402


ISSUE_TYPES = [
    "NO_MAPPING",
    "NO_DATE",
    "MISSING",
    "STALE_MAPPING",
    "NO_CONCEPT",
    "NO_TYPE",
    "BROAD",
    "DUPLICATE_DATA",
    "DUPLICATE_MAPPING",
    "INCONSISTENT_CONCEPT",
    "INVALID",
]


def find_parsed_data(folder):
    """Return the most recent parsed_data_*.tsv path, or None."""
    candidates = sorted(folder.glob("parsed_data*.tsv"), reverse=True)
    return candidates[0] if candidates else None


def make_description(row):
    """Human-readable label from a parsed_data row."""
    parts = [
        core.clean(row.get("product_name", "")),
        core.clean(row.get("strength", "")),
        core.clean(row.get("pharmaceutical_form", "")),
    ]
    return " / ".join(p for p in parts if p)


def audit_folder(folder: Path) -> list[dict]:
    """Return a list of issue dicts for an EMA product folder. Empty = clean."""
    parsed_path = find_parsed_data(folder)
    if parsed_path is None:
        return []

    issues = []
    if parsed_path.name == "parsed_data.tsv":
        issues.append(core.make_issue("NO_DATE", "", "parsed_data.tsv has no date suffix", "", "", ""))

    mapping_path = folder / "mapping.tsv"

    if not mapping_path.exists():
        data_rows = core.load_tsv(parsed_path)
        issues.append(core.make_issue("NO_MAPPING", "", f"{len(data_rows)} presentations unmapped", "", "", ""))
        return issues

    data_rows = core.load_tsv(parsed_path)
    mapping_rows = core.load_tsv(mapping_path)

    data_by_id = {core.clean(row.get("ma_number", "")): row for row in data_rows}

    def ema_sig(data_row):
        return (
            core.clean(data_row.get("strength", "")),
            core.clean(data_row.get("pharmaceutical_form", "")),
            core.clean(data_row.get("route_of_administration", "")),
            core.clean(data_row.get("packaging", "")),
            core.clean(data_row.get("content", "")),
            core.clean(data_row.get("product_name", "")),
        )

    issues += core.run_common_checks(
        "ma_number",
        data_rows,
        mapping_rows,
        describe=make_description,
    )
    issues += core.check_inconsistent_concepts(
        "ma_number", data_by_id, mapping_rows, sig_fn=ema_sig, describe=make_description,
    )
    issues += core.validate_folder_issues(mapping_path)
    return issues


def discover_folders(products_dir: Path):
    return sorted(
        p for p in products_dir.iterdir()
        if p.is_dir() and not p.name.startswith(".") and find_parsed_data(p) is not None
    )


def main():
    script_dir = Path(__file__).parent
    default_products = script_dir.parent.parent.parent / "data" / "ema" / "products"

    parser = core.build_argparser(
        "Audit all EMA product folders.",
        default_products,
        ISSUE_TYPES,
    )
    args = parser.parse_args()
    if args.issue:
        args.issue = args.issue.strip().upper()
    if args.details and not args.issue:
        parser.error("--details requires --issue")

    products_dir = Path(args.products_dir)
    if not products_dir.is_dir():
        import sys as _sys
        print(f"ERROR: {products_dir} not found", file=_sys.stderr)
        _sys.exit(1)

    folder_issues = {}
    for folder in discover_folders(products_dir):
        issues = audit_folder(folder)
        if issues:
            folder_issues[folder] = issues

    core.run_reporter(folder_issues, args, ISSUE_TYPES)


if __name__ == "__main__":
    main()
