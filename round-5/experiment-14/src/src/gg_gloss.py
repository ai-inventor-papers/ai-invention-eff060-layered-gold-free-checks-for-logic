#!/usr/bin/env python3
"""B5: gloss sweep. Union of non-identity symbol pairs over every kept equivalence map (E + PERTURB E-base search rows),
dedup per sentence by the symmetric pair key; calls of <= 12 pairs, one sentence per call, prompt gloss_gg_v2 (the
revision that passed the confirm gate), google/gemini-2.5-flash non-thinking. The first 50 calls give a cost estimate;
the rest runs only if the projection fits (cap $2.00 - 10% reserve). Writes results/gg_verdicts.json + results/gg_gloss_run.json."""
from __future__ import annotations

import asyncio
import hashlib
import json
import sys
import time
from collections import defaultdict

from common import DS_E, FREEZE, RES, ROOT, jdump, jl, sha1, setup_logger
from gloss_client import HARD_CAP, Client, ckey, run_calls, spent

sys.path.insert(0, str(FREEZE))
import gg  # noqa: E402

logger = setup_logger("gg_gloss")
PRE = json.loads((ROOT / "prereg_gg.json").read_text())
MODEL = PRE["checker"]["model"]
PROMPT = json.loads((RES / "prompt_gg_v2.json").read_text())
PSHA = hashlib.sha256(json.dumps(PROMPT, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def sentence_texts() -> dict:
    d = json.loads((DS_E / "full_data_out.json").read_text())
    g = [g for g in d["datasets"] if g["dataset"] == "heldout_sentences"][0]["examples"]
    return {e["metadata_sentence_id"]: json.loads(e["input"])["text"] for e in g}


def gloss_items() -> dict:
    items = defaultdict(dict)
    for r in jl(RES / "gg_search.jsonl"):
        if r["status"] != "MAPPED" or any(not m["nonidentity"] for m in r["maps"]):
            continue
        for m in r["maps"]:
            for it in m["nonidentity"]:
                items[r["sid"]].setdefault(json.dumps(list(gg.pair_key(it))), it)
    return items


def build_calls(items: dict, texts: dict) -> list[dict]:
    calls = []
    n = PROMPT["max_items_per_call"]
    for sid in sorted(items, key=lambda s: sha1("GLOSS|" + s)):
        its = sorted(items[sid].items(), key=lambda kv: sha1(kv[0]))
        for i in range(0, len(its), n):
            ch = its[i:i + n]
            msgs = gg.build_messages(PROMPT, texts[sid], [it for _, it in ch])
            calls.append({"sid": sid, "messages": msgs, "keys": [json.loads(k) for k, _ in ch]})
    return calls


async def run():
    texts = sentence_texts()
    items = gloss_items()
    calls = build_calls(items, texts)
    n_pairs = sum(len(v) for v in items.values())
    logger.info(f"{n_pairs} unique pairs in {len(items)} sentences -> {len(calls)} calls; spend so far ${spent():.4f}")
    stop_at = HARD_CAP * 0.9
    t0 = time.time()
    c1 = Client(MODEL, "gg_sweep_first50", stop_at=stop_at, logger=logger)
    v = await run_calls(c1, calls[:50], gg.parse_verdicts, PSHA)
    per_call = c1.stats["usd"] / max(1, c1.stats["calls"])
    proj = per_call * (len(calls) - 50)
    remaining = stop_at - spent()
    logger.info(f"first 50 calls: ${c1.stats['usd']:.4f} (${per_call:.6f}/call); projection for the rest ${proj:.4f}; remaining ${remaining:.4f}")
    run_info = {"n_pairs": n_pairs, "n_sentences": len(items), "n_calls": len(calls), "first50": c1.stats, "projection_rest_usd": proj,
                "remaining_before_rest": remaining, "prompt": PROMPT["version"], "prompt_sha256": PSHA, "model": MODEL}
    if proj <= remaining:
        c2 = Client(MODEL, "gg_sweep_rest", stop_at=stop_at, logger=logger)
        v.update(await run_calls(c2, calls[50:], gg.parse_verdicts, PSHA))
        run_info["rest"] = c2.stats
    else:
        run_info["rest"] = "NOT_RUN: projection exceeds remaining budget (F7)"
    verdicts = {}
    for c in calls:
        for k in c["keys"]:
            verdicts[json.dumps([c["sid"]] + k)] = v.get(ckey(MODEL, PSHA, c["sid"], k), "MISSING")
    from collections import Counter
    run_info["verdict_counts"] = dict(Counter(verdicts.values()))
    run_info["wall_s"] = time.time() - t0
    run_info["spend_total_after"] = spent()
    jdump(verdicts, RES / "gg_verdicts.json")
    jdump(run_info, RES / "gg_gloss_run.json")
    logger.info(f"gloss sweep done: {run_info['verdict_counts']} spend ${run_info['spend_total_after']:.4f}")


@logger.catch(reraise=True)
def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
