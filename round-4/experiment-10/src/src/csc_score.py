"""STAGE 6: label-blind scoring (CPU; ProcessPoolExecutor, spawn).

Per PERTURB row (5,402 = 4,234 mutants + 868 controls + 300 bases) and per exp-7 SIG row (2,210):
  CSC      c_csc (K3), c_csc_k4, c_csc_multi, c_csc_graded, majority    from CSC peers (data/peers_perturb_*.jsonl) if present
  SIGPROXY c_proxy_k3, c_proxy_k4, c_proxy_graded, proxy majority         from exp-7 SIG outputs of the same 4 families
  FREE3    c_free3_exact, c_free3_align (consensus_lib, as planned) + c_free3_lc (case-insensitive exact, CSC equality)
No operator / label field is read here (only keys, text, candidate, family, sentence id).
Output: results/scores_raw.jsonl (append, resumable by key).
Usage: python src/csc_score.py [--mini N]
"""
from __future__ import annotations

import json
import multiprocessing as mp
import os
import signal
import sys
import time
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from loguru import logger

SRC = Path(__file__).resolve().parent
ROOT = SRC.parent
DATA = ROOT / "data"
RES = ROOT / "results"
OUT = RES / "scores_raw.jsonl"
SLOT_MODEL = {"G4": "deepseek/deepseek-v3.2", "G6": "microsoft/phi-4", "G7": "openai/gpt-4.1-mini",
              "G2": "qwen/qwen3-235b-a22b-2507"}
GRADED_CAP_S = 90


def jl(p: Path) -> list[dict]:
    return [json.loads(x) for x in p.read_text().splitlines() if x.strip()] if p.exists() else []


class _Timeout(Exception):
    pass


def _alarm(signum, frame):  # noqa: ARG001
    raise _Timeout()


def _init_worker():
    for v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
        os.environ[v] = "1"
    sys.path.insert(0, str(SRC))
    sys.setrecursionlimit(20000)
    import csc_lib  # noqa: F401
    import consensus_lib  # noqa: F401


def _csc_block(L, text, cand, peers: list[dict] | None, prefix: str, with_multi: bool, with_graded: bool) -> dict:
    out = {}
    if not peers:
        return out
    r = L.consensus_score(text, cand, peers)
    out[f"c_{prefix}"] = r["c"]
    out[f"{prefix}_status"] = r["status"]
    out[f"{prefix}_per_peer"] = r["per_peer"]
    out[f"{prefix}_n_used"] = r["n_used"]
    out[f"{prefix}_n_unknown"] = r["n_unknown"]
    out[f"{prefix}_models"] = [p["model"] for p in peers]
    if with_multi:
        m = L.csc_multi_score(text, cand, peers)
        out[f"c_{prefix}_multi"] = m["c"]
        out[f"{prefix}_multi_n_alt"] = m.get("n_alt_endorse")
    if with_graded:
        t0 = time.time()
        signal.signal(signal.SIGALRM, _alarm)
        signal.alarm(GRADED_CAP_S)
        try:
            g = L.graded_consensus(text, cand, peers)
            out[f"c_{prefix}_graded"] = g.get("g")
            out[f"{prefix}_graded_status"] = g.get("status")
        except _Timeout:
            out[f"c_{prefix}_graded"] = None
            out[f"{prefix}_graded_status"] = "GRADED_TIMEOUT"
        finally:
            signal.alarm(0)
        out[f"{prefix}_graded_secs"] = round(time.time() - t0, 2)
    maj = L.peer_majority(peers)
    out[f"{prefix}_majority"] = maj["formula"]
    out[f"{prefix}_majority_status"] = maj["status"]
    out[f"{prefix}_n_classes"] = maj.get("n_classes")
    return out


def score_task(task: dict) -> dict:
    import csc_lib as L
    import consensus_lib as CL
    t0 = time.time()
    text, cand = task["text"], task["cand"]
    out = {"key": task["key"], "set": task["set"]}
    for arm in ("csc", "proxy", "local", "localbase"):
        if task.get(f"{arm}_k3"):
            out.update(_csc_block(L, text, cand, task[f"{arm}_k3"], arm, with_multi=True, with_graded=True))
        if task.get(f"{arm}_k4"):
            b = _csc_block(L, text, cand, task[f"{arm}_k4"], arm + "_k4", with_multi=False, with_graded=False)
            out.update({k: v for k, v in b.items() if not k.endswith("_majority")})
    t1 = time.time()
    f3 = task.get("free3") or []
    if f3:
        for mode in ("exact", "align"):
            try:
                r = CL.consensus_score(text, cand, f3, mode=mode)
                out[f"c_free3_{mode}"] = r["c_score"]
                out[f"free3_{mode}_status"] = r["status"]
                out[f"free3_{mode}_n"] = r["n_peers"]
            except Exception as ex:  # noqa: BLE001 - recorded, never silent
                out[f"c_free3_{mode}"] = None
                out[f"free3_{mode}_status"] = f"ERROR:{type(ex).__name__}"
        r = L.consensus_score(text, cand, f3)
        out["c_free3_lc"] = r["c"] if r["status"] == "OK" else None
        out["free3_lc_status"] = r["status"]
        maj = L.peer_majority(f3)
        out["free3_majority"] = maj["formula"]
        out["free3_majority_status"] = maj["status"]
    out["secs_csc"] = round(t1 - t0, 3)
    out["secs_free3"] = round(time.time() - t1, 3)
    return out


def _peer_dicts(fols_by_model: dict, models: list[str]) -> list[dict]:
    return [{"model": m, "fol": fols_by_model[m].get("fol"), "alt_fol": fols_by_model[m].get("alt_fol")}
            for m in models if m in fols_by_model]


def build_tasks() -> list[dict]:
    sys.path.insert(0, str(SRC))
    import csc_lib as L
    view = jl(DATA / "perturb_view.jsonl")
    free3 = json.loads((DATA / "free3_peers.json").read_text())
    # CSC peers (if any were generated)
    csc_peers = {}
    for f in ("peers_perturb_E.jsonl", "peers_perturb_R.jsonl"):
        for u in jl(DATA / f):
            csc_peers[(u["text"], u["sig_key"])] = {p["model"]: p for p in u["peers"] if p.get("status") == "ok"}
    # SIGPROXY peers: exp-7 SIG outputs of the four P families, per sentence
    proxy = defaultdict(dict)
    sig_rows = jl(DATA / "rcomp_sig_view.jsonl")
    for r in sig_rows:
        if r["slot"] in SLOT_MODEL:
            proxy[r["sentence_id"]][SLOT_MODEL[r["slot"]]] = {"fol": r["candidate_fol"] if r.get("parse_ok") else None,
                                                               "alt_fol": None}
    tasks = []
    for r in view:
        asg = L.peer_assignment(None)
        t = {"key": r["key"], "set": "PERTURB", "text": r["text"], "cand": r["candidate_fol"],
             "sentence_id": r["sentence_id"]}
        cp = csc_peers.get((r["text"], r["sig_key"]))
        if cp:
            t["csc_k3"] = _peer_dicts(cp, asg["k3"])
            t["csc_k4"] = _peer_dicts(cp, asg["k4"])
        if r["is_rcomp"] and r["sentence_id"] in proxy:
            t["proxy_k3"] = _peer_dicts(proxy[r["sentence_id"]], asg["k3"])
            t["proxy_k4"] = _peer_dicts(proxy[r["sentence_id"]], asg["k4"])
        fs = free3.get(r["sentence_id"])
        if fs:
            t["free3"] = [fs.get(s) for s in ("G4", "G6", "G7")]
        tasks.append(t)
    for r in sig_rows:
        asg = L.peer_assignment(r["family"])
        t = {"key": "SIG:" + r["row_key"], "set": "SIG", "text": r["text"], "cand": r["candidate_fol"] or "",
             "sentence_id": r["sentence_id"]}
        pr = proxy.get(r["sentence_id"], {})
        t["proxy_k3"] = _peer_dicts(pr, asg["k3"])
        if asg["k4"]:
            t["proxy_k4"] = _peer_dicts(pr, asg["k4"])
        tasks.append(t)
    return tasks


def build_local_tasks() -> list[dict]:
    """LOCAL2 secondary arm: each row of the 40 local bases scored against (i) the local peers cued with the ROW's own
    signature ('local') and (ii) the local peers cued with its BASE's signature ('localbase'; the within-sentence
    contrast term of Delta-anchor)."""
    view = jl(DATA / "perturb_view.jsonl")
    peers = {(u["text"], u["sig_key"]): u["peers"] for u in jl(DATA / "peers_local2.jsonl")}
    base_sig = {r["base_item_id"]: r["sig_key"] for r in view if r["fold"] == "BASE"}
    tasks = []
    for r in view:
        own = peers.get((r["text"], r["sig_key"]))
        bp = peers.get((r["text"], base_sig[r["base_item_id"]]))
        if own is None or bp is None:
            continue
        tasks.append({"key": r["key"], "set": "LOCAL2", "text": r["text"], "cand": r["candidate_fol"],
                      "sentence_id": r["sentence_id"],
                      "local_k3": [{"model": p["model"], "fol": p["fol"], "alt_fol": p["alt_fol"]} for p in own],
                      "localbase_k3": [{"model": p["model"], "fol": p["fol"], "alt_fol": p["alt_fol"]} for p in bp]})
    return tasks


def main(argv: list[str]) -> None:
    mini = int(argv[argv.index("--mini") + 1]) if "--mini" in argv else None
    local = "--local" in argv
    out_p = RES / ("scores_raw_mini.jsonl" if mini else ("scores_local2.jsonl" if local else "scores_raw.jsonl"))
    tasks = build_local_tasks() if local else build_tasks()
    if mini:
        view_keys = [t for t in tasks if t["set"] == "PERTURB"]
        sids = sorted({t["sentence_id"] for t in view_keys})[:mini]
        tasks = [t for t in tasks if t["sentence_id"] in set(sids)] + [t for t in tasks if t["set"] == "SIG"][:40]
        if out_p.exists():
            out_p.unlink()
    done = {json.loads(x)["key"] for x in out_p.read_text().splitlines() if x.strip()} if out_p.exists() else set()
    todo = [t for t in tasks if t["key"] not in done]
    # long candidates first (better load balance)
    todo.sort(key=lambda t: -len(t["cand"] or ""))
    nw = max(1, len(os.sched_getaffinity(0)) - 1)
    logger.info(f"scoring: {len(tasks)} tasks, {len(done)} done, {len(todo)} to do, {nw} workers")
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=nw, mp_context=mp.get_context("spawn"), initializer=_init_worker) as ex, \
            out_p.open("a") as fh:
        futs = {ex.submit(score_task, t): t["key"] for t in todo}
        for i, f in enumerate(as_completed(futs)):
            try:
                res = f.result()
            except Exception as e:  # noqa: BLE001
                logger.error(f"task {futs[f]} failed: {type(e).__name__}: {str(e)[:200]}")
                res = {"key": futs[f], "error": f"{type(e).__name__}: {str(e)[:200]}"}
            fh.write(json.dumps(res, ensure_ascii=False) + "\n")
            if (i + 1) % 200 == 0:
                fh.flush()
                el = time.time() - t0
                logger.info(f"scored {i + 1}/{len(todo)} in {el:.0f}s ({el / (i + 1):.2f}s/task; eta {(len(todo) - i - 1) * el / (i + 1) / 60:.1f} min)")
    logger.info(f"scoring done in {time.time() - t0:.0f}s -> {out_p}")


if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
    logger.add(ROOT / "logs" / "csc_score.log", rotation="30 MB", level="DEBUG")
    main(sys.argv)
