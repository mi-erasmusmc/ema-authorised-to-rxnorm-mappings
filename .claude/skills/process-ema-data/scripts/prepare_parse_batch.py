#!/usr/bin/env python3
"""Prepare a batch parsing prompt for multiple EMA product PDFs.

Outputs a self-contained prompt with PDF paths, output paths, TSV header,
and product metadata — so the agent can parse all PDFs without filesystem
exploration or skill doc lookups.
"""

import subprocess
import sys
from datetime import date
from pathlib import Path


def _gitroot():
    return Path(subprocess.check_output(
        ["git", "rev-parse", "--show-toplevel"], text=True
    ).strip())


GIT_ROOT = _gitroot()
PRODUCTS_DIR = GIT_ROOT / "data" / "ema" / "products"
TODAY = date.today().isoformat()

TSV_HEADER = (
    "ma_number\tema_product_number\tstrength\tpharmaceutical_form\t"
    "route_of_administration\tpackaging\tcontent\tpack_size\tproduct_name"
)

COLUMN_MAPPING = """\
Column → PDF field:
  ma_number → "MA (EU) number"
  strength → "Strength"
  pharmaceutical_form → "Pharmaceutical Form"
  route_of_administration → "Route of Administration"
  packaging → "Immediate Packaging"
  content → "Content (concentration)"
  pack_size → "Pack size"
  product_name → "(Invented) name"
  ema_product_number → derived from folder (provided below)"""


def read_product_name(folder):
    """Read product name from ema-info.txt."""
    info_file = folder / "ema-info.txt"
    if not info_file.exists():
        return None
    for line in info_file.read_text().splitlines():
        if line.startswith("Name of medicine:"):
            return line.split(":", 1)[1].strip()
    return None


def find_pdf(folder):
    """Find the single PDF in a product folder."""
    pdfs = list(folder.glob("*.pdf"))
    return pdfs[0] if pdfs else None


def find_existing_tsvs(folder):
    """Find existing parsed_data TSVs (with or without date suffix)."""
    return sorted(folder.glob("parsed_data*.tsv"))


def prepare_product(product_number):
    """Prepare prompt section for one product."""
    folder = PRODUCTS_DIR / product_number
    if not folder.exists():
        return f"## {product_number}\nSKIP: Product folder not found\n"

    product_name = read_product_name(folder) or "Unknown"
    pdf = find_pdf(folder)

    if not pdf:
        return f"## {product_number} — {product_name}\nSKIP: No PDF found\n"

    ema_product_number = f"EMEA/H/C/{product_number}"
    output_path = folder / f"parsed_data_{TODAY}.tsv"

    # Find old TSVs to delete (any that aren't today's)
    old_tsvs = [t for t in find_existing_tsvs(folder)
                if t.name != f"parsed_data_{TODAY}.tsv"]

    lines = [
        f"## {product_number} — {product_name}",
        f"PDF: {pdf.relative_to(GIT_ROOT)}",
        f"Output: {output_path.relative_to(GIT_ROOT)}",
        f"ema_product_number: {ema_product_number}",
    ]

    for old in old_tsvs:
        lines.append(f"Delete old: {old.relative_to(GIT_ROOT)}")

    return "\n".join(lines) + "\n"


def main():
    if len(sys.argv) < 2:
        print("Usage: prepare_parse_batch.py <product_number> [product_number ...]",
              file=sys.stderr)
        sys.exit(1)

    product_numbers = sys.argv[1:]

    print("Parse the following EMA product PDFs into TSV files.")
    print()
    print("TOOL RULES:")
    print("- Use the Read tool to read PDFs visually (you have multimodal capabilities). "
          "Use the pages parameter for multi-page PDFs (e.g., pages=\"1-10\").")
    print("- Use the Write tool to create TSV files. NEVER use Bash with heredoc/echo/cat to write files.")
    print("- Use Bash ONLY for deleting old files (rm command).")
    print("- Do NOT use pdftotext, pdfplumber, or any Python PDF extraction libraries.")
    print()
    print(f"TSV header (use exactly):")
    print(TSV_HEADER)
    print()
    print(COLUMN_MAPPING)
    print()

    for num in product_numbers:
        print("---")
        print(prepare_product(num))


if __name__ == "__main__":
    main()
