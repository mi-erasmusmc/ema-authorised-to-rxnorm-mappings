# DESVENLAFAXINA mapping review — 2026-11-11

Reviewed all 16 presentations: 50 mg and 100 mg extended-release oral tablets, covering ENZUDE, PRISTIQ, ALTER, STADA, EXITAL, CINFA, NEURAXPHARM, and NORMON.

## Brand corrections

[AEMPS ENZUDE SmPC 75553](https://cima.aemps.es/cima/dochtml/ft/75553/FT_75553.html), sections 1–3, identifies ENZUDE 50/100 mg extended-release tablets containing the labeled amount of desvenlafaxine as succinate monohydrate. The existing Pristiq-branded concepts use a different brand. Correct:

| cod_nacion | Presentation | Standard RxNorm concept | concept_id | concept_code | Type |
|---|---|---|---|---|---|
| 688105 | ENZUDE 50 mg | desvenlafaxine 50 MG Extended Release Oral Tablet | 19134913 | 845106 | EXACT |
| 688182 | ENZUDE 100 mg | desvenlafaxine 100 MG Extended Release Oral Tablet | 19134911 | 845104 | EXACT |

Hecate searches confirmed both unbranded concepts and the existing Pristiq-branded concepts. A standard search for ENZUDE returned no matching branded concept. Standard RxNorm already captures ingredient, clinical strength, and release form, so no Extension search is needed solely to add brand.

## Retained mappings

- **PRISTIQ (688231, 688232):** retain standard branded concepts `19134914 / 845107` (50 mg) and `19134912 / 845105` (100 mg), EXACT. [AEMPS SmPC 75560](https://cima.aemps.es/cima/dochtml/ft/75560/FT_75560.html) confirms both strengths as desvenlafaxine, supplied as succinate monohydrate, in extended-release tablets.
- **ALTER, STADA, EXITAL, CINFA, NEURAXPHARM:** retain the standard unbranded desvenlafaxine 50/100 mg extended-release tablets, EXACT. The SmPCs explicitly express the strength as desvenlafaxine **as benzoate**, rather than the mass of benzoate salt: [ALTER 86688](https://cima.aemps.es/cima/dochtml/ft/86688/FT_86688.html), [STADA 86719](https://cima.aemps.es/cima/dochtml/ft/86719/FT_86719.html), [EXITAL 86733](https://cima.aemps.es/cima/dochtml/ft/86733/FT_86733.html), [CINFA 86783](https://cima.aemps.es/cima/dochtml/ft/86783/FT_86783.html), and [NEURAXPHARM 86785](https://cima.aemps.es/cima/dochtml/ft/86785/FT_86785.html). Each linked SmPC covers both strengths. Avoid succinate-specific concepts for these benzoate products.
- **NORMON:** retain the same standard unbranded concepts, EXACT. [AEMPS SmPC 89360](https://cima.aemps.es/cima/dochtml/ft/89360/FT_89360.html) states 50/100 mg desvenlafaxine and an extended-release tablet dose form.

No numerical salt/base conversion is needed: the clinical strengths are already expressed as desvenlafaxine. Search results also include succinate-specific and `24 HR` concepts; the existing base-ingredient extended-release concepts match the labeled clinical strengths and formulation without adding salt or release-duration assumptions.

## Validation

Two mapping corrections; all **16 rows remain EXACT**. Folder and mapping validators pass without new suppressions. Regenerate the combined Spain overview. This review covers the existing source snapshot and does not refresh the AEMPS inventory.
