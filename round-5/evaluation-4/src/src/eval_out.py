"""eval_out.json (exp_eval_sol_out): aggregate verification counts + one example per numbers.csv row."""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

from src.ctx import Ctx


def _key(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9_]", "_", s).strip("_")


def write_eval_out(ws: Path, c: Ctx, fails, ledger, checklist, ids, sp, aud, mut, skel, figs) -> dict:
    rows = c.rows
    claims = [r for r in rows if r.get("value") not in (None, "")]
    m = {}
    m["n_numbers_rows"] = len(rows)
    m["n_claims_checked"] = len(claims)
    m["n_match"] = sum(r["match_hyp_vs_file"] == "MATCH" for r in claims)
    m["n_mismatch_hyp_vs_file"] = sum(r["match_hyp_vs_file"] == "MISMATCH" for r in claims)
    m["n_not_found"] = sum(r["match_hyp_vs_file"] == "NOT_FOUND" for r in claims)
    m["n_ambiguous"] = sum(r["match_hyp_vs_file"] == "AMBIGUOUS" for r in claims)
    m["n_transcribed_rows"] = sum(r["match_hyp_vs_file"] == "TRANSCRIBED" for r in rows)
    m["n_computed_rows"] = sum(r["match_hyp_vs_file"] == "COMPUTED" for r in rows)
    m["n_paper_value_found"] = sum(r["match_paper_vs_file"] in ("MATCH", "MISMATCH") for r in claims)
    m["n_match_paper_vs_file"] = sum(r["match_paper_vs_file"] == "MATCH" for r in claims)
    m["n_mismatch_paper_vs_file"] = sum(r["match_paper_vs_file"] == "MISMATCH" for r in claims)
    m["n_not_in_paper"] = sum(r["match_paper_vs_file"] == "NOT_IN_PAPER" for r in claims)
    secs = Counter()
    for r in claims:
        tag = _key(re.sub(r"^(hyp|review|plan)\s*", "", str(r.get("sec"))).split()[0] if r.get("sec") else "other")
        secs[(tag, r["match_hyp_vs_file"] == "MATCH")] += 1
    for (tag, ok), n in secs.items():
        m[f"sec_{tag}_{'match' if ok else 'nonmatch'}"] = n
    for r in claims:
        if r.get("ps") and r["match_paper_vs_file"] in ("MATCH", "MISMATCH"):
            k = "paper_sec_" + _key(r["ps"].lstrip("#").strip().replace(".", "_").split()[0] if r["ps"].startswith("#" * 3) else "learned")
            m[f"{k}_{r['match_paper_vs_file'].lower()}"] = m.get(f"{k}_{r['match_paper_vs_file'].lower()}", 0) + 1
    m["reviewer_items_closed"] = sum(x["status"] == "CLOSED" for x in checklist)
    m["reviewer_items_partial"] = sum(x["status"] == "PARTIAL" for x in checklist)
    m["reviewer_items_total"] = len(checklist)
    m["n_placeholders_resolved"] = sum(x["status"] == "RESOLVED" for x in ids)
    m["n_placeholders_unresolved"] = sum(x["status"] == "UNRESOLVED" for x in ids)
    m["n_corrections_markers"] = len(c.markers)
    m["n_corrections_markers_original_found"] = sum(x["status"] == "OK" for x in c.markers)
    m["lint_failures"] = len(fails)
    m["audit_rederive_pass"] = aud["n_pass"]
    m["audit_rederive_checks"] = aud["n_checks"]
    m["audit_placebo_ci_covers_0_5"] = int(aud["placebo_shuffled_labels_c_csc"]["covers_0_5"])
    m["checker_mutation_caught"] = mut["caught"]
    m["checker_untouched_match"] = mut["untouched_match"]
    m["spend_iter4_evidenced_usd"] = sp["evidenced_iter4_artifacts_usd"]
    m["spend_window_evidenced_all_artifacts_usd"] = sp["evidenced_total_usd"]
    m["spend_iter4_unaccounted_usd"] = sp["unaccounted_usd"]
    for role, n in Counter(x["data_role"] for x in ledger).items():
        m[f"n_claims_ledger_{_key(role)}"] = n
    m["n_claims_ledger"] = len(ledger)
    m["skeleton_shell_fields"] = len(skel["shell_fields"])
    m["skeleton_fields_present"] = sum("FIELD_PRESENT" in x["status"] for x in skel["shell_fields"])
    m["skeleton_files_found"] = sum(1 for v in skel["files"].values() if v)
    m["n_figures"] = len(figs)
    m["n_numbers_rows_used_in_record"] = len(c.used)
    m["llm_calls"] = 0
    m["spend_usd_this_artifact"] = 0.0
    ex = []
    for r in rows:
        e = {"input": f"[{r.get('sec')}] {r.get('text')}" + (f" — claimed {r.get('value')}" + (f" {r.get('ci')}" if r.get('ci') else "") if r.get("value") else ""),
             "output": f"{r.get('source_value')}" + (f" {r.get('source_ci')}" if r.get("source_ci") else ""),
             "predict_paper_value": str(r.get("paper_value") or "NOT_IN_PAPER"),
             "predict_hypothesis_value": str(r.get("value") or ""),
             "metadata_claim_id": r["id"], "metadata_status": r.get("match_hyp_vs_file"),
             "metadata_paper_status": r.get("match_paper_vs_file"), "metadata_paper_line": str(r.get("paper_line") or ""),
             "metadata_source": r.get("locator"), "metadata_data_role": r.get("role"),
             "eval_match_hyp_vs_file": 1.0 if r.get("match_hyp_vs_file") in ("MATCH", "TRANSCRIBED", "COMPUTED") else 0.0,
             "eval_match_paper_vs_file": {"MATCH": 1.0, "MISMATCH": 0.0}.get(r.get("match_paper_vs_file"), -1.0)}
        ex.append(e)
    ck = [{"input": f"critique {x['critique']} ({x['category']}, {x['severity']}): {x['summary']}", "output": x["status"],
           "predict_action": x["action"], "metadata_anchor": x["section_anchor"], "metadata_sources": x["sources"],
           "metadata_note": x["note"], "eval_closed": 1.0 if x["status"] == "CLOSED" else 0.0} for x in checklist]
    cl = [{"input": x["claim"], "output": f"{x['value']} {x['CI']}".strip(), "predict_data_role": x["data_role"],
           "predict_confirming_file": x["confirming_file"], "metadata_confirming_field": x["confirming_field"],
           "metadata_verdict_rule": x["verdict_rule"], "metadata_n": x["n"], "metadata_numbers_ids": x["numbers_csv_ids"], "eval_is_confirmatory": 1.0 if x["data_role"] == "CONFIRM-PENDING" else 0.0, "eval_has_confirming_file": 0.0 if x["confirming_file"].startswith("none") else 1.0} for x in ledger]
    out = {"metadata": {"evaluation_name": "corrected record and paper-ready fixes (iter 5, eval 4)",
                        "description": "File-sourced verification of every hypothesis §0.2-0.3 and review number; paste-ready corrected sections; claims ledger; iter-5 skeleton; independent audit; checker mutation test. CPU only, $0.",
                        "record": "record_final.md", "numbers": "numbers.csv", "workspace": str(ws)},
           "metrics_agg": {k: (float(v) if isinstance(v, (int, float)) else 0.0) for k, v in m.items()},
           "datasets": [{"dataset": "numbers_check", "examples": ex}, {"dataset": "reviewer_checklist", "examples": ck},
                        {"dataset": "claims_ledger", "examples": cl}]}
    (ws / "eval_out.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    return out
