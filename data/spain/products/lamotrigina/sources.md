# Lamotrigine dose-form review

Reviewed 2026-11-09.

- [AEMPS: Lamictal, all strengths](https://cima.aemps.es/cima/dochtml/ft/61569/FichaTecnica_61569.html), sections 2, 3 and 4.2: the 2, 5, 25, 50, 100 and 200 mg tablets are chewable/dispersible and may be chewed, dispersed in water or swallowed whole.
- [DailyMed: Lamictal](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=d7e3572d-56fe-4727-2bb4-013ccca22678), sections 2.5, 2.6 and 3: tablets for oral suspension (2, 5 and 25 mg) may be swallowed whole, chewed or dispersed in liquid. Lamictal ODT is a separate formulation intended to disintegrate on the tongue. These are distinct dose forms.
- [AEMPS: Lamotrigina Stada, 25/50/100/200 mg](https://cima.aemps.es/cima/dochtml/ft/66695/FichaTecnica_66695.html), sections 3 and 4.2.2: these tablets are dispersible; instructions specify dispersing in water or swallowing with water. Chewing is not specified. Do not infer chewability solely from other manufacturers' presentations.

## Mapping decisions

Standard RxNorm has exact Tablet for Oral Suspension concepts at 2, 5 and 25 mg. Retain the existing 2 and 5 mg mappings and use the 25 mg suspension-tablet concepts (705160 / 311264 unbranded; 19024857 / 201240 for Lamictal). These match the dispersible presentation more closely than ODT.

For chewable/dispersible 50, 100 and 200 mg tablets, standard RxNorm searches did not find suitable suspension-tablet or chewable concepts. Extension provides clean Chewable Tablet concepts:

| Strength | Unbranded concept / code | Lamictal concept / code |
| --- | --- | --- |
| 50 mg | 43643535 / OMOP901195 | 36893937 / OMOP992017 |
| 100 mg | 43679565 / OMOP900805 | 36887996 / OMOP1006760 |
| 200 mg | 43841444 / OMOP901095 | 36892976 / OMOP1001548 |

These Extension concepts resolve a clinically relevant form mismatch and are EXACT under the Spain skill's chewable-tablet convention. Preserve matching Lamictal branding. Crisomet and Labileno must not inherit the Lamictal brand; use unbranded concepts for those presentations.

Stada's dispersible-only 25 mg tablet maps EXACT to the standard Tablet for Oral Suspension concept. Searches including Extension did not find clean matching-strength Tablet for Oral Suspension concepts for its 50, 100 and 200 mg presentations. Retain the standard matching-strength Disintegrating Oral Tablet concepts as BROAD, explicitly recording the form mismatch and the ideal Tablet for Oral Suspension suggestions. Do not substitute Chewable Tablet or Effervescent Oral Tablet as EXACT without evidence for those properties.

Some source rows coded simply COMPRIMIDO DISPERSABLE nevertheless name Aurobindo/Aurovitas chewable/dispersible products in des_nomco. Preserve that more specific presentation information when choosing their concepts.

## Follow-up review — 2026-11-11

Reviewed all 89 rows across 15 registry patterns. Rechecked source/mapping row coverage, registration IDs, ingredient, strength, route, and Lamictal brand assignments. All agree. Strength distribution: 2 mg (1 row), 5 mg (3), 25 mg (20), 50 mg (23), 100 mg (20), and 200 mg (22).

Repeated standard and Extension searches for 2/5/25/50/100/200 mg Tablet for Oral Suspension, 50/100/200 mg Chewable Tablet, and matching brands. The previous clinical mapping decisions remain supported; no mapping changes are required.

- Standard Tablet for Oral Suspension remains appropriate at 2, 5 and 25 mg. [DailyMed section 2.5](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=d7e3572d-56fe-4727-2bb4-013ccca22678) explicitly permits chewing or dispersing these tablets; section 2.6 describes the separate mouth-disintegrating ODT formulation.
- Clean Extension Chewable Tablet concepts remain appropriate at 50, 100 and 200 mg for chewable/dispersible products, with matching Lamictal branding retained. No suitable matching-strength Tablet for Oral Suspension concepts were found at those strengths.
- Stada 50/100/200 mg (656062, 656063, 656069) remains BROAD to matching-strength standard ODT concepts with the dispersible-tablet suggestions. [Stada section 4.2.2](https://cima.aemps.es/cima/dochtml/ft/66695/FichaTecnica_66695.html) specifies dispersing in water or swallowing; it does not establish chewability. A strength-matched ODT fallback must not be relabelled EXACT.
- [Aurobindo sections 3 and 4.2](https://cima.aemps.es/cima/dochtml/ft/73095/FichaTecnica_73095.html) and [Aurovitas sections 3 and 4.2](https://cima.aemps.es/cima/dochtml/ft/81817/FT_81817.html) explicitly identify chewable/dispersible tablets and permit chewing. This supports the existing mappings where the registry form field merely says dispersible.
- [Teva sections 1–3](https://cima.aemps.es/cima/dochtml/ft/67350/FT_67350.html) confirm the 50/100/200 mg chewable/dispersible presentations. Searches also returned matching Teva-branded Extension concepts (43213774 / OMOP465704, 43147888 / OMOP465748, 43147873 / OMOP465664). The existing unbranded Extension concepts already preserve the clinical presentation and are retained as reviewed EXACT anchors. These branded alternatives add no strength or dose-form detail. No matching Crisomet or Labileno clinical brand concepts were found.

Result: 86 EXACT and 3 BROAD; both folder and mapping validators pass without suppressions. Mapping dates and the generated overview are unchanged because no mapping decisions changed.
