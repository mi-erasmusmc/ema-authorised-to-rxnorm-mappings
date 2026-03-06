---
name: process-latvia-data
description: Organize and structure Latvian national medicinal product data from the ZVA registry into product folders.
---

# Process Data: Latvian Products

Organize and structure Latvian national medicinal product data from the ZVA registry.

## When to Use

When asked to process, organize, or update Latvian product data.

## Data Source

Latvian State Agency of Medicines (ZVA) registry: https://dati.zva.gov.lv/zalu-registrs/export/en

Raw data is stored as `data/latvia/HumanProducts.json`.

## Directory Structure

Products are organized under `data/latvia/products/` by active substance and brand name:
```
data/latvia/products/<active_substance>/<product_name>/
```

Folder names are sanitized: lowercased, spaces replaced with underscores, truncated to 96 characters.

## Product Folder Contents

Each product folder contains:
- **`info.txt`** - Product metadata with fields:
  - `short_name`: Brand/product name
  - `active_substance`: Active substance (Latin name)
  - `marketing_authorisation_holder`: MAH company and country
  - `manufacturer`: Manufacturer details
  - `atc_code`: ATC classification code
  - `package_leaflet`: Link to patient information leaflet
  - `summary_of_product_characteristics`: Link to SmPC

## Scripts

All scripts are located in the `scripts/` subdirectory of this skill and use git-root-based paths. They can be invoked from any directory in the project.

- **`scripts/organize_products.py`** - Creates the folder structure from `HumanProducts.json`, generates `info.txt` files
- **`/workspace/scripts/generate_mapping_overviews.py latvia`** - Regenerates `latvia-to-rxnorm.tsv` from per-product mappings (generic script, not skill-specific)
