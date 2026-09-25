#!/usr/bin/env python3
"""Code smoke test of src/analyse_e2b.py on SYNTHETIC labels (random, never a result, nothing written outside tests/tmp):
population choice, S4 cross-fitting, cells/deltas, frontier IPW block, complexity, coverage, tau-b.
Run: exp5src/.venv/bin/python tests/test_analysis_synthetic.py"""
import json
import sys
from pathlib import Path

import numpy as np

WS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WS / "src"))
import analyse_e2b as A  # noqa: E402

rng = np.random.default_rng(1)
sents = {s["sentence_id"]: s for s in json.loads((WS / "e2b" / "sentences_E2B.json").read_text())}
rows = []
for i, sid in enumerate(sorted(sents)[:120]):
    for slot in ("G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8"):
        y = int(rng.random() < 0.7)
        s = sents[sid]
        r = {"row_key": f"{sid}|{slot}", "sentence_id": sid, "slot": slot, "system": slot, "family": slot, "word_bin": s["word_bin"],
             "words": s["words"], "n_conditions": s["n_conditions"], "n_quant": s["n_quant"], "depth": s["depth"], "fold_E2": A.fold_e2(sid),
             "label": "ERROR" if y else "CORRECT", "tier": "A_unaudited_ref", "reading_choice": False, "y_AB": y, "parse_ok": True,
             "in_R_AB": False, "in_R_A": False, "in_R_AB_cont": False, "in_R_AU": True, "V0": float(np.clip(0.4 * y + rng.random() * 0.6, 0, 1)),
             "flashlite_disg": float(rng.random()), "flashlite_disg_status": "ok", "in_frontier_subsample": rng.random() < 0.3,
             "frontier_inclusion_prob": 0.3, "frontier_orig": float(rng.random()), "gen_cost_usd": 1e-4, "secs_align_sentence": 1.0}
        for f in A.S4_FEATS:
            r.setdefault(f, float(rng.random()))
        rows.append(r)
pop = A.choose_population(rows)
assert pop["population"] == "R_A_UNAUDITED", pop
for r in rows:
    r["in_POP"] = r["in_R_AU"]
info = A.add_s4(rows)
assert sum(r["S4_E2B"] is not None for r in rows) == len(rows)
C = A.Cell([r for r in rows if r["in_POP"]], "t", 100)
m = C.metric("V0")
d = C.delta("V0", "flashlite_disg")
assert m["strat_auroc"] > 0.5 and d["strat_delta"] is not None
fb = A.frontier_block(rows, 50)
assert fb["status"] == "OK", fb
cx = A.complexity_block(rows, 50)
cv = A.coverage_block(rows)
tb = A.taub_block(rows, 50)
print("analysis synthetic smoke test PASSED", round(m["strat_auroc"], 3), round(d["strat_delta"], 3), fb["ratio_V0_over_frontier"], list(cx))
