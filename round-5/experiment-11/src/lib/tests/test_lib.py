"""lib entry points reproduce the pipeline's sealed E2 scores (V0, PT, c_exact) on the first 4 E2 sentences."""
import json, sys
from collections import defaultdict
from pathlib import Path
WS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(WS / "lib"))
import nl2fol_metrics as M  # noqa: E402


def test_lib_matches_pipeline():
    cand = [json.loads(l) for l in (WS / "e2" / "candidates_E2_nolabels.jsonl").read_text().splitlines()]
    sc = {json.loads(l)["row_key"]: json.loads(l) for l in (WS / "scores_E2A.jsonl").read_text().splitlines()}
    q = {json.loads(l)["text"]: json.loads(l).get("q") for l in (WS / "cache" / "E2_l3_q.jsonl").read_text().splitlines()}
    by = defaultdict(list)
    for r in cand:
        by[r["sentence_id"]].append(r)
    n = 0
    for sid in sorted(by)[:4]:
        rs = by[sid]
        for r in rs:
            s = sc[r["row_key"]]
            if not s["parse_ok"] or s["c_score_align__imputed"]:
                continue
            peers = [(p["candidate_fol"], p["family"]) for p in rs if p["row_key"] != r["row_key"]]
            v0 = M.c_score_align(r["candidate_fol"], peers, family=r["family"])
            assert abs(v0 - s["c_score_align"]) < 1e-9, (r["row_key"], v0, s["c_score_align"])
            ce = M.c_exact(r["candidate_fol"], peers, family=r["family"])
            if s.get("c_exact") is not None:
                assert abs(ce - s["c_exact"]) < 1e-9, (r["row_key"], "exact", ce, s["c_exact"])
            n += 1
        r = [x for x in rs if sc[x["row_key"]]["parse_ok"]][0]
        pt = M.peer_text(r["text"], r["candidate_fol"], [(p["candidate_fol"], p["family"]) for p in rs if p["row_key"] != r["row_key"]],
                         family=r["family"], q=q.get(r["text"]))
        assert abs(pt["p_error"] - sc[r["row_key"]]["p_peer_text"]) < 1e-9
    assert n >= 20
