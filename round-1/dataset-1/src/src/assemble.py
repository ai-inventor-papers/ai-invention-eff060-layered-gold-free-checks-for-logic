#!/usr/bin/env python3
"""STEP 5d/5f + 7a: combine auto labels, (optional) panel votes and reference audit into the final dataset.

The FINAL LABEL RULE (plan 5f) is applied wherever panel votes exist. Where they do not (panel blocked by the
shared OpenRouter key's daily limit), rows keep solver-only labels:
  auto CORRECT -> CORRECT, auto ERROR(ops) -> ERROR(ops)   (tier A; 'A_unaudited_ref' while the reference is unaudited)
  auto VOCAB_GRAN / COMPOUND / TIMEOUT_UNKNOWN -> UNRESOLVED (tier 'none': needs the panel)
  UNPARSEABLE -> UNPARSEABLE (kept in every denominator)
Outputs: work/assembled.json (4 groups, exp_sel_data_out shape), screen_adjudicated_labels.json, work/label_report.json.
"""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

from loguru import logger

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "labeller"))
sys.setrecursionlimit(10000)
from normalise import normalise  # noqa: E402
from screen import norm_screen  # noqa: E402
from disguise import Disguiser  # noqa: E402

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(ROOT / "logs" / "assemble.log", level="DEBUG")
W = ROOT / "work"
MEMBERS = ["P1", "P3", "R1"]
MEMBER_MODEL = {"P1": "anthropic/claude-haiku-4.5", "P3": "z-ai/glm-4.6", "R1": "moonshotai/kimi-k2-0905"}


def load_jsonl(p):
    p = Path(p)
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()] if p.exists() else []


def maj(votes: dict) -> tuple[int, int, int]:
    f = sum(1 for v in votes.values() if v["faithful"])
    return f, len(votes) - f, len(votes)


def final_rule(auto: str, votes: dict, ref_status: str) -> dict:
    """Plan 5f. votes = {member: {faithful, ops, conf}} for the row's class (may be empty)."""
    nf, nu, n = maj(votes)
    ops = sorted({o for v in votes.values() if not v["faithful"] for o in v.get("ops", [])})
    have = n >= 2
    if auto == "UNPARSEABLE":
        return {"final_label": "UNPARSEABLE", "label_tier": "-", "label_source": "parser"}
    if ref_status in ("NO_TRUSTED_REFERENCE", "DISPUTED_REFERENCE"):
        if nf >= 2:
            return {"final_label": "CORRECT", "label_tier": "C", "label_source": "panel_only"}
        if nu >= 2:
            return {"final_label": "ERROR", "error_ops": ops, "label_tier": "C", "label_source": "panel_only"}
        return {"final_label": "CONTESTED" if have else "UNRESOLVED", "label_tier": "C" if have else "none", "label_source": "panel_only"}
    unaudited = ref_status.startswith("UNAUDITED")
    tier_a = "A_unaudited_ref" if unaudited else "A"
    if auto == "CORRECT":
        return {"final_label": "CORRECT", "label_tier": tier_a, "label_source": "solver", "panel_dissent": nu >= 2}
    if auto == "ERROR":
        if nf >= 2:
            return {"final_label": "CONTESTED", "label_tier": tier_a, "label_source": "solver_vs_panel"}
        return {"final_label": "ERROR", "label_tier": tier_a, "label_source": "solver" if not have else "solver+panel"}
    if auto == "REFERENCE_SELF":  # the MALLS GPT-4 gold as a system: label = blind gold audit
        if nf >= 2:
            return {"final_label": "CORRECT", "label_tier": "B", "label_source": "panel_only"}
        if nu >= 2:
            return {"final_label": "ERROR", "error_ops": ops, "label_tier": "B", "label_source": "panel_only"}
        return {"final_label": "CONTESTED" if have else "UNRESOLVED", "label_tier": "B" if have else "none", "label_source": "panel_only"}
    # VOCAB_GRAN / COMPOUND / TIMEOUT_UNKNOWN
    if not have:
        return {"final_label": "UNRESOLVED", "label_tier": "none", "label_source": "pending_panel"}
    if nf >= 2:
        return {"final_label": "CORRECT", "correct_not_equivalent": True, "label_tier": "B", "label_source": "solver+panel"}
    if nu >= 2:
        head = "MEANING_RENAME" if auto == "VOCAB_GRAN" else "COMPOUND"
        return {"final_label": "ERROR", "error_ops": [head] + ops, "label_tier": "B", "label_source": "solver+panel"}
    return {"final_label": "CONTESTED", "label_tier": "B", "label_source": "solver+panel"}


def item_id(system: str, text: str, raw: str) -> str:
    return hashlib.sha1((system + "|" + norm_screen(text) + "|" + raw).encode()).hexdigest()[:16]


def heldout():
    sents = {s["sentence_id"]: s for s in json.loads((W / "sentences.json").read_text())}
    gens = {}
    for g in load_jsonl(ROOT / "raw" / "generations.jsonl"):
        if g.get("raw_output") is None or (g["slot"] == "G2" and g["prompt_variant"] == "zeroshot_v1"):
            continue
        gens[(g["sentence_id"], f"{g['slot']}|{g['prompt_variant']}")] = g
    for c in load_jsonl(ROOT / "raw" / "ccg2lambda_candidates.jsonl"):
        gens[(c["sentence_id"], "CCG|none")] = c
    labs = {r["sentence_id"]: r for r in load_jsonl(W / "labels_heldout.jsonl")}
    relabs = {r["sentence_id"]: r for r in load_jsonl(W / "labels_heldout_repaired.jsonl")}
    refs_rep = json.loads((W / "reference_overrides.json").read_text()) if (W / "reference_overrides.json").exists() else {}
    no_ref = set(json.loads((W / "no_trusted_reference.json").read_text())) if (W / "no_trusted_reference.json").exists() else set()
    panel = {r["sentence_id"]: r for r in load_jsonl(W / "panel_heldout.jsonl")}
    rows, sent_rows = [], []
    for sid in sorted(sents):
        s = sents[sid]
        lab = labs.get(sid)
        if lab is None or "error" in lab:
            logger.warning(f"no labels for {sid}")
            continue
        pv = panel.get(sid, {})
        votes = pv.get("votes", {})
        ref_cid = f"{sid}:c0"
        rv = {m: v for m, v in votes.get(ref_cid, {}).items() if m in MEMBERS}
        nf, nu, n = maj(rv)
        is_malls = s["source"].startswith("MALLS")
        if n >= 2 and nf >= 2:
            ref_status, audit = ("GOLD_PANEL_OK" if is_malls else "TRUSTED_AGREED"), "FAITHFUL"
        elif n >= 2 and nu >= 2:
            audit = "UNFAITHFUL"
            if is_malls:
                ref_status = "PANEL_REPAIRED" if sid in refs_rep else ("NO_TRUSTED_REFERENCE" if sid in no_ref else "GOLD_WRONG_UNREPAIRED")
            else:
                ref_status = "DISPUTED_REFERENCE"
        else:
            audit = "PENDING" if n < 2 else "SPLIT"
            ref_status = "UNAUDITED_MALLS_GPT4_GOLD" if is_malls else "UNAUDITED_AGREED_FOLIO"
        if ref_status == "GOLD_WRONG_UNREPAIRED":
            ref_status = "NO_TRUSTED_REFERENCE"
        use_lab = relabs.get(sid, lab) if ref_status == "PANEL_REPAIRED" else lab
        reference = refs_rep.get(sid, s["reference_fol"]) if ref_status == "PANEL_REPAIRED" else s["reference_fol"]
        amb_votes = [pv.get("ambiguous", {}).get(m) for m in MEMBERS if m in pv.get("ambiguous", {})]
        reading_choice = sum(bool(a) for a in amb_votes) >= 2
        # disguise over ALL formulas of the sentence (same construction as the panel run)
        cand_keys = sorted(k for (ss, k) in gens if ss == sid)
        if is_malls:
            cand_keys.append("GOLD|none")
        fol_of = {}
        for k in cand_keys:
            if k == "GOLD|none":
                fol_of[k] = s["reference_fol"]
            elif k == "CCG|none":
                fol_of[k] = gens[(sid, k)]["candidate_fol"]
            else:
                fol_of[k] = normalise(gens[(sid, k)]["raw_output"])[0]
        allf = [lab["reference"]] + [f for f in fol_of.values() if f]
        d = Disguiser(sid, s["text"], sorted(set(allf)))
        dtext = d.text(s["text"])
        cls_size = {c["class_idx"]: c["size"] for c in use_lab["classes"]}
        empty_cls = {c["class_idx"] for c in use_lab["classes"] if not c["rep_fol"].strip()}
        strata = {k: s.get(k) for k in ("words", "n_quant", "depth", "n_conditions", "text_conditions", "exception_type", "source_stratum", "ctrl_len_bin")}
        for k in cand_keys:
            slot, variant = k.split("|")
            if k == "GOLD|none":
                system, model, raw, gen = "malls_gpt4_gold", "gpt-4 (MALLS 2023 gold)", s["reference_fol"], {}
            elif k == "CCG|none":
                gen = gens[(sid, k)]; system, model, raw = "ccg2lambda", "ccg2lambda", gen["raw_output"]
            else:
                gen = gens[(sid, k)]; system, model, raw = gen["system"], gen["model"], gen["raw_output"]
            lr = dict(use_lab["rows"].get(k, {}))
            if not (fol_of.get(k) or "").strip():  # empty output: fol.parse('') wrongly succeeds -> force UNPARSEABLE
                lr = {"auto_label": "UNPARSEABLE", "class_idx": None, "parse_error": "empty"}
            auto = lr.get("auto_label", "UNPARSEABLE")
            cidx = lr.get("class_idx")
            if k == "GOLD|none":
                auto = "REFERENCE_SELF" if ref_status != "PANEL_REPAIRED" else auto
                cidx = 0 if ref_status != "PANEL_REPAIRED" else cidx
            cid = f"{sid}:c{cidx}" if cidx is not None else None
            # panel votes are per class of the ORIGINAL class collapse (reference-free); map through the candidate key
            orig_cidx = lab["rows"].get(k, {}).get("class_idx") if k != "GOLD|none" else 0
            cv = {m: v for m, v in votes.get(f"{sid}:c{orig_cidx}", {}).items() if m in MEMBERS} if orig_cidx is not None else {}
            fr = final_rule(auto, cv, ref_status)
            if ref_status == "NO_TRUSTED_REFERENCE":
                auto = "NO_REF" if auto != "UNPARSEABLE" else auto
            if reading_choice and fr["final_label"] in ("CORRECT", "ERROR", "CONTESTED"):
                fr["reading_choice"] = True
            fol = fol_of.get(k, "")
            try:
                dfol = d.formula(fol) if fol else None
            except Exception:  # noqa: BLE001
                dfol = None
            text_in = {"text": s["text"], "candidate_fol": fol, "reference_fol": reference, "system": system, "prompt_variant": variant}
            rows.append({
                "input": json.dumps(text_in, ensure_ascii=False),
                "output": fr["final_label"],
                "metadata_fold": "heldout",
                "metadata_item_id": item_id(system, s["text"], (raw or "").strip()),
                "metadata_sentence_id": sid,
                "metadata_system": system,
                "metadata_slot": slot,
                "metadata_family": gen.get("family", "openai-gpt4-2023" if k == "GOLD|none" else None),
                "metadata_system_class": "symbolic_eventsem" if k == "CCG|none" else ("reference_gold_as_system" if k == "GOLD|none" else "llm"),
                "metadata_generator_model_id": model,
                "metadata_prompt_variant": variant,
                "metadata_raw_output": raw,
                "metadata_normalisation_applied": gen.get("normalisation_applied"),
                "metadata_auto_label": auto,
                "metadata_equiv_status": lr.get("equiv_status"),
                "metadata_repair_ops": lr.get("repair_ops"),
                "metadata_repair_status": lr.get("repair_status"),
                "metadata_convention_flags": lr.get("convention_flags"),
                "metadata_panel_votes": cv or None,
                "metadata_final_label": fr["final_label"],
                "metadata_error_ops": fr.get("error_ops") if fr["final_label"] == "ERROR" and fr.get("error_ops") else (lr.get("repair_ops") if fr["final_label"] == "ERROR" else None),
                "metadata_label_tier": fr["label_tier"],
                "metadata_label_source": fr["label_source"],
                "metadata_addrop_only_suspect": bool(fr["final_label"] == "ERROR" and auto == "ERROR" and lr.get("repair_ops")
                                                     and set(lr["repair_ops"]) <= {"ADD", "DROP"}),
                "metadata_solver_lenient_label": {"CORRECT": "CORRECT", "VOCAB_GRAN": "CORRECT", "ERROR": "ERROR", "UNPARSEABLE": "UNPARSEABLE"}.get(auto, "UNRESOLVED"),
                "metadata_correct_not_equivalent": bool(fr.get("correct_not_equivalent")),
                "metadata_reading_choice": bool(fr.get("reading_choice")),
                "metadata_gold_audit_flag": audit,
                "metadata_reference_status": ref_status,
                "metadata_strata": strata,
                "metadata_disguised_text": dtext,
                "metadata_disguised_fol": dfol,
                "metadata_class_id": cid,
                "metadata_class_size": cls_size.get(cidx) if cidx is not None else None,
                "metadata_cost_usd": gen.get("cost_usd", 0.0),
                "metadata_finish_reason": gen.get("finish_reason"),
                "metadata_provider": gen.get("provider"),
            })
        sent_rows.append({
            "input": json.dumps({"text": s["text"], "reference_fol": reference}, ensure_ascii=False),
            "output": ref_status,
            "metadata_fold": "heldout",
            "metadata_sentence_id": sid,
            "metadata_source": s["source"],
            "metadata_original_reference_fol": s["reference_fol"],
            "metadata_ctrl_original_fol": s.get("original_fol"),
            "metadata_agreement_type": s.get("agreement_type"),
            "metadata_gold_audit_flag": audit,
            "metadata_gold_audit_votes": rv or None,
            "metadata_reading_choice": reading_choice,
            "metadata_strata": strata,
            "metadata_n_candidates": len(cand_keys),
            "metadata_n_classes": len(use_lab["classes"]) - len(empty_cls),
            "metadata_auto_label_counts": dict(Counter(use_lab["rows"][k].get("auto_label") for k in use_lab["rows"])),
            "metadata_disguised_text": dtext,
            "metadata_label_seconds": lab.get("secs"),
        })
    return rows, sent_rows


def screen():
    items = json.loads((W / "screen_items.json").read_text())
    labs = {r["sentence_id"]: r for r in load_jsonl(W / "labels_screen.jsonl")}
    panel = {r["sentence_id"]: r for r in load_jsonl(W / "panel_screen.jsonl")}
    th = {}
    p = W / "trackh_panel_rows.json"
    if p.exists():
        for r in json.loads(p.read_text()):
            th[r["id"]] = r
    rows, adj = [], {}
    for it in items:
        lab = labs.get(it["screen_sentence_id"])
        if lab is None:
            continue
        ref_bad = "error" in lab  # the screen reference itself does not parse -> no solver label possible
        lr = {} if ref_bad else lab["rows"].get(it["item_id"], {})
        auto = "REF_UNPARSEABLE" if ref_bad else lr.get("auto_label", "UNPARSEABLE")
        cidx = lr.get("class_idx")
        pv = panel.get(it["screen_sentence_id"], {})
        cv = {m: v for m, v in pv.get("votes", {}).get(f"{it['screen_sentence_id']}:c{cidx}", {}).items() if m in MEMBERS} if cidx is not None else {}
        if it["track"] == "H":
            t = th.get(str(it["record_id"]), {})
            cv = {m: {"faithful": v["orig_faithful"], "ops": v.get("orig_ops", []), "conf": None} for m, v in t.get("votes", {}).items() if m in MEMBERS}
        fr = final_rule(auto, cv, "SCREEN_REFERENCE") if auto != "REF_UNPARSEABLE" else \
            {"final_label": "NO_REFERENCE", "label_tier": "none", "label_source": "reference_unparseable"}
        if not cv and fr["label_tier"] in ("A",):
            fr["label_tier"] = "auto_only"
        if not cv and fr["final_label"] == "UNRESOLVED":
            fr["label_tier"] = "auto_only"
        reading = bool(it.get("ambiguous")) and it["track"] == "H" and fr["final_label"] != "CORRECT"
        addrop = bool(fr["final_label"] == "ERROR" and lr.get("repair_ops") and set(lr["repair_ops"]) <= {"ADD", "DROP"})
        rec = {"track": it["track"], "system": it["system"], "auto_label": auto, "equiv_status": lr.get("equiv_status"),
               "repair_ops": lr.get("repair_ops"), "repair_status": lr.get("repair_status"), "convention_flags": lr.get("convention_flags"),
               "panel_votes": cv or None, "final_label": fr["final_label"], "label_tier": fr["label_tier"],
               "reading_choice": reading, "addrop_only_suspect": addrop, "join_keys": it["join_keys"], "reference_fol": it["reference_fol"],
               "reference_source": it["reference_source"], "class_id": f"{it['screen_sentence_id']}:c{cidx}" if cidx is not None else None}
        adj[it["item_id"]] = rec
        rows.append({"input": json.dumps({"text": it["raw_text"], "candidate_fol": it["raw_fol"], "reference_fol": it["reference_fol"],
                                          "system": it["system"], "prompt_variant": "logiclm_released" if it["track"] == "L" else "human_original"}, ensure_ascii=False),
                     "output": fr["final_label"], "metadata_fold": "screen_audit", "metadata_item_id": it["item_id"],
                     "metadata_track": it["track"], "metadata_system": it["system"], "metadata_role": it["role"],
                     "metadata_record_id": it["record_id"], "metadata_screen_sentence_id": it["screen_sentence_id"],
                     "metadata_candidate_fol_normalised": it["candidate_fol_normalised"],
                     "metadata_normalisation_applied": it["normalisation_applied"],
                     "metadata_auto_label": auto, "metadata_equiv_status": lr.get("equiv_status"), "metadata_repair_ops": lr.get("repair_ops"),
                     "metadata_repair_status": lr.get("repair_status"), "metadata_convention_flags": lr.get("convention_flags"),
                     "metadata_panel_votes": cv or None, "metadata_final_label": fr["final_label"], "metadata_label_tier": fr["label_tier"],
                     "metadata_label_source": fr["label_source"], "metadata_reading_choice": reading, "metadata_addrop_only_suspect": addrop, "metadata_ambiguous_curated": it.get("ambiguous"),
                     "metadata_reference_source": it["reference_source"], "metadata_strata": it["strata"], "metadata_join_keys": it["join_keys"],
                     "metadata_class_id": rec["class_id"]})
    return rows, adj


def calibration():
    from panel import PROMPT_SHA1
    items = json.loads((W / "calibration_items.json").read_text())
    cache = load_jsonl(W / "panel_cache.jsonl")
    ver = defaultdict(dict)
    for r in cache:
        if r.get("parsed") and r["sentence_id"].startswith("calib|") and r["prompt_sha1"] == PROMPT_SHA1:
            for cid, v in r["verdicts"].items():
                ver[cid][r["member"]] = v
    rows = []
    for it in items:
        rows.append({"input": json.dumps({"text": it["text"], "candidate_fol": it["variant_fol"], "reference_fol": it["reference_fol"]}, ensure_ascii=False),
                     "output": it["gold"], "metadata_fold": "calibration", "metadata_subset": "synthetic_gate",
                     "metadata_calib_id": it["calib_id"], "metadata_sentence_id": it["sentence_id"], "metadata_variant_type": it["variant_type"],
                     "metadata_position": it["position"], "metadata_position_z3_profile": it.get("position_z3_profile"),
                     "metadata_z3_verified": it["z3_verified"], "metadata_rename_map": it.get("rename_map"),
                     "metadata_panel_verdicts_prompt_v2": ver.get(it["calib_id"]) or None})
    p = W / "trackh_panel_rows.json"
    if p.exists():
        for r in json.loads(p.read_text()):
            rows.append({"input": json.dumps({"text": r["text"], "original_fol": r["orig"], "corrected_fol": r["corr"]}, ensure_ascii=False),
                         "output": "ORIGINAL_UNFAITHFUL__CORRECTED_FAITHFUL", "metadata_fold": "calibration", "metadata_subset": "trackH_real_error_pairs",
                         "metadata_record_id": r["id"], "metadata_source": r["src"], "metadata_ambiguous_curated": r["ambiguous"],
                         "metadata_census_cls": r["census_cls"], "metadata_census_class": r["census_class"],
                         "metadata_panel_votes": r["votes"] or None, "metadata_panel_coverage": f"{len(r['votes'])}/3"})
    return rows


def main():
    h_rows, s_rows = heldout()
    sc_rows, adj = screen()
    cal = calibration()
    out = {"metadata": {"description": "Held-out NL->FOL faithfulness meta-evaluation set (run_u75jRHUss0zo, invention iter 1, dataset E). "
                                       "HELD-OUT: iteration 2 must not tune any threshold on heldout rows.",
                        "label_rule": "see dataset_card.md section 'Final label rule'", "panel_members": MEMBER_MODEL},
           "datasets": [{"dataset": "heldout_candidates", "examples": h_rows},
                        {"dataset": "heldout_sentences", "examples": s_rows},
                        {"dataset": "panel_calibration", "examples": cal},
                        {"dataset": "screen_audit", "examples": sc_rows}]}
    (W / "assembled.json").write_text(json.dumps(out, ensure_ascii=False))
    (ROOT / "screen_adjudicated_labels.json").write_text(json.dumps(adj, ensure_ascii=False, indent=0))
    logger.info(f"heldout rows {len(h_rows)} sentences {len(s_rows)} calibration {len(cal)} screen {len(sc_rows)}")
    logger.info(f"heldout final: {Counter(r['output'] for r in h_rows)}; tiers {Counter(r['metadata_label_tier'] for r in h_rows)}")
    logger.info(f"screen final: {Counter(r['output'] for r in sc_rows)}")


if __name__ == "__main__":
    main()
