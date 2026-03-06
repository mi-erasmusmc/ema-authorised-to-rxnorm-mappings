---
name: map-ema-drugs
description: Map EMA centrally authorised product presentations to RxNorm standard concepts. Use when asked to map an EMA product or create/review a mapping.tsv in an EMA product folder.
---

# Map Drugs: EMA Products

Map EMA centrally authorised product presentations to RxNorm standard concepts.

## When to Use

When asked to map an EMA product to RxNorm, or create/review a `mapping.tsv` in an EMA product folder.

## Finding Unmapped Products

To list all product folders that have parsed data but no `mapping.tsv`:

```bash
python3 .claude/skills/map-ema-drugs/find_unmapped.py
```

This prints folder names (one per line) that need mapping. Use it to find the next product to work on.

## Prerequisites

Refer to the `find-concepts` skill for how to search for RxNorm concepts, and the `map-drugs` skill for general mapping principles.

## Input Files

Each product folder under `data/ema/products/<ema_number>/` contains:
- **`ema-info.txt`**: Product metadata (medicine name, active substance, INN, therapeutic area)
- **`parsed_data*.tsv`**: One row per authorised presentation with `ma_number`, `strength`, `pharmaceutical_form`, `route_of_administration`, `packaging`, `content`, `pack_size`, `product_name`, `active_substance`, etc.

Read both files to understand the product before mapping.

## Output Format

Create `mapping.tsv` in the product folder following the schema in the `map-drugs` skill. The source ID column is `ma_number` (EU marketing authorisation number from `parsed_data.tsv`).

One row per `ma_number` in `parsed_data*.tsv`. Every presentation must be mapped.

**IMPORTANT**: Do not assume any logical ordering of `ma_number` values — they are NOT sorted by strength, dose form, or any other attribute. Always look up each `ma_number`'s actual strength and form from `parsed_data*.tsv` individually.

If a `mapping.tsv` already exists, check the mappings and note any needed changes in `flag.tsv`.

## Biosimilars

If `ema-info.txt` contains `Biosimilar: Yes`, follow the biosimilar mapping rules in the `map-drugs` skill.

## Validation

After creating or editing `mapping.tsv`, validate it:

```bash
python3 .claude/skills/map-drugs/validate_mapping.py data/ema/products/<ema_number>/mapping.tsv
```

Fix any errors, then **regenerate combined files**:

```bash
python3 scripts/generate_mapping_overviews.py
```

## Flagging Problems

If no suitable RxNorm results exist or mapping needs validation, add a `flag.txt` in the product folder explaining the issue.

## EU-only Products

Some EMA products have no FDA equivalent and no RxNorm concept. Leave concept fields empty, populate `suggestion` with the ideal concept name, and create `flag.txt`.
