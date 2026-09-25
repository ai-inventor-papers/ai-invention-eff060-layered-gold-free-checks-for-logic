"""Re-run STAGE 7 only (labels joined to the frozen scores in results/scores_unlabelled.jsonl)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
ROOT = Path(__file__).resolve().parent.parent
import analysis
analysis.run(ROOT, ROOT / "results", B=2000)
