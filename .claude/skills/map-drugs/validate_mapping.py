#!/usr/bin/env python3
"""Validate mapping.tsv files for correct structure and data types.

Usage:
    python3 .claude/skills/map-drugs/validate_mapping.py <path_to_mapping.tsv> [...]

Validates:
- last_updated_date is YYYY-MM-DD formatted and not null
- concept_id is a number or empty
- mapping_type is EXACT, BROAD, NO_MAPPING, or empty
- EXACT and BROAD require concept_id, concept_name, and concept_code (use NO_MAPPING if no mapping exists)
- EXACT mappings must include a strength value in the concept name (use BROAD if only ingredient-level concepts exist)
- suggestion is not identical to concept_name, including a concept_name plus only a [brand] suffix
- suggestion is not a stray YYYY-MM-DD value
- suggestion does not contain pipe-delimited pseudo-records
- non-empty suggestions contain a recognized RxNorm dose form

Exit code 0 if all files pass, 1 if any errors found.
"""

import csv
import json
from pathlib import Path
import re
import sys

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
BRAND_SUFFIX_RE = re.compile(r"^(?P<base>.+?) \[[^\]]+\]$")
# Matches a strength value+unit anywhere in the concept name (e.g. "20 MG/ML", "5000 UNT").
# Used to detect bare clinical drug components (ingredient+strength, no dose form).
STRENGTH_IN_NAME_RE = re.compile(
    r"\b\d+(?:\.\d+)?\s*(?:MG|UNT|MEQ|ACTUAT|MCI)\b",
    re.IGNORECASE,
)
EXACT_INJECTION_CONCENTRATION_RE = re.compile(r"/ML\b.*\bInjection\b", re.IGNORECASE)
LEADING_VOLUME_RE = re.compile(r"^\d+(?:\.\d+)?\s*ML\b", re.IGNORECASE)
PACK_LEADING_VOLUME_RE = re.compile(r"^\{\s*\d+\s*\(\s*\d+(?:\.\d+)?\s*ML\b", re.IGNORECASE)
# Contrast agents and similar compounds where RxNorm intentionally omits dose form
# from the concept name. EXACT is accepted for these even without a dose form.
# Key: concept_code (RxNorm CUI code, the stable identifier).
EXACT_NO_DOSE_FORM_EXEMPT_CODES = {
    "440782",       # iopamidol 612 MG/ML
    "328359",       # iopamidol 760 MG/ML
    # OMOP extension concepts for EU-only indacaterol strengths (150/300 µg).
    # These use the deprecated dose form term "Inhalant Powder" instead of "Inhalation Powder".
    # No standard RxNorm concept exists at these strengths.
    "OMOP1001937",  # indacaterol 0.15 MG Inhalant Powder
    "OMOP999050",   # indacaterol 0.3 MG Inhalant Powder
    # OMOP extension concept for EU-only indacaterol/glycopyrronium strength (85/43 µg).
    # Uses deprecated "Inhalant Powder"; no standard RxNorm concept at these strengths.
    "OMOP3108030",  # glycopyrronium 0.044 MG / indacaterol 0.085 MG Inhalant Powder
    # OMOP extension concepts for EU-only Trimbow (beclomethasone/formoterol/glycopyrronium).
    # Not marketed in the US; no standard RxNorm concepts exist.
    "OMOP4776211",  # Beclomethasone 0.084 MG/ACTUAT / formoterol 0.005 MG/ACTUAT / glycopyrronium 0.009 MG/ACTUAT Inhalant Solution [Trimbow]
    "OMOP4711822",  # Beclomethasone 0.084 MG/ACTUAT / formoterol 0.005 MG/ACTUAT / glycopyrronium 0.009 MG/ACTUAT Inhalant Powder [Trimbow]
    # OMOP extension concept for amorolfine medicated nail lacquer.
    # Uses "Medicated nail lacquer", a European dose form term not in RxNorm's standard vocabulary.
    # No standard RxNorm nail lacquer concept exists.
    "OMOP412029",   # Amorolfine 50 MG/ML Medicated nail lacquer
    # OMOP extension concepts for misoprostol vaginal presentations.
    # "Vaginal Tablet" and "Vaginal delivery system" are EU dose form terms not in RxNorm's standard vocabulary.
    # No standard RxNorm vaginal-tablet or vaginal-delivery-system concept for misoprostol exists.
    "OMOP5579822",  # misoprostol 0.2 MG Vaginal Tablet
    "OMOP3120717",  # Misoprostol 0.2 MG Vaginal delivery system
}

VALID_MAPPING_TYPES = {"EXACT", "BROAD", "NO_MAPPING", ""}

VALID_ID_COLUMNS = {"ma_number", "product_id", "cod_nacion"}
# Extra columns that follow the first ID column for certain formats
EXTRA_ID_COLUMNS = {"cod_nacion": ["nro_definitivo"]}
REQUIRED_COLUMNS = [
    "concept_id", "concept_name", "concept_code",
    "mapping_type", "comment", "suggestion", "last_updated_date",
]
DOSE_FORM_LOOKUP_PATH = Path(__file__).with_name("dose_form_lookup.json")


def load_dose_forms() -> list[str]:
    with DOSE_FORM_LOOKUP_PATH.open() as f:
        data = json.load(f)
    names = [item["name"].strip() for item in data if item.get("name")]
    # Match more specific dose forms first.
    return sorted(names, key=len, reverse=True)


VALID_DOSE_FORMS = load_dose_forms()
SUGGESTION_OPTIONAL_FILES = {
    Path("data/spain/products/multicomponente/mapping.tsv"),
}


BRAND_END_RE = re.compile(r"\[[^\]]+\]$")


def suggestion_has_valid_dose_form(suggestion: str) -> bool:
    lower_suggestion = suggestion.casefold()
    return any(dose_form.casefold() in lower_suggestion for dose_form in VALID_DOSE_FORMS)


def suggestion_has_valid_ending(suggestion: str) -> bool:
    """Suggestion must end with a dose form, a [brand] suffix, or 'Pack'."""
    if BRAND_END_RE.search(suggestion):
        return True
    if suggestion.casefold().endswith("pack"):
        return True
    lower = suggestion.casefold()
    return any(lower.endswith(df.casefold()) for df in VALID_DOSE_FORMS)


def _read_atc_code(mapping_path: Path) -> str:
    """Return the ATC code for the product folder, or '' if not found.

    Checks (in order):
    - ema-info.txt:  line starting with 'ATC code (human):'
    - data.tsv:      'atc' column (value may be 'CODE - Name'; only the code part is returned)
    """
    info_path = mapping_path.parent / "ema-info.txt"
    if info_path.exists():
        for line in info_path.read_text(encoding="utf-8").splitlines():
            if line.startswith("ATC code (human):"):
                return line.split(":", 1)[1].strip()

    data_path = mapping_path.parent / "data.tsv"
    if data_path.exists():
        with open(data_path, newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh, delimiter="\t")
            for row in reader:
                atc = (row.get("atc") or "").strip()
                if atc:
                    return atc.split(" - ")[0].strip()

    return ""


def validate_file(path: str) -> list[str]:
    errors = []
    normalized_path = Path(path)
    atc_code = _read_atc_code(normalized_path)
    try:
        with open(path, newline="") as f:
            reader = csv.DictReader(f, delimiter="\t")
            fields = reader.fieldnames or []

            # Check ID column (first column)
            if not fields or fields[0] not in VALID_ID_COLUMNS:
                errors.append(
                    f"  First column must be one of {sorted(VALID_ID_COLUMNS)}, "
                    f"got '{fields[0] if fields else '(empty)'}'"
                )
                return errors

            # Check required columns are present
            missing = [c for c in REQUIRED_COLUMNS if c not in fields]
            if missing:
                errors.append(f"  Missing required columns: {missing}")
                return errors

            extra = EXTRA_ID_COLUMNS.get(fields[0], [])
            expected = [fields[0]] + extra + REQUIRED_COLUMNS
            if fields != expected:
                errors.append(
                    f"  Column order mismatch: expected {expected}, "
                    f"got {fields}"
                )
                return errors

            atc_v = atc_code.upper().startswith("V")

            for i, row in enumerate(reader, start=2):
                line = f"line {i}"

                # last_updated_date: required, YYYY-MM-DD
                date = row.get("last_updated_date", "").strip()
                if not date:
                    errors.append(f"  {line}: last_updated_date is empty")
                elif not DATE_RE.match(date):
                    errors.append(
                        f"  {line}: last_updated_date '{date}' is not YYYY-MM-DD"
                    )

                # concept_id: number or empty
                cid = row.get("concept_id", "").strip()
                if cid and not cid.isdigit():
                    errors.append(
                        f"  {line}: concept_id '{cid}' is not a number"
                    )

                # mapping_type: EXACT, BROAD, NO_MAPPING, or empty
                mt = row.get("mapping_type", "").strip()
                if mt not in VALID_MAPPING_TYPES:
                    errors.append(
                        f"  {line}: mapping_type '{mt}' is not EXACT, BROAD, NO_MAPPING, or empty"
                    )

                # EXACT and BROAD require concept_id, concept_name, and concept_code.
                # If no mapping is possible, use NO_MAPPING instead.
                concept_name = row.get("concept_name", "").strip()
                concept_code = row.get("concept_code", "").strip()
                if mt in ("EXACT", "BROAD"):
                    if not cid:
                        errors.append(
                            f"  {line}: {mt} mappings require concept_id; "
                            f"if no mapping is available use NO_MAPPING"
                        )
                    if not concept_name:
                        errors.append(
                            f"  {line}: {mt} mappings require concept_name; "
                            f"if no mapping is available use NO_MAPPING"
                        )
                    if not concept_code:
                        errors.append(
                            f"  {line}: {mt} mappings require concept_code; "
                            f"if no mapping is available use NO_MAPPING"
                        )

                # EXACT mappings must specify a strength in the concept name (indicated by any digit).
                # Concepts with truncated names (ending "...") are skipped: the strength may be cut off.
                # Products with ATC codes starting with V (e.g. contrast media, diagnostics) are exempt:
                # RxNorm often omits strength for these.
                if (mt == "EXACT" and concept_name
                        and not concept_name.endswith("...")
                        and not atc_v
                        and not re.search(r'\d', concept_name)):
                    errors.append(
                        f"  {line}: EXACT concept '{concept_name[:80]}' has no strength; "
                        f"use BROAD if no strength-specific concept exists"
                    )

                # EXACT mappings to bare clinical drug components (has strength, no dose form) are invalid.
                # Concepts with truncated names (ending "...") are skipped: the dose form may be cut off.
                # Contrast agents and similar compounds are exempt via EXACT_NO_DOSE_FORM_EXEMPT_CODES.
                if (mt == "EXACT" and concept_name
                        and not concept_name.endswith("...")
                        and concept_code not in EXACT_NO_DOSE_FORM_EXEMPT_CODES
                        and STRENGTH_IN_NAME_RE.search(concept_name)
                        and not suggestion_has_valid_dose_form(concept_name)):
                    errors.append(
                        f"  {line}: EXACT concept '{concept_name[:80]}' has a strength but no "
                        f"dose form; use BROAD if no dose-form-specific concept exists"
                    )

                # EXACT concentration-style Injection concepts must start with an explicit volume.
                if (mt == "EXACT" and concept_name
                        and not concept_name.endswith("...")
                        and EXACT_INJECTION_CONCENTRATION_RE.search(concept_name)
                        and not LEADING_VOLUME_RE.search(concept_name)
                        and not PACK_LEADING_VOLUME_RE.search(concept_name)):
                    errors.append(
                        f"  {line}: EXACT concept '{concept_name[:80]}' uses /ML Injection without a leading volume; "
                        f"use a volume-specific concept or downgrade to BROAD"
                    )

                # BROAD and NO_MAPPING mappings require a suggestion
                # Products with ATC codes starting with V are exempt (diagnostics/contrast media).
                suggestion = row.get("suggestion", "").strip()
                suggestion_required = (
                    normalized_path not in SUGGESTION_OPTIONAL_FILES
                    and not atc_v
                )
                if mt == "BROAD" and suggestion_required and not suggestion:
                    errors.append(
                        f"  {line}: BROAD mappings require suggestion"
                    )
                if mt == "NO_MAPPING" and suggestion_required and not suggestion:
                    errors.append(
                        f"  {line}: NO_MAPPING mappings require suggestion"
                    )
                if suggestion:
                    if suggestion.casefold() == concept_name.casefold():
                        errors.append(
                            f"  {line}: suggestion must not equal concept_name"
                        )
                    m = BRAND_SUFFIX_RE.fullmatch(suggestion)
                    if m and m.group("base").casefold() == concept_name.casefold():
                        errors.append(
                            f"  {line}: suggestion must not differ from concept_name only by brand suffix"
                        )
                    if DATE_RE.fullmatch(suggestion):
                        errors.append(
                            f"  {line}: suggestion must not be a date"
                        )
                    if "|" in suggestion:
                        errors.append(
                            f"  {line}: suggestion must not contain pipe-delimited data"
                        )
                    if not suggestion_has_valid_dose_form(suggestion):
                        errors.append(
                            f"  {line}: suggestion must contain a valid dose form from dose_form_lookup.json"
                        )
                    if not suggestion_has_valid_ending(suggestion):
                        errors.append(
                            f"  {line}: suggestion must end with a dose form, [Brand], or 'Pack'"
                        )

    except FileNotFoundError:
        errors.append(f"  File not found: {path}")
    except Exception as e:
        errors.append(f"  Error reading file: {e}")

    return errors


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <mapping.tsv> [...]", file=sys.stderr)
        sys.exit(2)

    has_errors = False
    for path in sys.argv[1:]:
        errors = validate_file(path)
        if errors:
            has_errors = True
            print(f"FAIL {path}")
            for e in errors:
                print(e)
        else:
            print(f"OK   {path}")

    sys.exit(1 if has_errors else 0)


if __name__ == "__main__":
    main()
