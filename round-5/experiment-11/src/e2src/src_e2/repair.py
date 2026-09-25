#!/usr/bin/env python3
"""E2 STEP 7b: E's frozen reference repair (src/repair_refs.py main) with the D1 shim and the plan's phase cap
($1.0; E's __main__ hard-wires 0.6). Usage: repair.py [--cap 1.0]"""
import argparse
import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src_e2"))
sys.path.insert(0, str(ROOT / "src"))
from compat import install  # noqa: E402

install()
import repair_refs  # noqa: E402

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--cap", type=float, default=1.0)
    asyncio.run(repair_refs.main(cap=ap.parse_args().cap))
