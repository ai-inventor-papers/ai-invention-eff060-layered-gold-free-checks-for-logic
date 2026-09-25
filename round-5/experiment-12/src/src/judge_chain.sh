#!/bin/bash
# API judges on every parseable E2-B row (batch order), each sweep keeping the label commitment out of its budget.
cd "$(dirname "$0")/.."
PY=exp5src/.venv/bin/python
C=$(python3 src/label_commit.py); echo "label commitment $C"
$PY src/score_e2b.py judges --which flashlite --commit $C
C=$(python3 src/label_commit.py); $PY src/score_e2b.py judges --which nano --commit $C
C=$(python3 src/label_commit.py); $PY src/score_e2b.py judges --which costmatched_pilot --commit $C
echo "=== judge chain done $(date -u +%T)"
