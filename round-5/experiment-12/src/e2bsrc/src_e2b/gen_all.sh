#!/bin/bash
# Generation (10 frozen slots, fewshot_v1, T=0) for E2-B batches in hash order, each followed by E2's D4 transient retry.
cd "$(dirname "$0")/.."
PY=.venv/bin/python
export AII_HARD_CAP=${AII_HARD_CAP:-9.5}
for b in 1 2 3 4 5 6 7 8; do
  echo "=== batch $b $(date -u +%T)"
  $PY src_e2b/budget.py --estimate 0.06
  $PY src_e2/e.py generate.py --slots G1,G1b,G2,G3,G4,G5,G6,G7,G8,G9 --variants fewshot_v1 --sentences work/batch_$b.json --cap 1.3 --concurrency 16
  $PY src_e2/gen_retry.py --sentences work/batch_$b.json --concurrency 4 --cap 1.3
done
echo "=== gen done $(date -u +%T)"
