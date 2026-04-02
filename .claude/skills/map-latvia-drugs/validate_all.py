#!/usr/bin/env python3
"""
Validate all Latvia product folders and report issues across the entire registry.

Usage:
    python3 .claude/skills/map-latvia-drugs/validate_all.py
    python3 .claude/skills/map-latvia-drugs/validate_all.py --issue BROAD
    python3 .claude/skills/map-latvia-drugs/validate_all.py --issue MISSING --details
    python3 .claude/skills/map-latvia-drugs/validate_all.py --issue MISSING --min-count 3
    python3 .claude/skills/map-latvia-drugs/validate_all.py --issue INVALID --invalid-reason "dose form"

Default output (no --issue):
    One summary line per folder with any issues, showing counts by type.
    Sorted by total issue count descending.

With --issue ISSUE_TYPE:
    Only folders that have that issue type are shown.
    Sorted by count for that issue type descending.

With --details:
    Print full tab-separated rows for each matching folder.
    Requires --issue.

Issue types:
    UNMAPPED_FOLDER       - folder has data but no mapping.tsv
    MISSING               - product_id in data with no row in mapping.tsv
    STALE_MAPPING         - mapping row whose product_id no longer exists in data
    NO_CONCEPT            - mapping row with empty concept_id (and not NO_MAPPING)
    NO_TYPE               - mapping row with concept_id but empty mapping_type
    BROAD                 - mapping row with mapping_type=BROAD missing suggestion
    NO_MAPPING            - mapping row with mapping_type=NO_MAPPING missing suggestion
    REVIEW_VOLUME         - likely single-use injectable mapped to a concentration-only concept
    REVIEW_INJECTION_FORM - multi-use injectable solution/suspension concept includes packaging-style leading volume
    DUPLICATE_DATA        - duplicate product_id in data
    DUPLICATE_MAPPING     - duplicate product_id in mapping.tsv
    INCONSISTENT_CONCEPT  - EXACT rows with same clinical signature but different concept_ids
    INCONSISTENT_TYPE     - rows sharing same clinical signature and concept_id use different mapping_types
    INVALID               - mapping.tsv fails structural validation
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "map-drugs"))
import validate_core as core  # noqa: E402


def folder_display_name(folder: Path) -> str:
    """Return substance/product as the display name for a Latvia folder."""
    return f"{folder.parent.name}/{folder.name}"


VALIDATOR_CONFIG = {
    "id_col": "product_id",
    "suppressions_path_fn": lambda folder: folder.parent.parent.parent / "suppressions.tsv",
    "display_name_fn": folder_display_name,
}


def find_data_file(folder):
    """Return the most recent data_*.tsv path, or None."""
    candidates = sorted(folder.glob("data_*.tsv"), reverse=True)
    return candidates[0] if candidates else None


def make_description(row):
    """Human-readable label from a Latvia data row."""
    parts = [
        core.clean(row.get("original_name", "")),
        core.clean(row.get("strength", "")),
        core.clean(row.get("pharmaceutical_form", "")),
    ]
    return " / ".join(p for p in parts if p)


def validate_folder(folder: Path, suppressions=None) -> list[dict]:
    """Return a list of issue dicts for a Latvia product folder. Empty = clean."""
    data_path = find_data_file(folder)
    if data_path is None:
        return []

    mapping_path = folder / "mapping.tsv"

    if not mapping_path.exists():
        data_rows = core.load_tsv(data_path)
        return [core.make_issue("UNMAPPED_FOLDER", "", f"{len(data_rows)} presentations unmapped", "", "", "")]

    data_rows = core.load_tsv(data_path)
    mapping_rows = core.load_tsv(mapping_path)

    data_by_id = {core.clean(row.get("product_id", "")): row for row in data_rows}

    issues = core.run_common_checks(
        "product_id",
        data_rows,
        mapping_rows,
        describe=make_description,
    )

    issues += core.check_volume_issues(
        "product_id", data_by_id, mapping_rows, make_description,
        volume_review_kwargs=dict(
            description_key="product_strength",
            form_key="pharmaceutical_form",
            injectable_form_markers=("injection", "injectable", "infusion"),
        ),
    )

    # Inconsistency checks
    def latvia_sig(data_row):
        return (
            core.clean(data_row.get("original_name", "")),
            core.clean(data_row.get("strength", "")),
            core.clean(data_row.get("pharmaceutical_form", "")),
            core.clean(data_row.get("product_strength", "")),
        )

    issues += core.check_inconsistent_concepts(
        "product_id", data_by_id, mapping_rows, sig_fn=latvia_sig, describe=make_description,
    )
    issues += core.check_inconsistent_types(
        "product_id", data_by_id, mapping_rows, sig_fn=latvia_sig, describe=make_description,
    )
    issues += core.validate_folder_issues(mapping_path)

    if suppressions:
        issues = core.apply_suppressions(issues, folder.name, suppressions)

    return issues


def discover_folders(products_dir: Path):
    """Walk substance/product two-level hierarchy, yield product folders with data."""
    folders = []
    for substance_dir in sorted(products_dir.iterdir()):
        if not substance_dir.is_dir() or substance_dir.name.startswith("."):
            continue
        for product_dir in sorted(substance_dir.iterdir()):
            if not product_dir.is_dir():
                continue
            if find_data_file(product_dir) is not None:
                folders.append(product_dir)
    return folders


def main():
    script_dir = Path(__file__).parent
    default_products = script_dir.parent.parent.parent / "data" / "latvia" / "products"

    core.run_validator(
        id_col="product_id",
        default_products=default_products,
        issue_types=core.LATVIA_ISSUE_TYPES,
        validate_fn=validate_folder,
        discover_fn=discover_folders,
        description="Validate Latvia product folders.",
        suppressions_path_fn=lambda f: f.parent.parent.parent / "suppressions.tsv",
        display_name_fn=folder_display_name,
    )


if __name__ == "__main__":
    main()
