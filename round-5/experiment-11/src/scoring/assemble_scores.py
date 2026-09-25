#!/usr/bin/env python3
"""E2-A: assemble every LABEL-FREE score into scores_E2A.jsonl (one row per candidate row_key), then write score_seal.json.

Orientation: every score is higher = more likely ERROR. Conventions copied from exp-5 / T1:
  * unparseable candidate (T1 strict parse) -> 1.0 for every metric (COVERAGE view); flagged parse_ok = False;
  * parseable row with a missing consensus/text feature -> exp-5 frozen neutral value (flag <col>__imputed);
  * judge columns: 1 - p(faithful); missing judge -> None (judge comparisons are paired on rows where both exist).
Columns:
  c_score_align (V0, PRIMARY), p_peer_text (PT, frozen fusion), g_align, l2_bow, l3_z3, c_exact, c_pn (V1), c_rw (V2),
  c_pn_rw (V3), c_two (V4), c_v5 (V5), judge_cheap_{disg,orig} (flash-lite), judge_cheap2_{disg,orig} (nano),
  judge_local_qwen8b_{disg,orig}; pilot_* (the user's pilot structural metrics); n_peers_used, n_unknown_pairs; cost fields.
V2/V3/V5 family weights: frozen consensus_variants.family_weights, out-of-fold over E2's own sentences
(fold = sha1('E2_folds_v1|'+sentence_id) % 5), label-free. V4 coefficients from freeze_copy/selection.json (never refit).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import scoring.guard  # noqa: E402,F401
from scoring.common import CACHE, FROZEN, WS, by_sentence, candidates, jl, setup_log  # noqa: E402

import hashlib  # noqa: E402
import json  # noqa: E402
import time  # noqa: E402
from collections import Counter  # noqa: E402

from loguru import logger  # noqa: E402

sys.path.insert(0, str(FROZEN / "exp5" / "src"))
sys.path.insert(0, str(WS / "freeze_copy"))
PRE5 = json.loads((FROZEN / "exp5" / "results" / "prereg.json").read_text())
NEUTRAL = PRE5["imputation"]["neutral"]
OUT = WS / "scores_E2A.jsonl"


def fold_e2(sid: str) -> int:
    return int(hashlib.sha1(("E2_folds_v1|" + sid).encode()).hexdigest(), 16) % 5


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> None:
    setup_log("assemble_scores")
    import peer_text as PT
    import consensus_variants as CV
    frozen = PRE5["frozen"]
    cand = candidates()
    units = {u["key"]: u for u in jl(CACHE / "units_E2.jsonl")}
    cons = {}
    stats = {}
    for s in jl(CACHE / "consensus_sentences.jsonl"):
        stats[s["sentence_id"]] = s.get("stats", {})
        for r in s["rows"]:
            cons[r["key"]] = r
    exact = {}
    for s in jl(CACHE / "exact_E2.jsonl"):
        for r in s.get("rows", []):
            exact[r["key"]] = r
    judges = {}
    for name in ("judge_cheap", "judge_cheap2", "judge_local_qwen8b"):
        for r in jl(CACHE / f"{name}.jsonl"):
            if r.get("p") is not None:
                rk, cond = r["key"].rsplit("|", 1)
                judges[(rk, f"{name}_{cond}")] = r
    pilot = {r["key"]: r for r in jl(CACHE / "pilot_E2.jsonl")}
    # ---- variants V1-V5 + c_exact from the pairwise matrices (frozen freeze code)
    pw = {r["sentence_id"]: r for r in jl(CACHE / "pairwise_E2.jsonl") if "error" not in r}
    ix = {sid: CV.build_index(rec) for sid, rec in pw.items()}
    sel = json.loads((WS / "freeze_copy" / "selection.json").read_text())
    v4coef = sel.get("V4_coefficients_frozen")
    fold_of = {sid: fold_e2(sid) for sid in ix}
    W = {k: CV.family_weights(list(ix[s] for s in ix), fold_of, k) for k in range(5)}
    var = {}
    for sid, I in ix.items():
        w = W[fold_of[sid]]
        for rk in I["meta"]:
            if not I["meta"][rk].get("is_peer", True):
                continue
            ce = CV.c_exact(I, rk)
            ca = CV.c_score_align(I, rk)
            var[rk] = {"c_exact": ce, "c_align_pw": ca, "c_pn": CV.c_pn(I, rk), "c_rw": CV.c_rw(I, rk, w),
                       "c_pn_rw": CV.c_pn_rw(I, rk, w), "c_v5": CV.c_v5(I, rk, w),
                       "c_two": CV.c_two_channel(ce, ca, v4coef) if v4coef else None}
    n_imp = Counter()
    rows = []
    for c in cand:
        k = c["row_key"]
        u = units.get(k, {})
        po = bool(u.get("parse_ok"))
        s = cons.get(k, {})
        r = {"row_key": k, "item_id": c["item_id"], "sentence_id": c["sentence_id"], "stratum": c["stratum"], "slot": c["slot"],
             "system": c["system"], "family": c["family"], "pilot": c["pilot"], "words": c["words"], "word_bin": c["word_bin"],
             "exception_type": c["exception_type"], "text_conditions": c["text_conditions"], "fold_E2": fold_e2(c["sentence_id"]),
             "parse_ok": po, "consensus_coverage": s.get("coverage_status"), "n_peers_used": s.get("n_peers_used"),
             "n_unknown_align": s.get("ALIGN:n_unknown"), "gen_cost_usd": c["gen_cost_usd"]}
        feats = dict(s)
        for col, src in (("c_score_align", "c_score_align"), ("g_align", "ALIGN:g_score"), ("l2_bow", "l2_bow"), ("l3_z3", "l3_z3")):
            v = s.get(src)
            r[col + "__imputed"] = False
            if not po:
                r[col] = 1.0
            elif v is None:
                r[col] = NEUTRAL.get(src)
                r[col + "__imputed"] = True
                n_imp[col] += 1
            else:
                r[col] = float(v)
        if not po:
            r["p_peer_text"] = 1.0
        else:
            feats["coverage_status"] = "OK"
            r["p_peer_text"] = PT.fused_score(frozen, feats)["p_error"]
        vv = var.get(k, {})
        for col in ("c_exact", "c_pn", "c_rw", "c_pn_rw", "c_v5", "c_two", "c_align_pw"):
            r[col] = 1.0 if not po else vv.get(col)
        r["c_exact_z3direct"] = 1.0 if not po else exact.get(k, {}).get("c_exact")
        for jn in ("judge_cheap_disg", "judge_cheap_orig", "judge_cheap2_disg", "judge_cheap2_orig",
                   "judge_local_qwen8b_disg", "judge_local_qwen8b_orig"):
            j = judges.get((k, jn))
            r[jn] = 1.0 if not po else (None if j is None else 1.0 - float(j["p"]))
            r[jn + "_cost"] = (j or {}).get("cost")
            r[jn + "_share"] = (j or {}).get("n_rows_sharing")
        pm = pilot.get(k, {})
        for col in ("pilot_joint_conflict", "pilot_arity_incons", "pilot_shape_incons", "pilot_dangling", "pilot_rerun_jacc"):
            r[col] = None if not po else pm.get(col)  # the user's pilot metrics (T1 adaptation); unparseable rows are outside R_AB
        r["secs_consensus_sentence"] = stats.get(c["sentence_id"], {}).get("secs_total")
        rows.append(r)
    OUT.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    # reproduction cross-check: pairwise V0 vs exp-5 V0 (same eqmv; different pair caps -> report mismatches)
    mm = [r for r in rows if r["parse_ok"] and r["c_align_pw"] is not None and not r["c_score_align__imputed"]
          and abs(r["c_align_pw"] - r["c_score_align"]) > 1e-9]
    logger.info(f"scores_E2A: {len(rows)} rows; parseable {sum(r['parse_ok'] for r in rows)}; imputed {dict(n_imp)}; "
                f"V0 pairwise-vs-exp5 mismatches {len(mm)}")
    files = {"scores_E2A.jsonl": OUT, "e2/candidates_E2_nolabels.jsonl": WS / "e2" / "candidates_E2_nolabels.jsonl"}
    for d in ("scoring", "frozen", "freeze_copy"):
        for p in sorted((WS / d).rglob("*")):
            if p.is_file() and "__pycache__" not in str(p) and p.suffix in (".py", ".json", ".txt", ".sh", ".toml"):
                files[str(p.relative_to(WS))] = p
    for p in sorted(CACHE.glob("*.jsonl")):
        files[str(p.relative_to(WS))] = p
    seal = {"written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "written_ts": time.time(),
            "note": "label-free scores sealed BEFORE any E2 label is joined; verify with analysis/verify_score_seal.py",
            "n_rows": len(rows), "v0_pairwise_vs_exp5_mismatches": len(mm), "imputed": dict(n_imp),
            "sha256": {k: sha256(p) for k, p in files.items()}}
    (WS / "score_seal.json").write_text(json.dumps(seal, indent=1))
    logger.info(f"score_seal.json written ({len(files)} files hashed)")


if __name__ == "__main__":
    main()
