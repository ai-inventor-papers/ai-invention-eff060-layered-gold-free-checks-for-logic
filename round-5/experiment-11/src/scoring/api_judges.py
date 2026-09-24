#!/usr/bin/env python3
"""E2-A label-free API comparators, with the FROZEN iteration-3 T1 code (frozen/t1/src, byte-identical copies).

  prep      strict parse flag (T1 strict_parse_ok) + exp-D nonce disguise (T1 _disg_worker: disguise_item(text, fol))
            for every candidate row -> cache/units_E2.jsonl
  judges    flash-lite rubric-A JSON judge (judge_cheap) and gpt-4.1-nano P(YES) judge (judge_cheap2), ORIGINAL and
            DISGUISED views, on every parseable row; deduplicated by (text, fol) as in T1 -> cache/judge_cheap*.jsonl

Unparseable rows are never sent (they score 1.0 = flagged at analysis, as in T1). Reads only the label-free candidate
file (scoring/guard.py enforces it). Budget: T1 Budget with T1's component caps; its ledger is cache/t1_results/costs.jsonl.
Usage: env/.venv/bin/python scoring/api_judges.py --stage prep|judges [--which cheap_disg,cheap_orig,cheap2_disg,cheap2_orig]
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import scoring.guard  # noqa: E402,F401  (must be first)
from scoring.common import CACHE, FROZEN, append_jsonl, candidates, jl, setup_log  # noqa: E402

import argparse  # noqa: E402
import asyncio  # noqa: E402
import hashlib  # noqa: E402
import multiprocessing as mp  # noqa: E402
import os  # noqa: E402
import time  # noqa: E402
from concurrent.futures import ProcessPoolExecutor  # noqa: E402

from loguru import logger  # noqa: E402

T1 = FROZEN / "t1"
sys.path.insert(0, str(T1))
os.environ.setdefault("NLTK_DATA", str(FROZEN / "nltk_data"))
RES = CACHE / "t1_results"
RES.mkdir(exist_ok=True)
UNITS = CACHE / "units_E2.jsonl"
PROMPT_SHA_T1 = {"RUBRIC_A": "06686913c59b6d9a7daeb5748cb9f53ed2b2e812", "USER_JSON_A": "5b3ccfb9d82edbbfb5bd1bb7a4e574da62be38b4",
                 "USER_YESNO": "b36e93cb44615e19dcb36e85ad8664dcb2acb458"}


def sha1(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8")).hexdigest()


def _prep_chunk(chunk):
    sys.setrecursionlimit(10000)
    sys.path.insert(0, str(T1))
    os.environ.setdefault("NLTK_DATA", str(FROZEN / "nltk_data"))
    import scoring.guard  # noqa: F401
    from src.disguise import disguise_item
    from src.labeller.fol import parse
    from src.labeller.labeller import parse_ok
    from src.labeller.repair_census import atoms

    def strict_parse_ok(fol) -> bool:  # T1 method.py strict_parse_ok, verbatim logic
        if not fol or not fol.strip() or not parse_ok(fol):
            return False
        try:
            return all(isinstance(a[1], str) and a[1] for a in atoms(parse(fol)))
        except Exception:  # noqa: BLE001
            return False
    out = []
    for key, text, fol in chunk:
        ok = strict_parse_ok(fol)
        d = {"text_d": None, "fol_d": None, "ok": False, "fail_reasons": ["not_parseable"]}
        if ok:
            try:
                d = disguise_item(text, fol or None)
            except Exception as e:  # noqa: BLE001
                d = {"text_d": None, "fol_d": None, "ok": False, "fail_reasons": [f"exception:{str(e)[:80]}"]}
        out.append({"key": key, "parse_ok": ok, "text_d": d.get("text_d"), "fol_d": d.get("fol_d"), "disg_ok": d.get("ok"),
                    "disg_fail": d.get("fail_reasons")})
    return out


def stage_prep(workers: int) -> None:
    rows = candidates()
    have = {u["key"] for u in jl(UNITS)}
    todo = [(r["row_key"], r["text"], r["candidate_fol"]) for r in rows if r["row_key"] not in have]
    logger.info(f"prep: {len(todo)} rows to parse+disguise ({len(rows)} total)")
    chunks = [todo[i:i + 40] for i in range(0, len(todo), 40)]
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=workers, mp_context=mp.get_context("spawn")) as ex:
        for i, res in enumerate(ex.map(_prep_chunk, chunks)):
            append_jsonl(UNITS, res)
            if (i + 1) % 20 == 0:
                logger.info(f"prep {i + 1}/{len(chunks)} chunks {time.time() - t0:.0f}s")
    U = jl(UNITS)
    npo = sum(u["parse_ok"] for u in U)
    nf = sum(1 for u in U if u["parse_ok"] and not (u["disg_ok"] and u["fol_d"]))
    logger.info(f"prep done: {len(U)} units, parseable {npo}, disguise failures {nf} ({nf / max(1, npo):.2%}) in {time.time() - t0:.0f}s")


def stage_judges(which: list[str], concurrency: int) -> None:
    from src import budget as B
    from src import judges as J
    B.RES = RES  # ledger/state of this artifact (cache/t1_results), T1 caps unchanged
    J.CACHE_P = RES / "llm_cache.jsonl"
    for k, v in PROMPT_SHA_T1.items():
        assert J.PROMPT_SHA[k] == v, f"prompt sha mismatch {k}"
    import json
    pre = json.loads((T1 / "prereg_T1.json").read_text())
    rub, ut = J.RUBRIC_A, J.USER_JSON_A
    cand = {r["row_key"]: r for r in candidates()}
    U = [u for u in jl(UNITS) if u["parse_ok"]]
    U.sort(key=lambda u: sha1(u["key"]))

    async def run():
        async with B.Budget(concurrency=concurrency) as b:
            for w in which:
                name, cond = w.rsplit("_", 1)
                outp = CACHE / f"judge_{name}.jsonl"
                done = {r["key"]: r for r in jl(outp) if r.get("p") is not None}
                pairs = []
                for u in U:
                    c = cand[u["key"]]
                    t, f = (c["text"], c["candidate_fol"]) if cond == "orig" else (u["text_d"], u["fol_d"])
                    if t is None or f is None:
                        continue
                    k = f"{u['key']}|{cond}"
                    if k not in done:
                        pairs.append((k, t, f))
                m, uq = {}, {}
                for k, t, f in pairs:
                    uk = sha1(t + "||" + (f or ""))
                    m[k] = uk
                    uq.setdefault(uk, (t, f))
                uql = [(uk, t, f) for uk, (t, f) in uq.items()]
                t0 = time.time()
                if name == "cheap":
                    outs = await J.gather_limited([J.judge_json(b, component="judge_cheap", model=pre["models"]["judge_cheap"],
                                                                rubric=rub, text=t, fol=f, item_id=k, user_tmpl=ut) for k, t, f in uql], w)
                else:
                    outs = await J.gather_limited([J.judge_logprob(b, component="judge_cheap2", model=pre["models"]["judge_cheap2"],
                                                                   rubric=rub, text=t, fol=f, item_id=k) for k, t, f in uql], w)
                res = {k: o for (k, _, _), o in zip(uql, outs)}
                rows = [{"key": k, "p": res[m[k]].get("p"), "type": res[m[k]].get("type"), "fail": res[m[k]].get("fail"),
                         "src": res[m[k]].get("src"), "cost": res[m[k]].get("cost"), "seconds": res[m[k]].get("seconds"),
                         "dedup_key": m[k], "verdict": res[m[k]].get("verdict"), "n_rows_sharing": sum(1 for v in m.values() if v == m[k])}
                        for k, _, _ in pairs]
                append_jsonl(outp, rows)
                logger.info(f"{w}: {len(rows)} rows ({len(uql)} unique calls) in {time.time() - t0:.0f}s; "
                            f"failures {sum(r['p'] is None for r in rows)}; spent ${b.spent:.4f} {b.by_comp}; dead={b.dead}")
                if b.dead:
                    logger.error("key exhausted")
                    break
    asyncio.run(run())


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", required=True)
    ap.add_argument("--which", default="cheap_disg,cheap_orig,cheap2_disg,cheap2_orig")
    ap.add_argument("--workers", type=int, default=16)
    ap.add_argument("--concurrency", type=int, default=32)
    a = ap.parse_args()
    setup_log(f"api_judges_{a.stage}")
    if a.stage == "prep":
        stage_prep(a.workers)
    elif a.stage == "judges":
        stage_judges(a.which.split(","), a.concurrency)


if __name__ == "__main__":
    main()
