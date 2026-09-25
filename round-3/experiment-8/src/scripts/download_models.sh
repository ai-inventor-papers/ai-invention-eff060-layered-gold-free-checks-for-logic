#!/bin/bash
# Pre-download every local model this artifact uses into the run's shared HF cache (HF_HOME is preset by the platform).
set -e
cd "$(dirname "$0")/.."
PY=.venv/bin/python
$PY - <<'PYEOF'
from concurrent.futures import ThreadPoolExecutor
from huggingface_hub import snapshot_download
import time
M = [("Qwen/Qwen3-8B", ["*.json", "*.safetensors", "*.txt", "merges.txt", "vocab.json", "tokenizer*"]),
     ("meta-llama/Llama-3.1-8B-Instruct", ["*.json", "*.safetensors", "tokenizer*"]),
     ("MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli", None),
     ("cross-encoder/nli-deberta-v3-large", None),
     ("sentence-transformers/all-mpnet-base-v2", None)]
def dl(m):
    t = time.time()
    kw = {"allow_patterns": m[1]} if m[1] else {"ignore_patterns": ["*.onnx", "*.h5", "*.msgpack", "*.ot", "onnx/*", "openvino/*", "*.bin"] if "mpnet" in m[0] or "cross-encoder" in m[0] or "Moritz" in m[0] else []}
    try:
        p = snapshot_download(m[0], max_workers=8, **kw)
        print("OK", m[0], round(time.time() - t), p, flush=True)
    except Exception as e:
        print("FAIL", m[0], repr(e)[:300], flush=True)
with ThreadPoolExecutor(5) as ex:
    list(ex.map(dl, M))
PYEOF
