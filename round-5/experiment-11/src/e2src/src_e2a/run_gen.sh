#!/bin/bash
set -e
cd "$(dirname "$0")/.."
export AII_HARD_CAP=9.5
export AII_PROVIDER_PIN="$(cat src_e2a/pin.json)"
PY=.venv/bin/python
$PY src_e2/e.py generate.py --slots G1,G1b,G2,G3,G4,G5,G6,G7,G8,G9 --variants fewshot_v1 --sentences work/sentences.json --cap 1.3 --concurrency 32
$PY src_e2/gen_retry.py --sentences work/sentences.json --concurrency 6
echo GEN_DONE
