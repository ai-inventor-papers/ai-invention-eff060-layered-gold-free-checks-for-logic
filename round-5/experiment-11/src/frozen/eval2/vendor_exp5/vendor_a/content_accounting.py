"""Step-0 probe of CONTENT ACCOUNTING (text side of the COV invariant), run BEFORE any LLM output exists
(review critique 5 of iter 2).

content_accounting(text, fol) compares the text's content words with the word tokens projected from the formula's
predicate and constant names (CamelCase / snake split). Two alarms:
  ADD   an UNANCHORED predicate: none of its tokens matches a text content word (sortal/licensing policy: tokens
        in SORTAL = person/people/thing/entity/object/individual/human are licensed if the text has any animate or
        nominal subject, i.e. always licensed here; hedges and modals never need carrying).
  DROP  the share of text content words that no formula token carries.
Matching: EXACT (Porter stem) or LEX (stem, WordNet morphy lemma, synonyms and derivationally related forms).

Evaluation on curated FOLIO-conclusion + MALLS-test gold (arXiv 2606.02837):
  (1) false alarms on VERIFIED-CORRECT (corrected) gold, by number of predicates k;
  (2) PAIRED discrimination on the real non-equivalent (original, corrected) pairs: same text, erroneous vs correct
      formula; paired AUROC = P(score(original) > score(corrected)) + 0.5 P(tie), overall and by repair-census class.
"""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import nltk
from nltk.stem import PorterStemmer

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fol import parse  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
nltk.data.path.insert(0, str(ROOT / "nltk_data"))
from nltk.corpus import wordnet as wn  # noqa: E402

D = ROOT / "data"
PS = PorterStemmer()
TOKRE = re.compile(r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\d+")
FUNC = set("""a an the and or but nor not no none neither either both all every each any some several many much more most
less least few if then else when whenever while whereas unless except only also too than that which who whom whose what where
is are was were be been being am do does did done has have had having can could may might must shall should will would of in
on at to for from by with without into onto over under about as it its they them their there this these those he she him her
his hers we us our you your i me my one ones such same other another own so very just often usually typically generally
sometimes always never also either neither something someone somebody anything anyone everything everyone thing things
be is s t""".split())
HEDGE = {"often", "usually", "typically", "generally", "sometimes", "can", "could", "may", "might", "likely", "probably",
         "tend", "tends", "mostly", "commonly", "frequently", "normally"}
SORTAL = {"person", "people", "thing", "entity", "object", "individual", "human", "someone", "something"}


def text_words(text):
    ws = re.findall(r"[A-Za-z]+|\d+", text)
    return [w.lower() for w in ws if w.lower() not in FUNC and w.lower() not in HEDGE and w.lower() not in SORTAL and len(w) > 1]


def name_words(name):
    return [w.lower() for w in TOKRE.findall(name.replace("_", " ")) if w.lower() not in FUNC and len(w) > 1]


_lex_cache = {}


def lex(w):
    """stem-level expansion of w: its stem, WordNet lemmas of its synsets, derivationally related forms."""
    if w in _lex_cache:
        return _lex_cache[w]
    out = {PS.stem(w)}
    for pos in ("n", "v", "a", "r"):
        m = wn.morphy(w, pos)
        if m:
            out.add(PS.stem(m))
    for s in wn.synsets(w)[:4]:
        for l in s.lemmas()[:6]:
            n = l.name().lower()
            if "_" not in n:
                out.add(PS.stem(n))
            for d in l.derivationally_related_forms()[:4]:
                if "_" not in d.name():
                    out.add(PS.stem(d.name().lower()))
    _lex_cache[w] = out
    return out


def symbols(e, acc=None, bv=frozenset()):
    acc = {"preds": set(), "consts": set()} if acc is None else acc
    k = e[0]
    if k == "atom":
        acc["preds"].add(e[1])
        for a in e[2]:
            if a not in bv:
                acc["consts"].add(a)
    elif k in ("all", "ex"):
        symbols(e[2], acc, bv | {e[1]})
    elif k == "not":
        symbols(e[1], acc, bv)
    else:
        symbols(e[1], acc, bv); symbols(e[2], acc, bv)
    return acc


def content_accounting(text, fol, mode="LEX"):
    """Returns {'n_unanchored': int, 'drop_share': float, 'k': #predicates, 'unanchored': [...], 'dropped': [...]}.
    Raises ValueError on an unparseable formula (callers count it as a coverage failure)."""
    e = parse(fol) if isinstance(fol, str) else fol
    sy = symbols(e)
    tw = text_words(text)
    tstem = {PS.stem(w) for w in tw}
    tlex = set().union(*[lex(w) for w in tw]) if (mode == "LEX" and tw) else set(tstem)
    ftoks = [w for n in sy["preds"] | sy["consts"] for w in name_words(n)]
    fstem = {PS.stem(w) for w in ftoks}
    flex = set().union(*[lex(w) for w in ftoks]) if (mode == "LEX" and ftoks) else set(fstem)
    unanch = []
    for p in sy["preds"]:
        ws = name_words(p)
        if not ws or any(w in SORTAL for w in ws):
            continue
        hit = any(PS.stem(w) in tstem or (mode == "LEX" and lex(w) & tstem) for w in ws)
        if not hit:
            unanch.append(p)
    dropped = [w for w in tw if not (PS.stem(w) in fstem or (mode == "LEX" and lex(w) & fstem))]
    return {"n_unanchored": len(unanch), "drop_share": len(dropped) / max(1, len(tw)), "k": len(sy["preds"]),
            "unanchored": unanch, "dropped": dropped}


def load(p):
    return [json.loads(l) for l in open(p) if l.strip()]


def items():
    for r in load(D / "DSAVlab-UNIUD_MALLS_test_subset-CURATED__MALLS_instances.jsonl"):
        yield "MALLS", r["id"], r["NL_sentence"], r["FOL_sentence_old"], r["FOL_sentence_new"]
    for r in load(D / "DSAVlab-UNIUD_FOLIO_validation-curated__FOLIO_instances.jsonl"):
        if not str(r["id"]).startswith("story"):
            yield "FOLIO-concl", r["id"], r["NL_sentence"], r["FOL_sentence_old"], r["FOL_sentence"]


def paired_auc(pairs):
    if not pairs:
        return float("nan")
    return sum(1.0 if a > b else 0.5 if a == b else 0.0 for a, b in pairs) / len(pairs)


def main():
    rows_p = Path(__file__).with_name("repair_census.rows.json")
    census = {(r["src"], r["id"]): r for r in json.loads(rows_p.read_text())} if rows_p.exists() else {}
    for mode in ("EXACT", "LEX"):
        fa = defaultdict(Counter)
        pairs = defaultdict(list)
        nfail = 0
        for src, iid, nl, old, new in items():
            try:
                cn = content_accounting(nl, new, mode)
            except Exception:
                nfail += 1
                continue
            kb = "k1-2" if cn["k"] <= 2 else "k3-4" if cn["k"] <= 4 else "k5+"
            for b in (kb, "all"):
                fa[b]["n"] += 1
                fa[b]["add_alarm"] += cn["n_unanchored"] >= 1
                fa[b]["drop>0.34"] += cn["drop_share"] > 0.34
                fa[b]["drop>0.20"] += cn["drop_share"] > 0.20
            c = census.get((src, iid))
            if not c:
                continue
            try:
                co = content_accounting(nl, old, mode)
            except Exception:
                continue
            cls = c["cls"]
            grp = ("VOCAB/GRAN" if cls in ("VOCAB", "GRAN") else
                   "COV-type(ADD/DROP)" if any(o in cls.split("+") for o in ("ADD", "DROP")) else
                   "COMPOUND" if cls == "COMPOUND" else "STRUCT/POL-type")
            sc_o = co["n_unanchored"] + co["drop_share"]
            sc_n = cn["n_unanchored"] + cn["drop_share"]
            for g in (grp, "all-errors" if grp != "VOCAB/GRAN" else "vocab-only"):
                pairs[g].append((sc_o, sc_n))
        print(f"== mode {mode}  (unparseable correct formulas counted, not dropped: {nfail})")
        for b in ("k1-2", "k3-4", "k5+", "all"):
            f = fa[b]
            n = max(1, f["n"])
            print(f"  false alarms on correct gold {b:5s} n={f['n']:3d}  ADD(any unanchored)={f['add_alarm']/n:.2f}  "
                  f"DROP>0.20={f['drop>0.20']/n:.2f}  DROP>0.34={f['drop>0.34']/n:.2f}")
        for g, ps in sorted(pairs.items()):
            print(f"  paired AUROC (original-error scored worse than corrected) {g:20s} n={len(ps):3d}  {paired_auc(ps):.2f}")


if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    main()
