# Xeplion mapping sources

Reviewed 2026-11-20 for EMEA/H/C/002105. All six authorized presentations map as `EXACT`.

## Individual prefilled syringes

Section 2 of the Xeplion SmPC gives the labeled dose as paliperidone equivalent and specifies the corresponding mass of paliperidone palmitate and fill volume. Standard RxNorm expresses these same syringes as 156 MG/ML paliperidone palmitate at the corresponding fill volumes. DailyMed lists the unbranded concepts under the US product Invega Sustenna. [EMA Xeplion product information](https://www.ema.europa.eu/en/documents/product-information/xeplion-epar-product-information_en.pdf) · [DailyMed Invega Sustenna label and RxNorm codes](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=1af14e42-951d-414d-8564-5d5fce138554)

| Authorization | Paliperidone equivalent | Paliperidone palmitate | Fill volume | RxCUI | OMOP concept ID |
| --- | --- | --- | --- | --- | --- |
| EU/1/11/672/001 | 25 mg | 39 mg | 0.25 mL | 858073 | 40163942 |
| EU/1/11/672/002 | 50 mg | 78 mg | 0.5 mL | 858048 | 40163973 |
| EU/1/11/672/003 | 75 mg | 117 mg | 0.75 mL | 858056 | 40163988 |
| EU/1/11/672/004 | 100 mg | 156 mg | 1 mL | 858054 | 40163884 |
| EU/1/11/672/005 | 150 mg | 234 mg | 1.5 mL | 858052 | 40163887 |

## Treatment initiation pack

EU/1/11/672/006 contains one 150 mg syringe (1.5 mL) and one 100 mg syringe (1 mL), both expressed as paliperidone equivalents. The two syringes contain 234 mg and 156 mg of paliperidone palmitate, respectively. [EMA Xeplion product information, treatment initiation pack labeling](https://www.ema.europa.eu/en/documents/product-information/xeplion-epar-product-information_en.pdf#page=61)

Hecate returned the standard RxNorm concentration-level concept `1359483`, which omits both syringe volumes and the two-syringe composition. RxNorm Extension provides an `EXACT` branded clinical pack that specifies both volumes, one prefilled syringe of each, and the Xeplion brand. The pack uses the EMA strength basis of 100 MG/ML paliperidone equivalent. [RxNorm Extension concept in OHDSI Athena](https://athena.ohdsi.org/search-terms/terms/36897880)

| RxNorm Extension concept name | Concept code | OMOP concept ID |
| --- | --- | --- |
| `{1 (1.5 ML paliperidone 100 MG/ML Prefilled Syringe) / 1 (1 ML paliperidone 100 MG/ML Prefilled Syringe) } Pack [Xeplion]` | OMOP1006884 | 36897880 |
