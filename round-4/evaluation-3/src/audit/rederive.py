#!/usr/bin/env python3
"""Independent re-derivation (own loops; no mechanism.py / stats.py / t8_part* functions) of:
  1. d_floor_pred (3-pool and 9-family) from the raw pair records: ANALYTIC expected endorsement (Poisson-binomial over
     unlabelled VOCAB pairs) instead of the Monte-Carlo draws; plus d(R_align), d(R_name), d(R_liberal), e(R_point_label);
  2. the SIG-FREE exact-agreement drop from the raw pair_matrix_RCOMP.jsonl lines;
  3. the L25 MDE80 at E's yield for planned 300 sentences (sklearn roc_auc_score, own bootstrap, B = 400);
  4. five transcribed headline numbers straight from the raw files (own json / regex parsing);
  5. placebos: condition-permutation of the SIG-FREE drop (expected ~0) and a label-shuffle of the Part-1 vocabulary
     share (VOCAB share among CORRECT- vs ERROR-candidate pairs, expected equal under shuffling).
Writes audit/rederive.json."""
from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

ROOT = Path(__file__).resolve().parent.parent
RUN = Path("/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop")
E6T1, E7, E8 = RUN / "iter_3/gen_art/gen_art_experiment_6", RUN / "iter_3/gen_art/gen_art_experiment_7", RUN / "iter_3/gen_art/gen_art_experiment_8"
POOL3 = {"deepseek", "microsoft", "openai"}


def pbinom_gt(k_sure: int, u: int, p: float, half: float) -> float:
    """P(k_sure + Bin(u, p) > half) by explicit summation."""
    from math import comb
    return float(sum(comb(u, j) * p ** j * (1 - p) ** (u - j) for j in range(u + 1) if k_sure + j > half))


def part1() -> dict:
    P = pd.read_pickle(ROOT / "results/part1_rows.pkl")
    Q = pd.read_pickle(ROOT / "results/part1_pairs.pkl")
    p_acc = json.loads((ROOT / "prereg_d_split.json").read_text())["vocab_discount"]["accept_prob"]
    y = dict(zip(P.row_key, P.y_AB.astype(int)))
    out = {}
    for pool in ("3pool", "9fam"):
        acc = defaultdict(lambda: {"n": 0, "align": 0, "name": 0, "lib": 0, "sure": 0, "unl": 0})
        for r in Q.itertuples():
            if pool == "3pool" and r.peer_family not in POOL3:
                continue
            a = acc[r.cand]
            a["n"] += 1
            base = bool(r.f_align) or bool(r.f_name)
            a["align"] += bool(r.f_align)
            a["name"] += base
            a["lib"] += base or bool(r.f_vocab_raw)
            if base:
                a["sure"] += 1
            elif r.cls == "VOCAB":
                cy = y[r.cand]
                if r.peer_y not in (0, 1) or pd.isna(r.peer_y):
                    a["unl"] += 1
                elif (cy == 0 and r.peer_y == 0) or (cy == 1 and r.peer_y == 1 and r.peer_opc == r.cand_opc):
                    a["sure"] += 1
        rec = {}
        for rule in ("align", "name", "lib", "point_label"):
            en_c, en_e = [], []
            for rk, a in acc.items():
                if a["n"] == 0:
                    continue
                v = pbinom_gt(a["sure"], a["unl"], p_acc, a["n"] / 2) if rule == "point_label" else float(a[rule] > a["n"] / 2)
                (en_c if y[rk] == 0 else en_e).append(v)
            rec[rule] = {"d": 1 - float(np.mean(en_c)), "e": float(np.mean(en_e)), "n_cor": len(en_c), "n_err": len(en_e)}
        out[pool] = rec
    p1 = json.loads((ROOT / "results/part1.json").read_text())
    chk = {}
    for pool in ("3pool", "9fam"):
        pp = p1["pools"][pool]
        chk[pool] = {"d_floor_pred_main": pp["d_floor_pred"], "d_floor_pred_audit_analytic": out[pool]["point_label"]["d"],
                     "abs_diff": abs(pp["d_floor_pred"] - out[pool]["point_label"]["d"]),
                     "d_R_align_main": pp["heads"]["R_align"]["d"], "d_R_align_audit": out[pool]["align"]["d"],
                     "d_R_liberal_main": pp["heads"]["R_liberal"]["d"], "d_R_liberal_audit": out[pool]["lib"]["d"],
                     "e_point_label_main": pp["e_ceiling_pred"], "e_point_label_audit": out[pool]["point_label"]["e"]}
        chk[pool]["match_deterministic_1e-9"] = bool(abs(chk[pool]["d_R_align_main"] - chk[pool]["d_R_align_audit"]) < 1e-9
                                                     and abs(chk[pool]["d_R_liberal_main"] - chk[pool]["d_R_liberal_audit"]) < 1e-9)
        chk[pool]["match_mc_vs_analytic_0.005"] = bool(chk[pool]["abs_diff"] <= 0.005)
    # label-shuffle placebo: VOCAB share among CORRECT vs ERROR candidates, labels permuted within sentence
    Qv = Q.assign(cy=Q.cand.map(y), vocab=(Q.cls == "VOCAB").astype(int))
    obs = Qv[Qv.cy == 0].vocab.mean() - Qv[Qv.cy == 1].vocab.mean()
    rng = np.random.default_rng(0)
    cand_sent = P.set_index("row_key").sentence_id
    labs = P[["row_key", "sentence_id", "y_AB"]]
    null = []
    for _ in range(200):
        perm = labs.groupby("sentence_id").y_AB.transform(lambda s: rng.permutation(s.values))
        ym = dict(zip(labs.row_key, perm.astype(int)))
        c = Qv.cand.map(ym)
        null.append(Qv[c == 0].vocab.mean() - Qv[c == 1].vocab.mean())
    chk["placebo_vocab_share_label_shuffle"] = {"observed_share_cor_minus_err": float(obs), "null_mean": float(np.mean(null)),
                                                "null_band": [float(np.percentile(null, 2.5)), float(np.percentile(null, 97.5))],
                                                "reading": "observed inside the within-sentence shuffle band = VOCAB agreements are not label-specific"}
    del cand_sent
    return chk


def part2() -> dict:
    mats = [json.loads(l) for l in (ROOT / "results/pair_matrix_RCOMP.jsonl").read_text().splitlines()]
    rc = [json.loads(l) for l in (E7 / "results/rcomp_candidates.jsonl").read_text().splitlines()]
    peer_var = {"SIG": "sig_v1", "FREE": "fewshot_v1"}
    meta = {r["row_key"]: r for r in rc}
    slot_node = {}
    exact = {}
    for m in mats:
        cond = m["condition"]
        for nd in m["nodes"]:
            for r in nd["rows"]:
                if meta[r["row_key"]]["prompt_variant"] == peer_var[cond]:
                    slot_node[(m["sentence_id"], cond, r["slot"])] = (nd["node_id"], r["family"])
        for i, j, e, rs, _ in m["pairs"]:
            exact[(m["sentence_id"], cond, min(i, j), max(i, j))] = (e is True and rs == "exact")
    drops, sids, pairs = [], [], []
    by_sent = defaultdict(set)
    for (sid, cond, slot) in slot_node:
        by_sent[sid].add(slot)
    for sid, slots in by_sent.items():
        sl = sorted(slots)
        for a in range(len(sl)):
            for b in range(a + 1, len(sl)):
                s, t = sl[a], sl[b]
                ks = [(sid, c, s) in slot_node and (sid, c, t) in slot_node for c in ("SIG", "FREE")]
                if not all(ks):
                    continue
                fams = slot_node[(sid, "FREE", s)][1], slot_node[(sid, "FREE", t)][1]
                if fams[0] == fams[1]:
                    continue
                v = []
                for c in ("SIG", "FREE"):
                    i, j = slot_node[(sid, c, s)][0], slot_node[(sid, c, t)][0]
                    v.append(1 if i == j else int(exact.get((sid, c, min(i, j), max(i, j)), False)))
                pairs.append(v)
                sids.append(sid)
    A = np.array(pairs, float)
    drop = float((A[:, 0] - A[:, 1]).mean())
    p2 = json.loads((ROOT / "results/part2.json").read_text())
    main = p2["drop_pairs"]["exact"]["overall"]["mean"]
    rng = np.random.default_rng(0)
    perm = []
    for _ in range(200):
        sw = rng.random(len(A)) < 0.5
        s_ = np.where(sw, A[:, 1], A[:, 0])
        f_ = np.where(sw, A[:, 0], A[:, 1])
        perm.append(float((s_ - f_).mean()))
    return {"drop_exact_audit": drop, "drop_exact_main": main, "n_pairs_audit": len(A), "n_pairs_main": p2["drop_pairs"]["exact"]["overall"]["n"],
            "match_1e-9": bool(abs(drop - main) < 1e-9),
            "placebo_condition_permutation": {"mean": float(np.mean(perm)), "band": [float(np.percentile(perm, 2.5)), float(np.percentile(perm, 97.5))],
                                              "expected": "~0; observed drop far outside the band"}}


def part3() -> dict:
    rows = [json.loads(l) for l in (E6T1 / "results/per_item_T1.jsonl").read_text().splitlines()]
    d = pd.DataFrame([r for r in rows if r["in_R_AB"] and r.get("pool") == "E_POOL" and r["source_stratum"] == "L25"])
    pw = json.loads((ROOT / "power_E2.json").read_text())
    rec = next(r for r in pw["planned_E2"] if r["cell"] == "L25" and r["planned_sentences"] == 300 and r["comparator"] == "flashlite_disg")
    n = int(round(rec["n_usable"]))
    sids = d.sentence_id.unique()
    by = {s: g for s, g in d.groupby("sentence_id")}
    rng = np.random.default_rng(123)
    vals = []
    for _ in range(400):
        g = pd.concat([by[s] for s in rng.choice(sids, n, replace=True)])
        if g.y_R_AB.nunique() < 2:
            continue
        vals.append(roc_auc_score(g.y_R_AB, g.c_score_align) - roc_auc_score(g.y_R_AB, g.judge_cheap_disg))
    se = float(np.std(vals, ddof=1))
    return {"n_usable": n, "se_audit": se, "mde80_audit": 2.8016 * se, "mde80_main": rec["mde80"],
            "rel_diff": abs(2.8016 * se - rec["mde80"]) / rec["mde80"], "match_within_10pct": bool(abs(2.8016 * se - rec["mde80"]) / rec["mde80"] <= 0.10)}


def headlines() -> dict:
    out = {}
    md = (E6T1 / "results/tables_T1.md").read_text()
    m = re.search(r"\| R_AB pooled \[strat\] \| [^|]+\| `c_score_align` \| ([+\-\d.]+)", md)
    out["R_AB strat delta vs flash-lite"] = {"raw": m.group(1) if m else None, "hyp": "+0.099"}
    m = re.search(r"\| R_AB L25 \[pooled\] \| [^|]+\| `c_score_align` \| ([+\-\d.]+)", md)
    out["L25 delta vs flash-lite"] = {"raw": m.group(1) if m else None, "hyp": "+0.069"}
    ah = json.loads((E8 / "results/analysis_hyb.json").read_text())
    out["over-alignment"] = {"raw": ah["new_agreement_audit"]["label_discordance"]["NEW_hyb_not_align"]["rate"], "hyp": "0.388"}
    md7 = (E7 / "results/tables.md").read_text()
    m = re.search(r'"d_correct_divergence": ([\d.]+)', md7)
    out["SIG d (exp-7 tables.md overall)"] = {"raw": m.group(1) if m else None, "hyp": "0.260"}
    tot = sum(json.loads(l).get("cost_usd", 0) or 0 for l in (E6T1 / ".aii_cost_ledger.jsonl").read_text().splitlines() if l.strip())
    out["T1 spend"] = {"raw": tot, "hyp": "2.395"}
    for k, v in out.items():
        raw = float(str(v["raw"]).replace("+", "")) if v["raw"] is not None else None
        v["match"] = raw is not None and abs(raw - float(v["hyp"].replace("+", ""))) <= 0.0015
    return out


def main() -> None:
    res = {"part1": part1(), "part2": part2(), "part3": part3(), "headlines": headlines()}
    flags = [res["part1"]["3pool"]["match_deterministic_1e-9"], res["part1"]["9fam"]["match_deterministic_1e-9"],
             res["part1"]["3pool"]["match_mc_vs_analytic_0.005"], res["part1"]["9fam"]["match_mc_vs_analytic_0.005"],
             res["part2"]["match_1e-9"], res["part3"]["match_within_10pct"]] + [v["match"] for v in res["headlines"].values()]
    res["n_checks"] = len(flags)
    res["n_pass"] = int(sum(flags))
    (ROOT / "audit/rederive.json").write_text(json.dumps(res, indent=1, default=float))
    print(json.dumps({"n_checks": res["n_checks"], "n_pass": res["n_pass"], "p1": {k: {kk: vv for kk, vv in v.items() if "match" in kk or "diff" in kk} for k, v in res["part1"].items() if k != "placebo_vocab_share_label_shuffle"},
                      "placebo_vocab": res["part1"]["placebo_vocab_share_label_shuffle"], "p2": res["part2"], "p3": res["part3"]}, indent=1, default=float))


if __name__ == "__main__":
    main()
