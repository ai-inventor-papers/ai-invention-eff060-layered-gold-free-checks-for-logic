#!/usr/bin/env python3
"""A2/A3 (LABEL-FREE, sealed): score every dataset-E row with V0_rep, c_exact, V1, V2, V3, V5 (+ 3-pool plain c) from
eval-2's pairwise matrix using freeze/consensus_variants.py. Reads ONLY the ALLOWED_INPUTS (asserted + hashed in the log).
Writes results/scores_E_variants.jsonl, results/family_weights.json, results/gate_G1_labelfree.json and
prereg_improve_addendum.json (sha256 seal of the scores, written before any label join)."""
from __future__ import annotations

import json
import sys

import numpy as np

from common import FREEZE, MATRIX, NEUTRAL_C, RES, ROOT, jdump, jl, sha1, sha256_file, setup_logger, utc

sys.path.insert(0, str(FREEZE))
import consensus_variants as CV  # noqa: E402

logger = setup_logger("score_variants")
ALLOWED_INPUTS = [MATRIX, RES / "row_index_labelfree.jsonl", FREEZE / "consensus_variants.py"]


def fold_of_sid(sid: str) -> int:
    return int(sha1("E_folds_v1|" + sid), 16) % 5


@logger.catch(reraise=True)
def main():
    hashes = {str(p): sha256_file(p) for p in ALLOWED_INPUTS}
    logger.info(f"allowed inputs: {json.dumps(hashes)}")
    rows = jl(RES / "row_index_labelfree.jsonl")
    recs = jl(MATRIX)
    assert len(recs) == 700
    IX = {r["sentence_id"]: CV.build_index(r) for r in recs}
    fold = {}
    for r in rows:
        f = fold_of_sid(r["sentence_id"])
        assert f == r["fold_E"], (r["sentence_id"], f, r["fold_E"])
        fold[r["sentence_id"]] = f
    for sid in IX:
        fold.setdefault(sid, fold_of_sid(sid))
    # V2 weights per holdout fold + full-E
    idx_list = [IX[s] for s in sorted(IX)]
    W = {k: CV.family_weights(idx_list, fold, k) for k in range(5)}
    W_full = CV.family_weights(idx_list, fold, None)
    jdump({"per_fold_holdout": {str(k): v for k, v in W.items()}, "full_E": W_full, "shrink": CV.SHRINK,
           "note": "w^(k) estimated on sentences NOT in fold k; applied to rows of fold k"}, RES / "family_weights.json")
    logger.info(f"full-E family weights {json.dumps({k: round(v, 4) for k, v in W_full.items()})}")
    out = []
    n_mis = n_cmp = 0
    mism = []
    for r in rows:
        rk, sid = r["exp5_row_key"], r["sentence_id"]
        ix = IX.get(sid)
        rec = {"row_key": rk, "canonical_key": r["canonical_key"], "sentence_id": sid, "fold": fold[sid],
               "stratum": r["source_stratum"], "family": r["family"], "V0_frozen": r["c_score_align"]}
        in_mx = ix is not None and rk in ix["node_of"]
        rec["in_matrix"] = in_mx
        if not in_mx:
            rec.update(V0_rep=1.0, c_exact=1.0, V1=1.0, V2=1.0, V3=1.0, V5=1.0, c3_plain=1.0, n_peers=0, n_peers_3pool=0,
                       coverage_status="UNPARSEABLE")
        else:
            P = CV.peers_lofo(ix, rk)
            P3 = CV.peers_lofo(ix, rk, families=CV.POOL3)
            w = W[fold[sid]]
            rec.update(n_peers=len(P), n_peers_3pool=len(P3), coverage_status="OK" if len(P) >= 2 else "PEER_UNAVAILABLE",
                       V0_rep=CV.c_score_align(ix, rk, P), c_exact=CV.c_exact(ix, rk, P), V1=CV.c_pn(ix, rk, P),
                       V2=CV.c_rw(ix, rk, w, P), V3=CV.c_pn_rw(ix, rk, w, P), V5=CV.c_v5(ix, rk, w),
                       c3_plain=(CV.c_score_align(ix, rk, P3, min_peers=1)))
            rec["V5_imputed"] = rec["V5"] is None
            if rec["V5"] is None:
                rec["V5"] = NEUTRAL_C
            if rec["c3_plain"] is None:
                rec["c3_plain"] = NEUTRAL_C
        if rec["V0_rep"] is not None and rec["V0_frozen"] is not None:
            n_cmp += 1
            if abs(rec["V0_rep"] - rec["V0_frozen"]) > 1e-6:  # per_item_T1 stores 6 decimals
                n_mis += 1
                mism.append({"row_key": rk, "rep": rec["V0_rep"], "frozen": rec["V0_frozen"], "n_peers": rec["n_peers"]})
        out.append(rec)
    g1 = {"n_compared": n_cmp, "n_mismatch": n_mis, "mismatch_share": n_mis / n_cmp, "rule": "<= 0.005 of rows with |V0_rep - V0_frozen| > 1e-6 (the frozen column is rounded to 6 decimals)",
          "pass": n_mis / n_cmp <= 0.005, "mismatches": mism[:100],
          "n_rows_peer_unavailable": sum(r["coverage_status"] == "PEER_UNAVAILABLE" for r in out),
          "n_rows_unparseable": sum(r["coverage_status"] == "UNPARSEABLE" for r in out)}
    logger.info(f"G1 label-free part: {n_mis}/{n_cmp} = {n_mis / n_cmp:.4%} mismatch -> pass={g1['pass']}")
    jdump(g1, RES / "gate_G1_labelfree.json")
    sp = RES / "scores_E_variants.jsonl"
    with sp.open("w") as fh:
        for rec in out:
            fh.write(json.dumps(rec) + "\n")
    add = {"written_utc": utc(), "scores_file": "results/scores_E_variants.jsonl", "scores_sha256": sha256_file(sp),
           "family_weights_sha256": sha256_file(RES / "family_weights.json"), "allowed_inputs_sha256": hashes,
           "prereg_improve_sha256": (ROOT / "prereg_improve.sha256").read_text().split()[0],
           "note": "seal written BEFORE any label join (fit_v4.py / screen.py verify this hash)"}
    jdump(add, ROOT / "prereg_improve_addendum.json")
    logger.info(f"sealed scores sha256 {add['scores_sha256']}")
    if not g1["pass"]:
        raise SystemExit("G1 FAILED -> fallback F1")


if __name__ == "__main__":
    main()
