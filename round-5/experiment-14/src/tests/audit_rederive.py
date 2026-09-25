#!/usr/bin/env python3
# NOTE (published copy): this file names server paths this repository
# does not publish (a stage it does not ship, or another run's workspace),
# so the steps that read them will not run from a clone as written:
#   /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6/results/per_item_T1.jsonl
"""Independent re-derivation of the headline numbers from RAW files with a separate code path (plain json + sklearn
roc_auc_score; nothing imported from src/ or freeze/): (1) Part A: V0 and every variant's LONG-strat / L25 / CTRL AUROC and
the rule decision; (2) GG gates g1/g2 from scores_gg_perturb.jsonl and g3 from scores_gg_E.jsonl; (3) shuffled-label
placebo (must be ~0.5). Writes results/audit_rederive.json."""
import json
from pathlib import Path

import numpy as np
from sklearn.metrics import roc_auc_score

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "results"
PER = Path("/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6/results/per_item_T1.jsonl")


def rd(p):
    return [json.loads(l) for l in Path(p).read_text().splitlines() if l.strip()]


def strat(y, s, h):
    num = den = 0.0
    for g in sorted(set(h)):
        m = h == g
        n1, n0 = int(y[m].sum()), int((1 - y[m]).sum())
        if n1 and n0:
            num += roc_auc_score(y[m], s[m]) * n1 * n0
            den += n1 * n0
    return num / den


def main():
    lab = {r["canonical_key"]: r for r in rd(PER)}
    sc = {r["canonical_key"]: r for r in rd(RES / "scores_E_variants.jsonl")}
    v4 = {r["row_key"]: r["V4"] for r in rd(RES / "scores_E_V4.jsonl")}
    Z = [k for k, r in lab.items() if r["in_R_AB"] and r["pool"] == "E_POOL" and r["parse_ok"] and sc[k]["in_matrix"] and sc[k]["n_peers"] >= 2]
    y = np.array([lab[k]["y_R_AB"] for k in Z], int)
    h = np.array([lab[k]["source_stratum"] for k in Z])
    cols = {"V0": np.array([lab[k]["c_score_align"] for k in Z], float)}
    for v in ("V1", "V2", "V3", "V5"):
        cols[v] = np.array([sc[k][v] for k in Z], float)
    cols["V4"] = np.array([v4[sc[k]["row_key"]] for k in Z], float)
    L = np.isin(h, ["L25", "L20", "EXC"])
    stats = {v: {"LONG": strat(y[L], s[L], h[L]), "L25": roc_auc_score(y[h == "L25"], s[h == "L25"]),
                 "CTRL": roc_auc_score(y[h == "CTRL"], s[h == "CTRL"])} for v, s in cols.items()}
    q = [v for v in ("V1", "V2", "V3", "V4", "V5") if stats[v]["LONG"] - stats["V0"]["LONG"] >= 0.015
         and stats[v]["L25"] >= stats["V0"]["L25"] and stats[v]["CTRL"] >= stats["V0"]["CTRL"] - 0.01]
    decision = max(q, key=lambda v: stats[v]["LONG"]) if q else "NONE: V0 stands"
    sel = json.loads((ROOT / "freeze" / "selection.json").read_text())
    best = max(("V1", "V2", "V3", "V4", "V5"), key=lambda v: stats[v]["LONG"])
    A = {"n_Z": len(Z), "stats": stats, "decision": decision, "frozen_decision": sel["winner"], "decision_match": decision == sel["winner"],
         "best_variant_long": best, "best_delta_long": stats[best]["LONG"] - stats["V0"]["LONG"],
         "frozen_best_delta_long": sel["qualification"][best]["delta_long"],
         "delta_match_1e-9": abs(stats[best]["LONG"] - stats["V0"]["LONG"] - sel["qualification"][best]["delta_long"]) < 1e-9}
    # GG
    T = rd(RES / "scores_gg_perturb.jsonl")
    base = {r["base"]: r for r in T if r["kind"] == "BASE"}
    syn = [r for r in T if r["kind"] == "RENAME_SYN" and r["c_gg"] is not None and r["base"] in base and base[r["base"]]["c_gg"] is not None]
    flip = np.mean([(r["c_gg"] > 0.5) != (base[r["base"]]["c_gg"] > 0.5) for r in syn])
    fa = np.mean([r["c_gg"] > 0.5 for r in syn])
    fab = np.mean([base[r["base"]]["c_gg"] > 0.5 for r in syn])
    mr = [r for r in T if r["kind"] == "MEANING_RENAME" and r["c_gg"] is not None and r["c_align"] is not None]
    rec_gg, rec_al = np.mean([r["c_gg"] > 0.5 for r in mr]), np.mean([r["c_align"] > 0.5 for r in mr])
    G = {r["row_key"]: r for r in rd(RES / "scores_gg_E.jsonl")}
    cg = np.array([G[sc[k]["row_key"]]["c_gg"] for k in Z], float)
    g3 = strat(y, cg, h) - strat(y, cols["V0"], h)
    D = json.loads((RES / "gg_dev.json").read_text())["gates"]
    A["gg"] = {"g1_flip": flip, "g1_FA": fa, "g1_FA_base": fab, "g2_recall_gg": rec_gg, "g2_recall_align": rec_al, "g3_delta": g3,
               "match": bool(abs(flip - D["g1"]["paired_flip"]) < 1e-9 and abs(fa - D["g1"]["FA_SYN"]) < 1e-9 and abs(rec_gg - D["g2"]["recall_gg"]) < 1e-9
                             and abs(g3 - (D["g3"]["gg"] - D["g3"]["V0"])) < 1e-9)}
    rng = np.random.default_rng(0)
    ys = y.copy()
    for g in set(h):
        m = np.where(h == g)[0]
        ys[m] = rng.permutation(y[m])
    A["placebo_shuffled_within_stratum"] = {v: strat(ys, s, h) for v, s in {**cols, "c_gg": cg}.items()}
    A["placebo_ok"] = all(abs(v - 0.5) < 0.05 for v in A["placebo_shuffled_within_stratum"].values())
    (RES / "audit_rederive.json").write_text(json.dumps(A, indent=1, default=float))
    print(json.dumps({k: A[k] for k in ("decision", "decision_match", "best_variant_long", "best_delta_long", "delta_match_1e-9", "placebo_ok")}),
          json.dumps(A["gg"]), json.dumps(A["placebo_shuffled_within_stratum"]))


if __name__ == "__main__":
    main()
