"""G2 diagnostic: recompute the mismatching sentences' candidate-peer pairs under a given PYTHONHASHSEED."""
import sys, json
sys.path.insert(0, 'src')
import pairwise as PW
from paths import jl
sids = set(sys.argv[1].split(','))
PW.init_worker()
recs = [r for r in jl('results/pair_matrix_E.jsonl') if r['sentence_id'] in sids]
import peer_text as PT
from common import eqmv
out = {}
for r in recs:
    keys = [n['canon_fol'] for n in r['nodes']]
    for i, j, e, rs, s in r['pairs']:
        res = eqmv(PT.parse_fol(keys[i]), PT.parse_fol(keys[j]))
        out[f"{r['sentence_id']}|{i}|{j}"] = res[0]
print(json.dumps(out))
