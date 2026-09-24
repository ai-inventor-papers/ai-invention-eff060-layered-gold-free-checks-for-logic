#!/bin/bash
# label-free scoring chain (CPU); API judges in parallel
cd "$(dirname "$0")/.."
PY=env/.venv/bin/python
export PYTHONHASHSEED=0 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
( $PY scoring/api_judges.py --stage prep --workers 10 && $PY scoring/api_judges.py --stage judges --concurrency 32 ) > logs/chain_api.log 2>&1 &
$PY scoring/score_consensus.py --stage score --workers 30 > logs/chain_score.log 2>&1
$PY scoring/score_consensus.py --stage pairwise --workers 36 > logs/chain_pairwise.log 2>&1
$PY scoring/score_consensus.py --stage exact --workers 36 > logs/chain_exact.log 2>&1
wait
echo SCORING_CHAIN_DONE >> logs/chain_score.log
