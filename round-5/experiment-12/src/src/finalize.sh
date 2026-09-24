#!/bin/bash
# E2-B finalisation, in the pre-registered order:
#   (1) label-free score assembly + descriptive analysis + SCORE SEAL (no label read so far; open() guard active)
#   (2) E2's frozen label steps: assemble_e2 -> controls_e2 -> testability_e2 -> seal_e2 -> verify_seal
#       (if the run budget never returned, the INCOMPLETE batch-1 panel votes are moved aside first, so every sentence is
#        in the same no-panel regime: a started batch that cannot finish is excluded entirely, never partially used)
#   (3) rename controls scored (V0) and the score seal refreshed to include them (still label-free rows)
#   (4) join + analyses (analyse_e2b.py refuses to run unless both seals verify) -> E2B_FINAL_READY.json
#   (5) union with E2-A if its M3 marker exists; method_out.json; tables.md
cd "$(dirname "$0")/.."
PY=exp5src/.venv/bin/python
EPY=e2bsrc/.venv/bin/python
set -x
$PY src/score_e2b.py assemble
$PY src/descriptive_e2b.py
$PY src/seal_scores.py seal || exit 1
if [ -f e2b/api_blocked.flag ] && [ ! -f e2b/budget_stop_batches_complete.json ]; then
  python3 - <<'PY'
import json, time
from pathlib import Path
W = Path("e2bsrc/work")
prog = Path("e2b/progress.jsonl")
done_batches = [json.loads(l)["batch"] for l in prog.read_text().splitlines() if l.strip()] if prog.exists() else []
last = max(done_batches) if done_batches else 0
sents = json.loads(Path("e2b/sentences_E2B.json").read_text())
keep = {s["sentence_id"] for s in sents if s["e2b_batch"] <= last}
moved = {}
for n in ("panel_heldout.jsonl", "panel_heldout_adj.jsonl"):
    p = W / n
    if not p.exists():
        continue
    rs = [json.loads(l) for l in p.read_text().splitlines() if l.strip()]
    inc = [r for r in rs if r["sentence_id"] not in keep]
    with open(W / n.replace(".jsonl", "_incomplete_batch_excluded.jsonl"), "a") as f:
        for r in inc:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    p.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rs if r["sentence_id"] in keep))
    moved[n] = len(inc)
Path("e2b/budget_stop_batches_complete.json").write_text(json.dumps({"completed_batches": done_batches, "last_complete_batch": last,
    "panel_records_moved_aside_from_incomplete_batches": moved, "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "rule": "a started batch that could not finish end to end is excluded from the panel regime entirely"}, indent=1))
print("incomplete-batch panel records moved aside:", moved, "last complete batch:", last)
PY
fi
(cd e2bsrc && .venv/bin/python src_e2/assemble_e2.py && .venv/bin/python src_e2/controls_e2.py && .venv/bin/python src_e2/testability_e2.py && .venv/bin/python src_e2/seal_e2.py && .venv/bin/python src_e2/verify_seal.py) || exit 1
cp e2bsrc/seal.json e2b/seal.json; cp e2bsrc/testability_E2.json e2b/testability_E2B.json
$PY src/score_e2b.py controls --which labelled
$PY src/seal_scores.py seal || exit 1
$PY src/analyse_e2b.py --B ${B:-2000} --placebo-n ${PLACEBO_N:-300}
if [ -f e2b/m3_pointer.json ]; then
  E2A=$(python3 -c "import json;m=json.load(open('e2b/m3_pointer.json'))['marker'];print(m.get('per_row_file') or m.get('path') or m.get('per_item') or '')")
  if [ -n "$E2A" ]; then $PY src/union.py --e2a "$E2A" --e2a-marker "$(python3 -c "import json;print(json.load(open('e2b/m3_pointer.json'))['marker_path'])")"; fi
else
  echo '{"status": "NOT_COMPUTED_E2A_MISSING", "rerun": "exp5src/.venv/bin/python src/union.py --e2a <E2-A per-row file> --e2a-marker <E2A_FINAL_READY.json>"}' > analysis/union_longpool.json
fi
$PY src/make_method_out.py
$PY src/make_tables.py
