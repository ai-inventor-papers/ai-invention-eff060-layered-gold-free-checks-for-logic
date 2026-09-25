#!/usr/bin/env python3
"""Independent re-derivation of the headline numbers from the RAW files, using a different code path (stdlib + numpy
only; no import from confirm/, auc_tools or analysis_lib):
- results/scores_rcomp_free.jsonl (sealed scores) + results/rcomp_free_labels_final.jsonl (sealed labels);
- results/audit_rows.jsonl (raw auditor verdicts); results/judge_frontier_FREE.jsonl (raw frontier verdicts).
Recomputes the within-template AUROCs by brute-force pair counting and a simple sentence bootstrap (own implementation,
B=1000, sentences resampled within template, seed 7). It then repeats the provisional test on labels permuted within
template and checks that it FAILS (CI covers 0). Writes results/rederive_raw.json."""
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

WS = Path(__file__).resolve().parents[1]
R = WS / "results"


def jl(p):
    return [json.loads(l) for l in Path(p).read_text().splitlines() if l.strip()]


def auc_w(rows, key, w):
    """within-template AUROC; each row weighted by its sentence multiplicity w[sid] (pairs weighted by the product)."""
    by = defaultdict(lambda: ([], []))
    for r in rows:
        by[r["t"]][0 if r["y"] == 1 else 1].append((r[key], w.get(r["s"], 0)))
    U = P = 0.0
    for pos, neg in by.values():
        if not pos or not neg:
            continue
        nv = np.array([v for v, _ in neg])
        nw = np.array([ww for _, ww in neg], float)
        for v, ww in pos:
            if ww == 0:
                continue
            U += ww * (nw[nv < v].sum() + 0.5 * nw[nv == v].sum())
            P += ww * nw.sum()
    return U / P if P else float("nan")


def boot_delta(rows, a, b, B=1000, seed=7):
    rng = np.random.default_rng(seed)
    tpl = defaultdict(set)
    for r in rows:
        tpl[r["t"]].add(r["s"])
    tpl = {t: sorted(v) for t, v in tpl.items()}
    one = {r["s"]: 1 for r in rows}
    est = auc_w(rows, a, one) - auc_w(rows, b, one)
    ds = []
    for _ in range(B):
        w = defaultdict(int)
        for t, ss in tpl.items():
            for s in rng.choice(ss, size=len(ss), replace=True):
                w[s] += 1
        ds.append(auc_w(rows, a, w) - auc_w(rows, b, w))
    return est, [float(np.percentile(ds, 2.5)), float(np.percentile(ds, 97.5))]


def main():
    sc = {r["row_key"]: r for r in jl(R / "scores_rcomp_free.jsonl")}
    lab = {r["row_key"]: r for r in jl(R / "rcomp_free_labels_final.jsonl")}
    ymap = {"ERROR_CERT": 1, "UNRESOLVED_GLOSS_GATE_FAILED": 0}
    out = {"n_CORRECT_gated_untouched": sum(1 for k, l in lab.items() if l["label"] == "CORRECT" and not l["seen_iter3"])}
    for view, j in (("disg", "judge_cheap_disg"), ("orig", "judge_cheap_orig")):
        rows = [{"s": s["sentence_id"], "t": s["template_id"], "y": ymap[lab[k]["label"]], "c": s["c_score_align"], "j": s[j]}
                for k, s in sc.items() if s["untouched"] and lab[k]["label"] in ymap and s["c_score_align"] is not None and s[j] is not None]
        one = {r["s"]: 1 for r in rows}
        est, ci = boot_delta(rows, "c", "j")
        rng = np.random.default_rng(11)
        perm = [dict(r) for r in rows]
        byt = defaultdict(list)
        for i, r in enumerate(perm):
            byt[r["t"]].append(i)
        for t, ix in byt.items():
            ys = rng.permutation([perm[i]["y"] for i in ix])
            for i, y in zip(ix, ys):
                perm[i]["y"] = int(y)
        pest, pci = boot_delta(perm, "c", "j", B=500)
        out[view] = {"n": len(rows), "auroc_c_align": auc_w(rows, "c", one), "auroc_judge": auc_w(rows, "j", one), "delta": est, "ci_B1000": ci,
                     "permuted_labels": {"delta": pest, "ci_B500": pci, "test_fails_as_it_should": bool(pci[0] <= 0 <= pci[1]) is True}}
    # audit-labelled view (raw auditor verdicts, both auditors must agree)
    F = ("FAITHFUL", "FAITHFUL_DIFFERENT_DECOMPOSITION")
    v = defaultdict(dict)
    for r in jl(R / "audit_rows.jsonl"):
        if r.get("verdict"):
            v[r["row_key"]][r["auditor"]] = r["verdict"]
    rows = []
    for k, d in v.items():
        if len(d) < 2:
            continue
        a, b = d.get("sonnet5"), d.get("glm46")
        y = 0 if (a in F and b in F) else (1 if a == b == "UNFAITHFUL" else None)
        s = sc[k]
        if y is None or s["c_score_align"] is None or s["judge_cheap_disg"] is None:
            continue
        rows.append({"s": s["sentence_id"], "t": s["template_id"], "y": y, "c": s["c_score_align"], "j": s["judge_cheap_disg"]})
    est, ci = boot_delta(rows, "c", "j")
    out["audit_consensus_view_disg"] = {"n": len(rows), "n_err": sum(r["y"] for r in rows), "delta": est, "ci_B1000": ci}
    # frontier
    fr = {r["row_key"]: 1 - r["p"] for r in jl(R / "judge_frontier_FREE.jsonl") if r.get("p") is not None}
    rows = [{"s": sc[k]["sentence_id"], "t": sc[k]["template_id"], "y": ymap[lab[k]["label"]], "c": sc[k]["c_score_align"], "f": f}
            for k, f in fr.items()]
    one = {r["s"]: 1 for r in rows}
    est, ci = boot_delta(rows, "c", "f")
    out["frontier"] = {"n": len(rows), "auroc_c_align": auc_w(rows, "c", one), "auroc_frontier": auc_w(rows, "f", one), "delta": est, "ci_B1000": ci}
    A = json.loads((R / "analysis_rcomp.json").read_text())
    h = A["provisional_headline"]
    out["match_pipeline_point_estimates_1e-9"] = {
        v_: bool(abs(out[v_]["delta"] - h[v_]["delta"]) < 1e-9 and abs(out[v_]["auroc_c_align"] - h[v_]["auroc_a"]) < 1e-9) for v_ in ("disg", "orig")}
    out["match_frontier_1e-9"] = bool(abs(out["frontier"]["delta"] - A["frontier"]["c_align_minus_frontier"]["delta"]) < 1e-9)
    out["match_audit_view_1e-9"] = bool(abs(out["audit_consensus_view_disg"]["delta"] - A["audit_labelled_view"]["y_aud"]["disg"]["delta"]) < 1e-9)
    (R / "rederive_raw.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
