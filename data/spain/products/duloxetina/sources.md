# Duloxetine gastro-resistant tablets and capsules

Reviewed 2026-11-06.

## Product evidence

- [AEMPS Oxitril 30/60 mg SmPC](https://cima.aemps.es/cima/dochtml/ft/82579/FT_82579.html), sections 2, 3 and 6.1: identifies gastro-resistant tablets, describes their tablet shape and lists a tablet core and gastro-resistant coating. These are genuine tablets, not capsule presentations mislabeled in the nomenclator.
- [AEMPS Dulotex 30/60 mg SmPC](https://cima.aemps.es/cima/dochtml/ft/82593/FT_82593.html), sections 2 and 3: identifies gastro-resistant tablets containing 30 or 60 mg duloxetine, with tablet descriptions.
- [DailyMed Cymbalta label](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=2f7d4d67-10c1-4bf4-a7f2-c185fbad64ba), description: delayed-release capsules contain enteric-coated pellets, with strengths expressed as duloxetine base.

## Terminology evidence

- [NLM RxNorm overview](https://www.nlm.nih.gov/research/umls/rxnorm/overview.html): a clinical drug is represented by ingredient, strength and dose form.
- [NLM dose-form definitions](https://www.nlm.nih.gov/research/umls/rxnorm/docs/appendix2.html): delayed-release tablet and capsule forms are distinct; enteric coating belongs to delayed release. Extended release describes prolonged controlled release, rather than simply delayed onset.
- [NLM dose-form groups](https://www.nlm.nih.gov/research/umls/rxnorm/docs/appendix3.html): tablets and capsules can both belong to the broader Pill group. Membership in that group does not make their clinical-drug dose forms identical.

## Mapping decision

Searches through the find-concepts skill found standard RxNorm delayed-release capsule concepts for 30 and 60 mg, but no matching delayed-release tablet concepts in RxNorm or RxNorm Extension. Search absence is a vocabulary coverage finding, not proof that such a concept can never exist.

The existing Extension concepts named Extended Release Oral Tablet do not match the release mechanism documented for these products. Do not treat those names as synonyms for Delayed Release Oral Tablet without further vocabulary provenance evidence.

Retain BROAD mappings for the 20 tablet presentations to the matching-strength, unbranded delayed-release capsule concepts, with suggestions for duloxetine 30/60 MG Delayed Release Oral Tablet. This is an approximate mapping that retains strength and release mechanism while explicitly accepting a tablet/capsule mismatch; the target capsule is not a formal parent of the source tablet.

This decision does not establish a clinically meaningful efficacy difference or clinical interchangeability between the products. Even evidence of bioequivalence would not, by itself, make their RxNorm dose forms identical. EXACT here requires a matching presentation under the repository's mapping rules.
