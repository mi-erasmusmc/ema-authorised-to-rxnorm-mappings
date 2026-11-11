# Acetylcysteine mapping review — 2026-11-11

Reviewed all 65 presentations, grouped into 25 registry patterns. Searched standard RxNorm and RxNorm Extension through `make find_concepts`, including strength, preparation, volume, and matching-brand queries.

## Powder and granules

- Cinfamucol 600 mg (650136), Pensa 600 mg (650156), Cinfa 600 mg (650426), Cuve 600 mg (659208), and Cinfa 100 mg (650429): section 3 specifies powder for oral solution. No matching 100 or 600 mg Powder for Oral Solution concept was found. Retain the strength-matched Granules for Oral Solution concept as BROAD, with a powder suggestion.
  - [Cinfamucol, sections 2–4.2](https://cima.aemps.es/cima/dochtml/ft/66323/FT_66323.html)
  - [Pensa, section 3](https://cima.aemps.es/cima/dochtml/ft/66339/FT_66339.html)
  - [Cinfa 100/200/600 mg, section 3](https://cima.aemps.es/cima/dochtml/ft/66460/FT_66460.html)
  - [Cuve, section 3](https://cima.aemps.es/cima/dochtml/ft/68888/FT_68888.html)
- Farmasierra 600 mg (664110) and Macil 600 mg (774455): section 3 specifies effervescent powder. Retain the strength-matched granules concept as BROAD. The suggestion uses Powder for Oral Solution; the comment preserves effervescence, for which the dose-form lookup has no separate powder form.
  - [Farmasierra, section 3](https://cima.aemps.es/cima/dochtml/ft/63523/FT_63523.html)
  - [Macil, section 3](https://cima.aemps.es/cima/dochtml/ft/65293/FT_65293.html)
- Bexal 100 mg (730549): despite the product name and registry powder label, section 3 describes granules. Retain EXACT Granules for Oral Solution. Bexal 200 mg retains the Powder for Oral Solution concept matching its registered pharmaceutical form.
  - [Bexal, sections 1–3 and 4.2](https://cima.aemps.es/cima/dochtml/ft/62388/FT_62388.html)
- Tarbis 600 mg (789099): despite the product name and registry powder label, section 3 specifies effervescent granules, prepared as an oral solution. Retain EXACT Granules for Oral Solution, as for the effervescent-granule presentations of Viatris and Iniston. Effervescence does not imply a modified-release mechanism.
  - [Tarbis, sections 3 and 4.2](https://cima.aemps.es/cima/dochtml/ft/64921/FT_64921.html)
  - [Viatris, sections 3 and 4.2](https://cima.aemps.es/cima/dochtml/ft/65049/FT_65049.html)
- Retain the 200 mg Powder for Oral Solution and 100/200 mg Granules for Oral Solution mappings for the remaining matching presentations.

The five row-specific INCONSISTENT_TYPE suppressions cover Cinfa 100 mg / Bexal 100 mg and Farmasierra 600 mg / Macil 600 mg / Tarbis 600 mg. Their registry signatures collide, but their section 3 descriptions differ. The mapping comments explain each decision; the source data is unchanged.

## Dispersible and disintegrating tablets

- Normofludil forte (730517) and Acetilcisteina Normon (730833): replace plain Oral Tablet with the clean Extension concept `36272593`, Acetylcysteine 600 MG Tablet for Oral Suspension. These dispersible tablets are prepared in water before administration. They are not tablets that disintegrate in the mouth. This is the closest RxNorm dose-form representation of the dispersible preparation; the labels describe the resulting liquid as a solution.
  - [Normofludil, sections 3 and 4.2](https://cima.aemps.es/cima/dochtml/ft/85822/FT_85822.html)
  - [Normon leaflet, section 3](https://cima.aemps.es/cima/dochtml/p/85923/P_85923.html)
- Retain the plain 600 mg Oral Tablet mapping for the registered plain-tablet presentation (703376), and the 200 mg Disintegrating Oral Tablet form for the bucodispersible presentation (808501).

## Parenteral presentations

- Flumil and Kern Pharma 3 mL ampoules (758706, 764182, 766532): replace concentration-only standard concept `19095712` with Extension `43752926`, 3 ML Acetylcysteine 100 MG/ML Injectable Solution. This preserves the 300 mg ampoule dose. Keep BROAD: the Extension form is Injectable Solution rather than single-use Injection, and the product also supports inhalation/endotracheobronchial administration. Do not call this EXACT solely because volume and strength match.
  - [Flumil, sections 2–4.2](https://cima.aemps.es/cima/dochtml/ft/41474/FT_41474.html)
  - [Kern Pharma, sections 2–4.2](https://cima.aemps.es/cima/dochtml/ft/90038/FT_90038.html)
- Hidonac (702836): retain EXACT `43628966`, 25 ML Acetylcysteine 200 MG/ML Injection. Section 2 confirms 5 g/25 mL; section 6.3 requires immediate use after opening and disposal after use. The original volume-specific single-use mapping is supported.
  - [Hidonac, sections 2 and 6.3–6.5](https://cima.aemps.es/cima/dochtml/ft/58931/FT_58931.html)

## Solutions and brands

- Retain standard 20 MG/ML Oral Solution and Extension 40 MG/ML Oral Solution. Standard 40 MG/ML Oral Suspension is not the registered solution form.
- Retain the 200/600 mg effervescent-tablet forms and strengths. For Fluimucil 600 mg effervescent tablets (767682, 768418, 884403), 200 mg disintegrating tablets (808501), and 200 mg granules (848531), select matching branded Extension concepts. Extension was already needed for these dose forms; this does not replace an adequate standard concept merely to add a brand.
- Retain standard unbranded 600 mg Oral Tablet and 20 MG/ML Oral Solution even where Extension has Fluimucil branding. Do not substitute unrelated brands returned by semantic search, or an oral suspension for an oral solution.
