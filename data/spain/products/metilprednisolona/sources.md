# METILPREDNISOLONA mapping review — 2026-11-11

Reviewed all 46 source presentations (17 clinical patterns) against Hecate searches of standard RxNorm and, where clinically relevant detail was missing, RxNorm Extension. This reviews the existing source snapshot rather than refreshing the AEMPS registration inventory.

## Brand corrections — 13 rows

- URBASON 4 mg and 16 mg tablets were mapped to `[Medrol]` (four rows). [AEMPS SmPC 32729](https://cima.aemps.es/cima/dochtml/ft/32729/FT_32729.html), sections 1–3, confirms URBASON tablets at 4, 16, and 40 mg. Use standard unbranded 4 mg (`1506426 / 259966`) and 16 mg (`1506479 / 328161`) oral tablets, EXACT. Retain the already correct unbranded 40 mg tablet. Matching URBASON-branded Extension concepts exist, but standard RxNorm already captures strength and form, so Extension would add only brand.
- SOLU-MODERIN 125/500/1000 mg powders were mapped to `[Solu-Medrol]` (seven rows). [AEMPS SmPC 49768](https://cima.aemps.es/cima/dochtml/ft/49768/FT_49768.html), sections 1–3, identifies SOLU-MODERIN and expresses each vial's strength as methylprednisolone base equivalent, supplied as sodium succinate. Use unbranded standard total-dose Injection concepts: 125 mg (`35606533 / 1743704`), 500 mg (`35606538 / 1743720`), and 1000 mg (`35606542 / 1743726`), EXACT. SOLU-MODERIN and Solu-Medrol are different brand names under the repository's brand-matching rule.
- NORMON 40 mg powders were mapped to `[Solu-Medrol]` (two generic rows). [AEMPS SmPC 71864](https://cima.aemps.es/cima/dochtml/ft/71864/FT_71864.html), sections 1–3, confirms 40 mg methylprednisolone per vial as sodium succinate. Use standard unbranded `methylprednisolone 40 MG Injection` (`1506430 / 311659`), EXACT, consistent with the already correct URBASON 40 mg powders.

## Low-dose injectable powders — five rows

[AEMPS URBASON SmPC 34021](https://cima.aemps.es/cima/dochtml/ft/34021/FT_34021.html), sections 2, 6.3, 6.5, and 6.6, confirms 8/20/40/250 mg methylprednisolone base equivalents, supplied as sodium hemisuccinate. The 8/20/40 mg powders are reconstituted with 2 ml water; 250 mg uses 5 ml. Reconstituted solutions are used immediately. [NORMON SmPC 71864](https://cima.aemps.es/cima/dochtml/ft/71864/FT_71864.html), section 6.6, specifies 1 ml water for its 20/40 mg vials. These are solution-forming powders, not acetate depot suspensions.

- **URBASON 8 mg (691238, 691246):** replace the unrelated branded, strengthless Solu-Medrol concept with standard unbranded `methylprednisolone Injection` (`35606532 / 1743703`), BROAD. No clean 8 mg Injection or matching volume-specific single-use concept surfaced. The selected concept retains injection form but omits dose. Suggest `methylprednisolone 8 MG Injection [Urbason]`.
- **NORMON 20 mg (664588, 682811) and URBASON 20 mg (691261):** replace the strengthless Solu-Medrol concept with clean Extension `Methylprednisolone 20 MG Injectable Solution` (`41178645 / OMOP2376607`), BROAD. This retains the total 20 mg dose but the repository defines Injectable Solution as multiple use, whereas Injection denotes the single-use presentation. No suitable total-dose or volume-specific Injection concept surfaced. Suggestions retain the intended 20 mg Injection (and URBASON brand where applicable). This is a deliberate dose-preserving fallback, not an EXACT mapping.
- **URBASON 250 mg:** retain `2057251 / OMOP4958111`, EXACT. Standard searches lack a suitable 250 mg Injection; Extension supplies the correct total-dose powder-vial presentation. The sodium hemisuccinate mass is not the labeled clinical strength.

## Methylprednisolone aceponate skin products

[ADVENTAN cream SmPC 60137](https://cima.aemps.es/cima/dochtml/ft/60137/FT_60137.html), section 2, specifies **1 mg methylprednisolone aceponate per g**, rather than 1 mg methylprednisolone base. [ADVENTAN emulsion SmPC 62662](https://cima.aemps.es/cima/dochtml/ft/62662/FT_62662.html) identifies the same ester strength in an oil-in-water cutaneous emulsion; [ISZEMA emulsion SmPC 82969](https://cima.aemps.es/cima/dochtml/ft/82969/FT_82969.html) likewise specifies 1 mg/g aceponate.

Neither standard nor Extension searches produced a verified aceponate-specific clinical concept. Extension results such as `Methylprednisolone 0.001 MG/MG Topical Cream`, ointment, lotion, or `Methylprednisolone 1 MG/ML Topical Solution` omit the ester. Their numeric strengths cannot establish an EXACT ester match. Do not silently treat aceponate mass as methylprednisolone-base mass.

- Retain standard strengthless methylprednisolone cream (six rows) and ointment (eight rows) as BROAD, with aceponate-specific suggestions.
- Retain the five emulsion rows as BROAD cream fallbacks. This continues to omit the ester, strength, and precise emulsion form. A lotion Extension result does not by itself establish a verified closer presentation; no change was made solely on that basis.
- **Cutaneous solutions (662437, 728343, 959668):** improve the ingredient-only mapping to clean Extension `Methylprednisolone Topical Solution` (`40830446 / OMOP2028408`), BROAD. [ADVENTAN solution SmPC 63521](https://cima.aemps.es/cima/dochtml/ft/63521/FT_63521.html) and [SKINATAN solution SmPC 85015](https://cima.aemps.es/cima/dochtml/ft/85015/FT_85015.html), sections 2–3, confirm aceponate 1 mg/ml cutaneous solution. Extension is justified by the missing topical solution form in standard search results, while the ester and strength remain unrepresented. Keep the suggestion `methylprednisolone aceponate 1 MG/ML Topical Solution`.

## Validation

After 21 row corrections: **19 EXACT, 27 BROAD**. Spain folder validation and mapping validation pass without new suppressions. Regenerate the combined Spain overview from the corrected mapping file.
