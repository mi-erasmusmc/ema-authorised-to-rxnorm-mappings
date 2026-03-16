---
name: map-spain-drugs
description: Map Spanish national medicinal products from the AEMPS CIMA registry to RxNorm standard concepts. Use when asked to map a Spanish product, review or correct a Spain `mapping.tsv`, audit a Spain product folder, fix a bad EMA auto-link via `nro_definitivo`, or handle Spain-specific cases such as duplicate `nro_definitivo`, generics, biosimilars, herbal products, or radiopharmaceuticals.
---

# Map Drugs: Spanish Products

Map Spanish national medicinal products (AEMPS CIMA registry) to RxNorm standard concepts.

## Prerequisites

Refer to the `find-concepts` skill for RxNorm searches and the `map-drugs` skill for general mapping rules.

## Resources

- Use `audit_folder.py` to identify missing, stale, incomplete, or broad mappings in a Spain product folder.
- Use `audit_all.py` to audit all Spain product folders at once and surface the worst offenders by issue type.
- Use `apply_mappings.py` to merge targeted TSV updates into `mapping.tsv` without rewriting unchanged rows.
- Use `scripts/list_folder_patterns.py` to summarize repeated presentation patterns before concept search, especially in large folders.
- Use `scripts/run_clean_room_batch.py` for conservative bulk cleanup when missing rows can be filled from existing `EXACT` mappings in the same folder.
- Use `scripts/find_duplicate_nros.py` when you need a repo-level report of shared EMA-linked `nro_definitivo` values.
- Read `references/duplicate-nro-definitivo.md` when the auto-link produced the wrong volume, pack variant, or biosimilar concept.

## How Spain Mappings Work

Spain products are auto-linked to EMA mappings via `nro_definitivo` on first setup:

```text
EU/1/20/1476/001 -> strip "EU" + remove "/" -> 1201476001 = nro_definitivo
```

`link_ema_mappings.py` writes `mapping.tsv` per product folder. It is incremental: existing rows are not overwritten, new `cod_nacion` values are auto-mapped, and stale auto-generated rows are pruned.

Treat `mapping.tsv` as the editable source of truth. Manual corrections survive reruns. To reset a row to the current auto-link, delete that row from `mapping.tsv` and rerun `link_ema_mappings.py`.

## Input Files

Each product folder under `data/spain/products/{ingredient_slug}/` contains:

- `data.tsv`: One row per registered presentation with `cod_nacion`, `nro_definitivo`, `des_nomco`, `des_dcp`, `des_dosific`, `principios_activos`, `forma_farmaceutica`, `vias_administracion`, `atc`, `laboratorio_titular`, `sw_generico`, `sw_base_a_plantas`, `biosimilar`, and `radiofarmaco`.
- `mapping.tsv`: Current mappings. These are initially auto-generated and then manually maintained.

`cod_nacion` is the stable row key. `nro_definitivo` is a product-level identifier that may be shared across multiple pack variants.

## Workflow

1. Audit the folder:
   ```bash
   make audit_folder ARGS="data/spain/products/<folder>/"
   ```
   The default output is summary-first. It shows issue counts and repeated product patterns so you can decide quickly whether the folder is batchable.

   Use drill-down mode only when needed:
   ```bash
   make audit_folder ARGS="data/spain/products/<folder>/ --details"
   make audit_folder ARGS="data/spain/products/<folder>/ --details --issue MISSING"
   ```

   Review these issue types:
   - `MISSING`: `cod_nacion` exists in `data.tsv` but not in `mapping.tsv`
   - `NO_CONCEPT`: mapping row has no `concept_id`
   - `NO_TYPE`: mapping row has a concept but no `mapping_type`
   - `BROAD`: existing broad match that may be upgradeable
   - `REVIEW_VOLUME`: likely single-use injectable mapped to a concentration-only concept; search for a volume-specific `Injection` concept before accepting `EXACT`
   - `STALE_MAPPING`: mapping row points to a `cod_nacion` no longer present in `data.tsv`
   - `NRO_MISMATCH`: `nro_definitivo` in `mapping.tsv` disagrees with `data.tsv`
   - `DUPLICATE_DATA`: duplicate `cod_nacion` in `data.tsv`
   - `DUPLICATE_MAPPING`: duplicate `cod_nacion` in `mapping.tsv`
   - `INCONSISTENT_CONCEPT`: EXACT rows sharing the same clinical description and dose form but mapped to different concept_ids. For generics (`sw_generico=1`) this is usually a real error, but a legitimate split can occur when some products in the folder have their own RxNorm branded concept (e.g. `[Yargesa]`) while others do not — in that case the different concepts are both correct and the flag is a structural false positive. For branded products the check is per-brand key from `des_nomco`, not per manufacturer, so it only flags conflicts within the same branded line — **do not resolve by collapsing to a plain non-suffixed concept**. When the folder contains biosimilars, always read the biosimilar reference in `.claude/skills/map-drugs/biosimilars/` and apply the correct FDA-suffixed unbranded concept (Scenario 1) or BROAD+suggestion (Scenario 2). Never strip FDA suffixes (`-atto`, `-adaz`, `-fkjp`, etc.) in the name of harmonisation.

2. Read `data.tsv` to understand the presentation set, strengths, volumes, and flags for the product.

   For large folders, summarize the repeated patterns first:
   ```bash
   make list_folder_patterns ARGS="data/spain/products/<folder>/"
   ```
   This is read-only. It helps you spot which rows truly share the same clinical pattern before you reuse a concept across them.

   If the audit shows that `MISSING` is the dominant issue type, narrow to unmapped rows only:
   ```bash
   make list_folder_patterns ARGS="data/spain/products/<folder>/ --missing-only"
   ```

3. Search RxNorm concepts via the `find-concepts` skill. Translate Spanish ingredient names to English before searching (e.g., `acido zoledronico` → `zoledronic acid`):
   ```bash
   make find_concepts ARGS='"zoledronic acid 4 MG/5ML injection" "zoledronic acid 4 mg" "zoledronic acid injection"'
   ```
   Read the dose-form definitions returned by concept search and use them in the mapping decision. They are part of the evidence, not incidental output. In particular:
   - `Injection` may include a single-use sterile solution, suspension, or reconstituted powder intended for parenteral use
   - `Injectable Solution` may include a multiple-use solution or reconstituted powder intended to be injected
   - the exact wording often determines whether a powder-and-solvent, unit-dose, multidose, prefilled syringe, or metered-dose presentation can be mapped `EXACT` or must stay `BROAD`
   Do not assume a concept is too broad or too narrow until you have checked the dose-form definition that `find_concepts` printed for that concept family.
   When the auto-link looks suspicious, check the duplicate-`nro_definitivo` reference before changing the row.

4. Prepare a TSV containing only the rows you want to create or update. Do not rewrite unchanged rows.

   For mixed-pattern folders, default to **missing rows only**. Do not do full-folder rewrites when the folder contains multiple presentation families such as oral plus injectable, powder plus solution, unit-dose plus multidose, branded plus generic, or different release/device variants.

   Treat existing high-quality `EXACT` rows as anchors. Only overwrite an existing mapped row when you have a specific, verified reason, for example:
   - the current concept has the wrong route, dose form, strength, volume, or brand
   - the row is flagged by audit as incomplete or inconsistent and you confirmed the correction
   - the source data itself is anomalous and you are correcting to the defensible RxNorm presentation

   Before overwriting existing rows in a mixed-pattern folder, explicitly compare the current and proposed mappings for:
   - route changes
   - dose-form changes
   - branded-to-generic or generic-to-branded changes
   - oral vs injectable swaps
   - powder/granules vs solution/suspension swaps
   - unit-dose vs multidose / device changes

   If a folder needs both missing-row backfill and correction of a few existing rows, handle those as separate substeps instead of generating one folder-wide replacement table.

   Use `comment` only for mapping rationale that another reviewer would need to understand later, such as salt conversions, metered-versus-delivered dose decisions, biosimilar handling, or a manual correction caused by bad source data. Do not use `comment` for edit history like "upgraded mapping" or "changed to better concept".

   If `mapping_type` is `BROAD`, always populate `suggestion` with the ideal concept name you would use if standard RxNorm had the exact presentation.

5. Apply changes with the helper script:
   ```bash
   make apply_mappings ARGS="data/spain/products/<folder>/mapping.tsv" <<'EOF'
   cod_nacion	nro_definitivo	concept_id	concept_name	concept_code	mapping_type	comment	suggestion
   12345	72707	617312	atorvastatin 10 MG Oral Tablet	370584	EXACT
   EOF
   ```
   `apply_mappings.py` sets `last_updated_date` to today when not supplied and now rejects duplicate `cod_nacion` rows in the update input.

6. Backfill missing dates when needed:
   ```bash
   make apply_mappings ARGS="data/spain/products/<folder>/mapping.tsv --backfill-dates"
   ```

7. Validate and regenerate overviews:
   ```bash
   make validate_mapping ARGS="data/spain/products/<folder>/mapping.tsv"
   make generate_mapping_overviews ARGS=spain  # regenerate Spain only
   ```

## Conservative Bulk Cleanup

For low-risk bulk work, use the batch helper:

```bash
make run_clean_room_batch ARGS="--apply --limit 60 --pass-size 3"
```

It only selects folders where every missing row can be filled from an existing `EXACT` mapping in the same folder using the same full clinical pattern, then validates and audits each folder. This is a cleanup tool, not a substitute for concept search.

## Spain-specific Notes

- Generics: if `sw_generico=1`, prefer unbranded RxNorm concepts. Exception: if RxNorm has a standard concept for the product's own brand name (e.g. `[Yargesa]`), use it — a matching branded concept is more precise than unbranded. The rule prevents mapping a generic to the *originator's* brand (e.g. MIGLUSTAT ACCORD → [Zavesca]), not from using the generic brand's own concept when RxNorm recognises it.
- Branded products: when `sw_generico=0` and RxNorm has the matching brand, use the branded RxNorm concept and keep it. Do not replace a correct branded concept with a generic one for harmonisation. Only fall back to a generic concept when no matching branded RxNorm concept exists.
- Spanish names: `data.tsv` may contain Spanish ingredient names such as `acido zoledronico`; search RxNorm with the English ingredient name.
- Spanish solid-dose form nuance: `COMPRIMIDO BUCODISPERSABLE` or `liotab` rows sometimes align best to an RxNorm chewable-tablet concept rather than a plain oral-tablet concept. If RxNorm exposes the matching strength as `Chewable Tablet`, prefer that exact concept and record the rationale in `comment` instead of downgrading automatically to `BROAD`.
- Salt/base strength decisions: when Spain labels the clinical presentation in base terms in `des_dcp` or `des_dosific`, prefer the RxNorm concept that matches the labeled clinical strength and dose form, even if `principios_activos` lists a salt form. Check `weight_conversions.tsv` when the salt/base relationship could change the apparent strength, and use `comment` only if the choice would not be obvious to a later reviewer.
- Single-use injectables: when `des_dcp` includes a volume such as `2 ml` or `5 ml`, prefer the volume-specific RxNorm `Injection` concept if one exists. Treat a concentration-only concept such as `phenytoin sodium 50 MG/ML Injection` as a review signal, not the default exact match.
- Herbal products: if `sw_base_a_plantas=1`, still map to the best available RxNorm concept. When RxNorm only has an ingredient-, extract-, or dose-form-level botanical concept, use that concept with `mapping_type = BROAD` and populate `suggestion` with the ideal full Spanish presentation.
- Radiopharmaceuticals: if `radiofarmaco=1`, follow the specialist handling in `map-drugs`.
- Biosimilars: if `biosimilar=1`, follow the biosimilar rules and references in `map-drugs`. Biosimilar folders will legitimately have many different concept_ids for similar presentations because each biosimilar has its own FDA-suffixed INN (e.g. `adalimumab-atto`, `adalimumab-adaz`). **Never harmonise biosimilar rows to a plain non-suffixed concept** — doing so loses the biosimilar-specific identity. Check `.claude/skills/map-drugs/biosimilars/<inn>.tsv` for the EU→FDA name mapping before touching any biosimilar row.
