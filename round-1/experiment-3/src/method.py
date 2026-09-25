#!/usr/bin/env python3
"""Entry point: candidate C (cross-system z3 consensus) + self-consistency baselines on the frozen NL->FOL screen.

Runs the full pipeline in order (each stage is a module in src/; OpenRouter responses are cached in data/peer_raw/,
so a re-run does not re-bill). Stages: T0 tests -> screen (labels + hash) -> peers / SC sampling -> build ->
consensus (T3 mini, then full) -> analysis (writes results/summary.json + method_out.json) -> previews.

usage: python method.py [--skip-api] [--boot 2000]
"""
import argparse
import os
import subprocess
import sys
from pathlib import Path

from loguru import logger

ROOT = Path(__file__).resolve().parent
logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(ROOT / "logs" / "method.log", rotation="30 MB", level="DEBUG")


def run(args: list[str]) -> None:
    logger.info("$ " + " ".join(args))
    env = {**os.environ, "PYTHONHASHSEED": "0"}
    subprocess.run([sys.executable, *args], cwd=ROOT, env=env, check=True)


@logger.catch(reraise=True)
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-api", action="store_true", help="do not call OpenRouter; use cached responses only")
    ap.add_argument("--boot", type=int, default=2000)
    a = ap.parse_args()
    run(["-m", "pytest", "-c", "/dev/null", "--rootdir", ".", "--noconftest", "-q", "tests/test_fol.py"])
    run(["tests/census_regression.py"])
    run(["src/screen.py"])
    if not a.skip_api:
        for arm in ("peers", "sc_cheap", "sc_same"):
            run(["src/peers.py", "call", "--arm", arm])
    run(["src/peers.py", "build"])
    run(["src/consensus.py", "--mini", "20"])
    run(["src/consensus.py"])
    run(["src/analysis.py", "--boot", str(a.boot)])
    run(["tests/audit_rederive.py"])
    logger.info("done: method_out.json, results/summary.json, results/audit_rederive.json")


if __name__ == "__main__":
    main()
