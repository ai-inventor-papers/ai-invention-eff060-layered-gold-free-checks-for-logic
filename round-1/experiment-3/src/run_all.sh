#!/usr/bin/env bash
# Full pipeline, in order. OpenRouter responses are cached in data/peer_raw/, so re-runs do not re-bill.
set -euo pipefail
cd "$(dirname "$0")"
export PYTHONHASHSEED=0
PY=.venv/bin/python
$PY -m pytest -c /dev/null --rootdir . --noconftest -q tests/test_fol.py   # T0
$PY tests/census_regression.py                                          # T0 / F7
$PY src/screen.py                                                       # STEP 1 (labels + hash)
$PY src/peers.py call --arm peers --dry-run                             # T2
$PY src/peers.py call --arm peers                                       # STEP 3
$PY src/peers.py call --arm sc_cheap                                    # STEP 4
$PY src/peers.py call --arm sc_same                                     # STEP 4 (optional arm)
$PY src/peers.py build
$PY src/consensus.py --mini 20                                          # T3
$PY src/consensus.py                                                    # STEP 5/6 + T5
$PY src/analysis.py --boot 2000                                         # STEP 7/8
$PY tests/audit_rederive.py
