# Tolvaptan Accord mapping evidence

Reviewed 2026-11-11.

[EMA product information](https://www.ema.europa.eu/en/documents/product-information/tolvaptan-accord-epar-product-information_en.pdf), sections 1, 2 and 4.1, confirms 7.5, 15 and 30 mg tablets and the indication of adult hyponatremia secondary to SIADH.

[NLM RxNorm August 2025 release notes](https://www.nlm.nih.gov/research/umls/rxnorm/docs/2025/rxnorm_releasenotes_full_08042025.html) introduce the Hyponatremia qualitative distinction to distinguish the 15 and 30 mg generic tablets corresponding to Samsca from the unqualified Jynarque-associated tablet concepts. The appropriate standard concepts are 19036799 (RxCUI 849827), Hyponatremia tolvaptan 15 MG Oral Tablet, and 19036832 (RxCUI 849833), Hyponatremia tolvaptan 30 MG Oral Tablet. Eight mappings were corrected accordingly.

Standard RxNorm searches did not return a 7.5 mg tablet. Extension searches confirmed the existing unbranded tolvaptan 7.5 MG Oral Tablet, concept 35145367 (OMOP4802458). This strength does not have the overlapping standard 15/30 mg concepts to disambiguate; no Hyponatremia-qualified 7.5 mg concept was found. All four 7.5 mg rows are retained as EXACT. The Samsca brand is not used for Accord products.

All 12 source authorisation numbers were checked individually against their actual strengths. Validation reports only the existing NO_DATE issue: parsed_data.tsv has no date suffix and the original parsing date is undocumented.
