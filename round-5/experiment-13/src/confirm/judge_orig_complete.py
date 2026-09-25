#!/usr/bin/env python3
"""STEP 0b (PRE-SEAL, label-blind; deviation D16): complete exp 7's ORIGINAL-view flash-lite rubric-A judge on R_COMP
FREE rows. exp 7's run stopped when its budget ran out: 916 of 2,265 parseable FREE rows were scored, 224 failed with
network 502s and the rest were never attempted.

The prompt, model and parameters are byte-identical to exp 7's vendor_d.judges.judge_json path:
- RUBRIC_A / USER_JSON_A / parse_judge_json are ast-extracted from exp 7's file, and their sha1 values are asserted
  equal to exp 7's T4 regression record;
- gemini-2.5-flash-lite, T=0, max_tokens 150, response_format json_object, one "Return ONLY the JSON object." retry;
- score = 1 - p(faithful).
The regression check reconstructs exp 7's cache key for 40 already-scored orig rows and requires 40/40 hits in exp 7's
llm_cache.jsonl before any paid call.

Scope: parseable FREE rows with no exp-7 orig score, EXCLUDING rows whose exp-7 orig attempt ended in json_parse (a
judge failure, which stays a coverage failure, as in the disguised view). Every call goes through labeller gloss.Client
(ledger + $3.6 hard stop). Output: results/judge_orig_iter5_FREE.jsonl.
usage: judge_orig_complete.py [--regress-only] [--limit N]
"""
from __future__ import annotations

import argparse
import ast
import asyncio
import json
import sys
import time
from pathlib import Path

from cc import E7, LAB, RES, jl, load_scores, setup_logger, sha1

sys.path.insert(0, str(LAB / "src"))
logger = setup_logger("judge_orig_complete")
MODEL = "google/gemini-2.5-flash-lite"
OUT = RES / "judge_orig_iter5_FREE.jsonl"
JUDGES_PY = E7 / "src/vendor_x5/vendor_d/judges.py"


def extract_judge_code() -> dict:
    """Execute ONLY the RUBRIC_A / CODES / USER_JSON_A assignments and parse_judge_json from exp 7's judges.py."""
    src = JUDGES_PY.read_text()
    tree = ast.parse(src)
    keep = []
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", None) in ("RUBRIC_A", "CODES", "USER_JSON_A") for t in node.targets):
            keep.append(node)
        if isinstance(node, ast.FunctionDef) and node.name == "parse_judge_json":
            keep.append(node)
    mod = ast.Module(body=keep, type_ignores=[])
    ns = {"re": __import__("re"), "json": json, "math": __import__("math")}
    exec(compile(mod, str(JUDGES_PY), "exec"), ns)  # noqa: S102 - vetted constant + pure-function extraction
    reg = json.loads((E7 / "results/judge_regression_T4.json").read_text())["prompt_sha1"]
    assert sha1(ns["RUBRIC_A"]) == reg["RUBRIC_A"] and sha1(ns["USER_JSON_A"]) == reg["USER_JSON_A"], "prompt sha mismatch"
    return ns


def messages(ns: dict, text: str, fol: str) -> list[dict]:
    fol_s = fol if (fol and fol.strip()) else "(empty)"
    return [{"role": "system", "content": ns["RUBRIC_A"]}, {"role": "user", "content": ns["USER_JSON_A"].format(text=text, fol=fol_s)}]


def exp7_key(msgs: list[dict]) -> str:
    params = {"max_tokens": 150, "response_format": {"type": "json_object"}}
    return sha1(json.dumps(["judge_cheap_primary", MODEL, msgs, params], sort_keys=True, ensure_ascii=False))


def units() -> tuple[list[dict], list[dict], dict]:
    sents = json.loads((LAB / "work/sentences.json").read_text())
    rows = [r for r in load_scores("FREE") if r["parse_ok"] and (r.get("candidate_fol") or "").strip()]
    ex = {}
    for r in jl(E7 / "results/judge_FREE.jsonl"):
        if r["cond"] != "orig":
            continue
        prev = ex.get(r["row_key"])
        if r["p"] is not None:
            ex[r["row_key"]] = "scored"
        elif prev != "scored":
            ex[r["row_key"]] = "json_parse" if r["fail"] == "json_parse" else (prev if prev == "json_parse" else "infra")
    done = {r["row_key"] for r in jl(OUT) if r.get("p") is not None}
    for r in rows:
        r["text"] = sents[r["sentence_id"]]["text"]
    scored = [r for r in rows if ex.get(r["row_key"]) == "scored"]
    todo = [r for r in rows if ex.get(r["row_key"]) not in ("scored", "json_parse") and r["row_key"] not in done]
    todo.sort(key=lambda r: sha1("judge_orig_iter5|" + r["row_key"]))
    return scored, todo, ex


def regress(ns: dict, scored: list[dict]) -> dict:
    keys = set()
    for l in (E7 / "results/llm_cache.jsonl").read_text().splitlines():
        try:
            keys.add(json.loads(l)["key"])
        except (json.JSONDecodeError, KeyError):
            continue
    sample = sorted(scored, key=lambda r: sha1("regress|" + r["row_key"]))[:40]
    hits = sum(exp7_key(messages(ns, r["text"], r["candidate_fol"])) in keys for r in sample)
    out = {"n": len(sample), "cache_key_hits": hits, "pass": hits == len(sample)}
    logger.info(f"regression vs exp-7 cache keys: {out}")
    return out


async def run(ns: dict, todo: list[dict]) -> None:
    import gloss
    client = gloss.Client(phase="judge_orig_completion_iter5", concurrency=16)
    lock = asyncio.Lock()
    ex = {"response_format": {"type": "json_object"}}

    async def one(r):
        msgs = messages(ns, r["text"], r["candidate_fol"])
        t0 = time.time()
        cost, fail, out = 0.0, None, None
        try:
            u = {}
            txt, usd = await client.chat(MODEL, msgs, 150, logger, extra=ex, usage_out=u)
            cost += usd
            out = ns["parse_judge_json"](txt)
            if out is None and txt is not None:
                msgs2 = msgs + [{"role": "assistant", "content": txt or ""}, {"role": "user", "content": "Return ONLY the JSON object."}]
                txt, usd = await client.chat(MODEL, msgs2, 150, logger, extra=ex)
                cost += usd
                out = ns["parse_judge_json"](txt)
            if out is None:
                fail = "json_parse" if txt is not None else "api:no_response"
        except (gloss.BudgetExceeded, gloss.QuotaError) as e:
            fail = f"budget:{e}"
        rec = {"row_key": r["row_key"], "cond": "orig", "judge": "cheap", "model": MODEL,
               "p": out["p"] if out else None, "verdict": out.get("verdict") if out else None, "type": out.get("type") if out else None,
               "reason": out.get("reason") if out else None, "fail": fail, "cost": cost, "seconds": time.time() - t0,
               "source": "iter5_completion"}
        async with lock:
            with OUT.open("a") as fh:
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        return rec
    try:
        for s in range(0, len(todo), 200):
            part = todo[s:s + 200]
            res = await asyncio.gather(*[one(r) for r in part])
            nf = sum(r["p"] is None for r in res)
            logger.info(f"chunk {s // 200}: {len(part)} rows, failures {nf}, artifact spend ${client.total:.4f}")
            if any(str(r["fail"]).startswith("budget") for r in res):
                logger.error("budget stop")
                break
    finally:
        await client.close()


@logger.catch(reraise=True)
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--regress-only", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()
    ns = extract_judge_code()
    scored, todo, ex = units()
    logger.info(f"exp-7 orig scored {len(scored)}; json_parse kept as failures {sum(v == 'json_parse' for v in ex.values())}; "
                f"to score now {len(todo)}")
    rg = regress(ns, scored)
    (RES / "judge_orig_iter5_regression.json").write_text(json.dumps(rg, indent=1))
    assert rg["pass"], "prompt reconstruction does not reproduce exp-7 cache keys"
    if a.regress_only:
        return
    if a.limit:
        todo = todo[:a.limit]
    asyncio.run(run(ns, todo))
    got = [r for r in jl(OUT) if r.get("p") is not None]
    logger.info(f"iter-5 orig rows scored: {len(got)}")


if __name__ == "__main__":
    main()
