#!/usr/bin/env python3
"""R_COMP FREE confirmation of criterion (c): the metric (cross-family solver consensus c_score_align) vs the baseline
(the flash-lite rubric-A LLM judge, disguised and original views; plus local Qwen3-8B, frontier gemini-3.1-pro, c_exact
and the V1-V5 consensus variants), on free-vocabulary templated long sentences.

This is the entry point. It runs every step in the pre-registered order; each step is its own script. Paid steps are
cached and ledgered, so re-running them never re-bills. Steps:
  g0         $0  reproduce exp-7 SIG AUROCs (0.954 / 0.587)                         confirm/g0_repro.py
  judge_orig paid label-blind completion of the original-view judge (D16)          confirm/judge_orig_complete.py
  scores     $0  sealed score table + score seal (BEFORE any gloss call)            confirm/scores.py
  prereg     $0  prereg_rcomp_confirm.json (+ git commit, done once)                confirm/prereg.py
  pilot      paid gloss cost pilot + projection                                     confirm/gloss_pilot.py
  gate       paid gloss gate half A (gloss_v1); then half B (gloss_v2)             labeller/src/resume_gloss.py gate, gate.py
  gate_diag  $0  failure diagnostics (FALLBACK B)                                   confirm/gate_diagnostics.py
  finalize   $0  final labels + seal + post-seal join                               labeller/src/resume_gloss.py finalize
  audit      paid blind two-family audit (Sonnet-5 + GLM-4.6)                       confirm/audit_blind.py
  frontier   paid STEP F frontier judge (150 rows)                                  confirm/frontier_judge.py
  analysis   $0  verify seals, join ONCE, all analyses                              confirm/join_and_test.py
  report     $0  verdict, tables.md, method_out.json                                confirm/report.py
  checks     $0  re-derivation, deviations, ledger, final checks                    tests/rederive_confirm.py, confirm/final_checks.py
usage: uv run method.py [--steps analysis,report,checks]   (default: the $0 tail: analysis,report,checks)
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from loguru import logger

WS = Path(__file__).resolve().parent
PY = sys.executable
logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
(WS / "logs").mkdir(exist_ok=True)
logger.add(WS / "logs/method.log", rotation="30 MB", level="DEBUG")

STEPS = {
    "g0": [["confirm/g0_repro.py"]],
    "judge_orig": [["confirm/judge_orig_complete.py"]],
    "scores": [["confirm/scores.py"]],
    "prereg": [["confirm/prereg.py"]],
    "pilot": [["confirm/gloss_pilot.py"]],
    "gate": [["labeller/src/resume_gloss.py", "gate"], ["labeller/src/gate.py", "run", "--half", "B", "--version", "gloss_v2"]],
    "gate_diag": [["confirm/gate_diagnostics.py"]],
    "finalize": [["labeller/src/resume_gloss.py", "finalize", "--version", "gloss_v2"]],
    "audit": [["confirm/audit_blind.py"]],
    "frontier": [["confirm/frontier_judge.py"]],
    "analysis": [["confirm/join_and_test.py"]],
    "report": [["confirm/report.py"]],
    "checks": [["tests/rederive_confirm.py"], ["confirm/write_deviations.py"], ["confirm/final_checks.py"]],
}


@logger.catch(reraise=True)
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--steps", default="analysis,report,checks")
    a = ap.parse_args()
    for st in a.steps.split(","):
        for cmd in STEPS[st]:
            script = WS / cmd[0]
            cwd = script.parent if cmd[0].startswith("confirm/") else (WS / "labeller" if cmd[0].startswith("labeller/") else WS)
            args = [PY, str(script)] + cmd[1:]
            if cmd[0].startswith("labeller/"):
                args = [PY, str(Path(cmd[0]).relative_to("labeller"))] + cmd[1:]
            logger.info(f"[{st}] $ {' '.join(args)}")
            subprocess.run(args, check=True, cwd=cwd)
    logger.info("done")


if __name__ == "__main__":
    main()
