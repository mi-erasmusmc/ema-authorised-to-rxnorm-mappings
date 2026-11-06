# Levodopa/carbidopa mapping evidence

Reviewed 2026-11-06.

## Tablets

The three missing Kern Pharma presentations contain carbidopa/levodopa 25/100 mg or 25/250 mg in immediate-release tablets. They use standard unbranded concepts RxCUI 197444 and 197445, matching the existing generic anchors.

Sinemet Plus Retard 25/100 mg retains its standard branded extended-release concept. Sinemet Retard 50/200 mg uses the matching standard branded extended-release concept RxCUI 834341 instead of the existing unbranded concept. The Sinemet immediate-release presentations retain their existing matching branded concepts. Source strengths sometimes list carbidopa first and sometimes levodopa first; ingredient identities and product names were checked rather than relying on numeric position alone.

## Duodopa intestinal gel / enteral suspension

[AEMPS Duodopa SmPC](https://cima.aemps.es/cima/dochtml/ft/66547/FT_66547.html) specifies levodopa 20 mg/mL and carbidopa monohydrate 5 mg/mL. The product is administered continuously into the intestine; its Spanish source dose-form field is gastrointestinal suspension.

[DailyMed Duopa label and RxNorm table](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=7066d371-dc6a-0d6f-7bed-e5dd4ee912da) explicitly relates carbidopa monohydrate 5 mg/mL to anhydrous carbidopa 4.63 mg/mL. RxCUI 1599846 has an Oral Suspension clinical-drug name and an Enteral Suspension prescribable name. These support adapting the Spanish intestinal suspension to that standard concept as EXACT, rather than interpreting its Oral Suspension wording as necessarily a swallowed formulation.

Selected unbranded standard concept: OMOP 45892917 / RxCUI 1599846, `carbidopa 4.63 MG/ML / levodopa 20 MG/ML Oral Suspension`. The differing US brand name is not used. The previous Extension `Oral Gel [Duodopa]` concept is unnecessary because standard RxNorm already represents the relevant enteral formulation with explicit hydrate/base equivalence. The concentration-level concept is appropriate for individually titrated continuous infusion; cassette size is not a fixed administered dose.

This does not establish that every Oral Gel Extension concept denotes intestinal use. The separate Lecigon mapping remains BROAD because its three-ingredient Extension concept lacks equivalent supporting enteral terminology evidence.
