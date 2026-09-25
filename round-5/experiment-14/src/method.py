#!/usr/bin/env python3
"""Orchestrator of the iteration-5 FREEZE experiment (Part A V0-V5 screen, Part B GG, Part C library, outputs).

Runs the src/ scripts in the pre-registered order under PYTHONHASHSEED=0. Idempotent: a step whose declared output already
exists is skipped (the prereg / freeze writers also refuse to overwrite on their own), so re-running never re-bills
OpenRouter (every gloss verdict is cached in results/gloss_cache.jsonl) and never rewrites a frozen file.

Usage:
  .venv/bin/python method.py                      # every stage
  .venv/bin/python method.py --stage A            # A | B | GGB | C | OUT | TEST (comma-separated)
  .venv/bin/python method.py --stage OUT --force  # re-run steps even if their outputs exist (frozen writers still refuse)
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

from loguru import logger

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
PY = sys.executable

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
(ROOT / "logs").mkdir(exist_ok=True)
logger.add(ROOT / "logs" / "method.log", rotation="30 MB", level="DEBUG")

# (stage, script + args, cwd, output that marks the step done)
STEPS = [
    ("A", ["copy_inputs.py"], SRC, "inputs_manifest.json"),
    ("A", ["step0_gates.py"], SRC, "results/gate_G0.json"),
    ("A", ["prereg_improve.py"], SRC, "prereg_improve.json"),
    ("A", ["make_row_index.py"], SRC, "results/row_index_labelfree.jsonl"),
    ("A", ["score_variants.py"], SRC, "results/scores_E_variants.jsonl"),
    ("A", ["fit_v4.py"], SRC, "results/scores_E_V4.jsonl"),
    ("A", ["screen.py"], SRC, "results/screen_E.json"),
    ("A", ["select_rule.py"], SRC, "results/selection_E.json"),
    ("A", ["freeze_part_a.py"], SRC, "freeze/selection.json"),
    ("B", ["probe.py"], SRC, "results/probe.json"),
    ("B", ["prereg_gg.py"], SRC, "prereg_gg.json"),
    ("B", ["gg_search.py", "all"], SRC, "results/gg_search.jsonl"),
    ("B", ["gg_gates.py", "dev", "v1"], SRC, "results/gg_gates_dev_v1.json"),
    ("B", ["gg_gates.py", "confirm", "v2"], SRC, "results/gg_gates_confirm_v2.json"),
    ("B", ["gg_gloss.py"], SRC, "results/gg_verdicts.json"),
    ("B", ["gg_score.py"], SRC, "results/gg_dev.json"),
    ("B", ["freeze_part_b.py"], SRC, "freeze/gg_gate.json"),
    ("GGB", ["ggb_search.py", "all"], SRC, "results/ggb_search.jsonl"),
    ("GGB", ["ggb_score.py"], SRC, "results/ggb_dev.json"),
    ("C", ["vendor_lib.py"], SRC, "lib/PROVENANCE.json"),
    ("OUT", ["make_outputs.py"], SRC, "method_out.json"),
    ("OUT", ["make_tables.py"], SRC, "tables.md"),
    ("TEST", ["-m", "pytest", "-q", "tests/test_variants.py", "tests/test_gg.py", "tests/test_budget.py"], ROOT, None),
    ("TEST", ["tests/audit_rederive.py"], ROOT, None),
    ("TEST", ["tests/smoke_lib.py"], ROOT, None),
]
NEVER_FORCE = {"prereg_improve.py", "prereg_gg.py", "freeze_part_a.py"}  # immutable writers


@logger.catch(reraise=True)
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", default="A,B,GGB,C,OUT,TEST")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    stages = set(a.stage.split(","))
    env = {**os.environ, "PYTHONHASHSEED": "0"}
    for stage, args, cwd, marker in STEPS:
        if stage not in stages:
            continue
        name = args[0]
        if marker and (ROOT / marker).exists() and (not a.force or name in NEVER_FORCE):
            logger.info(f"[{stage}] skip {' '.join(args)} ({marker} exists)")
            continue
        logger.info(f"[{stage}] run {' '.join(args)}")
        t0 = time.time()
        try:
            subprocess.run([PY, *args], cwd=cwd, env=env, check=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"[{stage}] {name} failed with exit code {e.returncode}")
            raise
        logger.info(f"[{stage}] {name} done in {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
