#!/bin/bash
set -e
cd "$(dirname "$0")/.."
export AII_HARD_CAP=9.5
export AII_PROVIDER_PIN="$(cat src_e2a/pin.json)"
PY=.venv/bin/python
$PY src_e2/e.py gate.py --mode synthetic --members P1,P3,R1 --cap 0.30
$PY src_e2/e.py gate.py --mode trackh --members P1,P3,R1 --cap 0.50
$PY src_e2/drift_report.py
echo DRIFT_DONE
