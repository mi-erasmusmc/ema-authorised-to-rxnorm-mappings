# Diphtheria, tetanus and acellular pertussis vaccine review

Reviewed 2026-11-11 against product labels and Hecate searches of standard RxNorm and RxNorm Extension.

The source TSV omits antigen quantities. All six presentations contain a 0.5 ml dose, but they are not one interchangeable formulation. Replace the previous strength-free concepts with standard RxNorm concepts containing the individual antigen concentrations and the correct single-dose presentation.

## Labelled composition per 0.5 ml

| Product | Diphtheria / tetanus content (Lf) | Pertussis toxin / FHA / pertactin / fimbriae 2+3 (micrograms) | Selected concept |
|---|---|---|---|
| Boostrix | 2.5 / 5 | 8 / 8 / 2.5 / absent | 42800267, RxCUI 1300370, Prefilled Syringe [Boostrix] |
| Infanrix | 25 / 10 | 25 / 25 / 8 / absent | 42800271, RxCUI 1300384, Prefilled Syringe [Infanrix] |
| Triaxis, syringe | 2 / 5 | 2.5 / 5 / 3 / 5 | 42800264, RxCUI 1300189, unbranded Prefilled Syringe |
| Triaxis, vial | 2 / 5 | 2.5 / 5 / 3 / 5 | 42800463, RxCUI 1300205, unbranded Injection |

All are EXACT. Concentrations in the selected concepts are the per-dose contents divided by 0.5 ml, with micrograms converted to mg.

## Units and formulation

European minimum toxoid potency in IU and antigen content in Lf describe different measurements; there is no general numerical conversion between them. The standard RxNorm concepts express the Lf-based content with UNT. Confirm each formulation from its own label rather than comparing the EU minimum IU values directly to those RxNorm numbers.

- [AEMPS Boostrix SmPC](https://cima.aemps.es/cima/dochtml/ft/63684/FT_63684.html) explicitly supplies both IU potency and Lf content. The source syringe presentations match the strength-specific branded standard concept.
- [AEMPS Infanrix SmPC](https://cima.aemps.es/cima/pdfs/es/ft/61871/FT_61871.html.pdf) supplies the EU minimum potency and individual pertussis antigen quantities. It confirms a suspension, despite the source TSV's solution wording. [Australian government Infanrix product information](https://www.safetyandquality.gov.au/medicine-finder/infanrix) supplies both IU and Lf for the same named vaccine. The [US Infanrix label](https://dailymed.nlm.nih.gov/dailymed/fda/fdaDrugXsl.cfm?setid=de16dd6a-859b-4180-c6af-f930be14f26a&type=display) confirms the Lf-based composition represented by the standard RxNorm concept.
- [AEMPS Triaxis syringe SmPC](https://cima.aemps.es/cima/dochtml/ft/81067/FT_81067.html) and [vial SmPC](https://cima.aemps.es/cima/pdfs/es/ft/71870/FT_71870.pdf) explicitly provide both Lf and minimum IU potency, all four pertussis components, and the presentation. Standard unbranded RxNorm captures the full clinical formulation. The former branded Extension syringe concept omitted antigen strengths; the standard dose-specific concept adds clinically relevant detail. Do not choose an Adacel-branded concept for Triaxis, or an Extension concept solely to retain the Triaxis brand. Do not substitute a multidose Injectable Suspension concept for the single-dose vial.

No polio, hepatitis B or Hib antigens are present in these products. Do not select similarly named combination vaccines containing those additional antigens.
