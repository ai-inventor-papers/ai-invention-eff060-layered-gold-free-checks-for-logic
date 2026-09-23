#!/usr/bin/env python3
"""STEP 2: candidate generation. ONE frozen prompt per variant, temperature 0, no re-sampling on parse failure.

Resumable: every response is appended to raw/generations.jsonl keyed by (sentence_id, slot, prompt_variant).
Usage: generate.py [--limit N] [--slots G1,G2] [--variants fewshot_v1,zeroshot_v1] [--cap 3.5] [--sentences file]
"""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import sys
from pathlib import Path

from loguru import logger

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "labeller"))
sys.setrecursionlimit(10000)
from normalise import normalise  # noqa: E402
from or_client import BudgetExceeded, Client  # noqa: E402
from fol import parse  # noqa: E402

GEN = ROOT / "raw" / "generations.jsonl"
MANIFEST = ROOT / "work" / "generation_manifest.json"
logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(ROOT / "logs" / "generate.log", rotation="30 MB", level="DEBUG")

# slot -> (model id, family, extra params). Resolved from work/models_snapshot.json (cheapest current
# non-thinking instruct endpoint per family; see generation_manifest.json).
SLOTS = {
    "G1": ("meta-llama/llama-3.1-8b-instruct", "meta", {}),
    "G1b": ("meta-llama/llama-3.3-70b-instruct", "meta", {}),
    "G2": ("qwen/qwen3-235b-a22b-2507", "qwen", {}),
    "G3": ("mistralai/mistral-small-3.2-24b-instruct", "mistral", {}),
    "G4": ("deepseek/deepseek-v3.2", "deepseek", {"reasoning": {"enabled": False}}),
    "G5": ("google/gemma-3-27b-it", "google-gemma", {}),
    "G6": ("microsoft/phi-4", "microsoft", {}),
    "G7": ("openai/gpt-4.1-mini", "openai", {}),
    "G8": ("google/gemini-2.5-flash", "google-gemini", {"reasoning": {"max_tokens": 0}}),
    "G9": ("cohere/command-r7b-12-2024", "cohere", {}),
    "F": ("openai/gpt-5.1", "openai-frontier", {"reasoning": {"effort": "low"}}),
}
MAX_TOK = {"F": 4000}
ZERO_SHOT_SLOTS = ("G1b", "G2")


def load_prompt(variant: str) -> tuple[dict, str]:
    txt = (ROOT / "prompts" / f"{variant}.txt").read_text()
    return json.loads(txt), hashlib.sha1(txt.encode()).hexdigest()


def done_keys() -> set:
    keys = set()
    if GEN.exists():
        for line in GEN.read_text().splitlines():
            if line.strip():
                r = json.loads(line)
                if r.get("raw_output") is not None or r.get("final_failure"):
                    keys.add((r["sentence_id"], r["slot"], r["prompt_variant"]))
    return keys


def frontier_subset(sents: list[dict]) -> set:
    q = {"L25": 60, "L20": 50, "EXC": 40, "CTRL": 50}
    out = set()
    for st, n in q.items():
        out |= {s["sentence_id"] for s in sorted([s for s in sents if s["source_stratum"] == st], key=lambda s: s["sentence_id"])[:n]}
    return out


def parse_status(f: str) -> tuple[bool, str]:
    if not f:
        return False, "empty"
    try:
        parse(f)
        return True, ""
    except Exception as ex:  # noqa: BLE001 - parser raises assorted errors on junk
        return False, f"{type(ex).__name__}: {str(ex)[:100]}"


async def one(client, slot, variant, sent, prompt, psha, lock):
    model, fam, extra = SLOTS[slot]
    params = {**extra, "temperature": 0.0, "max_tokens": MAX_TOK.get(slot, 600)}
    msgs = [{"role": "system", "content": prompt["system"]}] + prompt["exemplars"] + \
           [{"role": "user", "content": prompt["user_template"].format(sentence=sent["text"])}]
    r = await client.chat(model, msgs, tag=f"{slot}:{variant}:{sent['sentence_id']}", retries=2, **params)
    raw = r["text"]
    fol, applied = normalise(raw)
    ok, err = parse_status(fol)
    rec = {"sentence_id": sent["sentence_id"], "slot": slot, "system": f"{slot}:{model}", "model": model, "family": fam,
           "prompt_variant": variant, "prompt_sha1": psha, "raw_output": raw, "candidate_fol": fol,
           "normalisation_applied": applied, "parse_ok": ok, "parse_error": err, "provider": r["provider"],
           "model_returned": r["model_returned"], "finish_reason": r["finish_reason"], "cost_usd": r["cost_usd"],
           "usage": r["usage"], "api_error": r["error"], "final_failure": raw is None}
    async with lock:
        with open(GEN, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")


@logger.catch(reraise=True)
async def amain(a):
    sents = json.loads((ROOT / (a.sentences or "work/sentences.json")).read_text())
    sents = sorted(sents, key=lambda s: s["sentence_id"])
    fsub = frontier_subset(sents) if not a.sentences else {s["sentence_id"] for s in sents}
    if a.limit:
        # pilot: stratified first-N by sha1 so every stratum is represented
        per = {}
        for s in sents:
            per.setdefault(s["source_stratum"], []).append(s)
        k = max(1, a.limit // len(per))
        sents = [s for v in per.values() for s in v[:k]]
        fsub = {s["sentence_id"] for s in sents}
    slots = a.slots.split(",") if a.slots else list(SLOTS)
    variants = a.variants.split(",")
    dk = done_keys()
    jobs = []
    for variant in variants:
        prompt, psha = load_prompt(variant)
        for slot in slots:
            if variant.startswith("zeroshot") and slot not in ZERO_SHOT_SLOTS:
                continue
            if slot == "F" and variant.startswith("zeroshot"):
                continue
            for s in sents:
                if slot == "F" and s["sentence_id"] not in fsub:
                    continue
                if (s["sentence_id"], slot, variant) not in dk:
                    jobs.append((slot, variant, s, prompt, psha))
    logger.info(f"jobs: {len(jobs)}")
    lock = asyncio.Lock()
    async with Client("generation", phase_cap=a.cap, concurrency=a.concurrency, timeout=180) as client:
        tasks = [asyncio.create_task(one(client, *j, lock)) for j in jobs]
        n = 0
        for fut in asyncio.as_completed(tasks):
            try:
                await fut
            except BudgetExceeded as e:
                logger.error(str(e))
                for t in tasks:
                    t.cancel()
                break
            n += 1
            if n % 500 == 0:
                logger.info(f"{n}/{len(jobs)} phase ${client.spent_phase:.3f} total ${client.spent_total:.3f}")
        logger.info(f"done calls={client.n_calls} phase ${client.spent_phase:.3f} total ${client.spent_total:.3f}")


def write_manifest():
    d = json.loads((ROOT / "work" / "models_snapshot.json").read_text())["data"]
    by = {m["id"]: m for m in d}
    man = []
    for slot, (mid, fam, extra) in SLOTS.items():
        m = by.get(mid, {})
        man.append({"slot": slot, "id": mid, "family": fam, "params": extra, "max_tokens": MAX_TOK.get(slot, 600),
                    "prompt_price_per_tok": m.get("pricing", {}).get("prompt"),
                    "completion_price_per_tok": m.get("pricing", {}).get("completion"),
                    "context": m.get("context_length"), "in_catalog": bool(m),
                    "zero_shot_also": slot in ZERO_SHOT_SLOTS, "subset": "frontier-200" if slot == "F" else "all-600"})
    MANIFEST.write_text(json.dumps(man, indent=1))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--slots", default="")
    ap.add_argument("--variants", default="fewshot_v1,zeroshot_v1")
    ap.add_argument("--cap", type=float, default=3.5)
    ap.add_argument("--concurrency", type=int, default=16)
    ap.add_argument("--sentences", default="")
    a = ap.parse_args()
    write_manifest()
    asyncio.run(amain(a))
