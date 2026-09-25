"""Download the local model weights into the run's shared HF cache (HF_HOME is preset by the harness)."""
import sys
import time
from huggingface_hub import snapshot_download

MODELS = sys.argv[1:] or ["Qwen/Qwen3-8B", "MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli",
                          "cross-encoder/nli-deberta-v3-large", "sentence-transformers/all-mpnet-base-v2",
                          "meta-llama/Llama-3.1-8B-Instruct"]
for m in MODELS:
    t0 = time.time()
    try:
        p = snapshot_download(m, allow_patterns=["*.json", "*.safetensors", "*.txt", "*.model", "tokenizer*", "*.py", "merges.txt", "vocab*",
                                                 "sentence_*", "1_Pooling/*", "modules.json", "spm.model"])
        print(f"OK {m} -> {p} in {time.time()-t0:.0f}s", flush=True)
    except Exception as e:  # noqa: BLE001
        print(f"FAIL {m}: {str(e)[:300]}", flush=True)
