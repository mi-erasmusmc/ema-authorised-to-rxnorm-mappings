# AMOXICILINA mapping review — 2026-11-11

Reviewed all 143 presentations, including capsule/tablet strengths, bottle concentrations, sachets, dispersible tablets, and injectable powders. RxNorm and RxNorm Extension candidates were searched through Hecate using the repository's `find_concepts` tool.

## Corrections

- **NORMON 500 mg sachets (611608, 694734, 694735):** [AEMPS SmPC 62785](https://cima.aemps.es/cima/dochtml/ft/62785/FT_62785.html), sections 2–3, confirms powder for oral suspension, despite `forma_farmaceutica` saying solution. Use Extension `43215451 / OMOP480457`, BROAD because the concept omits sachet strength.
- **ARDINE 500 mg sachets (694741, 694742):** [AEMPS SmPC 52371](https://cima.aemps.es/cima/dochtml/ft/52371/FT_52371.html), sections 1–3, confirms 500 mg per sachet. Correct the suggestion from 1000 mg to 500 mg. The existing strengthless suspension-powder concept remains BROAD. The SmPC was retrieved directly because the browser tool could not open it.
- **SANDOZ 750 mg film-coated tablets (695639, 695640):** Hecate confirms `19061770 / 249505` for `amoxicillin 750 MG Oral Tablet`. The stored concept code incorrectly repeated the OMOP concept ID.

## Dispersible tablets

The source products are dispersible tablets, rather than tablets intended to disintegrate in the mouth. AEMPS section 4.2 describes dispersion in water, sometimes with the alternative of swallowing with water:

- [SANDOZ 750/1000 mg, SmPC 70493](https://cima.aemps.es/cima/dochtml/ft/70493/FT_70493.html)
- [ALMUS 500/750/1000 mg, SmPC 81389](https://cima.aemps.es/cima/dochtml/ft/81389/FT_81389.html)
- [COMBIX 1000 mg, SmPC 84016](https://cima.aemps.es/cima/dochtml/ft/84016/FT_84016.html)
- [PENSA PHARMA 750/1000 mg, SmPC 84172](https://cima.aemps.es/cima/dochtml/ft/84172/FT_84172.html)
- [TARBIS FARMA 1000 mg, SmPC 84719](https://cima.aemps.es/cima/dochtml/ft/84719/FT_84719.html)
- [SUN 1000 mg, SmPC 85401](https://cima.aemps.es/cima/dochtml/ft/85401/FT_85401.html)
- [CLAMOXYL 1000 mg, SmPC 59133](https://cima.aemps.es/cima/dochtml/ft/59133/FT_59133.html)
- [CLAMOXYL 750 mg, SmPC 51426](https://cima.aemps.es/cima/dochtml/ft/51426/FT_51426.html)

Use clean Extension `Tablet for Oral Suspension` concepts for 500 mg (`36257292 / OMOP3108167`, two rows) and 1000 mg (`36275155 / OMOP3126030`, fourteen rows), EXACT. These preserve the labeled formulation more closely than `Disintegrating Oral Tablet`, whose repository dose-form definition specifies dissolution in the mouth.

No clean 750 mg `Tablet for Oral Suspension` concept surfaced in standard RxNorm or Extension searches. Use standard `amoxicillin 750 MG Oral Tablet` (`19061770 / 249505`) BROAD for nine rows, preserving unit strength and tablet form; suggest `Amoxicillin 750 MG Tablet for Oral Suspension`.

The validator groups PENSA PHARMA's 750 mg dispersible tablets with ordinary NORMON/ARDINE tablets because the source collapses both to `COMPRIMIDO`. The shared Oral Tablet concept is correctly EXACT for the ordinary tablets and BROAD for the dispersible tablets. Seven targeted `INCONSISTENT_TYPE` suppressions cover this confirmed false positive; row comments explain the distinction.

## Retained mappings and limits

- Standard unbranded concepts remain appropriate for capsules, ordinary tablets, and bottle suspensions. Bottle concentrations are 25 mg/ml or 50 mg/ml; pack volume adds no dose distinction.
- Sachets remain BROAD: searches did not find clean strength-specific suspension-powder concepts at 250, 500, or 1000 mg. Do not infer a final concentration from an unspecified glass of water, or substitute a tablet for a sachet.
- The 250/500/1000 mg injection concepts remain EXACT for powder vials expressed as total drug content. [AMITRON 500 mg SmPC 56265](https://cima.aemps.es/cima/dochtml/ft/56265/FT_56265.html) and [1000 mg SmPC 56266](https://cima.aemps.es/cima/dochtml/ft/56266/FT_56266.html) support the powder-vial presentation; reconstitution/dilution varies with administration. The 250 mg SmPC 56264 returned HTTP 404, so that row was assessed against the local presentation and matching Extension concept, without fresh SmPC confirmation.

The review covers the repository's existing source snapshot; it does not refresh the AEMPS registration inventory.
