#!/bin/bash
# Final label-joined pass: gate report, feature table, analysis (+tables, summary, method_out), audit, schema check, previews.
set -e
export PYTHONHASHSEED=0
cd "$(dirname "$0")"
.venv/bin/python method.py --stage b2_gate_report > logs/final_gate.log 2>&1
.venv/bin/python method.py --stage s4 > logs/final_s4.log 2>&1
.venv/bin/python method.py --stage analysis > logs/final_analysis.log 2>&1
.venv/bin/python tests/audit_E.py > logs/final_audit.log 2>&1
SKILL_DIR=/ai-inventor/.claude/skills/aii-json
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_validate_schema.py --format exp_gen_sol_out --file "$(pwd)/method_out.json"
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_format_mini_preview.py --input "$(pwd)/method_out.json"
ls -la *method_out.json
