"""Resumable, parallel caches for the two expensive primitives: pairwise eqmv and LABEL(cand, ref).

pairwise_eq.jsonl  {"a", "b", "eq": true|false|null, "route", "secs"}   (a <= b, formula strings)
label_cache.jsonl  {"cand", "ref", ...label fields...}
"""
from __future__ import annotations

import json
import multiprocessing as mp
import sys
import time
from pathlib import Path

from loguru import logger

ROOT = Path(__file__).resolve().parent.parent
PAIR_F = ROOT / "results" / "pairwise_eq.jsonl"
LABEL_F = ROOT / "results" / "label_cache.jsonl"


def key(a: str, b: str) -> tuple[str, str]:
    a, b = a.strip(), b.strip()
    return (a, b) if a <= b else (b, a)


def _pair_worker(chunk: list[tuple[str, str]]) -> list[dict]:
    sys.path.insert(0, str(ROOT / "src"))
    sys.setrecursionlimit(10000)
    from common import eqmv, safe_parse
    out = []
    for a, b in chunk:
        t0 = time.time()
        ea, eb = safe_parse(a), safe_parse(b)
        if ea is None or eb is None:
            eq, route = None, "unparseable"
        elif a == b:
            eq, route = True, "identical"
        else:
            try:
                eq, route = eqmv(ea, eb)
            except (RecursionError, ValueError, KeyError, TypeError) as e:
                eq, route = None, f"error:{type(e).__name__}"
        out.append({"a": a, "b": b, "eq": eq, "route": route, "secs": round(time.time() - t0, 3)})
    return out


def _label_worker(chunk: list[tuple[str, str, float]]) -> list[dict]:
    sys.path.insert(0, str(ROOT / "src"))
    sys.setrecursionlimit(10000)
    from common import label
    out = []
    for cand, ref, budget in chunk:
        t0 = time.time()
        try:
            lab = label(cand, ref, budget_s=budget)
        except (RecursionError, ValueError, KeyError, TypeError) as e:
            lab = {"label": "LABEL_ERROR", "auto_class": f"error:{type(e).__name__}", "repair_ops": [], "vocab_strict": None, "pmap": {}}
        lab.update(cand=cand, ref=ref, secs=round(time.time() - t0, 2))
        out.append(lab)
    return out


def _load(f: Path) -> list[dict]:
    if not f.exists():
        return []
    rows = []
    for l in f.read_text().splitlines():
        if l.strip():
            try:
                rows.append(json.loads(l))
            except json.JSONDecodeError:
                logger.warning("skipping a truncated cache line")
    return rows


class PairCache:
    def __init__(self):
        self.d = {(r["a"], r["b"]): r for r in _load(PAIR_F)}

    def get(self, a: str, b: str) -> dict | None:
        k = key(a, b)
        if k[0] == k[1]:  # identical formula strings are trivially equivalent (never sent to the workers)
            return {"a": k[0], "b": k[1], "eq": True, "route": "identical", "secs": 0.0}
        return self.d.get(k)

    def eq(self, a: str, b: str):
        r = self.get(a, b)
        return None if r is None else r["eq"]

    def compute(self, pairs, workers: int = 4, chunk: int = 20, tag: str = ""):
        todo = sorted({key(a, b) for a, b in pairs if a and b} - set(self.d))
        if not todo:
            return
        logger.info(f"[{tag}] eqmv pairs to compute: {len(todo)} (cached {len(self.d)})")
        chunks = [todo[i:i + chunk] for i in range(0, len(todo), chunk)]
        t0 = time.time()
        with mp.get_context("spawn").Pool(workers) as pool, open(PAIR_F, "a") as f:
            for i, res in enumerate(pool.imap_unordered(_pair_worker, chunks)):
                for r in res:
                    self.d[(r["a"], r["b"])] = r
                    f.write(json.dumps(r, ensure_ascii=False) + "\n")
                if (i + 1) % 50 == 0:
                    f.flush()
                    el = time.time() - t0
                    logger.info(f"[{tag}] {i + 1}/{len(chunks)} chunks, {el:.0f}s, eta {el / (i + 1) * (len(chunks) - i - 1):.0f}s")
        logger.info(f"[{tag}] done in {time.time() - t0:.0f}s")


class LabelCache:
    def __init__(self):
        self.d = {(r["cand"], r["ref"]): r for r in _load(LABEL_F)}

    def get(self, cand: str, ref: str) -> dict | None:
        return self.d.get((cand.strip(), ref.strip()))

    def compute(self, pairs, workers: int = 4, budget: float = 25.0, tag: str = ""):
        todo = sorted({(c.strip(), r.strip()) for c, r in pairs if r} - set(self.d))
        if not todo:
            return
        logger.info(f"[{tag}] labels to compute: {len(todo)}")
        chunks = [[(c, r, budget)] for c, r in todo]
        t0 = time.time()
        with mp.get_context("spawn").Pool(workers) as pool, open(LABEL_F, "a") as f:
            for i, res in enumerate(pool.imap_unordered(_label_worker, chunks)):
                for r in res:
                    self.d[(r["cand"], r["ref"])] = r
                    f.write(json.dumps(r, ensure_ascii=False) + "\n")
                if (i + 1) % 200 == 0:
                    f.flush()
                    logger.info(f"[{tag}] {i + 1}/{len(chunks)} labels, {time.time() - t0:.0f}s")
        logger.info(f"[{tag}] labels done in {time.time() - t0:.0f}s")


REPAIR_F = ROOT / "results" / "repair_cache.jsonl"


def _repair_worker(chunk: list[tuple[str, str, float]]) -> list[dict]:
    sys.path.insert(0, str(ROOT / "src"))
    sys.setrecursionlimit(10000)
    from common import medoid_repair, safe_parse
    out = []
    for c, m, budget in chunk:
        t0 = time.time()
        ec, em = safe_parse(c), safe_parse(m)
        if ec is None or em is None:
            d, ops = None, []
        else:
            try:
                d, ops = medoid_repair(ec, em, budget_s=budget)
            except (RecursionError, ValueError, KeyError, TypeError):
                d, ops = 3, ["COMPOUND"]
        out.append({"c": c, "m": m, "depth": d, "ops": ops, "secs": round(time.time() - t0, 2)})
    return out


class RepairCache:
    def __init__(self):
        self.d = {(r["c"], r["m"]): r for r in _load(REPAIR_F)}

    def get(self, c: str, m: str) -> dict | None:
        return self.d.get((c.strip(), m.strip()))

    def compute(self, pairs, workers: int = 4, budget: float = 10.0, tag: str = ""):
        todo = sorted({(c.strip(), m.strip()) for c, m in pairs} - set(self.d))
        if not todo:
            return
        logger.info(f"[{tag}] medoid repairs to compute: {len(todo)} (budget {budget}s each)")
        t0 = time.time()
        with mp.get_context("spawn").Pool(workers) as pool, open(REPAIR_F, "a") as f:
            for i, res in enumerate(pool.imap_unordered(_repair_worker, [[(c, m, budget)] for c, m in todo])):
                for r in res:
                    self.d[(r["c"], r["m"])] = r
                    f.write(json.dumps(r, ensure_ascii=False) + "\n")
                if (i + 1) % 100 == 0:
                    f.flush()
                    el = time.time() - t0
                    logger.info(f"[{tag}] {i + 1}/{len(todo)} repairs, {el:.0f}s, eta {el / (i + 1) * (len(todo) - i - 1):.0f}s")
        logger.info(f"[{tag}] repairs done in {time.time() - t0:.0f}s")
