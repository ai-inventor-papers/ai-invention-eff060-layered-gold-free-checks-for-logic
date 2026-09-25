#!/usr/bin/env python3
"""LABELLED SECONDARY BAR (fallback 6): the iteration-1 exp D LOCAL judge, Qwen/Qwen3-8B, greedy, rubric B + USER_JSON
(exp D prereg_local.json; its screen track-L AUROC was .757 disguised), run on dataset E because the shared OpenRouter
key hit its $50/day limit at ~18:00 UTC before the pre-registered flash-lite judge could run. It NEVER replaces the
flash-lite bar: rows are written to results/E_judge_local.jsonl and reported as judge_local_qwen8b_{disg,orig}.
Reads only data/E_blind.jsonl, data/api_priority.json (row order) and results/E_disguise_map.jsonl. Resumable (cache)."""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from loguru import logger

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from vendor_d import judges as J  # noqa: E402
from vendor_d.local_llm import LocalLM  # noqa: E402
from vendor_e.fol import parse as e_parse  # noqa: E402

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(ROOT / "logs" / "local_judge_E.log", rotation="30 MB", level="DEBUG")


def jl(p):
    return [json.loads(l) for l in Path(p).read_text().splitlines() if l.strip()] if Path(p).exists() else []


def parseable(s):
    try:
        e_parse(s)
        return bool(s and s.strip())
    except (ValueError, IndexError, RecursionError, TypeError):
        return False


@logger.catch(reraise=True)
def main():
    import torch
    torch.cuda.set_per_process_memory_fraction(0.9)
    rows = {r["row_key"]: r for r in jl(ROOT / "data" / "E_blind.jsonl")}
    order = json.loads((ROOT / "data" / "api_priority.json").read_text())
    dmap = {r["row_key"]: r for r in jl(ROOT / "results" / "E_disguise_map.jsonl")}
    n_first = order["n_analysable_first"]
    keys = [k for k in order["order"] if rows[k]["system_class"] != "symbolic_eventsem" and parseable(rows[k]["candidate_fol"])]
    first = [k for k in keys if order["order"].index(k) < n_first]
    rest = [k for k in keys if k not in set(first)]
    outp = ROOT / "results" / "E_judge_local.jsonl"
    have = {(r["row_key"], r["cond"]) for r in jl(outp)}
    lm = LocalLM("Qwen/Qwen3-8B")
    batches = [(first, "disg"), (first, "orig"), (rest, "disg"), (rest, "orig")]
    for ks, cond in batches:
        for s in range(0, len(ks), 512):
            part = [k for k in ks[s:s + 512] if (k, cond) not in have]
            units = []
            for k in part:
                if cond == "disg":
                    d = dmap.get(k)
                    if not d or not d.get("text_d") or not d.get("fol_d"):
                        continue
                    units.append((k, d["text_d"], d["fol_d"]))
                else:
                    units.append((k, rows[k]["text"], rows[k]["candidate_fol"]))
            if not units:
                continue
            msgs = [[{"role": "system", "content": J.RUBRIC_B},
                     {"role": "user", "content": J.USER_JSON.format(text=t, fol=f)}] for _, t, f in units]
            t0 = time.time()
            gen = lm.generate(msgs, max_new_tokens=150, bs=48, tag=f"E_{cond}")
            with outp.open("a") as fh:
                for (k, _, _), g in zip(units, gen):
                    o = J.parse_judge_json(g["text"])
                    fh.write(json.dumps({"row_key": k, "cond": cond, "p": o["p"] if o else None,
                                         "type": o.get("type") if o else None, "fail": None if o else "json_parse",
                                         "seconds": g["seconds"]}) + "\n")
            logger.info(f"local judge {cond} {s}+{len(units)} in {time.time() - t0:.0f}s")
    (ROOT / "logs" / "local_judge_done.flag").write_text("done\n")


if __name__ == "__main__":
    main()
