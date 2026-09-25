#!/usr/bin/env python3
# NOTE (published copy): this file names server paths this repository
# does not publish (a stage it does not ship, or another run's workspace),
# so the steps that read them will not run from a clone as written:
#   /ai-inventor/aii_data/runs/run_u75jRHUss0zo/iter_3/gen_hypo/claude_agent/data/yuan-yang__MALLS-v0__MALLS-v0.1-train.json
"""STEP 3/4: peer translations (6 fresh model families, T=0) and self-consistency samples (K=5, T=0.7)
through OpenRouter, with a response cache (never re-bills), a running cost total checked before every
call, hard stops, and a separate parse/map stage that turns cached responses into
results/peer_outputs.jsonl and results/sc_samples.jsonl.

usage:  peers.py call  --arm {peers,sc_cheap,sc_same} [--limit N] [--dry-run]
        peers.py build
        peers.py estimate
"""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import os
import random
import re
import sys
import time
from collections import Counter
from pathlib import Path

import aiohttp
from loguru import logger

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from common import LLM_SYSTEMS, norm, safe_parse  # noqa: E402

RES, RAW, LOGS = ROOT / "results", ROOT / "data" / "peer_raw", ROOT / "logs"
COST_LOG = LOGS / "cost_log.jsonl"
MALLS_TRAIN = Path("/ai-inventor/aii_data/runs/run_u75jRHUss0zo/iter_3/gen_hypo/claude_agent/data/yuan-yang__MALLS-v0__MALLS-v0.1-train.json")
URL = "https://openrouter.ai/api/v1/chat/completions"

PEERS = [  # (peer id, model, family) -- cheapest current non-reasoning instruct endpoint per family
    ("P1", "meta-llama/llama-3.3-70b-instruct", "meta"),
    ("P2", "qwen/qwen3-235b-a22b-2507", "qwen"),
    ("P3", "deepseek/deepseek-chat-v3.1", "deepseek"),
    ("P4", "mistralai/mistral-small-3.2-24b-instruct", "mistral"),
    ("P5", "google/gemini-2.5-flash-lite", "google"),
    ("P6", "openai/gpt-4.1-mini", "openai"),
]
SC_CHEAP = ("SCc", "openai/gpt-4.1-nano", "openai")
SC_SAME = ("SCs", "openai/gpt-3.5-turbo", "openai")
DISABLE_REASONING = {"deepseek/deepseek-chat-v3.1", "google/gemini-2.5-flash-lite", "qwen/qwen3-235b-a22b-2507"}
STOP_OPTIONAL, STOP_ALL = 8.0, 9.5

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(LOGS / "peers.log", rotation="30 MB", level="DEBUG")


# ------------------------------------------------------------------ prompts
def folio_prompt(u: dict) -> str:
    t = (ROOT / "data" / "logiclm" / "FOLIO.txt").read_text()
    return t.replace("[[PROBLEM]]", u["problem"]).replace("[[QUESTION]]", u["question"])


def malls_shots() -> list[dict]:
    """sha1-first 3 MALLS-train examples with <=20 words, parseable, 'exact-gold-looking'."""
    data = json.loads(MALLS_TRAIN.read_text())
    data.sort(key=lambda r: hashlib.sha1(r["NL"].encode()).hexdigest())
    out = []
    for r in data:
        nl, f = r["NL"].strip(), r["FOL"].strip()
        if len(nl.split()) > 20 or safe_parse(f) is None:
            continue
        if not re.search(r"[∀∃]", f) or re.search(r"[∈=<>]", f) or "\n" in f:
            continue
        out.append({"NL": nl, "FOL": f})
        if len(out) == 3:
            break
    return out


HEADER = """Given a sentence, the task is to parse the sentence into a first-order logic formular.
The grammar of the first-order logic formular is defined as follows:
1) logical conjunction of expr1 and expr2: expr1 ∧ expr2
2) logical disjunction of expr1 and expr2: expr1 ∨ expr2
3) logical exclusive disjunction of expr1 and expr2: expr1 ⊕ expr2
4) logical negation of expr1: ¬expr1
5) expr1 implies expr2: expr1 → expr2
6) expr1 if and only if expr2: expr1 ↔ expr2
7) logical universal quantification: ∀x
8) logical existential quantification: ∃x
Answer with exactly one line of the form 'FOL ::: <sentence>'."""


def malls_prompt(sentence: str, shots: list[dict]) -> str:
    parts = [HEADER]
    for s in shots:
        parts.append(f"------\nSentence:\n{s['NL']}\n###\n{s['FOL']} ::: {s['NL']}")
    parts.append(f"------\nSentence:\n{sentence}\n###")
    return "\n".join(parts)


# Format-only system message (identical for every peer and SC arm). Modern chat models do not continue the
# Logic-LM few-shot pattern on their own (dry run v0: prose, re-solved demo problems); the user prompt stays verbatim.
SYSTEM_F = ("You translate natural language into first-order logic. Continue the pattern of the examples for the LAST "
            "problem only. Output exactly three blocks and nothing else: 'Predicates:', 'Premises:' and 'Conclusion:', "
            "each line written as 'FOL ::: natural-language sentence', with one Premises line per sentence of the problem, "
            "in order, copying each sentence after ':::'. Do not answer the question, do not explain, no markdown.")
SYSTEM_M = ("You translate natural language into first-order logic. Output exactly one line of the form "
            "'FOL ::: sentence' for the last sentence and nothing else. No explanation, no markdown.")


def unit_prompt(u: dict, shots) -> str:
    return malls_prompt(u["sentence"], shots) if u["type"] == "U_M" else folio_prompt(u)


# ------------------------------------------------------------------ cost ledger
class Ledger:
    def __init__(self):
        self.total = 0.0
        if COST_LOG.exists():
            for l in COST_LOG.read_text().splitlines():
                if l.strip():
                    self.total += float(json.loads(l).get("cost_usd") or 0)
        self.prices = {}
        cat = ROOT / "data" / "or_models.json"
        if cat.exists():
            for m in json.loads(cat.read_text())["data"]:
                p = m.get("pricing") or {}
                try:
                    self.prices[m["id"]] = (float(p.get("prompt", 0)), float(p.get("completion", 0)))
                except (TypeError, ValueError):
                    pass

    def add(self, model: str, usage: dict, meta: dict) -> float:
        cost = usage.get("cost")
        if cost is None:
            pi, po = self.prices.get(model, (0.0, 0.0))
            cost = usage.get("prompt_tokens", 0) * pi + usage.get("completion_tokens", 0) * po
        cost = float(cost)
        self.total += cost
        rec = {"ts": time.time(), "model": model, "cost_usd": cost, "prompt_tokens": usage.get("prompt_tokens"),
               "completion_tokens": usage.get("completion_tokens"), "running_total": round(self.total, 6), **meta}
        with open(COST_LOG, "a") as f:
            f.write(json.dumps(rec) + "\n")
        led = os.environ.get("AII_COST_LEDGER")
        if led:
            try:
                with open(led, "a") as f:
                    f.write(json.dumps({"ts": rec["ts"], "tool": "openrouter_direct", "cost_usd": cost, "model": model,
                                        "input_tokens": usage.get("prompt_tokens", 0),
                                        "output_tokens": usage.get("completion_tokens", 0)}) + "\n")
            except OSError:
                logger.exception("ledger write failed")
        return cost


def cache_path(model: str, unit_id: str, sample: int, attempt: int) -> Path:
    slug = model.replace("/", "__")
    safe = re.sub(r"[^A-Za-z0-9_.-]", "_", unit_id)
    return RAW / slug / f"{safe}__s{sample}__a{attempt}.json"


def usable(text: str, utype: str) -> bool:
    p = parse_response(text, utype)
    if utype == "U_M":
        return bool(p["conclusion"])
    return bool(p["premises"]) and (bool(p["conclusion"]) or utype == "U_P")


async def one_call(session, sem, ledger: Ledger, *, model: str, prompt: str, temperature: float, meta: dict,
                   stop_at: float, max_tokens: int = 1500) -> dict | None:
    system = SYSTEM_M if meta.get("unit_id", "").startswith("M:") else SYSTEM_F
    body = {"model": model, "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens, "usage": {"include": True}}
    if temperature > 0:
        body["top_p"] = 1.0
    if model in DISABLE_REASONING:
        body["reasoning"] = {"enabled": False}
    headers = {"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}", "Content-Type": "application/json"}
    async with sem:
        for attempt in range(4):
            if ledger.total >= stop_at:
                logger.warning(f"cost stop {ledger.total:.3f} >= {stop_at}: skipping {meta}")
                return None
            t0 = time.time()
            try:
                async with session.post(URL, json=body, headers=headers, timeout=aiohttp.ClientTimeout(total=180)) as r:
                    js = await r.json(content_type=None)
                    if r.status != 200 or "choices" not in js:
                        raise RuntimeError(f"HTTP {r.status}: {str(js)[:300]}")
            except (aiohttp.ClientError, asyncio.TimeoutError, RuntimeError, json.JSONDecodeError) as e:
                logger.warning(f"{model} {meta.get('unit_id')} attempt {attempt}: {str(e)[:200]}")
                await asyncio.sleep(2 ** attempt + random.random())
                continue
            usage = js.get("usage") or {}
            cost = ledger.add(model, usage, meta)
            text = (js["choices"][0].get("message") or {}).get("content") or ""
            logger.debug(f"{model} {meta} ${cost:.5f} out={text[:200]!r}")
            return {"text": text, "usage": usage, "cost_usd": cost, "latency_s": round(time.time() - t0, 2),
                    "provider": js.get("provider"), "model_served": js.get("model")}
    return None


async def run_unit(session, sem, ledger, shots, *, model, u, sample, temperature, stop_at):
    """One (model, unit, sample): cached; one retry (same prompt) on empty/unusable output."""
    for attempt in range(2):
        p = cache_path(model, u["unit_id"], sample, attempt)
        if p.exists():
            rec = json.loads(p.read_text())
        else:
            rec = await one_call(session, sem, ledger, model=model, prompt=unit_prompt(u, shots), temperature=temperature,
                                 meta={"unit_id": u["unit_id"], "sample": sample, "attempt": attempt}, stop_at=stop_at)
            if rec is None:
                return
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(json.dumps(rec, ensure_ascii=False))
        if usable(rec["text"], u["type"]):
            return


def load_units() -> tuple[list, dict]:
    js = json.loads((RES / "units.json").read_text())
    return js["units"], js["premise_unit"]


def sc_same_units(units: list) -> list:
    """U_F / U_P units that carry a gpt-3.5-turbo track-L candidate (conclusion or premise source)."""
    items = json.loads((RES / "screen_items.json").read_text())
    _, prem_unit = load_units()
    need = set()
    for it in items:
        if it["track"] != "L" or it["system"] != "gpt-3.5-turbo":
            continue
        if it["kind"] == "conclusion":
            need.add(f"F:{it['concl_id']}")
        elif it["sentence_key"] in prem_unit:
            need.add(prem_unit[it["sentence_key"]])
    return [u for u in units if u["unit_id"] in need]


async def call_arm(arm: str, limit: int | None, dry: bool):
    units, _ = load_units()
    shots = malls_shots()
    ledger = Ledger()
    logger.info(f"running total at start: ${ledger.total:.4f}")
    if dry:
        rnd = random.Random(0)
        uf = [u for u in units if u["type"] == "U_F" and u["logiclm_entry"]]
        um = [u for u in units if u["type"] == "U_M"]
        units = rnd.sample(uf, 3) + rnd.sample(um, 3)
    elif limit:
        units = units[:limit]
    if arm == "peers":
        jobs = [(m, u, 0, 0.0, STOP_ALL) for _, m, _ in PEERS for u in units]
    elif arm == "sc_cheap":
        jobs = [(SC_CHEAP[1], u, k, 0.7, STOP_OPTIONAL) for u in units for k in range(5)]
    elif arm == "sc_same":
        su = sc_same_units(units)
        logger.info(f"SC_same units: {len(su)}")
        jobs = [(SC_SAME[1], u, k, 0.7, STOP_OPTIONAL) for u in su for k in range(5)]
    else:
        raise ValueError(arm)
    logger.info(f"arm={arm} jobs={len(jobs)}")
    sems = {}
    conn = aiohttp.TCPConnector(limit=64)
    async with aiohttp.ClientSession(connector=conn) as session:
        tasks = []
        for m, u, k, t, stop in jobs:
            sem = sems.setdefault(m, asyncio.Semaphore(8))
            tasks.append(run_unit(session, sem, ledger, shots, model=m, u=u, sample=k, temperature=t, stop_at=stop))
        done = 0
        for fut in asyncio.as_completed(tasks):
            try:
                await fut
            except Exception:
                logger.exception("unit failed")
            done += 1
            if done % 100 == 0:
                logger.info(f"{arm}: {done}/{len(tasks)} done, running total ${ledger.total:.4f}")
    logger.info(f"arm={arm} finished; running total ${ledger.total:.4f}")


# ------------------------------------------------------------------ parse + map
SEC = re.compile(r"^[#*\s`>-]*(predicates|premises|conclusions?)\b\s*[:*]*", re.I)


def parse_response(text: str, utype: str) -> dict:
    out = {"premises": [], "conclusion": []}
    sec = "conclusion" if utype == "U_M" else None
    for line in (text or "").split("\n"):
        t = line.strip().strip("`").strip()
        m = SEC.match(t)
        if m and ":::" not in t:
            w = m.group(1).lower()
            sec = "premises" if w.startswith("prem") else ("conclusion" if w.startswith("concl") else "pred")
            if sec in ("premises", "pred") and out["conclusion"]:
                out = {"premises": [], "conclusion": []}  # a later problem block: keep only the LAST block
            continue
        if ":::" not in t or sec not in ("premises", "conclusion"):
            continue
        f, n = t.split(":::", 1)
        if f.strip().strip("`*").strip().upper() == "FOL":
            # the model echoed the format label: 'FOL ::: <formula> [::: <sentence>]'
            rest = n.split(":::", 1)
            f, n = rest[0], (rest[1] if len(rest) > 1 else "")
        f = re.sub(r"^\s*(?:[-*•]|\d+[.)])\s+", "", f).strip().strip("`*").strip()
        f = re.sub(r"^FOL\s*:\s*", "", f)
        n = n.strip().strip("`*").strip()
        out[sec].append((f, n))
    return out


def map_unit(u: dict, parsed: dict) -> list[tuple[str, str, str, str]]:
    """-> [(sentence_key, nl, fol, mapping_mode)]"""
    out = []
    if u["type"] == "U_M":
        if parsed["conclusion"]:
            f, n = parsed["conclusion"][0]
            out.append((u["conclusion_key"], n, f, "text" if norm(n) == u["conclusion_key"] else "position"))
        return out
    if u["type"] == "U_F" and parsed["conclusion"]:
        f, n = parsed["conclusion"][0]
        out.append((u["conclusion_key"], n, f, "text" if norm(n) == u["conclusion_key"] else "position"))
    known = {}
    for s in LLM_SYSTEMS:
        for nl, key in u["premise_slots"].get(s, []):
            known.setdefault(norm(nl), key)
            known.setdefault(key, key)
    for nl, key in u["context_sents"]:
        known.setdefault(key, key)
    prem = parsed["premises"]
    pos_list = None
    for s in ["gpt-4", "gpt-3.5-turbo", "text-davinci-003"]:
        sl = u["premise_slots"].get(s, [])
        if sl and len(sl) == len(prem):
            pos_list = [k for _, k in sl]
            break
    if pos_list is None and len(u["context_sents"]) == len(prem):
        pos_list = [k for _, k in u["context_sents"]]
    for i, (f, n) in enumerate(prem):
        k = norm(n)
        if k in known:
            out.append((known[k], n, f, "text"))
        elif pos_list is not None:
            out.append((pos_list[i], n, f, "position"))
        else:
            out.append((None, n, f, "unmapped"))
    return out


def final_record(model: str, unit_id: str, sample: int) -> dict | None:
    """Last attempt on disk wins (attempt 1 exists only if attempt 0 was unusable)."""
    for attempt in (1, 0):
        p = cache_path(model, unit_id, sample, attempt)
        if p.exists():
            rec = json.loads(p.read_text())
            rec["attempts"] = attempt + 1
            rec["cost_all_attempts"] = sum(json.loads(cache_path(model, unit_id, sample, a).read_text())["cost_usd"]
                                           for a in range(attempt + 1) if cache_path(model, unit_id, sample, a).exists())
            return rec
    return None


def build():
    units, prem_unit = load_units()
    su = {u["unit_id"] for u in sc_same_units(units)}
    fam = {m: (pid, f) for pid, m, f in PEERS}
    arms = [("peer", m, 0) for _, m, _ in PEERS] + [("sc_cheap", SC_CHEAP[1], k) for k in range(5)] + \
           [("sc_same", SC_SAME[1], k) for k in range(5)]
    peer_rows, sc_rows, stats = [], [], Counter()
    for u in units:
        for arm, m, k in arms:
            if arm == "sc_same" and u["unit_id"] not in su:
                continue
            rec = final_record(m, u["unit_id"], k)
            base = {"unit_id": u["unit_id"], "unit_type": u["type"], "model": m, "sample": k}
            if arm == "peer":
                base.update(peer=fam[m][0], family=fam[m][1])
            if rec is None:
                stats[(arm, m, "missing_call")] += 1
                row = {**base, "sentence_norm": None, "nl": None, "fol": None, "parse_ok": False,
                       "mapping_mode": "call_missing", "cost_usd": 0.0, "latency_s": None, "raw_hash": None}
                (peer_rows if arm == "peer" else sc_rows).append({**row, "arm": arm})
                continue
            parsed = parse_response(rec["text"], u["type"])
            mapped = map_unit(u, parsed)
            rh = hashlib.sha1(rec["text"].encode()).hexdigest()[:12]
            if not mapped:
                stats[(arm, m, "response_unparseable")] += 1
                row = {**base, "sentence_norm": None, "nl": None, "fol": None, "parse_ok": False,
                       "mapping_mode": "response_unparseable", "cost_usd": rec["cost_all_attempts"],
                       "latency_s": rec["latency_s"], "raw_hash": rh}
                (peer_rows if arm == "peer" else sc_rows).append({**row, "arm": arm})
                continue
            share = rec["cost_all_attempts"] / len(mapped)
            for key, n, f, mode in mapped:
                ok = safe_parse(f) is not None
                stats[(arm, m, mode)] += 1
                stats[(arm, m, "parse_ok" if ok else "fol_unparseable")] += 1
                row = {**base, "arm": arm, "sentence_norm": key, "nl": n, "fol": f, "parse_ok": ok, "mapping_mode": mode,
                       "cost_usd": share, "unit_cost_usd": rec["cost_all_attempts"], "latency_s": rec["latency_s"],
                       "raw_hash": rh, "attempts": rec["attempts"]}
                (peer_rows if arm == "peer" else sc_rows).append(row)
    with open(RES / "peer_outputs.jsonl", "w") as f:
        for r in peer_rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(RES / "sc_samples.jsonl", "w") as f:
        for r in sc_rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    st = {"|".join(map(str, k)): v for k, v in sorted(stats.items())}
    (RES / "peer_build_stats.json").write_text(json.dumps(st, indent=1))
    logger.info(f"built {len(peer_rows)} peer rows, {len(sc_rows)} SC rows")
    for k, v in sorted(stats.items()):
        logger.info(f"  {k}: {v}")


def estimate():
    units, _ = load_units()
    shots = malls_shots()
    L = Ledger()
    # ~4 chars / token for the prompt; output tokens per the plan (0.7k story units, 0.08k single sentence)
    tin = {u["unit_id"]: len(unit_prompt(u, shots)) / 3.2 for u in units}
    tout = {u["unit_id"]: (700 if u["type"] != "U_M" else 80) for u in units}

    def cost(model, us, k=1):
        pi, po = L.prices[model]
        return k * sum(tin[u["unit_id"]] * pi + tout[u["unit_id"]] * po for u in us)
    est = {m: cost(m, units) for _, m, _ in PEERS}
    est_sc_cheap = cost(SC_CHEAP[1], units, 5)
    est_sc_same = cost(SC_SAME[1], sc_same_units(units), 5)
    out = {"n_units": Counter(u["type"] for u in units), "peers": est, "peers_total": sum(est.values()),
           "sc_cheap": est_sc_cheap, "sc_same": est_sc_same,
           "grand_total": sum(est.values()) + est_sc_cheap + est_sc_same, "abort_if_peers_over": 3.0,
           "mean_prompt_tokens": {t: sum(tin[u["unit_id"]] for u in units if u["type"] == t) / max(1, sum(1 for u in units if u["type"] == t))
                                  for t in ("U_F", "U_P", "U_M")}}
    (RES / "cost_estimate.json").write_text(json.dumps(out, indent=1, default=dict))
    logger.info(json.dumps(out, indent=1, default=dict))
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["call", "build", "estimate", "shots"])
    ap.add_argument("--arm", default="peers")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    if a.cmd == "call":
        if a.arm == "peers" and not a.dry_run:
            e = estimate()
            if e["peers_total"] > 3.0:
                raise SystemExit(f"ABORT: peer sweep estimate ${e['peers_total']:.2f} > $3")
        asyncio.run(call_arm(a.arm, a.limit, a.dry_run))
    elif a.cmd == "build":
        build()
    elif a.cmd == "estimate":
        estimate()
    else:
        print(json.dumps(malls_shots(), ensure_ascii=False, indent=1))
