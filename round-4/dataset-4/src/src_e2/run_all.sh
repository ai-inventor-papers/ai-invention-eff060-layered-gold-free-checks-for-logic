#!/bin/bash
# E2 end-to-end, in execution order. Every step is resumable (append-only raw files, per-sentence skip, panel cache
# never re-bills). Steps 0-2 are $0 and already executed; the LLM steps need the run's OpenRouter budget.
# Spend stop: AII_HARD_CAP (cumulative cost_ledger.jsonl) = 9.5.
set -e
cd "$(dirname "$0")/.."
PY=.venv/bin/python
export AII_HARD_CAP=${AII_HARD_CAP:-9.5}
R="$PY src_e2/e.py"
# --- $0 steps ---------------------------------------------------------------------------------------------
# $PY src_e2/select_e2.py && $PY src_e2/prereg_e2.py                            # step 1-2 (frozen; do not rerun)
# --- step 3: panel drift check (fresh cache) -------------------------------------------------------------
$R gate.py --mode synthetic --members P1,P3,R1 --cap 0.30
$R gate.py --mode trackh --members P1,P3,R1 --cap 0.50
$PY src_e2/drift_report.py
PASS=$($PY -c "import json;print(json.load(open('panel_drift_E2.json'))['passes'])")
# --- step 4: pilot (30 sentences; work/sentences.json = pilot) -------------------------------------------
cp work/sentences_pilot.json work/sentences.json
$R generate.py --slots G1,G1b,G2,G3,G4,G5,G6,G7,G8,G9 --variants fewshot_v1 --sentences work/sentences_pilot.json --cap 1.3
$PY src_e2/gen_retry.py --sentences work/sentences_pilot.json --concurrency 3
$R run_label.py --kind heldout --budget 8 --workers 4
if [ "$PASS" = "True" ]; then
  $R panel_run.py --kind heldout --members P1,P3,R1 --cap 4.6                   # pilot: all three raters (E's 5c)
fi
$PY src_e2/pilot_projection.py
# --- step 5-6: full generation + solver labels ----------------------------------------------------------
$PY src_e2/activate_full.py
$R generate.py --slots G1,G1b,G2,G3,G4,G5,G6,G7,G8,G9 --variants fewshot_v1 --sentences work/sentences.json --cap 1.3
$PY src_e2/gen_retry.py --sentences work/sentences.json --concurrency 4
$R run_label.py --kind heldout --budget 8 --workers 4
# --- step 7: panel (frozen protocol) ---------------------------------------------------------------------
if [ "$PASS" = "True" ]; then
  $R panel_run.py --kind heldout --members P3,R1 --cap 4.6                      # 7a/7c stage 1, full class coverage
  $R panel_run.py --kind heldout --members P3,R1 --adjudicate P1 --cap 1.9      # stage 2 (disagreements)
  $PY src_e2/repair.py --cap 1.0                                                  # 7b reference repair
  $R run_label.py --kind heldout --refs work/reference_overrides.json --out labels_heldout_repaired.jsonl --budget 8
fi
# --- steps 7d-12 ($0) ------------------------------------------------------------------------------------
$PY src_e2/assemble_e2.py
$PY src_e2/controls_e2.py
$PY src_e2/testability_e2.py
$PY src_e2/seal_e2.py && $PY src_e2/verify_seal.py
$PY data.py
$PY src_e2/card_e2.py
