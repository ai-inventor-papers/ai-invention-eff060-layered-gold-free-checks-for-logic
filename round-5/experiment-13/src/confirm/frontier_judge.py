#!/usr/bin/env python3
"""STEP F (budget-conditional, addendum prereg): frontier judge google/gemini-3.1-pro-preview on the ORIGINAL view with
exp 7's rubric-A prompt verbatim (ast-extracted and sha-checked by judge_orig_complete.extract_judge_code) and exp 7's
frontier config (reasoning effort low, max_tokens 4000, json_object, one JSON re-ask). The judge is label-blind.

Sample: 75 ERROR_CERT + 75 MAPPED rows from the provisional orig-view population (untouched; c_align and judge_orig
scored), round-robin over templates, rows shuffled within template with random.Random(20260924).
Runs a 5-row pilot first; the full sample runs only if the projection fits under the $3.6 stop minus a $0.36 reserve.
Output: results/judge_frontier_FREE.jsonl, results/frontier_sample.json.
usage: frontier_judge.py [--pilot-only]
"""
from __future__ import annotations

import argparse
import asyncio
import json
import random
import sys
import time
from collections import defaultdict

from cc import LAB, RES, dump, jl, setup_logger
from judge_orig_complete import extract_judge_code, messages

sys.path.insert(0, str(LAB / "src"))
logger = setup_logger("frontier_judge")
MODEL = "google/gemini-3.1-pro-preview"
EXTRA = {"reasoning": {"effort": "low"}, "response_format": {"type": "json_object"}}
OUT = RES / "judge_frontier_FREE.jsonl"


def sample(n_per: int = 75) -> list[dict]:
    labs = {r["row_key"]: r for r in jl(RES / "rcomp_free_labels_final.jsonl")}
    sc = {r["row_key"]: r for r in jl(RES / "scores_rcomp_free.jsonl")}
    pop = [labs[k] for k, s in sc.items() if s["untouched"] and s["c_score_align"] is not None and s["judge_cheap_orig"] is not None
           and labs[k]["label"] in ("ERROR_CERT", "UNRESOLVED_GLOSS_GATE_FAILED")]
    rng = random.Random(20260924)
    out = []
    for lab in ("ERROR_CERT", "UNRESOLVED_GLOSS_GATE_FAILED"):
        by = defaultdict(list)
        for r in sorted(pop, key=lambda r: r["row_key"]):
            if r["label"] == lab:
                by[r["template_id"]].append(r)
        for t in sorted(by):
            rng.shuffle(by[t])
        ts, i, ch = sorted(by), 0, []
        while len(ch) < n_per and any(by.values()):
            t = ts[i % len(ts)]
            if by[t]:
                ch.append(by[t].pop())
            i += 1
        out += ch
    return out


async def run(rows: list[dict], ns: dict) -> float:
    import gloss
    sents = json.loads((LAB / "work/sentences.json").read_text())
    done = {r["row_key"] for r in jl(OUT) if r.get("p") is not None}
    client = gloss.Client(phase="frontier_judge_iter5", concurrency=12)
    lock = asyncio.Lock()
    spent0 = client.total

    async def one(r):
        msgs = messages(ns, sents[r["sentence_id"]]["text"], r["candidate_fol"])
        t0 = time.time()
        cost, out, fail = 0.0, None, None
        try:
            txt, usd = await client.chat(MODEL, msgs, 4000, logger, extra=EXTRA)
            cost += usd
            out = ns["parse_judge_json"](txt)
            if out is None and txt is not None:
                m2 = msgs + [{"role": "assistant", "content": txt or ""}, {"role": "user", "content": "Return ONLY the JSON object."}]
                txt, usd = await client.chat(MODEL, m2, 4000, logger, extra=EXTRA)
                cost += usd
                out = ns["parse_judge_json"](txt)
            fail = None if out else ("json_parse" if txt is not None else "api:no_response")
        except (gloss.BudgetExceeded, gloss.QuotaError) as e:
            fail = f"budget:{e}"
        rec = {"row_key": r["row_key"], "cond": "orig", "judge": "frontier", "model": MODEL, "p": out["p"] if out else None,
               "verdict": out.get("verdict") if out else None, "type": out.get("type") if out else None, "fail": fail, "cost": cost,
               "seconds": time.time() - t0}
        async with lock:
            with OUT.open("a") as fh:
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    try:
        await asyncio.gather(*[one(r) for r in rows if r["row_key"] not in done])
    finally:
        await client.close()
    return client.total - spent0


@logger.catch(reraise=True)
def main() -> None:
    import gloss
    ap = argparse.ArgumentParser()
    ap.add_argument("--pilot-only", action="store_true")
    a = ap.parse_args()
    ns = extract_judge_code()
    rows = sample()
    dump(RES / "frontier_sample.json", [{k: r[k] for k in ("row_key", "label", "template_id")} for r in rows])
    order = [x for pair in zip(rows[:75], rows[75:]) for x in pair]
    pilot = order[:5]
    usd = asyncio.run(run(pilot, ns))
    per = usd / 5
    proj = per * (len(order) - 5)
    left = gloss.HARD_STOP_USD - 0.36 - gloss.spent()
    logger.info(f"pilot: ${usd:.4f} for 5 rows (${per:.4f}/row); projection ${proj:.3f}; room ${left:.3f}")
    dump(RES / "frontier_projection.json", {"pilot_usd": usd, "per_row": per, "projection_rest": proj, "room": left, "run": proj <= left})
    if a.pilot_only or proj > left:
        logger.warning("frontier: stopping after pilot" + (" (projection exceeds room)" if proj > left else ""))
        return
    asyncio.run(run(order[5:], ns))
    got = [r for r in jl(OUT) if r.get("p") is not None]
    logger.info(f"frontier rows scored: {len(got)}; spend now ${gloss.spent():.3f}")


if __name__ == "__main__":
    main()
