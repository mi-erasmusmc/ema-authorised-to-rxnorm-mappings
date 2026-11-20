# Xelevia mapping sources

Reviewed 2026-11-20 for EMEA/H/C/000762. Use the unbranded standard RxNorm phosphate oral tablet concepts as `EXACT` for all 24 presentations.

| Labeled strength | RxNorm concept name | RxCUI | OMOP concept ID |
| --- | --- | --- | --- |
| 25 mg | sitagliptin phosphate 25 MG Oral Tablet | 2709612 | 1465918 |
| 50 mg | sitagliptin phosphate 50 MG Oral Tablet | 2709608 | 1465915 |
| 100 mg | sitagliptin phosphate 100 MG Oral Tablet | 2709603 | 1465913 |

- Section 2 of the Xelevia SmPC specifies sitagliptin phosphate monohydrate in all three strengths, with the labeled milligrams expressed as sitagliptin equivalents. [EMA Xelevia product information](https://www.ema.europa.eu/en/documents/product-information/xelevia-epar-product-information_en.pdf#page=2)
- DailyMed lists the three unbranded phosphate concepts for Januvia, which contains the same salt. RxNorm records sitagliptin as the basis of strength for RxCUI `2709603`, so the 100 mg label maps directly to the 100 MG phosphate concept. [DailyMed Januvia label and RxNorm codes](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=f85a48d0-0407-4c50-b0fa-7673a160bf01) · [NLM RxNorm concept details](https://rxnav.nlm.nih.gov/REST/rxcui/2709603/historystatus.json)
- DailyMed lists `sitagliptin 100 MG Oral Tablet` (RxCUI `665033`) for Zituvio. Section 11 of the Zituvio label specifies sitagliptin free base. The phosphate concept captures the salt present in Xelevia. [DailyMed Zituvio label and RxNorm codes](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=b2da9d77-154b-48f7-8793-3f4a24dfafc6)
