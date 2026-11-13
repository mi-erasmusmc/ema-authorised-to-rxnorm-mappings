# Humira syringe presentation verification

Reviewed 2026-11-13.

The Spanish Ministry of Health's [CIPM 214 agreements, page 13](https://www.sanidad.gob.es/areas/farmacia/precios/comisionInteministerial/acuerdosNotasInformativas/docs/ACUERDOS_DE_LA_CIPM_214_web.pdf) lists national codes 722390 and 722391 as Humira 40 mg prefilled syringes containing 0.4 ml (one and six syringes respectively).

This agrees with `des_nomco`, `envase` and `unidad_contenido` in data.tsv. Their `des_dcp` incorrectly describes a pen. Map both to the 0.4 ML adalimumab 100 MG/ML Prefilled Syringe [Humira] concept, rather than the Auto-Injector concept. Source data is retained as supplied.
