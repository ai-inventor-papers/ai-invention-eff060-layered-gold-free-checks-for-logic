#!/usr/bin/env python3
"""E2-B label-free eqmv pairwise matrix (eval-2 pairwise.py + consensus_mx.py, byte-identical copies in eval2src/,
vendored exp-5 code = exp5src/src, identical to eval-2's vendor_exp5) and the M1 frozen variants V1-V5 + c_exact from
freeze_copy/consensus_variants.py (copied, sha verified against the M1 marker).

  matrix   -> scores/pairwise_classes_E2B.jsonl   (one line per sentence: nodes, pairs, cliques; label-free)
  variants -> scores/variants_E2B.jsonl           (row_key -> c_exact, V1..V5, V0_matrix re-derivation for the G2-style check)
V2/V3/V5 weights: out-of-fold over E2-B's own sentences, fold = int(sha1('E2_folds_v1|'+sid),16) % 5, shrink 20.
V4: frozen E coefficients from freeze_copy/selection.json (never refit).
Run with exp5src/.venv/bin/python under the same open() guard as score_e2b.py."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import multiprocessing as mp
import sys
import time
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

WS = Path(__file__).resolve().parents[1]
for p in (WS / "exp5src" / "src", WS / "exp5src" / "src" / "vendor_c", WS / "eval2src", WS / "src"):
    sys.path.insert(0, str(p))
sys.setrecursionlimit(10000)
import score_e2b as S  # noqa: E402  (guard, helpers, logger)

logger = S.logger
SC = WS / "scores"


def fold_e2(sid: str) -> int:
    return int(hashlib.sha1(("E2_folds_v1|" + sid).encode()).hexdigest(), 16) % 5


def _work(task: dict) -> dict:
    import pairwise
    return pairwise.work(task)


def _init(mem_gb: float = 3.5) -> None:
    import pairwise
    pairwise.init_worker(mem_gb)


def cmd_matrix(a) -> None:
    import consensus_mx as CM
    import pairwise
    import z3
    outp = SC / "pairwise_classes_E2B.jsonl"
    done = {r["sentence_id"] for r in S.jl(outp)}
    by = defaultdict(list)
    for r in S.rows_all():
        by[r["sentence_id"]].append(r)
    tasks = []
    for sid, rs in by.items():
        if sid in done:
            continue
        tasks.append({"sentence_id": sid, "source_stratum": "L25", "words": rs[0]["words"], "n_conditions": rs[0]["n_conditions"],
                      "rows": [{"row_key": r["row_key"], "fol": r["candidate_fol"], "slot": r["slot"], "family": r["family_vendor"],
                                "family_field": r["family"], "system_class": "llm"} for r in rs],
                      "order": (rs[0]["e2b_batch"], rs[0]["batch_key"])})
    tasks.sort(key=lambda t: t["order"])
    zver = z3.get_version_string()
    csha = pairwise.code_sha() if (Path(pairwise.__file__).parent.parent / "vendor_exp5").exists() else "exp5src-vendored"
    logger.info(f"matrix: {len(tasks)} sentences, workers {a.workers}")
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=a.workers, mp_context=mp.get_context("spawn"), initializer=_init) as ex, outp.open("a") as fh:
        futs = {ex.submit(_work, t): t for t in tasks}
        for i, fu in enumerate(as_completed(futs)):
            t = futs[fu]
            try:
                m = fu.result()
            except Exception as e:  # noqa: BLE001 - logged; the sentence gets no matrix line (variants -> None)
                logger.error(f"matrix {t['sentence_id']} failed: {e}")
                continue
            line = CM.pairwise_class_line(CM.SentenceMatrix(m), zver, csha)
            line["secs_total"] = m.get("secs_total")
            fh.write(json.dumps(line, ensure_ascii=False) + "\n")
            fh.flush()
            if (i + 1) % 25 == 0:
                logger.info(f"matrix {i + 1}/{len(tasks)} {time.time() - t0:.0f}s")
    logger.info(f"matrix done {time.time() - t0:.0f}s")


def _load_cv():
    marker = json.loads((WS / "freeze_copy" / "CONSENSUS_FREEZE_READY.copy.json").read_text())
    p = WS / "freeze_copy" / "consensus_variants.py"
    assert S.sha256(p) == marker["V"]["consensus_variants_sha256"], "consensus_variants.py sha mismatch vs M1"
    sel_p = WS / "freeze_copy" / "selection.json"
    assert S.sha256(sel_p) == marker["V"]["selection_sha256"], "selection.json sha mismatch vs M1"
    spec = importlib.util.spec_from_file_location("consensus_variants", p)
    cv = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cv)
    return cv, json.loads(sel_p.read_text()), marker


def cmd_variants(a) -> None:
    cv, sel, marker = _load_cv()
    recs = S.jl(SC / "pairwise_classes_E2B.jsonl")
    idx = [cv.build_index(r) for r in recs]
    fold_of = {ix["sid"]: fold_e2(ix["sid"]) for ix in idx}
    W = {k: cv.family_weights(idx, fold_of, k) for k in range(5)}
    W_all = cv.family_weights(idx, fold_of, None)
    coefs = sel["V4_coefficients_frozen"]
    rows = S.rows_all()
    by_sid = {ix["sid"]: ix for ix in idx}
    out = []
    for r in rows:
        ix = by_sid.get(r["sentence_id"])
        rec = {"row_key": r["row_key"], "sentence_id": r["sentence_id"], "fold_E2": fold_e2(r["sentence_id"])}
        if ix is None:
            rec.update({k: None for k in ("c_exact", "V0_matrix", "V1", "V2", "V3", "V4", "V5")})
            rec["variants_status"] = "no_matrix"
        else:
            w = W[fold_of[r["sentence_id"]]]
            ce = cv.c_exact(ix, r["row_key"])
            ca = cv.c_score_align(ix, r["row_key"])
            rec.update({"c_exact": ce, "V0_matrix": ca, "V1": cv.c_pn(ix, r["row_key"]), "V2": cv.c_rw(ix, r["row_key"], w),
                        "V3": cv.c_pn_rw(ix, r["row_key"], w), "V5": cv.c_v5(ix, r["row_key"], w), "variants_status": "ok"})
            rec["V4_needs_V0"] = True  # V4 = c_two_channel(c_exact, V0 exp-5) computed in the scores assembly
        out.append(rec)
    (SC / "variants_E2B.jsonl").write_text("".join(json.dumps(x) + "\n" for x in out))
    meta = {"weights_oof_by_fold": W, "weights_all_E2B": W_all, "weights_E_reference": sel.get("V2_full_E_weights_reference"),
            "V4_coefficients_frozen": coefs, "winner": sel["winner"], "consensus_variants_sha256": S.sha256(WS / "freeze_copy" / "consensus_variants.py"),
            "selection_sha256": S.sha256(WS / "freeze_copy" / "selection.json"), "n_sentences_matrix": len(idx),
            "V5_families": sel.get("V5_families"), "V5_neutral_note": sel.get("V5_note")}
    (SC / "variants_meta_E2B.json").write_text(json.dumps(meta, indent=1))
    logger.info(f"variants: {len(out)} rows; winner {sel['winner']}; weights(all) {W_all}")


if __name__ == "__main__":
    S.install_guard()
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["matrix", "variants"])
    ap.add_argument("--workers", type=int, default=1)
    a = ap.parse_args()
    {"matrix": cmd_matrix, "variants": cmd_variants}[a.cmd](a)
