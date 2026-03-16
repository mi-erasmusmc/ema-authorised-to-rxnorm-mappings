# Data

This folder contains EMA (European Medicines Agency) medicine data and Latvian national product data.

Scripts and tooling for processing this data live in `skills/`. See `skills/process-data/` and `skills/map-drugs/` for details.

## Directories

### `ema/`

EMA centrally authorised product data:

- **`medicines_output_medicines_report_en.xlsx`** - Raw Excel file downloaded from EMA
- **`medicines_report.tsv`** - TSV conversion of the Excel file
- **`products/`** - Subdirectories for each EMA product number, each containing:
    - `{product_number}_{medicine_name}_{YYYY-MM-DD}.pdf` - Authorised Presentations PDF
    - `parsed_data.tsv` - Parsed packaging data extracted from the PDF
    - `mapping.tsv` - RxNorm mapping for each MA number in this product
    - `ema-info.txt` - Medicine metadata from the EMA medicines report

### `latvia/`

Latvian national product data:

- **`HumanProducts.json`** - Raw registry export from ZVA
- **`products/`** - Per-product folders organized by active substance and brand name

## Usage

All scripts can be invoked from any directory in the project (they resolve paths via git root).

Download/update EMA data:

```bash
python3 skills/process-data/download_ema_presentation_files.py
```

Generate ema-info.txt files for all products:

```bash
python3 skills/process-data/generate_ema_info.py
```

Combine all product data and generate ema-to-rxnorm.tsv:

```bash
python3 scripts/generate_mapping_overviews.py
```

Check for missing files:

```bash
python3 skills/process-data/find_missing_files.py
```

Search for RxNorm concepts:

```bash
find_concepts "vildagliptin 50 mg oral tablet" "vildagliptin 50 mg"
```

List PDFs by date:

```bash
python3 skills/process-data/list_pdfs_by_date.py
```

## Data Sources

- EMA: https://www.ema.europa.eu/
- Latvian ZVA: https://dati.zva.gov.lv/zalu-registrs/export/en
