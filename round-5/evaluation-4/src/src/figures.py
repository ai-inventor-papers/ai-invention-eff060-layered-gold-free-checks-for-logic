"""Figures F1-F4, drawn only from numbers.csv rows (asserted), with the aii-data-fig-gen house style.
Hand-written matplotlib because the forest generator takes symmetric errors and our CIs are
asymmetric (copied verbatim). Each figure writes <name>.pdf, <name>.png and <name>.json (the plotted
values with their numbers.csv ids and a '# source:' caption line)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from src import io_locators as L
from src.claims_spec import EV2, CU
from src.ctx import Ctx

SK = "/ai-inventor/.claude/skills/aii-data-fig-gen/scripts"
if SK not in sys.path:
    sys.path.insert(0, SK)
import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from chart_style import (PALETTE, apply_house_style, clear_legends_of_data, fit_legends, fit_tick_labels,  # noqa: E402
                         fit_titles, place_legend)


def _val(c: Ctx, i: str) -> float:
    v = c.r[i]["source_value_raw"]
    c.used.add(i)
    return float(v)


def _ci(c: Ctx, i: str) -> list[float]:
    ci = c.r[i]["source_ci_raw"]
    assert ci is not None, f"{i} has no CI"
    return [float(ci[0]), float(ci[1])]


def _finish(fig, out: Path, spec: dict) -> None:
    fit_legends(fig)
    clear_legends_of_data(fig)
    fit_tick_labels(fig)
    fit_titles(fig)
    clear_legends_of_data(fig)
    fig.savefig(out.with_suffix(".pdf"))
    fig.savefig(out.with_suffix(".png"), dpi=200)
    plt.close(fig)
    out.with_suffix(".json").write_text(json.dumps(spec, indent=1))


def f1(c: Ctx, out: Path) -> dict:
    rows = [("pooled (R_AB, strat)", "t1_delta"), ("long pool L25+L20+EXC", "t1_long"), ("L25", "t1_l25"),
            ("L20", "t1_l20"), ("EXC", "t1_exc"), ("CTRL", "t1_ctrl")]
    fig, ax = plt.subplots(figsize=(7, 3.6), layout="constrained")
    data = []
    for k, (lab, i) in enumerate(rows[::-1]):
        v = _val(c, i)
        if c.r[i].get("source_ci_raw") is None and i == "t1_exc":
            ci = L.json_key(f"{L.I3}/gen_art_experiment_6/results/analysis_T1.json", "a_head_on.R_AB EXC.deltas.c_score_align - judge_cheap_disg [pooled].ci")[0]
            c.add("t1_exc_ci_lo", ci[0], "0.000", "analysis_T1.json :: a_head_on.R_AB EXC...ci[0]", "EXC CI lo")
            c.add("t1_exc_ci_hi", ci[1], "0.000", "analysis_T1.json :: a_head_on.R_AB EXC...ci[1]", "EXC CI hi")
        else:
            ci = _ci(c, i)
        ax.errorbar([v], [k], xerr=[[v - ci[0]], [ci[1] - v]], fmt="o", color=PALETTE[0], capsize=3)
        data.append(dict(label=lab, id=i, value=v, ci=ci))
    ax.axvline(0, color="#999999", linestyle="--", linewidth=1)
    ax.set_yticks(range(len(rows)), [r[0] for r in rows[::-1]])
    ax.set_xlabel("Δ strat AUROC, c_score_align − flash-lite disguised")
    ax.set_title("DEVELOPMENT (E): consensus vs cheap judge by stratum")
    spec = {"figure": "F1", "caption": "Development-set (E) Δ strat AUROC with 95% sentence-cluster bootstrap CIs (B = 2000) copied verbatim; L25 and CTRL CIs cover 0 (n.s.). Pooled/long are within-stratum AUROC; single strata are pooled within the stratum.",
            "source": "# source: /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6/results/analysis_T1.json a_head_on.*.deltas", "data": data}
    _finish(fig, out, spec)
    return spec


def f2(c: Ctx, out: Path) -> dict:
    cls = [("ADD", "ADD"), ("DROP", "DROP"), ("COMPOUND", "COMPOUND"), ("MR-type", "MR"), ("structural", "STRUCT"), ("polarity", "POL")]
    arms = [("FREE exact", "FREE_exact"), ("FREE ALIGN", "FREE_align"), ("CSC", "CSC")]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7, 3.4), layout="constrained", gridspec_kw={"width_ratios": [2.2, 1]})
    data = {"e_by_class_PRIMARY": [], "d_pooled": []}
    for j, (lab, arm) in enumerate(arms):
        ys = [_val(c, f"x9_t9_{k}_{arm}") for _, k in cls]
        a1.plot([x + (j - 1) * 0.18 for x in range(len(cls))], ys, "o", color=PALETTE[j], label=lab)
        data["e_by_class_PRIMARY"].append(dict(arm=lab, ids=[f"x9_t9_{k}_{arm}" for _, k in cls], values=ys))
    a1.set_xticks(range(len(cls)), [n for n, _ in cls])
    a1.set_ylabel("e (errors endorsed)")
    a1.set_title("e by error class (PRIMARY)")
    place_legend(a1, loc="upper left")
    bars = [("exact·F", "x9_full_d_fx"), ("ALIGN·F", "x9_full_d_fa"), ("exact·P", "x9_d_fx"), ("CSC·P", "x9_d_csc")]
    vals = [_val(c, i) for _, i in bars]
    a2.bar(range(len(bars)), vals, color=[PALETTE[0], PALETTE[1], PALETTE[0], PALETTE[2]])
    a2.set_xticks(range(len(bars)), [b for b, _ in bars])
    a2.set_ylabel("d (CORRECT rows flagged)")
    a2.set_title("d (F = FULL, P = PRIMARY)")
    data["d_pooled"] = [dict(label=b, id=i, value=v) for (b, i), v in zip(bars, vals)]
    fig.suptitle("Every vocabulary bridge trades d for e (DEVELOPMENT E)")
    spec = {"figure": "F2", "caption": "Left: share of real errors endorsed (e) per class on the completion-selected PRIMARY subset for the same 3 free peers scored exactly, with ALIGN, and for CSC-cued peers. Right: correct-row divergence d, FULL population (exact vs ALIGN) and PRIMARY (exact vs CSC); PRIMARY and FULL are different populations.",
            "source": "# source: /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_9/results/analysis.json e_anchoring_by_error_class.PRIMARY, a_ed_FULL.cells.R_AB, a_ed_PRIMARY.cells.R_AB", "data": data}
    _finish(fig, out, spec)
    return spec


def f3(c: Ctx, out: Path) -> dict:
    cls = [("IRREDUCIBLE", "e3_irr"), ("EXACT", "e3_exact"), ("ALIGN_ONLY", "e3_align"), ("VOCAB", "e3_vocab"), ("NAME_ONLY", "e3_name")]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7, 3.2), layout="constrained", gridspec_kw={"width_ratios": [1.3, 1]})
    left = 0.0
    vals = []
    for j, (n, i) in enumerate(cls):
        v = _val(c, i)
        a1.barh([0], [v], left=left, height=0.6, color=PALETTE[j], label=n)
        left += v
        vals.append(v)
    a1.set_yticks([0], ["9-family pairs"])
    a1.set_xlabel("share of (candidate, peer) pairs")
    a1.set_title("Pair classes")
    a1.set_ylim(-0.5, 1.6)
    a1.legend(loc="upper center", ncol=3, frameon=False, fontsize="small")
    b = [("9-family", "e3_77"), ("3-pool", "e3_61")]
    bv = [_val(c, i) for _, i in b]
    a2.bar(range(2), bv, color=[PALETTE[0], PALETTE[1]])
    a2.set_xticks(range(2), [x for x, _ in b])
    a2.set_ylim(0, 1)
    a2.set_ylabel("share labelled ERROR")
    a2.set_title("Non-agreeing peers of CORRECT candidates")
    fig.suptitle("Wrong peers, not words (DEVELOPMENT E)")
    spec = {"figure": "F3", "caption": "Left: eval-3 pair classes over all 9-family (candidate, peer) pairs. Right: among peers that disagree with a CORRECT candidate, the share that are themselves labelled ERROR.",
            "source": "# source: /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/tables/p1_class_shares.csv",
            "data": {"pair_classes": [dict(label=n, id=i, value=v) for (n, i), v in zip(cls, vals)], "peer_error_share": [dict(label=x, id=i, value=v) for (x, i), v in zip(b, bv)]}}
    _finish(fig, out, spec)
    return spec


def f4(c: Ctx, out: Path) -> dict:
    ks = [1, 2, 3, 4, 5, 6, 7]
    fig, ax = plt.subplots(figsize=(7, 3.8), layout="constrained")
    series = [("overall", "ev2_k{k}"), ("words T1", "ev2_k{k}_T1"), ("words T2", "ev2_k{k}_T2"), ("words T3 (long)", "ev2_k{k}_T3")]
    data = []
    for j, (lab, pat) in enumerate(series):
        ys = [_val(c, pat.format(k=k)) for k in ks]
        ax.plot(ks, ys, marker="o", color=PALETTE[j], label=lab)
        data.append(dict(label=lab, ids=[pat.format(k=k) for k in ks], values=ys))
    k95 = int(_val(c, "ev2_k95"))
    k95l = int(_val(c, "ev2_k95_t3"))
    ax.axvline(k95, color=PALETTE[0], linestyle=":", linewidth=1)
    ax.axvline(k95l, color=PALETTE[3], linestyle=":", linewidth=1)
    ax.set_xlabel("peer families k")
    ax.set_ylabel("AUROC (random k-subsets)")
    ax.set_title(f"k-curve: k95 = {k95} overall, {k95l} in the long tercile (DEVELOPMENT E)")
    place_legend(ax, loc="lower right")
    costs = [_val(c, f"cost_k{k}") for k in ks]
    sec = ax.secondary_xaxis("top", functions=(lambda x: x, lambda x: x))
    sec.set_xticks(ks, [f"{v * 1000:.2f}" for v in costs])
    sec.set_xlabel("FULL $ per sentence (×10⁻³)")
    spec = {"figure": "F4", "caption": "AUROC of consensus over random k-family pools on E rows with all 7 other families; dotted lines mark k95 overall and for the longest words tercile. Top axis: FULL peer-generation cost per SENTENCE.",
            "source": f"# source: {EV2}/results/part_a.json M4.random_k_primary; {CU}", "data": data, "k95": k95, "k95_long": k95l,
            "cost_ids": [f"cost_k{k}" for k in ks], "cost_usd_per_sentence": costs}
    _finish(fig, out, spec)
    return spec


def make_figures(c: Ctx, out_dir: Path) -> dict:
    out_dir.mkdir(exist_ok=True)
    apply_house_style()
    specs = {}
    for name, fn in (("F1_forest_dev", f1), ("F2_bridge_trades_d_for_e", f2), ("F3_wrong_peer_decomposition", f3), ("F4_k_curve_cost", f4)):
        specs[name] = fn(c, out_dir / name)
    # every plotted value came from numbers.csv (asserted: _val reads c.r only; spot-check equality with rows)
    for s in specs.values():
        for d in (s["data"] if isinstance(s["data"], list) else [x for v in s["data"].values() for x in v]):
            if "id" in d:
                assert abs(float(c.r[d["id"]]["source_value_raw"]) - d["value"]) < 1e-12
            for i, v in zip(d.get("ids", []), d.get("values", [])):
                assert abs(float(c.r[i]["source_value_raw"]) - v) < 1e-12
    return {k: str(out_dir / k) for k in specs}
