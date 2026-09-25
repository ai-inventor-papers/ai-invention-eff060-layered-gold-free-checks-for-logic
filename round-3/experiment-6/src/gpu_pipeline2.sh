#!/bin/bash
# Second GPU chain: waits for gpu_pipeline.sh to finish, then T2 repro + the post-hoc B2 thinking-reader diagnostic.
export PYTHONHASHSEED=0
cd "$(dirname "$0")"
while kill -0 $(cat logs/gpu_pipeline.pid) 2>/dev/null; do sleep 20; done
for st in "t2_repro" "b2_think"; do
  echo "$(date -u +%H:%M:%S) START $st" >> logs/gpu_pipeline.log
  .venv/bin/python method.py --stage $st > "logs/gpu_$(echo $st | tr ' ,-' '___').log" 2>&1
  echo "$(date -u +%H:%M:%S) END $st rc=$?" >> logs/gpu_pipeline.log
done
