# Tramadol release-duration review — 2026-11-11

Reviewed the 98 extended-release presentations in this 160-row folder, using the source `des_dcp` release intervals, AEMPS labels, and fresh standard RxNorm / RxNorm Extension searches. Also corrected the two immediate-release Normon 100 mg capsule rows encountered during this review. Other immediate-release and injectable presentations were outside this release-duration review.

## More specific standard concepts

| Source presentation | Rows upgraded | Standard concept ID | Concept name | RxNorm code |
| --- | ---: | --- | --- | --- |
| 12-hour 100 mg tablets | 25 | 19107328 | 12 HR tramadol hydrochloride 100 MG Extended Release Oral Tablet | 431722 |
| 12-hour 150 mg tablets | 25 | 19135621 | 12 HR tramadol hydrochloride 150 MG Extended Release Oral Tablet | 849561 |
| 12-hour 200 mg tablets | 25 | 19135622 | 12 HR tramadol hydrochloride 200 MG Extended Release Oral Tablet | 849562 |
| 24-hour Zytram 150 mg tablet | 1 | 19135623 | 24 HR tramadol hydrochloride 150 MG Extended Release Oral Tablet | 849563 |
| 24-hour Zytram 200 mg tablet | 1 | 1103351 | 24 HR tramadol hydrochloride 200 MG Extended Release Oral Tablet | 833711 |

These 77 rows previously used untimed extended-release concepts. The timed concepts preserve strength, salt, tablet form, and the source release interval and are EXACT. Do not use the 24 HR capsule concepts for 12-hour capsules simply because their strengths match.

- [Adolonta retard 50/100/150/200 mg, sections 2 and 4.2](https://cima.aemps.es/cima/dochtml/ft/61784/FT_61784.html): hydrochloride strengths and twice-daily administration.
- [Tramadol Retard Aurovitas Spain 100/150/200 mg, sections 2 and 4.2](https://cima.aemps.es/cima/dochtml/ft/72427/FT_72427.html): hydrochloride strengths and twice-daily administration, consistent with the source's 12-hour generic tablet patterns.
- [Zytram 150/200/300/400 mg, sections 2 and 4.2](https://cima.aemps.es/cima/dochtml/ft/63131/FichaTecnica_63131.html): hydrochloride strengths and administration at 24-hour intervals.

The three Dolpar rows and Zytram 300/400 mg already use appropriate 24 HR standard tablet concepts and are retained unchanged. The source identifies these as 24-hour products. The source's subtype identifiers (tipo 1 / tipo 2) are not separately encoded by RxNorm.

## Duration gaps and strength correction

- Captor Simplex / Tradonal retard 50/100/150/200 mg capsules (12 rows): retain the matching-strength standard ER capsules, but mark BROAD because they omit the 12-hour duration. Suggestions name the full 12 HR capsule presentation. No matching 12 HR capsule was found in standard or Extension searches.
  - [Captor Simplex, sections 2 and 4.2](https://cima.aemps.es/cima/dochtml/ft/68500/FT_68500.html) confirms hydrochloride strength and twice-daily administration.
- Adolonta retard 50 mg (658668, 658669) and Andromaco retard 50 mg (724483): use standard `19135765 / 849903`, tramadol hydrochloride 50 MG Extended Release Oral Capsule, as BROAD. This preserves the salt strength and ER property but loses tablet form and 12-hour duration. Suggestions specify the 12 HR 50 mg tablet.
  - Andromaco 724483 was incorrectly mapped EXACT to a **150 mg** ER tablet. [AEMPS sections 2 and 4.2](https://cima.aemps.es/cima/dochtml/ft/83726/FT_83726.html) confirm a 50 mg hydrochloride tablet administered twice daily.
  - Extension search returned `42480148 / OMOP418654`, Tramadol 50 MG Extended Release Oral Tablet, and a Tramal-branded counterpart. The concept name does not explicitly establish hydrochloride strength equivalence. Retained the standard salt-specific BROAD fallback rather than asserting an EXACT salt/base match from the name alone. The weight-conversion reference distinguishes 50 mg hydrochloride from approximately 43.9–44.09 mg tramadol base.
- Zytram BID 75 mg (880104): retain `19135538 / 849331`, tramadol hydrochloride 75 MG Extended Release Oral Tablet, as BROAD with a 12 HR suggestion. No matching timed concept was found.
  - [AEMPS sections 2 and 4.2](https://cima.aemps.es/cima/dochtml/ft/63134/FichaTecnica_63134.html) confirms 75 mg hydrochloride and a 12-hour interval.

## Immediate-release capsule correction

Normon 100 mg capsules (731035, 731036) were mapped BROAD to an **extended-release** capsule. [AEMPS sections 2–4.2](https://cima.aemps.es/cima/dochtml/ft/85977/FT_85977.html) describes ordinary hard capsules containing 100 mg hydrochloride, with administration every 6–8 hours. No matching immediate-release 100 mg capsule concept was found in standard or Extension searches. Use standard `1361248 / 2179635`, tramadol hydrochloride 100 MG Oral Tablet, as BROAD: it preserves strength and immediate release while acknowledging the capsule/tablet mismatch. Keep the ideal capsule in `suggestion`.

## Validation

95 mapping rows changed: 77 timed-concept upgrades, 12 capsule duration downgrades, three 50 mg tablet fallback updates (including the wrong-strength correction), one 75 mg duration downgrade, and two immediate-release capsule corrections. Both folder and mapping validators pass without suppressions. The Spain overview was regenerated.
