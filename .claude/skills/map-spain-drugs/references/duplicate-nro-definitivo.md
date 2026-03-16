# Duplicate `nro_definitivo`

Use this reference when a Spain row inherited the wrong EMA concept because multiple presentations share the same EMA-linked `nro_definitivo`.

## Why it happens

Some CIMA rows reuse one `nro_definitivo` across different pack sizes or presentation variants. The auto-link chooses one EMA mapping for that shared identifier, so at least one Spain row can inherit the wrong concept.

## Common pattern

The most common failure mode is a volume mismatch:

| cod_nacion | nro_definitivo | des_dosific | Correct EMA MA |
|---|---|---|---|
| 764394 | 1201515001 | 25 mg/ml inyectable 4 ml | EU/1/20/1515/001 |
| 764395 | 1201515001 | 25 mg/ml inyectable 16 ml | EU/1/20/1515/003 |

The larger volume row is often mapped to the smaller presentation's concept.

## How to review

1. Compare `des_dosific` in `data.tsv` with the mapped `concept_name` in `mapping.tsv`.
2. If strength or volume differs, search for the correct concept with `find-concepts`.
3. Update only the affected `cod_nacion` row and add a short comment explaining the override.

Example comment:

```text
nro_definitivo shared with 4 ml pack; manually corrected to 16 ml concept
```

## Product families worth checking

- Bevacizumab biosimilars with 4 ml and 16 ml vial variants
- Enoxaparin products with many dose-banded pack variants
- Onasemnogene abeparvovec with weight-banded pack entries
- Adalimumab biosimilars with 0.4 ml and 0.8 ml syringes

## Repo-level duplicate report

Run the helper script from the repo root:

```bash
make find_duplicate_nros
```

Add `--folder <ingredient_slug>` to limit the report to one Spain product folder.
