#!/bin/bash
# Resume after the run-budget stop (HTTP 403 aii_run_budget_exhausted at 11:39 UTC). Solver labels already exist for all
# 400 sentences (work/sentences.json = all 400, so E's frozen panel_run can index every labelled sentence); the panel is
# restricted to batches 1..b with the frozen --only option, so batches still complete end to end in hash order.
cd "$(dirname "$0")/.."
PY=.venv/bin/python
WS=..
START=${START:-1}
$PY src_e2b/activate_e2b.py --upto 8
for b in $(seq $START 8); do
  if [ $(date -u +%H%M) -ge 1538 ]; then echo "DEADLINE: last paid call 15:38 UTC reached before batch $b"; break; fi
  echo "=== batch $b start $(date -u +%T)"
  EST=$($PY src_e2b/batch_estimate.py)
  OK=$($PY -c "import sys;sys.path.insert(0,'src_e2b');import budget;print(budget.can_start($EST))")
  if [ "$OK" != "True" ]; then echo "BUDGET STOP before batch $b (estimate $EST)"; echo "{\"budget_stop_before_batch\": $b, \"estimate\": $EST}" > $WS/e2b/budget_stop.json; break; fi
  $PY -c "import json;s=json.load(open('$WS/e2b/sentences_E2B.json'));json.dump([x['sentence_id'] for x in s if x['e2b_batch']<=$b],open('work/only_upto_$b.json','w'))"
  $PY src_e2/e.py run_label.py --kind heldout --budget 8 --workers ${LABEL_WORKERS:-3}
  export AII_HARD_CAP=$($PY -c "import sys;sys.path.insert(0,'src_e2b');import budget;d=budget.spent_by_file();print(round(d['e2bsrc/cost_ledger.jsonl']+budget.remaining()-budget.RESERVE,4))")
  $PY src_e2b/pe.py panel_run.py --kind heldout --members P3,R1 --cap 4.6 --only work/only_upto_$b.json
  $PY src_e2b/quarantine_errors.py panel_heldout.jsonl
  if [ -f $WS/e2b/api_blocked.flag ]; then echo "API blocked during batch $b: stopping (batch $b incomplete, excluded)"; break; fi
  $PY src_e2b/pe.py panel_run.py --kind heldout --members P3,R1 --adjudicate P1 --cap 1.9
  $PY src_e2b/quarantine_errors.py panel_heldout_adj.jsonl
  if [ -f $WS/e2b/api_blocked.flag ]; then echo "API blocked during batch $b: stopping (batch $b incomplete, excluded)"; break; fi
  $PY src_e2b/pe.py src_e2/repair.py --cap 1.0
  $PY src_e2/e.py run_label.py --kind heldout --refs work/reference_overrides.json --out labels_heldout_repaired.jsonl --budget 8 --workers ${LABEL_WORKERS:-3}
  $PY src_e2b/batch_progress.py --batch $b
  echo "=== batch $b done $(date -u +%T)"
done
echo "=== resume driver exit $(date -u +%T)"
