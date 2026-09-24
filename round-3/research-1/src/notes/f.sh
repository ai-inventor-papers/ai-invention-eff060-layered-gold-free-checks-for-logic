#!/bin/bash
# usage: f.sh <outname> <url> [maxchars] [offset]
SKILL_DIR=/ai-inventor/.claude/skills/aii-web-tools
PY=$SKILL_DIR/../.ability_client_venv/bin/python
OUT=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_research_1/notes/raw/$1.txt
echo "URL: $2 | FETCH | $(date -u +%FT%TZ)" > $OUT
$PY $SKILL_DIR/scripts/aii_fast_web_fetch.py fetch --url "$2" --max-chars ${3:-12000} --char-offset ${4:-0} >> $OUT 2>&1
