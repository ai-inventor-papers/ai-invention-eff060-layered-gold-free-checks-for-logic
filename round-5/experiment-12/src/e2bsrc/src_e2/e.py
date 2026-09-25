#!/usr/bin/env python3
"""Thin runner: executes one of E's frozen scripts in src/ (byte-identical to E) with the D1 compatibility shim.
Usage: .venv/bin/python src_e2/e.py <script.py> [args...]"""
import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src_e2"))
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "labeller"))
from compat import install  # noqa: E402

install()
script = sys.argv[1]
sys.argv = [str(ROOT / "src" / script)] + sys.argv[2:]
runpy.run_path(str(ROOT / "src" / script), run_name="__main__")
