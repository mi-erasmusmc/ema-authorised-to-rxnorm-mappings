
## Mapping review 2026-11-09

Source: https://cima.aemps.es/cima/dochtml/p/90346/P_90346.html

Norditropin FlexPro 10 mg/1.5 mL is 6.7 mg/mL (10/1.5 = 6.6667), not the erroneous 10 mg/mL in des_dcp. The 15 mg/1.5 mL product is 10 mg/mL. Source ID 771542 is mapped using its product name and label.

## Device and formulation review 2026-11-09

- [AEMPS MiniQuick SmPC](https://cima.aemps.es/cima/dochtml/ft/61813/FT_61813.html): the 0.2–2 mg strengths yield their labeled dose in 0.25 mL and are supplied as single-use syringes. Standard RxNorm has exact unbranded 0.25 mL Prefilled Syringe concepts at all ten corresponding concentrations (0.8–8 mg/mL). These replace total-dose Injection concepts carrying the different US Genotropin brand.
- [AEMPS Kabipen SmPC](https://cima.aemps.es/cima/dochtml/ft/59427/FichaTecnica_59427.html): reconstituted concentrations are 5.3 and 12 mg/mL; the dual-chamber presentation is used with reusable Kabipen or supplied inside a multidose GoQuick device. It is not a single-use injection.
- AEMPS registration APIs for [59427](https://cima.aemps.es/cima/rest/medicamento?nregistro=59427) and [60117](https://cima.aemps.es/cima/rest/medicamento?nregistro=60117) distinguish the national codes: 678006 (5.3 mg) and 678005 (12 mg) are prefilled devices; 988998 (5.3 mg) and 696120 (12 mg) are separate dual-chamber vials. Use clean Extension Genotonorm Pen Injector concepts for the prefilled devices. The separate 5.3 mg vial has a clean Extension concentration-based Injectable Solution concept; the separate 12 mg presentation has an exact standard 1 mL 12 mg/mL Cartridge concept for the reusable system. Do not map 5.3 mg to 5 mg.
- [AEMPS Zomacton 4 mg SmPC](https://cima.aemps.es/cima/dochtml/ft/59483/FichaTecnica_59483.html): this multidose powder vial allows alternative reconstitution concentrations of 1.3 or 3.3 mg/mL. Use clean Extension `Somatropin 4 MG Injectable Solution [Zomacton]`, retaining vial content and multidose powder form without selecting one of the alternative concentrations. For the 10 mg/mL product ([registration 70642](https://cima.aemps.es/cima/dochtml/ft/70642/FT_70642.html)), use standard `somatropin 10 MG/ML Injectable Solution [Zomacton]`.
- Saizen's source presentation is 6 mg in a 1.03 mL cartridge at 5.83 mg/mL. Standard search returned a concentration-only concept and a mismatched 1.5 mL concept. Extension provides the clean matching 1.03 mL cartridge (43292489 / OMOP560927). Existing 1.5 and 2.5 mL 8 mg/mL Saizen Extension mappings are retained.
- Use the standard volume-specific Norditropin Pen Injector concepts for the 1.5 mL 5, 10 and 15 mg pens. Preserve the existing source-data correction for national code 771542.

### Omnitrope and biosimilar identity

No somatropin-specific biosimilar reference file was present in the repository. [FDA Purple Book entry 021426](https://purplebooksearch.fda.gov/index.cfm?blaNo=021426&event=productdetails) identifies US Omnitrope as Sandoz somatropin (unsuffixed), licensed under 351(a), including 5 mg/1.5 mL and 10 mg/1.5 mL multidose cartridges. Thus the matching Omnitrope-branded standard concepts identify the product directly; retain them rather than substituting another brand or inventing an FDA suffix. Preserve the existing clean volume-specific Omnitrope 15 mg/1.5 mL Extension concept. RxNorm ingredient, brand, strength/form and unbranded searches found no FDA-suffixed somatropin variant.

Extension changes above resolve a missing strength, dose form or cartridge volume, rather than adding brand alone. Existing Humatrope, NutropinAQ/Nutropin and clinically appropriate standard cartridge mappings are retained.

### Validator exceptions

Seven row-specific INCONSISTENT_CONCEPT suppressions preserve verified differences hidden by the source signature: Kabipen's prefilled devices versus separate dual-chamber vials (678005, 678006, 696120, 988998), and the correct 15 mg/1.5 mL FlexPro pens versus the 10 mg/1.5 mL pen with erroneous des_dcp (767797, 771297, 771542). The corresponding mapping comments explain each exception. Do not harmonise these presentations to one concept.
