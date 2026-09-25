#!/bin/bash
# F-KEY recovery: poll the (possibly replaced) key every 3 min; when it has budget, run the planned API arms, then re-analyse.
export PYTHONHASHSEED=0
cd "$(dirname "$0")"
KF=/ai-inventor/aii_data/.secrets/openrouter_key.private
while true; do
  rem=$(curl -s "$OPENROUTER_BASE_URL/key" -H "Authorization: Bearer $(cat $KF)" | python3 -c "import json,sys; print(json.load(sys.stdin)['data'].get('limit_remaining') or 0)" 2>/dev/null)
  echo "$(date -u +%H:%M:%S) remaining=$rem" >> logs/api_chain.log
  python3 -c "import sys; sys.exit(0 if float('${rem:-0}') > 3 else 1)" && break
  sleep 180
done
run() { echo "$(date -u +%H:%M:%S) START $*" >> logs/api_chain.log; OPENROUTER_API_KEY="$(cat $KF)" .venv/bin/python method.py "$@" >> logs/api_chain_stages.log 2>&1; echo "$(date -u +%H:%M:%S) END $* rc=$?" >> logs/api_chain.log; }
run --stage judges --which cheap_disg,cheap2_disg
run --stage judges --which cheap_orig,cheap2_orig
run --stage verbalise
run --stage sc_gen
run --stage sc_score --which sc5_samples
run --stage strong --limit 20
run --stage strong
run --stage b2_read_api
run --stage b2_gate_report --which b2,b2api
run --stage retest
run --stage nli --which api
run --stage s4
run --stage analysis
.venv/bin/python tests/audit_E.py > logs/api_chain_audit.log 2>&1
echo "$(date -u +%H:%M:%S) API CHAIN DONE" >> logs/api_chain.log
