#!/usr/bin/env bash
# Restore everything the manifest deletes after the round (venv, local GGUF models, NLTK data).
set -euo pipefail
cd "$(dirname "$0")"
uv venv .venv --python=3.12
uv pip install --python .venv/bin/python -r requirements.txt
uv pip install --python .venv/bin/python "llama-cpp-python" --only-binary llama-cpp-python \
  --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu
mkdir -p models src/data
.venv/bin/python - <<'PY'
from huggingface_hub import hf_hub_download
for repo, f in [("Qwen/Qwen2.5-1.5B-Instruct-GGUF", "qwen2.5-1.5b-instruct-q4_k_m.gguf"),
                ("bartowski/gemma-2-2b-it-GGUF", "gemma-2-2b-it-Q4_K_M.gguf"),
                ("bartowski/Llama-3.2-1B-Instruct-GGUF", "Llama-3.2-1B-Instruct-Q4_K_M.gguf")]:
    print(hf_hub_download(repo, f, local_dir="models"))
PY
E8=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/nltk_data
if [ -d "$E8" ]; then cp -r "$E8" src/data/; else .venv/bin/python -m nltk.downloader -d src/data/nltk_data wordnet omw-1.4 words; fi
