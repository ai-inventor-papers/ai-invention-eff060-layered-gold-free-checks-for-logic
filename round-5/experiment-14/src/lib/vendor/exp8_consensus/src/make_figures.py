#!/usr/bin/env python3
"""Figures (matplotlib, deterministic from results/*.csv) + JSON figure specs (results/figures/*.json):
  fig_tradeoff.png          invariance/sensitivity trade-off per metric: x = RENAME_SYN (and RENAME_NONCE) FA at the PRIMARY
                            threshold, y = MEANING_RENAME recall (E bases); a good metric sits top-left.
  fig_recall_heatmap.png    recall at the PRIMARY threshold, operator x metric (E bases, both polarities pooled).
  fig_wbauroc_heatmap.png   within-base AUROC (mutants vs same-base meaning-preserving controls), operator x metric.
  fig_downup.png            DOWN - UP paired detection difference with base-clustered 95% CI per metric (all operators).
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
R = ROOT / "results"
F = R / "figures"
F.mkdir(exist_ok=True)
OPS = ["NEG", "REV", "QUANT", "RESTR", "CONN", "DROP", "ADD", "SWAP", "BIND", "MEANING_RENAME"]
SHOW = ["c_align", "c_nf", "c_hyb", "g_align", "g_hyb", "p_peer_text", "p_text", "l2_bow", "l3_z3", "sc5_local_eq_frac",
        "rt_nli_min_local", "rt_embed_cos_local", "judge_local_qwen8b_disg", "judge_local_llama8b_disg", "judge_cheap_disg",
        "S4_local", "pilot_joint_conflict", "parse_fail"]


def fl(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return np.nan


def main():
    sens = list(csv.DictReader((R / "perturb_sensitivity.csv").open()))
    to = list(csv.DictReader((R / "tradeoff.csv").open()))
    du = list(csv.DictReader((R / "perturb_downup.csv").open()))
    mets = [m for m in SHOW if any(r["metric"] == m for r in sens)]
    # ---- trade-off
    pts = [r for r in to if r["subset"] == "E_bases" and r["metric"] in mets]
    fig, ax = plt.subplots(figsize=(7.5, 5.5))
    for r in pts:
        x1, x2, y = fl(r["RENAME_SYN_FA"]), fl(r["RENAME_NONCE_FA"]), fl(r["MEANING_RENAME_recall"])
        ax.scatter([x1], [y], marker="o", color="C0")
        ax.scatter([x2], [y], marker="x", color="C3")
        ax.plot([x1, x2], [y, y], color="grey", lw=0.5)
        ax.annotate(r["metric"], (x1, y), fontsize=7, xytext=(3, 3), textcoords="offset points")
    ax.set_xlabel("rename false-alarm rate on CORRECT controls (o = RENAME_SYN, x = RENAME_NONCE)")
    ax.set_ylabel("MEANING_RENAME recall (E bases)")
    ax.set_title("Invariance vs sensitivity at the E-derived FA-0.10 threshold (top-left is better)")
    ax.set_xlim(-0.03, 1.03)
    ax.set_ylim(-0.03, 1.03)
    fig.tight_layout()
    fig.savefig(F / "fig_tradeoff.png", dpi=160)
    plt.close(fig)
    # ---- heatmaps
    for col, fname, title in (("recall_primary", "fig_recall_heatmap.png", "Recall at the E-derived FA-0.10 threshold"),
                              ("within_base_auroc", "fig_wbauroc_heatmap.png", "Within-base AUROC (mutants vs same-base controls)")):
        M = np.full((len(mets), len(OPS)), np.nan)
        for i, m in enumerate(mets):
            for j, op in enumerate(OPS):
                r = next((r for r in sens if r["metric"] == m and r["operator"] == op and r["polarity"] == "ALL" and r["subset"] == "E_bases"), None)
                if r:
                    M[i, j] = fl(r.get(col))
        fig, ax = plt.subplots(figsize=(9, 0.38 * len(mets) + 1.5))
        im = ax.imshow(M, cmap="viridis", vmin=0 if col == "recall_primary" else 0.4, vmax=1, aspect="auto")
        ax.set_xticks(range(len(OPS)), OPS, rotation=45, ha="right", fontsize=8)
        ax.set_yticks(range(len(mets)), mets, fontsize=8)
        for i in range(len(mets)):
            for j in range(len(OPS)):
                if not np.isnan(M[i, j]):
                    ax.text(j, i, f"{M[i, j]:.2f}", ha="center", va="center", fontsize=6, color="w" if M[i, j] < 0.75 else "k")
        fig.colorbar(im, ax=ax)
        ax.set_title(title + " (PERTURB, E bases, synthetic -- not real-error AUROC)", fontsize=9)
        fig.tight_layout()
        fig.savefig(F / fname, dpi=160)
        plt.close(fig)
        json.dump({"type": "heatmap", "rows": mets, "cols": OPS, "values": [[None if np.isnan(v) else v for v in row] for row in M],
                   "source": "results/perturb_sensitivity.csv", "column": col, "subset": "E_bases", "polarity": "ALL"},
                  (F / fname.replace(".png", ".json")).open("w"), indent=1)
    # ---- DOWN - UP
    rows = [r for r in du if r["operator"] == "ALL" and r["metric"] in mets]
    fig, ax = plt.subplots(figsize=(6.5, 0.32 * len(rows) + 1.2))
    for i, r in enumerate(rows):
        d, lo, hi = fl(r["diff_DOWN_minus_UP"]), fl(r["ci_lo"]), fl(r["ci_hi"])
        ax.errorbar([d], [i], xerr=[[d - lo], [hi - d]], fmt="o", color="C0", ms=4)
    ax.axvline(0, color="k", lw=0.8)
    ax.axvspan(-0.05, 0.05, color="grey", alpha=0.15)
    ax.set_yticks(range(len(rows)), [r["metric"] for r in rows], fontsize=8)
    ax.set_xlabel("recall(DOWN) - recall(UP) on matched pairs (base-clustered 95% CI)")
    ax.set_title("Polarity asymmetry (grey band = pre-registered symmetric |diff| < 0.05)", fontsize=9)
    fig.tight_layout()
    fig.savefig(F / "fig_downup.png", dpi=160)
    plt.close(fig)
    json.dump({"type": "scatter", "x": "RENAME_SYN_FA / RENAME_NONCE_FA", "y": "MEANING_RENAME_recall", "points": pts,
               "source": "results/tradeoff.csv"}, (F / "fig_tradeoff.json").open("w"), indent=1)
    json.dump({"type": "forest", "rows": rows, "source": "results/perturb_downup.csv"}, (F / "fig_downup.json").open("w"), indent=1)
    print("figures written", sorted(p.name for p in F.iterdir()))


if __name__ == "__main__":
    main()
