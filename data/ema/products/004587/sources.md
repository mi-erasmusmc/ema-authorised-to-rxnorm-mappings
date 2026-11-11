# Nuceiva mapping evidence

Reviewed 2026-11-11. All four existing mapping rows were verified and retained.

- [EMA product information](https://www.ema.europa.eu/en/documents/product-information/nuceiva-epar-product-information_en.pdf), section 2, confirms separate 50-unit and 100-unit vials of botulinum toxin type A.
- [New Zealand Medsafe product details](https://www.medsafe.govt.nz/DbSearch/ProductDetail?Product_id=21862) identifies Nuceiva 100 Units as prabotulinumtoxinA (USAN).
- [FDA Jeuveau label](https://www.accessdata.fda.gov/drugsatfda_docs/label/2019/761085s001lbl.pdf), section 11, identifies the US ingredient as prabotulinumtoxinA-xvfs and describes the 100-unit single-dose powder vial. Toxin potency units cannot be converted to units of other botulinum toxin products.

Standard RxNorm and RxNorm Extension searches found unbranded prabotulinumtoxinA-xvfs 100 UNT Injection (1366470; RxCUI 2117871), which preserves the 100-unit presentation without introducing the different US brand Jeuveau. No 50-unit prabotulinumtoxinA concept was found. The three 50-unit presentations remain BROAD to botulinum toxin type A Injection (35605867; RxCUI 1732153), with suggestions specifying the correct ingredient, strength and Nuceiva brand. Other toxin subtypes and 100-unit vial concepts are unsuitable for those rows.

Validation reports only the existing NO_DATE issue because the source is named parsed_data.tsv. Its parsing date is not documented, so the source filename was retained.

## Strength-free precise-ingredient concept check

A follow-up RxNav check on 2026-11-11 confirmed that RxCUI 2648814, prabotulinumtoxinA-xvfs Injection, exists with term type SCDFP. It would be a clinically more specific BROAD target for the 50-unit vials if available as an OMOP standard concept. However, Hecate standard searches and the general search including nonstandard concepts did not return this concept. The precise ingredient itself (1366468; RxCUI 2117869) is nonstandard in the available OMOP vocabulary. Therefore the existing standard concept 35605867 is retained pending availability of a standard precise-ingredient/form target.

[RxNav related concepts for prabotulinumtoxinA-xvfs](https://rxnav.nlm.nih.gov/REST/rxcui/2117869/related.json?tty=SCDFP+SCDF) exposes both the precise-ingredient form and the broader botulinum toxin type A Injection form. The earlier searches were limited to standard concepts and did not establish that the precise-ingredient form was absent from RxNorm itself.
