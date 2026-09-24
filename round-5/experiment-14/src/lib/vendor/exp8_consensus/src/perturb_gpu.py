#!/usr/bin/env python3
"""PART B label-free GPU metrics on the PERTURB suite (4,234 mutants + 868 controls + 300 unmutated bases), with exp 6's
local code VERBATIM (vendor_e6/src): local Qwen3-8B JSON judge (exp D local rubric + user_json; orig and disguised),
local Llama-3.1-8B P(YES) judge (orig and disguised), local Qwen3-8B verbaliser (VERBALISE prompt, greedy) followed by
DeBERTa NLI both ways + mpnet cosine (round-trip). Disguise = dataset 3's per-sentence bijection (metadata_disguised_*).

usage: perturb_gpu.py [--limit N] [--which judges_disg,verb,nli,judges_orig] [--quant nf4]
Units = PERTURB rows (PT:) + unmutated bases (PB:) + E calibration rows (EC:, data/E_calib_units.jsonl: 864 R_AB LLM
CORRECT + 400 ERROR rows) so that PRIMARY thresholds use the same (nf4) quantisation as the PERTURB scores.
DEVIATION D-GPU16: the GPU of this machine has 16 GB (the run started on a 21 GB card), so both 8B models run
bitsandbytes nf4 (4-bit, bf16 compute); exp 6's E scores were bf16. Output names carry the suffix _nf4.
Outputs: results/perturb_scores/{judge_local_qwen8b_nf4,judge_local_llama8b_nf4,rt_verbal_local_nf4,rt_nli_local_nf4}.jsonl
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

from loguru import logger

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "vendor_e6"))  # `src.*` = exp 6's package (vendored)
os.environ.setdefault("NLTK_DATA", str(ROOT / "data" / "nltk_data"))
OUT = ROOT / "results" / "perturb_scores"
OUT.mkdir(parents=True, exist_ok=True)
EXPD = Path("/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_4")
LOCAL_Q8 = "Qwen/Qwen3-8B"
LOCAL_L8 = "meta-llama/Llama-3.1-8B-Instruct"

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(ROOT / "logs" / "perturb_gpu.log", rotation="30 MB", level="DEBUG")


def units(limit: int | None = None) -> list[dict]:
    """Every PERTURB row + one BASE row per base: key, text, fol, text_d, fol_d."""
    rows = [json.loads(l) for l in (ROOT / "data" / "perturb_rows.jsonl").read_text().splitlines() if l.strip()]
    U, seen = [], set()
    for r in rows:
        U.append({"key": "PT:" + r["item_id"], "text": r["text"], "fol": r["candidate_fol"], "text_d": r["disguised_text"],
                  "fol_d": r["disguised_fol"]})
        if r["base_item_id"] not in seen:
            seen.add(r["base_item_id"])
            U.append({"key": "PB:" + r["base_item_id"], "text": r["text"], "fol": r["reference_fol"],
                      "text_d": r["disguised_text"], "fol_d": r["disguised_reference_fol"]})
    cal = [json.loads(l) for l in (ROOT / "data" / "E_calib_units.jsonl").read_text().splitlines() if l.strip()]
    U += [{"key": c["key"], "text": c["text"], "fol": c["fol"], "text_d": c["text_d"], "fol_d": c["fol_d"]} for c in cal]
    if limit:  # small staged runs: take a spread over PERTURB and calibration units
        return U[:limit // 2] + U[-(limit - limit // 2):]
    return U


def done_keys(name: str) -> set:
    p = OUT / f"{name}.jsonl"
    if not p.exists():
        return set()
    return {json.loads(l)["key"] for l in p.read_text().splitlines() if l.strip()}


def append(name: str, rows: list[dict]):
    with (OUT / f"{name}.jsonl").open("a") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def _dedup(pairs):
    uq, m = {}, {}
    for k, t, f in pairs:
        dk = json.dumps([t, f], ensure_ascii=False)
        uq.setdefault(dk, (k, t, f))
        m[k] = uq[dk][0]
    return list(uq.values()), m


def stage_judges(U: list[dict], conds=("disg",), quant=None):
    from src import judges as J
    from src.common import disable_triton_overrides
    from src.local_llm import LocalLM
    disable_triton_overrides()
    pl = json.loads((EXPD / "prereg_local.json").read_text())
    rub, ut = pl["prompts"]["rubric"], pl["prompts"]["user_json"]
    lm, cur = None, None
    for w in [f"{m}_{c}" for c in conds for m in ("qwen8b", "llama8b")]:
        name, cond = w.rsplit("_", 1)
        fname = f"judge_local_{name}" + (f"_{quant}" if quant else "")
        dk = done_keys(fname)
        pairs = [(f"{u['key']}|{cond}", u["text"] if cond == "orig" else u["text_d"], u["fol"] if cond == "orig" else u["fol_d"])
                 for u in U if f"{u['key']}|{cond}" not in dk]
        if not pairs:
            continue
        model = LOCAL_Q8 if name == "qwen8b" else LOCAL_L8
        if cur != model:
            if lm is not None:
                lm.unload()
            lm, cur = LocalLM(model, quant=quant), model
        uq, m = _dedup(pairs)
        t0 = time.time()
        if name == "qwen8b":
            msgs = [[{"role": "system", "content": rub}, {"role": "user", "content": ut.format(text=t, fol=f or "(empty)")}] for _, t, f in uq]
            gen = lm.generate(msgs, max_new_tokens=150, tag=f"perturb_{w}", bs=96)
            outs, retry = [], []
            for i, g in enumerate(gen):
                o = J.parse_judge_json(g["text"])
                outs.append({**(o or {"p": None}), "fail": None if o else "json_parse", "seconds": g["seconds"]})
                if o is None:
                    retry.append(i)
            if retry:
                m2 = [msgs[i] + [{"role": "assistant", "content": gen[i]["text"]}, {"role": "user", "content": "Return ONLY the JSON object."}]
                      for i in retry]
                g2 = lm.generate(m2, max_new_tokens=150, tag=f"perturb_{w}_retry", bs=96)
                for i, g in zip(retry, g2):
                    o = J.parse_judge_json(g["text"])
                    if o:
                        outs[i] = {**o, "fail": None, "seconds": outs[i]["seconds"] + g["seconds"], "retried": True}
        else:
            msgs = [[{"role": "system", "content": rub},
                     {"role": "user", "content": J.USER_YESNO.format(text=t, fol=f or "(empty)")}] for _, t, f in uq]
            outs = [{"p": o["p"], "mass_yes_no": o.get("mass_yes_no"), "seconds": o["seconds"],
                     "fail": None if o["p"] is not None else "no_mass"} for o in lm.p_yes(msgs, tag=f"perturb_{w}", bs=64)]
        res = {k: o for (k, _, _), o in zip(uq, outs)}
        append(fname, [{"key": k, **res[m[k]], "dedup_key": m[k]} for k, _, _ in pairs])
        logger.info(f"{w}: {len(pairs)} rows ({len(uq)} unique) in {time.time() - t0:.0f}s; "
                    f"fails {sum(res[m[k]].get('p') is None for k, _, _ in pairs)}")
    if lm is not None:
        lm.unload()


def stage_verb(U: list[dict], quant=None):
    from src import judges as J
    from src.common import disable_triton_overrides, sha1
    from src.local_llm import LocalLM
    disable_triton_overrides()
    sfx = f"_{quant}" if quant else ""
    dk = done_keys("rt_verbal_local" + sfx)
    todo = [u for u in U if u["key"] not in dk]
    if not todo:
        return
    uq = {}
    for u in todo:
        uq.setdefault(sha1(u["fol"]), u["fol"])
    keys = list(uq)
    lm = LocalLM(LOCAL_Q8, quant=quant)
    t0 = time.time()
    gen = lm.generate([[{"role": "user", "content": J.VERBALISE.format(fol=uq[k])}] for k in keys], 120, tag="perturb_verbalise", bs=128)
    lm.unload()
    res = dict(zip(keys, gen))
    rows = []
    for u in todo:
        g = res[sha1(u["fol"])]
        v, leak = J.clean_verbalisation(g["text"])
        rows.append({"key": u["key"], "verbalisation": v or None, "leak": leak, "seconds": g["seconds"]})
    append("rt_verbal_local" + sfx, rows)
    logger.info(f"verbaliser: {len(rows)} rows ({len(keys)} unique) in {time.time() - t0:.0f}s")


def stage_nli(U: list[dict], quant=None):
    from src.common import disable_triton_overrides
    from src.roundtrip import NLI_ALT, NLI_MAIN, embed_cos, nli_probs
    disable_triton_overrides()
    V = {}
    sfx = f"_{quant}" if quant else ""
    for l in (OUT / f"rt_verbal_local{sfx}.jsonl").read_text().splitlines():
        r = json.loads(l)
        V[r["key"]] = r
    text = {u["key"]: u["text"] for u in U}
    dk = done_keys("rt_nli_local" + sfx)
    keys = [k for k in text if k in V and V[k].get("verbalisation") and k not in dk]
    if not keys:
        return
    pk = {k: (text[k], V[k]["verbalisation"]) for k in keys}
    uq = sorted(set(pk.values()))
    res = {p: {} for p in uq}
    t0 = time.time()
    for name, model in (("", NLI_MAIN), ("_alt", NLI_ALT)):
        f, _ = nli_probs([(t, v) for t, v in uq], model)
        b, _ = nli_probs([(v, t) for t, v in uq], model)
        for p_, x, y in zip(uq, f, b):
            res[p_][f"rt_nli_fwd{name}_local"] = x["entail"]
            res[p_][f"rt_nli_bwd{name}_local"] = y["entail"]
            res[p_][f"rt_nli_min{name}_local"] = min(x["entail"], y["entail"])
            res[p_][f"rt_nli_contra{name}_local"] = max(x["contra"], y["contra"])
    cos, _ = embed_cos([(t, v) for t, v in uq])
    for p_, c in zip(uq, cos):
        res[p_]["rt_embed_cos_local"] = c
    append("rt_nli_local" + sfx, [{"key": k, **res[pk[k]]} for k in keys])
    logger.info(f"NLI: {len(keys)} rows / {len(uq)} unique pairs in {time.time() - t0:.0f}s")


@logger.catch(reraise=True)
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--which", default="judges_disg,verb,nli,judges_orig")
    ap.add_argument("--quant", default="nf4")
    a = ap.parse_args()
    import torch
    free, total = torch.cuda.mem_get_info(0)
    logger.info(f"GPU free {free / 1e9:.1f} / {total / 1e9:.1f} GB")
    torch.cuda.set_per_process_memory_fraction(0.92)
    U = units(a.limit or None)
    logger.info(f"PERTURB GPU units: {len(U)}")
    w = a.which.split(",")
    q = a.quant or None
    if "judges_disg" in w:
        stage_judges(U, ("disg",), q)
    if "verb" in w:
        stage_verb(U, q)
    if "nli" in w:
        stage_nli(U, q)
    if "judges_orig" in w:
        stage_judges(U, ("orig",), q)
    logger.info("done")


if __name__ == "__main__":
    main()
