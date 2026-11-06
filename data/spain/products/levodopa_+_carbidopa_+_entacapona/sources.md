# Levodopa/carbidopa/entacapone mapping evidence

Reviewed 2026-11-06. This is the only Spain folder matching `levodopa_+_carbidopa_+_*`.

## Tablet presentations

The three missing parallel-import Stalevo rows match existing branded standard RxNorm tablet concepts at 75/18.75/200, 125/31.25/200 and 100/25/200 mg (levodopa/carbidopa/entacapone).

[AEMPS Stalevo 175 mg SmPC](https://cima.aemps.es/cima/dochtml/ft/103260036/FT_103260036.html) identifies the immediate-release film-coated tablet strength as 175/43.75/200 mg. Standard RxNorm searches did not return that strength; the clean Extension concepts round carbidopa to 43.8 mg. This is accepted as numeric rounding of the same presentation, with comments recording the difference. Generic tablets retain OMOP380324; the Stalevo tablet uses its matching branded Extension concept OMOP380333. The delayed-release Extension candidate and the 48.75 mg carbidopa candidate were rejected.

Source inconsistencies were retained in data.tsv and documented in mapping comments: 703500 has a contradictory des_dosific but consistently names 100/25/200 mg elsewhere; 703574 has 18.25 mg in des_dosific but 18.75 mg elsewhere; 770987 incorrectly uses a dosing-measure unit for entacapone while its product name and clinical presentation specify 200 mg.

## Lecigon intestinal gel

[AEMPS Lecigon SmPC](https://cima.aemps.es/cima/dochtml/ft/86092/FT_86092.html) states that each mL contains levodopa 20 mg, carbidopa monohydrate 5 mg (equivalent to anhydrous carbidopa 4.6 mg), and entacapone 20 mg. A cartridge contains 47 mL. Administration is continuous infusion into the intestine.

Standard RxNorm searches returned only two-ingredient carbidopa/levodopa suspension concepts. Extension searches found clean complete-combination concepts, including OMOP5216474 (`carbidopa 5 MG/ML / entacapone 20 MG/ML / levodopa 20 MG/ML Oral Gel [Lecigon]`). This retains the labeled strengths, all ingredients and the actual brand, improving the previous ingredient-incomplete fallback.

The mapping remains BROAD: the RxNorm definition of Oral Gel refers to the oral cavity, and no intestinal-gel dose form was found in the repository dose-form lookup. The suggestion uses the SmPC's stated anhydrous carbidopa equivalent, 4.6 mg/mL, while remaining constrained by the available RxNorm dose forms; it does not resolve that route limitation or assert that Lecigon is used in the mouth. The selected concept's 5 mg/mL carbidopa wording follows the monohydrate label rather than claiming 5 mg/mL anhydrous carbidopa. No density or hydrate conversion is inferred from the Extension name. The 47 mL prefix is unnecessary for this concentration-level continuous-infusion mapping; box-count candidates were rejected.
