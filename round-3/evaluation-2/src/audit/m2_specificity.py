#!/usr/bin/env python3
"""Why the M2 placebo does not fail: is the rise of divergence with length SPECIFIC to CORRECT rows?
(1) label x length interaction on all scorable R_AB rows: divergent ~ y*zw + zn + C(stratum) (cluster-robust GLM);
(2) permutation nulls of the M2 slope: row-level shuffles and WITHIN-sentence shuffles (keeps each sentence's composition).
Reads population_RAB.pkl only for convenience of the frame (row keys, labels, endorsement, words, n_conditions, stratum)."""
import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parent.parent
P = pd.read_pickle(ROOT / "results/population_RAB.pkl").reset_index(drop=True)
P["y"] = P.y_AB.astype(int)
P["div"] = 1 - P.end_MAJ.astype(int)
P["zw"] = (P.words - P.words.mean()) / P.words.std()
P["zn"] = (P.n_conditions - P.n_conditions.mean()) / P.n_conditions.std()
g = pd.factorize(P.sentence_id)[0]


def fit(f, frame, groups):
    return smf.glm(f, frame, family=sm.families.Binomial()).fit(cov_type="cluster", cov_kwds={"groups": groups})


out = {}
r = fit("div ~ y * zw + zn + C(stratum)", P, g)
ci = r.conf_int()
out["interaction_model"] = {k: {"b": float(r.params[k]), "ci": [float(ci.loc[k, 0]), float(ci.loc[k, 1])]} for k in ("zw", "y", "y:zw")}
out["interaction_model"]["reading"] = ("zw = length slope of divergence for CORRECT rows (y=0); y:zw = how much FLATTER/STEEPER it is for "
                                       "ERROR rows. M2 is label-specific only if y:zw < 0 with CI excluding 0.")
cor = P[P.y == 0]
obs = fit("div ~ zw + zn + C(stratum)", cor, pd.factorize(cor.sentence_id)[0]).params["zw"]
rng = np.random.default_rng(11)
nulls = {"row_shuffle": [], "within_sentence_shuffle": []}
for b in range(200):
    for kind in nulls:
        ys = rng.permutation(P.y.values) if kind == "row_shuffle" else P.groupby("sentence_id").y.transform(lambda s: rng.permutation(s.values)).values
        c = P[ys == 0]
        nulls[kind].append(fit("div ~ zw + zn + C(stratum)", c, pd.factorize(c.sentence_id)[0]).params["zw"])
out["M2_slope_observed_glm"] = float(obs)
for k, v in nulls.items():
    v = np.array(v)
    out[f"null_{k}"] = {"mean": float(v.mean()), "p2.5": float(np.percentile(v, 2.5)), "p97.5": float(np.percentile(v, 97.5)),
                        "p_obs_ge": float((np.sum(v >= obs) + 1) / (len(v) + 1))}
(ROOT / "audit/m2_specificity.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
