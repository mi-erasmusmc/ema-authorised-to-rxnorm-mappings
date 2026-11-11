# BiResp Spiromax mapping evidence

[EMA product information](https://www.ema.europa.eu/en/documents/product-information/biresp-spiromax-epar-product-information_en.pdf), reviewed 2026-11-11. Section 2 confirms that the lower-strength delivered dose of 160/4.5 micrograms is equivalent to the metered dose of 200/6 micrograms. The parsed EMA presentations specify 120 doses per lower-strength inhaler and 60 doses per higher-strength inhaler.

Standard RxNorm searches returned liquid Metered Dose Inhaler combination concepts, which do not match the powder form. Extension search found unbranded 120-actuation concept 35421281 (OMOP1154866) matching the labelled 0.16/0.0045 MG/ACTUAT dry powder presentation. The three lower-strength rows were updated to this concept. No matching BiResp-branded concept was found; DuoResp and Symbicort branded results were excluded.

The three existing higher-strength rows already match the labelled 0.32/0.009 MG/ACTUAT and 60-actuation dry powder inhaler via concept 35421264 (OMOP1154849) and were retained. All six mappings are EXACT.
