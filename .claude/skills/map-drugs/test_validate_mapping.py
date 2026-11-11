"""Regression checks for non-normalized dose forms in mapping suggestions."""

import csv
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import validate_mapping as validator


class SuggestionDoseFormTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "mapping.tsv"

    def write_mapping(self, suggestion):
        row = dict(
            ma_number="EU/1/24/1870/001", concept_id="36861273",
            concept_name="SERPLULIMAB", concept_code="OMOP5178890",
            mapping_type="BROAD", comment="", suggestion=suggestion,
            last_updated_date="2026-11-11",
        )
        with self.path.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(row), delimiter="\t")
            writer.writeheader()
            writer.writerow(row)

    def test_rejects_legacy_form_despite_valid_suffix(self):
        for suggestion in (
            "serplulimab 10 MG/ML Concentrate for Injectable Solution [Hetronifly]",
            "serplulimab 10 MG/ML Concentrate for Injectable Solution",
            "serplulimab 10 MG/ML CONCENTRATE  FOR  INJECTABLE  SOLUTION [Hetronifly]",
            "{(serplulimab 10 MG/ML Concentrate for Injectable Solution) } Pack",
        ):
            with self.subTest(suggestion=suggestion):
                self.write_mapping(suggestion)
                errors = validator.validate_file(str(self.path))
                self.assertTrue(any(
                    code == "BAD_SUGGESTION" and "not a normalized RxNorm dose form" in message
                    for code, message in errors
                ), errors)

    def test_accepts_normalized_injectable_forms(self):
        for suggestion in (
            "10 ML serplulimab 10 MG/ML Injection [Hetronifly]",
            "serplulimab 10 MG/ML Injectable Solution",
        ):
            with self.subTest(suggestion=suggestion):
                self.write_mapping(suggestion)
                self.assertEqual(validator.validate_file(str(self.path)), [])

    def test_cli_returns_failure_for_legacy_form(self):
        self.write_mapping("serplulimab 10 MG/ML Concentrate for Injectable Solution [Hetronifly]")
        result = subprocess.run(
            [sys.executable, str(Path(validator.__file__)), str(self.path)],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("not a normalized RxNorm dose form", result.stdout)


if __name__ == "__main__":
    unittest.main()
