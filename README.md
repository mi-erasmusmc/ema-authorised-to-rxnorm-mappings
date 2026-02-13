# EMA Authorised Products to RxNorm Mapping

This repository contains mappings between European Medicines Agency (EMA) authorised medicinal products and RxNorm
standardized drug terminology codes, as well as Swedish and Latvian national product mappings.

**Disclaimer:** While ongoing efforts are made to ensure the accuracy and quality of these mappings, they may contain
errors or inaccuracies. Users should verify mappings for their specific use case and employ these data at their own
discretion and risk. The authors and contributors assume no liability for any consequences arising from the use of this
dataset.

## Datasets

### File: `ema-to-rxnorm.tsv`

- **Format**: Tab-separated values (TSV)
- **Size**: 16,824 mappings
- **Last Updated**: 2026-02-12

### File: `sweden_to_rxnorm.tsv`

- **Format**: Tab-separated values (TSV)
- **Size**: ~91,100 mappings
- **Last Updated**: 2026-01-18

Swedish national products are linked to EMA products via EU marketing authorization numbers where applicable.

### File: `latvia-to-rxnorm.tsv`

- **Format**: Tab-separated values (TSV)
- **Mapped**: 31,802, 
- **Unmapped**: 7,238
- **Last Updated**: 2026-02-05

Latvian national products mapped to RxNorm concepts.

### Source Data

Raw source data is available in the `data/` folder, including the EMA medicines report, per-product Authorised Presentations PDFs, and parsed packaging data.

Scripts, tooling, and instructions for processing data and mapping drugs to RxNorm live in the `skills/` folder. These can be loaded into your AI agent's skills directory (e.g., `.claude/skills/`).

See `data/README.md` for data details and `skills/` for processing and mapping instructions.

### Column Descriptions (`ema-to-rxnorm.tsv`)

| Column                       | Description                                                    |
|------------------------------|----------------------------------------------------------------|
| `ma_number`                  | Marketing authorization number (e.g., EU/1/95/001/005)         |
| `concept_id`                 | OMOP concept identifier                                        |
| `concept_name`               | Standardized drug concept name describing the product          |
| `concept_code`               | RxNorm concept code                                            |
| `mapping_type`               | Type of mapping relationship (EXACT, BROAD, INCORRECT)         |
| `ema_active_substance`       | Active substance from the EMA medicines report                 |
| `pdf_strength`               | Strength as listed in the Authorised Presentations PDF         |
| `pdf_pharmaceutical_form`    | Pharmaceutical form from the PDF                               |
| `pdf_route_of_administration`| Route of administration from the PDF                           |
| `pdf_packaging`              | Packaging description from the PDF                             |
| `pdf_content`                | Content description from the PDF                               |
| `pdf_pack_size`              | Pack size from the PDF                                         |
| `ema_name_of_medicine`       | Medicine name from the EMA medicines report                    |
| `ema_product_number`         | EMA product number (e.g., EMEA/H/C/000071)                    |
| `ema_atc_code`               | ATC code from the EMA medicines report                         |
| `comment`                    | Optional note explaining the mapping decision                  |
| `suggestion`                 | Ideal concept name when no exact match exists in RxNorm        |
| `last_updated_date`          | Date when this mapping was last verified or updated            |

### Mapping Types

- **EXACT**: Direct one-to-one correspondence between EMA product and RxNorm concept
- **BROAD**: RxNorm concept represents a broader category than the specific EMA product
- **INCORRECT**: Mapping flagged as incorrect (pending review or correction)

## License

### Mapping Data

The mappings in `ema-to-rxnorm.tsv` are licensed
under [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/).

### Source Data

Please refer to the applicable licenses for source data:

- EMA data: [EMA Legal Notice](https://www.ema.europa.eu/en/about-us/about-website/legal-notice)
- RxNorm terminology: [RxNorm Terms of Service](https://www.nlm.nih.gov/research/umls/rxnorm/docs/termsofservice.html)

### RxNorm Attribution

This product uses publicly available data courtesy of the U.S. National Library of Medicine (NLM), National Institutes
of Health, Department of Health and Human Services; NLM is not responsible for the product and does not endorse or
recommend this or any other product.

### Expansion Plans

The project currently includes mappings for EMA centrally authorized products, Swedish national products, and Latvian national products. Plans are underway to expand coverage to additional EU member states.

## Contributing

Contributions are very welcome! Please open an issue or pull request in this repository.

## Acknowledgments

This data was created using publicly available information about drugs and their presentations from the EMA website. The
mappings were generated using an LLM based mapping tool (still to be made available) and extensive manual curation.

Creating this mapping was funded by Erasmus Medical Center Department of Informatics.
