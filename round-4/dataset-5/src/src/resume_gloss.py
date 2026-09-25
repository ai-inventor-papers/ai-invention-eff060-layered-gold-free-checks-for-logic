#!/usr/bin/env python3
"""Resume every step that needs paid LLM calls, in the pre-registered order (D9: the run's OpenRouter budget was exhausted
before this artifact's first call). Run once the Test-idea budget is raised:

    .venv/bin/python src/resume_gloss.py all        # gate -> FREE gloss -> final labels + seal -> join -> SIG e2e -> audit (ii) -> package
    .venv/bin/python src/resume_gloss.py <step>     # gate | free_gloss | finalize | sig_e2e | audit_ii | package

Budget: every call goes through gloss.Client (ledger cost_ledger.jsonl, artifact hard stop $6). Estimated total at the
catalogue prices in work/models_snapshot.json: gate ~$0.10, FREE gloss ~$0.95, SIG e2e ~$0.25, audit (ii) ~$0.45.
If the gate FAILS, the script stops: write prompts/gloss_v2.json (ONE revision, hashed into deviations.json), then run
`src/gate.py run --half B --version gloss_v2` and `resume_gloss.py free_gloss --version gloss_v2` onward.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import subprocess
import sys
import time
from collections import defaultdict

from common import RES, ROOT, WORK, dump, load_jsonl, setup_logger
from run_search import class_key

logger = setup_logger("resume_gloss")
PY = sys.executable


def run(cmd: list[str]) -> None:
    logger.info("$ " + " ".join(cmd))
    subprocess.run(cmd, check=True, cwd=ROOT)


def gate(version: str, half: str) -> bool:
    run([PY, "src/gate.py", "run", "--half", half, "--version", version])
    rep = json.loads((RES / "gate_report.json").read_text())[f"{version}_{half}"]
    return bool(rep["PASS"])


def pair_jobs(search_rows: list[dict], sents: dict, first_keys: set | None = None) -> list[dict]:
    by = defaultdict(set)
    for r in search_rows:
        if r.get("status") != "MAPPED":
            continue
        for u, m in r["pairs_union"]:
            by[r["sentence_id"]].add((u, m))
    jobs = [{"sentence_id": sid, "sentence": sents[sid]["text"], "pairs": sorted(p)} for sid, p in by.items()]
    if first_keys:  # untouched-subset sentences first
        jobs.sort(key=lambda j: (j["sentence_id"] not in first_keys, j["sentence_id"]))
    return jobs


async def rate(jobs: list[dict], version: str, phase: str) -> dict:
    import gloss
    client = gloss.Client(phase=phase)
    try:
        return await gloss.rate_pairs(client, jobs, version=version, logger=logger)
    finally:
        await client.close()


def free_gloss(version: str) -> None:
    import gloss
    sents = json.loads((WORK / "sentences.json").read_text())
    search = load_jsonl(RES / "map_search.jsonl")
    rows = load_jsonl(RES / "free_labels_v2.jsonl")
    untouched_sids = {r["sentence_id"] for r in rows if not r.get("seen_iter3", False)}
    jobs = pair_jobs(search, sents, untouched_sids)
    n = sum(len(j["pairs"]) for j in jobs)
    est = gloss.estimate_cost(n, gloss.live_prices())
    logger.info(f"FREE gloss: {n} unique pairs over {len(jobs)} sentences; estimated ${est:.2f}")
    v = asyncio.run(rate(jobs, version, f"free_gloss_{version}"))
    with (RES / "gloss_verdicts.jsonl").open("w") as fh:
        for j in jobs:
            for (u, m) in j["pairs"]:
                fh.write(json.dumps({"sentence_id": j["sentence_id"], "use": u, "meaning": m, "version": version,
                                     "haiku": v.get(("haiku", j["sentence_id"], u, m)),
                                     "qwen": v.get(("qwen", j["sentence_id"], u, m))}, ensure_ascii=False) + "\n")


def verify_correct_certificates() -> dict:
    """Re-verify, under z3 at write time, the map certificate of every CORRECT class: re-run the deterministic search,
    find the map with the certificate's entry set, rebuild its image and prove equivalence to the reading again."""
    import freelab as FL
    sents = json.loads((WORK / "sentences.json").read_text())
    rows = load_jsonl(RES / "free_labels_v2.jsonl")
    done, ok, bad = set(), 0, []
    for r in rows:
        if r["label"] not in ("CORRECT", "READING_CHOICE") or r["class_key"] in done:
            continue
        done.add(r["class_key"])
        s = sents[r["sentence_id"]]
        cert = r["map_certificate"]
        rfol = {"weak": s["reference_fol_weak"], "strong": s["reference_fol_strong"], "converse": s.get("reading_converse")}[cert["reading"]]
        cand, rd = FL.Candidate(r["candidate_fol"]), FL.Reading(rfol, s["units"])
        res = FL.search(cand, rd)
        want = sorted(cert["map"])
        hit = None
        for m in res["equiv_maps"]:
            ents = sorted(f"{a} => {b}" for a, b in FL.map_to_json(m["assign"], m["cmap"], cand, rd).items())
            if ents == want:
                hit = m
                break
        if hit is not None and FL.z3_equiv_retry(FL.build_image(cand, rd, hit["assign"], hit["cmap"]), rd.e) is True:
            ok += 1
        else:
            bad.append(r["class_key"])
    return {"n_classes": len(done), "reverified": ok, "failed": bad}


def finalize() -> None:
    run([PY, "src/assemble_labels.py", "--mode", "final"])
    rep = verify_correct_certificates()
    dump(RES / "certificate_reverification.json", rep)
    logger.info(f"certificate re-verification: {rep['reverified']}/{rep['n_classes']}; failed {len(rep['failed'])}")
    run([PY, "src/post_seal_join.py"])


def sig_e2e(version: str) -> None:
    import freelab as FL
    sents = json.loads((WORK / "sentences.json").read_text())
    rows = load_jsonl(RES / "sig_replay_rows.jsonl")
    sel = [r for r in rows if r["in_e2e_gloss_subsample_300"]]
    search = {r["class_key"]: r for r in load_jsonl(RES / "sig_replay_syn.jsonl")}
    srows = [search[class_key(r["sentence_id"], r["renamed_fol"])] for r in sel]
    v = asyncio.run(rate(pair_jobs(srows, sents), version, f"sig_e2e_{version}"))
    conf = defaultdict(int)
    for r, sr in zip(sel, srows):
        if sr["status"] == "MAPPED":
            vd = {(u, m): (v.get(("haiku", r["sentence_id"], u, m)), v.get(("qwen", r["sentence_id"], u, m))) for u, m in sr["pairs_union"]}
            lab, _ = FL.gloss_decision(sr["equiv_maps"], sr["pairs_union"], vd)
        else:
            lab = sr["status"]
        r["e2e_gloss_label"] = lab
        conf[(r["sig_label"], lab)] += 1
    by = {r["row_key"] + r["rename"]: r for r in sel}
    with (RES / "sig_replay_rows.jsonl").open("w") as fh:
        for r in rows:
            fh.write(json.dumps(by.get(r["row_key"] + r["rename"], r), ensure_ascii=False) + "\n")
    err = [r for r in sel if r["sig_label"] == "ERROR"]
    cor = [r for r in sel if r["sig_label"] == "CORRECT"]
    sa = json.loads((RES / "soundness_audit.json").read_text())
    sa["i_sig_replay"]["e2e_gloss_subsample_300"] = {
        "n": len(sel), "status": "DONE", "version": version, "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "confusion": {f"{a}->{b}": n for (a, b), n in sorted(conf.items())},
        "false_CORRECT_on_known_ERROR": round(sum(r["e2e_gloss_label"] == "CORRECT" for r in err) / max(len(err), 1), 4),
        "bar": "<= 0.05",
        "CORRECT_recall_on_known_CORRECT": round(sum(r["e2e_gloss_label"] == "CORRECT" for r in cor) / max(len(cor), 1), 4),
        "UNRESOLVED_share": round(sum(str(r["e2e_gloss_label"]).startswith("UNRESOLVED") for r in sel) / max(len(sel), 1), 4)}
    dump(RES / "soundness_audit.json", sa)


AUDIT_SYS = ("You audit first-order-logic translations of English rule sentences. Judge whether the candidate formula is "
             "faithful to the sentence, given the English meaning of each concept. Different predicate names, splitting or "
             "merging concepts, and logically equivalent restatements are fine if the truth conditions match the sentence "
             "(either the 'X unless E' = 'if not E then X' reading or the biconditional reading of the exception is acceptable).")
AUDIT_USER = ("Sentence: {text}\n\nConcepts used in the sentence (meaning of each, for reference):\n{concepts}\n\n"
              "Candidate formula: {fol}\n\nAnswer with JSON only: {{\"verdict\": \"FAITHFUL\" | \"FAITHFUL_DIFFERENT_DECOMPOSITION\" | "
              "\"UNFAITHFUL\" | \"UNSURE\", \"reason\": \"<one line>\"}}")


def audit_ii() -> None:
    import random
    import gloss
    rows = load_jsonl(RES / "free_labels_v2.jsonl")
    sents = json.loads((WORK / "sentences.json").read_text())
    rng = random.Random(20260924)
    pick = []
    for lab, n in (("ERROR_CERT", 60), ("CORRECT", 60)):
        by = defaultdict(list)
        for r in rows:
            if r["label"] == lab:
                by[r["template_id"]].append(r)
        chosen = []
        for t in sorted(by):
            rng.shuffle(by[t])
        i = 0
        while len(chosen) < n and any(by.values()):
            t = sorted(by)[i % len(by)]
            if by[t]:
                chosen.append(by[t].pop())
            i += 1
        pick += chosen

    async def go():
        client = gloss.Client(phase="audit_ii", concurrency=4)
        out = []
        try:
            async def one(r):
                s = sents[r["sentence_id"]]
                concepts = "\n".join(f"- {u['gloss_pos']}" for u in s["units"].values())
                msgs = [{"role": "system", "content": AUDIT_SYS},
                        {"role": "user", "content": AUDIT_USER.format(text=s["text"], concepts=concepts, fol=r["candidate_fol"])}]
                txt, _ = await client.chat(gloss.AUDITOR, msgs, 400, logger)
                try:
                    d = json.loads(txt[txt.index("{"): txt.rindex("}") + 1]) if txt else {}
                except ValueError:
                    d = {}
                out.append({"row_key": r["row_key"], "label": r["label"], "template_id": r["template_id"],
                            "verdict": d.get("verdict"), "reason": d.get("reason")})
            await asyncio.gather(*[one(r) for r in pick])
        finally:
            await client.close()
        return out
    res = asyncio.run(go())
    sa = json.loads((RES / "soundness_audit.json").read_text())
    ec = [r for r in res if r["label"] == "ERROR_CERT" and r["verdict"]]
    co = [r for r in res if r["label"] == "CORRECT" and r["verdict"]]
    from soundness import wilson
    k1 = sum(r["verdict"] in ("UNFAITHFUL", "UNSURE") for r in ec)
    k2 = sum(r["verdict"] in ("FAITHFUL", "FAITHFUL_DIFFERENT_DECOMPOSITION") for r in co)
    sa["ii_stronger_model_audit"] = {"model": gloss.AUDITOR, "n_ERROR_CERT": len(ec), "n_CORRECT": len(co),
                                     "ERROR_CERT_precision": round(k1 / max(len(ec), 1), 3), "ERROR_CERT_ci": wilson(k1, len(ec)),
                                     "CORRECT_precision": round(k2 / max(len(co), 1), 3), "CORRECT_ci": wilson(k2, len(co)),
                                     "rows": res}
    dump(RES / "soundness_audit.json", sa)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["all", "gate", "free_gloss", "finalize", "sig_e2e", "audit_ii", "package"])
    ap.add_argument("--version", default="gloss_v1")
    a = ap.parse_args()
    steps = ["gate", "free_gloss", "finalize", "sig_e2e", "audit_ii", "package"] if a.step == "all" else [a.step]
    for st in steps:
        logger.info(f"=== {st} ===")
        if st == "gate":
            if not gate(a.version, "A" if a.version == "gloss_v1" else "B"):
                logger.error("gate FAILED: write ONE revision prompts/gloss_v2.json, log it in deviations.json, then run "
                             "`src/gate.py run --half B --version gloss_v2`; if that fails too, run finalize with no "
                             "verdicts (MAPPED -> UNRESOLVED_GLOSS_GATE_FAILED)")
                return
        elif st == "free_gloss":
            free_gloss(a.version)
        elif st == "finalize":
            finalize()
        elif st == "sig_e2e":
            sig_e2e(a.version)
        elif st == "audit_ii":
            audit_ii()
        elif st == "package":
            run([PY, "src/build_output.py"])


if __name__ == "__main__":
    main()
