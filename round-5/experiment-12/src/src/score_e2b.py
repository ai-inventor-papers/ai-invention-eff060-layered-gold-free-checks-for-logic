#!/usr/bin/env python3
"""E2-B label-free scoring (Step 2 parallel work + Step 3). Runs with exp5src/.venv/bin/python.

Every sub-command reads ONLY label-free inputs (generations, the E2-B sentence file with text + label-free strata,
exp-5 code/prereg, caches) through an open() guard that REFUSES any path under sealed/ or whose name contains
'label' or 'reference', and logs every opened path to scores/file_access_log.txt.

  build      -> scores/rows_E2B.jsonl        one row per (sentence, generator slot): text, candidate_fol, family, parse
  disguise   -> scores/disguise_E2B.jsonl    exp-5 build_disguise (vendor_d.disguise.disguise_item, seed = norm(text))
  l3         -> exp5src/results/E_l3_q.jsonl  exp-5 L3 questionnaire (vendor_a fol_triage.role_questionnaire, flash-lite)
  judges --which flashlite|nano|costmatched_pilot|costmatched_disg|costmatched_orig|frontier_pilot|frontier
             -> scores/judge_<which>.jsonl    vendor_d judges (RUBRIC_A / USER_JSON_A byte-identical, PROMPT_SHA asserted)
  frontier_sample -> scores/frontier_subsample.json
  pool       -> scores/pool_E2B.jsonl         exp-5 pool_scoring.score_sentence with exp-5 frozen scoring_params
  assemble   -> scores/scores_E2B.jsonl       every metric/judge per row + PT fusion (exp-5 frozen), unparseable -> 1.0
Transport-only runtime patches (as E2's D0): vendor_d.budget.URL / vendor_a.llm.URL -> $OPENROUTER_BASE_URL.
"""
from __future__ import annotations

import argparse
import asyncio
import builtins
import hashlib
import io
import json
import math
import multiprocessing as mp
import os
import sys
import time
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

WS = Path(__file__).resolve().parents[1]
X5 = WS / "exp5src"
E2B = WS / "e2b"
SC = WS / "scores"
SC.mkdir(exist_ok=True)
(WS / "logs").mkdir(exist_ok=True)
sys.path.insert(0, str(X5 / "src"))
sys.path.insert(0, str(X5 / "src" / "vendor_a"))
sys.setrecursionlimit(10000)
os.environ.setdefault("NLTK_DATA", str(X5 / "data" / "nltk_data"))

from loguru import logger  # noqa: E402

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(WS / "logs" / "score_e2b.log", rotation="30 MB", level="DEBUG")

BASE_URL = os.environ["OPENROUTER_BASE_URL"].rstrip("/")
ACCESS_LOG = SC / "file_access_log.txt"
GEN = WS / "e2bsrc" / "raw" / "generations.jsonl"
SENTS = E2B / "sentences_E2B.json"
SLOT_ORDER = ["G1", "G1b", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9"]
FLASH = "google/gemini-2.5-flash-lite"
NANO = "openai/gpt-4.1-nano"
COSTM = "deepseek/deepseek-v3.2"
FRONT = "google/gemini-3.1-pro-preview"
EXPECTED_PROMPT_SHA = {"RUBRIC_A": None, "USER_JSON_A": None}  # filled from exp-5 vendored judges at import (asserted equal to exp 6's)


# ------------------------------------------------------------------------------------------------ open() guard
_real_open, _real_io_open = builtins.open, io.open


def _guard_path(p) -> None:
    try:
        s = os.fspath(p)
    except TypeError:
        return
    if not isinstance(s, str):
        return
    low = s.lower()
    name = os.path.basename(low)
    if "/sealed/" in low or ("label" in name and "nolabel" not in name) or "reference" in name:
        raise PermissionError(f"score guard: refusing to open {s}")
    if s != str(ACCESS_LOG):
        with _real_open(ACCESS_LOG, "a") as f:
            f.write(f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}\t{os.getpid()}\t{s}\n")


def _gopen(file, *a, **k):
    _guard_path(file)
    return _real_open(file, *a, **k)


def _gio_open(file, *a, **k):
    _guard_path(file)
    return _real_io_open(file, *a, **k)


def install_guard() -> None:
    builtins.open = _gopen
    io.open = _gio_open


# ------------------------------------------------------------------------------------------------ helpers
def jl(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def exp5_prereg() -> dict:
    p = X5 / "results" / "prereg.json"
    assert sha256(p) == (X5 / "results" / "prereg.sha256").read_text().split()[0], "exp-5 prereg sha mismatch"
    return json.loads(p.read_text())


def rows_all() -> list[dict]:
    return jl(SC / "rows_E2B.jsonl")


def batch_order(rows: list[dict]) -> list[dict]:
    return sorted(rows, key=lambda r: (r["e2b_batch"], r["batch_key"], SLOT_ORDER.index(r["slot"])))


# ------------------------------------------------------------------------------------------------ build
def cmd_build(_a) -> None:
    import peer_text as PT
    sents = json.loads(SENTS.read_text())
    by_sid = {s["sentence_id"]: s for s in sents}
    gens = {}
    for g in jl(GEN):
        if g["sentence_id"] in by_sid and g["prompt_variant"] == "fewshot_v1":
            gens[(g["sentence_id"], g["slot"])] = g  # the later record of a duplicate key wins (E's convention)
    pre = exp5_prereg()
    fam_v = pre["family_map_vendor"]
    out = []
    for (sid, slot), g in sorted(gens.items()):
        s = by_sid[sid]
        raw = g.get("raw_output")
        fol = g.get("candidate_fol") or ""
        if raw is None:
            fol = ""
        parse_ok = PT.parse_fol(fol) is not None if fol.strip() else False
        out.append({"row_key": f"{sid}|{slot}", "sentence_id": sid, "slot": slot, "system": g["system"], "family": g["family"],
                    "family_vendor": fam_v[slot], "model": g["model"], "text": s["text"], "candidate_fol": fol,
                    "raw_output": raw, "parse_ok": parse_ok, "gen_final_failure": raw is None, "gen_cost_usd": g.get("cost_usd"),
                    "e2b_batch": s["e2b_batch"], "batch_key": s["e2b_batch_key"], "e2b_origin": s["e2b_origin"],
                    "words": s["words"], "word_bin": s["word_bin"], "n_conditions": s["n_conditions"], "n_quant": s["n_quant"],
                    "depth": s["depth"], "text_conditions": s["text_conditions"], "exception_type": s["exception_type"]})
    (SC / "rows_E2B.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in out))
    logger.info(f"rows: {len(out)} over {len({r['sentence_id'] for r in out})} sentences; parse_ok {sum(r['parse_ok'] for r in out)}; "
                f"per batch {dict(Counter(r['e2b_batch'] for r in out))}")


# ------------------------------------------------------------------------------------------------ disguise
def cmd_disguise(_a) -> None:
    from vendor_d.disguise import disguise_item
    from vendor_d.common import norm
    p = SC / "disguise_E2B.jsonl"
    have = {r["row_key"] for r in jl(p)}
    todo = [r for r in rows_all() if r["row_key"] not in have]
    t0 = time.time()
    with p.open("a") as fh:
        for i, r in enumerate(todo):
            fol = r["candidate_fol"] if r["candidate_fol"].strip() else None
            try:
                d = disguise_item(r["text"], fol, seed_text=norm(r["text"]))
                rec = {"row_key": r["row_key"], "text_d": d["text_d"], "fol_d": d["fol_d"], "ok": d["ok"],
                       "fail_reasons": d["fail_reasons"], "leak_text": d["leak_text"], "leak_formula": d["leak_formula"]}
            except Exception as ex:  # noqa: BLE001 - counted, never silent
                logger.warning(f"disguise failed {r['row_key']}: {ex}")
                rec = {"row_key": r["row_key"], "text_d": None, "fol_d": None, "ok": False, "fail_reasons": [f"exc:{str(ex)[:80]}"]}
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            if (i + 1) % 500 == 0:
                logger.info(f"disguise {i + 1}/{len(todo)} {time.time() - t0:.0f}s")
    logger.info(f"disguise done: {len(jl(p))} rows")


# ------------------------------------------------------------------------------------------------ L3 questionnaire
def cmd_l3(_a) -> None:
    import llm as LA
    import fol_triage as FT
    LA.URL = BASE_URL + "/chat/completions"  # transport-only (D0-equivalent)
    LA.CACHE_P = X5 / "cache" / "llm_cache.jsonl"
    LA.LEDGER_P = X5 / "cache" / "l3_cost_ledger.jsonl"
    LA.HARD_STOP_USD = 0.5
    outp = X5 / "results" / "E_l3_q.jsonl"
    have = {(r["text"], r["cond"]) for r in jl(outp) if r.get("coverage_status") == "OK"}
    sents = sorted(json.loads(SENTS.read_text()), key=lambda s: (s["e2b_batch"], s["e2b_batch_key"]))
    texts = [s["text"] for s in sents if (s["text"], "orig") not in have]
    logger.info(f"L3: {len(texts)} texts to answer")

    async def run():
        async with LA.LLM(concurrency=16) as llm:
            async def one(t):
                try:
                    r = await FT.role_questionnaire(t, llm, FLASH, tag="L3")
                except LA.StopBudget as ex:
                    r = {"q": None, "coverage_status": "BUDGET_STOP", "cost_usd": 0.0, "secs": 0.0, "err": str(ex)}
                except RuntimeError as ex:
                    r = {"q": None, "coverage_status": "L3_FAIL", "cost_usd": 0.0, "secs": 0.0, "err": str(ex)[:200]}
                return {"text": t, "cond": "orig", **r}
            res = await asyncio.gather(*[one(t) for t in texts])
            with outp.open("a") as fh:
                for r in res:
                    fh.write(json.dumps(r, ensure_ascii=False) + "\n")
            logger.info(f"L3 ok {sum(r['coverage_status'] == 'OK' for r in res)}/{len(res)}; spent ${llm.spent:.4f}")
    asyncio.run(run())


# ------------------------------------------------------------------------------------------------ judges
def _vendor_budget():
    from vendor_d import budget as VB
    from vendor_d import judges as J
    VB.URL = BASE_URL + "/chat/completions"  # transport-only (D0-equivalent)
    VB.MODELS_URL = BASE_URL + "/models"
    VB.CAP_TOTAL = 9.5
    VB.CAPS.update({"judge_cheap_primary": 0.8, "judge_cheap2": 0.4, "costmatched": 2.4, "strong": 1.6, "setup_probe": 0.05})
    J.CACHE_P = X5 / "results" / "llm_cache.jsonl"
    exp6 = json.loads((WS / "e2b" / "prompt_sha_expected.json").read_text())
    for k in ("RUBRIC_A", "USER_JSON_A", "USER_YESNO"):
        assert J.PROMPT_SHA[k] == exp6[k], f"PROMPT_SHA {k} differs from exp 5/6"
    if not (X5 / "results" / "prices_refreshed.flag").exists():
        # vendor load_prices(refresh=True) calls the catalogue without auth (refused by this run's proxy): same record
        # shape, fetched through the base URL with the key
        import requests
        d = requests.get(BASE_URL + "/models", headers={"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}"}, timeout=60).json()
        d = d["data"] if isinstance(d, dict) else d
        prices = {m["id"]: {"in": float(m["pricing"]["prompt"]), "out": float(m["pricing"]["completion"]),
                            "params": m.get("supported_parameters", [])} for m in d}
        (X5 / "results" / "prices.json").write_text(json.dumps(prices, indent=0))
        (X5 / "results" / "prices_refreshed.flag").write_text(time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    return VB, J


def judge_units(which: str) -> list[tuple]:
    """(row_key, cond, text, fol) in batch order; unparseable candidates are never sent (scored 1.0 later)."""
    rows = batch_order([r for r in rows_all() if r["parse_ok"]])
    dmap = {r["row_key"]: r for r in jl(SC / "disguise_E2B.jsonl")}
    out = []
    for r in rows:
        if which.endswith("disg"):
            d = dmap.get(r["row_key"], {})
            if d.get("text_d") and d.get("fol_d"):
                out.append((r["row_key"], "disg", d["text_d"], d["fol_d"]))
        else:
            out.append((r["row_key"], "orig", r["text"], r["candidate_fol"]))
    return out


async def _run_judge(units, kind: str, outp: Path, max_tokens: int = 150, concurrency: int = 16) -> dict:
    VB, J = _vendor_budget()
    have = {(r["row_key"], r["cond"]) for r in jl(outp) if r.get("p") is not None}
    todo = [u for u in units if (u[0], u[1]) not in have]
    logger.info(f"judge {kind}: {len(todo)} units to score ({len(units)} requested)")
    n_fail = 0
    async with VB.Budget(concurrency=concurrency) as b:
        for s in range(0, len(todo), 400):
            part = todo[s:s + 400]
            t0 = time.time()
            if kind == "flashlite":
                coros = [J.judge_json(b, component="judge_cheap_primary", model=FLASH, rubric=J.RUBRIC_A, text=t, fol=f,
                                      item_id=f"{k}|{c}", max_tokens=150, user_tmpl=J.USER_JSON_A) for k, c, t, f in part]
            elif kind == "nano":
                coros = [J.judge_logprob(b, component="judge_cheap2", model=NANO, rubric=J.RUBRIC_A, text=t, fol=f,
                                         item_id=f"{k}|{c}") for k, c, t, f in part]
            elif kind == "costmatched":
                coros = [J.judge_json(b, component="costmatched", model=COSTM, rubric=J.RUBRIC_A, text=t, fol=f,
                                      item_id=f"{k}|{c}", max_tokens=max_tokens, extra={"reasoning": {"enabled": False}},
                                      user_tmpl=J.USER_JSON_A) for k, c, t, f in part]
            elif kind == "frontier":
                coros = [J.judge_json(b, component="strong", model=FRONT, rubric=J.RUBRIC_A, text=t, fol=f, item_id=f"{k}|{c}",
                                      max_tokens=4000, extra={"reasoning": {"effort": "low"}}, user_tmpl=J.USER_JSON_A)
                         for k, c, t, f in part]
            else:
                raise ValueError(kind)
            outs = await J.gather_limited(coros, f"{kind} chunk {s // 400}")
            with outp.open("a") as fh:
                for (k, c, _, _), o in zip(part, outs):
                    fh.write(json.dumps({"row_key": k, "cond": c, "model": {"flashlite": FLASH, "nano": NANO, "costmatched": COSTM, "frontier": FRONT}[kind],
                                         "max_tokens": max_tokens if kind == "costmatched" else None,
                                         **{kk: o.get(kk) for kk in ("p", "verdict", "type", "reason", "fail", "cost", "seconds", "src", "raw")}},
                                        ensure_ascii=False) + "\n")
            nf = sum(o.get("p") is None for o in outs)
            n_fail += nf
            logger.info(f"{kind} chunk {s // 400}: {len(part)} units {time.time() - t0:.0f}s fails {nf}; vendor spend ${b.spent:.4f}")
            if nf > 0.5 * len(part):
                logger.error(f"{kind}: more than half failed ({[o.get('fail') for o in outs if o.get('p') is None][:3]}); stopping")
                break
            if any(str(o.get("fail") or "").startswith("budget") for o in outs):
                logger.error(f"{kind}: budget cap hit; stopping (resumable)")
                break
    return {"n_todo": len(todo), "n_fail": n_fail}


def cmd_judges(a) -> None:
    sys.path.insert(0, str(WS / "e2bsrc" / "src_e2b"))
    import budget as BG
    w = a.which
    est_per = {"flashlite": 4.5e-5, "nano": 2.0e-5, "costmatched": 1.6e-4, "frontier": 6e-3}
    if w == "flashlite":
        units = judge_units("disg") + judge_units("orig")
        kind, outp = "flashlite", SC / "judge_flashlite.jsonl"
    elif w == "nano":
        units = judge_units("orig") + judge_units("disg")
        kind, outp = "nano", SC / "judge_nano.jsonl"
    elif w in ("costmatched_pilot", "costmatched_disg", "costmatched_orig", "costmatched_retry"):
        kind = "costmatched"
        mt = 300 if w == "costmatched_retry" else 150
        dp = SC / "costmatched_decision.json"
        if w in ("costmatched_disg", "costmatched_orig") and dp.exists() and json.loads(dp.read_text())["decision"].endswith("_MT300"):
            mt = 300  # the pre-declared single retry rule was triggered in the pilot
        outp = SC / ("judge_costmatched.jsonl" if mt == 150 else "judge_costmatched_mt300.jsonl")
        if w in ("costmatched_pilot", "costmatched_retry"):
            first = batch_order([r for r in rows_all() if r["parse_ok"] and r["e2b_batch"] == 1])[:30]
            keys = {r["row_key"] for r in first}
            units = [u for u in judge_units("disg") + judge_units("orig") if u[0] in keys]
        elif w == "costmatched_disg":
            units = judge_units("disg")
        else:
            units = judge_units("orig")
            if a.keys_file:
                keep = set(json.loads(Path(a.keys_file).read_text()))
                units = [u for u in units if u[0] in keep]
        res = asyncio.run(_run_judge(_budget_trim(units, est_per[kind], BG, a), kind, outp, max_tokens=mt))
        logger.info(f"{w}: {res}")
        return
    elif w in ("frontier", "frontier_pilot"):
        fs = json.loads((SC / "frontier_subsample.json").read_text())
        order = fs["order"][: (10 if w == "frontier_pilot" else fs.get("n_run", len(fs["order"])))]
        rk = {r["row_key"]: r for r in rows_all()}
        units = [(k, "orig", rk[k]["text"], rk[k]["candidate_fol"]) for k in order if rk[k]["parse_ok"]]
        kind, outp = "frontier", SC / "judge_frontier.jsonl"
    else:
        raise ValueError(w)
    res = asyncio.run(_run_judge(_budget_trim(units, est_per[kind], BG, a), kind, outp))
    logger.info(f"{w}: {res}")


def _budget_trim(units, per_call: float, BG, a) -> list:
    """Keep the largest batch-order prefix whose estimated cost fits remaining - reserve - commitments (a.commit)."""
    avail = BG.remaining() - BG.RESERVE - a.commit
    n_fit = max(0, int(avail / per_call)) if per_call > 0 else len(units)
    if n_fit < len(units):
        logger.warning(f"budget trim: {len(units)} units -> {n_fit} (avail ${avail:.3f}, est ${per_call:.2e}/call)")
    return units[:n_fit]


# ------------------------------------------------------------------------------------------------ frontier subsample
def cmd_frontier_sample(a) -> None:
    """300 rows, cells = words tercile (E2-B sentence cut points) x family (9), proportional, min 3 per cell;
    within-cell order sha1('E2B_frontier_v1|'+row_key); inclusion probability = n_cell_sampled / N_cell. Label-free."""
    import numpy as np
    rows = rows_all()
    sents = json.loads(SENTS.read_text())
    cuts = list(np.quantile([s["words"] for s in sents], [1 / 3, 2 / 3]))

    def terc(w):
        return 0 if w <= cuts[0] else (1 if w <= cuts[1] else 2)
    cells = defaultdict(list)
    for r in rows:
        cells[(terc(r["words"]), r["family"])].append(r)
    N = len(rows)
    target = a.n
    alloc = {c: max(3, round(target * len(v) / N)) for c, v in cells.items()}
    alloc = {c: min(n, len(cells[c])) for c, n in alloc.items()}
    while sum(alloc.values()) > target:  # trim the largest cells until the total is the target
        c = max(alloc, key=lambda c: (alloc[c] - 3 if alloc[c] > 3 else -1, str(c)))
        alloc[c] -= 1
    picked, incl = [], {}
    for c, v in sorted(cells.items(), key=lambda kv: str(kv[0])):
        v = sorted(v, key=lambda r: hashlib.sha1(("E2B_frontier_v1|" + r["row_key"]).encode()).hexdigest())
        for r in v[:alloc[c]]:
            picked.append(r["row_key"])
            incl[r["row_key"]] = alloc[c] / len(v)
    order = sorted(picked, key=lambda k: hashlib.sha1(("E2B_frontier_v1|" + k).encode()).hexdigest())
    out = {"rule": "cells = words tercile x family; proportional allocation, min 3 per cell; within-cell sha1('E2B_frontier_v1|'+row_key)",
           "tercile_cuts_words": cuts, "n_target": target, "n": len(order), "n_run": len(order), "order": order,
           "inclusion_prob": incl, "cells": {f"{c[0]}|{c[1]}": {"N": len(cells[c]), "n": alloc[c]} for c in cells},
           "drawn_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "rows_file_sha256": sha256(SC / "rows_E2B.jsonl")}
    (SC / "frontier_subsample.json").write_text(json.dumps(out, indent=1))
    logger.info(f"frontier subsample: {len(order)} rows in {len(cells)} cells; cuts {cuts}")


def cmd_frontier_cut(a) -> None:
    """After the pilot: if $/item > 6e-3 (or budget short) cut to the largest affordable prefix of the sha1 order and
    recompute inclusion probabilities within cells for the rows kept."""
    sys.path.insert(0, str(WS / "e2bsrc" / "src_e2b"))
    import budget as BG
    fs = json.loads((SC / "frontier_subsample.json").read_text())
    pil = [r for r in jl(SC / "judge_frontier.jsonl")]
    cost = [r["cost"] for r in pil if r.get("cost")]
    per = sum(cost) / max(1, len(cost)) if cost else 6e-3
    avail = BG.remaining() - BG.RESERVE - a.commit
    n_aff = int(avail / max(per, 1e-9))
    n_run = min(len(fs["order"]), n_aff) if per <= 6e-3 or True else 0
    fs["pilot_cost_per_item"] = per
    fs["n_run"] = max(len(pil), n_run)
    if fs["n_run"] < len(fs["order"]):
        kept = fs["order"][: fs["n_run"]]
        rk = {r["row_key"]: r for r in rows_all()}
        import numpy as np
        cuts = fs["tercile_cuts_words"]

        def cell(k):
            w = rk[k]["words"]
            t = 0 if w <= cuts[0] else (1 if w <= cuts[1] else 2)
            return f"{t}|{rk[k]['family']}"
        cnt = Counter(cell(k) for k in kept)
        fs["inclusion_prob"] = {k: cnt[cell(k)] / fs["cells"][cell(k)]["N"] for k in kept}
        fs["cut_note"] = f"cut to the first {fs['n_run']} of the sha1 order (budget); inclusion probabilities recomputed per cell"
    (SC / "frontier_subsample.json").write_text(json.dumps(fs, indent=1))
    logger.info(f"frontier: pilot ${per:.5f}/item, avail ${avail:.3f}, n_run {fs['n_run']}")


# ------------------------------------------------------------------------------------------------ pool scoring (V0 + PT features)
def pool_tasks(pre: dict, only_batches: set | None = None) -> list[dict]:
    fam_v = pre["family_map_vendor"]
    q = {}
    for r in jl(X5 / "results" / "E_l3_q.jsonl"):
        if r.get("coverage_status") == "OK":
            q[(r["text"], r["cond"])] = r["q"]
    by = defaultdict(list)
    for r in rows_all():
        if only_batches is None or r["e2b_batch"] in only_batches:
            by[r["sentence_id"]].append(r)
    out = []
    for sid, rs in by.items():
        text = rs[0]["text"]
        trs = [{"key": r["row_key"], "fol": r["candidate_fol"], "family": fam_v[r["slot"]], "family_field": r["family"],
                "system": r["system"], "is_peer": True} for r in rs]
        out.append({"sentence_id": sid, "text": text, "q": q.get((text, "orig")), "stratum": "L25", "rows": trs,
                    "e2b_batch": rs[0]["e2b_batch"], "batch_key": rs[0]["batch_key"]})
    out.sort(key=lambda t: (t["e2b_batch"], t["batch_key"]))
    return out


def warm_init(mem_gb: float = 3.5) -> None:
    """exp-5 PS.init_worker + pre-import of the text-side modules (nltk / spaCy cold imports take > the 30 s pair alarm on
    this filesystem and would leave a half-initialised module). No effect on any computed value."""
    import pool_scoring as PS
    import fol_triage as FT
    FT.nlp()
    PS.init_worker(mem_gb)


def cmd_pool(a) -> None:
    import pool_scoring as PS
    pre = exp5_prereg()
    P = dict(pre["scoring_params"])
    # auxiliary readouts switched off exactly as E2-A does (scoring/score_consensus.py): NF-anchored is a closed strand;
    # c_score_align, ALIGN:g_score, l2_bow, l3_z3 go through the unchanged code path (checked by verify_exp5_copy.py)
    P.update(variants=["ALIGN"], k6_seeds=0, famfield=False, medoid_budget_s=0)
    outp = SC / "pool_E2B.jsonl"
    done = {r["sentence_id"] for r in jl(outp)}
    T = [t for t in pool_tasks(pre) if t["sentence_id"] not in done]
    if a.limit:
        T = T[: a.limit]
    missing_q = sum(t["q"] is None for t in T)
    logger.info(f"pool: {len(T)} sentences to score, workers {a.workers}, params {P}; sentences without L3 q: {missing_q}")
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=a.workers, mp_context=mp.get_context("spawn"), initializer=warm_init,
                             initargs=(3.5,)) as ex, outp.open("a") as fh:
        futs = {ex.submit(PS.score_sentence, t, P): t for t in T}
        for i, fu in enumerate(as_completed(futs)):
            t = futs[fu]
            try:
                res = fu.result()
            except Exception as e:  # noqa: BLE001 - counted as coverage failure of every row of the sentence
                logger.error(f"sentence {t['sentence_id']} failed: {e}")
                res = {"sentence_id": t["sentence_id"], "rows": [{"key": r["key"], "coverage_status": "WORKER_FAIL"} for r in t["rows"]],
                       "stats": {"error": str(e)[:300]}}
            res["e2b_batch"] = t["e2b_batch"]
            res["had_q"] = t["q"] is not None
            res["params"] = P
            fh.write(json.dumps(res, ensure_ascii=False) + "\n")
            fh.flush()
            if (i + 1) % 10 == 0:
                logger.info(f"pool {i + 1}/{len(T)} sentences, {time.time() - t0:.0f}s wall")
    logger.info(f"pool done in {time.time() - t0:.0f}s")


# ------------------------------------------------------------------------------------------------ rename controls (V0)
def cmd_controls(a) -> None:
    """V0 on E2-B's RENAME_SYN / RENAME_NONCE controls (e2bsrc/controls_E2_nolabels.jsonl, label-free rows) and on their
    parents, with EXACTLY pool_scoring's c_score_align path: canonical strings via peer_text (parse_fol + canon), eq =
    vendor_c common.eqmv under the exp-5 pair cap, peers = the sentence's parseable rows of another vendor family
    (the control inherits its parent's family), 1 - share eq. The parent's recomputed value must equal its scores value."""
    import peer_text as PT
    import pool_scoring as PS
    from common import eqmv
    PS.init_worker(3.5)
    pre = exp5_prereg()
    cap = pre["scoring_params"]["pair_cap_s"]
    nol = {r["row_key"]: r for r in jl(WS / "e2bsrc" / "candidates_E2_nolabels.jsonl")}
    ctrl = jl(WS / "e2bsrc" / "controls_E2_nolabels.jsonl")
    rows = rows_all()
    by_sid = defaultdict(list)
    for r in rows:
        by_sid[r["sentence_id"]].append(r)
    out = []
    eqc = {}

    def eq(x, y):
        if x == y:
            return True
        k = (x, y) if x < y else (y, x)
        if k not in eqc:
            res, to = PS._with_alarm(cap, eqmv, PT.parse_fol(k[0]), PT.parse_fol(k[1]))
            eqc[k] = None if (to or res is None) else res[0]
        return eqc[k]

    def v0(fol, fam, sid, own_key):
        e = PT.parse_fol(fol)
        if e is None:
            return 1.0, 0
        cs = PT.canon(e)
        P = []
        for p in by_sid[sid]:
            if p["row_key"] == own_key or p["family_vendor"] == fam or not p["parse_ok"]:
                continue
            pe = PT.parse_fol(p["candidate_fol"])
            if pe is not None:
                P.append(PT.canon(pe))
        if len(P) < 2:
            return None, len(P)
        return 1 - sum(eq(cs, q) is True for q in P) / len(P), len(P)
    t0 = time.time()
    items = []
    if a.which == "lf":
        rk = {r["row_key"]: r for r in rows}
        for c in jl(SC / "controls_lf_E2B.jsonl"):
            if c.get("status") == "ok":
                pr = rk[c["parent_row_key"]]
                items.append({"row_key": f"{c['parent_row_key']}|{c['control_type']}", "control_parent_row_key": None,
                              "_mk": c["parent_row_key"], "_sid": pr["sentence_id"], "_slot": pr["slot"], "candidate_fol": c["candidate_fol"]})
    else:
        for c in ctrl:
            par = nol.get(c["control_parent_row_key"])
            if par is not None:
                items.append({**c, "_mk": f"{par['sentence_id']}|{par['slot']}", "_sid": par["sentence_id"], "_slot": par["slot"]})
    for c in items:
        par = {"sentence_id": c["_sid"], "slot": c["_slot"]}
        mk = c["_mk"]
        prow = next(r for r in by_sid[par["sentence_id"]] if r["row_key"] == mk)
        vc, npc = v0(c["candidate_fol"], prow["family_vendor"], par["sentence_id"], mk)
        vp, npp = v0(prow["candidate_fol"], prow["family_vendor"], par["sentence_id"], mk)
        out.append({"control_row_key": c["row_key"], "control_type": c["row_key"].rsplit("|", 1)[-1], "parent_e2_row_key": c.get("control_parent_row_key"),
                    "parent_row_key": mk, "sentence_id": par["sentence_id"], "slot": par["slot"], "V0_control": vc, "V0_parent_recomputed": vp,
                    "n_peers": npc, "candidate_fol": c["candidate_fol"]})
    (SC / ("controls_lf_scores_E2B.jsonl" if a.which == "lf" else "controls_scores_E2B.jsonl")).write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in out))
    logger.info(f"controls: {len(out)} rows scored in {time.time() - t0:.0f}s")


# ------------------------------------------------------------------------------------------------ local structural features (S4)
def cmd_local(a) -> None:
    """The user's pilot structural metrics (exp-6 src/pilot_metrics.pilot_one, copied) without a story (a MALLS sentence has
    no document): pilot_joint_conflict = candidate alone UNSAT (z3 5 s), pilot_arity_incons = in-candidate arity clashes,
    pilot_shape_incons (0 without a story). pilot_dangling / pilot_rerun_jacc are not applicable (no story, no zero-shot
    rerun) and are recorded as substituted."""
    sys.path.insert(0, str(WS / "exp6src"))
    from src.pilot_metrics import pilot_one
    outp = SC / "local_E2B.jsonl"
    done = {r["key"] for r in jl(outp)}
    rows = [r for r in rows_all() if r["row_key"] not in done]
    t0 = time.time()
    with outp.open("a") as fh:
        for i, r in enumerate(rows):
            try:
                o = pilot_one((r["row_key"], r["candidate_fol"], [], None, False))
            except Exception as e:  # noqa: BLE001 - recorded as a failure of the feature
                o = {"key": r["row_key"], "fail": f"exc:{str(e)[:80]}"}
            fh.write(json.dumps(o) + "\n")
    logger.info(f"local features: {len(rows)} rows in {time.time() - t0:.0f}s")


def _verdict_of(raw) -> str | None:
    import re
    m = re.search(r'"verdict"\s*:\s*"(UNFAITHFUL|FAITHFUL)"', raw or "", re.I)
    return m.group(1).upper() if m else None


# ------------------------------------------------------------------------------------------------ assemble scores
def cmd_assemble(a) -> None:
    import peer_text as PT
    pre = exp5_prereg()
    frozen, v, neutral = pre["frozen"], pre["variant"], pre["imputation"]["neutral"]
    rows = rows_all()
    sc = {}
    stats = {}
    for s in jl(SC / "pool_E2B.jsonl"):
        stats[s["sentence_id"]] = s.get("stats", {})
        for r in s["rows"]:
            sc[r["key"]] = r
    jd = defaultdict(dict)
    for name, fn in (("flashlite", "judge_flashlite.jsonl"), ("nano", "judge_nano.jsonl"), ("costmatched", "judge_costmatched.jsonl"),
                     ("costmatched_mt300", "judge_costmatched_mt300.jsonl"), ("frontier", "judge_frontier.jsonl")):
        for r in jl(SC / fn):
            if r.get("p") is not None or (r["row_key"], r["cond"]) not in jd[name]:
                jd[name][(r["row_key"], r["cond"])] = r
    # exp-6 T1 SENSITIVITY rule (_vfb): a fallback row gets the median P(faithful) of ok rows with the same verdict
    vfb_median = {}
    for name in jd:
        for cond in ("orig", "disg"):
            for vb in ("FAITHFUL", "UNFAITHFUL"):
                vals = [1.0 - j["p"] for (k_, c_), j in jd[name].items() if c_ == cond and j.get("p") is not None and str(j.get("verdict") or "").upper() == vb]
                if vals:
                    vfb_median[(name, cond, vb)] = float(sorted(vals)[len(vals) // 2])
    dmap = {r["row_key"]: r for r in jl(SC / "disguise_E2B.jsonl")}
    loc = {r["key"]: r for r in jl(SC / "local_E2B.jsonl")}
    var = {r["row_key"]: r for r in jl(SC / "variants_E2B.jsonl")}
    fs = json.loads((SC / "frontier_subsample.json").read_text()) if (SC / "frontier_subsample.json").exists() else {"inclusion_prob": {}, "order": []}
    fset = set(fs["order"][: fs.get("n_run", len(fs["order"]))])
    out = []
    for r in rows:
        k = r["row_key"]
        s = sc.get(k)
        cov = "UNPARSEABLE" if not r["parse_ok"] else (s.get("coverage_status", "NOT_SCORED") if s else "NOT_SCORED")
        rec = {kk: r[kk] for kk in ("row_key", "sentence_id", "slot", "system", "family", "family_vendor", "model", "e2b_batch",
                                     "e2b_origin", "words", "word_bin", "n_conditions", "n_quant", "depth", "text_conditions", "parse_ok")}
        rec["coverage_status"] = cov
        s = s or {}
        rec.update({"c_score_align": s.get("c_score_align"), "g_score": s.get(f"{v}:g_score"), "c_score_nf": s.get(f"{v}:c_score_nf"),
                    "nf_c_score": s.get("NF-anchored:c_score_nf"), "n_peers_used": s.get("n_peers_used"),
                    "peer_unavailable": s.get("peer_unavailable"), "l2_bow": s.get("l2_bow"), "l3_z3": s.get("l3_z3"),
                    "eqmv_medoid_eq": s.get("eqmv_medoid_eq"), "secs_pairs": s.get(f"{v}:secs_pairs"), "secs_text": s.get("secs_text_row"),
                    "secs_sentence_total": stats.get(r["sentence_id"], {}).get("secs_total"),
                    "secs_align_sentence": stats.get(r["sentence_id"], {}).get("secs_align")})
        feats = {kk: s.get(kk) for kk in s}
        feats["coverage_status"] = cov
        if cov == "UNPARSEABLE":
            rec.update(V0=1.0, p_peer_text=1.0, p_text=1.0, flag=1)
        else:
            rec["V0"] = rec["c_score_align"]
            if s:
                fsd = PT.fused_score(frozen, feats)
                rec.update(p_peer_text=fsd["p_error"], flag=fsd["flag"], fired_signal=fsd["fired_signal"], model_used=fsd["model_used"])
                rec["p_text"] = PT.apply_logistic(frozen["text_only"], feats)
            else:
                rec.update(p_peer_text=None, p_text=None)
        rec["V0_missing_reason"] = None if rec["V0"] is not None else ("peers<2" if s else "not_scored")
        # judges: oriented (higher = more likely error); unparseable -> 1.0
        for name, col in (("flashlite", "flashlite"), ("nano", "nano"), ("costmatched", "costmatched"), ("frontier", "frontier")):
            for cond in ("orig", "disg"):
                j = jd[name].get((k, cond))
                if name == "costmatched" and (j is None or j.get("p") is None):
                    j2 = jd["costmatched_mt300"].get((k, cond))
                    j = j2 if j2 is not None and j2.get("p") is not None else j
                c = f"{col}_{cond}"
                if cov == "UNPARSEABLE":
                    rec[c] = 1.0
                    rec[c + "_status"] = "unparseable"
                elif j is None:
                    rec[c] = None
                    rec[c + "_status"] = "not_run"
                elif j.get("p") is None:
                    f = str(j.get("fail"))
                    if f in ("json_parse", "no_verdict"):
                        # exp-6 T1 PRIMARY rule (pre-declared there): after one retry an unparseable judge reply -> oriented 0.5
                        rec[c] = 0.5
                        rec[c + "_status"] = "fallback"
                        vb = _verdict_of(j.get("raw"))
                        rec[c + "_vfb"] = vfb_median.get((name, cond, vb), 0.5)
                    else:
                        rec[c] = None
                        rec[c + "_status"] = "fail:" + f[:40]
                else:
                    rec[c] = 1.0 - j["p"]
                    rec[c + "_status"] = "ok"
                if rec.get(c + "_status") != "fallback":
                    rec[c + "_vfb"] = rec[c]
                rec[c + "_cost"] = (j or {}).get("cost")
                rec[c + "_seconds"] = (j or {}).get("seconds")
        lo = loc.get(k, {})
        rec["parse_fail"] = 0 if r["parse_ok"] else 1
        for c in ("pilot_joint_conflict", "pilot_arity_incons", "pilot_shape_incons"):
            rec[c] = lo.get(c) if r["parse_ok"] else None
        vv = var.get(k, {})
        for c in ("c_exact", "V1", "V2", "V3", "V5", "V0_matrix"):
            rec[c] = 1.0 if cov == "UNPARSEABLE" else vv.get(c)
        rec["variants_status"] = vv.get("variants_status")
        d = dmap.get(k, {})
        rec["disguise_ok"] = d.get("ok")
        rec["in_frontier_subsample"] = k in fset
        rec["frontier_inclusion_prob"] = fs["inclusion_prob"].get(k) if k in fset else None
        rec["gen_cost_usd"] = r.get("gen_cost_usd")
        rec["neutral_imputation"] = {"c_score_align": neutral.get("c_score_align")}
        out.append(rec)
    p = SC / "scores_E2B.jsonl"
    p.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in out))
    cov = Counter(r["coverage_status"] for r in out)
    logger.info(f"scores_E2B: {len(out)} rows; coverage {dict(cov)}; V0 present {sum(r['V0'] is not None for r in out)}; "
                f"flashlite_disg {sum(r['flashlite_disg'] is not None for r in out)}; costmatched_disg {sum(r['costmatched_disg'] is not None for r in out)}; "
                f"frontier {sum(r['frontier_orig'] is not None for r in out)}")


if __name__ == "__main__":
    install_guard()
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["build", "disguise", "l3", "judges", "frontier_sample", "frontier_cut", "pool", "local", "controls", "assemble"])
    ap.add_argument("--which", default="")
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--n", type=int, default=300)
    ap.add_argument("--commit", type=float, default=0.0, help="$ still committed to other sweeps (kept out of this sweep's budget)")
    ap.add_argument("--keys-file", dest="keys_file", default="")
    ap.add_argument("--no-nf", dest="no_nf", action="store_true")
    a = ap.parse_args()
    {"build": cmd_build, "disguise": cmd_disguise, "l3": cmd_l3, "judges": cmd_judges, "frontier_sample": cmd_frontier_sample,
     "frontier_cut": cmd_frontier_cut, "pool": cmd_pool, "local": cmd_local, "controls": cmd_controls, "assemble": cmd_assemble}[a.cmd](a)
