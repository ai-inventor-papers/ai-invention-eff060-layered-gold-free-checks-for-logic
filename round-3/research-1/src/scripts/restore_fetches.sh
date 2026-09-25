#!/bin/bash
# Re-fetch every page listed in notes/FETCH_INDEX.md into notes/full or notes/raw (same file names),
# so that `python3 notes/quotes.py` can re-verify the quote ledger. Web access + aii-web-tools skill required.
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_DIR=/ai-inventor/.claude/skills/aii-web-tools
PY=$SKILL_DIR/../.ability_client_venv/bin/python
mkdir -p "$ROOT/notes/full" "$ROOT/notes/raw"
grep -E '^\| 20' "$ROOT/notes/FETCH_INDEX.md" | while IFS='|' read -r _ ts file url mode _; do
  file=$(echo $file); url=$(echo $url); out="$ROOT/notes/$file"
  [ -s "$out" ] && continue
  echo "URL: $url | RESTORED FETCH | $(date -u +%FT%TZ)" > "$out"
  $PY $SKILL_DIR/scripts/aii_fast_web_fetch.py fetch --url "$url" --max-chars 400000 >> "$out" 2>/dev/null
done
