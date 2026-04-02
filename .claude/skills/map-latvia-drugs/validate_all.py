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

    # REVIEW_VOLUME and REVIEW_INJECTION_FORM for injectables
    for row in mapping_rows:
        product_id = core.clean(row.get("product_id", ""))
        if product_id not in data_by_id:
            continue
        if core.clean(row.get("mapping_type", "")) != "EXACT":
            continue
        concept_name = core.clean(row.get("concept_name", ""))
        if concept_name.startswith("{") or concept_name.endswith("Pack"):
            continue
        comment = core.clean(row.get("comment", "")).lower()
        if "overfill" in comment or "deliverable dose" in comment:
            continue
        data_row = data_by_id[product_id]
        if core.needs_volume_review(
            data_row,
            concept_name,
            description_key="product_strength",
            form_key="pharmaceutical_form",
            injectable_form_markers=("injection", "injectable", "infusion"),
        ):
            issues.append(core.make_issue(
                "REVIEW_VOLUME",
                product_id,
                make_description(data_row),
                core.clean(row.get("concept_id", "")),
                concept_name,
                core.clean(row.get("mapping_type", "")),
            ))
        if core.needs_injection_form_review(concept_name):
            issues.append(core.make_issue(
                "REVIEW_INJECTION_FORM",
                product_id,
                make_description(data_row),
                core.clean(row.get("concept_id", "")),
                concept_name,
                core.clean(row.get("mapping_type", "")),
            ))

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


def folder_display_name(folder: Path) -> str:
    """Return substance/product as the display name for a Latvia folder."""
    return f"{folder.parent.name}/{folder.name}"


def main():
    script_dir = Path(__file__).parent
    default_products = script_dir.parent.parent.parent / "data" / "latvia" / "products"

    parser = core.build_argparser(
        "Validate Latvia product folders.",
        default_products,
        core.LATVIA_ISSUE_TYPES,
    )
    args = core.parse_standard_args(parser)

    if args.folder:
        # Single-folder mode
        folder = Path(args.folder)
        suppressions_path = folder.parent.parent.parent / "suppressions.tsv"
        suppressions = core.load_suppressions(suppressions_path, id_col="product_id")
        issues = validate_folder(folder, suppressions=suppressions)
        core.run_single_folder_reporter(folder_display_name(folder), issues, args)
        return

    # Multi-folder mode
    products_dir = Path(args.products_dir)
    if not products_dir.is_dir():
        print(f"ERROR: {products_dir} not found", file=sys.stderr)
        sys.exit(1)

    suppressions_path = products_dir.parent / "suppressions.tsv"
    suppressions = core.load_suppressions(suppressions_path, id_col="product_id")

    folder_issues = {}
    for folder in discover_folders(products_dir):
        issues = validate_folder(folder, suppressions=suppressions)
        if issues:
            folder_issues[folder] = issues

    display_issues = {}
    for folder, issues in folder_issues.items():
        display_folder = _DisplayPath(folder, folder_display_name(folder))
        display_issues[display_folder] = issues

    core.run_reporter(display_issues, args, core.LATVIA_ISSUE_TYPES)


class _DisplayPath:
    """Wraps a Path so that .name returns a custom display string for the reporter."""

    def __init__(self, path: Path, display_name: str):
        self._path = path
        self.name = display_name

    def __fspath__(self):
        return str(self._path)

    def __str__(self):
        return str(self._path)

    def __hash__(self):
        return hash(self._path)

    def __eq__(self, other):
        if isinstance(other, _DisplayPath):
            return self._path == other._path
        return self._path == other


if __name__ == "__main__":
    main()
