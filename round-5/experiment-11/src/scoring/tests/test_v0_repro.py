"""V0 reproduction: the frozen exp-5 score_sentence call path used by scoring/score_consensus.py (with its declared
param overrides) reproduces c_score_align and ALIGN:g_score of dataset-E rows (exp-5 results/per_item_E.jsonl) to 1e-9.
Reads E's label-free blind rows and E's stored SCORES only (never E labels)."""
import json, sys, hashlib
from pathlib import Path
WS = Path(__file__).resolve().parents[2]
E5 = Path("../../../../../round-2/experiment-5/src")
sys.path.insert(0, str(WS / "frozen" / "exp5" / "src"))
sys.path.insert(0, str(WS))


def test_v0_reproduces_E_rows():
    import pool_scoring as PS
    from scoring.score_consensus import params, FAM
    blind = [json.loads(l) for l in (E5 / "data" / "E_blind.jsonl").read_text().splitlines() if l.strip()]
    per = {}
    for l in (E5 / "results" / "per_item_E.jsonl").read_text().splitlines():
        r = json.loads(l); per[r["row_key"]] = (r.get("c_score_align"), r.get("g_score"))
    by = {}
    for r in blind:
        by.setdefault(r["sentence_id"], []).append(r)
    sids = sorted(by, key=lambda s: hashlib.sha1(s.encode()).hexdigest())[:3]
    P = params(); P["do_text"] = False
    PS.init_worker(8.0)
    n = 0
    for sid in sids:
        rs = by[sid]
        t = {"sentence_id": sid, "text": rs[0]["text"], "q": None,
             "rows": [{"key": r["row_key"], "fol": r["candidate_fol"], "family": FAM[r["slot"]], "family_field": r["family"],
                       "system": r["system"], "is_peer": r["system_class"] == "llm"} for r in rs]}
        out = PS.score_sentence(t, P)
        for o in out["rows"]:
            exp_c, exp_g = per[o["key"]]
            got_c, got_g = o.get("c_score_align"), o.get("ALIGN:g_score")
            if exp_c is None:
                assert got_c is None
            else:
                assert abs(got_c - exp_c) < 1e-9, (o["key"], got_c, exp_c)
                n += 1
            if exp_g is not None and got_g is not None:
                assert abs(got_g - exp_g) < 1e-9, (o["key"], "g", got_g, exp_g)
    print("reproduced rows:", n)
    assert n >= 20
