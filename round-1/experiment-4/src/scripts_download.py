"""Download all local model weights into the run's shared HF cache (HF_HOME already set by the harness)."""
import sys, time
from huggingface_hub import snapshot_download
t0 = time.time()
m = sys.argv[1]
p = snapshot_download(m, allow_patterns=["*.json", "*.safetensors", "*.model", "*.txt", "tokenizer*", "*.py"],
                      ignore_patterns=["original/*", "*.pth", "*.bin", "onnx/*", "openvino/*"], max_workers=8)
print(m, p, f"{time.time()-t0:.0f}s", flush=True)
