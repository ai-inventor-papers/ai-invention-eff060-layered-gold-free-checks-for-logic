#!/usr/bin/env python3
"""E2-B entry point: runs the pre-registered pipeline stage by stage (each stage is a resumable script in e2bsrc/ or src/).

Method (PRIMARY) = frozen cross-family consensus V0 c_score_align (exp-5 byte-identical pool_scoring, leave-own-family-out);
baselines = flash-lite rubric-A judge (disguised = primary comparator, original), gpt-4.1-nano, cost-matched deepseek-v3.2,
frontier gemini-3.1-pro-preview, and S4 (cross-fitted stack of cheap baselines). See README.md and prereg_iter5_E2B.json.

  python3 method.py --stage all        # every stage in order (paid stages need OPENROUTER_API_KEY / OPENROUTER_BASE_URL)
  python3 method.py --stage <name>     # one stage: freeze_check select prereg generate labels score judges finalize rederive
Paid stages are cached/resumable: re-running with the kept raw/ and cache files re-bills nothing."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

WS = Path(__file__).resolve().parent
EPY = str(WS / "e2bsrc/.venv/bin/python")
SPY = str(WS / "exp5src/.venv/bin/python")
STAGES = {
    "freeze_check": [[EPY, "src_e2b/code_freeze_check.py"], "e2bsrc"],
    "select": [[EPY, "src_e2b/select_e2b.py"], "e2bsrc"],
    "prereg": [["python3", "src/prereg_e2b.py"], "."],  # refuses to overwrite the frozen prereg
    "generate": [["bash", "e2bsrc/src_e2b/gen_all.sh"], "."],
    "labels": [["bash", "e2bsrc/src_e2b/run_batches_resume.sh"], "."],
    "score": [["bash", "-c", "bash src/scoring_pipeline.sh && bash src/cpu_chain.sh"], "."],
    "judges": [["bash", "src/judge_resume.sh"], "."],
    "finalize": [["bash", "src/finalize.sh"], "."],
    "rederive": [[SPY, "src/rederive_headline.py"], "."],
}


def run(name: str) -> int:
    cmd, cwd = STAGES[name]
    print(f"=== stage {name}: {' '.join(cmd)} (cwd {cwd})", flush=True)
    return subprocess.run(cmd, cwd=str(WS / cwd)).returncode


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", default="all", choices=["all", *STAGES])
    a = ap.parse_args()
    names = [n for n in STAGES if n != "prereg"] if a.stage == "all" else [a.stage]
    for n in names:
        rc = run(n)
        if rc != 0:
            print(f"stage {n} failed (rc {rc})")
            return rc
    return 0


if __name__ == "__main__":
    sys.exit(main())
