# gen_demo_art_experiment_7 — report_results

> Phase: `gen_paper_repo` · `gen_demo_art`
> Run: `run_u75jRHUss0zo` — Gold-Free Faithfulness Metrics for NL-to-FOL Translation
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_demo_art_experiment_7` (terminal_claude_agent, claude-opus-5-5)

### [1] CONFIG · 2026-09-24 18:32:56 UTC

```
model: claude-opus-5-5 | effort: high | permission: bypassPermissions
```

### [2] SYSTEM-USER prompt · 2026-09-24 18:33:02 UTC

````
<conversion_philosophy>
**MINIMAL CHANGES — PRESERVE THE ORIGINAL CODE**

The goal is to make the artifact's code READABLE, UNDERSTANDABLE, and RUNNABLE in a short time
to someone reviewing the research, with the option to easily scale parameters back to original
values for a full run (which can take much longer). Think of this as annotating and reformatting,
not refactoring.

**DO:**
- Split the original script into logical notebook cells (imports, setup, processing, results)
- Add markdown cells BETWEEN code cells explaining what each section does and why
- Add inline comments where the logic is non-obvious
- Add a visualization/summary cell at the end showing key outputs
- Fix hardcoded file paths to use the GitHub data loading pattern

**DO NOT:**
- Rewrite functions or change algorithms
- Rename variables or restructure logic
- Add error handling, type hints, or "improvements" that weren't in the original
- Simplify or "clean up" the original code
- Remove any original comments or logic
- Change the computational approach

The reader should recognize the original script when looking at the notebook — it's the
same code, just split into cells with explanatory markdown between sections.
</conversion_philosophy>

<system_reminder>
Do not ask follow up questions and do not ask the user anything. Execute all steps independently.
You must follow the todo list provided in each prompt exactly as written.
No placeholders, stubs, or incomplete code — all code must be complete and functional.
</system_reminder>

<process_isolation>
CRITICAL: Multiple pipeline runs may execute simultaneously on this machine. `ps aux | grep method.py` matches ALL runs, not just yours.
- NEVER kill processes by name (`killall`, `pkill -f`, `ps aux | grep ... | xargs kill`). This kills OTHER runs' processes.
- NEVER monitor processes by name (`ps aux | grep method.py`). You will see other runs' processes and get confused.
- ALWAYS use PID-based process management:
  Run: `uv run method.py & PID=$!` or `timeout <seconds> uv run method.py & PID=$!`
  Check: `kill -0 $PID 2>/dev/null && echo "Running" || echo "Ended"`
  Stop: `kill $PID`
  Wait: `wait $PID; echo "Exit code: $?"`
  Monitor: `tail -f logs/run.log & TAIL_PID=$!` then `kill $TAIL_PID` when done
</process_isolation>

<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_YYD-HDzfQfEj`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_YYD-HDzfQfEj/`:
GOOD: `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_YYD-HDzfQfEj/file.py`, `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_YYD-HDzfQfEj/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
<disposable_outputs>
A SHARED CACHE ALREADY EXISTS FOR THIS RUN: `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/.shared_cache`
`HF_HOME`, `HF_HUB_CACHE`, `TRANSFORMERS_CACHE`, `HF_DATASETS_CACHE`,
`TORCH_HOME`, `PIP_CACHE_DIR` and `UV_CACHE_DIR` are ALREADY set to point
there. Every step and every iteration of this run shares it, so a model or
dataset an earlier experiment downloaded is already on disk for you.

DO NOT override those variables. In particular do NOT write the common
pattern `os.environ["HF_HOME"] = <workspace>/hf_cache` — `HF_HOME` and
`TRANSFORMERS_CACHE` are read differently by `huggingface_hub` (one has
`/hub` appended, the other does not), so pointing both at one directory
stores every weight TWICE. That mistake cost one run 25 GB of identical
blobs. If you must set them, use the values above verbatim.

YOUR WORKING DIRECTORY IS A DELIVERABLE. When this module ends it must read
like a GitHub repository someone else can fork, resume and run — and the bulk
it holds must be either worth keeping or restorable. This run shares a storage
volume with the database; a run that fills it stops every other run on the box.

So before you finish, produce TWO files:

1. `.aii/manifest.yaml` — one entry per heavy path, each with EXACTLY ONE decision.
   The `.aii/` directory ALREADY EXISTS in your cwd: write the file into
   it. Do not create, replace or `touch` `.aii` itself — a plain file by
   that name makes the manifest unwritable for the rest of the module.

```yaml
entries:
  - path: results/
    keep: six GPU-hours of sweep output, not reproducible inside this run
  - path: hf_cache/
    delete: redownloadable
    source: "huggingface-cli download meta-llama/Llama-3-8B"
  - path: checkpoints/
    delete: regenerable
    source: "uv run train.py --epochs 3 --seed 0"
```

   - `keep:` takes a ONE-LINE reason. Use it for the expensive and the
     irreproducible: trained weights, long-running results, datasets you
     collected yourself.
   - `delete:` takes `redownloadable` (and a `source:` naming the repo id, URL
     or command) or `regenerable` (and a `source:` that is the command which
     rebuilds it). These are deleted AFTER the round ends, never mid-step.
   - Every path is RELATIVE TO YOUR CWD and must resolve INSIDE it. Absolute
     paths, `..`, and anything resolving outside are rejected.
   - Globs and whole directories are fine. A whole `hf_cache/` is ONE entry —
     do not list files individually.

2. `README.md` — written as if your cwd were a GitHub repository: what you
   did, the layout with a line per important file/directory, how to run it,
   and a **"Restoring removed files"** section giving the install/download
   command for EVERY `delete` entry. An `install.sh` or `restore.sh` beside it
   is welcome.

A CHECKER RUNS WHEN YOU SUBMIT. If anything heavy has no decision it fails
your submission and hands you the uncovered list, grouped by directory with
sizes, and you fix the manifest and submit again.

WHAT NEEDS NO DECISION — do not write entries for these:
- text and code files, at ANY size (source, JSON, CSV, YAML, logs, markdown);
- anything under the auto-keep floor (10 MB), whatever it holds.
Only large binaries and cache directories (`hf_cache/`, `.venv/`,
`node_modules/`, `checkpoints/`, `wandb/`, `__pycache__/`, …) need one.

NEVER mark your results, figures, papers, code, logs or anything a later step
reads as `delete`. If a later step needs it, it is a `keep`.

WHAT A `keep` BUYS YOU. Anything you do not mark `delete` stays exactly where
you wrote it, on this run's storage volume, at the path it already has — it is
not moved, renamed or copied. A later round reads it there, by that absolute
workspace path, so a checkpoint you keep is a checkpoint the next round can
load instead of retraining. It is also the ONLY copy: the publish step pushes
your cwd to GitHub but skips every file of 100 MB or
more, so trained weights and large binary artifacts never leave the volume.
Name each kept artifact in your results and your `README.md` by its path
RELATIVE to your cwd, and say it stays on the run's volume rather than in the
published repository. Never write an absolute server path into a file that is
published: a reader's machine has none of them.
</disposable_outputs>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<task>
Convert this artifact's Python script into a demo notebook with MINIMAL changes to the original code.
Split into cells, add markdown explanations between sections, add a visualization cell at the end.
Output: mini_demo_data.json + code_demo.ipynb (notebook that loads data from GitHub URL)
</task>

<artifact_info>
id: art_YYD-HDzfQfEj
type: experiment
title: Rename-proof logic consensus and error-type tests
summary: >-
  Iteration-3 T3+T5 experiment (workspace gen_art_experiment_8). PART A: PEER_HYB consensus = ALIGN (name-similarity eqmv)
  OR NF-anchored name-free map, z3-verified; pair verdicts for every E candidate-peer pair in results/pairs_E.jsonl (sentence_id,
  cand, peer, align_eq, nf_eq, hyb_eq, nf_cost; joinable by T4). Pre-registered selection (results/prereg_hyb.json, frozen
  before label join): NEITHER HYB nor NF-anchored eligible (rename FA on PERTURB RENAME_SYN/NONCE HYB 0.841/0.700, NF 0.686/0.485
  at screen thresholds; exp D RENAME 0.050/0.030) -> nothing frozen, sibling R_COMP read uses ALIGN (results/selection.json).
  Mechanism: NF keeps 100% of a base's peer endorsers under renames (flip 0), HYB 74-75%, ALIGN 0-33%; NF's FA equals the
  unrenamed-reference FA (references often unendorsed on long sentences). E R_AB stratified AUROC (sentence-cluster CI): c_hyb
  0.738, c_align 0.741, c_nf 0.686; HYB-ALIGN -0.004 [-0.011,0.004]; HYB-NF +0.052; HYB-local Qwen judge +0.060 [0.018,0.100];
  placebo 0.515. Over-alignment: HYB's extra agreements are label-discordant 0.388 vs 0.127 for ALIGN agreements. PART B:
  27 metrics on 4,234 PERTURB mutants + 868 controls + 300 bases (results/perturb_scores.jsonl, perturb_sensitivity.csv, perturb_downup.csv,
  invariance_table.csv, tradeoff.csv, coverage_perturb.csv; prereg_perturb.json). Within-base AUROC over all E-base mutants:
  PEER+TEXT 0.948, c_align 0.866, c_hyb 0.847, p_text 0.845, l3 0.816, c_nf 0.785 (0.50 on MEANING_RENAME), S4_local 0.753,
  round-trip NLI 0.749, flash-lite judge (disguised) 0.680, SC-5 0.666, L2-bow 0.659, local Llama/Qwen judges (nf4) 0.653/0.643,
  pilot metrics ~0.50. Consensus polarity-symmetric (|DOWN-UP|<0.01); local judges, embedding round trip and L3 miss DOWN
  edits (-0.12 to -0.15). PART C: peer-medoid typed-repair typing 0.328 [0.277,0.387] > majority 0.177; oracle 0.802; 20 s
  fallback unchanged. PART D: src/consensus_lib.py (consensus_score exact/align/nf/hyb, graded_consensus, peer_pool, equivalent_modulo_vocab,
  minimal_typed_repair) + tests (31 pass). Deviations: 16 GB GPU -> nf4 local judges with thresholds refit on nf4 E calibration
  rows (AUROC cost 0.015-0.035); S4 full-E fit. Cost $0.35 OpenRouter. Independent raw re-derivation (tests/audit_raw.py)
  reproduces all headline numbers exactly; placebos ~0.5.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_8
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json
- reproducibility.md
out_demo_files:
- path: method.py
  description: Research methodology implementation
</artifact_info>

<github_repo>
Repo URL: https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic
Raw data URL: https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/main/round-3/experiment-8/demo/mini_demo_data.json

URLs won't work yet — files pushed to GitHub AFTER notebook creation.
Use local fallback pattern so notebook works locally (now) and in Colab (after deployment).
</github_repo>

<data_file_sizes>
Data files come in three sizes:
- preview_*_out.json — READ THIS to inspect the data structure
- mini_*_out.json (~3 examples) — use for prototyping/testing
- full_*_out.json (complete) — use for the final production run. NEVER open it directly (too large to read into context). Instead, extract values programmatically with shell commands (e.g. grep) or a Python script (use aii-long-running-tasks skill for scripts).
</data_file_sizes>

<install_dependencies_pattern>
Follow the aii-colab skill exactly. It has the install cell pattern, pre-installed package list, numpy 2.0 compat shims, and all Colab-specific rules.
</install_dependencies_pattern>

<data_loading_pattern>
`mini_demo_data.json` = curated subset for the demo.
Use this pattern for Colab compatibility (GitHub URL with local fallback):
```python
GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/main/round-3/experiment-8/demo/mini_demo_data.json"
import json
from pathlib import Path

def load_data():
    try:
        import urllib.request
        with urllib.request.urlopen(GITHUB_DATA_URL) as response:
            return json.loads(response.read().decode())
    except Exception: pass
    local = Path("mini_demo_data.json")
    if local.exists(): return json.loads(local.read_text())
    raise FileNotFoundError("Could not load mini_demo_data.json")
```
</data_loading_pattern>

<notebook_structure>
--- Setup ---
Cell 1 (markdown): Title, description, what this artifact does.
Cell 2 (code): Install dependencies — follow the aii-colab skill's install cell pattern exactly. Fill in all packages imported by the artifact's code.
Cell 3 (code): Imports — copy original import block as-is, plus any additional imports needed for the notebook (e.g. matplotlib for visualization).
Cell 4 (code): Data loading helper — use the <data_loading_pattern> above.
Cell 5 (code): `data = load_data()`

--- Config ---
Config cell (code): Define ALL tunable parameters (iterations, epochs, n_samples, hidden_size, etc.) as variables at the top of this cell. Start with the ABSOLUTE MINIMUM values — the smallest that produce any output at all (e.g. 1 iteration, 2 samples, smallest array size). These get gradually increased during testing — see TODOs.

--- Processing ---
Remaining cells: One code cell per logical section of the original script. Add a markdown cell BEFORE each code cell. Copy code as closely as possible, with these changes:
  1. Replace file paths to use the loaded `data` variable.
  2. Use the config variables from the config cell (NOT hardcoded values).
  3. Minimal fixes are allowed if something doesn't work in notebook context (e.g. adjusting paths, removing CLI args, fixing imports), but keep changes to the absolute minimum.

--- Results ---
Visualization cell (code): Print key results in a readable table, plot numeric data with matplotlib if appropriate.
</notebook_structure>

<priority>
WORKING > OPTIMIZED. A small-scale demo that runs correctly is the goal. Once the notebook passes with minimum config values, scale up only if time permits — do NOT spend multiple retries chasing larger parameters. If a working version exists, finish and move on.
</priority>

<max_notebook_total_runtime>600s (10 min)</max_notebook_total_runtime>

<test_environment>
To test-run the notebook in a clean environment (simulating Colab), create a disposable `.nb_env` in your workspace:
```bash
/usr/local/bin/python3.12 -m venv .nb_env
.nb_env/bin/pip install -q pip jupyter ipykernel
.nb_env/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb
rm -rf .nb_env
```
The timeout is set to <max_notebook_total_runtime>. The entire notebook must finish within this time.

What happens: the .venv starts empty (just jupyter). When the notebook's install cell runs, `google.colab` is NOT in sys.modules, so ALL packages get installed — non-Colab packages unconditionally, and Colab packages (numpy, pandas, etc.) at Colab's exact versions via the guard block. The result mirrors Colab's environment as closely as possible. If a cell fails, fix the notebook and re-run.
</test_environment>

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.


<todos>
TODO 1. Read and STRICTLY follow these skills: aii-colab, aii-long-running-tasks.
TODO 2. Read demo file and relevant preview_* files (preview only). Understand script structure: imports, setup, processing, output. Identify ALL tunable parameters (iterations, epochs, n_samples, hidden_size, batch_size, etc.) — these go in the config cell.
TODO 3. Create `mini_demo_data.json`: curated subset from at most ONE dataset (no more than 100 diverse examples). CRITICAL: do NOT read/grep full output file — may crash. Use `head -c 5000` or stream first entries with Python to pick examples.
TODO 4. Create `code_demo.ipynb` via NotebookEdit following <notebook_structure>. Set ALL config parameters to ABSOLUTE MINIMUM values — the smallest that produce any output (e.g. 1 iteration, 2 samples, smallest array sizes). Test-run using <test_environment>. Fix all errors until it passes.
TODO 5. GRADUALLY SCALE (but don't overdo it): increase config params step by step (e.g. ~2x each round). After each increase: test-run, record runtime, fix errors. STOP SCALING as soon as results look meaningful — a working small-scale demo beats a failed large-scale one. If full original params fit within <max_notebook_total_runtime> (10% margin), use them. Otherwise keep whatever works and comment out the true original values. Do NOT spend more than 2-3 scaling rounds.
TODO 6. Verify: (1) code_demo.ipynb contains GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/main/round-3/experiment-8/demo/mini_demo_data.json" exactly, (2) mini_demo_data.json exists, (3) uses GitHub URL pattern not just open('mini_demo_data.json').
</todos>

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "DemoExpectedFiles": {
      "description": "Expected output files from code demo notebook generation.",
      "properties": {
        "notebook": {
          "default": "",
          "description": "Path to the generated demo notebook. Example: 'code_demo.ipynb'",
          "title": "Notebook",
          "type": "string"
        },
        "mini_data_file": {
          "default": "",
          "description": "Path to the mini demo data JSON (curated subset). Example: 'mini_demo_data.json'",
          "title": "Mini Data File",
          "type": "string"
        }
      },
      "title": "DemoExpectedFiles",
      "type": "object"
    }
  },
  "description": "Dataset/experiment/evaluation \u2192 Jupyter notebook demo.\n\nTitle and summary come from the parent artifact (gen_art step),\nnot from the demo agent. The agent only outputs expected files.",
  "properties": {
    "out_expected_files": {
      "$ref": "#/$defs/DemoExpectedFiles",
      "description": "All output files you created. Must include the demo notebook."
    }
  },
  "required": [],
  "title": "CodeDemo",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [3] HUMAN-USER prompt · 2026-09-24 18:33:02 UTC

```
I work on converting natural-language text into first-order logic (NL→FOL, autoformalization) with
LLM pipelines. Evaluation is the bottleneck. Correct FOL for a sentence is not unique — different
predicate names, different decompositions of the same concept, and logically equivalent rewrites can
all be correct. Gold FOL annotations are rare and expensive. The metrics in use either need a gold
formula (exact match, BLEU, prover-checked equivalence to the gold) or only check that the output
parses. In my own pilot I used cheap structural metrics: whether a set of generated formulas loads
together without conflicts, whether predicate arities stay consistent, how many predicates are used
but never defined, and how similar the predicate sets are across reruns. Those measure stability and
composability, not whether a formula says what the sentence says.

Find new metrics for NL→FOL output quality. Operating situation: you are given a natural-language
sentence (or short passage) and a candidate FOL formalization produced by any system. There is no gold
formula, no ontology or controlled vocabulary, and no domain knowledge. The metric returns a score
that predicts whether the formalization is faithful to the text, and ideally which kind of error it
contains (quantifier or scope error, dropped or added condition, negation/polarity error, swapped
arguments, conflated or wrongly split concepts). Metrics may score a single formula or a set (several
samples for one sentence, or the formalizations of all sentences in one document). They must be
task-agnostic — usable for any NL→FOL setting, not tied to a domain, dataset or pipeline — and cheap
enough to run on every output (solver calls and small models are fine; a large-LLM judge per formula
only if shown to earn its cost).

Requirements:
- Keep the target fixed: the metric must predict faithfulness to the text. Detecting synthetic
  perturbations, parse validity, or run-to-run stability are not substitutes for that target.
- Validate against ground truth, never against the metric itself. Use public datasets with gold
  sentence-level FOL (e.g. FOLIO, MALLS, or others you find) to build a meta-evaluation set: real
  candidate formalizations from several different systems, plus controlled perturbations of gold
  formulas with known error types, labelled via prover-checked equivalence to gold. Handle two known
  problems: some gold annotations are wrong, and a candidate can be correct without being equivalent
  to the gold (different vocabulary or granularity). Estimate how often each happens and how it
  biases the labels. These datasets are public, so check whether LLM-based metrics benefit from having
  seen the gold.
- For each metric report: correlation with correctness at item and system level; sensitivity per error
  type; invariance under meaning-preserving rewrites (variable/predicate renaming, reordering,
  equivalent restatements); coverage — unparseable outputs are counted and reported, never silently
  dropped; and cost.
- Compare against baselines: parse/compile rate, round-trip (FOL→NL→compare) similarity,
  LLM-as-judge, sampling self-consistency, and the structural consistency metrics described above. A
  new metric matters only if it adds signal those don't.
- Report how each metric's reliability changes with sentence complexity (length, number of quantifiers,
  nesting depth, number of conditions and exceptions). Long, heavily conditioned sentences matter most
  to me.
- Negative results are welcome: if a family of metrics does not track correctness, show that clearly.

Out of scope: comparing grounded vs ungrounded generation (ontology vocabulary injected into prompts),
anything that depends on a particular ontology, and building a better NL→FOL translator. The
contribution is the measurement, not the translator.

Deliverables: reusable Python functions taking (text, fol) — or a set of such pairs — each with a
precise statement of what it measures; the meta-evaluation dataset with its labels; and the results.

I appended a pilot study of this problem with some metrics I already used but haven't verified. Just for reference.
```

### [4] TOOL CALL — Skill · 2026-09-24 18:33:08 UTC

```
aii-colab
```

### [5] TOOL RESULT — Skill · 2026-09-24 18:33:08 UTC

```
{"success": true, "commandName": "aii-colab"}
```

### [6] TOOL CALL — Skill · 2026-09-24 18:33:08 UTC

```
aii-long-running-tasks
```

### [7] TOOL RESULT — Skill · 2026-09-24 18:33:08 UTC

```
{"success": true, "commandName": "aii-long-running-tasks"}
```

### [8] TOOL CALL — Bash · 2026-09-24 18:33:08 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_8; ls -la $W; ls -la $W/src $W/results $W/tests 2>/dev/null | head -80; wc -l $W/method.py; ls -la /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_YYD-HDzfQfEj
```

### [9] TOOL RESULT — Bash · 2026-09-24 18:33:08 UTC

```
{"stdout": "total 59534\ndrwxr-xr-x 10 root   root    2034288 Sep 24 06:56 .\ndrwxr-xr-x  7 root   root    3000107 Sep 24 01:33 ..\ndrwxr-xr-x  2 root   root    1000143 Sep 24 06:06 .aii\n-rw-------  1 165536 165536       54 Sep 24 05:10 .aii_claude_session.json\n-rw-r--r--  1 165536 165536  1012124 Sep 24 03:09 .aii_cost_ledger.jsonl\n-rw-------  1 165536 165536    11467 Sep 24 06:06 .aii_worker_result.json\n-rw-r--r--  1 231072 231072  1372022 Sep 24 06:06 .repl_agent.ptylog\n-rw-r--r--  1 165536 165536     2935 Sep 24 06:01 .terminal_claude_agent_struct_out.json\n-rw-rw-rw-  1 165536 165536    18517 Sep 24 06:03 README.md\ndrwxr-xr-x  6 231072 231072  2021792 Sep 24 03:29 data\n-rw-r--r--  1 165536 165536 23289465 Sep 24 06:00 full_method_out.json\ndrwxr-xr-x  2 231072 231072  2000232 Sep 24 06:00 logs\n-rw-r--r--  1 165536 165536    12147 Sep 24 03:37 method.py\n-rw-r--r--  1 165536 165536 19033381 Sep 24 05:53 method_out.json\n-rw-r--r--  1 165536 165536    14240 Sep 24 06:00 mini_method_out.json\n-rw-r--r--  1 165536 165536    12349 Sep 24 06:00 preview_method_out.json\n-rw-rw-rw-  1 231072 231072     3408 Sep 24 06:00 pyproject.toml\n-rw-r--r--  1 165536 165536       27 Sep 24 03:32 pytest.ini\n-rw-r--r--  1 165536 165536     6962 Sep 24 06:01 reproducibility.md\n-rw-rw-rw-  1 165536 165536     2332 Sep 24 06:00 requirements.txt\n-rwxrwxrwx  1 165536 165536     1764 Sep 24 03:52 restore.sh\ndrwxr-xr-x  5 231072 231072  2007896 Sep 24 06:00 results\ndrwxr-xr-x  2 165536 165536  1000117 Sep 24 05:56 scripts\ndrwxr-xr-x  6 231072 231072  1074555 Sep 24 06:56 src\ndrwxr-xr-x  2 231072 231072  1002474 Sep 24 06:56 tests\ndrwxr-xr-x  3 231072 231072  1021572 Sep 24 01:58 vendor_e6\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results:\ntotal 75595\ndrwxr-xr-x  5 231072 231072  2007896 Sep 24 06:00 .\ndrwxr-xr-x 10 root   root    2034288 Sep 24 06:56 ..\n-rw-r--r--  1 165536 165536   130039 Sep 24 03:46 analysis_hyb.json\n-rw-r--r--  1 165536 165536    10208 Sep 24 05:52 analysis_perturb.json\n-rw-r--r--  1 165536 165536     1035 Sep 24 05:13 analysis_typing.json\n-rw-r--r--  1 165536 165536     1835 Sep 24 06:00 audit_raw.json\n-rw-r--r--  1 165536 165536      836 Sep 24 05:53 audit_rederive.json\n-rw-r--r--  1 165536 165536      179 Sep 24 03:09 budget_state.json\n-rw-r--r--  1 165536 165536      472 Sep 24 03:44 cost_ledger.jsonl\n-rw-r--r--  1 165536 165536  1396418 Sep 24 03:09 costs.jsonl\n-rw-r--r--  1 165536 165536     1487 Sep 24 05:52 coverage_perturb.csv\n-rw-r--r--  1 165536 165536     5889 Sep 24 05:53 deviations.json\ndrwxr-xr-x  2 165536 165536  1055273 Sep 24 03:49 figures\n-rw-r--r--  1 165536 165536   118774 Sep 24 05:52 invariance_table.csv\n-rw-r--r--  1 165536 165536    14779 Sep 24 03:44 invariance_table_consensus.csv\n-rw-r--r--  1 231072 231072      405 Sep 24 01:59 label_vector_check.json\n-rw-r--r--  1 165536 165536  3499292 Sep 24 03:09 llm_cache.jsonl\n-rw-r--r--  1 231072 231072  5818574 Sep 24 05:49 local_cache.jsonl\n-rw-r--r--  1 231072 231072 19505375 Sep 24 02:03 pairs_E.jsonl\n-rw-r--r--  1 231072 231072  3966740 Sep 24 02:05 pairs_screen.jsonl\n-rw-r--r--  1 165536 165536  4124775 Sep 24 03:46 per_item_hyb_E.jsonl\n-rw-r--r--  1 165536 165536   490429 Sep 24 03:44 per_item_screen_hyb.jsonl\n-rw-r--r--  1 165536 165536   187368 Sep 24 05:52 perturb_breakdowns.csv\n-rw-r--r--  1 165536 165536    33889 Sep 24 05:52 perturb_downup.csv\ndrwxr-xr-x  3 231072 231072  2001138 Sep 24 05:51 perturb_scores\n-rw-r--r--  1 165536 165536 14440487 Sep 24 05:52 perturb_scores.jsonl\n-rw-r--r--  1 165536 165536   485330 Sep 24 05:52 perturb_sensitivity.csv\n-rw-r--r--  1 165536 165536     5325 Sep 24 02:59 prereg_hyb.json\n-rw-r--r--  1 165536 165536      116 Sep 24 02:59 prereg_hyb.sha256\n-rw-r--r--  1 165536 165536     8379 Sep 24 03:18 prereg_perturb.json\n-rw-r--r--  1 165536 165536      120 Sep 24 03:18 prereg_perturb.sha256\n-rw-r--r--  1 231072 231072   118836 Sep 24 01:59 prices.json\n-rw-r--r--  1 165536 165536      623 Sep 24 05:53 quant_shift.json\n-rw-r--r--  1 231072 231072    18294 Sep 24 02:04 regression_gate.json\n-rw-r--r--  1 165536 165536     2512 Sep 24 03:17 s4_perturb_coefs.json\n-rw-r--r--  1 165536 165536     1802 Sep 24 05:53 sanity_checks.json\n-rw-r--r--  1 231072 231072 10105106 Sep 24 02:03 scores_E.jsonl\n-rw-r--r--  1 231072 231072  2953676 Sep 24 02:05 scores_screen.jsonl\n-rw-r--r--  1 165536 165536     2748 Sep 24 03:46 selection.json\n-rw-r--r--  1 231072 231072      324 Sep 24 01:59 stage_E_100.json\n-rw-r--r--  1 231072 231072      316 Sep 24 02:03 stage_E_all.json\n-rw-r--r--  1 231072 231072      318 Sep 24 01:57 stage_E_mini.json\n-rw-r--r--  1 231072 231072      215 Sep 24 02:05 stage_screen_all.json\ndrwxr-xr-x  2 231072 231072        1 Sep 24 02:00 tables\n-rw-r--r--  1 165536 165536    35195 Sep 24 05:53 tables.md\n-rw-r--r--  1 165536 165536     1181 Sep 24 05:52 thresholds_gpu.json\n-rw-r--r--  1 165536 165536     8798 Sep 24 05:52 tradeoff.csv\n-rw-r--r--  1 165536 165536     6454 Sep 24 05:13 typing.csv\n-rw-r--r--  1 165536 165536     5431 Sep 24 05:13 typing_confusion.csv\n-rw-r--r--  1 165536 165536  1697259 Sep 24 05:13 typing_per_row.jsonl\n-rw-r--r--  1 165536 165536   969656 Sep 24 03:43 typing_rows.jsonl\n-rw-r--r--  1 165536 165536   119905 Sep 24 03:55 typing_rows_s20.jsonl\n-rw-r--r--  1 165536 165536      633 Sep 24 03:55 typing_s20.json\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/src:\ntotal 7368\ndrwxr-xr-x  6 231072 231072 1074555 Sep 24 06:56 .\ndrwxr-xr-x 10 root   root   2034288 Sep 24 06:56 ..\n-rw-r--r--  1 231072 231072       0 Sep 24 01:36 __init__.py\n-rw-r--r--  1 165536 165536    8515 Sep 24 03:17 an_common.py\n-rw-r--r--  1 231072 231072   52084 Sep 24 01:36 analyse_E.py\n-rw-r--r--  1 165536 165536   22688 Sep 24 03:44 analyse_hyb.py\n-rw-r--r--  1 165536 165536   29604 Sep 24 03:44 analyse_perturb.py\n-rw-r--r--  1 165536 165536   12881 Sep 24 03:39 consensus_lib.py\n-rw-r--r--  1 231072 231072    6702 Sep 24 01:36 data_views.py\n-rw-r--r--  1 165536 165536    4412 Sep 24 03:17 fit_s4_perturb.py\n-rw-r--r--  1 165536 165536    6746 Sep 24 02:59 freeze_prereg_hyb.py\n-rw-r--r--  1 165536 165536    8593 Sep 24 03:18 freeze_prereg_perturb.py\n-rw-r--r--  1 231072 231072    1961 Sep 24 01:57 gate_check.py\n-rwxr-xr-x  1 231072 231072     913 Sep 24 01:36 key_monitor.sh\n-rw-r--r--  1 231072 231072    3806 Sep 24 01:36 local_judge_E.py\n-rw-r--r--  1 165536 165536    5734 Sep 24 03:48 make_figures.py\n-rw-r--r--  1 231072 231072   14292 Sep 24 01:49 pairs.py\n-rw-r--r--  1 231072 231072   42945 Sep 24 01:36 peer_text.py\n-rw-r--r--  1 165536 165536   10416 Sep 24 03:11 perturb_cpu.py\n-rw-rw-rw-  1 165536 165536   10062 Sep 24 03:28 perturb_gpu.py\n-rw-r--r--  1 231072 231072   10021 Sep 24 01:36 pool_scoring.py\n-rw-r--r--  1 231072 231072    5301 Sep 24 01:36 posthoc_nf_fusion.py\n203 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/method.py\ntotal 2973\ndrwxr-xr-x 3 root root 1002738 Sep 24 18:32 .\ndrwxr-xr-x 5 root root 2011494 Sep 24 18:31 ..\ndrwxr-xr-x 2 root root       1 Sep 24 18:31 .aii\n-rw------- 1 root root      54 Sep 24 18:32 .aii_claude_session.json\n-rw-r--r-- 1 root root   27989 Sep 24 18:33 .repl_agent.ptylog", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [10] TOOL CALL — Bash · 2026-09-24 18:33:12 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_8; cat $W/method.py; echo ======; head -c 4000 $W/preview_method_out.json; echo; ls $W/scripts $W/tests $W/data
```

### [11] TOOL RESULT — Bash · 2026-09-24 18:33:12 UTC

```
{"stdout": "#!/usr/bin/env python3\n\"\"\"Rename-invariant cross-family consensus (PEER_HYB) and per-error-type sensitivity of every gold-free NL->FOL metric.\n\nMETHOD (ours):  PEER_HYB consensus -- a candidate formula agrees with a peer formula of the same sentence (another model\n                family) if the iteration-1 name-similarity ALIGN map (eqmv) OR the exp-5 name-free NF-anchored map gives a\n                z3-verified equivalence; c_score_hyb = 1 - share of agreeing peers (leave-one-family-out), g_score_hyb =\n                graded claim-unit consensus under the composite map. Library: src/consensus_lib.py.\nBASELINES (same rows, same pipeline): ALIGN consensus (c_score_align, the iteration-2 survivor), NF-anchored consensus,\n                graded g, PEER+TEXT fusion, TEXT-only (L2-bow, L3), SC-5 local self-consistency, local round-trip NLI/embedding,\n                local LLM judges (Qwen3-8B, Llama-3.1-8B; disguised), flash-lite judge (disguised), S4 stack, parse rate and\n                the user's pilot structural metrics (reference rows).\n\nStages (each resumable; outputs under results/):\n  score      src/run_scoring.py screen|E        pair engine on the screen and on dataset E (+ PERTURB E-base rows)   [CPU]\n  gate       src/gate_check.py                  regression gate vs exp 5 frozen columns\n  freeze_a   src/freeze_prereg_hyb.py           PREREG_HYB (before any label join)\n  part_a     src/analyse_hyb.py                 screen thresholds, rename FA, over-alignment, SELECTION, E AUROCs, audit\n  calib      src/prep_calib.py                  E calibration rows for the nf4 local judges / flash-lite threshold\n  api        src/run_api_perturb.py             flash-lite judge on PERTURB + calibration rows (OpenRouter, ~$0.35)\n  cpu_b      src/perturb_cpu.py                 parse / pilot / L2 / L3 / PEER+TEXT / SC-5 on PERTURB\n  gpu_b      src/perturb_gpu.py                 local judges + round trip (nf4) on PERTURB + calibration rows    [GPU]\n  s4         src/fit_s4_perturb.py              S4_local full-E fit (before PERTURB labels)\n  freeze_b   src/freeze_prereg_perturb.py       PREREG_PERTURB (thresholds, statistics, predictions)\n  part_b     src/analyse_perturb.py             per operator x polarity sensitivity, DOWN/UP, invariance, trade-off\n  part_c     src/typing_perturb.py              error-type identification (peer medoid vs oracle vs judges)\n  tests      pytest tests/                      library unit tests (20 known pairs)\n  output     method.py output                   -> method_out.json (exp_gen_sol_out)\nusage: .venv/bin/python method.py run [--from STAGE]   |   .venv/bin/python method.py output\n\"\"\"\nfrom __future__ import annotations\n\nimport argparse\nimport json\nimport math\nimport subprocess\nimport sys\nfrom pathlib import Path\n\nfrom loguru import logger\n\nROOT = Path(__file__).resolve().parent\nRES = ROOT / \"results\"\nPY = str(ROOT / \".venv\" / \"bin\" / \"python\")\nsys.path.insert(0, str(ROOT / \"src\"))\n\nlogger.remove()\nlogger.add(sys.stdout, level=\"INFO\", format=\"{time:HH:mm:ss}|{level:<7}|{message}\")\nlogger.add(ROOT / \"logs\" / \"method.log\", rotation=\"30 MB\", level=\"DEBUG\")\n\nSTAGES = [\n    (\"score\", [[PY, \"src/run_scoring.py\", \"E\", \"--stage\", \"all\"], [PY, \"src/run_scoring.py\", \"screen\", \"--stage\", \"all\"]]),\n    (\"gate\", [[PY, \"src/gate_check.py\"]]),\n    (\"freeze_a\", [[PY, \"src/freeze_prereg_hyb.py\"]]),\n    (\"part_a\", [[PY, \"src/analyse_hyb.py\"]]),\n    (\"calib\", [[PY, \"src/prep_calib.py\"]]),\n    (\"api\", [[PY, \"src/run_api_perturb.py\"]]),\n    (\"cpu_b\", [[PY, \"src/perturb_cpu.py\"]]),\n    (\"gpu_b\", [[PY, \"src/perturb_gpu.py\", \"--which\", \"judges_disg,verb,nli\"]]),\n    (\"s4\", [[PY, \"src/fit_s4_perturb.py\"]]),\n    (\"freeze_b\", [[PY, \"src/freeze_prereg_perturb.py\"]]),\n    (\"part_b\", [[PY, \"src/analyse_perturb.py\"]]),\n    (\"part_c\", [[PY, \"src/typing_perturb.py\"]]),\n    (\"tests\", [[PY, \"-m\", \"pytest\", \"-q\", \"-c\", \"pytest.ini\", \"tests\"]]),\n]\nDONE_MARK = {\"freeze_a\": RES / \"prereg_hyb.sha256\", \"freeze_b\": RES / \"prereg_perturb.sha256\", \"calib\": ROOT / \"data\" / \"E_calib_units.jsonl\",\n             \"s4\": RES / \"s4_perturb_coefs.json\"}\n\n\ndef run(start: str | None):\n    go = start is None\n    for name, cmds in STAGES:\n        go = go or name == start\n        if not go:\n            continue\n        if name in DONE_MARK and DONE_MARK[name].exists():\n            logger.info(f\"{name}: already done ({DONE_MARK[name].name}); frozen files are never overwritten\")\n            continue\n        for c in cmds:\n            logger.info(f\"{name}: {' '.join(c[1:])}\")\n            subprocess.run(c, cwd=ROOT, check=True)\n\n\n# ================================================================================================ method_out.json\ndef s(x) -> str:\n    if x is None or (isinstance(x, float) and math.isnan(x)):\n        return \"NA\"\n    if isinstance(x, bool):\n        return str(x)\n    if isinstance(x, float):\n        return f\"{x:.6f}\"\n    return str(x)\n\n\ndef build_output():\n    import an_common as C\n    sel = json.loads((RES / \"selection.json\").read_text())\n    frozen = sel.get(\"frozen_score\")\n    frozen_label = sel.get(\"frozen_variant\") or \"NONE_ELIGIBLE\"\n    blind = {r[\"row_key\"]: r for r in C.jl(C.DATA / \"exp5\" / \"E_blind.jsonl\")}\n    ds = []\n    # ---- dataset E (development for the selection; real generator outputs)\n    ex = []\n    for r in C.jl(RES / \"per_item_hyb_E.jsonl\"):\n        b = blind[r[\"row_key\"]]\n        e = {\"input\": json.dumps({\"text\": b[\"text\"], \"candidate_fol\": b[\"candidate_fol\"], \"system\": b[\"system\"],\n                                  \"prompt_variant\": b[\"prompt_variant\"]}, ensure_ascii=False),\n             \"output\": r[\"final_label\"], \"metadata_fold\": \"E\", \"metadata_row_key\": r[\"row_key\"], \"metadata_sentence_id\": r[\"sentence_id\"],\n             \"metadata_stratum\": r[\"stratum\"], \"metadata_label_tier\": r[\"label_tier\"], \"metadata_y_R_AB\": r[\"y_AB\"],\n             \"metadata_system_class\": r[\"system_class\"], \"metadata_coverage_status\": r[\"coverage_status\"], \"metadata_n_peers\": r[\"n_peers\"],\n             \"predict_c_score_hyb\": s(r[\"c_hyb\"]), \"predict_g_score_hyb\": s(r[\"g_hyb\"]), \"predict_c_score_nf\": s(r[\"c_nf\"]),\n             \"predict_c_score_align\": s(r[\"c_align\"]), \"predict_g_score_align\": s(r[\"g_align\"]), \"predict_g_score_nf\": s(r[\"g_nf\"]),\n             \"predict_frozen_invariant\": s(r.get(frozen)) if frozen else frozen_label}\n        ex.append(e)\n    ds.append({\"dataset\": \"E_heldout_candidates\", \"examples\": ex})\n    # ---- PERTURB (mutants, controls, bases): every Part B metric\n    pb = C.jl(RES / \"perturb_scores.jsonl\")\n    A = json.loads((RES / \"analysis_perturb.json\").read_text())\n    mets = A[\"metrics\"]\n    ex = []\n    rows = {r[\"item_id\"]: r for r in C.jl(C.DATA / \"perturb_rows.jsonl\")}\n    for u in pb:\n        is_base = u[\"key\"].startswith(\"PB:\")\n        src = rows.get(u[\"item_id\"]) if not is_base else None\n        text = src[\"text\"] if src else next(r[\"text\"] for r in rows.values() if r[\"base_item_id\"] == u[\"base\"])\n        e = {\"input\": json.dumps({\"text\": text, \"candidate_fol\": u[\"fol\"]}, ensure_ascii=False),\n             \"output\": \"ERROR\" if u[\"y\"] == 1 else \"CORRECT\",\n             \"metadata_fold\": \"PERTURB_BASE\" if is_base else (\"PERTURB\" if u[\"y\"] == 1 else \"PERTURB_CONTROL\"),\n             \"metadata_key\": u[\"key\"], \"metadata_base_item_id\": u[\"base\"], \"metadata_operator\": u[\"operator\"],\n             \"metadata_op_fine\": u[\"op_fine\"], \"metadata_control_type\": u[\"control_type\"], \"metadata_polarity\": u[\"polarity\"],\n             \"metadata_matched_pair_id\": u[\"matched_pair_id\"], \"metadata_subtype\": u[\"subtype\"], \"metadata_base_status\": u[\"base_status\"],\n             \"metadata_base_endorsed\": u.get(\"base_endorsed\"),\n             \"predict_frozen_invariant\": s(u.get(frozen)) if frozen else frozen_label}\n        for m in mets:\n            e[f\"predict_{m}\"] = s(u.get(m)) if u.get(m + \"__status\") != \"fail\" else (\"FAIL(\" + s(u.get(m)) + \")\")\n        e[\"predict_c_score_hyb\"] = e.pop(\"predict_c_hyb\", \"NA\")\n        e[\"predict_g_score_hyb\"] = e.pop(\"predict_g_hyb\", \"NA\")\n        e[\"predict_c_score_nf\"] = e.pop(\"predict_c_nf\", \"NA\")\n        e[\"predict_c_score_align\"] = e.pop(\"predict_c_align\", \"NA\")\n        ex.append(e)\n    ds.append({\"dataset\": \"PERTURB_suite\", \"examples\": ex})\n    # ---- screen items, exp D rewrites, probes (consensus variants)\n    ex_rw, ex_sc = [], []\n    labs = json.loads((C.DATA / \"screen\" / \"screen_adjudicated_labels.json\").read_text())\n    inv = {x[\"rw_id\"]: x for x in json.loads((C.DATA / \"invariance_items.json\").read_text())}\n    items = {x[\"item_id\"]: x for x in json.loads((C.DATA / \"screen\" / \"screen_items.json\").read_text())}\n    probes = {f\"PR:{p['probe']}:{p['base_item_id']}\": p for p in json.loads((C.DATA / \"exp5\" / \"screen_probes.json\").read_text())}\n    for r in C.jl(RES / \"per_item_screen_hyb.jsonl\"):\n        k = r[\"key\"]\n        if k.startswith(\"M:\"):\n            continue\n        if k.startswith(\"RW:\"):\n            x = inv[k[3:]]\n            text, fol, fold = x[\"text\"], x[\"candidate_fol\"], \"REWRITE_EXPD\"\n            out = labs.get(x[\"base_item_id\"], {}).get(\"final_label\") or \"UNLABELLED\"  # a meaning-preserving rewrite inherits its base label\n            base = x[\"base_item_id\"]\n            extra = {\"metadata_rewrite_family\": x[\"family\"], \"metadata_base_item_id\": base,\n                     \"metadata_base_label\": labs.get(base, {}).get(\"final_label\")}\n        elif k.startswith(\"PR:\"):\n            p = probes[k]\n            b = items[p[\"base_item_id\"]]\n            text, fol, fold, out = b[\"text\"], p[\"fol\"], \"SCREEN_PROBE\", \"ERROR\"\n            extra = {\"metadata_probe\": p[\"probe\"], \"metadata_base_item_id\": p[\"base_item_id\"]}\n        else:\n            b = items.get(k)\n            if b is None:\n                continue\n            text, fol, fold, out = b[\"text\"], b[\"candidate_fol\"], \"SCREEN\", r[\"label\"] or \"UNLABELLED\"\n            extra = {\"metadata_track\": b[\"track\"], \"metadata_system\": b[\"system\"]}\n        e = {\"input\": json.dumps({\"text\": text, \"candidate_fol\": fol}, ensure_ascii=False), \"output\": out, \"metadata_fold\": fold,\n             \"metadata_key\": k, \"metadata_sentence_id\": r[\"sentence_id\"], **{kk: v for kk, v in extra.items() if v is not None},\n             \"predict_c_score_hyb\": s(r[\"c_hyb\"]), \"predict_g_score_hyb\": s(r[\"g_hyb\"]), \"predict_c_score_nf\": s(r[\"c_nf\"]),\n             \"predict_c_score_align\": s(r[\"c_align\"]), \"predict_frozen_invariant\": frozen_label if not frozen else s(r.get(frozen))}\n        (ex_rw if fold == \"REWRITE_EXPD\" else ex_sc).append(e)\n    ds.append({\"dataset\": \"expD_rewrites_screen\", \"examples\": ex_rw})\n    ds.append({\"dataset\": \"screen_items_and_probes\", \"examples\": ex_sc})\n    out = {\"metadata\": {\"method_name\": \"PEER_HYB rename-invariant cross-family consensus + PERTURB per-error-type sensitivity\",\n                        \"description\": \"Oriented scores (higher = more likely ERROR). E: real generator outputs with panel/solver labels \"\n                                       \"(development for the HYB/NF selection). PERTURB: synthetic typed mutants/controls (never pooled \"\n                                       \"with E). See README.md and results/.\",\n                        \"selection\": {k: sel[k] for k in (\"frozen_variant\", \"note\", \"E_strat_auroc_R_AB\")},\n                        \"prereg_hyb_sha256\": C.sha256_file(RES / \"prereg_hyb.json\"),\n                        \"prereg_perturb_sha256\": C.sha256_file(RES / \"prereg_perturb.json\"),\n                        \"predict_frozen_invariant\": \"NONE_ELIGIBLE = no rename-invariant variant passed the pre-registered rule; the R_COMP read uses ALIGN (predict_c_score_align)\" if not frozen else frozen},\n           \"datasets\": ds}\n    (ROOT / \"method_out.json\").write_text(json.dumps(out, ensure_ascii=False))\n    logger.info(f\"method_out.json: {[(d['dataset'], len(d['examples'])) for d in ds]}\")\n\n\n@logger.catch(reraise=True)\ndef main():\n    ap = argparse.ArgumentParser()\n    ap.add_argument(\"cmd\", choices=[\"run\", \"output\"])\n    ap.add_argument(\"--from\", dest=\"start\", default=None)\n    a = ap.parse_args()\n    if a.cmd == \"run\":\n        run(a.start)\n        build_output()\n    else:\n        build_output()\n\n\nif __name__ == \"__main__\":\n    main()\n======\n{\n  \"metadata\": {\n    \"method_name\": \"PEER_HYB rename-invariant cross-family consensus + PERTURB per-error-type sensitivity\",\n    \"description\": \"Oriented scores (higher = more likely ERROR). E: real generator outputs with panel/solver labels (development for the HYB/NF selection). PERTURB: synthetic typed mutants/controls (never pooled with E)...\",\n    \"selection\": {\n      \"frozen_variant\": null,\n      \"note\": \"NEITHER ELIGIBLE: no rename-invariant consensus exists here; both reported as failed; the R_COMP read uses ALIGN.\",\n      \"E_strat_auroc_R_AB\": {\n        \"HYB\": 0.7375072927473793,\n        \"NF-anchored\": 0.6859960770958894,\n        \"ALIGN\": 0.7414618757606236\n      }\n    },\n    \"prereg_hyb_sha256\": \"47d10ac6fa280defe95e2067c20c1367e8963c0dc5f7effbce12ba953a3363ae\",\n    \"prereg_perturb_sha256\": \"773d73a61bf5c07d40612b6b3afeb8be6d8cf2adfe3f44770e672a55e62d45bc\",\n    \"predict_frozen_invariant\": \"NONE_ELIGIBLE = no rename-invariant variant passed the pre-registered rule; the R_COMP read uses ALIGN (predict_c_score_align)\"\n  },\n  \"datasets\": [\n    {\n      \"dataset\": \"E_heldout_candidates\",\n      \"examples\": [\n        {\n          \"input\": \"{\\\"text\\\": \\\"When something is depressing, it is sad.\\\", \\\"candidate_fol\\\": \\\"\\\", \\\"system\\\": \\\"ccg2lambda\\\", \\\"prompt_variant\\\": \\\"none\\\"}\",\n          \"output\": \"UNPARSEABLE\",\n          \"metadata_fold\": \"E\",\n          \"metadata_row_key\": \"31452c4db10ee367|none\",\n          \"metadata_sentence_id\": \"0000c2274e80\",\n          \"metadata_stratum\": \"CTRL\",\n          \"metadata_label_tier\": \"-\",\n          \"metadata_y_R_AB\": null,\n          \"metadata_system_class\": \"symbolic_eventsem\",\n          \"metadata_coverage_status\": \"UNPARSEABLE\",\n          \"metadata_n_peers\": null,\n          \"predict_c_score_hyb\": \"1.000000\",\n          \"predict_g_score_hyb\": \"1.000000\",\n          \"predict_c_score_nf\": \"1.000000\",\n          \"predict_c_score_align\": \"1.000000\",\n          \"predict_g_score_align\": \"1.000000\",\n          \"predict_g_score_nf\": \"1.000000\",\n          \"predict_frozen_invariant\": \"NONE_ELIGIBLE\"\n        },\n        {\n          \"input\": \"{\\\"text\\\": \\\"When something is depressing, it is sad.\\\", \\\"candidate_fol\\\": \\\"∀x (Depressing(x) → Sad(x))\\\", \\\"system\\\": \\\"F:openai/gpt-5.1\\\", \\\"prompt_variant\\\": \\\"fewshot_v1\\\"}\",\n          \"output\": \"CORRECT\",\n          \"metadata_fold\": \"E\",\n          \"metadata_row_key\": \"b87a8dda4faced11|fewshot_v1\",\n          \"metadata_sentence_id\": \"0000c2274e80\",\n          \"metadata_stratum\": \"CTRL\",\n          \"metadata_label_tier\": \"A\",\n          \"metadata_y_R_AB\": 0,\n          \"metadata_system_class\": \"llm\",\n          \"metadata_coverage_status\": \"OK\",\n          \"metadata_n_peers\": 11,\n          \"predict_c_score_hyb\": \"0.090909\",\n          \"predict_g_score_hyb\": \"0.047619\",\n          \"predict_c_score_nf\": \"0.090909\",\n          \"predict_c_score_align\": \"0.090909\",\n          \"predict_g_score_align\": \"0.047619\",\n          \"predict_g_score_nf\": \"0.047619\",\n          \"predict_frozen_invariant\": \"NONE_ELIGIBLE\"\n        },\n        {\n          \"input\": \"{\\\"text\\\": \\\"When something is depressing, it is sad.\\\", \\\"candidate_fol\\\": \\\"∀x (Depressing(x) → Sad(x))\\\", \\\"system\\\": \\\"G1b:meta-llama/llama-3.3-70b-instruct\\\", \\\"prompt_variant\\\": \\\"fewshot_v1\\\"}\",\n          \"output\": \"CORRECT\",\n          \"metadata_fold\": \"E\",\n          \"metadata_row_key\": \"3222a9e5bc15a5c9|fewshot_v1\",\n          \"metadata_sentence_id\": \"0000c2274e80\",\n          \"metadata_stratum\": \"CTRL\",\n          \"metadata_label_tier\": \"A\",\n          \"metadata_y_R_AB\": 0,\n          \"metadata_system_class\": \"llm\",\n          \"metadata_coverage_status\": \"OK\",\n          \"metadata_n_peers\": 10,\n          \"predict_c_score_hyb\": \"0.000000\",\n          \"predict_g_score_hyb\": \"0.000000\",\n          \"predict_c_score_nf\": \"0.000000\",\n          \"predict_c_score_align\": \"0.000000\",\n          \"predict_g_score_align\": \"0.000000\",\n          \"predict_g_score_nf\": \"0.000000\",\n          \"predict_frozen_invariant\": \"NONE_ELIGIBLE\"\n        }\n     \n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data:\nE_calib_units.jsonl\nexp5\ninvariance_items.json\nnltk_data\nperturb_rows.jsonl\nprompts\nscreen\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/scripts:\ndownload_models.sh\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/tests:\naudit_raw.py\naudit_rederive.py\ntest_consensus_lib.py\ntest_isolation.py\ntest_threshold.py", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [12] TOOL CALL — Bash · 2026-09-24 18:33:18 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_8; cat $W/src/consensus_lib.py; echo =====; cat $W/src/an_common.py | head -120; cat $W/tests/test_consensus_lib.py | head -80; cat $W/pyproject.toml
```

### [13] TOOL RESULT — Bash · 2026-09-24 18:33:18 UTC

```
{"stdout": "\"\"\"consensus_lib: gold-free cross-family consensus metrics for NL->FOL candidates (iteration 3, Part D).\n\nWHAT THESE METRICS MEASURE. Agreement of a candidate formula with INDEPENDENT translations (\"peers\") of the SAME sentence\nproduced by other model families. They do NOT measure truth against a reference; a candidate that every peer also gets\nwrong in the same way (a coincident error) scores as faithful. Orientation everywhere: HIGHER = MORE LIKELY ERROR... [truncated, 29085 chars total]
```

### [14] TOOL CALL — Bash · 2026-09-24 18:33:32 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_8; cd $W; ls -la data/exp5 data/screen data/*.json* | head -40; cat results/selection.json | head -c 3000; echo; for f in results/per_item_hyb_E.jsonl data/exp5/E_blind.jsonl results/perturb_scores.jsonl data/perturb_rows.jsonl results/per_item_screen_hyb.jsonl; do echo "== $f $(wc -l < $f)"; head -1 $f | head -c 2500; echo; done
```

### [15] TOOL RESULT — Bash · 2026-09-24 18:33:32 UTC

```
{"stdout": "-rw-r--r-- 1 165536 165536  856134 Sep 24 03:02 data/E_calib_units.jsonl\n-rw-r--r-- 1 231072 231072  227205 Sep 24 01:38 data/invariance_items.json\n-rw-r--r-- 1 231072 231072 9578090 Sep 24 01:59 data/perturb_rows.jsonl\n\ndata/exp5:\ntotal 68713\ndrwxr-xr-x 2 231072 231072  2006325 Sep 24 01:38 .\ndrwxr-xr-x 6 231072 231072  2021792 Sep 24 03:29 ..\n-rw-r--r-- 1 231072 231072  6718145 Sep 24 01:36 E_blind.jsonl\n-rw-r--r-- 1 231072 231072       65 Sep 24 01:36 E_blind.sha256\n-rw-r--r-- 1 231072 231072  3569130 Sep 24 01:36 E_disguise_map.jsonl\n-rw-r--r-- 1 231072 231072     5807 Sep 24 01:36 E_judge.jsonl\n-rw-r--r-- 1 231072 231072  1937377 Sep 24 01:36 E_judge_local.jsonl\n-rw-r--r-- 1 231072 231072   853190 Sep 24 01:36 E_l3_q.jsonl\n-rw-r--r-- 1 231072 231072 10458429 Sep 24 01:36 E_labels.jsonl\n-rw-r--r-- 1 231072 231072   184275 Sep 24 01:36 analysis.json\n-rw-r--r-- 1 231072 231072   261314 Sep 24 01:36 api_priority.json\n-rw-r--r-- 1 231072 231072    19062 Sep 24 01:36 expA_prereg.json\n-rw-r--r-- 1 231072 231072    13709 Sep 24 01:36 expD_prereg.json\n-rw-r--r-- 1 231072 231072    12578 Sep 24 01:36 folds.json\n-rw-r--r-- 1 231072 231072   227205 Sep 24 01:36 invariance_items.json\n-rw-r--r-- 1 231072 231072  4960000 Sep 24 01:36 llm_cache.jsonl\n-rw-r--r-- 1 231072 231072  4763037 Sep 24 01:36 local_cache.jsonl\n-rw-r--r-- 1 231072 231072 22016065 Sep 24 01:36 per_item_E.jsonl\n-rw-r--r-- 1 231072 231072     2396 Sep 24 01:36 posthoc_nf_fusion.json\n-rw-r--r-- 1 231072 231072    17167 Sep 24 01:36 prereg.json\n-rw-r--r-- 1 231072 231072      112 Sep 24 01:36 prereg.sha256\n-rw-r--r-- 1 231072 231072   655065 Sep 24 01:36 rewrite_scores_pt.jsonl\n-rw-r--r-- 1 231072 231072    68101 Sep 24 01:36 screen_probes.json\n-rw-r--r-- 1 231072 231072  9586133 Sep 24 01:36 screen_scores.jsonl\n\ndata/screen:\ntotal 19436\ndrwxr-xr-x 2 231072 231072 2001514 Sep 24 01:36 .\ndrwxr-xr-x 6 231072 231072 2021792 Sep 24 03:29 ..\n-rw-r--r-- 1 231072 231072 2442818 Sep 24 01:36 expA_per_item.jsonl\n-rw-r--r-- 1 231072 231072  632634 Sep 24 01:36 expD_disguise_map.json\n-rw-r--r-- 1 231072 231072 3247282 Sep 24 01:36 expD_per_item_scores.jsonl\n-rw-r--r-- 1 231072 231072  692824 Sep 24 01:36 expD_rewrite_scores.jsonl\n-rw-r--r-- 1 231072 231072 1680482 Sep 24 01:36 expD_screen_items.json\n{\n \"prereg_sha256\": \"47d10ac6fa280defe95e2067c20c1367e8963c0dc5f7effbce12ba953a3363ae\",\n \"rule\": \"Among {HYB, NF-anchored}, a variant is eligible iff RENAME FA <= 0.10 on (i), (ii) and (iii). Among eligible variants, FREEZE the one with the higher E stratified AUROC under R_AB. Tie (|diff| < 0.005) -> NF-anchored (single-map variant with fewer agreements, less over-alignment risk). If neither is eligible: no rename-invariant consensus exists here; report both as failed and state that the R_COMP read uses ALIGN. R_COMP never takes part.\",\n \"evidence\": {\n  \"HYB\": {\n   \"score\": \"c_hyb\",\n   \"rename_FA\": {\n    \"i_expD_RENAME\": 0.050437062937062946,\n    \"ii_PERTURB_RENAME_SYN\": 0.8409090909090909,\n    \"iii_PERTURB_RENAME_NONCE\": 0.7\n   },\n   \"rename_FA_endorsed_bases_secondary\": {\n    \"ii_endorsed\": 0.7666666666666667,\n    \"iii_endorsed\": 0.6413043478260869\n   },\n   \"eligible\": false,\n   \"failing_sources\": [\n    \"ii_PERTURB_RENAME_SYN\",\n    \"iii_PERTURB_RENAME_NONCE\"\n   ]\n  },\n  \"NF-anchored\": {\n   \"score\": \"c_nf\",\n   \"rename_FA\": {\n    \"i_expD_RENAME\": 0.03028846153846154,\n    \"ii_PERTURB_RENAME_SYN\": 0.6861742424242424,\n    \"iii_PERTURB_RENAME_NONCE\": 0.4853030303030303\n   },\n   \"rename_FA_endorsed_bases_secondary\": {\n    \"ii_endorsed\": 0.5397222222222222,\n    \"iii_endorsed\": 0.38460144927536233\n   },\n   \"eligible\": false,\n   \"failing_sources\": [\n    \"ii_PERTURB_RENAME_SYN\",\n    \"iii_PERTURB_RENAME_NONCE\"\n   ]\n  }\n },\n \"E_strat_auroc_R_AB\": {\n  \"HYB\": 0.7375072927473793,\n  \"NF-anchored\": 0.6859960770958894,\n  \"ALIGN\": 0.7414618757606236\n },\n \"frozen_variant\": null,\n \"frozen_score\": null,\n \"note\": \"NEITHER ELIGIBLE: no rename-invariant consensus exists here; both reported as failed; the R_COMP read uses ALIGN.\",\n \"screen_thresholds\": {\n  \"c_align\": {\n   \"t\": 0.8,\n   \"lambda\": 0.5375,\n   \"tie_share_at_t\": 0.06504065040650407,\n   \"degenerate\": false\n  },\n  \"c_nf\": {\n   \"t\": 0.8,\n   \"lambda\": 0.38333333333333336,\n   \"tie_share_at_t\": 0.04878048780487805,\n   \"degenerate\": false\n  },\n  \"c_hyb\": {\n   \"t\": 0.6,\n   \"lambda\": 0.027272727272727303,\n   \"tie_share_at_t\": 0.08943089430894309,\n   \"degenerate\": false\n  },\n  \"g_align\": {\n   \"t\": 1.0,\n   \"lambda\": 0.6473684210526316,\n   \"tie_share_at_t\": 0.15447154471544716,\n   \"degenerate\": false\n  },\n  \"g_nf\": {\n   \"t\": 1.0,\n   \"lambda\": 0.7235294117647059,\n   \"tie_share_at_t\": 0.13821138211382114,\n   \"degenerate\": false\n  },\n  \"g_hyb\": {\n   \"t\": 1.0,\n   \"lambda\": 0.7235294117647059,\n   \"tie_share_at_t\": 0.13821138211382114,\n   \"degenerate\": false\n  }\n },\n \"R_COMP_read_uses\": \"ALIGN (c_align)\",\n \"caveat\": \"E is DEVELOPMENT data for this choice (2 candidates): the E AUROC of the frozen variant is optimistically selected; the held-out read is the sibling's R_COMP run.\"\n}\n== results/per_item_hyb_E.jsonl 8507\n{\"row_key\": \"31452c4db10ee367|none\", \"sentence_id\": \"0000c2274e80\", \"stratum\": \"CTRL\", \"system\": \"ccg2lambda\", \"system_class\": \"symbolic_eventsem\", \"fold_E\": 1, \"coverage_status\": \"UNPARSEABLE\", \"n_peers\": null, \"n_unknown_hyb\": null, \"c_hyb\": 1.0, \"g_hyb\": 1.0, \"c_align\": 1.0, \"c_nf\": 1.0, \"g_align\": 1.0, \"g_nf\": 1.0, \"c_align_re\": 1.0, \"c_nf_re\": 1.0, \"c_nf_pairs\": 1.0, \"final_label\": \"UNPARSEABLE\", \"label_tier\": \"-\", \"y_AB\": null, \"y_A\": null}\n\n== data/exp5/E_blind.jsonl 8507\n{\"item_id\": \"31452c4db10ee367\", \"sentence_id\": \"0000c2274e80\", \"system\": \"ccg2lambda\", \"slot\": \"CCG\", \"family\": \"symbolic\", \"system_class\": \"symbolic_eventsem\", \"generator_model_id\": \"ccg2lambda\", \"prompt_variant\": \"none\", \"row_key\": \"31452c4db10ee367|none\", \"text\": \"When something is depressing, it is sad.\", \"candidate_fol\": \"\", \"strata\": {\"words\": 7, \"n_quant\": 1, \"depth\": 1, \"n_conditions\": 1, \"text_conditions\": 1, \"exception_type\": null, \"source_stratum\": \"CTRL\", \"ctrl_len_bin\": \"0-11\", \"l25_topup_batch\": false}}\n\n== results/perturb_scores.jsonl 5402\n{\"key\": \"PT:a734abce6b9f8177\", \"item_id\": \"a734abce6b9f8177\", \"base\": \"68a12f5080ef6661\", \"sentence_id\": \"0000c2274e80\", \"y\": 1, \"operator\": \"ADD\", \"op_fine\": \"ADD\", \"control_type\": null, \"polarity\": \"DOWN\", \"matched_pair_id\": \"59ae53c70664\", \"pair_complete\": true, \"subtype\": \"ADD_FOREIGN\", \"base_status\": \"TRUSTED_AGREED\", \"is_rcomp\": false, \"strata\": {\"words\": 7, \"n_quant\": 1, \"depth\": 1, \"n_conditions\": 1, \"text_conditions\": 1, \"exception_type\": null, \"source_stratum\": \"CTRL\", \"ctrl_len_bin\": \"0-11\", \"l25_topup_batch\": false}, \"fol\": \"∀x (Depressing(x) ∧ SupermassiveBlackHoleAtCenter(x) → Sad(x))\", \"reference_fol\": \"∀x (Depressing(x) → Sad(x))\", \"unparseable\": false, \"c_align\": 1.0, \"c_align__status\": \"ok\", \"c_nf\": 1.0, \"c_nf__status\": \"ok\", \"c_hyb\": 1.0, \"c_hyb__status\": \"ok\", \"g_align\": 1.0, \"g_align__status\": \"ok\", \"g_nf\": 1.0, \"g_nf__status\": \"ok\", \"g_hyb\": 1.0, \"g_hyb__status\": \"ok\", \"parse_fail\": 0.0, \"parse_fail__status\": \"ok\", \"pilot_joint_conflict\": 0.0, \"pilot_joint_conflict__status\": \"ok\", \"pilot_arity_incons\": 0.0, \"pilot_arity_incons__status\": \"ok\", \"pilot_shape_incons\": 0.0, \"pilot_shape_incons__status\": \"ok\", \"pilot_dangling\": 0.6666666666666666, \"pilot_dangling__status\": \"ok\", \"l2_bow\": 1.0, \"l2_bow__status\": \"ok\", \"p_peer_text\": 0.9999394769763303, \"p_peer_text__status\": \"ok\", \"p_text\": 0.9992814485820477, \"p_text__status\": \"ok\", \"l3_z3\": 0.6666666666666666, \"l3_z3__status\": \"ok\", \"sc5_local_eq_frac\": 1.0, \"sc5_local_eq_frac__status\": \"ok\", \"sc5_local_entropy\": 0.45056120886630463, \"sc5_local_entropy__status\": \"ok\", \"judge_local_qwen8b_disg\": 0.15000000000000002, \"judge_local_qwen8b_disg__status\": \"ok\", \"judge_local_llama8b_disg\": 0.8805195758067078, \"judge_local_llama8b_disg__status\": \"ok\", \"rt_nli_min_local\": 0.999456554884091, \"rt_nli_min_local__status\": \"ok\", \"rt_nli_fwd_local\": 0.999456554884091, \"rt_nli_fwd_local__status\": \"ok\", \"rt_nli_bwd_local\": 0.5747319757938385, \"rt_nli_bwd_local__status\": \"ok\", \"rt_nli_contra_local\": 0.03400562331080437, \"rt_nli_contra_local__status\": \"ok\", \"rt_nli_min_alt_local\": 0.9999805094248586, \"rt_nli_min_alt_local__status\": \"ok\", \"rt_embed_cos_local\": 0.2951723337173462, \"rt_embed_cos_local__status\": \"ok\", \"judge_cheap_disg\": 1.0, \"judge_cheap_disg__status\": \"ok\", \"judge_cheap_type\": \"ADD\", \"judge_local_qwen8b_type\": \"NONE\", \"S4_local\": 0.819107439429283, \"S4_local__status\": \"ok\", \"base_endorsed\": true, \"base_endorsed_align\": true}\n\n== data/perturb_rows.jsonl 5102\n{\"item_id\": \"a734abce6b9f8177\", \"sentence_id\": \"0000c2274e80\", \"base_item_id\": \"68a12f5080ef6661\", \"fold\": \"PERTURB\", \"system\": \"PERTURB:ADD:DOWN\", \"label\": \"ERROR\", \"operator\": \"ADD\", \"control_type\": null, \"op_fine\": \"ADD\", \"polarity\": \"DOWN\", \"matched_pair_id\": \"59ae53c70664\", \"matched_pair_complete\": true, \"subtype\": \"ADD_FOREIGN\", \"base_source\": \"E_TRUSTED_AGREED\", \"base_trust\": \"trusted\", \"strata\": {\"words\": 7, \"n_quant\": 1, \"depth\": 1, \"n_conditions\": 1, \"text_conditions\": 1, \"exception_type\": null, \"source_stratum\": \"CTRL\", \"ctrl_len_bin\": \"0-11\", \"l25_topup_batch\": false}, \"text\": \"When something is depressing, it is sad.\", \"candidate_fol\": \"∀x (Depressing(x) ∧ SupermassiveBlackHoleAtCenter(x) → Sad(x))\", \"reference_fol\": \"∀x (Depressing(x) → Sad(x))\", \"reference_fol_weak\": \"∀x (Depressing(x) → Sad(x))\", \"reference_fol_strong\": null, \"disguised_text\": \"When babobing is gunining, it is milup.\", \"disguised_fol\": \"∀x (((Gunining(x) ∧ LeponiveMezelNupebAtGataf(x)) → Milup(x)))\", \"disguised_reference_fol\": \"∀x ((Gunining(x) → Milup(x)))\", \"edited_predicate\": null, \"error_ops\": [\"ADD\"]}\n\n== results/per_item_screen_hyb.jsonl 1870\n{\"key\": \"d873519fe5b6a02d\", \"sentence_id\": \"67b9b243c5ed\", \"coverage_status\": \"OK\", \"c_align\": 0.2222222222222222, \"c_nf\": 0.2222222222222222, \"c_hyb\": 0.2222222222222222, \"g_align\": 0.12499999999999989, \"g_nf\": 0.12499999999999989, \"g_hyb\": 0.12499999999999989, \"c_nf_pairs\": 0.2222222222222222, \"n_peers\": 9, \"n_unknown_hyb\": 0, \"label\": null}", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_YYD-HDzfQfEj", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [16] TOOL CALL — Bash · 2026-09-24 18:33:38 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_8; cd $W; python3 -c "
import json
d=json.load(open('method_out.json'))
for x in d['datasets']: print(x['dataset'],len(x['examples']))
A=json.load(open('results/analysis_perturb.json')); print(list(A.keys())); print(A['metrics'])
"; ls -la data/screen/; find / -name screen_adjudicated_labels.json 2>/dev/null | head -3; python3 -c "
import json
x=json.load(open('$W/data/invariance_items.json')); print(type(x),len(x)); print(json.dumps(x[0])[:800])
p=json.load(open('$W/data/exp5/screen_probes.json')); print(len(p)); print(json.dumps(p[0])[:600])
"; cut -c1-200 results/per_item_screen_hyb.jsonl | awk -F'"' '{print substr(\$4,1,3)}' | sort | uniq -c | head
```

### [17] TOOL RESULT — Bash · 2026-09-24 18:35:38 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false, "backgroundTaskId": "b1n9nuxr9", "timedOutAfterMs": 120000, "backgroundCwdHint": "Session cwd remains /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_YYD-HDzfQfEj; directory changes made by the backgrounded command do not apply to subsequent commands."}
```

### [18] ASSISTANT · 2026-09-24 18:35:42 UTC

```
Inspecting the source result files to pick a demo subset; the filesystem `find /` is slow, so I'll wait on it briefly.
```

### [19] TOOL CALL — Bash · 2026-09-24 18:35:42 UTC

```
sleep 20; cat /tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-YYD-HDzfQfEj/921fc65d-5ce4-4ae5-9da8-7c8e9ce14d4b/tasks/b1n9nuxr9.output
```

### [20] TOOL RESULT — Bash · 2026-09-24 18:36:02 UTC

```
{"stdout": "E_heldout_candidates 8507\nPERTURB_suite 5402\nexpD_rewrites_screen 261\nscreen_items_and_probes 1600\n['prereg_perturb_sha256', 'available', 'metrics', 'thresholds_used', 'tie_share_at_t_E', 'base_endorsement', 'thresholds_secondary', 'n_complete_pairs', 'common_subset', 'n_rows']\n['c_align', 'c_nf', 'c_hyb', 'g_align', 'g_nf', 'g_hyb', 'parse_fail', 'pilot_joint_conflict', 'pilot_arity_incons', 'pilot_shape_incons', 'pilot_dangling', 'l2_bow', 'l3_z3', 'p_peer_text', 'p_text', 'sc5_local_eq_frac', 'sc5_local_entropy', 'judge_local_qwen8b_disg', 'judge_local_llama8b_disg', 'rt_nli_min_local', 'rt_nli_fwd_local', 'rt_nli_bwd_local', 'rt_nli_contra_local', 'rt_nli_min_alt_local', 'rt_embed_cos_local', 'judge_cheap_disg', 'S4_local']\ntotal 19436\ndrwxr-xr-x 2 231072 231072 2001514 Sep 24 01:36 .\ndrwxr-xr-x 6 231072 231072 2021792 Sep 24 03:29 ..\n-rw-r--r-- 1 231072 231072 2442818 Sep 24 01:36 expA_per_item.jsonl\n-rw-r--r-- 1 231072 231072  632634 Sep 24 01:36 expD_disguise_map.json\n-rw-r--r-- 1 231072 231072 3247282 Sep 24 01:36 expD_per_item_scores.jsonl\n-rw-r--r-- 1 231072 231072  692824 Sep 24 01:36 expD_rewrite_scores.jsonl\n-rw-r--r-- 1 231072 231072 1680482 Sep 24 01:36 expD_screen_items.json\n-rw-r--r-- 1 231072 231072 4556597 Sep 24 01:36 peer_outputs.jsonl\n-rw-r--r-- 1 231072 231072  950464 Sep 24 01:36 screen_adjudicated_labels.json\n-rw-r--r-- 1 231072 231072 1011061 Sep 24 01:36 screen_items.json\n-rw-r--r-- 1 231072 231072  661279 Sep 24 01:36 units.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [21] TOOL CALL — Bash · 2026-09-24 18:36:14 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_8; cd $W; timeout 100 python3 -c "
import json,collections
labs=json.load(open('data/screen/screen_adjudicated_labels.json')); print(type(labs),len(labs)); k=next(iter(labs)); print(k, json.dumps(labs[k])[:500])
it=json.load(open('data/screen/screen_items.json')); print(type(it),len(it)); print(json.dumps(it[0])[:600])
inv=json.load(open('data/invariance_items.json')); print(len(inv)); print(json.dumps(inv[0])[:600])
p=json.load(open('data/exp5/screen_probes.json')); print(len(p)); print(json.dumps(p[0])[:500])
rows=[json.loads(l) for l in open('results/per_item_screen_hyb.jsonl')]
print(collections.Counter(r['key'][:3] if ':' in r['key'][:3] else 'plain' for r in rows))
E=[json.loads(l) for l in open('results/per_item_hyb_E.jsonl')]
c=collections.Counter(r['sentence_id'] for r in E); print('E per sentence', collections.Counter(c.values()).most_common(8))
print(collections.Counter(r['stratum'] for r in E), collections.Counter(r['y_AB'] for r in E))
"
```

### [22] TOOL RESULT — Bash · 2026-09-24 18:36:14 UTC

```
{"stdout": "<class 'dict'> 1173\n634fdb0b6ece1d72 {\"track\": \"L\", \"system\": \"gpt-3.5-turbo\", \"auto_label\": \"ERROR\", \"equiv_status\": \"NONEQ\", \"repair_ops\": [\"ADD\", \"DROP\"], \"repair_status\": \"FOUND\", \"convention_flags\": [], \"panel_votes\": null, \"final_label\": \"ERROR\", \"label_tier\": \"auto_only\", \"reading_choice\": false, \"addrop_only_suspect\": true, \"join_keys\": {\"system\": \"gpt-3.5-turbo\", \"raw_text\": \"Bonnie performs in school talent shows often.\", \"normtext\": \"bonnie performs in school talent shows often\", \"raw_fol\": \"Perform(bonnie)\"}, \"reference\n<class 'list'> 1169\n{\"item_id\": \"0039a78a4874a842\", \"track\": \"H\", \"kind\": \"malls\", \"system\": \"human_original\", \"text\": \"A product is eco-friendly if it is made from sustainable materials, has a low carbon footprint, or encourages conservation of resources.\", \"candidate_fol\": \"\\u2200x (Product(x) \\u2227 (SustainableMaterials(x) \\u2228 LowCarbonFootprint(x) \\u2228 EncouragesConservation(x)) \\u2192 EcoFriendly(x))\", \"reference_fol\": \"\\u2200x (Product(x) \\u2227 (SustainableMaterials(x) \\u2228 LowCarbonFootprint(x) \\u2228 EncouragesConservation(x)) \\u2192 EcoFriendly(x))\", \"ambiguous\": true, \"story_id\": null, \"source\"\n282\n{\"rw_id\": \"0093af5f8509f6d0_REPRINT\", \"base_item_id\": \"0093af5f8509f6d0\", \"family\": \"REPRINT\", \"text\": \"If a superhero movie is named after a character, that character is a good guy.\", \"candidate_fol\": \"\\u2200x (\\u2200y (SuperheroMovie(x) \\u2227 NamedAfter(x, y) \\u2192 GoodGuy(y)))\", \"system\": \"gpt-4\", \"track\": \"L\", \"story_premises_fol\": [\"\\u2200x (SuperheroMovie(x) \\u2192 GoodGuysWin(x))\", \"SuperheroMovie(surprisingAdventures)\", \"\\u2200x \\u2200y ((GoodGuy(x) \\u2227 \\u00acGoodGuy(y)) \\u2192 (Fight(x, y) \\u2227 Fight(y, x)))\", \"Fight(digby, nemesis)\", \"NamedAfter(surprisingAdventures, digby)\", \n431\n{\"probe\": \"MEANING_RENAME\", \"base_item_id\": \"3afa2e6e67b530a9\", \"fol\": \"BoughtToEarnProfitFrom(karen, strangerThings, lisa)\", \"detail\": \"ShareWith->BoughtToEarnProfitFrom\"}\nCounter({'plain': 1169, 'PR:': 431, 'RW:': 261, 'M:P': 6, 'M:L': 3})\nE per sentence [(13, 351), (14, 178), (6, 100), (12, 71)]\nCounter({'L25': 3260, 'L20': 2000, 'CTRL': 1907, 'EXC': 1340}) Counter({None: 5821, 1: 1822, 0: 864})", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_YYD-HDzfQfEj", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [23] TOOL CALL — Bash · 2026-09-24 18:36:40 UTC

```
mkdir -p /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_YYD-HDzfQfEj/scripts; cat > /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_YYD-HDzfQfEj/scripts/make_mini_demo_data.py <<'EOF'
"""Build mini_demo_data.json: a <=100-row curated subset of the source tables that method.py's build_output() reads.
Streams the source jsonl files line by line (never loads full_method_out.json)."""
import collections, hashlib, json, sys
from pathlib import Path

SRC = Path(sys.argv[1])  # experiment workspace (gen_art_experiment_8)
OUT = Path(__file__).resolve().parent.parent / "mini_demo_data.json"
RES, DATA = SRC / "results", SRC / "data"


def jl(p):
    with open(p) as f:
        for l in f:
            if l.strip():
                yield json.loads(l)


# ---- E: 3 whole sentences (one per stratum CTRL / EXC / L25) that contain both CORRECT and ERROR R_AB labels
E = list(jl(RES / "per_item_hyb_E.jsonl"))
by_s = collections.defaultdict(list)
for r in E:
    by_s[r["sentence_id"]].append(r)
perturb_sids = set()
for u in jl(RES / "perturb_scores.jsonl"):
    perturb_sids.add(u["sentence_id"])
chosen = []
for stratum in ("CTRL", "EXC", "L25"):
    cands = []
    for sid, rs in by_s.items():
        ys = [r["y_AB"] for r in rs]
        if rs[0]["stratum"] == stratum and 0 in ys and 1 in ys and sid in perturb_sids and 12 <= len(rs) <= 14:
            bal = min(ys.count(0), ys.count(1))
            cands.append((-bal, sid))
    chosen.append(sorted(cands)[0][1])
E_rows = [r for sid in chosen for r in by_s[sid]]
keys = {r["row_key"] for r in E_rows}
E_blind = [b for b in jl(DATA / "exp5" / "E_blind.jsonl") if b["row_key"] in keys]

# ---- PERTURB: mutants + controls + base row for one base per chosen E sentence, capped at 36 rows
pb_all = [u for u in jl(RES / "perturb_scores.jsonl") if u["sentence_id"] in chosen]
bases_per_sid = {}
for u in pb_all:
    bases_per_sid.setdefault(u["sentence_id"], u["base"])
pb = []
for sid in chosen:
    grp = [u for u in pb_all if u["base"] == bases_per_sid[sid]]
    base_rows = [u for u in grp if u["key"].startswith("PB:")]
    muts = [u for u in grp if not u["key"].startswith("PB:")]
    # diversity: one row per (operator/control_type, polarity) first
    seen, pick = set(), []
    for u in muts:
        k = (u["operator"], u["control_type"], u["polarity"])
        if k not in seen:
            seen.add(k)
            pick.append(u)
    pb += base_rows[:1] + pick[:11]
item_ids = {u["item_id"] for u in pb}
base_ids = {u["base"] for u in pb}
perturb_rows, have_base = [], set()
for r in jl(DATA / "perturb_rows.jsonl"):
    if r["item_id"] in item_ids:
        perturb_rows.append(r)
    elif r["base_item_id"] in base_ids and r["base_item_id"] not in have_base:
        perturb_rows.append(r)  # build_output looks up a base's text through any row with that base_item_id
        have_base.add(r["base_item_id"])

# ---- screen: 8 labelled plain items + 8 exp-D rewrites + 8 probes
labs = json.loads((DATA / "screen" / "screen_adjudicated_labels.json").read_text())
inv = {x["rw_id"]: x for x in json.loads((DATA / "invariance_items.json").read_text())}
items = {x["item_id"]: x for x in json.loads((DATA / "screen" / "screen_items.json").read_text())}
probes = {f"PR:{p['probe']}:{p['base_item_id']}": p for p in json.loads((DATA / "exp5" / "screen_probes.json").read_text())}
scr = list(jl(RES / "per_item_screen_hyb.jsonl"))
plain = [r for r in scr if r["key"] in items and r["label"] in ("CORRECT", "ERROR")]
plain = [r for r in plain if r["label"] == "CORRECT"][:4] + [r for r in plain if r["label"] == "ERROR"][:4]
rw_seen, rw = set(), []
for r in scr:
    if r["key"].startswith("RW:") and inv[r["key"][3:]]["family"] not in rw_seen and len(rw) < 8:
        rw_seen.add(inv[r["key"][3:]]["family"]); rw.append(r)
pr_seen, pr = set(), []
for r in scr:
    if r["key"].startswith("PR:") and probes[r["key"]]["probe"] not in pr_seen and len(pr) < 8:
        pr_seen.add(probes[r["key"]]["probe"]); pr.append(r)
scr_rows = plain + rw + pr
inv_sub = [inv[r["key"][3:]] for r in rw]
probe_sub = [probes[r["key"]] for r in pr]
item_sub = {r["key"]: items[r["key"]] for r in plain}
for p in probe_sub:
    item_sub[p["base_item_id"]] = items[p["base_item_id"]]
lab_keys = {x["base_item_id"] for x in inv_sub}
lab_sub = {k: {kk: labs[k][kk] for kk in ("final_label", "label_tier", "system", "track")} for k in lab_keys if k in labs}

sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
out = {
    "_about": "Curated subset of the inputs of method.py build_output() (experiment 8, iteration 3). Keys mirror the source files.",
    "selection": json.loads((RES / "selection.json").read_text()),
    "prereg_sha256": {"prereg_hyb.json": sha(RES / "prereg_hyb.json"), "prereg_perturb.json": sha(RES / "prereg_perturb.json")},
    "analysis_perturb_metrics": json.loads((RES / "analysis_perturb.json").read_text())["metrics"],
    "E_blind": E_blind,
    "per_item_hyb_E": E_rows,
    "perturb_scores": pb,
    "perturb_rows": perturb_rows,
    "screen_adjudicated_labels": lab_sub,
    "invariance_items": inv_sub,
    "screen_items": list(item_sub.values()),
    "screen_probes": probe_sub,
    "per_item_screen_hyb": scr_rows,
}
OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1))
print("sentences", chosen)
print({k: len(v) for k, v in out.items() if isinstance(v, (list, dict))})
print("scored rows:", len(E_rows) + len(pb) + len(scr_rows), "bytes", OUT.stat().st_size)
EOF
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_YYD-HDzfQfEj && timeout 300 python3 scripts/make_mini_demo_data.py /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_8
```

### [24] TOOL RESULT — Bash · 2026-09-24 18:36:42 UTC

```
{"stdout": "sentences ['0ef71f65ea70', '0e011c6bf867', '0155490485cc']\n{'selection': 10, 'prereg_sha256': 2, 'analysis_perturb_metrics': 27, 'E_blind': 41, 'per_item_hyb_E': 41, 'perturb_scores': 34, 'perturb_rows': 33, 'screen_adjudicated_labels': 5, 'invariance_items': 6, 'screen_items': 9, 'screen_probes': 3, 'per_item_screen_hyb': 17}\nscored rows: 92 bytes 245403", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [25] TOOL CALL — Bash · 2026-09-24 18:36:46 UTC

```
python3 -c "
import json,collections as c
d=json.load(open('mini_demo_data.json'))
print(c.Counter(r['y_AB'] for r in d['per_item_hyb_E']), c.Counter(r['stratum'] for r in d['per_item_hyb_E']))
print(c.Counter((u['y'],u['operator'] or u['control_type']) for u in d['perturb_scores']))
print(c.Counter(r['key'][:3] for r in d['per_item_screen_hyb']), [r['label'] for r in d['per_item_screen_hyb']])
"
```

### [26] TOOL RESULT — Bash · 2026-09-24 18:36:46 UTC

```
{"stdout": "Counter({1: 19, 0: 18, None: 4}) Counter({'EXC': 14, 'L25': 14, 'CTRL': 13})\nCounter({(1, 'NEG'): 5, (1, 'BIND'): 4, (1, 'ADD'): 4, (0, 'BASE'): 3, (1, 'CONN'): 3, (1, 'DROP'): 2, (1, 'MEANING_RENAME'): 2, (0, 'RENAME_NONCE'): 2, (1, 'QUANT'): 2, (1, 'RESTR'): 2, (1, 'REV'): 2, (1, 'SWAP'): 1, (0, 'REORDER_COMMUTE'): 1, (0, 'DEMORGAN'): 1})\nCounter({'RW:': 6, 'PR:': 3, '20d': 1, '841': 1, '860': 1, '8ff': 1, '597': 1, '475': 1, '573': 1, '07a': 1}) ['CORRECT', 'CORRECT', 'CORRECT', 'CORRECT', 'ERROR', 'ERROR', 'ERROR', 'ERROR', None, None, None, None, None, None, None, None, None]", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [27] TOOL CALL — Bash · 2026-09-24 18:38:34 UTC

```
cat > /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_YYD-HDzfQfEj/scripts/build_notebook.py <<'PYEOF'
"""Writes code_demo.ipynb (cells below). Re-run after editing: python3 scripts/build_notebook.py"""
import json
from pathlib import Path

cells = []
md = lambda s: cells.append({"cell_type": "markdown", "metadata": {}, "source": s.strip("\n")})
code = lambda s: cells.append({"cell_type": "code", "metadata": {}, "execution_co... [truncated, 26262 chars total]
```

### [28] TOOL RESULT — Bash · 2026-09-24 18:38:34 UTC

```
{"stdout": "cells: 30", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [29] TOOL CALL — Bash · 2026-09-24 18:38:44 UTC

```
python3 - <<'EOF'
import re
p='scripts/build_notebook.py'; s=open(p).read()
# extract bodies
e_start=s.index("md(r'''\n### 1. Dataset E")
b_start=s.index("md(r'''\n### 3. Screen items")
e_code=s[s.index('    blind = {r["row_key"]',e_start):s.index("''')",s.index('    blind = {r["row_key"]',e_start))]
p_code=s[s.index('    # ---- PERTURB (mutants',e_start):s.index("''')",s.index('    # ---- PERTURB (mutants',e_start))]
s=s[:e_start]+s[b_start:]
s=s.replace('''    ds = []
    build_output_E(ds, frozen, frozen_label)
    build_output_perturb(ds, frozen, frozen_label)
''', e_code.replace('    blind = {r["row_key"]: r for r in C.jl(C.DATA / "exp5" / "E_blind.jsonl")}\n','').replace('    # ---- dataset E','    ds = []\n    # ---- dataset E') + p_code)
s=s.replace('''    frozen_label = sel.get("frozen_variant") or "NONE_ELIGIBLE"
    ds = []''','''    frozen_label = sel.get("frozen_variant") or "NONE_ELIGIBLE"
    blind = {r["row_key"]: r for r in C.jl(C.DATA / "exp5" / "E_blind.jsonl")}''') if False else s
open(p,'w').write(s)
EOF
grep -n "blind\|ds = \[\]\|build_output_" scripts/build_notebook.py | head
```

### [30] TOOL RESULT — Bash · 2026-09-24 18:38:44 UTC

```
{"stdout": "Traceback (most recent call last):\n  File \"<stdin>\", line 4, in <module>\nValueError: substring not found\n65:`mini_demo_data.json` bundles the subset of each source table that `build_output()` reads. Its keys mirror the original files: `results/per_item_hyb_E.jsonl`, `data/exp5/E_blind.jsonl`, `results/perturb_scores.jsonl`, `data/perturb_rows.jsonl`, `results/selection.json` and so on. The notebook fetches the file from GitHub and falls back to a local copy.\n200:    _JL = {\"E_blind.jsonl\": \"E_blind\", \"per_item_hyb_E.jsonl\": \"per_item_hyb_E\", \"perturb_scores.jsonl\": \"perturb_scores\",\n225:def build_output_E(ds, frozen, frozen_label):\n226:    blind = {r[\"row_key\"]: r for r in C.jl(C.DATA / \"exp5\" / \"E_blind.jsonl\")}\n230:        b = blind[r[\"row_key\"]]\n248:def build_output_perturb(ds, frozen, frozen_label):\n291:    ds = []\n292:    build_output_E(ds, frozen, frozen_label)\n293:    build_output_perturb(ds, frozen, frozen_label)", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [31] ASSISTANT · 2026-09-24 18:38:48 UTC

```
Merging `build_output()` back into one function so it matches the original. I'll edit the generator directly.
```

### [32] TOOL CALL — Read · 2026-09-24 18:38:48 UTC

```
/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_YYD-HDzfQfEj/scripts/build_notebook.py
```

### [33] TOOL RESULT — Read · 2026-09-24 18:38:48 UTC

```
{"type": "text", "file": {"filePath": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_YYD-HDzfQfEj/scripts/build_notebook.py", "content": "    def sha256_file(p: Path) -> str:\n        return data[\"prereg_sha256\"][Path(p).name]\n''')\n\nmd(r'''\n## `build_output()`: assembling `method_out.json`\nThis function is the original, split across three cells for readability. The only edits are marked `# demo:`: the `json.loads(read_text())` calls become lookups in `data`, and `import an_common as C` is replaced by the stand-in above.\n\n### 1. Dataset E: real outputs of 10 LLM generators plus symbolic systems\nEach row carries the candidate, its label and its six consensus scores:\n* `c_*` = binary share of peers that disagree;\n* `g_*` = graded claim-unit disagreement;\n* each for the three maps `hyb`, `align` and `nf`.\n\nAn unparseable candidate gets score 1.0 and coverage status `UNPARSEABLE`; it is never dropped. `y_R_AB` is the label used for AUROC: tier A/B CORRECT (0) or ERROR (1).\n''')\ncode(r'''\ndef build_output_E(ds, frozen, frozen_label):\n    blind = {r[\"row_key\"]: r for r in C.jl(C.DATA / \"exp5\" / \"E_blind.jsonl\")}\n    # ---- dataset E (development for the selection; real generator outputs)\n    ex = []\n    for r in C.jl(RES / \"per_item_hyb_E.jsonl\"):\n        b = blind[r[\"row_key\"]]\n        e = {\"input\": json.dumps({\"text\": b[\"text\"], \"candidate_fol\": b[\"candidate_fol\"], \"system\": b[\"system\"],\n                                  \"prompt_variant\": b[\"prompt_variant\"]}, ensure_ascii=False),\n             \"output\": r[\"final_label\"], \"metadata_fold\": \"E\", \"metadata_row_key\": r[\"row_key\"], \"metadata_sentence_id\": r[\"sentence_id\"],\n             \"metadata_stratum\": r[\"stratum\"], \"metadata_label_tier\": r[\"label_tier\"], \"metadata_y_R_AB\": r[\"y_AB\"],\n             \"metadata_system_class\": r[\"system_class\"], \"metadata_coverage_status\": r[\"coverage_status\"], \"metadata_n_peers\": r[\"n_peers\"],\n             \"predict_c_score_hyb\": s(r[\"c_hyb\"]), \"predict_g_score_hyb\": s(r[\"g_hyb\"]), \"predict_c_score_nf\": s(r[\"c_nf\"]),\n             \"predict_c_score_align\": s(r[\"c_align\"]), \"predict_g_score_align\": s(r[\"g_align\"]), \"predict_g_score_nf\": s(r[\"g_nf\"]),\n             \"predict_frozen_invariant\": s(r.get(frozen)) if frozen else frozen_label}\n        ex.append(e)\n    ds.append({\"dataset\": \"E_heldout_candidates\", \"examples\": ex})\n''')\n\nmd(r'''\n### 2. PERTURB suite: typed mutants, meaning-preserving controls and unmutated bases\nEvery mutant has a known error type (`operator`), a polarity, and `y = 1`. Controls and bases have `y = 0`. All 27 Part-B metrics are copied into the row. A metric that failed on a row appears as `FAIL(...)`, never as a silent gap.\n''')\ncode(r'''\ndef build_output_perturb(ds, frozen, frozen_label):\n    # ---- PERTURB (mutants, controls, bases): every Part B metric\n    pb = C.jl(RES / \"perturb_scores.jsonl\")\n    A = {\"metrics\": data[\"analysis_perturb_metrics\"]}  # demo: was json.loads((RES / \"analysis_perturb.json\").read_text())\n    mets = A[\"metrics\"]\n    ex = []\n    rows = {r[\"item_id\"]: r for r in C.jl(C.DATA / \"perturb_rows.jsonl\")}\n    for u in pb:\n        is_base = u[\"key\"].startswith(\"PB:\")\n        src = rows.get(u[\"item_id\"]) if not is_base else None\n        text = src[\"text\"] if src else next(r[\"text\"] for r in rows.values() if r[\"base_item_id\"] == u[\"base\"])\n        e = {\"input\": json.dumps({\"text\": text, \"candidate_fol\": u[\"fol\"]}, ensure_ascii=False),\n             \"output\": \"ERROR\" if u[\"y\"] == 1 else \"CORRECT\",\n             \"metadata_fold\": \"PERTURB_BASE\" if is_base else (\"PERTURB\" if u[\"y\"] == 1 else \"PERTURB_CONTROL\"),\n             \"metadata_key\": u[\"key\"], \"metadata_base_item_id\": u[\"base\"], \"metadata_operator\": u[\"operator\"],\n             \"metadata_op_fine\": u[\"op_fine\"], \"metadata_control_type\": u[\"control_type\"], \"metadata_polarity\": u[\"polarity\"],\n             \"metadata_matched_pair_id\": u[\"matched_pair_id\"], \"metadata_subtype\": u[\"subtype\"], \"metadata_base_status\": u[\"base_status\"],\n             \"metadata_base_endorsed\": u.get(\"base_endorsed\"),\n             \"predict_frozen_invariant\": s(u.get(frozen)) if frozen else frozen_label}\n        for m in mets:\n            e[f\"predict_{m}\"] = s(u.get(m)) if u.get(m + \"__status\") != \"fail\" else (\"FAIL(\" + s(u.get(m)) + \")\")\n        e[\"predict_c_score_hyb\"] = e.pop(\"predict_c_hyb\", \"NA\")\n        e[\"predict_g_score_hyb\"] = e.pop(\"predict_g_hyb\", \"NA\")\n        e[\"predict_c_score_nf\"] = e.pop(\"predict_c_nf\", \"NA\")\n        e[\"predict_c_score_align\"] = e.pop(\"predict_c_align\", \"NA\")\n        ex.append(e)\n    ds.append({\"dataset\": \"PERTURB_suite\", \"examples\": ex})\n''')\n\nmd(r'''\n### 3. Screen items, exp-D meaning-preserving rewrites and screen probes; then write the file\n* **`RW:` rows** are rewrites of a screen item: renames, reprints, equivalent restatements. Each inherits its base item's label. The rename false-alarm rate that drove the selection is measured on these rows and on PERTURB.\n* **`PR:` rows** are probes: deliberately wrong edits, labelled ERROR.\n* **Plain rows** are screen items with their adjudicated label.\n\nThe last step records the selection outcome in the metadata (`frozen_variant = null`, meaning *none eligible*) and writes `method_out.json`.\n''')\ncode(r'''\ndef build_output():\n    # demo: `import an_common as C` -> the stand-in class C defined above\n    sel = data[\"selection\"]  # demo: was json.loads((RES / \"selection.json\").read_text())\n    frozen = sel.get(\"frozen_score\")\n    frozen_label = sel.get(\"frozen_variant\") or \"NONE_ELIGIBLE\"\n    ds = []\n    build_output_E(ds, frozen, frozen_label)\n    build_output_perturb(ds, frozen, frozen_label)\n    # ---- screen items, exp D rewrites, probes (consensus variants)\n    ex_rw, ex_sc = [], []\n    labs = data[\"screen_adjudicated_labels\"]  # demo: was json.loads((C.DATA / \"screen\" / \"screen_adjudicated_labels.json\").read_text())\n    inv = {x[\"rw_id\"]: x for x in data[\"invariance_items\"]}  # demo: was data/invariance_items.json", "numLines": 90, "startLine": 208, "totalLines": 454}}
```

### [34] ASSISTANT · 2026-09-24 18:39:00 UTC

```
I'll rewrite lines 212–293 so the three sections live in one `build_output()` again, with the markdown describing all three parts before it.
```

### [35] TOOL CALL — Bash · 2026-09-24 18:39:00 UTC

```
python3 - <<'EOF'
p='scripts/build_notebook.py'; L=open(p).read().split('\n')
# 1-indexed lines: E body 226-240, perturb body 249-274, build_output header 286-293
e_body=L[225:240]; p_body=L[248:274]
new_md='''md(r\'\'\'
## `build_output()`: assembling `method_out.json`
This is the original function in one cell. The only edits are marked `# demo:`: the `json.loads(read_text())` calls become lookups in `data`, and `import an_common as C` is replaced by the stand-in above. It builds four datasets:

1. **Dataset E**: real outputs of 10 LLM generators plus symbolic systems. Each row carries the candidate, its label and six consensus scores:
   * `c_*` = binary share of peers that disagree;
   * `g_*` = graded claim-unit disagreement;
   * each for the three maps `hyb`, `align` and `nf`.

   An unparseable candidate gets score 1.0 and coverage status `UNPARSEABLE`; it is never dropped. `y_R_AB` is the label used for AUROC: tier A/B CORRECT (0) or ERROR (1).
2. **PERTURB suite**: typed mutants, meaning-preserving controls and unmutated bases. Every mutant has a known error type (`operator`), a polarity, and `y = 1`. Controls and bases have `y = 0`. All 27 Part-B metrics are copied into the row. A metric that failed on a row appears as `FAIL(...)`, never as a silent gap.
3. **Screen / exp-D rows**:
   * **`RW:` rows** are rewrites of a screen item: renames, reprints, equivalent restatements. Each inherits its base item's label. The rename false-alarm rate that drove the selection is measured on these rows and on PERTURB.
   * **`PR:` rows** are probes: deliberately wrong edits, labelled ERROR.
   * **Plain rows** are screen items with their adjudicated label.

The last step records the selection outcome in the metadata (`frozen_variant = null`, meaning *none eligible*) and writes `method_out.json`.
\'\'\')
code(r\'\'\'
def build_output():
    # demo: `import an_common as C` -> the stand-in class C defined above
    sel = data["selection"]  # demo: was json.loads((RES / "selection.json").read_text())
    frozen = sel.get("frozen_score")
    frozen_label = sel.get("frozen_variant") or "NONE_ELIGIBLE"'''.split('\n')
body = [e_body[0], "    ds = []"] + e_body[1:] + p_body
L = L[:211] + new_md + body + L[293:]
open(p,'w').write('\n'.join(L))
EOF
sed -n 205,300p scripts/build_notebook.py
```

### [36] TOOL RESULT — Bash · 2026-09-24 18:39:00 UTC

```
{"stdout": "        return data[C._JL[Path(p).name]]\n\n    @staticmethod\n    def sha256_file(p: Path) -> str:\n        return data[\"prereg_sha256\"][Path(p).name]\n''')\n\nmd(r'''\n## `build_output()`: assembling `method_out.json`\nThis is the original function in one cell. The only edits are marked `# demo:`: the `json.loads(read_text())` calls become lookups in `data`, and `import an_common as C` is replaced by the stand-in above. It builds four datasets:\n\n1. **Dataset E**: real outputs of 10 LLM generators plus symbolic systems. Each row carries the candidate, its label and six consensus scores:\n   * `c_*` = binary share of peers that disagree;\n   * `g_*` = graded claim-unit disagreement;\n   * each for the three maps `hyb`, `align` and `nf`.\n\n   An unparseable candidate gets score 1.0 and coverage status `UNPARSEABLE`; it is never dropped. `y_R_AB` is the label used for AUROC: tier A/B CORRECT (0) or ERROR (1).\n2. **PERTURB suite**: typed mutants, meaning-preserving controls and unmutated bases. Every mutant has a known error type (`operator`), a polarity, and `y = 1`. Controls and bases have `y = 0`. All 27 Part-B metrics are copied into the row. A metric that failed on a row appears as `FAIL(...)`, never as a silent gap.\n3. **Screen / exp-D rows**:\n   * **`RW:` rows** are rewrites of a screen item: renames, reprints, equivalent restatements. Each inherits its base item's label. The rename false-alarm rate that drove the selection is measured on these rows and on PERTURB.\n   * **`PR:` rows** are probes: deliberately wrong edits, labelled ERROR.\n   * **Plain rows** are screen items with their adjudicated label.\n\nThe last step records the selection outcome in the metadata (`frozen_variant = null`, meaning *none eligible*) and writes `method_out.json`.\n''')\ncode(r'''\ndef build_output():\n    # demo: `import an_common as C` -> the stand-in class C defined above\n    sel = data[\"selection\"]  # demo: was json.loads((RES / \"selection.json\").read_text())\n    frozen = sel.get(\"frozen_score\")\n    frozen_label = sel.get(\"frozen_variant\") or \"NONE_ELIGIBLE\"\n    blind = {r[\"row_key\"]: r for r in C.jl(C.DATA / \"exp5\" / \"E_blind.jsonl\")}\n    ds = []\n    # ---- dataset E (development for the selection; real generator outputs)\n    ex = []\n    for r in C.jl(RES / \"per_item_hyb_E.jsonl\"):\n        b = blind[r[\"row_key\"]]\n        e = {\"input\": json.dumps({\"text\": b[\"text\"], \"candidate_fol\": b[\"candidate_fol\"], \"system\": b[\"system\"],\n                                  \"prompt_variant\": b[\"prompt_variant\"]}, ensure_ascii=False),\n             \"output\": r[\"final_label\"], \"metadata_fold\": \"E\", \"metadata_row_key\": r[\"row_key\"], \"metadata_sentence_id\": r[\"sentence_id\"],\n             \"metadata_stratum\": r[\"stratum\"], \"metadata_label_tier\": r[\"label_tier\"], \"metadata_y_R_AB\": r[\"y_AB\"],\n             \"metadata_system_class\": r[\"system_class\"], \"metadata_coverage_status\": r[\"coverage_status\"], \"metadata_n_peers\": r[\"n_peers\"],\n             \"predict_c_score_hyb\": s(r[\"c_hyb\"]), \"predict_g_score_hyb\": s(r[\"g_hyb\"]), \"predict_c_score_nf\": s(r[\"c_nf\"]),\n             \"predict_c_score_align\": s(r[\"c_align\"]), \"predict_g_score_align\": s(r[\"g_align\"]), \"predict_g_score_nf\": s(r[\"g_nf\"]),\n             \"predict_frozen_invariant\": s(r.get(frozen)) if frozen else frozen_label}\n        ex.append(e)\n    ds.append({\"dataset\": \"E_heldout_candidates\", \"examples\": ex})\n    # ---- PERTURB (mutants, controls, bases): every Part B metric\n    pb = C.jl(RES / \"perturb_scores.jsonl\")\n    A = {\"metrics\": data[\"analysis_perturb_metrics\"]}  # demo: was json.loads((RES / \"analysis_perturb.json\").read_text())\n    mets = A[\"metrics\"]\n    ex = []\n    rows = {r[\"item_id\"]: r for r in C.jl(C.DATA / \"perturb_rows.jsonl\")}\n    for u in pb:\n        is_base = u[\"key\"].startswith(\"PB:\")\n        src = rows.get(u[\"item_id\"]) if not is_base else None\n        text = src[\"text\"] if src else next(r[\"text\"] for r in rows.values() if r[\"base_item_id\"] == u[\"base\"])\n        e = {\"input\": json.dumps({\"text\": text, \"candidate_fol\": u[\"fol\"]}, ensure_ascii=False),\n             \"output\": \"ERROR\" if u[\"y\"] == 1 else \"CORRECT\",\n             \"metadata_fold\": \"PERTURB_BASE\" if is_base else (\"PERTURB\" if u[\"y\"] == 1 else \"PERTURB_CONTROL\"),\n             \"metadata_key\": u[\"key\"], \"metadata_base_item_id\": u[\"base\"], \"metadata_operator\": u[\"operator\"],\n             \"metadata_op_fine\": u[\"op_fine\"], \"metadata_control_type\": u[\"control_type\"], \"metadata_polarity\": u[\"polarity\"],\n             \"metadata_matched_pair_id\": u[\"matched_pair_id\"], \"metadata_subtype\": u[\"subtype\"], \"metadata_base_status\": u[\"base_status\"],\n             \"metadata_base_endorsed\": u.get(\"base_endorsed\"),\n             \"predict_frozen_invariant\": s(u.get(frozen)) if frozen else frozen_label}\n        for m in mets:\n            e[f\"predict_{m}\"] = s(u.get(m)) if u.get(m + \"__status\") != \"fail\" else (\"FAIL(\" + s(u.get(m)) + \")\")\n        e[\"predict_c_score_hyb\"] = e.pop(\"predict_c_hyb\", \"NA\")\n        e[\"predict_g_score_hyb\"] = e.pop(\"predict_g_hyb\", \"NA\")\n        e[\"predict_c_score_nf\"] = e.pop(\"predict_c_nf\", \"NA\")\n        e[\"predict_c_score_align\"] = e.pop(\"predict_c_align\", \"NA\")\n        ex.append(e)\n    ds.append({\"dataset\": \"PERTURB_suite\", \"examples\": ex})\n    # ---- screen items, exp D rewrites, probes (consensus variants)\n    ex_rw, ex_sc = [], []\n    labs = data[\"screen_adjudicated_labels\"]  # demo: was json.loads((C.DATA / \"screen\" / \"screen_adjudicated_labels.json\").read_text())\n    inv = {x[\"rw_id\"]: x for x in data[\"invariance_items\"]}  # demo: was data/invariance_items.json\n    items = {x[\"item_id\"]: x for x in data[\"screen_items\"]}  # demo: was data/screen/screen_items.json\n    probes = {f\"PR:{p['probe']}:{p['base_item_id']}\": p for p in data[\"screen_probes\"]}  # demo: was data/exp5/screen_probes.json\n    for r in C.jl(RES / \"per_item_screen_hyb.jsonl\"):\n        k = r[\"key\"]\n        if k.startswith(\"M:\"):\n            continue\n        if k.startswith(\"RW:\"):\n            x = inv[k[3:]]\n            text, fol, fold = x[\"text\"], x[\"candidate_fol\"], \"REWRITE_EXPD\"\n            out = labs.get(x[\"base_item_id\"], {}).get(\"final_label\") or \"UNLABELLED\"  # a meaning-preserving rewrite inherits its base label\n            base = x[\"base_item_id\"]\n            extra = {\"metadata_rewrite_family\": x[\"family\"], \"metadata_base_item_id\": base,\n                     \"metadata_base_label\": labs.get(base, {}).get(\"final_label\")}\n        elif k.startswith(\"PR:\"):\n            p = probes[k]\n            b = items[p[\"base_item_id\"]]\n            text, fol, fold, out = b[\"text\"], p[\"fol\"], \"SCREEN_PROBE\", \"ERROR\"\n            extra = {\"metadata_probe\": p[\"probe\"], \"metadata_base_item_id\": p[\"base_item_id\"]}\n        else:", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [37] ASSISTANT · 2026-09-24 18:39:06 UTC

```
Now the first test run with every row cap set to the minimum (2).
```

### [38] TOOL CALL — Bash · 2026-09-24 18:39:06 UTC

```
sed -i 's/^MAX_E_ROWS = None /MAX_E_ROWS = 2    /; s/^MAX_PERTURB_ROWS = None /MAX_PERTURB_ROWS = 2    /; s/^MAX_SCREEN_ROWS = None /MAX_SCREEN_ROWS = 2    /' scripts/build_notebook.py && grep -n "^MAX_" scripts/build_notebook.py && python3 scripts/build_notebook.py && /usr/local/bin/python3.12 -m venv .nb_env && .nb_env/bin/pip install -q pip jupyter ipykernel 2>&1 | tail -2; start=$(date +%s); timeout 700 .nb_env/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -30; echo "runtime $(( $(date +%s)-start ))s"
```

### [39] TOOL RESULT — Bash · 2026-09-24 18:49:54 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false, "backgroundTaskId": "bx0qyklxi", "timedOutAfterMs": 600000}
```

### [40] ASSISTANT · 2026-09-24 18:50:46 UTC

```
The first test run moved to the background because the venv and pip installs are slow on this filesystem. I'll check its progress.
```

### [41] TOOL CALL — Bash · 2026-09-24 18:50:46 UTC

```
sleep 5; cat /tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-YYD-HDzfQfEj/921fc65d-5ce4-4ae5-9da8-7c8e9ce14d4b/tasks/bx0qyklxi.output; ls /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_YYD-HDzfQfEj/.nb_env/lib/python3.12/site-packages | wc -l
```

### [42] TOOL RESULT — Bash · 2026-09-24 18:50:46 UTC

```
{"stdout": "94:MAX_E_ROWS = 2           # E candidate rows (demo file has 41; full run: 8507)\n95:MAX_PERTURB_ROWS = 2     # PERTURB mutant/control/base rows (demo file has 34; full run: 5402)\n96:MAX_SCREEN_ROWS = 2      # screen items + exp-D rewrites + probes (demo file has 17; full run: 1870 scored keys)\ncells: 26\n[notice] A new release of pip is available: 25.0.1 -> 26.2.1\n[notice] To update, run: python3.12 -m pip install --upgrade pip\n223", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [43] TOOL CALL — Bash · 2026-09-24 18:50:46 UTC

```
F=/tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-YYD-HDzfQfEj/921fc65d-5ce4-4ae5-9da8-7c8e9ce14d4b/tasks/bx0qyklxi.output; for i in $(seq 1 55); do grep -q "runtime" $F && break; sleep 10; done; cat $F
```

### [44] TOOL RESULT — Bash · 2026-09-24 18:55:20 UTC

```
{"stdout": "94:MAX_E_ROWS = 2           # E candidate rows (demo file has 41; full run: 8507)\n95:MAX_PERTURB_ROWS = 2     # PERTURB mutant/control/base rows (demo file has 34; full run: 5402)\n96:MAX_SCREEN_ROWS = 2      # screen items + exp-D rewrites + probes (demo file has 17; full run: 1870 scored keys)\ncells: 26\n[notice] A new release of pip is available: 25.0.1 -> 26.2.1\n[notice] To update, run: python3.12 -m pip install --upgrade pip\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m A new release of pip is available: \u001b[0m\u001b[31;49m25.0.1\u001b[0m\u001b[39;49m -> \u001b[0m\u001b[32;49m26.2.1\u001b[0m\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m To update, run: \u001b[0m\u001b[32;49mpython3.12 -m pip install --upgrade pip\u001b[0m\n\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m A new release of pip is available: \u001b[0m\u001b[31;49m25.0.1\u001b[0m\u001b[39;49m -> \u001b[0m\u001b[32;49m26.2.1\u001b[0m\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m To update, run: \u001b[0m\u001b[32;49mpython3.12 -m pip install --upgrade pip\u001b[0m\n[NbConvertApp] Writing 158486 bytes to code_demo.ipynb\nruntime 378s\n\n[exited with code 0]", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [45] ASSISTANT · 2026-09-24 18:55:20 UTC

```
The minimum-config run passed in 378 s, almost all of it pip installs. Next I'll check the cell outputs, then scale to all demo rows.
```

### [46] TOOL CALL — Bash · 2026-09-24 18:55:20 UTC

```
python3 -c "
import json
nb=json.load(open('code_demo.ipynb'))
for i,c in enumerate(nb['cells']):
    if c['cell_type']!='code': continue
    for o in c['outputs']:
        t=o.get('text') or o.get('data',{}).get('text/plain') or o.get('ename','')
        if isinstance(t,list): t=''.join(t)
        print(f'--- cell {i} [{o[\"output_type\"]}]'); print(str(t)[:1200])
"
```

### [47] TOOL RESULT — Bash · 2026-09-24 18:55:20 UTC

```
{"stdout": "--- cell 1 [stream]\n\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m A new release of pip is available: \u001b[0m\u001b[31;49m25.0.1\u001b[0m\u001b[39;49m -> \u001b[0m\u001b[32;49m26.2.1\u001b[0m\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m To update, run: \u001b[0m\u001b[32;49mpython3.12 -m pip install --upgrade pip\u001b[0m\n\n--- cell 1 [stream]\n\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m A new release of pip is available: \u001b[0m\u001b[31;49m25.0.1\u001b[0m\u001b[39;49m -> \u001b[0m\u001b[32;49m26.2.1\u001b[0m\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m To update, run: \u001b[0m\u001b[32;49mpython3.12 -m pip install --upgrade pip\u001b[0m\n\n--- cell 6 [stream]\n{'selection': 10, 'prereg_sha256': 2, 'analysis_perturb_metrics': 27, 'E_blind': 41, 'per_item_hyb_E': 41, 'perturb_scores': 34, 'perturb_rows': 33, 'screen_adjudicated_labels': 5, 'invariance_items': 6, 'screen_items': 9, 'screen_probes': 3, 'per_item_screen_hyb': 17}\n\n--- cell 8 [stream]\n2 2 2\n\n--- cell 10 [execute_result]\n2\n--- cell 13 [stream]\nscore     src/run_scoring.py E --stage all ; src/run_scoring.py screen --stage all\ngate      src/gate_check.py\nfreeze_a  src/freeze_prereg_hyb.py\npart_a    src/analyse_hyb.py\ncalib     src/prep_calib.py\napi       src/run_api_perturb.py\ncpu_b     src/perturb_cpu.py\ngpu_b     src/perturb_gpu.py --which judges_disg,verb,nli\ns4        src/fit_s4_perturb.py\nfreeze_b  src/freeze_prereg_perturb.py\npart_b    src/analyse_perturb.py\npart_c    src/typing_perturb.py\ntests     -m pytest -q -c pytest.ini tests\n\n--- cell 21 [stream]\n18:53:00|INFO   |method_out.json: [('E_heldout_candidates', 2), ('PERTURB_suite', 2), ('expD_rewrites_screen', 0), ('screen_items_and_probes', 2)]\n\n--- cell 21 [stream]\n{\n \"frozen_variant\": null,\n \"note\": \"NEITHER ELIGIBLE: no rename-invariant consensus exists here; both reported as failed; the R_COMP read uses ALIGN.\",\n \"E_strat_auroc_R_AB\": {\n  \"HYB\": 0.7375072927473793,\n  \"NF-anchored\": 0.6859960770958894,\n  \"ALIGN\": 0.7414618757606236\n }\n}\n\n--- cell 23 [stream]\nE_heldout_candidates       2\nPERTURB_suite              2\nexpD_rewrites_screen       0\nscreen_items_and_probes    2 \n\nSentence: The son of Brian Winter, Andy Winter, is a football player who plays for Hamilton Academical.\n                               system                                                                                                                                                                                                                                                       candidate_fol  output  predict_c_score_align  predict_c_score_hyb  predict_c_score_nf\n                           ccg2lambda ∃x1 ((((Son(x1) ∧ ∃x2 (((Winter(x2) ∧ Brian(x2)) ∧ Eq(x1, x2)))) ∧ ∃x3 (((Winter(x3) ∧ Andy(x3)) ∧ Eq(x1, x3)))) ∧ ∃x4 ((((Player(x4) ∧ Football(x4)) ∧ ∃e5 (((Play(e5) ∧ Subj(e5, x4)) ∧ ∃x6 (((Academical(x6) ∧ Hamilton(x6)) ∧ For(e5, x6)))))) ∧ Eq(x1, x4)))))   ERROR               1.000000             1.000000            1.000000\nG1b:meta-llama/llama-3.3-70b-instruct                                                                                                                                                                Son(andyWinter, brianWinter) ∧ FootballPl\n--- cell 24 [stream]\nMean score by row kind (higher = flagged as error). Controls/BASE should be low, mutants high:\n\n--- cell 24 [stream]\n      c_score_align  c_score_hyb  c_score_nf  p_peer_text  l3_z3  judge_cheap_disg  parse_fail\nkind                                                                                          \nBASE           0.42         0.42        0.42         0.51    1.0               0.0         0.0\nBIND           1.00         1.00        1.00         0.92    1.0               1.0         0.0\n\nDemo PERTURB AUROC (mutants vs controls+bases, n=2, 1 mutants):\ng_align                     1.0\ng_nf                        1.0\np_peer_text                 1.0\nrt_nli_min_alt_local        1.0\nrt_embed_cos_local          1.0\nrt_nli_contra_local         1.0\nrt_nli_bwd_local            1.0\nrt_nli_min_local            1.0\nrt_nli_fwd_local            1.0\njudge_local_qwen8b_disg     1.0\njudge_local_llama8b_disg    1.0\nc_score_hyb                 1.0\ng_score_hyb                 1.0\njudge_cheap_disg            1.0\nS4_local                    1.0\nc_score_nf                  1.0\nc_score_align               1.0\npilot_joint_conflict        0.5\nparse_fail                  0.5\np_text                      0.5\nl3_z3                       0.5\nl2_bow                      0.5\npilot_dangling              0.5\npilot_arity_incons \n--- cell 25 [display_data]\n<Figure size 1700x520 with 3 Axes>\n--- cell 25 [stream]\nmetadata_fold  output predict_c_score_align predict_c_score_hyb predict_c_score_nf\n       SCREEN CORRECT              0.400000            0.400000           0.400000\n       SCREEN CORRECT              0.600000            0.600000           0.600000", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [48] ASSISTANT · 2026-09-24 18:55:20 UTC

```
It runs cleanly. For readability I'll shorten long formulas in the E table, then scale all caps to `None` (every demo row) and re-run.
```

### [49] TOOL CALL — Bash · 2026-09-24 18:55:20 UTC

```
python3 - <<'EOF'
p='scripts/build_notebook.py'; s=open(p).read()
s=s.replace('''E["candidate_fol"] = E["input"].map(lambda s_: json.loads(s_)["candidate_fol"])''','''E["candidate_fol"] = E["input"].map(lambda s_: json.loads(s_)["candidate_fol"][:80])  # truncated for display''')
s=s.replace("MAX_E_ROWS = 2    ","MAX_E_ROWS = None ").replace("MAX_PERTURB_ROWS = 2    ","MAX_PERTURB_ROWS = None ").replace("MAX_SCREEN_ROWS = 2    ","MAX_SCREEN_ROWS = None ")
open(p,'w').write(s)
EOF
grep -n "^MAX_" scripts/build_notebook.py; python3 scripts/build_notebook.py; start=$(date +%s); timeout 700 .nb_env/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | grep -v notice | tail -5; echo "runtime $(( $(date +%s)-start ))s"
```

### [50] TOOL RESULT — Bash · 2026-09-24 18:56:22 UTC

```
{"stdout": "94:MAX_E_ROWS = None        # E candidate rows (demo file has 41; full run: 8507)\n95:MAX_PERTURB_ROWS = None  # PERTURB mutant/control/base rows (demo file has 34; full run: 5402)\n96:MAX_SCREEN_ROWS = None   # screen items + exp-D rewrites + probes (demo file has 17; full run: 1870 scored keys)\ncells: 26\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n\n\n[NbConvertApp] Writing 187978 bytes to code_demo.ipynb\nruntime 50s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [51] TOOL CALL — Bash · 2026-09-24 18:56:22 UTC

```
python3 -c "
import json,base64
nb=json.load(open('code_demo.ipynb'))
for i,c in enumerate(nb['cells']):
    if c['cell_type']!='code' or i<20: continue
    for o in c['outputs']:
        if 'image/png' in o.get('data',{}): open('scripts/_fig_check.png','wb').write(base64.b64decode(o['data']['image/png'])); print('fig saved'); continue
        t=o.get('text') or o.get('data',{}).get('text/plain') or o.get('ename','')
        if isinstance(t,list): t=''.join(t)
        print(f'--- cell {i}'); print(str(t)[:3500])
"
```

### [52] TOOL RESULT — Bash · 2026-09-24 18:56:22 UTC

```
{"stdout": "--- cell 21\n18:54:15|INFO   |method_out.json: [('E_heldout_candidates', 41), ('PERTURB_suite', 34), ('expD_rewrites_screen', 6), ('screen_items_and_probes', 11)]\n\n--- cell 21\n{\n \"frozen_variant\": null,\n \"note\": \"NEITHER ELIGIBLE: no rename-invariant consensus exists here; both reported as failed; the R_COMP read uses ALIGN.\",\n \"E_strat_auroc_R_AB\": {\n  \"HYB\": 0.7375072927473793,\n  \"NF-anchored\": 0.6859960770958894,\n  \"ALIGN\": 0.7414618757606236\n }\n}\n\n--- cell 23\nE_heldout_candidates       41\nPERTURB_suite              34\nexpD_rewrites_screen        6\nscreen_items_and_probes    11 \n\nSentence: The son of Brian Winter, Andy Winter, is a football player who plays for Hamilton Academical.\n                                     system                                                                    candidate_fol  output  predict_c_score_align  predict_c_score_hyb  predict_c_score_nf\n                                 ccg2lambda ∃x1 ((((Son(x1) ∧ ∃x2 (((Winter(x2) ∧ Brian(x2)) ∧ Eq(x1, x2)))) ∧ ∃x3 (((Winter   ERROR               1.000000             1.000000            1.000000\n      G1b:meta-llama/llama-3.3-70b-instruct Son(andyWinter, brianWinter) ∧ FootballPlayer(andyWinter) ∧ PlaysFor(andyWinter, CORRECT               0.333333             0.333333            0.333333\n      G1b:meta-llama/llama-3.3-70b-instruct ∃x (SonOf(x, brianWinter) ∧ Name(x, andyWinter) ∧ FootballPlayer(x) ∧ PlaysFor(x   ERROR               0.888889             0.888889            0.888889\n        G1:meta-llama/llama-3.1-8b-instruct Son(brianWinter, andyWinter) ∧ FootballPlayer(andyWinter) ∧ PlaysFor(andyWinter,   ERROR               1.000000             1.000000            1.000000\n               G2:qwen/qwen3-235b-a22b-2507 Son(andyWinter, brianWinter) ∧ FootballPlayer(andyWinter) ∧ PlaysFor(andyWinter, CORRECT               0.400000             0.400000            0.400000\n               G2:qwen/qwen3-235b-a22b-2507 ∃x (Son(x, brianWinter) ∧ Name(x, andyWinter) ∧ FootballPlayer(x) ∧ PlaysFor(x,    ERROR               0.900000             0.900000            0.900000\nG3:mistralai/mistral-small-3.2-24b-instruct ∃x (Person(x) ∧ SonOf(x, brianWinter) ∧ Name(x, andyWinter) ∧ FootballPlayer(x)    ERROR               1.000000             1.000000            1.000000\n                  G4:deepseek/deepseek-v3.2 FootballPlayer(andyWinter) ∧ SonOf(andyWinter, brianWinter) ∧ PlaysFor(andyWinte CORRECT               0.454545             0.454545            0.454545\n                   G5:google/gemma-3-27b-it SonOf(andyWinter, brianWinter) ∧ FootballPlayer(andyWinter) ∧ PlaysFor(andyWinte CORRECT               0.500000             0.500000            0.500000\n                         G6:microsoft/phi-4 SonOf(andyWinter, brianWinter) ∧ FootballPlayer(andyWinter) ∧ PlaysFor(andyWinte CORRECT               0.454545             0.454545            0.454545\n                     G7:openai/gpt-4.1-mini Son(andyWinter, brianWinter) ∧ FootballPlayer(andyWinter) ∧ PlaysFor(andyWinter, CORRECT               0.454545             0.454545            0.454545\n                 G8:google/gemini-2.5-flash SonOf(andyWinter, brianWinter) ∧ FootballPlayer(andyWinter) ∧ PlaysFor(andyWinte CORRECT               0.500000             0.500000            0.500000\n              G9:cohere/command-r7b-12-2024             FootballPlayer(AndyWinter) ∧ PlaysFor(AndyWinter, hamiltonAccademic)   ERROR               1.000000             1.000000            1.000000\n\nCoverage (never dropped): {'OK': 41}\n\nE rows with an R_AB label: 37 (ERROR=19)\n               demo AUROC (R_AB)  full-run stratified AUROC\nc_score_hyb                0.778                      0.738\nc_score_align              0.782                      0.741\nc_score_nf                 0.838                      0.686\ng_score_hyb                0.883                        NaN\ng_score_align              0.870                        NaN\ng_score_nf                 0.883                        NaN\n\n--- cell 24\nMean score by row kind (higher = flagged as error). Controls/BASE should be low, mutants high:\n                      c_score_align  c_score_hyb  c_score_nf  p_peer_text  l3_z3  judge_cheap_disg  parse_fail\nkind                                                                                                          \nADD                            1.00         1.00        1.00         1.00   0.38              1.00         0.0\nBASE                           0.52         0.52        0.65         0.49   0.50              0.02         0.0\nBIND                           1.00         1.00        1.00         0.85   0.60              1.00         0.0\nCONN                           1.00         1.00        1.00         0.86   0.50              1.00         0.0\nDROP                           0.96         0.96        0.96         0.97   0.68              0.52         0.0\nMEANING_RENAME                 1.00         0.71        0.71         1.00   0.97              0.52         0.0\nNEG                            1.00         1.00        1.00         0.87   0.59              1.00         0.0\nQUANT                          1.00         1.00        1.00         0.84   0.31              1.00         0.0\nRESTR                          1.00         1.00        1.00         0.84   0.31              1.00         0.0\nREV                            1.00         1.00        1.00         0.86   0.42              1.00         0.0\nSWAP                           0.92         0.92        0.92         0.89   1.00              0.00         0.0\nctrl:DEMORGAN                  0.42         0.42        0.42         0.19   0.00              1.00         0.0\nctrl:RENAME_NONCE              1.00         0.71        0.71         1.00   0.70              0.52         0.0\nctrl:REORDER_COMMUTE           0.42         0.42        0.42         0.51   1.00              0.00         0.0\n\n--- cell 24\n\nDemo PERTURB AUROC (mutants vs controls+bases, n=34, 27 mutants):\nc_score_hyb                 0.905\nS4_local                    0.873\nc_score_align               0.847\nc_score_nf                  0.825\njudge_cheap_disg            0.812\nrt_nli_min_local            0.799\nrt_nli_fwd_local            0.788\nrt_nli_min_alt_local        0.772\njudge_local_qwen8b_disg     0.767\nrt_embed_cos_local          0.762\nrt_nli_contra_local         0.746\ng_nf                        0.725\ng_score_hyb                 0.725\ng_align                     0.698\np_peer_text                 0.693\nrt_nli_bwd_local            0.672\njudge_local_llama8b_disg    0.579\nsc5_local_entropy           0.574\nsc5_local_eq_frac           0.553\nl3_z3                       0.526\nl2_bow                      0.526\npilot_joint_conflict        0.519\nparse_fail                  0.500\npilot_shape_incons          0.500\npilot_arity_incons          0.500\npilot_dangling              0.500\np_text                      0.497\n\nfig saved\n--- cell 25\nmetadata_fold metadata_rewrite_family metadata_probe  output predict_c_score_align predict_c_score_hyb predict_c_score_nf\n REWRITE_EXPD                  RENAME                CORRECT              1.000000            0.400000           0.400000\n REWRITE_EXPD          CONTRAPOSITIVE                CORRECT              0.600000            0.600000           0.600000\n REWRITE_EXPD                 REORDER                CORRECT              0.400000            0.400000           0.400000\n REWRITE_EXPD                DEMORGAN                CORRECT              0.400000            0.400000           0.400000\n REWRITE_EXPD                 REPRINT                  ERROR              0.000000            0.000000           0.000000\n REWRITE_EXPD                  PRENEX                CORRECT              0.000000            0.000000           0.000000\n       SCREEN                                        CORRECT              0.400000            0.400000           0.400000\n       SCREEN                                        CORRECT              0.600000            0.600000           0.600000\n       SCREEN                                        CORRECT              0.400000            0.400000           0.400000\n       SCREEN                                        CORRECT              0.600000            0.600000           0.600000\n       SCREEN                                          ERROR              0.400000            0.400000           0.400000\n       SCREEN                                          ERROR              0.000000            0.000000           0.000000\n       SCREEN                                          ERROR              0.000000            0.000000           0.000000\n       SCREEN                                          ERROR              0.000000            0.000000           0.000000\n SCREEN_PROBE                         MEANING_RENAME   ERROR              1.000000            0.600000           0.600000\n SCREEN_PROBE                           ROLE_PERMUTE   ERROR              1.000000            1.000000           1.000000\n SCREEN_PROBE                                   SWAP   ERROR              1.000000            1.000000           1.000000", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [53] ASSISTANT · 2026-09-24 18:56:22 UTC

```
All rows run in 50 s. The demo rows show the expected effect: on a RENAME rewrite, ALIGN gives 1.0 while HYB/NF give 0.4. Now I'll look at the figure.
```

### [54] TOOL CALL — Read · 2026-09-24 18:56:22 UTC

```
/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_YYD-HDzfQfEj/scripts/_fig_check.png
```

### [55] TOOL RESULT — Read · 2026-09-24 18:56:22 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [56] ASSISTANT · 2026-09-24 18:56:22 UTC

```
Two small figure fixes: panel (a) shares colours with (c) but uses them for different things, and the legend in (c) covers bars. I'll switch (a) to greys, move the legend in (c), and run once more.
```

### [57] TOOL CALL — Bash · 2026-09-24 18:56:22 UTC

```
python3 - <<'EOF'
p='scripts/build_notebook.py'; s=open(p).read()
s=s.replace('label=f"demo ({len(lab)} rows)", color="#4C72B0")','label=f"demo ({len(lab)} rows)", color="#4D4D4D")')
s=s.replace('label="full run (8,507 rows)", color="#DD8452")','label="full run (8,507 rows)", color="#B3B3B3")')
s=s.replace('ax[2].tick_params(axis="x", labelsize=7, rotation=75); ax[2].legend(fontsize=8)','ax[2].tick_params(axis="x", labelsize=7, rotation=75); ax[2].set_xlabel("")\nax[2].legend(fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.42), ncol=3)')
open(p,'w').write(s)
EOF
python3 scripts/build_notebook.py; start=$(date +%s); timeout 700 .nb_env/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | grep -iE "error|Writing"; echo "runtime $(( $(date +%s)-start ))s"; python3 -c "
import json,base64
nb=json.load(open('code_demo.ipynb'))
for c in nb['cells']:
    for o in c.get('outputs',[]):
        if o['output_type']=='error': print('ERR',o['ename'])
        if 'image/png' in o.get('data',{}): open('scripts/_fig_check.png','wb').write(base64.b64decode(o['data']['image/png']))
"
```

### [58] TOOL RESULT — Bash · 2026-09-24 18:56:22 UTC

```
{"stdout": "cells: 26\n[NbConvertApp] Writing 184204 bytes to code_demo.ipynb\nruntime 54s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [59] TOOL CALL — Read · 2026-09-24 18:56:22 UTC

```
/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_YYD-HDzfQfEj/scripts/_fig_check.png
```

### [60] TOOL RESULT — Read · 2026-09-24 18:56:22 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [61] ASSISTANT · 2026-09-24 18:56:22 UTC

```
The figure looks right. Next: clean up the test artifacts and run the TODO 6 checks.
```

### [62] TOOL CALL — Bash · 2026-09-24 18:56:22 UTC

```
rm -rf .nb_env scripts/_fig_check.png method_out.json logs && grep -c 'GITHUB_DATA_URL = \\"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/main/round-3/experiment-8/demo/mini_demo_data.json\\"' code_demo.ipynb; grep -c "urllib.request.urlopen(GITHUB_DATA_URL)" code_demo.ipynb; ls -la; du -sh .; ls -la .aii; git status --short | head
```

### [63] TOOL RESULT — Bash · 2026-09-24 18:56:22 UTC

```
{"stdout": "1\n1\ntotal 6074\ndrwxr-xr-x 4 root root 2000118 Sep 24 18:56 .\ndrwxr-xr-x 6 root root 2000594 Sep 24 18:34 ..\ndrwxr-xr-x 2 root root       1 Sep 24 18:31 .aii\n-rw------- 1 root root      54 Sep 24 18:32 .aii_claude_session.json\n-rw-r--r-- 1 root root  791378 Sep 24 18:56 .repl_agent.ptylog\n-rw-r--r-- 1 root root  184292 Sep 24 18:55 code_demo.ipynb\n-rw-r--r-- 1 root root  245403 Sep 24 18:36 mini_demo_data.json\ndrwxr-xr-x 2 root root 1003027 Sep 24 18:56 scripts\n4.1M\t.\ntotal 1954\ndrwxr-xr-x 2 root root       1 Sep 24 18:31 .\ndrwxr-xr-x 4 root root 2000118 Sep 24 18:56 ..\nfatal: not a git repository (or any parent up to mount point /ai-inventor)\nStopping at filesystem boundary (GIT_DISCOVERY_ACROSS_FILESYSTEM not set).", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [64] ASSISTANT · 2026-09-24 18:56:38 UTC

```
Checks pass. The workspace holds nothing heavy (4.1 MB total), so the manifest needs no entries. Writing the manifest, the README and the structured output.
```

### [65] TOOL CALL — Bash · 2026-09-24 18:56:38 UTC

````
cat > .aii/manifest.yaml <<'EOF'
# Nothing heavy is left in this workspace: all files are text/JSON/notebook under the 10 MB auto-keep floor.
# The disposable test venv (.nb_env/) was already removed; rebuild it with the command in README.md.
entries: []
EOF
cat > README.md <<'EOF'
# Demo: rename-proof logic consensus and error-type tests (round 3, experiment 8)

This is a Colab-ready demo notebook for `method.py` from the experiment "Rename-proof logic consensus and error-type tests". The experiment belongs to a study of **gold-free metrics for NL→FOL output**: scores that predict whether a candidate first-order-logic formula is faithful to its sentence without a gold formula.

## What the notebook does
* It splits the original `method.py` into cells and adds explanations between them. Code changes are kept to a minimum.
  * The 13-stage pipeline (`STAGES`, `DONE_MARK`, `run()`) is shown unchanged but **not executed**. It needs the full experiment workspace, z3, a GPU and OpenRouter. The flag `RUN_PIPELINE = False` controls this.
  * The output stage, **`build_output()`**, runs verbatim on a curated subset of its real input tables. The only changes are file reads redirected to the loaded `data` dict, each marked `# demo:`.
* The final cells summarise the `method_out.json` that was just built:
  * E-candidate AUROCs for the consensus maps (HYB / ALIGN / NF), next to the full-run numbers;
  * per-error-type mean scores and AUROCs for all 27 PERTURB metrics;
  * a rename-invariance view.

## Layout
| Path | What it is |
|---|---|
| `code_demo.ipynb` | The demo notebook, executed. It runs in about 1 min once the packages are installed. |
| `mini_demo_data.json` | The demo data: 41 E rows (3 sentences, one each from strata CTRL / EXC / L25), 34 PERTURB rows (mutants, controls, bases), 17 screen / exp-D rewrite / probe rows, plus the matching lookup tables (`E_blind`, `perturb_rows`, `screen_items`, …) and `selection.json`. |
| `scripts/make_mini_demo_data.py` | Rebuilds `mini_demo_data.json` from the experiment workspace. It streams the source JSONL files. |
| `scripts/build_notebook.py` | Generates `code_demo.ipynb` from the cell sources. |

## How to run
* **Colab:** open `code_demo.ipynb` and run all cells. The data is fetched from `GITHUB_DATA_URL`.
* **Locally** (the notebook falls back to `./mini_demo_data.json`):
```bash
python3.12 -m venv .nb_env && .nb_env/bin/pip install -q jupyter ipykernel
.nb_env/bin/jupyter nbconvert --to notebook --execute code_demo.ipynb --output code_demo.ipynb
```
* **Row caps:** the config cell sets `MAX_E_ROWS`, `MAX_PERTURB_ROWS` and `MAX_SCREEN_ROWS`. `None` means all demo rows. The full run had 8,507 E rows, 5,402 PERTURB rows and 1,870 screen keys.

## Restoring removed files
Nothing was marked `delete` (`.aii/manifest.yaml` has no entries). The test environment `.nb_env/` was temporary and was deleted after testing. To recreate it, run the `python3.12 -m venv` command above.
EOF
cat > .terminal_claude_agent_struct_out.json <<'EOF'
{"out_expected_files": {"notebook": "code_demo.ipynb", "mini_data_file": "mini_demo_data.json"}}
EOF
cat .terminal_claude_agent_struct_out.json
````

### [66] TOOL RESULT — Bash · 2026-09-24 18:56:38 UTC

```
{"stdout": "{\"out_expected_files\": {\"notebook\": \"code_demo.ipynb\", \"mini_data_file\": \"mini_demo_data.json\"}}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [67] ASSISTANT · 2026-09-24 18:56:48 UTC

```
The demo notebook `code_demo.ipynb` and its data file `mini_demo_data.json` are built. The notebook runs top to bottom in a fresh Python 3.12 environment with no errors.

**What runs and what doesn't.** `method.py` has two parts: a 13-stage pipeline and a final step, `build_output()`, that writes `method_out.json`.
- **The pipeline is shown but not run.** It needs the full experiment workspace, z3, a GPU and OpenRouter. It is copied unchanged next to a printed stage plan, behind `RUN_PIPELINE = False`.
- **`build_output()` runs on real data.** Its code is unchanged except where it reads files: those reads now come from the loaded demo data, each marked `# demo:`. A small stand-in replaces the helper module `an_common`.

**Demo data.** `mini_demo_data.json` holds 92 scored rows taken from the experiment's real input tables:
- 41 E candidates from 3 sentences, one each from the CTRL, EXC and L25 strata, with both CORRECT and ERROR labels;
- 34 PERTURB rows (mutants of 11 error types, plus controls and bases);
- 17 screen, rewrite and probe rows.

**Scaling.** The config cell has three row caps. I first ran with each set to 2 (378 s from a clean environment, almost all of it package installs), then with all demo rows (about 50 s once packages are installed). Both passed. The full-run sizes (8,507 E rows, 5,402 PERTURB rows) are noted in comments.

**Results cells.** On these few dozen rows the numbers are only illustrative:
- **E:** AUROC is about 0.78 for both HYB and ALIGN. The full-run values (0.738 and 0.741) are shown next to them.
- **PERTURB:** consensus scores, S4 and the flash-lite judge rank highest. The user's pilot structural metrics sit at 0.50, i.e. chance.
- **Renames:** on renamed controls ALIGN gives 1.0 (no peer agrees) while HYB/NF give 0.71. That is the effect behind the pre-registered selection.

**TODO 6 checks pass:**
1. `GITHUB_DATA_URL` appears exactly as specified.
2. `mini_demo_data.json` exists.
3. The data is loaded through the GitHub URL with a local fallback.

I also added `README.md`, an empty `.aii/manifest.yaml` (nothing large is left; the whole folder is 4.1 MB), the two scripts that rebuild the data and the notebook, and `.terminal_claude_agent_struct_out.json`. There was no todo-list tool in this session, so I followed the TODOs in order without one.

Files are in `art_YYD-HDzfQfEj/`:
- `code_demo.ipynb`
- `mini_demo_data.json`
- `README.md`
- `scripts/make_mini_demo_data.py`
- `scripts/build_notebook.py`
```
