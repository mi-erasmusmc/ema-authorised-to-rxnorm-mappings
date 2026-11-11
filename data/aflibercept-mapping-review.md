# Aflibercept review — 2026-11-11

Reviewed the biosimilar reference and all local aflibercept presentations across EMA, Latvia and Spain, including the Eylea and Zaltrap originators.

| Source | Product folders | Final rows | EXACT | BROAD |
|---|---:|---:|---:|---:|
| EMA | 14 | 32 | 14 | 18 |
| Latvia | 14 | 28 | 14 | 14 |
| Spain | 1 | 17 | 8 | 9 |
| Total | 29 | 77 | 36 | 41 |

The reference now covers twelve authorised EU biosimilar brands and six FDA families. Added Eyluxvi and linked Baiama to Ahzantive/FYB203/aflibercept-mrbb. Normalised holder capitalisation. Skojoy was withdrawn before authorisation and is excluded. Evidence and reusable mapping guidance are in [aflibercept.sources.md](../.claude/skills/map-drugs/biosimilars/aflibercept.sources.md).

Mapping decisions:

- Preserve matching branded standard Eydenzelt, Opuviz, Pavblu, Ahzantive, Eylea and Zaltrap concepts. Spain's unbranded Eydenzelt and Opuviz rows now use the matching standard brands.
- Baiama vial now maps EXACT to unbranded aflibercept-mrbb Injection. Baiama syringe remains BROAD but now identifies mrbb, rather than plain aflibercept. Never use the different Ahzantive brand for Baiama.
- Ahzantive syringes now preserve the matching mrbb ingredient and delivered dose through the standard branded Injection as BROAD. No matching mrbb Prefilled Syringe was found. Opuviz syringes retain the same approach with yszy. Suggestions retain the correct syringe form.
- Yesafili previously mapped EXACT to plain aflibercept in EMA and Latvia. Changed to BROAD with jbvf suggestions: the FDA counterpart is established, but no matching jbvf concept was found. Afqlir remains BROAD with abzv suggestions for the same vocabulary gap.
- Mynzepli, Vgenfli and Eyluxvi previously had plain-aflibercept EXACT rows. These now use BROAD with brand-specific xxxx suggestions because no FDA counterpart was established. Afiveg and Eiyzey also use this policy.
- Added five missing Latvia mappings: Afiveg vial/syringe, Eiyzey vial/syringe, and Eyluxvi vial.
- Corrected Spain's fill-volume Extension mappings for Mynzepli and Ahzantive to the 0.05 mL delivered-dose standard concepts. Eiyzey and Afiveg concentration-only fallbacks now retain the delivered dose as well. These rows remain BROAD for the biosimilar or syringe gaps described above.
- Spain's high-dose Eylea syringe previously used `0.184 ML ... Injection` as EXACT. The syringe delivers 8 mg in 0.07 mL; the 0.184 mL is excess fill. Changed to the matching standard branded delivered-dose Injection as BROAD, with the missing Prefilled Syringe suggestion, consistent with EMA and Latvia. Eylea high-dose RxNorm uses rounded 114 MG/ML terminology for this 8 mg presentation.
- Zaltrap remains EXACT to the matching branded ziv-aflibercept concepts for its intravenous 4 mL/8 mL vials.

Changes affect fifty rows across twenty-three mapping files: thirty-eight rows have concept, type or suggestion changes (including five new rows); twelve only gain explanatory comments and review dates. EMA changes are recorded in each affected folder's `flag.tsv`.

Eight Latvia REVIEW_VOLUME flags were confirmed as false positives using labelled delivered doses rather than excess container fill. Added per-row suppressions and corresponding mapping comments for Eydenzelt, Pavblu, Baiama, Eylea, Ahzantive and Opuviz. No wildcard suppression was used.

Validation:

- All 29 mapping files pass structural validation; all source-folder checks pass except four pre-existing EMA NO_DATE warnings for undated `parsed_data.tsv` files (006339, 006150, 006438, 006607). The combined validator reports these source warnings with a nonzero exit status; they are not mapping errors.
- Reference rows have the expected five columns, and the EU-brand set exactly matches the twelve authorised biosimilars in the local EMA medicines report.
- Regenerated all three combined overview files. All 77 reviewed rows match their source mappings across concept ID/name/code, mapping type, comments, suggestions and review date.
- Standard and Extension searches found no matching jbvf/abzv concepts, mrbb/yszy syringes or dose-specific high-dose Eylea syringe. All retained branded standard concept identifiers were checked through Hecate.
- Whitespace validation passes with the repository's existing CRLF files accounted for.
