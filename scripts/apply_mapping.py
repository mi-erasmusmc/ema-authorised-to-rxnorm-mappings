#!/usr/bin/env python3
"""Apply a mapping decision to unmapped rows by product_id range or pattern.

Usage:
    # Map all IDs starting with prefix (covers all pack sizes):
    python3 scripts/apply_mapping.py <substance_dir> \
        --ids "23-0087-*" \
        --concept-id 46221241 --concept-name "deferasirox 90 MG Oral Tablet" \
        --concept-code 1607796 --mapping-type EXACT

    # Map specific IDs:
    python3 scripts/apply_mapping.py <substance_dir> \
        --ids "EU/1/06/356/001,EU/1/06/356/002" \
        --concept-id 1786082 --concept-name "deferasirox 125 MG ..." \
        --concept-code 616159 --mapping-type EXACT

    # Map a range:
    python3 scripts/apply_mapping.py <substance_dir> \
        --ids "EU/1/06/356/001..EU/1/06/356/010" \
        --concept-id 1786082 ...

--ids supports: comma-separated, glob (*), or range (..)
For BROAD mappings, --suggestion is required.
"""

import argparse
import csv
import fnmatch
import glob
import os
import subprocess
import sys
from datetime import date

TODAY = date.today().isoformat()


def parse_ids(ids_str):
    """Parse --ids into a match function.

    Supports:
      - Comma-separated: "A,B,C"
      - Glob: "23-0087-*"
      - Range: "23-0087-01..23-0087-03"
      - Combined: "23-0087-*,24-0001-01"
    """
    parts = [p.strip() for p in ids_str.split(",")]

    matchers = []
    for part in parts:
        if ".." in part:
            start, end = part.split("..", 1)
            matchers.append(("range", start.strip(), end.strip()))
        elif "*" in part or "?" in part:
            matchers.append(("glob", part))
        else:
            matchers.append(("exact", part))

    def matches(pid):
        for m in matchers:
            if m[0] == "exact" and pid == m[1]:
                return True
            elif m[0] == "glob" and fnmatch.fnmatch(pid, m[1]):
                return True
            elif m[0] == "range" and m[1] <= pid <= m[2]:
                return True
        return False

    return matches


def main():
    parser = argparse.ArgumentParser(description="Apply mapping by product_id.")
    parser.add_argument("substance_dir", help="Substance directory path")
    parser.add_argument("--ids", required=True,
                        help="Product IDs: comma-separated, glob (*), or range (..)")
    parser.add_argument("--concept-id", required=True)
    parser.add_argument("--concept-name", required=True)
    parser.add_argument("--concept-code", default="")
    parser.add_argument("--mapping-type", required=True, choices=["EXACT", "BROAD"])
    parser.add_argument("--comment", default="")
    parser.add_argument("--suggestion", default="")
    args = parser.parse_args()

    if args.mapping_type == "BROAD" and not args.suggestion:
        print("Error: BROAD mappings require --suggestion", file=sys.stderr)
        sys.exit(1)

    substance_dir = args.substance_dir.rstrip("/")
    matches = parse_ids(args.ids)
    filled = 0
    files_changed = []

    for mapping_file in sorted(glob.glob(os.path.join(substance_dir, "*/mapping.tsv"))):
        with open(mapping_file) as f:
            reader = csv.DictReader(f, delimiter="\t")
            fieldnames = reader.fieldnames
            rows = list(reader)

        changed = False
        for row in rows:
            pid = row["product_id"]
            if not matches(pid):
                continue
            if row.get("concept_id"):
                continue  # already mapped, skip
            row["concept_id"] = args.concept_id
            row["concept_name"] = args.concept_name
            row["concept_code"] = args.concept_code
            row["mapping_type"] = args.mapping_type
            row["comment"] = args.comment
            row["suggestion"] = args.suggestion
            row["last_updated_date"] = TODAY
            changed = True
            filled += 1

        if changed:
            with open(mapping_file, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t",
                                        lineterminator="\n")
                writer.writeheader()
                writer.writerows(rows)
            files_changed.append(mapping_file)

    print(f"Applied: {filled} rows across {len(files_changed)} files")

    # Validate changed files
    for f in files_changed:
        result = subprocess.run(
            ["python3", "skills/map-drugs/validate_mapping.py", f],
            capture_output=True, text=True
        )
        status = "OK" if result.returncode == 0 else "FAIL"
        print(f"  {status} {f}")
        if result.returncode != 0:
            # Only show first 3 errors to keep output compact
            lines = result.stderr.strip().split("\n")
            for line in lines[:4]:
                print(f"    {line}")
            if len(lines) > 4:
                print(f"    ... and {len(lines)-4} more")


if __name__ == "__main__":
    main()
