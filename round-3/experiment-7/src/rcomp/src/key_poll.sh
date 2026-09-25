#!/bin/bash
# Poll the shared OpenRouter key's remaining daily budget every 5 min (no billing); log to logs/key_status.log.
cd "$(dirname "$0")/.."
end=$(( $(date +%s) + ${1:-20000} ))
while [ $(date +%s) -lt $end ]; do
  r=$(curl -s -m 20 "${OPENROUTER_BASE_URL%/}/key" -H "Authorization: Bearer $OPENROUTER_API_KEY" | python3 -c "import sys,json; d=json.load(sys.stdin)['data']; print(d['limit_remaining'], d['usage_daily'])" 2>/dev/null)
  echo "$(date -u +%FT%TZ) $r" >> logs/key_status.log
  sleep 300
done
