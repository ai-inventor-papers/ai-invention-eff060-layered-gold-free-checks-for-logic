"""LOCAL2: labelled SECONDARY anchoring arm with small local peers (NOT the pre-registered CSC peers).

Why it exists: the OpenRouter budget of this run was exhausted before any CSC peer call (deviation D-BUDGET), so the
pre-registered peers (deepseek-v3.2 / phi-4 / gpt-4.1-mini / qwen3-235b) could not be queried. The plan allows a
local-model arm only as a labelled secondary. It uses the SAME CSC prompt bytes (dataset-E few-shot + symbols block;
gemma has no system role, so its system text is prepended to the first user turn) at temperature 0 with two small
instruct models of two families, run on CPU through llama.cpp (Q4_K_M GGUF):
    qwen2.5-1.5b-instruct (qwen), gemma-2-2b-it (google).
(Llama-3.2-1B was tried in a 3-prompt smoke test and dropped before any scoring: 0/3 parseable outputs.)
Scope: 40 E bases drawn with seed 0 (no operator / label information used); every unique (text, signature) of their rows
(27 bases were completed before the CPU deadline; `--finalize` keeps only complete bases)
(base signature + every new signature). Output: data/peers_local2.jsonl, cache data/local_llm_cache.jsonl.
What it can answer: the anchoring MECHANISM (do peers copy listed symbols by role: GENUINE / SYNONYM / NONCE / DONOR /
FOREIGN?) and the within-sentence mutant-signature vs base-signature contrast. What it cannot: the pre-registered gates.
"""
from __future__ import annotations

import hashlib
import json
import random
import sys
import time
from pathlib import Path

from loguru import logger

SRC = Path(__file__).resolve().parent
ROOT = SRC.parent
sys.path.insert(0, str(SRC))
import csc_lib as L  # noqa: E402

DATA = ROOT / "data"
MODELS = {"local/qwen2.5-1.5b-instruct-q4km": ("qwen2.5-1.5b-instruct-q4_k_m.gguf", "qwen", True),
          "local/gemma-2-2b-it-q4km": ("gemma-2-2b-it-Q4_K_M.gguf", "google", False)}
# The GGUF weights (0.8-1.6 GB each) are NOT kept in the workspace (GitHub 100 MB limit): they are re-downloaded on
# demand from these public repos into models/ (git-ignored). The cached outputs in data/local_llm_cache.jsonl make every
# already-run call free, so --finalize and re-scoring never need the weights.
HF_REPO = {"qwen2.5-1.5b-instruct-q4_k_m.gguf": "Qwen/Qwen2.5-1.5B-Instruct-GGUF",
           "gemma-2-2b-it-Q4_K_M.gguf": "bartowski/gemma-2-2b-it-GGUF"}


def ensure_model(fname: str) -> Path:
    """Local path of a GGUF weight file; downloaded from its public HF repo if missing."""
    p = ROOT / "models" / fname
    if not p.exists():
        from huggingface_hub import hf_hub_download
        logger.info(f"downloading {HF_REPO[fname]}/{fname} -> models/")
        hf_hub_download(HF_REPO[fname], fname, local_dir=str(ROOT / "models"))
    return p
CACHE = DATA / "local_llm_cache.jsonl"
N_BASES = 40


def jl(p: Path) -> list[dict]:
    return [json.loads(x) for x in p.read_text().splitlines() if x.strip()] if p.exists() else []


def select_jobs() -> list[dict]:
    view = jl(DATA / "perturb_view.jsonl")
    bases = sorted({r["base_item_id"] for r in view if r["fold"] == "BASE" and not r["is_rcomp"]})
    keep = set(random.Random(0).sample(bases, N_BASES))
    jobs = {}
    for r in view:
        if r["base_item_id"] in keep:
            jobs[(r["text"], r["sig_key"])] = {"text": r["text"], "sig_key": r["sig_key"], "signature": r["signature"],
                                               "base_item_id": r["base_item_id"]}
    return sorted(jobs.values(), key=lambda j: (j["base_item_id"], j["sig_key"])), sorted(keep)


def msgs_for(model_key: str, text: str, sig) -> list[dict]:
    m = L.csc_prompt(text, sig)
    if not MODELS[model_key][2]:  # no system role
        m = [{"role": "user", "content": m[0]["content"] + "\n\n" + m[1]["content"]}] + m[2:]
    return m


def main(argv: list[str]) -> None:
    limit = int(argv[argv.index("--limit") + 1]) if "--limit" in argv else None
    finalize = "--finalize" in argv  # no generation: keep only bases whose every signature has every model's output
    jobs, bases = select_jobs()
    if limit:
        jobs = jobs[:limit]
    cache = {r["key"]: r for r in jl(CACHE)}
    logger.info(f"LOCAL2: {len(bases)} bases, {len(jobs)} signatures x {len(MODELS)} models; cached {len(cache)}")
    for mk, (fname, fam, _) in ({} if finalize else MODELS).items():
        from llama_cpp import Llama
        llm = None
        t0 = time.time()
        n_new = 0
        for i, j in enumerate(jobs):
            sig = [(n, int(a)) for n, a in j["signature"]]
            msgs = msgs_for(mk, j["text"], sig)
            k = hashlib.sha1((mk + "|" + json.dumps(msgs, ensure_ascii=False, sort_keys=True)).encode()).hexdigest()
            if k in cache:
                continue
            if llm is None:
                llm = Llama(str(ensure_model(fname)), n_ctx=4096, n_threads=4, verbose=False, seed=0)
                pass  # llama-cpp-python reuses the longest matching prompt prefix of the previous call (shared few-shot prefix)
            ts = time.time()
            try:
                r = llm.create_chat_completion(messages=msgs, temperature=0.0, max_tokens=300)
                content = r["choices"][0]["message"]["content"]
                usage = r.get("usage", {})
                status = "ok"
            except (ValueError, RuntimeError) as ex:
                content, usage, status = None, {}, f"ERROR:{type(ex).__name__}"
            rec = {"key": k, "model": mk, "text": j["text"], "sig_key": j["sig_key"], "content": content,
                   "status": status, "secs": round(time.time() - ts, 2), "usage": usage, "cost_usd": 0.0}
            cache[k] = rec
            with CACHE.open("a") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            n_new += 1
            if n_new % 25 == 0:
                el = time.time() - t0
                logger.info(f"{mk}: {i + 1}/{len(jobs)} ({el / n_new:.1f}s/call)")
        del llm
        logger.info(f"{mk} done in {time.time() - t0:.0f}s ({n_new} new)")
    def _key(mk, j):
        sig = [(n, int(a)) for n, a in j["signature"]]
        return hashlib.sha1((mk + "|" + json.dumps(msgs_for(mk, j["text"], sig), ensure_ascii=False, sort_keys=True)).encode()).hexdigest()
    complete = {b for b in bases if all(_key(mk, j) in cache for j in jobs if j["base_item_id"] == b for mk in MODELS)}
    if finalize:
        jobs = [j for j in jobs if j["base_item_id"] in complete]
        bases = sorted(complete)
        logger.info(f"finalize: {len(bases)} complete bases, {len(jobs)} signatures")
    out = []
    for j in jobs:
        sig = [(n, int(a)) for n, a in j["signature"]]
        peers = []
        for mk in MODELS:
            k = hashlib.sha1((mk + "|" + json.dumps(msgs_for(mk, j["text"], sig), ensure_ascii=False, sort_keys=True)).encode()).hexdigest()
            rec = cache.get(k, {})
            pr = L.parse_peer(rec.get("content"))
            peers.append({"model": mk, "family": MODELS[mk][1], "raw": rec.get("content"), **pr,
                          "parse_ok": L.parse(pr["fol"]) is not None, "status": rec.get("status"), "secs": rec.get("secs")})
        out.append({**j, "peers": peers})
    with (DATA / "peers_local2.jsonl").open("w") as f:
        for r in out:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    (DATA / "local2_bases.json").write_text(json.dumps(bases))
    logger.info(f"wrote {len(out)} signature records")


if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
    logger.add(ROOT / "logs" / "local_peers.log", rotation="30 MB", level="DEBUG")
    main(sys.argv)
