---
name: map-latvia-drugs
description: Map Latvian national medicinal products to RxNorm standard concepts. Use when asked to map a Latvian product or create/review a mapping.tsv in a Latvia product folder.
---

# Map Drugs: Latvian Products

Map Latvian national medicinal products to RxNorm standard concepts.

## When to Use

When asked to map a Latvian product to RxNorm, or create/review a `mapping.tsv` in a Latvia product folder.

## Prerequisites

Refer to the `find-concepts` skill for how to search for RxNorm concepts, and the `map-drugs` skill for general mapping principles.

## Input Files

Each product folder under `data/latvia/products/<active_substance>/<product_name>/` contains:
- **`data_<date>.tsv`**: Presentation-level data with `product_id`, `original_name`, `strength`, `pharmaceutical_form`, `product_strength` (total dose/volume), `package_en`, and `package_size`. **This is the primary input — read it first.**
- **`info.txt`**: Product metadata with `short_name`, `active_substance`, `marketing_authorisation_holder`, `manufacturer`, `atc_code`, and links to PIL and SmPC

The parent folder name is the active substance (Latin name), and the product folder name is the brand name.

## Output Format

Create `mapping.tsv` in the product folder following the schema in the `map-drugs` skill. The source ID column is `product_id` (Latvian product registry ID).

## Mapping Workflow

1. **Read `data_*.tsv`** to get all presentations — this has `product_id`, `strength`, `pharmaceutical_form`, and `product_strength` (total dose/volume) for every registered package
2. **Read `info.txt`** to get the active substance (English name from Latin folder name) and brand name
3. **Only check the SmPC link** if `data_*.tsv` does not provide enough detail to make an informed mapping decision (e.g., ambiguous dose form, unclear concentration basis)
4. **Search broadly** using the `find-concepts` skill:
   ```
   find_concepts "warfarin sodium 3 MG Oral Tablet" "warfarin 3 mg" "warfarin oral tablet"
   ```
5. **Verify the match** - confirm ingredient and strength match exactly
6. **Validate** the mapping:
   ```
   python3 .claude/skills/map-drugs/validate_mapping.py data/latvia/products/<substance>/<product>/mapping.tsv
   ```
7. **Regenerate combined files** after all mappings are complete:
   ```
   python3 scripts/generate_mapping_overviews.py
   ```

## Latvia-specific Pitfalls

- **Latin vs English substance names**: Folders use Latin names (e.g., `warfarinum_natricum`) but RxNorm uses English (e.g., `warfarin sodium`)
- **Products without RxNorm equivalent**: Leave concept fields empty, populate `suggestion`
