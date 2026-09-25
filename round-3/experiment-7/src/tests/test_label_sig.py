"""T1/T2: SIG prompt render checks and SIG labeller unit tests on known items from dataset 3 (run before real labels)."""
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import label_sig as LS  # noqa: E402
import sig_prompt as SP  # noqa: E402

RC = ROOT / "rcomp"
PRELIM = {s["sentence_id"]: s for s in json.loads((RC / "work" / "rcomp_sentences_preliminary_iter2.json").read_text())}
FINAL = {s["sentence_id"]: s for s in json.loads((RC / "work" / "rcomp_sentences.json").read_text())}
SENTS = {**PRELIM, **FINAL}
MUT = [m for m in json.loads((RC / "work" / "perturb_suite.json").read_text()) if m["base_source"] == "RCOMP"]
CTR = [c for c in json.loads((RC / "work" / "perturb_controls.json").read_text()) if c["base_source"] == "RCOMP"]


def _label(sid, fols):
    rows = [{"row_key": f"r{i}", "candidate_fol": f, "parse_ok": True} for i, f in enumerate(fols)]
    out = LS.label_sentence({"sent": SENTS[sid], "rows": rows})
    labs = []
    for i in range(len(fols)):
        o = out["rows"][f"r{i}"]
        st = o["sig_status_strict"]
        labs.append(st if st != "ON_SIGNATURE" else out["classes"][o["class_strict"]]["label"])
    return labs


def test_sig_block_render():
    lex = SP.load_lexicon()
    prompt, _, _ = SP.load_prompt()
    raw = json.loads((RC / "prompts" / "fewshot_v1.txt").read_text())
    for t in [f"T{i}" for i in range(1, 10)]:
        s = next(x for x in FINAL.values() if x["template_id"] == t)
        b = SP.build_signature_block(s, lex)
        body = b.split("\n", 1)[1]
        preds, consts = SP.signature_symbols(s)
        for p, a in preds.items():
            assert f"{p}/{a}:" in b
        for c in consts:
            assert c in b.split("Constants:")[-1]
        names = [l.split("/")[0] for l in body.splitlines() if not l.startswith("Constants:")]
        assert names == sorted(names, key=lambda n: (n.lower(), n))
        # structural wording never appears outside the fixed header (content glosses are checked separately)
        glossless = re.sub(r":[^\n]*", "", body)
        assert not any(re.search(r"\b" + w + r"\b", glossless.lower()) for w in SP.FORBIDDEN_WORDS)
        msgs = SP.sig_messages(s, prompt, lex)
        assert msgs[0]["content"] == raw["system"] and msgs[1:-1] == raw["exemplars"]
        assert msgs[-1]["content"].startswith(raw["user_template"].format(sentence=s["text"]))


def test_references_correct_and_case():
    for sid in list(FINAL)[:12]:
        s = FINAL[sid]
        mangled = re.sub(r"\b([A-Z][A-Za-z0-9]*)\(", lambda m: m.group(1).lower() + "(", s["reference_fol_weak"])
        labs = _label(sid, [s["reference_fol_weak"], s["reference_fol_strong"], mangled])
        assert labs == ["CORRECT", "CORRECT", "CORRECT"], (sid, labs)


def test_mutants_error():
    ok_ops = [m for m in MUT if m["operator"] not in ("MEANING_RENAME",) and m.get("subtype") != "ADD_FOREIGN"]
    ok_ops.sort(key=lambda m: hashlib.sha1(m["item_id"].encode()).hexdigest())
    picked, seen = [], {}
    for m in ok_ops:  # spread over operators
        if (seen.get(m["operator"], 0) < 4 and m["sentence_id"] in SENTS
                and LS.signature_status(m["candidate_fol"], SENTS[m["sentence_id"]])[0] == "ON_SIGNATURE"):
            picked.append(m); seen[m["operator"]] = seen.get(m["operator"], 0) + 1
        if len(picked) == 30:
            break
    assert len(picked) == 30
    for m in picked:
        lab = _label(m["sentence_id"], [m["candidate_fol"]])[0]
        assert lab in ("ERROR", "READING_CHOICE"), (m["system"], m["candidate_fol"], lab)
        if SENTS[m["sentence_id"]].get("reading_converse") is None:
            assert lab == "ERROR"


def test_controls():
    nonce = [c for c in CTR if c["control_type"] == "RENAME"][:15]
    for c in nonce:
        assert _label(c["sentence_id"], [c["candidate_fol"]])[0] == "OFF_SIGNATURE", c["candidate_fol"]
    for ct in ("REORDER", "CONTRAPOSITIVE"):
        for c in [x for x in CTR if x["control_type"] == ct][:10]:
            assert _label(c["sentence_id"], [c["candidate_fol"]])[0] == "CORRECT", (ct, c["candidate_fol"])


def test_t8_converse_reading_choice():
    t8 = [s for s in FINAL.values() if s["template_id"] == "T8"][:5]
    assert t8
    for s in t8:
        assert _label(s["sentence_id"], [s["reading_converse"]])[0] == "READING_CHOICE"


def test_offsig_arity():
    s = next(x for x in FINAL.values() if x["template_id"] == "T1")
    f = re.sub(r"\b([A-Z][A-Za-z0-9]*)\(x\)", r"\1(x, x)", s["reference_fol_weak"], count=1)
    assert _label(s["sentence_id"], [f])[0] == "OFF_SIGNATURE_ARITY"
