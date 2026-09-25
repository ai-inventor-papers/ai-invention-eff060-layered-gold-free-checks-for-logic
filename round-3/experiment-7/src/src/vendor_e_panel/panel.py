"""Family-disjoint LLM panel: one batched call per (sentence, model, <=8 formulas), disguised, blind, cached.

Cache key = sha1(sentence_id | model | PROMPT_SHA1 | sorted class_ids) -> work/panel_cache.jsonl (never re-billed).
Formulas are shown shuffled (seed = sha1(sentence_id)), unlabelled; the reference class is one of them.
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))  # PATCH iter3 exp7: vendored location
from or_client import BudgetExceeded, Client  # noqa: E402

CACHE = Path(__file__).resolve().parents[2] / "results" / "panel_cache.jsonl"  # PATCH iter3 exp7
MEMBERS = {
    "P1": {"model": "anthropic/claude-haiku-4.5", "family": "anthropic", "params": {"temperature": 0.0, "max_tokens": 1500}},
    "P2": {"model": "x-ai/grok-4.3", "family": "xai", "params": {"temperature": 0.0, "max_tokens": 1200, "reasoning": {"enabled": False}}},
    "P3": {"model": "z-ai/glm-4.6", "family": "zhipu", "params": {"temperature": 0.0, "max_tokens": 1500, "reasoning": {"enabled": False}}},
    "P1alt": {"model": "anthropic/claude-sonnet-4.6", "family": "anthropic", "params": {"temperature": 0.0, "max_tokens": 1500}},
    "R1": {"model": "moonshotai/kimi-k2-0905", "family": "moonshot", "params": {"temperature": 0.0, "max_tokens": 1500}},
    "R2": {"model": "minimax/minimax-01", "family": "minimax", "params": {"temperature": 0.0, "max_tokens": 1500}},
}
OPS = {
    "NEG": "a negation is missing, added or misplaced",
    "REV": "an implication points the wrong way (condition and consequence swapped, 'only if' misread)",
    "QUANT": "universal used where existential is meant, or vice versa",
    "RESTR": "a restriction is rendered with the wrong connective (e.g. ∀x (A(x) ∧ B(x)) instead of ∀x (A(x) → B(x)), or ∃x (A → B) instead of ∃x (A ∧ B))",
    "CONN": "another wrong connective (and / or / exclusive-or / iff)",
    "MOVE": "a condition is attached to the wrong part of the formula (antecedent vs consequent, wrong clause)",
    "DROP": "something the sentence states is missing",
    "ADD": "something the sentence does not state is added",
    "SWAP": "arguments of a relation are in the wrong order or roles",
    "BIND": "a wrong variable or constant is used in an argument slot (wrong binding, wrong individual)",
    "SCOPE": "wrong scope or order of quantifiers, or of a negation relative to a quantifier",
    "UNGLUE": "independent claims are glued under one quantifier block (or one claim wrongly split)",
    "OTHER": "any other meaning difference",
}
TEMPLATE = (
    "Below is an English sentence and a numbered list of candidate first-order logic (FOL) formalizations of it. "
    "Content words have been replaced by invented words, consistently in the sentence and in the formulas; treat them "
    "as unknown concepts. A formula may also use invented words that do not occur in the sentence: they stand for the "
    "translator's own paraphrase of a sentence word.\n\n"
    "Sentence: {sentence}\n\nFormulas:\n{formulas}\n\n"
    "Notation: ∀ ∃ quantifiers; ¬ not; ∧ and; ∨ inclusive or; → implies; ↔ if and only if; ⊕ exclusive or. "
    "Lower-case arguments not bound by a quantifier are constants (named individuals or specific things).\n\n"
    "For EACH formula decide independently whether it is FAITHFUL to the sentence: it says what the sentence says, no "
    "more and no less. Different predicate or constant names, splitting one concept into several predicates or merging "
    "several into one, and logically equivalent forms (contrapositive, De Morgan, reordering, moving quantifiers) are "
    "all fine. Remember in particular: A → B is equivalent to its contrapositive ¬B → ¬A (this is NOT a reversed "
    "implication); ¬(A ∧ B) is equivalent to ¬A ∨ ¬B; ¬¬A is equivalent to A; ∀x ∀y (…) and ∀x (∀y (…)) are the same; "
    "extra parentheses change nothing. Check such rewrites by logic, not by surface form. "
    "Judge meaning, not style. If the sentence has two legitimate readings, a formula that matches either "
    "reading is faithful; then also set sentence_ambiguous to true.\n\n"
    "If a formula is unfaithful, list ALL applicable error operators:\n{ops}\n\n"
    "Return ONLY a JSON object, no other text:\n"
    '{{"judgements": [{{"id": "F1", "faithful": true or false, "ops": ["..."], "confidence": 1-5}}, ...], '
    '"sentence_ambiguous": true or false}}\n'
    "confidence: 5 = certain, 1 = guess. Use an empty ops list for a faithful formula.")
OPS_TXT = "\n".join(f"- {k}: {v}" for k, v in OPS.items())
PROMPT_SHA1 = hashlib.sha1((TEMPLATE + OPS_TXT).encode()).hexdigest()


def cache_key(sentence_id: str, model: str, class_ids: list[str]) -> str:
    return hashlib.sha1(f"{sentence_id}|{model}|{PROMPT_SHA1}|{'|'.join(sorted(class_ids))}".encode()).hexdigest()


def load_cache() -> dict:
    out = {}
    if CACHE.exists():
        for line in CACHE.read_text().splitlines():
            if line.strip():
                r = json.loads(line)
                if r.get("parsed"):  # failed calls (parsed=False) are retried, never served from cache
                    out[r["key"]] = r
    return out


def build_prompt(sentence: str, items: list[tuple[str, str]], seed: str) -> tuple[str, list[str]]:
    order = list(items)
    random.Random(int(hashlib.sha1(seed.encode()).hexdigest()[:12], 16)).shuffle(order)
    fl = "\n".join(f"F{i + 1}: {f}" for i, (_, f) in enumerate(order))
    return TEMPLATE.format(sentence=sentence, formulas=fl, ops=OPS_TXT), [cid for cid, _ in order]


def parse_reply(text: str, n: int) -> dict | None:
    if not text:
        return None
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        return None
    try:
        d = json.loads(m.group(0))
    except json.JSONDecodeError:
        return None
    js = d.get("judgements")
    if not isinstance(js, list):
        return None
    out = {}
    for j in js:
        try:
            idx = int(str(j.get("id", "")).lstrip("Ff")) - 1
        except ValueError:
            continue
        if 0 <= idx < n and isinstance(j.get("faithful"), (bool, str)):
            fv = j["faithful"] if isinstance(j["faithful"], bool) else str(j["faithful"]).lower() in ("true", "yes")
            ops = [o for o in (j.get("ops") or []) if isinstance(o, str)]
            out[idx] = {"faithful": fv, "ops": [o.upper() for o in ops], "conf": j.get("confidence")}
    if len(out) != n:
        return None
    amb = d.get("sentence_ambiguous")
    return {"per": out, "ambiguous": bool(amb) if isinstance(amb, bool) else str(amb).lower() in ("true", "yes")}


class Panel:
    def __init__(self, client: Client, lock: asyncio.Lock | None = None):
        self.client = client
        self.cache = load_cache()
        self.lock = lock or asyncio.Lock()

    async def judge(self, member: str, sentence_id: str, sentence: str, items: list[tuple[str, str]], tag: str = "") -> dict:
        """items = [(class_id, disguised_fol)] (<=8). Returns {class_id: verdict} + ambiguous, or {'error': ...}."""
        cfg = MEMBERS[member]
        cids = [c for c, _ in items]
        key = cache_key(sentence_id, cfg["model"], cids)
        if key in self.cache:
            r = self.cache[key]
            return {"verdicts": r["verdicts"], "ambiguous": r["ambiguous"], "cached": True}
        prompt, order = build_prompt(sentence, items, sentence_id)
        msgs = [{"role": "user", "content": prompt}]
        cost, parsed, texts = 0.0, None, []
        for attempt in range(2):
            r = await self.client.chat(cfg["model"], msgs, tag=f"{member}:{tag}:{sentence_id}", retries=3, **cfg["params"])
            cost += r["cost_usd"]
            texts.append(r["text"] if r["text"] is not None else f"ERROR {r['error']}")
            parsed = parse_reply(r["text"], len(order))
            if parsed is not None or r["text"] is None:
                break
            msgs = msgs + [{"role": "assistant", "content": r["text"] or ""},
                           {"role": "user", "content": "Your reply was not a valid JSON object with one judgement per formula. Return ONLY the JSON object."}]
        rec = {"key": key, "sentence_id": sentence_id, "member": member, "model": cfg["model"], "prompt_sha1": PROMPT_SHA1,
               "shown_order": order, "texts": texts, "cost_usd": cost, "parsed": parsed is not None}
        if parsed is not None:
            rec["verdicts"] = {order[i]: v for i, v in parsed["per"].items()}
            rec["ambiguous"] = parsed["ambiguous"]
        async with self.lock:
            with open(CACHE, "a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        if parsed is None:
            return {"error": texts[-1][:200]}
        self.cache[key] = rec
        return {"verdicts": rec["verdicts"], "ambiguous": rec["ambiguous"], "cached": False}


def chunks(items: list, k: int = 8) -> list[list]:
    if len(items) <= k:
        return [items]
    n = -(-len(items) // k)
    size = -(-len(items) // n)
    return [items[i:i + size] for i in range(0, len(items), size)]


async def gather_guarded(coros):
    out = []
    for fut in asyncio.as_completed(coros):
        try:
            out.append(await fut)
        except BudgetExceeded as e:
            out.append({"error": f"budget: {e}"})
    return out
