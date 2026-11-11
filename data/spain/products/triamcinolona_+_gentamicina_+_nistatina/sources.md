# Interderm mapping evidence

Reviewed 2026-11-11.

The source presentation is Interderm cream: gentamicin 1 mg/g, nystatin 100,000 units/g, and triamcinolone acetonide 1 mg/g. The principios_activos nystatin unit of mg is inconsistent with the units/g in des_dcp and des_dosific.

Standard RxNorm and RxNorm Extension searches for the three-ingredient combination and Interderm did not identify a matching concept. The BROAD mapping retains nystatin/triamcinolone cream and omits gentamicin. The suggestion preserves the full gram-based composition.

[DailyMed nystatin/triamcinolone acetonide cream label](https://www.dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=ea065dd4-dfd3-46a2-92de-8a0b49cb9455) describes 100,000 nystatin units and 1 mg triamcinolone acetonide per gram. Its RxNorm table links the gram-based product to RxCUI 1053753, whose SCD name uses 100000 UNT/ML and 1 MG/ML. This supports the selected cream subset without assuming a density conversion.

Four stale Positon rows (694117, 694125, 694133, 694141) were removed from this folder. All four source presentations and their reviewed mappings already exist in the triamcinolona_+_neomicina_+_nistatina folder.
