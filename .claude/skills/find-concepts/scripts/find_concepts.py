#!/usr/bin/env python3
"""Search the Hecate search_standard API for RxNorm concepts."""

import argparse
import os
import ssl
import subprocess
import sys
import urllib.error
import urllib.request
import urllib.parse
import json
import certifi


def _gitroot():
    return subprocess.check_output(
        ["git", "rev-parse", "--show-toplevel"], text=True
    ).strip()


GIT_ROOT = _gitroot()
SKILL_DIR = os.path.join(GIT_ROOT, ".claude", "skills", "map-drugs")


def load_dose_form_lookup():
    """Load the flat dose form lookup (sorted longest-name-first)."""
    path = os.path.join(SKILL_DIR, "dose_form_lookup.json")
    with open(path) as f:
        return json.load(f)


def find_dose_form(concept_name, dose_forms):
    """Find the first (longest) dose form name contained in concept_name."""
    name_lower = concept_name.lower()
    for df in dose_forms:
        if df["name"].lower() in name_lower:
            return df
    return None


RXNAV_BASE = "https://rxnav.nlm.nih.gov/REST/rxcui/{rxcui}/{endpoint}.json"


def resolve_full_name(rxcui):
    """Return the full RxNorm name for an rxcui, or None if not found."""
    ctx = ssl.create_default_context(cafile=certifi.where())
    for endpoint, extract in [
        ("properties", lambda p: p.get("properties", {}).get("name")),
        ("historystatus", lambda p: p.get("rxcuiStatusHistory", {}).get("attributes", {}).get("name")),
    ]:
        url = RXNAV_BASE.format(rxcui=rxcui, endpoint=endpoint)
        try:
            with urllib.request.urlopen(url, context=ctx) as resp:
                payload = json.loads(resp.read())
            name = extract(payload)
            if name:
                return name
        except urllib.error.URLError:
            pass
    return None


def search(query, limit=5, vocabulary_ids=("RxNorm",)):
    params = urllib.parse.urlencode({
        "q": query,
        "limit": limit,
        "vocabulary_id": ",".join(vocabulary_ids),
    })
    url = f"https://hecate.pantheon-hds.com/api/search_standard?{params}"
    ctx = ssl.create_default_context(cafile=certifi.where())
    with urllib.request.urlopen(url, context=ctx) as resp:
        return json.loads(resp.read())


def main():
    parser = argparse.ArgumentParser(description="Search Hecate for RxNorm concepts.")
    parser.add_argument("queries", nargs="+", metavar="QUERY", help="search queries")
    parser.add_argument(
        "--extension", action="store_true",
        help="also search RxNorm Extension vocabulary",
    )
    args = parser.parse_args()

    vocab_ids = ["RxNorm"]
    if args.extension:
        vocab_ids.append("RxNorm Extension")

    dose_forms = load_dose_form_lookup()

    seen = set()
    rows = []
    matched_dose_forms = {}
    for query in args.queries:
        for result in search(query, vocabulary_ids=vocab_ids):
            for concept in result.get("concepts", []):
                cid = concept["concept_id"]
                if cid not in seen:
                    seen.add(cid)
                    name = concept["concept_name"]
                    code = concept["concept_code"]
                    # Auto-resolve truncated names; OMOP-prefixed codes are
                    # RxNorm Extension concepts and cannot be looked up via RxNav.
                    if "..." in name and not code.startswith("OMOP"):
                        resolved = resolve_full_name(code)
                        if resolved:
                            name = resolved
                    df = find_dose_form(name, dose_forms)
                    if df:
                        matched_dose_forms[df["name"]] = df
                    rows.append((str(cid), name, code))

    print("concept_id\tconcept_name\tconcept_code")
    for row in rows:
        print("\t".join(row))

    if matched_dose_forms:
        print("\nDose form definitions:")
        for name, df in sorted(matched_dose_forms.items()):
            print(f"  {name}: {df['description']}")


if __name__ == "__main__":
    main()
