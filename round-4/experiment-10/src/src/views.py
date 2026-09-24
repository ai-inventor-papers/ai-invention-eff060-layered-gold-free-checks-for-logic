"""STAGE 1: label-blind data views.

Outputs (data/):
  perturb_view.jsonl   one row per PERTURB mutant / control + one BASE row per base (key 'PT:<item>' / 'PB:<base>'),
                       with text, candidate FOL, signature (display names, arity), sig_key, sig_shared_with_base.
                       Operator / label fields are carried but NOT used by any peer or scoring code.
  unique_sigs_perturb.jsonl  unique (text, sig_key) groups with their row keys and base_source.
  rcomp_free_view.jsonl FIREWALLED projection of exp-7 FREE rows (whitelist only; labels never read).
  rcomp_sig_view.jsonl  exp-7 SIG rows (development; all fields) + sentence text.
  free3_peers.json      matched UNCUED peers of the same three families (G4 deepseek, G6 phi-4, G7 gpt-4.1-mini, few-shot)
                        per E base (dataset E heldout_candidates) and per R_COMP base (exp-7 FREE, via whitelist).
results/sig_sharing.csv  the KEY STRUCTURAL FACT: per operator x base_source, share of rows sharing the base signature.
"""
from __future__ import annotations

import csv
import gc
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

from loguru import logger

SRC = Path(__file__).resolve().parent
ROOT = SRC.parent
sys.path.insert(0, str(SRC))
import csc_lib as L  # noqa: E402

RUN = Path("/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop")
E8 = RUN / "iter_3/gen_art/gen_art_experiment_8"
E7 = RUN / "iter_3/gen_art/gen_art_experiment_7"
DS3 = RUN / "iter_2/gen_art/gen_art_dataset_3/full_data_out.json"
DSE = RUN / "iter_1/gen_art/gen_art_dataset_1/full_data_out.json"
DATA = ROOT / "data"
RES = ROOT / "results"

FREE_WHITELIST = ("row_key", "item_id", "sentence_id", "template_id", "slot", "system", "family", "condition",
                  "candidate_fol", "parse_ok", "prompt_variant", "free_align_class_id", "free_hyb_class_id")


class FirewallError(KeyError):
    pass


class FreeRow(dict):
    """A FREE row holding ONLY whitelisted fields; asking for any other field raises FirewallError."""

    def __getitem__(self, k):
        if k not in FREE_WHITELIST:
            raise FirewallError(f"firewall: field {k!r} of a FREE row is not whitelisted")
        return dict.__getitem__(self, k)

    def get(self, k, default=None):
        if k not in FREE_WHITELIST:
            raise FirewallError(f"firewall: field {k!r} of a FREE row is not whitelisted")
        return dict.get(self, k, default)


def project_free(line: str) -> FreeRow | None:
    """json.loads then an immediate whitelist comprehension; the full dict is dropped at once. Non-FREE -> None."""
    d = json.loads(line)
    if d.get("condition") != "FREE":
        del d
        return None
    r = FreeRow({k: d[k] for k in FREE_WHITELIST if k in d})
    del d
    return r


def jl(p: Path) -> list[dict]:
    return [json.loads(x) for x in p.read_text().splitlines() if x.strip()] if p.exists() else []


def wjl(p: Path, rows) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def op_label(r: dict) -> str:
    if r.get("fold") == "BASE":
        return "BASE"
    if r.get("control_type"):
        return r["control_type"]
    if r.get("operator") == "ADD":
        return r.get("subtype") or "ADD"
    return r["operator"]


def sig_json(sig) -> list:
    return [[n, a] for n, a in sig]


def build_perturb_view() -> dict:
    rows = jl(E8 / "data" / "perturb_rows.jsonl")
    ds3 = json.loads(DS3.read_text())
    groups = {g["dataset"]: g["examples"] for g in ds3["datasets"]}
    suite = groups["perturb_suite"]
    rcomp_sent = {e["metadata_sentence_id"]: json.loads(e["input"]) for e in groups["rcomp_sentences"]}
    rename_map = {e["metadata_item_id"]: e.get("metadata_rename_map") for e in suite}
    del ds3, groups
    gc.collect()
    n_mut = sum(r["fold"] == "PERTURB" for r in rows)
    n_ctl = sum(r["fold"] == "PERTURB_CONTROL" for r in rows)
    bases = {r["base_item_id"] for r in rows}
    ids_rows, ids_ds3 = {r["item_id"] for r in rows}, {e["metadata_item_id"] for e in suite}
    counts = {"mutants": n_mut, "controls": n_ctl, "bases": len(bases), "suite_rows": len(suite),
              "item_ids_equal_dataset3": ids_rows == ids_ds3}
    logger.info(f"perturb_rows: {counts}")
    assert n_mut == 4234 and n_ctl == 868 and len(bases) == 300 and ids_rows == ids_ds3, counts
    # BASE rows from exp-8 PB rows (fol = the unmutated reference the mutants were built from)
    pb = {}
    for line in (E8 / "results" / "perturb_scores.jsonl").read_text().splitlines():
        if '"PB:' in line[:20]:
            x = json.loads(line)
            pb[x["base"]] = x
    base_rows = {}
    for r in rows:
        b = r["base_item_id"]
        if b in base_rows:
            continue
        x = pb[b]
        base_rows[b] = {"key": "PB:" + b, "item_id": b, "base_item_id": b, "sentence_id": r["sentence_id"],
                        "fold": "BASE", "operator": None, "op_fine": None, "subtype": None, "control_type": "BASE",
                        "polarity": None, "matched_pair_id": None, "base_source": r["base_source"],
                        "is_rcomp": r["base_source"] == "RCOMP", "strata": r["strata"], "text": r["text"],
                        "candidate_fol": x["fol"], "reference_fol": r["reference_fol"],
                        "reference_fol_weak": r.get("reference_fol_weak"), "reference_fol_strong": r.get("reference_fol_strong"),
                        "edited_predicate": None, "y": 0, "template_id": None}
    n_e = sum(not b["is_rcomp"] for b in base_rows.values())
    counts.update(bases_E=n_e, bases_RCOMP=len(base_rows) - n_e)
    assert n_e == 200 and len(base_rows) - n_e == 100, counts
    # the base's reference FOL must equal its row's reference FOL (sanity)
    mism = sum(1 for b in base_rows.values() if L.eq_exact(b["candidate_fol"], b["reference_fol"]) is not True)
    counts["base_fol_neq_reference"] = mism
    out = []
    for r in rows:
        tid = None
        if r["base_source"] == "RCOMP":
            tid = (r.get("strata") or {}).get("template_id")
        out.append({"key": "PT:" + r["item_id"], "item_id": r["item_id"], "base_item_id": r["base_item_id"],
                    "sentence_id": r["sentence_id"], "fold": r["fold"], "operator": r["operator"], "op_fine": r["op_fine"],
                    "subtype": r["subtype"], "control_type": r["control_type"], "polarity": r["polarity"],
                    "matched_pair_id": r["matched_pair_id"], "base_source": r["base_source"],
                    "is_rcomp": r["base_source"] == "RCOMP", "strata": r["strata"], "text": r["text"],
                    "candidate_fol": r["candidate_fol"], "reference_fol": r["reference_fol"],
                    "reference_fol_weak": r.get("reference_fol_weak"), "reference_fol_strong": r.get("reference_fol_strong"),
                    "edited_predicate": r.get("edited_predicate"), "rename_map": rename_map.get(r["item_id"]),
                    "y": 1 if r["fold"] == "PERTURB" else 0, "template_id": tid})
    for b in base_rows.values():
        if b["is_rcomp"]:
            b["template_id"] = (b.get("strata") or {}).get("template_id")
        out.append(b)
    base_sig = {}
    for r in out:
        sig = L.extract_signature(r["candidate_fol"])
        r["signature"] = sig_json(sig)
        r["sig_key"] = L.sig_key(sig)
        r["op_label"] = op_label(r)
        r["cand_parse_ok"] = L.parse(r["candidate_fol"]) is not None
        if r["fold"] == "BASE":
            base_sig[r["base_item_id"]] = r["sig_key"]
    for r in out:
        r["sig_shared_with_base"] = r["sig_key"] == base_sig[r["base_item_id"]]
    counts["unparseable_candidates"] = sum(not r["cand_parse_ok"] for r in out)
    # text consistency with dataset 3 for R_COMP bases
    miss = sum(1 for r in out if r["is_rcomp"] and r["sentence_id"] not in rcomp_sent)
    counts["rcomp_rows_sentence_missing_in_ds3"] = miss
    wjl(DATA / "perturb_view.jsonl", out)
    # unique (text, sig) groups
    grp = defaultdict(list)
    for r in out:
        grp[(r["text"], r["sig_key"])].append(r)
    uniq = []
    for (text, sk), rs in grp.items():
        rs_sorted = sorted(rs, key=lambda r: r["key"])
        uniq.append({"text": text, "sig_key": sk, "signature": rs_sorted[0]["signature"],
                     "row_keys": [r["key"] for r in rs_sorted], "is_rcomp": rs_sorted[0]["is_rcomp"],
                     "has_base": any(r["fold"] == "BASE" for r in rs), "sentence_id": rs_sorted[0]["sentence_id"],
                     "base_item_id": rs_sorted[0]["base_item_id"]})
    uniq.sort(key=lambda u: (u["is_rcomp"], u["sentence_id"], u["sig_key"]))
    wjl(DATA / "unique_sigs_perturb.jsonl", uniq)
    counts.update(n_rows_view=len(out), n_unique_sigs=len(uniq), n_unique_sigs_E=sum(not u["is_rcomp"] for u in uniq),
                  n_unique_sigs_RCOMP=sum(u["is_rcomp"] for u in uniq))
    # sig sharing table
    tab = defaultdict(lambda: {"n_rows": 0, "sigs": set(), "shared": 0})
    for r in out:
        src = "RCOMP" if r["is_rcomp"] else "E"
        for key in ((r["op_label"], src), (r["op_label"], "ALL")):
            t = tab[key]
            t["n_rows"] += 1
            t["sigs"].add((r["text"], r["sig_key"]))
            t["shared"] += int(r["sig_shared_with_base"])
    with (RES / "sig_sharing.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["op_label", "base_source", "n_rows", "n_unique_sigs", "n_new_sigs_vs_base", "share_sharing_base_sig"])
        for (op, src), t in sorted(tab.items()):
            w.writerow([op, src, t["n_rows"], len(t["sigs"]), t["n_rows"] - t["shared"], round(t["shared"] / t["n_rows"], 4)])
    logger.info(f"perturb view: {counts}")
    return counts


def build_rcomp_views() -> dict:
    ds3 = json.loads(DS3.read_text())
    rs = {e["metadata_sentence_id"]: json.loads(e["input"]) for g in ds3["datasets"] if g["dataset"] == "rcomp_sentences"
          for e in g["examples"]}
    del ds3
    gc.collect()
    # fallback text source (plan): exp 7's own sentence file, for sentence ids absent from dataset 3's final export
    n_fallback = 0
    for x in json.loads((E7 / "rcomp" / "work" / "rcomp_sentences.json").read_text()):
        if x["sentence_id"] not in rs:
            rs[x["sentence_id"]] = {"text": x["text"], "_source": "exp7_rcomp_work"}
            n_fallback += 1
    free, sig = [], []
    with (E7 / "results" / "rcomp_candidates.jsonl").open() as fh:
        for line in fh:
            if not line.strip():
                continue
            if '"condition": "FREE"' in line:
                r = project_free(line)
                if r is not None:
                    free.append(r)
            else:
                d = json.loads(line)
                if d.get("condition") == "SIG":
                    sig.append(d)
    n_text_missing = 0
    for r in free:
        t = rs.get(dict.__getitem__(r, "sentence_id"))
        if t is None:
            n_text_missing += 1
    for r in sig:
        t = rs.get(r["sentence_id"])
        r["text"] = t["text"] if t else None
        n_text_missing += t is None
        s = L.extract_signature(r["candidate_fol"]) if r.get("parse_ok") else []
        r["signature"] = sig_json(s)
        r["sig_key"] = L.sig_key(s)
    free_out = []
    for r in free:
        d = dict(r)
        t = rs.get(d["sentence_id"])
        d["text"] = t["text"] if t else None
        s = L.extract_signature(d["candidate_fol"]) if d.get("parse_ok") else []
        d["signature"] = sig_json(s)
        d["sig_key"] = L.sig_key(s)
        d["cand_parse_ok"] = L.parse(d["candidate_fol"]) is not None if d.get("candidate_fol") else False
        free_out.append(d)
    wjl(DATA / "rcomp_free_view.jsonl", free_out)
    wjl(DATA / "rcomp_sig_view.jsonl", sig)
    c = {"free_rows": len(free_out), "free_parse_ok": sum(bool(r.get("parse_ok")) for r in free_out),
         "free_cand_parse_ok_dsE_parser": sum(r["cand_parse_ok"] for r in free_out),
         "sig_rows": len(sig), "sig_parse_ok": sum(bool(r.get("parse_ok")) for r in sig),
         "sig_unique_text_sig": len({(r["text"], r["sig_key"]) for r in sig if r.get("parse_ok")}),
         "free_unique_text_sig": len({(r["text"], r["sig_key"]) for r in free_out if r["cand_parse_ok"]}),
         "text_missing": n_text_missing, "n_sentences_text_from_exp7_fallback": n_fallback, "free_whitelist": list(FREE_WHITELIST)}
    logger.info(f"rcomp views: {c}")
    return c


def build_free3() -> dict:
    view = jl(DATA / "perturb_view.jsonl")
    e_sids = {r["sentence_id"] for r in view if r["fold"] == "BASE" and not r["is_rcomp"]}
    r_sids = {r["sentence_id"] for r in view if r["fold"] == "BASE" and r["is_rcomp"]}
    slots = {"G4": "deepseek", "G6": "microsoft", "G7": "openai"}
    free3 = defaultdict(dict)
    d = json.loads(DSE.read_text())
    for g in d["datasets"]:
        if g["dataset"] != "heldout_candidates":
            continue
        for e in g["examples"]:
            if e["metadata_sentence_id"] in e_sids and e["metadata_slot"] in slots and e["metadata_prompt_variant"] == "fewshot_v1":
                free3[e["metadata_sentence_id"]][e["metadata_slot"]] = json.loads(e["input"])["candidate_fol"] or None
    del d
    gc.collect()
    for r in jl(DATA / "rcomp_free_view.jsonl"):
        if r["sentence_id"] in r_sids and r["slot"] in slots and r["prompt_variant"] == "fewshot_v1":
            free3[r["sentence_id"]][r["slot"]] = r["candidate_fol"] or None
    out = {sid: v for sid, v in free3.items()}
    (DATA / "free3_peers.json").write_text(json.dumps(out, ensure_ascii=False, indent=0))
    c = {"E_bases_with_free3": sum(1 for s in e_sids if s in out), "E_bases": len(e_sids),
         "E_bases_with_ge2_parseable": sum(1 for s in e_sids if sum(L.parse(f) is not None for f in out.get(s, {}).values()) >= 2),
         "RCOMP_bases_with_free3": sum(1 for s in r_sids if s in out), "RCOMP_bases": len(r_sids),
         "RCOMP_bases_with_ge2_parseable": sum(1 for s in r_sids if sum(L.parse(f) is not None for f in out.get(s, {}).values()) >= 2)}
    logger.info(f"FREE3: {c}")
    return c


def main() -> dict:
    c = {"perturb": build_perturb_view(), "rcomp": build_rcomp_views(), "free3": build_free3()}
    (RES / "data_views_summary.json").write_text(json.dumps(c, indent=1))
    return c


if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
    logger.add(ROOT / "logs" / "views.log", rotation="30 MB", level="DEBUG")
    main()
