---
name: map-drugs
description: General principles for mapping pharmaceutical products to RxNorm concepts. Covers mapping types (EXACT/BROAD/NO_MAPPING), terminology adaptation, unit conversions, and common pitfalls.
user-invocable: false
---

# Map Drugs to RxNorm

General principles for mapping pharmaceutical products to RxNorm concepts.

## When to Use

When asked to map a product to RxNorm, create or review a `mapping.tsv`, or find RxNorm concepts for a drug.

## Required Skills

- **`find-concepts`** - Search for RxNorm concepts using the semantic search API

## General Mapping Principles

These apply across all data sources:

### Mapping Types

- **EXACT**: Contains all clinically relevant information, matches active ingredient, strength, and dose form.
- **BROAD**: Less specific match. Use when only a concept without specific strength/volume is available, or for vaccines/biologicals with less granular RxNorm coverage. When choosing between multiple BROAD candidates, pick the one that preserves the most clinically relevant information — dose (strength + volume) matters more than device/form differences. For example, `0.5 ML etanercept 50 MG/ML Prefilled Syringe` is preferred over `etanercept 50 MG/ML Auto-Injector` for a 25 mg pen injector, because the volume distinguishes the 25 mg dose from the 50 mg dose.
- **NO_MAPPING**: No suitable RxNorm concept exists (e.g., EU-only strength or product with no FDA equivalent). Leave concept fields empty, populate `suggestion` with the ideal concept name, and do NOT set `mapping_type` to EXACT or BROAD. A `suggestion` is required.
- **`suggestion` formatting must follow RxNorm style**: `{volume} {ingredient} {strength}/{ML or MG} {dose form} [{Brand}]`. Strength is always per-unit concentration (e.g. `10 MG/ML`), never total dose (e.g. `250 MG/25 ML`). Volume is the leading container size when clinically relevant. Pack concepts follow RxNorm pack structure; do not improvise.
- **Brand** Use unbranded concepts unless the brand is the same in both EU and US (e.g., Twinrix, Lantus), RxNorm contains US brands which may differ from EU names do not use these. Minor label variations do not constitute a brand difference — if the base brand name matches, the branded RxNorm concept is appropriate. This includes suffixes like "Velotab", "DIF", "Ellipta", "Control", "Maintena", qualifiers like "Adult"/"Paediatric", and other sub-brand or formulation descriptors added to the same base brand.

### Standard vs Extension Priority

- Start with standard RxNorm, but do not stop there if a clinically relevant element needed for `EXACT` is missing.
- If standard RxNorm lacks a clinically relevant part of the presentation such as dose form, release type, route-specific presentation, or clinically relevant single-use volume, search RxNorm Extension.
- Prefer a clean Extension concept over a weaker standard `BROAD` concept when the Extension concept adds the missing clinically relevant detail without introducing supplier names, box counts, or other non-clinical packaging noise.
- Do not reject an Extension concept merely because it includes clinically relevant presentation detail. For example, `Injectable Solution`, `Prefilled Syringe`, and single-use volume can be necessary parts of an `EXACT` clinical drug concept.

### Partial-ingredient Combination Products

When the full ingredient combination is not available, map to the closest clinically representative subset rather than forcing an incorrect `EXACT` match.

- Use `BROAD` when one or more active ingredients, extract components, or formulation-defining parts of the combination are missing from RxNorm.
- Prefer the candidate that preserves the most clinically meaningful part of the presentation: usually the core active ingredients, then strength, then dose form.
- Populate `suggestion` with the ideal full concept name you would use if standard RxNorm contained the complete combination.
- Use `comment` only when a later reviewer would not be able to infer which ingredients or components were omitted from the chosen RxNorm concept.

Example: a four-ingredient oral solution where RxNorm only contains a two-ingredient subset should map `BROAD` to the closest represented subset, with `suggestion` naming the full four-ingredient presentation.

### Botanical and Extract Combinations

Multi-extract herbal products often have incomplete or inconsistent representation in standard RxNorm. Handle them conservatively.

- If the full botanical combination is absent, map `BROAD` to the closest represented extract set instead of stretching to a misleading `EXACT`.
- Match dose form carefully; for botanical products, form mismatches are often a better reason to stay `BROAD` than to use a loosely related tablet/solution concept.
- For single-ingredient botanical products, do not leave the row unmapped just because RxNorm lacks the exact strength or presentation. Use the most appropriate ingredient-, extract-, or dose-form-level concept that RxNorm does contain, and mark it `BROAD` when strength and/or form are not fully matched.
- Use `comment` to note important omitted botanicals, extract types, or other non-obvious gaps only when needed for reviewer clarity.
- Use `suggestion` to capture the ideal full botanical presentation, especially when several named extracts are missing from RxNorm.

### Terminology Adaptation

Terminology must be adapted to RxNorm conventions:
- "film-coated tablet" / "tablet" -> "oral tablet"
- "solution for injection" -> "injectable solution" or "injection"
- "capsule, hard" -> "oral capsule"

### Dose Form Selection

`dose_form_lookup.json` in this skill directory contains all valid RxNorm dose forms with descriptions. Search it by keyword:
```bash
make search_dose_forms ARGS="topical cream"
make search_dose_forms ARGS="injection"
make search_dose_forms ARGS="oral tablet"
```
Keywords are matched against name + description. Use this to verify a dose form exists before writing a suggestion — the validator rejects suggestions that don't end with a valid dose form.

The `find-concepts` script also returns dose form definitions alongside search results — use these to select the correct form. Key distinction for injectables include:
- **Injectable Solution**: multi-use product (e.g., vials intended for multiple withdrawals)
- **Injectable Suspension**: multi-use product (e.g., vials intended for multiple withdrawals)
- **Injection**: single-use product
- **Prefilled Syringe**: single-use solution in a syringe

### Precision: Volume-specific vs Generic Concepts

The clinical role of the leading volume in an RxNorm concept name depends on container type:

- **Single-use containers** (ampoules, prefilled syringes, auto-injectors — dose forms: Injection, Prefilled Syringe, Auto-Injector): the volume is part of the dose and clinically relevant. If a volume-specific concept exists and matches (e.g., `2 ML ondansetron 2 MG/ML Injection`), use it — this is EXACT. If no volume-specific concept exists, use the concentration-only concept (e.g., `ondansetron 2 MG/ML Injection`) — BROAD.
- **Multi-use containers** (vials — dose forms: Injectable Solution, Injectable Suspension): the container volume is packaging information only, not dose information. Prefer a concentration-only concept such as `daratumumab 120 MG/ML Injectable Solution` when one exists. Do not choose a volume-prefixed concept for a multi-use product merely because it mirrors the pack size. If standard RxNorm lacks the concentration-plus-dose-form concept but Extension has a clean one, use the clean Extension concentration-level concept for `EXACT`.
- If you can only find a **less specific** concept (e.g., missing clinically relevant strength or form), the mapping is **BROAD**, not EXACT.

### Common Pitfalls

- **Concentration vs total dose**: EMA lists both; RxNorm may express as concentration and/or total volume
- **Biologicals/vaccines**: BROAD mapping acceptable when exact match unavailable
- **Multiple strengths**: Different strengths must map to different RxNorm concepts
- **Inherited auto-links with no `mapping_type`**: treat these as unreviewed candidates, not accepted mappings. If a row has a `concept_id` and concept text but blank `mapping_type`, verify the concept before keeping it and write `EXACT` or `BROAD` explicitly once reviewed.
- **Base to salt conversions**: Check `weight_conversions.tsv` in this skill directory when in doubt
- **Metoprolol succinate ER tablets**: RxNorm concepts use tartrate-equivalent labeling (25/50/100/200 MG), following the US Toprol-XL convention. EU generics label by actual succinate content (23.75/47.5/95/190 MG). These are the same dose — map EXACT. FDA label confirms: "tablets contain 23.75, 47.5, 95 and 190 mg of metoprolol succinate equivalent to 25, 50, 100 and 200 mg of metoprolol tartrate." Note: 142.5 mg succinate (= 150 mg tartrate) has no RxNorm equivalent as Toprol-XL was never marketed at 150 mg.
- **Metered vs actuated dose**: Verify via SmPC/FDA labelling, add `sources.md` if needed
- **Pack sizes**: Different pack sizes of the same drug map to the same RxNorm concept
- **Unit conversion**: IU = UNT, RxNorm uses MG not µg or MCG

## Output Format

Create `mapping.tsv` in the product folder with these columns:

| Column | Description |
|--------|-------------|
| `<source_id>` | Source-specific ID (e.g., `ma_number` for EMA, `product_id` for Latvia, `cod_nacion` for Spain) |
| `concept_id` | RxNorm `concept_id` from search results |
| `concept_name` | RxNorm `concept_name` from search results |
| `concept_code` | RxNorm `concept_code` from search results |
| `mapping_type` | `EXACT`, `BROAD`, `NO_MAPPING`, or empty |
| `comment` | Optional note explaining the mapping decision |
| `suggestion` | Ideal concept name when no exact match exists |
| `last_updated_date` | Date in `YYYY-MM-DD` format |

See source-specific skills for the exact ID column name and any additional columns.

## Standard Mapping Workflow

All data sources follow the same general workflow. Source-specific skills document deviations and extra steps.

1. **Validate the folder** to understand existing issues:
   ```bash
   make validate_spain ARGS="<folder>/"      # Spain
   make validate_latvia ARGS="<folder>/"     # Latvia
   make validate_ema ARGS="<folder>/"        # EMA
   ```

2. **Read the source data** to understand presentations, strengths, volumes, and forms.
   For large folders, summarize repeated patterns first:
   ```bash
   make list_folder_patterns ARGS="<folder>/"
   make list_folder_patterns ARGS="<folder>/ --missing-only"  # unmapped rows only
   ```
   For Latvia folders that mix device families under the same strength/form, prefer:
   ```bash
   make list_folder_patterns ARGS="<folder>/ --package-aware"
   ```

3. **Search RxNorm concepts** via the `find-concepts` skill. Bundle 4-6 queries per call. Translate non-English ingredient names to English before searching. Always retry with `--extension` before concluding no concept exists.

4. **Apply mapping decisions.** Source-specific apply tools set `last_updated_date` automatically.
   - Use `comment` only for mapping rationale another reviewer would need (salt conversions, metered-vs-delivered dose, biosimilar handling, manual corrections from bad source data). Do not use it for edit history.
   - If `mapping_type` is `BROAD`, always populate `suggestion`.

5. **Validate and regenerate**:
   ```bash
   make validate_mapping ARGS="<path_to_mapping.tsv>"
   ```

### Working with Mixed-pattern Folders

When a folder contains multiple presentation families (oral + injectable, powder + solution, branded + generic, different release/device variants):

- **Treat existing high-quality EXACT rows as anchors.** Only overwrite when you have a specific, verified reason:
  - The current concept has the wrong route, dose form, strength, volume, or brand
  - The row is flagged by validate as incomplete or inconsistent and you confirmed the correction
  - The source data itself is anomalous and you are correcting to the defensible RxNorm presentation
- **Separate backfill from corrections.** If a folder needs both missing-row backfill and correction of a few existing rows, handle those as separate substeps.
- Before overwriting existing rows, explicitly compare the current and proposed mappings for route changes, dose-form changes, branded-to-generic or generic-to-branded changes, oral vs injectable swaps, powder vs solution swaps, and unit-dose vs multidose/device changes.

### Suppressing Known False Positives

When a validate flag is a confirmed false positive (the mapping is correct but the check cannot distinguish the legitimate case), add a row to the source's `suppressions.tsv`:
```
folder	issue	<source_id>
<folder_name>	<ISSUE_TYPE>	<id_value>
```
Record *why* in the `comment` column of the corresponding `mapping.tsv` row. Use `<source_id>=*` to suppress all rows of an issue type in a folder.

## Biosimilars

### Reference Data
Check `.claude/skills/map-drugs/biosimilars/` for per-INN reference files listing known biosimilars with FDA names and EU equivalents.
Check `.claude/skills/map-drugs/covid_vaccines.tsv` for known COVID-19 vaccine variant names, concentration tiers, and the current preferred RxNorm or RxNorm Extension concepts.

### Search Strategy
Run **all** of these queries:
1. EU biosimilar brand name
2. INN + strength + form with brand
3. INN + strength + form (unbranded)
4. INN alone (to discover FDA-suffixed variants)

### Scenario 1: FDA-suffixed INN exists in RxNorm
Map to the **unbranded FDA-suffixed concept** with `mapping_type` = **EXACT**. Do NOT use US-branded concepts.

Example: Insulin aspart Sanofi (EU) = insulin aspart-szjj (FDA):
- **concept_name**: `3 ML insulin aspart-szjj 100 UNT/ML Pen Injector`
- **mapping_type**: `EXACT`

### Scenario 2: No FDA equivalent
Map to the **plain INN (unbranded) concept** with `mapping_type` = **BROAD**, and construct the `suggestion`:
```
<volume> <INN>-xxxx <strength> <dose_form> [<EU Brand Name>]
```

Example: Izamby (denosumab biosimilar, 60 MG/ML, 1 ML prefilled syringe):
- **concept_name**: `1 ML denosumab 60 MG/ML Prefilled Syringe`
- **mapping_type**: `BROAD`
- **suggestion**: `1 ML denosumab-xxxx 60 MG/ML Prefilled Syringe [Izamby]`

### Important
- Do NOT use US brand names when EU has different name (e.g., `[Merilog]`, `[Zarxio]`)
- Do NOT use the originator brand for non-originator drug (e.g., `[Prolia]`, `[Xgeva]`)

## COVID-19 Vaccines

For COVID-19 vaccine folders or products, consult `covid_vaccines.tsv` before searching from scratch. It is intentionally cross-dataset and captures reusable guidance for:

- platform families such as vector, mRNA, and recombinant protein vaccines
- named ingredient and variant patterns such as `tozinameran`, `raxtozinameran`, `andusomeran`, `NVX-CoV2373`, and `Bimervax`
- dose-tier logic such as Comirnaty 3/10/30 microgram presentations
- conservative fallback rules for cases that should remain `BROAD` with product-specific `suggestion`

Use the TSV as a lookup and a starting point, not as a folder-specific mapping table. Still verify named ingredient or variant, platform, dose tier, route/form, and whether the row is one of the documented conservative `BROAD` cases.

