# Mapping sources

Checked 2026-11-09.

- [CIMA Opuviz prefilled syringe SmPC](https://cima.aemps.es/cima/dochtml/ft/1241865003/FT_1241865003.html), sections 2/4.2/6.6: extractable fill is at least 0.1 mL but the administered dose is 2 mg in 0.05 mL. [Vial SmPC](https://cima.aemps.es/cima/dochtml/ft/1241865002/FT_1241865002.html) likewise specifies adjustment to 0.05 mL.
- [CIMA Baiama prefilled syringe SmPC](https://cima.aemps.es/cima/dochtml/ft/1241887002/FT_1241887002.html), section 4.2: 0.09 mL extractable volume includes excess removed before delivery of 0.05 mL (2 mg).
- [CIMA Eydenzelt prefilled syringe leaflet](https://cima.aemps.es/cima/dochtml/p/1241895001/P_1241895001.html) identifies 0.182 mL container fill. [Vial leaflet](https://cima.aemps.es/cima/dochtml/p/1241895002/P_1241895002.html) identifies the 0.05 mL administered dose; the mapping therefore uses dose volume, rather than excess fill volume.
- FDA suffix choices follow `.claude/skills/map-drugs/biosimilars/aflibercept.tsv`: Eydenzelt = aflibercept-boav, Opuviz = aflibercept-yszy. Baiama lacks a documented FDA counterpart and remains BROAD to unsuffixed aflibercept. Opuviz prefilled syringe remains BROAD because the suffix-and-dose-specific RxNorm result is an Injection, rather than a Prefilled Syringe.
