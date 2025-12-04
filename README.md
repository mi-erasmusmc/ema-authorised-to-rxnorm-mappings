# EMA Authorised Products to RxNorm Mapping

This repository contains mappings between European Medicines Agency (EMA) authorised medicinal products and RxNorm
standardized drug terminology codes.

**Disclaimer:** While ongoing efforts are made to ensure the accuracy and quality of these mappings, they may contain
errors or inaccuracies. Users should verify mappings for their specific use case and employ these data at their own
discretion and risk. The authors and contributors assume no liability for any consequences arising from the use of this
dataset.

## Dataset

### File: `ema-to-rxnorm.tsv`

- **Format**: Tab-separated values (TSV)
- **Size**: ~16,790 mappings
- **Last Updated**: 2025-12-04

Raw source data is available in the `source_data/` folder, including:

- `medicines_output_medicines_en.xlsx`: EMA medicines database
- `parsed_pdf_data.tsv`: Parsed pharmaceutical product information
- `ema_pdfs/`: Collection of EMA authorized presentations PDFs

### Column Descriptions

| Column                  | Description                                                                                 |
|-------------------------|---------------------------------------------------------------------------------------------|
| `product_number`        | EMA product number (e.g., EMEA/H/C/000071)                                                  |
| `ma_number`             | Marketing authorization number (e.g., EU/1/95/001/005)                                      |
| `concept_name`          | Standardized drug concept name describing the product                                       |
| `concept_id`            | OMOP concept identifier                                                                     |
| `concept_class_id`      | Classification of the drug concept (Clinical Drug, Branded Drug, Quant Clinical Drug, etc.) |
| `vocabulary_id`         | Source vocabulary (RxNorm or RxNorm Extension)                                              |
| `rxcui`                 | RxNorm Concept Unique Identifier                                                            |
| `mapping_type`          | Type of mapping relationship (EXACT, BROAD)                                                 |
| `suggestion_or_comment` | Additional notes or context for the mapping                                                 |
| `last_updated_date`     | Date when this mapping was last verified or updated                                         |

### Mapping Types

- **EXACT**: Direct one-to-one correspondence between EMA product and RxNorm concept
- **BROAD**: RxNorm concept represents a broader category than the specific EMA product

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

## Contributing

Contributions are very welcome! Please open an issue or pull request in this repository.

## Acknowledgments

This data was created using publicly available information about drugs and their presentations from the EMA website. The
mappings were generated using an LLM based mapping tool (still to be made available) and extensive manual curation.

Creating this mapping was funded by Erasmus Medical Center Department of Informatics.
