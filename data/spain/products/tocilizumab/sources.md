# Tocilizumab mapping evidence

Reviewed 2026-11-13.

## Biosimilar identity

- [FDA biosimilar product information](https://www.fda.gov/drugs/biosimilars/biosimilar-product-information) identifies Tyenne as tocilizumab-aazg and Tofidence as tocilizumab-bavi.
- [FDA Avtozma label](https://www.accessdata.fda.gov/drugsatfda_docs/label/2025/761420s000lbl.pdf) identifies Avtozma as tocilizumab-anoh, including its 162 mg/0.9 mL subcutaneous presentation.
- [EMA Tosmova EPAR](https://www.ema.europa.eu/en/medicines/human/EPAR/tocilizumab-stada) explicitly identifies Tosmova as previously Tocilizumab STADA and Tofidence. The shared biosimilar reference now uses current EU name Tosmova for US Tofidence/tocilizumab-bavi; the former names remain documented here.

Biosimilar mappings use matching branded FDA-suffixed standard RxNorm concepts for Tyenne and Avtozma. Tosmova uses unbranded tocilizumab-bavi concepts because its EU brand differs from the US Tofidence brand.

## Presentation checks

[EMA Avtozma product information](https://www.ema.europa.eu/en/documents/product-information/avtozma-epar-product-information_en.pdf) describes single-use 162 mg/0.9 mL syringes and pens. The concentration is 180 mg/mL; the missing four-pen pack uses the same volume-specific Auto-Injector concept as existing Avtozma pen rows. Pack count does not change the concept.

Existing vial mappings distinguish 4, 10 and 20 mL at 20 mg/mL, preserving the corresponding single-use presentation and biosimilar suffix. Shared nro_definitivo values do not justify collapsing those volumes. RoActemra uses unbranded standard RxNorm concepts because the EU brand differs from US Actemra. The 4 and 10 mL vial concepts retain the actual single-use volume. [EMA RoActemra EPAR](https://www.ema.europa.eu/en/medicines/human/EPAR/roactemra) confirms the EU product name and tocilizumab ingredient.

For 767313, unidad_contenido incorrectly says pen while the product name, clinical description, dose-form field and container all identify a syringe; the syringe concept is retained.

## Selected Avtozma concepts

- Prefilled syringe: OMOP 1466419 / RxCUI 2705432, `0.9 ML tocilizumab-anoh 180 MG/ML Prefilled Syringe [Avtozma]`.
- Pen: OMOP 1466421 / RxCUI 2705439, `0.9 ML tocilizumab-anoh 180 MG/ML Auto-Injector [Avtozma]`.

Both are standard RxNorm EXACT matches. Extension fallback was unnecessary.
