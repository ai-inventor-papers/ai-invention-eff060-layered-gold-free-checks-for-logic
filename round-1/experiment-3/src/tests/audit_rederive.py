#!/usr/bin/env python3
"""Independent re-derivation of the headline numbers from RAW files, through a different code path.

Reads: results/screen_items.json (labels), results/peer_outputs.jsonl + results/sc_samples.jsonl (raw mapped outputs),
results/units.json (sentence -> source unit), results/pairwise_eq.jsonl (raw z3 results), data/peer_raw/*.json (costs).
It does NOT read consensus.json / analysis_table.jsonl / summary.json, except to compare at the end.
AUROC = brute-force pairwise win counting (not rank-based); pools, eq_frac, medoids and SC shares are rebuilt here.
Placebo: the same statistics on permuted labels must collapse to AUROC ~0.5 / delta ~0.
"""
import glob
import json
import random
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from fol import parse  # noqa: E402  (only to decide parseability)

R = ROOT / "results"


def jl(p):
    return [json.loads(l) for l in open(p) if l.strip()]


def parses(s):
    if not s or not s.strip():
        return False
    try:
        parse(s)
        return True
    except Exception:  # any parser failure = unparseable
        return False


def auc_pairs(y, s):
    pos = [v for v, t in zip(s, y) if t == 1]
    neg = [v for v, t in zip(s, y) if t == 0]
    P, N = np.array(pos)[:, None], np.array(neg)[None, :]
    return float(((P > N).sum() + 0.5 * (P == N).sum()) / (len(pos) * len(neg)))


def main():
    items = json.load(open(R / "screen_items.json"))
    uj = json.load(open(R / "units.json"))
    EQ = {}
    for r in jl(R / "pairwise_eq.jsonl"):
        EQ[(r["a"], r["b"])] = r["eq"]

    def eq(a, b):
        a, b = a.strip(), b.strip()
        if a == b:
            return True
        return EQ.get((a, b) if a <= b else (b, a))

    # sentence -> source unit (conclusion: F:<concl_id>; premise: premise_unit map; MALLS: M:<id>)
    src = {}
    for it in sorted(items, key=lambda x: (x["track"] != "L", x["item_id"])):
        t = it["sentence_key"]
        if t in src:
            continue
        src[t] = (f"F:{it['concl_id']}" if it["kind"] == "conclusion" else
                  uj["premise_unit"].get(t) if it["kind"] == "premise" else f"M:{it['malls_id']}")
    unit_entry = {u["unit_id"]: u.get("logiclm_entry") for u in uj["units"]}
    peers = defaultdict(dict)
    for r in jl(R / "peer_outputs.jsonl"):
        if r.get("sentence_norm") is not None:
            peers[(r["unit_id"], r["sentence_norm"])].setdefault(r["peer"], r["fol"])
    sc = defaultdict(lambda: defaultdict(dict))
    sc_units = defaultdict(set)
    for r in jl(R / "sc_samples.jsonl"):
        if r["mapping_mode"] != "call_missing":
            sc_units[r["arm"]].add(r["unit_id"])
        if r.get("sentence_norm") is not None:
            sc[r["arm"]][(r["unit_id"], r["sentence_norm"])].setdefault(r["sample"], r["fol"])

    def ent_num(e):
        import re
        m = re.search(r"(\d+)$", e or "")
        return int(m.group(1)) if m else 10 ** 9
    members = {}
    by_t = defaultdict(list)
    for it in items:
        by_t[it["sentence_key"]].append(it)
    ORDER = ["P1", "P2", "P3", "P4", "P5", "P6", "gpt-3.5-turbo", "gpt-4", "text-davinci-003"]
    for t, its in by_t.items():
        u = src[t]
        m = {p: f for p, f in peers.get((u, t), {}).items()}
        for s in ORDER[6:]:
            c = sorted([x for x in its if x["track"] == "L" and x["system"] == s],
                       key=lambda x: (x.get("logiclm_entry") != unit_entry.get(u), ent_num(x.get("logiclm_entry")), x["item_id"]))
            if c:
                m[s] = c[0]["candidate_fol"]
        members[t] = {k: v.strip() for k, v in m.items() if parses(v)}

    rows = []
    for it in items:
        if it["track"] != "L" or it["label"] not in ("CORRECT", "ERROR"):
            continue
        t = it["sentence_key"]
        pool = {k: v for k, v in members[t].items() if k != it["system"]}
        c = it["candidate_fol"].strip()
        eqs = {k: eq(c, v) is True for k, v in pool.items()}
        cs = 1.0 if len(pool) < 2 else 1 - sum(eqs.values()) / len(pool)
        # medoid: most partners, then larger component (approximated by degree ties -> order), then fixed order
        ids = sorted(pool, key=ORDER.index)
        deg = {a: sum(eq(pool[a], pool[b]) is True for b in ids if b != a) for a in ids}
        # component sizes via BFS
        comp = {}
        for a in ids:
            if a in comp:
                continue
            q, seen = [a], {a}
            while q:
                x = q.pop()
                for b in ids:
                    if b not in seen and eq(pool[x], pool[b]) is True:
                        seen.add(b); q.append(b)
            for x in seen:
                comp[x] = len(seen)
        med = sorted(ids, key=lambda a: (-deg[a], -comp[a], ORDER.index(a)))[0] if ids else None
        flag = True if (med is None or len(pool) < 2) else not eqs[med]
        u = src[t]
        scs = None
        if u in sc_units["sc_cheap"]:
            smp = sc["sc_cheap"].get((u, t), {})
            scs = 1 - sum(1 for k in range(5) if smp.get(k) and parses(smp[k]) and eq(c, smp[k]) is True) / 5
        # alignability of candidate predicates to the reference, recomputed inline from the ASTs
        from repair_census import align as _align
        ce, re_ = parse(c), parse(it["reference_fol"])

        def _preds(e, acc):
            if e[0] == "atom":
                acc.add((e[1], len(e[2])))
            elif e[0] in ("all", "ex"):
                _preds(e[2], acc)
            elif e[0] == "not":
                _preds(e[1], acc)
            else:
                _preds(e[1], acc); _preds(e[2], acc)
            return acc
        pc_, pr_ = _preds(ce, set()), _preds(re_, set())
        pm = _align(ce, re_)[1]
        clean = all(p in pr_ or p in pm for p in pc_)
        rows.append({"y": int(it["label"] == "ERROR"), "c": cs, "sc": scs, "flag": flag, "sys": it["system"], "t": t, "clean": clean})

    y = [r["y"] for r in rows]
    c = [r["c"] for r in rows]
    out = {"n": len(rows), "n_err": sum(y), "auroc_c_score": round(auc_pairs(y, c), 4)}
    sub = [r for r in rows if r["sc"] is not None]
    ys, cs_, ss = [r["y"] for r in sub], [r["c"] for r in sub], [r["sc"] for r in sub]
    out.update(n_sc=len(sub), auroc_c_on_sc_subset=round(auc_pairs(ys, cs_), 4), auroc_sc5_cheap=round(auc_pairs(ys, ss), 4),
               delta_c_minus_sc=round(auc_pairs(ys, cs_) - auc_pairs(ys, ss), 4))
    vc = [r for r in rows if r["clean"]]
    out.update(n_vocab_clean=len(vc), n_err_vocab_clean=sum(r["y"] for r in vc),
               auroc_c_vocab_clean=round(auc_pairs([r["y"] for r in vc], [r["c"] for r in vc]), 4))
    fl = [r["flag"] for r in rows]
    out["recall_at_threshold"] = round(sum(f for f, t in zip(fl, y) if t) / sum(y), 4)
    out["false_alarm_at_threshold"] = round(sum(f for f, t in zip(fl, y) if not t) / (len(y) - sum(y)), 4)
    # placebo: permuted labels (200 permutations)
    rnd = random.Random(1)
    pa, pd_ = [], []
    for _ in range(200):
        yp = y[:]; rnd.shuffle(yp)
        pa.append(auc_pairs(yp, c))
        ysp = ys[:]; rnd.shuffle(ysp)
        pd_.append(auc_pairs(ysp, cs_) - auc_pairs(ysp, ss))
    out["placebo_permuted_auroc_c_mean"] = round(float(np.mean(pa)), 4)
    out["placebo_permuted_auroc_c_p95"] = round(float(np.percentile(pa, 95)), 4)
    out["placebo_permuted_delta_mean"] = round(float(np.mean(pd_)), 4)
    out["placebo_permuted_delta_p97_5"] = round(float(np.percentile(pd_, 97.5)), 4)
    out["perm_p_value_c_score"] = (1 + sum(v >= out["auroc_c_score"] for v in pa)) / 201
    out["placebo_constant_score_auroc"] = auc_pairs(y, [0.0] * len(y))
    # cost from raw cached responses (not the cost log)
    raw = sum(json.load(open(f))["cost_usd"] for f in glob.glob(str(ROOT / "data" / "peer_raw*" / "*" / "*.json")))
    log = sum(json.loads(l)["cost_usd"] for l in open(ROOT / "logs" / "cost_log.jsonl") if l.strip())
    out["cost_from_raw_cache_usd"] = round(raw, 4)
    out["cost_from_cost_log_usd"] = round(log, 4)
    # comparison with the pipeline's aggregated numbers
    S = json.load(open(R / "summary.json"))
    P = S["auroc"]["primary"]
    out["pipeline"] = {"auroc_c_score": P["c_score"]["auroc"], "auroc_sc5_cheap": P["sc5_cheap"]["auroc"],
                       "delta": S["paired_delta_auroc"]["primary"]["c_score-sc5_cheap"]["delta"],
                       "recall": P["c_score"]["threshold"]["recall"], "false_alarm": P["c_score"]["threshold"]["false_alarm"],
                       "cost_total": S["cost"]["total_usd"],
                       "auroc_c_vocab_clean": S["auroc"]["vocab_clean"]["c_score"]["auroc"], "n_vocab_clean": S["auroc"]["vocab_clean"]["c_score"]["n"]}
    (R / "audit_rederive.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
