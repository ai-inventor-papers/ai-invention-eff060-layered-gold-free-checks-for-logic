#!/usr/bin/env python3
"""S7d: LOCAL secondary judge on R_COMP, the exp-5 / exp-D local bar (Qwen/Qwen3-8B, greedy, thinking off, RUBRIC_B +
USER_JSON, max_new_tokens 150), run on the DISGUISED (text, fol) of every parseable row of a condition. It is a labelled
secondary row (judge_local_disg) and never replaces the pre-registered flash-lite bar.

Label-blind: reads only results/disguise_map_<COND>.jsonl (written by run_judges.py from the candidate rows).
Guard: results/testability_<COND>.json must exist and predate this process. Resumable through the LocalLM cache
(results/local_cache.jsonl). Output: results/judge_local_<COND>.jsonl {row_key, cond='disg', p, type, fail, seconds}.
Runs in the separate GPU env (.venv_gpu: torch, transformers, accelerate, loguru).

usage: .venv_gpu/bin/python src/local_judge_rcomp.py --cond SIG|FREE [--limit N] [--bs 48] [--orig]
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"
sys.path.insert(0, str(ROOT / "src" / "vendor_x5"))

from loguru import logger  # noqa: E402


def jl(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []


def main() -> None:
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
    logger.add(ROOT / "logs" / "local_judge_rcomp.log", rotation="30 MB", level="DEBUG")
    ap = argparse.ArgumentParser()
    ap.add_argument("--cond", choices=["SIG", "FREE"], default="SIG")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--bs", type=int, default=48)
    ap.add_argument("--orig", action="store_true", help="also judge the original (text, fol) after all disguised units")
    a = ap.parse_args()
    t_start = time.time()
    g = RES / f"testability_{a.cond}.json"
    import os
    if a.cond == "FREE" and os.environ.get("FREE_PREJOIN") == "1":
        logger.warning("FREE_PREJOIN=1: label-blind FREE judge scores before the FREE declaration (join guarded in analyse.py)")
    elif not g.exists() or g.stat().st_mtime >= t_start:
        raise SystemExit(f"{g.name} missing or newer than this run: declare testability first")
    import torch
    from vendor_d import judges as J
    from vendor_d.local_llm import LocalLM
    torch.cuda.set_per_process_memory_fraction(0.9)
    dm = [r for r in jl(RES / f"disguise_map_{a.cond}.jsonl") if r.get("text_d") and r.get("fol_d")]
    dm = sorted({r["row_key"]: r for r in dm}.values(), key=lambda r: r["row_key"])
    orig = {r["row_key"]: r for r in jl(RES / f"judge_rows_{a.cond}.jsonl")}  # original (text, fol), label-blind export
    if a.limit:
        dm = dm[:a.limit]
    outp = RES / f"judge_local_{a.cond}.jsonl"
    have = {(r["row_key"], r["cond"]) for r in jl(outp)}
    units = [(r["row_key"], "disg", r["text_d"], r["fol_d"]) for r in dm]
    if a.orig:  # secondary contamination row (orig - disg), as exp 5 did on E
        units += [(k, "orig", orig[k]["text"], orig[k]["fol"]) for k in [r["row_key"] for r in dm] if k in orig]
    todo = [u for u in units if (u[0], u[1]) not in have]
    logger.info(f"[{a.cond}] local judge: {len(todo)} units to score ({len(dm)} rows with a disguise; orig={a.orig})")
    if not todo:
        return
    lm = LocalLM("Qwen/Qwen3-8B")
    for s in range(0, len(todo), 512):
        part = todo[s:s + 512]
        msgs = [[{"role": "system", "content": J.RUBRIC_B}, {"role": "user", "content": J.USER_JSON.format(text=t, fol=f)}]
                for _, _, t, f in part]
        t0 = time.time()
        gen = lm.generate(msgs, max_new_tokens=150, bs=a.bs, tag=f"RCOMP_{a.cond}")
        with outp.open("a") as fh:
            for (k, c, _, _), g_ in zip(part, gen):
                o = J.parse_judge_json(g_["text"])
                fh.write(json.dumps({"row_key": k, "cond": c, "judge": "local_qwen3_8b",
                                     "p": o["p"] if o else None, "type": o.get("type") if o else None,
                                     "fail": None if o else "json_parse", "seconds": g_["seconds"]}) + "\n")
        logger.info(f"[{a.cond}] local judge {s + len(part)}/{len(todo)} in {time.time() - t0:.0f}s")
    logger.info(f"[{a.cond}] local judge done in {time.time() - t_start:.0f}s")


if __name__ == "__main__":
    main()
