#!/bin/bash
# Restore every path marked `delete` in .aii/manifest.yaml.  Usage: bash restore.sh [venv|nltk|models|all]  (default all)
set -e
cd "$(dirname "$0")"
what=${1:-all}
if [[ "$what" == venv || "$what" == all ]]; then
  uv venv .venv --python=3.12
  uv pip install --python .venv/bin/python -r requirements.txt
  # this box's NVIDIA driver supports CUDA 12.8: the default torch 2.14 (cu13) wheel cannot initialise CUDA
  uv pip install --python .venv/bin/python "torch==2.11.0" --index-url https://download.pytorch.org/whl/cu128 --reinstall-package torch
fi
if [[ "$what" == nltk || "$what" == all ]]; then
  mkdir -p data/nltk_data
  .venv/bin/python -c "import nltk; [nltk.download(p, download_dir='data/nltk_data') for p in ('wordnet', 'omw-1.4', 'words')]"
fi
if [[ "$what" == models || "$what" == all ]]; then
  # weights go to the run's shared HF cache (HF_HOME preset by the harness), never into this workspace
  .venv/bin/python scripts_download.py Qwen/Qwen3-8B Qwen/Qwen3-14B meta-llama/Llama-3.1-8B-Instruct \
    MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli cross-encoder/nli-deberta-v3-large sentence-transformers/all-mpnet-base-v2
fi
