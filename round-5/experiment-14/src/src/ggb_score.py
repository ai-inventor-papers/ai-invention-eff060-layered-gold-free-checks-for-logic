#!/usr/bin/env python3
"""GG_B (SECONDARY): gloss the non-identity entries of the freelab maps (results/ggb_search.jsonl) with the PRIMARY checker
and prompt (gloss_gg_v2; item A = the candidate symbol use, B = its image under the map, e.g. 'Bird(x) ∧ Flies(x)',
'¬Tall(x)', 'Has(x, wings)'), then score c_ggb(x) = 1 - share of P(x) agreeing, where a pair agrees iff PRIMARY GG agrees
OR some GG_B map has every non-identity entry YES. Reports AUROC / e / d / T9 e beside V0, PRIMARY GG and c_exact.
Writes results/ggb_verdicts.json, results/scores_ggb_E.jsonl, results/ggb_dev.json, tables/ggb_*.csv."""
from __future__ import annotations

import asyncio
import hashlib
import json
import sys
from collections import Counter, defaultdict

import numpy as np
import pandas as pd

from common import FREEZE, MATRIX, RES, ROOT, SEED, TAB, B, jdump, jl, sha1, setup_logger
from gloss_client import HARD_CAP, Client, ckey, run_calls, spent
from labels import T9, frame
from stats import SentBoot, WAuc, WStratAuc, auroc, boot_ci, strat_auroc

sys.path.insert(0, str(FREEZE))
import consensus_variants as CV  # noqa: E402
import gg  # noqa: E402
import gg_score as GS  # noqa: E402
from gg_gloss import sentence_texts  # noqa: E402

logger = setup_logger("ggb_score")
PROMPT = json.loads((RES / "prompt_gg_v2.json").read_text())
PSHA = hashlib.sha256(json.dumps(PROMPT, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
MODEL = json.loads((ROOT / "prereg_gg.json").read_text())["checker"]["model"]


def item_of(e: list) -> tuple:
    kind, a, b = e
    return ("const" if kind == "const" else "pred", a, b, a, b)


def key_of(e: list) -> list:
    return ["ggb"] + list(e)


async def gloss(SB: dict, texts: dict) -> dict:
    items = defaultdict(dict)
    for r in SB.values():
        if r["status"] != "MAPPED" or any(not m["entries"] for m in r["maps"]):
            continue
        for m in r["maps"]:
            for e in m["entries"]:
                items[r["sid"]].setdefault(json.dumps(key_of(e)), e)
    calls = []
    for sid in sorted(items, key=lambda s: sha1("GGB|" + s)):
        its = sorted(items[sid].items(), key=lambda kv: sha1(kv[0]))
        for i in range(0, len(its), 12):
            ch = its[i:i + 12]
            calls.append({"sid": sid, "messages": gg.build_messages(PROMPT, texts[sid], [item_of(e) for _, e in ch]),
                          "keys": [json.loads(k) for k, _ in ch]})
    n_items = sum(len(v) for v in items.values())
    stop_at = HARD_CAP * 0.9
    c1 = Client(MODEL, "ggb_first50", stop_at=stop_at, logger=logger)
    v = await run_calls(c1, calls[:50], gg.parse_verdicts, PSHA)
    per = c1.stats["usd"] / max(1, c1.stats["calls"])
    proj, rem = per * max(0, len(calls) - 50), stop_at - spent()
    info = {"n_items": n_items, "n_calls": len(calls), "first50": c1.stats, "projection_rest": proj, "remaining": rem}
    logger.info(f"GG_B gloss: {n_items} items / {len(calls)} calls; first50 ${c1.stats['usd']:.4f}; projection ${proj:.4f}; remaining ${rem:.4f}")
    if proj <= rem:
        c2 = Client(MODEL, "ggb_rest", stop_at=stop_at, logger=logger)
        v.update(await run_calls(c2, calls[50:], gg.parse_verdicts, PSHA))
        info["rest"] = c2.stats
    else:
        info["rest"] = "NOT_RUN (F7 budget)"
    ver = {}
    for c in calls:
        for k in c["keys"]:
            ver[json.dumps([c["sid"]] + k)] = v.get(ckey(MODEL, PSHA, c["sid"], k), "MISSING")
    info["verdict_counts"] = dict(Counter(ver.values()))
    return ver, info


def decide_b(rec, sid, ver) -> tuple[bool, str]:
    if rec is None or rec["status"] != "MAPPED":
        return False, (rec or {}).get("status", "no_record")
    for m in rec["maps"]:
        if all(ver.get(json.dumps([sid] + key_of(e))) == "YES" for e in m["entries"]):
            return True, "gloss_yes" if m["entries"] else "identity_bridge"
    return False, "gloss_rejected"


@logger.catch(reraise=True)
def main():
    SB = {r["id"]: r for r in jl(RES / "ggb_search.jsonl")}
    texts = sentence_texts()
    ver, info = asyncio.run(gloss(SB, texts))
    jdump(ver, RES / "ggb_verdicts.json")
    S = GS.load_search()
    vp = json.loads((RES / "gg_verdicts.json").read_text())
    df = frame()
    searched = set(df[df.Z].sentence_id)
    out, why = [], Counter()
    for r in jl(MATRIX):
        sid = r["sentence_id"]
        if sid not in searched:
            continue
        ix = CV.build_index(r)
        for rk in ix["node_of"]:
            P = CV.peers_lofo(ix, rk)
            if len(P) < 2:
                continue
            c = ix["node_of"][rk]
            ag = agu = 0
            for p in P:
                pn = ix["node_of"][p]
                if pn == c or (ix["kind"].get((c, pn)) == "exact" and ix["eq"].get((c, pn)) is True):
                    ag += 1
                    agu += 1
                    continue
                i, j = min(c, pn), max(c, pn)
                a, *_ = GS.decide(S.get(f"E|{sid}|{i}|{j}"), sid, vp)
                if a:
                    ag += 1
                    agu += 1
                    continue
                rb = SB.get(f"E|{sid}|{i}|{j}")
                b_, w = decide_b(rb, sid, ver)
                ag += b_
                agu += bool(rb and rb["status"] == "MAPPED")
            out.append({"row_key": rk, "c_ggb": 1 - ag / len(P), "c_ggb_allyes": 1 - agu / len(P)})
        for i, j, eq, kind, _s in r["pairs"]:
            if kind == "exact":
                continue
            a, *_ = GS.decide(S.get(f"E|{sid}|{i}|{j}"), sid, vp)
            if a:
                why[("primary", eq is True)] += 1
                continue
            b_, w = decide_b(SB.get(f"E|{sid}|{i}|{j}"), sid, ver)
            why[(f"ggb:{w}", eq is True, kind)] += 1
    G = pd.DataFrame(out)
    df = df.merge(G, on="row_key", how="left")
    G2 = pd.DataFrame(jl(RES / "scores_gg_E.jsonl"))[["row_key", "c_gg"]]
    df = df.merge(G2, on="row_key", how="left")
    df.loc[df.sentence_id.isin(searched) & ~df.in_matrix, "c_ggb"] = 1.0
    with (RES / "scores_ggb_E.jsonl").open("w") as fh:
        for rec in df[df.sentence_id.isin(searched)][["row_key", "c_ggb", "c_ggb_allyes"]].to_dict("records"):
            fh.write(json.dumps({k: (None if v is None or (isinstance(v, float) and np.isnan(v)) else v) for k, v in rec.items()}) + "\n")
    P = df[df.Z].reset_index(drop=True)
    P.loc[P.c_ggb.isna() & ~P.in_matrix, ["c_ggb", "c_ggb_allyes"]] = 1.0
    gloss_ran = any(v in ("YES", "NO", "NO_UNPARSEABLE") for v in ver.values())
    assert P.c_ggb.notna().all()
    y, st = P.y.values.astype(int), P.stratum.values
    Wf = SentBoot(P.sentence_id.values, b=B, seed=SEED).W()
    D = {"gloss": info, "pair_outcomes": {str(k): v for k, v in why.items()}, "auroc": {}, "ed": {}, "t9_e": {}}
    cells = {"ALL-strat": (None, "strat"), "pooled": (None, "pooled"), "LONG-strat": (("L25", "L20", "EXC"), "strat"),
             "L25": (("L25",), "pooled"), "CTRL": (("CTRL",), "pooled")}
    for cn, (strata, stat) in cells.items():
        m = np.ones(len(P), bool) if strata is None else np.isin(st, strata)
        ser = {}
        for s in ("c_ggb", "c_ggb_allyes", "c_gg", "c_exact", "V0_frozen"):
            v = P[s].astype(float).values[m]
            f = WStratAuc(y[m], v, st[m]) if stat == "strat" else WAuc(y[m], v)
            pt = strat_auroc(y[m], v, st[m]) if stat == "strat" else auroc(y[m], v)
            ser[s] = (pt, np.array([f(w) for w in Wf[:, m]]))
        D["auroc"][cn] = {s: {"auroc": pt, "ci": boot_ci(bs)} for s, (pt, bs) in ser.items()}
        for s in ("c_ggb", "c_ggb_allyes", "c_gg"):
            D["auroc"][cn][f"{s} - V0"] = {"delta": ser[s][0] - ser["V0_frozen"][0], "ci": boot_ci(ser[s][1] - ser["V0_frozen"][1])}
        D["auroc"][cn]["c_ggb - c_gg"] = {"delta": ser["c_ggb"][0] - ser["c_gg"][0], "ci": boot_ci(ser["c_ggb"][1] - ser["c_gg"][1])}
    fl = {s: P[s].astype(float).values > 0.5 for s in ("c_ggb", "c_ggb_allyes", "c_gg", "c_exact", "V0_frozen")}
    for cut, m in (("ALL", np.ones(len(P), bool)), ("LONG", P.long.values), ("L25", st == "L25"), ("words_T3", P.words_t.values == "T3")):
        D["ed"][cut] = {s: {"e": float((~fl[s][m & (y == 1)]).mean()), "d": float(fl[s][m & (y == 0)].mean())} for s in fl}
    for cl in T9:
        m = np.array([cl in x for x in P.t9])
        if m.sum():
            D["t9_e"][cl] = {"n": int(m.sum()), **{s: float((~fl[s][m]).mean()) for s in fl}}
    D["status"] = "SCORED" if gloss_ran else "UNTESTED(budget): the run-level OpenRouter budget was exhausted before the GG_B gloss (HTTP 403 aii_run_budget_exhausted); GG_B agreement is bracketed by c_gg (no bridged map accepted; c_ggb == c_gg as run) and c_ggb_allyes (every bridged map accepted)"
    D["g3_secondary"] = {"pass": bool(D["auroc"]["ALL-strat"]["c_ggb"]["auroc"] >= D["auroc"]["ALL-strat"]["V0_frozen"]["auroc"] - 0.01),
                         "note": "SECONDARY row: does not change the PRIMARY GG status in M1"}
    D["search"] = {"n_pairs": len(SB), "status": dict(Counter(r["status"].split(":")[0] for r in SB.values())),
                   "capped": sum(r["capped"] for r in SB.values()), "cpu_s": sum(r["secs"] or 0 for r in SB.values()), "n_killed_at_deadline": sum(bool(r.get("killed_at_wall_deadline")) for r in SB.values()),
                   "bridges_in_accepted_maps": dict(Counter(b for r in SB.values() if r["status"] == "MAPPED" for m in r["maps"][:1] for b in m["bridges"]))}
    D["spend_total_after"] = spent()
    D["bracket_note"] = ("agreement sets are nested (GG ⊆ GG_B ⊆ GG_B all-yes), so per row c_ggb_allyes <= c_ggb <= c_gg and, at c > 0.5, "
                         "GG_B's e lies in [e(c_gg), e(c_ggb_allyes)] and its d in [d(c_ggb_allyes), d(c_gg)]; AUROC is NOT guaranteed to lie between the brackets")
    jdump(D, RES / "ggb_dev.json")
    logger.info(f"GG_B status {D['status'][:40]}; allyes ALL-strat {D['auroc']['ALL-strat']['c_ggb_allyes']['auroc']:.4f} LONG {D['auroc']['LONG-strat']['c_ggb_allyes']['auroc']:.4f}")
    logger.info(f"GG_B ALL-strat {D['auroc']['ALL-strat']['c_ggb']['auroc']:.4f} vs V0 {D['auroc']['ALL-strat']['V0_frozen']['auroc']:.4f} "
                f"vs GG {D['auroc']['ALL-strat']['c_gg']['auroc']:.4f}; e/d ALL {json.dumps(D['ed']['ALL'])}")
    with open(TAB / "ggb_auroc.csv", "w") as fh:
        fh.write("# source: results/ggb_dev.json :: src/ggb_score.py main()\n")
        pd.DataFrame([{"cell": c, "score": s, **v} for c, d in D["auroc"].items() for s, v in d.items()]).to_csv(fh, index=False)


if __name__ == "__main__":
    main()
