#!/bin/bash
# T1 full API sweeps in the pre-registered priority (prereg_T1.execution_order); every stage is cached + idempotent.
# Phase A (parallel, distinct budget components): flash-lite both views | nano both views | frontier ORIGINAL view
# Phase B: API verbaliser | SC-5 samples      Phase C: retest      (GPU NLI + CPU sc_score run separately)
# Phase D: frontier DISGUISED view under the shared-key reserve rule
cd "$(dirname "$0")"
export PYTHONHASHSEED=0
PY=.venv/bin/python
$PY method.py --stage judges --which cheap_disg,cheap_orig > logs/sweep_cheap.log 2>&1 & P1=$!
$PY method.py --stage judges --which cheap2_disg,cheap2_orig > logs/sweep_cheap2.log 2>&1 & P2=$!
$PY method.py --stage strong --which orig > logs/sweep_strong_orig.log 2>&1 & P3=$!
wait $P1 $P2
echo "$(date -u +%T) phase A cheap done" >> logs/api_chain_T1.log
$PY method.py --stage verbalise > logs/sweep_verbalise.log 2>&1 & P4=$!
$PY method.py --stage sc_gen > logs/sweep_sc_gen.log 2>&1 & P5=$!
wait $P3 $P4 $P5
echo "$(date -u +%T) phase A/B done" >> logs/api_chain_T1.log
$PY method.py --stage retest > logs/sweep_retest.log 2>&1
echo "$(date -u +%T) retest done" >> logs/api_chain_T1.log
$PY method.py --stage strong --which disg > logs/sweep_strong_disg.log 2>&1
echo "$(date -u +%T) phase D done" >> logs/api_chain_T1.log
