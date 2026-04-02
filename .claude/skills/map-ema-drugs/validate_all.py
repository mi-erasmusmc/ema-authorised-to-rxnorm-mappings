#!/usr/bin/env python3
"""
Validate all EMA product folders and report issues across the entire registry.

Usage:
    python3 .claude/skills/map-ema-drugs/validate_all.py
    python3 .claude/skills/map-ema-drugs/validate_all.py --issue STALE_MAPPING
    python3 .claude/skills/map-ema-drugs/validate_all.py --issue MISSING --details
    python3 .claude/skills/map-ema-drugs/validate_all.py --issue BROAD --min-count 2
    python3 .claude/skills/map-ema-drugs/validate_all.py --issue INVALID --invalid-reason "dose form"

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
    UNMAPPED_FOLDER   - folder has parsed data but no mapping.tsv at all
    NO_DATE           - parsed_data file has no date (parsed_data.tsv instead of parsed_data_dateXX.tsv)
    MISSING           - ma_number in parsed_data with no row in mapping.tsv
    STALE_MAPPING     - mapping row whose ma_number no longer exists in parsed_data
    NO_CONCEPT        - mapping row with empty concept_id
    NO_TYPE           - mapping row with concept_id but empty mapping_type
    BROAD             - mapping row with mapping_type=BROAD missing suggestion
    NO_MAPPING        - mapping row with mapping_type=NO_MAPPING missing suggestion
    REVIEW_VOLUME     - likely single-use injectable mapped to a concentration-only concept
    REVIEW_INJECTION_FORM - multi-use injectable solution/suspension concept includes packaging-style leading volume
    DUPLICATE_DATA    - duplicate ma_number in parsed_data
    DUPLICATE_MAPPING - duplicate ma_number in mapping.tsv
    INCONSISTENT_CONCEPT - EXACT rows with same clinical signature but different concept_ids
    INCONSISTENT_TYPE - rows sharing same clinical signature and concept_id use different mapping_types
    INVALID           - mapping.tsv fails structural validation
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "map-drugs"))
import validate_core as core  # noqa: E402


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


def validate_folder(folder: Path, suppressions=None) -> list[dict]:
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
        issues.append(core.make_issue("UNMAPPED_FOLDER", "", f"{len(data_rows)} presentations unmapped", "", "", ""))
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
            core.clean(data_row.get("pack_size", "")),
            core.clean(data_row.get("product_name", "")),
        )

    issues += core.run_common_checks(
        "ma_number",
        data_rows,
        mapping_rows,
        describe=make_description,
    )

    for row in mapping_rows:
        ma_number = core.clean(row.get("ma_number", ""))
        if ma_number not in data_by_id:
            continue
        if core.clean(row.get("mapping_type", "")) != "EXACT":
            continue
        concept_name = core.clean(row.get("concept_name", ""))
        if concept_name.startswith("{") or concept_name.endswith("Pack"):
            continue
        comment = core.clean(row.get("comment", "")).lower()
        if "overfill" in comment or "deliverable dose" in comment:
            continue
        data_row = data_by_id[ma_number]
        if core.needs_volume_review(
            data_row,
            concept_name,
            description_key="content",
            form_key="pharmaceutical_form",
            route_key="route_of_administration",
            injectable_form_markers=("injection", "injectable"),
            route_skip_markers=("intravitreal",),
        ):
            issues.append(core.make_issue(
                "REVIEW_VOLUME",
                ma_number,
                make_description(data_row),
                core.clean(row.get("concept_id", "")),
                concept_name,
                core.clean(row.get("mapping_type", "")),
            ))
        if core.needs_injection_form_review(concept_name):
            issues.append(core.make_issue(
                "REVIEW_INJECTION_FORM",
                ma_number,
                make_description(data_row),
                core.clean(row.get("concept_id", "")),
                concept_name,
                core.clean(row.get("mapping_type", "")),
            ))

    issues += core.check_inconsistent_concepts(
        "ma_number", data_by_id, mapping_rows, sig_fn=ema_sig, describe=make_description,
    )
    issues += core.check_inconsistent_types(
        "ma_number", data_by_id, mapping_rows, sig_fn=ema_sig, describe=make_description,
    )
    issues += core.validate_folder_issues(mapping_path)

    if suppressions:
        issues = core.apply_suppressions(issues, folder.name, suppressions)

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
        "Validate EMA product folders.",
        default_products,
        core.EMA_ISSUE_TYPES,
    )
    args = core.parse_standard_args(parser)

    if args.folder:
        # Single-folder mode
        folder = Path(args.folder)
        suppressions_path = folder.parent.parent / "suppressions.tsv"
        suppressions = core.load_suppressions(suppressions_path, id_col="ma_number")
        issues = validate_folder(folder, suppressions=suppressions)
        core.run_single_folder_reporter(folder.name, issues, args)
        return

    # Multi-folder mode
    products_dir = Path(args.products_dir)
    if not products_dir.is_dir():
        print(f"ERROR: {products_dir} not found", file=sys.stderr)
        sys.exit(1)

    suppressions_path = products_dir.parent / "suppressions.tsv"
    suppressions = core.load_suppressions(suppressions_path, id_col="ma_number")

    folder_issues = {}
    for folder in discover_folders(products_dir):
        issues = validate_folder(folder, suppressions=suppressions)
        if issues:
            # Suppress NO_DATE-only folders -- a missing date suffix is not actionable
            if all(i["issue"] == "NO_DATE" for i in issues):
                continue
            folder_issues[folder] = issues

    core.run_reporter(folder_issues, args, core.EMA_ISSUE_TYPES)


if __name__ == "__main__":
    main()
