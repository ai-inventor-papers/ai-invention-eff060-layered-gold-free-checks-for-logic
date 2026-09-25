#!/usr/bin/env python3
"""S3: SIG-condition candidate generation (thin wrapper over rcomp/src_e/generate.py, dataset E's generator).

Same 10 few-shot slots (G1, G1b, G2..G9), same params (temperature 0, max_tokens 600 unless --max-tokens), same
normalise() and parse_status(), same client (rcomp/src_e/or_client.py, patched for the artifact budget). The ONLY
difference from FREE: the final user message carries the signature block of src/sig_prompt.py.
Records go to rcomp/raw/generations_sig.jsonl (a SEPARATE file: dataset-3's label_rcomp never mixes conditions),
keyed (sentence_id, slot, prompt_variant='sig_v1'); key-limit / budget failures are retried on the next run.

usage: gen_sig.py pilot            sha1-first 20 main sentences x 10 slots -> results/sig_pilot_projection.json
       gen_sig.py full  [--limit N] remaining main sentences (N = sha1-first N only)
       gen_sig.py reserve          the 100-sentence reserve (pre-registered top-up; only if testability fails)
"""
from __future__ import annotations

import argparse
import asyncio
import json
import sys
import time
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RC = ROOT / "rcomp"
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(RC / "src_e"))
import generate as G  # noqa: E402  (dataset-E generator: SLOTS, normalise, parse_status; configures loguru)
from loguru import logger  # noqa: E402
from or_client import BudgetExceeded, Client  # noqa: E402

import sig_prompt as SP  # noqa: E402

logger.add(ROOT / "logs" / "gen_sig.log", rotation="30 MB", level="DEBUG")
OUT = RC / "raw" / "generations_sig.jsonl"
FEW = ["G1", "G1b", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9"]
VARIANT = "sig_v1"


def jl(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []


def done_keys() -> set:
    keys = set()
    for r in jl(OUT):
        if r.get("raw_output") is not None or (r.get("final_failure") and "Key limit" not in (r.get("api_error") or "")
                                               and "budget" not in (r.get("api_error") or "").lower()):
            keys.add((r["sentence_id"], r["slot"], r["prompt_variant"]))
    return keys


def sentences(batch: str) -> list[dict]:
    rs = json.loads((RC / "work" / "rcomp_sentences.json").read_text())
    return sorted([r for r in rs if r["batch"] == batch], key=lambda r: r["sentence_id"])


async def one(client, slot, sent, prompt, psha, lex, lock, max_tokens):
    model, fam, extra = G.SLOTS[slot]
    params = {**extra, "temperature": 0.0, "max_tokens": max_tokens}
    msgs = SP.sig_messages(sent, prompt, lex)
    r = await client.chat(model, msgs, tag=f"{slot}:{VARIANT}:{sent['sentence_id']}", retries=2, **params)
    raw = r["text"]
    fol, applied = G.normalise(raw)
    ok, err = G.parse_status(fol)
    rec = {"sentence_id": sent["sentence_id"], "slot": slot, "system": f"{slot}:{model}", "model": model, "family": fam,
           "prompt_variant": VARIANT, "prompt_sha1": psha, "raw_output": raw, "candidate_fol": fol,
           "normalisation_applied": applied, "parse_ok": ok, "parse_error": err, "provider": r["provider"],
           "model_returned": r["model_returned"], "finish_reason": r["finish_reason"], "cost_usd": r["cost_usd"],
           "usage": r["usage"], "api_error": r["error"], "final_failure": raw is None, "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    async with lock:
        with open(OUT, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return rec


async def run(sents: list[dict], cap: float, max_tokens: int, concurrency: int = 16) -> dict:
    prompt, psha, _ = SP.load_prompt()
    lex = SP.load_lexicon()
    dk = done_keys()
    jobs = [(slot, s) for s in sents for slot in FEW if (s["sentence_id"], slot, VARIANT) not in dk]
    logger.info(f"SIG jobs: {len(jobs)} ({len(sents)} sentences x {len(FEW)} slots, {len(dk)} done)")
    lock = asyncio.Lock()
    stopped = None
    async with Client("generation_sig", phase_cap=cap, concurrency=concurrency, timeout=180) as client:
        tasks = [asyncio.create_task(one(client, slot, s, prompt, psha, lex, lock, max_tokens)) for slot, s in jobs]
        n = 0
        for fut in asyncio.as_completed(tasks):
            try:
                await fut
            except BudgetExceeded as e:
                logger.error(f"budget stop: {e}")
                stopped = str(e)
                for t in tasks:
                    t.cancel()
                break
            n += 1
            if n % 250 == 0:
                logger.info(f"SIG {n}/{len(jobs)} phase ${client.spent_phase:.4f}")
        logger.info(f"SIG done: calls={client.n_calls} phase ${client.spent_phase:.4f} total(rcomp ledger) ${client.spent_total:.4f}")
    return {"stopped": stopped}


def pilot_projection(pilot_ids: set, n_total: int, max_tokens: int) -> dict:
    by_slot = defaultdict(list)
    parse = defaultdict(list)
    offsig = defaultdict(list)
    sents = {s["sentence_id"]: s for s in sentences("main")}
    import label_sig as LS
    for r in jl(OUT):
        if r["sentence_id"] in pilot_ids and r.get("raw_output") is not None:
            by_slot[r["slot"]].append(r.get("cost_usd") or 0.0)
            parse[r["slot"]].append(bool(r["parse_ok"]))
            if r["parse_ok"]:
                st = LS.signature_status(r["candidate_fol"], sents[r["sentence_id"]])[0]
                offsig[r["slot"]].append(st != "ON_SIGNATURE")
    per = {k: sum(v) / len(v) for k, v in by_slot.items()}
    proj = sum(per.values()) * n_total
    out = {"per_call_usd": per, "parse_rate": {k: sum(v) / len(v) for k, v in parse.items()},
           "off_signature_rate": {k: (sum(v) / len(v) if v else None) for k, v in offsig.items()},
           "projected_full_usd": proj, "n_sentences": n_total, "max_tokens": max_tokens,
           "warn_offsig_gt_40pct": [k for k, v in offsig.items() if v and sum(v) / len(v) > 0.4]}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["pilot", "full", "reserve"])
    ap.add_argument("--cap", type=float, default=1.5)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--max-tokens", type=int, default=600)
    a = ap.parse_args()
    main_s = sentences("main")
    if a.cmd == "pilot":
        p = main_s[:20]
        res = asyncio.run(run(p, a.cap, a.max_tokens))
        proj = pilot_projection({s["sentence_id"] for s in p}, len(main_s), a.max_tokens)
        proj["stopped"] = res["stopped"]
        (ROOT / "results" / "sig_pilot_projection.json").write_text(json.dumps(proj, indent=1))
        logger.info(json.dumps(proj))
    elif a.cmd == "full":
        sel = main_s[: a.limit] if a.limit else main_s
        res = asyncio.run(run(sel, a.cap, a.max_tokens))
        if res["stopped"]:
            raise SystemExit(3)
    else:
        res = asyncio.run(run(sentences("reserve"), a.cap, a.max_tokens))
        if res["stopped"]:
            raise SystemExit(3)


if __name__ == "__main__":
    main()
