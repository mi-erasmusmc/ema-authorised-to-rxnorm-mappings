---
name: find-concepts
description: Search for RxNorm standard concepts using the Hecate semantic search API. Primary search tool for drug mapping.
---

# Find RxNorm Concepts

Search for RxNorm standard concepts using the Hecate semantic search API.

## When to Use

When you need to find RxNorm concepts for a drug product during mapping. This is the primary search tool used by both EMA and Latvia mapping skills.

## Usage

Run via the Makefile from the repo root. Each query is searched independently; results are deduplicated and returned as TSV.

Single query (wrap in inner double quotes inside outer single quotes):
```bash
make find_concepts ARGS='"alemtuzumab 10 MG/ML Injection"'
```

Multiple queries (each inner-quoted, space-separated):
```bash
make find_concepts ARGS='"alemtuzumab 10 MG/ML Injection" "alemtuzumab injection"'
```

> **Quoting rule:** always use `ARGS='...'` (outer single quotes) with `"..."` (inner double quotes) around each multi-word query. Without inner quotes, spaces split each word into a separate query.

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

```bash
make find_concepts ARGS='"vildagliptin 50 mg oral tablet [Xiliarx]" "vildagliptin 50 mg" "vildagliptin oral tablet"'
```

For combination products:
```bash
make find_concepts ARGS='"emtricitabine 200 MG / tenofovir disoproxil fumarate 300 MG Oral Tablet" "emtricitabine / tenofovir oral tablet"'
```

## RxNorm Extension Fallback

When standard RxNorm search does not return a suitable EXACT match, retry with the `--extension` flag:

```bash
make find_concepts ARGS='--extension "vildagliptin 50 mg oral tablet"'
```

This searches both RxNorm and RxNorm Extension. Extension concepts have codes like `OMOP1234567` instead of numeric RxNorm codes.

### When to use Extension concepts

- Only after confirming no suitable standard RxNorm concept exists
- Prefer a standard RxNorm concept when it is equally specific and clinically appropriate
- Prefer a clean Extension concept over a weaker standard concept when the Extension concept adds a missing clinically relevant element needed for `EXACT`, such as dose form, release type, route-specific presentation, or clinically relevant single-use volume

### Extension pitfalls — be selective

RxNorm Extension contains duplicates, errors, and concepts that should not exist. Apply these filters:

1. **No supplier or non-clinical packaging concepts** — skip anything that includes a supplier name (e.g. `by Accord`) or box information (`Box of 30`, `by Company X`). We only want clinical drug concepts.
2. **Do not reject clinically relevant presentation detail** — a clean Extension concept is acceptable if it adds missing dose-form or presentation detail such as `Injectable Solution`, `Prefilled Syringe`, or a clinically relevant single-use volume. These are part of the clinical drug concept, not disqualifying packaging noise.
3. **Stay close to RxNorm patterns** — the Extension concept name must follow standard RxNorm conventions.
4. **Use correct dose forms** — verify the dose form in the Extension concept matches what the product actually is (use the dose form definitions printed by the script).
5. **Prefer BROAD over bad Extension** — if the only Extension match is dubious, it is better to map BROAD to a standard RxNorm concept than EXACT to a questionable Extension concept.

## Reference Data

The `map-drugs` skill directory contains reference files to assist mapping:

- **`dose_form_lookup.json`** - Maps RxNorm dose form names to descriptions (used automatically by the script)
- **`weight_conversions.tsv`** - Base-to-salt weight conversions for when EMA and RxNorm express strengths differently
- **`biosimilars/`** directory in `map-drugs` - Per-INN reference files listing known biosimilars with FDA names, EU brand names, and authorisation holders
