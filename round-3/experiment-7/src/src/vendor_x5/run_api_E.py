#!/usr/bin/env python3
"""STEP 3: label-free API jobs on dataset E (background, resumable, cached).

Phases (priority order; each phase is cached so a re-run only pays for missing calls):
  1. L3 questionnaire (exp A role_questionnaire, flash-lite, TEXT ONLY) on the 700 unique E texts.
  2. judge_cheap_disg: exp D judge_json(RUBRIC_A, USER_JSON_A, google/gemini-2.5-flash-lite, max_tokens=150) on the exp-D
     nonce disguise of (text, fol) (disguise_item(text, fol, seed_text=norm(text))). Rows in data/api_priority.json order.
  3. judge_cheap_orig: same on the original (text, fol).
  4. L3 questionnaire on the disguised texts (contamination arm for L3).
Unparseable candidates are never sent to the judge (the scorer sets them to 1.0 = flagged, like every metric).
Reads ONLY data/E_blind.jsonl and data/api_priority.json (an ordering of row keys), never a label.
Budget: vendored exp-D Budget (reserve-inside-semaphore) with caps below; plus a live check of the shared key.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
import time
from pathlib import Path

import requests
from loguru import logger

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "src" / "vendor_a"))
sys.setrecursionlimit(10000)
os.environ.setdefault("NLTK_DATA", str(ROOT / "data" / "nltk_data"))

from vendor_d import budget as VB  # noqa: E402
from vendor_d import judges as J  # noqa: E402
from vendor_d.common import norm  # noqa: E402
from vendor_e.fol import parse as e_parse  # noqa: E402

RES = ROOT / "results"
VB.CAP_TOTAL = 3.0
VB.CAPS = {"judge_cheap_primary": 2.4, "setup_probe": 0.05}
L3_HARD_STOP = 0.8
JUDGE_MODEL = "google/gemini-2.5-flash-lite"
KEY_FLOOR = 0.10  # stop when the shared key has less than this left (other runs share it)

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(ROOT / "logs" / "run_api_E.log", rotation="30 MB", level="DEBUG")


def key_remaining() -> float | None:
    try:
        d = requests.get(os.environ["OPENROUTER_BASE_URL"].rstrip("/") + "/key", headers={"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}"},
                         timeout=20).json()["data"]
        return None if d.get("limit_remaining") is None else float(d["limit_remaining"])
    except (requests.RequestException, KeyError, ValueError) as e:
        logger.warning(f"key check failed: {e}")
        return None


def parseable(s: str) -> bool:
    if not s or not s.strip():
        return False
    try:
        e_parse(s)
        return True
    except (ValueError, IndexError, RecursionError, TypeError):
        return False


def jl(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []


def build_disguise(rows: list[dict]) -> dict:
    """row_key -> exp-D disguise record (cached in results/E_disguise_map.jsonl)."""
    from vendor_d.disguise import disguise_item
    p = RES / "E_disguise_map.jsonl"
    have = {r["row_key"]: r for r in jl(p)}
    todo = [r for r in rows if r["row_key"] not in have]
    t0 = time.time()
    with p.open("a") as fh:
        for i, r in enumerate(todo):
            fol = r["candidate_fol"] if r["candidate_fol"].strip() else None
            try:
                d = disguise_item(r["text"], fol, seed_text=norm(r["text"]))
                rec = {"row_key": r["row_key"], "text_d": d["text_d"], "fol_d": d["fol_d"], "ok": d["ok"],
                       "fail_reasons": d["fail_reasons"], "leak_text": d["leak_text"], "leak_formula": d["leak_formula"]}
            except Exception as ex:  # noqa: BLE001 - a disguise failure is logged and counted, never silent
                logger.warning(f"disguise failed {r['row_key']}: {ex}")
                rec = {"row_key": r["row_key"], "text_d": None, "fol_d": None, "ok": False, "fail_reasons": [f"exc:{str(ex)[:80]}"]}
            have[r["row_key"]] = rec
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            if (i + 1) % 1000 == 0:
                logger.info(f"disguise {i + 1}/{len(todo)} {time.time() - t0:.0f}s")
    return have


async def l3_phase(texts: list[str], tag_cond: str) -> None:
    import llm as LA
    import fol_triage as FT
    LA.CACHE_P = ROOT / "cache" / "llm_cache.jsonl"
    LA.LEDGER_P = ROOT / "cache" / "l3_cost_ledger.jsonl"
    LA.HARD_STOP_USD = L3_HARD_STOP
    outp = RES / "E_l3_q.jsonl"
    have = {(r["text"], r["cond"]) for r in jl(outp) if r.get("coverage_status") == "OK"}
    todo = [t for t in dict.fromkeys(texts) if (t, tag_cond) not in have]
    logger.info(f"L3[{tag_cond}]: {len(todo)} texts to answer ({len(texts)} total)")
    if not todo:
        return
    async with LA.LLM(concurrency=16) as llm:
        async def one(t):
            try:
                r = await FT.role_questionnaire(t, llm, JUDGE_MODEL, tag="L3")
            except LA.StopBudget as ex:
                r = {"q": None, "coverage_status": "BUDGET_STOP", "cost_usd": 0.0, "secs": 0.0, "err": str(ex)}
            except RuntimeError as ex:
                r = {"q": None, "coverage_status": "L3_FAIL", "cost_usd": 0.0, "secs": 0.0, "err": str(ex)[:200]}
            return {"text": t, "cond": tag_cond, **r}
        res = await asyncio.gather(*[one(t) for t in todo])
        with outp.open("a") as fh:
            for r in res:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        ok = sum(r["coverage_status"] == "OK" for r in res)
        logger.info(f"L3[{tag_cond}]: ok {ok}/{len(res)}; new calls {llm.n_calls}; L3 ledger ${llm.spent:.4f}")


async def judge_phase(units: list[tuple[str, str, str, str]], chunk: int = 400) -> bool:
    """units: (row_key, cond, text, fol). Returns False if stopped for budget/key."""
    outp = RES / "E_judge.jsonl"
    have = {(r["row_key"], r["cond"]) for r in jl(outp) if r.get("p") is not None}
    todo = [u for u in units if (u[0], u[1]) not in have]
    logger.info(f"judge: {len(todo)} units to score ({len(units)} requested)")
    async with VB.Budget(concurrency=16) as b:
        for s in range(0, len(todo), chunk):
            kr = key_remaining()
            logger.info(f"judge chunk {s // chunk}: key remaining ${kr}; artifact judge spend ${b.spent:.4f}")
            if kr is not None and kr < KEY_FLOOR:
                logger.error(f"shared key nearly exhausted (${kr}); stopping judge phase (resumable)")
                return False
            part = todo[s:s + chunk]
            t0 = time.time()
            outs = await J.gather_limited([J.judge_json(b, component="judge_cheap_primary", model=JUDGE_MODEL,
                                                        rubric=J.RUBRIC_A, text=t, fol=f, item_id=f"{k}|{c}",
                                                        max_tokens=150, user_tmpl=J.USER_JSON_A)
                                           for k, c, t, f in part], f"judge chunk {s // chunk}")
            with outp.open("a") as fh:
                for (k, c, _, _), o in zip(part, outs):
                    fh.write(json.dumps({"row_key": k, "cond": c, **{kk: o.get(kk) for kk in
                                         ("p", "verdict", "type", "reason", "fail", "cost", "seconds")}}, ensure_ascii=False) + "\n")
            nf = sum(o.get("p") is None for o in outs)
            logger.info(f"judge chunk {s // chunk}: {len(part)} units in {time.time() - t0:.0f}s, failures {nf}; spend ${b.spent:.4f}")
            if nf > 0.5 * len(part):
                fails = [o.get("fail") for o in outs if o.get("p") is None][:3]
                logger.error(f"more than half failed ({fails}); stopping (resumable)")
                return False
    return True


@logger.catch(reraise=True)
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phases", default="l3,disg,orig,l3disg,rest")
    ap.add_argument("--limit", type=int, default=0, help="only the first N priority rows (staged scale-up)")
    a = ap.parse_args()
    rows = jl(ROOT / "data" / "E_blind.jsonl")
    order = json.loads((ROOT / "data" / "api_priority.json").read_text())
    by = {r["row_key"]: r for r in rows}
    n_first = order["n_analysable_first"]
    ordered = [by[k] for k in order["order"]]
    if a.limit:
        ordered = ordered[:a.limit]
    phases = a.phases.split(",")
    logger.info(f"rows {len(rows)}; analysable-first {n_first}; key remaining ${key_remaining()}")
    if "l3" in phases:
        texts = sorted({r["text"] for r in ordered})
        asyncio.run(l3_phase(texts, "orig"))
    dmap = build_disguise(ordered)
    nd_fail = sum(not dmap[r["row_key"]]["ok"] for r in ordered)
    logger.info(f"disguise: {len(ordered)} rows, assertion failures {nd_fail}")
    pars = [r for r in ordered if r["system_class"] != "symbolic_eventsem" and parseable(r["candidate_fol"])]
    logger.info(f"parseable judge rows: {len(pars)} / {len(ordered)}")
    first = [r for r in pars if order["order"].index(r["row_key"]) < n_first] if not a.limit else pars
    first_keys = {r["row_key"] for r in first}
    gold = [r for r in pars if r["system_class"] == "reference_gold_as_system" and r["row_key"] not in first_keys]
    rest = [r for r in pars if r["row_key"] not in first_keys and r["system_class"] != "reference_gold_as_system"]

    def units(rs, cond):
        out = []
        for r in rs:
            if cond == "disg":
                d = dmap[r["row_key"]]
                if d.get("text_d") is None or d.get("fol_d") is None:
                    continue
                out.append((r["row_key"], "disg", d["text_d"], d["fol_d"]))
            else:
                out.append((r["row_key"], "orig", r["text"], r["candidate_fol"]))
        return out
    ok = True
    if "disg" in phases and ok:
        ok = asyncio.run(judge_phase(units(first, "disg")))
    if "orig" in phases and ok:
        ok = asyncio.run(judge_phase(units(first, "orig")))
    if "disg" in phases and ok:
        ok = asyncio.run(judge_phase(units(gold, "disg") + units(gold, "orig")))
    if "l3disg" in phases and ok:
        td = sorted({dmap[r["row_key"]]["text_d"] for r in pars if dmap[r["row_key"]].get("text_d")})
        asyncio.run(l3_phase(td, "disg"))
    if "rest" in phases and ok:
        ok = asyncio.run(judge_phase(units(rest, "disg") + units(rest, "orig")))
    logger.info(f"run_api_E finished (completed={ok}); key remaining ${key_remaining()}")


if __name__ == "__main__":
    main()
