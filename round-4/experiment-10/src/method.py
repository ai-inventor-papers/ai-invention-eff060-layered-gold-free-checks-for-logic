#!/usr/bin/env python3
"""Orchestrator: Candidate-Signature Consensus (CSC) on PERTURB and R_COMP (iteration 4, T6-P).

Stages (comma-separated with --stage, or 'all'):
  views     STAGE 1  data views, signatures, sig_sharing.csv, firewalled FREE view, FREE3 peers      (CPU, $0)
  tests     unit tests (tests/test_csc_lib.py) - must pass before any API call                      (CPU, $0)
  pilot     STAGE 3  30 signatures x 4 models; compliance, usage, projection, prompt choice          (API ~$0.12)
  prereg    STAGE 4  freeze results/prereg_csc_P.json (+sha256); never overwritten                  (CPU)
  peers     STAGE 5  CSC peer sweeps perturb_E -> free -> perturb_R -> sig -> retest                 (API ~$3.4)
  local     LOCAL2 secondary local-peer arm (llama.cpp, CPU)                                          ($0)
  score     STAGE 6  CSC / SIGPROXY / FREE3 scores (+ --local LOCAL2 scores)                         (CPU)
  typing    STAGE 7  same-vocabulary typed-repair searches                                          (CPU)
  analysis  STAGE 7  all tables (verifies the prereg sha256 first), tables.md, deviations            (CPU)
  manifest  job manifest for the peer sweep + firewall record                                        (CPU)
  output    STAGE 9  perturb_csc_scores.jsonl, csc_rcomp_sig_scores.jsonl, method_out.json            (CPU)
  rederive  independent re-derivation (tests/rederive.py)                                              (CPU)
'all' runs every $0 stage in order and the API stages only when the OpenRouter key has budget (1-token probe).
"""
from __future__ import annotations

import argparse
import asyncio
import subprocess
import sys
from pathlib import Path

from loguru import logger

ROOT = Path(__file__).resolve().parent
PY = sys.executable
(ROOT / "logs").mkdir(exist_ok=True)
logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(ROOT / "logs" / "method.log", rotation="30 MB", level="DEBUG")


def run(args: list[str], timeout: int = 7200) -> None:
    logger.info("$ " + " ".join(args))
    r = subprocess.run(args, cwd=ROOT, timeout=timeout)
    if r.returncode != 0:
        raise RuntimeError(f"stage failed ({r.returncode}): {' '.join(args)}")


def key_has_budget() -> bool:
    sys.path.insert(0, str(ROOT / "src"))
    import or_client
    try:
        ok, msg = asyncio.run(or_client.probe())
    except Exception as ex:  # noqa: BLE001 - network errors mean 'no budget now'
        ok, msg = False, f"{type(ex).__name__}: {ex}"
    logger.info(f"key probe: {msg}")
    return ok


STAGES = {
    "views": [[PY, "src/views.py"]],
    "tests": [[PY, "-m", "pytest", "-q", "tests/test_csc_lib.py", "-p", "no:cacheprovider"]],
    "pilot": [[PY, "src/peers_run.py", "pilot"]],
    "prereg": [[PY, "src/csc_prereg.py"]],
    "peers": [[PY, "src/peers_run.py", "all"]],
    "local": [[PY, "src/local_peers.py"]],
    "score": [[PY, "src/csc_score.py"], [PY, "src/csc_score.py", "--local"]],
    "typing": [[PY, "src/csc_typing.py", "--which", "oracle,csc,proxy,free3"]],
    "analysis": [[PY, "src/csc_analysis.py"], [PY, "src/csc_tables.py"]],
    "manifest": [[PY, "src/csc_manifest.py"]],
    "output": [[PY, "src/csc_output.py"]],
    "rederive": [[PY, "tests/rederive.py"]],
}
ORDER = ["views", "tests", "pilot", "prereg", "peers", "local", "score", "typing", "manifest", "analysis", "output", "rederive"]
API = {"pilot", "peers"}


@logger.catch(reraise=True)
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", default="all")
    a = ap.parse_args()
    stages = ORDER if a.stage == "all" else a.stage.split(",")
    api_ok = None
    for st in stages:
        if st not in STAGES:
            raise SystemExit(f"unknown stage {st}; choose from {ORDER}")
        if st in API:
            if api_ok is None:
                api_ok = key_has_budget()
            if not api_ok:
                logger.warning(f"skipping {st}: OpenRouter key has no budget (deviation D-BUDGET)")
                continue
        for cmd in STAGES[st]:
            run(cmd)
    logger.info("done")


if __name__ == "__main__":
    main()
