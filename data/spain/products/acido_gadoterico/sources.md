# Gadoteric acid prefilled syringe mapping rationale

Reviewed 2026-11-06 using Hecate standard RxNorm and RxNorm Extension searches.
Standard searches did not return matching volume-specific prefilled syringes.
Extension provides clean 0.5 mmol/mL concepts at all three required volumes:

| Volume | Unbranded concept ID / code | Dotarem concept ID / code |
| --- | --- | --- |
| 10 mL | 21166676 / OMOP311901 | 21088044 / OMOP311904 |
| 15 mL | 21078333 / OMOP313214 | 21147005 / OMOP313216 |
| 20 mL | 21176569 / OMOP314396 | 21068633 / OMOP314398 |

Use the branded mmol/mL concepts for the six Dotarem syringe rows and unbranded
mmol/mL concepts for the three Clariscan syringe rows. These capture ingredient,
concentration, device, and volume and are EXACT. The existing vial/bottle mappings
are unchanged by this syringe-focused update.

The [Dotarem SmPC](https://cima.aemps.es/cima/dochtml/ft/67489/FT_67489.html)
confirms 0.5 mmol/mL gadoterate meglumine containing 279.32 mg/mL gadoteric acid,
and describes the 10, 15, and 20 mL prefilled syringes. The
[combined Clariscan SmPC](https://cima.aemps.es/cima/dochtml/ft/81884/FT_81884.html)
also confirms 0.5 mmol/mL gadoteric acid as gadoterate meglumine and the prefilled
syringe presentation.

Do not confuse gadoteric-acid mass with meglumine-salt mass. Retaining the exact
labeled molar concentration avoids ambiguities in Extension's 279/280 and 377
mg/mL concepts. The 10 mL branded Clariscan search result spells its brand
"CLARISCA"; clean unbranded mmol/mL syringe concepts avoid that defect and keep
the three Clariscan mappings consistent. Supplier-specific and box concepts were
excluded, as were erroneous results naming gadoteridol with the Dotarem brand.
