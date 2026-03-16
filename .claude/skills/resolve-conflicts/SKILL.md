---
name: resolve-conflicts
description: Find and resolve conflicting mappings between EMA and Latvia RxNorm mapping files. Use when asked to find, review, or fix conflicts between ema-to-rxnorm.tsv and latvia-to-rxnorm.tsv.
---

# Resolve Mapping Conflicts

Find and resolve cases where the same product (identified by `ma_number`/`product_id`) is mapped to different RxNorm concepts in `ema-to-rxnorm.tsv` vs `latvia-to-rxnorm.tsv`.

## When to Use

When asked to find or fix conflicts between EMA and Latvia RxNorm mappings, or to align mappings across both sources.

## Prerequisites

Refer to the `find-concepts` skill for searching RxNorm concepts, and the `map-drugs` skill for general mapping principles.

## Step 1: Find Conflicts

```bash
make find_conflicts ARGS="[limit]"
```

- With no arguments: prints all conflicting EMA folders
- With a number argument: prints only that many folders (useful for batch work)

Conflicts are **grouped by EMA folder** since all ma_numbers in a folder share the same `mapping.tsv` and should be resolved together. Output shows for each folder:
- Product name and conflicting ma_numbers
- **The EMA folder path** and **all Latvia folder paths** containing `mapping.tsv` files to edit

## Step 2: Resolve in Parallel

**Launch one subagent per conflict group** using the Task tool so they run in parallel with isolated context. Each subagent resolves one EMA folder group independently.

The prompt for each subagent should include:
- The EMA folder path and all Latvia folder paths from the script output
- Instructions to follow the resolution steps below
- The `map-drugs`, `find-concepts`, `map-ema-drugs`, and `map-latvia-drugs` skill files as context (read them and include their contents in the prompt)

Example:
```
Task(subagent_type="general-purpose", prompt="""
Resolve mapping conflicts for <product_name>.

EMA folder: <ema_folder_path>
Latvia folders:
- <latvia_folder_path_1>
- <latvia_folder_path_2>

<include skill contents for map-drugs, find-concepts, map-ema-drugs, map-latvia-drugs>

Follow the resolution steps:
1. Read the EMA mapping.tsv and all Latvia mapping.tsv files
2. Read source data (parsed_data*.tsv for EMA, info.txt for Latvia)
3. Determine the correct mapping for each conflicting ma_number
4. Update the less accurate mapping.tsv file(s)
""")
```

Launch all subagents in a single message so they run concurrently.

## Resolution Steps (for subagents)

### Investigate
1. **Read the EMA `mapping.tsv`** to see all mappings in that folder
2. **Read each Latvia `mapping.tsv`** to see all mappings
3. **Read source data** — `parsed_data*.tsv` (EMA) and `info.txt` (Latvia) to understand the actual product (strength, form, pack size)
4. **Compare the mappings** for each conflicting ma_number — determine which concept is more accurate, or whether both are wrong

### Common Conflict Patterns

**Different strengths or dose forms chosen**
Read the source data carefully. The correct concept should match the actual strength and pharmaceutical form of the product. Use `find-concepts` to search if needed.

**One side is BROAD, the other is EXACT**
Prefer the EXACT mapping if it accurately represents the product. If neither is exact, both should be BROAD with the same concept.

**Branded vs unbranded concept**
When the brand name is the same in EU and US (e.g., Tobi, Erivedge, Lantus), always prefer the **branded** RxNorm concept — it is more precise. Only use unbranded concepts when the EU and US brands differ. See the `map-drugs` skill for full branding rules.

**Both mapped to valid but different concepts**
Investigate which concept better represents the product. Consider:
- Does the concept match the strength exactly?
- Does the dose form match (e.g., Pen Injector vs Injectable Solution)?
- Is one correctly branded and the other unbranded? Prefer branded when the brand matches across EU/US.
Both mappings should converge on the same `concept_id`.

### Update
Edit the `mapping.tsv` in the folder that has the less accurate mapping:
- Update `concept_id`, `concept_name`, `concept_code`, `mapping_type` to match the correct mapping
- Update `last_updated_date` to today's date
- Add a `comment` noting the alignment if helpful

**Important**: Only edit the `mapping.tsv` in the product-level folder (the source of truth). The combined `ema-to-rxnorm.tsv` and `latvia-to-rxnorm.tsv` files are regenerated from these folders.

## Step 3: Regenerate Combined Files

After all subagents complete, regenerate the combined TSV files from the updated individual `mapping.tsv` files:

```bash
make generate_mapping_overviews
```

This rebuilds both `ema-to-rxnorm.tsv` and `latvia-to-rxnorm.tsv` from individual mapping files.

## Step 4: Verify

Re-run the conflict finder to confirm the conflict count decreased:

```bash
make find_conflicts
```
