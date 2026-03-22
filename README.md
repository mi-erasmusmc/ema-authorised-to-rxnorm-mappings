# EMA Authorised Products to RxNorm Mapping

Mappings between European Medicines Agency (EMA) centrally authorised medicinal products and RxNorm/OMOP standardized
drug concepts, along with Spanish and Latvian national product mappings. To our knowledge, these are the first
comprehensive publicly available mappings of all EMA authorised products to OMOP standard concepts.

## Datasets

| File | Mappings                        | Last Updated |
|------|---------------------------------|--------------|
| `ema-to-rxnorm.tsv` | 16,553                         | 2026-03-16 |
| `spain-to-rxnorm.tsv` | 30,069                       | 2026-03-16 |
| `latvia-to-rxnorm.tsv` | 33,123 mapped, 5,826 unmapped | 2026-03-22 |

Because EMA centrally authorised products are valid across all EU member states, these mappings can serve as a
foundation or cross-reference for country-specific drug vocabulary mappings throughout Europe. Spanish and Latvian
national products are linked to EMA products via EU marketing authorization numbers where applicable.

Each mapping is classified as **EXACT** (direct correspondence) or **BROAD** (RxNorm concept is broader than the
specific product). Raw source data is available in `data/`. See [Column Descriptions](#column-descriptions) below for
full schema details.

---

## Architecture

This repository is also a methodological experiment: it demonstrates a skill-based, file-driven knowledge architecture
for LLM-assisted vocabulary mapping that replaces traditional application infrastructure with a structured workspace
accessible to off-the-shelf coding agents.

### Why Not Just Ask an LLM?

Mapping source drug vocabularies to OMOP standardized concepts remains a labour-intensive task in observational
research. A naive approach to LLM-assisted mapping — decompose each drug entry into its parts, perform semantic
search against RxNorm, and ask the LLM to pick the best candidate — works for straightforward formulations but fails
for a significant proportion of products. RxNorm encodes domain-specific conventions that cannot be reliably resolved
by string similarity and LLM reranking alone: the distinction between various "injectables", base vs. salt weight
conversions, whether an inhaler's dose is metered or actuated, or selecting the correct biosimilar suffix. Resolving
these cases requires providing the LLM with additional context not available in a simple drug name string.

### Skills, Not Software

Rather than building a traditional application or custom agent pipeline, this project externalizes domain knowledge as
files — instruction documents, scripts, reference materials, and curated context — organized in a Git repository. The
emerging class of coding agents (Claude Code, Codex, Open Code, etc.) already provide file system access, script
execution, sub-agent orchestration, and context management out of the box. Instead of reimplementing these capabilities
in custom code, we leverage them directly: the researcher's effort goes into **curating domain knowledge that can be
transferred to the LLM as a skill**, rather than building infrastructure.

Each **skill** is a self-contained directory containing an instruction file for the LLM, processing scripts, and
references to external resources the agent can access on demand. Skills are agent-agnostic — they can be loaded into
any coding agent's skill directory regardless of the underlying LLM provider.

```
.claude/
  skills/                   # Skill definitions
    map-ema-drugs/          #   EMA mapping skill with RxNorm conventions
    map-latvia-drugs/       #   Latvia national product mapping skill
    find-concepts/          #   Semantic search against RxNorm via Hecate API
    process-ema-data/       #   PDF parsing and data extraction
    resolve-conflicts/      #   Cross-dataset conflict resolution
  agents/                   # Agent definitions
data/
  ema/products/             # Per-product folders with parsed data and context
  latvia/products/          # Latvian product data
  spain/products/           # Spanish product data
```

### Just-in-Time Context Loading

LLMs have a finite attention budget: as context length grows, model accuracy degrades, and token usage has a direct
cost. Instead of loading all reference material upfront, the architecture follows a **just-in-time context loading**
strategy: the agent retrieves only the context needed for the case at hand. Per-product folders contain parsed source
data, and the agent loads relevant reference documents (SmPCs, RxNorm conventions, prior mapping decisions) only when
needed for complex cases.

### Tiered Mapping Strategy

The mapping process follows a tiered strategy designed around the observation that most drugs are easy to map but a
long tail of complex products requires disproportionate effort:

1. **Tier 1 — Bulk processing**: Scripts decompose drug entries, perform semantic search against RxNorm, and have
   the LLM select the best match from a shortlist. This handles most simple formulations (predominantly oral tablets
   and capsules) efficiently at minimal token cost.

2. **Tier 2 — Context-assisted reasoning**: Cases that fail or produce low-confidence matches are handled with
   selectively loaded context. The agent reads relevant reference documents and applies clinical reasoning to resolve
   ambiguities, writing its mappings and reasoning directly to output files — a form of structured note-taking that
   persists knowledge outside the context window and enables human review.

## Limitations

- Risk of silent mapping errors inherent to LLM-generated output
- Significant token costs for complex cases requiring extensive context
- Approximately 2,000 mappings have been manually verified; systematic evaluation across the full dataset remains
  future work

## Using the Skills

Skills and agents live in `.claude/skills/` and `.claude/agents/`. This is the convention used by
[Claude Code](https://docs.anthropic.com/en/docs/claude-code), but the skills themselves are agent-agnostic — each
skill is just a directory containing an instruction file, scripts, and references. They can be adapted to any coding
agent that supports custom instructions:

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code/skills) — uses `.claude/skills/` natively
- [GitHub Copilot](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/create-skills) — reads `.claude/skills/` natively (also supports `.github/skills/`)
- [OpenAI Codex](https://developers.openai.com/codex/skills/) — copy to `.agents/skills/`
- [OpenCode](https://opencode.ai/docs/skills/) — reads `.claude/skills/` natively (also supports `.opencode/skills/` and `.agents/skills/`)

## Column Descriptions

Columns in `ema-to-rxnorm.tsv` (other files follow similar conventions):

| Column                        | Description                                             |
|-------------------------------|---------------------------------------------------------|
| `ma_number`                   | Marketing authorization number (e.g., EU/1/95/001/005)  |
| `concept_id`                  | OMOP concept identifier                                 |
| `concept_name`                | Standardized drug concept name describing the product   |
| `concept_code`                | RxNorm concept code                                     |
| `mapping_type`                | Type of mapping relationship (EXACT, BROAD)             |
| `ema_active_substance`        | Active substance from the EMA medicines report          |
| `pdf_strength`                | Strength as listed in the Authorised Presentations PDF  |
| `pdf_pharmaceutical_form`     | Pharmaceutical form from the PDF                        |
| `pdf_route_of_administration` | Route of administration from the PDF                    |
| `pdf_packaging`               | Packaging description from the PDF                      |
| `pdf_content`                 | Content description from the PDF                        |
| `pdf_pack_size`               | Pack size from the PDF                                  |
| `ema_name_of_medicine`        | Medicine name from the EMA medicines report             |
| `ema_product_number`          | EMA product number (e.g., EMEA/H/C/000071)              |
| `ema_atc_code`                | ATC code from the EMA medicines report                  |
| `comment`                     | Optional note explaining the mapping decision           |
| `suggestion`                  | Ideal concept name when no exact match exists in RxNorm |
| `last_updated_date`           | Date when this mapping was last verified or updated     |

## License

The mapping files are licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). For source
data licenses, see [EMA Legal Notice](https://www.ema.europa.eu/en/about-us/about-website/legal-notice) and
[RxNorm Terms of Service](https://www.nlm.nih.gov/research/umls/rxnorm/docs/termsofservice.html).

This product uses publicly available data courtesy of the U.S. National Library of Medicine (NLM), National Institutes
of Health, Department of Health and Human Services; NLM is not responsible for the product and does not endorse or
recommend this or any other product.

## Contributing

Contributions are welcome. Please open an issue or pull request.

## Acknowledgments

Created using publicly available information from the EMA website and national drug registries. The mappings were
generated using the skill-based LLM architecture described above with extensive manual curation.

Funded by Erasmus Medical Center Department of Informatics.

**Disclaimer:** These mappings may contain errors or inaccuracies. Users should verify mappings for their specific
use case. The authors assume no liability for any consequences arising from use of this dataset.
