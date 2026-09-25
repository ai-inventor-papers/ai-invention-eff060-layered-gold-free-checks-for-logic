#!/usr/bin/env python3
# NOTE (published copy): this file names server paths this repository
# does not publish (a stage it does not ship, or another run's workspace),
# so the steps that read them will not run from a clone as written:
#   /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5
"""S7b / S7c / S9: LLM-judge comparators through the vendored exp-D judge path (identical rubric, disguise, cache keying).

cheap     google/gemini-2.5-flash-lite, judges.judge_json(RUBRIC_A, USER_JSON_A, max_tokens=150, json_object, T=0) on
          (a) disguise_item(text, fol, seed_text=norm(text)) [judge_cheap_disg, the pre-registered bar] and
          (b) the original (text, fol) [judge_cheap_orig]; EVERY parseable row of the condition (label-blind).
          Order: all disguised units first, then all original units (so a budget stop leaves the bar complete).
frontier  exp-D judge_strong config (google/gemini-3.1-pro-preview, reasoning effort low, max_tokens 4000), same rubric,
          on a sha1-ordered stratified SIG subsample (target 75 ERROR / 75 CORRECT, >= 5 per template where available);
          10-call pilot first; the subsample is cut to what the allowance covers (orig first, then disg).
Score = 1 - P(faithful) (higher = more suspicious). Parse failure -> one retry inside judge_json -> None (counted).
A disguise failure -> judge_cheap_disg None for that row (counted, never silent).
Guard: results/testability_<COND>.json must exist and predate this process.

usage: run_judges.py cheap --cond SIG|FREE [--limit N] [--cap USD]
       run_judges.py frontier [--pilot] [--n-rows N] [--cap USD]
       run_judges.py regress   (T4: exp-5 cache-key + disguise regression on 10 dataset-E rows, $0)
"""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import os
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"
for p in (ROOT / "src" / "vendor_x5", ROOT / "src" / "vendor_x5" / "vendor_a", ROOT / "src", ROOT / "rcomp" / "src_e"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
sys.setrecursionlimit(10000)

from loguru import logger  # noqa: E402

from vendor_d import budget as VB  # noqa: E402
from vendor_d import judges as J  # noqa: E402
from vendor_d.common import norm  # noqa: E402

import artifact_budget as ART  # noqa: E402
import score_consensus as SC  # noqa: E402

CHEAP = "google/gemini-2.5-flash-lite"
FRONTIER = "google/gemini-3.1-pro-preview"
FRONTIER_EXTRA = {"reasoning": {"effort": "low"}}
FRONTIER_MAXTOK = 4000
KEY_FLOOR = 0.25


def jl(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []


def sha1(s: str) -> str:
    return hashlib.sha1(s.encode()).hexdigest()


def rows_for(cond: str) -> list[dict]:
    """Every parseable candidate row of the condition (label-blind): key, text, fol, template."""
    out = []
    for t in SC.build_tasks(cond):
        for r in t["rows"]:
            if r["parse_ok"] and r["fol"].strip():
                out.append({"row_key": r["key"], "sentence_id": t["sentence_id"], "text": t["text"], "fol": r["fol"],
                            "template_id": t["template_id"], "slot": r["slot"]})
    return out


def disguise_map(rows: list[dict], cond: str) -> dict:
    from vendor_d.disguise import disguise_item
    p = RES / f"disguise_map_{cond}.jsonl"
    have = {r["row_key"]: r for r in jl(p)}
    todo = [r for r in rows if r["row_key"] not in have]
    t0 = time.time()
    with p.open("a") as fh:
        for i, r in enumerate(todo):
            try:
                d = disguise_item(r["text"], r["fol"], seed_text=norm(r["text"]))
                rec = {"row_key": r["row_key"], "text_d": d["text_d"], "fol_d": d["fol_d"], "ok": d["ok"],
                       "fail_reasons": d["fail_reasons"], "leak_text": d["leak_text"], "leak_formula": d["leak_formula"]}
            except Exception as ex:  # noqa: BLE001 - a disguise failure is counted, never silent
                logger.warning(f"disguise failed {r['row_key']}: {ex}")
                rec = {"row_key": r["row_key"], "text_d": None, "fol_d": None, "ok": False, "fail_reasons": [f"exc:{str(ex)[:80]}"]}
            have[r["row_key"]] = rec
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            if (i + 1) % 500 == 0:
                logger.info(f"disguise {i + 1}/{len(todo)} {time.time() - t0:.0f}s")
    return have


def guard(cond: str, t_start: float) -> None:
    if cond == "FREE" and os.environ.get("FREE_PREJOIN") == "1":
        # prereg S8: the FREE declaration must precede any FREE score being JOINED to labels (not computed); judges are
        # label-blind, so FREE judge scores may be computed first; analyse.py enforces declaration-before-join.
        logger.warning("FREE_PREJOIN=1: computing label-blind FREE judge scores before the FREE declaration (join guarded later)")
        return
    p = RES / f"testability_{cond}.json"
    if not p.exists() or p.stat().st_mtime >= t_start:
        raise SystemExit(f"{p.name} missing or newer than this judge run: declare testability first")


async def judge_units(units: list[tuple], outp: Path, component: str, model: str, max_tokens: int, extra: dict | None,
                      tag: str, chunk: int = 300, concurrency: int = 16) -> bool:
    """units: (row_key, cond, text, fol). Appends to outp; returns False when stopped for budget/key."""
    have = {(r["row_key"], r["cond"], r.get("judge", "cheap")) for r in jl(outp) if r.get("p") is not None}
    todo = [u for u in units if (u[0], u[1], tag) not in have]
    logger.info(f"[{tag}] {len(todo)} units to score ({len(units)} requested)")
    async with VB.Budget(concurrency=concurrency) as b:
        for s in range(0, len(todo), chunk):
            kr = ART.key_remaining(force=True)
            logger.info(f"[{tag}] chunk {s // chunk}: key remaining ${kr}; component spend ${b.by_comp.get(component, 0):.4f}")
            if kr is not None and kr < KEY_FLOOR:
                logger.error(f"[{tag}] shared key below floor (${kr}); stopping (resumable)")
                return False
            part = todo[s:s + chunk]
            t0 = time.time()
            outs = await J.gather_limited([J.judge_json(b, component=component, model=model, rubric=J.RUBRIC_A, text=t, fol=f,
                                                        item_id=f"{k}|{c}", max_tokens=max_tokens, extra=extra,
                                                        user_tmpl=J.USER_JSON_A) for k, c, t, f in part], f"{tag} chunk {s // chunk}")
            with outp.open("a") as fh:
                for (k, c, _, _), o in zip(part, outs):
                    fh.write(json.dumps({"row_key": k, "cond": c, "judge": tag, "model": model,
                                         **{kk: o.get(kk) for kk in ("p", "verdict", "type", "reason", "fail", "cost", "seconds")}},
                                        ensure_ascii=False) + "\n")
            nf = sum(o.get("p") is None for o in outs)
            nb = sum(str(o.get("fail") or "").startswith("budget") for o in outs)
            logger.info(f"[{tag}] chunk {s // chunk}: {len(part)} units in {time.time() - t0:.0f}s, failures {nf} (budget {nb}); "
                        f"spend ${b.spent:.4f}")
            if nb:
                logger.error(f"[{tag}] budget stop inside chunk ({nb} units); stopping (resumable)")
                return False
            if nf > 0.5 * len(part):
                logger.error(f"[{tag}] more than half failed ({[o.get('fail') for o in outs if o.get('p') is None][:3]}); stopping")
                return False
    return True


def run_cheap(cond: str, limit: int, cap: float) -> None:
    t_start = time.time()
    guard(cond, t_start)
    VB.CAP_TOTAL = 9.5
    VB.CAPS = {**VB.CAPS, "judge_cheap_primary": cap}
    rows = sorted(rows_for(cond), key=lambda r: sha1("judge|" + r["row_key"]))
    if limit:
        rows = rows[:limit]
    dmap = disguise_map(rows, cond)
    nfail = sum(1 for r in rows if dmap[r["row_key"]].get("text_d") is None or dmap[r["row_key"]].get("fol_d") is None)
    logger.info(f"[{cond}] {len(rows)} parseable rows; disguise failures {nfail} ({nfail / max(1, len(rows)):.1%})")
    disg = [(r["row_key"], "disg", dmap[r["row_key"]]["text_d"], dmap[r["row_key"]]["fol_d"]) for r in rows
            if dmap[r["row_key"]].get("text_d") is not None and dmap[r["row_key"]].get("fol_d") is not None]
    orig = [(r["row_key"], "orig", r["text"], r["fol"]) for r in rows]
    outp = RES / f"judge_{cond}.jsonl"
    ok = asyncio.run(judge_units(disg, outp, "judge_cheap_primary", CHEAP, 150, None, "cheap"))
    if ok:
        ok = asyncio.run(judge_units(orig, outp, "judge_cheap_primary", CHEAP, 150, None, "cheap"))
    logger.info(f"[{cond}] cheap judge finished (complete={ok}); artifact spend ${ART.total():.4f}")


def frontier_subsample(n_target: int = 150) -> list[dict]:
    """sha1-ordered, stratified 50/50 ERROR/CORRECT, proportional over templates with >= 5 per template where available."""
    labs = [r for r in jl(RES / "sig_labels.jsonl") if r["label"] in ("CORRECT", "ERROR") and r["slot"] in SC.FEW]
    out = []
    for lab in ("ERROR", "CORRECT"):
        pool = [r for r in labs if r["label"] == lab]
        by_t = defaultdict(list)
        for r in sorted(pool, key=lambda r: sha1("frontier|" + r["row_key"])):
            by_t[r["template_id"]].append(r)
        half = n_target // 2
        quota = {t: max(min(5, len(v)), round(half * len(v) / len(pool))) for t, v in by_t.items()}
        while sum(quota.values()) > half:  # trim the largest quotas
            t = max(quota, key=lambda t: (quota[t] - 5, len(by_t[t])))
            quota[t] -= 1
        while sum(quota.values()) < half and any(quota[t] < len(by_t[t]) for t in quota):
            t = max((t for t in quota if quota[t] < len(by_t[t])), key=lambda t: len(by_t[t]) - quota[t])
            quota[t] += 1
        for t, v in by_t.items():
            out += v[:quota[t]]
    return sorted(out, key=lambda r: sha1("frontier|" + r["row_key"]))


def run_frontier(pilot: bool, n_rows: int, cap: float) -> None:
    t_start = time.time()
    guard("SIG", t_start)
    VB.CAP_TOTAL = 9.5
    VB.CAPS = {**VB.CAPS, "strong": cap}
    sub = frontier_subsample(150)
    (RES / "frontier_subsample.json").write_text(json.dumps([{k: r[k] for k in ("row_key", "label", "template_id")} for r in sub], indent=0))
    if pilot:
        sel = sub[:5]
    else:
        # keep the ERROR/CORRECT balance under a cut: interleave by label in sha1 order
        e = [r for r in sub if r["label"] == "ERROR"]
        c = [r for r in sub if r["label"] == "CORRECT"]
        inter = [x for pair in zip(e, c) for x in pair] + e[len(c):] + c[len(e):]
        sel = inter[:n_rows] if n_rows else inter
    task_rows = {r["row_key"]: r for r in rows_for("SIG")}
    dmap = disguise_map([task_rows[r["row_key"]] for r in sel], "SIG")
    orig = [(r["row_key"], "orig", task_rows[r["row_key"]]["text"], task_rows[r["row_key"]]["fol"]) for r in sel]
    disg = [(r["row_key"], "disg", dmap[r["row_key"]]["text_d"], dmap[r["row_key"]]["fol_d"]) for r in sel
            if dmap[r["row_key"]].get("text_d") and dmap[r["row_key"]].get("fol_d")]
    outp = RES / "judge_frontier_SIG.jsonl"
    ok = asyncio.run(judge_units(orig, outp, "strong", FRONTIER, FRONTIER_MAXTOK, FRONTIER_EXTRA, "frontier", chunk=50, concurrency=12))
    if ok:
        ok = asyncio.run(judge_units(disg, outp, "strong", FRONTIER, FRONTIER_MAXTOK, FRONTIER_EXTRA, "frontier", chunk=50, concurrency=12))
    got = [r for r in jl(outp) if r.get("p") is not None]
    costs = [r["cost"] for r in jl(outp) if r.get("cost")]
    logger.info(f"frontier: {len(got)} scored units; mean $/call {sum(costs) / max(1, len(costs)):.5f}; complete={ok}")


def regress() -> None:
    """T4 ($0): identical prompt construction -> identical exp-5 cache keys for 10 dataset-E rows; disguise identical."""
    X5 = Path("/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5")
    cache_keys = set()
    for l in (X5 / "results" / "llm_cache.jsonl").read_text().splitlines():
        try:
            cache_keys.add(json.loads(l)["key"])
        except (json.JSONDecodeError, KeyError):
            continue
    judged = [r for r in jl(X5 / "results" / "E_judge.jsonl") if r.get("p") is not None][:10]
    blind = {r["row_key"]: r for r in jl(X5 / "data" / "E_blind.jsonl")}
    dm = {r["row_key"]: r for r in jl(X5 / "results" / "E_disguise_map.jsonl")}
    hits, dis_same = [], []
    from vendor_d.disguise import disguise_item
    for r in judged:
        b = blind[r["row_key"]]
        if r["cond"] == "disg":
            text, fol = dm[r["row_key"]]["text_d"], dm[r["row_key"]]["fol_d"]
        else:
            text, fol = b["text"], b["candidate_fol"]
        msgs = [{"role": "system", "content": J.RUBRIC_A}, {"role": "user", "content": J.USER_JSON_A.format(text=text, fol=fol)}]
        k = J._ckey("judge_cheap_primary", CHEAP, msgs, {"max_tokens": 150, "response_format": {"type": "json_object"}})
        hits.append(k in cache_keys)
    for rk in list(dm)[:5]:
        b = blind[rk]
        d = disguise_item(b["text"], b["candidate_fol"] if b["candidate_fol"].strip() else None, seed_text=norm(b["text"]))
        dis_same.append(d["text_d"] == dm[rk]["text_d"] and d["fol_d"] == dm[rk]["fol_d"])
    out = {"n_judge_rows": len(judged), "cache_key_hits": sum(hits), "disguise_identical": sum(dis_same), "n_disguise": len(dis_same),
           "prompt_sha1": {k: J.PROMPT_SHA[k] for k in ("RUBRIC_A", "USER_JSON_A")}, "pass": all(hits) and all(dis_same)}
    (RES / "judge_regression_T4.json").write_text(json.dumps(out, indent=1))
    logger.info(json.dumps(out))


def main():
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
    logger.add(ROOT / "logs" / "run_judges.log", rotation="30 MB", level="DEBUG")
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["cheap", "frontier", "regress"])
    ap.add_argument("--cond", choices=["SIG", "FREE"], default="SIG")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--cap", type=float, default=0.7)
    ap.add_argument("--pilot", action="store_true")
    ap.add_argument("--n-rows", type=int, default=0)
    a = ap.parse_args()
    if a.cmd == "cheap":
        run_cheap(a.cond, a.limit, a.cap)
    elif a.cmd == "frontier":
        run_frontier(a.pilot, a.n_rows, a.cap)
    else:
        regress()


if __name__ == "__main__":
    main()
