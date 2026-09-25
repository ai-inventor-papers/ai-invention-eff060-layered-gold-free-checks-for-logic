"""Independent re-derivation (separate code path: pandas groupby, no helper shared with src/csc_analysis.py).

Recomputes from the raw per-row files and compares to the reported tables to 1e-9:
  * e per operator (ALL polarity) for every variant and base source      vs results/anchoring.csv
  * control FA and paired base FA / flip                                 vs results/controls_fa.csv
  * typing strict accuracy per target / base source (ALL)                vs results/typing_csc.csv
  * SIG e / d at c > 0.5                                                 vs results/rcomp_sig_csc.json
  * gate status (CSC arms absent -> UNTESTED)                            vs results/csc_gate_P.json
Plus a shuffled-label placebo: e of SIGPROXY_K3 on operator labels permuted within base is ~equal across operators.
Writes results/rederive.json; exits non-zero on any mismatch.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "results"
TOL = 1e-9
COLS = {"SIGPROXY_K3": "c_proxy", "SIGPROXY_K4": "c_proxy_k4", "SIGPROXY_graded": "c_proxy_graded",
        "FREE_c_align_exp8": "c_align_exp8", "FREE_c_hyb_exp8": "c_hyb_exp8", "FREE3_exact": "c_free3_exact",
        "FREE3_align": "c_free3_align", "FREE3_lc": "c_free3_lc", "JUDGE_flashlite_disg_exp8": "judge_cheap_disg_exp8",
        "LOCAL2_own_sig": "c_local", "LOCAL2_base_sig": "c_localbase", "LOCAL2_graded": "c_local_graded",
        "CSC_K3": "c_csc", "CSC_K4": "c_csc_k4", "CSC_multi": "c_csc_multi", "CSC_graded": "c_csc_graded"}


def main() -> int:
    df = pd.read_json(RES / "perturb_csc_scores.jsonl", lines=True)
    df["src"] = np.where(df["is_rcomp"], "RCOMP", "E")
    an = pd.read_csv(RES / "anchoring.csv")
    checks, bad = 0, []
    mut = df[df["fold"] == "PERTURB"]
    for v, col in COLS.items():
        if col not in df or df[col].notna().sum() == 0:
            continue
        m = mut[mut[col].notna()]
        g = (m[col] <= 0.5).groupby([m["op_label"], m["src"]]).mean()
        for (op, src), e in g.items():
            rep = an[(an.variant == v) & (an.op_label == op) & (an.polarity == "ALL") & (an.base_source == src)]
            checks += 1
            if len(rep) != 1 or abs(round(e, 3) - rep["e"].iloc[0]) > TOL:
                bad.append(("anchoring", v, op, src, e, rep["e"].tolist()))
    # controls
    cf = pd.read_csv(RES / "controls_fa.csv")
    base = df[df["fold"] == "BASE"].set_index("base_item_id")
    ctl = df[df["fold"] == "PERTURB_CONTROL"]
    for v, col in COLS.items():
        if col not in df or df[col].notna().sum() == 0:
            continue
        c = ctl[ctl[col].notna()].copy()
        c["bscore"] = c["base_item_id"].map(base[col])
        c = c[c["bscore"].notna()]
        c["f"] = (c[col] > 0.5).astype(float)
        c["fb"] = (c["bscore"] > 0.5).astype(float)
        for (ct, src), x in c.groupby(["op_label", "src"]):
            rep = cf[(cf.variant == v) & (cf.control_type == ct) & (cf.base_source == src)]
            checks += 3
            if len(rep) != 1:
                bad.append(("controls_missing", v, ct, src))
                continue
            for a, b in ((x["f"].mean(), "FA_gt05"), (x["fb"].mean(), "paired_base_FA"), ((x["f"] - x["fb"]).abs().mean(), "flip_rate")):
                if abs(round(a, 3) - rep[b].iloc[0]) > TOL:
                    bad.append(("controls", v, ct, src, b, a, rep[b].iloc[0]))
    # typing
    tr = pd.read_json(RES / "typing_rows_csc.jsonl", lines=True)
    tt = pd.read_csv(RES / "typing_csc.csv")
    tr["src"] = np.where(tr["is_rcomp"], "RCOMP", "E")
    for t in ("oracle", "proxy", "free3", "csc"):
        if f"{t}_pred" not in tr:
            continue
        x = tr[tr[f"{t}_pred"].notna()]
        for src, y in x.groupby("src"):
            acc = y[f"{t}_strict"].astype(bool).mean()
            rep = tt[(tt.target == t) & (tt.base_source == src) & (tt.true_op == "ALL")]
            checks += 1
            if len(rep) != 1 or abs(round(acc, 3) - rep["strict"].iloc[0]) > TOL:
                bad.append(("typing", t, src, acc, rep["strict"].tolist()))
    # SIG e/d
    sg = json.loads((RES / "rcomp_sig_csc.json").read_text())
    s = pd.read_json(RES / "csc_rcomp_sig_scores.jsonl", lines=True)
    s = s[s["label"].isin(["CORRECT", "ERROR"])]
    for m in ("c_proxy", "c_score_sig"):
        y = s[s[m].notna()]
        e = (y[y.label == "ERROR"][m] <= 0.5).mean()
        d = (y[y.label == "CORRECT"][m] > 0.5).mean()
        checks += 2
        if abs(round(e, 3) - sg["e_d_at_0.5"][m]["e_error_endorsed"]) > TOL or abs(round(d, 3) - sg["e_d_at_0.5"][m]["d_correct_flagged"]) > TOL:
            bad.append(("sig_e_d", m, e, d, sg["e_d_at_0.5"][m]))
    # gates
    g = json.loads((RES / "csc_gate_P.json").read_text())
    csc_present = "c_csc" in df and df["c_csc"].notna().any()
    checks += 1
    if not csc_present and not str(g["G3_P"]["verdict"]).startswith("UNTESTED"):
        bad.append(("gate", g["G3_P"]))
    # placebo
    rng = np.random.default_rng(0)
    m = mut[mut["c_proxy"].notna()].copy()
    m["perm"] = m.groupby("base_item_id")["op_label"].transform(lambda z: rng.permutation(z.values))
    plc = (m["c_proxy"] <= 0.5).groupby(m["perm"]).mean()
    out = {"n_checks": checks, "n_mismatch": len(bad), "mismatches": [list(map(str, b)) for b in bad[:20]],
           "placebo_sigproxy_e_by_permuted_op": {k: round(float(v), 4) for k, v in plc.items()},
           "placebo_spread": round(float(plc.max() - plc.min()), 4), "all_pass": not bad}
    (RES / "rederive.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1)[:1500])
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
