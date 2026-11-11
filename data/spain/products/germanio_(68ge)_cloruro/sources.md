Reviewed 2026-11-11.

- [National GalliaPharm SmPC](https://cima.aemps.es/cima/dochtml/ft/79102/FT_79102.html), sections 2–4: Ge-68/Ga-68 radionuclide generator, 0.74–1.85 GBq; not for direct administration.
- [Galliad SmPC](https://cima.aemps.es/cima/dochtml/ft/83618/FT_83618.html), sections 2–4: the same parent/daughter radionuclides and generator activity range; not for direct administration.
- [EMA GalliaPharm opinion](https://www.ema.europa.eu/en/documents/smop-initial/chmp-summary-positive-opinion-galliapharm_en.pdf): eight generator activities from 1.11 to 3.70 GBq; Ge-68 generates Ga-68 chloride for in vitro radiolabelling.

Searches of standard RxNorm and Extension for germanium chloride, germanium Ge-68, GalliaPharm and the generator found no suitable isotope-specific generator concept. Retain germanium 19059405 (4784) as BROAD. Suggestions describe the actual generator and both radionuclides; previous Injection suggestions misrepresented the presentation. Activities are total generator activities, not solution concentrations.

The BAD_SUGGESTION suppression is limited to this folder: the validator requires an RxNorm dose form, but Radionuclide Generator has no equivalent in its dose-form lookup. Using Injection to satisfy the validator would be incorrect. The source radiofarmaco=0 on cod_nacion 766225 is inconsistent with its generator identity; mapping is based on the product description and authorised presentation.
