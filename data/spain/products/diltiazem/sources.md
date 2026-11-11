# DILTIAZEM mapping review — 2026-11-11

Reviewed all 61 presentations (15 source patterns). Standard and Extension Hecate searches covered strengths, tablet versus capsule, and 12/24-hour extended-release concepts. AEMPS SmPCs were retrieved for each unique registration where available. The registration inventory itself was not refreshed.

## Duration-specific mappings — 31 rows

The following selections interpret the **labeled extended-release formulation together with its product-specific regimen** as the corresponding RxNorm 12/24-hour release family. They are mapping inferences, not measurements of drug-release kinetics or assertions of interchangeability. Half-life, time to peak, and dosing of a different strength alone were not used to choose duration.

| Source presentations | Rows | Selected standard concept | concept_id / concept_code | Evidence |
|---|---:|---|---|---|
| LACEROL RETARD 90 mg; ANGIODROX 90 mg | 3 | 12 HR diltiazem hydrochloride 90 MG Extended Release Oral Capsule | 19133582 / 830869 | [60005](https://cima.aemps.es/cima/dochtml/ft/60005/FT_60005.html), [60215](https://cima.aemps.es/cima/dochtml/ft/60215/FT_60215.html): 90 mg twice daily |
| DILTIWAS RETARD 120 mg; DOCLIS RETARD 120 mg | 2 | 12 HR diltiazem hydrochloride 120 MG Extended Release Oral Capsule | 19133585 / 830872 | [60091](https://cima.aemps.es/cima/dochtml/ft/60091/FT_60091.html), [60089](https://cima.aemps.es/cima/dochtml/ft/60089/FT_60089.html): usual 120 mg every 12 hours |
| CRONODINE 120 mg | 2 | 24 HR diltiazem hydrochloride 120 MG Extended Release Oral Capsule | 19133574 / 830861 | [61132](https://cima.aemps.es/cima/dochtml/ft/61132/FT_61132.html): single daily dose; formulation-specific discussion of therapeutic levels at 24 hours |
| TRUMSAL 180 mg | 1 | 24 HR diltiazem hydrochloride 180 MG Extended Release Oral Capsule | 19133570 / 830845 | [61133](https://cima.aemps.es/cima/dochtml/ft/61133/FT_61133.html): single daily dose and formulation-specific 24-hour pharmacokinetic discussion |
| CRONODINE 240 mg; LACEROL HTA RETARD 240 mg | 3 | 24 HR diltiazem hydrochloride 240 MG Extended Release Oral Capsule | 19133566 / 830837 | [61134](https://cima.aemps.es/cima/dochtml/ft/61134/FT_61134.html), [60200](https://cima.aemps.es/cima/dochtml/ft/60200/FT_60200.html): once-daily capsules |
| LACEROL RETARD 300 mg; ANGIODROX 300 mg; MASDIL 300 mg; TILKER 300 mg; STADA/DERMOGEN/FARMALIDER 300 mg | 8 | 24 HR diltiazem hydrochloride 300 MG Extended Release Oral Capsule | 19133562 / 830801 | Once-daily capsule regimens in the individual SmPCs linked below |
| LACEROL COR RETARD 240 mg; CARRELDON RETARD 240 mg | 3 | 24 HR diltiazem hydrochloride 240 MG Extended Release Oral Tablet | 19133591 / 830879 | [60740](https://cima.aemps.es/cima/dochtml/ft/60740/FT_60740.html), [60742](https://cima.aemps.es/cima/dochtml/ft/60742/FT_60742.html): once-daily tablets; product-specific pharmacokinetic studies |

The individual 300 mg capsule SmPCs are [LACEROL 61652](https://cima.aemps.es/cima/dochtml/ft/61652/FT_61652.html), [ANGIODROX 60214](https://cima.aemps.es/cima/dochtml/ft/60214/FT_60214.html), [MASDIL 59911](https://cima.aemps.es/cima/dochtml/ft/59911/FT_59911.html), [TILKER 59950](https://cima.aemps.es/cima/dochtml/ft/59950/FT_59950.html), [STADA 77586](https://cima.aemps.es/cima/dochtml/ft/77586/FT_77586.html), [DERMOGEN 78966](https://cima.aemps.es/cima/dochtml/ft/78966/FT_78966.html), and [FARMALIDER 78967](https://cima.aemps.es/cima/dochtml/ft/78967/FT_78967.html). STADA was retrieved directly when browser retrieval failed.

Existing strengths, oral routes, and tablet/capsule distinctions are preserved. ANGIODROX 300 mg also uses the hydrochloride-specific name consistent with the source's listed ingredient.

### Additional Hecate standard concepts — nine rows

- **MASDIL RETARD 120 mg tablets (639195, 864975) and TILKER 120 mg tablets (653725):** [58483](https://cima.aemps.es/cima/dochtml/ft/58483/FT_58483.html) specifies every 12 hours; [60101](https://cima.aemps.es/cima/dochtml/ft/60101/FT_60101.html) specifies morning and evening. Use Hecate standard `12 HR diltiazem 120 MG Extended Release Oral Tablet` (`1328170 / 246395`), EXACT. The legacy ingredient name is diltiazem; retain the labeled clinical strength rather than introducing a salt-mass conversion. This concept captures the tablet formulation and 12-hour distinction.
- **All six 200 mg capsules:** [UNI-MASDIL 60820](https://cima.aemps.es/cima/dochtml/ft/60820/FT_60820.html), [TILKER 60819](https://cima.aemps.es/cima/dochtml/ft/60819/FT_60819.html), [STADA 77587](https://cima.aemps.es/cima/dochtml/ft/77587/FT_77587.html), [FARMALIDER 78934](https://cima.aemps.es/cima/dochtml/ft/78934/FT_78934.html), and [DERMOGEN 78965](https://cima.aemps.es/cima/dochtml/ft/78965/FT_78965.html) specify once-daily extended-release capsules. Use Hecate standard `24 HR diltiazem hydrochloride 200 MG Extended Release Oral Capsule` (`19133847 / 833716`), EXACT.

### OHDSI concept eligibility and NLM status

The mapping target is the OHDSI standard vocabulary returned by Hecate. NLM's current RxNorm status is not an independent eligibility filter: a concept marked Obsolete by NLM can remain usable when Hecate returns it as standard and it clinically matches the source presentation. Check for a superseding/replacement concept separately; obsolescence alone is not evidence of replacement and must not force a BROAD mapping.

Both concepts above were reconfirmed through Hecate's standard search on 2026-11-11. NLM history for [246395](https://rxnav.nlm.nih.gov/REST/rxcui/246395/historystatus.json) and [833716](https://rxnav.nlm.nih.gov/REST/rxcui/833716/historystatus.json) reports Obsolete, but neither response identifies a remapped/replacement clinical drug concept (remappedDate is empty and derivedConcepts lists only the ingredient). These status findings do not override their Hecate standard-concept eligibility.

## Retained mappings and limits

- **14 immediate-release 60 mg tablets:** retain the standard hydrochloride Oral Tablet concept. A dosing interval is not added to an immediate-release concept. For example, [MASDIL 55285](https://cima.aemps.es/cima/dochtml/ft/55285/FT_55285.html) specifies conventional tablets given every eight hours, not an eight-hour extended-release formulation.
- **LACEROL RETARD 120/180 mg and ANGIODROX 120/180 mg (six rows):** retain the generic extended-release capsule concepts. Their labels describe twice-daily angina regimens and daily hypertension doses; these do not establish a unique release-duration distinction. The 300 mg pharmacokinetic discussion must not be transferred automatically to the lower strengths. Evidence: [LACEROL 60006](https://cima.aemps.es/cima/dochtml/ft/60006/FT_60006.html), [60007](https://cima.aemps.es/cima/dochtml/ft/60007/FT_60007.html), [ANGIODROX 60217](https://cima.aemps.es/cima/dochtml/ft/60217/FT_60217.html), and [60216](https://cima.aemps.es/cima/dochtml/ft/60216/FT_60216.html).
- **DINISOR RETARD 120/180 mg tablets (three rows):** [58590](https://cima.aemps.es/cima/dochtml/ft/58590/FT_58590.html) and [59776](https://cima.aemps.es/cima/dochtml/ft/59776/FT_59776.html) confirm modified-release tablets but do not establish a unique 12/24-hour regimen. Retain the generic extended-release tablet concepts.
- **Seven rows lack an accessible current SmPC:** registrations 59190 (two LACEROL RETARD 120 mg rows), 62272 (MUNDIPHARMA 300 mg), 60008 (DILACLAN HTA 300 mg), 60090 (DOCLIS RETARD 240 mg), and historical TILKER registrations 11456610496 and 27502 returned HTTP 404. Retain existing strength/form mappings from the local source without inferring duration from another registration or the shared brand name.
- Standard unbranded concepts remain preferred; searches did not establish matching standard brand concepts for the Spanish brands. Standard RxNorm covers the clinical strengths/forms, so Extension was not used solely to add a brand.
- Several AEMPS labels describe the ingredient as diltiazem “as hydrochloride,” while the source ingredient column explicitly lists hydrochloride at the nominal clinical strength. Preserve the labeled clinical strength; no molecular-weight conversion was introduced.

## Validation

31 rows changed to duration-specific concepts. Final totals: **61 EXACT, 0 BROAD**. Folder and mapping validators pass without new suppressions. Regenerate the combined Spain overview.
