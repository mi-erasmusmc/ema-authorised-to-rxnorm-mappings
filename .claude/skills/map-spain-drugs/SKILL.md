---
name: map-spain-drugs
description: Map Spanish national medicinal products from the AEMPS CIMA registry to RxNorm standard concepts. Use when asked to map a Spanish product, review or correct a Spain `mapping.tsv`, validate a Spain product folder, fix a bad EMA auto-link via `nro_definitivo`, or handle Spain-specific cases such as duplicate `nro_definitivo`, generics, biosimilars, herbal products, or radiopharmaceuticals.
---

# Map Drugs: Spanish Products

Map Spanish national medicinal products (AEMPS CIMA registry) to RxNorm standard concepts.

## Prerequisites

Refer to the `find-concepts` skill for RxNorm searches and the `map-drugs` skill for general mapping rules and the standard workflow.

## Resources

- Use `validate_all.py` to validate Spain product folders — pass a folder path for a single folder, or omit it to validate all folders at once.
- Use `apply_mappings.py` to merge targeted TSV updates (by `cod_nacion`) into `mapping.tsv` without rewriting unchanged rows.
- Use `apply_pattern_mappings.py` to expand one mapping decision per presentation pattern into all matching `cod_nacion` rows (useful for folders with many pack variants of the same presentation).
- Use `make list_folder_patterns` to summarize repeated presentation patterns before concept search, especially in large folders.
- Use `scripts/run_clean_room_batch.py` for conservative bulk cleanup when missing rows can be filled from existing `EXACT` mappings in the same folder.
- Use `scripts/find_duplicate_nros.py` when you need a repo-level report of shared EMA-linked `nro_definitivo` values.
- Read `references/duplicate-nro-definitivo.md` when the auto-link produced the wrong volume, pack variant, or biosimilar concept.

## How Spain Mappings Work

Spain products are linked to EMA mappings via `nro_definitivo`:

```text
EU/1/20/1476/001 -> strip "EU" + remove "/" -> 1201476001 = nro_definitivo
```

Treat `mapping.tsv` as the editable source of truth. Manual corrections survive data refreshes.

## Input Files

Each product folder under `data/spain/products/{ingredient_slug}/` contains:

- `data.tsv`: One row per registered presentation with `cod_nacion`, `nro_definitivo`, `des_nomco`, `des_dcp`, `des_dosific`, `principios_activos`, `forma_farmaceutica`, `vias_administracion`, `atc`, `laboratorio_titular`, `sw_generico`, `sw_base_a_plantas`, `biosimilar`, and `radiofarmaco`.
- `mapping.tsv`: Current mappings. These are initially auto-generated and then manually maintained.

`cod_nacion` is the stable row key. `nro_definitivo` is a product-level identifier that may be shared across multiple pack variants.

## Workflow

Follow the standard mapping workflow in `map-drugs`. Spain-specific deviations:

1. **Validate:**
   ```bash
   make validate_spain ARGS="data/spain/products/<folder>/"
   ```
   The default output is summary-first. Use drill-down mode only when needed:
   ```bash
   make validate_spain ARGS="data/spain/products/<folder>/ --details"
   make validate_spain ARGS="data/spain/products/<folder>/ --details --issue MISSING"
   ```

   Spain-specific issue types beyond those in `map-drugs`:
   - `NRO_MISMATCH`: `nro_definitivo` in `mapping.tsv` disagrees with `data.tsv`
   - `INCONSISTENT_CONCEPT`: for branded products the check is per-brand key from `des_nomco`, not per manufacturer — **do not resolve by collapsing to a plain non-suffixed concept**. When the folder contains biosimilars, always read the biosimilar reference in `.claude/skills/map-drugs/biosimilars/` and apply the correct FDA-suffixed unbranded concept.
   - `INCONSISTENT_TYPE`: rows sharing the same clinical signature and the same concept_id but with different `mapping_type` values. Resolve by applying the correct type consistently.

   When the auto-link looks suspicious, check the duplicate-`nro_definitivo` reference before changing the row.

2. **Search:** Translate Spanish ingredient names to English before searching (e.g., `acido zoledronico` -> `zoledronic acid`).

3. **Apply changes** — two options:

   **By ID** (targeted updates):
   ```bash
   make apply_mappings ARGS="data/spain/products/<folder>/mapping.tsv" <<'EOF'
   cod_nacion	nro_definitivo	concept_id	concept_name	concept_code	mapping_type	comment	suggestion
   12345	72707	617312	atorvastatin 10 MG Oral Tablet	370584	EXACT
   EOF
   ```

   **By pattern** (one decision -> many rows):
   ```bash
   make apply_spain_patterns ARGS="data/spain/products/<folder>/mapping.tsv" <<'EOF'
   des_dcp	vias_administracion	forma_farmaceutica	sw_generico	des_dosific	unidad_contenido	concept_id	concept_name	concept_code	mapping_type	comment	suggestion
   ATORVASTATINA 10 MG COMPRIMIDOS	ORAL	COMPRIMIDO	1	10 mg	comprimidos	617312	atorvastatin 10 MG Oral Tablet	370584	EXACT
   EOF
   ```

   Backfill missing dates:
   ```bash
   make apply_mappings ARGS="data/spain/products/<folder>/mapping.tsv --backfill-dates"
   ```

4. **Validate and regenerate:**
   ```bash
   make validate_mapping ARGS="data/spain/products/<folder>/mapping.tsv"
   make generate_mapping_overviews ARGS=spain
   ```

## Conservative Bulk Cleanup

For low-risk bulk work, use the batch helper:

```bash
make run_clean_room_batch ARGS="--apply --limit 60 --pass-size 3"
```

It only selects folders where every missing row can be filled from an existing `EXACT` mapping in the same folder using the same full clinical pattern, then validates each folder.

## Spain-specific Notes

- Generics: if `sw_generico=1`, prefer unbranded RxNorm concepts. Exception: if RxNorm has a standard concept for the product's own brand name (e.g. `[Yargesa]`), use it — a matching branded concept is more precise than unbranded. The rule prevents mapping a generic to the *originator's* brand (e.g. MIGLUSTAT ACCORD -> [Zavesca]), not from using the generic brand's own concept when RxNorm recognises it.
- Branded products: when `sw_generico=0` and RxNorm has the matching brand, use the branded RxNorm concept and keep it. Do not replace a correct branded concept with a generic one for harmonisation. Only fall back to a generic concept when no matching branded RxNorm concept exists.
- If standard RxNorm already has an adequate unbranded concept and RxNorm Extension only adds the matching brand name without adding any other clinically relevant detail, keep the standard RxNorm concept instead of upgrading to Extension just for brand.
- If Extension is already required for some other clinically relevant reason, such as dose form, release type, route-specific presentation, or clinically relevant single-use volume, it is acceptable to keep or choose the branded Extension concept when the brand also matches.
- Spanish solid-dose form nuance: `COMPRIMIDO BUCODISPERSABLE` or `liotab` rows sometimes align best to an RxNorm chewable-tablet concept rather than a plain oral-tablet concept. If RxNorm exposes the matching strength as `Chewable Tablet`, prefer that exact concept and record the rationale in `comment`.
- Salt/base strength decisions: when Spain labels the clinical presentation in base terms in `des_dcp` or `des_dosific`, prefer the RxNorm concept that matches the labeled clinical strength and dose form, even if `principios_activos` lists a salt form. Check `weight_conversions.tsv` when the salt/base relationship could change the apparent strength.
- Single-use injectables: when `des_dcp` includes a volume such as `2 ml` or `5 ml`, prefer the volume-specific RxNorm `Injection` concept if one exists.
- Herbal products: if `sw_base_a_plantas=1`, still map to the best available RxNorm concept. When RxNorm only has an ingredient-, extract-, or dose-form-level botanical concept, use that concept with `mapping_type = BROAD` and populate `suggestion`.
- Radiopharmaceuticals: if `radiofarmaco=1`, follow the specialist handling in `map-drugs`.
- Biosimilars: if `biosimilar=1`, follow the biosimilar rules and references in `map-drugs`. **Never harmonise biosimilar rows to a plain non-suffixed concept.** Check `.claude/skills/map-drugs/biosimilars/<inn>.tsv` for the EU->FDA name mapping before touching any biosimilar row.
