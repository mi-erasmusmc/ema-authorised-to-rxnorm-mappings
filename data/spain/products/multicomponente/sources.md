# Multicomponente mapping evidence

Reviewed 2026-11-10. The folder combines unrelated formulations; decisions are based on the actual named products and registered compositions, not the shared multicomponente label.


## Fluids, coagulation products and vitamins (reviewed 2026-11-10)

The source collapses many ingredient lists into `N/A (más de 4 PA)`. Composition was checked against CIMA section 2; concentrations below use the final formulation, with labelled salt/hydrate strengths preserved. Hecate searches covered standard RxNorm then Extension, including broader result sets from the same search_standard endpoint. Supplier/box concepts, unrelated brands, wrong concentrations and isotope-labelled vitamin concepts were excluded.

All selections in this cluster are BROAD: the full clinically specific formulation, quantitative strengths, relevant reconstitution volume, or presentation could not be matched without unsupported assumptions. Suggestions preserve the intended formulation. Nominal coagulation-complex potency is factor IX activity rather than equal activity of every factor.

- [POLIELECTROLÍTICA PLUS BRAUN MINIPLASCO CONCENTRADO PARA SOLUCIÓN PARA PERFUSIÓN (67343)](https://cima.aemps.es/cima/dochtml/ft/67343/FT_67343.html): Preserves magnesium acetate, potassium acetate and sodium chloride; omits calcium gluconate and zinc chloride. Source is a concentrate for dilution. Selected `40152675` / `801141`.

- [VOLULYTE 6% SOLUCION PARA PERFUSION (70228)](https://cima.aemps.es/cima/dochtml/ft/70228/FT_70228.html): Omits the balanced electrolyte vehicle. Source starch is HES 130/0.4; do not substitute hetastarch. Selected `43011673` / `1363390`.

- [GELOPLASMA, SOLUCION PARA PERFUSION (68045)](https://cima.aemps.es/cima/dochtml/ft/68045/FT_68045.html): Modified fluid gelatin is partially hydrolysed and succinylated. Available standard concept omits strength and electrolyte vehicle; Gelofusine 40 mg/mL is a different product. Selected `40101482` / `379284`.

- [IONOLYTE SOLUCION  PARA PERFUSION (74568)](https://cima.aemps.es/cima/dochtml/ft/74568/FT_74568.html): CIMA corrects source decimal errors: potassium and magnesium chloride are each 0.30 mg/mL. Available strength-specific Extension concepts round sodium chloride to 6 mg/mL. Selected `43022207` / `OMOP4837344`.

- [GELASPAN 40 MG/ML SOLUCION PARA PERFUSION (76222)](https://cima.aemps.es/cima/dochtml/ft/76222/FT_76222.html): Available quantitative concepts differ from verified source concentrations. Selected `43689244` / `OMOP919980`.

- [SUPLIVEN CONCENTRADO PARA SOLUCION PARA PERFUSION (81396)](https://cima.aemps.es/cima/dochtml/ft/81396/FT_81396.html): Source strengths use the labelled hydrated salts. Strength-specific inherited concept had incorrect copper and manganese concentrations. Selected `36955736` / `OMOP5202114`.

- [MAINTELYTE SOLUCION PARA PERFUSION (84093)](https://cima.aemps.es/cima/dochtml/ft/84093/FT_84093.html): Source acetate strength is explicitly the trihydrate; selected Extension concept does not specify hydration state. Selected `36062937` / `OMOP4988994`.

- [APIROSERUM NORMAION RESTAURADOR (45434)](https://cima.aemps.es/cima/dochtml/ft/45434/FT_45434.html): Preserves five electrolyte ingredients; omits glucose and citrate. Calcium, magnesium, acetate and citrate are expressed in anhydrous-equivalent source strengths. Selected `40151792` / `801450`.

- [NORMOFUNDINA CON POTASIO SOLUCIÓN PARA PERFUSIÓN (63007)](https://cima.aemps.es/cima/dochtml/ft/63007/FT_63007.html): Available quantitative concepts differ from verified source concentrations. Selected `43707059` / `OMOP917069`.

- [ESTEROFUNDINA CON GLUCOSA 5% SOLUCION PARA PERFUSION (41756)](https://cima.aemps.es/cima/dochtml/ft/41756/FT_41756.html): Available quantitative concepts differ from verified source concentrations. Selected `43815277` / `OMOP958455`.

- [ESTEROFUNDINA DE BALANCE SOLUCION PARA PERFUSION (47059)](https://cima.aemps.es/cima/dochtml/ft/47059/FT_47059.html): Archived product composition; source potassium chloride is 0.180 g per 100 mL. Hydrated salts as labelled; glucose is anhydrous-equivalent. Selected `43599273` / `OMOP958285`.

- [OCTAPLEX, 500 UI POLVO Y DISOLVENTE PARA SOLUCION INYECTABLE. (66447)](https://cima.aemps.es/cima/dochtml/ft/66447/FT_66447.html): Nominal 500 IU is based on factor IX activity in a 20 mL reconstituted vial; other factors and proteins C/S have variable ranges. Replaces the equal-1-unit formulation, which does not describe these potency ratios. Selected `35602741` / `1670052`.

- [ISOFUNDIN SOLUCION PARA PERFUSION (66709)](https://cima.aemps.es/cima/dochtml/ft/66709/FT_66709.html): Available quantitative concepts differ from verified source concentrations. Selected `36887563` / `OMOP1000265`.

- [ELEVIT COMPRIMIDOS RECUBIERTOS CON PELICULA (67267)](https://cima.aemps.es/cima/dochtml/ft/67267/FT_67267.html): Prenatal iron/folate subset. Available branded Extension Elevit concepts have incorrect iron/mineral salts and delayed-release form; other vitamins/minerals omitted. Selected `40131875` / `619032`.

- [VIAFLO PLASMALYTE 148 (PH 7,4), SOLUCION PARA PERFUSION (67821)](https://cima.aemps.es/cima/dochtml/ft/67821/FT_67821.html): IV infusion; replaces the incorrect Irrigation Solution concept. Magnesium chloride is hexahydrate and sodium acetate is trihydrate in CIMA. Selected `40152082` / `801356`.

- [ISOHES 6% SOLUCION  PARA PERFUSION (68812)](https://cima.aemps.es/cima/dochtml/ft/68812/FT_68812.html): Closest HES 130 concept; source substitution is 0.42 and the balanced electrolyte vehicle is not represented. Selected `43011673` / `1363390`.

- [CARDI-BRAUN MANTENIMIENTO SOLUCION PARA PERFUSION (69784)](https://cima.aemps.es/cima/dochtml/ft/69784/FT_69784.html): Preserves glucose, potassium chloride, sodium chloride and citrate only. Source is intracardiac cardioplegia; selected IV subset does not encode that use. Glucose 34.66 mg/mL monohydrate equals 31.51 mg/mL anhydrous. Selected `21034809` / `OMOP399120`.

- [CARDI-BRAUN REPERFUSION SOLUCION PARA PERFUSION (69785)](https://cima.aemps.es/cima/dochtml/ft/69785/FT_69785.html): Glucose/potassium chloride subset only; source is intracardiac cardioplegia and includes amino acids, citrate, phosphate and tromethamine. Glucose 40.553 mg/mL monohydrate equals 36.87 mg/mL anhydrous. Selected `36880829` / `OMOP997855`.

- [BERIPLEX 500 UI POLVO Y DISOLVENTE PARA SOLUCION INYECTABLE (69890)](https://cima.aemps.es/cima/dochtml/ft/69890/FT_69890.html): Nominal 500 IU is based on factor IX activity in a 20 mL reconstituted vial; other factors and proteins C/S have variable ranges. Replaces the equal-1-unit formulation, which does not describe these potency ratios. Selected `35602741` / `1670052`.

- [NEURODAVUR PLUS, INYECTABLE (48981)](https://cima.aemps.es/cima/dochtml/ft/48981/FT_48981.html): Dexamethasone injection subset; omits hydroxocobalamin, lidocaine and vitamins B1/B6. Official AEMPS archived SmPC lists 1.6 mg dexamethasone sodium phosphate per 2.5 mL ampoule. Selected `1719010` / `1812073`.

- [SOLUVIT LIOFILIZADO PARA SOLUCION PARA PERFUSION (61228)](https://cima.aemps.es/cima/dochtml/ft/61228/FT_61228.html): Available quantitative concepts differ from verified source concentrations. Selected `43264123` / `OMOP572762`.

- [CELSIOR SOLUCION PARA LA CONSERVACION DE ORGANOS (73767)](https://cima.aemps.es/cima/dochtml/ft/73767/FT_73767.html): Full ingredient family with surface-solution form; source is ex vivo organ preservation, not IV injection. Available strength-specific concepts differ in histidine and other concentrations. Selected `43743133` / `OMOP920318`.

- [LUNAFEM CAPSULAS BLANDAS (73818)](https://cima.aemps.es/cima/dochtml/ft/73818/FT_73818.html): Preserves ten-vitamin/iron subset; omits vitamin E, calcium and zinc. Iron is supplied as ferrous fumarate; suggestion expresses elemental iron as labelled. Selected `43832986` / `OMOP769306`.

- [BERIPLEX 1000 UI  POLVO Y DISOLVENTE PARA SOLUCION INYECTABLE (76961)](https://cima.aemps.es/cima/dochtml/ft/76961/FT_76961.html): Nominal 1000 IU is based on factor IX activity in a 40 mL reconstituted vial; other factors and proteins C/S have variable ranges. Replaces the equal-1-unit formulation, which does not describe these potency ratios. Selected `35602741` / `1670052`.

- [PROTHROMPLEX TOTAL 600 UI / 20 ML POLVO Y DISOLVENTE PARA SOLUCION INYECTABLE (78913)](https://cima.aemps.es/cima/dochtml/ft/78913/FT_78913.html): Nominal potency is factor IX activity; 20 mL after reconstitution. Factor VII is 25 IU/mL in current Total products; inherited 24 IU/mL formulation was not exact. Product-level complex concept preserves variable factor potencies without inventing fixed ratios. Selected `1254255` / `OMOP5556257`.

- [FEIBA 25 U/ML POLVO Y DISOLVENTE PARA SOLUCION PARA PERFUSION (80118)](https://cima.aemps.es/cima/dochtml/ft/80118/FT_80118.html): Matches nominal vial potency; concept does not distinguish reconstitution concentration/volume. Selected `42931431` / `OMOP4658194`.

- [OCTAPLEX 1000 UI POLVO Y DISOLVENTE PARA SOLUCION PARA PERFUSION (80417)](https://cima.aemps.es/cima/dochtml/ft/80417/FT_80417.html): Nominal 1000 IU is based on factor IX activity in a 40 mL reconstituted vial; other factors and proteins C/S have variable ranges. Replaces the equal-1-unit formulation, which does not describe these potency ratios. Selected `35602741` / `1670052`.

- [HYPERLITE CONCENTRADO PARA SOLUCION PARA PERFUSION (59925)](https://cima.aemps.es/cima/dochtml/ft/59925/FT_59925.html): Source is a concentrate for dilution; potassium is acetate, not chloride. Selected `45775951` / `1547457`.

- [FEIBA 50 U/ML POLVO Y DISOLVENTE PARA SOLUCION PARA PERFUSION (80119)](https://cima.aemps.es/cima/dochtml/ft/80119/FT_80119.html): Matches nominal vial potency; concept does not distinguish reconstitution concentration/volume. Selected `42931436` / `OMOP4658198`.

- [BECOZYME C FORTE COMPRIMIDOS RECUBIERTOS (40869)](https://cima.aemps.es/cima/dochtml/ft/40869/FT_40869.html): Five B-vitamin subset; omits ascorbic acid, biotin and cyanocobalamin. Selected concept does not resolve the salt-specific source strengths. Selected `40986296` / `OMOP2184258`.

- [CERNEVIT POLVO PARA SOLUCIÓN INYECTABLE Y PARA PERFUSIÓN (60022)](https://cima.aemps.es/cima/dochtml/ft/60022/FT_60022.html): Strength-specific candidates differ in vitamin strengths, use wrong vitamin forms, or include cobalt-57-labelled cyanocobalamin; chose complete unquantified ingredient combination. Selected `2935340` / `OMOP5152076`.

- [BENELYTE SOLUCION PARA PERFUSION (82351)](https://cima.aemps.es/cima/dochtml/ft/82351/FT_82351.html): Source glucose monohydrate 11 mg/mL equals anhydrous glucose 10 mg/mL. Previous concept also had incorrect sodium chloride strength. Selected `43707059` / `OMOP917069`.

- [NATROVIT POLVO PARA SOLUCION PARA PERFUSION EFG (82702)](https://cima.aemps.es/cima/dochtml/ft/82702/FT_82702.html): Strength-specific candidates differ in vitamin strengths, use wrong vitamin forms, or include cobalt-57-labelled cyanocobalamin; chose complete unquantified ingredient combination. Selected `2935340` / `OMOP5152076`.

- [VIANT POLVO PARA SOLUCION PARA PERFUSION (83664)](https://cima.aemps.es/cima/dochtml/ft/83664/FT_83664.html): Complete 12-vitamin subset; omits vitamin K1 0.15 mg. Dexpanthenol 14 mg corresponds to pantothenic acid 15 mg. Selected `2935340` / `OMOP5152076`.

- [CUSTODIOL SOLUCION PARA CARDIOPLEJIA Y PARA CONSERVACION DE ORGANOS (84838)](https://cima.aemps.es/cima/dochtml/ft/84838/FT_84838.html): Topical Solution is the closest surface-perfusion/organ-preservation presentation. Concept uses potassium alpha-ketoglutarate rather than source alpha-ketoglutaric acid and omits quantitative/histidine salt detail; do not use the erroneous Oral Solution or IV concept. Selected `43851150` / `OMOP919523`.

- [FUNSIX CAPSULAS (55439)](https://cima.aemps.es/cima/dochtml/ft/55439/FT_55439.html): Biotin/riboflavin capsule subset; omits amino acids, millet, pantothenate, pyridoxine and vitamin E. Previous vitamin A mapping was unrelated. Composition from archived manufacturer PIL-FOOD leaflet for registration 55439. Selected `40830853` / `OMOP2028815`.

- [PROTHROMPLEX TOTAL 500 UI POLVO Y DISOLVENTE PARA SOLUCIÓN INYECTABLE (88851)](https://cima.aemps.es/cima/dochtml/ft/88851/FT_88851.html): Nominal potency is factor IX activity; 17 mL after reconstitution. Factor VII is 25 IU/mL in current Total products; inherited 24 IU/mL formulation was not exact. Product-level complex concept preserves variable factor potencies without inventing fixed ratios. Selected `1254255` / `OMOP5556257`.

- [INFUTRAZE CONCENTRADO PARA SOLUCION PARA PERFUSION (88927)](https://cima.aemps.es/cima/dochtml/ft/88927/FT_88927.html): Copper chloride injection subset; full five-element formulation not found. Previous concept added fluoride, which is absent from Infutraze. Source is a single-use 10 mL concentrate ampoule. Standard RxNorm `1734715` / `2688015` preserves the injection subset.

- [CORHUM SOLUCIÓN PARA CARDIOPLEJIA Y PARA CONSERVACIÓN DE ÓRGANOS (89242)](https://cima.aemps.es/cima/dochtml/ft/89242/FT_89242.html): Topical Solution is the closest surface-perfusion/organ-preservation presentation. Concept uses potassium alpha-ketoglutarate rather than source alpha-ketoglutaric acid and omits quantitative/histidine salt detail; do not use the erroneous Oral Solution or IV concept. Selected `43599037` / `OMOP919513`.

- [FEIBA 100 U/ML POLVO Y DISOLVENTE PARA SOLUCIÓN PARA PERFUSIÓN (89446)](https://cima.aemps.es/cima/dochtml/ft/89446/FT_89446.html): Matches nominal vial potency; concept does not distinguish reconstitution concentration/volume. Selected `42931431` / `OMOP4658194`.

- [HIDROPOLIVIT A -C GRANULADO PARA SUSPENSION ORAL (44002)](https://cima.aemps.es/cima/dochtml/ft/44002/FT_44002.html): Three-vitamin subset matching the constituted suspension; source is powder for oral suspension. Omits vitamin E, riboflavin, pyridoxine, niacinamide and biotin. Selected `1466256` / `2713890`.

- [HIDROPOLIVIT A MINERAL COMPRIMIDOS MASTICABLES (44019)](https://cima.aemps.es/cima/dochtml/ft/44019/FT_44019.html): Vitamins A/C/D and fluoride chewable-tablet subset; omits the other five vitamins and nine minerals. Source fluoride is supplied as sodium fluoride. Selected `1145963` / `2371958`.

- [HIDROPOLIVIT COMPLEX COMPRIMIDOS RECUBIERTOS (44001)](https://cima.aemps.es/cima/dochtml/ft/44001/FT_44001.html): Five B-vitamin subset; omits vitamins C/D/E and biotin. Composition from archived manufacturer SmPC. Selected `40986296` / `OMOP2184258`.

- [HIDROPOLIVIT GOTAS  ORALES EN SOLUCION (44000)](https://cima.aemps.es/cima/dochtml/ft/44000/FT_44000.html): Three-vitamin oral solution subset; omits vitamin E, riboflavin, pyridoxine, biotin and niacinamide. Source has no thiamine or B12. Selected `42799204` / `1292775`.

- [PROTHROMPLEX 600 UI/20 ml POLVO Y DISOLVENTE PARA SOLUCION INYECTABLE (54938)](https://cima.aemps.es/cima/dochtml/ft/54938/FT_54938.html): Nominal potency is factor IX activity; 20 mL after reconstitution. Factor VII is 25 IU/mL in current Total products; inherited 24 IU/mL formulation was not exact. Product-level complex concept preserves variable factor potencies without inventing fixed ratios. Selected `1254255` / `OMOP5556257`.

Additional primary/archived documents:

- [Esterofundina con Glucosa 5% official PDF](https://cima.aemps.es/cima/pdfs/ft/41756/FT_41756.pdf) supplied the composition where HTML was unavailable.

- [Neurodavur Plus official AEMPS archived SmPC](https://www.aemps.gob.es/informa/notasInformativas/medicamentosUsoHumano/seguridad/2005/docs/neurodavur_FT.pdf): five active ingredients in a 2.5 mL ampoule.

- [Hidropolivit A-C manufacturer SmPC hosted by ANEFP](https://anefp.org/sites/default/files/7692409_ft.pdf): eight active vitamins per sachet, powder for suspension.

- [Hidropolivit Complex manufacturer SmPC hosted by BOT Plus](https://botplusweb.farmaceuticos.com/documentos/2013/1/16/54370.pdf): nine vitamins per tablet; does not include retinol or cyanocobalamin.

- Funsix registration 55439 has been withdrawn and current CIMA documents/REST are unavailable. The [archived manufacturer PIL-FOOD leaflet reproduced with registration 55439](https://www.botica.info/medicamentos/pil-food-capsulas) identifies the nine active ingredients and quantities; this is an archived composition, not current marketed-product verification. The previous vitamin A concept was unrelated.

- Esterofundina de Balance (47059) and Prothromplex (54938) are also no longer available through CIMA HTML/REST/PDF. The [archived manufacturer Esterofundina technical sheet](https://imedi.es/esterofundina-de-balance-solucion-para-perfusion/tecnica) and [archived Prothromplex leaflet](https://farmacic.com/medicamentos/prothromplex-600-ui-20-ml-polvo-y-disolvente-para-solucion-inyectable-54938) support conservative mappings. The Esterofundina leaflet potassium value has an internal typo (1.180 mg/mL versus 0.180 g/100 mL and 24.2 mmol/L); 1.8 mg/mL follows the consistent latter values. No exact mapping is asserted.

- Feiba 100 U/mL CN 764553 is the 1000 U vial despite the local des_dosific typo of 100 U. The labelled 25/50/100 U/mL formulations have distinct dilution volumes; total-vial potency concepts remain BROAD.


Removed stale mapping CN 763982 (registration 59755), absent from current source rows.


## Dialysis and hemofiltration review (2026-11-10)

134 rows / 57 registered formulation variants were reviewed. The source `data.tsv` hides the ingredients as `N/A (más de 4 PA)`, so primary product documents were used to reconstruct the composition. Post-mixing concentrations, rather than individual chamber concentrate strengths, drive the suggestions. Dihydrate/hexahydrate salts are represented as ionic calcium/magnesium equivalents in suggestions to avoid confusing hydrated and anhydrous masses.

Hecate standard and Extension searches were performed by brand and by complete ingredient strings. The higher-recall searches requested 30 results, using the same `search_standard` API as `find-concepts`; results were checked for unwanted ingredients, supplier/box packaging, route and units. No exact match to these Spanish compositions was established.

- Dianeal PD4, Balance and CAPD/DPCA: standard 40166942 (`875807`) preserves all five ingredients and the intraperitoneal form. The numeric Dianeal PD-2 concepts have implausibly tiny concentrations and the PD-2 brand is not PD4; they are unsuitable. Extension peritoneal concepts use different glucose/hydrated-salt/electrolyte concentrations.
- Physioneal 35/40 contains bicarbonate as well as lactate. Standard 40166942 is a five-of-six ingredient BROAD subset with correct peritoneal form. The former EXACT mappings to Dianeal PD-2 have wrong brand, glucose strength and buffer composition.
- Bicavera contains bicarbonate and no lactate. Extension 2936712 (`OMOP5153418`) preserves all five ingredients; its parenteral Injection form is a limitation explicitly recorded in each comment. It is BROAD, never EXACT. The former concepts introduced magnesium sulfate, potassium or phosphate, or lactate, which are absent.
- Extraneal and Polithera: clean Extension intraperitoneal full-combination forms 44096265 (`OMOP1090896`, matching Extraneal brand) and 44069055 (`OMOP1063686`, unbranded) improve the route representation. They remain BROAD because exact Spanish electrolyte strengths were not found. Standard 40238877 has an Injectable Solution form, not the source intraperitoneal form. A malformed duplicated segment in one old Extraneal concept_name is removed.
- Nutrineal PD4: Extension ingredient 588017 (`OMOP3138396`, Amino Acids) is a conservative route-neutral BROAD concept. The previous standard concept was an IV amino-acid/electrolyte nutrition combination containing sodium acetate rather than the source sodium lactate, and one Clear-Flex row incorrectly contained glucose. All 15 amino acids and four electrolytes are captured in suggestions. Lysine is labeled as hydrochloride in the original SmPC, and its mass is retained as that salt.
- Priosol, Accusol and Multibic: clean Extension full ingredient-set concepts 2936712/2936732 are preferred to wrong lactate/acetate-containing mixtures. For Multibic the matching brand 2936711/2936731 is retained because Extension was already necessary for the correct complete combination. All remain BROAD due to missing strengths and dialysis-specific form.
- Prismasol: 2936732 preserves six core ingredients but omits lactate. The previous strength-only concept 2936748 was wrong in concentration and omitted bicarbonate. Phoxilium: 35159107 (`OMOP4816091`) preserves calcium chloride, magnesium chloride, potassium chloride, bicarbonate and sodium chloride, omitting phosphate and containing no glucose or acetate. Biphozyl: standard 40161285 (`853456`) preserves magnesium chloride/bicarbonate/sodium chloride, omitting potassium/phosphate; it avoids the previous acetate/gluconate mix. Hemosol B0: the same standard subset avoids mapping to an individual concentrated chamber and preserves the final bicarbonate-based solution; calcium and lactate are omitted.
- Selutrio 40: the three-chamber system permits three final glucose/electrolyte formulations, so its suggestion is intentionally strengthless and the comment records the variable mixture. Original manufacturer SmPC: [Selutrio 40](https://botplusweb.farmaceuticos.com/documentos/2015/5/28/85344.pdf). The separate Selutrio 10 document has different calcium and must not substitute for 40.
- Nikkiso Formula E2 is discontinued and no accessible primary composition document was found. It remains BROAD with a strengthless full-combination suggestion and an explicit source limitation. Its previous tiny-strength replacement-fluid concept is not defensible. The four-ingredient representative subset is Extension 42957595 (`OMOP4684122`). Quantitative values from secondary registries were deliberately not used.

Primary AEMPS SmPCs were retrieved for the following registration numbers (section 2):

- [DIANEAL PD4 GLUCOSA 1,36% SOLUCION PARA DIALISIS PERITONEAL (60050)](https://cima.aemps.es/cima/dochtml/ft/60050/FT_60050.html)
- [DIANEAL PD4 GLUCOSA 2.27% SOLUCION PARA DIALISIS PERITONEAL (60051)](https://cima.aemps.es/cima/dochtml/ft/60051/FT_60051.html)
- [DIANEAL PD4 GLUCOSA 1,36 % CON SISTEMA DE DESCONEXION INTEGRADO SOLUCION PARA DIALISIS PERITONEAL (60053)](https://cima.aemps.es/cima/dochtml/ft/60053/FT_60053.html)
- [DIANEAL PD4 GLUCOSA 2,27 % CON SISTEMA DE DESCONEXION INTEGRADO SOLUCION PARA DIALISIS PERITONEAL (60054)](https://cima.aemps.es/cima/dochtml/ft/60054/FT_60054.html)
- [NUTRINEAL PD4 CON 1.1% AMINOACIDOS, SOLUCION PARA DIALISIS PERITONEAL (60384)](https://cima.aemps.es/cima/dochtml/ft/60384/FT_60384.html)
- [NUTRINEAL PD4 CON 1.1% DE AMINOACIDOS CON SISTEMA DE DESCONEXION INTEGRADO, SOLUCION PARA DIALISIS PERITONEAL (60386)](https://cima.aemps.es/cima/dochtml/ft/60386/FT_60386.html)
- [EXTRANEAL (ICODEXTRINA 7,5%) SOLUCION PARA DIALISIS PERITONEAL (61860)](https://cima.aemps.es/cima/dochtml/ft/61860/FT_61860.html)
- [CAPD/DPCA 2 SOLUCION PARA DIALISIS PERITONEAL (61886)](https://cima.aemps.es/cima/dochtml/ft/61886/FT_61886.html)
- [CAPD/DPCA 3  SOLUCION PARA DIALISIS PERITONEAL (61887)](https://cima.aemps.es/cima/dochtml/ft/61887/FT_61887.html)
- [CAPD/DPCA 4  SOLUCION PARA DIALISIS PERITONEAL (61888)](https://cima.aemps.es/cima/dochtml/ft/61888/FT_61888.html)
- [HEMOSOL B0 SOLUCION PARA HEMOFILTRACION Y HEMODIALISIS (62900)](https://cima.aemps.es/cima/dochtml/ft/62900/FT_62900.html)
- [PHYSIONEAL 40 GLUCOSA 3,86% P/V / 38,6 mg/ml  SOLUCION PARA DIALISIS PERITONEAL (63077)](https://cima.aemps.es/cima/dochtml/ft/63077/FT_63077.html)
- [PHYSIONEAL 40 GLUCOSA 1,36% P/V / 13,6 mg/ml SOLUCION PARA DIALISIS PERITONEAL (63078)](https://cima.aemps.es/cima/dochtml/ft/63078/FT_63078.html)
- [PHYSIONEAL 40 GLUCOSA 2,27% P/V / 22,7 mg/ml SOLUCION PARA DIALISIS PERITONEAL (63079)](https://cima.aemps.es/cima/dochtml/ft/63079/FT_63079.html)
- [CAPD/DPCA 17 SOLUCION PARA DIALISIS PERITONEAL (63233)](https://cima.aemps.es/cima/dochtml/ft/63233/FT_63233.html)
- [CAPD/DPCA 18 SOLUCION PARA DIALISIS PERITONEAL (63234)](https://cima.aemps.es/cima/dochtml/ft/63234/FT_63234.html)
- [CAPD/DPCA 19 SOLUCION PARA DIALISIS PERITONEAL (63235)](https://cima.aemps.es/cima/dochtml/ft/63235/FT_63235.html)
- [BICAVERA GLUCOSA 2,3%, Calcio 1,75 mmol/l SOLUCION PARA DIALISIS PERITONEAL (64754)](https://cima.aemps.es/cima/dochtml/ft/64754/FT_64754.html)
- [BICAVERA GLUCOSA 1,5%, Calcio 1,75 mmol/l SOLUCION PARA DIALISIS PERITONEAL (64755)](https://cima.aemps.es/cima/dochtml/ft/64755/FT_64755.html)
- [BICAVERA GLUCOSA  4,25%, Calcio 1,75 mmol/l SOLUCION PARA DIALISIS PERITONEAL (64756)](https://cima.aemps.es/cima/dochtml/ft/64756/FT_64756.html)
- [BALANCE 1,5 % GLUCOSA, 1,75 mmol/L DE CALCIO, SOLUCION PARA DIALISIS PERITONEAL (64979)](https://cima.aemps.es/cima/dochtml/ft/64979/FT_64979.html)
- [BALANCE 4,25 % GLUCOSA, 1,75  mmol/1 DE CALCIO, SOLUCION PARA DIALISIS PERITONEAL (64980)](https://cima.aemps.es/cima/dochtml/ft/64980/FT_64980.html)
- [BALANCE 2,3 % GLUCOSA, 1,75 mmol/L DE CALCIO, SOLUCION PARA DIALISIS PERITONEAL (64981)](https://cima.aemps.es/cima/dochtml/ft/64981/FT_64981.html)
- [BALANCE 4,25 % GLUCOSA, 1,25 mmol/L DE CALCIO, SOLUCION PARA DIALISIS PERITONEAL (64982)](https://cima.aemps.es/cima/dochtml/ft/64982/FT_64982.html)
- [BALANCE 1,5 % GLUCOSA, 1,25 mmol/L DE CALCIO, SOLUCION PARA DIALISIS PERITONEAL (64983)](https://cima.aemps.es/cima/dochtml/ft/64983/FT_64983.html)
- [BALANCE 2,3 % GLUCOSA, 1,25 mmol/L DE CALCIO, SOLUCION PARA DIALISIS PERITONEAL (64984)](https://cima.aemps.es/cima/dochtml/ft/64984/FT_64984.html)
- [PHYSIONEAL 35 GLUCOSA 1,36% P/V / 13,6 mg/ml SOLUCION PARA DIALISIS PERITONEAL (65759)](https://cima.aemps.es/cima/dochtml/ft/65759/FT_65759.html)
- [PHYSIONEAL 35 GLUCOSA 2,27% P/V / 22,7 mg/ml SOLUCION PARA DIALISIS PERITONEAL (65760)](https://cima.aemps.es/cima/dochtml/ft/65760/FT_65760.html)
- [PHYSIONEAL 35 GLUCOSA 3,86% P/V / 38,6 mg/ml SOLUCION PARA DIALISIS PERITONEAL (65761)](https://cima.aemps.es/cima/dochtml/ft/65761/FT_65761.html)
- [MULTIBIC  2 MMOL/L DE POTASIO SOLUCIÓN PARA HEMODIÁLISIS Y HEMOFILTRACIÓN (65804)](https://cima.aemps.es/cima/dochtml/ft/65804/FT_65804.html)
- [MULTIBIC  SIN POTASIO SOLUCIÓN PARA HEMODIÁLISIS Y HEMOFILTRACIÓN (65805)](https://cima.aemps.es/cima/dochtml/ft/65805/FT_65805.html)
- [MULTIBIC  3 MMOL/L DE POTASIO SOLUCIÓN PARA HEMODIÁLISIS Y HEMOFILTRACIÓN (65814)](https://cima.aemps.es/cima/dochtml/ft/65814/FT_65814.html)
- [MULTIBIC  4 MMOL/L DE POTASIO SOLUCIÓN PARA HEMODIÁLISIS Y HEMOFILTRACIÓN (65815)](https://cima.aemps.es/cima/dochtml/ft/65815/FT_65815.html)
- [PRISMASOL 2 mmol/l POTASIO, SOLUCION PARA HEMODIALISIS Y HEMOFILTRACION (65896)](https://cima.aemps.es/cima/dochtml/ft/65896/FT_65896.html)
- [PHYSIONEAL 40 GLUCOSA 1,36% P/V / 13,6 mg/ml CLEAR-FLEX SOLUCION PARA DIALISIS PERITONEAL (66306)](https://cima.aemps.es/cima/dochtml/ft/66306/FT_66306.html)
- [PHYSIONEAL 40 GLUCOSA 2,27% P/V / 22,7 mg/ml CLEAR-FLEX SOLUCION PARA DIALISIS PERITONEAL (66307)](https://cima.aemps.es/cima/dochtml/ft/66307/FT_66307.html)
- [PHYSIONEAL 35 GLUCOSA 1,36% P/V / 13,6 mg/ml CLEAR-FLEX SOLUCION PARA DIALISIS PERITONEAL (66308)](https://cima.aemps.es/cima/dochtml/ft/66308/FT_66308.html)
- [PHYSIONEAL 35 GLUCOSA 2,27% P/V / 22,7 mg/ml CLEAR-FLEX SOLUCION PARA DIALISIS PERITONEAL (66309)](https://cima.aemps.es/cima/dochtml/ft/66309/FT_66309.html)
- [PHYSIONEAL 35 GLUCOSA 3,86% P/V / 38,6 mg/ml CLEAR-FLEX SOLUCION PARA DIALISIS PERITONEAL (66310)](https://cima.aemps.es/cima/dochtml/ft/66310/FT_66310.html)
- [PHYSIONEAL 40 GLUCOSA 3,86% P/V / 38,6 mg/ml CLEAR-FLEX SOLUCION PARA DIALISIS PERITONEAL (66390)](https://cima.aemps.es/cima/dochtml/ft/66390/FT_66390.html)
- [PRIOSOL CON 4  mmol/L DE POTASIO SOLUCION PARA HEMOFILTRACION (67213)](https://cima.aemps.es/cima/dochtml/ft/67213/FT_67213.html)
- [PRIOSOL CON 2 mmol/L DE POTASIO SOLUCION PARA HEMOFILTRACION (67214)](https://cima.aemps.es/cima/dochtml/ft/67214/FT_67214.html)
- [PRIOSOL SIN POTASIO SOLUCION PARA HEMOFILTRACION (67215)](https://cima.aemps.es/cima/dochtml/ft/67215/FT_67215.html)
- [ACCUSOL 35 POTASIO 2 mmol/L SOLUCION PARA HEMOFILTRACION, HEMODIALISIS Y HEMODIAFILTRACION (67611)](https://cima.aemps.es/cima/dochtml/ft/67611/FT_67611.html)
- [ACCUSOL 35 POTASIO 4 mmol/L SOLUCION PARA HEMOFILTRACION, HEMODIALISIS Y HEMODIAFILTRACION (67612)](https://cima.aemps.es/cima/dochtml/ft/67612/FT_67612.html)
- [PHOXILIUM 1,2 mmol/L DE FOSFATO SOLUCION PARA HEMODIALISIIS/HEMOFILTRACION (71309)](https://cima.aemps.es/cima/dochtml/ft/71309/FT_71309.html)
- [PRISMASOL 4 mmol/L POTASIO SOLUCION PARA  HEMODIALISIS Y HEMOFILTRACION (71310)](https://cima.aemps.es/cima/dochtml/ft/71310/FT_71310.html)
- [BIPHOZYL SOLUCION PARA HEMODIALISIS/HEMOFILTRACION (79998)](https://cima.aemps.es/cima/dochtml/ft/79998/FT_79998.html)
- [BICAVERA GLUCOSA 2,3%, CALCIO 1,25 MMOL/L SOLUCION PARA DIALISIS PERITONEAL (81963)](https://cima.aemps.es/cima/dochtml/ft/81963/FT_81963.html)
- [BICAVERA GLUCOSA 1,5%, CALCIO 1,25 MMOL/L SOLUCION PARA DIALISIS PERITONEAL (81964)](https://cima.aemps.es/cima/dochtml/ft/81964/FT_81964.html)
- [BICAVERA GLUCOSA 4,25%, CALCIO 1,25 MMOL/L SOLUCION PARA DIALISIS PERITONEAL (81965)](https://cima.aemps.es/cima/dochtml/ft/81965/FT_81965.html)
- [POLITHERA (ICODEXTRINA 7,5 %) SOLUCIÓN PARA DIÁLISIS PERITONEAL (89184)](https://cima.aemps.es/cima/dochtml/ft/89184/FT_89184.html)

Nutrineal Clear-Flex (65535): [original manufacturer SmPC](https://botplusweb.farmaceuticos.com/documentos/2016/9/29/102642.pdf) confirms the same full composition as the other Nutrineal PD4 presentations.
Dianeal PD4 3.86% (60052/60055) retains the same PD4 electrolyte family and the source-labeled 38.6 mg/ml anhydrous glucose; the discontinued Spanish documents return 404.


## Miscellaneous combinations (reviewed 2026-11-10)

Source compositions were checked against AEMPS CIMA technical sheets, because the local `principios_activos`/strength fields describe only an unspecified combination. Hecate searches covered standard RxNorm and RxNorm Extension, with brand and translated ingredient/dose-form queries. Clean concepts without suppliers or box counts were selected. No full matching-strength concepts were found for the BROAD combinations below.

- [Pleinvue, 82959](https://cima.aemps.es/cima/dochtml/ft/82959/FT_82959.html): two sequential doses, with the second split across A/B sachets, exactly match the standard unbranded Plenvu two-dose pack (1510756/2045244). Existing MoviPrep concept has a different composition and strengths. Imported presentations with the same Pleinvue name follow the same clinical formulation. Preserved the unbranded standard pack because the US brand spelling differs.
- [VapoRub, 22051](https://cima.aemps.es/cima/dochtml/ft/22051/FT_22051.html): five active ingredients. The former EXACT US camphor/menthol concept omitted eucalyptus oil, turpentine and thymol, and had different strengths. Clean Extension 43133709/OMOP503685 preserves the full five-ingredient ointment, without strengths. Selected BROAD.
- [Iberogast, 75509](https://cima.aemps.es/cima/dochtml/ft/75509/FT_75509.html) has nine liquid botanical extracts. Selected strengthless nine-botanical Extension oral solution 2937080/OMOP5153790 [Iberogast]. The mass-based Extension strengths were not assumed equivalent to the labeled liquid-extract volume fractions. Plant-part and preparation terminology also differs, so BROAD. The imported Iberogast rows were mapped consistently by named formulation.
- [Iberogast Elemental, 88986](https://cima.aemps.es/cima/dochtml/ft/88986/FT_88986.html) contains six botanicals, with different proportions, and omits angelica, celandine and milk thistle. The former nine-botanical concept introduced absent ingredients. Selected clean three-component licorice/chamomile/peppermint oral-solution subset 41267373/OMOP2465335, BROAD, with the full six-botanical suggestion and preparation mismatch documented.
- [Imupret, 79944](https://cima.aemps.es/cima/dochtml/ft/79944/FT_79944.html): seven powdered plants, not echinacea. Full Extension candidates were rejected: some introduce oats instead of oak, while others misrepresent marshmallow root as flower, oak bark as nut, or powdered flowers as oil. Standard horsetail whole extract 44818471/1535478 is a conservative botanical ingredient subset; source preparation and omitted plants are explicit in the suggestion/comment.
- [DiurinAT, 61578](https://cima.aemps.es/cima/dochtml/ft/61578/FT_61578.html): birch, horsetail, corn silk and couch-grass dry extracts in an oral suspension. Former Iberogast concept was unrelated. Clean Extension horsetail oral solution retains one relevant botanical; BROAD records form and extract differences.
- [Tutukon, 82648](https://cima.aemps.es/cima/dochtml/ft/82648/FT_82648.html): aqueous combined distillate of eight plants, total 94.66 g/100 ml. Do not turn starting-herb masses into individual final-extract concentrations. Horsetail oral solution is BROAD; full botanical identity and total mixed-distillate amount are documented. Former eucalyptol ingredient was absent.
- [Agua del Carmen, 27454](https://cima.aemps.es/cima/dochtml/ft/27454/FT_27454.html): multi-herb distillate plus 15 essential oils, 3.75 ml mixed distillate per 5 ml dose. Clean melissa oral-solution Extension preserves route/form better than ingredient alone. Suggested complete botanical/oil identity deliberately does not misstate starting-plant weights as final extract concentrations.
- [Citorsal, 25093](https://cima.aemps.es/cima/dochtml/ft/25093/FT_25093.html): glucose, four electrolyte salts, calcium lactate, magnesium sulfate and citric acid; no polyethylene glycol. One sachet is constituted in 500 ml water. Suggestion quantities are per sachet (five times the composition per 100 ml). Clean four-ingredient Extension powder retains glucose/KCl/NaCl/sodium citrate; BROAD records four omitted components.
- [Clensia, 81575](https://cima.aemps.es/cima/dochtml/ft/81575/FT_81575.html): each paired A/B unit contains seven actives, including PEG4000 52.5 g, simethicone 80 mg and sodium sulfate 3.75 g. Extension three-component oral solution is a clinically meaningful subset, BROAD because other salts/citric acid and powder constitution are absent. Suggestion gives the paired A/B powder quantities.
- [Rinobanedif, 41402](https://cima.aemps.es/cima/dochtml/ft/41402/FT_41402.html): neomycin and prednisolone plus bacitracin, phenylephrine, chlorobutanol and standardized eucalyptus/niaouli oils. Standard neomycin/prednisolone topical ointment retains two principal actives. Nasal route and omitted components remain explicit in the BROAD suggestion/comment. Oil quantities are variable ranges standardized to cineole; no false exact fixed oil strength is assigned.
- Cinodio: archived [technical sheet](https://imedi.es/cinodio-comprimidos-recubiertos), manufacturer Laboratorios ERN text (registration printed 48.219 although local source row is 49218), confirms caffeine, thiamine, pyridoxine, cyanocobalamin, folic acid and glutamine. Existing vitamin B complex tablet retained BROAD, with omitted caffeine/glutamine and full suggestion. Live CIMA documents for the local registration were unavailable; this is the archived named-brand composition, not an independently verified current registration document.
- [Ruscus Llorens, 45946](https://cima.aemps.es/cima/dochtml/ft/45946/FT_45946.html): dibucaine, prednisolone, zinc oxide, ruscogenin and levomenthol. Standard dibucaine/prednisolone rectal ointment remains BROAD; 0.0019 mg/mg prednisolone concepts do not match the 0.0015 mg/mg source.
- [Dertrase official archived leaflet](https://cima.aemps.es/cima/pdfs/p/32935/Prospecto_32935.pdf), also [manufacturer leaflet mirror](https://farmaciajimenez.com/storage/products/dertrase-pomada-40-g/Prospecto-Dertrase-pomada.pdf): chymotrypsin and trypsin plus nitrofurazone, RNA hydrolysate, carglumic acid, methionine and inositol. The former papain-containing mapping introduced an absent ingredient. Clean chymotrypsin ointment Extension is BROAD, with all omitted components recorded. Source concentrations follow the leaflet per 100 g composition.
- [Frenadol Complex, 49269](https://cima.aemps.es/cima/dochtml/ft/49269/FT_49269.html): acetaminophen 650 mg, chlorpheniramine maleate 4 mg, dextromethorphan HBr 20 mg, caffeine citrate 30 mg and ascorbic acid 250 mg per sachet. Standard first-three-ingredient powder is BROAD. Former pheniramine/phenylephrine combination was wrong. Source specifically labels caffeine citrate; suggestion retains that salt.
- [Rinomicine tablets, 42550](https://cima.aemps.es/cima/dochtml/ft/42550/FT_42550.html), [coated tablets, 48578](https://cima.aemps.es/cima/dochtml/ft/48578/FT_48578.html), [sachets, 56526](https://cima.aemps.es/cima/dochtml/ft/56526/FT_56526.html): each is a distinct multi-ingredient strength pattern. Use strengthless acetaminophen/chlorpheniramine/phenylephrine tablet or powder subset, BROAD; no pheniramine substitution and no imported wrong strengths. Caffeine/salicylamide are omitted, plus vitamin C in sachets. Source sachets form a suspension, explicitly documented.
- [Propalgina Plus, 56999](https://cima.aemps.es/cima/dochtml/ft/56999/FT_56999.html): standard four-ingredient acetaminophen/chlorpheniramine/dextromethorphan/phenylephrine powder subset, BROAD for missing ascorbic acid and strengths.
- [Otocerum, 32103](https://cima.aemps.es/cima/dochtml/ft/32103/FT_32103.html): benzocaine/turpentine/chlorobutanol/phenol/castor oil; no antipyrine. Standard benzocaine otic solution BROAD.
- [Otogen Calmante, 46544](https://cima.aemps.es/cima/dochtml/ft/46544/FT_46544.html): tetracaine, phenol, menthol, clove oil and benzalkonium, with neither benzocaine nor antipyrine. Extension tetracaine otic solution BROAD retains the anesthetic and correct route.
- [Vinciseptil Otico, 50169](https://cima.aemps.es/cima/dochtml/ft/50169/FT_50169.html): fluocinolone, neomycin, polymyxin B, benzydamine and tetracaine. Clean three-ingredient Extension otic solution retains more clinically relevant ingredients than prior fluocinolone alone, BROAD for omitted components and strength.
- [Blasgina, 50441](https://cima.aemps.es/cima/dochtml/ft/50441/FT_50441.html): miconazole nitrate/metronidazole/neomycin/polymyxin B/Centella asiatica; no nystatin. Standard miconazole nitrate 100 mg vaginal insert retains matching strength/form, BROAD for the four omitted actives.
- [Radio Salil, 50101](https://cima.aemps.es/cima/dochtml/ft/50101/FT_50101.html): camphor, menthol, methyl salicylate, methyl nicotinate and salicylic acid. Standard first-three-ingredient cream subset BROAD, replacing a concept containing absent diethylamine salicylate and niacin.
- [Sinus, 41653](https://cima.aemps.es/cima/dochtml/ft/41653/FT_41653.html): eucalyptol, eucalyptus/pine/peppermint oils, menthol and camphor. Clean eucalyptus oil/menthol inhalant solution Extension preserves inhalation route and two ingredients, BROAD.
- [Anginovag, 37453](https://cima.aemps.es/cima/dochtml/ft/37453/FT_37453.html): dequalinium, enoxolone, hydrocortisone, lidocaine and tyrothricin. Standard lidocaine/tyrothricin lozenge retains two core actives, BROAD with spray/lozenge mismatch explicit. Former benzalkonium/hexylresorcinol/zinc chloride concept had no matching actives.
- [Bronquidiazina CR, 33618](https://cima.aemps.es/cima/dochtml/ft/33618/FT_33618.html): existing sulfamethoxazole/trimethoprim suspension retained BROAD; adds bromhexine/tolu balsam omissions and complete suggestion. Concentrations calculated from the labeled 7.5 ml dose.
- [Trutest 36, 85395](https://cima.aemps.es/cima/dochtml/ft/85395/FT_85395.html): 35 individual contact allergens/mixtures plus a negative control, supplied in three epicutaneous panels. No representative clinical drug/pack in standard or Extension searches for Trutest, T.R.U.E. Test and allergen patch test. Former Epicoccum mold extract is absent. NO_MAPPING is preferable to an arbitrary single allergen; suggestion lists the distinct patches and per-patch strengths in pack structure.


## Additional topical, probiotic, herbal and cough combinations (2026-11-10)

10 rows / 7 formulations. Hecate standard and Extension searches considered complete combinations, clinically representative subsets and matching forms. All mappings remain BROAD with full-combination suggestions.

- [Linimento Naion official SmPC](https://cima.aemps.es/cima/pdfs/ft/34157/FT_34157.pdf), section 2: per ml camphor 43 mg, menthol 48 mg, opodeldoc balsam 200 mg, salicylic acid 4.8 mg, turpentine 200 mg, methyl salicylate 8 mg, capsicum tincture 8 mg, rosemary tincture 16 mg and lavender tincture 16 mg. Source dose-form field says cutaneous liquid, but SmPC identifies pump spray. Clean Extension 36261771 (`OMOP3112646`) preserves all four core rubefacients and spray form, improving on standard three-ingredient spray/ointment subsets. Other components are explicitly omitted in comment.
- [Masagil solution official SmPC](https://cima.aemps.es/cima/pdfs/es/ft/902303/902303_ft.pdf), section 2: rosemary oil 9.06 mg/ml, methyl salicylate 23.62 mg/ml, turpentine 172.4 mg/ml, camphor 30 mg/ml, concentrated 30% ammonia solution 4.51 mg/ml; the SmPC separately gives actual ammonia as 0.124 g/100 ml (= 1.24 mg/ml), which is used in suggestion. No full combination found. Standard 1355869 (`2106100`, camphor/methyl salicylate Topical Solution) preserves two clinically central ingredients and form. Turpentine, rosemary oil and ammonia omission is explicit.
- [Masagil Spray official SmPC](https://cima.aemps.es/cima/pdfs/es/ft/57146/FT_57146.html.pdf), section 2: methyl salicylate 100 mg/ml, turpentine 100 mg/ml, camphor 40 mg/ml, menthol 40 mg/ml. Extension 36261771 is the full strengthless spray combination. No exact strengths found. Source `principios_activos` for 979807 duplicates camphor and omits menthol; source SmPC supports the same formulation as 971317. Comment records that source error. Source `data.tsv` has not been edited.
- [Pazbronquial official historical leaflet](https://cima.aemps.es/cima/pdfs/es/p/38575/P_38575.pdf), composition table: strengths are per 100 ml, converted to mg/ml. Codeine phosphate and ephedrine hydrochloride are each 1 mg/ml. Potassium guaiacolsulfonate is not guaifenesin. Standard 40146242 (`757226`, codeine/ephedrine Oral Solution) preserves both central cough/bronchodilator ingredients and form. Remaining expectorants, vitamins, menthol and botanical components are omitted with comment. Ethanol and sucrose are vehicle ingredients, excluded from ideal active combination.
- [Schoum original manufacturer leaflet](https://botplusweb.farmaceuticos.com/documentos/2003/11/17/17642.pdf), composition per 15 ml: melissa extract 75 mg, rhubarb 18 mg, fumaria 15 mg, boldo 7.5 mg, hamamelis 4.5 mg, hydrastis 3 mg, piscidia 3 mg, peppermint oil 6 mg. Converted to mg/ml. Standard RxNorm contains melissa extract ingredient but lacks matching oral solution. Extension 43656808 (`OMOP938017`, Melissa officinalis extract Oral Solution) adds clinically relevant form. Searches did not find a suitable complete botanical combination. Electrolyte salts listed as excipients in the original leaflet are excluded.
- [Tulgrasum original manufacturer leaflet](https://botplusweb.farmaceuticos.com/Documentos/2005/6/2/23584.pdf), composition per cm²: benzalkonium chloride 3.8 micrograms, benzyl benzoate 158.7 micrograms, threonine 15.8 micrograms, cysteine 35.6 micrograms, glycine 31.6 micrograms. Standard 40171646 (`899296`, benzalkonium Medicated Pad) preserves the antiseptic/dressing; four omitted actives are recorded. Suggestions retain per-area strengths in mg/cm² because source presentation rows do not identify patch dimensions; no unsupported mass per pad is inferred. Extension search did not expose the full five-component dressing.
- Salvacolon: original Spanish product is discontinued; accessible primary SmPC/leaflet was not found. [Catalan health-service medicines bulletin, 2006](https://scientiasalut.gencat.cat/bitstream/handle/11351/2409/BIT_2006_18_03_cas.pdf?isAllowed=y&sequence=2), table 1, confirms Salvacolon as a liquid Bacillus subtilis product. [Basque health-service INFAC bulletin, 2003](https://www.euskadi.eus/contenidos/informacion/cevime_infac_2003/es_def/adjuntos/infac_v11_n9.pdf), table 2, confirms Bacillus subtilis combined with vitamins. Standard 42898675 (`1311119`, Bacillus subtilis) preserves the principal probiotic without introducing oral-tablet/capsule or injectable forms. Remaining full combination is recorded as a strengthless suggestion. Historical secondary registries disagree over vitamin B12 form and quantitative per-unit interpretation; no unsupported strengths or cobalamin subtype are asserted. The ingredient-level mapping is supported by the official health-service bulletins; quantitative formulation remains a source limitation.


## Parenteral nutrition review — 2026-11-10

Reviewed all 140 presentations (74 registrations/formulations). The local source hides ingredient lists and strengths as “more than 4 active substances”, so mapping decisions were checked against section 2 of the official product information or the archived Spanish AEMPS leaflet. Different registrations were reviewed separately, rather than transferring the same high-strength amino-acid product across all brands.

### Mapping decisions

- Standard RxNorm was searched first; Extension searches followed when the full ingredient set or appropriate presentation was absent. A final strength-focused standard and Extension search was performed for each of the 74 formulations. Supplier and box-count concepts were rejected.
- Synthamin 17 without electrolytes (58197) matches standard concept 19131341 / RxCUI 801644 exactly: all 15 amino acid strengths agree; lysine hydrochloride 7.26 mg/mL is equivalent to lysine 5.8 mg/mL. Synthamin 17 with electrolytes (58196) uses the same strength-preserving concept as BROAD because the four added electrolyte components are absent.
- Remaining presentations use BROAD mappings. Several inherited EXACT rows had unrelated strengths or omitted glucose/lipids/electrolytes; those classifications were corrected. Suggestions state the complete source formulation and concentration. Some Extension combination names are truncated in the terminology source; no EXACT claim was inferred from a truncated constituent list.
- Clinimix concentrations in the component chambers are halved after mixing the equal-volume amino-acid and glucose chambers. The N9G15E label therefore gives glucose 75 mg/mL in the mixed solution, not 150 mg/mL.
- Smofkabiven amounts headed “corresponding to” for calcium chloride, magnesium sulfate, sodium acetate and zinc sulfate are anhydrous equivalents. Their names in suggestions reflect those equivalents; concentrations were also checked against the labelled mmol/L electrolyte totals. Finomel uses the explicitly stated hydrated salts.
- Numeta suggestions describe all three chambers activated. The optional two-chamber amino-acid/glucose-only solution has different concentrations.
- Glamin supplies glycine/glutamine and tyrosine as glycylglutamine and glycyltyrosine dipeptides; suggestions retain the actual dipeptides. Its BROAD concept represents the constituent amino acids.
- Pediaven G15/G20/G25 trace element and hydrate quantities were checked separately; G25 has different amounts. Oliclinomel N5-800E has glucose 100 mg/mL and potassium chloride 1.79 mg/mL.
- Nephramine has no retrievable current CIMA SmPC. Its restricted essential-amino-acid formulation is supported by the Spanish SEGHNP clinical nutrition monograph below; lysine is expressed as acetate and the small cysteine component is retained in the suggestion. It remains BROAD.

### Source documents by registration

| Registration | Formulation | Source |
|---|---|---|
| 67038 | NEPHROTECT SOLUCION PARA PERFUSION | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/67038/FT_67038.html) |
| 61211 | CLINIMIX N9G15E SOLUCION PARA PERFUSION | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/61211/FT_61211.html) |
| 61215 | CLINIMIX N12G20E SOLUCION PARA PERFUSION | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/61215/FT_61215.html) |
| 61218 | CLINIMIX N14G30E SOLUCION PARA PERFUSION | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/61218/FT_61218.html) |
| 61212 | CLINIMIX N12G20 SOLUCION PARA PERFUSION | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/61212/FT_61212.html) |
| 58192 | SYNTHAMIN 9 REFORMULADO SOLUCION PARA PERFUSION | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/58192/FT_58192.html) |
| 58193 | SYNTHAMIN 9 REFORMULADO SIN ELECTROLITOS SOLUCION PARA PERFUSION | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/58193/FT_58193.html) |
| 58194 | SYNTHAMIN 14 REFORMULADO SOLUCION PARA PERFUSION | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/58194/FT_58194.html) |
| 58195 | SYNTHAMIN 14 REFORMULADO SIN ELECTROLITOS SOLUCION PARA PERFUSION | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/58195/FT_58195.html) |
| 58197 | SYNTHAMIN 17 REFORMULADO SIN ELECTROLITOS SOLUCION PARA PERFUSION | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/58197/FT_58197.html) |
| 58196 | SYNTHAMIN 17 REFORMULADO SOLUCION PARA PERFUSION | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/58196/FT_58196.html) |
| 67054 | AMINOPLASMAL B.BRAUN 10% E SOLUCION PARA PERFUSION | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/67054/FT_67054.html) |
| 67055 | AMINOPLASMAL B.BRAUN 5% SOLUCION PARA PERFUSION | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/67055/FT_67055.html) |
| 67057 | AMINOPLASMAL B.BRAUN 10% SOLUCION PARA PERFUSION | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/67057/FT_67057.html) |
| 58115 | PRIMENE 10% SOLUCIÓN PARA PERFUSIÓN | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/58115/FT_58115.html) |
| 68639 | TAURAMIN 12,6% SOLUCION PARA PERFUSION | [Archived Spanish AEMPS leaflet](https://www.botica.info/medicamentos/tauramin-126-solucion-para-perfusion) |
| 70895 | SMOFKABIVEN CENTRAL EMULSION PARA PERFUSION | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/70895/FT_70895.html) |
| 70892 | SMOFKABIVEN SIN ELECTROLITOS CENTRAL EMULSION PARA PERFUSION | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/70892/FT_70892.html) |
| 70513 | SMOFKABIVEN PERIFERICO EMULSION PARA PERFUSION | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/70513/FT_70513.html) |
| 62985 | KABIVEN EMULSION PARA PERFUSION | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/62985/FT_62985.html) |
| 59737 | ISOPLASMAL G  SOLUCION PARA PERFUSION | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/59737/FT_59737.html) |
| 72062 | PERIOLIMEL N4E  EMULSION PARA PERFUSION | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/72062/FT_72062.html) |
| 72063 | OLIMEL N7E EMULSION PARA PERFUSION | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/72063/FT_72063.html) |
| 72065 | OLIMEL N9E EMULSION PARA PERFUSION | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/72065/FT_72065.html) |
| 72066 | OLIMEL N9 EMULSION PARA PERFUSION | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/72066/FT_72066.html) |
| 61491 | GLAMIN SOLUCION PARA PERFUSION | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/61491/FT_61491.html) |
| 63596 | KABIVEN PERIFERICO EMULSION PARA PERFUSION | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/63596/FT_63596.html) |
| 74019 | NUMETA  G16%E, EMULSION PARA PERFUSION | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/74019/FT_74019.html) |
| 74020 | NUMETA  G19%E, EMULSION PARA PERFUSION | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/74020/FT_74020.html) |
| 78871 | AMINOPLASMAL PAED 10% SOLUCION PARA PERFUSION | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/78871/FT_78871.html) |
| 78892 | AMINOPLASMAL B.BRAUN 15% SOLUCION PARA PERFUSION | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/78892/FT_78892.html) |
| 78950 | PEDIAVEN G15 SOLUCION PARA PERFUSION | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/78950/FT_78950.html) |
| 78951 | PEDIAVEN G20 SOLUCION PARA PERFUSION | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/78951/FT_78951.html) |
| 78952 | PEDIAVEN G25 SOLUCION PARA PERFUSION | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/78952/FT_78952.html) |
| 59964 | AMINOPLASMAL PO 12,5% SOLUCION PARA PERFUSION | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/59964/FT_59964.html) |
| 59965 | AMINOPLASMAL PO 10% SOLUCION PARA PERFUSION | [Archived Spanish AEMPS leaflet](https://www.botica.info/medicamentos/aminoplasmal-po-10-solucion-para-perfusion) |
| 81161 | NUMETA G13% E EMULSION PARA PERFUSION | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/81161/FT_81161.html) |
| 61214 | CLINIMIX N9G20E SOLUCION PARA PERFUSION | [Archived Spanish AEMPS leaflet](https://www.botica.info/medicamentos/clinimix-n9g20e-solucion-para-perfusion) |
| 61217 | CLINIMIX N14G30 SOLUCION PARA PERFUSION | [Archived Spanish AEMPS leaflet](https://www.botica.info/medicamentos/clinimix-n14g30-solucion-para-perfusion) |
| 82101 | OMEGAFLEX ESPECIAL SIN ELECTROLITOS EMULSION PARA PERFUSION | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/82101/FT_82101.html) |
| 82102 | OMEGAFLEX PERI EMULSION PARA PERFUSION | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/82102/FT_82102.html) |
| 82103 | OMEGAFLEX PLUS EMULSION PARA PERFUSION | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/82103/FT_82103.html) |
| 82104 | OMEGAFLEX ESPECIAL EMULSION PARA PERFUSION | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/82104/FT_82104.html) |
| 82263 | LIPOFLEX PERI EMULSION PARA PERFUSION EFG | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/82263/FT_82263.html) |
| 82264 | LIPOFLEX PLUS EMULSION PARA PERFUSION EFG | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/82264/FT_82264.html) |
| 82265 | LIPOFLEX SPECIAL EMULSION PARA PERFUSION EFG | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/82265/FT_82265.html) |
| 82266 | LIPOFLEX SPECIAL SIN ELECTROLITOS EMULSION PARA PERFUSION EFG | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/82266/FT_82266.html) |
| 82508 | SMOFKABIVEN EXTRA NITROGEN SIN ELECTROLITOS EMULSION PARA PERFUSION | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/82508/FT_82508.html) |
| 82509 | SMOFKABIVEN EXTRA NITROGEN EMULSION PARA PERFUSION | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/82509/FT_82509.html) |
| 83767 | SMOFKABIVEN LOW OSMO PERIFERICO EMULSION PARA PERFUSION | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/83767/FT_83767.html) |
| 83966 | FINOMEL EMULSION PARA PERFUSION | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/83966/FT_83966.html) |
| 83967 | FINOMEL PERI EMULSION PARA PERFUSION | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/83967/FT_83967.html) |
| 84205 | OLIMEL N12E  EMULSION PARA PERFUSION | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/84205/FT_84205.html) |
| 84398 | OLIMEL N12 EMULSION PARA PERFUSION | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/84398/FT_84398.html) |
| 59878 | VAMIN 18 SIN ELECTROLITOS SOLUCION PARA PERFUSION | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/59878/FT_59878.html) |
| 59885 | VAMIN 14 SIN ELECTROLITOS SOLUCION PARA PERFUSION | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/59885/FT_59885.html) |
| 59796 | FREAMINE HBC 6.9 % SOLUCION PARA PERFUSION | [Archived Spanish AEMPS leaflet](https://www.botica.info/medicamentos/freamine-hbc-69-solucion-para-perfusion) |
| 59798 | TROPHAMINE 6% SOLUCION PARA PERFUSION | [Archived Spanish AEMPS leaflet](https://www.botica.info/medicamentos/trophamine-6-solucion-para-perfusion) |
| 59628 | AMINOVEN INFANT 10% SOLUCION PARA PERFUSION | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/59628/FT_59628.html) |
| 59669 | AMINOSTERIL N-HEPA 8% SOLUCION PARA PERFUSION INTRAVENOSA | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/59669/FT_59669.html) |
| 59736 | AMINOPLASMAL L-12,5 SOLUCION PARA PERFUSION | [Archived Spanish AEMPS leaflet](https://www.botica.info/medicamentos/aminoplasmal-l-125) |
| 59755 | AMINOPLASMAL HEPA SOLUCION PARA PERFUSION | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/59755/FT_59755.html) |
| 65936 | TAURAMIN 8% , SOLUCION PARA PERFUSION | [Archived Spanish AEMPS leaflet](https://www.botica.info/medicamentos/tauramin-8-solucion-para-perfusion) |
| 65937 | TAURAMIN 10% , SOLUCION PARA PERFUSION | [Archived Spanish AEMPS leaflet](https://www.botica.info/medicamentos/tauramin-10-solucion-para-perfusion) |
| 62981 | AMINOVEN 10% SOLUCION PARA PERFUSION | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/62981/FT_62981.html) |
| 62982 | AMINOVEN  5% SOLUCION PARA PERFUSION | [Archived Spanish AEMPS leaflet](https://www.botica.info/medicamentos/aminoven-5-solucion-para-perfusion) |
| 62983 | AMINOVEN 15% SOLUCION PARA PERFUSION | [AEMPS SmPC, section 2](https://cima.aemps.es/cima/dochtml/ft/62983/FT_62983.html) |
| 62975 | AMINOVEN 3,5% GLUCOSA / ELECTROLITOS SOLUCION PARA PERFUSION | [Archived Spanish AEMPS leaflet](https://www.botica.info/medicamentos/aminoven-35-glucosa-electrolitos-solucion-para-perfusion) |
| 64355 | OLICLINOMEL N4-550E EMULSION PARA PERFUSION | [Archived Spanish AEMPS leaflet](https://www.botica.info/medicamentos/oliclinomel-n4-550e-emulsion-para-perfusion) |
| 56700 | NEPHRAMINE SOLUCION PARA PERFUSION | [SEGHNP monograph, table 4](https://www.seghnp.org/sites/default/files/2017-05/nutricion%20parenteral%20en%20pediatria.pdf) |
| 56770 | AMINOPLASMAL L-5 SOLUCION PARA PERFUSION | [Archived Spanish AEMPS leaflet](https://www.botica.info/medicamentos/aminoplasmal-l-5) |
| 56771 | AMINOPLASMAL L-10 SOLUCION PARA PERFUSION | [Archived Spanish AEMPS leaflet](https://www.botica.info/medicamentos/aminoplasmal-l-10) |
| 57045 | AMINOPLASMAL L-10 CON ELECTROLITOS SOLUCION PARA PERFUSION | [Archived AEMPS SmPC, section 2](https://botplusweb.farmaceuticos.com/documentos/2010/5/14/43047.pdf) |
| 64357 | OLICLINOMEL N5-800E EMULSION PARA PERFUSION | [Archived Spanish AEMPS leaflet](https://www.botica.info/medicamentos/oliclinomel-n5-800e-emulsion-para-perfusion) |

Archived leaflet pages reproduce historical AEMPS documents; they were used where current CIMA URLs returned 404. The historical source, not a different contemporary brand formulation, determines the suggestion.
