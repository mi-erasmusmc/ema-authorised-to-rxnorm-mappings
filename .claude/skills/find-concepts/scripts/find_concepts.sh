#!/usr/bin/env bash
set -euo pipefail

extension=false
queries=()
for arg in "$@"; do
  case "$arg" in
    --extension) extension=true ;;
    *) queries+=("$arg") ;;
  esac
done

if [[ ${#queries[@]} -eq 0 ]]; then
  echo "usage: find_concepts.sh [--extension] QUERY..." >&2
  exit 2
fi

if $extension; then
  vocab="RxNorm,RxNorm Extension"
else
  vocab="RxNorm"
fi

limit=5
git_root=$(git rev-parse --show-toplevel)
dose_forms_json="$git_root/.claude/skills/map-drugs/dose_form_lookup.json"

workdir=$(mktemp -d)
trap 'rm -rf "$workdir"' EXIT
seen_file="$workdir/seen"
rows_file="$workdir/rows"
dose_file="$workdir/dose_forms"
: > "$seen_file"
: > "$rows_file"
: > "$dose_file"
dose_lookup_file="$workdir/dose_lookup"
jq -r '.[] | [.name, (.name | ascii_downcase), .description] | @tsv' "$dose_forms_json" > "$dose_lookup_file"

resolve_full_name() {
  local rxcui="$1" payload name endpoint
  for endpoint in properties historystatus; do
    if ! payload=$(curl -fsS --max-time 10 "https://rxnav.nlm.nih.gov/REST/rxcui/${rxcui}/${endpoint}.json" 2>/dev/null); then
      continue
    fi
    if [[ "$endpoint" == "properties" ]]; then
      name=$(jq -r '.properties.name // empty' <<<"$payload")
    else
      name=$(jq -r '.rxcuiStatusHistory.attributes.name // empty' <<<"$payload")
    fi
    if [[ -n "$name" ]]; then
      printf '%s\n' "$name"
      return 0
    fi
  done
  return 1
}

record_dose_form() {
  awk -F '\t' -v concept="$1" '
    BEGIN { concept = tolower(concept) }
    index(concept, $2) { print $1 "\t" $3; exit }
  ' "$dose_lookup_file" >> "$dose_file"
}

for query in "${queries[@]}"; do
  payload=$(curl -fsS --max-time 20 --get \
    --data-urlencode "q=$query" \
    --data-urlencode "limit=$limit" \
    --data-urlencode "vocabulary_id=$vocab" \
    "https://hecate.pantheon-hds.com/api/search_standard")

  while IFS=$'\t' read -r cid name code; do
    [[ -z "${cid:-}" ]] && continue
    if grep -Fxq "$cid" "$seen_file"; then
      continue
    fi
    printf '%s\n' "$cid" >> "$seen_file"

    if [[ "$name" == *"..."* && "$code" != OMOP* ]]; then
      resolved=$(resolve_full_name "$code" || true)
      if [[ -n "${resolved:-}" ]]; then
        name="$resolved"
      fi
    fi

    record_dose_form "$name"
    printf '%s\t%s\t%s\n' "$cid" "$name" "$code" >> "$rows_file"
  done < <(jq -r '.[]?.concepts[]? | [.concept_id, .concept_name, .concept_code] | @tsv' <<<"$payload")
done

printf 'concept_id\tconcept_name\tconcept_code\n'
cat "$rows_file"

if [[ -s "$dose_file" ]]; then
  printf '\nDose form definitions:\n'
  sort -u "$dose_file" | while IFS=$'\t' read -r name desc; do
    printf '  %s: %s\n' "$name" "$desc"
  done
fi
