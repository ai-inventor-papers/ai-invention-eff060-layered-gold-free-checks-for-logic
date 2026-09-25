import sys, json, time
sys.path.insert(0, 'src'); import common
from freelab import label_candidate
S = json.load(open('work/sentences.json'))
rows = [json.loads(l) for l in open('work/free_rows.jsonl')]
rows = [r for r in rows if r['input_status'] == 'PARSED']
import random; random.seed(3)
for r in random.sample(rows, 12):
    s = S[r['sentence_id']]
    rd = {'weak': s['reference_fol_weak'], 'strong': s['reference_fol_strong']}
    if s.get('reading_converse'): rd['converse'] = s['reading_converse']
    t = time.time()
    out = label_candidate(r['candidate_fol'], rd, s['units'])
    print(s['template_id'], r['candidate_fol'][:150])
    print('  ->', out['status'], out.get('matched_reading'), 'maps', out.get('n_maps_enumerated'), 'fp', out.get('n_maps_fingerprint_pass'), 'eq', out.get('n_equiv_maps'), out.get('nonequiv_certificate_type_counts'), f'{time.time()-t:.1f}s')
    if out.get('equiv_maps'):
        print('   map', out['equiv_maps'][0]['map'], out['equiv_maps'][0]['bridges'])
        print('   pairs', out['gloss_pairs_per_map'][0][:8])
