"""STAGES 3 + 5: CSC peer generation (pilot, sweeps, test-retest). Label-blind: peers see (text, signature) only.

Jobs are unique (text, signature, model, variant, namespace); the LLM cache (data/csc_llm_cache.jsonl) makes every
repeat free. Each stage writes its peer file; cumulative $ is checked before every call (src/budget.py, hard stop 9.5).
Usage: python src/peers_run.py pilot | perturb_E | free | perturb_R | sig | retest | all
"""
from __future__ import annotations

import asyncio
import json
import random
import statistics
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

import aiohttp
from loguru import logger

SRC = Path(__file__).resolve().parent
ROOT = SRC.parent
sys.path.insert(0, str(SRC))
import csc_budget as budget  # noqa: E402
import csc_lib as L  # noqa: E402
import or_client as llm  # noqa: E402

DATA = ROOT / "data"
RES = ROOT / "results"
PROMPT_CHOICE = RES / "csc_prompt_choice.json"


def jl(p: Path) -> list[dict]:
    return [json.loads(x) for x in p.read_text().splitlines() if x.strip()] if p.exists() else []


def wjl(p: Path, rows) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def prompt_variant() -> str:
    if PROMPT_CHOICE.exists():
        return json.loads(PROMPT_CHOICE.read_text())["variant"]
    return "v1"


def sig_tuples(sig_json) -> list[tuple[str, int]]:
    return [(n, int(a)) for n, a in sig_json]


def peer_record(model: str, rec: dict) -> dict:
    pr = L.parse_peer(rec.get("content"))
    return {"model": model, "family": L.PEER_FAMILY[model], "raw": rec.get("content"), "fol": pr["fol"],
            "alt_fol": pr["alt_fol"], "format": pr["format"], "parse_ok": L.parse(pr["fol"]) is not None,
            "alt_parse_ok": L.parse(pr["alt_fol"]) is not None if pr["alt_fol"] else False,
            "cost": float(rec.get("cost_usd") or 0.0), "latency": rec.get("latency_s"), "status": rec.get("status"),
            "cache_hit": bool(rec.get("cache_hit")), "prompt_tokens": rec.get("prompt_tokens"),
            "completion_tokens": rec.get("completion_tokens")}


async def run_jobs(jobs: list[dict], stage: str, variant: str, namespace: str = "") -> dict:
    """jobs: [{'text', 'signature', 'models': [...]}] -> {(text, sig_key): {model: peer_record}}."""
    cl = llm.Client(stage=stage)
    out: dict = defaultdict(dict)
    t0 = time.time()
    flat = []
    for j in jobs:
        sig = sig_tuples(j["signature"])
        msgs = L.csc_prompt(j["text"], sig, variant)
        sk = L.sig_key(sig)
        for m in j["models"]:
            flat.append((j["text"], sk, m, msgs))
    logger.info(f"[{stage}] {len(jobs)} signatures, {len(flat)} model calls (variant {variant}, ns {namespace!r}); "
                f"spent so far ${budget.cumulative():.4f}")
    done = 0
    conn = aiohttp.TCPConnector(limit=80)
    async with aiohttp.ClientSession(connector=conn) as s:
        async def one(t, sk, m, msgs):
            nonlocal done
            try:
                rec = await cl.chat(s, m, msgs, L.PEER_EXTRA[m], namespace=namespace, meta={"stage": stage, "sig_key": sk})
            except llm.KeyLimit as ex:
                logger.error(f"KEY LIMIT: {ex}")
                rec = {"status": "API_FAIL", "content": None, "cost_usd": 0.0, "err": "key_limit"}
            except budget.BudgetExceeded as ex:
                logger.error(f"BUDGET: {ex}")
                rec = {"status": "API_FAIL", "content": None, "cost_usd": 0.0, "err": "budget"}
            out[(t, sk)][m] = peer_record(m, rec)
            done += 1
            if done % 500 == 0:
                logger.info(f"[{stage}] {done}/{len(flat)} calls, {time.time() - t0:.0f}s, new calls {cl.n_calls}, "
                            f"hits {cl.n_hits}, total ${budget.cumulative():.4f}")
        await asyncio.gather(*[one(*x) for x in flat])
    logger.info(f"[{stage}] done {len(flat)} in {time.time() - t0:.0f}s; new calls {cl.n_calls}, cache hits {cl.n_hits}; "
                f"total ${budget.cumulative():.4f}; key_dead={cl.key_dead}")
    return out


# ============================================================================================ job builders
def perturb_jobs(is_rcomp: bool, bases_keep: set | None = None, k4: bool = True) -> list[dict]:
    jobs = []
    for u in jl(DATA / "unique_sigs_perturb.jsonl"):
        if u["is_rcomp"] != is_rcomp:
            continue
        if bases_keep is not None and u["base_item_id"] not in bases_keep:
            continue
        jobs.append({"text": u["text"], "signature": u["signature"], "sig_key": u["sig_key"],
                     "models": list(L.PEER_MODELS) if k4 else L.peer_assignment(None)["k3"]})
    return jobs


def free_jobs() -> list[dict]:
    need: dict = {}
    for r in jl(DATA / "rcomp_free_view.jsonl"):
        if not r["cand_parse_ok"]:
            continue
        asg = L.peer_assignment(r["family"])
        models = asg["k4"] or asg["k3"]
        k = (r["text"], r["sig_key"])
        if k not in need:
            need[k] = {"text": r["text"], "signature": r["signature"], "sig_key": r["sig_key"], "models": []}
        for m in models:
            if m not in need[k]["models"]:
                need[k]["models"].append(m)
    for v in need.values():
        v["models"] = [m for m in L.PEER_MODELS if m in v["models"]]
    return list(need.values())


def sig_rows_selected() -> list[dict]:
    rows = [r for r in jl(DATA / "rcomp_sig_view.jsonl") if r.get("parse_ok")]
    uniq = {(r["text"], r["sig_key"]) for r in rows}
    shrink = RES / "shrink_state.json"
    st = json.loads(shrink.read_text()) if shrink.exists() else {}
    if len(uniq) <= 1000 and not st.get("sig_400"):
        return rows
    rng = random.Random(0)
    strata = defaultdict(list)
    for r in rows:
        strata[(r["template_id"], r["label"], r["family"])].append(r)
    target = 400 if st.get("sig_400") else 1000
    out = []
    for k in sorted(strata):
        g = strata[k]
        n = max(1, round(target * len(g) / len(rows)))
        out += rng.sample(g, min(n, len(g)))
    return out


def sig_jobs() -> list[dict]:
    need: dict = {}
    for r in sig_rows_selected():
        asg = L.peer_assignment(r["family"])
        models = asg["k4"] or asg["k3"]
        k = (r["text"], r["sig_key"])
        if k not in need:
            need[k] = {"text": r["text"], "signature": r["signature"], "sig_key": r["sig_key"], "models": []}
        for m in models:
            if m not in need[k]["models"]:
                need[k]["models"].append(m)
    for v in need.values():
        v["models"] = [m for m in L.PEER_MODELS if m in v["models"]]
    return list(need.values())


def save_peers(path: Path, jobs: list[dict], res: dict) -> None:
    rows = []
    for j in jobs:
        k = (j["text"], j["sig_key"])
        rows.append({"text": j["text"], "sig_key": j["sig_key"], "signature": j["signature"],
                     "peers": [res[k][m] for m in j["models"] if m in res.get(k, {})]})
    wjl(path, rows)


# ============================================================================================ pilot
def pilot() -> dict:
    rng = random.Random(0)
    view = jl(DATA / "perturb_view.jsonl")
    E = [r for r in view if not r["is_rcomp"]]

    def pick(pred, n):
        cand = sorted({(r["text"], r["sig_key"]): r for r in E if pred(r)}.values(), key=lambda r: r["key"])
        return rng.sample(cand, n)
    sel = pick(lambda r: r["fold"] == "BASE", 4) + pick(lambda r: r["op_label"] == "ADD_FOREIGN", 2) + \
        pick(lambda r: r["op_label"] == "MEANING_RENAME", 2) + pick(lambda r: r["op_label"] == "RENAME_SYN", 1) + \
        pick(lambda r: r["op_label"] == "RENAME_NONCE", 1)
    jobs = [{"text": r["text"], "signature": r["signature"], "sig_key": r["sig_key"], "models": list(L.PEER_MODELS),
             "kind": "PERTURB:" + ("BASE" if r["fold"] == "BASE" else r["op_label"])} for r in sel]
    fj = free_jobs()
    rng.shuffle(fj)
    jobs += [{**j, "models": list(L.PEER_MODELS), "kind": "FREE"} for j in fj[:10]]
    sj = sig_jobs()
    rng.shuffle(sj)
    jobs += [{**j, "models": list(L.PEER_MODELS), "kind": "SIG"} for j in sj[:10]]
    res = asyncio.run(run_jobs(jobs, "pilot", "v1"))
    per_model = defaultdict(lambda: {"n": 0, "json": 0, "fol_line": 0, "bare": 0, "fail": 0, "parse_ok": 0, "cost": [],
                                     "lat": [], "alt_given": 0, "api_fail": 0})
    usage = defaultdict(list)
    for j in jobs:
        k = (j["text"], j["sig_key"])
        sig = sig_tuples(j["signature"])
        for m in j["models"]:
            p = res[k][m]
            d = per_model[m]
            d["n"] += 1
            d[p["format"]] += 1
            d["parse_ok"] += int(p["parse_ok"])
            d["alt_given"] += int(bool(p["alt_fol"]))
            d["api_fail"] += int(p["status"] != "ok")
            d["cost"].append(p["cost"])
            if p["latency"] is not None:
                d["lat"].append(p["latency"])
            if j["kind"] == "PERTURB:BASE" and p["parse_ok"]:
                used = L.symbol_usage(sig, [p["fol"]])
                usage[m] += [u[0] for u in used]
    summ = {}
    for m, d in per_model.items():
        summ[m] = {"n": d["n"], "json_compliance": d["json"] / d["n"], "fol_line": d["fol_line"] / d["n"],
                   "bare": d["bare"] / d["n"], "fail": d["fail"] / d["n"], "parse_rate": d["parse_ok"] / d["n"],
                   "alt_given_rate": d["alt_given"] / d["n"], "api_fail": d["api_fail"],
                   "mean_cost_usd": statistics.mean(d["cost"]), "mean_latency_s": statistics.mean(d["lat"]) if d["lat"] else None,
                   "genuine_usage_on_base_sigs": (sum(usage[m]) / len(usage[m])) if usage[m] else None}
    all_usage = [u for m in usage for u in usage[m]]
    genuine = sum(all_usage) / len(all_usage) if all_usage else None
    mean_cost = {m: summ[m]["mean_cost_usd"] for m in summ}
    # projection (x 1.1)
    n_calls = {"perturb_E": sum(len(j["models"]) for j in perturb_jobs(False)),
               "free": sum(len(j["models"]) for j in free_jobs()),
               "perturb_R": sum(len(j["models"]) for j in perturb_jobs(True)),
               "sig": sum(len(j["models"]) for j in sig_jobs()),
               "retest": 60 * 4}
    per_stage = {}
    for st, fn in (("perturb_E", lambda: perturb_jobs(False)), ("free", free_jobs), ("perturb_R", lambda: perturb_jobs(True)),
                   ("sig", sig_jobs)):
        per_stage[st] = sum(mean_cost[m] for j in fn() for m in j["models"]) * 1.1
    per_stage["retest"] = 60 * sum(mean_cost.values()) * 1.1
    proj = sum(per_stage.values())
    variant = "v1"
    deviations = []
    if genuine is not None and genuine < 0.5:
        variant = "v1b"
        deviations.append("D-PROMPT: listed-GENUINE usage < 0.5 on base signatures -> pre-declared v1b prefix")
    low_json = [m for m in summ if summ[m]["json_compliance"] < 0.8]
    if low_json:
        deviations.append(f"JSON compliance < 0.8 for {low_json}: FOL-line fallback kept (alt_fol = null), multi-reading "
                          "reported as K3-partial")
    out = {"per_model": summ, "genuine_usage_on_base_sigs_all": genuine, "n_signatures": len(jobs),
           "kinds": dict(Counter(j["kind"] for j in jobs)), "n_calls_projected": n_calls,
           "projected_cost_usd_by_stage": per_stage, "projected_total_usd": proj,
           "pilot_spend_usd": sum(p["cost"] for k in res for p in res[k].values() if not p["cache_hit"]),
           "shrink_needed": proj > 8.5, "prompt_variant_chosen": variant, "deviations": deviations,
           "decision_rule": "variant v1b iff listed-GENUINE usage < 0.5 on the pilot base signatures (label-blind)"}
    (RES / "pilot_projection.json").write_text(json.dumps(out, indent=1))
    import hashlib
    PROMPT_CHOICE.write_text(json.dumps({"variant": variant, "block_template": L.BLOCK_TEMPLATE,
                                         "block_template_sha256": L.block_template_sha256(),
                                         "v1b_prefix": L.V1B_PREFIX if variant == "v1b" else None,
                                         "prompt_file_sha256": hashlib.sha256(L.PROMPT_PATH.read_bytes()).hexdigest(),
                                         "decided_from": "results/pilot_projection.json (pilot only, no outcomes)"}, indent=1))
    wjl(DATA / "peers_pilot.jsonl", [{"kind": j["kind"], "text": j["text"], "sig_key": j["sig_key"],
                                      "peers": [res[(j["text"], j["sig_key"])][m] for m in j["models"]]} for j in jobs])
    logger.info(f"pilot: {json.dumps(summ, indent=0)[:1500]}")
    logger.info(f"pilot genuine usage {genuine}, projection ${proj:.2f}, variant {variant}")
    return out


# ============================================================================================ sweeps
def shrink_state() -> dict:
    p = RES / "shrink_state.json"
    return json.loads(p.read_text()) if p.exists() else {}


def apply_shrink_if_needed(stage: str) -> dict:
    st = shrink_state()
    if budget.soft_exceeded() or json.loads((RES / "pilot_projection.json").read_text()).get("shrink_needed"):
        order = ["sig_400", "rcomp_50", "drop_k4_perturb", "drop_retest"]
        for o in order:
            if not st.get(o):
                st[o] = f"applied before stage {stage} at ${budget.cumulative():.3f}"
                logger.warning(f"SHRINK: {o}")
                break
        (RES / "shrink_state.json").write_text(json.dumps(st, indent=1))
    return st


def rcomp_50_bases() -> set:
    view = jl(DATA / "perturb_view.jsonl")
    bt = sorted({(r["template_id"], r["base_item_id"]) for r in view if r["fold"] == "BASE" and r["is_rcomp"]})
    by = defaultdict(list)
    for t, b in bt:
        by[t].append(b)
    rng = random.Random(0)
    keep = set()
    for t in sorted(by):
        keep |= set(rng.sample(by[t], max(1, round(len(by[t]) / 2))))
    return keep


def stage(name: str) -> None:
    variant = prompt_variant()
    st = apply_shrink_if_needed(name)
    if name == "perturb_E":
        jobs = perturb_jobs(False, k4=not st.get("drop_k4_perturb"))
        res = asyncio.run(run_jobs(jobs, name, variant))
        save_peers(DATA / "peers_perturb_E.jsonl", jobs, res)
    elif name == "perturb_R":
        keep = rcomp_50_bases() if st.get("rcomp_50") else None
        jobs = perturb_jobs(True, keep, k4=not st.get("drop_k4_perturb"))
        res = asyncio.run(run_jobs(jobs, name, variant))
        save_peers(DATA / "peers_perturb_R.jsonl", jobs, res)
    elif name == "free":
        jobs = free_jobs()
        res = asyncio.run(run_jobs(jobs, name, variant))
        save_peers(DATA / "peers_free_unique.jsonl", jobs, res)
    elif name == "sig":
        jobs = sig_jobs()
        res = asyncio.run(run_jobs(jobs, name, variant))
        save_peers(DATA / "peers_sig.jsonl", jobs, res)
    elif name == "retest":
        if st.get("drop_retest"):
            logger.warning("retest dropped by shrink order")
            return
        jobs = perturb_jobs(False)
        rng = random.Random(0)
        jobs = rng.sample(sorted(jobs, key=lambda j: (j["text"], j["sig_key"])), 60)
        res = asyncio.run(run_jobs(jobs, name, variant, namespace="retest-nonce-1"))
        save_peers(DATA / "peers_retest.jsonl", jobs, res)
    else:
        raise ValueError(name)


def main(argv: list[str]) -> None:
    what = argv[1] if len(argv) > 1 else "all"
    if what == "pilot":
        pilot()
        return
    order = ["perturb_E", "free", "perturb_R", "sig", "retest"] if what == "all" else [what]
    for s in order:
        stage(s)


if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
    logger.add(ROOT / "logs" / "peers_run.log", rotation="30 MB", level="DEBUG")
    main(sys.argv)
