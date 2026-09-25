"""skeleton_iter5.md: §5 headings, a reasoning block, and table shells whose cells name the sibling
output file::field ({{file::json.path}}). At finish, glob the sibling workspaces and record which named
files exist (path, sha256, mtime, top-level keys) in skeleton_resolution.json; shell fields that do not
exist are flagged. Confirmatory numbers are filled ONLY when the file AND its seal marker exist."""
from __future__ import annotations

import datetime as dt
import glob
import hashlib
import json
import re
from pathlib import Path

from src import io_locators as L
from src.ctx import Ctx

GS5 = f"{L.RUN}/iter_5/gen_strat/gen_strat_1/.terminal_claude_agent_struct_out.json"
HYP = f"{L.RUN}/iter_4/upd_hypo/upd_hypo/.terminal_claude_agent_struct_out.json"
SIB = f"{L.RUN}/iter_5/gen_art"
SELF_NAME = "gen_art_evaluation_4"

FILES = ["confirm_verdict_E2A.json", "confirm_verdict_E2B.json", "union_longpool.json", "confirm_verdict_rcomp.json",
         "freeze/selection.json", "freeze/gg_gate.json", "freeze/CONSENSUS_FREEZE_READY.json", "hmech_E2.json", "improve_E2.json",
         "rename_E2.json", "e2/E2_DRIFT_DECISION.json", "e2/E2A_FINAL_READY.json", "e2b/E2B_FINAL_READY.json", "score_seal.json",
         "score_seal_rcomp.json", "judges_costmatched.jsonl", "judge_frontier.jsonl", "screen_E.json", "gg_dev.json"]
SEALS = {"confirm_verdict_E2A.json": ["e2/E2A_FINAL_READY.json", "score_seal.json"],
         "confirm_verdict_E2B.json": ["e2b/E2B_FINAL_READY.json", "score_seal.json"],
         "union_longpool.json": ["e2b/E2B_FINAL_READY.json"],
         "confirm_verdict_rcomp.json": ["score_seal_rcomp.json"]}

SHELLS = {
    "§5.2 Drift gate (E2 panel, pinned providers)": [
        ("decision (PASS/FAIL)", "e2/E2_DRIFT_DECISION.json::decision"),
        ("drift criteria (track-H flag rates etc.)", "e2/E2_DRIFT_DECISION.json::criteria"),
        ("replayed judgements / per-member agreement", "e2/E2_DRIFT_DECISION.json::n_replayed|per_member_agreement"),
        ("pinned provider per panel model", "e2/E2_DRIFT_DECISION.json::pinned_providers")],
    "§5.3 E2-A long-pool confirmation (PRIMARY, pre-declared)": [
        ("Δ strat c_score_align − flash-lite disguised [CI]", "confirm_verdict_E2A.json::longpool.delta_strat_flashlite_disg.ci"),
        ("Δ vs flash-lite original", "confirm_verdict_E2A.json::longpool.delta_strat_flashlite_orig.point"),
        ("Δ vs gpt-4.1-nano", "confirm_verdict_E2A.json::longpool.delta_strat_nano.point"),
        ("nested [S4_E2 + c] − S4_E2 [CI]", "confirm_verdict_E2A.json::nested.delta_strat.ci"),
        ("L25 alone Δ [CI] (MDE stated)", "confirm_verdict_E2A.json::L25.delta_strat_flashlite_disg.ci"),
        ("DT sign", "confirm_verdict_E2A.json::DT.delta_sign"),
        ("n (usable sentences / rows) and completed fraction per stratum", "confirm_verdict_E2A.json::n"),
        ("verdict", "confirm_verdict_E2A.json::verdict")],
    "§5.4 E2-B replication, union and heterogeneity": [
        ("E2-B long-pool Δ [CI]", "confirm_verdict_E2B.json::longpool.delta_strat_flashlite_disg.ci"),
        ("union long-pool Δ [CI]", "union_longpool.json::union.delta_strat_flashlite_disg.ci"),
        ("between-sample heterogeneity", "union_longpool.json::heterogeneity"),
        ("cost-matched judge Δ", "confirm_verdict_E2B.json::costmatched.delta"),
        ("frontier ratio [CI], 300-row subsample", "confirm_verdict_E2B.json::frontier.ratio.ci")],
    "§5.5 R_COMP FREE, criterion (c)": [
        ("gloss gate balanced accuracy", "confirm_verdict_rcomp.json::gloss_gate.balanced_accuracy"),
        ("CORRECT / ERROR rows (untouched)", "confirm_verdict_rcomp.json::labels.counts_untouched"),
        ("within-template Δ vs flash-lite disguised [CI]", "confirm_verdict_rcomp.json::criterion_c.disg.ci"),
        ("within-template Δ vs flash-lite original [CI]", "confirm_verdict_rcomp.json::criterion_c.orig.ci"),
        ("with/without out-of-family form classes", "confirm_verdict_rcomp.json::sensitivity.excl_out_of_family"),
        ("verdict", "confirm_verdict_rcomp.json::verdict")],
    "§5.6 H-MECH (i)–(iv) on E2 labels": [
        ("(i) share of non-agreeing peers of CORRECT labelled ERROR", "hmech_E2.json::i.share_peer_error"),
        ("(ii) SCATTER ratio", "hmech_E2.json::ii.scatter_ratio"),
        ("(iii) NET Δ(e+d) [CI]", "hmech_E2.json::iii.net_delta.ci"),
        ("(iv) exact vs ALIGN d and e (MR-type, ADD/DROP)", "hmech_E2.json::iv.align_vs_exact")],
    "§5.7 H-IMPROVE (dev screen → frozen → E2)": [
        ("variants screened / winner or NONE", "freeze/selection.json::winner"),
        ("screen table (E long pool, L25, CTRL)", "screen_E.json::delta_vs_V0|variants"),
        ("winner − V0 on E2 long pool [CI]", "improve_E2.json::delta_vs_V0.ci")],
    "§5.8 H-RENAME / GG": [
        ("GG dev gate PASS/FAIL (gloss model id, prompt sha)", "freeze/gg_gate.json::status|gate.pass"),
        ("RENAME_SYN paired flip on E2 CORRECT", "rename_E2.json::RENAME_SYN.flip"),
        ("c_score_align rename FA and flip on E2", "rename_E2.json::c_score_align")],
    "§5.9 Complexity, coverage, cost, system-level τ-b": [
        ("d / e slopes over words and conditions", "confirm_verdict_E2A.json::complexity"),
        ("coverage (unparseables in denominator)", "confirm_verdict_E2A.json::coverage"),
        ("$ and seconds per candidate, FULL vs MARGINAL", "confirm_verdict_E2A.json::cost"),
        ("system-level τ-b (13 system × variant rows)", "confirm_verdict_E2A.json::system_level.tau_b")],
    "§5.10 Verdict table": [
        ("H-PRIMARY", "confirm_verdict_E2A.json::verdict"), ("criterion (c)", "confirm_verdict_rcomp.json::verdict"),
        ("H-MECH (i)–(iv)", "hmech_E2.json::verdicts"), ("H-IMPROVE", "improve_E2.json::verdict"), ("H-RENAME", "rename_E2.json::verdict")],
}


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _has_path(d, dotted: str) -> bool:
    try:
        L._walk_key(d, dotted)
        return True
    except (L.NotFound, KeyError, IndexError, TypeError):
        return False


def resolve_siblings() -> dict:
    found = {}
    for f in FILES:
        hits = [p for p in glob.glob(f"{SIB}/*/{f}") + glob.glob(f"{SIB}/*/*/{f}") if f"/{SELF_NAME}/" not in p]
        recs = []
        for h in sorted(set(hits)):
            p = Path(h)
            keys = None
            if p.suffix == ".json":
                try:
                    keys = list(json.loads(p.read_text()).keys())[:60]
                except (json.JSONDecodeError, AttributeError, UnicodeDecodeError):
                    keys = "UNREADABLE_OR_NOT_OBJECT"
            recs.append(dict(path=h, sha256=_sha(p), mtime=dt.datetime.fromtimestamp(p.stat().st_mtime, dt.timezone.utc).isoformat(), top_level_keys=keys))
        found[f] = recs
    return found


def write_skeleton(c: Ctx, ws: Path) -> dict:
    gs = json.loads(L._read_text(GS5))["strategies"][0]
    rv = json.loads(L._read_text(L.REVIEW))
    hyp = json.loads(L._read_text(HYP))["hypothesis"]
    c.add("rv4_score", rv["score"], "0", f"{L.REVIEW} :: score", "iter-4 review score")
    c.add("rv4_n", len(rv["critiques"]), "0", f"{L.REVIEW} :: len(critiques)", "iter-4 review critiques")
    caps = []
    for i, a in enumerate(gs["artifact_directions"]):
        m = re.search(r"[Hh]ard cap \$(\d+(?:\.\d+)?)", a["approach"])
        cid = c.add(f"i5_cap_{i}", float(m.group(1)) if m else 0.0, "$0.0", f"{GS5} :: artifact_directions[{i}].approach regex 'Hard cap $x' (0 if none: this $0 evaluation)", f"iter-5 cap {i}")
        caps.append(f"| {a['type']} | {a['objective'][:120].replace('|', '/')}… | {c.v(cid)} |")
    i0, i1 = hyp.find("4. SUCCESS CRITERIA"), hyp.find("5. PAPER OBLIGATIONS")
    crit = hyp[i0:i1].rsplit("=====", 1)[0].strip() if i0 >= 0 else "NOT FOUND in hypothesis"
    sib = resolve_siblings()
    resolution = {"globbed_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(), "files": sib, "shell_fields": []}
    body = []
    for head, cells in SHELLS.items():
        rows = []
        for label, ref in cells:
            f, field = ref.split("::")
            recs = sib.get(f, [])
            status, filled = "FILE_MISSING", f"{{{{{ref}}}}}"
            if recs:
                p = Path(recs[-1]["path"])
                try:
                    d = json.loads(p.read_text())
                    alts = field.split("|")
                    field = next((a for a in alts if _has_path(d, a)), alts[0])
                    ok = _has_path(d, field)
                except (json.JSONDecodeError, UnicodeDecodeError):
                    d, ok = None, False
                tok_ok = True
                if f.startswith("e2/") or f.startswith("e2b/"):
                    tok_ok = isinstance(d, dict) and str(d.get("token", "")).startswith("aii_iter5_")
                if f.startswith("freeze/"):
                    rd = [r for r in sib.get("freeze/CONSENSUS_FREEZE_READY.json", []) if Path(r["path"]).parent == p.parent]
                    tok_ok = bool(rd) and json.loads(Path(rd[0]["path"]).read_text()).get("token") == "aii_iter5_consensus_freeze_v1"
                status = "FIELD_PRESENT" if ok else "FIELD_MISSING (proposed name; resolve at paper time)"
                seals = SEALS.get(f, [])
                sealed = all(any(Path(r["path"]).parent == p.parent or Path(r["path"]).parent.parent == p.parent for r in sib.get(s, [])) for s in seals) if seals else True
                if ok and sealed and tok_ok and d is not None:
                    filled = f"{json.dumps(L._walk_key(d, field))[:120]} (from `{p}`)"
                    status += "; FILLED (seal present)"
                elif ok:
                    status += "; NOT FILLED (seal marker or token missing)"
            resolution["shell_fields"].append(dict(section=head, label=label, ref=ref, status=status))
            rows.append(f"| {label} | {filled} | {status} |")
        body.append(f"### {head}\n\n| quantity | value (shell) | resolution |\n|-|-|-|\n" + "\n".join(rows))
    md = f"""# §5 Iteration 5 — skeleton (cells are `{{{{file::json.path}}}}` shells)

## §5.1 Reasoning block

- The iteration-4 review scored the record {c.v('rv4_score')} (blocking) with {c.v('rv4_n')} critiques; the corrected record (`record_final.md`, this artifact) closes them with file-sourced text.
- Move: **{gs['title']}** — DEEPEN on the one live lead, frozen `c_score_align`; E is development data, E2 / E2-B / R_COMP FREE are the untouched confirmation data.
- Predictions (strategy, stated in advance): {gs['expected_outcome'][:900]}
- Gates: the CONFIRM / PARTIAL / DISCONFIRM rules below (verbatim from the hypothesis §4), the drift gate, the freeze markers (token-checked).
- Planned artifacts and caps (iteration-5 strategy):

| type | objective (truncated) | cap |
|-|-|-|
{chr(10).join(caps)}

## Decision rules (verbatim, hypothesis §4)

```
{crit}
```

""" + "\n\n".join(body) + f"""

Resolution of every shell cell: `skeleton_resolution.json` (globbed `{SIB}/*/`; this artifact's own workspace excluded). A value is filled only if the file exists AND its seal marker exists; otherwise the `{{{{…}}}}` placeholder stays.
"""
    (ws / "skeleton_iter5.md").write_text(md)
    (ws / "skeleton_resolution.json").write_text(json.dumps(resolution, indent=1))
    return resolution
