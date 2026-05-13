# Spain — AEMPS National Medicinal Products

Data from the Spanish Agency of Medicines and Medical Devices (AEMPS) CIMA registry, mapped to RxNorm standard concepts.

## Folder structure

```
data/spain/
  prescripcion.tsv          # raw source data from AEMPS (do not edit)
  download_aemps.py         # fetches/updates prescripcion.tsv
  split_by_ingredient.py    # splits prescripcion.tsv into per-ingredient product folders
  link_ema_mappings.py      # auto-maps presentations via EMA link (incremental — safe to rerun)
  fetch_pdf.py              # fetches product PDFs on demand
  products/
    {ingredient_slug}/
      data.tsv              # product rows for this ingredient (auto-generated, do not edit)
      mapping.tsv           # RxNorm mappings — directly editable, manual edits survive reruns
```

## How mappings are generated

`link_ema_mappings.py` links Spain presentations to EMA mappings by normalising the EMA
`ma_number` and comparing it to `nro_definitivo`:

```
EU/1/20/1515/001  →  strip "EU" + remove "/"  →  1201515001
```

The script is **incremental**:
- Existing rows in `mapping.tsv` are **preserved** — manual edits survive reruns.
- New `cod_nacion` values (added to source data) are auto-mapped and appended.
- Stale `cod_nacion` values (removed from source data) are pruned.

`cod_nacion` is the stable unique key per presentation; `nro_definitivo` is a product-level
identifier shared across pack sizes (similar to the EMA product number `EMEA/H/C/...`).

## Fixing incorrect mappings

Edit `mapping.tsv` directly. Because the script is incremental, your changes will not be
overwritten on the next rerun. Add a `comment` explaining the correction so it's clear
the row was manually fixed.

To reset a row back to auto-mapping, delete that row from `mapping.tsv` and rerun
`link_ema_mappings.py`.

## Known data quality issue: duplicate nro_definitivo

161 EMA-linked `nro_definitivo` values appear on more than one Spain row — a defect in
Spain's CIMA source data. The most common cause is different pack volumes being assigned
the same national number:

| cod_nacion | nro_definitivo | des_dosific | Correct EMA MA |
|---|---|---|---|
| 764394 | 1201515001 | 25 mg/ml inyectable 4 ml | EU/1/20/1515/001 |
| 764395 | 1201515001 | 25 mg/ml inyectable 16 ml | EU/1/20/1515/003 |

The auto-match assigns both to the same EMA concept. Check `mapping.tsv` for rows where
the concept name volume does not match `des_dosific`, then edit the wrong row in place.

See the `map-spain-drugs` skill for the full list of affected patterns and a helper script
to find all duplicates.

## Updating source data

To refresh from AEMPS without losing manual edits:

```bash
# Download latest nomenclator and re-split into product folders
make update_spain

# Review what changed
make list_spain_changes

# Regenerate combined output
make generate_mapping_overviews ARGS=spain
```
