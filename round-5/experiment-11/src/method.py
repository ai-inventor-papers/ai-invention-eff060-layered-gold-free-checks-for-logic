#!/usr/bin/env python3
"""E2-A entry point: runs the label-free scoring, the seals/join and the analyses in the order actually executed.
Paid API stages (drift gate, generation, panel, API judges) are in e2src/src_e2a/*.sh and scoring/api_judges.py; they
are cached and never re-billed. Usage: python method.py [--from STAGE] [--prefix 110]
Stages: l3, consensus, pairwise, exact, prep, judges, local_judge, pilot, assemble, labels, join, analyse, rename, union, outputs"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

WS = Path(__file__).resolve().parent
PY = str(WS / "env" / ".venv" / "bin" / "python")
GPU = "/root/e2a_gpu/.venv/bin/python"
E2PY = str(WS / "e2src" / ".venv" / "bin" / "python")


def stages(prefix: int) -> list[tuple[str, list[str], Path]]:
    s = [("l3", [PY, "scoring/score_consensus.py", "--stage", "l3"], WS),
         ("consensus", [PY, "scoring/score_consensus.py", "--stage", "score", "--workers", "30"], WS),
         ("pairwise", [PY, "scoring/score_consensus.py", "--stage", "pairwise", "--workers", "36"], WS),
         ("exact", [PY, "scoring/score_consensus.py", "--stage", "exact", "--workers", "36"], WS),
         ("prep", [PY, "scoring/api_judges.py", "--stage", "prep", "--workers", "10"], WS),
         ("judges", [PY, "scoring/api_judges.py", "--stage", "judges", "--concurrency", "32"], WS),
         ("local_judge", [GPU, "scoring/local_judge.py", "--which", "qwen8b_disg,qwen8b_orig", "--bs", "64"], WS),
         ("pilot", [PY, "scoring/pilot_metrics_E2.py"], WS),
         ("assemble", [PY, "scoring/assemble_scores.py"], WS)]
    s += [(f"labels:{x}", [E2PY, f"src_e2/{x}.py"], WS / "e2src")
          for x in ("assemble_e2", "controls_e2", "testability_e2", "seal_e2", "verify_seal")]
    s += [("join", [PY, "analysis/analyse_E2A.py", "--stage", "join"], WS),
          ("analyse", [PY, "analysis/analyse_E2A.py", "--stage", "analyse"] + (["--prefix", str(prefix)] if prefix else []), WS),
          ("rename", [PY, "analysis/rename_V0.py"], WS),
          ("union", [PY, "analysis/union_E2B.py", "--deadline-utc", "2026-09-24T15:40:00Z", "--once"], WS),
          ("outputs", [PY, "analysis/make_outputs.py"], WS)]
    return s


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="start", default="l3")
    ap.add_argument("--prefix", type=int, default=110)
    a = ap.parse_args()
    env = dict(os.environ, PYTHONHASHSEED="0", OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1")
    run = False
    for name, cmd, cwd in stages(a.prefix):
        run = run or name.startswith(a.start)
        if run:
            print(f"== {name}: {' '.join(cmd)}", flush=True)
            subprocess.run(cmd, cwd=cwd, env=env, check=True)


if __name__ == "__main__":
    sys.exit(main())
