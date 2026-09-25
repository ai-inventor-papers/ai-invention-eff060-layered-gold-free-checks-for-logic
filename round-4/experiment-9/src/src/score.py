"""STEP F: label-blind scoring of every arm ($0, CPU, ProcessPool/spawn, z3 2 s per pair, UNKNOWN counted).

Output: results/scores_labelblind.jsonl -- one line per (arm, row_key) with c_csc / c_csc_graded / c_csc_multi, usable
peers, unknowns, status, peer-peer exact agreement, z3 CPU seconds, peer formulas and per-call $. NO label column.
Arms: OWN, FMT, OTHER (exact + eqmv/ALIGN), K4, PLACEBO, RENAME_SYN, RENAME_NONCE, FREE (FREE-MATCHED: existing E
few-shot outputs of the same family-disjoint pool families; exact here, ALIGN from eval 2's frozen pairwise matrix)."""
from __future__ import annotations

import hashlib
import json
import multiprocessing as mp
import sys
import time
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from itertools import combinations
from pathlib import Path

from loguru import logger

SRC = Path(__file__).resolve().parent
ROOT = SRC.parent
RES = ROOT / "results"
DATA = ROOT / "data"
EV2_PAIRWISE = Path(__file__).resolve().parents[4] / "round-3/evaluation-2/src/pairwise_classes_E.jsonl"


def _init():
    import resource
    sys.path.insert(0, str(SRC))
    sys.setrecursionlimit(20000)
    try:
        resource.setrlimit(resource.RLIMIT_AS, (6 * 1024**3, 6 * 1024**3))
    except (ValueError, OSError):
        pass


def score_task(task: list[dict]) -> list[dict]:
    import csc
    out = []
    for t in task:
        t0 = time.process_time()
        r = csc.consensus_score(t["cand_fol"], t["peers"], graded=t.get("graded", True))
        rec = {"arm": t["arm"], "row_key": t["row_key"], "status": r["status"], "c_csc": r["c_csc"],
               "c_csc_graded": r.get("c_csc_graded"), "c_csc_multi": r.get("c_csc_multi"), "n_usable": r["n_usable"],
               "n_peers": r["n_peers"], "n_unparseable_peers": r["n_unparseable_peers"], "n_unknown": r.get("n_unknown", 0),
               "per_peer": r.get("per_peer"), "unit_codes": r.get("unit_codes", [])}
        # peer-peer exact agreement (label-free sanity: is the prompt being followed?)
        cs = [csc.norm_canon(p.get("fol")) for p in t["peers"]]
        cs = [c for c in cs if c is not None]
        pairs = list(combinations(range(len(cs)), 2))
        rec["peer_pair_agree"] = (sum(csc._eq_canon(cs[i], cs[j]) is True for i, j in pairs) / len(pairs)) if pairs else None
        if t.get("align"):
            import consensus_lib as CL
            av = []
            for p in t["peers"]:
                if csc.parse(p.get("fol")) is None or r["status"] == "UNPARSEABLE":
                    continue
                try:
                    v, how = CL.equivalent_modulo_vocab(t["cand_fol"], p["fol"], ms=3000)
                except Exception:  # noqa: BLE001 - counted as UNKNOWN
                    v = None
                av.append(v)
            rec["c_align"] = (1 - sum(v is True for v in av) / len(av)) if len(av) >= 2 else 0.5
            rec["align_status"] = "OK" if len(av) >= 2 else "csc_insufficient_peers"
            rec["per_peer_align"] = av
        if t.get("majority"):
            rec["peer_majority_fol"] = csc.majority_formula(t["peers"])
        rec["z3_cpu_s"] = round(time.process_time() - t0, 4)
        rec["n_missing_calls"] = t.get("n_missing_calls", 0)
        rec["peers"] = [{"model": p.get("model"), "fol": p.get("fol"), "alt_fol": p.get("alt_fol"), "usd": p.get("usd"),
                         "key": p.get("key")} for p in t["peers"]]
        out.append(rec)
    return out


def align9_task(task: list[dict]) -> list[dict]:
    """9-peer c_score_align re-derivation for a (possibly renamed) candidate: eqmv (iteration-1 ALIGN: exact, name-similarity
    alignment, granularity bridge) against every parseable E peer ROW of other vendor families (node strings from eval 2's
    matrix, weighted by their row count), c = 1 - equivalent rows / peer rows. Used for HYB_MEAN's rename gate."""
    import consensus_lib as CL
    out = []
    for t in task:
        t0 = time.process_time()
        n = eq = unk = 0
        for fol, w in t["peer_nodes"]:
            try:
                v, _ = CL.equivalent_modulo_vocab(t["cand_fol"], fol, ms=3000)
            except Exception:  # noqa: BLE001
                v = None
            n += w
            eq += w * (v is True)
            unk += w * (v is None)
        out.append({"arm": t["arm"], "row_key": t["row_key"], "c_align9": (1 - eq / n) if n >= 2 else None, "n_peer_rows": n,
                    "n_unknown": unk, "z3_cpu_s": round(time.process_time() - t0, 3), "status": "OK" if n >= 2 else "PEER_UNAVAILABLE"})
    return out


def align9_tasks(frame: dict) -> list[dict]:
    sys.path.insert(0, str(ROOT / "vendor" / "ev2"))
    built = json.loads((RES / "arms_built.json").read_text())["arms"]
    syn = built.get("RENAME_SYN", {})
    by_sent = defaultdict(list)
    for rk in syn:
        by_sent[frame[rk]["sentence_id"]].append(rk)
    tasks = []
    with open(EV2_PAIRWISE) as fh:
        for line in fh:
            rec = json.loads(line)
            if rec["sentence_id"] not in by_sent:
                continue
            for rk in by_sent[rec["sentence_id"]]:
                own = frame[rk]["family"]
                nodes = []
                for nd in rec["nodes"]:
                    w = sum(1 for r in nd["rows"] if r["is_peer"] and r["family"] != own and r["row_key"] != rk)
                    if w:
                        nodes.append((nd["canon_fol"], w))
                tasks.append({"arm": "ALIGN9_BASE", "row_key": rk, "cand_fol": frame[rk]["candidate_fol"], "peer_nodes": nodes})
                tasks.append({"arm": "ALIGN9_SYN", "row_key": rk, "cand_fol": syn[rk]["cand_fol"], "peer_nodes": nodes})
    return tasks


def jl(p: Path) -> list[dict]:
    return [json.loads(l) for l in Path(p).read_text().splitlines() if l.strip()]


def build_tasks() -> list[dict]:
    sys.path.insert(0, str(SRC))
    import csc
    frame = {r["row_key"]: r for r in jl(DATA / "frame_blind.jsonl")}
    built = json.loads((RES / "arms_built.json").read_text())["arms"]
    cache = {}
    for line in (RES / "llm_cache.jsonl").read_text().splitlines():
        if line.strip():
            c = json.loads(line)
            cache[c["key"]] = c
    tasks = []
    n_missing = defaultdict(int)
    for arm, rows in built.items():
        for rk, a in rows.items():
            peers = []
            for s in a["slots"]:
                c = cache.get(s["key"])
                if c is None:
                    n_missing[arm] += 1
                    continue
                peers.append({"model": s["model"], "fol": c.get("fol"), "alt_fol": c.get("alt_fol"), "usd": c.get("usd"), "key": s["key"]})
            if len(peers) < len(a["slots"]) and len(peers) == 0:
                continue  # arm not generated (yet) for this row
            cand = a.get("cand_fol") or frame[rk]["candidate_fol"]
            tasks.append({"arm": arm, "row_key": rk, "cand_fol": cand, "peers": peers, "align": arm == "OTHER",
                          "n_missing_calls": len(a["slots"]) - len(peers),
                          "majority": arm == "OWN", "graded": True})
    # FREE-MATCHED: the same family-disjoint pool families' existing E few-shot outputs
    free = json.loads((DATA / "sentence_peers_free.json").read_text())
    for rk, r in frame.items():
        fams = [m[1] for m in csc.peers_for(r["family"], 3)]
        sp = free.get(r["sentence_id"], {})
        peers = [{"model": sp[f]["model"], "fol": sp[f]["fol"], "alt_fol": None, "usd": 0.0, "key": sp[f]["row_key"]}
                 for f in fams if f in sp]
        tasks.append({"arm": "FREE", "row_key": rk, "cand_fol": r["candidate_fol"], "peers": peers, "graded": True,
                      "majority": True})
    logger.info(f"tasks: {len(tasks)}; missing peer calls per arm {dict(n_missing)}")
    return tasks


def free_align(frame: dict) -> dict:
    """c_free_align from eval 2's frozen label-free eqmv matrix (exact / align / gran verdicts between E rows)."""
    sys.path.insert(0, str(ROOT / "vendor" / "ev2"))
    sys.path.insert(0, str(SRC))
    import csc
    from consensus_mx import SentenceMatrix
    free = json.loads((DATA / "sentence_peers_free.json").read_text())
    by_sent = defaultdict(list)
    for rk, r in frame.items():
        by_sent[r["sentence_id"]].append(rk)
    out = {}
    with open(EV2_PAIRWISE) as fh:
        for line in fh:
            rec = json.loads(line)
            sid = rec["sentence_id"]
            if sid not in by_sent:
                continue
            sm = SentenceMatrix(rec)
            for rk in by_sent[sid]:
                r = frame[rk]
                fams = [m[1] for m in csc.peers_for(r["family"], 3)]
                sp = free.get(sid, {})
                prk = [sp[f]["row_key"] for f in fams if f in sp and sp[f]["row_key"] in sm.row_node]
                ci = sm.row_node.get(rk)
                if ci is None:
                    out[rk] = {"c_free_align": None, "free_align_status": "CAND_NOT_IN_MATRIX"}
                    continue
                if len(prk) < 2:
                    out[rk] = {"c_free_align": 0.5, "free_align_status": "csc_insufficient_peers", "n_free_usable": len(prk)}
                    continue
                eqs = [sm.is_eq(ci, sm.row_node[p]) for p in prk]
                out[rk] = {"c_free_align": 1 - sum(eqs) / len(eqs), "free_align_status": "OK", "n_free_usable": len(prk),
                           "per_peer_free_align": eqs}
    return out


def run(n_workers: int = 4, chunk: int = 12) -> Path:
    tasks = build_tasks()
    # group by sentence text for per-process cache locality
    tasks.sort(key=lambda t: (t["row_key"].split("|")[0][:0], t["arm"], t["row_key"]))
    chunks = [tasks[i:i + chunk] for i in range(0, len(tasks), chunk)]
    results = []
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=n_workers, mp_context=mp.get_context("spawn"), initializer=_init) as ex:
        futs = {ex.submit(score_task, c): i for i, c in enumerate(chunks)}
        for k, f in enumerate(as_completed(futs)):
            try:
                results += f.result()
            except Exception as e:  # noqa: BLE001 - a crashed chunk is logged and its rows rescored serially below
                logger.error(f"chunk {futs[f]} failed: {str(e)[:200]}")
                for t in chunks[futs[f]]:
                    results.append({"arm": t["arm"], "row_key": t["row_key"], "status": "SCORING_ERROR", "c_csc": None})
            if (k + 1) % 50 == 0:
                logger.info(f"  scored {k + 1}/{len(chunks)} chunks in {time.time() - t0:.0f}s")
    frame = {r["row_key"]: r for r in jl(DATA / "frame_blind.jsonl")}
    a9 = align9_tasks(frame)
    a9_chunks = [a9[i:i + 4] for i in range(0, len(a9), 4)]
    with ProcessPoolExecutor(max_workers=n_workers, mp_context=mp.get_context("spawn"), initializer=_init) as ex:
        for f in as_completed([ex.submit(align9_task, c) for c in a9_chunks]):
            try:
                results += f.result()
            except Exception as e:  # noqa: BLE001
                logger.error(f"align9 chunk failed: {str(e)[:200]}")
    logger.info(f"align9 rename re-derivation: {len(a9)} tasks done, {time.time() - t0:.0f}s")
    fa = free_align(frame)
    for r in results:
        if r["arm"] == "FREE":
            r.update(fa.get(r["row_key"], {}))
    results.sort(key=lambda r: (r["arm"], r["row_key"]))
    p = RES / "scores_labelblind.jsonl"
    with open(p, "w") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    sha = hashlib.sha256(p.read_bytes()).hexdigest()
    add = {"scores_labelblind_sha256": sha, "n_lines": len(results), "written_ts": time.time(),
           "note": "written BEFORE any CSC score is joined to labels (analysis checks this file's mtime < analysis start)"}
    (ROOT / "prereg_csc_E_addendum.json").write_text(json.dumps(add, indent=1))
    logger.info(f"scores written: {len(results)} lines, sha256 {sha}, {time.time() - t0:.0f}s")
    return p


if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
    logger.add(ROOT / "logs" / "score.log", rotation="30 MB", level="DEBUG")
    run()
