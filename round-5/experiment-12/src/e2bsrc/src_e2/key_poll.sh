#!/bin/bash
# Polls the run's OpenRouter key status via the proxy base URL every 10 min (free endpoint; never prints the key).
# Appends "UTC limit limit_remaining usage" to logs/key_poll.log. Runs for at most 36 polls (6 h).
cd "$(dirname "$0")/.."
for i in $(seq 1 36); do
  r=$(curl -s "$OPENROUTER_BASE_URL/key" -H "Authorization: Bearer $OPENROUTER_API_KEY" | python3 -c "import json,sys;d=json.load(sys.stdin)['data'];print(d.get('limit'), d.get('limit_remaining'), round(d.get('usage',0),3))" 2>/dev/null)
  echo "$(date -u +%H:%M:%S) $r" >> logs/key_poll.log
  sleep 600
done
