#!/bin/bash
# full-text fetch: F.sh <name> <url>
SKILL_DIR=/ai-inventor/.claude/skills/aii-web-tools
PY=$SKILL_DIR/../.ability_client_venv/bin/python
OUT=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_research_1/notes/full/$1.md
echo "URL: $2 | FULL FETCH | $(date -u +%FT%TZ)" > $OUT
$PY $SKILL_DIR/scripts/aii_fast_web_fetch.py fetch --url "$2" --max-chars 400000 2>/dev/null >> $OUT
