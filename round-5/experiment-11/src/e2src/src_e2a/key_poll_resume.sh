#!/bin/bash
# Poll the run key every 15 min (plan fallback RUN-BUDGET 402/403). When >= $0.50 remains: resume the paid chain
# (panel prefixes -> API judges -> repair/relabel). Cached calls are never re-billed. Log: logs_e2a/key_poll.log
cd "$(dirname "$0")/.."
WS=$(cd .. && pwd)
while true; do
  R=$(curl -s -m 30 -H "Authorization: Bearer $OPENROUTER_API_KEY" "${OPENROUTER_BASE_URL%/}/key")
  REM=$(echo "$R" | python3 -c "import sys,json;d=json.load(sys.stdin)['data'];print(d.get('limit_remaining'))" 2>/dev/null)
  LIM=$(echo "$R" | python3 -c "import sys,json;d=json.load(sys.stdin)['data'];print(d.get('limit'))" 2>/dev/null)
  echo "$(date -u +%FT%TZ) limit=$LIM remaining=$REM" >> logs_e2a/key_poll.log
  if python3 -c "import sys; sys.exit(0 if float('${REM:-0}' or 0) >= 0.5 else 1)" 2>/dev/null; then
    echo "$(date -u +%FT%TZ) RESUME" >> logs_e2a/key_poll.log
    bash src_e2a/run_panel.sh > logs_e2a/panel_resume.log 2>&1 &
    (cd "$WS" && PYTHONHASHSEED=0 OPENBLAS_NUM_THREADS=1 env/.venv/bin/python scoring/api_judges.py --stage judges --concurrency 24 > logs/chain_api_resume.log 2>&1)
    wait
    echo "$(date -u +%FT%TZ) RESUME_DONE" >> logs_e2a/key_poll.log
    exit 0
  fi
  sleep 900
done
