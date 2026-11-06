# Tocilizumab mapping evidence

Reviewed 2026-11-06.

## Biosimilar identity

- [FDA biosimilar product information](https://www.fda.gov/drugs/biosimilars/biosimilar-product-information) identifies Tyenne as tocilizumab-aazg and Tofidence as tocilizumab-bavi.
- [FDA Avtozma label](https://www.accessdata.fda.gov/drugsatfda_docs/label/2025/761420s000lbl.pdf) identifies Avtozma as tocilizumab-anoh, including its 162 mg/0.9 mL subcutaneous presentation.
- [EMA Tosmova EPAR](https://www.ema.europa.eu/en/medicines/human/EPAR/tocilizumab-stada) explicitly identifies Tosmova as previously Tocilizumab STADA and Tofidence. The shared biosimilar reference now uses current EU name Tosmova for US Tofidence/tocilizumab-bavi; the former names remain documented here.

Biosimilar mappings use unbranded FDA-suffixed concepts even when matching branded concepts exist. Avtozma syringe 768851 incorrectly used Tyenne's aazg suffix; it now uses anoh, consistent with its brand and other Avtozma presentations.

## Presentation checks

[EMA Avtozma product information](https://www.ema.europa.eu/en/documents/product-information/avtozma-epar-product-information_en.pdf) describes single-use 162 mg/0.9 mL syringes and pens. The concentration is 180 mg/mL; the missing four-pen pack uses the same volume-specific Auto-Injector concept as existing Avtozma pen rows. Pack count does not change the concept.

Existing vial mappings distinguish 4, 10 and 20 mL at 20 mg/mL, preserving the corresponding single-use presentation and biosimilar suffix. Shared nro_definitivo values do not justify collapsing those volumes. Existing RoActemra/Actemra originator mappings were retained.

For 767313, unidad_contenido incorrectly says pen while the product name, clinical description, dose-form field and container all identify a syringe; the existing syringe concept was retained with a clarifying comment.

## Selected Avtozma concepts

- Prefilled syringe: OMOP 1466418 / RxCUI 2705425, `0.9 ML tocilizumab-anoh 180 MG/ML Prefilled Syringe`.
- Pen: OMOP 1466420 / RxCUI 2705435, `0.9 ML tocilizumab-anoh 180 MG/ML Auto-Injector`.

Both are standard RxNorm EXACT matches. Extension fallback was unnecessary.
