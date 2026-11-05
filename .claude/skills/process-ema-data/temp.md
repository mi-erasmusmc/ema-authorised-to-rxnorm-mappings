   - Filename: `parsed_data_<today>.tsv`
   - Header row with all column names
   - One row per product presentation
   - Tab delimiters, no trailing tabs or spaces

## Example

**Input PDF content:**
```
MA (EU) number: EU/1/23/1727/001
(Invented) name: BEKEMV
Strength: 300 mg
Pharmaceutical Form: Concentrate for solution for infusion
Route of Administration: Intravenous use
Immediate Packaging: vial (glass)
Content (concentration): 30 ml (10 mg/ml)
Pack size: 1 vial
```

**Output TSV:**
```
ma_number	ema_product_number	strength	pharmaceutical_form	route_of_administration	packaging	content	pack_size	product_name
EU/1/23/1727/001	EMEA/H/C/005652	300 mg	Concentrate for solution for infusion	Intravenous use	vial (glass)	30 ml (10 mg/ml)	1 vial	BEKEMV
```

## Footnote Handling

Some PDFs use footnote markers in the Strength column (e.g. `--15`, `--16`) whose definitions appear as multi-line blocks later in the PDF. When this occurs:

1. Write the **marker + reference** in the strength column: e.g. `--15 see footnote.txt`
   - **Always keep the marker** — it is the only link between the TSV row and the correct footnote entry.
2. Create `footnote.txt` in the same product folder with the full footnote text exactly as it appears in the PDF.

Short, simple footnotes (a single phrase that fits naturally in the cell) can be inlined directly without creating footnote.txt.

**Example strength column values:**
- Elaborate multi-line: `--15 see footnote.txt`
- Simple inline: `30 micrograms/dose`