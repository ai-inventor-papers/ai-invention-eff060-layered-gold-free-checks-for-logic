#!/bin/bash
# E2-A label chain (frozen dataset-4 protocol; drift PASS). Solver labels on all 550, then the panel in sha1-ordered
# prefixes of 110 sentences (stage 1 P3+R1, then P1 adjudication of disagreements), then reference repair + relabel.
set -e
cd "$(dirname "$0")/.."
export AII_HARD_CAP=9.5
export AII_PROVIDER_PIN="$(cat src_e2a/pin.json)"
PY=.venv/bin/python
R="$PY src_e2/e.py"
$PY src_e2a/order.py 0
$R run_label.py --kind heldout --budget 8 --workers 40
echo "$(date -u +%T) SOLVER_LABELS_DONE" >> logs_e2a/progress.log
for N in 110 220 330 440 550; do
  $PY src_e2a/order.py $N
  $R panel_run.py --kind heldout --members P3,R1 --cap 4.6
  $R panel_run.py --kind heldout --members P3,R1 --adjudicate P1 --cap 1.9
  echo "$(date -u +%T) PANEL_PREFIX_DONE $N" >> logs_e2a/progress.log
done
$PY src_e2a/order.py 0
$PY src_e2/repair.py --cap 1.0
$R run_label.py --kind heldout --refs work/reference_overrides.json --out labels_heldout_repaired.jsonl --budget 8 --workers 40
echo "$(date -u +%T) LABELS_DONE" >> logs_e2a/progress.log
