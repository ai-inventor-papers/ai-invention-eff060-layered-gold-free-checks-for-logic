"""Round-trip (FOL -> NL -> compare) scoring on GPU: bidirectional NLI (DeBERTa-v3-large MNLI/FEVER/ANLI/LING/WANLI,
robustness checkpoint cross-encoder/nli-deberta-v3-large) and all-mpnet-base-v2 cosine between the source text and the
cheap-LLM verbalisation. The LLM steps (verbalise, re-formalise) live in judges.py / method.py.
"""
from __future__ import annotations

import gc
import re
import time

from loguru import logger

NLI_MAIN = "MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli"
NLI_ALT = "cross-encoder/nli-deberta-v3-large"
EMB = "sentence-transformers/all-mpnet-base-v2"


def _label_idx(model) -> dict:
    m = {v.lower(): int(k) for k, v in model.config.id2label.items()}
    return {"entail": next(i for l, i in m.items() if l.startswith("entail")),
            "contra": next(i for l, i in m.items() if l.startswith("contra"))}


def nli_probs(pairs: list[tuple[str, str]], model_name: str, batch: int = 32) -> tuple[list[dict], float]:
    """pairs of (premise, hypothesis) -> [{'entail','contra'}]. OOM -> halve batch."""
    import torch
    from transformers import AutoModelForSequenceClassification, AutoTokenizer
    from .common import disable_triton_overrides
    disable_triton_overrides()
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    tok = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name, torch_dtype=torch.float16 if dev == "cuda" else torch.float32).to(dev).eval()
    li = _label_idx(model)
    out = []
    t0 = time.time()
    i = 0
    while i < len(pairs):
        chunk = pairs[i:i + batch]
        try:
            enc = tok([p for p, _ in chunk], [h for _, h in chunk], truncation=True, max_length=384, padding=True,
                      return_tensors="pt").to(dev)
            with torch.no_grad():
                pr = torch.softmax(model(**enc).logits.float(), -1).cpu().numpy()
            for row in pr:
                out.append({"entail": float(row[li["entail"]]), "contra": float(row[li["contra"]])})
            i += batch
        except torch.cuda.OutOfMemoryError:
            torch.cuda.empty_cache()
            batch = max(1, batch // 2)
            logger.warning(f"OOM -> batch {batch}")
    secs = time.time() - t0
    del model
    gc.collect()
    if dev == "cuda":
        torch.cuda.empty_cache()
    logger.info(f"NLI {model_name}: {len(pairs)} pairs in {secs:.1f}s on {dev}")
    return out, secs


def embed_cos(pairs: list[tuple[str, str]]) -> tuple[list[float], float]:
    import torch
    from sentence_transformers import SentenceTransformer
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    m = SentenceTransformer(EMB, device=dev)
    t0 = time.time()
    a = m.encode([p for p, _ in pairs], batch_size=64, convert_to_tensor=True, normalize_embeddings=True)
    b = m.encode([h for _, h in pairs], batch_size=64, convert_to_tensor=True, normalize_embeddings=True)
    cos = (a * b).sum(-1).cpu().numpy().tolist()
    secs = time.time() - t0
    del m
    gc.collect()
    return [float(c) for c in cos], secs


def signature(fol: str) -> str:
    """Names with arities of a candidate (regex, works on unparseable strings): 'Perform/1, Attend/2, bonnie (constant)'."""
    from .disguise import formula_roles
    preds, consts = {}, []
    for m in re.finditer(r"([A-Za-z_][A-Za-z0-9_'\-]*)\s*\(([^()]*)\)", fol):
        preds.setdefault(m.group(1), len([a for a in m.group(2).split(",") if a.strip()]))
    for name, role in formula_roles(fol):
        if role == "const" and name not in consts and not re.fullmatch(r"[a-z]\d*", name):
            consts.append(name)
        if role == "pred" and name not in preds:
            preds[name] = 0
    parts = [f"{n}/{a}" for n, a in preds.items()] + [f"{c} (constant)" for c in consts]
    return ", ".join(parts)
