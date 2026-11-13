# Teriparatide presentation evidence

Reviewed 2026-11-13.

## Cartridges and biosimilar identity

[EMA Movymia product information](https://www.ema.europa.eu/en/documents/product-information/movymia-epar-product-information_en.pdf) and [EMA Terrosa product information](https://www.ema.europa.eu/en/documents/product-information/terrosa-epar-product-information_en.pdf) distinguish 2.4 ML cartridges for reusable pens from disposable prefilled pens. Cartridges contain 250 micrograms/ML and provide 28 doses of 20 micrograms. The cartridge-plus-pen starter packs retain the cartridge drug presentation.

Teriparatide is an exception to the FDA-suffix biosimilar mapping rule. The [FDA Bonsity approval letter](https://www.accessdata.fda.gov/drugsatfda_docs/appletter/2019/211939Orig1s000ltr.pdf) identifies plain teriparatide and approval under section 505(b)(2) of the FD&C Act. FDA's [biological-product definition](https://www.fda.gov/about-fda/economic-impact-analyses-fda-regulations/definition-term-biological-product-final-regulatory-impact-analysis) defines proteins as polymers longer than 40 amino acids; [NLM identifies teriparatide as the 1–34 fragment](https://meshb.nlm.nih.gov/record/ui?ui=D019379). The [FDA suffix guidance](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/nonproprietary-naming-biological-products-guidance-industry) concerns biological products licensed under the PHS Act. The EU biosimilar designation alone therefore does not justify a hypothetical `teriparatide-xxxx` identity or a BROAD mapping.

Standard RxNorm searches by brand, ingredient, strength and form returned plain teriparatide, with no matching suffixed ingredient. [RxNav ingredient relations for the 28-dose pen](https://rxnav.nlm.nih.gov/REST/rxcui/1435115/related.json?tty=IN+PIN) identify teriparatide (RxCUI 32915). Use EXACT when ingredient, strength and presentation match. Extension is needed for the cartridge dose form: retain `2.4 ML teriparatide 0.25 MG/ML Cartridge`, and the matching Terrosa Extension concept where available. Kauliv's concentration-level `teriparatide 0.25 MG/ML Cartridge` is also EXACT: its 3 ML multidose reservoir is packaging rather than a single administered dose.

[EMA Kauliv product information](https://www.ema.europa.eu/en/documents/product-information/kauliv-epar-product-information_en.pdf) confirms 3 ML cartridges containing 750 micrograms at 250 micrograms/ML. [CIMA Kauliv leaflet](https://cima.aemps.es/cima/dochtml/p/1221710003/P_1221710003.html) specifies 28 doses. Do not infer extra doses from reservoir fill volume.

## Deliverable doses in pens

Use standard RxNorm `28 ACTUAT teriparatide 0.02 MG/ACTUAT Pen Injector` as EXACT for the 28-dose pens, including the EU biosimilars. This preserves the labeled delivered dose count without treating reservoir overfill as additional doses.

- [CIMA Tetridar SmPC](https://cima.aemps.es/cima/dochtml/ft/82563/FT_82563.html): 28 doses of 20 micrograms per pen.
- [CIMA Duratil SmPC](https://cima.aemps.es/cima/dochtml/ft/85653/FT_85653.html): 28 doses of 20 micrograms per pen.
- [EMA Teriparatide SUN product information](https://www.ema.europa.eu/en/documents/product-information/teriparatide-sun-epar-product-information_en.pdf): 28 doses in a disposable prefilled pen.
- [EMA Forsteo product information](https://www.ema.europa.eu/en/documents/product-information/forsteo-epar-product-information_en.pdf): 28 doses per pen.
- [CIMA Terrosa prefilled pen leaflet](https://cima.aemps.es/cima/dochtml/p/1161159004/Prospecto.html): 28 fixed doses per disposable pen; this applies equally to the parallel-import presentation.
- [EMA Livogiva product information](https://www.ema.europa.eu/en/documents/product-information/livogiva-epar-product-information_en.pdf): 2.7 ML reservoir, sufficient for 28 doses. The source `des_dcp` says 2.4 ML; the 28-actuation concept avoids propagating that discrepancy. Source data is retained as supplied.

Sondelbay also maps EXACT to the 28-actuation concept. Brand-only Extension concepts do not replace clinically adequate standard RxNorm pen concepts.

## DailyMed cartridge wording versus RxNorm dose form

[DailyMed Bonsity](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=2d0c89a2-3849-adf6-007d-aeca21cf417c) and [DailyMed unbranded teriparatide](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=1b007339-dd0d-f019-5e0a-9b1b0f75011c) describe a glass cartridge pre-assembled into a pen. Their RxNorm tables map the finished presentation to RxCUI 1435115, `28 ACTUAT teriparatide 0.02 MG/ACTUAT Pen Injector`; Bonsity additionally maps to branded RxCUI 2716408. Here the cartridge is an internal component of the supplied pen, not a separately replaceable cartridge presentation.

By contrast, Movymia SmPC section 6.6 specifies cartridges for a separate reusable Movymia Pen; the cartridge-only packs do not include the pen. This supports retaining the Cartridge dose form for these presentations. The [RxNav related SCD query for teriparatide](https://rxnav.nlm.nih.gov/REST/rxcui/32915/related.json?tty=SCD), checked 2026-11-13, returned Pen Injector concepts and no Cartridge clinical drug. Standard-concept semantic searches likewise found no teriparatide Cartridge clinical drug. Extension is therefore needed to preserve the separate-cartridge presentation in an EXACT mapping; DailyMed's pen mappings do not establish equivalence of the two supplied forms.
