#!/usr/bin/env python3
# NOTE (published copy): this file names server paths this repository
# does not publish (a stage it does not ship, or another run's workspace),
# so the steps that read them will not run from a clone as written:
#   /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5
"""Testing plan 6: (1) every file of exp5src/src is byte-identical to iter_2 exp 5 src (sha256); (2) the copied
pool_scoring.score_sentence with exp-5's frozen scoring_params reproduces the stored exp-5 c_score_align and p_peer_text
of dataset-E rows (sentences chosen by sha1 order among L25, until >= 50 rows). -> e2b/exp5_repro_check.json"""
import hashlib
import json
import sys
import time
from pathlib import Path

WS = Path(__file__).resolve().parents[1]
X5 = WS / "exp5src"
ORIG = Path("/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5")
sys.path.insert(0, str(X5 / "src"))
sys.path.insert(0, str(X5 / "src" / "vendor_a"))
sys.setrecursionlimit(10000)
import os  # noqa: E402
os.environ.setdefault("NLTK_DATA", str(X5 / "data" / "nltk_data"))


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def jl(p):
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()]


def main():
    files = {}
    for p in sorted((ORIG / "src").rglob("*.py")):
        rel = p.relative_to(ORIG)
        c = X5 / rel
        files[str(rel)] = {"orig": sha(p), "copy": sha(c) if c.exists() else None}
    ident = all(v["orig"] == v["copy"] for v in files.values())
    import peer_text as PT
    import pool_scoring as PS
    import fol_triage as FT  # warm the text-side imports (cold nltk/spaCy import > 30 s pair alarm here)
    FT.nlp()
    PS.init_worker(6.0)
    pre = json.loads((X5 / "results" / "prereg.json").read_text())
    P = dict(pre["scoring_params"])
    reduced = "--reduced" in sys.argv
    if reduced:  # E2-A / E2-B production params: auxiliary readouts off
        P.update(variants=["ALIGN"], k6_seeds=0, famfield=False, medoid_budget_s=0)
    fam_v = pre["family_map_vendor"]
    blind = jl(ORIG / "data" / "E_blind.jsonl")
    stored = {r["row_key"]: r for r in jl(ORIG / "results" / "per_item_E.jsonl")}
    q = {(r["text"], r["cond"]): r["q"] for r in jl(ORIG / "results" / "E_l3_q.jsonl") if r.get("coverage_status") == "OK"}
    by = {}
    for r in blind:
        by.setdefault(r["sentence_id"], []).append(r)
    sids = sorted([s for s, rs in by.items() if rs[0]["strata"]["source_stratum"] == "L25"], key=lambda s: hashlib.sha1(s.encode()).hexdigest())
    checked, t0 = [], time.time()
    for sid in sids:
        rs = by[sid]
        t = {"sentence_id": sid, "text": rs[0]["text"], "q": q.get((rs[0]["text"], "orig")),
             "rows": [{"key": r["row_key"], "fol": r["candidate_fol"], "family": fam_v[r["slot"]], "family_field": r["family"],
                       "system": r["system"], "is_peer": r["system_class"] == "llm"} for r in rs]}
        res = PS.score_sentence(t, P)
        for r in res["rows"]:
            st = stored[r["key"]]
            feats = dict(r)
            feats["coverage_status"] = r.get("coverage_status")
            pt = PT.fused_score(pre["frozen"], feats)["p_error"] if r.get("coverage_status") == "OK" else 1.0
            checked.append({"row_key": r["key"], "c_new": r.get("c_score_align"), "c_stored": st.get("c_score_align"),
                            "pt_new": pt, "pt_stored": st.get("p_peer_text")})
        if len(checked) >= 50:
            break
    def eq(a, b):
        return (a is None and b is None) or (a is not None and b is not None and abs(a - b) < 1e-9)
    n_c = sum(eq(c["c_new"], c["c_stored"]) for c in checked)
    n_p = sum(eq(c["pt_new"], c["pt_stored"]) for c in checked)
    out = {"files_identical": ident, "n_files": len(files), "files": files, "n_rows": len(checked), "c_score_align_exact_matches": n_c,
           "p_peer_text_exact_matches": n_p, "secs": round(time.time() - t0, 1), "rows": checked}
    out["params"] = P
    (WS / "e2b" / ("exp5_repro_check_reduced_params.json" if reduced else "exp5_repro_check.json")).write_text(json.dumps(out, indent=1))
    print(json.dumps({k: out[k] for k in ("files_identical", "n_files", "n_rows", "c_score_align_exact_matches", "p_peer_text_exact_matches", "secs")}))


if __name__ == "__main__":
    main()
