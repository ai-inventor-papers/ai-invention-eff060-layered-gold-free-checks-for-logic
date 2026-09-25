#!/bin/bash
# E2-B labels, batch by batch in hash order, each batch completed end to end:
#   solver labels -> [wait for drift decision] -> panel stage 1 (P3,R1) -> P1 adjudication -> reference repair -> repaired labels.
# Frozen scripts run on the CUMULATIVE set (work/sentences.json = batches 1..b); they are resumable and skip done sentences.
# Before each batch: budget check (estimate from actuals; stop if estimate > remaining - reserve).
cd "$(dirname "$0")/.."
PY=.venv/bin/python
WS=..
START=${START:-1}
while ! grep -q "=== gen done" ../logs/gen_all.log; do echo "waiting for generation $(date -u +%T)"; sleep 30; done
for b in $(seq $START 8); do
  echo "=== batch $b start $(date -u +%T)"
  EST=$($PY src_e2b/batch_estimate.py)
  OK=$($PY -c "import sys;sys.path.insert(0,'src_e2b');import budget;print(budget.can_start($EST))")
  if [ "$OK" != "True" ]; then echo "BUDGET STOP before batch $b (estimate $EST)"; echo "{\"budget_stop_before_batch\": $b, \"estimate\": $EST}" > $WS/e2b/budget_stop.json; break; fi
  $PY src_e2b/activate_e2b.py --upto $b
  $PY src_e2/e.py run_label.py --kind heldout --budget 8 --workers ${LABEL_WORKERS:-3}
  while [ ! -f $WS/e2b/drift_decision.json ]; do echo "waiting for drift decision $(date -u +%T)"; sleep 60; done
  export AII_HARD_CAP=$($PY -c "import sys;sys.path.insert(0,'src_e2b');import budget;import json;d=budget.spent_by_file();print(round(d['e2bsrc/cost_ledger.jsonl']+budget.remaining()-budget.RESERVE,4))")
  echo "AII_HARD_CAP for E2 scripts: $AII_HARD_CAP"
  $PY src_e2b/pe.py panel_run.py --kind heldout --members P3,R1 --cap 4.6
  $PY src_e2b/pe.py panel_run.py --kind heldout --members P3,R1 --adjudicate P1 --cap 1.9
  $PY src_e2b/pe.py src_e2/repair.py --cap 1.0
  $PY src_e2/e.py run_label.py --kind heldout --refs work/reference_overrides.json --out labels_heldout_repaired.jsonl --budget 8 --workers ${LABEL_WORKERS:-3}
  $PY src_e2b/batch_progress.py --batch $b
  echo "=== batch $b done $(date -u +%T)"
done
echo "=== all batches done $(date -u +%T)"
