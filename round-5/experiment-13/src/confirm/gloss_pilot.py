#!/usr/bin/env python3
"""STEP 1a: gloss cost pilot. Rates the gate items of 3 half-A sentences with both checkers through the unchanged
labeller gloss.rate_pairs (verdicts are cached, so the gate reuses them), measures $ per call and per pair verdict from
the ledger, and projects the gate, FREE gloss, SIG e2e and audits. Writes results/cost_projection.json."""
from __future__ import annotations

import asyncio
import json
import sys
from collections import defaultdict

from cc import LAB, RES, dump, jl, setup_logger

sys.path.insert(0, str(LAB / "src"))
logger = setup_logger("gloss_pilot")


def calls_for(pairs_per_sentence: list[int], per_call: int = 12) -> int:
    return sum(-(-n // per_call) for n in pairs_per_sentence if n)


@logger.catch(reraise=True)
def main() -> None:
    import gloss
    from resume_gloss import pair_jobs
    from run_search import class_key
    items = json.loads((LAB / "results/gate_items.json").read_text())
    by = defaultdict(list)
    for i in items:
        if i["half"] == "A":
            by[i["sentence_id"]].append(i)
    sids = sorted(by)[:3]
    jobs = [{"sentence_id": s, "sentence": by[s][0]["sentence"], "pairs": [(i["candidate_atom"], i["proposed_meaning"]) for i in by[s]]}
            for s in sids]
    led0 = len(jl(LAB / "cost_ledger.jsonl"))
    usd0 = gloss.spent()

    async def go():
        c = gloss.Client(phase="gloss_pilot_gate_A")
        try:
            return await gloss.rate_pairs(c, jobs, version="gloss_v1", logger=logger)
        finally:
            await c.close()
    v = asyncio.run(go())
    new = jl(LAB / "cost_ledger.jsonl")[led0:]
    usd = gloss.spent() - usd0
    n_pairs = sum(len(j["pairs"]) for j in jobs)
    per_ck = defaultdict(lambda: [0, 0.0])
    for r in new:
        per_ck[r["model"]][0] += 1
        per_ck[r["model"]][1] += r["usd"]
    usd_per_call = {m: c[1] / max(c[0], 1) for m, c in per_ck.items()}
    nv = sum(x == "NO_VERDICT" for x in v.values())
    # projections: calls per checker
    gate_sizes = [len(by[s]) for s in sorted(by)]
    sents = json.loads((LAB / "work/sentences.json").read_text())
    search = jl(LAB / "results/map_search.jsonl")
    free_jobs = pair_jobs(search, sents)
    free_sizes = [len(j["pairs"]) for j in free_jobs]
    sig_rows = [r for r in jl(LAB / "results/sig_replay_rows.jsonl") if r["in_e2e_gloss_subsample_300"]]
    ssearch = {r["class_key"]: r for r in jl(LAB / "results/sig_replay_syn.jsonl")}
    srows = [ssearch[class_key(r["sentence_id"], r["renamed_fol"])] for r in sig_rows]
    sig_sizes = [len(j["pairs"]) for j in pair_jobs(srows, sents)]
    per_call_both = sum(usd_per_call.values())
    proj = {"gate_A": calls_for(gate_sizes) * per_call_both, "free_gloss": calls_for(free_sizes) * per_call_both,
            "sig_e2e": calls_for(sig_sizes) * per_call_both}
    # audits: Sonnet-5 ~ 700 in / 120 out tokens per row; GLM-4.6 ~ 700 in / 400 out (reasoning allowance)
    proj["audit_sonnet_140"] = 140 * (700 * 2e-6 + 150 * 1e-5)
    proj["audit_glm_140"] = 140 * (700 * 0.43e-6 + 600 * 1.75e-6)
    proj["mandatory_total"] = sum(proj.values())
    out = {"pilot_sentences": sids, "pilot_pairs": n_pairs, "pilot_calls": len(new), "pilot_usd": usd,
           "usd_per_call": usd_per_call, "no_verdict_pairs": nv, "n_pair_verdicts": len(v),
           "json_parse_ok_share": 1 - nv / max(len(v), 1),
           "n_free_pairs": sum(free_sizes), "n_free_sentences": len(free_jobs), "n_free_calls_per_checker": calls_for(free_sizes),
           "n_gate_A_calls_per_checker": calls_for(gate_sizes), "n_sig_e2e_pairs": sum(sig_sizes),
           "n_sig_e2e_calls_per_checker": calls_for(sig_sizes), "projection_usd": proj,
           "catalogue_estimate_free": gloss.estimate_cost(sum(free_sizes), gloss.live_prices()),
           "spent_before_projection": gloss.spent(),
           "proceed": bool(gloss.spent() + proj["mandatory_total"] <= 3.24)}
    dump(RES / "cost_projection.json", out)
    logger.info(json.dumps(out, default=str)[:1500])


if __name__ == "__main__":
    main()
