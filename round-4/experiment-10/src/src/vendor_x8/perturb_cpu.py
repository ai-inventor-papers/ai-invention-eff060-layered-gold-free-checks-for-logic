#!/usr/bin/env python3
# NOTE (published copy): this file names server paths this repository
# does not publish (a stage it does not ship, or another run's workspace),
# so the steps that read them will not run from a clone as written:
#   /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_6
"""PART B label-free CPU metrics on every PERTURB unit (4,234 mutants + 868 controls = PT:<item_id>, 300 bases = PB:<base>).

  parse_fail        dataset-E parser (vendor_e.fol via peer_text.parse_fol): 1 if unparseable.
  pilot_*           the user's pilot structural metrics (exp 6 pilot_metrics.pilot_one VERBATIM). PERTURB rows are single
                    sentences, so -- exactly as exp 6 did on E -- the pilot 'document' is an artificial group: rows of the
                    same system (PERTURB:<op>:<pol> / CONTROL:<type> / BASE) and base source, sha1 bucket of ~20 bases;
                    story = the other parseable formulas of the document. pilot_rerun_jacc has no analogue (no reruns) -> NA.
  l2_bow            exp 5 l2_bow (content accounting of text vs formula), unchanged.
  l3_z3             exp 5 l3_z3 against the CACHED role questionnaire of the base sentence (data/exp5/E_l3_q.jsonl, $0);
                    R_COMP bases have no cached questionnaire -> NA (not run; see coverage_perturb.csv).
  p_peer_text       exp 5 frozen PEER+TEXT fusion (features ALIGN:g_score = g_align, c_score_align = c_align, l2_bow, l3_z3);
                    peer_unavailable (R_COMP bases, no peers) -> frozen TEXT-only model (pre-registered rule).
  p_text            exp 5 frozen TEXT-only model.
  sc5_local_*       SC-5 with exp 6's cached local Qwen3-8B samples of the SAME E sentence (results/scores/sc5_local_samples),
                    exp 6 scorer: eq_frac = #samples equivalent modulo vocabulary / 5 (oriented 1 - eq_frac), entropy of
                    the equivalence classes; E bases only (R_COMP sentences have no samples -> NA).
Consensus columns (c/g x align/nf/hyb) come from results/scores_E.jsonl (the pair engine run).
Output: results/perturb_scores/cpu.jsonl (key -> columns + statuses)
"""
from __future__ import annotations

import hashlib
import json
import multiprocessing as mp
import os
import sys
import time
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from loguru import logger

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
os.environ.setdefault("NLTK_DATA", str(ROOT / "data" / "nltk_data"))
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
E6 = Path("/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_6")
OUT = ROOT / "results" / "perturb_scores" / "cpu.jsonl"

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(ROOT / "logs" / "perturb_cpu.log", rotation="30 MB", level="DEBUG")


def jl(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []


def sha1(s: str) -> str:
    return hashlib.sha1(s.encode()).hexdigest()


def units() -> list[dict]:
    rows = jl(ROOT / "data" / "perturb_rows.jsonl")
    U, seen = [], set()
    for r in rows:
        U.append({"key": "PT:" + r["item_id"], "text": r["text"], "fol": r["candidate_fol"], "sentence_id": r["sentence_id"],
                  "base": r["base_item_id"], "system": r["system"], "src": "R_COMP" if r["base_source"].startswith("R_COMP") else "E"})
        if r["base_item_id"] not in seen:
            seen.add(r["base_item_id"])
            U.append({"key": "PB:" + r["base_item_id"], "text": r["text"], "fol": r["reference_fol"], "sentence_id": r["sentence_id"],
                      "base": r["base_item_id"], "system": "BASE", "src": "R_COMP" if r["base_source"].startswith("R_COMP") else "E"})
    return U


# ------------------------------------------------------------------------------------------------ workers
def _text_worker(chunk):
    import sys as _s
    _s.setrecursionlimit(20000)
    import peer_text as PT
    out = []
    for u, q in chunk:
        e = PT.parse_fol(u["fol"])
        r = {"key": u["key"], "parse_fail": int(e is None)}
        if e is not None:
            try:
                r.update({k: v for k, v in PT.l2_bow(u["text"], e).items() if k in ("l2_bow", "bow_n_unanch", "bow_uncarried")})
            except (RecursionError, KeyError, ValueError, TypeError, IndexError, AttributeError) as ex:
                r["l2_bow"], r["l2_err"] = None, str(ex)[:80]
            try:
                l3 = PT.l3_z3(q, e)
                r["l3_z3"] = l3["l3_z3"]
                r["l3_status"] = "ok" if q is not None else "no_questionnaire"
            except Exception as ex:  # noqa: BLE001 - z3/role-profile failure is a coverage failure, recorded
                r["l3_z3"], r["l3_status"] = None, f"fail:{str(ex)[:60]}"
        out.append(r)
    return out


def _pilot_worker(chunk):
    sys.path.insert(0, str(ROOT / "vendor_e6"))
    from src.pilot_metrics import pilot_one
    return [pilot_one(a) for a in chunk]


def _sc_worker(chunk):
    sys.path.insert(0, str(ROOT / "vendor_e6"))
    import sys as _s
    _s.setrecursionlimit(10000)
    from src.labeller.labeller import equivalent_modulo_vocab
    out = []
    for a, b in chunk:
        try:
            cls = equivalent_modulo_vocab(a, b, ms=2000, do_search=False)["cls"]
        except Exception as e:  # noqa: BLE001
            cls = f"EXC:{type(e).__name__}"
        out.append({"a": a, "b": b, "cls": cls, "eq": cls in ("EQUIV", "VOCAB", "GRAN")})
    return out


def workers() -> int:
    return max(1, len(os.sched_getaffinity(0)) - 2)


def run_pool(fn, items, chunk, label):
    t0 = time.time()
    chunks = [items[i:i + chunk] for i in range(0, len(items), chunk)]
    out = []
    with ProcessPoolExecutor(max_workers=workers(), mp_context=mp.get_context("spawn")) as ex:
        for i, res in enumerate(ex.map(fn, chunks)):
            out.extend(res)
            if (i + 1) % 20 == 0:
                logger.info(f"{label}: {i + 1}/{len(chunks)} chunks, {time.time() - t0:.0f}s")
    logger.info(f"{label}: {len(items)} items in {time.time() - t0:.0f}s")
    return out


@logger.catch(reraise=True)
def main():
    U = units()
    if len(sys.argv) > 1 and sys.argv[1] == "--mini":
        U = U[:40]
    logger.info(f"PERTURB units {len(U)}")
    # ---------------- text side (+ parse)
    q = {r["text"]: r["q"] for r in jl(ROOT / "data" / "exp5" / "E_l3_q.jsonl") if r.get("cond") == "orig" and r.get("coverage_status") == "OK"}
    T = run_pool(_text_worker, [(u, q.get(u["text"])) for u in U], 25, "text")
    res = {r["key"]: r for r in T}
    # ---------------- frozen fusion (needs consensus columns from scores_E)
    import peer_text as PT
    pre5 = json.loads((ROOT / "data" / "exp5" / "prereg.json").read_text())
    frozen = pre5["frozen"]
    cons = {}
    for s in jl(ROOT / "results" / "scores_E.jsonl"):
        for r in s["rows"]:
            if r["key"].startswith(("PT:", "PB:")):
                cons[r["key"]] = r
    for u in U:
        r = res[u["key"]]
        c = cons.get(u["key"], {})
        if r["parse_fail"]:
            r.update(p_peer_text=1.0, p_text=1.0, fusion_model="none")
            continue
        feats = {"ALIGN:g_score": c.get("g_align"), "c_score_align": c.get("c_align"), "l2_bow": r.get("l2_bow"),
                 "l3_z3": r.get("l3_z3"), "coverage_status": "OK", "peer_unavailable": c.get("c_align") is None}
        fs = PT.fused_score(frozen, feats)
        r.update(p_peer_text=fs["p_error"], fusion_model=fs["model_used"], p_text=PT.apply_logistic(frozen["text_only"], feats))
    # ---------------- pilot structural metrics (artificial documents)
    by_doc = defaultdict(list)
    for u in U:
        by_doc[(u["system"], u["src"], int(sha1(u["base"]), 16) % max(1, round(300 / 20)))].append(u)
    args = []
    for us in by_doc.values():
        ok = [v for v in us if res[v["key"]]["parse_fail"] == 0]
        for u in us:
            story = [v["fol"] for v in ok if v["key"] != u["key"]]
            args.append((u["key"], u["fol"] if res[u["key"]]["parse_fail"] == 0 else None, story, [], True))
    P = run_pool(_pilot_worker, args, 10, "pilot")
    for p in P:
        r = res[p["key"]]
        for c in ("pilot_joint_conflict", "pilot_arity_incons", "pilot_shape_incons", "pilot_dangling"):
            r[c] = p.get(c)
        r["pilot_rerun_jacc"] = None
        r["pilot_status"] = "unparseable" if p.get("parse_fail") else ("z3_fail" if p.get("pilot_joint_conflict") is None else "ok")
    # ---------------- SC-5 local (exp 6 cached samples of the same E sentence)
    samp = {r["key"]: r for r in jl(E6 / "results" / "scores" / "sc5_local_samples.jsonl")}
    sys.path.insert(0, str(ROOT / "vendor_e6"))
    from src.labeller.labeller import parse_ok
    from src.consensus_min import sc_scores_one
    samp_ok = {s: [f if (f and parse_ok(f)) else None for f in r["samples"]] for s, r in samp.items()}
    cache = {}
    for r in jl(E6 / "results" / "sc_pair_cache_sc5_local_samples.jsonl"):
        cache[(sha1(r["a"]), sha1(r["b"]))] = r["eq"]
    pairs = set()
    for u in U:
        smp = samp_ok.get(u["sentence_id"])
        if smp is None or res[u["key"]]["parse_fail"]:
            continue
        for f in smp:
            if f and f != u["fol"] and (sha1(u["fol"]), sha1(f)) not in cache and (sha1(f), sha1(u["fol"])) not in cache:
                pairs.add((u["fol"], f))
    logger.info(f"SC pairs to compute: {len(pairs)}")
    for r in run_pool(_sc_worker, sorted(pairs), 20, "sc5"):
        cache[(sha1(r["a"]), sha1(r["b"]))] = r["eq"]

    def eq(a, b):
        if a == b:
            return True
        return bool(cache.get((sha1(a), sha1(b)), cache.get((sha1(b), sha1(a)), False)))
    for u in U:
        r = res[u["key"]]
        smp = samp_ok.get(u["sentence_id"])
        if r["parse_fail"]:
            r.update(sc5_local_eq_frac=1.0, sc5_local_entropy=None, sc5_status="unparseable")
        elif smp is None:
            r.update(sc5_local_eq_frac=None, sc5_local_entropy=None, sc5_status="no_samples")
        else:
            s = sc_scores_one(u["fol"], smp, eq)
            r.update(sc5_local_eq_frac=1.0 - s["sc5_eq_frac"], sc5_local_entropy=s["sc5_entropy"], sc5_status="ok")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w") as fh:
        for u in U:
            fh.write(json.dumps(res[u["key"]], ensure_ascii=False) + "\n")
    logger.info(f"wrote {len(U)} rows to {OUT}")


if __name__ == "__main__":
    main()
