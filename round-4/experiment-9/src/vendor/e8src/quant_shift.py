#!/usr/bin/env python3
"""D-GPU16 diagnostic: on the 1,264 E calibration rows (864 R_AB LLM CORRECT + 400 ERROR, identical rows for every column),
AUROC and FA-0.10 behaviour of the nf4 local judges / round trip (this artifact) vs the bf16 exp 6 columns, plus the
flash-lite judge. Writes results/quant_shift.json."""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import an_common as C  # noqa: E402
import fit_s4_perturb as S4  # noqa: E402
import stats as ST  # noqa: E402

C.guard("prereg_perturb")
cal = C.jl(C.DATA / "E_calib_units.jsonl")
feat = {r["row_key"]: r for r in C.jl(S4.E6 / "E_baseline_features.jsonl")}  # exp 6 row_key (= E_units row_key)
PS = C.RES / "perturb_scores"
src = {"judge_local_qwen8b_disg": {r["key"].rsplit("|", 1)[0]: r for r in C.jl(PS / "judge_local_qwen8b_nf4.jsonl")},
       "judge_local_llama8b_disg": {r["key"].rsplit("|", 1)[0]: r for r in C.jl(PS / "judge_local_llama8b_nf4.jsonl")},
       "judge_cheap_disg": {r["key"]: r for r in C.jl(PS / "judge_cheap_disg.jsonl")}}
nli = {r["key"]: r for r in C.jl(PS / "rt_nli_local_nf4.jsonl")}
y = np.array([1 if c["label"] == "ERROR" else 0 for c in cal])
out = {"n": len(cal), "n_error": int(y.sum())}
for m, S in src.items():
    v = np.array([1.0 - S[c["key"]]["p"] if S.get(c["key"], {}).get("p") is not None else 1.0 for c in cal])
    o = {"auroc_nf4_or_api": ST.auc_fast(y, v)}
    if m in ("judge_local_qwen8b_disg", "judge_local_llama8b_disg"):
        b = np.array([feat[c["row_key"]].get(m) if feat[c["row_key"]].get(m) is not None else 1.0 for c in cal])
        o["auroc_bf16_exp6"] = ST.auc_fast(y, b)
        o["spearman_nf4_vs_bf16"] = float(__import__("scipy.stats").stats.spearmanr(v, b).correlation)
    out[m] = o
if nli:
    for m in ("rt_nli_min_local", "rt_embed_cos_local"):
        v = np.array([1.0 if nli.get(c["key"], {}).get(m) is None else 1.0 - nli[c["key"]][m] for c in cal])
        b = np.array([feat[c["row_key"]].get(m) if feat[c["row_key"]].get(m) is not None else 1.0 for c in cal])
        out[m] = {"auroc_nf4": ST.auc_fast(y, v), "auroc_bf16_exp6": ST.auc_fast(y, b)}
(C.RES / "quant_shift.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
