---
name: map-spain-drugs
description: Map Spanish national medicinal products to RxNorm standard concepts. Use when asked to map a Spanish product or create/review a mapping.tsv in a Spain product folder.
---

# Map Drugs: Spanish Products

Map Spanish national medicinal products (AEMPS CIMA registry) to RxNorm standard concepts.

## When to Use

When asked to map a Spain product to RxNorm, correct a wrong auto-mapping, or review a `mapping.tsv` in a Spain product folder.

## Prerequisites

Refer to the `find-concepts` skill for searching RxNorm concepts, and the `map-drugs` skill for general mapping principles.

## How Spain Mappings Work

Spain products are auto-linked to EMA mappings via `nro_definitivo` on first setup:

```
EU/1/20/1476/001  →  strip "EU" + remove "/"  →  1201476001  =  nro_definitivo
```

`link_ema_mappings.py` runs this match and writes `mapping.tsv` per product folder. It is **incremental** — existing rows are never overwritten. Only new `cod_nacion` values (new source data) are auto-mapped; stale rows (removed from source) are pruned.

This means **`mapping.tsv` is directly editable**. Edit it to fix wrong mappings. Your changes survive any subsequent rerun.

To reset a row to auto-mapping, delete the row from `mapping.tsv` and rerun `link_ema_mappings.py`.

## Input Files

Each product folder under `data/spain/products/{ingredient_slug}/` contains:
- **`data.tsv`**: One row per registered presentation with `cod_nacion`, `nro_definitivo`, `des_nomco` (brand name), `des_dcp` (clinical description), `des_dosific` (dosage string), `principios_activos` (active ingredient + dose), `forma_farmaceutica`, `vias_administracion`, `atc`, `laboratorio_titular` (MAH), `situacion_registro` (Autorizado / Anulado / Suspenso)
- **`mapping.tsv`**: Current mappings — auto-generated initially, directly editable

`cod_nacion` is the stable unique key per presentation. `nro_definitivo` is a product-level identifier (shared across pack sizes, similar to EMA product number).

## Output Format

Edit `mapping.tsv` following the schema in the `map-drugs` skill. The source ID columns are `cod_nacion` and `nro_definitivo` (both present, but `cod_nacion` is the unique key per row).

After editing, validate and regenerate:

```bash
python3 .claude/skills/map-drugs/validate_mapping.py data/spain/products/<folder>/mapping.tsv
python3 scripts/generate_mapping_overviews.py spain
```

## Known Data Quality Issue: Duplicate nro_definitivo

**161 EMA-linked `nro_definitivo` values appear on more than one Spain row.** This is a known defect in Spain's CIMA source data.

The most common cause: different pack volumes assigned the same `nro_definitivo`. Example:

| cod_nacion | nro_definitivo | des_dosific | Correct EMA MA |
|---|---|---|---|
| 764394 | 1201515001 | 25 mg/ml inyectable 4 ml | EU/1/20/1515/001 |
| 764395 | 1201515001 | 25 mg/ml inyectable 16 ml | EU/1/20/1515/003 |

The auto-match assigns both rows to the same EMA concept (whichever MA number the `nro_definitivo` resolves to). **The larger volume is almost always mapped to the wrong concept.**

### How to identify and fix

1. Look for rows in `mapping.tsv` where the concept name volume doesn't match `des_dosific`
2. Search for the correct concept using the `find-concepts` skill
3. Edit the wrong row directly in `mapping.tsv` — add a `comment` explaining the correction:
   ```
   nro_definitivo shared with 4ml; manually corrected to 16ml concept
   ```

Common duplicate patterns to check:
- **Bevacizumab biosimilars** (multiple products): 4 ml and 16 ml vials sharing one number
- **Enoxaparin** (`EU/1/16/1132/...`): many dose-banded pack variants
- **Onasemnogene abeparvovec** (`EU/1/20/1443/001`): 37 entries weight-banded packs
- **Adalimumab biosimilars**: 0.4 ml and 0.8 ml prefilled syringes sometimes share a number

### Finding duplicates programmatically

```bash
python3 -c "
import csv
from collections import defaultdict

ema_nros = set()
with open('ema-to-rxnorm.tsv') as f:
    for row in csv.DictReader(f, delimiter='\t'):
        ma = row['ma_number']
        if ma.startswith('EU'):
            ema_nros.add(ma[2:].replace('/', ''))

counts = defaultdict(list)
with open('data/spain/prescripcion.tsv') as f:
    for row in csv.DictReader(f, delimiter='\t'):
        nro = row['nro_definitivo'].strip()
        if nro in ema_nros:
            counts[nro].append((row['cod_nacion'], row['des_dosific']))

for nro, entries in sorted(counts.items()):
    if len(entries) > 1:
        print(nro)
        for cod, desc in entries:
            print(f'  {cod}  {desc}')
"
```

## Mapping Workflow

1. **Read `data.tsv`** for the product folder to understand all presentations
2. **Check `mapping.tsv`** — most products already have an auto-mapping from EMA
3. **Verify each row** — confirm the concept name volume/strength matches `des_dosific`
4. **Fix duplicates** — identify rows with wrong volumes, search for the correct concept, edit in place
5. **Map unmapped rows** — for presentations with no auto-match, use `find-concepts` to find the right concept
6. **Validate and regenerate**:
   ```bash
   python3 .claude/skills/map-drugs/validate_mapping.py data/spain/products/<folder>/mapping.tsv
   python3 scripts/generate_mapping_overviews.py spain
   ```

## Spain-specific Notes

- **Spanish substance names**: `data.tsv` uses Spanish names (e.g., `bevacizumab`, `ácido zoledrónico`). The folder name is slugified from `des_dcsa` (active substance group name). Use the English name when searching RxNorm.
- **Anulado / Suspenso products**: `situacion_registro` indicates withdrawn/suspended products — map them anyway; the status is tracked separately.
- **Herbal products**: `sw_base_a_plantas = 1` — these typically have no RxNorm concept. Leave concept fields empty, populate `suggestion`.
- **Radiopharmaceuticals**: `radiofarmaco = 1` — specialist RxNorm handling, follow `map-drugs` principles.
- **Biosimilars**: `biosimilar = 1` — follow biosimilar rules in `map-drugs` skill.
