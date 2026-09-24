#!/bin/bash
# Sequential GPU pipeline (F-KEY local path). Each stage is cached/idempotent; a failed stage does not stop the next.
export PYTHONHASHSEED=0
cd "$(dirname "$0")"
for st in "local_judges" "local_verb" "local_sc" "b2_read --which dev,gate,screen" "nli --which local" "b2_read --which unbatched,rewrites,Eref,E" "local_strong" "t2_repro"; do
  echo "$(date -u +%H:%M:%S) START $st" >> logs/gpu_pipeline.log
  .venv/bin/python method.py --stage $st > "logs/gpu_$(echo $st | tr ' ,-' '___').log" 2>&1
  echo "$(date -u +%H:%M:%S) END $st rc=$?" >> logs/gpu_pipeline.log
done
