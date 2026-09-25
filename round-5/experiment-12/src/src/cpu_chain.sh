#!/bin/bash
# CPU-side label-free scoring, niced so the label batches keep priority: waits for the L3 questionnaires, then
# exp-5 pool scoring (V0, PT features), local structural features, eval-2 pairwise matrix, M1 variants.
cd "$(dirname "$0")/.."
PY=exp5src/.venv/bin/python
while ! grep -q "L3 ok" logs/score_e2b.log 2>/dev/null; do sleep 20; done
nice -n 10 $PY src/score_e2b.py pool --workers ${POOL_WORKERS:-2}
nice -n 10 $PY src/score_e2b.py local
nice -n 10 $PY src/pairwise_e2b.py matrix --workers ${MX_WORKERS:-2}
$PY src/pairwise_e2b.py variants
echo "=== cpu chain done $(date -u +%T)"
