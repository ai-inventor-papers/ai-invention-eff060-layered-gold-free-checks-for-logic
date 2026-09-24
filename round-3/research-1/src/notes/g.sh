#!/bin/bash
# usage: g.sh <outname> <url> <pattern> [maxmatches]
SKILL_DIR=/ai-inventor/.claude/skills/aii-web-tools
PY=$SKILL_DIR/../.ability_client_venv/bin/python
OUT=../notes/raw/$1.txt
echo "URL: $2 | PATTERN: $3 | $(date -u +%FT%TZ)" > $OUT
$PY $SKILL_DIR/scripts/aii_fast_web_fetch.py grep --url "$2" --pattern "$3" --max-matches ${4:-40} --context-chars 300 -i >> $OUT 2>&1
