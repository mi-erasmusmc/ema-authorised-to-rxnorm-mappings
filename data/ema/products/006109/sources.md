# Anzupgo mapping evidence

Reviewed 2026-11-11 following a check of the apparent MG/G versus MG/ML discrepancy.

- [EMA product information](https://www.ema.europa.eu/en/documents/product-information/anzupgo-epar-product-information_en.pdf), section 2: each gram contains 20 mg delgocitinib, matching local parsed_data_2026-03-31.tsv.
- [FDA prescribing information, June 2026](https://www.accessdata.fda.gov/drugsatfda_docs/label/2026/219155s004lbl.pdf), sections 3 and 11: the US cream is also 2%, containing 20 mg delgocitinib per gram.
- [DailyMed product label and RxNorm table](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=a59bf36e-6f04-4b47-b385-8040c95f040c): the structured ingredient table states 20 mg in 1 g. The RxNorm table explicitly links this product to RxCUI 2721172, with SBD name `delgocitinib 20 MG/ML Topical Cream [Anzupgo]` and prescribable synonym `Anzupgo 2 % Topical Cream`.
- [RxNav all properties for 2721172](https://rxnav.nlm.nih.gov/REST/rxcui/2721172/allProperties.json?prop=all) independently confirms the 2% synonym, FDA application NDA219155, and the same SPL set ID.

These product-specific links establish that the standard RxNorm concept represents the same labeled 20 mg/g (2%) Anzupgo cream. The MG/ML spelling is its normalized terminology representation, not evidence of a different American strength. No physical density conversion is asserted. The prior decision to reject standard RxNorm solely because its normalized denominator differed was incorrect.

All three presentations map EXACT to standard OMOP concept 37353891 (RxCUI 2721172). Extension concept 859007 is unnecessary once the standard concept identity is verified. Tube sizes and the multipack do not alter this clinical drug mapping. flag.tsv records the correction to the earlier review.
