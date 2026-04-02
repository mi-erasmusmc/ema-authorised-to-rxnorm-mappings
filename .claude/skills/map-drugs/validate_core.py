#!/usr/bin/env python3
"""
Shared validation utilities for drug mapping folders (EMA, Spain, Latvia, ...).

Provides common data-quality checks, structural validation via validate_mapping.py,
and reporter helpers reused across source-specific validation scripts.

Issue dict schema (returned by run_common_checks and validate_folder_issues):
    issue        str  -- issue type name
    source_id    str  -- source-specific ID (ma_number, cod_nacion, ...)
    description  str  -- human-readable label for the row
    concept_id   str  -- mapped concept_id (may be empty)
    concept_name str  -- mapped concept_name (may be empty)
    mapping_type str  -- EXACT, BROAD, NO_MAPPING, or empty

Extra source-specific fields (e.g. nro_definitivo) may also be present.
"""

import argparse
import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from validate_mapping import COMMON_CHECK_OVERLAP_CODES, validate_file  # noqa: E402


# -- Issue type registry -------------------------------------------------------

STRUCTURAL_ISSUE_TYPES = [
    "EMPTY_DATE",
    "BAD_DATE",
    "BAD_CONCEPT_ID",
    "BAD_MAPPING_TYPE",
    "EXACT_NO_STRENGTH",
    "EXACT_NO_DOSE_FORM",
    "EXACT_NO_VOLUME",
    "BAD_SUGGESTION",
    "INVALID_STRUCTURE",
]

COMMON_ISSUE_TYPES = [
    "MISSING",
    "STALE_MAPPING",
    "NO_CONCEPT",
    "NO_TYPE",
    "BROAD",
    "NO_MAPPING",
    "REVIEW_VOLUME",
    "REVIEW_INJECTION_FORM",
    "DUPLICATE_DATA",
    "DUPLICATE_MAPPING",
    "INCONSISTENT_CONCEPT",
    "INCONSISTENT_TYPE",
]

EMA_ISSUE_TYPES = ["UNMAPPED_FOLDER", "NO_DATE"] + COMMON_ISSUE_TYPES + STRUCTURAL_ISSUE_TYPES
SPAIN_ISSUE_TYPES = ["NRO_MISMATCH"] + COMMON_ISSUE_TYPES + STRUCTURAL_ISSUE_TYPES
LATVIA_ISSUE_TYPES = ["UNMAPPED_FOLDER"] + COMMON_ISSUE_TYPES + STRUCTURAL_ISSUE_TYPES

DETAIL_HEADER = [
    "issue",
    "source_id",
    "description",
    "concept_id",
    "concept_name",
    "mapping_type",
]


# -- Utilities -----------------------------------------------------------------

def load_tsv(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def clean(value):
    return str(value).strip() if value is not None else ""


def duplicate_values(rows, key):
    counts = Counter(clean(row.get(key, "")) for row in rows if clean(row.get(key, "")))
    return sorted(v for v, c in counts.items() if c > 1)


def make_issue(issue, source_id, description, concept_id, concept_name, mapping_type, **extra):
    d = {
        "issue": clean(issue),
        "source_id": clean(source_id),
        "description": clean(description),
        "concept_id": clean(concept_id),
        "concept_name": clean(concept_name),
        "mapping_type": clean(mapping_type),
    }
    for k, v in extra.items():
        d[k] = clean(v)
    return d


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


MULTIUSE_INJECTION_FORM_RE = re.compile(
    r"\bInjectable (?:Solution|Suspension)\b",
    re.IGNORECASE,
)
LEADING_VOLUME_RE = re.compile(r"^\d+(?:\.\d+)?\s*ML\b", re.IGNORECASE)
CONCENTRATION_STRENGTH_RE = re.compile(
    r"\b\d+(?:\.\d+)?\s*(?:MG|MCG|UG|G|UNT|IU|UI|MEQ|MMOL|MCI|PFU)\s*/\s*(?:ML|L)\b",
    re.IGNORECASE,
)


def needs_injection_form_review(concept_name):
    concept = clean(concept_name)
    if not concept:
        return False
    if not MULTIUSE_INJECTION_FORM_RE.search(concept):
        return False
    if not LEADING_VOLUME_RE.search(concept):
        return False
    return bool(CONCENTRATION_STRENGTH_RE.search(concept))


def check_volume_issues(
    source_id_col, data_by_id, mapping_rows, describe,
    volume_review_kwargs,
    skip_packs=True,
    skip_overfill_comment=True,
    extra_fields_fn=None,
):
    """Check REVIEW_VOLUME and REVIEW_INJECTION_FORM for EXACT mapping rows."""
    issues = []
    for row in mapping_rows:
        sid = clean(row.get(source_id_col, ""))
        if sid not in data_by_id:
            continue
        mapping_type = clean(row.get("mapping_type", ""))
        if mapping_type != "EXACT":
            continue
        concept_name = clean(row.get("concept_name", ""))
        if skip_packs and (concept_name.startswith("{") or concept_name.endswith("Pack")):
            continue
        if skip_overfill_comment:
            comment = clean(row.get("comment", "")).lower()
            if "overfill" in comment or "deliverable dose" in comment:
                continue
        data_row = data_by_id[sid]
        concept_id = clean(row.get("concept_id", ""))
        extra = extra_fields_fn(row, data_row) if extra_fields_fn else {}
        if needs_volume_review(data_row, concept_name, **volume_review_kwargs):
            issues.append(make_issue(
                "REVIEW_VOLUME", sid, describe(data_row),
                concept_id, concept_name, mapping_type, **extra,
            ))
        if needs_injection_form_review(concept_name):
            issues.append(make_issue(
                "REVIEW_INJECTION_FORM", sid, describe(data_row),
                concept_id, concept_name, mapping_type, **extra,
            ))
    return issues


# -- Suppressions --------------------------------------------------------------

def load_suppressions(path, id_col="source_id"):
    """Load a suppressions.tsv and return {folder_name: set of (issue, source_id)}.

    The TSV must have columns: folder, issue, <id_col>.
    Use id_col="*" rows to suppress all rows of an issue type in a folder.
    """
    result = {}
    if not Path(path).exists():
        return result
    rows = load_tsv(path)
    for row in rows:
        folder_name = clean(row.get("folder", ""))
        issue = clean(row.get("issue", ""))
        sid = clean(row.get(id_col, ""))
        if folder_name and issue:
            result.setdefault(folder_name, set()).add((issue, sid))
    return result


def apply_suppressions(issues, folder_name, suppressions, id_key="source_id"):
    """Filter issues using the suppressions dict from load_suppressions.

    Supports both per-row suppression (issue, specific_id) and
    wildcard suppression (issue, "*") which suppresses all rows of that issue type.
    """
    suppressed = suppressions.get(folder_name, set())
    if not suppressed:
        return issues
    wildcard_issues = {issue for issue, sid in suppressed if sid == "*"}
    return [
        i for i in issues
        if i["issue"] not in wildcard_issues
        and (i["issue"], i.get(id_key, "")) not in suppressed
    ]


# -- Common checks -------------------------------------------------------------

def run_common_checks(source_id_col, data_rows, mapping_rows, describe=None):
    """
    Run the common mapping quality checks shared across all data sources.

    Args:
        source_id_col : column name for the source ID (e.g. "ma_number", "cod_nacion")
        data_rows     : list of dicts from the source data file
        mapping_rows  : list of dicts read from mapping.tsv
        describe      : optional callable(data_row) -> str for human-readable row labels

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

    Returns a list of issue dicts, one per structural error found.
    Skips errors whose codes overlap with common checks (NO_CONCEPT, BROAD, NO_MAPPING)
    to avoid double-counting.
    """
    if not Path(mapping_path).exists():
        return []
    errors = validate_file(str(mapping_path))
    return [
        make_issue(code, "", msg.strip(), "", "", "")
        for code, msg in errors
        if code not in COMMON_CHECK_OVERLAP_CODES
    ]


def _check_inconsistency(issue_name, source_id_col, data_by_id, mapping_rows, sig_fn,
                         describe, group_key_fn, divergence_field, row_filter):
    """Shared implementation for inconsistency checks.

    Groups mapping rows by group_key_fn(sig, row), then flags groups where
    divergence_field takes more than one distinct value.
    """
    if describe is None:
        describe = lambda row: ""  # noqa: E731

    key_to_values = defaultdict(set)
    key_to_rows = defaultdict(list)

    for row in mapping_rows:
        sid = clean(row.get(source_id_col, ""))
        concept_id = clean(row.get("concept_id", ""))
        mapping_type = clean(row.get("mapping_type", ""))
        if not row_filter(concept_id, mapping_type):
            continue
        data_row = data_by_id.get(sid)
        if data_row is None:
            continue
        sig = sig_fn(data_row)
        if sig is None:
            continue
        key = group_key_fn(sig, row)
        key_to_values[key].add(clean(row.get(divergence_field, "")))
        key_to_rows[key].append(row)

    issues = []
    for key, values in key_to_values.items():
        if len(values) > 1:
            for row in key_to_rows[key]:
                sid = clean(row.get(source_id_col, ""))
                data_row = data_by_id.get(sid, {})
                issues.append(make_issue(
                    issue_name,
                    sid,
                    describe(data_row),
                    clean(row.get("concept_id", "")),
                    clean(row.get("concept_name", "")),
                    clean(row.get("mapping_type", "")),
                ))
    return issues


def check_inconsistent_concepts(source_id_col, data_by_id, mapping_rows, sig_fn, describe=None):
    """Detect EXACT rows sharing a clinical signature but using different concept_ids."""
    return _check_inconsistency(
        "INCONSISTENT_CONCEPT", source_id_col, data_by_id, mapping_rows, sig_fn, describe,
        group_key_fn=lambda sig, row: sig,
        divergence_field="concept_id",
        row_filter=lambda cid, mt: cid and mt == "EXACT",
    )


def check_inconsistent_types(source_id_col, data_by_id, mapping_rows, sig_fn, describe=None):
    """Detect rows sharing a clinical signature and concept_id but using different mapping_types."""
    return _check_inconsistency(
        "INCONSISTENT_TYPE", source_id_col, data_by_id, mapping_rows, sig_fn, describe,
        group_key_fn=lambda sig, row: (sig, clean(row.get("concept_id", ""))),
        divergence_field="mapping_type",
        row_filter=lambda cid, mt: cid and mt,
    )


# -- Reporter ------------------------------------------------------------------

def format_summary_line(folder_name, counts, issue_types):
    parts = [f"{counts[t]} {t}" for t in issue_types if counts[t] > 0]
    return f"{folder_name}\t{', '.join(parts)}"


def build_argparser(description, default_products_dir, issue_types):
    """Return a configured ArgumentParser with folder, --products-dir, --issue, --details, --min-count."""
    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "folder",
        nargs="?",
        help="Single folder to validate. Omit to validate all folders.",
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
        help="Print row-level TSV for matching folders (requires --issue in multi-folder mode)",
    )
    parser.add_argument(
        "--min-count",
        type=int,
        default=1,
        metavar="N",
        help="Only show folders with at least N occurrences of the issue (default: 1)",
    )
    return parser


def parse_standard_args(parser):
    """Parse args from a build_argparser()-created parser with standard validation."""
    args = parser.parse_args()
    if args.issue:
        args.issue = args.issue.strip().upper()
    # In multi-folder mode, --details requires --issue
    if args.details and not args.issue and not args.folder:
        parser.error("--details requires --issue")
    return args


def run_reporter(folder_issues, args, issue_types, detail_header=None, sort_key="source_id",
                 display_name_fn=None):
    """
    Print validation results to stdout.

    Args:
        folder_issues    : dict mapping Path -> list[issue dict]
        args             : parsed argparse namespace with .issue, .details, .min_count
        issue_types      : ordered list of all issue type names for summary formatting
        detail_header    : column names for --details rows (defaults to DETAIL_HEADER)
        sort_key         : issue dict key to sort detail rows by (default: "source_id")
        display_name_fn  : callable(folder) -> str (default: folder.name)
    """
    if detail_header is None:
        detail_header = DETAIL_HEADER
    if display_name_fn is None:
        display_name_fn = lambda f: f.name  # noqa: E731

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
                for issue in sorted(filtered, key=lambda x: x.get(sort_key, "")):
                    row_vals = [display_name_fn(folder)] + [issue.get(col, "") for col in detail_header]
                    print("\t".join(row_vals))
        else:
            for folder, issues in matching:
                count = sum(1 for i in issues if i["issue"] == args.issue)
                print(f"{count}\t{display_name_fn(folder)}")

    else:
        ranked = sorted(folder_issues.items(), key=lambda item: -len(item[1]))
        total_issues = sum(len(issues) for issues in folder_issues.values())
        print(f"# {len(folder_issues)} folders with issues, {total_issues} total\n")
        for folder, issues in ranked:
            counts = Counter(i["issue"] for i in issues)
            print(format_summary_line(display_name_fn(folder), counts, issue_types))


def run_single_folder_reporter(folder_name, issues, args, detail_header=None):
    """
    Print single-folder validation results to stdout.

    Default output shows a summary line followed by grouped pattern counts per issue type.
    With --details, prints row-level TSV. --issue filters to one issue type in either mode.
    """
    if detail_header is None:
        detail_header = DETAIL_HEADER

    if not issues:
        print("OK - no issues found")
        return

    issue_filter = args.issue if hasattr(args, "issue") else None

    if args.details:
        filtered = [i for i in issues if not issue_filter or i["issue"] == issue_filter]
        if not filtered:
            print(f"OK - no {issue_filter} issues found")
            return
        print("\t".join(detail_header))
        for issue in sorted(filtered, key=lambda i: (i["issue"], i.get("source_id", ""))):
            print("\t".join(issue.get(col, "") for col in detail_header))
        return

    # Summary with pattern grouping
    counts = Counter(i["issue"] for i in issues)
    summary_parts = [f"{c} {t}" for t, c in sorted(counts.items())]
    print(f"# {folder_name}: {', '.join(summary_parts)}")
    print()

    grouped = {}
    for issue in issues:
        issue_type = issue["issue"]
        label = issue["description"] or issue["concept_name"] or issue["source_id"]
        grouped.setdefault(issue_type, Counter())[label] += 1

    issue_hints = {
        "REVIEW_INJECTION_FORM": (
            "Injectable Solution/Suspension is a multi-use container form: the leading volume is "
            "packaging size, not dose. Use the concentration-only concept or switch to a single-use dose form if that is more accurate."
        ),
        "REVIEW_VOLUME": (
            "Single-use injectable mapped to a concentration-only concept. "
            "A volume-specific concept (e.g. '2 ML drug 5 MG/ML Injection') may be available and should be used for EXACT."
        ),
    }

    for issue_type in sorted(grouped):
        if issue_filter and issue_type != issue_filter:
            continue
        print(f"[{issue_type}]")
        if issue_type in issue_hints:
            print(f"  {issue_hints[issue_type]}")
        for label, count in grouped[issue_type].most_common():
            print(f"{count}\t{label}")
        print()


def run_validator(
    *,
    id_col,
    default_products,
    issue_types,
    validate_fn,
    discover_fn,
    description="Validate product folders.",
    suppressions_path_fn=None,
    display_name_fn=None,
    detail_header=None,
    sort_key="source_id",
    skip_filter=None,
):
    """Unified main() for source-specific validators.

    Args:
        id_col: source ID column name (e.g. "ma_number")
        default_products: default path to the products directory
        issue_types: ordered list of issue type names
        validate_fn: callable(folder, suppressions=...) -> list[dict]
        discover_fn: callable(products_dir) -> list[Path]
        description: argparser description
        suppressions_path_fn: callable(folder) -> Path for single-folder mode
            (default: folder.parent.parent / "suppressions.tsv")
        display_name_fn: callable(folder) -> str (default: folder.name)
        detail_header: column names for --details rows
        sort_key: issue dict key to sort detail rows by
        skip_filter: callable(issues) -> bool, skip folder in multi-mode if True
    """
    if suppressions_path_fn is None:
        suppressions_path_fn = lambda f: f.parent.parent / "suppressions.tsv"  # noqa: E731
    if display_name_fn is None:
        display_name_fn = lambda f: f.name  # noqa: E731

    parser = build_argparser(description, default_products, issue_types)
    args = parse_standard_args(parser)

    if args.folder:
        folder = Path(args.folder)
        suppressions_path = suppressions_path_fn(folder)
        suppressions = load_suppressions(suppressions_path, id_col=id_col)
        issues = validate_fn(folder, suppressions=suppressions)
        run_single_folder_reporter(
            display_name_fn(folder), issues, args, detail_header=detail_header,
        )
        return

    products_dir = Path(args.products_dir)
    if not products_dir.is_dir():
        print(f"ERROR: {products_dir} not found", file=sys.stderr)
        sys.exit(1)

    suppressions_path = products_dir.parent / "suppressions.tsv"
    suppressions = load_suppressions(suppressions_path, id_col=id_col)

    folder_issues = {}
    for folder in discover_fn(products_dir):
        issues = validate_fn(folder, suppressions=suppressions)
        if issues:
            if skip_filter and skip_filter(issues):
                continue
            folder_issues[folder] = issues

    run_reporter(
        folder_issues, args, issue_types,
        detail_header=detail_header, sort_key=sort_key,
        display_name_fn=display_name_fn,
    )
