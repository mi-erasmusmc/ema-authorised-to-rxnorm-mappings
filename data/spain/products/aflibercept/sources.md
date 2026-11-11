# Mapping sources

Checked 2026-11-09.

- [CIMA Opuviz prefilled syringe SmPC](https://cima.aemps.es/cima/dochtml/ft/1241865003/FT_1241865003.html), sections 2/4.2/6.6: extractable fill is at least 0.1 mL but the administered dose is 2 mg in 0.05 mL. [Vial SmPC](https://cima.aemps.es/cima/dochtml/ft/1241865002/FT_1241865002.html) likewise specifies adjustment to 0.05 mL.
- [CIMA Baiama prefilled syringe SmPC](https://cima.aemps.es/cima/dochtml/ft/1241887002/FT_1241887002.html), section 4.2: 0.09 mL extractable volume includes excess removed before delivery of 0.05 mL (2 mg).
- [CIMA Eydenzelt prefilled syringe leaflet](https://cima.aemps.es/cima/dochtml/p/1241895001/P_1241895001.html) identifies 0.182 mL container fill. [Vial leaflet](https://cima.aemps.es/cima/dochtml/p/1241895002/P_1241895002.html) identifies the 0.05 mL administered dose; the mapping therefore uses dose volume, rather than excess fill volume.
- Reviewed again 2026-11-11: FDA suffix choices and evidence are recorded in `.claude/skills/map-drugs/biosimilars/aflibercept.sources.md`. Baiama is FYB203, the same biosimilar as Ahzantive (aflibercept-mrbb). Its syringe remains BROAD to the mrbb Injection because no matching syringe concept was found. Opuviz syringe likewise remains BROAD to the matching branded yszy Injection. Matching branded standard Eydenzelt and Opuviz concepts are preferred.
- [EMA Eylea SmPC](https://www.ema.europa.eu/en/documents/product-information/eylea-epar-product-information_en.pdf), section 2: the high-dose syringe contains 0.184 mL but delivers 8 mg in 0.07 mL. The old fill-volume Extension Injection was not an exact syringe match; use the standard delivered-dose Injection as BROAD with a syringe suggestion.
- Mynzepli and Eiyzey use the 0.05 mL delivered dose, with BROAD plain-aflibercept mappings and biosimilar-specific suggestions. Ahzantive syringe uses the matching mrbb dose as BROAD; Afqlir remains BROAD because abzv is absent from the searched vocabulary.
