#!/usr/bin/env python3
"""
Shared audit utilities for drug mapping folders (EMA, Spain, Latvia, …).

Provides common data-quality checks, structural validation via validate_mapping.py,
and reporter helpers reused across source-specific audit scripts.

Issue dict schema (returned by run_common_checks and validate_folder_issues):
    issue        str  — issue type name
    source_id    str  — source-specific ID (ma_number, cod_nacion, …)
    description  str  — human-readable label for the row
    concept_id   str  — mapped concept_id (may be empty)
    concept_name str  — mapped concept_name (may be empty)
    mapping_type str  — EXACT, BROAD, NO_MAPPING, or empty
"""

import argparse
import csv
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from validate_mapping import validate_file  # noqa: E402


COMMON_CHECKS = [
    "MISSING",
    "STALE_MAPPING",
    "NO_CONCEPT",
    "NO_TYPE",
    "BROAD",
    "NO_MAPPING",
    "DUPLICATE_DATA",
    "DUPLICATE_MAPPING",
    "INVALID",
]

DETAIL_HEADER = [
    "issue",
    "source_id",
    "description",
    "concept_id",
    "concept_name",
    "mapping_type",
]


# ── Utilities ──────────────────────────────────────────────────────────────────

def load_tsv(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def clean(value):
    return str(value).strip() if value is not None else ""


def duplicate_values(rows, key):
    counts = Counter(clean(row.get(key, "")) for row in rows if clean(row.get(key, "")))
    return sorted(v for v, c in counts.items() if c > 1)


def make_issue(issue, source_id, description, concept_id, concept_name, mapping_type):
    return {
        "issue": clean(issue),
        "source_id": clean(source_id),
        "description": clean(description),
        "concept_id": clean(concept_id),
        "concept_name": clean(concept_name),
        "mapping_type": clean(mapping_type),
    }


def extract_ml(text):
    match = re.search(r"(\d+(?:[.,]\d+)?)\s*ml\b", clean(text), flags=re.IGNORECASE)
    if not match:
        return None
    return match.group(1).replace(",", ".")


def normalize_numeric_string(value):
    value = clean(value)
    if not value:
        return value
    try:
        number = float(value)
    except ValueError:
        return value.lower()
    if number.is_integer():
        return str(int(number))
    return format(number, "g")


def needs_volume_review(
    data_row,
    concept_name,
    *,
    description_key,
    unit_key=None,
    form_key=None,
    route_key=None,
    injectable_unit_markers=(),
    injectable_form_markers=(),
    route_skip_markers=(),
    concept_dose_form="injection",
    strength_marker="mg/ml",
):
    description = clean(data_row.get(description_key, ""))
    volume = extract_ml(description)
    if not volume:
        return False

    unit_value = clean(data_row.get(unit_key, "")).lower() if unit_key else ""
    form_value = clean(data_row.get(form_key, "")).lower() if form_key else ""
    route_value = clean(data_row.get(route_key, "")).lower() if route_key else ""
    if injectable_unit_markers or injectable_form_markers:
        unit_matches = any(marker in unit_value for marker in injectable_unit_markers)
        form_matches = any(marker in form_value for marker in injectable_form_markers)
        if not unit_matches and not form_matches:
            return False
    if route_skip_markers and any(marker in route_value for marker in route_skip_markers):
        return False

    concept_lower = clean(concept_name).lower()
    if concept_dose_form and concept_dose_form not in concept_lower:
        return False
    if strength_marker and strength_marker not in concept_lower:
        return False
    prefix_match = re.match(r"^(?P<volume>\d+(?:\.\d+)?)\s*ml\b", concept_lower)
    if not prefix_match:
        return True
    return normalize_numeric_string(prefix_match.group("volume")) != normalize_numeric_string(volume)


# ── Common checks ──────────────────────────────────────────────────────────────

def run_common_checks(source_id_col, data_rows, mapping_rows, describe=None):
    """
    Run the common mapping quality checks shared across all data sources.

    Args:
        source_id_col : column name for the source ID (e.g. "ma_number", "cod_nacion")
        data_rows     : list of dicts from the source data file
        mapping_rows  : list of dicts read from mapping.tsv
        describe      : optional callable(data_row) → str for human-readable row labels

    Returns a list of issue dicts (see module docstring for schema).

    Checks performed: DUPLICATE_DATA, DUPLICATE_MAPPING, MISSING, STALE_MAPPING,
                      NO_CONCEPT, NO_TYPE, BROAD, NO_MAPPING.
    """
    if describe is None:
        describe = lambda row: ""  # noqa: E731

    data_by_id = {clean(row.get(source_id_col, "")): row for row in data_rows}
    duplicate_data_ids = set(duplicate_values(data_rows, source_id_col))

    mapped_ids = {clean(row.get(source_id_col, "")) for row in mapping_rows}
    duplicate_mapping_ids = set(duplicate_values(mapping_rows, source_id_col))

    issues = []

    for sid in sorted(duplicate_data_ids):
        issues.append(make_issue("DUPLICATE_DATA", sid, describe(data_by_id.get(sid, {})), "", "", ""))

    for sid in sorted(duplicate_mapping_ids):
        issues.append(make_issue("DUPLICATE_MAPPING", sid, "", "", "", ""))

    for row in data_rows:
        sid = clean(row.get(source_id_col, ""))
        if sid not in mapped_ids:
            issues.append(make_issue("MISSING", sid, describe(row), "", "", ""))

    for row in mapping_rows:
        sid = clean(row.get(source_id_col, ""))
        concept_id = clean(row.get("concept_id", ""))
        concept_name = clean(row.get("concept_name", ""))
        mapping_type = clean(row.get("mapping_type", ""))
        suggestion = clean(row.get("suggestion", ""))
        data_row = data_by_id.get(sid)

        if data_row is None:
            issues.append(make_issue("STALE_MAPPING", sid, "", concept_id, concept_name, mapping_type))
            continue

        description = describe(data_row)

        if not concept_id and mapping_type != "NO_MAPPING":
            issues.append(make_issue("NO_CONCEPT", sid, description, concept_id, concept_name, mapping_type))
        elif not mapping_type:
            issues.append(make_issue("NO_TYPE", sid, description, concept_id, concept_name, mapping_type))
        elif mapping_type == "BROAD" and not suggestion:
            issues.append(make_issue("BROAD", sid, description, concept_id, concept_name, mapping_type))
        elif mapping_type == "NO_MAPPING" and not suggestion:
            issues.append(make_issue("NO_MAPPING", sid, description, concept_id, concept_name, mapping_type))

    return issues


def validate_folder_issues(mapping_path):
    """
    Validate mapping.tsv structure via validate_mapping.py.
    Returns a list of INVALID issue dicts, one per structural error found.
    """
    if not Path(mapping_path).exists():
        return []
    errors = validate_file(str(mapping_path))
    return [make_issue("INVALID", "", error.strip(), "", "", "") for error in errors]


def check_inconsistent_concepts(source_id_col, data_by_id, mapping_rows, sig_fn, describe=None):
    """
    Detect EXACT mapping rows that share the same clinical signature but use different concept_ids.

    Args:
        source_id_col : column name for the source ID
        data_by_id    : dict mapping source_id → data row
        mapping_rows  : list of dicts read from mapping.tsv
        sig_fn        : callable(data_row) → hashable signature tuple representing the
                        clinical identity (e.g. strength + form + route). Rows whose
                        data_row is missing are skipped.
        describe      : optional callable(data_row) → str for human-readable labels

    Returns a list of INCONSISTENT_CONCEPT issue dicts for every mapping row that
    belongs to a signature group where more than one concept_id is used.
    """
    if describe is None:
        describe = lambda row: ""  # noqa: E731

    from collections import defaultdict
    sig_to_concepts = defaultdict(set)
    sig_to_rows = defaultdict(list)

    for row in mapping_rows:
        sid = clean(row.get(source_id_col, ""))
        concept_id = clean(row.get("concept_id", ""))
        mapping_type = clean(row.get("mapping_type", ""))
        if not concept_id or mapping_type != "EXACT":
            continue
        data_row = data_by_id.get(sid)
        if data_row is None:
            continue
        sig = sig_fn(data_row)
        if sig is None:
            continue
        sig_to_concepts[sig].add(concept_id)
        sig_to_rows[sig].append(row)

    issues = []
    for sig, concepts in sig_to_concepts.items():
        if len(concepts) > 1:
            for row in sig_to_rows[sig]:
                sid = clean(row.get(source_id_col, ""))
                data_row = data_by_id.get(sid, {})
                issues.append(make_issue(
                    "INCONSISTENT_CONCEPT",
                    sid,
                    describe(data_row),
                    clean(row.get("concept_id", "")),
                    clean(row.get("concept_name", "")),
                    clean(row.get("mapping_type", "")),
                ))
    return issues


def check_inconsistent_types(source_id_col, data_by_id, mapping_rows, sig_fn, describe=None):
    """
    Detect mapping rows that share the same clinical signature and the same concept_id
    but use different mapping_types.

    This catches the case where identical concepts are expected and present but some rows
    are EXACT while others are BROAD (or any other type mismatch).

    Args:
        source_id_col : column name for the source ID
        data_by_id    : dict mapping source_id → data row
        mapping_rows  : list of dicts read from mapping.tsv
        sig_fn        : callable(data_row) → hashable signature tuple
        describe      : optional callable(data_row) → str for human-readable labels

    Returns a list of INCONSISTENT_TYPE issue dicts.
    """
    if describe is None:
        describe = lambda row: ""  # noqa: E731

    from collections import defaultdict
    key_to_types = defaultdict(set)
    key_to_rows = defaultdict(list)

    for row in mapping_rows:
        sid = clean(row.get(source_id_col, ""))
        concept_id = clean(row.get("concept_id", ""))
        mapping_type = clean(row.get("mapping_type", ""))
        if not concept_id or not mapping_type:
            continue
        data_row = data_by_id.get(sid)
        if data_row is None:
            continue
        sig = sig_fn(data_row)
        if sig is None:
            continue
        key = (sig, concept_id)
        key_to_types[key].add(mapping_type)
        key_to_rows[key].append(row)

    issues = []
    for (sig, concept_id), types in key_to_types.items():
        if len(types) > 1:
            for row in key_to_rows[(sig, concept_id)]:
                sid = clean(row.get(source_id_col, ""))
                data_row = data_by_id.get(sid, {})
                issues.append(make_issue(
                    "INCONSISTENT_TYPE",
                    sid,
                    describe(data_row),
                    clean(row.get("concept_id", "")),
                    clean(row.get("concept_name", "")),
                    clean(row.get("mapping_type", "")),
                ))
    return issues


# ── Reporter ───────────────────────────────────────────────────────────────────

def format_summary_line(folder_name, counts, issue_types):
    parts = [f"{counts[t]} {t}" for t in issue_types if counts[t] > 0]
    return f"{folder_name}\t{', '.join(parts)}"


def build_argparser(description, default_products_dir, issue_types):
    """Return a configured ArgumentParser with --products-dir, --issue, --details, --min-count."""
    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--products-dir",
        default=str(default_products_dir),
        help="Path to the products directory (auto-detected by default)",
    )
    parser.add_argument(
        "--issue",
        help=f"Filter to folders with this issue type. One of: {', '.join(issue_types)}",
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
    return parser


def run_reporter(folder_issues, args, issue_types, detail_header=None):
    """
    Print audit results to stdout.

    Args:
        folder_issues : dict mapping Path → list[issue dict]
        args          : parsed argparse namespace with .issue, .details, .min_count
        issue_types   : ordered list of all issue type names for summary formatting
        detail_header : column names for --details rows (defaults to DETAIL_HEADER)
    """
    if detail_header is None:
        detail_header = DETAIL_HEADER

    if not folder_issues:
        print("OK - no issues found")
        return

    if args.issue:
        matching = [
            (folder, issues)
            for folder, issues in folder_issues.items()
            if sum(1 for i in issues if i["issue"] == args.issue) >= args.min_count
        ]
        matching.sort(key=lambda item: -sum(1 for i in item[1] if i["issue"] == args.issue))

        if not matching:
            print(f"OK - no {args.issue} issues found (min-count={args.min_count})")
            return

        total = sum(
            sum(1 for i in issues if i["issue"] == args.issue)
            for _, issues in matching
        )
        print(f"# {args.issue}: {total} occurrences in {len(matching)} folders\n")

        if args.details:
            print("\t".join(["folder"] + detail_header))
            for folder, issues in matching:
                filtered = [i for i in issues if i["issue"] == args.issue]
                for issue in sorted(filtered, key=lambda x: x.get("source_id", "")):
                    row_vals = [folder.name] + [issue.get(col, "") for col in detail_header]
                    print("\t".join(row_vals))
        else:
            for folder, issues in matching:
                count = sum(1 for i in issues if i["issue"] == args.issue)
                print(f"{count}\t{folder.name}")

    else:
        ranked = sorted(folder_issues.items(), key=lambda item: -len(item[1]))
        total_issues = sum(len(issues) for issues in folder_issues.values())
        print(f"# {len(folder_issues)} folders with issues, {total_issues} total\n")
        for folder, issues in ranked:
            counts = Counter(i["issue"] for i in issues)
            print(format_summary_line(folder.name, counts, issue_types))
