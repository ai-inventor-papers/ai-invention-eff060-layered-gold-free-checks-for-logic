#!/bin/bash
# Re-launch the resumable API job whenever the shared OpenRouter key has budget again (checks every 5 min).
cd "$(dirname "$0")/.."
export NLTK_DATA=$PWD/data/nltk_data
while true; do
  export OPENROUTER_API_KEY="$(cat /ai-inventor/aii_data/.secrets/openrouter_key.private)"
  rem=$(curl -s "${OPENROUTER_BASE_URL%/}/key" -H "Authorization: Bearer $OPENROUTER_API_KEY" | .venv/bin/python -c "import json,sys; print(json.load(sys.stdin)['data'].get('limit_remaining'))" 2>/dev/null)
  echo "$(date -u +%H:%M:%S) key remaining: $rem" >> logs/key_monitor.log
  if .venv/bin/python -c "import sys; sys.exit(0 if float('$rem') > 0.4 else 1)" 2>/dev/null; then
    echo "$(date -u +%H:%M:%S) launching run_api_E" >> logs/key_monitor.log
    .venv/bin/python src/run_api_E.py --phases disg,orig,l3disg,rest >> logs/run_api_E_2.out 2>&1
  fi
  if [ -f logs/api_done.flag ]; then exit 0; fi
  sleep 120
done
