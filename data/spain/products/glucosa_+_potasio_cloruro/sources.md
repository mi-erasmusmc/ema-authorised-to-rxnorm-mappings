# Glucose / potassium chloride mapping rationale

Reviewed 2026-11-06 using Hecate standard RxNorm and Extension searches for
500 mL and 1000 mL presentations at both potassium strengths.

All 21 presentations can be mapped EXACT using the labeled clinical strengths:

| Volume | Potassium chloride | Concept ID | Code | Vocabulary |
| --- | --- | --- | --- | --- |
| 1000 mL | 0.02 mEq/mL | 19076326 | 309783 | RxNorm |
| 1000 mL | 0.04 mEq/mL | 19076329 | 309786 | RxNorm |
| 500 mL | 1.5 mg/mL | 21148144 | OMOP330784 | RxNorm Extension |
| 500 mL | 3 mg/mL | 21108893 | OMOP330757 | RxNorm Extension |

Each concept also specifies glucose 50 mg/mL and Injection. Extension is needed
for the missing 500 mL single-use presentation; these are clean unbranded
concepts without suppliers or box counts. Do not use the superficially similar
500 mL standard concepts that add sodium chloride as an active ingredient.

## Strength and volume evidence

- [Kabi 0.02 mEq/mL SmPC](https://cima.aemps.es/cima/dochtml/ft/82652/FT_82652.html),
  section 2: glucose 50 mg/mL, potassium chloride 1.50 mg/mL, 20 mmol/L potassium;
  both 500 and 1000 mL containers. For monovalent potassium, mmol and mEq agree.
- [Viaflo 0.15% SmPC](https://cima.aemps.es/cima/dochtml/ft/65421/FT_65421.html):
  glucose (as monohydrate) 50 g/L and potassium chloride 1.5 g/L, labeled 20 mmol/L.
- [Grifols 0.02 mEq/mL SmPC](https://cima.aemps.es/cima/dochtml/ft/60785/FT_60785.html):
  glucose 50 g/L and potassium chloride 1.49 g/L, labeled 20 mmol/L.
  In particular, source row 704616 incorrectly reports glucose 20 mg; use the
  verified 5% glucose clinical strength instead.
- [Grifols 0.04 mEq/mL SmPC](https://cima.aemps.es/cima/dochtml/ft/60787/FT_60787.html):
  glucose 50 g/L and potassium chloride 3 g/L, labeled 40 mmol/L.
- [B. Braun 0.02 mEq/mL SmPC](https://cima.aemps.es/cima/dochtml/ft/76104/FT_76104.html):
  explicitly distinguishes glucose 50 g/L from glucose monohydrate 55 g/L.
  Do not convert the labeled glucose 50 mg/mL down to 45.46 mg/mL merely because
  the ingredient field mentions monohydrate.
- [Altan combined SmPC](https://cima.aemps.es/cima/dochtml/ft/68925/FichaTecnica_68925.html):
  explicitly labels glucose 50 mg/mL and KCl 1.5 or 3 mg/mL, corresponding to
  10 or 20 mEq per 500 mL; packs contain one or twenty 500 mL bags. Its tables
  inconsistently call the 25 g glucose content monohydrate. Follow the explicit
  labeled clinical strength, recording this discrepancy in the mapping comments.

The 1.49/1.50 mg/mL and 2.98/3 mg/mL differences reflect rounding of the same
nominal 0.02/0.04 mEq/mL clinical strengths, not different strengths. Source
ingredient entries such as KCl 0.02 mg or 0.04 mg are unit errors; the product
name, clinical presentation, and SmPC supply the defensible strength.
Container volume is taken from the clinical presentation, not the pack count.
