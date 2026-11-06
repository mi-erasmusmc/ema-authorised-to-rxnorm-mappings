# Barium sulfate mapping rationale

Reviewed 2026-11-06 using Hecate searches in standard RxNorm, then RxNorm Extension.
Standard RxNorm returned the ingredient only. Extension returned clean oral
suspension and enema concepts, including a 50 mg/mL oral suspension. Searches for
the source powder strengths, 830 mg/mL, and powder for oral suspension did not
return matching clinical drugs. Powder for Oral Solution is unsuitable for these
insoluble suspensions.

- [ROVI TAC SmPC, sections 2–4.2](https://cima.aemps.es/cima/dochtml/ft/81945/FT_81945.html):
  the supplied 150 mL oral suspension contains 7.5 g (50 mg/mL). Map EXACT to
  43150289, Barium Sulfate 50 MG/ML Oral Suspension (OMOP487632). The subsequently
  diluted administration concentration is not the labeled product strength.
- [Barilux concentrate SmPC, sections 2–4.2](https://cima.aemps.es/cima/dochtml/ft/73287/FT_73287.html):
  both packs contain a 50 mg/mL concentrate, authorized for oral and rectal use.
  Map BROAD to 43194387, Barium Sulfate 50 MG/ML (OMOP487630), retaining strength
  without asserting a ready-to-use oral suspension. Concentrate form and routes
  are not captured. The 8000 mL source row is a pack quantity, not a single dose.
- [Barilux powder SmPC](https://cima.aemps.es/cima/dochtml/ft/73154/FT_73154.html):
  764.32 g active ingredient per powder container, with oral and rectal use.
  The oral suspension concept represents only the prepared oral formulation.
- [Barigraf rectal powder SmPC, sections 2–4.2](https://cima.aemps.es/cima/dochtml/ft/57393/FT_57393.html):
  555.2 g per container; different reconstitution concentrations are authorized.
  Use the strength-free enema concept BROAD for rectal powders rather than
  assigning a single arbitrary concentration. The suggestion's 555200 MG is
  mass per powder/enema unit, not an MG/ML concentration.
- [Barigraf TAC SmPC](https://cima.aemps.es/cima/dochtml/ft/73640/FT_73640.html):
  each sachet contains 10 g and must be reconstituted. The oral suspension concept
  is BROAD because it omits the powder form and unit strength.

Other oral powders likewise use the strength-free oral suspension concept BROAD,
with the source unit strength retained in suggestions. The 830 mg/mL dual-route
suspension uses that concept BROAD, with the omitted strength and route recorded.
No foreign brand, mismatched strength, supplier, or box concept was substituted.
