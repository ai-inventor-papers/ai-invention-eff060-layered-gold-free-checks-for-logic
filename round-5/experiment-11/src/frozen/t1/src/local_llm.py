"""Local open-weight LLM backend on the GPU (used because the shared OpenRouter key's $50/day limit was exhausted by
other runs at 13:29 UTC; see README). Greedy decoding (T=0), chat templates, batched left-padded generation, and
single-forward-pass P(YES) scoring. Results are cached in results/local_cache.jsonl (key = sha1(model|messages|params)).

Cost accounting: API cost 0; GPU seconds are measured per batch and amortised per item; an equivalent $ figure uses
GPU_USD_PER_HOUR (RunPod on-demand RTX 4000 Ada price, 2026-09) so metrics stay comparable in $/item.
"""
from __future__ import annotations

import gc
import json
import math
import time

from loguru import logger

from .common import RES, sha1

GPU_USD_PER_HOUR = 0.26
CACHE_P = RES / "local_cache.jsonl"
_cache = None

YES_V = ["YES", "Yes", "yes", " YES", " Yes", " yes"]
NO_V = ["NO", "No", "no", " NO", " No", " no"]


def _load_cache():
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


def _put(key, rec):
    _load_cache()[key] = rec
    with CACHE_P.open("a") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


class LocalLM:
    def __init__(self, name: str, quant: str | None = None, max_len: int = 2048):
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
        from .common import disable_triton_overrides
        disable_triton_overrides()
        self.name, self.quant = name, quant
        t0 = time.time()
        self.tok = AutoTokenizer.from_pretrained(name)
        self.tok.padding_side = "left"
        if self.tok.pad_token is None:
            self.tok.pad_token = self.tok.eos_token
        kw = {"dtype": torch.bfloat16, "device_map": "cuda"}
        if quant == "nf4":
            from transformers import BitsAndBytesConfig
            kw["quantization_config"] = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4",
                                                            bnb_4bit_compute_dtype=torch.bfloat16, bnb_4bit_use_double_quant=True)
        self.model = AutoModelForCausalLM.from_pretrained(name, **kw).eval()
        self.max_len = max_len
        self.is_qwen3 = "qwen3" in name.lower()
        logger.info(f"loaded {name} (quant={quant}) in {time.time()-t0:.0f}s; "
                    f"VRAM {torch.cuda.memory_allocated()/1e9:.1f} GB")
        self.yes_ids = sorted({i for v in YES_V for i in [self._first_id(v)] if i is not None})
        self.no_ids = sorted({i for v in NO_V for i in [self._first_id(v)] if i is not None})

    def _first_id(self, s):
        ids = self.tok.encode(s, add_special_tokens=False)
        return ids[0] if len(ids) == 1 else None

    def render(self, messages: list[dict]) -> str:
        kw = {"tokenize": False, "add_generation_prompt": True}
        if self.is_qwen3:
            kw["enable_thinking"] = False
        try:
            return self.tok.apply_chat_template(messages, **kw)
        except Exception:  # noqa: BLE001 - templates without a system role: fold system into the first user turn
            if messages and messages[0]["role"] == "system":
                m = [{"role": "user", "content": messages[0]["content"] + "\n\n" + messages[1]["content"]}] + messages[2:]
                return self.tok.apply_chat_template(m, **kw)
            raise

    def unload(self):
        import torch
        del self.model
        gc.collect()
        torch.cuda.empty_cache()

    # ----------------------------------------------------------------------------------------------------------
    def generate(self, batch_msgs: list[list[dict]], max_new_tokens: int, bs: int = 16, tag: str = "") -> list[dict]:
        """Greedy generation. Returns [{'text','seconds','cached'}] in input order."""
        import torch
        cache = _load_cache()
        keys = [sha1(json.dumps([self.name, self.quant, m, max_new_tokens, "gen"], ensure_ascii=False)) for m in batch_msgs]
        out = [None] * len(batch_msgs)
        todo = []
        for i, k in enumerate(keys):
            if k in cache:
                out[i] = {**cache[k]["resp"], "cached": True}
            else:
                todo.append(i)
        # sort by prompt length to reduce padding
        prompts = {i: self.render(batch_msgs[i]) for i in todo}
        todo.sort(key=lambda i: len(prompts[i]))
        t_all = time.time()
        j = 0
        while j < len(todo):
            idx = todo[j:j + bs]
            try:
                enc = self.tok([prompts[i] for i in idx], return_tensors="pt", padding=True, truncation=True,
                               max_length=self.max_len, add_special_tokens=False).to("cuda")
                t0 = time.time()
                with torch.no_grad():
                    gen = self.model.generate(**enc, max_new_tokens=max_new_tokens, do_sample=False, temperature=None,
                                              top_p=None, top_k=None, pad_token_id=self.tok.pad_token_id)
                secs = (time.time() - t0) / len(idx)
                for row, i in enumerate(idx):
                    txt = self.tok.decode(gen[row, enc["input_ids"].shape[1]:], skip_special_tokens=True).strip()
                    rec = {"text": txt, "seconds": secs}
                    _put(keys[i], {"key": keys[i], "model": self.name, "tag": tag, "resp": rec})
                    out[i] = {**rec, "cached": False}
                j += bs
            except torch.cuda.OutOfMemoryError:
                torch.cuda.empty_cache()
                bs = max(1, bs // 2)
                logger.warning(f"OOM in generate -> bs {bs}")
        if todo:
            logger.info(f"[{tag}] {self.name}: generated {len(todo)} in {time.time()-t_all:.0f}s "
                        f"({(time.time()-t_all)/len(todo):.2f}s/item)")
        return out

    def p_yes(self, batch_msgs: list[list[dict]], bs: int = 16, tag: str = "") -> list[dict]:
        """P(YES) / (P(YES)+P(NO)) at the first generated position (sum over case/space variants)."""
        import torch
        cache = _load_cache()
        keys = [sha1(json.dumps([self.name, self.quant, m, "pyes"], ensure_ascii=False)) for m in batch_msgs]
        out = [None] * len(batch_msgs)
        todo = [i for i, k in enumerate(keys) if k not in cache]
        for i, k in enumerate(keys):
            if k in cache:
                out[i] = {**cache[k]["resp"], "cached": True}
        prompts = {i: self.render(batch_msgs[i]) for i in todo}
        todo.sort(key=lambda i: len(prompts[i]))
        t_all = time.time()
        j = 0
        while j < len(todo):
            idx = todo[j:j + bs]
            try:
                enc = self.tok([prompts[i] for i in idx], return_tensors="pt", padding=True, truncation=True,
                               max_length=self.max_len, add_special_tokens=False).to("cuda")
                t0 = time.time()
                with torch.no_grad():
                    logits = self.model(**enc, logits_to_keep=1).logits[:, -1, :].float()
                lp = torch.log_softmax(logits, -1).cpu()
                secs = (time.time() - t0) / len(idx)
                for row, i in enumerate(idx):
                    y = sum(math.exp(lp[row, t].item()) for t in self.yes_ids)
                    n = sum(math.exp(lp[row, t].item()) for t in self.no_ids)
                    p = y / (y + n) if y + n > 0 else None
                    rec = {"p": p, "mass_yes_no": y + n, "seconds": secs}
                    _put(keys[i], {"key": keys[i], "model": self.name, "tag": tag, "resp": rec})
                    out[i] = {**rec, "cached": False}
                j += bs
            except torch.cuda.OutOfMemoryError:
                torch.cuda.empty_cache()
                bs = max(1, bs // 2)
                logger.warning(f"OOM in p_yes -> bs {bs}")
        if todo:
            logger.info(f"[{tag}] {self.name}: scored {len(todo)} in {time.time()-t_all:.0f}s")
        return out


def sample_many(lm: "LocalLM", batch_msgs: list[list[dict]], n: int, max_new_tokens: int, temperature: float = 0.7,
                bs: int = 16, tag: str = "", seed: int = 0) -> list[list[str]]:
    """n samples per prompt at temperature T (top_p 1.0), cached per (prompt, n, T); torch seed fixed per batch."""
    import torch
    cache = _load_cache()
    keys = [sha1(json.dumps([lm.name, lm.quant, m, max_new_tokens, "sample", n, temperature, seed], ensure_ascii=False))
            for m in batch_msgs]
    out = [None] * len(batch_msgs)
    todo = []
    for i, k in enumerate(keys):
        if k in cache:
            out[i] = cache[k]["resp"]["texts"]
        else:
            todo.append(i)
    prompts = {i: lm.render(batch_msgs[i]) for i in todo}
    todo.sort(key=lambda i: len(prompts[i]))
    t_all = time.time()
    j = 0
    while j < len(todo):
        idx = todo[j:j + bs]
        try:
            enc = lm.tok([prompts[i] for i in idx], return_tensors="pt", padding=True, truncation=True,
                         max_length=lm.max_len, add_special_tokens=False).to("cuda")
            torch.manual_seed(seed + j)
            t0 = time.time()
            with torch.no_grad():
                gen = lm.model.generate(**enc, max_new_tokens=max_new_tokens, do_sample=True, temperature=temperature,
                                        top_p=1.0, top_k=0, num_return_sequences=n, pad_token_id=lm.tok.pad_token_id)
            secs = (time.time() - t0) / len(idx)
            L = enc["input_ids"].shape[1]
            for row, i in enumerate(idx):
                texts = [lm.tok.decode(gen[row * n + s, L:], skip_special_tokens=True).strip() for s in range(n)]
                _put(keys[i], {"key": keys[i], "model": lm.name, "tag": tag, "resp": {"texts": texts, "seconds": secs}})
                out[i] = texts
            j += bs
        except torch.cuda.OutOfMemoryError:
            torch.cuda.empty_cache()
            bs = max(1, bs // 2)
            logger.warning(f"OOM in sample_many -> bs {bs}")
    if todo:
        logger.info(f"[{tag}] {lm.name}: sampled {len(todo)}x{n} in {time.time()-t_all:.0f}s")
    return out
