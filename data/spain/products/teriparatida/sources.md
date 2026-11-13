# Teriparatide presentation evidence

Reviewed 2026-11-13.

## Cartridges and biosimilar identity

[EMA Movymia product information](https://www.ema.europa.eu/en/documents/product-information/movymia-epar-product-information_en.pdf) and [EMA Terrosa product information](https://www.ema.europa.eu/en/documents/product-information/terrosa-epar-product-information_en.pdf) distinguish 2.4 ML cartridges for reusable pens from disposable prefilled pens. Cartridges contain 250 micrograms/ML and provide 28 doses of 20 micrograms. The cartridge-plus-pen starter packs retain the cartridge drug presentation.

Standard RxNorm searches by brand, ingredient, strength and form did not establish corresponding FDA-suffixed ingredients for Movymia, Terrosa, Livogiva, Sondelbay or Kauliv. These products remain BROAD with product-specific `-xxxx` suggestions. Extension is needed for the cartridge dose form: use `2.4 ML teriparatide 0.25 MG/ML Cartridge`, and the matching Terrosa Extension concept where available. No suitable volume-specific 3 ML Kauliv cartridge concept was found; its existing concentration-level Cartridge mapping remains BROAD.

[EMA Kauliv product information](https://www.ema.europa.eu/en/documents/product-information/kauliv-epar-product-information_en.pdf) confirms 3 ML cartridges containing 750 micrograms at 250 micrograms/ML. [CIMA Kauliv leaflet](https://cima.aemps.es/cima/dochtml/p/1221710003/P_1221710003.html) specifies 28 doses. Do not infer extra doses from reservoir fill volume.

## Deliverable doses in pens

Use standard RxNorm `28 ACTUAT teriparatide 0.02 MG/ACTUAT Pen Injector` for the 28-dose pens. This preserves the labeled delivered dose count without treating reservoir overfill as additional doses. Keep non-biosimilar Tetridar, Duratil, Teriparatida SUN and Forsteo EXACT; biosimilars remain BROAD for identity.

- [CIMA Tetridar SmPC](https://cima.aemps.es/cima/dochtml/ft/82563/FT_82563.html): 28 doses of 20 micrograms per pen.
- [CIMA Duratil SmPC](https://cima.aemps.es/cima/dochtml/ft/85653/FT_85653.html): 28 doses of 20 micrograms per pen.
- [EMA Teriparatide SUN product information](https://www.ema.europa.eu/en/documents/product-information/teriparatide-sun-epar-product-information_en.pdf): 28 doses in a disposable prefilled pen.
- [EMA Forsteo product information](https://www.ema.europa.eu/en/documents/product-information/forsteo-epar-product-information_en.pdf): 28 doses per pen.
- [CIMA Terrosa prefilled pen leaflet](https://cima.aemps.es/cima/dochtml/p/1161159004/Prospecto.html): 28 fixed doses per disposable pen; this applies equally to the parallel-import presentation.
- [EMA Livogiva product information](https://www.ema.europa.eu/en/documents/product-information/livogiva-epar-product-information_en.pdf): 2.7 ML reservoir, sufficient for 28 doses. The source `des_dcp` says 2.4 ML; the 28-actuation concept avoids propagating that discrepancy. Source data is retained as supplied.

The existing Sondelbay 28-actuation BROAD mapping is retained. Brand-only Extension concepts do not replace clinically adequate standard RxNorm pen concepts.
