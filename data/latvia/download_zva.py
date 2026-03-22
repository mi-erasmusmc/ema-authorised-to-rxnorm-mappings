#!/usr/bin/env python3
"""
Download the latest HumanProducts.json from the ZVA (Latvian State Agency of Medicines) registry.

Source: https://dati.zva.gov.lv/zalu-registrs/export/en
Download: https://dati.zva.gov.lv/zalu-registrs/export/HumanProducts.json.zip
"""

import io
import json
import ssl
import sys
import urllib.request
import zipfile
from pathlib import Path

URL = "https://dati.zva.gov.lv/zalu-registrs/export/HumanProducts.json.zip"
OUT = Path(__file__).parent / "HumanProducts.json"


def main():
    print(f"Downloading {URL} ...", file=sys.stderr)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    data = urllib.request.urlopen(URL, timeout=60, context=ctx).read()
    print(f"Downloaded {len(data):,} bytes", file=sys.stderr)

    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        names = zf.namelist()
        json_files = [n for n in names if n.endswith(".json")]
        if not json_files:
            print(f"ERROR: no .json file found in zip. Contents: {names}", file=sys.stderr)
            sys.exit(1)
        filename = json_files[0]
        print(f"Extracting {filename} ...", file=sys.stderr)
        content = zf.read(filename)

    # Validate JSON before writing
    try:
        records = json.loads(content.decode("utf-8-sig"))
        print(f"Parsed {len(records):,} records", file=sys.stderr)
    except json.JSONDecodeError as e:
        print(f"ERROR: invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)

    OUT.write_bytes(content)
    print(f"Done. Written to {OUT}", file=sys.stderr)


if __name__ == "__main__":
    main()
