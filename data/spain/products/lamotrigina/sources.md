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
