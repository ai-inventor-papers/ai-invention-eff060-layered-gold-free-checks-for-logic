#!/usr/bin/env bash
# Full reproduction: CPU only, no network, no LLM calls ($0). ~30 s.
set -euo pipefail
cd "$(dirname "$0")"
[ -x .venv/bin/python ] || { uv venv .venv --python=3.12 && uv pip install --python .venv/bin/python -r pyproject.toml; }
.venv/bin/python eval.py
