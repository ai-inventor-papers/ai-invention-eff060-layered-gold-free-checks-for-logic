# gen_demo_art_dataset_4 — report_results

> Phase: `gen_paper_repo` · `gen_demo_art`
> Run: `gen_paper_repo_a2e1d024cc16` — Cross-Family Solver Consensus as a Gold-Free Faithfulness Metric for Logic Translation
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_demo_art_dataset_4` (terminal_claude_agent, claude-opus-5-5)

### [1] CONFIG · 2026-09-25 16:37:28 UTC

```
model: claude-opus-5-5 | effort: high | permission: bypassPermissions
```

### [2] SYSTEM-USER prompt · 2026-09-25 16:37:34 UTC

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
Your workspace: `/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_Ia_FT284H33j`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_Ia_FT284H33j/`:
GOOD: `/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_Ia_FT284H33j/file.py`, `/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_Ia_FT284H33j/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
<disposable_outputs>
A SHARED CACHE ALREADY EXISTS FOR THIS RUN: `/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/.shared_cache`
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
id: art_Ia_FT284H33j
type: dataset
title: Name-free labels for free-vocabulary logic translations
summary: >-
  T7b name-free labels for R_COMP FREE (free-vocabulary NL->FOL rule translations; 221 templated sentences, 10 LLM slots /
  9 families). full_data_out.json (exp_sel_data_out) has 3 groups: (1) rcomp_free_labels, 2,652 rows (one per FREE generation
  record, row_key = exp-7 recipe), label from an exhaustive, certificate-backed, name-free map search (injective symbol maps
  + B1/B2 reification, B3 merge, B4 split, B5 lexical negation; z3 relevance/polarity prunes, 128-model finite countermodels,
  z3 equivalence; 0 caps, 0 z3 unknown) under a hashed prereg v1.1. IMPORTANT: labels are SEARCH-ONLY (deviation D9: run OpenRouter
  budget exhausted before this artifact's first call, $0 spent): ERROR_CERT 759 (final, exact relative to the family), UNRESOLVED_GLOSS_NOT_RUN
  1,506 (z3-equivalent under some map, gloss check pending), UNPARSEABLE 188, NO_OUTPUT 199; no CORRECT class yet -> AUROC
  NOT_TESTABLE; metadata_label_binary_search_provisional (ERROR_CERT vs MAPPED) is TESTABLE (all 759/1,506; untouched 636/1,175)
  with audited contamination ~13% each side. Metadata: seen_iter3 (454 rows; untouched subset 2,198 is primary), map_certificate,
  gloss_pairs, certificate counts, strata (template, clause_type, word_tercile, prompt_variant). Seal sha256 9609ebbb... (all),
  b364a49a... (untouched). (2) gloss_gate_items: 840 known-answer (symbol use, meaning) items, 7 classes x 120, halves A/B;
  checker verdicts pending. (3) sig_soundness_replay: 4,280 = 2,140 SIG rows x {nonce, synonym} renames with known pure-z3
  labels: false ERROR_CERT on known-CORRECT 0/1,595, identity map recovery 100%, known-ERROR rescue by non-identity maps 9-10%
  (what the gloss check must stop), oracle-checker ceiling recall 1.00 / false-CORRECT 0.00. Executor (non-blind) audit: ERROR_CERT
  precision 0.867 [0.76,0.93] (out-of-family faithful forms: disjunctive split, one predicate with two constants, exists-for-constant,
  in-name negation); MAPPED faithful 0.867. Old iter-3 tier-A labels: 34/34 CORRECT are MAPPED; 297/420 old ERROR are MAPPED,
  17/20 hand-checked are old aligner false errors. Reusable functions in src/freelab.py (exhaustive_map_label, equivalent_modulo_vocab_exhaustive,
  gloss_decision); src/resume_gloss.py runs gate -> FREE gloss -> final labels/seal -> SIG e2e -> Sonnet-5 audit (~$1.8) once
  budget is available. See dataset_card.md, deviations.json.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5
out_expected_files:
- data.py
- full_data_out.json
- preview_data_out.json
- mini_data_out.json
- reproducibility.md
out_demo_files:
- path: data.py
  description: Dataset fetching/generation script
</artifact_info>

<github_repo>
Repo URL: https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic
Raw data URL: https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_An1uy2kF2SjZ/round-4/dataset-5/demo/mini_demo_data.json

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
GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_An1uy2kF2SjZ/round-4/dataset-5/demo/mini_demo_data.json"
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
To test-run the notebook in a clean environment (simulating Colab), use the disposable venv at `/tmp/aii_nb_test_envs/art_Ia_FT284H33j-125d92329bed`. It is on this machine's local disk, outside your workspace, which is on a slow network volume: never create a venv inside your workspace.
```bash
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_Ia_FT284H33j-125d92329bed
UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_Ia_FT284H33j-125d92329bed/bin/python jupyter ipykernel
/tmp/aii_nb_test_envs/art_Ia_FT284H33j-125d92329bed/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb
```
The timeout is set to <max_notebook_total_runtime>. The entire notebook must finish within this time.
`UV_VENV_CLEAR=1` recreates the venv empty at the start of every test, so each test starts clean. Do NOT delete it yourself: the pipeline removes it after you finish. If you run a test in the background, wait for its result before starting the next test.

What happens: the venv starts with only pip, jupyter and ipykernel. When the notebook's install cell runs, `google.colab` is NOT in sys.modules, so ALL packages get installed — non-Colab packages unconditionally, and Colab packages (numpy, pandas, etc.) at Colab's exact versions via the guard block. The result mirrors Colab's environment as closely as possible. If a cell fails, fix the notebook and re-run.
</test_environment>

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.


<todos>
TODO 1. Read and STRICTLY follow these skills: aii-colab, aii-long-running-tasks.
TODO 2. Read demo file and relevant preview_* files (preview only). Understand script structure: imports, setup, processing, output. Identify ALL tunable parameters (iterations, epochs, n_samples, hidden_size, batch_size, etc.) — these go in the config cell.
TODO 3. Create `mini_demo_data.json`: curated subset from at most ONE dataset (no more than 100 diverse examples). CRITICAL: do NOT read/grep full output file — may crash. Use `head -c 5000` or stream first entries with Python to pick examples.
TODO 4. Create `code_demo.ipynb` via NotebookEdit following <notebook_structure>. Set ALL config parameters to ABSOLUTE MINIMUM values — the smallest that produce any output (e.g. 1 iteration, 2 samples, smallest array sizes). Test-run using <test_environment>. Fix all errors until it passes.
TODO 5. GRADUALLY SCALE (but don't overdo it): increase config params step by step (e.g. ~2x each round). After each increase: test-run, record runtime, fix errors. STOP SCALING as soon as results look meaningful — a working small-scale demo beats a failed large-scale one. If full original params fit within <max_notebook_total_runtime> (10% margin), use them. Otherwise keep whatever works and comment out the true original values. Do NOT spend more than 2-3 scaling rounds.
TODO 6. Verify: (1) code_demo.ipynb contains GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_An1uy2kF2SjZ/round-4/dataset-5/demo/mini_demo_data.json" exactly, (2) mini_demo_data.json exists, (3) uses GitHub URL pattern not just open('mini_demo_data.json').
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

### [3] HUMAN-USER prompt · 2026-09-25 16:37:34 UTC

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

### [4] TOOL CALL — Skill · 2026-09-25 16:37:38 UTC

```
aii-colab
```

### [5] TOOL RESULT — Skill · 2026-09-25 16:37:38 UTC

```
{"success": true, "commandName": "aii-colab"}
```

### [6] TOOL CALL — Skill · 2026-09-25 16:37:38 UTC

```
aii-long-running-tasks
```

### [7] TOOL RESULT — Skill · 2026-09-25 16:37:38 UTC

```
{"success": true, "commandName": "aii-long-running-tasks"}
```

### [8] TOOL CALL — Bash · 2026-09-25 16:37:42 UTC

```
A=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5; ls -la $A $A/src; wc -l $A/data.py $A/src/*.py; ls -la; ls .aii
```

### [9] TOOL RESULT — Bash · 2026-09-25 16:37:42 UTC

```
{"stdout": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5:\ntotal 37062\ndrwxr-xr-x 11 root root  2009731 Sep 24 10:50 .\ndrwxr-xr-x  7 root root  2038559 Sep 24 07:07 ..\ndrwxr-xr-x  2 root root    72500 Sep 24 07:55 .aii\n-rw-------  1 root root       54 Sep 24 07:08 .aii_claude_session.json\n-rw-r--r--  1 root root     1526 Sep 24 07:28 .aii_cost_ledger.jsonl\n-rw-------  1 root root     8646 Sep 24 07:55 .aii_worker_result.json\n-rw-r--r--  1 root root  2425895 Sep 24 07:55 .repl_agent.ptylog\n-rw-r--r--  1 root root     3026 Sep 24 07:54 .terminal_claude_agent_struct_out.json\n-rw-r--r--  1 root root     7886 Sep 24 07:53 README.md\n-rw-r--r--  1 root root     2054 Sep 24 07:12 VENDOR_SHA256.json\n-rw-r--r--  1 root root      819 Sep 24 07:45 cost_ledger.jsonl\n-rw-r--r--  1 root root     3714 Sep 24 07:53 data.py\n-rw-r--r--  1 root root    10436 Sep 24 07:46 dataset_card.md\n-rw-r--r--  1 root root     4460 Sep 24 07:36 deviations.json\n-rw-r--r--  1 root root 20238149 Sep 24 07:51 full_data_out.json\ndrwxr-xr-x  2 root root  1014830 Sep 24 07:48 logs\n-rw-r--r--  1 root root    25038 Sep 24 07:51 mini_data_out.json\n-rw-r--r--  1 root root    12063 Sep 24 07:25 prereg_freelab.json\n-rw-r--r--  1 root root       86 Sep 24 07:25 prereg_freelab.sha256\n-rw-r--r--  1 root root    11204 Sep 24 07:22 prereg_freelab_v1.json\n-rw-r--r--  1 root root       89 Sep 24 07:25 prereg_freelab_v1.sha256\n-rw-r--r--  1 root root    15836 Sep 24 07:51 preview_data_out.json\ndrwxr-xr-x  2 root root  1000110 Sep 24 07:22 prompts\n-rw-r--r--  1 root root      781 Sep 24 07:53 pyproject.toml\n-rw-r--r--  1 root root       27 Sep 24 07:20 pytest.ini\n-rw-r--r--  1 root root     8805 Sep 24 07:53 reproducibility.md\ndrwxr-xr-x  2 root root  2004356 Sep 24 07:46 results\ndrwxr-xr-x  2 root root  1014457 Sep 24 10:50 src\ndrwxr-xr-x  3 root root  2002457 Sep 24 07:50 temp\ndrwxr-xr-x  2 root root  1001128 Sep 24 10:50 tests\ndrwxr-xr-x  2 root root  1002841 Sep 24 10:50 vendor\ndrwxr-xr-x  2 root root  2000711 Sep 24 07:46 work\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src:\ntotal 3102\ndrwxr-xr-x  2 root root 1014457 Sep 24 10:50 .\ndrwxr-xr-x 11 root root 2009731 Sep 24 10:50 ..\n-rw-r--r--  1 root root    9766 Sep 24 07:37 assemble_labels.py\n-rw-r--r--  1 root root    6169 Sep 24 07:43 build_output.py\n-rw-r--r--  1 root root    2436 Sep 24 07:20 common.py\n-rw-r--r--  1 root root   37862 Sep 24 07:32 freelab.py\n-rw-r--r--  1 root root   12832 Sep 24 07:31 gate.py\n-rw-r--r--  1 root root    8622 Sep 24 07:30 gloss.py\n-rw-r--r--  1 root root    4014 Sep 24 07:28 hf_survey.py\n-rw-r--r--  1 root root    9645 Sep 24 07:20 inputs.py\n-rw-r--r--  1 root root    5518 Sep 24 07:37 post_seal_join.py\n-rw-r--r--  1 root root   12216 Sep 24 07:25 prereg.py\n-rw-r--r--  1 root root    2308 Sep 24 07:45 provisional_view.py\n-rw-r--r--  1 root root   12023 Sep 24 07:42 resume_gloss.py\n-rw-r--r--  1 root root    5114 Sep 24 07:24 run_search.py\n-rw-r--r--  1 root root    4296 Sep 24 07:34 sig_rename.py\n-rw-r--r--  1 root root   11806 Sep 24 07:43 soundness.py\n-rw-r--r--  1 root root    3419 Sep 24 07:12 vendor_copy.py\n    67 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/data.py\n   177 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/assemble_labels.py\n    98 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/build_output.py\n    70 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/common.py\n   838 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/freelab.py\n   279 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/gate.py\n   205 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/gloss.py\n    83 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/hf_survey.py\n   191 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/inputs.py\n   112 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/post_seal_join.py\n   141 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/prereg.py\n    42 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/provisional_view.py\n   247 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/resume_gloss.py\n   117 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/run_search.py\n    96 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/sig_rename.py\n   202 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/soundness.py\n    69 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/vendor_copy.py\n  3034 total\ntotal 2966\ndrwxr-xr-x 3 root root 1003141 Sep 25 16:37 .\ndrwxr-xr-x 7 root root 2000132 Sep 25 16:37 ..\ndrwxr-xr-x 2 root root       1 Sep 25 16:36 .aii\n-rw------- 1 root root      54 Sep 25 16:37 .aii_claude_session.json\n-rw-r--r-- 1 root root   32336 Sep 25 16:37 .repl_agent.ptylog", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [10] TOOL CALL — Bash · 2026-09-25 16:37:44 UTC

```
A=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5; cat $A/data.py; head -c 6000 $A/preview_data_out.json
```

### [11] TOOL RESULT — Bash · 2026-09-25 16:37:44 UTC

```
{"stdout": "# /// script\n# requires-python = \">=3.12\"\n# dependencies = [\"loguru==0.7.3\"]\n# ///\n\"\"\"Build full_data_out.json (exp_sel_data_out) from the three chosen datasets, one example per data row:\n  rcomp_free_labels      2,652 FREE rows, name-free labels (search-only, sealed; see dataset_card.md)\n  gloss_gate_items         840 known-answer (symbol use, meaning) items\n  sig_soundness_replay   4,280 renamed SIG rows with known pure-z3 labels\nAll three are derived from this run's R_COMP artifacts by src/*.py (results/*.jsonl, work/sentences.json).\nusage: uv run data.py\n\"\"\"\nfrom __future__ import annotations\n\nimport json\nimport sys\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parent\nsys.path.insert(0, str(ROOT / \"src\"))\nsys.path.insert(0, str(ROOT / \"vendor\"))\n\nfrom loguru import logger  # noqa: E402\n\nlogger.remove()\nlogger.add(sys.stdout, level=\"INFO\", format=\"{time:HH:mm:ss}|{level:<7}|{message}\")\n(ROOT / \"logs\").mkdir(exist_ok=True)\nlogger.add(ROOT / \"logs\" / \"data.log\", rotation=\"30 MB\", level=\"DEBUG\")\n\nSELECTED = [\"rcomp_free_labels\", \"gloss_gate_items\", \"sig_soundness_replay\"]\n\n\n@logger.catch(reraise=True)\ndef main() -> None:\n    import build_output as B  # run-derived plan groups (reads results/*.jsonl, work/sentences.json)\n    groups = [B.free_group(), B.gate_group(), B.sig_group()]\n    for g in groups:\n        assert g[\"examples\"], g[\"dataset\"]\n        for e in g[\"examples\"]:\n            assert isinstance(e[\"input\"], str) and isinstance(e[\"output\"], str), g[\"dataset\"]\n            assert not ({\"split\", \"dataset\", \"context\"} & set(e)), g[\"dataset\"]\n    seal = json.loads((ROOT / \"results\" / \"seal.json\").read_text())[\"seals\"][-1]\n    t = json.loads((ROOT / \"results\" / \"testability_FREE_v2.json\").read_text())\n    out = {\"metadata\": {\n        \"artifact\": \"T7b name-free labels for free-vocabulary rule translations (run_u75jRHUss0zo, iter 4, gen_art_dataset_5)\",\n        \"workspace\": str(ROOT),\n        \"selection\": (\"the three plan groups (chosen as best 3 of 6 standardised candidates; folio / malls_test / \"\n                      \"logicnli_test were context only: no multi-system candidates, ~36-39% wrong gold, or no FOL; their \"\n                      \"standardised record is temp/candidates_data_out.json)\"),\n        \"label_mode\": seal[\"mode\"],\n        \"status_note\": (\"SEARCH-ONLY labels: the paid gloss step could not run (deviation D9: run OpenRouter budget \"\n                        \"exhausted before this artifact's first call; re-probed at packaging, still HTTP 403). ERROR_CERT is \"\n                        \"final and certificate-backed; MAPPED rows are UNRESOLVED_GLOSS_NOT_RUN until src/resume_gloss.py \"\n                        \"runs. metadata_label_binary_search_provisional (ERROR vs MAPPED) is a provisional view with audited \"\n                        \"contamination (results/soundness_audit.json).\"),\n        \"seal_all_rows_sha256\": seal[\"label_vector_sha256_all_rows\"],\n        \"seal_untouched_sha256\": seal.get(\"label_vector_sha256_untouched\"),\n        \"prereg_sha256\": seal[\"prereg_sha256\"],\n        \"testability_all_rows\": {k: t[\"all_rows\"][k] for k in (\"n_ERROR\", \"n_CORRECT\", \"TESTABLE\", \"label_counts\")},\n        \"testability_untouched\": {k: t[\"untouched_subset\"][k] for k in (\"n_ERROR\", \"n_CORRECT\", \"TESTABLE\", \"label_counts\")},\n        \"provisional_view_testable\": {k: t[\"search_provisional_view\"][k][\"TESTABLE\"] for k in (\"all_rows\", \"untouched_subset\")},\n    }, \"datasets\": [g for g in groups if g[\"dataset\"] in SELECTED]}\n    (ROOT / \"full_data_out.json\").write_text(json.dumps(out, ensure_ascii=False))\n    logger.info(f\"full_data_out.json: {[(g['dataset'], len(g['examples'])) for g in out['datasets']]}\")\n\n\nif __name__ == \"__main__\":\n    main()\n{\n  \"metadata\": {\n    \"artifact\": \"T7b name-free labels for free-vocabulary rule translations (run_u75jRHUss0zo, iter 4, gen_art_dataset_5)\",\n    \"workspace\": \"/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5\",\n    \"selection\": \"the three plan groups (chosen as best 3 of 6 standardised candidates; folio / malls_test / logicnli_test were context only: no multi-system candidates, ~36-39% wrong gold, or no FOL; their standardise...\",\n    \"label_mode\": \"search_only\",\n    \"status_note\": \"SEARCH-ONLY labels: the paid gloss step could not run (deviation D9: run OpenRouter budget exhausted before this artifact's first call; re-probed at packaging, still HTTP 403). ERROR_CERT is final and...\",\n    \"seal_all_rows_sha256\": \"9609ebbb725832c467389e9d04b6334ca906ba10d400e7a7dccd976d39ebe3dd\",\n    \"seal_untouched_sha256\": \"b364a49a8e21835de660689097b462212f3f72b96ef66b437a14cc60e039f500\",\n    \"prereg_sha256\": \"b081c39991f52da2f419a6cefe56da48705d8abddf292d0faa89cec0b393a799\",\n    \"testability_all_rows\": {\n      \"n_ERROR\": 759,\n      \"n_CORRECT\": 0,\n      \"TESTABLE\": false,\n      \"label_counts\": {\n        \"ERROR_CERT\": 759,\n        \"UNRESOLVED_GLOSS_NOT_RUN\": 1506,\n        \"UNPARSEABLE\": 188,\n        \"NO_OUTPUT\": 199\n      }\n    },\n    \"testability_untouched\": {\n      \"n_ERROR\": 636,\n      \"n_CORRECT\": 0,\n      \"TESTABLE\": false,\n      \"label_counts\": {\n        \"ERROR_CERT\": 636,\n        \"UNRESOLVED_GLOSS_NOT_RUN\": 1175,\n        \"UNPARSEABLE\": 188,\n        \"NO_OUTPUT\": 199\n      }\n    },\n    \"provisional_view_testable\": {\n      \"all_rows\": true,\n      \"untouched_subset\": true\n    }\n  },\n  \"datasets\": [\n    {\n      \"dataset\": \"rcomp_free_labels\",\n      \"examples\": [\n        {\n          \"input\": \"{\\\"text\\\": \\\"Each legislator who is at Board Game night, who visits a coffee shop regularly, and who can distinguish the taste of different condiments is Emily's friend, except if the legislator is an el...\",\n          \"output\": \"ERROR_CERT\",\n          \"metadata_row_key\": \"a81d2862772cd744|FREE|G1|fewshot_v1\",\n          \"metadata_item_id\": \"a81d2862772cd744\",\n          \"metadata_sentence_id\": \"001a7f0caf5a\",\n          \"metadata_template_id\": \"T1\",\n          \"metadata_clause_type\": \"unless\",\n          \"metadata_words\": 34,\n          \"metadata_word_tercile\": \"W2\",\n          \"metadata_nconds_weak\": 5,\n          \"metadata_negated_condition\": null,\n          \"metadata_nested\": false,\n          \"metadata_label_binary\": \"ERROR\",\n          \"metadata_label_binary_search_provisional\": \"ERROR\",\n          \"metadata_label_source\": \"exhaustive_map_v1\",\n          \"metadata_search_status\": \"ERROR_CERT\",\n          \"metadata_matched_reading\": null,\n          \"metadata_map_certificate\": null,\n          \"metadata_n_maps_enumerated\": 0,\n          \"metadata_n_maps_fingerprint_pass\": 0,\n          \"metadata_n_equiv_maps\": 0,\n          \"metadata_n_equiv_map_orbits\": 0,\n          \"metadata_nonequiv_certificate_type_counts\": {\n            \"count_prune_subtree\": 291,\n            \"no_polarity_compatible_target\": 10\n          },\n          \"metadata_gloss_pairs\": null,\n          \"metadata_gloss_decision\": null,\n          \"metadata_unresolved_reason\": null,\n          \"metadata_irrelevant_symbols\": [],\n          \"metadata_search_secs\": 0.06,\n          \"metadata_seen_iter3\": false,\n          \"metadata_old_label_iter3\": \"UNRESOLVED\",\n          \"metadata_fold\": \"RCOMP_FREE\"\n        },\n        {\n          \"input\": \"{\\\"text\\\": \\\"Each legislator who is at Board Game night, who visits a coffee shop regularly, and who can distinguish the taste of different condiments is Emily's friend, except if the legislator is an el...\",\n          \"output\": \"UNRESOLVED_GLOSS_NOT_RUN\",\n          \"metadata_row_key\": \"94bcb373f89b6d9a|FREE|G1b|fewshot_v1\",\n          \"metadata_item_id\": \"94bcb373f89b6d9a\",\n          \"metadata_sentence_id\": \"001a7f0caf5a\",\n          \"metadata_template_id\": \"T1\",\n          \"metadata_clause_type\": \"unless\",\n          \"metadata_words\": 34,\n          \"metadata_word_tercile\": \"W2\",\n          \"metadata_nconds_weak\": 5,\n          \"metadata_negated_condition\": null,\n          \"metadata_nested\": false,\n          \"metadata_label_binary\": \"EXCLUDED\",\n          \"metadata_label_binary_search_provisional\": \"MAPPED\",\n          \"metadata_label_source\": \"exhaustive_map_v1\",\n          \"metadata_search_status\": \"MAPPED\",\n          \"metadata_matched_reading\": \"strong\",\n          \"metadata_map_certificate\": {\n            \"status\": \"z3_equivalent_map_not_gloss_checked\",\n            \"reading\": \"strong\",\n            \"map\": [\n              \"Attends(x, boardGameNight) => At(x, boardGameNight)\",\n              \"CanDistinguish(x, condiments) => Can(x, distinguishTheTasteOfDifferentCondiments)\",\n              \"ElectedOfficial(x) => ElectedOfficial(x)\"\n            ],\n            \"bridges\": [\n              \"B2\"\n            ]\n          },\n          \"metadata_n_maps_enumerated\": 48,\n          \"metadata_n_maps_fingerprint_pass\": 48,\n          \"metadata_n_equiv_maps\": 48,\n          \"metadata_n_equiv_map_orbits\": 2,\n          \"metadata_nonequiv_certificate_type_counts\": {\n            \"count_prune_subtree\": 360\n          },\n          \"metadata_gloss_pairs\": [\n            {\n              \"cand_atom\": \"Attends(x, boardGameNight)\",\n              \"meaning\": \"x is at Board Game night\",\n              \"haiku\": null,\n              \"qwen\": null\n            },\n            {\n              \"cand_atom\": \"CanDistinguish(x, condiments)\",\n              \"meaning\": \"x can distinguish the taste of different condiments\",\n              \"haiku\": null,\n              \"qwen\": null\n            },\n            {\n              \"cand_atom\": \"ElectedOfficial(x)\",\n              \"meaning\": \"x is an elected official\",\n              \"haiku\": null,\n              \"qwen\": null\n            }\n          ],\n          \"metadata_gloss_decision\": null,\n          \"metadata_unresolved_reason\": \"gloss check not run (D9: API budget exhausted)\",\n          \"metadata_irrelevant_symb", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [12] TOOL CALL — Bash · 2026-09-25 16:37:48 UTC

```
A=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5; cat $A/src/build_output.py; cat $A/src/common.py; ls -la $A/vendor $A/results; cat $A/pyproject.toml
```

### [13] TOOL RESULT — Bash · 2026-09-25 16:37:48 UTC

```
{"stdout": "#!/usr/bin/env python3\n\"\"\"STEP I: full_data_out.json (exp_sel_data_out) with three groups:\n  rcomp_free_labels     one row per FREE generation record (2,652), label = name-free label (search-only now, D9)\n  gloss_gate_items      840 known-answer (symbol use, meaning) items, 7 classes, halves A/B\n  sig_soundness_replay  4,280 rows = 2,140 SIG rows x {nonce, synonym} renames, output = known pure-z3 SIG label\n\"\"\"\nfrom __future__ import annotations\n\nimport json\n\nfrom common import RES, ROOT, WORK, load_jsonl, setup_logger\n\nlogger = setup_logger(\"build_output\")\n\n\ndef md(d: dict) -> dict:\n    return {f\"metadata_{k}\": v for k, v in d.items()}\n\n\ndef free_group() -> dict:\n    rows = load_jsonl(RES / \"free_labels_v2.jsonl\")\n    ex = []\n    for r in rows:\n        inp = {\"text\": r[\"text\"], \"candidate_fol\": r[\"candidate_fol\"], \"system\": r[\"system\"], \"family\": r[\"family\"],\n               \"slot\": r[\"slot\"], \"prompt_variant\": r[\"prompt_variant\"], \"condition\": \"FREE\", \"template_id\": r[\"template_id\"]}\n        search_bin = {\"ERROR_CERT\": \"ERROR\", \"UNRESOLVED_GLOSS_NOT_RUN\": \"MAPPED\"}.get(r[\"label\"], \"EXCLUDED\")\n        meta = {\n            \"row_key\": r[\"row_key\"], \"item_id\": r[\"item_id\"], \"sentence_id\": r[\"sentence_id\"], \"template_id\": r[\"template_id\"],\n            \"clause_type\": r[\"clause_type\"], \"words\": r[\"words\"], \"word_tercile\": r[\"word_tercile\"],\n            \"nconds_weak\": r[\"nconds_weak\"], \"negated_condition\": r[\"negated_condition\"], \"nested\": r[\"nested\"],\n            \"label_binary\": r[\"label_binary\"], \"label_binary_search_provisional\": search_bin,\n            \"label_source\": r[\"label_source\"], \"search_status\": r.get(\"search_status\"),\n            \"matched_reading\": r.get(\"matched_reading\") or r.get(\"matched_reading_search\"),\n            \"map_certificate\": r.get(\"map_certificate\"),\n            \"n_maps_enumerated\": r.get(\"n_maps_enumerated\"), \"n_maps_fingerprint_pass\": r.get(\"n_maps_fingerprint_pass\"),\n            \"n_equiv_maps\": r.get(\"n_equiv_maps\"), \"n_equiv_map_orbits\": r.get(\"n_equiv_map_orbits\"),\n            \"nonequiv_certificate_type_counts\": r.get(\"nonequiv_certificate_type_counts\"),\n            \"gloss_pairs\": r.get(\"gloss_pairs\"), \"gloss_decision\": r.get(\"gloss_decision\"),\n            \"unresolved_reason\": r.get(\"unresolved_reason\"), \"irrelevant_symbols\": r.get(\"irrelevant_symbols\"),\n            \"search_secs\": r.get(\"search_secs\"), \"seen_iter3\": r.get(\"seen_iter3\"),\n            \"old_label_iter3\": r.get(\"old_label_iter3\"), \"fold\": \"RCOMP_FREE\"}\n        ex.append({\"input\": json.dumps(inp, ensure_ascii=False), \"output\": r[\"label\"], **md(meta)})\n    return {\"dataset\": \"rcomp_free_labels\", \"examples\": ex}\n\n\ndef gate_group() -> dict:\n    items = json.loads((RES / \"gate_items.json\").read_text())\n    ex = []\n    for i in items:\n        inp = {\"sentence\": i[\"sentence\"], \"candidate_atom\": i[\"candidate_atom\"], \"proposed_meaning\": i[\"proposed_meaning\"]}\n        meta = {\"item_id\": i[\"item_id\"], \"class\": i[\"class\"], \"half\": i[\"half\"], \"sentence_id\": i[\"sentence_id\"],\n                \"template_id\": i[\"template_id\"], \"note\": i[\"note\"], \"prompt_version\": \"gloss_v1\",\n                \"haiku_verdict\": i.get(\"haiku_gloss_v1\"), \"qwen_verdict\": i.get(\"qwen_gloss_v1\"), \"fold\": \"GLOSS_GATE\"}\n        ex.append({\"input\": json.dumps(inp, ensure_ascii=False), \"output\": i[\"gold\"], **md(meta)})\n    return {\"dataset\": \"gloss_gate_items\", \"examples\": ex}\n\n\ndef sig_group() -> dict:\n    sents = json.loads((WORK / \"sentences.json\").read_text())\n    rows = load_jsonl(RES / \"sig_replay_rows.jsonl\")\n    ex = []\n    for r in rows:\n        inp = {\"text\": sents[r[\"sentence_id\"]][\"text\"], \"candidate_fol\": r[\"renamed_fol\"], \"rename\": r[\"rename\"],\n               \"template_id\": r[\"template_id\"]}\n        meta = {k: r[k] for k in (\"row_key\", \"sentence_id\", \"slot\", \"template_id\", \"sig_matched_reading\", \"canon_fol\",\n                                  \"search_status\", \"identity_map_found\", \"non_identity_map_found\", \"n_equiv_maps\",\n                                  \"n_equiv_map_orbits\", \"n_maps_enumerated\", \"nonequiv_certificate_type_counts\",\n                                  \"oracle_end_to_end_label\", \"in_e2e_gloss_subsample_300\", \"e2e_gloss_label\")}\n        meta[\"map_equiv_found\"] = r[\"search_status\"] in (\"MAPPED\", \"READING_CHOICE\")\n        meta[\"fold\"] = f\"SIG_REPLAY_{r['rename'].upper()}\"\n        ex.append({\"input\": json.dumps(inp, ensure_ascii=False), \"output\": r[\"sig_label\"], **md(meta)})\n    return {\"dataset\": \"sig_soundness_replay\", \"examples\": ex}\n\n\ndef main() -> None:\n    seal = json.loads((RES / \"seal.json\").read_text())[\"seals\"]\n    t = json.loads((RES / \"testability_FREE_v2.json\").read_text())\n    out = {\"metadata\": {\n        \"artifact\": \"T7b name-free labels for free-vocabulary rule translations (run_u75jRHUss0zo, iter 4, gen_art_dataset_5)\",\n        \"workspace\": str(ROOT),\n        \"label_mode\": seal[-1][\"mode\"],\n        \"status_note\": (\"SEARCH-ONLY labels: the paid gloss step could not run (deviation D9: run OpenRouter budget \"\n                        \"exhausted before this artifact's first call). ERROR_CERT is final and certificate-backed; MAPPED rows \"\n                        \"are UNRESOLVED_GLOSS_NOT_RUN until src/resume_gloss.py runs. metadata_label_binary_search_provisional \"\n                        \"(ERROR vs MAPPED) is a provisional view with audited contamination (see results/soundness_audit.json).\"),\n        \"seal_all_rows_sha256\": seal[-1][\"label_vector_sha256_all_rows\"],\n        \"seal_untouched_sha256\": seal[-1].get(\"label_vector_sha256_untouched\"),\n        \"prereg_sha256\": seal[-1][\"prereg_sha256\"],\n        \"testability_all_rows\": {k: t[\"all_rows\"][k] for k in (\"n_ERROR\", \"n_CORRECT\", \"TESTABLE\", \"label_counts\")},\n        \"testability_untouched\": {k: t[\"untouched_subset\"][k] for k in (\"n_ERROR\", \"n_CORRECT\", \"TESTABLE\", \"label_counts\")}\n        if isinstance(t.get(\"untouched_subset\"), dict) else None,\n    }, \"datasets\": [free_group(), gate_group(), sig_group()]}\n    (ROOT / \"full_data_out.json\").write_text(json.dumps(out, ensure_ascii=False))\n    logger.info(f\"full_data_out.json: {[(d['dataset'], len(d['examples'])) for d in out['datasets']]}\")\n\n\nif __name__ == \"__main__\":\n    main()\n\"\"\"Shared paths, hashing and JSON helpers for the FREE name-free labeller (no metric, evaluator-model or aligner code here).\"\"\"\nfrom __future__ import annotations\n\nimport hashlib\nimport json\nimport re\nimport sys\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nfor _p in (ROOT / \"vendor\", ROOT / \"src\"):\n    if str(_p) not in sys.path:\n        sys.path.insert(0, str(_p))\nsys.setrecursionlimit(10000)\n\nRUN = Path(\"/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop\")\nE7 = RUN / \"iter_3/gen_art/gen_art_experiment_7\"\nD3 = RUN / \"iter_2/gen_art/gen_art_dataset_3\"\nGEN_FREE = E7 / \"rcomp/raw/generations.jsonl\"          # FREE raw generations: no scores, no labels\nSENTS = E7 / \"rcomp/work/rcomp_sentences.json\"\nD3_FULL = D3 / \"full_data_out.json\"\nLEXICON = D3 / \"lexicon.json\"\nSIG_LABELS = E7 / \"results/sig_labels.jsonl\"            # SIG labels only (pure z3), no scores\nOLD_CANDIDATES = E7 / \"results/rcomp_candidates.jsonl\"  # opened ONLY in STEP H (post-seal) via a whitelist loader\nNLTK_DATA = E7 / \"data/nltk_data\"\nRES = ROOT / \"results\"\nWORK = ROOT / \"work\"\nLOGS = ROOT / \"logs\"\nfor _d in (RES, WORK, LOGS):\n    _d.mkdir(exist_ok=True)\n\n\ndef sha1(s: str) -> str:\n    return hashlib.sha1(s.encode()).hexdigest()\n\n\ndef sha256_bytes(b: bytes) -> str:\n    return hashlib.sha256(b).hexdigest()\n\n\ndef sha256_file(p: Path) -> str:\n    return hashlib.sha256(Path(p).read_bytes()).hexdigest()\n\n\ndef norm_text(s: str) -> str:\n    \"\"\"Dataset E's select_sentences.norm (verbatim logic) used in the item_id recipe.\"\"\"\n    s = s.lower().replace(\"’\", \"'\").replace(\"‘\", \"'\").replace(\"“\", '\"').replace(\"”\", '\"')\n    s = re.sub(r\"[^a-z0-9 ]\", \" \", s)\n    return re.sub(r\"\\s+\", \" \", s).strip()\n\n\ndef item_id(system: str, text: str, raw: str | None) -> str:\n    \"\"\"exp 7 / dataset 3 recipe: sha1(system | norm(text) | raw_output)[:16] (raw None -> '').\"\"\"\n    return sha1(system + \"|\" + norm_text(text) + \"|\" + (raw or \"\"))[:16]\n\n\ndef load_jsonl(p: Path) -> list[dict]:\n    return [json.loads(l) for l in Path(p).read_text().splitlines() if l.strip()]\n\n\ndef dump(p: Path, obj) -> None:\n    Path(p).write_text(json.dumps(obj, indent=1, ensure_ascii=False))\n\n\ndef setup_logger(name: str):\n    from loguru import logger\n    logger.remove()\n    logger.add(sys.stdout, level=\"INFO\", format=\"{time:HH:mm:ss}|{level:<7}|{message}\")\n    logger.add(LOGS / f\"{name}.log\", rotation=\"30 MB\", level=\"DEBUG\")\n    return logger\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/results:\ntotal 48538\ndrwxr-xr-x  2 root root  2004356 Sep 24 07:46 .\ndrwxr-xr-x 11 root root  2009731 Sep 24 10:50 ..\n-rw-r--r--  1 root root    10436 Sep 24 07:46 dataset_card.md\n-rw-r--r--  1 root root  8143542 Sep 24 07:37 free_labels_v2.jsonl\n-rw-r--r--  1 root root   427414 Sep 24 07:32 gate_items.json\n-rw-r--r--  1 root root      303 Sep 24 07:45 gate_report.json\n-rw-r--r--  1 root root     1106 Sep 24 07:13 input_counts.json\n-rw-r--r--  1 root root 17748257 Sep 24 07:35 map_search.jsonl\n-rw-r--r--  1 root root    23765 Sep 24 07:37 old_label_agreement.json\n-rw-r--r--  1 root root     3623 Sep 24 07:37 seal.json\n-rw-r--r--  1 root root    31504 Sep 24 07:13 shape_census.json\n-rw-r--r--  1 root root  7459154 Sep 24 07:37 sig_replay_nonce.jsonl\n-rw-r--r--  1 root root  3820323 Sep 24 07:43 sig_replay_rows.jsonl\n-rw-r--r--  1 root root  7937822 Sep 24 07:39 sig_replay_syn.jsonl\n-rw-r--r--  1 root root    23836 Sep 24 07:43 soundness_audit.json\n-rw-r--r--  1 root root    52908 Sep 24 07:45 testability_FREE_v2.json\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/vendor:\ntotal 2973\ndrwxr-xr-x  2 root root 1002841 Sep 24 10:50 .\ndrwxr-xr-x 11 root root 2009731 Sep 24 10:50 ..\n-rw-r--r--  1 root root       0 Sep 24 07:12 __init__.py\n-rw-r--r--  1 root root    9244 Sep 24 07:12 fol.py\n-rw-r--r--  1 root root    4916 Sep 24 07:12 fol_triage_min.py\n-rw-r--r--  1 root root    1510 Sep 24 07:12 label_sig_min.py\n-rw-r--r--  1 root root    3557 Sep 24 07:12 perturb_min.py\n-rw-r--r--  1 root root    1584 Sep 24 07:12 repair_census_min.py\n-rw-r--r--  1 root root    1412 Sep 24 07:12 sig_prompt_min.py\n-rw-r--r--  1 root root    6871 Sep 24 07:12 templates.py\n[project]\nname = \"freelab-u75j\"\nversion = \"0.1.0\"\ndescription = \"T7b: name-free (alignment-free) labels for free-vocabulary NL->FOL rule translations (run_u75jRHUss0zo iter 4, gen_art_dataset_5)\"\nrequires-python = \">=3.12\"\ndependencies = [\n    \"anyio==4.15.1\",\n    \"certifi==2026.7.22\",\n    \"click==8.5.0\",\n    \"cloudpickle==3.1.2\",\n    \"defusedxml==0.7.1\",\n    \"h11==0.16.0\",\n    \"httpcore==1.0.9\",\n    \"httpx==0.28.1\",\n    \"idna==3.20\",\n    \"iniconfig==2.3.0\",\n    \"joblib==1.6.0\",\n    \"loguru==0.7.3\",\n    \"nltk==3.10.3\",\n    \"numpy==2.5.3\",\n    \"packaging==26.3\",\n    \"pluggy==1.6.0\",\n    \"psutil==7.2.2\",\n    \"pygments==2.21.0\",\n    \"pytest==9.1.1\",\n    \"pyyaml==6.0.3\",\n    \"regex==2026.9.10\",\n    \"tqdm==4.70.1\",\n    \"typing-extensions==4.16.0\",\n    \"z3-solver==5.1.0.0\",\n]", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [14] TOOL CALL — Bash · 2026-09-25 16:37:54 UTC

```
A=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5; grep -n "^def \|^from\|^import\|^class " $A/src/freelab.py $A/src/run_search.py $A/vendor/fol.py $A/vendor/templates.py; sed -n 1,60p $A/src/run_search.py; ls -la $A/work
```

### [15] TOOL RESULT — Bash · 2026-09-25 16:37:54 UTC

```
{"stdout": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/freelab.py:30:from __future__ import annotations\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/freelab.py:32:import itertools\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/freelab.py:33:import re\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/freelab.py:34:import time\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/freelab.py:35:import zlib\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/freelab.py:36:from collections import Counter, defaultdict\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/freelab.py:37:from functools import lru_cache\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/freelab.py:39:import z3\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/freelab.py:41:from fol import mkpred, parse, preds, profile, to_z3, valid, U\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/freelab.py:42:from repair_census_min import atoms, bound_vars\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/freelab.py:55:def to_str(e) -> str:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/freelab.py:67:def name_tokens(n: str) -> list[str]:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/freelab.py:71:def negation_named(name: str) -> bool:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/freelab.py:77:def free_consts(e) -> set:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/freelab.py:93:def occurrences(e):\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/freelab.py:110:def conj_chains(e):\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/freelab.py:138:def rename_const(e, old: str, new: str, bv=frozenset()):\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/freelab.py:149:def z3_equiv(a, b, ms: int) -> bool | None:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/freelab.py:155:def z3_equiv_retry(a, b) -> bool | None:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/freelab.py:165:def _atom_val(i: int, name: str, args: tuple) -> bool:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/freelab.py:170:def _const_val(i: int, name: str) -> int:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/freelab.py:174:def dom_size(i: int) -> int:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/freelab.py:178:def ev(e, i: int, env: dict) -> bool:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/freelab.py:202:def fingerprint(e, n: int = N_FP) -> tuple:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/freelab.py:206:def first_mismatch(e, ref_fp: tuple) -> int | None:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/freelab.py:215:def analyse_symbols(e) -> dict:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/freelab.py:263:def unit_display(u: dict, subj: str = \"x\") -> str:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/freelab.py:269:class Reading:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/freelab.py:316:def unit_display_of_atom(a, units: dict) -> str | None:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/freelab.py:324:class Candidate:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/freelab.py:363:def _pol_ok(p, q) -> bool:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/freelab.py:370:def unit_options(key: str, cand: Candidate, rd: Reading) -> list[tuple]:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/freelab.py:391:def rel_options(key: str, cand: Candidate, rd: Reading) -> list[tuple]:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/freelab.py:403:def build_image(cand: Candidate, rd: Reading, assign: dict, cmap: dict):\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/freelab.py:442:def map_to_json(assign: dict, cmap: dict, cand: Candidate, rd: Reading) -> dict:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/freelab.py:462:def bridges_of(assign: dict, cand: Candidate, rd: Reading) -> list[str]:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/freelab.py:483:def search(cand: Candidate, rd: Reading, max_maps: int = MAX_MAPS, max_secs: float = MAX_SECS,\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/freelab.py:537:def _covers(opt) -> list[str]:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/freelab.py:545:def _dfs(i, syms, assign, used_units, used_rels, n_struct, need, consts, cand, rd, res, t0, max_maps, max_secs, keep):\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/freelab.py:591:def _leaf(assign, consts, cand, rd, res, t0, max_maps, max_secs, keep):\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/freelab.py:623:def _finish(res, t0):\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/freelab.py:631:def pair_items(m: dict, cand: Candidate, rd: Reading) -> list[tuple[str, str]]:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/freelab.py:685:def label_candidate(candidate_fol: str, readings: dict, glosses: dict | None = None, max_maps: int = MAX_MAPS,\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/freelab.py:700:def label_with(cand: Candidate, rds: dict, max_maps: int, max_secs: float, t0: float | None = None) -> dict:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/freelab.py:765:def gloss_decision(maps: list[dict], pairs_union: list, verdict: dict) -> tuple[str, int | None]:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/freelab.py:791:def exhaustive_map_label(candidate_fol: str, readings: dict, atoms: dict | None = None, glosses: dict | None = None,\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/freelab.py:818:def equivalent_modulo_vocab_exhaustive(a_fol: str, b_fol: str, max_maps: int = MAX_MAPS, max_secs: float = MAX_SECS\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/run_search.py:8:from __future__ import annotations\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/run_search.py:10:import argparse\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/run_search.py:11:import json\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/run_search.py:12:import multiprocessing as mp\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/run_search.py:13:import re\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/run_search.py:14:import resource\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/run_search.py:15:import time\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/run_search.py:16:from collections import defaultdict\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/run_search.py:17:from concurrent.futures import ProcessPoolExecutor, as_completed\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/run_search.py:19:from common import RES, WORK, load_jsonl, setup_logger, sha1\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/run_search.py:24:def class_key(sid: str, fol: str) -> str:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/run_search.py:28:def work_sentence(job: dict) -> list[dict]:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/run_search.py:57:def run(classes_by_sid: dict, sents: dict, outp, logger, limit: int | None, cap_mult: int = 1) -> None:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/src/run_search.py:91:def main() -> None:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/vendor/fol.py:7:import re\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/vendor/fol.py:8:import z3\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/vendor/fol.py:16:def tokenize(s: str) -> list[str]:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/vendor/fol.py:32:class Parser:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/vendor/fol.py:101:def parse(s: str):\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/vendor/fol.py:105:def preds(e, acc=None):\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/vendor/fol.py:122:def to_z3(e, env, P):\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/vendor/fol.py:141:def mkpred(name, n):\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/vendor/fol.py:146:def valid(c, ms=3000):\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/vendor/fol.py:154:def profile(e, ms=3000):\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/vendor/fol.py:173:def equivalent(e1, e2, ms=5000):\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/vendor/fol.py:179:def connectivity_flags(e):\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/vendor/fol.py:228:def prenex_blocks(e):\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/vendor/fol.py:241:def coupled_independent_vars(e):\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/vendor/fol.py:251:def token_profile(prof):\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/vendor/templates.py:14:from __future__ import annotations\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/vendor/templates.py:16:import re\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/vendor/templates.py:27:def lit(s: dict) -> str:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/vendor/templates.py:31:def cvp(s: dict) -> str:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/vendor/templates.py:35:def art(noun: str) -> str:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/vendor/templates.py:39:def conj(*xs: str) -> str:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/vendor/templates.py:43:def plural_vp(vp: str) -> str | None:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/vendor/templates.py:66:def fill(t: str, v: int, N: str, S: str, C: list[dict], Q: dict, X: dict | None, person: bool) -> dict:\n#!/usr/bin/env python3\n\"\"\"STEP C (and audit (i) search): exhaustive map search per unique (sentence, candidate) class, CPU only.\n\nusage: run_search.py free [--limit N]          -> results/map_search.jsonl       (FREE classes)\n       run_search.py sig --rename nonce|syn    -> results/sig_replay_{nonce,syn}.jsonl (renamed SIG classes)\nResumable (skips class keys already written). ProcessPoolExecutor(spawn), one task per sentence.\n\"\"\"\nfrom __future__ import annotations\n\nimport argparse\nimport json\nimport multiprocessing as mp\nimport re\nimport resource\nimport time\nfrom collections import defaultdict\nfrom concurrent.futures import ProcessPoolExecutor, as_completed\n\nfrom common import RES, WORK, load_jsonl, setup_logger, sha1\n\nNUM_WORKERS = 4\n\n\ndef class_key(sid: str, fol: str) -> str:\n    return sha1(sid + \"|\" + re.sub(r\"\\s+\", \"\", fol))[:16]\n\n\ndef work_sentence(job: dict) -> list[dict]:\n    import sys\n    sys.setrecursionlimit(10000)\n    import common  # noqa: F401  (paths)\n    import freelab as FL\n    s = job[\"sent\"]\n    rdfs = {\"weak\": s[\"reference_fol_weak\"], \"strong\": s[\"reference_fol_strong\"]}\n    if s.get(\"reading_converse\"):\n        rdfs[\"converse\"] = s[\"reading_converse\"]\n    rds = {k: FL.Reading(v, s[\"units\"]) for k, v in rdfs.items()}\n    out = []\n    for ck, fol in job[\"classes\"]:\n        t0 = time.time()\n        try:\n            cand = FL.Candidate(fol)\n        except (ValueError, IndexError, TypeError, KeyError, RecursionError) as ex:\n            out.append({\"class_key\": ck, \"sentence_id\": s[\"sentence_id\"], \"candidate_fol\": fol, \"status\": \"UNPARSEABLE\",\n                        \"error\": str(ex)[:160]})\n            continue\n        try:\n            r = FL.label_with(cand, rds, FL.MAX_MAPS * job.get(\"cap_mult\", 1), FL.MAX_SECS * job.get(\"cap_mult\", 1), t0)\n        except Exception as ex:  # noqa: BLE001 - one class must not kill the sentence\n            out.append({\"class_key\": ck, \"sentence_id\": s[\"sentence_id\"], \"candidate_fol\": fol,\n                        \"status\": \"UNRESOLVED_Z3_UNKNOWN\", \"error\": f\"{type(ex).__name__}: {str(ex)[:160]}\"})\n            continue\n        out.append({\"class_key\": ck, \"sentence_id\": s[\"sentence_id\"], \"candidate_fol\": fol, **r})\n    return out\n\n\ndef run(classes_by_sid: dict, sents: dict, outp, logger, limit: int | None, cap_mult: int = 1) -> None:\n    done = set()\n    if outp.exists():\n        done = {json.loads(l)[\"class_key\"] for l in outp.read_text().splitlines() if l.strip()}\ntotal 11210\ndrwxr-xr-x  2 root root 2000711 Sep 24 07:46 .\ndrwxr-xr-x 11 root root 2009731 Sep 24 10:50 ..\n-rw-r--r--  1 root root    2359 Sep 24 07:38 audit_errcert_keys.json\n-rw-r--r--  1 root root    2359 Sep 24 07:39 audit_mapped_keys.json\n-rw-r--r--  1 root root   43178 Sep 24 07:39 audit_mapped_view.txt\n-rw-r--r--  1 root root    1062 Sep 24 07:18 dev_trial_D1.py\n-rw-r--r--  1 root root    9223 Sep 24 07:40 executor_audit_verdicts.json\n-rw-r--r--  1 root root 1767883 Sep 24 07:13 free_rows.jsonl\n-rw-r--r--  1 root root  806127 Sep 24 07:21 models_snapshot.json\n-rw-r--r--  1 root root    1373 Sep 24 07:33 probe_free_models_D9.py\n-rw-r--r--  1 root root  685497 Sep 24 07:13 sentences.json\n-rw-r--r--  1 root root 1429393 Sep 24 07:34 sig_renamed_nonce.jsonl\n-rw-r--r--  1 root root 1663307 Sep 24 07:35 sig_renamed_syn.jsonl\n-rw-r--r--  1 root root 1053397 Sep 24 07:13 sig_rows.jsonl", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [16] ASSISTANT · 2026-09-25 16:38:04 UTC

```
Reading the artifact's `data.py` and its preview data is done. Next I'll build a stratified 100-row demo subset from the full output file, using a script so the whole file never enters context.
```

### [17] TOOL CALL — Bash · 2026-09-25 16:38:04 UTC

```
python3 - <<'EOF'
import json, random
from collections import Counter, defaultdict
A="/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/full_data_out.json"
d=json.load(open(A))
print(d["metadata"].keys())
g={x["dataset"]:x for x in d["datasets"]}
ex=g["rcomp_free_labels"]["examples"]
print(len(ex), Counter(e["output"] for e in ex))
print(Counter(e["metadata_clause_type"] for e in ex), Counter(e["metadata_word_tercile"] for e in ex))
print(Counter(json.loads(e["input"])["family"] for e in ex))
print(json.loads(ex[5]["input"]))
print(max(len(json.dumps(e)) for e in ex))
EOF
```

### [18] TOOL RESULT — Bash · 2026-09-25 16:38:06 UTC

```
{"stdout": "dict_keys(['artifact', 'workspace', 'selection', 'label_mode', 'status_note', 'seal_all_rows_sha256', 'seal_untouched_sha256', 'prereg_sha256', 'testability_all_rows', 'testability_untouched', 'provisional_view_testable'])\n2652 Counter({'UNRESOLVED_GLOSS_NOT_RUN': 1506, 'ERROR_CERT': 759, 'NO_OUTPUT': 199, 'UNPARSEABLE': 188})\nCounter({'unless': 888, 'except_when': 336, 'provided_that+unless': 312, 'as_long_as+unless': 300, 'except_when+provided_that': 288, 'but_only_if': 276, 'provided_that': 252}) Counter({'W2': 984, 'W3': 924, 'W1': 744})\nCounter({'meta': 663, 'qwen': 442, 'mistral': 221, 'deepseek': 221, 'google-gemma': 221, 'microsoft': 221, 'openai': 221, 'google-gemini': 221, 'cohere': 221})\n{'text': \"Each legislator who is at Board Game night, who visits a coffee shop regularly, and who can distinguish the taste of different condiments is Emily's friend, except if the legislator is an elected official.\", 'candidate_fol': '∀x ((Legislator(x) ∧ At(x, boardGameNight) ∧ RegularlyVisits(x, coffeeShop) ∧ CanDistinguish(x, taste, differentCondiments) ∧ ¬ElectedOfficial(x)) → Friend(x, emily))', 'system': 'G3:mistralai/mistral-small-3.2-24b-instruct', 'family': 'mistral', 'slot': 'G3', 'prompt_variant': 'fewshot_v1', 'condition': 'FREE', 'template_id': 'T1'}\n15484", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [19] TOOL CALL — Bash · 2026-09-25 16:38:16 UTC

```
python3 - <<'EOF'
import json, random
from collections import Counter, defaultdict
A="/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/full_data_out.json"
d=json.load(open(A))
ex=[x for x in d["datasets"] if x["dataset"]=="rcomp_free_labels"][0]["examples"]
rng=random.Random(0)
quota={"ERROR_CERT":40,"UNRESOLVED_GLOSS_NOT_RUN":40,"UNPARSEABLE":10,"NO_OUTPUT":10}
pick=[]
for lab,q in quota.items():
    pool=[e for e in ex if e["output"]==lab]; rng.shuffle(pool)
    # round-robin over (clause_type, family) strata for diversity
    by=defaultdict(list)
    for e in pool: by[(e["metadata_clause_type"], json.loads(e["input"])["family"])].append(e)
    keys=sorted(by); rng.shuffle(keys); sel=[]
    while len(sel)<q:
        for k in keys:
            if by[k] and len(sel)<q: sel.append(by[k].pop())
    pick+=sel
pick.sort(key=lambda e:e["metadata_row_key"])
md=dict(d["metadata"]); md.pop("workspace",None)
md["demo_subset_note"]="100 of 2,652 rcomp_free_labels rows, stratified by label (40/40/10/10) x clause_type x LLM family (seed 0); corpus-level counts above refer to the full dataset."
out={"metadata":md,"datasets":[{"dataset":"rcomp_free_labels","examples":pick}]}
json.dump(out,open("mini_demo_data.json","w"),ensure_ascii=False,indent=1)
print(Counter(e["output"] for e in pick), Counter(e["metadata_clause_type"] for e in pick), Counter(json.loads(e["input"])["family"] for e in pick), Counter(e["metadata_word_tercile"] for e in pick), sum(e["metadata_seen_iter3"] for e in pick))
EOF
ls -la mini_demo_data.json
```

### [20] TOOL RESULT — Bash · 2026-09-25 16:38:16 UTC

```
{"stdout": "Counter({'ERROR_CERT': 40, 'UNRESOLVED_GLOSS_NOT_RUN': 40, 'NO_OUTPUT': 10, 'UNPARSEABLE': 10}) Counter({'except_when': 17, 'unless': 17, 'provided_that': 15, 'as_long_as+unless': 14, 'provided_that+unless': 14, 'except_when+provided_that': 12, 'but_only_if': 11}) Counter({'qwen': 19, 'mistral': 13, 'google-gemma': 12, 'openai': 11, 'deepseek': 10, 'meta': 10, 'cohere': 9, 'google-gemini': 9, 'microsoft': 7}) Counter({'W2': 48, 'W3': 29, 'W1': 23}) 10\n-rw-r--r-- 1 root root 332810 Sep 25 16:38 mini_demo_data.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [21] TOOL CALL — Bash · 2026-09-25 16:38:28 UTC

```
mkdir -p /tmp/claude-0/-ai-inventor-aii-data-runs-run-An1uy2kF2SjZ-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-Ia-FT284H33j/257e4f52-95ca-458d-82e4-999d69f460e7/scratchpad; A=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5; python3 -c "
import json;t=json.load(open('$A/results/testability_FREE_v2.json'));print(list(t.keys()));print({k:list(v.keys()) if isinstance(v,dict) else v for k,v in t.items()})" | head -c 3000; python3 -c "
import json;s=json.load(open('$A/results/seal.json'));print(s['seals'][-1].keys())"
```

### [22] TOOL RESULT — Bash · 2026-09-25 16:38:28 UTC

```
{"stdout": "['mode', 'utc', 'rule', 'word_terciles', 'all_rows', 'untouched_subset', 'note', 'seen_iter3_subset', 'search_provisional_view']\n{'mode': 'search_only', 'utc': '2026-09-24T07:37:10Z', 'rule': 'TESTABLE iff >= 50 ERROR and >= 50 CORRECT rows, each class spread over >= 25 sentences', 'word_terciles': ['cut_1', 'cut_2'], 'all_rows': ['population', 'n_rows', 'n_ERROR', 'n_CORRECT', 'sentences_with_ERROR', 'sentences_with_CORRECT', 'TESTABLE', 'reportable_30_30', 'label_counts', 'strata'], 'untouched_subset': ['population', 'n_rows', 'n_ERROR', 'n_CORRECT', 'sentences_with_ERROR', 'sentences_with_CORRECT', 'TESTABLE', 'reportable_30_30', 'label_counts', 'strata'], 'note': 'SEARCH-ONLY labels (D9): no CORRECT class exists until the gloss step runs, so AUROC is NOT_TESTABLE; the ERROR_CERT class alone supports recall-type analyses; MAPPED rows are UNRESOLVED_GLOSS_NOT_RUN', 'seen_iter3_subset': ['population', 'n_rows', 'n_ERROR', 'n_CORRECT', 'sentences_with_ERROR', 'sentences_with_CORRECT', 'TESTABLE', 'reportable_30_30', 'label_counts', 'strata'], 'search_provisional_view': ['definition', 'all_rows', 'untouched_subset', 'contamination']}\ndict_keys(['utc', 'mode', 'label_vector_sha256_all_rows', 'n_rows', 'label_counts', 'prereg_sha256', 'prereg_v1_sha256', 'vendor_sha256', 'code_sha256', 'map_search_sha256', 'old_labels_joined', 'stage', 'label_vector_sha256_untouched', 'n_untouched', 'note'])", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [23] TOOL CALL — Write · 2026-09-25 16:39:34 UTC

```
File: /tmp/claude-0/-ai-inventor-aii-data-runs-run-An1uy2kF2SjZ-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-Ia-FT284H33j/257e4f52-95ca-458d-82e4-999d69f460e7/scratchpad/make_nb.py

import json
from pathlib import Path

OUT = Path("/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_Ia_FT284H33j/code_demo.ipynb")
cells = []


def md(s):
    cells.append({"cell_type": "markdown", "metadata": {}, "source": s.strip("\n")})


def code(s):
    cells.append({"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": s.strip("\n")})


md(r"""
# Name-free labels for free-vocabulary NL→FOL translations: dataset demo

This notebook walks through the **`rcomp_free_labels`** group of the dataset artifact *"Name-free labels for free-vocabulary logic translations"* (T7b).

**What the dataset contains.** 221 templated English rule sentences (for example *"Each legislator who … is Emily's friend, except if …"*) were translated into first-order logic by 10 LLM slots from 9 model families. The prompts used **free vocabulary**: each model chose its own predicate and constant names. That gives **2,652 (sentence, candidate FOL) rows**. Each row gets a faithfulness label that **does not depend on symbol names**. An exhaustive search looks for a symbol map from the candidate's vocabulary onto the reference reading's vocabulary. The map is injective, and it may use the bridges B1/B2 (reification), B3 (merge), B4 (split) and B5 (lexical negation). The search uses z3 relevance/polarity prunes, 128-model finite countermodels and z3 equivalence checks. It hit 0 caps and returned 0 z3 `unknown` results.

| label | meaning | full-dataset count |
|---|---|---|
| `ERROR_CERT` | no admissible map makes the candidate equivalent to any reading of the sentence. This label is **final** and backed by a certificate | 759 |
| `UNRESOLVED_GLOSS_NOT_RUN` | some map makes it z3-equivalent (MAPPED), but the LLM **gloss check** (does each symbol really mean the mapped phrase?) has not run yet | 1,506 |
| `UNPARSEABLE` | the output does not parse as FOL | 188 |
| `NO_OUTPUT` | the model returned nothing | 199 |

The paid gloss step could not run: the run's OpenRouter budget was exhausted (deviation D9). So the labels are **search-only**, and no `CORRECT` class exists yet. The binary view `metadata_label_binary_search_provisional` (ERROR vs MAPPED) is provisional. An audit estimated about 13% contamination on each side.

**What the original script (`data.py`) does.** It assembles the three plan groups (`rcomp_free_labels`, `gloss_gate_items`, `sig_soundness_replay`) from the run's `results/*.jsonl`. It checks that each example has string `input`/`output` fields and no reserved keys. Then it attaches the seal and testability metadata and writes `full_data_out.json` in the `exp_sel_data_out` format. Here the same code runs on a **curated 100-row subset** of `rcomp_free_labels`: 40 ERROR_CERT, 40 UNRESOLVED, 10 UNPARSEABLE and 10 NO_OUTPUT, stratified by clause type and LLM family. The subset is loaded from GitHub. The notebook then explores and plots the labels.
""")

code(r"""
import subprocess, sys
def _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])

# loguru — used by the original data.py, NOT pre-installed on Colab, always install
_pip('loguru==0.7.3')

# pandas, matplotlib — pre-installed on Colab, install locally only (at Colab's exact versions)
if 'google.colab' not in sys.modules:
    _pip('numpy==2.0.2', 'pandas==2.2.2', 'matplotlib==3.10.0')
""")

md(r"""
## Imports
This is the original import block of `data.py`. The original also inserts `src/` and `vendor/` into `sys.path` so that it can import `build_output`. The notebook does not need those modules, because it reads the already-built rows from the demo JSON. It adds `pandas` and `matplotlib` for the analysis at the end.
""")

code(r"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from loguru import logger

# --- notebook additions (analysis / plotting) ---
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
""")

md(r"""
## Data loading
The loader fetches `mini_demo_data.json` from the GitHub repository. If that fails, it falls back to a local copy. The file has the same `exp_sel_data_out` layout as the artifact's `full_data_out.json`: a `metadata` block plus `datasets: [{dataset, examples}]`.
""")

code(r"""
GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_An1uy2kF2SjZ/round-4/dataset-5/demo/mini_demo_data.json"
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
""")

code(r"""
data = load_data()
print({g["dataset"]: len(g["examples"]) for g in data["datasets"]})
print(data["metadata"]["demo_subset_note"])
""")

md(r"""
## Config
`data.py` has no numeric hyperparameters. The only knobs are which groups to keep (`SELECTED`) and, in this notebook, how many rows of the demo subset to process.
- `MAX_EXAMPLES`: rows of `rcomp_free_labels` to run through the pipeline. The demo file holds 100, and the original run used all **2,652**.
- `N_SHOW`: how many decoded examples to print in the inspection cell.
- `SELECTED`: the original list of plan groups. Only `rcomp_free_labels` ships in the demo file. The other two groups (840 gloss-gate items and 4,280 SIG soundness-replay rows) are in the artifact's `full_data_out.json`.
""")

code(r"""
MAX_EXAMPLES = 100   # demo subset size; original full run: 2652 rcomp_free_labels rows (+ 840 gate + 4280 SIG rows)
N_SHOW = 3           # decoded examples printed below

SELECTED = ["rcomp_free_labels", "gloss_gate_items", "sig_soundness_replay"]
""")

md(r"""
## Logger setup (original)
This is the original loguru configuration: INFO to stdout, plus a DEBUG file sink under `logs/`. `ROOT` was the script's own folder. In the notebook it is the current working directory.
""")

code(r"""
ROOT = Path.cwd()  # original: Path(__file__).resolve().parent

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
(ROOT / "logs").mkdir(exist_ok=True)
logger.add(ROOT / "logs" / "data.log", rotation="30 MB", level="DEBUG")
""")

md(r"""
## How a row is built (from `src/build_output.py::free_group`)
In the original script, `B.free_group()` reads `results/free_labels_v2.jsonl` and turns each labelled record into one example:
- **`input`**: a JSON *string* with `text` (the English sentence), `candidate_fol` (the LLM's formula), `system`, `family`, `slot`, `prompt_variant`, `condition="FREE"` and `template_id`.
- **`output`**: the label (`ERROR_CERT`, `UNRESOLVED_GLOSS_NOT_RUN`, `UNPARSEABLE` or `NO_OUTPUT`).
- **`metadata_*`**: strata (`template_id`, `clause_type`, `words`, `word_tercile`, `nconds_weak`, `nested`, …) and the search evidence. The evidence includes `map_certificate` (the symbol map and the bridges it used), `n_maps_enumerated`, `n_equiv_maps`, `nonequiv_certificate_type_counts` (why the maps that were ruled out failed), `gloss_pairs` (the (symbol, meaning) pairs the gloss checker will judge), `seen_iter3`, and the old iter-3 label.

The notebook reuses that function's `md()` helper and the provisional binary mapping. In the cell below, `groups` comes from the loaded demo data rather than from `B.free_group(), B.gate_group(), B.sig_group()`.
""")

code(r"""
def md(d: dict) -> dict:  # from build_output.py (used to prefix metadata keys)
    return {f"metadata_{k}": v for k, v in d.items()}

# original: import build_output as B; groups = [B.free_group(), B.gate_group(), B.sig_group()]
groups = [{"dataset": g["dataset"], "examples": g["examples"][:MAX_EXAMPLES]} for g in data["datasets"]]

# same provisional binary view that free_group() writes (ERROR vs MAPPED; everything else EXCLUDED)
for g in groups:
    for e in g["examples"]:
        search_bin = {"ERROR_CERT": "ERROR", "UNRESOLVED_GLOSS_NOT_RUN": "MAPPED"}.get(e["output"], "EXCLUDED")
        assert e["metadata_label_binary_search_provisional"] == search_bin, e["metadata_row_key"]
print({g["dataset"]: len(g["examples"]) for g in groups})
""")

md(r"""
## `main()`: validate the groups and assemble the output file (original logic)
This follows the original `main()`. Every group must be non-empty, and every example must have string `input`/`output` and none of the reserved keys `split`/`dataset`/`context`. The script then builds the top-level metadata from the **seal** (sha256 hashes of the label vector for all rows and for the untouched subset, and of the preregistration) and from the **testability** report. That report applies the rule *TESTABLE iff ≥50 ERROR and ≥50 CORRECT rows, each class spread over ≥25 sentences*.

There is one change. The original read `seal` and `t` from `results/seal.json` and `results/testability_FREE_v2.json`. Here they are rebuilt from the metadata block that shipped with the data, so the same dictionary-building code runs unchanged. The output goes to `demo_data_out.json` instead of overwriting `full_data_out.json`.
""")

code(r"""
M = data["metadata"]
# original: seal = json.loads((ROOT / "results" / "seal.json").read_text())["seals"][-1]
seal = {"mode": M["label_mode"], "label_vector_sha256_all_rows": M["seal_all_rows_sha256"],
        "label_vector_sha256_untouched": M["seal_untouched_sha256"], "prereg_sha256": M["prereg_sha256"]}
# original: t = json.loads((ROOT / "results" / "testability_FREE_v2.json").read_text())
t = {"all_rows": M["testability_all_rows"], "untouched_subset": M["testability_untouched"],
     "search_provisional_view": {k: {"TESTABLE": v} for k, v in M["provisional_view_testable"].items()}}


@logger.catch(reraise=True)
def main() -> None:
    for g in groups:
        assert g["examples"], g["dataset"]
        for e in g["examples"]:
            assert isinstance(e["input"], str) and isinstance(e["output"], str), g["dataset"]
            assert not ({"split", "dataset", "context"} & set(e)), g["dataset"]
    out = {"metadata": {
        "artifact": "T7b name-free labels for free-vocabulary rule translations (run_u75jRHUss0zo, iter 4, gen_art_dataset_5)",
        "workspace": str(ROOT),
        "selection": ("the three plan groups (chosen as best 3 of 6 standardised candidates; folio / malls_test / "
                      "logicnli_test were context only: no multi-system candidates, ~36-39% wrong gold, or no FOL; their "
                      "standardised record is temp/candidates_data_out.json)"),
        "label_mode": seal["mode"],
        "status_note": ("SEARCH-ONLY labels: the paid gloss step could not run (deviation D9: run OpenRouter budget "
                        "exhausted before this artifact's first call; re-probed at packaging, still HTTP 403). ERROR_CERT is "
                        "final and certificate-backed; MAPPED rows are UNRESOLVED_GLOSS_NOT_RUN until src/resume_gloss.py "
                        "runs. metadata_label_binary_search_provisional (ERROR vs MAPPED) is a provisional view with audited "
                        "contamination (results/soundness_audit.json)."),
        "seal_all_rows_sha256": seal["label_vector_sha256_all_rows"],
        "seal_untouched_sha256": seal.get("label_vector_sha256_untouched"),
        "prereg_sha256": seal["prereg_sha256"],
        "testability_all_rows": {k: t["all_rows"][k] for k in ("n_ERROR", "n_CORRECT", "TESTABLE", "label_counts")},
        "testability_untouched": {k: t["untouched_subset"][k] for k in ("n_ERROR", "n_CORRECT", "TESTABLE", "label_counts")},
        "provisional_view_testable": {k: t["search_provisional_view"][k]["TESTABLE"] for k in ("all_rows", "untouched_subset")},
    }, "datasets": [g for g in groups if g["dataset"] in SELECTED]}
    (ROOT / "demo_data_out.json").write_text(json.dumps(out, ensure_ascii=False))  # original: full_data_out.json
    logger.info(f"demo_data_out.json: {[(g['dataset'], len(g['examples'])) for g in out['datasets']]}")
    return out


out = main()
print(json.dumps({k: out["metadata"][k] for k in ("label_mode", "testability_all_rows", "provisional_view_testable")}, indent=1))
""")

md(r"""
## Inspect a few rows
Each `input` string is decoded to show the sentence, the free-vocabulary candidate and the label. For MAPPED rows the **map certificate** is printed as well: the candidate symbols mapped onto phrases of the reference reading, plus any bridges used. For ERROR_CERT rows the output shows how the non-equivalent maps were ruled out.
""")

code(r"""
ex = out["datasets"][0]["examples"]
shown = Counter()
for e in ex:
    if shown[e["output"]] >= 1 or sum(shown.values()) >= N_SHOW:
        continue
    shown[e["output"]] += 1
    inp = json.loads(e["input"])
    print("=" * 100)
    print(f"LABEL: {e['output']}   system: {inp['system']}   clause: {e['metadata_clause_type']}   words: {e['metadata_words']}")
    print("TEXT :", inp["text"])
    print("FOL  :", inp["candidate_fol"])
    if e["metadata_map_certificate"]:
        c = e["metadata_map_certificate"]
        print(f"MAP  : reading={c['reading']} bridges={c['bridges']}")
        for m in c["map"]:
            print("       ", m)
        print(f"       {e['metadata_n_equiv_maps']} equivalent maps in {e['metadata_n_equiv_map_orbits']} orbits "
              f"(of {e['metadata_n_maps_enumerated']} enumerated)")
    if e["metadata_nonequiv_certificate_type_counts"]:
        print("NON-EQUIV CERTS:", e["metadata_nonequiv_certificate_type_counts"])
    if e["metadata_unresolved_reason"]:
        print("UNRESOLVED:", e["metadata_unresolved_reason"])
""")

md(r"""
## Results: label distribution, strata and search evidence
The rows are flattened into a table. The cells below report the following:
1. Label counts in the demo subset next to the full-dataset counts from the seal metadata.
2. The ERROR-vs-MAPPED provisional view per clause type and per word tercile (sentence-length bin), which shows how certificate-backed errors spread over sentence complexity.
3. The ERROR rate per LLM family.
4. The kinds of non-equivalence certificates, and the bridges used by successful maps.
""")

code(r"""
df = pd.DataFrame([{**{k[len('metadata_'):]: v for k, v in e.items() if k.startswith('metadata_') and not isinstance(v, (dict, list))},
                    "label": e["output"], "family": json.loads(e["input"])["family"]} for e in ex])

full_counts = out["metadata"]["testability_all_rows"]["label_counts"]
tab = pd.DataFrame({"demo_subset": df["label"].value_counts(), "full_dataset": pd.Series(full_counts)}).fillna(0).astype(int)
print("Label counts (demo subset is stratified, so proportions differ from the full dataset):")
print(tab.to_string(), "\n")

bin_df = df[df["label_binary_search_provisional"] != "EXCLUDED"]
for col in ("clause_type", "word_tercile"):
    ct = pd.crosstab(bin_df[col], bin_df["label_binary_search_provisional"])
    ct["ERROR_share"] = (ct.get("ERROR", 0) / ct.sum(axis=1)).round(2)
    print(f"Provisional ERROR vs MAPPED by {col}:")
    print(ct.to_string(), "\n")

cert_types = Counter()
bridges = Counter()
for e in ex:
    for k, v in (e["metadata_nonequiv_certificate_type_counts"] or {}).items():
        cert_types[k] += v
    if e["metadata_map_certificate"]:
        bridges.update(e["metadata_map_certificate"].get("bridges") or ["identity/none"])
print("Non-equivalence certificate types (summed over rows):", dict(cert_types.most_common()))
print("Bridges used by MAPPED certificates:", dict(bridges.most_common()))
print(f"Median search time per row: {df['search_secs'].median():.2f}s (max {df['search_secs'].max():.2f}s)")
""")

code(r"""
fig, axes = plt.subplots(2, 2, figsize=(14, 9))

# (a) label counts: demo vs full (normalised)
(tab / tab.sum()).plot.bar(ax=axes[0, 0], color=["#4C72B0", "#DD8452"])
axes[0, 0].set_title("Label share: demo subset vs full dataset")
axes[0, 0].set_ylabel("share of rows"); axes[0, 0].tick_params(axis="x", rotation=20)

# (b) provisional ERROR vs MAPPED by clause type
ct = pd.crosstab(bin_df["clause_type"], bin_df["label_binary_search_provisional"])
ct.plot.barh(stacked=True, ax=axes[0, 1], color={"ERROR": "#C44E52", "MAPPED": "#55A868"})
axes[0, 1].set_title("Provisional ERROR vs MAPPED by clause type"); axes[0, 1].set_xlabel("rows")

# (c) ERROR share by LLM family (over ERROR+MAPPED rows)
fam = pd.crosstab(bin_df["family"], bin_df["label_binary_search_provisional"])
(fam.get("ERROR", 0) / fam.sum(axis=1)).sort_values().plot.barh(ax=axes[1, 0], color="#8172B3")
axes[1, 0].set_title("ERROR_CERT share by LLM family (ERROR+MAPPED rows)"); axes[1, 0].set_xlim(0, 1)

# (d) non-equivalence certificate types
if cert_types:
    pd.Series(dict(cert_types.most_common())).plot.bar(ax=axes[1, 1], color="#937860", logy=True)
axes[1, 1].set_title("Non-equivalence certificate types (log scale)"); axes[1, 1].tick_params(axis="x", rotation=30)

plt.tight_layout()
plt.show()
""")

md(r"""
**Reading the results.** `ERROR_CERT` rows come with a proof-style certificate that *no* name-free map rescues the candidate, so they are final relative to the bridge family. `MAPPED` rows are only **provisionally** correct: an audit of the SIG soundness replay showed that 9–10% of known-wrong formulas can be "rescued" by a non-identity symbol map. Catching those is the job of the pending gloss check (`src/resume_gloss.py` in the artifact). Because no `CORRECT` class exists yet, AUROC-type evaluations on this dataset are `NOT_TESTABLE`. Only the provisional ERROR-vs-MAPPED view is testable, with about 13% audited contamination on each side.
""")

nb = {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                                   "language_info": {"name": "python"}}, "nbformat": 4, "nbformat_minor": 5}
for i, c in enumerate(nb["cells"]):
    c["id"] = f"cell-{i}"
OUT.write_text(json.dumps(nb, indent=1, ensure_ascii=False))
print("wrote", OUT)
```

### [24] TOOL RESULT — Write · 2026-09-25 16:39:34 UTC

```
{"type": "create", "filePath": "/tmp/claude-0/-ai-inventor-aii-data-runs-run-An1uy2kF2SjZ-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-Ia-FT284H33j/257e4f52-95ca-458d-82e4-999d69f460e7/scratchpad/make_nb.py", "content": "import json\nfrom pathlib import Path\n\nOUT = Path(\"/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_Ia_FT284H33j/code_demo.ipynb\")\ncells = []\n\n\ndef md(s):\n    cells.append({\"cell_type\": \"markdown\", \"metadata\": {}, \"source\": s.strip(\"\\n\")})\n\n\ndef code(s):\n    cells.append({\"cell_type\": \"code\", \"metadata\": {}, \"execution_count\": None, \"outputs\": [], \"source\": s.strip(\"\\n\")})\n\n\nmd(r\"\"\"\n# Name-free labels for free-vocabulary NL→FOL translations: dataset demo\n\nThis notebook walks through the **`rcomp_free_labels`** group of the dataset artifact *\"Name-free labels for free-vocabulary logic translations\"* (T7b).\n\n**What the dataset contains.** 221 templated English rule sentences (for example *\"Each legislator who … is Emily's friend, except if …\"*) were translated into first-order logic by 10 LLM slots from 9 model families. The prompts used **free vocabulary**: each model chose its own predicate and constant names. That gives **2,652 (sentence, candidate FOL) rows**. Each row gets a faithfulness label that **does not depend on symbol names**. An exhaustive search looks for a symbol map from the candidate's vocabulary onto the reference reading's vocabulary. The map is injective, and it may use the bridges B1/B2 (reification), B3 (merge), B4 (split) and B5 (lexical negation). The search uses z3 relevance/polarity prunes, 128-model finite countermodels and z3 equivalence checks. It hit 0 caps and returned 0 z3 `unknown` results.\n\n| label | meaning | full-dataset count |\n|---|---|---|\n| `ERROR_CERT` | no admissible map makes the candidate equivalent to any reading of the sentence. This label is **final** and backed by a certificate | 759 |\n| `UNRESOLVED_GLOSS_NOT_RUN` | some map makes it z3-equivalent (MAPPED), but the LLM **gloss check** (does each symbol really mean the mapped phrase?) has not run yet | 1,506 |\n| `UNPARSEABLE` | the output does not parse as FOL | 188 |\n| `NO_OUTPUT` | the model returned nothing | 199 |\n\nThe paid gloss step could not run: the run's OpenRouter budget was exhausted (deviation D9). So the labels are **search-only**, and no `CORRECT` class exists yet. The binary view `metadata_label_binary_search_provisional` (ERROR vs MAPPED) is provisional. An audit estimated about 13% contamination on each side.\n\n**What the original script (`data.py`) does.** It assembles the three plan groups (`rcomp_free_labels`, `gloss_gate_items`, `sig_soundness_replay`) from the run's `results/*.jsonl`. It checks that each example has string `input`/`output` fields and no reserved keys. Then it attaches the seal and testability metadata and writes `full_data_out.json` in the `exp_sel_data_out` format. Here the same code runs on a **curated 100-row subset** of `rcomp_free_labels`: 40 ERROR_CERT, 40 UNRESOLVED, 10 UNPARSEABLE and 10 NO_OUTPUT, stratified by clause type and LLM family. The subset is loaded from GitHub. The notebook then explores and plots the labels.\n\"\"\")\n\ncode(r\"\"\"\nimport subprocess, sys\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\n\n# loguru — used by the original data.py, NOT pre-installed on Colab, always install\n_pip('loguru==0.7.3')\n\n# pandas, matplotlib — pre-installed on Colab, install locally only (at Colab's exact versions)\nif 'google.colab' not in sys.modules:\n    _pip('numpy==2.0.2', 'pandas==2.2.2', 'matplotlib==3.10.0')\n\"\"\")\n\nmd(r\"\"\"\n## Imports\nThis is the original import block of `data.py`. The original also inserts `src/` and `vendor/` into `sys.path` so that it can import `build_output`. The notebook does not need those modules, because it reads the already-built rows from the demo JSON. It adds `pandas` and `matplotlib` for the analysis at the end.\n\"\"\")\n\ncode(r\"\"\"\nfrom __future__ import annotations\n\nimport json\nimport sys\nfrom pathlib import Path\n\nfrom loguru import logger\n\n# --- notebook additions (analysis / plotting) ---\nfrom collections import Counter\nimport pandas as pd\nimport matplotlib.pyplot as plt\n\"\"\")\n\nmd(r\"\"\"\n## Data loading\nThe loader fetches `mini_demo_data.json` from the GitHub repository. If that fails, it falls back to a local copy. The file has the same `exp_sel_data_out` layout as the artifact's `full_data_out.json`: a `metadata` block plus `datasets: [{dataset, examples}]`.\n\"\"\")\n\ncode(r\"\"\"\nGITHUB_DATA_URL = \"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_An1uy2kF2SjZ/round-4/dataset-5/demo/mini_demo_data.json\"\nimport json\nfrom pathlib import Path\n\ndef load_data():\n    try:\n        import urllib.request\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\n            return json.loads(response.read().decode())\n    except Exception: pass\n    local = Path(\"mini_demo_data.json\")\n    if local.exists(): return json.loads(local.read_text())\n    raise FileNotFoundError(\"Could not load mini_demo_data.json\")\n\"\"\")\n\ncode(r\"\"\"\ndata = load_data()\nprint({g[\"dataset\"]: len(g[\"examples\"]) for g in data[\"datasets\"]})\nprint(data[\"metadata\"][\"demo_subset_note\"])\n\"\"\")\n\nmd(r\"\"\"\n## Config\n`data.py` has no numeric hyperparameters. The only knobs are which groups to keep (`SELECTED`) and, in this notebook, how many rows of the demo subset to process.\n- `MAX_EXAMPLES`: rows of `rcomp_free_labels` to run through the pipeline. The demo file holds 100, and the original run used all **2,652**.\n- `N_SHOW`: how many decoded examples to print in the inspection cell.\n- `SELECTED`: the original list of plan groups. Only `rcomp_free_labels` ships in the demo file. The other two groups (840 gloss-gate items and 4,280 SIG soundness-replay rows) are in the artifact's `full_data_out.json`.\n\"\"\")\n\ncode(r\"\"\"\nMAX_EXAMPLES = 100   # demo subset size; original full run: 2652 rcomp_free_labels rows (+ 840 gate + 4280 SIG rows)\nN_SHOW = 3           # decoded examples printed below\n\nSELECTED = [\"rcomp_free_labels\", \"gloss_gate_items\", \"sig_soundness_replay\"]\n\"\"\")\n\nmd(r\"\"\"\n## Logger setup (original)\nThis is the original loguru configuration: INFO to stdout, plus a DEBUG file sink under `logs/`. `ROOT` was the script's own folder. In the notebook it is the current working directory.\n\"\"\")\n\ncode(r\"\"\"\nROOT = Path.cwd()  # original: Path(__file__).resolve().parent\n\nlogger.remove()\nlogger.add(sys.stdout, level=\"INFO\", format=\"{time:HH:mm:ss}|{level:<7}|{message}\")\n(ROOT / \"logs\").mkdir(exist_ok=True)\nlogger.add(ROOT / \"logs\" / \"data.log\", rotation=\"30 MB\", level=\"DEBUG\")\n\"\"\")\n\nmd(r\"\"\"\n## How a row is built (from `src/build_output.py::free_group`)\nIn the original script, `B.free_group()` reads `results/free_labels_v2.jsonl` and turns each labelled record into one example:\n- **`input`**: a JSON *string* with `text` (the English sentence), `candidate_fol` (the LLM's formula), `system`, `family`, `slot`, `prompt_variant`, `condition=\"FREE\"` and `template_id`.\n- **`output`**: the label (`ERROR_CERT`, `UNRESOLVED_GLOSS_NOT_RUN`, `UNPARSEABLE` or `NO_OUTPUT`).\n- **`metadata_*`**: strata (`template_id`, `clause_type`, `words`, `word_tercile`, `nconds_weak`, `nested`, …) and the search evidence. The evidence includes `map_certificate` (the symbol map and the bridges it used), `n_maps_enumerated`, `n_equiv_maps`, `nonequiv_certificate_type_counts` (why the maps that were ruled out failed), `gloss_pairs` (the (symbol, meaning) pairs the gloss checker will judge), `seen_iter3`, and the old iter-3 label.\n\nThe notebook reuses that function's `md()` helper and the provisional binary mapping. In the cell below, `groups` comes from the loaded demo data rather than from `B.free_group(), B.gate_group(), B.sig_group()`.\n\"\"\")\n\ncode(r\"\"\"\ndef md(d: dict) -> dict:  # from build_output.py (used to prefix metadata keys)\n    return {f\"metadata_{k}\": v for k, v in d.items()}\n\n# original: import build_output as B; groups = [B.free_group(), B.gate_group(), B.sig_group()]\ngroups = [{\"dataset\": g[\"dataset\"], \"examples\": g[\"examples\"][:MAX_EXAMPLES]} for g in data[\"datasets\"]]\n\n# same provisional binary view that free_group() writes (ERROR vs MAPPED; everything else EXCLUDED)\nfor g in groups:\n    for e in g[\"examples\"]:\n        search_bin = {\"ERROR_CERT\": \"ERROR\", \"UNRESOLVED_GLOSS_NOT_RUN\": \"MAPPED\"}.get(e[\"output\"], \"EXCLUDED\")\n        assert e[\"metadata_label_binary_search_provisional\"] == search_bin, e[\"metadata_row_key\"]\nprint({g[\"dataset\"]: len(g[\"examples\"]) for g in groups})\n\"\"\")\n\nmd(r\"\"\"\n## `main()`: validate the groups and assemble the output file (original logic)\nThis follows the original `main()`. Every group must be non-empty, and every example must have string `input`/`output` and none of the reserved keys `split`/`dataset`/`context`. The script then builds the top-level metadata from the **seal** (sha256 hashes of the label vector for all rows and for the untouched subset, and of the preregistration) and from the **testability** report. That report applies the rule *TESTABLE iff ≥50 ERROR and ≥50 CORRECT rows, each class spread over ≥25 sentences*.\n\nThere is one change. The original read `seal` and `t` from `results/seal.json` and `results/testability_FREE_v2.json`. Here they are rebuilt from the metadata block that shipped with the data, so the same dictionary-building code runs unchanged. The output goes to `demo_data_out.json` instead of overwriting `full_data_out.json`.\n\"\"\")\n\ncode(r\"\"\"\nM = data[\"metadata\"]\n# original: seal = json.loads((ROOT / \"results\" / \"seal.json\").read_text())[\"seals\"][-1]\nseal = {\"mode\": M[\"label_mode\"], \"label_vector_sha256_all_rows\": M[\"seal_all_rows_sha256\"],\n        \"label_vector_sha256_untouched\": M[\"seal_untouched_sha256\"], \"prereg_sha256\": M[\"prereg_sha256\"]}\n# original: t = json.loads((ROOT / \"results\" / \"testability_FREE_v2.json\").read_text())\nt = {\"all_rows\": M[\"testability_all_rows\"], \"untouched_subset\": M[\"testability_untouched\"],\n     \"search_provisional_view\": {k: {\"TESTABLE\": v} for k, v in M[\"provisional_view_testable\"].items()}}\n\n\n@logger.catch(reraise=True)\ndef main() -> None:\n    for g in groups:\n        assert g[\"examples\"], g[\"dataset\"]\n        for e in g[\"examples\"]:\n            assert isinstance(e[\"input\"], str) and isinstance(e[\"output\"], str), g[\"dataset\"]\n            assert not ({\"split\", \"dataset\", \"context\"} & set(e)), g[\"dataset\"]\n    out = {\"metadata\": {\n        \"artifact\": \"T7b name-free labels for free-vocabulary rule translations (run_u75jRHUss0zo, iter 4, gen_art_dataset_5)\",\n        \"workspace\": str(ROOT),\n        \"selection\": (\"the three plan groups (chosen as best 3 of 6 standardised candidates; folio / malls_test / \"\n                      \"logicnli_test were context only: no multi-system candidates, ~36-39% wrong gold, or no FOL; their \"\n                      \"standardised record is temp/candidates_data_out.json)\"),\n        \"label_mode\": seal[\"mode\"],\n        \"status_note\": (\"SEARCH-ONLY labels: the paid gloss step could not run (deviation D9: run OpenRouter budget \"\n                        \"exhausted before this artifact's first call; re-probed at packaging, still HTTP 403). ERROR_CERT is \"\n                        \"final and certificate-backed; MAPPED rows are UNRESOLVED_GLOSS_NOT_RUN until src/resume_gloss.py \"\n                        \"runs. metadata_label_binary_search_provisional (ERROR vs MAPPED) is a provisional view with audited \"\n                        \"contamination (results/soundness_audit.json).\"),\n        \"seal_all_rows_sha256\": seal[\"label_vector_sha256_all_rows\"],\n        \"seal_untouched_sha256\": seal.get(\"label_vector_sha256_untouched\"),\n        \"prereg_sha256\": seal[\"prereg_sha256\"],\n        \"testability_all_rows\": {k: t[\"all_rows\"][k] for k in (\"n_ERROR\", \"n_CORRECT\", \"TESTABLE\", \"label_counts\")},\n        \"testability_untouched\": {k: t[\"untouched_subset\"][k] for k in (\"n_ERROR\", \"n_CORRECT\", \"TESTABLE\", \"label_counts\")},\n        \"provisional_view_testable\": {k: t[\"search_provisional_view\"][k][\"TESTABLE\"] for k in (\"all_rows\", \"untouched_subset\")},\n    }, \"datasets\": [g for g in groups if g[\"dataset\"] in SELECTED]}\n    (ROOT / \"demo_data_out.json\").write_text(json.dumps(out, ensure_ascii=False))  # original: full_data_out.json\n    logger.info(f\"demo_data_out.json: {[(g['dataset'], len(g['examples'])) for g in out['datasets']]}\")\n    return out\n\n\nout = main()\nprint(json.dumps({k: out[\"metadata\"][k] for k in (\"label_mode\", \"testability_all_rows\", \"provisional_view_testable\")}, indent=1))\n\"\"\")\n\nmd(r\"\"\"\n## Inspect a few rows\nEach `input` string is decoded to show the sentence, the free-vocabulary candidate and the label. For MAPPED rows the **map certificate** is printed as well: the candidate symbols mapped onto phrases of the reference reading, plus any bridges used. For ERROR_CERT rows the output shows how the non-equivalent maps were ruled out.\n\"\"\")\n\ncode(r\"\"\"\nex = out[\"datasets\"][0][\"examples\"]\nshown = Counter()\nfor e in ex:\n    if shown[e[\"output\"]] >= 1 or sum(shown.values()) >= N_SHOW:\n        continue\n    shown[e[\"output\"]] += 1\n    inp = json.loads(e[\"input\"])\n    print(\"=\" * 100)\n    print(f\"LABEL: {e['output']}   system: {inp['system']}   clause: {e['metadata_clause_type']}   words: {e['metadata_words']}\")\n    print(\"TEXT :\", inp[\"text\"])\n    print(\"FOL  :\", inp[\"candidate_fol\"])\n    if e[\"metadata_map_certificate\"]:\n        c = e[\"metadata_map_certificate\"]\n        print(f\"MAP  : reading={c['reading']} bridges={c['bridges']}\")\n        for m in c[\"map\"]:\n            print(\"       \", m)\n        print(f\"       {e['metadata_n_equiv_maps']} equivalent maps in {e['metadata_n_equiv_map_orbits']} orbits \"\n              f\"(of {e['metadata_n_maps_enumerated']} enumerated)\")\n    if e[\"metadata_nonequiv_certificate_type_counts\"]:\n        print(\"NON-EQUIV CERTS:\", e[\"metadata_nonequiv_certificate_type_counts\"])\n    if e[\"metadata_unresolved_reason\"]:\n        print(\"UNRESOLVED:\", e[\"metadata_unresolved_reason\"])\n\"\"\")\n\nmd(r\"\"\"\n## Results: label distribution, strata and search evidence\nThe rows are flattened into a table. The cells below report the following:\n1. Label counts in the demo subset next to the full-dataset counts from the seal metadata.\n2. The ERROR-vs-MAPPED provisional view per clause type and per word tercile (sentence-length bin), which shows how certificate-backed errors spread over sentence complexity.\n3. The ERROR rate per LLM family.\n4. The kinds of non-equivalence certificates, and the bridges used by successful maps.\n\"\"\")\n\ncode(r\"\"\"\ndf = pd.DataFrame([{**{k[len('metadata_'):]: v for k, v in e.items() if k.startswith('metadata_') and not isinstance(v, (dict, list))},\n                    \"label\": e[\"output\"], \"family\": json.loads(e[\"input\"])[\"family\"]} for e in ex])\n\nfull_counts = out[\"metadata\"][\"testability_all_rows\"][\"label_counts\"]\ntab = pd.DataFrame({\"demo_subset\": df[\"label\"].value_counts(), \"full_dataset\": pd.Series(full_counts)}).fillna(0).astype(int)\nprint(\"Label counts (demo subset is stratified, so proportions differ from the full dataset):\")\nprint(tab.to_string(), \"\\n\")\n\nbin_df = df[df[\"label_binary_search_provisional\"] != \"EXCLUDED\"]\nfor col in (\"clause_type\", \"word_tercile\"):\n    ct = pd.crosstab(bin_df[col], bin_df[\"label_binary_search_provisional\"])\n    ct[\"ERROR_share\"] = (ct.get(\"ERROR\", 0) / ct.sum(axis=1)).round(2)\n    print(f\"Provisional ERROR vs MAPPED by {col}:\")\n    print(ct.to_string(), \"\\n\")\n\ncert_types = Counter()\nbridges = Counter()\nfor e in ex:\n    for k, v in (e[\"metadata_nonequiv_certificate_type_counts\"] or {}).items():\n        cert_types[k] += v\n    if e[\"metadata_map_certificate\"]:\n        bridges.update(e[\"metadata_map_certificate\"].get(\"bridges\") or [\"identity/none\"])\nprint(\"Non-equivalence certificate types (summed over rows):\", dict(cert_types.most_common()))\nprint(\"Bridges used by MAPPED certificates:\", dict(bridges.most_common()))\nprint(f\"Median search time per row: {df['search_secs'].median():.2f}s (max {df['search_secs'].max():.2f}s)\")\n\"\"\")\n\ncode(r\"\"\"\nfig, axes = plt.subplots(2, 2, figsize=(14, 9))\n\n# (a) label counts: demo vs full (normalised)\n(tab / tab.sum()).plot.bar(ax=axes[0, 0], color=[\"#4C72B0\", \"#DD8452\"])\naxes[0, 0].set_title(\"Label share: demo subset vs full dataset\")\naxes[0, 0].set_ylabel(\"share of rows\"); axes[0, 0].tick_params(axis=\"x\", rotation=20)\n\n# (b) provisional ERROR vs MAPPED by clause type\nct = pd.crosstab(bin_df[\"clause_type\"], bin_df[\"label_binary_search_provisional\"])\nct.plot.barh(stacked=True, ax=axes[0, 1], color={\"ERROR\": \"#C44E52\", \"MAPPED\": \"#55A868\"})\naxes[0, 1].set_title(\"Provisional ERROR vs MAPPED by clause type\"); axes[0, 1].set_xlabel(\"rows\")\n\n# (c) ERROR share by LLM family (over ERROR+MAPPED rows)\nfam = pd.crosstab(bin_df[\"family\"], bin_df[\"label_binary_search_provisional\"])\n(fam.get(\"ERROR\", 0) / fam.sum(axis=1)).sort_values().plot.barh(ax=axes[1, 0], color=\"#8172B3\")\naxes[1, 0].set_title(\"ERROR_CERT share by LLM family (ERROR+MAPPED rows)\"); axes[1, 0].set_xlim(0, 1)\n\n# (d) non-equivalence certificate types\nif cert_types:\n    pd.Series(dict(cert_types.most_common())).plot.bar(ax=axes[1, 1], color=\"#937860\", logy=True)\naxes[1, 1].set_title(\"Non-equivalence certificate types (log scale)\"); axes[1, 1].tick_params(axis=\"x\", rotation=30)\n\nplt.tight_layout()\nplt.show()\n\"\"\")\n\nmd(r\"\"\"\n**Reading the results.** `ERROR_CERT` rows come with a proof-style certificate that *no* name-free map rescues the candidate, so they are final relative to the bridge family. `MAPPED` rows are only **provisionally** correct: an audit of the SIG soundness replay showed that 9–10% of known-wrong formulas can be \"rescued\" by a non-identity symbol map. Catching those is the job of the pending gloss check (`src/resume_gloss.py` in the artifact). Because no `CORRECT` class exists yet, AUROC-type evaluations on this dataset are `NOT_TESTABLE`. Only the provisional ERROR-vs-MAPPED view is testable, with about 13% audited contamination on each side.\n\"\"\")\n\nnb = {\"cells\": cells, \"metadata\": {\"kernelspec\": {\"display_name\": \"Python 3\", \"language\": \"python\", \"name\": \"python3\"},\n                                   \"language_info\": {\"name\": \"python\"}}, \"nbformat\": 4, \"nbformat_minor\": 5}\nfor i, c in enumerate(nb[\"cells\"]):\n    c[\"id\"] = f\"cell-{i}\"\nOUT.write_text(json.dumps(nb, indent=1, ensure_ascii=False))\nprint(\"wrote\", OUT)\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [25] TOOL CALL — Bash · 2026-09-25 16:39:42 UTC

```
python3 /tmp/claude-0/-ai-inventor-aii-data-runs-run-An1uy2kF2SjZ-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-Ia-FT284H33j/257e4f52-95ca-458d-82e4-999d69f460e7/scratchpad/make_nb.py && sed -i 's/MAX_EXAMPLES = 100 /MAX_EXAMPLES = 2 /' code_demo.ipynb && grep -c "MAX_EXAMPLES = 2 " code_demo.ipynb && \
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_Ia_FT284H33j-125d92329bed && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_Ia_FT284H33j-125d92329bed/bin/python jupyter ipykernel && time /tmp/aii_nb_test_envs/art_Ia_FT284H33j-125d92329bed/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -20
```

### [26] TOOL RESULT — Bash · 2026-09-25 16:40:02 UTC

```
{"stdout": "wrote /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_Ia_FT284H33j/code_demo.ipynb\n1\n\u001b[32m     70\u001b[39m plot_obj = PLOT_CLASSES[kind](data, **kwargs)\n\u001b[32m---> \u001b[39m\u001b[32m71\u001b[39m \u001b[30;43mplot_obj\u001b[39;49m\u001b[30;43m.\u001b[39;49m\u001b[30;43mgenerate\u001b[39;49m\u001b[30;43m(\u001b[39;49m\u001b[30;43m)\u001b[39;49m\n\u001b[32m     72\u001b[39m plot_obj.draw()\n\u001b[32m     73\u001b[39m \u001b[38;5;28;01mreturn\u001b[39;00m plot_obj.result\n\n\u001b[36mFile \u001b[39m\u001b[32m/tmp/aii_nb_test_envs/art_Ia_FT284H33j-125d92329bed/lib/python3.12/site-packages/pandas/plotting/_matplotlib/core.py:499\u001b[39m, in \u001b[36mMPLPlot.generate\u001b[39m\u001b[34m(self)\u001b[39m\n\u001b[32m    497\u001b[39m \u001b[38;5;129m@final\u001b[39m\n\u001b[32m    498\u001b[39m \u001b[38;5;28;01mdef\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[34mgenerate\u001b[39m(\u001b[38;5;28mself\u001b[39m) -> \u001b[38;5;28;01mNone\u001b[39;00m:\n\u001b[32m--> \u001b[39m\u001b[32m499\u001b[39m     \u001b[30;43mself\u001b[39;49m\u001b[30;43m.\u001b[39;49m\u001b[30;43m_compute_plot_data\u001b[39;49m\u001b[30;43m(\u001b[39;49m\u001b[30;43m)\u001b[39;49m\n\u001b[32m    500\u001b[39m     fig = \u001b[38;5;28mself\u001b[39m.fig\n\u001b[32m    501\u001b[39m     \u001b[38;5;28mself\u001b[39m._make_plot(fig)\n\n\u001b[36mFile \u001b[39m\u001b[32m/tmp/aii_nb_test_envs/art_Ia_FT284H33j-125d92329bed/lib/python3.12/site-packages/pandas/plotting/_matplotlib/core.py:698\u001b[39m, in \u001b[36mMPLPlot._compute_plot_data\u001b[39m\u001b[34m(self)\u001b[39m\n\u001b[32m    696\u001b[39m \u001b[38;5;66;03m# no non-numeric frames or series allowed\u001b[39;00m\n\u001b[32m    697\u001b[39m \u001b[38;5;28;01mif\u001b[39;00m is_empty:\n\u001b[32m--> \u001b[39m\u001b[32m698\u001b[39m     \u001b[38;5;28;01mraise\u001b[39;00m \u001b[38;5;167;01mTypeError\u001b[39;00m(\u001b[33m\"\u001b[39m\u001b[33mno numeric data to plot\u001b[39m\u001b[33m\"\u001b[39m)\n\u001b[32m    700\u001b[39m \u001b[38;5;28mself\u001b[39m.data = numeric_data.apply(\u001b[38;5;28mtype\u001b[39m(\u001b[38;5;28mself\u001b[39m)._convert_to_ndarray)\n\n\u001b[31mTypeError\u001b[39m: no numeric data to plot\n\n\nreal\t0m15.908s\nuser\t0m12.411s\nsys\t0m1.029s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [27] ASSISTANT · 2026-09-25 16:40:12 UTC

```
Two rows is too few for the family-share plot: the ERROR column comes back empty. I'll make the crosstabs always include both columns.
```

### [28] TOOL CALL — Bash · 2026-09-25 16:40:12 UTC

```
S=/tmp/claude-0/-ai-inventor-aii-data-runs-run-An1uy2kF2SjZ-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-Ia-FT284H33j/257e4f52-95ca-458d-82e4-999d69f460e7/scratchpad/make_nb.py; python3 - "$S" <<'EOF'
import sys
p=sys.argv[1]; s=open(p).read()
s=s.replace('''    ct = pd.crosstab(bin_df[col], bin_df["label_binary_search_provisional"])
    ct["ERROR_share"] = (ct.get("ERROR", 0) / ct.sum(axis=1)).round(2)''','''    ct = pd.crosstab(bin_df[col], bin_df["label_binary_search_provisional"]).reindex(columns=["ERROR", "MAPPED"], fill_value=0)
    ct["ERROR_share"] = (ct["ERROR"] / ct.sum(axis=1)).round(2)''')
s=s.replace('''ct = pd.crosstab(bin_df["clause_type"], bin_df["label_binary_search_provisional"])
ct.plot''','''ct = pd.crosstab(bin_df["clause_type"], bin_df["label_binary_search_provisional"]).reindex(columns=["ERROR", "MAPPED"], fill_value=0)
ct.plot''')
s=s.replace('''fam = pd.crosstab(bin_df["family"], bin_df["label_binary_search_provisional"])
(fam.get("ERROR", 0) / fam.sum(axis=1))''','''fam = pd.crosstab(bin_df["family"], bin_df["label_binary_search_provisional"]).reindex(columns=["ERROR", "MAPPED"], fill_value=0)
(fam["ERROR"] / fam.sum(axis=1)).astype(float)''')
open(p,'w').write(s)
EOF
grep -c reindex $S
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_Ia_FT284H33j && python3 $S && sed -i 's/MAX_EXAMPLES = 100 /MAX_EXAMPLES = 2 /' code_demo.ipynb && \
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_Ia_FT284H33j-125d92329bed && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_Ia_FT284H33j-125d92329bed/bin/python jupyter ipykernel && time /tmp/aii_nb_test_envs/art_Ia_FT284H33j-125d92329bed/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -5
```

### [29] TOOL RESULT — Bash · 2026-09-25 16:40:28 UTC

```
{"stdout": "3\nwrote /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_Ia_FT284H33j/code_demo.ipynb\n\u001b[32m   1967\u001b[39m e_edge = \u001b[38;5;28mself\u001b[39m.ax_pos[-\u001b[32m1\u001b[39m] + \u001b[32m0.25\u001b[39m + \u001b[38;5;28mself\u001b[39m.bar_width + \u001b[38;5;28mself\u001b[39m.lim_offset\n\u001b[32m   1969\u001b[39m \u001b[38;5;28mself\u001b[39m._decorate_ticks(ax, \u001b[38;5;28mself\u001b[39m._get_index_name(), str_index, s_edge, e_edge)\n\n\u001b[31mIndexError\u001b[39m: index 0 is out of bounds for axis 0 with size 0\n\n\nreal\t0m14.622s\nuser\t0m12.209s\nsys\t0m0.912s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [30] ASSISTANT · 2026-09-25 16:40:40 UTC

```
Next failure: with 2 rows, the ERROR-vs-MAPPED table can be empty. I'll only draw those two panels when it has rows.
```

### [31] TOOL CALL — Bash · 2026-09-25 16:40:40 UTC

```
S=/tmp/claude-0/-ai-inventor-aii-data-runs-run-An1uy2kF2SjZ-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-Ia-FT284H33j/257e4f52-95ca-458d-82e4-999d69f460e7/scratchpad/make_nb.py; python3 - "$S" <<'EOF'
import sys
p=sys.argv[1]; s=open(p).read()
old_b='''ct = pd.crosstab(bin_df["clause_type"], bin_df["label_binary_search_provisional"]).reindex(columns=["ERROR", "MAPPED"], fill_value=0)
ct.plot.barh(stacked=True, ax=axes[0, 1], color={"ERROR": "#C44E52", "MAPPED": "#55A868"})'''
new_b='''if len(bin_df):  # needs at least one ERROR/MAPPED row
    ct = pd.crosstab(bin_df["clause_type"], bin_df["label_binary_search_provisional"]).reindex(columns=["ERROR", "MAPPED"], fill_value=0)
    ct.plot.barh(stacked=True, ax=axes[0, 1], color={"ERROR": "#C44E52", "MAPPED": "#55A868"})'''
old_c='''fam = pd.crosstab(bin_df["family"], bin_df["label_binary_search_provisional"]).reindex(columns=["ERROR", "MAPPED"], fill_value=0)
(fam["ERROR"] / fam.sum(axis=1)).astype(float).sort_values().plot.barh(ax=axes[1, 0], color="#8172B3")'''
new_c='''if len(bin_df):
    fam = pd.crosstab(bin_df["family"], bin_df["label_binary_search_provisional"]).reindex(columns=["ERROR", "MAPPED"], fill_value=0)
    (fam["ERROR"] / fam.sum(axis=1)).astype(float).sort_values().plot.barh(ax=axes[1, 0], color="#8172B3")'''
assert old_b in s and old_c in s
s=s.replace(old_b,new_b).replace(old_c,new_c)
open(p,'w').write(s)
EOF
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_Ia_FT284H33j && python3 $S && sed -i 's/MAX_EXAMPLES = 100 /MAX_EXAMPLES = 2 /' code_demo.ipynb && \
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_Ia_FT284H33j-125d92329bed && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_Ia_FT284H33j-125d92329bed/bin/python jupyter ipykernel && time /tmp/aii_nb_test_envs/art_Ia_FT284H33j-125d92329bed/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -5
```

### [32] TOOL RESULT — Bash · 2026-09-25 16:40:56 UTC

```
{"stdout": "wrote /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_Ia_FT284H33j/code_demo.ipynb\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n[NbConvertApp] Writing 126711 bytes to code_demo.ipynb\n\nreal\t0m14.535s\nuser\t0m12.119s\nsys\t0m0.922s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [33] ASSISTANT · 2026-09-25 16:41:02 UTC

```
The notebook passes with 2 rows in 15 s. Now scaling up: 25 rows, then the full 100-row subset.
```

### [34] TOOL CALL — Bash · 2026-09-25 16:41:02 UTC

```
S=/tmp/claude-0/-ai-inventor-aii-data-runs-run-An1uy2kF2SjZ-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-Ia-FT284H33j/257e4f52-95ca-458d-82e4-999d69f460e7/scratchpad/make_nb.py; E=/tmp/aii_nb_test_envs/art_Ia_FT284H33j-125d92329bed
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_Ia_FT284H33j
for N in 25 100; do python3 $S >/dev/null && sed -i "s/MAX_EXAMPLES = 100 /MAX_EXAMPLES = $N /" code_demo.ipynb && grep -o "MAX_EXAMPLES = [0-9]* " code_demo.ipynb | head -1 && \
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 $E && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python $E/bin/python jupyter ipykernel && /usr/bin/time -f "N=$N %es" $E/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -2; done
```

### [35] TOOL RESULT — Bash · 2026-09-25 16:41:04 UTC

```
{"stdout": "MAX_EXAMPLES = 25 \n/bin/bash: line 7: /usr/bin/time: No such file or directory\nMAX_EXAMPLES = 100 \n/bin/bash: line 7: /usr/bin/time: No such file or directory", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [36] TOOL CALL — Bash · 2026-09-25 16:41:08 UTC

```
E=/tmp/aii_nb_test_envs/art_Ia_FT284H33j-125d92329bed
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_Ia_FT284H33j
for N in 25 100; do sed -i -E "s/MAX_EXAMPLES = [0-9]+ /MAX_EXAMPLES = $N /" code_demo.ipynb; grep -o "MAX_EXAMPLES = [0-9]* " code_demo.ipynb | head -1
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 $E && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python $E/bin/python jupyter ipykernel
s=$(date +%s); $E/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -1; echo "N=$N $(( $(date +%s)-s ))s"; done
```

### [37] TOOL RESULT — Bash · 2026-09-25 16:41:40 UTC

```
{"stdout": "MAX_EXAMPLES = 25 \n[NbConvertApp] Writing 180518 bytes to code_demo.ipynb\nN=25 15s\nMAX_EXAMPLES = 100 \n[NbConvertApp] Writing 195967 bytes to code_demo.ipynb\nN=100 15s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [38] ASSISTANT · 2026-09-25 16:41:48 UTC

```
Both runs pass in about 15 s. Now checking the executed outputs and the plot.
```

### [39] TOOL CALL — Bash · 2026-09-25 16:41:48 UTC

```
python3 - <<'EOF'
import json,base64
nb=json.load(open("code_demo.ipynb"))
for i,c in enumerate(nb["cells"]):
    if c["cell_type"]!="code": continue
    for o in c["outputs"]:
        if o.get("output_type")=="error": print("ERR",i,o["ename"])
        t=o.get("text") or o.get("data",{}).get("text/plain")
        if t and i>=12: print(f"--- cell {i}\n", "".join(t)[:2500])
        if "image/png" in o.get("data",{}): open("/tmp/claude-0/-ai-inventor-aii-data-runs-run-An1uy2kF2SjZ-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-Ia-FT284H33j/257e4f52-95ca-458d-82e4-999d69f460e7/scratchpad/fig.png","wb").write(base64.b64decode(o["data"]["image/png"]))
EOF
grep -c 'GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_An1uy2kF2SjZ/round-4/dataset-5/demo/mini_demo_data.json"' code_demo.ipynb; ls -la
```

### [40] TOOL RESULT — Bash · 2026-09-25 16:41:48 UTC

```
{"stdout": "--- cell 12\n {'rcomp_free_labels': 100}\n\n--- cell 14\n 16:41:38|INFO   |demo_data_out.json: [('rcomp_free_labels', 100)]\n\n--- cell 14\n {\n \"label_mode\": \"search_only\",\n \"testability_all_rows\": {\n  \"n_ERROR\": 759,\n  \"n_CORRECT\": 0,\n  \"TESTABLE\": false,\n  \"label_counts\": {\n   \"ERROR_CERT\": 759,\n   \"UNRESOLVED_GLOSS_NOT_RUN\": 1506,\n   \"UNPARSEABLE\": 188,\n   \"NO_OUTPUT\": 199\n  }\n },\n \"provisional_view_testable\": {\n  \"all_rows\": true,\n  \"untouched_subset\": true\n }\n}\n\n--- cell 16\n ====================================================================================================\nLABEL: NO_OUTPUT   system: G2:qwen/qwen3-235b-a22b-2507   clause: but_only_if   words: 44\nTEXT : If an artificial satellite is built by Carrozzeria Colli, has a built-in infuser, and is designed for traveling on ice, then the artificial satellite gathers light through a lens or a mirror, but only if the artificial satellite stores energy in an electric field.\nFOL  : \n====================================================================================================\nLABEL: UNPARSEABLE   system: G4:deepseek/deepseek-v3.2   clause: except_when+provided_that   words: 33\nTEXT : Except if the democratic election is brain image acquisition, each democratic election that has a legal dispute and that releases heat is considered spontaneous, provided that the democratic election involves two opposing teams.\nFOL  : ∀x ((DemocraticElection(x) ∧ Has(x, legalDispute) ∧ Releases(x, heat) ∧ Involves(x, twoOpposingTeams) ∧ ¬(x = brainImageAcquisition)) → Considered(x, spontaneous))\n====================================================================================================\nLABEL: ERROR_CERT   system: G7:openai/gpt-4.1-mini   clause: as_long_as+unless   words: 30\nTEXT : A wetland that is not by Phoenix and that receives voice and data follows the scientific method as long as the wetland orbits a star, unless the wetland boils water.\nFOL  : ∀x ((Wetland(x) ∧ ¬By(x, phoenix) ∧ Receives(x, voice) ∧ Receives(x, data) ∧ Orbits(x, star) ∧ ¬Boils(x, water)) → Follows(x, scientificMethod))\nNON-EQUIV CERTS: {'no_polarity_compatible_target': 4}\n\n--- cell 18\n Label counts (demo subset is stratified, so proportions differ from the full dataset):\n                          demo_subset  full_dataset\nERROR_CERT                         40           759\nNO_OUTPUT                          10           199\nUNPARSEABLE                        10           188\nUNRESOLVED_GLOSS_NOT_RUN           40          1506 \n\nProvisional ERROR vs MAPPED by clause_type:\nlabel_binary_search_provisional  ERROR  MAPPED  ERROR_share\nclause_type                                                \nas_long_as+unless                    7       4         0.64\nbut_only_if                          4       5         0.44\nexcept_when                          6       7         0.46\nexcept_when+provided_that            4       6         0.40\nprovided_that                        7       7         0.50\nprovided_that+unless                 5       5         0.50\nunless                               7       6         0.54 \n\nProvisional ERROR vs MAPPED by word_tercile:\nlabel_binary_search_provisional  ERROR  MAPPED  ERROR_share\nword_tercile                                               \nW1                                   8      11         0.42\nW2                                  16      23         0.41\nW3                                  16       6         0.73 \n\nNon-equivalence certificate types (summed over rows): {'count_prune_subtree': 15091, 'countermodel': 2172, 'no_polarity_compatible_target': 406, 'z3_sat': 120, 'unmappable_symbol': 6}\nBridges used by MAPPED certificates: {'B2': 43, 'B1': 19, 'identity/none': 9, 'B5': 4, 'B4': 2, 'B3': 1}\nMedian search time per row: 0.22s (max 3.36s)\n\n--- cell 19\n <Figure size 1400x900 with 4 Axes>\n0\ntotal 5015\ndrwxr-xr-x  4 root root 2000103 Sep 25 16:41 .\ndrwxr-xr-x  7 root root 2000371 Sep 25 16:37 ..\ndrwxr-xr-x  2 root root       1 Sep 25 16:36 .aii\n-rw-------  1 root root      54 Sep 25 16:37 .aii_claude_session.json\n-rw-r--r--  1 root root  279013 Sep 25 16:41 .repl_agent.ptylog\n-rw-r--r--+ 1 root root  196016 Sep 25 16:41 code_demo.ipynb\n-rw-r--r--  1 root root  274866 Sep 25 16:41 demo_data_out.json\ndrwxr-xr-x  2 root root   51800 Sep 25 16:39 logs\n-rw-r--r--  1 root root  332810 Sep 25 16:38 mini_demo_data.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [41] THINKING · 2026-09-25 16:42:02 UTC

```
Everything runs, but two fixes remain: I'll adjust the inspection cell to display a MAPPED row with its certificate first, and switch the exact-URL check to Python since the grep returned 0 due to JSON-escaped quotes.
```

### [42] TOOL CALL — Bash · 2026-09-25 16:42:02 UTC

```
S=/tmp/claude-0/-ai-inventor-aii-data-runs-run-An1uy2kF2SjZ-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-Ia-FT284H33j/257e4f52-95ca-458d-82e4-999d69f460e7/scratchpad/make_nb.py; python3 - "$S" <<'EOF'
import sys
p=sys.argv[1]; s=open(p).read()
old='''shown = Counter()
for e in ex:
    if shown[e["output"]] >= 1 or sum(shown.values()) >= N_SHOW:
        continue
    shown[e["output"]] += 1
    inp'''
new='''# one row per label, MAPPED (with a certificate) first, then ERROR_CERT, UNPARSEABLE, NO_OUTPUT
order = ["UNRESOLVED_GLOSS_NOT_RUN", "ERROR_CERT", "UNPARSEABLE", "NO_OUTPUT"]
picked = [next(e for e in ex if e["output"] == lab) for lab in order if any(e["output"] == lab for e in ex)][:N_SHOW]
for e in picked:
    inp'''
assert old in s; s=s.replace(old,new); open(p,'w').write(s)
EOF
E=/tmp/aii_nb_test_envs/art_Ia_FT284H33j-125d92329bed
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_Ia_FT284H33j && python3 $S && rm -rf logs demo_data_out.json && \
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 $E && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python $E/bin/python jupyter ipykernel && s=$(date +%s) && $E/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -1; echo "$(( $(date +%s)-s ))s"
python3 - <<'EOF'
import json,base64
nb=json.load(open("code_demo.ipynb"))
src="\n".join(c["source"] if isinstance(c["source"],str) else "".join(c["source"]) for c in nb["cells"])
print("URL exact:", 'GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_An1uy2kF2SjZ/round-4/dataset-5/demo/mini_demo_data.json"' in src, "urlopen" in src)
print("errors:", [o["ename"] for c in nb["cells"] if c["cell_type"]=="code" for o in c["outputs"] if o.get("output_type")=="error"])
c=nb["cells"][16]; print("".join(o.get("text","") for o in c["outputs"])[:1800])
for o in nb["cells"][19]["outputs"]:
    if "image/png" in o.get("data",{}): open("/tmp/claude-0/-ai-inventor-aii-data-runs-run-An1uy2kF2SjZ-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-Ia-FT284H33j/257e4f52-95ca-458d-82e4-999d69f460e7/scratchpad/fig.png","wb").write(base64.b64decode(o["data"]["image/png"]))
EOF
```

### [43] TOOL RESULT — Bash [ERROR] · 2026-09-25 16:42:18 UTC

```
Error: Exit code 1
wrote /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_Ia_FT284H33j/code_demo.ipynb
[NbConvertApp] Writing 196786 bytes to code_demo.ipynb
14s
URL exact: True True
errors: []
Traceback (most recent call last):
  File "<stdin>", line 6, in <module>
TypeError: sequence item 0: expected str instance, list found
```

### [44] TOOL CALL — Bash · 2026-09-25 16:42:24 UTC

```
python3 - <<'EOF'
import json,base64
nb=json.load(open("code_demo.ipynb"))
c=nb["cells"][16]; print("".join("".join(o.get("text","")) for o in c["outputs"])[:2000])
for o in nb["cells"][19]["outputs"]:
    if "image/png" in o.get("data",{}): open("/tmp/claude-0/-ai-inventor-aii-data-runs-run-An1uy2kF2SjZ-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-Ia-FT284H33j/257e4f52-95ca-458d-82e4-999d69f460e7/scratchpad/fig.png","wb").write(base64.b64decode(o["data"]["image/png"]))
EOF
```

### [45] TOOL RESULT — Bash · 2026-09-25 16:42:24 UTC

```
{"stdout": "====================================================================================================\nLABEL: UNRESOLVED_GLOSS_NOT_RUN   system: G6:microsoft/phi-4   clause: as_long_as+unless   words: 31\nTEXT : A flower that is peer-reviewed and that exceeds its elastic limit has a battery storage system so long as the flower is in an urban area, unless the flower is addictive.\nFOL  : ∀x ((Flower(x) ∧ PeerReviewed(x) ∧ ExceedsElasticLimit(x) ∧ InUrbanArea(x) ∧ ¬Addictive(x)) → HasBatteryStorageSystem(x))\nMAP  : reading=weak bridges=[]\n        Addictive(x) => Addictive(x)\n        ExceedsElasticLimit(x) => ExceedsElasticLimit(x)\n        Flower(x) => Flower(x)\n        HasBatteryStorageSystem(x) => HasBatteryStorageSystem(x)\n        InUrbanArea(x) => InUrbanArea(x)\n        PeerReviewed(x) => PeerReviewed(x)\n       48 equivalent maps in 1 orbits (of 48 enumerated)\nNON-EQUIV CERTS: {'count_prune_subtree': 291, 'no_polarity_compatible_target': 10}\nUNRESOLVED: gloss check not run (D9: API budget exhausted)\n====================================================================================================\nLABEL: ERROR_CERT   system: G7:openai/gpt-4.1-mini   clause: as_long_as+unless   words: 30\nTEXT : A wetland that is not by Phoenix and that receives voice and data follows the scientific method as long as the wetland orbits a star, unless the wetland boils water.\nFOL  : ∀x ((Wetland(x) ∧ ¬By(x, phoenix) ∧ Receives(x, voice) ∧ Receives(x, data) ∧ Orbits(x, star) ∧ ¬Boils(x, water)) → Follows(x, scientificMethod))\nNON-EQUIV CERTS: {'no_polarity_compatible_target': 4}\n====================================================================================================\nLABEL: UNPARSEABLE   system: G4:deepseek/deepseek-v3.2   clause: except_when+provided_that   words: 33\nTEXT : Except if the democratic election is brain image acquisition, each democratic election that has a legal dispute and that releases heat is considered spontaneous, provided that the democratic election involv", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [46] TOOL CALL — Read · 2026-09-25 16:42:24 UTC

```
/tmp/claude-0/-ai-inventor-aii-data-runs-run-An1uy2kF2SjZ-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-Ia-FT284H33j/257e4f52-95ca-458d-82e4-999d69f460e7/scratchpad/fig.png
```

### [47] TOOL RESULT — Read · 2026-09-25 16:42:24 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [48] ASSISTANT · 2026-09-25 16:42:34 UTC

```
The figure looks right. One cosmetic fix: the legend overlaps the clause-type bars, so I'll move it. Then a final re-run, the README and the manifest.
```

### [49] TOOL CALL — Bash · 2026-09-25 16:42:34 UTC

```
S=/tmp/claude-0/-ai-inventor-aii-data-runs-run-An1uy2kF2SjZ-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-Ia-FT284H33j/257e4f52-95ca-458d-82e4-999d69f460e7/scratchpad/make_nb.py; python3 - "$S" <<'EOF'
import sys
p=sys.argv[1]; s=open(p).read()
old='''    ct.plot.barh(stacked=True, ax=axes[0, 1], color={"ERROR": "#C44E52", "MAPPED": "#55A868"})'''
new=old+'''
    axes[0, 1].legend(loc="lower right", fontsize=8)'''
assert old in s; s=s.replace(old,new); open(p,'w').write(s)
EOF
E=/tmp/aii_nb_test_envs/art_Ia_FT284H33j-125d92329bed
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_Ia_FT284H33j && python3 $S && rm -rf logs demo_data_out.json && \
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 $E && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python $E/bin/python jupyter ipykernel && s=$(date +%s) && $E/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -1; echo "$(( $(date +%s)-s ))s"
python3 -c "
import json;nb=json.load(open('code_demo.ipynb'));print([o['ename'] for c in nb['cells'] if c['cell_type']=='code' for o in c['outputs'] if o.get('output_type')=='error'])"; du -sh * .[a-z]* 2>/dev/null
```

### [50] TOOL RESULT — Bash · 2026-09-25 16:42:50 UTC

```
{"stdout": "wrote /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_Ia_FT284H33j/code_demo.ipynb\n[NbConvertApp] Writing 191502 bytes to code_demo.ipynb\n15s\n[]\n188K\tcode_demo.ipynb\n269K\tdemo_data_out.json\n11K\tlogs\n326K\tmini_demo_data.json\n512\t.aii\n512\t.aii_claude_session.json\n339K\t.repl_agent.ptylog", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [51] ASSISTANT · 2026-09-25 16:43:00 UTC

```
Final run passes with no errors in 15 s. Writing the README, manifest and structured output.
```

### [52] TOOL CALL — Bash · 2026-09-25 16:43:00 UTC

````
cat > .aii/manifest.yaml <<'EOF'
# Nothing in this workspace is heavy (all files are small text/JSON/notebook, < 1 MB total).
entries: []
EOF
cat > README.md <<'EOF'
# Demo: name-free labels for free-vocabulary NL→FOL translations

A runnable Colab-compatible walkthrough of the dataset artifact *"Name-free labels for free-vocabulary logic
translations"* (T7b, `rcomp_free_labels`). The artifact labels 2,652 LLM-produced FOL translations of 221 templated
rule sentences **without relying on symbol names**. An exhaustive, certificate-backed search looks for a symbol map
(injective maps plus reification, merge, split and lexical-negation bridges; z3 equivalence) onto a reference reading.
The labels are search-only. `ERROR_CERT` is final. `UNRESOLVED_GLOSS_NOT_RUN` means the candidate is z3-equivalent under some map, but the gloss check
has not run yet. The other labels are `UNPARSEABLE` and `NO_OUTPUT`.

The notebook keeps the artifact's `data.py` logic (validate groups → build metadata/seal block → write output). It runs
that logic on a curated 100-row subset, then inspects decoded rows and plots the labels by clause type, LLM family and
non-equivalence certificate type.

## Layout
| path | what |
|---|---|
| `code_demo.ipynb` | the demo notebook (executed; runs in ~15 s) |
| `mini_demo_data.json` | 100 of 2,652 `rcomp_free_labels` rows (40 ERROR_CERT / 40 UNRESOLVED / 10 UNPARSEABLE / 10 NO_OUTPUT, stratified by clause type × LLM family, seed 0) plus the full-dataset metadata (seal hashes, testability) |
| `demo_data_out.json` | written by the notebook: the re-assembled `exp_sel_data_out` file for the demo subset |
| `logs/data.log` | loguru log written by the notebook |

## Run
Open `code_demo.ipynb` in Colab or Jupyter and run all cells. The data loads from the GitHub raw URL, or from the local
`mini_demo_data.json` if the URL is unreachable. To test it headless:
```bash
jupyter nbconvert --to notebook --execute code_demo.ipynb --output code_demo.ipynb
```
`MAX_EXAMPLES` in the config cell controls how many rows are processed (max 100 here; the full dataset has 2,652).

## Restoring removed files
Nothing is marked for deletion (`.aii/manifest.yaml` has no entries). `demo_data_out.json` and `logs/` are regenerated
by running the notebook.
EOF
cat > .terminal_claude_agent_struct_out.json <<'EOF'
{"out_expected_files": {"notebook": "code_demo.ipynb", "mini_data_file": "mini_demo_data.json"}}
EOF
cat .terminal_claude_agent_struct_out.json
````

### [53] TOOL RESULT — Bash · 2026-09-25 16:43:00 UTC

```
{"stdout": "{\"out_expected_files\": {\"notebook\": \"code_demo.ipynb\", \"mini_data_file\": \"mini_demo_data.json\"}}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [54] ASSISTANT · 2026-09-25 16:43:10 UTC

```
I've built the demo notebook and its data subset. The notebook runs cleanly in the fresh Colab-matched test environment, in about 15 seconds.

**`mini_demo_data.json`** holds 100 of the 2,652 rows from the `rcomp_free_labels` group only. It has 40 `ERROR_CERT`, 40 `UNRESOLVED_GLOSS_NOT_RUN`, 10 `UNPARSEABLE` and 10 `NO_OUTPUT` rows, spread across clause types and all 9 LLM families (seed 0). It keeps the full dataset's metadata: seal hashes and testability counts.

**`code_demo.ipynb`** keeps the original `data.py` code and adds markdown between the sections. Four things differ from the original:
- **Row source:** rows come from the loaded data instead of `import build_output as B; B.free_group()…`. A comment in the cell shows the original line.
- **Seal and testability:** the original read these from `results/seal.json` and `results/testability_FREE_v2.json`. The notebook rebuilds the same dictionaries from the shipped metadata, so `main()`'s checks and output-building code are otherwise unchanged.
- **Output file:** it writes `demo_data_out.json` instead of overwriting `full_data_out.json`.
- **Added at the end:** a cell that decodes one row of each label (a MAPPED row with its symbol map, an `ERROR_CERT` row with its certificate counts), summary tables by clause type and sentence length, and a 4-panel figure.

**Scaling:** I ran it with 2, then 25, then 100 rows (`MAX_EXAMPLES`). Every run took about 15 seconds, so the final setting is the whole 100-row subset. The comment in the config cell gives the original size (2,652 rows, plus 840 gloss-gate and 4,280 SIG rows in the other two groups).

**What the 100 rows show:** in the longest sentences (top word tercile), 73% of the rows that reached a verdict are `ERROR_CERT`, against about 41% in the other two terciles. This is a stratified sample of 22 rows in that tercile, so treat it as illustrative only.

**Checks:** the notebook contains the exact `GITHUB_DATA_URL` and uses the download-with-local-fallback loader. That URL won't work until the files are pushed, so the test runs used the local copy.

I didn't use a todo-tracking tool because none was available here, and I generated the notebook with a Python script rather than NotebookEdit. I also wrote `README.md`. `.aii/manifest.yaml` has no entries because nothing in the workspace is large.

Files are in `art_Ia_FT284H33j/`:
- `code_demo.ipynb`
- `mini_demo_data.json`
- `README.md`
- `.aii/manifest.yaml`
- `.terminal_claude_agent_struct_out.json`
```
