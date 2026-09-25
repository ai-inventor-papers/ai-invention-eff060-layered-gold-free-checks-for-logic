#!/usr/bin/env python3
"""Two figures (PDF + PNG + JSON spec): fig_d_floor_vs_words, fig_sig_vs_free_agreement. Every plotted number is read
from tables/p1_rule_cuts.csv, results/part2.json and tables/p2_slot_pairs.csv."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from t8_paths import FIG, RESD, TAB, jdump  # noqa: E402
from stats import SentBoot, ci  # noqa: E402

plt.rcParams.update({"font.size": 9, "pdf.fonttype": 42, "ps.fonttype": 42, "axes.spines.top": False, "axes.spines.right": False})
PAL = {"R_exact": "#7f7f7f", "R_align": "#0072B2", "R_point_label": "#D55E00", "R_liberal": "#E69F00", "R_oracle": "#009E73"}
LAB = {"R_exact": "R_exact (EXACT only)", "R_align": "R_align = END_MAJ", "R_point_label": "R_point_label (primary prediction)",
       "R_liberal": "R_liberal (every NF/HYB agreement)", "R_oracle": "R_oracle (no-anchoring floor)"}


def fig1() -> dict:
    T = pd.read_csv(TAB / "p1_rule_cuts.csv", comment="#")
    p2 = json.loads((RESD / "part2.json").read_text())
    weak = next(r["d"] for r in p2["SIG_d_by_reading"] if r["cell"] == "weak" and r["rule"] == "END_MAJ_align")
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.0), sharey=True)
    spec = {"figure": "fig_d_floor_vs_words", "sig_weak_reading_d": weak, "panels": {}}
    for ax, pool, title in zip(axes, ("9fam", "3pool"), ("All 9 vendor families (secondary)", "Matched 3-family pool (PRIMARY)")):
        spec["panels"][pool] = {}
        for k, rule in enumerate(PAL):
            s = T[(T.pool == pool) & (T.rule == rule) & (T.dim == "words_tercile")].sort_values("cell")
            x = np.arange(len(s)) + (k - 2) * 0.07
            yerr = np.vstack([s.d - s.d_ci_lo, s.d_ci_hi - s.d]) if rule in ("R_point_label", "R_align") else None
            ax.errorbar(x, s.d, yerr=yerr, marker="o", ms=4, lw=1.4, capsize=2, color=PAL[rule], label=LAB[rule])
            spec["panels"][pool][rule] = {"cells": s.cell.tolist(), "d": s.d.round(4).tolist(), "d_ci_lo": s.d_ci_lo.round(4).tolist(),
                                          "d_ci_hi": s.d_ci_hi.round(4).tolist(), "n_cor": s.n_cor.tolist()}
        ax.axhline(weak, ls="--", lw=1, color="k")
        ax.text(-0.15, weak + 0.02, f"SIG weak-reading d = {weak:.3f}", ha="left", fontsize=7)
        ax.set_xticks(range(3), ["T1 (≤20 words)", "T2 (21-26)", "T3 (>26)"])
        ax.set_title(title, fontsize=9)
        ax.set_ylim(0, 1)
    axes[0].set_ylabel("d = P(not endorsed | CORRECT)")
    axes[1].legend(fontsize=6.5, frameon=False, loc="lower right")
    fig.tight_layout()
    for ext in ("pdf", "png"):
        fig.savefig(FIG / f"fig_d_floor_vs_words.{ext}", dpi=200)
    plt.close(fig)
    spec["source"] = ["tables/p1_rule_cuts.csv (dim = words_tercile)", "results/part2.json :: SIG_d_by_reading"]
    return spec


def fig2() -> dict:
    PR = pd.read_csv(TAB / "p2_slot_pairs.csv")
    PR = PR[PR.sig_exact.notna()]
    cols = [("sig_exact", "SIG exact (shared vocabulary)", "#0072B2"), ("free_exact", "FREE exact", "#7f7f7f"),
            ("free_align", "FREE ALIGN (eqmv)", "#E69F00"), ("free_nf", "FREE NF", "#009E73")]
    tpls = sorted(PR.template_id.unique(), key=lambda t: int(t[1:]))
    fig, ax = plt.subplots(figsize=(7.2, 3.0))
    spec = {"figure": "fig_sig_vs_free_agreement", "templates": tpls, "series": {}}
    w = 0.2
    for k, (c, lab, col) in enumerate(cols):
        m, lo, hi = [], [], []
        for t in tpls:
            g = PR[PR.template_id == t]
            v = g[c].values.astype(float)
            W = SentBoot(g.sentence_id.values, b=1000, seed=0).W()
            b = ci((W @ v) / W.sum(1))
            m.append(v.mean())
            lo.append(b[0])
            hi.append(b[1])
        x = np.arange(len(tpls)) + (k - 1.5) * w
        ax.bar(x, m, w, color=col, label=lab, yerr=np.vstack([np.array(m) - lo, np.array(hi) - m]), capsize=1.5, error_kw={"lw": 0.7})
        spec["series"][c] = {"label": lab, "mean": np.round(m, 4).tolist(), "ci_lo": np.round(lo, 4).tolist(), "ci_hi": np.round(hi, 4).tolist()}
    ax.set_xticks(range(len(tpls)), tpls)
    ax.set_ylabel("cross-family pair agreement")
    ax.set_xlabel("R_COMP template (same sentences and slot pairs in both conditions)")
    ax.legend(fontsize=7, frameon=False, ncol=4, loc="upper center", bbox_to_anchor=(0.5, 1.15))
    ax.set_ylim(0, 1)
    fig.tight_layout()
    for ext in ("pdf", "png"):
        fig.savefig(FIG / f"fig_sig_vs_free_agreement.{ext}", dpi=200)
    plt.close(fig)
    spec["source"] = ["tables/p2_slot_pairs.csv (sentence-cluster bootstrap B = 1000)"]
    return spec


def main() -> None:
    FIG.mkdir(exist_ok=True)
    jdump(FIG / "fig_d_floor_vs_words.json", fig1())
    jdump(FIG / "fig_sig_vs_free_agreement.json", fig2())


if __name__ == "__main__":
    main()
