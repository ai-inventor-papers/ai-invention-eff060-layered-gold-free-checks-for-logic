#!/bin/bash
# Judge sweeps after the budget stop (resumable; failed units are re-asked, answered ones never re-billed).
# Order follows the shrink order in reverse priority: flash-lite + nano (cheap comparators) -> cost-matched pilot ->
# cost-matched disguised -> cost-matched original -> frontier (the first paid item to shrink after GG).
cd "$(dirname "$0")/.."
PY=exp5src/.venv/bin/python
C() { python3 src/label_commit.py; }
late() { [ $(date -u +%H%M) -ge 1538 ]; }
$PY src/score_e2b.py judges --which flashlite --commit $(C)
late && exit 0
$PY src/score_e2b.py judges --which nano --commit $(C)
$PY src/score_e2b.py judges --which costmatched_pilot --commit $(C)
D=$(python3 src/costmatched_decision.py); echo "cost-matched decision: $D"
if [ "$D" = "RETRY_MT300" ]; then $PY src/score_e2b.py judges --which costmatched_retry --commit $(C); D=$(python3 src/costmatched_decision.py); echo "after retry: $D"; fi
case "$D" in
  RUN_DISG_AND_ORIG*|RUN_DISG_ONLY*)
    $PY src/score_e2b.py judges --which costmatched_disg --commit $(C)
    if [[ "$D" == RUN_DISG_AND_ORIG* ]]; then $PY src/score_e2b.py judges --which costmatched_orig --commit $(C); fi ;;
  *) echo "cost-matched full sweep not run: $D" ;;
esac
late && exit 0
python3 -c "print('frontier commitment', $(C))"
$PY src/score_e2b.py frontier_cut --commit $(C)
$PY src/score_e2b.py judges --which frontier --commit $(C)
echo "=== judge resume done $(date -u +%T)"
