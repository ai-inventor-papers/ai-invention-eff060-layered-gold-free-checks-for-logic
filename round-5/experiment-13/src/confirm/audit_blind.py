#!/usr/bin/env python3
"""Blind two-family audit of the provisional R_COMP FREE labels (addendum prereg, fallback B; extends dataset-5 audit_ii).

Sample: 100 ERROR_CERT + 100 MAPPED (= UNRESOLVED_GLOSS_GATE_FAILED) rows from the untouched provisional disguised-view
population. Rows are round-robined over templates; within a template they are shuffled with random.Random(20260924).
Auditors: anthropic/claude-sonnet-5 and z-ai/glm-4.6 (fallback moonshotai/kimi-k2-0905). Both get dataset-5
resume_gloss.AUDIT_SYS / AUDIT_USER verbatim: sentence, template concept glosses, candidate formula; never a label or a
score. Every call goes through labeller gloss.Client (ledger, $3.6 hard stop). An audit never changes a label.
Writes results/audit_rows.jsonl (per call) and results/audit_report.json.
usage: audit_blind.py [--pilot N] [--report-only]
"""
from __future__ import annotations

import argparse
import asyncio
import json
import random
import re
import sys
from collections import Counter, defaultdict

from cc import LAB, RES, dump, jl, setup_logger, wilson

sys.path.insert(0, str(LAB / "src"))
logger = setup_logger("audit_blind")
AUDITORS = {"sonnet5": ("anthropic/claude-sonnet-5", 400, {"reasoning": {"enabled": False}}),  # D19: reasoning off (pilot: 2/6 empty at 400)
            "glm46": ("z-ai/glm-4.6", 3000, None)}
FALLBACK_2ND = ("moonshotai/kimi-k2-0905", 800, None)
OUT = RES / "audit_rows.jsonl"
N_PER = 100
FAITH = ("FAITHFUL", "FAITHFUL_DIFFERENT_DECOMPOSITION")


def sample() -> list[dict]:
    labs = {r["row_key"]: r for r in jl(RES / "rcomp_free_labels_final.jsonl")}
    sc = {r["row_key"]: r for r in jl(RES / "scores_rcomp_free.jsonl")}
    pop = [labs[k] for k, s in sc.items() if s["untouched"] and s["c_score_align"] is not None and s["judge_cheap_disg"] is not None
           and labs[k]["label"] in ("ERROR_CERT", "UNRESOLVED_GLOSS_GATE_FAILED")]
    rng = random.Random(20260924)
    pick = []
    for lab in ("ERROR_CERT", "UNRESOLVED_GLOSS_GATE_FAILED"):
        by = defaultdict(list)
        for r in sorted(pop, key=lambda r: r["row_key"]):
            if r["label"] == lab:
                by[r["template_id"]].append(r)
        for t in sorted(by):
            rng.shuffle(by[t])
        chosen, i, ts = [], 0, sorted(by)
        while len(chosen) < N_PER and any(by.values()):
            t = ts[i % len(ts)]
            if by[t]:
                chosen.append(by[t].pop())
            i += 1
        pick += chosen
    return pick


def parse(txt: str | None) -> dict:
    """JSON object; fallback (D19): a truncated object still carrying '"verdict": "<CODE>"'."""
    if not txt:
        return {}
    try:
        return json.loads(txt[txt.index("{"): txt.rindex("}") + 1])
    except ValueError:
        m = re.search(r'"verdict"\s*:\s*"(FAITHFUL_DIFFERENT_DECOMPOSITION|FAITHFUL|UNFAITHFUL|UNSURE)"', txt)
        return {"verdict": m.group(1), "reason": "(truncated JSON; verdict recovered by regex)"} if m else {}


async def run(rows: list[dict], auditors: dict) -> None:
    import gloss
    from resume_gloss import AUDIT_SYS, AUDIT_USER
    sents = json.loads((LAB / "work/sentences.json").read_text())
    have = {(r["row_key"], r["auditor"]) for r in jl(OUT) if r.get("verdict")}
    client = gloss.Client(phase="audit_blind_iter5", concurrency=8)
    lock = asyncio.Lock()

    async def one(r, name, model, max_tokens, extra):
        s = sents[r["sentence_id"]]
        concepts = "\n".join(f"- {u['gloss_pos']}" for u in s["units"].values())
        msgs = [{"role": "system", "content": AUDIT_SYS},
                {"role": "user", "content": AUDIT_USER.format(text=s["text"], concepts=concepts, fol=r["candidate_fol"])}]
        u = {}
        try:
            txt, _ = await client.chat(model, msgs, max_tokens, logger, extra=extra, usage_out=u)
        except (gloss.BudgetExceeded, gloss.QuotaError) as e:
            txt, u = None, {"error": str(e)[:100]}
        d = parse(txt)
        v = str(d.get("verdict") or "").strip().upper() or None
        rec = {"row_key": r["row_key"], "auditor": name, "model": model, "verdict": v, "reason": d.get("reason"),
               "raw": None if v else (txt or "")[:300], **{k: u.get(k) for k in ("usd", "prompt_tokens", "completion_tokens")}}
        async with lock:
            with OUT.open("a") as fh:
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    try:
        tasks = [one(r, n, *cfg) for r in rows for n, cfg in auditors.items() if (r["row_key"], n) not in have]
        logger.info(f"{len(tasks)} audit calls; spend so far ${client.total:.3f}")
        await asyncio.gather(*tasks)
        logger.info(f"done; spend ${client.total:.3f}")
    finally:
        await client.close()


def kappa(a: list, b: list) -> float | None:
    n = len(a)
    if not n:
        return None
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / (n * n)
    return round((po - pe) / (1 - pe), 4) if pe < 1 else None


def consensus_verdict(vk: dict, names: list[str]) -> str | None:
    """FAITHFUL if both auditors say FAITHFUL*, UNFAITHFUL if both say UNFAITHFUL, None otherwise (disagreement/UNSURE)."""
    if len(names) < 2 or not all(vk.get(n) for n in names[:2]):
        return None
    a, b = vk[names[0]], vk[names[1]]
    if a in FAITH and b in FAITH:
        return "FAITHFUL"
    if a == "UNFAITHFUL" and b == "UNFAITHFUL":
        return "UNFAITHFUL"
    return None


def report(rows: list[dict]) -> dict:
    lab = {r["row_key"]: r["label"] for r in rows}
    v = defaultdict(dict)
    for r in jl(OUT):
        if r.get("verdict"):
            v[r["row_key"]][r["auditor"]] = r["verdict"]
    names = sorted({n for d in v.values() for n in d})
    out = {"n_sampled": len(rows), "auditors": {n: AUDITORS.get(n, FALLBACK_2ND)[0] for n in names}, "by_auditor": {}}
    for n in names + ["consensus"]:
        blk = {}
        for L, nm in (("ERROR_CERT", "ERROR_CERT"), ("UNRESOLVED_GLOSS_GATE_FAILED", "MAPPED")):
            ks = [k for k in lab if lab[k] == L]
            if n == "consensus":
                vs = [consensus_verdict(v[k], names) for k in ks]
            else:
                vs = [v[k].get(n) for k in ks]
            got = [x for x in vs if x]
            unf = sum(x == "UNFAITHFUL" for x in got)
            fai = sum(x in FAITH for x in got)
            uns = sum(x == "UNSURE" for x in got)
            blk[nm] = {"n_labelled": len(ks), "n_verdict": len(got), "counts": dict(Counter(got)),
                       "unfaithful_share": round(unf / max(len(got), 1), 4), "unfaithful_ci": wilson(unf, len(got)),
                       "faithful_share": round(fai / max(len(got), 1), 4), "faithful_ci": wilson(fai, len(got)),
                       "unfaithful_share_excl_unsure": round(unf / max(unf + fai, 1), 4), "unfaithful_ci_excl_unsure": wilson(unf, unf + fai),
                       "faithful_share_excl_unsure": round(fai / max(unf + fai, 1), 4), "faithful_ci_excl_unsure": wilson(fai, unf + fai),
                       "n_unsure": uns}
        blk["ERROR_CERT_precision"] = blk["ERROR_CERT"]["unfaithful_share"]
        blk["MAPPED_faithful"] = blk["MAPPED"]["faithful_share"]
        blk["contamination_a_error_side"] = round(1 - blk["ERROR_CERT"]["unfaithful_share_excl_unsure"], 4)
        blk["contamination_b_mapped_side"] = round(1 - blk["MAPPED"]["faithful_share_excl_unsure"], 4)
        out["by_auditor"][n] = blk
    if len(names) >= 2:
        both = [k for k in v if all(v[k].get(n) for n in names[:2])]
        a = [v[k][names[0]] for k in both]
        b = [v[k][names[1]] for k in both]
        bin_ = lambda x: "F" if x in FAITH else ("U" if x == "UNFAITHFUL" else "S")  # noqa: E731
        out["auditor_agreement"] = {"n_both": len(both), "kappa_4way": kappa(a, b), "kappa_3way_F_U_S": kappa([bin_(x) for x in a], [bin_(x) for x in b]),
                                    "raw_agreement_3way": round(sum(bin_(x) == bin_(y) for x, y in zip(a, b)) / max(len(both), 1), 4)}
    out["per_row"] = [{"row_key": k, "label": lab[k], **v.get(k, {})} for k in lab]
    return out


@logger.catch(reraise=True)
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pilot", type=int, default=0)
    ap.add_argument("--report-only", action="store_true")
    ap.add_argument("--retry-missing", action="store_true", help="D19: one retry of rows without a verdict, larger max_tokens")
    a = ap.parse_args()
    rows = sample()
    logger.info(f"sample: {dict(Counter(r['label'] for r in rows))}; templates {dict(Counter(r['template_id'] for r in rows))}")
    if a.retry_missing:
        # regex recovery of already-returned truncated JSON (no call), then one retry with a larger output budget
        recs = jl(OUT)
        for r in recs:
            if not r.get("verdict") and r.get("raw"):
                d = parse(r["raw"])
                if d.get("verdict"):
                    r.update(verdict=d["verdict"], reason=d["reason"], recovered="regex")
        OUT.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in recs))
        big = {"sonnet5": ("anthropic/claude-sonnet-5", 1500, {"reasoning": {"enabled": False}}), "glm46": ("z-ai/glm-4.6", 8000, None)}
        asyncio.run(run(rows, big))
    elif not a.report_only:
        asyncio.run(run(rows[:a.pilot] + rows[N_PER:N_PER + a.pilot] if a.pilot else rows, AUDITORS))
    rep = report(rows)
    dump(RES / "audit_report.json", rep)
    logger.info(json.dumps({k: v for k, v in rep.items() if k != "per_row"}, default=str)[:2500])


if __name__ == "__main__":
    main()
