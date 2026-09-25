"""T3: consensus unit tests on a synthetic 4-family pool + regression of the vendored exp-5 c_score_align on dataset E.
Run: .venv/bin/python -m pytest tests/test_consensus_rcomp.py -q"""
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for p in (ROOT / "src" / "vendor_x5", ROOT / "src", ROOT / "rcomp" / "src_e"):
    sys.path.insert(0, str(p))
import consensus_rcomp as CR  # noqa: E402
import score_consensus as SC  # noqa: E402

X5 = Path(__file__).resolve().parents[4] / "round-2/experiment-5/src"
BASE = "∀x (Dog(x) ∧ Barks(x) ∧ ¬Young(x) → Loud(x))"
CONTRA = "∀x (¬Loud(x) → ¬(Dog(x) ∧ Barks(x) ∧ ¬Young(x)))"
MUT = "∀x (Dog(x) ∧ Barks(x) ∧ Young(x) → Loud(x))"


def test_identical_zero():
    assert CR.consensus_exact(BASE, [BASE, BASE, BASE]) == 0.0


def test_contrapositive_counts_equal():
    assert CR.consensus_exact(BASE, [CONTRA, BASE, CONTRA]) == 0.0


def test_mutant_one():
    assert CR.consensus_exact(MUT, [BASE, CONTRA, BASE]) == 1.0


def test_fewer_than_two_peers_none():
    assert CR.consensus_exact(BASE, [BASE]) is None


def _task(rows):
    return {"sentence_id": "syn", "text": "Every dog that barks and is not young is loud.", "cond": "SIG", "template_id": "T1",
            "sent": None, "rows": rows}


def _row(key, fol, fam, slot, peer=True):
    return {"key": key, "fol": fol, "family": fam, "family_field": fam, "system": slot, "slot": slot, "is_peer": peer, "parse_ok": True}


def test_family_disjoint_loo_and_hyb_bound():
    """Two meta rows never see each other; HYB agreement >= each component's (c_hyb <= min(c_align, c_nf))."""
    rows = [_row("a", BASE, "meta", "G1"), _row("b", MUT, "meta", "G1b"), _row("c", BASE, "qwen", "G2"),
            _row("d", CONTRA, "mistral", "G3"), _row("e", BASE, "openai", "G7")]
    params, _ = SC.exp5_params()
    import pool_scoring as PS
    out = PS.score_sentence({"sentence_id": "syn", "text": _task(rows)["text"], "q": None,
                             "rows": [{k: r[k] for k in ("key", "fol", "family", "family_field", "system", "is_peer")} for r in rows]}, params)
    by = {o["key"]: o for o in out["rows"]}
    assert by["a"]["n_peers_hyb"] == 3 and "b" not in by["a"]["peer_equal_align"]  # meta rows are not peers of each other
    assert by["b"]["c_score_align"] == 1.0 and by["a"]["c_score_align"] == 0.0
    for o in by.values():
        if o.get("c_score_hyb") is not None:
            assert o["c_score_hyb"] <= min(o["c_score_align"], o["NF-anchored:c_score_nf"]) + 1e-12


def test_exp5_c_score_align_regression():
    """c_score_align reproduces exp 5 (per_item_E.jsonl) to 1e-9 on 5 dataset-E rows (vendored-code regression)."""
    per = {}
    for l in (X5 / "results" / "per_item_E.jsonl").read_text().splitlines():
        r = json.loads(l)
        if r.get("c_score_align") is not None and r["strata"]["source_stratum"] == "CTRL":
            per[r["row_key"]] = r
    blind = [json.loads(l) for l in (X5 / "data" / "E_blind.jsonl").read_text().splitlines() if l.strip()]
    by = defaultdict(list)
    for r in blind:
        by[r["sentence_id"]].append(r)
    fam_v = json.loads((ROOT / "src" / "vendor_x5" / "prereg_exp5.json").read_text())["family_map_vendor"]
    params, _ = SC.exp5_params()
    import pool_scoring as PS
    checked = 0
    for sid in sorted({per[k]["sentence_id"] for k in per})[:5]:
        rs = by[sid]
        sent = {"sentence_id": sid, "text": rs[0]["text"], "q": None,
                "rows": [{"key": r["row_key"], "fol": r["candidate_fol"], "family": fam_v[r["slot"]], "family_field": r["family"],
                          "system": r["system"], "is_peer": r["system_class"] == "llm"} for r in rs]}
        out = {o["key"]: o for o in PS.score_sentence(sent, params)["rows"]}
        for r in rs:
            if r["row_key"] in per and out.get(r["row_key"], {}).get("c_score_align") is not None:
                assert abs(out[r["row_key"]]["c_score_align"] - per[r["row_key"]]["c_score_align"]) < 1e-9, r["row_key"]
                checked += 1
    assert checked >= 5
