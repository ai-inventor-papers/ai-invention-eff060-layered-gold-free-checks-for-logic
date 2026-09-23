#!/bin/bash
# Wait until the shared OpenRouter key has daily budget again (polls every 10 min, no billing), then run ./run_all.sh.
# Usage: nohup ./watch_and_run.sh [max_seconds] > logs/watch.log 2>&1 &
cd "$(dirname "$0")"
end=$(( $(date +%s) + ${1:-86400} ))
while [ $(date +%s) -lt $end ]; do
  rem=$(curl -s -m 20 https://openrouter.ai/api/v1/key -H "Authorization: Bearer $OPENROUTER_API_KEY" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['limit_remaining'])" 2>/dev/null)
  echo "$(date -u +%FT%TZ) remaining=${rem:-?}"
  if [ -n "$rem" ] && python3 -c "import sys; sys.exit(0 if float('$rem') >= 3.0 else 1)"; then
    ./run_all.sh; rc=$?
    [ $rc -eq 0 ] && exit 0
  fi
  sleep 600
done
