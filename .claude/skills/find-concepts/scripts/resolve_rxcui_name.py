#!/usr/bin/env python3
"""Resolve full RxNorm concept names, falling back to historystatus for retired RXCUIs."""

import argparse
import json
import ssl
import sys
import urllib.error
import urllib.request

import certifi


BASE_URL = "https://rxnav.nlm.nih.gov/REST/rxcui/{rxcui}/{endpoint}.json"


def fetch_json(rxcui, endpoint):
    url = BASE_URL.format(rxcui=rxcui, endpoint=endpoint)
    ctx = ssl.create_default_context(cafile=certifi.where())
    with urllib.request.urlopen(url, context=ctx) as resp:
        return json.loads(resp.read()), url


def name_from_properties(payload):
    return payload.get("properties", {}).get("name")


def name_from_historystatus(payload):
    history = payload.get("rxcuiStatusHistory", {})
    return history.get("attributes", {}).get("name")


def resolve_name(rxcui):
    payload, url = fetch_json(rxcui, "properties")
    name = name_from_properties(payload)
    if name:
        return name, "properties", url

    payload, url = fetch_json(rxcui, "historystatus")
    name = name_from_historystatus(payload)
    if name:
        return name, "historystatus", url

    return "", "", ""


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Resolve the full RxNorm concept name for one or more RXCUIs. "
            "Checks properties first, then historystatus if properties is empty."
        )
    )
    parser.add_argument("rxcuis", nargs="+", help="one or more RXCUIs")
    args = parser.parse_args()

    print("rxcui\tconcept_name\tresolved_from\turl")
    missing = False
    for rxcui in args.rxcuis:
        try:
            name, source, url = resolve_name(rxcui)
        except urllib.error.URLError as exc:
            print(f"{rxcui}\t\tERROR\t{exc}", file=sys.stderr)
            missing = True
            continue

        if not name:
            missing = True
        print(f"{rxcui}\t{name}\t{source}\t{url}")

    sys.exit(1 if missing else 0)


if __name__ == "__main__":
    main()
