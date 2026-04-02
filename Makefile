# Usage: make <target> [ARGS="..."]
# Example: make validate_spain_folder ARGS="data/spain/products/12345/ --details"

.SILENT:
PYTHON = python3

# ── Spain ──────────────────────────────────────────────────────────────────────
validate_spain:
	$(PYTHON) .claude/skills/map-spain-drugs/validate_all.py $(ARGS)

apply_mappings:
	$(PYTHON) .claude/skills/map-spain-drugs/apply_mappings.py $(ARGS)

find_duplicate_nros:
	$(PYTHON) .claude/skills/map-spain-drugs/scripts/find_duplicate_nros.py $(ARGS)

list_folder_patterns:
	$(PYTHON) .claude/skills/map-spain-drugs/scripts/list_folder_patterns.py $(ARGS)

run_clean_room_batch:
	$(PYTHON) .claude/skills/map-spain-drugs/scripts/run_clean_room_batch.py $(ARGS)

download_spain_nomenclator:
	$(PYTHON) data/spain/download_aemps.py $(ARGS)

split_spain_by_ingredient:
	$(PYTHON) data/spain/split_by_ingredient.py $(ARGS)

list_spain_changes:
	$(PYTHON) data/spain/changed_products.py $(ARGS)

fetch_spain_pdf:
	$(PYTHON) data/spain/fetch_pdf.py $(ARGS)

update_spain_data: download_spain_nomenclator split_spain_by_ingredient

download_zva:
	$(PYTHON) data/latvia/download_zva.py $(ARGS)

deduplicate_latvia:
	$(PYTHON) data/latvia/deduplicate_data_files.py $(ARGS)

# ── EMA ────────────────────────────────────────────────────────────────────────
validate_ema:
	$(PYTHON) .claude/skills/map-ema-drugs/validate_all.py $(ARGS)

find_unmapped:
	$(PYTHON) .claude/skills/map-ema-drugs/find_unmapped.py $(ARGS)

generate_ema_info:
	$(PYTHON) .claude/skills/process-ema-data/scripts/generate_ema_info.py $(ARGS)

find_missing_files:
	$(PYTHON) .claude/skills/process-ema-data/scripts/find_missing_files.py $(ARGS)

list_pdfs_by_date:
	$(PYTHON) .claude/skills/process-ema-data/scripts/list_pdfs_by_date.py $(ARGS)

prepare_parse_batch:
	$(PYTHON) .claude/skills/process-ema-data/scripts/prepare_parse_batch.py $(ARGS)

fetch_ema_updates:
	$(PYTHON) .claude/skills/process-ema-data/scripts/fetch_ema_updates.py $(ARGS)

download_ema_presentation_files:
	$(PYTHON) .claude/skills/process-ema-data/scripts/download_ema_presentation_files.py $(ARGS)

# ── Latvia ─────────────────────────────────────────────────────────────────────
validate_latvia:
	$(PYTHON) .claude/skills/map-latvia-drugs/validate_all.py $(ARGS)

organize_products:
	$(PYTHON) .claude/skills/process-latvia-data/scripts/organize_products.py $(ARGS)

fill_missing_latvian_mappings:
	$(PYTHON) scripts/fill-missing-latvian-mappings.py $(ARGS)

# ── General ────────────────────────────────────────────────────────────────────
find_concepts:
	$(PYTHON) .claude/skills/find-concepts/scripts/find_concepts.py $(ARGS)

resolve_rxcui_name:
	$(PYTHON) .claude/skills/find-concepts/scripts/resolve_rxcui_name.py $(ARGS)

validate_mapping:
	$(PYTHON) .claude/skills/map-drugs/validate_mapping.py $(ARGS)

find_conflicts:
	$(PYTHON) .claude/skills/resolve-conflicts/scripts/find_conflicts.py $(ARGS)

apply_mapping:
	$(PYTHON) scripts/apply_mapping.py $(ARGS)

show_unmapped:
	$(PYTHON) scripts/show_unmapped.py $(ARGS)

sync_mappings:
	$(PYTHON) scripts/sync-mappings.py $(ARGS)

generate_mapping_overviews:
	$(PYTHON) scripts/generate_mapping_overviews.py $(ARGS) & echo "OK"

# ── DB load ────────────────────────────────────────────────────────────────────
load_ema:
	./load-ema-to-rxnorm.sh

load_latvia:
	./load-latvia-to-rxnorm.sh

load_spain:
	./load-spain-to-rxnorm.sh

.PHONY: validate_spain apply_mappings find_duplicate_nros \
        list_folder_patterns run_clean_room_batch \
        download_spain_nomenclator split_spain_by_ingredient list_spain_changes \
        fetch_spain_pdf update_spain_data \
        validate_ema find_unmapped generate_ema_info find_missing_files list_pdfs_by_date \
        prepare_parse_batch fetch_ema_updates download_ema_presentation_files \
        validate_latvia organize_products fill_missing_latvian_mappings find_concepts \
        resolve_rxcui_name validate_mapping find_conflicts apply_mapping \
        show_unmapped sync_mappings generate_mapping_overviews \
        load_ema load_latvia load_spain
