"""Offline regression tests for historical Latvia package data."""

import contextlib
import csv
import importlib.util
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import generate_mapping_overviews as overviews


spec = importlib.util.spec_from_file_location(
    "deduplicate", overviews.GIT_ROOT / "data/latvia/deduplicate_data_files.py"
)
deduplicate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(deduplicate)


class LatviaUpdateTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.products = self.root / "latvia/products"
        self.folder = self.products / "ingredient/brand"
        self.folder.mkdir(parents=True)
        (self.folder / "info.txt").write_text("short_name: Brand\n")

    def snapshot(self, date, rows, folder=None):
        path = (folder or self.folder) / f"data_{date}.tsv"
        with path.open("w", newline="") as f:
            writer = csv.writer(f, delimiter="\t")
            writer.writerow(["product_id", "original_name", "inter_code"])
            writer.writerows(rows)
        return path

    def deduplicate(self):
        with patch.object(deduplicate, "PRODUCTS_DIR", self.products):
            with contextlib.redirect_stdout(io.StringIO()):
                deduplicate.main()

    def test_update_preserves_removed_package_in_overview(self):
        older = self.snapshot("2026-05-04", [
            ["01-0176-01", "Original package", "01-0176"],
            ["I001806-01", "Before update", "old-code"],
        ])
        newer = self.snapshot("2026-11-06", [
            ["I001806-01", "Updated package", "new-code"],
        ])
        (self.folder / "mapping.tsv").write_text(
            "product_id\tconcept_id\n01-0176-01\t\nI001806-01\t123\n"
        )
        self.deduplicate()
        self.assertTrue(older.exists())
        self.assertTrue(newer.exists())
        with patch.object(overviews, "LATVIA_DIR", self.root / "latvia"):
            with patch.object(overviews, "GIT_ROOT", self.root):
                with contextlib.redirect_stdout(io.StringIO()):
                    overviews.regenerate_latvia()
        with (self.root / "latvia-to-rxnorm.tsv").open() as f:
            rows = {r["product_id"]: r for r in csv.DictReader(f, delimiter="\t")}
        self.assertEqual(rows["01-0176-01"]["inter_code"], "01-0176")
        self.assertEqual(rows["01-0176-01"]["original_name"], "Original package")
        self.assertEqual(rows["01-0176-01"]["concept_id"], "")
        self.assertEqual(rows["I001806-01"]["inter_code"], "new-code")
        self.assertEqual(rows["I001806-01"]["concept_id"], "123")

    def test_identical_snapshot_removed_without_losing_history(self):
        historical = self.snapshot("2026-02-12", [["retired", "Retired", "old"]])
        older = self.snapshot("2026-05-04", [["current", "Current", "new"]])
        newer = self.snapshot("2026-11-06", [["current", "Current", "new"]])
        self.deduplicate()
        self.assertTrue(historical.exists())
        self.assertTrue(older.exists())
        self.assertFalse(newer.exists())
        self.assertEqual(set(overviews._load_latvia_products(self.products)),
                         {"retired", "current"})

    def test_newest_record_wins_when_product_moves_folders(self):
        other = self.products / "aaa/new_brand"
        other.mkdir(parents=True)
        self.snapshot("2026-05-04", [["package", "Old name", "old"]])
        self.snapshot("2026-11-06", [["package", "New name", "new"]], folder=other)
        products = overviews._load_latvia_products(self.products)
        self.assertEqual(products["package"]["original_name"], "New name")
        self.assertEqual(products["package"]["inter_code"], "new")


if __name__ == "__main__":
    unittest.main()
