# Burosumab presentation evidence

Reviewed 2026-11-06.

The [EMA Crysvita product information](https://www.ema.europa.eu/en/documents/product-information/crysvita-epar-product-information_en.pdf), section 2, distinguishes:

| Presentation | Amount | Volume |
|---|---:|---:|
| Vial | 10 mg | 1 mL |
| Vial | 20 mg | 1 mL |
| Vial | 30 mg | 1 mL |
| Prefilled syringe | 10 mg | 0.33 mL |
| Prefilled syringe | 20 mg | 0.67 mL |
| Prefilled syringe | 30 mg | 1 mL |

Section 6.6 and the packaging text identify both containers as single use. The syringes are subcutaneous injections; the Spanish structured form field describing infusion conflicts with the product name, clinical presentation and route.

Standard RxNorm provides matching branded 1 mL Injection concepts for all three vials. Preserve these EXACT mappings, including the US ingredient name burosumab-twza.

Searches in standard RxNorm and RxNorm Extension, using burosumab, burosumab-twza, Crysvita, syringe strengths and volumes, found no matching Prefilled Syringe concepts. Extension returns 0.33 mL and 0.67 mL concepts at nominal 30 mg/mL, but labels them Injectable Solution, whose local RxNorm definition is a multiple-use preparation. Do not treat those as exact syringe matches. The rounded label volumes should not produce artificial concentrations of 30.303 or 29.851 mg/mL.

Map all three syringes BROAD to standard branded Injection concepts with Prefilled Syringe suggestions. For the smaller syringes use the concentration-only 30 mg/mL concept: the 1 mL vial concepts at 10 or 20 mg/mL have different concentrations. For the 30 mg syringe the 1 mL 30 mg/mL Injection concept preserves dose and volume, but the syringe form remains unmatched.

The existing EMA mapping is outside this Spain edit. Its syringe suggestions use Injection, and its 30 mg syringe is marked EXACT to Injection; those rows require a separate form review.
