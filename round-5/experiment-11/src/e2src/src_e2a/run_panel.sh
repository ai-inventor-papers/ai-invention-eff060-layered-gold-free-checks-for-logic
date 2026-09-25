#!/bin/bash
# E2-A panel in sha1-ordered prefixes (solver labels already done on all 550; work/sentences.json = all 550).
set -e
cd "$(dirname "$0")/.."
export AII_HARD_CAP=9.5
export AII_PROVIDER_PIN="$(cat src_e2a/pin.json)"
PY=.venv/bin/python
R="$PY src_e2/e.py"
$PY src_e2a/order.py 0
for N in 110 220 330 440 550; do
  $PY src_e2a/labels_prefix.py $N
  $R panel_run.py --kind heldout --members P3,R1 --cap 4.6 --labels labels_heldout_prefix.jsonl
  $R panel_run.py --kind heldout --members P3,R1 --adjudicate P1 --cap 1.9 --labels labels_heldout_prefix.jsonl
  echo "$(date -u +%T) PANEL_PREFIX_DONE $N" >> logs_e2a/progress.log
done
$R panel_run.py --kind heldout --members P3,R1 --cap 4.6
$R panel_run.py --kind heldout --members P3,R1 --adjudicate P1 --cap 1.9
echo "$(date -u +%T) PANEL_FULL_DONE" >> logs_e2a/progress.log
$PY src_e2/repair.py --cap 1.0
$R run_label.py --kind heldout --refs work/reference_overrides.json --out labels_heldout_repaired.jsonl --budget 8 --workers 24
echo "$(date -u +%T) LABELS_DONE" >> logs_e2a/progress.log
