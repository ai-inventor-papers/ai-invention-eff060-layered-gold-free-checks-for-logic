"""POST-HOC sensitivity (not pre-registered): microsoft/phi-4 sometimes emits the LAST few-shot exemplar's formula
(CanMake(x, cookies) ∧ CanMake(x, muffins) → Baker(x)) instead of / in front of its translation -- in 58/177 CSC calls
(partly via the single re-ask turn) and 24/292 of its original dataset-E outputs. Rule (symmetric for CSC and
FREE-MATCHED): a peer output that uses an exemplar-only predicate (CanMake/2 or Baker/1) while the sentence mentions none of
bake/baker/cookie/muffin is INVALID and leaves the denominator (like an unparseable peer). Rescore c_csc and c_free_exact on
PRIMARY rows and compare, paired, with the same bootstrap."""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np

SRC = Path(__file__).resolve().parent
ROOT = SRC.parent
sys.path.insert(0, str(SRC))
import csc  # noqa: E402
from analyse import Cell, build_frame, jdump, jl  # noqa: E402
from stats import SentBoot  # noqa: E402

EX = re.compile(r"\b(CanMake|Baker)\(")
TXT = re.compile(r"bak|cookie|muffin", re.I)


def invalid(fol: str | None, text: str) -> bool:
    return bool(fol) and bool(EX.search(fol)) and not TXT.search(text)


def main() -> dict:
    P, _ = build_frame()
    S = {}
    for r in jl(ROOT / "results" / "scores_labelblind.jsonl"):
        if r["arm"] in ("OWN", "FREE"):
            S[(r["arm"], r["row_key"])] = r
    cache = {json.loads(l)["key"]: json.loads(l) for l in (ROOT / "results" / "llm_cache.jsonl").read_text().splitlines() if l.strip()}
    routes = Counter()
    for c in cache.values():
        if invalid(c.get("fol"), "x"):
            routes[(c["model"], c["route"])] += 1
    new_csc, new_free, n_drop = [], [], Counter()
    for r in P.itertuples():
        for arm, dst in (("OWN", new_csc), ("FREE", new_free)):
            rec = S.get((arm, r.row_key))
            if rec is None or not r.PRIMARY:
                dst.append(np.nan)
                continue
            peers = [p for p in rec["peers"] if not invalid(p.get("fol"), r.text)]
            n_drop[arm] += len(rec["peers"]) - len(peers)
            dst.append(csc.consensus_score(r.candidate_fol, peers, graded=False)["c_csc"])
    P["c_csc_clean"] = new_csc
    P["c_free_exact_clean"] = new_free
    for c in ("c_csc_clean", "c_free_exact_clean"):
        P["en_" + c] = np.where(P[c].isna(), np.nan, (P[c] <= 0.5).astype(float))
    boot = SentBoot(P.sentence_id.values, 2000, 0)
    cell = Cell("PRIMARY", P, P.PRIMARY.values, boot)
    out = {"label": "POST-HOC sensitivity, not pre-registered", "rule": __doc__, "contaminated_calls_by_model_route": {f"{m}|{rt}": v for (m, rt), v in routes.items()},
           "peers_dropped_on_PRIMARY": dict(n_drop),
           "strat_auroc": {c: cell.metric(c, "strat") for c in ("c_csc", "c_csc_clean", "c_free_exact", "c_free_exact_clean", "T1__c_score_align")},
           "delta_strat": {"c_csc_clean - c_free_exact_clean": cell.delta("c_csc_clean", "c_free_exact_clean", "strat"),
                           "c_csc_clean - T1__c_score_align": cell.delta("c_csc_clean", "T1__c_score_align", "strat"),
                           "c_csc_clean - c_csc": cell.delta("c_csc_clean", "c_csc", "strat")},
           "ed": {c: cell.ed("en_" + c) for c in ("c_csc", "c_csc_clean", "c_free_exact", "c_free_exact_clean")}}
    jdump(out, ROOT / "results" / "posthoc_phi_contamination.json")
    print(json.dumps({k: out[k] for k in ("contaminated_calls_by_model_route", "peers_dropped_on_PRIMARY")}, indent=1))
    for c, m in out["strat_auroc"].items():
        print(c, round(m["point"], 3), [round(x, 3) for x in m["ci"]])
    for c, m in out["delta_strat"].items():
        print(c, round(m["delta"], 3), [round(x, 3) for x in m["ci"]])
    for c, m in out["ed"].items():
        print(c, "e", round(m["e"], 3), "d", round(m["d"], 3))
    return out


if __name__ == "__main__":
    main()
