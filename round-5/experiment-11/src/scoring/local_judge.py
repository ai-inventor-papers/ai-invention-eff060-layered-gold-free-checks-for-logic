#!/usr/bin/env python3
"""E2-A local judge: Qwen3-8B (bf16, greedy, thinking off) rubric-A JSON judge, the FROZEN T1 path
(frozen/t1/src/local_llm.LocalLM + method.py _local_json_judge logic verbatim; prompts from exp-4 prereg_local.json).
Views: disguised (primary for S4_E2) then original. Parseable rows only; deduplicated by (text, fol).
Output cache/judge_local_qwen8b.jsonl rows {key: row_key|cond, p (faithful prob), fail, seconds}.
Usage: /root/e2a_gpu/.venv/bin/python scoring/local_judge.py [--which qwen8b_disg,qwen8b_orig]
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import scoring.guard  # noqa: E402,F401
from scoring.common import CACHE, FROZEN, append_jsonl, candidates, jl, setup_log  # noqa: E402

import argparse  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import time  # noqa: E402

from loguru import logger  # noqa: E402

sys.path.insert(0, str(FROZEN / "t1"))
PREREG_LOCAL = FROZEN / "t1" / "prereg_local_expD.json"
MODEL = "Qwen/Qwen3-8B"


def sha1(s: str) -> str:
    return hashlib.sha1(s.encode()).hexdigest()


def _msgs_json(rub, ut, text, fol):
    return [{"role": "system", "content": rub},
            {"role": "user", "content": ut.format(text=text, fol=fol if (fol and fol.strip()) else "(empty)")}]


def _local_json_judge(lm, units_, rub, ut, tag, max_new_tokens=150, bs=64):
    """T1 method.py _local_json_judge verbatim (one 'Return ONLY the JSON object.' retry)."""
    from src import judges as J
    msgs = [_msgs_json(rub, ut, t, f) for _, t, f in units_]
    gen = lm.generate(msgs, max_new_tokens=max_new_tokens, tag=tag, bs=bs)
    outs, retry = [], []
    for i, g in enumerate(gen):
        o = J.parse_judge_json(g["text"])
        outs.append({**(o or {"p": None}), "fail": None if o else "json_parse", "seconds": g["seconds"], "raw": g["text"][:300]})
        if o is None:
            retry.append(i)
    if retry:
        m2 = [msgs[i] + [{"role": "assistant", "content": gen[i]["text"]}, {"role": "user", "content": "Return ONLY the JSON object."}]
              for i in retry]
        g2 = lm.generate(m2, max_new_tokens=max_new_tokens, tag=tag + "_retry", bs=bs)
        for i, g in zip(retry, g2):
            o = J.parse_judge_json(g["text"])
            if o:
                outs[i] = {**o, "fail": None, "seconds": outs[i]["seconds"] + g["seconds"], "raw": g["text"][:300], "retried": True}
    return outs


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--which", default="qwen8b_disg,qwen8b_orig")
    ap.add_argument("--bs", type=int, default=64)
    a = ap.parse_args()
    setup_log("local_judge")
    from src import local_llm as L
    L.CACHE_P = CACHE / "local_cache.jsonl"
    pl = json.loads(PREREG_LOCAL.read_text())
    rub, ut = pl["prompts"]["rubric"], pl["prompts"]["user_json"]
    cand = {r["row_key"]: r for r in candidates()}
    U = [u for u in jl(CACHE / "units_E2.jsonl") if u["parse_ok"]]
    U.sort(key=lambda u: sha1(u["key"]))
    lm = L.LocalLM(MODEL)
    outp = CACHE / "judge_local_qwen8b.jsonl"
    for w in a.which.split(","):
        cond = w.rsplit("_", 1)[1]
        done = {r["key"] for r in jl(outp) if r.get("p") is not None}
        pairs = []
        for u in U:
            c = cand[u["key"]]
            t, f = (c["text"], c["candidate_fol"]) if cond == "orig" else (u["text_d"], u["fol_d"])
            if t is None or f is None or f"{u['key']}|{cond}" in done:
                continue
            pairs.append((f"{u['key']}|{cond}", t, f))
        m, uq = {}, {}
        for k, t, f in pairs:
            uk = sha1(t + "||" + (f or ""))
            m[k] = uk
            uq.setdefault(uk, (t, f))
        uql = [(uk, t, f) for uk, (t, f) in uq.items()]
        t0 = time.time()
        outs = _local_json_judge(lm, uql, rub, ut, f"judge_local_{w}", bs=a.bs)
        res = {k: o for (k, _, _), o in zip(uql, outs)}
        rows = [{"key": k, **{kk: vv for kk, vv in res[m[k]].items() if kk != "raw"}, "dedup_key": m[k]} for k, _, _ in pairs]
        append_jsonl(outp, rows)
        logger.info(f"local {w}: {len(rows)} rows ({len(uql)} unique) in {time.time() - t0:.0f}s; "
                    f"failures {sum(r['p'] is None for r in rows)}")
    lm.unload()


if __name__ == "__main__":
    main()
