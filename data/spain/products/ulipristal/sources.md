# Ulipristal mapping review

Reviewed 2026-11-09.

- [EMA: ellaOne](https://www.ema.europa.eu/en/medicines/human/EPAR/ellaone) and [product information](https://www.ema.europa.eu/en/documents/product-information/ellaone-epar-product-information_en.pdf): the European product is ellaOne, containing 30 mg ulipristal acetate per tablet.
- [FDA: ella prescribing information](https://www.accessdata.fda.gov/drugsatfda_docs/label/2015/022474s007lbl.pdf): the US product is named ella and contains 30 mg ulipristal acetate per tablet.

Hecate searches found standard RxNorm `ulipristal acetate 30 MG Oral Tablet` (40224655; 1005924) and `ulipristal acetate 5 MG Oral Tablet` (45775367; 1546350). These preserve the labeled ingredient, strength and dose form, so both are EXACT matches.

RxNorm Extension separately represents `ulipristal 30 MG Oral Tablet [EllaOne]` (21129355; OMOP295987) and `ulipristal 5 MG Oral Tablet [Esmya]` (21159000; OMOP296073). Neither adds a clinically relevant dose-form or presentation detail missing from standard RxNorm. Retain the standard unbranded concepts under the standard-over-Extension rule. Do not substitute the US `[Ella]` brand for the separately represented European ellaOne brand.
