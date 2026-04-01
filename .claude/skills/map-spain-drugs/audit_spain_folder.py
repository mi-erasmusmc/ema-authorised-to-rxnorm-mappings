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
    MISSING               - cod_nacion in data.tsv with no row in mapping.tsv
    NO_TYPE               - mapping row with empty mapping_type
    NO_CONCEPT            - mapping row with empty concept_id
    BROAD                 - mapping row with mapping_type=BROAD missing suggestion
    NO_MAPPING            - mapping row with mapping_type=NO_MAPPING missing suggestion
    STALE_MAPPING         - mapping row whose cod_nacion no longer exists in data.tsv
    NRO_MISMATCH          - mapping row whose nro_definitivo disagrees with data.tsv
    DUPLICATE_DATA        - duplicate cod_nacion in data.tsv
    DUPLICATE_MAPPING     - duplicate cod_nacion in mapping.tsv
    REVIEW_VOLUME         - likely single-use injectable mapped to a concentration-only concept
    INCONSISTENT_CONCEPT  - EXACT rows with the same des_dcp, sw_generico, and forma_farmaceutica map to different
                            concept_ids. For branded products the comparison is narrowed to the same brand key.
    INCONSISTENT_TYPE     - rows sharing the same clinical signature and concept_id use different mapping_types
                            (e.g. one row is EXACT while another with the same concept is BROAD).
    INVALID               - mapping.tsv fails structural validation (bad date, invalid suggestion, etc.)
"""

import argparse
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "map-drugs"))

import audit_core as core  # noqa: E402


DETAIL_HEADER = [
    "issue",
    "cod_nacion",
    "nro_definitivo",
    "des_dcp",
    "concept_id",
    "concept_name",
    "mapping_type",
]


def _core_to_spain(issue, nro_definitivo=""):
    """Convert a core audit issue dict to Spain's dict format."""
    return {
        "issue": issue["issue"],
        "cod_nacion": issue["source_id"],
        "nro_definitivo": nro_definitivo,
        "des_dcp": issue["description"],
        "concept_id": issue["concept_id"],
        "concept_name": issue["concept_name"],
        "mapping_type": issue["mapping_type"],
    }


def make_issue(issue, cod, nro_definitivo, des_dcp, concept_id, concept_name, mapping_type):
    return {
        "issue": core.clean(issue),
        "cod_nacion": core.clean(cod),
        "nro_definitivo": core.clean(nro_definitivo),
        "des_dcp": core.clean(des_dcp),
        "concept_id": core.clean(concept_id),
        "concept_name": core.clean(concept_name),
        "mapping_type": core.clean(mapping_type),
    }


def branded_signature_key(data_row):
    des_nomco = core.clean(data_row.get("des_nomco", ""))
    if des_nomco:
        match = re.match(r"^(.*?)(?:\s+\d+(?:[.,]\d+)?\s*(?:mg|mcg|g|ui|iu|ml)\b|$)", des_nomco, flags=re.IGNORECASE)
        if match:
            brand = core.clean(match.group(1))
            if brand:
                return brand.upper()
    return core.clean(data_row.get("laboratorio_titular", "")).upper()


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


def load_suppressions(suppressions_path: Path) -> dict:
    """Load audit_suppressions.tsv and return {folder_name: set of (issue, cod_nacion)}."""
    result = {}
    if not suppressions_path.exists():
        return result
    rows = core.load_tsv(suppressions_path)
    for row in rows:
        folder_name = core.clean(row.get("folder", ""))
        issue = core.clean(row.get("issue", ""))
        cod = core.clean(row.get("cod_nacion", ""))
        if folder_name and issue and cod:
            result.setdefault(folder_name, set()).add((issue, cod))
    return result


def audit_folder(folder: Path, suppressed: set = None):
    """Return a list of issue dicts for a product folder. Empty list = clean.

    suppressed: optional set of (issue_type, cod_nacion) tuples to exclude.
    """
    data_path = folder / "data.tsv"
    mapping_path = folder / "mapping.tsv"

    if not data_path.exists():
        return []

    data_rows = core.load_tsv(data_path)
    data_by_cod = {core.clean(row["cod_nacion"]): row for row in data_rows}
    mapping_rows = core.load_tsv(mapping_path) if mapping_path.exists() else []

    # Common checks (shared with EMA and other sources)
    issues = [
        _core_to_spain(i)
        for i in core.run_common_checks(
            "cod_nacion",
            data_rows,
            mapping_rows,
            describe=lambda row: core.clean(row.get("des_dcp", "")),
        )
    ]

    # Structural validation
    issues += [_core_to_spain(i) for i in core.validate_folder_issues(mapping_path)]

    # Spain-specific: NRO_MISMATCH and REVIEW_VOLUME
    for row in mapping_rows:
        cod = core.clean(row.get("cod_nacion", ""))
        if cod not in data_by_cod:
            continue  # STALE already caught by core
        data_row = data_by_cod[cod]
        des_dcp = core.clean(data_row.get("des_dcp", ""))
        concept = core.clean(row.get("concept_name", ""))
        mapping_type = core.clean(row.get("mapping_type", ""))
        concept_id = core.clean(row.get("concept_id", ""))
        source_nro = core.clean(data_row.get("nro_definitivo", ""))
        mapped_nro = core.clean(row.get("nro_definitivo", ""))

        if source_nro and mapped_nro and source_nro != mapped_nro:
            issues.append(make_issue("NRO_MISMATCH", cod, mapped_nro, des_dcp, concept_id, concept, mapping_type))

        if mapping_type == "EXACT" and core.needs_volume_review(
            data_row,
            concept,
            description_key="des_dcp",
            unit_key="unidad_contenido",
            form_key="forma_farmaceutica",
            injectable_unit_markers=("inye",),
            injectable_form_markers=("inyect",),
        ):
            issues.append(make_issue("REVIEW_VOLUME", cod, mapped_nro, des_dcp, concept_id, concept, mapping_type))

    # Spain-specific: INCONSISTENT_CONCEPT
    def spain_sig(data_row):
        des_dcp = core.clean(data_row.get("des_dcp", ""))
        if not des_dcp:
            return None
        sw_generico = core.clean(data_row.get("sw_generico", ""))
        forma = core.clean(data_row.get("forma_farmaceutica", ""))
        if sw_generico == "0":
            return (des_dcp, sw_generico, forma, branded_signature_key(data_row))
        return (des_dcp, sw_generico, forma)

    for issue in core.check_inconsistent_concepts(
        "cod_nacion", data_by_cod, mapping_rows, sig_fn=spain_sig,
        describe=lambda row: core.clean(row.get("des_dcp", "")),
    ):
        # Remap to Spain format (nro_definitivo not available here; use empty string)
        issues.append(_core_to_spain(issue))

    for issue in core.check_inconsistent_types(
        "cod_nacion", data_by_cod, mapping_rows, sig_fn=spain_sig,
        describe=lambda row: core.clean(row.get("des_dcp", "")),
    ):
        issues.append(_core_to_spain(issue))

    if suppressed:
        issues = [i for i in issues if (i["issue"], i["cod_nacion"]) not in suppressed]

    return issues


def main():
    args = parse_args()
    folder = Path(args.folder)

    if not (folder / "data.tsv").exists():
        print(f"ERROR: {folder / 'data.tsv'} not found", file=sys.stderr)
        sys.exit(1)

    suppressions_path = folder.parent.parent / "audit_suppressions.tsv"
    all_suppressions = load_suppressions(suppressions_path)
    suppressed = all_suppressions.get(folder.name, set())
    issues = audit_folder(folder, suppressed=suppressed)

    if not issues:
        print("OK - no issues found")
        return

    if args.details:
        print_details(issues, issue_filter=args.issue)
        return

    print_summary(folder.name, issues)


if __name__ == "__main__":
    main()
