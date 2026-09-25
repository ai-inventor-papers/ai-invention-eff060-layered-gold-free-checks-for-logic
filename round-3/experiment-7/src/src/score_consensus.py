#!/usr/bin/env python3
"""S7a / S9: label-blind consensus scoring of R_COMP candidates (SIG or FREE). NEVER reads a label file.

Inputs: rcomp/raw/generations_sig.jsonl (SIG) or rcomp/raw/generations.jsonl (FREE), rcomp/work/rcomp_sentences.json
(text, template, and - SIG only - the signature, which is part of the SIG prompt, not a label), exp-5 frozen params.
Per sentence (one ProcessPool task, spawn, RLIMIT_AS 3.5 GB, SIGALRM per pair as in exp 5):
  c_score_sig  (SIG only) 1 - share of family-disjoint peers z3-equivalent to the candidate after canon_case
               (exact names; ms 5000; None -> not equal, counted in n_unknown_sig); off-signature peers count as not equal;
               None for an off-signature / unparseable candidate or |P_c| < 2.
  exp-5 pool_scoring.score_sentence with the FROZEN params (variants ALIGN + NF-anchored, k=5, tau 0.5, timeout 2000 ms,
               pair cap 30 s; text side, k6, medoid, famfield OFF): ALIGN:g_score, NF-anchored:g_score,
               NF-anchored:c_score_nf, c_score_align (eqmv), and c_score_hyb (vendor patch: ALIGN OR NF-anchored).
Peers: parseable few-shot rows (SIG: sig_v1; FREE: fewshot_v1) of a different vendor family (exp-5 family_map_vendor).
Zero-shot FREE rows are candidates only. Extra (non-peer) rows may be passed for the rename-invariance pass.

usage: score_consensus.py run --cond SIG|FREE [--stage mini|50|all] [--workers N]
       score_consensus.py rename [--workers N] [--max-rows N]   (S10.8, SIG CORRECT rows only; uses labels to SELECT rows)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import multiprocessing as mp
import os
import random
import sys
import time
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RC = ROOT / "rcomp"
RES = ROOT / "results"
for p in (ROOT / "src" / "vendor_x5", ROOT / "src", RC / "src_e"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
sys.setrecursionlimit(20000)

FEW = ["G1", "G1b", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9"]
PEER_VARIANT = {"SIG": "sig_v1", "FREE": "fewshot_v1"}
GEN_FILE = {"SIG": RC / "raw" / "generations_sig.jsonl", "FREE": RC / "raw" / "generations.jsonl"}


def jl(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []


def sha1(s: str) -> str:
    return hashlib.sha1(s.encode()).hexdigest()


def exp5_params() -> dict:
    pre = json.loads((ROOT / "src" / "vendor_x5" / "prereg_exp5.json").read_text())
    P = dict(pre["scoring_params"])
    P.update({"do_text": False, "k6_seeds": 0, "medoid_budget_s": 0, "famfield": False, "allpool": False, "codes": False,
              "hyb": True})
    return P, pre["family_map_vendor"]


def row_key(item_id: str, cond: str, slot: str, variant: str) -> str:
    return f"{item_id}|{cond}|{slot}" if cond == "SIG" else f"{item_id}|{cond}|{slot}|{variant}"


def build_tasks(cond: str) -> list[dict]:
    import select_sentences as ss
    _, fam_v = exp5_params()
    sents = {s["sentence_id"]: s for s in json.loads((RC / "work" / "rcomp_sentences.json").read_text())}
    last = {}
    for r in jl(GEN_FILE[cond]):
        if r["sentence_id"] not in sents:
            continue
        if cond == "FREE" and r["prompt_variant"] not in ("fewshot_v1", "zeroshot_v1"):
            continue
        if cond == "FREE" and r["slot"] == "F":
            continue
        last[(r["sentence_id"], r["slot"], r["prompt_variant"])] = r
    by = defaultdict(list)
    for r in last.values():
        if r.get("raw_output") is None:
            continue
        s = sents[r["sentence_id"]]
        iid = sha1(r["system"] + "|" + ss.norm(s["text"]) + "|" + r["raw_output"])[:16]
        by[r["sentence_id"]].append({"key": row_key(iid, cond, r["slot"], r["prompt_variant"]), "fol": r["candidate_fol"] or "",
                                     "family": fam_v[r["slot"]], "family_field": r["family"], "system": r["system"],
                                     "slot": r["slot"], "is_peer": r["prompt_variant"] == PEER_VARIANT[cond] and r["slot"] in FEW,
                                     "parse_ok": bool(r["parse_ok"])})
    tasks = []
    for sid, rows in by.items():
        s = sents[sid]
        tasks.append({"sentence_id": sid, "text": s["text"], "cond": cond, "template_id": s["template_id"],
                      "sent": {k: s[k] for k in ("sentence_id", "text", "reference_fol_weak", "reference_fol_strong",
                                                 "reading_converse", "lexicon_ids", "template_id")} if cond == "SIG" else None,
                      "rows": sorted(rows, key=lambda r: r["key"])})
    tasks.sort(key=lambda t: sha1(t["sentence_id"]))
    return tasks


def c_score_sig_rows(task: dict, pair_cap_s: int = 30) -> dict:
    """Exact-signature consensus. Returns {row_key: {...}} (the SIG-exact variant of consensus_exact)."""
    import label_sig as LS
    import pool_scoring as PS
    from fol import equivalent as feq  # rcomp labeller parser/z3 (identical file to the dataset-E parser)
    sent = task["sent"]
    canon = {}
    for r in task["rows"]:
        if not r["parse_ok"]:
            canon[r["key"]] = (None, "UNPARSEABLE")
            continue
        st, ast, _ = LS.canon_case(r["fol"], sent)
        canon[r["key"]] = ((LS._to_str(ast), ast) if ast is not None else None, st)
    cache = {}

    def eq(a, b):
        if a[0] == b[0]:
            return True
        k = (a[0], b[0]) if a[0] < b[0] else (b[0], a[0])
        if k not in cache:
            res, to = PS._with_alarm(pair_cap_s, feq, a[1], b[1], 5000)
            cache[k] = None if to else res
        return cache[k]
    pool = [r for r in task["rows"] if r["is_peer"] and r["parse_ok"]]
    out = {}
    for r in task["rows"]:
        t0 = time.time()
        c, st = canon[r["key"]]
        P_c = [p for p in pool if p["family"] != r["family"] and p["key"] != r["key"]]
        o = {"sig_status_scorer": st, "n_peers_sig": len(P_c)}
        if c is None or len(P_c) < 2:
            o["c_score_sig"] = None
        else:
            eqs = [eq(c, canon[p["key"]][0]) if canon[p["key"]][0] is not None else False for p in P_c]
            o["c_score_sig"] = 1 - sum(e is True for e in eqs) / len(P_c)
            o["n_unknown_sig"] = sum(e is None for e in eqs)
            o["n_peers_equal_sig"] = sum(e is True for e in eqs)
            o["peer_equal_sig"] = {p["slot"]: (e is True) for p, e in zip(P_c, eqs)}
        o["secs_sig"] = round(time.time() - t0, 4)
        out[r["key"]] = o
    return out


def init_scoring_worker(mem_gb: float = 3.5) -> None:
    """exp-5 worker init (RLIMIT_AS, SIGALRM handler) + warm the lazily imported modules BEFORE any per-pair alarm.
    PATCH iter3 exp7: a SIGALRM pair cap firing during a first, slow `import nltk` / wordnet load / pandas import left
    the module partially initialised in sys.modules and failed every later sentence of that worker (WORKER_FAIL)."""
    import pool_scoring as PS
    import nltk  # noqa: F401
    from nltk.corpus import wordnet as wn
    try:
        wn.synsets("dog")
    except LookupError:
        pass
    from nltk.stem import PorterStemmer  # noqa: F401
    import pandas  # noqa: F401
    import asyncio  # noqa: F401
    import scipy.ndimage  # noqa: F401
    import scipy.optimize  # noqa: F401
    import peer_text  # noqa: F401
    import label_sig  # noqa: F401
    import fol  # noqa: F401
    PS.init_worker(mem_gb)  # RLIMIT_AS + SIGALRM handler only after the warm imports (imports under the cap hit MemoryError)


def score_task(task: dict, params: dict) -> dict:
    import pool_scoring as PS
    t0 = time.time()
    res = {"sentence_id": task["sentence_id"], "cond": task["cond"], "rows": {}, "stats": {}}
    if task["cond"] == "SIG":
        ts = time.time()
        sig = c_score_sig_rows(task, params["pair_cap_s"])
        res["stats"]["secs_sig"] = round(time.time() - ts, 2)
        for k, v in sig.items():
            res["rows"].setdefault(k, {}).update(v)
    sent = {"sentence_id": task["sentence_id"], "text": task["text"], "q": None,
            "rows": [{"key": r["key"], "fol": r["fol"], "family": r["family"], "family_field": r["family_field"],
                      "system": r["system"], "is_peer": r["is_peer"] and r["parse_ok"]} for r in task["rows"]]}
    ps = PS.score_sentence(sent, params)
    for o in ps["rows"]:
        d = {k: v for k, v in o.items() if k not in ("key",) and not k.endswith("unit_codes")}
        res["rows"].setdefault(o["key"], {}).update(d)
    res["stats"].update(ps["stats"])
    res["stats"]["secs_total"] = round(time.time() - t0, 2)
    res["stats"]["n_rows"] = len(task["rows"])
    return res


def assert_testability(cond: str, t_start: float) -> None:
    if cond == "FREE" and os.environ.get("FREE_PREJOIN") == "1":
        return  # prereg S8: FREE declaration precedes the JOIN (enforced in analyse.py); scoring is label-blind
    p = RES / f"testability_{cond}.json"
    if not p.exists():
        raise SystemExit(f"{p.name} missing: testability must be declared before any {cond} score is computed")
    if p.stat().st_mtime >= t_start:
        raise SystemExit(f"{p.name} is newer than this scorer's start")


def run(cond: str, stage: str, workers: int, skip_guard: bool = False) -> None:
    from loguru import logger
    import pool_scoring as PS
    t_start = time.time()
    if not skip_guard:
        assert_testability(cond, t_start)
    params, _ = exp5_params()
    tasks = build_tasks(cond)
    outp = RES / f"scores_{cond}.jsonl" if not skip_guard else ROOT / "logs" / f"dryrun_scores_{cond}.jsonl"  # dry-run never touches results/
    done = {r["sentence_id"] for r in jl(outp)}
    sel = tasks[:5] if stage == "mini" else tasks[:50] if stage == "50" else tasks
    todo = [t for t in sel if t["sentence_id"] not in done]
    logger.info(f"[{cond}] {len(sel)} sentences selected, {len(todo)} to score; params {params}")
    secs = []
    with ProcessPoolExecutor(max_workers=workers, mp_context=mp.get_context("spawn"), initializer=init_scoring_worker,
                             initargs=(3.5,)) as ex, outp.open("a") as fh:
        futs = {ex.submit(score_task, t, params): t for t in todo}
        for i, fu in enumerate(as_completed(futs), 1):
            t = futs[fu]
            try:
                r = fu.result()
            except Exception as e:  # noqa: BLE001 - counted: every row of the sentence gets coverage_status WORKER_FAIL
                logger.error(f"[{cond}] sentence {t['sentence_id']} failed: {type(e).__name__}: {e}")
                r = {"sentence_id": t["sentence_id"], "cond": cond, "rows": {x["key"]: {"coverage_status": "WORKER_FAIL"} for x in t["rows"]},
                     "stats": {"error": str(e)[:300]}}
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
            fh.flush()
            secs.append(r["stats"].get("secs_total", 0))
            if i % 20 == 0:
                logger.info(f"[{cond}] {i}/{len(todo)} sentences, {time.time() - t_start:.0f}s wall, mean {sum(secs) / len(secs):.1f} cpu-s/sentence")
    logger.info(f"[{cond}] stage {stage} done in {time.time() - t_start:.0f}s wall")
    (RES / f"scores_{cond}_stage_{stage}.json").write_text(json.dumps({"wall_s": time.time() - t_start, "n": len(todo),
                                                                     "mean_cpu_s": (sum(secs) / len(secs)) if secs else None}))


# ------------------------------------------------------------------------------------------ S10.8 rename invariance
CONS, VOW = "bdfgklmnprtvz", "aeiou"


def rename_copies(fol: str, seed: str) -> list[tuple[str, str]]:
    """[(RENAME_NONCE, fol'), (RENAME_SYN, fol')?]: one predicate renamed everywhere (dataset-3 control renamer for SYN;
    a sha1-seeded nonce for NONCE). Meaning-preserving by construction (a consistent renaming)."""
    saved = list(sys.path)  # PATCH iter3 exp7: spawned workers inherit sys.path; rcomp/src/common.py must not shadow vendor_c/common.py
    sys.path.insert(0, str(RC / "src"))
    sys.path.insert(0, str(RC / "labeller"))
    try:
        return _rename_copies(fol, seed)
    finally:
        sys.path[:] = saved


def _rename_copies(fol: str, seed: str) -> list[tuple[str, str]]:
    from fol import parse
    from repair_census import symbols, rename
    import label_sig as LS
    e = parse(fol)
    Pe, _ = symbols(e)
    names = {p[0] for p in Pe}
    p = sorted(Pe, key=lambda q: sha1(seed + q[0]))[0]
    rng = random.Random(int(sha1("nonce|" + seed), 16))
    while True:
        nn = ("".join(rng.choice(CONS) + rng.choice(VOW) for _ in range(2)) + rng.choice(CONS)).capitalize()
        if nn not in names:
            break
    out = [("RENAME_NONCE", LS._to_str(rename(e, {p: nn}, {})))]
    try:
        import perturb as PB  # dataset-3 control renamer (WordNet mutual first-sense synonym)
        kind, _, e2 = PB.control_rename(e, seed)
        if kind == "RENAME_SYN":
            out.append(("RENAME_SYN", LS._to_str(e2)))
    except Exception:  # noqa: BLE001 - no synonym available -> no SYN copy for this row
        pass
    return out


def run_rename(workers: int, max_rows: int) -> None:
    """Score renamed copies of SIG CORRECT rows as EXTRA candidates (never peers) against the UNCHANGED pool."""
    from loguru import logger
    import pool_scoring as PS
    params, _ = exp5_params()
    labs = {r["row_key"]: r for r in jl(RES / "sig_labels.jsonl")}
    tasks = {t["sentence_id"]: t for t in build_tasks("SIG")}
    rows_by = defaultdict(list)
    cands = sorted([r for r in labs.values() if r["label"] == "CORRECT" and r["slot"] in FEW], key=lambda r: sha1("ren|" + r["row_key"]))
    if max_rows:
        cands = cands[:max_rows]
    for r in cands:
        for kind, f in rename_copies(r["candidate_fol"], r["row_key"]):
            rows_by[r["sentence_id"]].append((r, kind, f))
    outp = RES / "scores_rename_SIG.jsonl"
    done = {x["sentence_id"] for x in jl(outp)}
    new_tasks = []
    for sid, lst in rows_by.items():
        if sid in done:
            continue
        t = json.loads(json.dumps(tasks[sid]))
        for r, kind, f in lst:
            fam = next(x["family"] for x in t["rows"] if x["key"] == r["row_key"])
            t["rows"].append({"key": f"REN|{kind}|{r['row_key']}", "fol": f, "family": fam, "family_field": r["family"],
                              "system": r["system"], "slot": r["slot"], "is_peer": False, "parse_ok": True})
        new_tasks.append(t)
    logger.info(f"rename pass: {sum(len(v) for v in rows_by.values())} renamed copies over {len(new_tasks)} sentences")
    with ProcessPoolExecutor(max_workers=workers, mp_context=mp.get_context("spawn"), initializer=init_scoring_worker,
                             initargs=(3.5,)) as ex, outp.open("a") as fh:
        futs = {ex.submit(score_task, t, params): t for t in new_tasks}
        for fu in as_completed(futs):
            t = futs[fu]
            try:
                r = fu.result()
            except Exception as e:  # noqa: BLE001
                logger.error(f"rename sentence {t['sentence_id']} failed: {e}")
                continue
            r["rows"] = {k: v for k, v in r["rows"].items() if k.startswith("REN|")}
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
            fh.flush()
    logger.info("rename pass done")


def main():
    from loguru import logger
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
    logger.add(ROOT / "logs" / "score_consensus.log", rotation="30 MB", level="DEBUG")
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["run", "rename"])
    ap.add_argument("--cond", choices=["SIG", "FREE"], default="SIG")
    ap.add_argument("--stage", choices=["mini", "50", "all"], default="all")
    ap.add_argument("--workers", type=int, default=24)
    ap.add_argument("--max-rows", type=int, default=0)
    ap.add_argument("--skip-guard", action="store_true", help="timing dry-run into a scratch file only")
    a = ap.parse_args()
    if a.cmd == "run":
        run(a.cond, a.stage, a.workers, a.skip_guard)
    else:
        run_rename(a.workers, a.max_rows)


if __name__ == "__main__":
    main()
