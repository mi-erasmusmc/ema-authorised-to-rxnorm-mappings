---
name: find-concepts
description: Search for RxNorm standard concepts using the Hecate semantic search API. Primary search tool for drug mapping.
---

# Find RxNorm Concepts

Search for RxNorm standard concepts using the Hecate semantic search API.

## When to Use

When you need to find RxNorm concepts for a drug product during mapping. This is the primary search tool used by both EMA and Latvia mapping skills.

## Usage

```
find_concepts <query1> [query2] ...
```

Each query argument is searched independently. Results are deduplicated and returned as TSV.

## Output Columns

| Column | Description |
|--------|-------------|
| `concept_id` | OMOP concept identifier |
| `concept_name` | Standardized RxNorm drug concept name |
| `concept_code` | RxNorm concept code |

The script also prints dose form definitions for any matched dose forms in the results.
Pay attention to these dose form definitions as they are important for selecting the best concept

## Search Strategy

Cast a broad net with multiple queries of decreasing specificity:

```
find_concepts \
  "vildagliptin 50 mg oral tablet [Xiliarx]" \
  "vildagliptin 50 mg" \
  "vildagliptin oral tablet"
```

For combination products:
```
find_concepts \
  "emtricitabine 200 MG / tenofovir disoproxil fumarate 300 MG Oral Tablet" \
  "emtricitabine / tenofovir oral tablet"
```

## RxNorm Extension Fallback

When standard RxNorm search does not return a suitable EXACT match, retry with the `--extension` flag:

```
find_concepts --extension \
  "vildagliptin 50 mg oral tablet"
```

This searches both RxNorm and RxNorm Extension. Extension concepts have codes like `OMOP1234567` instead of numeric RxNorm codes.

### When to use Extension concepts

- Only after confirming no suitable standard RxNorm concept exists
- Prefer the closest RxNorm concept over an Extension concept when both are reasonable

### Extension pitfalls — be selective

RxNorm Extension contains duplicates, errors, and concepts that should not exist. Apply these filters:

1. **No supplier/packaging concepts** — skip anything that includes a supplier name (e.g. `by Accord`) or box information (box of 30). We only want clinical drug concepts.
2. **Stay close to RxNorm patterns** — the Extension concept name must follow standard RxNorm conventions.
3. **Use correct dose forms** — verify the dose form in the Extension concept matches what the product actually is (use the dose form definitions printed by the script).
4. **Prefer BROAD over bad Extension** — if the only Extension match is dubious, it is better to map BROAD to a standard RxNorm concept than EXACT to a questionable Extension concept.

## Reference Data

The `map-drugs` skill directory contains reference files to assist mapping:

- **`dose_form_lookup.json`** - Maps RxNorm dose form names to descriptions (used automatically by the script)
- **`weight_conversions.tsv`** - Base-to-salt weight conversions for when EMA and RxNorm express strengths differently
- **`biosimilars/`** directory in `map-drugs` - Per-INN reference files listing known biosimilars with FDA names, EU brand names, and authorisation holders
