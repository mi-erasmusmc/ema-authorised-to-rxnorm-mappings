# CLOMETIAZOL mapping review — 2026-11-11

Reviewed the single presentation, cod_nacion `654161`, DISTRANEURINE 192 mg soft capsules (registration `46186`).

[AEMPS SmPC 46186](https://cima.aemps.es/cima/dochtml/ft/46186/FT_46186.html), sections 2–3, confirms **192 mg clometiazol per capsule**, in a soft capsule. Section 4.2 specifies oral administration and swallowing the capsule whole. RxNorm uses the English ingredient spelling `chlormethiazole`.

Hecate standard RxNorm searches for `clomethiazole 192 MG Oral Capsule` and `chlormethiazole 192 MG Oral Capsule` returned:

- `19092285 / 251425`: `chlormethiazole 192 MG Oral Capsule`.
- Other results included 300 mg capsules and the unrelated Heminevrin brand; neither is preferable to the matching unbranded 192 mg capsule.

Replace Extension `41066132 / OMOP2264094`, `Chlormethiazole 192 MG Oral Capsule [Distraneurin]`, with standard `19092285 / 251425`, **EXACT**. The existing Extension concept adds brand detail without a clinically relevant improvement in ingredient, labeled strength, or dose form. Standard RxNorm therefore takes precedence under the current mapping rules, without needing to decide whether Distraneurine and Distraneurin are equivalent brand spellings.

The repository's `weight_conversions.tsv` records 192 mg clomethiazole as equivalent to 300 mg clomethiazole edisilate. No salt conversion is needed here: AEMPS explicitly labels the clinical presentation as 192 mg clometiazol, matching the selected concept.

Spain folder and mapping validators pass. The review covers the existing source snapshot rather than refreshing the AEMPS inventory.
