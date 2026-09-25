#!/bin/bash
# Label-free scoring chain (runs while labels are produced): build -> disguise -> L3 -> flash-lite (disg, orig) ->
# nano (orig, disg) -> cost-matched pilot (30 rows, both views). Each judge sweep keeps the label commitment out of its budget.
cd "$(dirname "$0")/.."
PY=exp5src/.venv/bin/python
while ! grep -q "=== gen done" logs/gen_all.log; do sleep 20; done
$PY src/score_e2b.py build
$PY src/score_e2b.py disguise
$PY src/score_e2b.py l3
C=$(python3 src/label_commit.py); echo "label commitment $C"
$PY src/score_e2b.py judges --which flashlite --commit $C
C=$(python3 src/label_commit.py); $PY src/score_e2b.py judges --which nano --commit $C
C=$(python3 src/label_commit.py); $PY src/score_e2b.py judges --which costmatched_pilot --commit $C
echo "=== scoring chain done $(date -u +%T)"
