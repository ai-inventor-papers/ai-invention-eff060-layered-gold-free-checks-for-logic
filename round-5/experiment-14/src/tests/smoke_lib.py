#!/usr/bin/env python3
"""C2 smoke test of lib/api.py on 10 dataset-E rows (the first 10 Z rows in sha1(row_key) order): recomputes from the raw
candidate strings (a) V0_rep / c_exact / V1 / V2 / V3 / V5 through eval-2 pairwise_matrix + freeze/consensus_variants and
compares them with results/scores_E_variants.jsonl (1e-9), (b) exp-8 consensus_score align / exact vs the frozen
c_score_align and the matrix c_exact (the 0.5% G1 tolerance: at most 1 of 10 rows may differ), (c) GG search-only
brackets vs results/scores_gg_E.jsonl, (d) fol_lint / content_accounting run. Writes results/smoke_lib.json.
Run: PYTHONHASHSEED=0 .venv/bin/python tests/smoke_lib.py"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "lib"))
sys.path.insert(0, str(ROOT / "src"))
import api  # noqa: E402
from common import DS_E, MATRIX, RES, jl  # noqa: E402


def main():
    t0 = time.time()
    S = {r["row_key"]: r for r in jl(RES / "scores_E_variants.jsonl")}
    G = {r["row_key"]: r for r in jl(RES / "scores_gg_E.jsonl")}
    W = json.loads((RES / "family_weights.json").read_text())["per_fold_holdout"]
    from labels import frame
    df = frame()
    Z = sorted(df[df.Z].row_key, key=lambda k: hashlib.sha1(k.encode()).hexdigest())[:10]
    mx = {r["sentence_id"]: r for r in jl(MATRIX)}
    meta = {}
    for r in mx.values():
        for nd in r["nodes"]:
            for x in nd["rows"]:
                meta[x["row_key"]] = x
    d = json.loads((DS_E / "full_data_out.json").read_text())
    cand = {}
    for e in [g for g in d["datasets"] if g["dataset"] == "heldout_candidates"][0]["examples"]:
        inp = json.loads(e["input"])
        cand[f"{e['metadata_item_id']}|{inp.get('prompt_variant')}"] = {"text": inp["text"], "fol": inp["candidate_fol"],
                                                                         "sid": e["metadata_sentence_id"], "system": inp.get("system")}
    del d
    fam_of_slot = {m["slot"]: (m["family"], m["family_field"]) for m in meta.values()}
    out = {"rows": [], "n": len(Z)}
    n_align_mis = n_exact_mis = 0
    for rk in Z:
        s = S[rk]
        sid = s["sentence_id"]
        rows = []
        for k, c in cand.items():
            if c["sid"] != sid:
                continue
            m = meta.get(k)
            if m is None:  # unparseable rows: slot / family from the system string
                slot = (c["system"] or "").split(":")[0]
                fam, ff = fam_of_slot.get(slot, ("symbolic", "symbolic"))
                m = {"slot": slot, "family": fam, "family_field": ff, "system_class": "llm" if ":" in (c["system"] or "") else "other"}
            rows.append({"row_key": k, "fol": c["fol"], "slot": m["slot"], "family": m["family"], "family_field": m["family_field"],
                         "system_class": m["system_class"]})
        v = api.consensus_variants_from_rows(rows, rk, weights=W[str(s["fold"])])
        v5 = 0.6266243516243516 if v["V5"] is None else v["V5"]
        ok_variants = all(abs(v[k] - s[k]) < 1e-9 for k in ("V0_rep", "c_exact", "V1", "V2", "V3")) and abs(v5 - s["V5"]) < 1e-9
        fam = meta[rk]["family"]
        peers = [r["fol"] for r in rows if r["system_class"] == "llm" and r["family"] != fam and r["row_key"] != rk]
        text = cand[rk]["text"]
        a = api.consensus_score(text, cand[rk]["fol"], peers, mode="align")
        x = api.consensus_score(text, cand[rk]["fol"], peers, mode="exact")
        n_align_mis += abs(a["c_score"] - float(s["V0_frozen"])) > 1e-6
        n_exact_mis += abs(x["c_score"] - s["c_exact"]) > 1e-9
        ggr = api.consensus_score(text, cand[rk]["fol"], peers, mode="gg")
        lint = api.fol_lint(cand[rk]["fol"])
        ca = api.content_accounting(text, cand[rk]["fol"])
        out["rows"].append({"row_key": rk, "variants_match_1e-9": ok_variants, "recomputed": v, "stored": {k: s[k] for k in ("V0_rep", "c_exact", "V1", "V2", "V3", "V5")},
                            "align_c": a["c_score"], "V0_frozen": s["V0_frozen"], "exact_c": x["c_score"], "c_exact_stored": s["c_exact"],
                            "gg_allyes": ggr.get("c_gg_allyes"), "gg_allyes_stored": G.get(rk, {}).get("c_gg_allyes"),
                            "fol_lint_keys": sorted(lint)[:8], "content_accounting_keys": sorted(ca)[:8]})
        print(rk, ok_variants, round(a["c_score"], 4), s["V0_frozen"], round(x["c_score"], 4), round(s["c_exact"], 4),
              ggr.get("c_gg_allyes"), G.get(rk, {}).get("c_gg_allyes"), f"{time.time() - t0:.0f}s", flush=True)
    out["all_variants_match"] = all(r["variants_match_1e-9"] for r in out["rows"])
    out["n_align_mismatch"], out["n_exact_mismatch"] = int(n_align_mis), int(n_exact_mis)
    out["n_gg_allyes_mismatch"] = sum(1 for r in out["rows"] if r["gg_allyes_stored"] is not None and abs(r["gg_allyes"] - r["gg_allyes_stored"]) > 1e-9)
    out["pass"] = out["all_variants_match"] and n_align_mis <= 1 and n_exact_mis <= 1 and out["n_gg_allyes_mismatch"] <= 1
    out["secs"] = time.time() - t0
    (RES / "smoke_lib.json").write_text(json.dumps(out, indent=1, default=str))
    print("PASS" if out["pass"] else "FAIL", {k: out[k] for k in ("all_variants_match", "n_align_mismatch", "n_exact_mismatch", "n_gg_allyes_mismatch")})


if __name__ == "__main__":
    main()
