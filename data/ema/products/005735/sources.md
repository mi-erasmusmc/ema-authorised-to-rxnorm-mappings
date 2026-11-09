Mapping review: 2026-11-06.

- Source: latest local authorised-presentations PDF, parsed TSV, and footnote.txt. Each authorisation number was checked against its own form, dose and content.
- [EMA Comirnaty product information](https://www.ema.europa.eu/en/documents/product-information/comirnaty-epar-product-information_en.pdf): labelled ready-to-use doses are 0.3 mL; the 10 microgram concentrate is 0.05 MG/ML after dilution (0.2 mL dose). Fill volumes 0.48 and 0.418 mL include excess and do not define the administered dose.
- [EMA Spikevax product information](https://www.ema.europa.eu/en/documents/product-information/spikevax-previously-covid-19-vaccine-moderna-epar-product-information_en.pdf): multidose 2.5 mL vials differ from single-dose 0.5 mL vials and prefilled syringes; 50 micrograms/0.5 mL and 25 micrograms/0.25 mL both equal 0.1 MG/ML.
- Hecate standard RxNorm and RxNorm Extension searches: JN.1 and XFG for both brands; KP.2 and LP.8.1 dose tiers, dose-specific single-use concepts and multidose Injectable Suspension forms. No suitable JN.1/XFG-specific concepts or missing strain-specific multidose forms were returned.

Mapping review: 2026-11-09.

- Checked parsed_data_2026-11-09.tsv and the updated footnote.txt: LP.8.1 and XFG doses are 30 or 10 micrograms per 0.3 mL, corresponding to 0.1 or 0.0333 MG/ML. New XFG syringe packs /058 and /059 add needles without changing the clinical presentation.
- Rechecked Hecate standard RxNorm and RxNorm Extension for XFG, LP.8.1 multidose Injectable Suspension, and pediatric 0.0333 MG/ML fallbacks. No XFG-specific concept or matching LP.8.1 multidose form was returned. Existing LP.8.1 exact and broad concepts were confirmed.
- Removed 13 mappings absent from the current authorised-presentations table and recorded them in flag.tsv.
