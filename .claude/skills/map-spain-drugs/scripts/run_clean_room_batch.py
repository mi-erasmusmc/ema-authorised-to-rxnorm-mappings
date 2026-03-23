#!/usr/bin/env python3
"""
Run conservative clean-room Spain mapping batches.

This script only auto-applies updates when every missing row in a folder can be
filled from an existing EXACT mapping in the same folder using the same full
clinical pattern key. It is intended for low-risk bulk cleanup, not fresh
concept discovery.

Usage:
    python3 .claude/skills/map-spain-drugs/scripts/run_clean_room_batch.py
    python3 .claude/skills/map-spain-drugs/scripts/run_clean_room_batch.py --apply
    python3 .claude/skills/map-spain-drugs/scripts/run_clean_room_batch.py --apply --limit 60 --pass-size 3
"""

from __future__ import annotations

import argparse
import csv
import subprocess
import sys
from collections import defaultdict
from pathlib import Path


PATTERN_FIELDS = [
    "des_dcp",
    "vias_administracion",
    "forma_farmaceutica",
    "sw_generico",
    "des_dosific",
    "unidad_contenido",
]

MANIFEST_COLUMNS = [
    "pass_number",
    "folder",
    "action",
    "row_count",
    "total_rows",
    "status",
    "details",
]

UPDATE_COLUMNS = [
    "cod_nacion",
    "nro_definitivo",
    "concept_id",
    "concept_name",
    "concept_code",
    "mapping_type",
    "comment",
    "suggestion",
]


def clean(value: object) -> str:
    if value is None:
        return ""
    return str(value).strip()


def load_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def run_command(args: list[str], stdin: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        input=stdin,
        text=True,
        capture_output=True,
        check=False,
    )


def pattern_key(row: dict[str, str]) -> tuple[str, ...]:
    return tuple(clean(row.get(field, "")) for field in PATTERN_FIELDS)


def extract_ml(text: str) -> str | None:
    lowered = clean(text).lower().replace(",", ".")
    for token in lowered.split():
        if token.endswith("ml"):
            return token[:-2]
    parts = lowered.split()
    for index, token in enumerate(parts[:-1]):
        if parts[index + 1] == "ml":
            return token
    return None


def needs_volume_review(data_row: dict[str, str], concept_name: str) -> bool:
    des_dcp = clean(data_row.get("des_dcp", ""))
    unit = clean(data_row.get("unidad_contenido", "")).lower()
    form = clean(data_row.get("forma_farmaceutica", "")).lower()
    volume = extract_ml(des_dcp)
    if not volume:
        return False
    if "inye" not in unit and "inyect" not in form:
        return False
    concept_lower = clean(concept_name).lower()
    if "injection" not in concept_lower:
        return False
    if "mg/ml" not in concept_lower:
        return False
    return not concept_lower.startswith(f"{volume} ml ")


def candidate_plan(folder: Path) -> dict[str, object] | None:
    data_path = folder / "data.tsv"
    mapping_path = folder / "mapping.tsv"
    if not data_path.exists() or not mapping_path.exists():
        return None

    data_rows = load_tsv(data_path)
    mapping_rows = load_tsv(mapping_path)
    data_by_cod = {clean(row.get("cod_nacion", "")): row for row in data_rows}

    exact_by_pattern: dict[tuple[str, ...], set[tuple[str, str, str, str, str]]] = defaultdict(set)
    mapped_by_cod = {}
    missing_dates = 0

    for row in mapping_rows:
        cod = clean(row.get("cod_nacion", ""))
        mapped_by_cod[cod] = row
        mapping_type = clean(row.get("mapping_type", ""))
        concept_id = clean(row.get("concept_id", ""))
        if mapping_type == "BROAD" or not concept_id:
            return None
        if mapping_type == "EXACT" and not clean(row.get("last_updated_date", "")):
            missing_dates += 1
        if mapping_type == "EXACT" and cod in data_by_cod and needs_volume_review(data_by_cod[cod], clean(row.get("concept_name", ""))):
            return None
        if mapping_type != "EXACT" or cod not in data_by_cod:
            continue
        exact_by_pattern[pattern_key(data_by_cod[cod])].add(
            (
                concept_id,
                clean(row.get("concept_name", "")),
                clean(row.get("concept_code", "")),
                clean(row.get("comment", "")),
                clean(row.get("suggestion", "")),
            )
        )

    updates = []
    for data_row in data_rows:
        cod = clean(data_row.get("cod_nacion", ""))
        matches = exact_by_pattern.get(pattern_key(data_row), set())
        mapped_row = mapped_by_cod.get(cod)
        if not mapped_row:
            if len(matches) != 1:
                return None
            concept_id, concept_name, concept_code, comment, suggestion = next(iter(matches))
            updates.append(
                {
                    "cod_nacion": cod,
                    "nro_definitivo": clean(data_row.get("nro_definitivo", "")),
                    "concept_id": concept_id,
                    "concept_name": concept_name,
                    "concept_code": concept_code,
                    "mapping_type": "EXACT",
                    "comment": comment,
                    "suggestion": suggestion,
                }
            )
            continue

        mapping_type = clean(mapped_row.get("mapping_type", ""))
        if mapping_type == "EXACT":
            continue
        if len(matches) != 1:
            return None
        concept_id, concept_name, concept_code, comment, suggestion = next(iter(matches))
        if (
            clean(mapped_row.get("concept_id", "")) != concept_id
            or clean(mapped_row.get("concept_name", "")) != concept_name
            or clean(mapped_row.get("concept_code", "")) != concept_code
        ):
            return None
        updates.append(
            {
                "cod_nacion": cod,
                "nro_definitivo": clean(mapped_row.get("nro_definitivo", "")) or clean(data_row.get("nro_definitivo", "")),
                "concept_id": concept_id,
                "concept_name": concept_name,
                "concept_code": concept_code,
                "mapping_type": "EXACT",
                "comment": comment,
                "suggestion": suggestion,
            }
        )

    if updates:
        return {
            "folder": folder.name,
            "action": "pattern_fill",
            "row_count": len(updates),
            "total_rows": len(data_rows),
            "updates": updates,
        }
    if missing_dates:
        return {
            "folder": folder.name,
            "action": "date_backfill",
            "row_count": missing_dates,
            "total_rows": len(data_rows),
            "updates": [],
        }
    return None


def select_candidates(base: Path) -> list[dict[str, object]]:
    selected = []
    for folder in sorted(path for path in base.iterdir() if path.is_dir()):
        plan = candidate_plan(folder)
        if not plan:
            continue
        selected.append(plan)
    selected.sort(key=lambda item: (item["action"] != "pattern_fill", item["row_count"], item["total_rows"], item["folder"]))
    return selected


def build_update_tsv(rows: list[dict[str, str]]) -> str:
    lines = ["\t".join(UPDATE_COLUMNS)]
    for row in rows:
        lines.append("\t".join(clean(row.get(column, "")) for column in UPDATE_COLUMNS))
    return "\n".join(lines) + "\n"


def apply_updates(repo_root: Path, folder_name: str, updates: list[dict[str, str]]) -> tuple[str, str]:
    mapping_path = repo_root / "data" / "spain" / "products" / folder_name / "mapping.tsv"
    apply_message = "No mapping rows needed"
    if updates:
        apply_cmd = [
            "python3",
            str(repo_root / ".claude" / "skills" / "map-spain-drugs" / "apply_mappings.py"),
            str(mapping_path),
        ]
        apply_result = run_command(apply_cmd, stdin=build_update_tsv(updates))
        if apply_result.returncode != 0:
            return "apply_failed", clean(apply_result.stderr) or clean(apply_result.stdout)
        apply_message = clean(apply_result.stdout)

    backfill_cmd = [
        "python3",
        str(repo_root / ".claude" / "skills" / "map-spain-drugs" / "apply_mappings.py"),
        str(mapping_path),
        "--backfill-dates",
    ]
    backfill_result = run_command(backfill_cmd)
    if backfill_result.returncode != 0:
        return "backfill_failed", clean(backfill_result.stderr) or clean(backfill_result.stdout)

    validate_cmd = [
        "python3",
        str(repo_root / ".claude" / "skills" / "map-drugs" / "validate_mapping.py"),
        str(mapping_path),
    ]
    validate_result = run_command(validate_cmd)
    if validate_result.returncode != 0:
        return "validate_failed", clean(validate_result.stdout) or clean(validate_result.stderr)

    audit_cmd = [
        "python3",
        str(repo_root / ".claude" / "skills" / "map-spain-drugs" / "audit_spain_folder.py"),
        str(mapping_path.parent),
    ]
    audit_result = run_command(audit_cmd)
    audit_text = clean(audit_result.stdout) or clean(audit_result.stderr)
    if audit_result.returncode != 0 or audit_text != "OK - no issues found":
        return "audit_failed", audit_text

    return "completed", apply_message


def write_manifest(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=MANIFEST_COLUMNS, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--base",
        default="data/spain/products",
        help="Base folder containing Spain product folders",
    )
    parser.add_argument(
        "--manifest",
        default="tmp/map-spain-drugs-batch/manifest.tsv",
        help="Where to write the manifest TSV",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=60,
        help="Maximum number of folders to include",
    )
    parser.add_argument(
        "--pass-size",
        type=int,
        default=3,
        help="Number of folders per pass",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply updates, validate, and audit the selected folders",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[4]
    base = repo_root / args.base
    manifest_path = repo_root / args.manifest

    candidates = select_candidates(base)[: args.limit]
    manifest_rows = []

    for index, candidate in enumerate(candidates, start=1):
        pass_number = ((index - 1) // args.pass_size) + 1
        folder_name = str(candidate["folder"])
        action = str(candidate["action"])
        row_count = int(candidate["row_count"])
        total_rows = int(candidate["total_rows"])
        updates = list(candidate["updates"])
        status = "planned"
        if action == "pattern_fill":
            details = f"{row_count} rows reusable from existing EXACT patterns"
        else:
            details = f"{row_count} legacy dates to backfill on exact-only folder"
        if args.apply:
            status, details = apply_updates(repo_root, folder_name, updates)
        manifest_rows.append(
            {
                "pass_number": str(pass_number),
                "folder": folder_name,
                "action": action,
                "row_count": str(row_count),
                "total_rows": str(total_rows),
                "status": status,
                "details": details,
            }
        )

    write_manifest(manifest_path, manifest_rows)

    print(f"manifest\t{manifest_path}")
    print(f"selected\t{len(manifest_rows)}")
    if manifest_rows:
        max_pass = max(int(row["pass_number"]) for row in manifest_rows)
    else:
        max_pass = 0
    print(f"passes\t{max_pass}")
    for row in manifest_rows:
        print(
            "\t".join(
                [
                    row["pass_number"],
                    row["folder"],
                    row["action"],
                    row["row_count"],
                    row["status"],
                    row["details"],
                ]
            )
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
