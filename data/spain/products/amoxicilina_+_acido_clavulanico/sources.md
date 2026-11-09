# Mapping notes

Checked 2026-11-09 against `data.tsv` for the newly added sachet presentations.

- 770748: `des_nomco` and `des_dcp` agree on 250 mg amoxicillin / 62.5 mg clavulanate; `des_dosific` contains a conflicting 200 mg entry. The suggestion follows the agreeing product and clinical names.
- The 500 mg / 125 mg sachets and the 250 mg / 62.5 mg sachet are powders reconstituted as oral suspension, with no reconstitution volume in the source. Searches found no unambiguous concentration-based exact RxNorm concept, so use the combination Oral Suspension as BROAD rather than inventing a concentration. RxNorm Extension Oral Powder concepts are not used because that dose form is defined as powder taken orally without reconstitution into liquid.
