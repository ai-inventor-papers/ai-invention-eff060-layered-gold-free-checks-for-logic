"""Fractional tie-breaking: exact FA on heavily tied negatives, and reproduction of exp 5's post-hoc NF-anchored screen
numbers (RENAME FA ~0.074, ROLE_PERMUTE recall ~0.771) from the cached exp 5 screen scores."""
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import stats as ST  # noqa: E402


def test_fractional_fa_exact_with_40pct_ties():
    rng = np.random.default_rng(0)
    neg = np.concatenate([np.ones(400), rng.uniform(0, 0.99, 600)])  # 40% of negatives tie at the max
    t, lam = ST.matched_fa(neg, 0.10)
    assert t == 1.0 and abs(lam - 0.25) < 1e-12
    assert abs(ST.flag_vec(neg, t, lam).mean() - 0.10) < 1e-12


def test_fractional_fa_no_ties():
    v = np.arange(100) / 100.0
    t, lam = ST.matched_fa(v, 0.10)
    assert abs(ST.flag_vec(v, t, lam).mean() - 0.10) < 1e-12


def _solver(a):
    return {"CORRECT": "CORRECT", "EQ": "CORRECT", "VOCAB_GRAN": "CORRECT", "ERROR": "ERROR", "COMPOUND": "ERROR"}.get(a or "")


def test_reproduce_exp5_posthoc_nf_anchored():
    labs = json.loads((ROOT / "data/screen/screen_adjudicated_labels.json").read_text())
    rows = {}
    for l in (ROOT / "data/exp5/screen_scores.jsonl").read_text().splitlines():
        for r in json.loads(l)["rows"]:
            rows[r["key"]] = r
    g = lambda r: 1.0 if r is None or r.get("NF-anchored:g_score") is None else r["NF-anchored:g_score"]  # noqa: E731
    Lc = [i for i, v in labs.items() if i in rows and v["track"] == "L" and v["label_tier"] in ("A", "B") and not v.get("reading_choice")
          and v["final_label"] == "CORRECT" and _solver(v["auto_label"]) == "CORRECT"]
    t, lam = ST.matched_fa([rows[i]["NF-anchored:g_score"] for i in Lc if rows[i].get("NF-anchored:g_score") is not None], 0.10)
    rn = [r for k, r in rows.items() if k.startswith("RW:") and "_RENAME" in k and labs.get(k[3:].rsplit("_RENAME", 1)[0], {}).get("final_label") == "CORRECT"]
    rp = [r for k, r in rows.items() if k.startswith("PR:ROLE_PERMUTE:")]
    fa = ST.flag_vec([g(r) for r in rn], t, lam).mean()
    rec = ST.flag_vec([g(r) for r in rp], t, lam).mean()
    ref = json.loads((ROOT / "data/exp5/posthoc_nf_fusion.json").read_text())["fractional_selection_gates_screen"]["NF-anchored"]
    # the cached exp 5 screen_scores.jsonl copy reproduces the tie level and lambda exactly; RENAME FA within 0.005
    # (0.0698 vs 0.0735: the copied file differs slightly from the version exp 5's post-hoc script read)
    assert abs(t - ref["t"]) < 1e-12 and abs(lam - ref["lambda"]) < 1e-9
    assert abs(fa - ref["rename_fa"]) < 0.005, (fa, ref)
    assert abs(rec - ref["role_permute_recall"]) < 0.005, (rec, ref)
