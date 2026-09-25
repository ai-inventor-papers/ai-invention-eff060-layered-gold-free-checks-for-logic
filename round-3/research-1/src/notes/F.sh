#!/bin/bash
# full-text fetch: F.sh <name> <url>
SKILL_DIR=../../../../tools/aii-web-tools
PY=$SKILL_DIR/../.ability_client_venv/bin/python
OUT=../notes/full/$1.md
echo "URL: $2 | FULL FETCH | $(date -u +%FT%TZ)" > $OUT
$PY $SKILL_DIR/scripts/aii_fast_web_fetch.py fetch --url "$2" --max-chars 400000 2>/dev/null >> $OUT
