#!/usr/bin/env python3
"""E2-B step 0.3-0.4 ($0, no LLM): draw E2-B by E2's frozen rule, continued.

1. Re-run E2's frozen selection (src_e2/select_e2.py main(), byte-identical) into a scratch work dir and ASSERT that
   it reproduces work/pool_E2.json (sha256 98cdccff...) and census_E2.json exactly. Any mismatch -> exit 1 (STOP).
2. Rebuild the L25 candidate lists with the same functions (E's exclusion + E2 extra exclusion + E 12-gram filter,
   MALLS-train, >=25 words, >=3 gold conditions, minus EXC ids), in the same sha1('E2_v1|'+sid) order.
3. used = every E2 id (EXC 100, L25 448, DT 110); accepted_grams = union of the 12-grams of all those rows (F2).
4. E2-B = the 98 L25 surplus in e2_rank order, then take(long_) then take(short) (E2's take(): skip used, skip any
   12-gram collision with accepted_grams, then accept and add its grams) until 400; reserve = the next 150.
5. Assert 0 text / 12-gram collisions with E's 700 and 0 id / text / 12-gram collisions with the E2 rows.
6. Batches: sort E2-B by sha1('E2B_batch_v1|'+sid) and cut into 8 x 50.
Outputs (in <WS>/e2b/): sentences_E2B.json, reserve_E2B.json, census_E2B.json, batches_E2B.json.
Re-running gives byte-identical outputs (checked by --check-twice in the testing plan)."""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WS = ROOT.parent
OUT = WS / "e2b"
sys.path.insert(0, str(ROOT / "src_e2"))
sys.argv = [sys.argv[0]]
import select_e2 as s2  # noqa: E402  (imports E's select_sentences as s2.ss)

ss = s2.ss
POOL_SHA = "98cdccffa55226db6599c6b81b0228a667d4e805215e404f832edd9b776527f7"
N_TARGET, N_RESERVE, N_BATCH = 400, 150, 50


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def reproduce_e2() -> dict:
    """Run E2's main() with W pointed at a scratch dir; ROOT-level census/exclusion outputs are backed up, compared, restored."""
    scratch = ROOT / "work" / "_repro_E2"
    scratch.mkdir(parents=True, exist_ok=True)
    bak = {n: (ROOT / n).read_bytes() for n in ("census_E2.json", "exclusion_log_E2.json")}
    s2.W = scratch
    try:
        s2.main()
        got = {"pool": sha256(scratch / "pool_E2.json"), "census_identical": (ROOT / "census_E2.json").read_bytes() == bak["census_E2.json"],
               "exclusion_log_identical": (ROOT / "exclusion_log_E2.json").read_bytes() == bak["exclusion_log_E2.json"],
               "active_sentences_sha256": sha256(scratch / "sentences.json")}
    finally:
        for n, b in bak.items():
            (ROOT / n).write_bytes(b)
    got["pool_expected"] = POOL_SHA
    got["pool_ok"] = got["pool"] == POOL_SHA == sha256(ROOT / "work" / "pool_E2.json")
    got["active_expected"] = json.loads((ROOT / "prereg_E2.json").read_text())["selection_hashes"]["work/sentences.json (active base set)"]
    got["active_ok"] = got["active_sentences_sha256"] == got["active_expected"]
    shutil.rmtree(scratch)
    return got


def l25_lists(exc_ids: set):
    """Exactly select_e2.main()'s path to `short` / `long_` (same functions, same order)."""
    ex_all, _ = ss.build_exclusion()
    extra = s2.extra_exclusion_texts()
    for texts in extra.values():
        ex_all |= {ss.h(t) for t in texts}
    e_grams = set()
    for t in extra["E_700_sentences"]:
        e_grams |= s2.grams12(t)
    train_pool, _ = ss.malls_pool(ex_all)
    train_pool = [r for r in train_pool if not (s2.grams12(r["text"]) & e_grams)]
    for r in train_pool:
        r["e2_key"] = s2.e2key(r["sentence_id"])
    srt = lambda xs: sorted(xs, key=lambda r: r["e2_key"])  # noqa: E731
    l25_all = srt([r for r in train_pool if r["words"] >= 25 and r["n_conditions"] >= 3 and r["sentence_id"] not in exc_ids])
    short = [r for r in l25_all if r["words"] <= 29]
    long_ = [r for r in l25_all if r["words"] >= 30]
    return short, long_, extra, e_grams


def main() -> int:
    OUT.mkdir(exist_ok=True)
    rep = reproduce_e2()
    print(json.dumps(rep))
    if not (rep["pool_ok"] and rep["census_identical"] and rep["active_ok"]):
        print("STOP: E2 selection not reproduced")
        return 1
    pool = json.loads((ROOT / "work" / "pool_E2.json").read_text())
    e2_rows = pool["EXC"] + pool["L25"] + pool["DT"]
    used = {r["sentence_id"] for r in e2_rows}
    accepted_grams: set = set()
    for r in e2_rows:
        accepted_grams |= s2.grams12(r["text"])
    n_e2_grams = len(accepted_grams)
    short, long_, extra, e_grams = l25_lists({r["sentence_id"] for r in pool["EXC"]})
    within12 = Counter()

    def take(rows, n, tag):  # E2's take(), verbatim logic
        out = []
        for r in rows:
            if len(out) >= n:
                break
            if r["sentence_id"] in used:
                continue
            g = s2.grams12(r["text"])
            if g & accepted_grams:
                within12[tag] += 1
                continue
            accepted_grams.update(g)
            used.add(r["sentence_id"])
            out.append(r)
        return out

    surplus = sorted([r for r in pool["L25"] if r["l25_tier"] == "surplus"], key=lambda r: r["e2_rank"])
    assert len(surplus) == 98
    # the surplus rows were accepted by E2 already (their grams are in accepted_grams); they enter E2-B first, as-is
    cont_need = N_TARGET - len(surplus)
    cont = take(long_, cont_need, "long")
    cont += take(short, cont_need - len(cont), "short")
    reserve = take(long_, N_RESERVE, "long_reserve")
    reserve += take(short, N_RESERVE - len(reserve), "short_reserve")
    remaining_long = sum(r["sentence_id"] not in used for r in long_)
    remaining_short = sum(r["sentence_id"] not in used for r in short)
    rows = []
    for i, r in enumerate(surplus + cont):
        r = dict(r)
        r["e2b_rank"] = i
        r["e2b_origin"] = "E2_surplus" if i < len(surplus) else "continuation"
        r["source_stratum"] = "L25"
        r["word_bin"] = "30-34" if r["words"] >= 30 else "25-29"
        r["l25_tier"] = r.get("l25_tier") or "e2b_continuation"
        r["sample"] = "E2B"
        r["source_dataset"] = r["source"]
        r["reference_status_initial"] = "MALLS_GPT4_GOLD"
        r.setdefault("agreement_type", None)
        r.setdefault("convention_flag", None)
        r["e2b_batch_key"] = hashlib.sha1(("E2B_batch_v1|" + r["sentence_id"]).encode()).hexdigest()
        rows.append(r)
    res_rows = []
    for i, r in enumerate(reserve):
        r = dict(r)
        r.update({"e2b_rank": N_TARGET + i, "e2b_origin": "reserve", "source_stratum": "L25", "sample": "E2B",
                  "word_bin": "30-34" if r["words"] >= 30 else "25-29", "l25_tier": "e2b_reserve", "source_dataset": r["source"],
                  "reference_status_initial": "MALLS_GPT4_GOLD", "agreement_type": None, "convention_flag": None})
        res_rows.append(r)
    # batches: hash order, 8 x 50
    order = sorted(rows, key=lambda r: r["e2b_batch_key"])
    for i, r in enumerate(order):
        r["e2b_batch"] = i // N_BATCH + 1
    rows = sorted(order, key=lambda r: r["e2b_rank"])
    # ---- assertions ----
    ids = [r["sentence_id"] for r in rows + res_rows]
    assert len(ids) == len(set(ids)), "duplicate ids"
    e_norm = {ss.norm(t) for t in extra["E_700_sentences"]}
    e2_nonsurplus = [r for r in e2_rows if r.get("l25_tier") != "surplus"]
    e2ns_ids = {r["sentence_id"] for r in e2_nonsurplus}
    e2ns_norm = {ss.norm(r["text"]) for r in e2_nonsurplus}
    e2ns_grams = set()
    for r in e2_nonsurplus:
        e2ns_grams |= s2.grams12(r["text"])
    coll = {"E700_text": sum(ss.norm(r["text"]) in e_norm for r in rows + res_rows),
            "E700_12gram": sum(bool(s2.grams12(r["text"]) & e_grams) for r in rows + res_rows),
            "E2_nonsurplus_id": sum(r["sentence_id"] in e2ns_ids for r in rows + res_rows),
            "E2_nonsurplus_text": sum(ss.norm(r["text"]) in e2ns_norm for r in rows + res_rows),
            "E2_nonsurplus_12gram": sum(bool(s2.grams12(r["text"]) & e2ns_grams) for r in rows + res_rows)}
    # within E2-B 12-gram uniqueness (continuation + reserve vs everything accepted before them)
    seen, within_coll = set(), 0
    for r in rows + res_rows:
        g = s2.grams12(r["text"])
        within_coll += bool(g & seen)
        seen |= g
    coll["within_E2B_12gram"] = within_coll
    assert all(v == 0 for v in coll.values()), coll
    assert len(rows) == N_TARGET, len(rows)
    (OUT / "sentences_E2B.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1))
    (OUT / "reserve_E2B.json").write_text(json.dumps(res_rows, ensure_ascii=False, indent=1))
    batches = {str(b): [r["sentence_id"] for r in order if r["e2b_batch"] == b] for b in range(1, N_TARGET // N_BATCH + 1)}
    (OUT / "batches_E2B.json").write_text(json.dumps({"rule": "sort by sha1('E2B_batch_v1|'+sentence_id), cut into 8 x 50", "batches": batches}, indent=1))
    census = {
        "e2_reproduction": rep,
        "rule": "E2-B = E2's 98 L25 surplus (e2_rank order) + continuation of E2's take(long_) then take(short) over sha1('E2_v1|'+sid), "
                "skipping every E2 id, accepted_grams seeded with the 12-grams of all 658 E2 rows (EXC 100, L25 448, DT 110)",
        "n_E2_rows_seeding": len(e2_rows), "n_E2_12grams_seeded": n_e2_grams,
        "L25_supply_after_filters_total": {"25-29": len(short), ">=30": len(long_)},
        "E2B": {"n": len(rows), "from_E2_surplus": len(surplus), "continuation": len(cont),
                "word_bin_counts": dict(Counter(r["word_bin"] for r in rows)),
                "surplus_word_bins": dict(Counter(r["word_bin"] for r in rows[:len(surplus)])),
                "continuation_word_bins": dict(Counter(r["word_bin"] for r in rows[len(surplus):])),
                "share_25_29": round(sum(r["word_bin"] == "25-29" for r in rows) / len(rows), 3),
                "mean_words": round(sum(r["words"] for r in rows) / len(rows), 2),
                "mean_n_conditions": round(sum(r["n_conditions"] for r in rows) / len(rows), 2),
                "batch_counts": {b: len(v) for b, v in batches.items()},
                "surplus_per_batch": {b: sum(1 for sid in v if sid in {r['sentence_id'] for r in surplus}) for b, v in batches.items()}},
        "reserve": {"n": len(res_rows), "word_bin_counts": dict(Counter(r["word_bin"] for r in res_rows))},
        "supply_remaining_after_E2B_and_reserve": {"25-29": remaining_short, ">=30": remaining_long},
        "within_E2B_12gram_drops": dict(within12),
        "collision_checks_all_zero": coll,
        "sha256": {}}
    for n in ("sentences_E2B.json", "reserve_E2B.json", "batches_E2B.json"):
        census["sha256"][n] = sha256(OUT / n)
    (OUT / "census_E2B.json").write_text(json.dumps(census, indent=1))
    print(json.dumps({k: census[k] for k in ("E2B", "reserve", "supply_remaining_after_E2B_and_reserve", "within_E2B_12gram_drops", "collision_checks_all_zero", "sha256")}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
