---
name: map-latvia-drugs
description: Map Latvian national medicinal products to RxNorm standard concepts. Use when asked to map a Latvian product or create/review a mapping.tsv in a Latvia product folder.
---

# Map Drugs: Latvian Products

Map Latvian national medicinal products to RxNorm standard concepts.

## When to Use

When asked to map a Latvian product to RxNorm, or create/review a `mapping.tsv` in a Latvia product folder.

## Prerequisites

Refer to the `find-concepts` skill for how to search for RxNorm concepts, and the `map-drugs` skill for general mapping principles and the standard workflow.

## Resources

- Use `validate_all.py` to validate Latvia product folders and triage issue-heavy folders.
- Use `make list_folder_patterns` to summarize repeated presentation patterns before concept search, especially when one product has many pack variants.
- For Latvia folders that mix device families under the same strength/form pattern, use `make list_folder_patterns ARGS="... --package-aware"` so `package_en` distinguishes patterns without splitting on pack size.
- Use `apply_pattern_mappings.py` to expand one mapping decision per Latvia pattern into all matching `product_id` rows.

## Input Files

Each product folder under `data/latvia/products/<active_substance>/<product_name>/` contains:
- **`data_<date>.tsv`**: Presentation-level data with `product_id`, `original_name`, `strength`, `pharmaceutical_form`, `product_strength` (total dose/volume), `package_en`, and `package_size`. **This is the primary input — read it first.**
- **`info.txt`**: Product metadata with `short_name`, `active_substance`, `marketing_authorisation_holder`, `manufacturer`, `atc_code`, and links to PIL and SmPC

The parent folder name is the active substance (Latin name), and the product folder name is the brand name.

## Output Format

Create `mapping.tsv` in the product folder following the schema in the `map-drugs` skill. The source ID column is `product_id` (Latvian product registry ID).

## Workflow

Follow the standard mapping workflow in `map-drugs`. Latvia-specific deviations:

1. **Validate:**
   ```bash
   make validate_latvia ARGS="data/latvia/products/<substance>/<product>/"
   ```
   Use drill-down mode for details:
   ```bash
   make validate_latvia ARGS="data/latvia/products/<substance>/<product>/ --details"
   make validate_latvia ARGS="data/latvia/products/<substance>/<product>/ --details --issue MISSING"
   ```

   Issue types: `UNMAPPED_FOLDER`, `MISSING`, `STALE_MAPPING`, `NO_CONCEPT`, `NO_TYPE`, `BROAD`, `NO_MAPPING`, `REVIEW_VOLUME`, `REVIEW_INJECTION_FORM`, `DUPLICATE_DATA`, `DUPLICATE_MAPPING`, `INCONSISTENT_CONCEPT`, `INCONSISTENT_TYPE`, plus structural validation issues.

2. **Read data:** Read `data_*.tsv` first, then `info.txt` for active substance and brand name. **Only check the SmPC link** if the data file doesn't provide enough detail for an informed mapping decision.

3. **Search:** Translate Latin substance names to English before searching (e.g., `warfarinum natricum` -> `warfarin sodium`).

4. **Apply pattern decisions** when multiple rows share the same presentation:
   ```bash
   make apply_latvia_patterns ARGS="data/latvia/products/<substance>/<product>/mapping.tsv" <<'EOF'
   original_name	strength	pharmaceutical_form	product_strength	concept_id	concept_name	concept_code	mapping_type	comment	suggestion
   CarvedilolHexal 6.25 mg tablets	6.25 mg	Tablet	6,25 mg	19022749	carvedilol 6.25 MG Oral Tablet	200031	EXACT
   EOF
   ```

   For mixed-device folders where `package_en` matters:
   ```bash
   make apply_latvia_patterns ARGS="data/latvia/products/<substance>/<product>/mapping.tsv --package-aware" <<'EOF'
   original_name	strength	pharmaceutical_form	product_strength	package_en	concept_id	concept_name	concept_code	mapping_type	comment	suggestion
   Nordimet	10 mg	Solution for injection	10 mg/0,4 ml	Glass pre-filled pen	44506728	methotrexate 25 MG/ML Auto-Injector	1441408	BROAD	RxNorm lacks the matching volume-specific 25 MG/ML auto-injector presentation.	0.4 ML methotrexate 25 MG/ML Auto-Injector
   Nordimet	10 mg	Solution for injection	10 mg/0,4 ml	Glass pre-filled syringe with safety system	1146757	0.4 ML methotrexate 25 MG/ML Prefilled Syringe	2377333	EXACT
   EOF
   ```

   Backfill missing dates:
   ```bash
   make apply_latvia_patterns ARGS="data/latvia/products/<substance>/<product>/mapping.tsv --backfill-dates"
   ```

5. **Validate and regenerate:**
   ```bash
   make validate_mapping ARGS="data/latvia/products/<substance>/<product>/mapping.tsv"
   make generate_mapping_overviews
   ```

## Suppressions

Confirmed false positives can be suppressed in `data/latvia/suppressions.tsv`. See the suppressions section in `map-drugs` for the format. Latvia uses `product_id` as the ID column.

## Latvia-specific Pitfalls

- **Latin vs English substance names**: Folders use Latin names (e.g., `warfarinum_natricum`) but RxNorm uses English (e.g., `warfarin sodium`)
- **Products without RxNorm equivalent**: Leave concept fields empty, populate `suggestion`
