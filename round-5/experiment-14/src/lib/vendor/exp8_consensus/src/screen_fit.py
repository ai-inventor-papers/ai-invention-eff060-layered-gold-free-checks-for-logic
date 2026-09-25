#!/usr/bin/env python3
"""STEP 4 (screen only): compute PEER/TEXT features on the iteration-1 screen, select the NF variant, fit the fusion,
freeze everything in results/prereg.json (sha256 + UTC timestamp). Dataset E is NOT read here.

usage: screen_fit.py compute [--mini N]   -> results/screen_scores.jsonl (+ probes / rewrites rows), prereg_selection.json
       screen_fit.py fit                  -> results/screen_fit.json, results/prereg.json, results/prereg.sha256
"""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import math
import multiprocessing as mp
import os
import random
import sys
import time
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from loguru import logger

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))
os.environ.setdefault("NLTK_DATA", str(ROOT / "data" / "nltk_data"))
import peer_text as PT  # noqa: E402
import pool_scoring as PS  # noqa: E402

SD = ROOT / "data" / "screen"
RES = ROOT / "results"
PEER_FAMILY = {"P1": "meta", "P2": "qwen", "P3": "deepseek", "P4": "mistral", "P5": "google", "P6": "openai"}
LLM_SYSTEMS = ["gpt-3.5-turbo", "gpt-4", "text-davinci-003"]
PARAMS = {"variants": ["NF-pure", "NF-anchored", "ALIGN"], "k": 5, "tau": {"NF-pure": None, "NF-anchored": 0.5, "ALIGN": None},
          "timeout_ms": 2000, "pair_cap_s": 30, "k6_seeds": 5, "medoid_budget_s": 0, "do_align": True,
          "do_text": True, "codes": True, "allpool": True, "famfield": False}
N_WORKERS = 12

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(ROOT / "logs" / "screen_fit.log", rotation="30 MB", level="DEBUG")


def jl(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []


def sha1(s: str) -> str:
    return hashlib.sha1(s.encode()).hexdigest()


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


# =================================================================================================== labels
def solver_label(auto: str | None) -> str | None:
    return {"CORRECT": "CORRECT", "EQ": "CORRECT", "VOCAB_GRAN": "CORRECT", "ERROR": "ERROR", "COMPOUND": "ERROR"}.get(auto or "")


def adj_label(v: dict) -> str | None:
    if v["label_tier"] in ("A", "B") and v["final_label"] in ("CORRECT", "ERROR") and not v.get("reading_choice"):
        return v["final_label"]
    return None


# =================================================================================================== pools
def build_pools(items: list[dict]) -> dict:
    """sentence_key -> {'text', 'members': {member_id: fol}} (exp C build_sentences logic, SC samples omitted)."""
    uj = json.loads((SD / "units.json").read_text())
    peers = jl(SD / "peer_outputs.jsonl")
    src_unit = {}
    for it in sorted(items, key=lambda x: (x["track"] != "L", x["item_id"])):
        t = it["sentence_key"]
        if t in src_unit:
            continue
        if it["kind"] == "conclusion":
            src_unit[t] = f"F:{it['concl_id']}"
        elif it["kind"] == "premise":
            src_unit[t] = uj["premise_unit"].get(t)
        else:
            src_unit[t] = f"M:{it['malls_id']}"
    peer_by = defaultdict(dict)
    for r in peers:
        if r.get("sentence_norm") is None:
            continue
        peer_by[(r["unit_id"], r["sentence_norm"])].setdefault(r["peer"], r)
    uidx = {u["unit_id"]: u for u in uj["units"]}
    by_t = defaultdict(list)
    for it in items:
        by_t[it["sentence_key"]].append(it)
    out = {}
    for t, its in by_t.items():
        u = src_unit.get(t)
        entry = uidx[u].get("logiclm_entry") if u in uidx else None
        mem = {}
        for p in PEER_FAMILY:
            row = peer_by.get((u, t), {}).get(p)
            if row and row.get("fol") and PT.parse_fol(row["fol"]) is not None:
                mem[p] = row["fol"].strip()
        for s in LLM_SYSTEMS:
            cands = [x for x in its if x["track"] == "L" and x["system"] == s]
            if not cands:
                continue
            en = lambda x: int(x["logiclm_entry"].rsplit("_", 1)[-1]) if x.get("logiclm_entry") and x["logiclm_entry"].rsplit("_", 1)[-1].isdigit() else 10 ** 9
            cands.sort(key=lambda x: (x.get("logiclm_entry") != entry, en(x), x["item_id"]))
            f = cands[0]["candidate_fol"]
            if f and PT.parse_fol(f) is not None:
                mem["LL:" + s] = f.strip()
        out[t] = {"text": its[0]["text"], "members": mem}
    return out


# =================================================================================================== probes
def _pred_names(e):
    return list(PT.pred_keys(e))


def make_probes(base_items: list[dict], vocab_by_arity: dict, story_preds: dict) -> list[dict]:
    """MEANING_RENAME / ROLE_PERMUTE / SWAP probes (ERROR by construction; z3 non-equivalence under identity verified)."""
    out = []
    base = sorted(base_items, key=lambda x: sha1("probe|" + x["item_id"]))
    counts = Counter()
    for x in base:
        e = PT.parse_fol(x["candidate_fol"])
        if e is None:
            continue
        keys = _pred_names(e)
        rnd = random.Random(sha1("probe|" + x["item_id"]))
        # MEANING_RENAME: one predicate -> a different same-arity predicate from the same story, else from the screen vocab
        if counts["MEANING_RENAME"] < 150 and keys:
            k = keys[rnd.randrange(len(keys))]
            pool = [n for n, a in story_preds.get(x["item_id"], []) if a == k[1] and n not in {q[0] for q in keys}]
            if not pool:
                pool = [n for n in vocab_by_arity.get(k[1], []) if n not in {q[0] for q in keys}]
            if pool:
                new = pool[rnd.randrange(len(pool))]
                e2 = PT.rename(e, {k: new}, {})
                if EQ(e, e2) is False:
                    out.append({"probe": "MEANING_RENAME", "base_item_id": x["item_id"], "fol": PT.to_str(e2), "detail": f"{k[0]}->{new}"})
                    counts["MEANING_RENAME"] += 1
        # ROLE_PERMUTE: swap two same-arity predicates with different polarity profiles
        if counts["ROLE_PERMUTE"] < 150:
            sig = PT.symbol_signature(e)["preds"]
            cand_pairs = [(a, b) for a, b in __import__("itertools").combinations(keys, 2)
                          if a[1] == b[1] and sig[a]["pol"] != sig[b]["pol"]]
            if cand_pairs:
                a, b = cand_pairs[rnd.randrange(len(cand_pairs))]
                e2 = PT.rename(e, {a: b[0], b: a[0]}, {})
                if EQ(e, e2) is False:
                    out.append({"probe": "ROLE_PERMUTE", "base_item_id": x["item_id"], "fol": PT.to_str(e2), "detail": f"{a[0]}<->{b[0]}"})
                    counts["ROLE_PERMUTE"] += 1
        # SWAP: permute the arguments of one binary atom
        if counts["SWAP"] < 150:
            vs = PT._variants_swap(e)
            if vs:
                e2 = vs[rnd.randrange(len(vs))]
                if EQ(e, e2) is False:
                    out.append({"probe": "SWAP", "base_item_id": x["item_id"], "fol": PT.to_str(e2), "detail": "swap"})
                    counts["SWAP"] += 1
    logger.info(f"probes: {dict(counts)}")
    return out


def EQ(a, b):
    try:
        return PT.EFOL.equivalent(a, b, ms=5000)
    except Exception:  # noqa: BLE001
        return None


# =================================================================================================== L3 questionnaires
def questionnaires(texts: list[str]) -> dict:
    """Cached exp A flash-lite answers (iteration 1 cache; zero new cost). Missing -> None (L3 imputed z=0)."""
    import llm as LA
    import fol_triage as FT
    LA.CACHE_P = ROOT / "cache" / "expA_llm_cache.jsonl"
    LA.LEDGER_P = ROOT / "cache" / "expA_ledger_unused.jsonl"
    out = {}

    async def run():
        llm = LA.CachedLLM()
        for t in dict.fromkeys(texts):
            try:
                r = await FT.role_questionnaire(t, llm, "google/gemini-2.5-flash-lite", tag="L3")
                out[t] = r["q"]
            except LA.CacheMiss:
                out[t] = None
    asyncio.run(run())
    logger.info(f"L3 questionnaires from the iteration-1 cache: {sum(v is not None for v in out.values())}/{len(out)}")
    return out


# =================================================================================================== compute
SELECTION_RULE = {
    "rule": ("component threshold per variant = smallest g_score value giving FA <= 0.10 on AGREE-set CORRECT items of "
             "track L (LLM systems); eligible iff RENAME FA <= 0.10 (share of RENAME rewrites of screen-CORRECT bases with "
             "g >= threshold) AND ROLE_PERMUTE probe recall >= 0.50; choose the eligible variant with the highest AGREE-set "
             "AUROC of g_score; |ΔAUROC| < 0.005 -> NF-anchored. None eligible -> F1 FAILED: peer signal = c_score_align-based "
             "consensus (iteration-1 aligner) and NF numbers reported as a negative."),
    "variants": {"NF-pure": {"k": 5, "tau": "inf"}, "NF-anchored": {"k": 5, "tau": 0.5}},
    "degenerate_rule_F2": "if the selected g_score has AGREE AUROC < 0.6 or > 40% of AGREE items tie at g=0 -> fuse "
                          "c_score_nf instead of g_score ([c_score_nf, l2_bow, l3_z3]) and report F2 as failed",
    "design_changes_before_any_scoring": [
        "signature cost extended with a semantic clamp profile (5 components x 0.2) after unit tests showed a contrapositive "
        "being mis-aligned by purely syntactic signatures (tests/test_peer_text.py::test_equivalent_rewrites_zero)",
        "k-best by exact Murty enumeration instead of Murty-lite (the lite variant missed the identity mapping on ties)",
        "NF-anchored cost: if both symbols are text-anchored, cost = anchor cost + 0.25 x structural cost, else structural + "
        "0.5 (the additive 1.0 x anchor rule tied a constant swap with its correction; test_swap_code)",
        "NEG unit code = one literal-polarity toggle of the unit has majority support (plain ¬unit is not the NEG repair)",
        "mapping acceptance counts entailments NOT refuted by the finite-model refuter (sound upper bound of the z3 count); "
        "z3 then verifies the accepted mapping only (speed; z3 on all k mappings would multiply E time by ~k)",
        "coverage pools per-peer shares of majority units (mean over peers) instead of z3-deduplicating units across peers",
        "item_id in E is not unique (115 zero/few-shot twins with identical outputs): rows are keyed by row_key = item_id|prompt_variant",
    ],
    "written_utc": None,
}


def compute(mini: int = 0):
    RES.mkdir(exist_ok=True)
    sel = dict(SELECTION_RULE)
    sel["written_utc"] = datetime.now(timezone.utc).isoformat()
    p = RES / "prereg_selection.json"
    if not p.exists():
        p.write_text(json.dumps(sel, indent=1, ensure_ascii=False))
        (RES / "prereg_selection.sha256").write_text(sha256_file(p) + "\n")
    items = json.loads((SD / "screen_items.json").read_text())
    labs = json.loads((SD / "screen_adjudicated_labels.json").read_text())
    pools = build_pools(items)
    inv = json.loads((ROOT / "data" / "invariance_items.json").read_text())
    by_id = {x["item_id"]: x for x in items}
    fam = lambda x: "openai" if x["track"] == "L" else "human"
    # probes from screen-CORRECT items of tracks L/H
    correct = [x for x in items if labs.get(x["item_id"], {}).get("final_label") == "CORRECT" and PT.parse_fol(x["candidate_fol"])]
    vocab = defaultdict(set)
    for x in items:
        e = PT.parse_fol(x["candidate_fol"])
        if e is not None:
            for k in PT.pred_keys(e):
                vocab[k[1]].add(k[0])
    vocab = {a: sorted(v) for a, v in vocab.items()}
    story = {r["base_item_id"]: [tuple(d) for d in r.get("declared_predicates") or []] for r in inv}
    probes = make_probes(correct, vocab, story)
    (RES / "screen_probes.json").write_text(json.dumps(probes, ensure_ascii=False, indent=0))
    # sentences to score
    extra = defaultdict(list)
    for r in inv:
        if r["base_item_id"] in by_id:
            extra[by_id[r["base_item_id"]]["sentence_key"]].append({"key": "RW:" + r["rw_id"], "fol": r["candidate_fol"],
                                                                    "base": r["base_item_id"], "family": fam(by_id[r["base_item_id"]]),
                                                                    "system": by_id[r["base_item_id"]]["system"]})
    for i, pr in enumerate(probes):
        b = by_id[pr["base_item_id"]]
        extra[b["sentence_key"]].append({"key": f"PR:{pr['probe']}:{pr['base_item_id']}", "fol": pr["fol"], "base": pr["base_item_id"],
                                         "family": fam(b), "system": b["system"]})
    keys = sorted(pools)
    if mini:
        keys = sorted(random.Random(0).sample(keys, mini))
    qs = questionnaires([pools[t]["text"] for t in keys])
    tasks = []
    by_t = defaultdict(list)
    for x in items:
        by_t[x["sentence_key"]].append(x)
    for t in keys:
        rows = [{"key": x["item_id"], "fol": x["candidate_fol"], "family": fam(x), "system": x["system"], "is_peer": False}
                for x in by_t[t] if x["track"] in ("L", "H")]
        rows += [{"key": "M:" + m, "fol": f, "family": PEER_FAMILY.get(m, "openai"), "system": m.replace("LL:", ""),
                  "is_peer": True} for m, f in pools[t]["members"].items()]
        rows += [dict(r, is_peer=False) for r in extra.get(t, [])]
        tasks.append({"sentence_id": sha1(t)[:12], "sentence_key": t, "text": pools[t]["text"], "q": qs.get(pools[t]["text"]), "rows": rows})
    logger.info(f"screen sentences {len(tasks)}; rows {sum(len(t['rows']) for t in tasks)}; probes {len(probes)}")
    outp = RES / ("screen_scores.jsonl" if not mini else f"screen_scores_mini{mini}.jsonl")
    done = {r["sentence_id"] for r in jl(outp)} if not mini else set()
    todo = [t for t in tasks if t["sentence_id"] not in done]
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=N_WORKERS, mp_context=mp.get_context("spawn"), initializer=PS.init_worker,
                             initargs=(3.5,)) as ex, outp.open("a") as fh:
        futs = {ex.submit(PS.score_sentence, t, PARAMS): t for t in sorted(todo, key=lambda t: -len(t["rows"]))}
        for i, fu in enumerate(as_completed(futs)):
            t = futs[fu]
            try:
                res = fu.result()
            except Exception as e:  # noqa: BLE001 - a sentence failure is logged and its rows marked, never dropped
                logger.error(f"sentence {t['sentence_id']} failed: {e}")
                res = {"sentence_id": t["sentence_id"], "rows": [{"key": r["key"], "coverage_status": "WORKER_FAIL"} for r in t["rows"]],
                       "stats": {"error": str(e)[:200]}}
            res["sentence_key"] = t["sentence_key"]
            fh.write(json.dumps(res, ensure_ascii=False) + "\n")
            fh.flush()
            if (i + 1) % 25 == 0:
                logger.info(f"screen {i + 1}/{len(todo)} sentences, {time.time() - t0:.0f}s")
    logger.info(f"screen compute done in {time.time() - t0:.0f}s")


# =================================================================================================== fit
def auroc(y, s):
    from sklearn.metrics import roc_auc_score
    y, s = np.asarray(y), np.asarray(s, dtype=float)
    return float(roc_auc_score(y, s)) if len(set(y)) == 2 else float("nan")


def thr_at_fa(s_neg: list[float], fa: float = 0.10) -> float:
    """Smallest threshold t with share(s_neg >= t) <= fa (flag iff score >= t)."""
    vals = sorted(set(s_neg))
    s_neg = np.asarray(s_neg)
    for t in vals + [max(vals) + 1e-9]:
        if np.mean(s_neg >= t) <= fa:
            return float(t)
    return float("inf")


def fit_logistic(X: np.ndarray, y: np.ndarray, groups: list, features: list[str]) -> dict:
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import GroupKFold
    mu = np.nanmean(X, axis=0)
    sd = np.nanstd(X, axis=0)
    sd[sd == 0] = 1.0
    Z = np.where(np.isnan(X), 0.0, (X - mu) / sd)
    best = None
    oof_by_c = {}
    for C in (0.1, 1.0, 10.0):
        oof = np.zeros(len(y))
        for tr, te in GroupKFold(5).split(Z, y, groups):
            m = LogisticRegression(C=C, max_iter=2000).fit(Z[tr], y[tr])
            oof[te] = m.predict_proba(Z[te])[:, 1]
        a = auroc(y, oof)
        oof_by_c[C] = (a, oof)
        if best is None or a > best[0] + 1e-12:
            best = (a, C)
    m = LogisticRegression(C=best[1], max_iter=2000).fit(Z, y)
    return {"features": features, "mean": mu.tolist(), "sd": sd.tolist(), "coef": m.coef_[0].tolist(),
            "intercept": float(m.intercept_[0]), "C": best[1], "oof_auroc": best[0], "oof_auroc_by_C": {str(c): v[0] for c, v in oof_by_c.items()},
            "_oof": oof_by_c[best[1]][1].tolist(), "_insample": m.predict_proba(Z)[:, 1].tolist()}


def fit():
    items = {x["item_id"]: x for x in json.loads((SD / "screen_items.json").read_text())}
    labs = json.loads((SD / "screen_adjudicated_labels.json").read_text())
    rows = {}
    for s in jl(RES / "screen_scores.jsonl"):
        for r in s["rows"]:
            r["sentence_key"] = s["sentence_key"]
            rows[r["key"]] = r
    sel = json.loads((RES / "prereg_selection.json").read_text())
    # ---------------- label sets
    agree, all_adj = [], []
    conf = Counter()
    for iid, v in labs.items():
        if iid not in items or iid not in rows or v["track"] not in ("L", "H"):
            continue
        sl, al = solver_label(v["auto_label"]), adj_label(v)
        conf[(v["track"], sl, al)] += 1
        if al is not None:
            all_adj.append((iid, al))
        if sl is not None and al is not None and sl == al:
            agree.append((iid, al))
    cnt = Counter((items[i]["track"], l) for i, l in agree)
    logger.info(f"AGREE set {len(agree)}: {dict(cnt)}; confusion {dict(conf)}")
    y_ag = np.array([1 if l == "ERROR" else 0 for _, l in agree])
    grp = [rows[i]["sentence_key"] for i, _ in agree]
    L_correct = [i for i, l in agree if l == "CORRECT" and items[i]["track"] == "L"]
    out = {"agree_counts": {f"{k[0]}:{k[1]}": v for k, v in cnt.items()},
           "label_confusion": {f"{k[0]}|solver={k[1]}|adj={k[2]}": v for k, v in conf.items()}}

    def col(ids, c, default=None):
        return [rows[i].get(c, default) for i in ids]
    # ---------------- variant selection
    var_ev = {}
    for v in ("NF-pure", "NF-anchored"):
        g = [x if x is not None else 1.0 for x in col([i for i, _ in agree], f"{v}:g_score")]
        gneg = [rows[i][f"{v}:g_score"] for i in L_correct if rows[i].get(f"{v}:g_score") is not None]
        thr = thr_at_fa(gneg, 0.10)
        rn = [r for k, r in rows.items() if k.startswith("RW:") and "_RENAME" in k and labs.get(k[3:].rsplit("_RENAME", 1)[0], {}).get("final_label") == "CORRECT"]
        rn_fa = float(np.mean([(r.get(f"{v}:g_score") if r.get(f"{v}:g_score") is not None else 1.0) >= thr for r in rn])) if rn else None
        rp = [r for k, r in rows.items() if k.startswith("PR:ROLE_PERMUTE:")]
        rp_rec = float(np.mean([(r.get(f"{v}:g_score") if r.get(f"{v}:g_score") is not None else 1.0) >= thr for r in rp])) if rp else None
        ties0 = float(np.mean([x == 0 for x in g]))
        var_ev[v] = {"threshold": thr, "agree_auroc": auroc(y_ag, g), "rename_fa": rn_fa, "n_rename": len(rn),
                     "role_permute_recall": rp_rec, "n_role_permute": len(rp), "share_g0": ties0,
                     "eligible": bool(rn_fa is not None and rp_rec is not None and rn_fa <= 0.10 and rp_rec >= 0.50)}
    elig = [v for v in var_ev if var_ev[v]["eligible"]]
    if not elig:
        chosen, f1_failed = None, True
    else:
        f1_failed = False
        if len(elig) == 2 and abs(var_ev["NF-pure"]["agree_auroc"] - var_ev["NF-anchored"]["agree_auroc"]) < 0.005:
            chosen = "NF-anchored"
        else:
            chosen = max(elig, key=lambda v: var_ev[v]["agree_auroc"])
    logger.info(f"variant evidence {json.dumps(var_ev)} -> chosen {chosen} (F1 failed={f1_failed})")
    out["variant_evidence"] = var_ev
    out["variant_chosen"] = chosen
    out["F1_failed"] = f1_failed
    # the peer feature used for fusion
    # F1 failed -> graded consensus with the iteration-1 aligner inside (variant ALIGN) is the peer signal, fused with
    # c_score_align (iteration-1 binary consensus) in place of c_score_nf; the F2 degeneracy rule applies to ALIGN:g_score
    base_v = "ALIGN" if f1_failed else chosen
    g_all = [x if x is not None else 1.0 for x in col([i for i, _ in agree], f"{base_v}:g_score")]
    gv = {"agree_auroc": auroc(y_ag, g_all), "share_g0": float(np.mean([x == 0 for x in g_all]))}
    out["peer_variant_used"] = base_v
    out["peer_variant_evidence"] = gv
    second = "c_score_align" if f1_failed else f"{chosen}:c_score_nf"
    if gv["agree_auroc"] < 0.6 or gv["share_g0"] > 0.40:
        out["F2_failed"] = True
        peer_feat = second
        feats_fused = [second, "l2_bow", "l3_z3"]
    else:
        out["F2_failed"] = False
        peer_feat = f"{base_v}:g_score"
        feats_fused = [peer_feat, second, "l2_bow", "l3_z3"]
    out["peer_feature"] = peer_feat
    feats_fused = list(dict.fromkeys(feats_fused))

    def X_of(ids, feats):
        return np.array([[np.nan if rows[i].get(f) is None else float(rows[i][f]) for f in feats] for i in ids], dtype=float)
    ag_ids = [i for i, _ in agree]
    models = {}
    for name, feats, ids, yv, gg in (("fusion", feats_fused, ag_ids, y_ag, grp),
                                     ("text_only", ["l2_bow", "l3_z3"], ag_ids, y_ag, grp)):
        m = fit_logistic(X_of(ids, feats), yv, gg, feats)
        ins = m.pop("_insample")
        m.pop("_oof")
        neg = [p for i, p in zip(ids, ins) if i in set(L_correct)]
        m["threshold"] = thr_at_fa(neg, 0.10)
        models[name] = m
    adj_ids = [i for i, _ in all_adj]
    y_adj = np.array([1 if l == "ERROR" else 0 for _, l in all_adj])
    m = fit_logistic(X_of(adj_ids, feats_fused), y_adj, [rows[i]["sentence_key"] for i in adj_ids], feats_fused)
    ins = m.pop("_insample")
    m.pop("_oof")
    m["threshold"] = thr_at_fa([p for i, p, l in zip(adj_ids, ins, y_adj) if l == 0 and items[i]["track"] == "L"], 0.10)
    models["sensitivity_all_adj"] = m
    gpe = [rows[i].get(peer_feat) for i in L_correct if rows[i].get(peer_feat) is not None]
    models["peer_only"] = {"feature": peer_feat, "threshold": thr_at_fa(gpe, 0.10), "agree_auroc": auroc(y_ag, [x if x is not None else 1.0 for x in col(ag_ids, peer_feat)])}
    out["models"] = models
    # ---------------- descriptive screen numbers (all on the AGREE set)
    desc = {}
    for c in [f"{v}:{k}" for v in ("NF-pure", "NF-anchored", "ALIGN") for k in ("g_score", "c_score_nf", "g_score_allpool", "g_score_k6")] + \
             ["c_score_align", "c_score_align_allpool", "l2_bow", "l3_z3", "l2_role"]:
        vals = col(ag_ids, c)
        ok = [(yy, float(x)) for yy, x in zip(y_ag, vals) if x is not None]
        if len(ok) > 20:
            desc[c] = {"auroc": auroc([a for a, _ in ok], [b for _, b in ok]), "n": len(ok)}
    out["agree_auroc_components"] = desc
    # P2 pre-test: Spearman(peer, text) among errors
    from scipy.stats import spearmanr
    err = [i for i, l in agree if l == "ERROR"]
    a_ = [rows[i].get(peer_feat) for i in err]
    b_ = [rows[i].get("l2_bow") for i in err]
    ok = [(x, y) for x, y in zip(a_, b_) if x is not None and y is not None]
    out["P2_pretest_spearman_peer_vs_l2bow_errors"] = float(spearmanr([x for x, _ in ok], [y for _, y in ok])[0]) if ok else None
    # placebo: labels shuffled within sentence
    rng = np.random.default_rng(20260923)
    fused_in = [PT.apply_logistic(models["fusion"], rows[i]) for i in ag_ids]
    yp = y_ag.copy()
    by_s = defaultdict(list)
    for j, gk in enumerate(grp):
        by_s[gk].append(j)
    pl = []
    for _ in range(200):
        yy = yp.copy()
        perm = rng.permutation(len(yy))
        yy = yy[perm]
        pl.append(auroc(yy, fused_in))
    out["placebo_shuffled_auroc_mean"] = float(np.mean(pl))
    # regression checks vs iteration 1
    A = {r["item_id"]: r for r in jl(SD / "expA_per_item.jsonl")}
    same_bow = same_l3 = n_bow = n_l3 = 0
    for i, r in rows.items():
        a = A.get(i)
        if not a or a.get("track") not in ("L", "H") or r.get("l2_bow") is None:
            continue
        if a.get("bow_n_unanch") is not None:
            n_bow += 1
            same_bow += abs(((a.get("bow_n_unanch") or 0) + (a.get("bow_uncarried") or 0)) - r["l2_bow"]) < 1e-9
        if a.get("l3_score") is not None and r.get("l3_z3") is not None:
            n_l3 += 1
            same_l3 += abs(a["l3_score"] - r["l3_z3"]) < 1e-9
    trL = [(i, x["label"]) for i, x in items.items() if x["track"] == "L" and x["label"] in ("CORRECT", "ERROR") and i in rows]
    ca = [rows[i].get("c_score_align_allpool") for i, _ in trL]
    ok = [(1 if l == "ERROR" else 0, 1.0 if s is None else s) for (i, l), s in zip(trL, ca)]
    out["regression"] = {"l2_bow_identical": same_bow / max(1, n_bow), "n_bow": n_bow, "l3_identical": same_l3 / max(1, n_l3), "n_l3": n_l3,
                         "c_score_align_allpool_trackL_auroc": auroc([a for a, _ in ok], [b for _, b in ok]), "n_trackL": len(ok),
                         "expected_expC": 0.866}
    logger.info(f"regression {out['regression']}")
    (RES / "screen_fit.json").write_text(json.dumps(out, indent=1, ensure_ascii=False, default=float))
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["compute", "fit", "freeze"])
    ap.add_argument("--mini", type=int, default=0)
    a = ap.parse_args()
    if a.stage == "compute":
        compute(a.mini)
    elif a.stage == "fit":
        fit()


# =================================================================================================== freeze
FAMILY_MAP_VENDOR = {"G1": "meta", "G1b": "meta", "G2": "qwen", "G3": "mistral", "G4": "deepseek", "G5": "google",
                     "G8": "google", "G6": "microsoft", "G7": "openai", "F": "openai", "G9": "cohere",
                     "GOLD": "gold_as_system_never_peer", "CCG": "ccg2lambda_never_peer"}


def freeze():
    fitres = json.loads((RES / "screen_fit.json").read_text())
    rows = {}
    for s in jl(RES / "screen_scores.jsonl"):
        for r in s["rows"]:
            rows[r["key"]] = r
    labs = json.loads((SD / "screen_adjudicated_labels.json").read_text())
    agree_ids = [i for i, v in labs.items() if i in rows and v["track"] in ("L", "H") and solver_label(v["auto_label"]) is not None
                 and adj_label(v) is not None and solver_label(v["auto_label"]) == adj_label(v)]
    neutral = {}
    for f in ["ALIGN:g_score", "ALIGN:c_score_nf", "c_score_align", "NF-anchored:g_score", "NF-anchored:c_score_nf",
              "NF-pure:g_score", "l2_bow", "l3_z3"]:
        vals = [rows[i][f] for i in agree_ids if rows[i].get(f) is not None]
        neutral[f] = float(np.mean(vals)) if vals else None
    code_sha = {}
    for p in sorted((SRC).rglob("*.py")):
        code_sha[str(p.relative_to(ROOT))] = hashlib.sha1(p.read_bytes()).hexdigest()
    models = fitres["models"]
    frozen = {"variant": fitres["peer_variant_used"], "tau": {"NF-pure": None, "NF-anchored": 0.5, "ALIGN": None}, "k": 5,
              "timeout_ms": 2000, "fusion": models["fusion"], "text_only": models["text_only"],
              "sensitivity_all_adj": models["sensitivity_all_adj"], "peer_only": models["peer_only"]}
    card = (Path("/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_dataset_1") / "dataset_card.md").read_text()
    table = card[card.index("| stratum | sents | LLM rows |"):card.index("**Tier-A-only** counts")].strip()
    pre = {
        "title": "PEER+TEXT held-out confirmation on dataset E (run_u75jRHUss0zo iter 2, gen_art_experiment_5)",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "note": "Frozen on the iteration-1 screen ONLY. Dataset E labels have not been opened by any code of this artifact; "
                "E is scored once after this file's sha256 is written.",
        "code_sha1": code_sha,
        "E_blind_sha256": sha256_file(ROOT / "data" / "E_blind.jsonl"),
        "prereg_selection_sha256": (RES / "prereg_selection.sha256").read_text().strip(),
        "family_map_vendor": FAMILY_MAP_VENDOR,
        "family_map_sensitivity": "row metadata family field (google-gemma vs google-gemini, openai vs openai-frontier separate)",
        "peers": "E: every parseable LLM row of the sentence whose vendor family differs from the candidate's (leave-one-FAMILY-out); "
                 "malls_gpt4_gold and ccg2lambda rows are scored as candidates, never peers. Screen: P1-P6 + Logic-LM rows; "
                 "track-L (OpenAI) candidates get P1-P5, track-H (human) candidates get all.",
        "scoring_params": {"variants": ["ALIGN", "NF-anchored"], "k": 5, "tau": {"NF-pure": None, "NF-anchored": 0.5, "ALIGN": None},
                           "timeout_ms": 2000, "pair_cap_s": 30, "k6_seeds": 5, "medoid_budget_s": 2, "do_align": True,
                           "do_text": True, "codes": True, "famfield": True, "allpool": False},
        "unit_cap": 16, "fm_domains": [[1, 16], [2, 24], [3, 24]], "clamp_domains": [[1, 64], [2, 64]],
        "variant": fitres["peer_variant_used"],
        "selection_evidence": {"variant_evidence": fitres["variant_evidence"], "F1_failed": fitres["F1_failed"],
                               "peer_variant_evidence": fitres["peer_variant_evidence"], "F2_failed": fitres["F2_failed"],
                               "peer_feature": fitres["peer_feature"], "agree_counts": fitres["agree_counts"],
                               "agree_auroc_components_screen": fitres["agree_auroc_components"],
                               "P2_pretest_spearman_screen": fitres["P2_pretest_spearman_peer_vs_l2bow_errors"],
                               "placebo_screen": fitres["placebo_shuffled_auroc_mean"], "regression": fitres["regression"]},
        "frozen": frozen,
        "imputation": {"unparseable": "1.0 (most suspicious) for every metric, including the judges",
                       "parseable_missing": "screen AGREE-set mean of the feature (neutral) for PEER-only; fusion uses z=0 for a "
                                            "missing feature and the frozen TEXT-only model when the peer feature is missing",
                       "neutral": neutral,
                       "judge_missing": "a parseable row without a judge score is NOT imputed: judge comparisons are restricted "
                                        "to rows where both scores exist (fallback 6 subsample), with n reported"},
        "label_regimes": {
            "R_AB": "system_class llm, label_tier in {A,B}, final_label in {CORRECT, ERROR}, not reading_choice; CONTESTED excluded "
                    "(sensitivities CONTESTED->CORRECT and ->ERROR; with/without the L25 top-up); malls_gpt4_gold rows a separate "
                    "gold-as-system table",
            "R_A": "R_AB restricted to label_tier == A"},
        "testability": {"rule": ">=50 ERROR and >=50 CORRECT rows (and >=25 sentences each side), else untestable/sign-only",
                        "dataset_card_table": table,
                        "declared_testable_R_AB": ["pooled", "L25", "L20", "EXC", "CTRL", "long pool L25+L20+EXC"],
                        "declared_testable_R_A": ["L20", "EXC", "pooled L20+EXC"],
                        "sign_only_R_A": ["L25", "CTRL", "pooled all strata (reported, not decisive)"]},
        "analyses": {
            "bootstrap": {"B": 2000, "cluster": "sentence_id", "seed": 20260923, "ci": "percentile 95%"},
            "a_headline": "ΔAUROC = p_peer_text - judge_cheap_disg (flash-lite, disguised) on identical rows; pooled R_AB, pooled R_A "
                          "(L20+EXC), per stratum, long pool; plus every component. Criterion (a)-this-artifact: CI>0 pooled R_AB AND "
                          "sign>0 pooled R_A. Criterion (c)-long: CI>0 in the long pool. DeLong as secondary.",
            "a_judge_fallback": "if flash-lite disguised scores exist for < 300 rows per class in pooled R_AB when analysis runs, the "
                                "flash-lite comparison is reported on the judged subsample only (descriptive if untestable) and the "
                                "LOCAL iteration-1 exp D judge (Qwen3-8B, rubric B, .757 on screen) is the LABELLED SECONDARY BAR on "
                                "all rows; the flash-lite judge is never replaced in the criterion wording.",
            "b_P1": "matched FA 0.10 and 0.20 thresholds on the regime's CORRECT rows; recall by error group STRUCT (tier-A, "
                    "repair_ops ⊆ {QUANT,SCOPE,BIND,SWAP,NEG,REV,RESTR}, <=2 ops), COVERAGE (ops ⊆ {ADD,DROP}), MEANING_RENAME (tier-B "
                    "errors with MEANING_RENAME in error_ops), PEER_ENDORSED (errors eqmv to the aligner medoid, eqmv_medoid_eq True); "
                    "PEER = peer-only score, TEXT = text-only model. CONFIRMED if PEER>TEXT on STRUCT and TEXT>PEER on "
                    "MEANING_RENAME∪PEER_ENDORSED with >=1 CI excluding 0 and no reversal with CI excluding 0; REFUTED if either "
                    "reverses with CI excluding 0; else INCONCLUSIVE.",
            "c_P2": "Spearman(peer score, TEXT) among true errors (CI); fusion-gain decomposition over {peer-endorsed, non-endorsed} "
                    "errors vs all CORRECT; CONFIRMED if rho < 0.4 AND share of (fused - best single) gain from peer-endorsed >= 0.5.",
            "d_P3": "per metric logistic y ~ z(s) + z(words) + z(s)z(words), cluster-bootstrap CI of the interaction, for "
                    "c_score_align, ALIGN g, NF c_score, fused, judge; AUROC by word bin; fused-minus-judge Δ per stratum and "
                    "difference-in-Δ (long pool minus CTRL). CONFIRMED if the NF/aligner c_score interaction < 0 (CI), |g| <= 0.5|c| "
                    "and diff-in-Δ > 0.",
            "e_P4": "shared rewrite set (exp D invariance_items, screen pools): FA on rewrites of CORRECT bases and flip rate per family "
                    "for g, c_score_align, NF, l2_bow, l3, fused; judge rows from exp D rewrite_scores. CONFIRMED if fused FA <= 0.10 "
                    "on EVERY family and a judge >= 0.25 on >= 1 family. Probes descriptive.",
            "f_types": "R_A errors with 1-2 repair_ops: top unit code (NEG>QUANT>SWAP>DROP>ADD) contained in repair_ops; chance = "
                       "marginal code distribution; medoid_ops agreement; judge error_type agreement.",
            "g_system": "13 system x variant rows: mean fused p and mean judge vs R_AB error rate; Kendall tau-b with sentence "
                        "bootstrap CI; descriptive.",
            "h_complexity": "AUROC and FA@threshold vs words, n_quant, depth, n_conditions, exception_type (bins >=30/30).",
            "i_contamination": "AUROC(orig) - AUROC(disg) for judge and L3 (paired bootstrap), DiD fused-vs-judge; MDE = 2.8 x SE.",
            "j_coverage_cost": "every E row in the denominator; $ per item and cpu-s per item per component.",
            "k_misc": "gold-as-system flag rate vs panel gold audit; FA on tier-B CORRECT vs tier-A CORRECT.",
            "k6_check": "g_score_k6 (mean over 5 seeded 6-peer subsamples) reported next to g_score (screen pools ~5 peers, E ~9-11).",
        },
        "deviations_at_freeze": [
            "F1 FAILED on the screen by the pre-registered selection rule (both NF variants: >10% of AGREE track-L CORRECT items "
            "have g=1, so the FA-0.10 threshold flags nothing and ROLE_PERMUTE recall = 0). Per fallback 3 the peer signal is graded "
            "consensus with the iteration-1 aligner (variant ALIGN) fused with c_score_align; the shared-aligner confound with the "
            "solver labeller stays OPEN in this run. NF-anchored is still scored on E as a reported negative.",
            "OpenRouter shared key exhausted at ~18:00 UTC (limit_remaining 0) after 699/700 E L3 questionnaires and 20 judge units; "
            "fallback 6 judge rule above; key monitor re-launches the flash-lite judge if the key returns.",
            "L3 contamination arm (disguised questionnaire) depends on the key; reported only if it runs.",
        ] + SELECTION_RULE["design_changes_before_any_scoring"],
    }
    p = RES / "prereg.json"
    p.write_text(json.dumps(pre, indent=1, ensure_ascii=False, default=float))
    sha = sha256_file(p)
    (RES / "prereg.sha256").write_text(f"{sha}  prereg.json  {pre['timestamp_utc']}\n")
    logger.info(f"prereg frozen sha256 {sha}")


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "freeze":
    freeze()
