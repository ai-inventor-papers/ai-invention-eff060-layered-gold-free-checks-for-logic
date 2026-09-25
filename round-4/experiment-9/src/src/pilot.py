"""STEP D: 30-row CSC-OWN pilot -> per-model parse / JSON / alt_fol / listed-symbol usage / $ / seconds, and the cost
projection for every planned arm (unique (text, signature, model) keys x mean $ per call per model)."""
from __future__ import annotations

import asyncio
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from loguru import logger

sys.path.insert(0, str(Path(__file__).resolve().parent))
import arms as A  # noqa: E402
import csc  # noqa: E402
import csc_llm as llm  # noqa: E402

ROOT = A.ROOT
RES = ROOT / "results"


def symbol_usage(rec_fol: str | None, listed: set) -> float | None:
    s = csc.extract_signature(rec_fol) if rec_fol else None
    if not s:
        return None
    used = {(n, a) for n, a, _ in s}
    return len(used & listed) / len(used)


@logger.catch(reraise=True)
def run(n: int = 30) -> dict:
    frame = A.load_frame()
    labels = {r["row_key"]: r["y"] for r in A.jl(A.DATA / "labels_RAB.jsonl")}
    rows = A.stratified(frame, n, "PILOT")
    built = A.build_arms(rows, None, sizes={"OWN": None})
    jobs = A.dedupe(built["jobs"]["OWN"])
    res = asyncio.run(llm.run_jobs(jobs, concurrency=24, stop_at=1.0))
    recs = res["records"]
    per = defaultdict(lambda: defaultdict(list))
    for r in rows:
        own = built["arms"]["OWN"][r["row_key"]]
        listed = {(n, a) for n, a, _ in csc.extract_signature(r["candidate_fol"])}
        for s in own["slots"]:
            rec = recs.get(s["key"])
            if rec is None:
                continue
            m = s["model"]
            per[m]["parse"].append(csc.parse(rec["fol"]) is not None)
            per[m]["json"].append(rec["route"] in ("json", "json_fenced", "json_regex"))
            per[m]["alt"].append(rec["alt_fol"] is not None)
            u = symbol_usage(rec["fol"], listed)
            if u is not None:
                per[m]["usage"].append(u)
            per[m]["usd"].append(rec["usd"])
            per[m]["secs"].append(rec["secs"])
            per[m]["in_tok"].append(rec["in_tok"])
            per[m]["out_tok"].append(rec["out_tok"])
    stats = {m: {"n": len(v["parse"]), "parse_rate": float(np.mean(v["parse"])), "json_valid": float(np.mean(v["json"])),
                 "alt_nonnull": float(np.mean(v["alt"])), "listed_symbol_usage": float(np.mean(v["usage"])) if v["usage"] else None,
                 "usd_per_call": float(np.mean(v["usd"])), "secs_per_call": float(np.mean(v["secs"])),
                 "in_tok": float(np.mean(v["in_tok"])), "out_tok": float(np.mean(v["out_tok"]))} for m, v in per.items()}
    # quick label-joined sanity only on pilot rows is NOT done (label-blind until prereg); show a few examples instead
    examples = []
    for r in rows[:5]:
        own = built["arms"]["OWN"][r["row_key"]]
        examples.append({"text": r["text"], "cand": r["candidate_fol"], "sig": own["sig_items"],
                         "peers": [{"model": s["model"], "fol": (recs.get(s["key"]) or {}).get("fol"),
                                    "alt": (recs.get(s["key"]) or {}).get("alt_fol")} for s in own["slots"]]})
    # full projection
    full = A.build_arms(frame, labels)
    usd = {m: stats[m]["usd_per_call"] for m in stats}
    proj = {}
    for arm, js in full["jobs"].items():
        uj = A.dedupe(js)
        proj[arm] = {"unique_calls": len(uj), "usd": float(sum(usd.get(j["model"], max(usd.values())) for j in uj))}
    allj = A.dedupe([j for js in full["jobs"].values() for j in js])
    proj["ALL_dedup_across_arms"] = {"unique_calls": len(allj), "usd": float(sum(usd.get(j["model"], max(usd.values())) for j in allj))}
    out = {"n_rows": len(rows), "per_model": stats, "spent_total": res["spent"], "projection": proj,
           "selection": full["selection"] | {"RENAME": {k: v for k, v in full["selection"].get("RENAME", {}).items() if k != "rows"}},
           "examples": examples}
    (RES / "pilot.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    logger.info(json.dumps({k: out[k] for k in ("per_model", "projection", "spent_total")}, indent=1))
    return out


if __name__ == "__main__":
    logger.add(ROOT / "logs" / "pilot.log", rotation="30 MB", level="DEBUG")
    run()
