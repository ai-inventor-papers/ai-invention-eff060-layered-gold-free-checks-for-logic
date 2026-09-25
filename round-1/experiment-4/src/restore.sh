#!/usr/bin/env bash
# Restore every path marked `delete` in .aii/manifest.yaml.  Usage: bash restore.sh [venv|nltk|pilot|models|all]
set -euo pipefail
cd "$(dirname "$0")"
what="${1:-all}"
if [[ "$what" == venv || "$what" == all ]]; then
  uv venv .venv --python=3.12
  grep -v -i "en-core-web-sm\|en_core_web_sm" requirements.txt > /tmp/req_noen.txt || true
  uv pip install --python .venv/bin/python -r /tmp/req_noen.txt
  .venv/bin/python -m spacy download en_core_web_sm
fi
if [[ "$what" == nltk || "$what" == all ]]; then
  mkdir -p data/nltk_data/corpora && cd data/nltk_data/corpora
  for p in words wordnet omw-1.4; do
    curl -sL -o "$p.zip" "https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/$p.zip" && unzip -q -o "$p.zip" && rm "$p.zip"
  done
  cd - >/dev/null
fi
if [[ "$what" == pilot || "$what" == all ]]; then
  python3 -c "import zipfile; zipfile.ZipFile('/ai-inventor/aii_data/runs/run_u75jRHUss0zo/user_uploads/dpv_pilot_study.zip').extractall('pilot_ref')"
fi
if [[ "$what" == models || "$what" == all ]]; then
  # model weights live in the run's shared HF cache (HF_HOME), not in this workspace
  for m in Qwen/Qwen3-8B meta-llama/Llama-3.1-8B-Instruct Qwen/Qwen3-14B MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli \
           cross-encoder/nli-deberta-v3-large sentence-transformers/all-mpnet-base-v2; do
    .venv/bin/python scripts_download.py "$m"
  done
fi
