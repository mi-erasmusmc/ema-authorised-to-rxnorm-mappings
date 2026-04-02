#!/usr/bin/env python3
"""
Validate Spain product folders and report issues.

Usage:
    python3 .claude/skills/map-spain-drugs/validate_all.py                          # all folders
    python3 .claude/skills/map-spain-drugs/validate_all.py data/spain/products/foo/  # single folder
    python3 .claude/skills/map-spain-drugs/validate_all.py data/spain/products/foo/ --details
    python3 .claude/skills/map-spain-drugs/validate_all.py --issue MISSING --details
    python3 .claude/skills/map-spain-drugs/validate_all.py --issue INVALID --invalid-reason "dose form"
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "map-drugs"))

import validate_core as core  # noqa: E402

# Spain detail header includes nro_definitivo as an extra column.
DETAIL_HEADER = [
    "issue",
    "source_id",
    "nro_definitivo",
    "description",
    "concept_id",
    "concept_name",
    "mapping_type",
]

VALIDATOR_CONFIG = {
    "id_col": "cod_nacion",
    "suppressions_path_fn": lambda folder: folder.parent.parent / "suppressions.tsv",
    "display_name_fn": lambda folder: folder.name,
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


def validate_folder(folder: Path, suppressions=None):
    """Return a list of issue dicts for a product folder. Empty list = clean."""
    data_path = folder / "data.tsv"
    mapping_path = folder / "mapping.tsv"

    if not data_path.exists():
        return []

    data_rows = core.load_tsv(data_path)
    data_by_cod = {core.clean(row["cod_nacion"]): row for row in data_rows}
    mapping_rows = core.load_tsv(mapping_path) if mapping_path.exists() else []

    describe = lambda row: core.clean(row.get("des_dcp", ""))  # noqa: E731

    issues = core.run_common_checks("cod_nacion", data_rows, mapping_rows, describe=describe)
    issues += core.validate_folder_issues(mapping_path)

    # Spain-specific: NRO_MISMATCH
    for row in mapping_rows:
        cod = core.clean(row.get("cod_nacion", ""))
        if cod not in data_by_cod:
            continue
        data_row = data_by_cod[cod]
        source_nro = core.clean(data_row.get("nro_definitivo", ""))
        mapped_nro = core.clean(row.get("nro_definitivo", ""))

        if source_nro and mapped_nro and source_nro != mapped_nro:
            issues.append(core.make_issue(
                "NRO_MISMATCH", cod, describe(data_row),
                core.clean(row.get("concept_id", "")),
                core.clean(row.get("concept_name", "")),
                core.clean(row.get("mapping_type", "")),
                nro_definitivo=mapped_nro,
            ))

    # Volume/injection checks
    def spain_extra_fields(row, data_row):
        return {"nro_definitivo": core.clean(row.get("nro_definitivo", ""))}

    issues += core.check_volume_issues(
        "cod_nacion", data_by_cod, mapping_rows, describe,
        volume_review_kwargs=dict(
            description_key="des_dcp",
            unit_key="unidad_contenido",
            form_key="forma_farmaceutica",
            injectable_unit_markers=("inye",),
            injectable_form_markers=("inyect",),
        ),
        skip_packs=False,
        skip_overfill_comment=False,
        extra_fields_fn=spain_extra_fields,
    )

    # Inconsistency checks
    def spain_sig(data_row):
        des_dcp = core.clean(data_row.get("des_dcp", ""))
        if not des_dcp:
            return None
        sw_generico = core.clean(data_row.get("sw_generico", ""))
        forma = core.clean(data_row.get("forma_farmaceutica", ""))
        if sw_generico == "0":
            return (des_dcp, sw_generico, forma, branded_signature_key(data_row))
        return (des_dcp, sw_generico, forma)

    issues += core.check_inconsistent_concepts(
        "cod_nacion", data_by_cod, mapping_rows, sig_fn=spain_sig, describe=describe,
    )
    issues += core.check_inconsistent_types(
        "cod_nacion", data_by_cod, mapping_rows, sig_fn=spain_sig, describe=describe,
    )

    if suppressions:
        issues = core.apply_suppressions(issues, folder.name, suppressions)

    return issues


def discover_folders(products_dir: Path):
    return sorted(p for p in products_dir.iterdir() if p.is_dir() and (p / "data.tsv").exists())


def main():
    script_dir = Path(__file__).parent
    default_products = script_dir.parent.parent.parent / "data" / "spain" / "products"

    core.run_validator(
        id_col="cod_nacion",
        default_products=default_products,
        issue_types=core.SPAIN_ISSUE_TYPES,
        validate_fn=validate_folder,
        discover_fn=discover_folders,
        description="Validate Spain product folders.",
        detail_header=DETAIL_HEADER,
        sort_key="source_id",
    )


if __name__ == "__main__":
    main()
