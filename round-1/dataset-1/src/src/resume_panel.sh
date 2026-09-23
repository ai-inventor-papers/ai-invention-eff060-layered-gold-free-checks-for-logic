#!/bin/bash
# Finish the LLM-dependent steps once the shared OpenRouter key has credit again (check: GET /api/v1/key limit_remaining).
# Every step is resumable: panel responses are cached in work/panel_cache.jsonl (never re-billed), generation and
# repair outputs are append-only jsonl. Spend so far is in cost_ledger.jsonl; or_client.py stops at $9.50 cumulative.
set -e
cd "$(dirname "$0")/.."
PY=.venv/bin/python
$PY src/gate.py --mode trackh --members P1,P3,R1 --cap 0.35            # 4c real-error check (96 track-H pairs)
$PY src/panel_run.py --kind heldout --members P1,P3,R1 --limit 30 --cap 3.0   # 5c pilot: re-extrapolate cost
$PY src/panel_run.py --kind heldout --members P1,P3,R1 --cap 3.0      # 5b full blind pass (gold audit + adjudication)
$PY src/repair_refs.py                                                # 5e reference repair for GOLD_WRONG
$PY src/run_label.py --kind heldout --refs work/reference_overrides.json --out labels_heldout_repaired.jsonl
# 6b screen scope: sentences with any VOCAB_GRAN/COMPOUND/TIMEOUT class + 20% sha1 sample of the rest
$PY src/screen_scope.py
$PY src/panel_run.py --kind screen --members P1,P3,R1 --only work/screen_panel_scope.json --cap 1.3
$PY src/assemble.py && $PY src/stats.py && $PY src/finalize.py
