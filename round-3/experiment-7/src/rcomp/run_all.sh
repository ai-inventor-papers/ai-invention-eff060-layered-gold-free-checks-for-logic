#!/bin/bash
# Resumable end-to-end run of every OpenRouter phase of R_COMP, in pre-registered order. Every step caches per call,
# so re-running never re-bills; a step exiting 3 means "key limit / cap reached": the script stops and can be re-run.
# The $0 steps (source pool, lexicon checks, composition, selection, PERTURB, assembly) are re-run where they depend
# on LLM results. Needs OPENROUTER_API_KEY. Hard stop: AII_HARD_CAP (default 9.5 USD, cumulative over cost_ledger.jsonl).
set -u
cd "$(dirname "$0")"
export AII_HARD_CAP=${AII_HARD_CAP:-9.5}
PY=.venv/bin/python
step() { echo "=== $(date -u +%FT%TZ) $*"; "$@"; rc=$?; if [ $rc -eq 3 ]; then echo "STOP (key limit / cap) at: $*"; exit 3; elif [ $rc -ne 0 ]; then echo "FAILED ($rc): $*"; exit $rc; fi; }
rem=$(curl -s -m 20 "${OPENROUTER_BASE_URL%/}/key" -H "Authorization: Bearer $OPENROUTER_API_KEY" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['limit_remaining'])" 2>/dev/null)
echo "key remaining today: ${rem:-unknown}"
if [ -n "$rem" ] && python3 -c "import sys; sys.exit(0 if float('$rem') < 0.3 else 1)"; then echo "key budget exhausted; retry after the daily reset"; exit 3; fi

if [ ! -s raw/generations.jsonl ]; then
  # --- pre-generation: lexicon (2a remainder, 2c audit), composition, fluency, reference audit, final selection
  # 2a extraction is closed: its $0.4 cap was reached with 57/64 jobs (plan cap rule); the 7 unextracted jobs stay out
  step $PY src/lexicon.py audit --cap 0.5
  step $PY src/lexicon.py build
  step $PY src/compose.py
  step $PY src/select_rcomp.py preselect
  step $PY src/llm_phases.py fluency --cap 0.1
  step $PY src/llm_phases.py audit --cap 0.7
  step $PY src/select_rcomp.py final
  step $PY src/perturb.py
  step $PY src/adjudicate.py select
  $PY -c "import json,hashlib,time; s=json.load(open('work/rcomp_sentences.json')); ids=sorted(x['sentence_id'] for x in s); json.dump({'frozen_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'n':len(ids),'sha256_sentence_ids':hashlib.sha256('|'.join(ids).encode()).hexdigest(),'n_audit_pending':sum(x['audit_status']=='PENDING' for x in s)},open('work/rcomp_freeze.json','w'),indent=1)"
fi
if [ ! -f work/generation_plan.json ]; then step $PY src/gen_rcomp.py pilot --cap 1.5; fi
step $PY src/gen_rcomp.py full --cap 1.5
step $PY src/label_rcomp.py
step $PY src/adjudicate.py check --cap 0.2
step $PY src/adjudicate.py queue
step $PY src/adjudicate.py run --cap 2.5
step $PY src/assemble.py
step uv run data.py
# --- pre-registered top-up (reserve of 100) if tiers A+B lack CORRECT/ERROR rows or sentences
if $PY -c "import json,sys; sys.exit(0 if json.load(open('work/testability.json'))['topup_rule_fires'] else 1)"; then
  step $PY src/gen_rcomp.py topup --cap 2.1
  step $PY src/label_rcomp.py
  step $PY src/adjudicate.py queue
  step $PY src/adjudicate.py run --cap 3.2
  step $PY src/assemble.py
  step uv run data.py
fi
$PY src/prereg.py declare || true
step $PY src/verify.py
step $PY src/card.py
SKILL_DIR=/ai-inventor/.claude/skills/aii-json
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_validate_schema.py --format exp_sel_data_out --file "$PWD/full_data_out.json"
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_format_mini_preview.py --input "$PWD/full_data_out.json" --format exp_sel_data_out \
  && mv full_full_data_out.json full_data_out.json && mv mini_full_data_out.json mini_data_out.json && mv preview_full_data_out.json preview_data_out.json
echo "=== done $(date -u +%FT%TZ)"
