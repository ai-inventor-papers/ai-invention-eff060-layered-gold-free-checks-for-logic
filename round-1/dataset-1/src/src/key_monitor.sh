#!/bin/bash
# Polls the shared OpenRouter key every 5 min; appends limit_remaining to logs/key_monitor.log
for i in $(seq 1 60); do
  r=$(curl -s https://openrouter.ai/api/v1/key -H "Authorization: Bearer $OPENROUTER_API_KEY" | python3 -c "import json,sys;d=json.load(sys.stdin)['data'];print(d['limit_remaining'], round(d['usage_daily'],2))" 2>/dev/null)
  echo "$(date -u +%H:%M:%S) $r" >> logs/key_monitor.log
  sleep 300
done
