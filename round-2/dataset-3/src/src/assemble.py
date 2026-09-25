#!/usr/bin/env python3
"""STEP 8 final rule + STEP 10 disguise + STEP 11 assembly and statistics.

Reads (whatever exists): work/rcomp_sentences.json, work/rcomp_labels.json, raw/adjudication.jsonl,
work/adjudication_queue.json, work/adjudicator_check*.json, work/perturb_*.json, raw/fluency_items.jsonl,
raw/ref_audit_items.jsonl, lexicon.json, cost_ledger.jsonl, E's full_data_out.json (L25 comparison).
Writes: work/assembled.json (exp_sel_data_out layout; data.py re-verifies every row against temp/datasets/ and writes
full_data_out.json; groups rcomp_sentences, rcomp_candidates [only once candidates
exist: the schema forbids empty groups], perturb_suite, adjudicator_check), rcomp_peers.json, work/testability.json,
work/stats.json, work/disguise_guard.json.
"""
from __future__ import annotations

import json
import math
from collections import Counter, defaultdict

from common import E_DIR, RAW, ROOT, W, dump, load_jsonl, sha1, setup_logger

logger = setup_logger("assemble")
SIB = ROOT.parent / "gen_art_dataset_2"


def wilson(k: int, n: int, z: float = 1.96):
    if not n:
        return None
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(k / n, 4), round(c - h, 4), round(c + h, 4)]


def sibling_gate_status() -> str:
    for name in ("gate_report.json", "gate_result.json"):
        p = SIB / "work" / name
        if p.exists():
            try:
                g = json.loads(p.read_text())
                v = str(g.get("verdict") or g.get("gate") or g.get("status") or "").upper()
                if v:
                    return v
            except json.JSONDecodeError:
                pass
    if (SIB / "work" / "gate_report_VOID_key_outage.json").exists():
        return "VOID_KEY_OUTAGE"
    return "NOT_AVAILABLE"


def final_rows(sents: dict, check: dict | None) -> list[dict]:
    p = W / "rcomp_labels.json"
    if not p.exists():
        return []
    labs = json.loads(p.read_text())
    adj = {r["key"]: r for r in load_jsonl(RAW / "adjudication.jsonl") if r.get("final")}
    queued = {x["class_id"]: x["priority"] for x in (json.loads((W / "adjudication_queue.json").read_text())
                                                      if (W / "adjudication_queue.json").exists() else [])}
    gate = sibling_gate_status()
    provisional = not gate.startswith("PASS") or (check is not None and check.get("balanced_accuracy") is not None
                                                  and check["balanced_accuracy"] < 0.80)
    ref_wrong = Counter()
    for r in labs:
        a = adj.get("rcomp|" + (r["class_id"] or ""))
        if a and a.get("reference_wrong"):
            ref_wrong[r["sentence_id"]] += 1  # counted per candidate row that inherits a reference_wrong class verdict
    # REF_FLAGGED needs >= 2 distinct adjudications (classes), not rows
    rw_cls = defaultdict(set)
    for r in labs:
        a = adj.get("rcomp|" + (r["class_id"] or ""))
        if a and a.get("reference_wrong"):
            rw_cls[r["sentence_id"]].add(r["class_id"])
    ref_flagged = {s for s, c in rw_cls.items() if len(c) >= 2}
    out = []
    for r in labs:
        L = r["solver_label"]
        a = adj.get("rcomp|" + (r["class_id"] or "")) if r["class_id"] else None
        v = a.get("verdict") if a else None
        row = {"final_label": None, "label_tier": None, "correct_not_equivalent": False, "reading_choice": False,
               "adj_pending": False, "error_ops": None, "label_source": None}
        if L == "UNPARSEABLE":
            row.update(final_label="UNPARSEABLE", label_tier="-", label_source="parser")
        elif L == "CORRECT":
            row.update(final_label="CORRECT", label_tier="A", label_source="solver_EQ")
        elif L in ("VOCAB_GRAN", "COMPOUND", "TIMEOUT_UNKNOWN"):
            if v == "FAITHFUL":
                row.update(final_label="CORRECT", label_tier="B", correct_not_equivalent=True, label_source="adjudicator")
            elif v == "UNFAITHFUL":
                ops = sorted(set(a.get("ops") or []) | ({"MEANING_RENAME"} if L == "VOCAB_GRAN" else set()))
                row.update(final_label="ERROR", label_tier="B", error_ops=ops, label_source="adjudicator")
            elif v == "AMBIGUOUS_READING":
                row.update(final_label="CONTESTED", label_tier="B", reading_choice=True, label_source="adjudicator")
            else:
                row.update(final_label="UNRESOLVED", label_tier="none", adj_pending=r["class_id"] in queued,
                           label_source="routed_not_adjudicated")
        elif L == "ERROR":
            ops = r.get("solver_repair_ops")
            if v == "FAITHFUL":
                row.update(final_label="CONTESTED", label_tier="A", error_ops=ops, label_source="solver_vs_adjudicator")
            elif v == "UNFAITHFUL":
                row.update(final_label="ERROR", label_tier="A", error_ops=ops, label_source="solver+adjudicator_confirmed")
            elif v == "AMBIGUOUS_READING":
                row.update(final_label="ERROR", label_tier="A", error_ops=ops, reading_choice=True, label_source="solver")
            else:
                row.update(final_label="ERROR", label_tier="A", error_ops=ops, adj_pending=r["class_id"] in queued,
                           label_source="solver")
        if r["sentence_id"] in ref_flagged and row["label_tier"] in ("A", "B"):
            row["label_tier"] = "C"
        row.update({"adj_verdict": v, "adj_ops": (a or {}).get("ops"), "adj_location": (a or {}).get("location"),
                    "adj_reference_wrong": (a or {}).get("reference_wrong"), "adj_priority": queued.get(r["class_id"]),
                    "tier_b_provisional": provisional and row["label_tier"] == "B",
                    "ref_flagged_by_adjudication": r["sentence_id"] in ref_flagged,
                    "adjudicator_gate_status": gate})
        out.append({**r, **row})
    return out


def testability(rows: list[dict], sents: dict) -> dict:
    def cell(sub, tiers):
        ok = [r for r in sub if r["label_tier"] in tiers and r["final_label"] in ("CORRECT", "ERROR") and not r["reading_choice"]
              and not r["ref_flagged_by_adjudication"]]
        c = [r for r in ok if r["final_label"] == "CORRECT"]
        e = [r for r in ok if r["final_label"] == "ERROR"]
        res = {"correct_rows": len(c), "correct_sentences": len({r["sentence_id"] for r in c}),
               "error_rows": len(e), "error_sentences": len({r["sentence_id"] for r in e})}
        res["testable"] = res["correct_rows"] >= 50 and res["error_rows"] >= 50 and res["correct_sentences"] >= 25 \
            and res["error_sentences"] >= 25
        return res
    main = [r for r in rows if not sents[r["sentence_id"]]["topup_batch"]]
    out = {"rule": "tiers A+B, >= 50 CORRECT and >= 50 ERROR LLM rows over >= 25 sentences each; CONTESTED, reading_choice, "
                   "REF_FLAGGED excluded", "main_A+B": cell(main, ("A", "B")), "main_A_only": cell(main, ("A",)),
           "with_topup_A+B": cell(rows, ("A", "B")), "with_topup_A_only": cell(rows, ("A",))}
    out["verdict"] = "TESTABLE" if out["main_A+B"]["testable"] or out["with_topup_A+B"]["testable"] else "NOT_TESTABLE"
    out["topup_rule_fires"] = not (out["main_A+B"]["correct_rows"] >= 50 and out["main_A+B"]["correct_sentences"] >= 25
                                   and out["main_A+B"]["error_rows"] >= 50 and out["main_A+B"]["error_sentences"] >= 25)
    return out


def disguise_all(sents: dict, cand_rows: list[dict], pert: list[dict]) -> tuple[dict, dict]:
    """E's disguise.py per sentence; bijection over the text and ALL formulas of that sentence."""
    from disguise import Disguiser
    from fol import parse, equivalent
    by_s = defaultdict(set)
    texts = {}
    for s in sents.values():
        texts[s["sentence_id"]] = s["text"]
        by_s[s["sentence_id"]] |= {s["reference_fol_weak"], s["reference_fol_strong"]} | ({s["reading_converse"]} if s.get("reading_converse") else set())
    for r in cand_rows:
        if r.get("candidate_fol"):
            by_s[r["sentence_id"]].add(r["candidate_fol"])
    for m in pert:
        texts.setdefault(m["sentence_id"], m["text"])
        by_s[m["sentence_id"]] |= {m["base_fol"], m["candidate_fol"]} | set(m.get("accepted_readings") or [])
    dis, guard = {}, {"sentences_checked": 0, "pairs_checked": 0, "mismatches": 0, "examples": []}
    for k, sid in enumerate(sorted(by_s)):
        fs = sorted(by_s[sid])
        D = Disguiser(sid, texts[sid], fs)
        dis[sid] = {"text": D.text(texts[sid]), "fol": {f: D.formula(f) for f in fs}}
        if guard["sentences_checked"] < 30 and k % 7 == 0:
            guard["sentences_checked"] += 1
            base = fs[0]
            for f in fs[1:6]:
                try:
                    a = equivalent(parse(base), parse(f), ms=3000)
                    b = equivalent(parse(dis[sid]["fol"][base]), parse(dis[sid]["fol"][f]), ms=3000)
                except Exception:  # noqa: BLE001 - unparseable candidates have no disguise
                    continue
                guard["pairs_checked"] += 1
                if a != b:
                    guard["mismatches"] += 1
                    guard["examples"].append([sid, base, f, a, b])
    return dis, guard


def e_l25_error_rates() -> dict:
    d = json.loads((E_DIR / "full_data_out.json").read_text())
    hc = [g for g in d["datasets"] if g["dataset"] == "heldout_candidates"][0]["examples"]
    agg = defaultdict(Counter)
    for r in hc:
        if r["metadata_strata"]["source_stratum"] != "L25" or r["metadata_system_class"] != "llm":
            continue
        if r["metadata_label_tier"] not in ("A", "B") or r["metadata_reading_choice"] or r["output"] not in ("CORRECT", "ERROR"):
            continue
        agg[f"{r['metadata_slot']}:{r['metadata_prompt_variant']}"][r["output"]] += 1
    return {k: {"n": v["CORRECT"] + v["ERROR"], "error_rate": round(v["ERROR"] / (v["CORRECT"] + v["ERROR"]), 3)}
            for k, v in sorted(agg.items())}


def main():
    import select_sentences as ss
    rs = json.loads((W / "rcomp_sentences.json").read_text())
    sents = {r["sentence_id"]: r for r in rs}
    pert = json.loads((W / "perturb_suite.json").read_text())
    ctrl = json.loads((W / "perturb_controls.json").read_text())
    check_items = json.loads((W / "adjudicator_check_items.json").read_text())
    check = json.loads((W / "adjudicator_check.json").read_text()) if (W / "adjudicator_check.json").exists() else None
    rows = final_rows(sents, check)
    rows = [r for r in rows if r.get("expected") is None]  # never assemble dry-run rows
    dis, guard = disguise_all(sents, rows, pert + ctrl)
    dump(W / "disguise_guard.json", guard)
    logger.info(f"disguise guard {guard['pairs_checked']} pairs, mismatches {guard['mismatches']}")
    assert guard["mismatches"] == 0
    lex = json.loads((ROOT / "lexicon.json").read_text())
    groups = []
    # ---- rcomp_sentences
    ex = []
    for s in sorted(rs, key=lambda s: (s["batch"], s["sentence_id"])):
        status = ("REF_FLAGGED" if s["ref_flagged"] else
                  ("REF_BY_CONSTRUCTION_AUDITED_OK" if s["audit_status"] == "AUDITED" else "REF_BY_CONSTRUCTION_AUDIT_PENDING"))
        inp = {"text": s["text"], "reference_fol": s["reference_fol_weak"], "reference_fol_weak": s["reference_fol_weak"],
               "reference_fol_strong": s["reference_fol_strong"], "reading_converse": s.get("reading_converse")}
        ex.append({"input": json.dumps(inp, ensure_ascii=False), "output": status, "metadata_fold": "R_COMP",
                   "metadata_sentence_id": s["sentence_id"], "metadata_template_id": s["template_id"],
                   "metadata_surface_variant": s["surface_variant"], "metadata_clause_type": s["clause_type"],
                   "metadata_nested": s["nested"], "metadata_sentence_seed": s["sentence_seed"], "metadata_sort_group": s["sort_group"],
                   "metadata_source_rule_ids": s["source_rule_ids"], "metadata_lexicon_ids": s["lexicon_ids"],
                   "metadata_noun_lexicon_id": s["noun_lexicon_id"], "metadata_condition_lexicon_ids": s["condition_lexicon_ids"],
                   "metadata_negated_condition": s["negated_condition"], "metadata_fluency": s["fluency"],
                   "metadata_fluency_status": s["fluency_status"], "metadata_audit_status": s["audit_status"],
                   "metadata_audit_verdicts": s["audit_verdicts"], "metadata_ref_flagged": s["ref_flagged"],
                   "metadata_topup_batch": s["topup_batch"], "metadata_batch": s["batch"],
                   "metadata_profile_weak": s["profile_weak"], "metadata_profile_strong": s["profile_strong"],
                   "metadata_strata": {"words": s["words"], "n_quant": s["nquant"], "depth": s["depth_weak"],
                                       "n_conditions": s["nconds_weak"], "text_conditions": s["text_conditions"],
                                       "exception_type": s["exception_type"], "template_id": s["template_id"],
                                       "nested": s["nested"], "word_bin": s["word_bin"]},
                   "metadata_disguised_text": dis[s["sentence_id"]]["text"],
                   "metadata_disguised_fol_weak": dis[s["sentence_id"]]["fol"].get(s["reference_fol_weak"]),
                   "metadata_disguised_fol_strong": dis[s["sentence_id"]]["fol"].get(s["reference_fol_strong"])})
    groups.append({"dataset": "rcomp_sentences", "examples": ex})
    # ---- rcomp_candidates
    if rows:
        ex = []
        for r in sorted(rows, key=lambda r: (r["sentence_id"], r["system"], r["prompt_variant"])):
            s = sents[r["sentence_id"]]
            inp = {"text": s["text"], "candidate_fol": r.get("candidate_fol") or "", "reference_fol": s["reference_fol_weak"],
                   "reference_fol_weak": s["reference_fol_weak"], "reference_fol_strong": s["reference_fol_strong"],
                   "system": r["system"], "prompt_variant": r["prompt_variant"]}
            e = {"input": json.dumps(inp, ensure_ascii=False), "output": r["final_label"], "metadata_fold": "R_COMP",
                 "metadata_item_id": r["item_id"], "metadata_sentence_id": r["sentence_id"], "metadata_system": r["system"],
                 "metadata_slot": r["slot"], "metadata_family": r["family"], "metadata_prompt_variant": r["prompt_variant"],
                 "metadata_raw_output": r["raw_output"], "metadata_parse_ok": r["parse_ok"], "metadata_api_error": r.get("api_error"),
                 "metadata_auto_label_weak": r.get("solver_auto_label_weak"), "metadata_auto_label_strong": r.get("solver_auto_label_strong"),
                 "metadata_solver_label": r["solver_label"], "metadata_matched_reading": r.get("solver_matched_reading"),
                 "metadata_repair_ops": r.get("solver_repair_ops"), "metadata_repair_reading": r.get("solver_repair_reading"),
                 "metadata_repair_status": {k: r.get(f"solver_repair_status_{k}") for k in ("weak", "strong")},
                 "metadata_convention_flags": r.get("solver_convention_flags"),
                 "metadata_addrop_only_suspect": bool(r.get("solver_addrop_only_suspect")),
                 "metadata_only_if_converse": bool(r.get("solver_only_if_converse")),
                 "metadata_lex_anchored_vocab": r.get("solver_lex_anchored_vocab"),
                 "metadata_adj_verdict": r["adj_verdict"], "metadata_adj_ops": r["adj_ops"], "metadata_adj_location": r["adj_location"],
                 "metadata_adj_reference_wrong": r["adj_reference_wrong"], "metadata_adj_priority": r["adj_priority"],
                 "metadata_adj_pending": r["adj_pending"], "metadata_label_tier": r["label_tier"], "metadata_label_source": r["label_source"],
                 "metadata_error_ops": r["error_ops"], "metadata_correct_not_equivalent": r["correct_not_equivalent"],
                 "metadata_reading_choice": r["reading_choice"], "metadata_tier_b_provisional": r["tier_b_provisional"],
                 "metadata_ref_flagged": r["ref_flagged_by_adjudication"], "metadata_adjudicator_gate_status": r["adjudicator_gate_status"],
                 "metadata_class_id": r["class_id"], "metadata_class_size": r["class_size"], "metadata_topup_batch": s["topup_batch"],
                 "metadata_strata": {"words": s["words"], "n_quant": s["nquant"], "depth": s["depth_weak"], "n_conditions": s["nconds_weak"],
                                     "exception_type": s["exception_type"], "template_id": s["template_id"], "nested": s["nested"],
                                     "word_bin": s["word_bin"]},
                 "metadata_disguised_text": dis[r["sentence_id"]]["text"],
                 "metadata_disguised_fol": dis[r["sentence_id"]]["fol"].get(r.get("candidate_fol")),
                 "metadata_cost_usd": r.get("cost_usd")}
            ex.append(e)
        groups.append({"dataset": "rcomp_candidates", "examples": ex})
        peers = defaultdict(lambda: {"candidates": []})
        for r in rows:
            s = sents[r["sentence_id"]]
            p = peers[r["sentence_id"]]
            p.update({"text": s["text"], "reference_fol_weak": s["reference_fol_weak"], "reference_fol_strong": s["reference_fol_strong"],
                      "template_id": s["template_id"]})
            p["candidates"].append({k: r.get(k) for k in ("item_id", "system", "family", "slot", "prompt_variant", "raw_output",
                                                           "candidate_fol", "parse_ok")})
        dump(ROOT / "rcomp_peers.json", dict(peers))
        tst = testability(rows, sents)
        dump(W / "testability.json", tst)
    # ---- perturb_suite
    ex = []
    for m in pert + ctrl:
        is_c = m["system"].startswith("CONTROL")
        inp = {"text": m["text"], "candidate_fol": m["candidate_fol"], "reference_fol": m["base_fol"],
               "reference_fol_weak": m["base_fol"], "reference_fol_strong": (m.get("accepted_readings") or [None])[0],
               "system": m["system"], "prompt_variant": "none"}
        e = {"input": json.dumps(inp, ensure_ascii=False), "output": "CORRECT" if is_c else "ERROR",
             "metadata_fold": "PERTURB_CONTROL" if is_c else "PERTURB", "metadata_item_id": m["item_id"],
             "metadata_sentence_id": m["sentence_id"], "metadata_base_item_id": m["base_item_id"], "metadata_system": m["system"],
             "metadata_base_source": m["base_source"], "metadata_base_trust": m["base_trust"],
             "metadata_template_id": m.get("template_id"), "metadata_reading_converse": m.get("reading_converse"),
             "metadata_strata": m["strata"],
             "metadata_disguised_text": dis[m["sentence_id"]]["text"],
             "metadata_disguised_fol": dis[m["sentence_id"]]["fol"].get(m["candidate_fol"]),
             "metadata_disguised_reference_fol": dis[m["sentence_id"]]["fol"].get(m["base_fol"])}
        if is_c:
            e.update({"metadata_control_type": m["control_type"], "metadata_subtype": m["subtype"],
                      "metadata_verified": m["verified"], "metadata_rename_map": m.get("rename_map"), "metadata_error_ops": []})
        else:
            e.update({"metadata_operator": m["operator"], "metadata_subtype": m["subtype"],
                      "metadata_position_polarity": m["position_polarity"], "metadata_polarity_method": m["polarity_method"],
                      "metadata_matched_pair_id": m["matched_pair_id"], "metadata_matched_pair_complete": m["matched_pair_complete"],
                      "metadata_edited_path": m["edited_path"], "metadata_edited_predicate": m["edited_predicate"],
                      "metadata_donor_item_id": m["donor_item_id"], "metadata_error_ops": [m["operator"]]})
        ex.append(e)
    groups.append({"dataset": "perturb_suite", "examples": ex})
    # ---- adjudicator_check
    chk = {r["item_id"]: r for r in (check or {}).get("rows", [])}
    ex = []
    for it in check_items:
        inp = {"text": it["text"], "candidate_fol": it["candidate_fol"], "reference_fol": it["reference_fol_weak"],
               "reference_fol_weak": it["reference_fol_weak"], "reference_fol_strong": it["reference_fol_strong"],
               "system": it["system"], "prompt_variant": "none"}
        c = chk.get(it["item_id"], {})
        ex.append({"input": json.dumps(inp, ensure_ascii=False), "output": it["known_label"], "metadata_fold": "ADJ_CHECK",
                   "metadata_item_id": it["item_id"], "metadata_sentence_id": it["sentence_id"], "metadata_system": it["system"],
                   "metadata_operator": it["operator"], "metadata_subtype": it["subtype"], "metadata_control_type": it["control_type"],
                   "metadata_position_polarity": it["position_polarity"], "metadata_template_id": it["template_id"],
                   "metadata_adj_verdict": c.get("verdict"), "metadata_adj_ops": c.get("ops"),
                   "metadata_adj_status": "DONE" if c.get("verdict") else "PENDING_OPENROUTER_KEY_LIMIT"})
    groups.append({"dataset": "adjudicator_check", "examples": ex})
    meta = {"name": "R_COMP + PERTURB (run_u75jRHUss0zo, invention iter 2, gen_art_dataset_3)",
            "description": "Long composed sentences with references trusted by construction (weak/strong exception readings) "
                           "and a typed-perturbation suite with matched DOWN/UP positions; see dataset_card.md.",
            "workspace": str(ROOT), "prereg": "prereg_rcomp.json", "item_id_recipe": "sha1(system|norm(text)|raw_output)[:16]",
            "groups": {g["dataset"]: len(g["examples"]) for g in groups},
            "rcomp_candidates_status": "present" if rows else "PENDING: OpenRouter shared key hit its daily limit before generation; run ./run_all.sh"}
    dump(W / "assembled.json", {"metadata": meta, "datasets": groups})
    # ---- statistics for the card
    st = {"groups": meta["groups"], "disguise_guard": guard, "e_l25_error_rates": e_l25_error_rates(),
          "lexicon": {k: lex[k] for k in ("n_entries", "n_usable_not_wrong", "audit_counts", "groups", "log")},
          "lexicon_check_log": json.loads((W / "lexicon_check_log.json").read_text()),
          "source_pool_log": json.loads((W / "source_pool_log.json").read_text()),
          "compose_log": json.loads((W / "compose_log.json").read_text()),
          "select_log": json.loads((W / "select_log.json").read_text()),
          "perturb_log": json.loads((W / "perturb_log.json").read_text())}
    lex_aud = Counter(e.get("audit") for e in lex["entries"])
    n_aud = lex_aud.get("OK", 0) + lex_aud.get("WRONG", 0)
    st["lexicon_audit_wrong_rate"] = wilson(lex_aud.get("WRONG", 0), n_aud)
    flu = [s["fluency"] for s in rs if s["fluency"] is not None]
    st["fluency_distribution"] = dict(Counter(flu)) if flu else "PENDING"
    aud = [s for s in rs if s["audit_status"] == "AUDITED"]
    st["reference_audit_flag_rate_selected"] = wilson(sum(s["ref_flagged"] for s in aud), len(aud)) if aud else "PENDING"
    pre_a = load_jsonl(RAW / "ref_audit_items.jsonl")
    st["reference_audit_flag_rate_preselect"] = wilson(sum(r["ref_flagged"] for r in pre_a), len(pre_a)) if pre_a else "PENDING"
    st["per_template"] = dict(Counter((s["batch"], s["template_id"]) for s in rs).items()) and \
        {f"{b}:{t}": n for (b, t), n in Counter((s["batch"], s["template_id"]) for s in rs).items()}
    st["exception_type"] = dict(Counter(str(s["exception_type"]) for s in rs if s["batch"] == "main"))
    st["word_bins"] = dict(Counter(s["word_bin"] for s in rs if s["batch"] == "main"))
    st["words_mean_main"] = round(sum(s["words"] for s in rs if s["batch"] == "main") / max(1, sum(s["batch"] == "main" for s in rs)), 2)
    st["sort_groups_main"] = dict(Counter(s["sort_group"] for s in rs if s["batch"] == "main"))
    st["negated_condition_share_main"] = round(sum(s["negated_condition"] is not None for s in rs if s["batch"] == "main") / 250, 3)
    # perturb
    st["perturb_op_pol"] = {f"{k[0]}:{k[1]}": v for k, v in sorted(Counter((m["select_key"], m["position_polarity"]) for m in pert).items())}
    st["perturb_by_base_source"] = dict(Counter(m["base_source"] for m in pert))
    st["controls_by_type"] = dict(Counter(c["subtype"] for c in ctrl))
    st["controls_by_base_source"] = dict(Counter(c["base_source"] for c in ctrl))
    pairs = Counter(m["matched_pair_id"] for m in pert)
    st["matched_pairs"] = {"complete": sum(v == 2 for v in pairs.values()), "single": sum(v == 1 for v in pairs.values())}
    cov = defaultdict(lambda: [0, 0])
    for m in pert:
        cov[m["select_key"]][0 if m["matched_pair_complete"] else 1] += 1
    st["matched_pair_coverage_by_op"] = {k: {"rows_in_complete_pairs": v[0], "rows_unpaired": v[1]} for k, v in sorted(cov.items())}
    # costs
    led = load_jsonl(ROOT / "cost_ledger.jsonl")
    st["cost_by_phase"] = {k: round(v, 4) for k, v in Counter({}).items()}
    cb = defaultdict(float)
    nb = Counter()
    for r in led:
        cb[r["phase"]] += r.get("cost_usd", 0.0); nb[r["phase"]] += 1
    st["cost_by_phase"] = {k: {"usd": round(v, 4), "calls": nb[k]} for k, v in cb.items()}
    st["cost_total_usd"] = round(sum(cb.values()), 4)
    st["adjudicator_check"] = {k: v for k, v in (check or {}).items() if k != "rows"} if check else "PENDING"
    st["sibling_gate_status"] = sibling_gate_status()
    if rows:
        st["candidates"] = candidate_stats(rows, sents)
        st["testability"] = json.loads((W / "testability.json").read_text())
    dump(W / "stats.json", st)
    logger.info(f"assembled: {meta['groups']}; cost ${st['cost_total_usd']}")


def candidate_stats(rows: list[dict], sents: dict) -> dict:
    out = {}
    out["final_label"] = dict(Counter(r["final_label"] for r in rows))
    out["tier"] = dict(Counter(r["label_tier"] for r in rows))
    out["solver_label"] = dict(Counter(r["solver_label"] for r in rows))
    tt = defaultdict(Counter)
    for r in rows:
        s = sents[r["sentence_id"]]
        tt[f"{s['template_id']}|{s['exception_type']}|{r['label_tier']}"][r["final_label"]] += 1
    out["template_x_exception_x_tier"] = {k: dict(v) for k, v in sorted(tt.items())}
    cor = [r for r in rows if r["final_label"] == "CORRECT"]
    out["weak_vs_strong_tierA"] = dict(Counter(r.get("solver_matched_reading") for r in cor if r["label_tier"] == "A"))
    out["weak_vs_strong_tierB_modulo_vocab"] = dict(Counter(r.get("solver_matched_reading_modulo_vocab") for r in cor if r["label_tier"] == "B"))
    t8 = [r for r in rows if sents[r["sentence_id"]]["template_id"] == "T8" and r["parse_ok"]]
    out["only_if_converse_rate_T8"] = wilson(sum(bool(r.get("solver_only_if_converse")) for r in t8), len(t8))
    conf = Counter((r["solver_label"], r["adj_verdict"]) for r in rows if r["adj_verdict"])
    out["solver_vs_adjudicator"] = {f"{a}|{b}": n for (a, b), n in conf.items()}
    p4 = [r for r in rows if r.get("adj_priority") == 4 and r["adj_verdict"] in ("FAITHFUL", "UNFAITHFUL")]
    out["solver_error_precision_P4"] = wilson(sum(r["adj_verdict"] == "UNFAITHFUL" for r in p4), len(p4))
    vg = [r for r in rows if r["solver_label"] == "VOCAB_GRAN" and r["adj_verdict"] in ("FAITHFUL", "UNFAITHFUL")]
    out["lex_anchored_vs_adjudicator"] = {f"{a}|{b}": n for (a, b), n in Counter((r.get("solver_lex_anchored_vocab"), r["adj_verdict"]) for r in vg).items()}
    per = defaultdict(Counter)
    for r in rows:
        if r["label_tier"] in ("A", "B") and r["final_label"] in ("CORRECT", "ERROR") and not r["reading_choice"]:
            per[f"{r['slot']}:{r['prompt_variant']}"][r["final_label"]] += 1
    out["error_rate_per_system"] = {k: {"n": v["CORRECT"] + v["ERROR"], "error_rate": round(v["ERROR"] / (v["CORRECT"] + v["ERROR"]), 3)}
                                    for k, v in sorted(per.items())}
    out["unparseable_per_system"] = dict(Counter(f"{r['slot']}:{r['prompt_variant']}" for r in rows if r["final_label"] == "UNPARSEABLE"))
    out["unresolved"] = sum(r["final_label"] == "UNRESOLVED" for r in rows)
    out["adj_pending"] = sum(r["adj_pending"] for r in rows)
    return out


if __name__ == "__main__":
    main()
