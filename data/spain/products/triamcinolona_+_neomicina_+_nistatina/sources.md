# Positon mapping evidence

Reviewed 2026-11-06.

The Spain source contains 30 g and 60 g packs of cream and ointment, each labeled in the clinical presentation as neomycin 2.5 mg/g, nystatin 100,000 units/g and triamcinolone acetonide 1 mg/g.

Standard RxNorm and RxNorm Extension searches for Positon and the complete three-ingredient combination did not return a matching concept. Four-ingredient neomycin/nystatin/thiostrepton/triamcinolone products were rejected because they introduce thiostrepton. The selected BROAD fallbacks retain nystatin and triamcinolone acetonide, their strengths and the source dose form; neomycin is omitted and explicitly recorded in each comment and full-combination suggestion.

## Cream strength convention

[DailyMed nystatin/triamcinolone acetonide cream label](https://www.dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=ea065dd4-dfd3-46a2-92de-8a0b49cb9455) describes 100,000 nystatin units and 1 mg triamcinolone acetonide per gram. Its RxNorm table links that product to RxCUI 1053753, whose name uses 100000 UNT/ML and 1 MG/ML. This supports choosing that terminology concept as the cream subset without assuming a physical density conversion.

## Selected concepts

- Cream: OMOP 40234727 / RxCUI 1053753, `nystatin 100000 UNT/ML / triamcinolone acetonide 1 MG/ML Topical Cream`.
- Ointment: OMOP 40234705 / RxCUI 1053697, `nystatin 100 UNT/MG / triamcinolone acetonide 0.001 MG/MG Topical Ointment`. The per-mg values are equivalent to 100,000 units/g and 1 mg/g.

Pack mass does not change the concentration-level topical mapping.
