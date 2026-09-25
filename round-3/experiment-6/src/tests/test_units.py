"""T0 unit tests (run before any sweep): blind loader, folds, disguise, prompt hashes, SC scorer, S4 placebo.
B2 construction tests live in tests/test_b2.py.  Usage: PYTHONHASHSEED=0 .venv/bin/python tests/test_units.py"""
import json
import os
import sys
from pathlib import Path

os.environ.setdefault("PYTHONHASHSEED", "0")
os.environ.setdefault("NLTK_DATA", str(Path(__file__).resolve().parent.parent / "data" / "nltk_data"))
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.setrecursionlimit(10000)
import numpy as np  # noqa: E402

from src.e_pool import LABEL_KEYS, fold_of_sentence, load_E  # noqa: E402

res = {}
# (1) label-blind loader
rows = load_E(blind=True)
res["T1_blind_no_label_keys"] = not any(k in r for r in rows for k in LABEL_KEYS)
res["T1_rows"] = len(rows) == 8507 and len({r["metadata_sentence_id"] for r in rows}) == 700
# (2) fold determinism + no sentence split
f1 = {r["metadata_sentence_id"]: fold_of_sentence(r["metadata_sentence_id"]) for r in rows}
f2 = {r["metadata_sentence_id"]: fold_of_sentence(r["metadata_sentence_id"]) for r in rows}
res["T2_folds_deterministic"] = f1 == f2
if (ROOT / "folds_E.json").exists():
    fj = json.loads((ROOT / "folds_E.json").read_text())
    res["T2_folds_file_matches"] = fj["sentence_fold"] == f1
    per_row = {}
    for r in rows:
        per_row.setdefault(r["metadata_sentence_id"], set()).add(fj["item_fold"][r["metadata_item_id"]])
    res["T2_no_sentence_split"] = all(len(v) == 1 for v in per_row.values())
# (3) disguise on 50 rows: assertions (AST inverse map, arity multiset, no collision) + z3 equivalence under inverse map
from src.disguise import disguise_item  # noqa: E402
from src.labeller.fol import equivalent, parse  # noqa: E402
from src.labeller.repair_census import rename, symbols  # noqa: E402
U = [u for u in json.loads((ROOT / "data" / "E_units.json").read_text()) if u["parse_ok"]][:50]
n_ok = n_eq = 0
for u in U:
    d = disguise_item(u["text"], u["candidate_fol"])
    n_ok += d["ok"]
    inv_p = {v: k.split("|")[0] for k, v in d["name_map"].items() if k.endswith("|pred")}
    inv_c = {v: k.split("|")[0] for k, v in d["name_map"].items() if k.endswith("|const")}
    e1 = parse(d["fol_d"])
    P1, _ = symbols(e1)
    back = rename(e1, {(n, a): inv_p.get(n, n) for (n, a) in P1}, inv_c)
    n_eq += equivalent(back, parse(u["candidate_fol"]), 3000) is True
res["T3_disguise_assertions_ok"] = f"{n_ok}/50"
res["T3_disguise_z3_equiv_under_inverse"] = f"{n_eq}/50"
# (4) prompt hashes = exp D
from src import judges as J  # noqa: E402
res["T4_rubricA_sha1"] = J.PROMPT_SHA["RUBRIC_A"] == "06686913c59b6d9a7daeb5748cb9f53ed2b2e812"
res["T4_user_json_A_sha1"] = J.PROMPT_SHA["USER_JSON_A"] == "5b3ccfb9d82edbbfb5bd1bb7a4e574da62be38b4"
# (5) SC scorer
from src.consensus_min import sc_scores_one  # noqa: E402
eqf = lambda a, b: a == b  # noqa: E731
res["T5_identical_samples_eq_frac_1"] = sc_scores_one("A(x)", ["A(x)"] * 5, eqf)["sc5_eq_frac"] == 1.0
res["T5_no_parsed_samples_eq_frac_0"] = sc_scores_one("A(x)", [None] * 5, eqf)["sc5_eq_frac"] == 0.0
res["T5_entropy_all_missing"] = round(sc_scores_one("A(x)", [None] * 5, eqf)["sc5_entropy"], 3) == round(np.log(6), 3)
# (7) S4 on shuffled labels ~0.5
from sklearn.metrics import roc_auc_score  # noqa: E402

from src.s4 import fit_s4_oof  # noqa: E402
rng = np.random.default_rng(0)
tab = [{"row_key": f"r{i}", "f1": float(rng.normal()), "f1__status": "ok", "f2": float(rng.normal()), "f2__status": "ok"} for i in range(2000)]
folds = {f"r{i}": i % 5 for i in range(2000)}
lab = {f"r{i}": int(rng.integers(0, 2)) for i in range(2000)}
oof, _ = fit_s4_oof(tab, lab, folds, ["f1", "f2"])
a = roc_auc_score([lab[k] for k in lab], [oof[k] for k in lab])
res["T7_shuffled_oof_auroc"] = round(float(a), 3)
res["T7_pass"] = bool(0.45 <= a <= 0.55)
print(json.dumps({k: (bool(v) if isinstance(v, np.bool_) else v) for k, v in res.items()}, indent=1))
bad = [k for k, v in res.items() if isinstance(v, (bool, np.bool_)) and not v]
print("T0", "PASS" if not bad else f"FAIL {bad}")
(ROOT / "results" / "test_units.json").write_text(json.dumps({k: (bool(v) if isinstance(v, np.bool_) else v) for k, v in res.items()}, indent=1))
