# Spanish unmapped presentation review — 2026-11-09

Three mapping agents reviewed 430 missing-concept source rows across 234 ingredient folders. The `multicomponente` folder was excluded. Three source rows duplicate identifiers already mapped in alternate ingredient folders; their mappings were aligned with those existing entries.

The regenerated export contains **30,890 mapped and 10 unmapped presentations**, with all 30,900 presentation keys retained. This adds **422 mappings: 359 EXACT and 63 BROAD**. Across the source folders, the 430 reviewed rows comprise 360 EXACT, 65 BROAD and 5 NO_MAPPING decisions. Previously populated mappings were preserved, both in the source folders and the export.

Standard RxNorm searches were followed by RxNorm Extension searches where necessary. BROAD decisions include ideal-concept suggestions. Primary label evidence for source discrepancies, unit conversions and device decisions is recorded in the affected product folders' `sources.md` files.

## Remaining unmapped presentations

| Presentations | Reason |
|---|---|
| Flutenal/flupamesone: 696864, 696898, 758813, 758888 | No suitable concept found in standard RxNorm or Extension; retained NO_MAPPING with suggestions. |
| Boey/trenibotulinumtoxinE: 771395 | No suitable concept found in standard RxNorm or Extension; NO_MAPPING with suggestion and label evidence. |
| 764021, 768050, 769407, 769568, 770875 | In `multicomponente`, excluded from this review. |

## Validation and follow-up

All reviewed rows have a mapping decision and date. Newly added or revised rows pass structural mapping validation. The existing BCG Tice row's EXACT_NO_STRENGTH warning remains unchanged. A semantic comparison confirmed that no previously populated mapping was altered, and the excluded `multicomponente/mapping.tsv` is byte-for-byte unchanged.

`make validate_spain` still reports existing issues elsewhere and INCONSISTENT_CONCEPT flags in the following folders. These arise when the new decision differs from an older mapping sharing the validator's clinical signature. The older rows were retained for separate review; no suppressions were added.

| Folder | Reason for the differing mapping |
|---|---|
| `anastrozol`, `lacosamida` | New Arimidex/Vimpat rows use matching standard branded concepts; older rows use unbranded equivalents. |
| `bromuro_umeclidinio` | New Incruse row uses the concentration-level inhaler concept; older rows specify 30 actuations. |
| `doxilamina_+_piridoxina` | New Cariban row uses a delayed-release capsule; older rows use tablets. |
| `efmoroctocog_alfa` | New rows preserve 1000/2000/3000 UNT strengths; older anchors use 1 UNT. |
| `esomeprazol_+_naproxeno` | New generic uses an unbranded concept; an older generic row uses the originator brand Vimovo. |
| `inmunoglobulina_g_humana` | New Hizentra vial rows use Injection; older rows use Prefilled Syringe. The clinical signature omits container details. |
| `lamotrigina` | New chewable/dispersible presentation uses Chewable Tablet; older anchors use Disintegrating Oral Tablet. |
| `levetiracetam` | New Desitin sachet uses Oral Granules; an older row uses Tablet for Oral Suspension. |
| `memantina`, `mesalazina` | New rows use clinically sufficient standard RxNorm concepts; older rows use branded Extension concepts. |
| `miglustat` | New Waymade generic uses an unbranded concept; other products use different brands. |
| `olanzapina` | New Zyprexa Velotab rows use matching branded disintegrating tablets; older rows use unbranded equivalents. |
| `somatropina` | Norditropin 10 mg/1.5 mL is 6.67 mg/mL despite the source clinical description stating 10 mg/mL. Label evidence is recorded in the folder. |
| `teicoplanina` | New powder presentations use total-dose Injection concepts; older rows use reconstituted-concentration Injectable Solution concepts. |
| `ulipristal` | New EllaOne rows use unbranded concepts; older rows use the US brand Ella. |
