#!/usr/bin/env python3
"""T6-E: Candidate-Signature Consensus (CSC) on development set E -- pipeline entry point.

Stages (each idempotent; LLM calls are disk-cached in results/llm_cache.jsonl, so no call is ever repeated):
  prep     integrity checks (prompt sha256, R_AB label sha1), label-blind frame, FREE-MATCHED peers   (src/prep.py)
  pilot    30-row CSC pilot: per-model parse/JSON/cost, projection for every arm                       (src/pilot.py)
  prereg   prereg_csc_E.json + sha256 (before any CSC score is joined to labels)                        (src/gen.py prereg)
  mini     200-row stratified mini-sweep (OWN + FORMAT-ONLY) + 20 PLACEBO rows                           (src/gen.py mini)
  full     all arms (OWN, FMT, OTHER, K4, RENAME_SYN, RENAME_NONCE, PLACEBO)                              (src/gen.py full)
  repro    $0 reproduction of eval 2's 3-family pool (0.7427) and T1's c_score_align (0.741)             (src/repro.py)
  score    label-blind scoring of every arm (+ FREE-MATCHED, + 9-peer ALIGN re-derivation), hashed       (src/score.py)
  analyse  label-joined analyses (a)-(k), gates                                                          (src/analyse.py)
  posthoc  POST-HOC phi-4 exemplar-leakage sensitivity                                                (src/posthoc_contam.py)
  audit    independent re-derivation of headline numbers + permuted-label placebo (src/audit_rederive.py [extra])
  report   csc_gate_E.json, per_item_csc_E.jsonl, tables.md, deviations.json, method_out.json            (src/report.py)
usage: PYTHONHASHSEED=0 .venv/bin/python method.py [stage ...]   (default: repro score analyse posthoc report -- the $0 stages)
"""
from __future__ import annotations

import os
import resource
import subprocess
import sys
from pathlib import Path

from loguru import logger

ROOT = Path(__file__).resolve().parent
STAGES = {"prep": ["src/prep.py"], "pilot": ["src/pilot.py"], "prereg": ["src/gen.py", "prereg"], "mini": ["src/gen.py", "mini"],
          "full": ["src/gen.py", "full"], "repro": ["src/repro.py"], "score": ["src/score.py"], "analyse": ["src/analyse.py"],
          "posthoc": ["src/posthoc_contam.py"], "report": ["src/report.py"], "audit": ["src/audit_rederive.py"], "audit_extra": ["src/audit_rederive.py", "extra"], "test": ["-m", "pytest", "-q", "-c", "pytest.ini", "tests"]}

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
(ROOT / "logs").mkdir(exist_ok=True)
logger.add(ROOT / "logs" / "method.log", rotation="30 MB", level="DEBUG")


@logger.catch(reraise=True)
def main(stages: list[str]) -> None:
    ram = 20 * 1024**3  # container limit 29 GB; the heaviest stage (analysis bootstrap) needs < 4 GB
    resource.setrlimit(resource.RLIMIT_AS, (ram, ram))
    env = {**os.environ, "PYTHONHASHSEED": "0"}  # repair_census.fp uses hash()
    for st in stages:
        if st not in STAGES:
            raise ValueError(f"unknown stage {st}; choose from {list(STAGES)}")
        logger.info(f"=== stage {st}")
        r = subprocess.run([sys.executable, *STAGES[st]], cwd=ROOT, env=env)
        if r.returncode != 0:
            raise RuntimeError(f"stage {st} failed with exit code {r.returncode}")
    logger.info("done")


if __name__ == "__main__":
    main(sys.argv[1:] or ["repro", "score", "analyse", "posthoc", "report"])
