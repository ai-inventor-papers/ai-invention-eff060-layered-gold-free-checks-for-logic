#!/usr/bin/env python3
"""STEP 5 (+ STEP 6 rewrites, T5 sanity checks, secondary peer-as-candidate sample).

For every screen candidate c of sentence t:
  pool      = parsed LLM outputs for t (P1..P6 fresh peers + Logic-LM systems), leaving out c's own system;
              'human_original' is never a pool member
  eq_frac_* = share of pool members that are eqmv-equivalent to c (z3 timeouts count as NOT equivalent)
  medoid    = pool member with most eqmv partners in the pool (ties: larger component, then P1..P6, s1..s3)
  medoid_depth / medoid_ops = minimal typed repair c -> medoid (0 if eqmv(c, medoid))
  cluster_entropy = semantic entropy of the eqmv components of pool ∪ {c}
  sc5_* = share of the K=5 self-consistency samples eqmv-equivalent to c (missing/unparseable = not equivalent)

usage: consensus.py [--mini N] [--budget S] [--no-secondary]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

from loguru import logger

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.setrecursionlimit(10000)
from common import LLM_SYSTEMS, alignable_frac, item_id, safe_parse, strata  # noqa: E402
from eqcache import LabelCache, PairCache, RepairCache  # noqa: E402
from fol import equivalent  # noqa: E402
import rewrites as RW  # noqa: E402

RES = ROOT / "results"
PEER_IDS = ["P1", "P2", "P3", "P4", "P5", "P6"]
NONOAI = ["P1", "P2", "P3", "P4", "P5"]
ORDER = PEER_IDS + LLM_SYSTEMS
PEER_MODEL = {"P1": "meta-llama/llama-3.3-70b-instruct", "P2": "qwen/qwen3-235b-a22b-2507", "P3": "deepseek/deepseek-chat-v3.1",
              "P4": "mistralai/mistral-small-3.2-24b-instruct", "P5": "google/gemini-2.5-flash-lite", "P6": "openai/gpt-4.1-mini"}
PEER_FAMILY = {"P1": "meta", "P2": "qwen", "P3": "deepseek", "P4": "mistral", "P5": "google", "P6": "openai"}

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(ROOT / "logs" / "consensus.log", rotation="30 MB", level="DEBUG")


def jl(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []


def entry_num(eid: str | None) -> int:
    m = re.search(r"(\d+)$", eid or "")
    return int(m.group(1)) if m else 10 ** 9


def fol_ok(s: str | None) -> str | None:
    return s.strip() if s and safe_parse(s) is not None else None


# ------------------------------------------------------------------ sentence pools
def build_sentences(items, peers, sc, units, prem_unit):
    uidx = {u["unit_id"]: u for u in units}
    src_unit = {}
    for it in sorted(items, key=lambda x: (x["track"] != "L", x["item_id"])):
        t = it["sentence_key"]
        if t in src_unit:
            continue
        if it["kind"] == "conclusion":
            src_unit[t] = f"F:{it['concl_id']}"
        elif it["kind"] == "premise":
            src_unit[t] = prem_unit.get(t)
        else:
            src_unit[t] = f"M:{it['malls_id']}"
    peer_by = defaultdict(dict)   # (unit, key) -> {peer: row}
    for r in peers:
        if r.get("sentence_norm") is None:
            continue
        peer_by[(r["unit_id"], r["sentence_norm"])].setdefault(r["peer"], r)
    sc_by = defaultdict(lambda: defaultdict(dict))  # arm -> (unit, key) -> {sample: row}
    for r in sc:
        if r.get("sentence_norm") is None:
            continue
        sc_by[r["arm"]][(r["unit_id"], r["sentence_norm"])].setdefault(r["sample"], r)
    sc_units = defaultdict(set)  # arm -> units that have at least one SC call on disk
    for r in sc:
        if r["mapping_mode"] != "call_missing":
            sc_units[r["arm"]].add(r["unit_id"])
    unit_called = defaultdict(set)  # unit -> peers whose call returned something (attempted)
    for r in peers:
        if r["mapping_mode"] != "call_missing":
            unit_called[r["unit_id"]].add(r["peer"])
    sents = {}
    by_t = defaultdict(list)
    for it in items:
        by_t[it["sentence_key"]].append(it)
    for t, its in by_t.items():
        u = src_unit.get(t)
        unit_entry = uidx[u].get("logiclm_entry") if u in uidx else None
        members, raw = {}, {}
        for p in PEER_IDS:
            row = peer_by.get((u, t), {}).get(p)
            raw[p] = row["fol"] if row else None
            members[p] = fol_ok(row["fol"]) if row else None
        attempted = {p for p in PEER_IDS if p in unit_called.get(u, set())}
        for s in LLM_SYSTEMS:
            cands = [x for x in its if x["track"] == "L" and x["system"] == s]
            if not cands:
                continue
            cands.sort(key=lambda x: (x.get("logiclm_entry") != unit_entry, entry_num(x.get("logiclm_entry")), x["item_id"]))
            members[s] = fol_ok(cands[0]["candidate_fol"])
            raw[s] = cands[0]["candidate_fol"]
            attempted.add(s)
        scs = {}
        for arm in ("sc_cheap", "sc_same"):
            d = sc_by[arm].get((u, t), {})
            scs[arm] = [fol_ok(d[k]["fol"]) if k in d else None for k in range(5)]
            scs[arm + "_present"] = u in sc_units[arm]
        ref = next((x["reference_fol"] for x in its if x["label"] != "REF_UNPARSEABLE"), None)
        sents[t] = {"key": t, "unit": u, "members": members, "raw": raw, "attempted": sorted(attempted), "sc": scs,
                    "ref": ref, "text": its[0]["text"]}
    return sents


def entropy(sizes: list[int]) -> float:
    n = sum(sizes)
    return abs(-sum(k / n * math.log(k / n) for k in sizes if k)) if n else 0.0


def components(nodes: list[str], eqf) -> list[list[str]]:
    parent = {n: n for n in nodes}

    def f(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for i, a in enumerate(nodes):
        for b in nodes[i + 1:]:
            if eqf(a, b) is True:
                parent[f(a)] = f(b)
    comps = defaultdict(list)
    for n in nodes:
        comps[f(n)].append(n)
    return list(comps.values())


def score_candidate(cfol: str | None, own: str, S: dict, pc: PairCache, pool_ids: list[str] | None = None) -> dict:
    """Pool statistics for one candidate formula (medoid repair filled in later)."""
    mem = S["members"]
    pool = {m: f for m, f in mem.items() if m != own and f is not None and (pool_ids is None or m in pool_ids)}
    n_total = len([m for m in S["attempted"] if m != own and (pool_ids is None or m in pool_ids)])
    out = {"n_peers_parsed": len(pool), "n_peers_total": n_total, "pool_ids": sorted(pool, key=ORDER.index)}
    cf = fol_ok(cfol)
    if cf is None:
        out.update(coverage_status="candidate_unparseable")
        return out
    eqv = {m: pc.eq(cf, f) for m, f in pool.items()}
    out["pool_eq"] = {m: eqv[m] for m in out["pool_ids"]}
    out["n_timeouts"] = sum(v is None for v in eqv.values())

    def frac(ids):
        ids = [m for m in ids if m in pool]
        return (sum(eqv[m] is True for m in ids) / len(ids)) if ids else None
    out["eq_frac_full"] = frac(list(pool))
    out["eq_frac_peers6"] = frac(PEER_IDS)
    out["eq_frac_nonoai"] = frac(NONOAI)
    out["eq_frac_llm2"] = frac(LLM_SYSTEMS)
    ids = out["pool_ids"]
    # pool graph (member ids as nodes; equality through cached eqmv of their formulas)
    ef = lambda a, b: pc.eq(pool[a], pool[b])
    comps = components(ids, ef)
    comp_of = {m: len(c) for c in comps for m in c}
    comps_c = components(["__c__"] + ids, lambda a, b: (eqv[b] if a == "__c__" else (eqv[a] if b == "__c__" else ef(a, b))))
    out["cluster_entropy"] = entropy([len(c) for c in comps_c])
    out["n_classes"] = len(comps_c)
    if len(pool) < 2:
        out.update(coverage_status="insufficient_pool")
    else:
        out.update(coverage_status="ok")
    if pool:
        deg = {m: sum(ef(m, q) is True for q in ids if q != m) for m in ids}
        med = sorted(ids, key=lambda m: (-deg[m], -comp_of[m], ORDER.index(m)))[0]
        assert med != own, "leave-one-out violated: medoid is the candidate's own system"
        out["medoid"] = med
        out["medoid_fol"] = pool[med]
        out["medoid_support"] = deg[med] / (len(ids) - 1) if len(ids) > 1 else None
        out["eq_medoid"] = eqv[med]
    return out


def sc_scores(cfol: str | None, S: dict, pc: PairCache) -> dict:
    out = {}
    cf = fol_ok(cfol)
    for arm, name in (("sc_cheap", "cheap"), ("sc_same", "same")):
        smp = S["sc"][arm]
        present = S["sc"].get(arm + "_present")
        out[f"sc5_present_{name}"] = bool(present)
        if cf is None:
            out[f"sc5_eq_frac_{name}"] = 0.0 if present else None
            continue
        if not present:
            out[f"sc5_eq_frac_{name}"] = None
            continue
        eqs = [pc.eq(cf, s) is True if s else False for s in smp]
        out[f"sc5_eq_frac_{name}"] = sum(eqs) / 5
        nodes = ["__c__"] + [f"s{k}" for k in range(5) if smp[k]]
        fm = {"__c__": cf, **{f"s{k}": smp[k] for k in range(5) if smp[k]}}
        comps = components(nodes, lambda a, b: pc.eq(fm[a], fm[b]))
        sizes = [len(c) for c in comps] + [1] * sum(1 for s in smp if not s)  # missing samples = singleton classes
        out[f"sc5_entropy_{name}"] = entropy(sizes)
    return out


# ------------------------------------------------------------------ planted errors (T5b pipeline check only)
def plant(e):
    """One typed edit: DROP the right operand of the first ∧/∨, else NEG the first atom."""
    def drop(x):
        k = x[0]
        if k in ("and", "or"):
            return x[1], True
        if k == "atom":
            return x, False
        if k in ("all", "ex"):
            b, d = drop(x[2]); return (k, x[1], b), d
        if k == "not":
            b, d = drop(x[1]); return ("not", b), d
        a, d = drop(x[1])
        if d:
            return (k, a, x[2]), True
        b, d = drop(x[2]); return (k, x[1], b), d

    def neg(x):
        k = x[0]
        if k == "atom":
            return ("not", x), True
        if k in ("all", "ex"):
            b, d = neg(x[2]); return (k, x[1], b), d
        if k == "not":
            b, d = neg(x[1]); return ("not", b), d
        a, d = neg(x[1])
        return (k, a, x[2]), d
    new, done = drop(e)
    if done and equivalent(new, e, ms=3000) is False:
        return new, "DROP"
    new, done = neg(e)
    if done and equivalent(new, e, ms=3000) is False:
        return new, "NEG"
    return None, None


@logger.catch(reraise=True)
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mini", type=int, default=0, help="restrict to the first N sentences (sorted keys)")
    ap.add_argument("--budget", type=float, default=10.0, help="medoid repair search budget (s)")
    ap.add_argument("--no-secondary", action="store_true")
    a = ap.parse_args()
    t_all = time.time()
    items = json.loads((RES / "screen_items.json").read_text())
    uj = json.loads((RES / "units.json").read_text())
    peers, sc = jl(RES / "peer_outputs.jsonl"), jl(RES / "sc_samples.jsonl")
    sents = build_sentences(items, peers, sc, uj["units"], uj["premise_unit"])
    keys = sorted(sents)
    if a.mini:
        rnd = random.Random(0)
        keys = sorted(rnd.sample(keys, min(a.mini, len(keys))))
        items = [x for x in items if x["sentence_key"] in set(keys)]
    logger.info(f"sentences: {len(keys)}, candidates: {len(items)}, peer rows: {len(peers)}, sc rows: {len(sc)}")
    pc, lc, rc = PairCache(), LabelCache(), RepairCache()

    # ---------------- rewrite + planted + gold pseudo-candidates
    correct = sorted([x for x in items if x["label"] == "CORRECT" and fol_ok(x["candidate_fol"])], key=lambda x: x["item_id"])
    rw_sel = correct[:150]
    rewrites = []
    for x in rw_sel:
        e = safe_parse(x["candidate_fol"])
        for fam, fn in RW.FAMILIES.items():
            try:
                if fam.startswith("RENAME"):
                    new, maps = RW.rename_rewrite(e, preds=fam != "RENAME_CONST_ONLY", consts=fam != "RENAME_PRED_ONLY")
                else:
                    new, maps = fn(e), None
            except (RecursionError, ValueError, KeyError, TypeError):
                logger.exception(f"rewrite {fam} failed on {x['item_id']}")
                new, maps = None, None
            if new is None or new == e:
                rewrites.append({"item_id": x["item_id"], "family": fam, "applicable": False})
                continue
            s = RW.to_str(new)
            ok_parse = safe_parse(s) is not None
            chk = equivalent(RW.inverse_rename(safe_parse(s), maps) if maps else safe_parse(s), e, ms=5000) if ok_parse else None
            rewrites.append({"item_id": x["item_id"], "family": fam, "applicable": True, "fol": s, "reparse_ok": ok_parse,
                             "equivalent_to_original": chk})
    bad = [r for r in rewrites if r.get("applicable") and r.get("equivalent_to_original") is not True]
    logger.info(f"rewrites: {sum(r['applicable'] for r in rewrites)} applicable; not-proved-equivalent: {len(bad)}")
    planted = []
    pl_sel = sorted([x for x in correct if x["track"] == "L"], key=lambda x: x["item_id"])
    for x in pl_sel:
        if len(planted) == 30:
            break
        new, op = plant(safe_parse(x["candidate_fol"]))
        if new is not None:
            planted.append({"item_id": x["item_id"], "op": op, "fol": RW.to_str(new)})

    # ---------------- pairwise eqmv
    by_id = {x["item_id"]: x for x in items}
    pairs = set()
    for t in keys:
        S = sents[t]
        fs = {f for f in S["members"].values() if f}
        fs |= {f for arm in ("sc_cheap", "sc_same") for f in S["sc"][arm] if f}
        fs |= {fol_ok(x["candidate_fol"]) for x in items if x["sentence_key"] == t} - {None}
        if S["ref"] and fol_ok(S["ref"]):
            fs.add(S["ref"].strip())
        fs = sorted(fs)
        pairs |= {(fs[i], fs[j]) for i in range(len(fs)) for j in range(i + 1, len(fs))}
    for r in rewrites + planted:
        if not r.get("fol") or not fol_ok(r["fol"]):
            continue
        S = sents[by_id[r["item_id"]]["sentence_key"]]
        pairs |= {(r["fol"], f) for f in S["members"].values() if f}
    t0 = time.time()
    pc.compute(pairs, tag="pairs")
    t_pairs = time.time() - t0
    logger.info(f"pairwise stage {t_pairs:.0f}s for {len(pairs)} pairs")

    # ---------------- primary candidates
    recs = []
    for x in items:
        S = sents[x["sentence_key"]]
        r = score_candidate(x["candidate_fol"], x["system"], S, pc)
        r.update(sc_scores(x["candidate_fol"], S, pc))
        r["item_id"] = x["item_id"]
        recs.append(r)
    need = [(fol_ok(by_id[r["item_id"]]["candidate_fol"]), r["medoid_fol"]) for r in recs
            if r.get("medoid_fol") and r.get("eq_medoid") is not True and r["coverage_status"] != "candidate_unparseable"]
    t0 = time.time()
    rc.compute(need, budget=a.budget, tag="medoid-repair")
    t_rep = time.time() - t0
    for r in recs:
        x = by_id[r["item_id"]]
        cf = fol_ok(x["candidate_fol"])
        if r["coverage_status"] == "candidate_unparseable" or not r.get("medoid_fol"):
            r.update(medoid_depth=3, medoid_ops=["NO_MEDOID" if cf else "CANDIDATE_UNPARSEABLE"])
        elif r["eq_medoid"] is True:
            r.update(medoid_depth=0, medoid_ops=[])
        else:
            rep = rc.get(cf, r["medoid_fol"])
            r.update(medoid_depth=rep["depth"] if rep and rep["depth"] is not None else 3,
                     medoid_ops=rep["ops"] if rep else ["COMPOUND"], medoid_repair_secs=rep["secs"] if rep else None)
        # seconds: z3 time attributable to this candidate
        secs = sum((pc.get(cf, S_f) or {}).get("secs", 0) for S_f in
                   [sents[x["sentence_key"]]["members"][m] for m in r.get("pool_ids", [])]) if cf else 0.0
        r["seconds_z3"] = round(secs + (r.get("medoid_repair_secs") or 0), 3)
        # pre-registered scores (coverage failures -> most suspicious value)
        N = r["n_peers_parsed"] + 1
        if r["coverage_status"] == "ok":
            r["c_score"] = 1 - r["eq_frac_full"]
        else:
            r["c_score"] = 1.0
            r["medoid_depth"] = 3 if r["coverage_status"] != "ok" else r["medoid_depth"]
        if r.get("cluster_entropy") is None or r["coverage_status"] != "ok":
            r["cluster_entropy"] = math.log(max(N, 2))
        r["alignable_frac"] = alignable_frac(safe_parse(x["candidate_fol"]), safe_parse(x["reference_fol"]))
    # ---------------- diagnostics labels: medoid vs reference for every labelled candidate
    lab_pairs = {(r["medoid_fol"], by_id[r["item_id"]]["reference_fol"]) for r in recs
                 if r.get("medoid_fol") and by_id[r["item_id"]]["label"] not in ("REF_UNPARSEABLE",)}
    # gold-as-candidate
    gold = []
    for t in keys:
        S = sents[t]
        if S["ref"] and fol_ok(S["ref"]):
            g = score_candidate(S["ref"], "__gold__", S, pc)
            gold.append({"sentence_key": t, "eq_frac_full": g.get("eq_frac_full"), "n_peers_parsed": g["n_peers_parsed"],
                         "is_trackL": any(x["track"] == "L" for x in items if x["sentence_key"] == t)})
    # ---------------- secondary: peer outputs as candidates
    peer_cands = []
    if not a.no_secondary:
        for t in keys:
            S = sents[t]
            if not S["ref"]:
                continue
            for p in PEER_IDS:
                if p not in S["attempted"]:
                    continue
                f = S["raw"].get(p)
                peer_cands.append({"sentence_key": t, "peer": p, "fol": f})
                if f and S["ref"]:
                    lab_pairs.add((f, S["ref"]))
    t0 = time.time()
    lc.compute(lab_pairs, budget=25.0, tag="labels")
    t_lab = time.time() - t0
    for r in recs:
        x = by_id[r["item_id"]]
        if r.get("medoid_fol") and x["label"] != "REF_UNPARSEABLE":
            ml = lc.get(r["medoid_fol"], x["reference_fol"])
            r["medoid_label"] = ml["label"] if ml else None
            r["medoid_ref_ops"] = ml["repair_ops"] if ml else None
    # ---------------- peer-as-candidate records
    peer_recs = []
    for pcand in peer_cands:
        S = sents[pcand["sentence_key"]]
        f = pcand["fol"]
        lab = lc.get(f, S["ref"]) if f else None
        r = score_candidate(f, pcand["peer"], S, pc)
        its = [x for x in items if x["sentence_key"] == pcand["sentence_key"]]
        tracks = sorted({x["track"] for x in its})
        cf = fol_ok(f)
        rec = {"unit": S["unit"], "model": PEER_MODEL[pcand["peer"]], "peer": pcand["peer"], "family": PEER_FAMILY[pcand["peer"]],
               "text": S["text"], "sentence_key": pcand["sentence_key"], "fol": f, "reference_fol": S["ref"],
               "label": (lab["label"] if lab else "UNPARSEABLE") if f else "PEER_MISSING",
               "auto_class": lab["auto_class"] if lab else None, "repair_ops": lab["repair_ops"] if lab else [],
               "vocab_strict": lab.get("vocab_strict") if lab else None,
               "strata": strata(S["text"], S["ref"]), "item_id": item_id(PEER_MODEL[pcand["peer"]], S["text"], f or ""),
               "sentence_tracks": tracks, "kind": its[0]["kind"],
               "eq_frac_full": r.get("eq_frac_full"), "eq_frac_peers6": r.get("eq_frac_peers6"),
               "eq_frac_llm2": r.get("eq_frac_llm2"), "n_peers_parsed": r["n_peers_parsed"],
               "coverage_status": r.get("coverage_status"), "cluster_entropy": r.get("cluster_entropy"),
               "medoid_flag": (r.get("eq_medoid") is not True) if cf else True, "pool_eq": r.get("pool_eq"),
               "alignable_frac": alignable_frac(safe_parse(f), safe_parse(S["ref"])) if f else None}
        rec["c_score"] = (1 - rec["eq_frac_full"]) if rec["coverage_status"] == "ok" else 1.0
        rec.update(sc_scores(f, S, pc))
        peer_recs.append(rec)

    # ---------------- rewrites / planted scoring
    rec_by = {r["item_id"]: r for r in recs}
    for rw in rewrites:
        if not rw.get("applicable") or not rw.get("reparse_ok"):
            continue
        x = by_id[rw["item_id"]]
        S = sents[x["sentence_key"]]
        base = rec_by[x["item_id"]]
        r = score_candidate(rw["fol"], x["system"], S, pc)
        rw["eq_frac_full"] = r.get("eq_frac_full")
        rw["base_eq_frac_full"] = base.get("eq_frac_full")
        rw["coverage_status"] = r.get("coverage_status")
        rw["flag"] = (pc.eq(rw["fol"], base["medoid_fol"]) is not True) if base.get("medoid_fol") else True
        rw["base_flag"] = base["medoid_depth"] >= 1
    for pl in planted:
        x = by_id[pl["item_id"]]
        S = sents[x["sentence_key"]]
        base = rec_by[x["item_id"]]
        r = score_candidate(pl["fol"], x["system"], S, pc)
        pl["c_score"] = (1 - r["eq_frac_full"]) if r.get("coverage_status") == "ok" else 1.0
        pl["base_c_score"] = base["c_score"]
        pl["rises"] = pl["c_score"] > pl["base_c_score"]
        pl["rises_or_max"] = pl["c_score"] > pl["base_c_score"] or pl["base_c_score"] == 1.0

    out = {"records": recs, "gold_as_candidate": gold, "rewrites": rewrites, "planted": planted,
           "timing": {"pairs_s": round(t_pairs, 1), "repair_s": round(t_rep, 1), "labels_s": round(t_lab, 1),
                      "total_s": round(time.time() - t_all, 1), "n_pairs": len(pairs), "n_sentences": len(keys),
                      "repair_budget_s": a.budget},
           "sentences": {t: {k: v for k, v in sents[t].items() if k in ("unit", "members", "attempted", "ref")} for t in keys}}
    suffix = f"_mini{a.mini}" if a.mini else ""
    (RES / f"consensus{suffix}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    (RES / f"peer_outputs_labelled{suffix}.json").write_text(json.dumps(peer_recs, ensure_ascii=False, indent=1))
    cov = Counter(r["coverage_status"] for r in recs)
    logger.info(f"coverage: {dict(cov)}; timing {out['timing']}")
    logger.info(f"per-candidate seconds (z3): mean {sum(r['seconds_z3'] for r in recs) / max(1, len(recs)):.3f}")


if __name__ == "__main__":
    main()
