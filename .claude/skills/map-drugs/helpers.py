#!/usr/bin/env python3
"""
Shared helpers for drug mapping scripts (apply, pattern listing, etc.).

Used by source-specific apply and pattern scripts to avoid duplicating
CSV I/O, string cleaning, and error handling.
"""

import csv
import sys
from pathlib import Path


def clean(value):
    """Strip whitespace from a value, treating None as empty string."""
    if value is None:
        return ""
    return str(value).strip()


def fail(message):
    """Print an error message to stderr and exit."""
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(1)


def load_tsv(path):
    """Load a TSV file and return a list of dicts."""
    with open(path, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path, rows, columns):
    """Write rows to a TSV file with the given column order."""
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def find_dated_file(folder, pattern="data_*.tsv"):
    """Return the most recent file matching a date-suffixed glob, or None."""
    candidates = sorted(folder.glob(pattern), reverse=True)
    return candidates[0] if candidates else None


def find_duplicates(rows, key):
    """Return sorted list of values that appear more than once in rows[key]."""
    seen = set()
    duplicates = set()
    for row in rows:
        value = clean(row.get(key, ""))
        if not value:
            continue
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return sorted(duplicates)


def pattern_key(row, fields):
    """Build a hashable tuple from the given fields of a row."""
    return tuple(clean(row.get(field, "")) for field in fields)
