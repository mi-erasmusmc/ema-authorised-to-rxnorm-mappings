---
name: process-ema-data
description: Parse EMA Authorised Presentations PDF files into structured TSV format. Use when asked to parse, extract, or process raw EMA product PDFs, or to fetch/download new EMA data.
---

# Process Data: EMA Product PDFs

Parse EMA Authorised Presentations PDF files into structured TSV format.

## When to Use

When asked to parse an EMA product PDF, extract packaging data from a product folder, update parsed data, or fetch new/updated PDFs from EMA.

## Input

- PDF files in numbered subfolders: `data/ema/products/<ema_number>/<ema_number>_<product_name>_<date>.pdf`
- Example: `data/ema/products/006156/006156_stoboclo_2026-01-14.pdf`

## Output

- TSV file: `parsed_data_<today>.tsv` in the same subfolder as the PDF
- Example: `data/ema/products/006156/parsed_data_2026-01-16.tsv`

## TSV Columns

| Column | Description | PDF Source |
|--------|-------------|------------|
| ma_number | Marketing Authorization number | "MA (EU) number" |
| ema_product_number | EMA product identifier (format: `EMEA/H/C/XXXXXX`) | Derived from folder name |
| strength | Drug strength | "Strength" |
| pharmaceutical_form | Form of the medication | "Pharmaceutical Form" |
| route_of_administration | How the drug is administered | "Route of Administration" |
| packaging | Container type | "Immediate Packaging" |
| content | Volume/amount with concentration | "Content (concentration)" |
| pack_size | Number of units in pack | "Pack size" |
| product_name | Brand/invented name | "(Invented) name" |

## Fetching New Data

When asked to fetch, download, or update EMA data, run a single command:

```bash
make update_ema
```

This automatically:
1. Detects the most recent PDF date from existing files
2. Downloads the EMA medicines report and new/updated Authorised Presentations PDFs
3. Generates `ema-info.txt` metadata for any new product folders

To override the auto-detected date cutoff:
```bash
make update_ema ARGS="--since YYYY-MM-DD"
```

After fetching, proceed to parse the new PDFs using the steps below.

## Parsing Steps

1. **Locate the PDF** in its numbered subfolder under `data/ema/products/`

2. **Extract the PDF date** from the filename (e.g., `2026-01-14`)

3. **Check for existing TSV** (`parsed_data_*.tsv`) in the same subfolder:
   - If TSV date >= PDF date: **Skip** - no processing needed
   - If no TSV exists or TSV date < PDF date: Continue

4. **Read the PDF** and extract the table data

5. **Create/Update the TSV**:
   - Filename: `parsed_data_<today>.tsv`
   - Header row with all column names
   - One row per product presentation
   - Tab delimiters, no trailing tabs or spaces
   - Delete old TSV file if updating

## Example

**Input PDF content:**
```
MA (EU) number: EU/1/23/1727/001
(Invented) name: BEKEMV
Strength: 300 mg
Pharmaceutical Form: Concentrate for solution for infusion
Route of Administration: Intravenous use
Immediate Packaging: vial (glass)
Content (concentration): 30 ml (10 mg/ml)
Pack size: 1 vial
```

**Output TSV:**
```
ma_number	ema_product_number	strength	pharmaceutical_form	route_of_administration	packaging	content	pack_size	product_name
EU/1/23/1727/001	EMEA/H/C/005652	300 mg	Concentrate for solution for infusion	Intravenous use	vial (glass)	30 ml (10 mg/ml)	1 vial	BEKEMV
```

## Footnote Handling

Some PDFs use footnote markers in the Strength column (e.g. `--15`, `--16`) whose definitions appear as multi-line blocks later in the PDF. When this occurs:

1. Write the **marker + reference** in the strength column: e.g. `--15 see footnote.txt`
   - **Always keep the marker** — it is the only link between the TSV row and the correct footnote entry.
2. Create `footnote.txt` in the same product folder with the full footnote text exactly as it appears in the PDF.

Short, simple footnotes (a single phrase that fits naturally in the cell) can be inlined directly without creating footnote.txt.

**Example strength column values:**
- Elaborate multi-line: `--15 see footnote.txt`
- Simple inline: `30 micrograms/dose`

## Batch Parsing

To parse multiple products efficiently using subagents:

1. **Generate the batch prompt:**
   ```bash
   make prepare_parse_batch ARGS="000476 006208 006322"
   ```
   This outputs a self-contained prompt with PDF paths, output paths, TSV header, column mappings, and product metadata. Products with no PDF are marked SKIP.

2. **Invoke background subagents** with the output as the prompt. Use `subagent_type: "pdf-parser"` — this routes to a custom Haiku agent defined in `.claude/agents/pdf-parser.md` with `permissionMode: acceptEdits`, so it can write files without interactive approval. Split into batches of ~5 products per agent for parallelism.

3. The generated prompt from `prepare_parse_batch.py` contains pre-computed paths — use them directly (no globbing or filesystem exploration needed).

**Fallback:** If subagents fail (e.g. permission issues), read all PDFs in parallel (using Read tool) in the main context, then write all TSVs in parallel (using Write tool).

## Scripts

All scripts are located in `.claude/skills/process-ema-data/scripts/` and should be invoked with this full path from the workspace root:

- **`.claude/skills/process-ema-data/scripts/fetch_ema_updates.py`** - One-command wrapper: detects latest date, downloads updates, generates metadata
- **`.claude/skills/process-ema-data/scripts/download_ema_presentation_files.py`** - Downloads the EMA medicines report and Authorised Presentations PDFs
- **`.claude/skills/process-ema-data/scripts/generate_ema_info.py`** - Generates `ema-info.txt` metadata files from `medicines_report.tsv`
- **`.claude/skills/process-ema-data/scripts/prepare_parse_batch.py`** - Generates a batch parsing prompt for multiple products (eliminates per-product filesystem exploration)
- **`scripts/generate_mapping_overviews.py ema`** - Regenerates `ema-to-rxnorm.tsv` from per-product data (generic script, not skill-specific)
- **`.claude/skills/process-ema-data/scripts/find_missing_files.py`** - Audits product folders for missing files
- **`.claude/skills/process-ema-data/scripts/list_pdfs_by_date.py`** - Lists PDFs sorted by date
