
## Mapping review 2026-11-09

Source: https://www.ema.europa.eu/es/documents/product-information/wegovy-epar-product-information_es.pdf

Wegovy 7.2 mg is a single-dose 0.75 mL pen (9.6 mg/mL), contrary to the source multidose unit label. Mapped to the single-use Auto-Injector concept.

## Mapping review 2026-11-13

Reviewed all 31 rows against current Hecate RxNorm/RxNorm Extension searches. Corrected five rows; existing oral mappings, matching pen mappings, and the four BROAD higher-strength FlexTouch mappings were retained.

- [Wegovy EMA product information](https://www.ema.europa.eu/en/documents/product-information/wegovy-epar-product-information_en.pdf), section 2; also [AEMPS SmPC](https://cima.aemps.es/cima/dochtml/ft/1211608006/FT_1211608006.html): the 0.25 mg FlexTouch pen contains four doses, totaling 1 mg in 1.5 mL. Extension concept 36508201 represents this total and volume as 0.667 MG/ML (1/1.5), whereas the SmPC states the rounded concentration as 0.68 mg/mL. Use this volume-specific Pen Injector EXACT for 758085 and 767122 instead of the prior 3 mL concept. No suitable standard 1.5 mL pen or clean matching branded Extension pen was found.
- The same Wegovy SmPC distinguishes 0.5 mg FlexTouch in 1.5 mL (1.34 mg/mL) from 0.5 mg FlexTouch in 3 mL (0.68 mg/mL). For 767530, use the unbranded standard 3 mL 0.68 MG/ML pen concept, rather than the 1.5 mL concept inherited through the shared registration number. Standard RxNorm already captures the presentation; Extension is not needed for brand alone.
- [Ozempic EMA product information](https://www.ema.europa.eu/en/documents/product-information/ozempic-epar-product-information_en.pdf), sections 2 and 6.5 and eight-dose pen labelling: the eight-dose 0.5 mg pen contains 4 mg in 3 mL at 1.34 mg/mL; the eight-dose 1 mg pen contains 8 mg in 3 mL at 2.68 mg/mL. Correct 767868 and 767870 respectively to these branded standard 3 mL concepts, overriding mappings inherited through shared registration numbers.
- [CIMA API, 767868](https://cima.aemps.es/cima/rest/medicamento?cn=767868) identifies the 3 mL presentation and lists semaglutide at 1.34 mg. Combined with the local eight-dose count and EMA composition, this supports overriding the local des_dcp value of 0.74 mL per 0.5 mg dose, which instead describes the four-dose 0.68 mg/mL pen. The eight-dose pen delivers each 0.5 mg dose in 0.37 mL. [CIMA API, 767870](https://cima.aemps.es/cima/rest/medicamento?cn=767870) confirms the 3 mL presentation with eight needles.
- For Wegovy 1.7 and 2.4 mg FlexTouch, standard searches return single-use Auto-Injectors rather than the multidose pen. Extension searches did not find matching Pen Injectors. Keep the existing clean branded 3 mL Injectable Solution Extension concepts BROAD: they preserve concentration and total content but omit the pen device. Suggestions retain the complete FlexTouch presentation.
- Rybelsus tablets (3/7/14 mg and 1.5/4/9 mg) and Wegovy tablets (1.5/4/9/25 mg) retain their matching branded standard Oral Tablet concepts. Keep the source-labelled strength for each formulation; do not convert between oral formulation strengths.
