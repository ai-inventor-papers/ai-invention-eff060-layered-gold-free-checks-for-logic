#!/usr/bin/env python3
"""PART B API arm: judge_cheap_disg = google/gemini-2.5-flash-lite, exp D rubric A (RUBRIC_A + USER_JSON_A, max_tokens 150,
T=0, JSON mode; exp D judges.judge_json VERBATIM) on the DISGUISED (text, fol) of
  * every PERTURB row (dataset 3's per-sentence bijection: metadata_disguised_text / metadata_disguised_fol),
  * the 300 unmutated bases (control type BASE; metadata_disguised_reference_fol),
  * E calibration rows (EC:, data/E_calib_units.jsonl: 864 R_AB LLM CORRECT + 400 ERROR, exp 6's exp-D disguise) --
    needed because the frozen exp 5/exp 6 judge_cheap_disg E scores cover only a handful of rows (exp 5's key died), so the
    PRIMARY FA-0.10 threshold is fixed on these E CORRECT rows.
Order: 20-row pilot -> E calibration -> E-base PERTURB rows -> R_COMP-base rows (the error-type label is kept for Part C).
Budget: vendored exp-D Budget (reservation inside the semaphore); artifact cap $1.0 for this arm (plan), key floor $0.8
(the key is shared with sibling artifacts). Base URL from OPENROUTER_BASE_URL (never hard-coded); explicit User-Agent
(the proxy's Cloudflare front rejects the default Python UA with 403).
usage: run_api_perturb.py [--limit N] [--phase pilot|all]
Output: results/perturb_scores/judge_cheap_disg.jsonl  (key, p, verdict, type, reason, fail, cost, seconds)
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
import time
from pathlib import Path

import aiohttp
import requests
from loguru import logger

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from vendor_d import budget as VB  # noqa: E402
from vendor_d import judges as J  # noqa: E402

BASE = os.environ["OPENROUTER_BASE_URL"].rstrip("/")
VB.URL = BASE + "/chat/completions"
VB.CAP_TOTAL = 1.0
VB.CAPS = {"judge_cheap_perturb": 1.0}
UA = {"User-Agent": "aii-experiment/1.0 (aiohttp)"}
MODEL = "google/gemini-2.5-flash-lite"
KEY_FLOOR = 0.8
OUT = ROOT / "results" / "perturb_scores" / "judge_cheap_disg.jsonl"
LEDGER = ROOT / "results" / "cost_ledger.jsonl"
os.environ.setdefault("AII_COST_LEDGER", str(LEDGER))

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(ROOT / "logs" / "run_api_perturb.log", rotation="30 MB", level="DEBUG")


def key_remaining() -> float | None:
    try:
        d = requests.get(BASE + "/key", headers={"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}", **UA},
                         timeout=20).json()["data"]
        return None if d.get("limit_remaining") is None else float(d["limit_remaining"])
    except (requests.RequestException, KeyError, ValueError) as e:
        logger.warning(f"key check failed: {e}")
        return None


def jl(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []


def units() -> list[tuple[str, str, str]]:
    rows = jl(ROOT / "data" / "perturb_rows.jsonl")
    cal = jl(ROOT / "data" / "E_calib_units.jsonl")
    E, R, seen = [], [], set()
    for r in rows:
        tgt = R if r["base_source"].startswith("R_COMP") else E
        tgt.append(("PT:" + r["item_id"], r["disguised_text"], r["disguised_fol"]))
        if r["base_item_id"] not in seen:
            seen.add(r["base_item_id"])
            tgt.append(("PB:" + r["base_item_id"], r["disguised_text"], r["disguised_reference_fol"]))
    C = [(c["key"], c["text_d"], c["fol_d"]) for c in cal]
    return C + E + R


async def run(U: list[tuple[str, str, str]], chunk: int = 500) -> bool:
    have = {r["key"] for r in jl(OUT) if r.get("p") is not None}
    todo = [u for u in U if u[0] not in have]
    logger.info(f"judge_cheap_disg: {len(todo)} to score ({len(U)} requested)")
    async with VB.Budget(concurrency=24) as b:
        await b.session.close()
        b.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=240), headers=UA)
        for s in range(0, len(todo), chunk):
            kr = key_remaining()
            logger.info(f"chunk {s // chunk}: key remaining ${kr}; arm spend ${b.spent:.4f}")
            if kr is not None and kr < KEY_FLOOR:
                logger.error(f"shared key below floor (${kr}); stopping (resumable)")
                return False
            part = todo[s:s + chunk]
            t0 = time.time()
            outs = await J.gather_limited([J.judge_json(b, component="judge_cheap_perturb", model=MODEL, rubric=J.RUBRIC_A,
                                                        text=t, fol=f, item_id=k, max_tokens=150, user_tmpl=J.USER_JSON_A)
                                           for k, t, f in part], f"chunk {s // chunk}")
            with OUT.open("a") as fh:
                for (k, _, _), o in zip(part, outs):
                    fh.write(json.dumps({"key": k, **{kk: o.get(kk) for kk in ("p", "verdict", "type", "reason", "fail", "cost", "seconds")}},
                                        ensure_ascii=False) + "\n")
            nf = sum(o.get("p") is None for o in outs)
            logger.info(f"chunk {s // chunk}: {len(part)} in {time.time() - t0:.0f}s, failures {nf}; arm spend ${b.spent:.4f}")
            if nf > 0.5 * len(part):
                logger.error(f"more than half failed: {[o.get('fail') for o in outs if o.get('p') is None][:3]}")
                return False
    return True


@logger.catch(reraise=True)
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    U = units()
    if a.limit:
        U = U[:a.limit // 2] + U[864:864 + a.limit - a.limit // 2]
    logger.info(f"units {len(U)}; key remaining ${key_remaining()}")
    ok = asyncio.run(run(U))
    logger.info(f"done (completed={ok}); key remaining ${key_remaining()}")


if __name__ == "__main__":
    main()
