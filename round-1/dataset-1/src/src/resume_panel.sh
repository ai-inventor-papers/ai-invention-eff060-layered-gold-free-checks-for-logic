#!/bin/bash
# LLM-dependent steps, in the order they were actually executed after the shared key's daily limit reset (2026-09-23).
# Every step is resumable: panel responses are cached in work/panel_cache.jsonl (key = sentence|model|prompt_sha1|class ids;
# failed calls are retried, never served from cache), generations and repairs are append-only jsonl, per-sentence outputs
# are skipped when already present. Spend is in cost_ledger.jsonl; or_client.py stops at $9.50 cumulative.
set -e
cd "$(dirname "$0")/.."
PY=.venv/bin/python
$PY src/gate.py --mode trackh --members P1,P3,R1 --cap 0.6                       # 4c real-error check (96 track-H pairs)
$PY src/select_topup.py                                                           # pre-registered L25 top-up (100 sentences)
$PY src/generate.py --slots G2 --variants zeroshot_v1 --sentences work/sentences_600_before_topup.json   # key-limit losses
$PY src/generate.py --slots G9,G1,G6,G3,G2 --variants fewshot_v1 --sentences work/sentences_topup.json  # top-up candidates
$PY src/extend_labels.py --budget 8                                               # new rows into existing classes (ids stable)
$PY src/run_label.py --kind heldout --budget 8                                    # labels for the 100 top-up sentences
$PY src/screen_scope.py
$PY src/panel_run.py --kind screen --members P1,P3,R1 --only work/screen_panel_scope.json --cap 1.3     # 6b
$PY src/panel_run.py --kind screen --members P1,P3,R1 --vg-only --out panel_screen_vg.jsonl --cap 1.3  # 6b VOCAB_GRAN strings
$PY src/panel_run.py --kind heldout --members P1,P3,R1 --ctrl-reduced --limit 30 --cap 6.3            # 5c pilot (3 raters)
$PY src/panel_run.py --kind heldout --members P3,R1 --ctrl-reduced --cap 4.6                          # 5b stage 1
$PY src/panel_run.py --kind heldout --members P3,R1 --adjudicate P1 --cap 1.6                         # 5b stage 2 (disagreements)
$PY src/repair_refs.py                                                            # 5e reference repair for GOLD_WRONG
$PY src/run_label.py --kind heldout --refs work/reference_overrides.json --out labels_heldout_repaired.jsonl
$PY src/assemble.py && $PY src/stats.py && $PY src/card.py && $PY data.py         # 5d/5f + 7
