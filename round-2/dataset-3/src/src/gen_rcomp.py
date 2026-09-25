#!/usr/bin/env python3
"""STEP 6: candidate generation over R_COMP sentences with dataset E's generate.py, UNCHANGED (src_e/generate.py).

  pilot    12 sha1-first main sentences, every slot (10 few-shot + zero-shot G1b/G2 + F), then measures $/call per slot
           and projects the full run; if the projection exceeds the $1.5 cap, slot F drops from 80 to 40 sentences
           (decision written to work/generation_plan.json).
  full     main batch: 10 few-shot slots + zero-shot G1b/G2 on all 250; F (gpt-5.1, effort low, 4000 tokens) on the
           sha1-first 80 (or 40).
  topup    the 100-sentence reserve with the full slot set (only when the pre-registered top-up rule fires).
generate.py appends to raw/generations.jsonl keyed (sentence_id, slot, prompt_variant) and retries key-limit failures.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import defaultdict

from common import RAW, ROOT, W, dump, load_jsonl, setup_logger

logger = setup_logger("gen_rcomp")
FEW = "G1,G1b,G2,G3,G4,G5,G6,G7,G8,G9"
PY = str(ROOT / ".venv" / "bin" / "python")
GEN = str(ROOT / "src_e" / "generate.py")


def sentences(batch: str) -> list[dict]:
    rs = json.loads((W / "rcomp_sentences.json").read_text())
    return sorted([{"sentence_id": r["sentence_id"], "text": r["text"], "source_stratum": "RCOMP"} for r in rs
                   if r["batch"] == batch], key=lambda r: r["sentence_id"])


def run(slots: str, variants: str, sfile: str, cap: float) -> int:
    cmd = [PY, GEN, "--slots", slots, "--variants", variants, "--sentences", sfile, "--cap", str(cap), "--concurrency", "16"]
    logger.info(" ".join(cmd))
    return subprocess.run(cmd, cwd=ROOT).returncode


def key_limited(ids: set) -> int:
    """Keys whose LATEST record is a key-limit failure (generate.py retries these on the next run)."""
    last = {}
    for r in load_jsonl(RAW / "generations.jsonl"):
        if r["sentence_id"] in ids:
            last[(r["sentence_id"], r["slot"], r["prompt_variant"])] = r
    return sum(1 for r in last.values() if r.get("final_failure") and "Key limit exceeded" in (r.get("api_error") or ""))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["pilot", "full", "topup"])
    ap.add_argument("--cap", type=float, default=1.5)
    a = ap.parse_args()
    main_s = sentences("main")
    if a.cmd == "pilot":
        p = main_s[:12]
        dump(W / "rcomp_gen_pilot.json", p)
        run(FEW + ",F", "fewshot_v1,zeroshot_v1", "work/rcomp_gen_pilot.json", a.cap)
        ids = {s["sentence_id"] for s in p}
        cost = defaultdict(list)
        for r in load_jsonl(RAW / "generations.jsonl"):
            if r["sentence_id"] in ids and r.get("raw_output") is not None:
                cost[(r["slot"], r["prompt_variant"])].append(r.get("cost_usd") or 0.0)
        per = {f"{k[0]}:{k[1]}": sum(v) / len(v) for k, v in cost.items() if v}
        n_main = len(main_s)
        proj_wo_f = sum(c * n_main for k, c in per.items() if not k.startswith("F:"))
        f_cost = per.get("F:fewshot_v1", 0.0)
        n_f = 80 if proj_wo_f + f_cost * 80 <= a.cap else 40
        plan = {"per_call_usd": per, "projection_without_F": proj_wo_f, "F_per_call": f_cost,
                "projection_total": proj_wo_f + f_cost * n_f, "F_sentences": n_f, "cap": a.cap,
                "pilot_key_limited_failures": key_limited(ids)}
        logger.info(json.dumps(plan))
        if plan["pilot_key_limited_failures"] or not per:
            logger.error("pilot hit the key limit: no generation plan written; re-run after the reset")
            raise SystemExit(3)
        dump(W / "generation_plan.json", plan)
    elif a.cmd == "full":
        plan = json.loads((W / "generation_plan.json").read_text())
        dump(W / "rcomp_gen_main.json", main_s)
        dump(W / "rcomp_gen_F.json", main_s[: plan["F_sentences"]])
        run(FEW, "fewshot_v1,zeroshot_v1", "work/rcomp_gen_main.json", a.cap)
        run("F", "fewshot_v1", "work/rcomp_gen_F.json", a.cap)
        n = key_limited({s["sentence_id"] for s in main_s})
        logger.info(f"key-limited failures pending retry: {n}")
        raise SystemExit(3 if n else 0)
    else:
        res = sentences("reserve")
        dump(W / "rcomp_gen_topup.json", res)
        run(FEW, "fewshot_v1,zeroshot_v1", "work/rcomp_gen_topup.json", a.cap)
        n = key_limited({s["sentence_id"] for s in res})
        raise SystemExit(3 if n else 0)


if __name__ == "__main__":
    sys.exit(main())
