#!/bin/bash
# F-KEY: poll the shared OpenRouter key every 20 min (free GET /api/v1/key), log limit_remaining.
while true; do
  r=$(curl -s "$OPENROUTER_BASE_URL/key" -H "Authorization: Bearer $OPENROUTER_API_KEY" | python3 -c "import json,sys; d=json.load(sys.stdin)['data']; print(d.get('limit_remaining'), d.get('usage_daily'))" 2>&1)
  echo "$(date -u +%H:%M:%S) $r" >> logs/key_poll.log
  sleep 1200
done
