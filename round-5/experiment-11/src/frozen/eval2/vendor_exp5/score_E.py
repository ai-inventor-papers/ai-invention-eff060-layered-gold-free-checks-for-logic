#!/usr/bin/env python3
"""STEP 5: score dataset E ONCE with the frozen PEER+TEXT pipeline. Reads ONLY data/E_blind.jsonl, results/prereg.json,
the label-free API outputs (results/E_l3_q.jsonl, E_judge*.jsonl, E_disguise_map.jsonl) and, for the rewrite/probe
table, the screen score file. Never opens the E label view.

usage: score_E.py run --stage mini|100|all      -> results/E_sentences.jsonl (resumable, per sentence)
       score_E.py assemble                      -> results/per_item_E.jsonl, results/rewrite_scores_pt.jsonl
"""
from __future__ import annotations

import argparse
import hashlib
import json
import multiprocessing as mp
import os
import sys
import time
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from loguru import logger

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))
os.environ.setdefault("NLTK_DATA", str(ROOT / "data" / "nltk_data"))
import peer_text as PT  # noqa: E402
import pool_scoring as PS  # noqa: E402

RES = ROOT / "results"
STRATA = ["CTRL", "EXC", "L20", "L25"]
N_WORKERS = 12

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(ROOT / "logs" / "score_E.log", rotation="30 MB", level="DEBUG")


def jl(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def fold_E(sentence_id: str) -> int:
    return int(hashlib.sha1(("E_folds_v1|" + sentence_id).encode()).hexdigest(), 16) % 5


def load_prereg() -> dict:
    p = RES / "prereg.json"
    if not p.exists():
        raise SystemExit("results/prereg.json missing: freeze on the screen first")
    sha = (RES / "prereg.sha256").read_text().split()[0]
    if sha != sha256_file(p):
        raise SystemExit("prereg.json does not match prereg.sha256")
    pre = json.loads(p.read_text())
    blind_sha = sha256_file(ROOT / "data" / "E_blind.jsonl")
    if blind_sha != pre["E_blind_sha256"]:
        raise SystemExit("E_blind.jsonl changed after the freeze")
    return pre


def tasks(pre: dict) -> list[dict]:
    rows = jl(ROOT / "data" / "E_blind.jsonl")
    fam_v = pre["family_map_vendor"]
    q = {}
    for r in jl(RES / "E_l3_q.jsonl"):
        if r.get("coverage_status") == "OK":
            q[(r["text"], r["cond"])] = r["q"]
    dmap = {r["row_key"]: r for r in jl(RES / "E_disguise_map.jsonl")}
    by = defaultdict(list)
    for r in rows:
        by[r["sentence_id"]].append(r)
    out = []
    for sid, rs in by.items():
        text = rs[0]["text"]
        trs = []
        for r in rs:
            d = dmap.get(r["row_key"], {})
            trs.append({"key": r["row_key"], "fol": r["candidate_fol"], "family": fam_v[r["slot"]], "family_field": r["family"],
                        "system": r["system"], "is_peer": r["system_class"] == "llm",
                        "fol_disg": d.get("fol_d"), "q_disg": q.get((d.get("text_d"), "disg")) if d.get("text_d") else None})
        out.append({"sentence_id": sid, "text": text, "q": q.get((text, "orig")), "stratum": rs[0]["strata"]["source_stratum"],
                    "rows": trs})
    out.sort(key=lambda t: (STRATA.index(t["stratum"]), hashlib.sha1(t["sentence_id"].encode()).hexdigest()))
    return out


def run(stage: str):
    pre = load_prereg()
    P = dict(pre["scoring_params"])
    T = tasks(pre)
    outp = RES / "E_sentences.jsonl"
    done = {r["sentence_id"] for r in jl(outp)}
    if stage == "mini":
        sel = [t for s in STRATA for t in [x for x in T if x["stratum"] == s][:5]]
    elif stage == "100":
        sel = [t for s in STRATA for t in [x for x in T if x["stratum"] == s][:25]]
    else:
        sel = T
    todo = [t for t in sel if t["sentence_id"] not in done]
    logger.info(f"stage {stage}: {len(sel)} sentences selected, {len(todo)} to score; params {P}")
    t0 = time.time()
    secs_by = defaultdict(list)
    with ProcessPoolExecutor(max_workers=N_WORKERS, mp_context=mp.get_context("spawn"), initializer=PS.init_worker,
                             initargs=(3.5,)) as ex, outp.open("a") as fh:
        futs = {ex.submit(PS.score_sentence, t, P): t for t in todo}
        for i, fu in enumerate(as_completed(futs)):
            t = futs[fu]
            try:
                res = fu.result()
            except Exception as e:  # noqa: BLE001 - counted as coverage failure of every row of the sentence
                logger.error(f"sentence {t['sentence_id']} failed: {e}")
                res = {"sentence_id": t["sentence_id"], "rows": [{"key": r["key"], "coverage_status": "WORKER_FAIL"} for r in t["rows"]],
                       "stats": {"error": str(e)[:300]}}
            res["stratum"] = t["stratum"]
            fh.write(json.dumps(res, ensure_ascii=False) + "\n")
            fh.flush()
            secs_by[t["stratum"]].append(res["stats"].get("secs_total", 0))
            if (i + 1) % 20 == 0:
                logger.info(f"E {i + 1}/{len(todo)} sentences, {time.time() - t0:.0f}s wall")
    wall = time.time() - t0
    per = {s: (sum(v) / len(v), len(v)) for s, v in secs_by.items() if v}
    logger.info(f"stage {stage} done in {wall:.0f}s wall; mean cpu-s per sentence by stratum {per}")
    remaining = Counter(t["stratum"] for t in T if t["sentence_id"] not in {r["sentence_id"] for r in jl(outp)})
    proj = sum(per.get(s, (30, 0))[0] * n for s, n in remaining.items()) / N_WORKERS
    logger.info(f"projection for the remaining {sum(remaining.values())} sentences: {proj / 60:.1f} min wall")
    (RES / f"E_stage_{stage}.json").write_text(json.dumps({"wall_s": wall, "per_stratum": per, "projection_min": proj / 60}))


def assemble():
    pre = load_prereg()
    frozen = pre["frozen"]
    v = pre["variant"]
    rows = {r["row_key"]: r for r in jl(ROOT / "data" / "E_blind.jsonl")}
    sc = {}
    stats = {}
    for s in jl(RES / "E_sentences.jsonl"):
        stats[s["sentence_id"]] = s["stats"]
        for r in s["rows"]:
            sc[r["key"]] = r
    jd = defaultdict(dict)
    for r in jl(RES / "E_judge.jsonl"):
        if r.get("p") is not None:
            jd[r["row_key"]][r["cond"]] = r
    jloc = defaultdict(dict)
    for r in jl(RES / "E_judge_local.jsonl"):
        if r.get("p") is not None:
            jloc[r["row_key"]][r["cond"]] = r
    l3cost = defaultdict(float)
    for r in jl(RES / "E_l3_q.jsonl"):
        l3cost[r["text"]] += r.get("cost_usd") or 0.0
    n_rows_text = Counter(r["text"] for r in rows.values())
    pre_sha = (RES / "prereg.sha256").read_text().split()[0]
    neutral = pre["imputation"]["neutral"]
    out = []
    for k, b in rows.items():
        s = sc.get(k, {"coverage_status": "NOT_SCORED"})
        parse_ok = PT.parse_fol(b["candidate_fol"]) is not None
        cov = "UNPARSEABLE" if not parse_ok else s.get("coverage_status", "NOT_SCORED")
        rec = {"row_key": k, "item_id": b["item_id"], "sentence_id": b["sentence_id"], "system": b["system"], "slot": b["slot"],
               "family": b["family"], "family_vendor": pre["family_map_vendor"][b["slot"]], "system_class": b["system_class"],
               "prompt_variant": b["prompt_variant"], "stratum": b["strata"]["source_stratum"], "strata": b["strata"],
               "fold_E": fold_E(b["sentence_id"]), "coverage_status": cov, "prereg_sha256": pre_sha, "variant": v}
        g = s.get(f"{v}:g_score")
        feats = {kk: s.get(kk) for kk in s}
        feats["coverage_status"] = cov
        rec.update({
            "g_score": g, "support": s.get(f"{v}:support"), "coverage": s.get(f"{v}:coverage"),
            "c_score_nf": s.get(f"{v}:c_score_nf"), "g_score_k6": s.get(f"{v}:g_score_k6"),
            "g_score_famfield": s.get(f"{v}:g_score_famfield"), "nf_eq_medoid": s.get(f"{v}:nf_eq_medoid"),
            "unit_codes": s.get(f"{v}:unit_codes"), "top_code": s.get(f"{v}:top_code"), "n_units": s.get(f"{v}:n_units"),
            "units_truncated": s.get(f"{v}:units_truncated"), "n_unknown": s.get(f"{v}:n_unknown"),
            "n_peers_used": s.get("n_peers_used"), "peer_unavailable": s.get("peer_unavailable"),
            "c_score_align": s.get("c_score_align"), "eqmv_medoid_eq": s.get("eqmv_medoid_eq"),
            # NF-anchored (name-free; F1 FAILED on the screen) kept as a reported negative
            "nf_g_score": s.get("NF-anchored:g_score"), "nf_c_score": s.get("NF-anchored:c_score_nf"),
            "nf_eq_medoid_nf": s.get("NF-anchored:nf_eq_medoid"), "nf_top_code": s.get("NF-anchored:top_code"),
            "nf_unit_codes": s.get("NF-anchored:unit_codes"), "nf_secs_pairs": s.get("NF-anchored:secs_pairs"),
            "medoid_depth": s.get("medoid_depth"), "medoid_ops": s.get("medoid_ops"),
            "l2_bow": s.get("l2_bow"), "l3_z3": s.get("l3_z3"), "l3_z3_disg": s.get("l3_z3_disg"),
            "l3_fields": s.get("l3_fields"), "l1_codes": s.get("l1_codes"), "l2_role": s.get("l2_role"),
        })
        rec["l1_any"] = (1 if rec["l1_codes"] else 0) if rec["l1_codes"] is not None else None
        # frozen fusion, PEER-only, TEXT-only, SENSITIVITY
        if cov == "UNPARSEABLE":
            for c in ("p_peer_text", "p_text", "p_sensitivity", "peer_only"):
                rec[c] = 1.0
            rec.update(flag=1, fired_signal="UNPARSEABLE", model_used="none")
        else:
            fs = PT.fused_score(frozen, feats)
            rec.update(p_peer_text=fs["p_error"], flag=fs["flag"], fired_signal=fs["fired_signal"], model_used=fs["model_used"])
            rec["p_text"] = PT.apply_logistic(frozen["text_only"], feats)
            rec["p_sensitivity"] = PT.apply_logistic(frozen["sensitivity_all_adj"], feats) if feats.get(frozen["fusion"]["features"][0]) is not None \
                else rec["p_text"]
            pf = frozen["peer_only"]["feature"]
            rec["peer_only"] = s.get(pf) if s.get(pf) is not None else neutral.get(pf)
        # judges (oriented: higher = more likely an error); unparseable -> 1.0 like every metric
        for cond in ("orig", "disg"):
            j = jd.get(k, {}).get(cond)
            jl_ = jloc.get(k, {}).get(cond)
            if cov == "UNPARSEABLE":
                rec[f"judge_cheap_{cond}"] = 1.0
                rec[f"judge_local_qwen8b_{cond}"] = 1.0
            else:
                rec[f"judge_cheap_{cond}"] = (1 - j["p"]) if j else None
                rec[f"judge_local_qwen8b_{cond}"] = (1 - jl_["p"]) if jl_ else None
            rec[f"judge_cheap_{cond}_type"] = j.get("type") if j else None
            rec[f"judge_cheap_{cond}_verdict"] = j.get("verdict") if j else None
            rec[f"judge_local_qwen8b_{cond}_type"] = jl_.get("type") if jl_ else None
        rec["judge_cost_usd"] = sum((jd.get(k, {}).get(c) or {}).get("cost") or 0.0 for c in ("orig", "disg"))
        st = stats.get(b["sentence_id"], {})
        rec["cost_usd_peer_text"] = l3cost.get(b["text"], 0.0) / max(1, n_rows_text[b["text"]])
        rec["secs_pairs"] = s.get(f"{v}:secs_pairs")
        rec["secs_text"] = s.get("secs_text_row")
        rec["secs_sentence_total"] = st.get("secs_total")
        out.append(rec)
    outp = RES / "per_item_E.jsonl"
    outp.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in out))
    assert outp.stat().st_mtime > (RES / "prereg.sha256").stat().st_mtime
    logger.info(f"per_item_E: {len(out)} rows; coverage {Counter(r['coverage_status'] for r in out)}; "
                f"judge_cheap_disg present {sum(r['judge_cheap_disg'] is not None for r in out)}; "
                f"local judge disg present {sum(r['judge_local_qwen8b_disg'] is not None for r in out)}")
    # rewrite / probe rows on the screen pools, scored with the frozen pipeline
    rw = []
    for s in jl(RES / "screen_scores.jsonl"):
        for r in s["rows"]:
            if r["key"].startswith(("RW:", "PR:")) or not r["key"].startswith("M:"):
                feats = dict(r)
                fs = PT.fused_score(frozen, feats) if r.get("coverage_status") == "OK" else {"p_error": 1.0, "flag": 1}
                rw.append({"key": r["key"], "sentence_key": s.get("sentence_key"), "g_score": r.get(f"{v}:g_score"),
                           "c_score_nf": r.get(f"{v}:c_score_nf"), "c_score_align": r.get("c_score_align"),
                           "l2_bow": r.get("l2_bow"), "l3_z3": r.get("l3_z3"), "p_peer_text": fs["p_error"], "flag": fs["flag"],
                           "top_code": r.get(f"{v}:top_code"), "coverage_status": r.get("coverage_status"),
                           **{f"{vv}:g_score": r.get(f"{vv}:g_score") for vv in ("NF-pure", "NF-anchored")}})
    (RES / "rewrite_scores_pt.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rw))
    logger.info(f"rewrite/probe/screen rows with frozen scores: {len(rw)}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["run", "assemble"])
    ap.add_argument("--stage", default="mini", choices=["mini", "100", "all"])
    a = ap.parse_args()
    if a.cmd == "run":
        run(a.stage)
    else:
        assemble()
