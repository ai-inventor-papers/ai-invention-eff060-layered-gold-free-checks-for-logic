#!/usr/bin/env python3
"""T8 orchestrator: predicting the vocabulary fix (d split), R_COMP second population, iteration-5 power, verified record.

CPU only, no LLM calls, $0. Runs the plan's execution order; every step is a script under src/ (or audit/):
  prereg -> R_COMP matrix (mini, s50, all; resumable) -> Part 1 (+NET) -> Part 3 -> Part 2 -> Part 4 -> figures
  -> audit -> eval_out.json -> record.md/source hashes.
usage: .venv/bin/python eval.py [--skip-matrix] [--from STEP]
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
logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(ROOT / "logs" / "eval.log", rotation="30 MB", level="DEBUG")

STEPS = [("prereg", ["src/t8_prereg.py"]),
         ("matrix_mini", ["src/t8_run_rcomp_matrix.py", "--stage", "mini"]),
         ("matrix_s50", ["src/t8_run_rcomp_matrix.py", "--stage", "s50"]),
         ("matrix_all", ["src/t8_run_rcomp_matrix.py", "--stage", "all"]),
         ("part1", ["src/t8_part1.py"]), ("part1_net", ["src/t8_part1_net.py"]), ("part3", ["src/t8_part3.py"]),
         ("part2", ["src/t8_part2.py"]), ("part4", ["src/t8_part4.py"]), ("figs", ["src/t8_figs.py"]),
         ("audit", ["audit/rederive.py"]), ("eval_out", ["src/t8_eval_out.py"]), ("record_md", ["src/t8_record_md.py"])]


@logger.catch(reraise=True)
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-matrix", action="store_true", help="reuse results/pair_matrix_RCOMP.jsonl")
    ap.add_argument("--from", dest="start", default="prereg", choices=[s for s, _ in STEPS])
    a = ap.parse_args()
    env = dict(os.environ, PYTHONHASHSEED="0", PYTHONDONTWRITEBYTECODE="1")
    names = [s for s, _ in STEPS]
    for name, cmd in STEPS[names.index(a.start):]:
        if a.skip_matrix and name.startswith("matrix"):
            continue
        t0 = time.time()
        logger.info(f"step {name}: {' '.join(cmd)}")
        subprocess.run([sys.executable, *cmd], cwd=ROOT, env=env, check=True)
        logger.info(f"step {name} done in {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
