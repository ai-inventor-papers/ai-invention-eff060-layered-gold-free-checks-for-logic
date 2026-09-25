#!/usr/bin/env python3
"""STEP F: soundness audits -> results/soundness_audit.json and results/sig_replay_rows.jsonl.

(i)  SIG replay (exact, $0): each on-signature SIG row renamed (nonce / WordNet synonym) and searched name-free.
     - ERROR_CERT false-error rate on SIG-CORRECT rows (share with no equivalent map; bar <= 0.02);
     - identity recovery: share of SIG-CORRECT rows whose equivalent maps include the identity (un-renaming) map;
     - rescue rate on SIG-ERROR rows (share with a NON-identity equivalent map: rows the gloss check must stop);
     - ORACLE-CHECKER ceiling: a checker that answers YES exactly for identity pairs -> end-to-end labels vs SIG
       labels (this is the pipeline's upper bound; the real checkers' end-to-end numbers need the gloss step, D9).
(ii) executor audit (non-blind, D9 substitute for the blind Sonnet audit): ERROR_CERT precision and MAPPED precision
     with Wilson 95% CIs, reasons tallied.
(iii) old-label agreement (results/old_label_agreement.json) + the 20 hand-classified disagreements.
"""
from __future__ import annotations

import json
import math
import random
import re
from collections import Counter, defaultdict

from common import RES, WORK, dump, load_jsonl, setup_logger
from run_search import class_key

logger = setup_logger("soundness")


def wilson(k: int, n: int, z: float = 1.96) -> list:
    if n == 0:
        return [None, None]
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(max(0.0, c - h), 3), round(min(1.0, c + h), 3)]


def entry_is_identity(entry: str, inv: dict) -> bool:
    """entry 'Cand(x, k) => Target(x, c)' (or const:k => c). inv: renamed name -> original name."""
    left, right = entry.split(" => ", 1)
    if left.startswith("const:"):
        return inv.get("const:" + left[6:], left[6:]) == right
    if right.startswith("¬") or " ∧ " in right or right in ("<fresh>", "<free>") or "[split]" in right:
        return False
    if "/" in left.split("(")[0]:  # relation map 'P/2 => R(x, y)' is the identity iff straight order and names invert
        return inv.get(left.split("/")[0], left.split("/")[0]) == right.split("(")[0] and right.endswith("(x, y)")
    ln, rn = left.split("(")[0], right.split("(")[0]
    if inv.get(ln, ln) != rn:
        return False
    la = [a.strip() for a in left[left.index("(") + 1:-1].split(",")] if "(" in left else []
    ra = [a.strip() for a in right[right.index("(") + 1:-1].split(",")] if "(" in right else []
    if len(la) != len(ra):
        return False
    return all(inv.get("const:" + a, a) == b for a, b in zip(la, ra))


def replay(mode: str) -> tuple[dict, list]:
    rows = load_jsonl(WORK / f"sig_renamed_{mode}.jsonl")
    search = {r["class_key"]: r for r in load_jsonl(RES / f"sig_replay_{mode}.jsonl")}
    out = []
    for r in rows:
        sr = search.get(class_key(r["sentence_id"], r["renamed_fol"]))
        inv = {v: k for k, v in r["rename_map"].items() if not k.startswith("const:")}
        inv.update({f"const:{v}": k[6:] for k, v in r["rename_map"].items() if k.startswith("const:")})
        st = sr["status"] if sr else "MISSING"
        ident = {"weak": False, "strong": False, "converse": False}
        nonid = False
        if sr and sr.get("equiv_maps"):
            ents = sr["map_entries_union"]
            for m in sr["equiv_maps"]:
                is_id = all(entry_is_identity(ents[i], inv) for i in m["entry_ids"])
                if is_id:
                    ident[m["reading"]] = True
                else:
                    nonid = True
        # oracle checker: YES exactly on identity pairs -> CORRECT iff an identity weak/strong map exists, READING_CHOICE
        # iff only an identity converse map exists, ERROR_GLOSS iff maps exist but none is identity
        if st in ("MAPPED", "READING_CHOICE"):
            oracle = ("CORRECT" if (ident["weak"] or ident["strong"]) else
                      ("READING_CHOICE" if ident["converse"] else "ERROR_GLOSS"))
        else:
            oracle = st
        out.append({"row_key": r["row_key"], "sentence_id": r["sentence_id"], "slot": r["slot"], "template_id": r["template_id"],
                    "sig_label": r["sig_label"], "sig_matched_reading": r["matched_reading"], "rename": mode,
                    "canon_fol": r["canon_fol"], "renamed_fol": r["renamed_fol"], "search_status": st,
                    "identity_map_found": ident, "non_identity_map_found": nonid,
                    "n_equiv_maps": sr.get("n_equiv_maps") if sr else None,
                    "n_equiv_map_orbits": sr.get("n_equiv_map_orbits") if sr else None,
                    "n_maps_enumerated": sr.get("n_maps_enumerated") if sr else None,
                    "nonequiv_certificate_type_counts": sr.get("nonequiv_certificate_type_counts") if sr else None,
                    "oracle_end_to_end_label": oracle})
    corr = [o for o in out if o["sig_label"] == "CORRECT"]
    err = [o for o in out if o["sig_label"] == "ERROR"]
    rc = [o for o in out if o["sig_label"] == "READING_CHOICE"]
    fe = sum(o["search_status"] == "ERROR_CERT" for o in corr)
    idr = sum(o["identity_map_found"]["weak"] or o["identity_map_found"]["strong"] for o in corr)
    resc = sum(o["search_status"] in ("MAPPED", "READING_CHOICE") for o in err)
    conf = Counter((o["sig_label"], o["oracle_end_to_end_label"]) for o in out)
    rep = {"mode": mode, "n_rows": len(out), "n_CORRECT": len(corr), "n_ERROR": len(err), "n_READING_CHOICE": len(rc),
           "ERROR_CERT_false_error_rate_on_SIG_CORRECT": round(fe / max(len(corr), 1), 4),
           "false_error_ci": wilson(fe, len(corr)), "bar": "<= 0.02", "PASS": fe / max(len(corr), 1) <= 0.02,
           "identity_map_recovery_on_SIG_CORRECT": round(idr / max(len(corr), 1), 4),
           "ERROR_CERT_share_on_SIG_ERROR": round(sum(o["search_status"] == "ERROR_CERT" for o in err) / max(len(err), 1), 4),
           "rescue_rate_on_SIG_ERROR (non-identity equivalent map exists)": round(resc / max(len(err), 1), 4),
           "rescue_ci": wilson(resc, len(err)),
           "READING_CHOICE_rows_mapped": round(sum(o["search_status"] == "MAPPED" for o in rc) / max(len(rc), 1), 4),
           "oracle_confusion": {f"{a}->{b}": v for (a, b), v in sorted(conf.items())},
           "oracle_false_CORRECT_on_SIG_ERROR": round(sum(o["oracle_end_to_end_label"] == "CORRECT" for o in err) / max(len(err), 1), 4),
           "oracle_CORRECT_recall_on_SIG_CORRECT": round(sum(o["oracle_end_to_end_label"] == "CORRECT" for o in corr) / max(len(corr), 1), 4),
           "rescue_by_template": {t: round(sum(o["search_status"] == "MAPPED" for o in err if o["template_id"] == t) /
                                           max(sum(1 for o in err if o["template_id"] == t), 1), 3)
                                  for t in sorted({o["template_id"] for o in err})}}
    return rep, out


def stratified_300(out_syn: list) -> list:
    """The pre-registered 300-row (150 CORRECT / 150 ERROR, stratified by template) synonym-replay subsample on which the
    end-to-end gloss pipeline is to be run (pending, D9)."""
    rng = random.Random(20260924)
    pick = []
    for lab in ("CORRECT", "ERROR"):
        by = defaultdict(list)
        for o in out_syn:
            if o["sig_label"] == lab:
                by[o["template_id"]].append(o)
        for t in by:
            rng.shuffle(by[t])
        i = 0
        chosen = []
        while len(chosen) < 150 and any(by.values()):
            t = sorted(by)[i % len(by)]
            if by[t]:
                chosen.append(by[t].pop())
            i += 1
        pick += chosen
    return [o["row_key"] for o in pick]


def executor_audit() -> dict:
    v = json.loads((WORK / "executor_audit_verdicts.json").read_text())
    ek = json.loads((WORK / "audit_errcert_keys.json").read_text())
    mk = json.loads((WORK / "audit_mapped_keys.json").read_text())
    rep = {"auditor": v["auditor"], "protocol": v["protocol"]}
    ev = v["ERROR_CERT"]
    n = len(ev)
    not_faithful = sum(x[0] in ("UNFAITHFUL", "UNSURE") for x in ev.values())
    rep["ERROR_CERT"] = {"n": n, "verdicts": dict(Counter(x[0] for x in ev.values())),
                         "implied_precision_not_rated_faithful": round(not_faithful / n, 3), "ci": wilson(not_faithful, n),
                         "out_of_family_faithful_forms": dict(Counter(
                             ("disjunctive split / one predicate with two constants" if ("disjunctive" in x[1] or "two constants" in x[1] or "two different constants" in x[1])
                              else "relational / ∃-for-constant" if ("∃" in x[1] or "relational" in x[1])
                              else "negation inside the name (B5 regex miss)" if "negation inside" in x[1] else "other")
                             for x in ev.values() if x[0] == "FAITHFUL_DIFFERENT_DECOMPOSITION")),
                         "rows": [{"row_key": ek[int(i)], "verdict": x[0], "reason": x[1]} for i, x in ev.items()],
                         "flag": None}
    if rep["ERROR_CERT"]["implied_precision_not_rated_faithful"] < 0.90:
        rep["ERROR_CERT"]["flag"] = ("implied ERROR_CERT precision < 0.90: the FREE ERROR class carries out-of-family "
                                     "correct forms; labels are kept as frozen; iteration 5 should report FREE AUROC with and "
                                     "without the flagged form classes (sensitivity)")
    mv = v["MAPPED"]
    m = len(mv)
    faithful = sum(x[0] == "FAITHFUL" for x in mv.values())
    rep["MAPPED"] = {"n": m, "verdicts": dict(Counter(x[0] for x in mv.values())),
                     "share_faithful (upper bound of CORRECT precision if the gloss check accepted every MAPPED row)": round(faithful / m, 3),
                     "ci": wilson(faithful, m),
                     "rows": [{"row_key": mk[int(i)], "verdict": x[0], "reason": x[1]} for i, x in mv.items()]}
    hv = v["old_vs_new_disagreements_hand_classified"]
    rep["old_vs_new_hand_classification"] = dict(Counter(x[0] for x in hv.values()))
    rep["old_vs_new_hand_rows"] = hv
    return rep


def main() -> None:
    rep = {"i_sig_replay": {}, "ii_executor_audit": None, "iii_old_labels": None}
    all_rows = []
    outs = {}
    for mode in ("nonce", "syn"):
        r, out = replay(mode)
        rep["i_sig_replay"][mode] = r
        outs[mode] = out
        all_rows += out
        logger.info(f"replay {mode}: {json.dumps({k: v for k, v in r.items() if not isinstance(v, dict)})}")
    sel = set(stratified_300(outs["syn"]))
    for o in all_rows:
        o["in_e2e_gloss_subsample_300"] = o["rename"] == "syn" and o["row_key"] in sel
        o["e2e_gloss_label"] = None
    rep["i_sig_replay"]["e2e_gloss_subsample_300"] = {"n": len(sel), "status": "PENDING (D9: no API budget)",
                                                      "runner": "src/resume_gloss.py"}
    with (RES / "sig_replay_rows.jsonl").open("w") as fh:
        for o in all_rows:
            fh.write(json.dumps(o, ensure_ascii=False) + "\n")
    rep["ii_executor_audit"] = executor_audit()
    old = json.loads((RES / "old_label_agreement.json").read_text())
    rep["iii_old_labels"] = {k: old[k] for k in ("agreement_table_old_tierA_vs_new", "kappa_old_vs_new_search_view",
                                                 "new_row_keys_missing_in_old", "seen_iter3", "untouched", "note")}
    rep["iii_old_labels"]["hand_classified_20"] = rep["ii_executor_audit"]["old_vs_new_hand_classification"]
    dump(RES / "soundness_audit.json", rep)
    logger.info(f"executor audit: ERROR_CERT {rep['ii_executor_audit']['ERROR_CERT']['verdicts']} MAPPED {rep['ii_executor_audit']['MAPPED']['verdicts']}")


if __name__ == "__main__":
    main()
