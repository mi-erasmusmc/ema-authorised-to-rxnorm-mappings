#!/usr/bin/env python3
"""
Fetch AEMPS product PDFs by nro_definitivo.

PDF types:
  ft  — ficha técnica (prescribing information)
  p   — prospecto (patient leaflet)

URL patterns:
  https://cima.aemps.es/cima/pdfs/es/ft/{nro}/{nro}_ft.pdf
  https://cima.aemps.es/cima/pdfs/es/p/{nro}/{nro}_p.pdf

Usage:
  python3 fetch_pdf.py 66337         # downloads both PDFs for nro_definitivo 66337
  python3 fetch_pdf.py 66337 ft      # ficha técnica only
  python3 fetch_pdf.py 66337 p       # prospecto only

Returns the local file path on stdout so callers can pipe it further.
"""

import ssl
import sys
import urllib.request
from pathlib import Path

CACHE_DIR = Path(__file__).parent / ".pdf_cache"

URL_TEMPLATES = {
    "ft": "https://cima.aemps.es/cima/pdfs/es/ft/{nro}/{nro}_ft.pdf",
    "p":  "https://cima.aemps.es/cima/pdfs/es/p/{nro}/{nro}_p.pdf",
}


def fetch_pdf(nro: str, kind: str = "ft") -> Path:
    """Download a PDF and return its local cached path.

    Args:
        nro:  nro_definitivo value from data.tsv
        kind: "ft" (ficha técnica) or "p" (prospecto)
    """
    if kind not in URL_TEMPLATES:
        raise ValueError(f"kind must be 'ft' or 'p', got {kind!r}")

    out_path = CACHE_DIR / kind / f"{nro}_{kind}.pdf"
    if out_path.exists():
        return out_path

    url = URL_TEMPLATES[kind].format(nro=nro)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        with urllib.request.urlopen(url, timeout=30, context=ctx) as resp:
            data = resp.read()
    except urllib.error.HTTPError as e:
        raise FileNotFoundError(f"PDF not found for nro={nro} kind={kind}: HTTP {e.code}") from e

    out_path.write_bytes(data)
    return out_path


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)

    nro = args[0]
    kinds = [args[1]] if len(args) > 1 else list(URL_TEMPLATES)

    for kind in kinds:
        try:
            path = fetch_pdf(nro, kind)
            print(path)
        except FileNotFoundError as e:
            print(f"WARNING: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
