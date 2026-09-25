#!/usr/bin/env bash
# Reproduce T8 end to end (CPU only, $0). Execution order = plan order; PYTHONDONTWRITEBYTECODE keeps the read-only
# eval-2 workspace free of new __pycache__ files; PYTHONHASHSEED=0 as in eval 2.
set -euo pipefail
cd "$(dirname "$0")"
export PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1
PY=.venv/bin/python
[ -x "$PY" ] || { uv venv .venv --python=3.12 && uv pip install --python .venv/bin/python -r pyproject.toml; }
$PY src/t8_prereg.py                      # 1. prereg_d_split.json + sha256 (BEFORE any Part-1 number)
for s in mini s50 all; do $PY src/t8_run_rcomp_matrix.py --stage $s; done   # 2. R_COMP matrix (resumable)
$PY src/t8_part1.py                       # 3. gates G0-G2 + Part 1
$PY src/t8_part1_net.py                   #    NET per rule
$PY src/t8_part3.py                       # 4. power_E2.json
$PY src/t8_part2.py                       # 5. R_COMP analyses (G3, SIG e/d, SIG-FREE drop, validation)
$PY src/t8_part4.py                       # 6. verified record tables (a)-(m)
$PY src/t8_figs.py                        # 7. figures
$PY audit/rederive.py                     # 8. independent re-derivation + placebos
$PY src/t8_eval_out.py                    # 9. eval_out.json
$PY src/t8_record_md.py                   # 10. record.md + source hashes
