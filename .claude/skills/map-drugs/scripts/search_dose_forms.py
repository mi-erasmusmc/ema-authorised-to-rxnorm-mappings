#!/usr/bin/env python3
"""
Search for valid RxNorm dose forms by keyword.

Usage:
    python3 .claude/skills/map-drugs/scripts/search_dose_forms.py emulsion
    python3 .claude/skills/map-drugs/scripts/search_dose_forms.py topical cream
    python3 .claude/skills/map-drugs/scripts/search_dose_forms.py injection syringe
"""

import json
import sys
from pathlib import Path

LOOKUP_PATH = Path(__file__).resolve().parent.parent / "dose_form_lookup.json"


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <keyword> [keyword ...]", file=sys.stderr)
        sys.exit(2)

    keywords = [k.lower() for k in sys.argv[1:]]

    with LOOKUP_PATH.open() as f:
        forms = json.load(f)

    def keyword_matches(keyword, combined, words):
        """Match if keyword is a substring of text OR shares a common stem with any word."""
        if keyword in combined:
            return True
        # Stem match: trim common suffixes and compare roots
        stem = keyword.rstrip("s")
        for suffix in ("ion", "ed", "ing", "ive", "able"):
            if stem.endswith(suffix):
                stem = stem[: -len(suffix)]
                break
        return any(w.startswith(stem) for w in words) if len(stem) >= 3 else False

    matches = []
    for entry in forms:
        name = entry.get("name", "")
        desc = entry.get("description", "")
        combined = f"{name} {desc}".lower()
        words = combined.split()
        if any(keyword_matches(kw, combined, words) for kw in keywords):
            matches.append(entry)

    if not matches:
        print(f"No dose forms matching: {' '.join(keywords)}")
        sys.exit(1)

    for entry in sorted(matches, key=lambda e: e["name"]):
        print(f"{entry['name']}")
        if entry.get("description"):
            print(f"  {entry['description']}")


if __name__ == "__main__":
    main()
