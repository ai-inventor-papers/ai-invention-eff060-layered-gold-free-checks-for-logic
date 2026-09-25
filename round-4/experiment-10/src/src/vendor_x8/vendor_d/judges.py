"""LLM judges, round-trip LLM steps and the gold-recall probe. All calls go through budget.Budget and are cached in
results/llm_cache.jsonl keyed by sha1(component|model|messages|params), so staged re-runs (mini -> 100 -> full) never
pay twice for the same call.
"""
from __future__ import annotations

import asyncio
import json
import math
import re
import time
from pathlib import Path

from loguru import logger

from .budget import Budget, BudgetExceeded
from .common import RES, sha1

PRIMARY = "google/gemini-2.5-flash-lite"
PRIMARY_FALLBACKS = ["qwen/qwen3-30b-a3b-instruct-2507"]  # gemini-2.0-flash-lite-001 is no longer listed on OpenRouter
SECONDARY = "openai/gpt-4.1-nano"

RUBRIC_A = ("You check whether a first-order logic formula faithfully expresses the meaning of an English sentence. "
            "Predicate and constant names may differ from the words of the sentence; logically equivalent rewritings "
            "are acceptable; judge MEANING only: quantifiers, which things are conditions vs asserted properties, "
            "negation, argument order, and whether any content is missing or added.")
CENSUS = ("Error type codes: NEG negation wrong/missing; REV implication direction reversed; QUANT wrong quantifier; "
          "RESTR restrictor misplaced (e.g. ∀x(A∧B) where ∀x(A→B) is meant, or ∃x(A→B)); CONN wrong connective "
          "(∧/∨/⊕/→/↔); MOVE content attached to the wrong part; DROP a condition or content missing; ADD content not "
          "in the sentence; SWAP arguments in the wrong order; BIND variable wrongly bound or free; SCOPE quantifier "
          "scope wrong; UNGLUE independent claims wrongly merged or split; COMPOUND several of these; NONE.")
RUBRIC_B = RUBRIC_A + " " + CENSUS
CODES = ["NEG", "REV", "QUANT", "RESTR", "CONN", "MOVE", "DROP", "ADD", "SWAP", "BIND", "SCOPE", "UNGLUE", "COMPOUND", "NONE"]
USER_JSON = ('Sentence: {text}\nFormula: {fol}\nReturn JSON: {{"faithful_prob": <0-100>, "verdict": "FAITHFUL"|"UNFAITHFUL", '
             '"error_type": <one code from the list, NONE if faithful>, "reason": "<=25 words"}}')
USER_JSON_A = ('Sentence: {text}\nFormula: {fol}\nReturn JSON: {{"faithful_prob": <0-100>, "verdict": "FAITHFUL"|"UNFAITHFUL", '
               '"error_type": <one of ' + "/".join(CODES) + ', NONE if faithful>, "reason": "<=25 words"}}')
USER_YESNO = "Sentence: {text}\nFormula: {fol}\nAnswer with one word: YES if faithful, NO otherwise."
VERBALISE = ("Translate this first-order logic formula into one plain English sentence. Say exactly what the formula says, "
             "including odd or unnatural structure; do not fix it. Read CamelCase predicate names as words. Formula: {fol}")
REFORMALISE = ("Write a first-order logic formula (symbols ∀ ∃ ¬ ∧ ∨ → ↔ ⊕) for this sentence, using ONLY these "
               "predicates/constants: {sig}. Use the notation ∀x (P(x) → Q(x)). Return only the formula on one line, "
               "no explanation. Sentence: {sent}")
RECALL = ("Translate this sentence into first-order logic in FOLIO notation: {text}\n"
          "Return only the formula on one line, no explanation.")

PROMPT_SHA = {k: sha1(v) for k, v in {"RUBRIC_A": RUBRIC_A, "RUBRIC_B": RUBRIC_B, "USER_JSON": USER_JSON,
                                      "USER_JSON_A": USER_JSON_A, "USER_YESNO": USER_YESNO, "VERBALISE": VERBALISE,
                                      "REFORMALISE": REFORMALISE, "RECALL": RECALL}.items()}

CACHE_P = RES / "llm_cache.jsonl"
_cache: dict | None = None


def _load_cache() -> dict:
    global _cache
    if _cache is None:
        _cache = {}
        if CACHE_P.exists():
            for l in CACHE_P.read_text().splitlines():
                try:
                    r = json.loads(l)
                    _cache[r["key"]] = r
                except json.JSONDecodeError:
                    continue
    return _cache


def _ckey(component, model, messages, params) -> str:
    return sha1(json.dumps([component, model, messages, params], sort_keys=True, ensure_ascii=False))


async def cached_call(b: Budget, *, component: str, model: str, messages: list[dict], max_tokens: int, item_id: str,
                      extra: dict | None = None) -> dict:
    cache = _load_cache()
    params = {"max_tokens": max_tokens, **(extra or {})}
    k = _ckey(component, model, messages, params)
    if k in cache:
        r = dict(cache[k]["resp"])
        r["cached"] = True
        return r
    r = await b.call(component=component, model=model, messages=messages, max_tokens=max_tokens, item_id=item_id,
                     extra=extra)
    rec = {"key": k, "component": component, "model": model, "item_id": item_id,
           "resp": {kk: r[kk] for kk in ("text", "logprobs", "cost", "in_tok", "out_tok", "seconds", "finish")}}
    cache[k] = rec
    with CACHE_P.open("a") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    r["cached"] = False
    return r


# ------------------------------------------------------------------ parsing
def parse_judge_json(text: str) -> dict | None:
    if not text:
        return None
    t = text.strip()
    t = re.sub(r"^```(?:json)?\s*|\s*```$", "", t)
    m = re.search(r"\{.*\}", t, re.S)
    obj = None
    if m:
        try:
            obj = json.loads(m.group(0))
        except json.JSONDecodeError:
            obj = None
    if obj is None:
        m2 = re.search(r'"?faithful_prob"?\s*:\s*"?(\d+(?:\.\d+)?)', t)
        if not m2:
            return None
        obj = {"faithful_prob": float(m2.group(1))}
        m3 = re.search(r'"error_type"\s*:\s*"([A-Z]+)"', t)
        if m3:
            obj["error_type"] = m3.group(1)
    try:
        p = float(obj.get("faithful_prob"))
    except (TypeError, ValueError):
        return None
    if math.isnan(p):
        return None
    p = min(100.0, max(0.0, p)) / 100.0
    et = str(obj.get("error_type") or "").upper().strip()
    et = et if et in CODES else ("NONE" if p >= 0.5 and not et else (et[:12] or None))
    return {"p": p, "verdict": obj.get("verdict"), "type": et, "reason": str(obj.get("reason", ""))[:200]}


def p_yes_from_logprobs(lp) -> float | None:
    try:
        tops = lp["content"][0]["top_logprobs"]
    except (TypeError, KeyError, IndexError):
        return None
    y = sum(math.exp(t["logprob"]) for t in tops if t["token"].strip().upper() == "YES")
    n = sum(math.exp(t["logprob"]) for t in tops if t["token"].strip().upper() == "NO")
    if y + n <= 0:
        return None
    return y / (y + n)


LOGIC_SYM = re.compile(r"[∀∃¬∧∨→↔⊕]|[A-Za-z_][A-Za-z0-9_]*\([^()]*\)")


def clean_verbalisation(text: str) -> tuple[str, bool]:
    """Deterministic post-processing of the verbaliser output (fixed before any label join): keep only the English
    sentence. 'The formula ¬(A ∧ B) says: "It is not ..."' -> 'It is not ...'. Returns (sentence, leaked_symbols)."""
    t = (text or "").replace("**", "").strip()
    m = re.search(r'(?:says|means|states|expresses|translates to|reads)\s*(?:that)?\s*:?\s*["“]([^"”]+)["”]', t, re.I)
    if m:
        t = m.group(1)
    else:
        lines = [l.strip() for l in t.splitlines() if l.strip()]
        t = lines[0] if lines else ""
        if re.match(r"^(the )?(formula|fol|translation|english)\b[^:]*:", t, re.I):
            t = t.split(":", 1)[1].strip()
            if not t and len(lines) > 1:  # '...translates into the following plain English sentence:' + sentence on next line
                t = lines[1]
        m2 = re.match(r"^(?:the )?(?:formula|fol|expression)\b.*?\b(?:says|states|means|expresses|asserts)\s+(?:that\s+)?(.+)$", t, re.I)
        if m2:
            t = m2.group(1).strip()
            t = t[:1].upper() + t[1:]
    t = t.strip().strip('"“”').strip()
    return t, bool(LOGIC_SYM.search(t))


def extract_formula(text: str) -> str | None:
    if not text:
        return None
    t = re.sub(r"```[a-z]*", "", text).strip()
    lines = [l.strip() for l in t.splitlines() if l.strip()]
    for l in lines:
        if re.search(r"[∀∃¬∧∨→↔⊕]|[A-Za-z_][A-Za-z0-9_]*\(", l):
            l = re.sub(r"^(formula|fol|answer)\s*:\s*", "", l, flags=re.I).strip().strip("`$").rstrip(".")
            return l
    return lines[0] if lines else None


# ------------------------------------------------------------------ task runners
async def judge_json(b: Budget, *, component: str, model: str, rubric: str, text: str, fol: str | None, item_id: str,
                     max_tokens: int = 150, extra: dict | None = None, user_tmpl: str = USER_JSON) -> dict:
    fol_s = fol if (fol and fol.strip()) else "(empty)"
    msgs = [{"role": "system", "content": rubric}, {"role": "user", "content": user_tmpl.format(text=text, fol=fol_s)}]
    ex = {"response_format": {"type": "json_object"}, **(extra or {})}
    t0 = time.time()
    cost = 0.0
    try:
        r = await cached_call(b, component=component, model=model, messages=msgs, max_tokens=max_tokens, item_id=item_id, extra=ex)
        cost += 0 if r["cached"] else r["cost"]
        out = parse_judge_json(r["text"])
        if out is None:  # one retry
            msgs2 = msgs + [{"role": "assistant", "content": r["text"] or ""},
                            {"role": "user", "content": "Return ONLY the JSON object."}]
            r2 = await cached_call(b, component=component, model=model, messages=msgs2, max_tokens=max_tokens, item_id=item_id, extra=ex)
            cost += 0 if r2["cached"] else r2["cost"]
            out = parse_judge_json(r2["text"])
            r = r2
        if out is None:
            return {"p": None, "fail": "json_parse", "raw": (r["text"] or "")[:300], "cost": cost, "seconds": time.time() - t0}
        return {**out, "fail": None, "cost": cost, "seconds": r["seconds"], "finish": r.get("finish")}
    except BudgetExceeded as e:
        return {"p": None, "fail": f"budget:{e}", "cost": cost, "seconds": time.time() - t0}
    except Exception as e:  # noqa: BLE001 - API failure is a metric failure, counted in coverage
        logger.warning(f"judge {model} {item_id} failed: {e}")
        return {"p": None, "fail": f"api:{str(e)[:120]}", "cost": cost, "seconds": time.time() - t0}


async def judge_logprob(b: Budget, *, component: str, model: str, rubric: str, text: str, fol: str | None,
                        item_id: str) -> dict:
    fol_s = fol if (fol and fol.strip()) else "(empty)"
    msgs = [{"role": "system", "content": rubric}, {"role": "user", "content": USER_YESNO.format(text=text, fol=fol_s)}]
    t0 = time.time()
    try:
        r = await cached_call(b, component=component, model=model, messages=msgs, max_tokens=1, item_id=item_id,
                              extra={"logprobs": True, "top_logprobs": 5})
        p = p_yes_from_logprobs(r["logprobs"])
        src = "logprobs"
        if p is None:
            v = (r["text"] or "").strip().upper()
            p = 1.0 if v.startswith("YES") else (0.0 if v.startswith("NO") else None)
            src = "verdict_fallback"
        return {"p": p, "fail": None if p is not None else "no_verdict", "src": src,
                "cost": 0 if r["cached"] else r["cost"], "seconds": r["seconds"]}
    except BudgetExceeded as e:
        return {"p": None, "fail": f"budget:{e}", "cost": 0, "seconds": time.time() - t0}
    except Exception as e:  # noqa: BLE001
        logger.warning(f"judge2 {item_id} failed: {e}")
        return {"p": None, "fail": f"api:{str(e)[:120]}", "cost": 0, "seconds": time.time() - t0}


async def simple_text(b: Budget, *, component: str, model: str, prompt: str, item_id: str, max_tokens: int) -> dict:
    t0 = time.time()
    try:
        r = await cached_call(b, component=component, model=model, messages=[{"role": "user", "content": prompt}],
                              max_tokens=max_tokens, item_id=item_id)
        return {"text": r["text"], "fail": None if r["text"] else "empty", "cost": 0 if r["cached"] else r["cost"],
                "seconds": r["seconds"]}
    except BudgetExceeded as e:
        return {"text": None, "fail": f"budget:{e}", "cost": 0, "seconds": time.time() - t0}
    except Exception as e:  # noqa: BLE001
        logger.warning(f"{component} {item_id} failed: {e}")
        return {"text": None, "fail": f"api:{str(e)[:120]}", "cost": 0, "seconds": time.time() - t0}


async def gather_limited(coros, label: str = ""):
    t0 = time.time()
    res = await asyncio.gather(*coros, return_exceptions=True)
    nf = sum(1 for r in res if isinstance(r, Exception))
    if nf:
        logger.error(f"{label}: {nf} tasks raised")
    logger.info(f"{label}: {len(res)} tasks in {time.time()-t0:.0f}s")
    return [r if not isinstance(r, Exception) else {"p": None, "text": None, "fail": f"exc:{r}"} for r in res]
