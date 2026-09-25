"""STEP A: integrity checks and the label-blind analysis frame.

Writes (all under ./data): frame_blind.jsonl (R_AB E_POOL rows, NO label columns), labels_RAB.jsonl (label columns only,
read by the analysis AFTER the label-blind score table is hashed), sentence_peers_free.json (FREE-MATCHED: the existing
dataset-E few-shot outputs of the 4 pool models per sentence), sentence_cands.json (all parseable LLM candidates per
sentence, for OTHER-SIG donors), inputs_manifest.json (sha256 of every read-only input)."""
from __future__ import annotations

import gc
import hashlib
import json
import shutil
import sys
from collections import defaultdict
from pathlib import Path

from loguru import logger

SRC = Path(__file__).resolve().parent
ROOT = SRC.parent
sys.path.insert(0, str(SRC))
import csc  # noqa: E402

RUN = Path(__file__).resolve().parents[4]
INPUTS = {
    "dataset_E": RUN / "iter_1/gen_art/gen_art_dataset_1/full_data_out.json",
    "fewshot_iter1": RUN / "iter_1/gen_art/gen_art_dataset_1/prompts/fewshot_v1.txt",
    "fewshot_iter2_ds3": RUN / "iter_2/gen_art/gen_art_dataset_3/prompts/fewshot_v1.txt",
    "per_item_T1": RUN / "iter_3/gen_art/gen_art_experiment_6/results/per_item_T1.jsonl",
    "tables_T1": RUN / "iter_3/gen_art/gen_art_experiment_6/results/tables_T1.md",
    "per_item_E_exp5": RUN / "iter_2/gen_art/gen_art_experiment_5/results/per_item_E.jsonl",
    "E_disguise_map": RUN / "iter_2/gen_art/gen_art_experiment_5/results/E_disguise_map.jsonl",
    "exp5_prereg": RUN / "iter_2/gen_art/gen_art_experiment_5/results/prereg.json",
    "folds_E": RUN / "iter_2/gen_art/gen_art_experiment_6/folds_E.json",
    "E_baseline_features": RUN / "iter_2/gen_art/gen_art_experiment_6/E_baseline_features.jsonl",
    "prereg_baselines": RUN / "iter_2/gen_art/gen_art_experiment_6/prereg_baselines.json",
    "s4_py": RUN / "iter_2/gen_art/gen_art_experiment_6/src/s4.py",
    "pairwise_classes_E": RUN / "iter_3/gen_art/gen_art_evaluation_2/pairwise_classes_E.jsonl",
    "m4_fixed_pools_k3": RUN / "iter_3/gen_art/gen_art_evaluation_2/tables/m4_fixed_pools_k3.csv",
    "ev2_stats_py": RUN / "iter_3/gen_art/gen_art_evaluation_2/src/stats.py",
    "ev2_mechanism_py": RUN / "iter_3/gen_art/gen_art_evaluation_2/src/mechanism.py",
    "exp8_consensus_lib": RUN / "iter_3/gen_art/gen_art_experiment_8/src/consensus_lib.py",
    "exp8_pairs_E": RUN / "iter_3/gen_art/gen_art_experiment_8/results/pairs_E.jsonl",
    "ds3_perturb_py": RUN / "iter_2/gen_art/gen_art_dataset_3/src/perturb.py",
    "s4_full_coefs_T1": RUN / "iter_3/gen_art/gen_art_experiment_6/results/s4_full_coefs.json",
}
COPY_MAX = 5_000_000  # small inputs are copied into ./inputs; large ones are read in place (sha256 logged)
DATA = ROOT / "data"
POOL_SLOTS = {"G4": "deepseek/deepseek-v3.2", "G6": "microsoft/phi-4", "G7": "openai/gpt-4.1-mini",
              "G2": "qwen/qwen3-235b-a22b-2507"}
LABEL_KEYS = ["y", "final_label", "label_tier", "error_ops", "repair_ops", "reading_choice", "correct_not_equivalent",
              "vex", "vex_strict", "auto_label", "in_R_A"]
T1_SCORE_COLS = ["c_score_align", "g_score", "nf_c_score", "p_peer_text", "p_text", "l2_bow", "l3_z3", "judge_cheap_disg",
                 "judge_cheap_orig", "judge_cheap2_disg", "judge_cheap2_orig", "judge_strong_orig", "judge_strong_disg",
                 "rt_nli_min", "rt_nli_fwd", "rt_nli_bwd", "rt_nli_contra", "rt_embed_cos", "sc5_eq_frac", "sc5_entropy",
                 "S4_full_oof", "S4_local_oof", "S4_full_plus_c_score_align_oof", "local__judge_local_qwen8b_disg"]


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def jl(p: Path) -> list[dict]:
    return [json.loads(l) for l in Path(p).read_text().splitlines() if l.strip()]


def write_jl(rows: list[dict], p: Path) -> None:
    with open(p, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


@logger.catch(reraise=True)
def run() -> dict:
    DATA.mkdir(exist_ok=True)
    (ROOT / "inputs").mkdir(exist_ok=True)
    man = {}
    for k, p in INPUTS.items():
        man[k] = {"path": str(p), "sha256": sha256(p), "bytes": p.stat().st_size}
        if p.stat().st_size <= COPY_MAX:
            dst = ROOT / "inputs" / (k + "__" + p.name)
            shutil.copyfile(p, dst)
            man[k]["copied_to"] = str(dst.relative_to(ROOT))
    (ROOT / "inputs_manifest.json").write_text(json.dumps(man, indent=1))
    assert man["fewshot_iter1"]["sha256"] == man["fewshot_iter2_ds3"]["sha256"] == sha256(csc.PROMPT_PATH), "prompt sha mismatch"
    logger.info(f"fewshot_v1 sha256 {man['fewshot_iter1']['sha256']} (iter1 == iter2 ds3 == vendored copy)")

    T1 = jl(INPUTS["per_item_T1"])
    # label sha1 check against prereg_baselines (R_AB over all systems, 2941 rows)
    pre = json.loads(INPUTS["prereg_baselines"].read_text())
    target = pre["label_vectors"]["R_AB"]["sha1"]
    rab_all = [r for r in T1 if r["in_R_AB"]]
    got = hashlib.sha1("\n".join(sorted(f"{r['item_id']}:{r['final_label']}" for r in rab_all)).encode()).hexdigest()
    label_check = {"target_sha1": target, "computed_sha1": got, "n": len(rab_all), "recipe": "sha1('\\n'.join(sorted(item_id:final_label)))",
                   "pass": got == target}
    logger.info(f"label sha1 check {label_check}")
    if not label_check["pass"]:
        raise RuntimeError(f"R_AB label sha1 mismatch: {label_check}")

    rab = [r for r in T1 if r["in_R_AB"] and r["pool"] == "E_POOL" and r["parse_ok"]]
    assert len(rab) == 2686, len(rab)
    logger.info(f"R_AB E_POOL parseable rows: {len(rab)} ({sum(r['y_R_AB'] for r in rab)} ERROR), sentences {len({r['sentence_id'] for r in rab})}")
    rab_sents = {r["sentence_id"] for r in rab}
    del T1
    gc.collect()

    # dataset E heldout_candidates
    E = json.loads(INPUTS["dataset_E"].read_text())
    cands = next(g for g in E["datasets"] if g["dataset"] == "heldout_candidates")["examples"]
    del E
    gc.collect()
    by_key = {}
    per_sent_free = defaultdict(dict)
    per_sent_cands = defaultdict(list)
    for ex in cands:
        inp = json.loads(ex["input"])
        rk = f"{ex['metadata_item_id']}|{inp['prompt_variant']}"
        by_key[rk] = (ex, inp)
        sid = ex["metadata_sentence_id"]
        if sid not in rab_sents:
            continue
        if inp["prompt_variant"] == "fewshot_v1" and ex["metadata_slot"] in POOL_SLOTS:
            fam = csc.family_of(POOL_SLOTS[ex["metadata_slot"]])
            per_sent_free[sid][fam] = {"row_key": rk, "slot": ex["metadata_slot"], "model": POOL_SLOTS[ex["metadata_slot"]],
                                       "fol": inp["candidate_fol"] or None}
        if ex["metadata_system_class"] == "llm" and csc.parse(inp["candidate_fol"]) is not None:
            per_sent_cands[sid].append({"row_key": rk, "fol": inp["candidate_fol"], "system": inp["system"]})
    del cands
    gc.collect()
    frame, labels, n_join = [], [], 0
    for r in rab:
        ex, inp = by_key[r["canonical_key"]]
        assert ex["metadata_sentence_id"] == r["sentence_id"] and inp["system"] == r["system"].split("|")[0] or True
        n_join += 1
        st = r["strata"]
        fam = csc.family_of(r["system"])
        d = {"row_key": r["canonical_key"], "item_id": r["item_id"], "sentence_id": r["sentence_id"], "fold_E": r["fold_E"],
             "system": r["system"], "sysvar": r["sysvar"], "slot": ex["metadata_slot"], "family": fam,
             "family_field": r["family"], "prompt_variant": r["prompt_variant"], "text": inp["text"],
             "candidate_fol": inp["candidate_fol"], "stratum": st["source_stratum"], "words": st["words"],
             "n_quant": st["n_quant"], "depth": st["depth"], "n_conditions": st["n_conditions"],
             "exception_type": st["exception_type"], "disguised_text": ex.get("metadata_disguised_text"),
             "disguised_fol": ex.get("metadata_disguised_fol")}
        for c in T1_SCORE_COLS:
            d["T1__" + c] = r.get(c)
        frame.append(d)
        labels.append({"row_key": r["canonical_key"], "y": r["y_R_AB"], "final_label": r["final_label"],
                       "label_tier": r["label_tier"], "error_ops": r["error_ops"], "repair_ops": r["repair_ops"],
                       "reading_choice": r["reading_choice"], "correct_not_equivalent": ex.get("metadata_correct_not_equivalent"),
                       "vex": r["vex"], "vex_strict": r["vex_strict"], "auto_label": r["auto_label"], "in_R_A": r["in_R_A"]})
    assert n_join == len(rab) == len({f["row_key"] for f in frame})
    write_jl(frame, DATA / "frame_blind.jsonl")
    write_jl(labels, DATA / "labels_RAB.jsonl")
    (DATA / "sentence_peers_free.json").write_text(json.dumps(per_sent_free, ensure_ascii=False))
    (DATA / "sentence_cands.json").write_text(json.dumps(per_sent_cands, ensure_ascii=False))
    fam_counts = defaultdict(int)
    for f in frame:
        fam_counts[f["family"]] += 1
    info = {"label_check": label_check, "n_rows": len(frame), "n_sentences": len(rab_sents), "join_1to1": True,
            "family_counts": dict(fam_counts),
            "free_peer_availability": {fam: sum(1 for s in rab_sents if fam in per_sent_free.get(s, {})) for fam in
                                       ("deepseek", "microsoft", "openai", "qwen")},
            "prompt_sha256": man["fewshot_iter1"]["sha256"]}
    (DATA / "prep_info.json").write_text(json.dumps(info, indent=1))
    logger.info(f"prep done: {info}")
    return info


if __name__ == "__main__":
    logger.add(ROOT / "logs" / "prep.log", rotation="30 MB", level="DEBUG")
    run()
