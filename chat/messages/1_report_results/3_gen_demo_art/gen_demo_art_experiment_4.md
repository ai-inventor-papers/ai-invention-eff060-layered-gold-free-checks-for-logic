# gen_demo_art_experiment_4 — report_results

> Phase: `gen_paper_repo` · `gen_demo_art`
> Run: `gen_paper_repo_a2e1d024cc16` — Cross-Family Solver Consensus as a Gold-Free Faithfulness Metric for Logic Translation
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_demo_art_experiment_4` (terminal_claude_agent, claude-opus-5-5)

### [1] CONFIG · 2026-09-25 16:10:25 UTC

```
model: claude-opus-5-5 | effort: high | permission: bypassPermissions
```

### [2] SYSTEM-USER prompt · 2026-09-25 16:10:31 UTC

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
Your workspace: `/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_2/art_TaxJRnPcJMuZ`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_2/art_TaxJRnPcJMuZ/`:
GOOD: `/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_2/art_TaxJRnPcJMuZ/file.py`, `/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_2/art_TaxJRnPcJMuZ/results/out.json`
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
id: art_TaxJRnPcJMuZ
type: experiment
title: Peer agreement plus text checks, held-out test
summary: >-
  Held-out confirmation of PEER+TEXT (NL->FOL faithfulness without gold) on dataset E (8,507 candidate rows, 700 sentences),
  frozen on the iteration-1 screen (prereg sha256 b9f28b1b, git a6896ce) and scored once. PEER = graded cross-family consensus
  (claim units, peer aligned into candidate vocabulary, finite-model refuter + z3 entailment; support/coverage/g_score, unit
  error codes); TEXT = iteration-1 L2-bow + L3 (text-only questionnaire vs z3 role profile); fused by a screen-fitted logistic.
  RESULTS (R_AB tiers A+B, 1822 ERR/864 COR): PEER+TEXT AUROC .790 [.75,.82] (stratified .753; long pool .768; tier-A L20+EXC
  .818) vs iteration-1 c_score_align .782, NF-anchored c_score .743, TEXT .693, local Qwen3-8B disguised judge .712. Delta
  vs local judge +.078 [.043,.112] pooled, +.115 long pool, +.075 stratified; CTRL -.031 n.s. The pre-registered flash-lite
  judge bar is UNTESTABLE (shared OpenRouter key hit $0 at 18:00 UTC; the replacement key was also exhausted, polled 19:10-22:13
  UTC; 20 rows); the local judge is a labelled secondary bar. Fusion does NOT beat c_score_align alone (stratified +.011 n.s.;
  tier A c_score_align .860 > .818), and that aligner is shared with the solver labeller (confound open). Name-free alignment
  'failed' the screen gate only through a threshold-tie artefact; post hoc NF-anchored passes (RENAME FA .074, ROLE_PERMUTE
  recall .77) and its fusion gives .759 on E. P1 INCONCLUSIVE (PEER>TEXT on ADD/DROP errors, TEXT>PEER on peer-endorsed),
  P2 REFUTED, P3 INCONCLUSIVE (gap vs judge grows with length, diff-in-delta +.146 CI>0), P4 REFUTED (fused RENAME FA .385).
  Unit-code typing at chance (.37 vs .38). Disguise improves the judge (no contamination benefit). Within-stratum placebo
  .59 (composition), global .50. FILES: results/per_item_E.jsonl (row_key=item_id|prompt_variant, fold_E=sha1('E_folds_v1|'+sid)%5,
  every score) for the iteration-3 join; results/analysis.json, tables.md, p_tests.json, deviations.json, prereg.json; src/peer_text.py
  reusable functions; method_out.json (exp_gen_sol_out, predict_* for all metrics). Audits: tests/audit_rederive.py re-derives
  pooled AUROCs and headline delta to 1e-9; tests/placebo_headline.py (shuffled labels fail); prefilter audit 0 conflicts;
  judge prompt identity 30/30. OpenRouter spend $0.155.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json
out_demo_files:
- path: method.py
  description: Research methodology implementation
</artifact_info>

<github_repo>
Repo URL: https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic
Raw data URL: https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_An1uy2kF2SjZ/round-2/experiment-5/demo/mini_demo_data.json

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
GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_An1uy2kF2SjZ/round-2/experiment-5/demo/mini_demo_data.json"
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
To test-run the notebook in a clean environment (simulating Colab), use the disposable venv at `/tmp/aii_nb_test_envs/art_TaxJRnPcJMuZ-7aa3e4ae5ffc`. It is on this machine's local disk, outside your workspace, which is on a slow network volume: never create a venv inside your workspace.
```bash
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_TaxJRnPcJMuZ-7aa3e4ae5ffc
UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_TaxJRnPcJMuZ-7aa3e4ae5ffc/bin/python jupyter ipykernel
/tmp/aii_nb_test_envs/art_TaxJRnPcJMuZ-7aa3e4ae5ffc/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb
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
TODO 6. Verify: (1) code_demo.ipynb contains GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_An1uy2kF2SjZ/round-2/experiment-5/demo/mini_demo_data.json" exactly, (2) mini_demo_data.json exists, (3) uses GitHub URL pattern not just open('mini_demo_data.json').
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

### [3] HUMAN-USER prompt · 2026-09-25 16:10:31 UTC

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

### [4] ASSISTANT · 2026-09-25 16:10:39 UTC

```
I'll start by loading the required skills and inspecting the artifact.
```

### [5] TOOL CALL — Skill · 2026-09-25 16:10:39 UTC

```
aii-colab
```

### [6] TOOL CALL — Skill · 2026-09-25 16:10:39 UTC

```
aii-long-running-tasks
```

### [7] TOOL RESULT — Skill · 2026-09-25 16:10:39 UTC

```
{"success": true, "commandName": "aii-colab"}
```

### [8] TOOL RESULT — Skill · 2026-09-25 16:10:39 UTC

```
{"success": true, "commandName": "aii-long-running-tasks"}
```

### [9] TOOL CALL — Bash · 2026-09-25 16:10:39 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5; ls -la $W; ls -la $W/results $W/src $W/tests 2>/dev/null | head -50; wc -l $W/method.py; ls -la /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_2/art_TaxJRnPcJMuZ
```

### [10] TOOL RESULT — Bash · 2026-09-25 16:10:39 UTC

```
{"stdout": "total 62897\ndrwxr-xr-x 10 root   root    2016678 Sep 24 23:21 .\ndrwxr-xr-x  7 root   root    2057101 Sep 23 17:47 ..\ndrwxr-xr-x  2 root   root    1000101 Sep 23 22:21 .aii\n-rw-------  1 root   root         54 Sep 24 23:20 .aii_claude_session.json\n-rw-r--r--  1 231072 231072    90114 Sep 23 17:59 .aii_cost_ledger.jsonl\ndrwxr-xr-x  8 231072 231072  2001718 Sep 23 22:14 .git\n-rw-r--r--  1 231072 231072       53 Sep 23 18:58 .gitignore\n-rw-r--r--  1 231072 231072    90577 Sep 24 23:22 .repl_agent.ptylog\n-rw-r--r--  1 root   root       2976 Sep 24 23:22 .terminal_claude_agent_struct_out.json\n-rw-r--r--  1 231072 231072    16456 Sep 23 22:17 README.md\ndrwxr-xr-x  2 231072 231072  2000274 Sep 23 17:58 cache\ndrwxr-xr-x  3 231072 231072  2003203 Sep 24 01:10 data\n-rw-r--r--  1 231072 231072 26916860 Sep 23 18:57 full_method_out.json\ndrwxr-xr-x  2 231072 231072  1037828 Sep 23 22:13 logs\n-rw-r--r--  1 231072 231072     8261 Sep 23 18:30 method.py\n-rw-r--r--  1 231072 231072 20956520 Sep 23 18:56 method_out.json\n-rw-r--r--  1 231072 231072    62032 Sep 23 18:57 mini_method_out.json\n-rw-r--r--  1 231072 231072    61745 Sep 23 18:57 preview_method_out.json\n-rw-r--r--  1 231072 231072     2224 Sep 23 19:05 pyproject.toml\n-rw-r--r--  1 231072 231072       22 Sep 23 18:05 pytest.ini\n-rw-r--r--  1 root   root      10561 Sep 24 23:21 reproducibility.md\n-rwxrwxrwx  1 231072 231072      789 Sep 23 18:58 restore.sh\ndrwxr-xr-x  3 231072 231072  2006792 Sep 23 19:05 results\ndrwxr-xr-x  6 231072 231072  1054970 Sep 23 19:10 src\ndrwxr-xr-x  2 231072 231072  1001666 Sep 23 19:05 tests\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/results:\ntotal 73490\ndrwxr-xr-x  3 231072 231072  2006792 Sep 23 19:05 .\ndrwxr-xr-x 10 root   root    2016678 Sep 24 23:21 ..\n-rw-r--r--  1 231072 231072  3569130 Sep 23 18:00 E_disguise_map.jsonl\n-rw-r--r--  1 231072 231072     5807 Sep 23 17:58 E_judge.jsonl\n-rw-r--r--  1 231072 231072  1937377 Sep 23 18:52 E_judge_local.jsonl\n-rw-r--r--  1 231072 231072   853190 Sep 23 17:59 E_l3_q.jsonl\n-rw-r--r--  1 231072 231072 14889871 Sep 23 18:43 E_sentences.jsonl\n-rw-r--r--  1 231072 231072      170 Sep 23 18:27 E_stage_100.json\n-rw-r--r--  1 231072 231072      180 Sep 23 18:45 E_stage_all.json\n-rw-r--r--  1 231072 231072      188 Sep 23 18:25 E_stage_mini.json\n-rw-r--r--  1 231072 231072   184275 Sep 23 18:56 analysis.json\n-rw-r--r--  1 231072 231072     2264 Sep 23 18:56 audit_rederive.json\n-rw-r--r--  1 231072 231072      204 Sep 23 19:08 budget_state.json\n-rw-r--r--  1 231072 231072     4327 Sep 23 17:58 costs.jsonl\n-rw-r--r--  1 231072 231072     7336 Sep 23 22:13 deviations.json\n-rw-r--r--  1 231072 231072       94 Sep 23 18:48 judge_cache_regression.json\n-rw-r--r--  1 231072 231072  4960000 Sep 23 17:58 llm_cache.jsonl\n-rw-r--r--  1 231072 231072  4763037 Sep 23 18:52 local_cache.jsonl\n-rw-r--r--  1 231072 231072      556 Sep 23 18:56 p_tests.json\n-rw-r--r--  1 231072 231072 22016065 Sep 23 18:52 per_item_E.jsonl\n-rw-r--r--  1 231072 231072      368 Sep 23 19:05 placebo_headline.json\n-rw-r--r--  1 231072 231072     2396 Sep 23 18:54 posthoc_nf_fusion.json\n-rw-r--r--  1 231072 231072      221 Sep 23 18:31 prefilter_audit.json\n-rw-r--r--  1 231072 231072    17167 Sep 23 18:23 prereg.json\n-rw-r--r--  1 231072 231072      112 Sep 23 18:23 prereg.sha256\n-rw-r--r--  1 231072 231072     2081 Sep 23 18:18 prereg_selection.json\n-rw-r--r--  1 231072 231072       65 Sep 23 18:18 prereg_selection.sha256\n-rw-r--r--  1 231072 231072   118722 Sep 23 17:58 prices.json\n-rw-r--r--  1 231072 231072   655065 Sep 23 18:52 rewrite_scores_pt.jsonl\n-rw-r--r--  1 231072 231072     5012 Sep 23 18:22 screen_fit.json\n-rw-r--r--  1 231072 231072    68101 Sep 23 18:20 screen_probes.json\n-rw-r--r--  1 231072 231072  9586133 Sep 23 18:21 screen_scores.jsonl\n-rw-r--r--  1 231072 231072   177904 Sep 23 18:17 screen_scores_mini12.jsonl\n-rw-r--r--  1 231072 231072  7380451 Sep 23 18:19 screen_scores_nfonly.jsonl\ndrwxr-xr-x  2 231072 231072        1 Sep 23 17:58 tables\n-rw-r--r--  1 231072 231072    13240 Sep 23 18:56 tables.md\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/src:\ntotal 7130\ndrwxr-xr-x  6 231072 231072 1054970 Sep 23 19:10 .\ndrwxr-xr-x 10 root   root   2016678 Sep 24 23:21 ..\n-rw-r--r--  1 231072 231072       0 Sep 23 17:58 __init__.py\n-rw-r--r--  1 231072 231072   52084 Sep 23 18:54 analyse_E.py\n-rw-r--r--  1 231072 231072    6702 Sep 23 17:57 data_views.py\n-rwxrwxrwx  1 231072 231072     913 Sep 23 19:10 key_monitor.sh\n-rw-r--r--  1 231072 231072    3806 Sep 23 18:12 local_judge_E.py\n-rw-r--r--  1 231072 231072   42945 Sep 23 18:20 peer_text.py\n-rw-r--r--  1 231072 231072   10021 Sep 23 18:15 pool_scoring.py\n138 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/method.py\ntotal 1993\ndrwxr-xr-x 3 root root 1003129 Sep 25 16:10 .\ndrwxr-xr-x 3 root root 1003129 Sep 25 16:09 ..\ndrwxr-xr-x 2 root root       1 Sep 25 16:09 .aii\n-rw------- 1 root root      54 Sep 25 16:10 .aii_claude_session.json\n-rw-r--r-- 1 root root   31990 Sep 25 16:10 .repl_agent.ptylog", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [11] TOOL CALL — Bash · 2026-09-25 16:10:41 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5; cat $W/method.py; cat $W/pyproject.toml; head -c 3000 $W/preview_method_out.json
```

### [12] TOOL RESULT — Bash · 2026-09-25 16:10:41 UTC

```
{"stdout": "#!/usr/bin/env python3\n\"\"\"PEER+TEXT on held-out dataset E: end-to-end driver (method AND baselines side by side, one pipeline).\n\nMethod (ours): PEER+TEXT = graded cross-family consensus (peer formalisations aligned into the candidate's vocabulary,\nclaim-unit entailment by finite-model refutation + z3; support / coverage / g_score, unit error codes) fused with the\nsolver-exact text checks of iteration 1 (L2-bow content accounting, L3 text questionnaire vs z3 role profile) by a\nlogistic frozen on the iteration-1 screen (fit only where the solver label and the adjudicated label agree).\nBaselines on the SAME rows: the disguised and original cheap LLM judge (exp D rubric-A prompt, gemini-2.5-flash-lite;\npre-registered bar), the local Qwen3-8B judge (exp D local bar; labelled secondary because the shared OpenRouter key\nran out), the iteration-1 binary consensus c_score_align, the name-free (NF-anchored) consensus, L2-bow alone, L3 alone,\nL1 lint and L2-role (columns only).\n\nStages (each is resumable and cached; `uv run method.py all` reruns everything that is missing):\n  views     src/data_views.py             E blind view (allowlist) + label view + API row order\n  api       src/run_api_E.py               L3 questionnaires + flash-lite judges on E (needs the shared key)\n  local     src/local_judge_E.py           local Qwen3-8B judge on E (GPU; .venv_gpu)\n  screen    src/screen_fit.py compute|fit|freeze   screen features, variant selection, fusion fit, prereg freeze\n  score     src/score_E.py run --stage mini|100|all ; assemble\n  analyse   src/analyse_E.py               the only label join (guarded by the prereg hash + mtimes)\n  outputs   build method_out.json (exp_gen_sol_out) + full/mini/preview variants\n\"\"\"\nfrom __future__ import annotations\n\nimport json\nimport subprocess\nimport sys\nfrom pathlib import Path\n\nfrom loguru import logger\n\nROOT = Path(__file__).resolve().parent\nPY = str(ROOT / \".venv\" / \"bin\" / \"python\")\nPY_GPU = str(ROOT / \".venv_gpu\" / \"bin\" / \"python\")\n\nlogger.remove()\nlogger.add(sys.stdout, level=\"INFO\", format=\"{time:HH:mm:ss}|{level:<7}|{message}\")\nlogger.add(ROOT / \"logs\" / \"method.log\", rotation=\"30 MB\", level=\"DEBUG\")\n\n\ndef sh(args: list[str]) -> None:\n    logger.info(\"$ \" + \" \".join(args))\n    r = subprocess.run(args, cwd=ROOT)\n    if r.returncode != 0:\n        raise RuntimeError(f\"stage failed ({r.returncode}): {' '.join(args)}\")\n\n\ndef jl(p: Path) -> list[dict]:\n    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []\n\n\ndef s(x) -> str:\n    if x is None:\n        return \"NA\"\n    if isinstance(x, float):\n        return f\"{x:.6f}\"\n    return str(x)\n\n\ndef build_outputs() -> None:\n    \"\"\"method_out.json in the exp_gen_sol_out schema: one example per E row (input = blind-view JSON, output = the E\n    final label joined AFTER the analysis), predict_* = every metric's score (higher = more likely an error).\"\"\"\n    items = jl(ROOT / \"results\" / \"per_item_E.jsonl\")\n    labels = {r[\"row_key\"]: r for r in jl(ROOT / \"data\" / \"E_labels.jsonl\")}\n    blind = {r[\"row_key\"]: r for r in jl(ROOT / \"data\" / \"E_blind.jsonl\")}\n    analysis = json.loads((ROOT / \"results\" / \"analysis.json\").read_text())\n    pre = json.loads((ROOT / \"results\" / \"prereg.json\").read_text())\n    ex = []\n    for r in items:\n        b = blind[r[\"row_key\"]]\n        L = labels[r[\"row_key\"]]\n        inp = {\"text\": b[\"text\"], \"candidate_fol\": b[\"candidate_fol\"], \"system\": b[\"system\"], \"prompt_variant\": b[\"prompt_variant\"],\n               \"row_key\": r[\"row_key\"], \"item_id\": b[\"item_id\"], \"sentence_id\": b[\"sentence_id\"]}\n        e = {\"input\": json.dumps(inp, ensure_ascii=False), \"output\": L[\"final_label\"],\n             \"predict_peer_text\": s(r.get(\"p_peer_text\")), \"predict_peer_text_flag\": s(r.get(\"flag\")),\n             \"predict_peer\": s(r.get(\"peer_only\")), \"predict_text\": s(r.get(\"p_text\")),\n             \"predict_g_score\": s(r.get(\"g_score\")), \"predict_c_score_nf\": s(r.get(\"c_score_nf\")),\n             \"predict_c_score_align\": s(r.get(\"c_score_align\")), \"predict_nf_g_score\": s(r.get(\"nf_g_score\")),\n             \"predict_nf_c_score\": s(r.get(\"nf_c_score\")), \"predict_l2_bow\": s(r.get(\"l2_bow\")), \"predict_l3\": s(r.get(\"l3_z3\")),\n             \"predict_l1_any\": s(r.get(\"l1_any\")), \"predict_l2_role\": s(r.get(\"l2_role\")),\n             \"predict_judge_cheap_disg\": s(r.get(\"judge_cheap_disg\")), \"predict_judge_cheap_orig\": s(r.get(\"judge_cheap_orig\")),\n             \"predict_judge_local_qwen8b_disg\": s(r.get(\"judge_local_qwen8b_disg\")),\n             \"predict_judge_local_qwen8b_orig\": s(r.get(\"judge_local_qwen8b_orig\")),\n             \"metadata_row_key\": r[\"row_key\"], \"metadata_item_id\": r[\"item_id\"], \"metadata_sentence_id\": r[\"sentence_id\"],\n             \"metadata_system\": r[\"system\"], \"metadata_system_class\": r[\"system_class\"], \"metadata_family_vendor\": r[\"family_vendor\"],\n             \"metadata_stratum\": r[\"stratum\"], \"metadata_strata\": r[\"strata\"], \"metadata_fold_E\": r[\"fold_E\"],\n             \"metadata_label_tier\": L[\"label_tier\"], \"metadata_repair_ops\": L[\"repair_ops\"], \"metadata_error_ops\": L[\"error_ops\"],\n             \"metadata_reading_choice\": L[\"reading_choice\"], \"metadata_coverage_status\": r[\"coverage_status\"],\n             \"metadata_unit_codes\": [c[\"code\"] + \":\" + c.get(\"unit\", \"\")[:120] for c in (r.get(\"unit_codes\") or [])][:12],\n             \"metadata_top_code\": r.get(\"top_code\"), \"metadata_fired_signal\": r.get(\"fired_signal\"),\n             \"metadata_model_used\": r.get(\"model_used\"), \"metadata_n_unknown\": r.get(\"n_unknown\"),\n             \"metadata_n_peers_used\": r.get(\"n_peers_used\"), \"metadata_peer_unavailable\": r.get(\"peer_unavailable\"),\n             \"metadata_support\": r.get(\"support\"), \"metadata_coverage\": r.get(\"coverage\"),\n             \"metadata_medoid_ops\": r.get(\"medoid_ops\"), \"metadata_judge_local_type\": r.get(\"judge_local_qwen8b_disg_type\"),\n             \"metadata_cost_usd\": (r.get(\"cost_usd_peer_text\") or 0.0), \"metadata_judge_cost_usd\": r.get(\"judge_cost_usd\"),\n             \"metadata_secs\": (r.get(\"secs_pairs\") or 0.0) + (r.get(\"secs_text\") or 0.0),\n             \"metadata_prereg_sha256\": r[\"prereg_sha256\"]}\n        ex.append(e)\n    heads = {k: {kk: vv for kk, vv in v.items() if kk in (\"n\", \"n_error\", \"n_correct\", \"metrics\")} for k, v in analysis[\"a_tables\"].items()}\n    out = {\"metadata\": {\n        \"method_name\": \"PEER+TEXT (graded cross-family consensus fused with solver-exact text checks), frozen on the screen, scored once on E\",\n        \"prereg_sha256\": (ROOT / \"results\" / \"prereg.sha256\").read_text().split()[0],\n        \"peer_variant\": pre[\"variant\"], \"F1_failed_on_screen\": pre[\"selection_evidence\"][\"F1_failed\"],\n        \"fusion\": pre[\"frozen\"][\"fusion\"], \"text_only\": pre[\"frozen\"][\"text_only\"],\n        \"orientation\": \"every predict_* is oriented so that higher = more likely an error; NA = not available\",\n        \"headline_auroc_tables\": heads, \"criteria\": analysis[\"criteria\"],\n        \"p_tests\": json.loads((ROOT / \"results\" / \"p_tests.json\").read_text()),\n        \"workspace\": str(ROOT)},\n        \"datasets\": [{\"dataset\": \"E_heldout_candidates\", \"examples\": ex}]}\n    (ROOT / \"method_out.json\").write_text(json.dumps(out, ensure_ascii=False))\n    logger.info(f\"method_out.json: {len(ex)} examples, {(ROOT / 'method_out.json').stat().st_size / 1e6:.1f} MB\")\n\n\n@logger.catch(reraise=True)\ndef main():\n    stage = sys.argv[1] if len(sys.argv) > 1 else \"all\"\n    if stage in (\"views\", \"all\"):\n        sh([PY, \"src/data_views.py\"])\n    if stage in (\"api\", \"all\"):\n        sh([PY, \"src/run_api_E.py\"])\n    if stage in (\"local\", \"all\") and Path(PY_GPU).exists():\n        sh([PY_GPU, \"src/local_judge_E.py\"])\n    if stage in (\"screen\", \"all\"):\n        if not (ROOT / \"results\" / \"prereg.json\").exists():\n            sh([PY, \"src/screen_fit.py\", \"compute\"])\n            sh([PY, \"src/screen_fit.py\", \"fit\"])\n            sh([PY, \"src/screen_fit.py\", \"freeze\"])\n    if stage in (\"score\", \"all\"):\n        for st in (\"mini\", \"100\", \"all\"):\n            sh([PY, \"src/score_E.py\", \"run\", \"--stage\", st])\n        sh([PY, \"src/score_E.py\", \"assemble\"])\n    if stage in (\"analyse\", \"all\"):\n        sh([PY, \"src/analyse_E.py\"])\n    if stage in (\"outputs\", \"all\"):\n        build_outputs()\n\n\nif __name__ == \"__main__\":\n    main()\n[project]\nname = \"peer-text-heldout\"\nversion = \"0.1.0\"\ndescription = \"PEER+TEXT (graded cross-family consensus + solver-exact text checks) confirmed once on held-out NL->FOL set E\"\nrequires-python = \">=3.12\"\n# every package pinned to the exact version installed in .venv (uv pip freeze, 2026-09-23); .venv has no pip.\n# GPU judge env (.venv_gpu, separate): torch, transformers, accelerate, loguru, huggingface_hub, aiohttp, requests, z3-solver\ndependencies = [\n  \"aiohappyeyeballs==2.7.1\",\n  \"aiohttp==3.14.3\",\n  \"aiosignal==1.4.0\",\n  \"annotated-doc==0.0.5\",\n  \"annotated-types==0.8.0\",\n  \"anyio==4.15.1\",\n  \"attrs==26.1.0\",\n  \"blis==1.3.3\",\n  \"catalogue==2.0.10\",\n  \"certifi==2026.7.22\",\n  \"charset-normalizer==3.5.1\",\n  \"click==8.5.0\",\n  \"cloudpathlib==0.25.0\",\n  \"cloudpickle==3.1.2\",\n  \"confection==1.3.3\",\n  \"cymem==2.0.13\",\n  \"defusedxml==0.7.1\",\n  \"en-core-web-sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl\",\n  \"formulaic==1.2.2\",\n  \"frozenlist==1.8.0\",\n  \"h11==0.16.0\",\n  \"httpcore==1.0.9\",\n  \"httpx==0.28.1\",\n  \"idna==3.20\",\n  \"iniconfig==2.3.0\",\n  \"interface-meta==2.0.1\",\n  \"jinja2==3.1.6\",\n  \"joblib==1.6.0\",\n  \"loguru==0.7.3\",\n  \"markdown-it-py==4.2.0\",\n  \"markupsafe==3.0.3\",\n  \"mdurl==0.1.2\",\n  \"multidict==6.9.1\",\n  \"murmurhash==1.0.15\",\n  \"narwhals==2.26.0\",\n  \"nltk==3.10.3\",\n  \"numpy==2.5.3\",\n  \"packaging==26.3\",\n  \"pandas==3.0.6\",\n  \"patsy==1.0.3\",\n  \"pluggy==1.6.0\",\n  \"preshed==3.0.13\",\n  \"propcache==0.5.4\",\n  \"psutil==7.2.2\",\n  \"pydantic==2.13.5\",\n  \"pydantic-core==2.46.5\",\n  \"pygments==2.21.0\",\n  \"pytest==9.1.1\",\n  \"python-dateutil==2.9.0.post0\",\n  \"regex==2026.9.10\",\n  \"requests==2.34.2\",\n  \"rich==15.0.0\",\n  \"scikit-learn==1.9.1\",\n  \"scipy==1.18.1\",\n  \"setuptools==84.0.0\",\n  \"shellingham==1.5.4\",\n  \"six==1.17.0\",\n  \"smart-open==8.0.1\",\n  \"spacy==3.8.16\",\n  \"spacy-legacy==3.0.12\",\n  \"spacy-loggers==1.0.5\",\n  \"srsly==2.5.3\",\n  \"statsmodels==0.15.0\",\n  \"thinc==8.3.13\",\n  \"threadpoolctl==3.7.0\",\n  \"tqdm==4.70.1\",\n  \"typer==0.27.2\",\n  \"typing-extensions==4.16.0\",\n  \"typing-inspection==0.4.4\",\n  \"urllib3==2.8.0\",\n  \"wasabi==1.1.3\",\n  \"weasel==1.0.0\",\n  \"wrapt==2.4.1\",\n  \"yarl==1.25.1\",\n  \"z3-solver==5.1.0.0\",\n]\n{\n  \"metadata\": {\n    \"method_name\": \"PEER+TEXT (graded cross-family consensus fused with solver-exact text checks), frozen on the screen, scored once on E\",\n    \"prereg_sha256\": \"b9f28b1bf6bfd29c99d03eb128f2ad64fd2d14d40356a4c5f1fdd16a415838ab\",\n    \"peer_variant\": \"ALIGN\",\n    \"F1_failed_on_screen\": true,\n    \"fusion\": {\n      \"features\": [\n        \"ALIGN:g_score\",\n        \"c_score_align\",\n        \"l2_bow\"\n      ],\n      \"mean\": [\n        0.566210851187638,\n        0.6266243516243517,\n        0.31995795248635645\n      ],\n      \"sd\": [\n        0.42959266854520983,\n        0.4161087088100467,\n        0.3876575298036705\n      ],\n      \"coef\": [\n        -0.11585513552537881,\n        1.7464702715295488,\n        3.0865271611542133\n      ],\n      \"intercept\": 2.613671543622261,\n      \"C\": 10.0,\n      \"oof_auroc\": 0.9429959803975552,\n      \"oof_auroc_by_C\": {\n        \"0.1\": 0.9328093166675844,\n        \"1.0\": 0.9423627553548813,\n        \"10.0\": 0.9429959803975552\n      },\n      \"threshold\": 0.6902659323258526\n    },\n    \"text_only\": {\n      \"features\": [\n        \"l2_bow\",\n        \"l3_z3\"\n      ],\n      \"mean\": [\n        0.31995795248635645,\n        0.5109047193497596\n      ],\n      \"sd\": [\n        0.3876575298036705,\n        0.5618448432724922\n      ],\n      \"coef\": [\n        2.7158606402943537,\n        1.3045478277515505\n      ],\n      \"intercept\": 2.1116354643227795,\n      \"C\": 10.0,\n      \"oof_auroc\": 0.8733825229888224,\n      \"oof_auroc_by_C\": {\n        \"0.1\": 0.8706293706293706,\n        \"1.0\": 0.8733549914652277,\n        \"10.0\": 0.8733825229888224\n      },\n      \"threshold\": 0.7809534183242605\n    },\n    \"orientation\": \"every predict_* is oriented so that higher = more likely an error; NA = not available\",\n    \"headline_auroc_tables\": {\n      \"R_AB pooled\": {\n        \"n\": 2686,\n        \"n_error\": 1822,\n        \"n_correct\": 864,\n        \"metrics\": {\n          \"p_peer_text\": {\n            \"auroc\": 0.7900410873277229,\n            \"ci\": [\n              0.7515964802454704,\n              0.8234980895606637\n            ],\n            \"auprc\": 0.8790429206220931,\n            \"prevalence\": 0.6783320923306031\n          },\n          \"peer_only\": {\n            \"auroc\": 0.7480644235069317,\n            \"ci\": [\n              0.7060020851444325,\n              0.7863879373530582\n            ],\n            \"auprc\": 0.8240954811343213,\n            \"prevalence\": 0.6783320923306031\n          },\n          \"p_text\": {\n            \"auroc\": 0.6931596714030166,\n            \"ci\": [\n              0.6517033173882918,\n              0.7316063394711673\n            ],\n            \"auprc\": 0.8119152615487248,\n            \"prevalence\": 0.6783320923306031\n          },\n          \"g_score\": {\n            \"auroc\": 0.7480644235069317,\n            \"ci\": [\n              0.7060020851444325,\n              0.7863879373530582\n            ],\n            \"auprc\": 0.8240954811343213,\n            \"prevalence\": 0.6783320923306031\n          },\n          \"c_score_nf\": {\n            \"auroc\": 0.7464127", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [13] ASSISTANT · 2026-09-25 16:10:49 UTC

```
method.py is an orchestrator (subprocess stages) plus `build_outputs()`. Let me inspect the inputs build_outputs joins and the preview examples.
```

### [14] TOOL CALL — Bash · 2026-09-25 16:10:49 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5; cd $W; python3 - <<'EOF'
import json
p=json.load(open('preview_method_out.json'))
print(list(p['metadata'].keys()))
ex=p['datasets'][0]['examples']; print(len(ex)); print(json.dumps(ex[0],indent=1)[:3000])
for k in ['analysis.json','prereg.json','p_tests.json']:
    d=json.load(open('results/'+k)); print(k, list(d.keys())[:40] if isinstance(d,dict) else type(d))
EOF
ls -la data data/*; cat results/prereg.sha256; head -c 1500 results/per_item_E.jsonl; echo; head -c 800 data/E_labels.jsonl; echo; head -c 800 data/E_blind.jsonl; wc -l results/per_item_E.jsonl data/E_labels.jsonl data/E_blind.jsonl
```

### [15] TOOL RESULT — Bash · 2026-09-25 16:10:51 UTC

```
{"stdout": "['method_name', 'prereg_sha256', 'peer_variant', 'F1_failed_on_screen', 'fusion', 'text_only', 'orientation', 'headline_auroc_tables', 'criteria', 'p_tests', 'workspace']\n3\n{\n \"input\": \"{\\\"text\\\": \\\"When something is depressing, it is sad.\\\", \\\"candidate_fol\\\": \\\"\\\", \\\"system\\\": \\\"ccg2lambda\\\", \\\"prompt_variant\\\": \\\"none\\\", \\\"row_key\\\": \\\"31452c4db10ee367|none\\\", \\\"item_id\\\": \\\"31452c4db10ee367\\\", \\\"sentence...\",\n \"output\": \"UNPARSEABLE\",\n \"predict_peer_text\": \"1.000000\",\n \"predict_peer_text_flag\": \"1\",\n \"predict_peer\": \"1.000000\",\n \"predict_text\": \"1.000000\",\n \"predict_g_score\": \"NA\",\n \"predict_c_score_nf\": \"NA\",\n \"predict_c_score_align\": \"NA\",\n \"predict_nf_g_score\": \"NA\",\n \"predict_nf_c_score\": \"NA\",\n \"predict_l2_bow\": \"NA\",\n \"predict_l3\": \"NA\",\n \"predict_l1_any\": \"NA\",\n \"predict_l2_role\": \"NA\",\n \"predict_judge_cheap_disg\": \"1.000000\",\n \"predict_judge_cheap_orig\": \"1.000000\",\n \"predict_judge_local_qwen8b_disg\": \"1.000000\",\n \"predict_judge_local_qwen8b_orig\": \"1.000000\",\n \"metadata_row_key\": \"31452c4db10ee367|none\",\n \"metadata_item_id\": \"31452c4db10ee367\",\n \"metadata_sentence_id\": \"0000c2274e80\",\n \"metadata_system\": \"ccg2lambda\",\n \"metadata_system_class\": \"symbolic_eventsem\",\n \"metadata_family_vendor\": \"ccg2lambda_never_peer\",\n \"metadata_stratum\": \"CTRL\",\n \"metadata_strata\": {\n  \"words\": 7,\n  \"n_quant\": 1,\n  \"depth\": 1,\n  \"n_conditions\": 1,\n  \"text_conditions\": 1,\n  \"exception_type\": null,\n  \"source_stratum\": \"CTRL\",\n  \"ctrl_len_bin\": \"0-11\",\n  \"l25_topup_batch\": false\n },\n \"metadata_fold_E\": 1,\n \"metadata_label_tier\": \"-\",\n \"metadata_repair_ops\": null,\n \"metadata_error_ops\": null,\n \"metadata_reading_choice\": false,\n \"metadata_coverage_status\": \"UNPARSEABLE\",\n \"metadata_unit_codes\": [],\n \"metadata_top_code\": null,\n \"metadata_fired_signal\": \"UNPARSEABLE\",\n \"metadata_model_used\": \"none\",\n \"metadata_n_unknown\": null,\n \"metadata_n_peers_used\": null,\n \"metadata_peer_unavailable\": null,\n \"metadata_support\": null,\n \"metadata_coverage\": null,\n \"metadata_medoid_ops\": null,\n \"metadata_judge_local_type\": null,\n \"metadata_cost_usd\": 1.1664285714285715e-05,\n \"metadata_judge_cost_usd\": 0.0,\n \"metadata_secs\": 0.0,\n \"metadata_prereg_sha256\": \"b9f28b1bf6bfd29c99d03eb128f2ad64fd2d14d40356a4c5f1fdd16a415838ab\"\n}\nanalysis.json ['coverage_imputation', 'a_tables', 'a_sensitivity', 'criteria', 'b_P1', 'c_P2', 'd_P3', 'e_P4', 'f_error_types', 'g_system', 'h_complexity', 'i_contamination', 'j_coverage_cost', 'k_misc', 'placebo_within_stratum', 'placebo_global_shuffle', 'a_stratified']\nprereg.json ['title', 'timestamp_utc', 'note', 'code_sha1', 'E_blind_sha256', 'prereg_selection_sha256', 'family_map_vendor', 'family_map_sensitivity', 'peers', 'scoring_params', 'unit_cap', 'fm_domains', 'clamp_domains', 'variant', 'selection_evidence', 'frozen', 'imputation', 'label_regimes', 'testability', 'analyses', 'deviations_at_freeze']\np_tests.json ['P1_R_AB', 'P1_R_A', 'P2', 'P3', 'P4', 'criteria']\n-rw-r--r-- 1 231072 231072  6718145 Sep 23 17:57 data/E_blind.jsonl\n-rw-r--r-- 1 231072 231072       65 Sep 23 17:57 data/E_blind.sha256\n-rw-r--r-- 1 231072 231072 10458429 Sep 23 17:57 data/E_labels.jsonl\n-rw-r--r-- 1 231072 231072   261314 Sep 23 17:57 data/api_priority.json\n-rw-r--r-- 1 231072 231072    19062 Sep 23 17:55 data/expA_prereg.json\n-rw-r--r-- 1 231072 231072    13709 Sep 23 17:55 data/expD_prereg.json\n-rw-r--r-- 1 231072 231072    12578 Sep 23 17:55 data/folds.json\n-rw-r--r-- 1 231072 231072   227205 Sep 23 17:55 data/invariance_items.json\n\ndata:\ntotal 23179\ndrwxr-xr-x  3 231072 231072  2003203 Sep 24 01:10 .\ndrwxr-xr-x 10 root   root    2016678 Sep 24 23:21 ..\n-rw-r--r--  1 231072 231072  6718145 Sep 23 17:57 E_blind.jsonl\n-rw-r--r--  1 231072 231072       65 Sep 23 17:57 E_blind.sha256\n-rw-r--r--  1 231072 231072 10458429 Sep 23 17:57 E_labels.jsonl\n-rw-r--r--  1 231072 231072   261314 Sep 23 17:57 api_priority.json\n-rw-r--r--  1 231072 231072    19062 Sep 23 17:55 expA_prereg.json\n-rw-r--r--  1 231072 231072    13709 Sep 23 17:55 expD_prereg.json\n-rw-r--r--  1 231072 231072    12578 Sep 23 17:55 folds.json\n-rw-r--r--  1 231072 231072   227205 Sep 23 17:55 invariance_items.json\ndrwxr-xr-x  2 231072 231072  2001514 Sep 23 18:48 screen\n\ndata/screen:\ntotal 19418\ndrwxr-xr-x 2 231072 231072 2001514 Sep 23 18:48 .\ndrwxr-xr-x 3 231072 231072 2003203 Sep 24 01:10 ..\n-rw-r--r-- 1 231072 231072 2442818 Sep 23 18:11 expA_per_item.jsonl\n-rw-r--r-- 1 231072 231072  632634 Sep 23 18:48 expD_disguise_map.json\n-rw-r--r-- 1 231072 231072 3247282 Sep 23 18:11 expD_per_item_scores.jsonl\n-rw-r--r-- 1 231072 231072  692824 Sep 23 18:11 expD_rewrite_scores.jsonl\n-rw-r--r-- 1 231072 231072 1680482 Sep 23 18:48 expD_screen_items.json\n-rw-r--r-- 1 231072 231072 4556597 Sep 23 18:11 peer_outputs.jsonl\n-rw-r--r-- 1 231072 231072  950464 Sep 23 18:11 screen_adjudicated_labels.json\n-rw-r--r-- 1 231072 231072 1011061 Sep 23 18:11 screen_items.json\n-rw-r--r-- 1 231072 231072  661279 Sep 23 18:11 units.json\nb9f28b1bf6bfd29c99d03eb128f2ad64fd2d14d40356a4c5f1fdd16a415838ab  prereg.json  2026-09-23T18:23:50.564681+00:00\n{\"row_key\": \"31452c4db10ee367|none\", \"item_id\": \"31452c4db10ee367\", \"sentence_id\": \"0000c2274e80\", \"system\": \"ccg2lambda\", \"slot\": \"CCG\", \"family\": \"symbolic\", \"family_vendor\": \"ccg2lambda_never_peer\", \"system_class\": \"symbolic_eventsem\", \"prompt_variant\": \"none\", \"stratum\": \"CTRL\", \"strata\": {\"words\": 7, \"n_quant\": 1, \"depth\": 1, \"n_conditions\": 1, \"text_conditions\": 1, \"exception_type\": null, \"source_stratum\": \"CTRL\", \"ctrl_len_bin\": \"0-11\", \"l25_topup_batch\": false}, \"fold_E\": 1, \"coverage_status\": \"UNPARSEABLE\", \"prereg_sha256\": \"b9f28b1bf6bfd29c99d03eb128f2ad64fd2d14d40356a4c5f1fdd16a415838ab\", \"variant\": \"ALIGN\", \"g_score\": null, \"support\": null, \"coverage\": null, \"c_score_nf\": null, \"g_score_k6\": null, \"g_score_famfield\": null, \"nf_eq_medoid\": null, \"unit_codes\": null, \"top_code\": null, \"n_units\": null, \"units_truncated\": null, \"n_unknown\": null, \"n_peers_used\": null, \"peer_unavailable\": null, \"c_score_align\": null, \"eqmv_medoid_eq\": null, \"nf_g_score\": null, \"nf_c_score\": null, \"nf_eq_medoid_nf\": null, \"nf_top_code\": null, \"nf_unit_codes\": null, \"nf_secs_pairs\": null, \"medoid_depth\": null, \"medoid_ops\": null, \"l2_bow\": null, \"l3_z3\": null, \"l3_z3_disg\": null, \"l3_fields\": null, \"l1_codes\": null, \"l2_role\": null, \"l1_any\": null, \"p_peer_text\": 1.0, \"p_text\": 1.0, \"p_sensitivity\": 1.0, \"peer_only\": 1.0, \"flag\": 1, \"fired_signal\": \"UNPARSEABLE\", \"model_used\": \"none\", \"judge_cheap_orig\": 1.0, \"judge_local_qwen8b_orig\": 1.0, \"judge_cheap_orig_type\": null, \"judge_cheap_orig\n{\"row_key\": \"31452c4db10ee367|none\", \"item_id\": \"31452c4db10ee367\", \"sentence_id\": \"0000c2274e80\", \"system\": \"ccg2lambda\", \"system_class\": \"symbolic_eventsem\", \"prompt_variant\": \"none\", \"family\": \"symbolic\", \"output\": \"UNPARSEABLE\", \"reference_fol\": \"∀x (Depressing(x) → Sad(x))\", \"strata\": {\"words\": 7, \"n_quant\": 1, \"depth\": 1, \"n_conditions\": 1, \"text_conditions\": 1, \"exception_type\": null, \"source_stratum\": \"CTRL\", \"ctrl_len_bin\": \"0-11\", \"l25_topup_batch\": false}, \"final_label\": \"UNPARSEABLE\", \"label_tier\": \"-\", \"auto_label\": \"UNPARSEABLE\", \"equiv_status\": null, \"repair_ops\": null, \"repair_status\": null, \"error_ops\": null, \"label_source\": \"parser\", \"addrop_only_suspect\": false, \"solver_lenient_label\": \"UNPARSEABLE\", \"correct_not_equivalent\": false, \"reading_choice\": false, \"gold_aud\n{\"item_id\": \"31452c4db10ee367\", \"sentence_id\": \"0000c2274e80\", \"system\": \"ccg2lambda\", \"slot\": \"CCG\", \"family\": \"symbolic\", \"system_class\": \"symbolic_eventsem\", \"generator_model_id\": \"ccg2lambda\", \"prompt_variant\": \"none\", \"row_key\": \"31452c4db10ee367|none\", \"text\": \"When something is depressing, it is sad.\", \"candidate_fol\": \"\", \"strata\": {\"words\": 7, \"n_quant\": 1, \"depth\": 1, \"n_conditions\": 1, \"text_conditions\": 1, \"exception_type\": null, \"source_stratum\": \"CTRL\", \"ctrl_len_bin\": \"0-11\", \"l25_topup_batch\": false}}\n{\"item_id\": \"b87a8dda4faced11\", \"sentence_id\": \"0000c2274e80\", \"system\": \"F:openai/gpt-5.1\", \"slot\": \"F\", \"family\": \"openai-frontier\", \"system_class\": \"llm\", \"generator_model_id\": \"openai/gpt-5.1\", \"prompt_variant\": \"fewshot_v1\", \"row_key\": \"b87a8dda4faced11|fewshot_v1\", \"text    8507 results/per_item_E.jsonl\n    8507 data/E_labels.jsonl\n    8507 data/E_blind.jsonl\n   25521 total", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_2/art_TaxJRnPcJMuZ", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [16] TOOL CALL — Bash · 2026-09-25 16:11:03 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5; cd $W; grep -n "def \|sigmoid\|intercept" src/peer_text.py | head -60; grep -rn "p_peer_text" src/*.py | head -10; python3 - <<'EOF'
import json, collections
L=[json.loads(l) for l in open('data/E_labels.jsonl')]
print(collections.Counter((r['final_label'],r['label_tier']) for r in L).most_common(20))
P=[json.loads(l) for l in open('results/per_item_E.jsonl')]
print(collections.Counter(r['stratum'] for r in P)); print(collections.Counter(r['coverage_status'] for r in P))
print(collections.Counter(r['system'] for r in P).most_common(30))
import statistics
print(statistics.mean(len(json.dumps(r)) for r in P), statistics.mean(len(json.dumps(r)) for r in L))
print(list(L[0].keys()))
a=json.load(open('results/analysis.json')); print(list(a['a_tables'].keys())); print(json.dumps(a['criteria'])[:1500]); print(len(json.dumps(a['a_tables'])))
EOF
```

### [17] TOOL RESULT — Bash · 2026-09-25 16:11:03 UTC

```
{"stdout": "63:def parse_fol(s: str | None):\n73:def to_str(e) -> str:\n85:def free_vars(e, bound=frozenset()) -> set:\n96:def mentions(e, v: str) -> bool:\n107:def alpha(e, env=None, ctr=None):\n123:def canon(e) -> str:\n127:def pred_keys(e, acc=None) -> dict:\n143:def constants(e, bound=frozenset(), acc=None) -> dict:\n160:def rename(e, pmap: dict, cmap: dict, bound=frozenset()):\n173:def _conseq_pieces(c) -> list:\n189:def claim_units(e, cap: int = UNIT_CAP) -> tuple[list, list, bool]:\n197:    def emit(prefix, x, loc):\n204:    def split(x, prefix, loc):\n236:def units_of(s: str):\n245:def _occurrences(e):\n249:    def go(x, pol, binders, depth):\n270:def _qdepth(e) -> int:\n284:def clamp_profile(e) -> dict:\n304:def symbol_signature(e) -> dict:\n343:def _jac(a, b) -> float:\n349:def pred_cost(a: dict, b: dict) -> float:\n363:def _text_tokens(text: str) -> tuple:\n370:def text_anchor(symbol: str, text: str) -> frozenset:\n379:def anchor_cost(a: frozenset, b: frozenset) -> float:\n390:def _solve(M: np.ndarray):\n395:def name_free_align(cand, peer, text: str | None = None, variant: str = \"NF-pure\", k: int = 5,\n429:    def to_map(r, c):\n453:def _murty(M: np.ndarray, nr: int, k: int, to_map) -> list:\n457:    def solve(forced, forbidden):\n501:def _seed(*parts) -> int:\n506:def _table(name: str, arity: int, d: int, m: int) -> np.ndarray:\n513:def _const(name: str, d: int, m: int) -> np.ndarray:\n518:def _fm_eval(e, d: int, m: int, clamp: tuple | None = None) -> np.ndarray | None:\n528:    def shape_at(i):\n534:    def ev(x):\n571:def _binders(e):\n586:def fm_vector(s: str, e=None) -> list:\n598:def fm_refutes(prem_s: str, unit_s: str, prem=None, unit=None) -> bool:\n608:def z3_entails(prem, unit, ms: int = 2000):\n628:    def __init__(self, timeout_ms: int = 2000, use_fm: bool = True):\n634:    def __call__(self, prem_s: str, unit_s: str, prem=None, unit=None):\n663:def pair_result(cand_s: str, peer_s: str, ent: Entailer, text: str | None = None, variant: str = \"NF-pure\",\n712:def _variants_quant(u):\n716:    def go(x, path):\n733:def _variants_swap(u):\n736:    def go(x, path):\n752:def _variants_neg(u):\n756:    def go(x, path):\n773:def _replace(e, path, fn):\n784:def _majority_support(ent: Entailer, peers_r: list[str], u_s: str) -> bool:\n802:def graded_consensus(cand_s: str, pool: list[str], pairs: dict, ent: Entailer, return_codes: bool = True,\n826:    def fwd_of(i, r):\n904:def g_from_subset(cand_s: str, pool: list[str], pairs: dict, ent: Entailer) -> float | None:\n909:def nf_medoid(pool: list[str], pairs: dict) -> int | None:\n925:def l2_bow(text: str, fol_ast) -> dict:\n933:def l3_z3(q: dict | None, fol_ast, prof: dict | None = None) -> dict:\n945:def text_side(text: str, fol_ast, q: dict | None, prof: dict | None = None, with_role: bool = True) -> dict:\n973:def _z(x, mu, sd):\n977:def apply_logistic(model: dict, feats: dict) -> float:\n978:    \"\"\"model = {'features', 'mean', 'sd', 'coef', 'intercept'}; missing feature -> z = 0.\"\"\"\nsrc/analyse_E.py:181:        for c in (\"p_peer_text\", \"p_text\", \"p_sensitivity\"):\nsrc/analyse_E.py:185:    CORE = [\"p_peer_text\", \"peer_only\", \"p_text\", \"g_score\", \"c_score_nf\", \"c_score_align\", \"l2_bow\", \"l3_z3\",\nsrc/analyse_E.py:226:        ev = evaluate(rs, CORE, pairs=[(\"p_peer_text\", \"p_text\"), (\"p_peer_text\", \"peer_only\"), (\"p_peer_text\", \"c_score_align\"),\nsrc/analyse_E.py:232:                ej = evaluate(rj, [\"p_peer_text\", \"p_text\", \"peer_only\", \"c_score_align\", j],\nsrc/analyse_E.py:233:                              pairs=[(\"p_peer_text\", j), (\"p_text\", j), (\"c_score_align\", j), (\"peer_only\", j)])\nsrc/analyse_E.py:238:        logger.info(f\"(a) {name}: n={ev['n']} err={ev['n_error']} fused={ev['metrics'].get('p_peer_text', {}).get('auroc')}\")\nsrc/analyse_E.py:245:        sens[nm] = evaluate(rs, [\"p_peer_text\", \"p_text\", \"peer_only\", \"c_score_align\"], b=500)\nsrc/analyse_E.py:247:        sens[nm][\"vs_local_judge\"] = evaluate(rj, [\"p_peer_text\", \"judge_local_qwen8b_disg\"],\nsrc/analyse_E.py:248:                                              pairs=[(\"p_peer_text\", \"judge_local_qwen8b_disg\")], b=500)\nsrc/analyse_E.py:253:        pr = e.get(\"paired\", {}).get(f\"p_peer_text - {j}\")\n[(('ERROR', 'C'), 2990), (('ERROR', 'B'), 1495), (('UNPARSEABLE', '-'), 1086), (('CORRECT', 'C'), 776), (('CORRECT', 'B'), 549), (('ERROR', 'A'), 478), (('CORRECT', 'A'), 419), (('UNRESOLVED', 'none'), 276), (('CONTESTED', 'A'), 147), (('CONTESTED', 'C'), 125), (('CONTESTED', 'B'), 113), (('ERROR', 'A_unaudited_ref'), 42), (('CORRECT', 'A_unaudited_ref'), 6), (('CONTESTED', 'A_unaudited_ref'), 5)]\nCounter({'L25': 3260, 'L20': 2000, 'CTRL': 1907, 'EXC': 1340})\nCounter({'OK': 7421, 'UNPARSEABLE': 1086})\n[('G2:qwen/qwen3-235b-a22b-2507', 1300), ('G1b:meta-llama/llama-3.3-70b-instruct', 1200), ('G1:meta-llama/llama-3.1-8b-instruct', 700), ('G3:mistralai/mistral-small-3.2-24b-instruct', 700), ('G6:microsoft/phi-4', 700), ('G9:cohere/command-r7b-12-2024', 700), ('G4:deepseek/deepseek-v3.2', 600), ('G5:google/gemma-3-27b-it', 600), ('G7:openai/gpt-4.1-mini', 600), ('G8:google/gemini-2.5-flash', 600), ('malls_gpt4_gold', 550), ('F:openai/gpt-5.1', 200), ('ccg2lambda', 57)]\n2628.972728341366 1247.0055248618785\n['row_key', 'item_id', 'sentence_id', 'system', 'system_class', 'prompt_variant', 'family', 'output', 'reference_fol', 'strata', 'final_label', 'label_tier', 'auto_label', 'equiv_status', 'repair_ops', 'repair_status', 'error_ops', 'label_source', 'addrop_only_suspect', 'solver_lenient_label', 'correct_not_equivalent', 'reading_choice', 'gold_audit_flag', 'reference_status', 'class_id', 'class_size', 'panel_votes', 'panel_scope', 'convention_flags']\n['R_AB pooled', 'R_AB L25', 'R_AB L20', 'R_AB EXC', 'R_AB CTRL', 'R_AB long (L25+L20+EXC)', 'R_A pooled L20+EXC', 'R_A L20', 'R_A EXC', 'R_A all strata (sign only)', 'R_A L25 (sign only)', 'R_A CTRL (sign only)']\n{\"judge_cheap_disg\": {\"testable_pooled_R_AB (>=300/class)\": false, \"a_R_AB_CI_gt_0\": false, \"a_R_A_sign_gt_0\": false, \"criterion_a_this_artifact\": false, \"criterion_c_long_CI_gt_0\": false, \"delta_R_AB\": {\"delta\": 0.05729166666666663, \"ci\": [-0.20000000000000007, 0.36035633484162893], \"p_boot_le0\": 0.3295, \"delong_z\": 0.4965609778692823, \"delong_p\": 0.6194986766828512}, \"delta_R_A\": null, \"delta_long\": null}, \"judge_local_qwen8b_disg\": {\"testable_pooled_R_AB (>=300/class)\": true, \"a_R_AB_CI_gt_0\": true, \"a_R_A_sign_gt_0\": true, \"criterion_a_this_artifact\": true, \"criterion_c_long_CI_gt_0\": true, \"delta_R_AB\": {\"delta\": 0.07828508049762173, \"ci\": [0.04337606521047203, 0.11223555043519434], \"p_boot_le0\": 0.0, \"delong_z\": 7.010055377113383, \"delong_p\": 2.382316566240661e-12}, \"delta_R_A\": {\"delta\": 0.2639805983533057, \"ci\": [0.1567325331336816, 0.35851538812692046], \"p_boot_le0\": 0.0, \"delong_z\": 7.688474849402802, \"delong_p\": 1.4876988529977098e-14}, \"delta_long\": {\"delta\": 0.11485732208040067, \"ci\": [0.07452931373932889, 0.1566149242625134], \"p_boot_le0\": 0.0, \"delong_z\": 7.775568274757718, \"delong_p\": 7.549516567451064e-15}}}\n86725", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_2/art_TaxJRnPcJMuZ", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [18] ASSISTANT · 2026-09-25 16:11:23 UTC

```
Now I'll build the curated mini data (100 rows, stratified across labels/strata/systems, with matching label + blind rows and the analysis/prereg pieces `build_outputs()` reads).
```

### [19] TOOL CALL — Bash · 2026-09-25 16:11:23 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5; OUT=/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_2/art_TaxJRnPcJMuZ; cd $W; python3 - <<EOF
import json, random, collections
random.seed(0)
jl=lambda p:[json.loads(l) for l in open(p) if l.strip()]
P=jl('results/per_item_E.jsonl'); L={r['row_key']:r for r in jl('data/E_labels.jsonl')}; B={r['row_key']:r for r in jl('data/E_blind.jsonl')}
def cat(r):
    l=L[r['row_key']]
    if l['final_label'] in('ERROR','CORRECT') and l['label_tier'] in('A','B'): return l['final_label']
    return 'OTHER'
pools=collections.defaultdict(list)
for r in P: pools[(cat(r), r['stratum'])].append(r)
quota={'ERROR':40,'CORRECT':40}
sel=[]
for c,q in quota.items():
    strata=['L25','L20','EXC','CTRL']
    for i,s in enumerate(strata):
        pool=pools[(c,s)]; random.shuffle(pool)
        # prefer distinct systems
        seen=set(); pick=[]
        for r in pool:
            if r['system'] not in seen: pick.append(r); seen.add(r['system'])
            if len(pick)==q//4: break
        sel+=pick
oth=[r for r in P if cat(r)=='OTHER']; random.shuffle(oth)
need={'UNPARSEABLE':7,'C':7,'CONTESTED':3,'UNRESOLVED':3}
for r in oth:
    l=L[r['row_key']]; k='UNPARSEABLE' if l['final_label']=='UNPARSEABLE' else ('CONTESTED' if l['final_label']=='CONTESTED' else ('UNRESOLVED' if l['final_label']=='UNRESOLVED' else ('C' if l['label_tier']=='C' else None)))
    if k and need.get(k,0)>0: sel.append(r); need[k]-=1
print(len(sel), collections.Counter(cat(r) for r in sel), collections.Counter(r['stratum'] for r in sel), len({r['system'] for r in sel}))
a=json.load(open('results/analysis.json')); pre=json.load(open('results/prereg.json'))
print(len(json.dumps(pre['selection_evidence'])), len(json.dumps(pre['frozen'])))
d={"description":"Curated 100-row subset of held-out dataset E (NL->FOL candidates, gold-free faithfulness scores + solver/adjudicated labels) for the PEER+TEXT demo. per_item_E = every metric score per row; E_labels = label view (joined only after scoring); E_blind = blind view (text + candidate FOL); analysis/prereg/p_tests = frozen full-E results.",
   "per_item_E":sel,"E_labels":[L[r['row_key']] for r in sel],"E_blind":[B[r['row_key']] for r in sel],
   "analysis":{"a_tables":a['a_tables'],"criteria":a['criteria']},
   "prereg":{"variant":pre['variant'],"selection_evidence":pre['selection_evidence'],"frozen":pre['frozen']},
   "p_tests":json.load(open('results/p_tests.json')),
   "prereg_sha256":open('results/prereg.sha256').read()}
json.dump(d,open('$OUT/mini_demo_data.json','w'),ensure_ascii=False)
EOF
ls -la $OUT/mini_demo_data.json
```

### [20] TOOL RESULT — Bash · 2026-09-25 16:11:23 UTC

```
{"stdout": "100 Counter({'ERROR': 40, 'CORRECT': 40, 'OTHER': 20}) Counter({'CTRL': 28, 'EXC': 25, 'L25': 24, 'L20': 23}) 13\n2053 1758\n-rw-r--r-- 1 root root 537077 Sep 25 16:11 /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_2/art_TaxJRnPcJMuZ/mini_demo_data.json", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_2/art_TaxJRnPcJMuZ", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [21] TOOL CALL — Bash · 2026-09-25 16:11:27 UTC

```
sed -n 970,1000p /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/src/peer_text.py; grep -n "apply_logistic\|ALIGN:g_score" /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/src/*.py | head
```

### [22] TOOL RESULT — Bash · 2026-09-25 16:11:27 UTC

```
{"stdout": "# =================================================================================================== fusion\ndef _z(x, mu, sd):\n    return 0.0 if x is None else (x - mu) / (sd if sd > 0 else 1.0)\n\n\ndef apply_logistic(model: dict, feats: dict) -> float:\n    \"\"\"model = {'features', 'mean', 'sd', 'coef', 'intercept'}; missing feature -> z = 0.\"\"\"\n    s = model[\"intercept\"]\n    for f, m, sd, c in zip(model[\"features\"], model[\"mean\"], model[\"sd\"], model[\"coef\"]):\n        s += c * _z(feats.get(f), m, sd)\n    return 1 / (1 + math.exp(-s))\n\n\ndef fused_score(frozen: dict, feats: dict) -> dict:\n    \"\"\"Frozen PEER+TEXT fusion. Unparseable -> p_error 1.0. peer_unavailable -> frozen TEXT-only model (pre-registered).\n    fired_signal = argmax standardized contribution (PEER = g/c_score_nf features, TEXT = l2_bow/l3).\"\"\"\n    if feats.get(\"coverage_status\") == \"UNPARSEABLE\":\n        return {\"p_error\": 1.0, \"flag\": 1, \"fired_signal\": \"UNPARSEABLE\", \"model_used\": \"none\"}\n    main = frozen[\"fusion\"]\n    use = main\n    if feats.get(\"peer_unavailable\") or feats.get(main[\"features\"][0]) is None:\n        use = frozen[\"text_only\"]\n    p = apply_logistic(use, feats)\n    contrib = {f: c * _z(feats.get(f), m, sd) for f, m, sd, c in zip(use[\"features\"], use[\"mean\"], use[\"sd\"], use[\"coef\"])}\n    top = max(contrib, key=contrib.get) if contrib else None\n    sig = \"PEER\" if top in (\"g_score\", \"c_score_nf\", \"c_score_align\") else (\"TEXT\" if top else None)\n    thr = main[\"threshold\"] if use is main else frozen[\"text_only\"][\"threshold\"]\n    return {\"p_error\": p, \"flag\": int(p >= thr), \"fired_signal\": sig, \"model_used\": \"fusion\" if use is main else \"text_only\"}\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/src/analyse_E.py:167:    IMPUTE = {\"peer_only\": neutral.get(\"ALIGN:g_score\"), \"g_score\": neutral.get(\"ALIGN:g_score\"),\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/src/analyse_E.py:170:              \"l2_bow\": neutral.get(\"l2_bow\"), \"l3_z3\": neutral.get(\"l3_z3\"), \"g_score_k6\": neutral.get(\"ALIGN:g_score\"),\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/src/analyse_E.py:171:              \"g_score_famfield\": neutral.get(\"ALIGN:g_score\"), \"l1_any\": 0.0, \"l2_role\": 0.0}\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/src/peer_text.py:977:def apply_logistic(model: dict, feats: dict) -> float:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/src/peer_text.py:994:    p = apply_logistic(use, feats)\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/src/posthoc_nf_fusion.py:67:            p_nf = PT.apply_logistic(m, f) if f.get(\"NF-anchored:g_score\") is not None else PT.apply_logistic(pre[\"frozen\"][\"text_only\"], f)\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/src/score_E.py:196:            rec[\"p_text\"] = PT.apply_logistic(frozen[\"text_only\"], feats)\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/src/score_E.py:197:            rec[\"p_sensitivity\"] = PT.apply_logistic(frozen[\"sensitivity_all_adj\"], feats) if feats.get(frozen[\"fusion\"][\"features\"][0]) is not None \\\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/src/screen_fit.py:402:    # c_score_align (iteration-1 binary consensus) in place of c_score_nf; the F2 degeneracy rule applies to ALIGN:g_score\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/src/screen_fit.py:460:    fused_in = [PT.apply_logistic(models[\"fusion\"], rows[i]) for i in ag_ids]", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [23] ASSISTANT · 2026-09-25 16:11:35 UTC

```
Let me check that re-applying the frozen fusion to the stored per-item features reproduces `p_peer_text`, so the notebook can show it.
```

### [24] TOOL CALL — Bash · 2026-09-25 16:11:35 UTC

```
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_2/art_TaxJRnPcJMuZ; python3 - <<'EOF'
import json, math
d=json.load(open('mini_demo_data.json')); fr=d['prereg']['frozen']
def _z(x, mu, sd): return 0.0 if x is None else (x - mu) / (sd if sd > 0 else 1.0)
def apply_logistic(model, feats):
    s = model["intercept"]
    for f, m, sd, c in zip(model["features"], model["mean"], model["sd"], model["coef"]): s += c * _z(feats.get(f), m, sd)
    return 1 / (1 + math.exp(-s))
mx=0; n=0
for r in d['per_item_E']:
    if r['coverage_status']=='UNPARSEABLE': continue
    f=dict(r); f['ALIGN:g_score']=r['g_score']
    use=fr['fusion'] if not (r.get('peer_unavailable') or r['g_score'] is None) else fr['text_only']
    p=apply_logistic(use,f); mx=max(mx,abs(p-r['p_peer_text'])); n+=1
    tp=apply_logistic(fr['text_only'],f); 
print(n,mx, list(fr.keys()))
EOF
```

### [25] TOOL RESULT — Bash · 2026-09-25 16:11:35 UTC

```
{"stdout": "93 0 ['variant', 'tau', 'k', 'timeout_ms', 'fusion', 'text_only', 'sensitivity_all_adj', 'peer_only']", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [26] ASSISTANT · 2026-09-25 16:13:03 UTC

```
The fusion reproduces `p_peer_text` exactly. Next I'll write the notebook.
```

### [27] TOOL CALL — Bash · 2026-09-25 16:13:03 UTC

```
mkdir -p /tmp/claude-0/-ai-inventor-aii-data-runs-run-An1uy2kF2SjZ-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-2-art-TaxJRnPcJMuZ/4e49c832-2fbe-4a52-9414-4d449ba99b62/scratchpad; cat > /tmp/claude-0/-ai-inventor-aii-data-runs-run-An1uy2kF2SjZ-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-2-art-TaxJRnPcJMuZ/4e49c832-2fbe-4a52-9414-4d449ba99b62/scratchpad/gen_nb.py <<'PYEOF'
import json, sys
cells = []
def md(s): cells.append({"cell_type": "markdown", "metadata... [truncated, 23682 chars total]
```

### [28] TOOL RESULT — Bash · 2026-09-25 16:13:03 UTC

```
{"stdout": "dict_keys(['P1_R_AB', 'P1_R_A', 'P2', 'P3', 'P4', 'criteria'])\n{\"P1_R_AB\": \"INCONCLUSIVE\", \"P1_R_A\": \"INCONCLUSIVE\", \"P2\": \"REFUTED\", \"P3\": \"INCONCLUSIVE\", \"P4\": \"REFUTED\", \"criteria\": {\"judge_cheap_disg\": {\"testable_pooled_R_AB (>=300/class)\": false, \"a_R_AB_CI_gt_0\": false, \"a_R_A_sign_gt_0\": false, \"criterion_a_this_artifact\": false, \"criterion_c_long_CI_gt_0\": false}, \"judge_local_qwen8b_disg\": {\"testable_pooled_R_AB (>=300/class)\": true, \"a_R_AB_CI_gt_0\": true, \"a_R_A_sign_gt_0\": true, \"criterion_a_this_artifact\": true, \"criterion_c_long_CI_gt_0\": true}}}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": true}
```

### [29] ASSISTANT · 2026-09-25 16:13:11 UTC

```
Notebook generated. For the first test run I'll set `N_ROWS` to a minimal 10.
```

### [30] TOOL CALL — Bash · 2026-09-25 16:13:11 UTC

```
sed -i 's/N_ROWS = 100          # original/N_ROWS = 10           # original/' code_demo.ipynb && grep -c "N_ROWS = 10  " code_demo.ipynb && UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_TaxJRnPcJMuZ-7aa3e4ae5ffc && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_TaxJRnPcJMuZ-7aa3e4ae5ffc/bin/python jupyter ipykernel && time /tmp/aii_nb_test_envs/art_TaxJRnPcJMuZ-7aa3e4ae5ffc/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -5
```

### [31] TOOL RESULT — Bash · 2026-09-25 16:13:47 UTC

```
{"stdout": "1\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n[NbConvertApp] Writing 93707 bytes to code_demo.ipynb\n\nreal\t0m31.085s\nuser\t0m21.909s\nsys\t0m3.469s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [32] TOOL CALL — Bash · 2026-09-25 16:13:51 UTC

```
python3 -c "
import json
nb=json.load(open('code_demo.ipynb'))
for c in nb['cells']:
    if c['cell_type']!='code': continue
    for o in c['outputs']:
        if o.get('output_type')=='stream': print(o['text'][-2500:] if isinstance(o['text'],str) else ''.join(o['text'])[-2500:])
        elif o.get('output_type')=='error': print('ERR',o['ename'],o['evalue'])
        else: print('[',o.get('output_type'), list(o.get('data',{}).keys()),']')
"
```

### [33] TOOL RESULT — Bash · 2026-09-25 16:13:51 UTC

```
{"stdout": "Curated 100-row subset of held-out dataset E (NL->FOL candidates, gold-free faithfulness scores + solver/adjudicated labels) for the PEER+TEXT demo. per_item_E = every metric score per row; E_labels = label view (joined only after scoring); E_blind = blind view (text + candidate FOL); analysis/prereg/p_tests = frozen full-E results.\n{'description': 'str', 'per_item_E': 100, 'E_labels': 100, 'E_blind': 100, 'analysis': 2, 'prereg': 3, 'p_tests': 6, 'prereg_sha256': 'str'}\n\nfrozen fusion features: ['ALIGN:g_score', 'c_score_align', 'l2_bow', 'l3_z3'] coef: [-0.116, 1.746, 3.087, 0.845] threshold: 0.69\nmax |recomputed - stored p_peer_text| over 10 rows: 0.00e+00\n\n16:13:44|INFO   |method_out.json: 10 examples, 0.1 MB\n\nFull E, R_AB pooled: n=2686 (errors=1822, correct=864)\n                metric  auroc  ci_lo  ci_hi  auprc\n     PEER+TEXT (fused)  0.790  0.752  0.823  0.879\nc_score_align (iter-1)  0.782  0.744  0.818  0.861\n   PEER only (g_score)  0.748  0.706  0.786  0.824\n            c_score_nf  0.746  0.705  0.784  0.828\n                L2-bow  0.734  0.706  0.762  0.830\n             TEXT only  0.693  0.652  0.732  0.812\n                 L3 z3  0.579  0.529  0.625  0.720\n\nOther frozen headline slices (PEER+TEXT vs c_score_align vs local judge):\n  R_AB long (L25+L20+EXC)    p_peer_text=0.768  c_score_align=0.759\n  R_A pooled L20+EXC         p_peer_text=0.818  c_score_align=0.860\n  R_AB CTRL                  p_peer_text=0.708  c_score_align=0.742\n\nDelta PEER+TEXT - local judge (pooled R_AB): +0.078  CI [+0.043, +0.112]  DeLong p=2.4e-12\n\nDemo subset (tiers A/B): 10 rows, 10 errors / 0 correct\n                metric  auroc  demo_auroc\n     PEER+TEXT (fused)  0.790         NaN\nc_score_align (iter-1)  0.782         NaN\n   PEER only (g_score)  0.748         NaN\n            c_score_nf  0.746         NaN\n                L2-bow  0.734         NaN\n             TEXT only  0.693         NaN\n                 L3 z3  0.579         NaN\n\n[ display_data ['image/png', 'text/plain'] ]\n                                                                  text                                                candidate_fol                 system p_peer_text flag signal top_code label tier\nA species of plant that produces flowers, is pollinated by insects or  ∀x (ProducesFlowers(x) ∧ (PollinatedByInsects(x) ∨ Pollinate G1b:meta-llama/llama-3    0.965779    1   PEER      ADD ERROR    B\nA scientist who studies astronomy or astrophysics but not both will ha ∀x ∀y (Scientist(x) ∧ Scientist(y) ∧ (Astronomy(x) ⊕ Astroph        malls_gpt4_gold    0.962414    1   PEER    QUANT ERROR    B\nA deciduous tree sheds its leaves annually, an evergreen tree retains  ∀x ((DeciduousTree(x) → ShedsAnnually(x, leaves)) ∧ (Evergre G3:mistralai/mistral-s    0.885209    1   PEER     DROP ERROR    B\nA scientific experiment x is conducted by a researcher y using equipme Conduction(x, y, z) → (Design(x, y) ∧ Execute(x, y) ∧ Employ G1:meta-llama/llama-3.    0.992581    1   PEER      ADD ERROR    B\nA parasitic relationship involves a parasite that lives on or in a hos ∀x (ParasiticRelationship(x) ↔ ∃p ∃h (Parasite(p) ∧ Host(h)  G2:qwen/qwen3-235b-a22    0.967483    1   PEER      ADD ERROR    B\nA setting is a rainforest when it is a dense, tropical or subtropical  ∀x (Setting(x) ∧ DenseForest(x) ∧ (Tropical(x) ∨ Subtropical     G6:microsoft/phi-4    0.928400    1   PEER      ADD ERROR    B\nAn animal is a mammal when it is a warm-blooded vertebrate, possesses  ∀x ((Animal(x) ∧ WarmBloodedVertebrate(x) ∧ PossessesHairOrF       F:openai/gpt-5.1    0.678812    0   PEER      ADD ERROR    A\nA setting is a rainforest when it is a dense, tropical or subtropical  ∀x (Setting(x) → (Rainforest(x) ↔ (DenseForest(x) ∧ (Tropica G4:deepseek/deepseek-v    0.764551    1   PEER      ADD ERROR    B\n\nPre-registered tests (full E):\n  P1_R_AB: INCONCLUSIVE\n  P1_R_A: INCONCLUSIVE\n  P2: REFUTED\n  P3: INCONCLUSIVE\n  P4: REFUTED\n  criteria: {\"judge_cheap_disg\": {\"testable_pooled_R_AB (>=300/class)\": false, \"a_R_AB_CI_gt_0\": false, \"a_R_A_sign_gt_0\": false, \"criterion_a_this_artifact\": false, \"crite", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [34] THINKING · 2026-09-25 16:13:57 UTC

```
The run passed, but I spotted three issues: local-judge rows are missing from the headline table, the markdown incorrectly states fusion has fewer than 4 features, and the subset ordering groups all ERROR rows first, leaving small N_ROWS runs with only one class. I'll check the metric keys next.
```

### [35] TOOL CALL — Bash · 2026-09-25 16:13:57 UTC

```
python3 -c "
import json
d=json.load(open('mini_demo_data.json'))
t=d['analysis']['a_tables']['R_AB pooled']; print(t.keys()); print(t['metrics'].keys())
for k,v in t.items():
  if k!='metrics': print(k, json.dumps(v)[:600])
"
```

### [36] TOOL RESULT — Bash · 2026-09-25 16:13:57 UTC

```
{"stdout": "dict_keys(['n', 'n_error', 'n_correct', 'n_sentences', 'metrics', 'paired', 'vs_judge_local_qwen8b_disg', 'vs_judge_local_qwen8b_orig', 'vs_judge_cheap_disg', 'vs_judge_cheap_orig'])\ndict_keys(['p_peer_text', 'peer_only', 'p_text', 'g_score', 'c_score_nf', 'c_score_align', 'l2_bow', 'l3_z3', 'nf_g_score', 'nf_c_score', 'p_sensitivity', 'g_score_k6', 'g_score_famfield', 'l1_any', 'l2_role'])\nn 2686\nn_error 1822\nn_correct 864\nn_sentences 292\npaired {\"p_peer_text - p_text\": {\"delta\": 0.09688141592470634, \"ci\": [0.06324073915040206, 0.13087146698961588], \"p_boot_le0\": 0.0, \"delong_z\": 12.558269759847686, \"delong_p\": 0.0}, \"p_peer_text - peer_only\": {\"delta\": 0.04197666382079124, \"ci\": [0.013715223077458701, 0.06927536246975752], \"p_boot_le0\": 0.0025, \"delong_z\": 4.175108755603893, \"delong_p\": 2.9784372880703458e-05}, \"p_peer_text - c_score_align\": {\"delta\": 0.0076635362036021615, \"ci\": [-0.010170490903609294, 0.025022947422011273], \"p_boot_le0\": 0.188, \"delong_z\": 1.2709605422857735, \"delong_p\": 0.2037426862740006}, \"c_score_align - nf_c_s\nvs_judge_local_qwen8b_disg {\"n\": 2686, \"n_error\": 1822, \"n_correct\": 864, \"n_sentences\": 292, \"metrics\": {\"p_peer_text\": {\"auroc\": 0.7900410873277229, \"ci\": [0.7515964802454704, 0.8234980895606637], \"auprc\": 0.8790429206220931, \"prevalence\": 0.6783320923306031}, \"p_text\": {\"auroc\": 0.6931596714030166, \"ci\": [0.6517033173882918, 0.7316063394711673], \"auprc\": 0.8119152615487248, \"prevalence\": 0.6783320923306031}, \"peer_only\": {\"auroc\": 0.7480644235069317, \"ci\": [0.7060020851444325, 0.7863879373530582], \"auprc\": 0.8240954811343213, \"prevalence\": 0.6783320923306031}, \"c_score_align\": {\"auroc\": 0.7823775511241208, \"ci\": [0.7\nvs_judge_local_qwen8b_orig {\"n\": 2686, \"n_error\": 1822, \"n_correct\": 864, \"n_sentences\": 292, \"metrics\": {\"p_peer_text\": {\"auroc\": 0.7900410873277229, \"ci\": [0.7515964802454704, 0.8234980895606637], \"auprc\": 0.8790429206220931, \"prevalence\": 0.6783320923306031}, \"p_text\": {\"auroc\": 0.6931596714030166, \"ci\": [0.6517033173882918, 0.7316063394711673], \"auprc\": 0.8119152615487248, \"prevalence\": 0.6783320923306031}, \"peer_only\": {\"auroc\": 0.7480644235069317, \"ci\": [0.7060020851444325, 0.7863879373530582], \"auprc\": 0.8240954811343213, \"prevalence\": 0.6783320923306031}, \"c_score_align\": {\"auroc\": 0.7823775511241208, \"ci\": [0.7\nvs_judge_cheap_disg {\"n\": 20, \"n_error\": 8, \"n_correct\": 12, \"n_sentences\": 16, \"metrics\": {\"p_peer_text\": {\"auroc\": 0.8072916666666666, \"ci\": [0.5, 1.0], \"auprc\": 0.7481150793650794, \"prevalence\": 0.4}, \"p_text\": {\"auroc\": 0.703125, \"ci\": [0.4062297077922078, 0.9501190476190474], \"auprc\": 0.5927083333333334, \"prevalence\": 0.4}, \"peer_only\": {\"auroc\": 0.6822916666666666, \"ci\": [0.38618125701459033, 0.96875], \"auprc\": 0.5597298534798535, \"prevalence\": 0.4}, \"c_score_align\": {\"auroc\": 0.6354166666666666, \"ci\": [0.3272314049586777, 0.9437847222222222], \"auprc\": 0.5154761904761904, \"prevalence\": 0.4}, \"judge_cheap_di\nvs_judge_cheap_orig {\"n\": 0, \"untestable\": true}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [37] THINKING · 2026-09-25 16:14:15 UTC

```
I found that judge AUROCs are excluded from `build_outputs`. I'll pull them from `data["analysis"]` in the visualization cell instead, fixing the markdown and subset ordering.
```

### [38] TOOL CALL — Bash · 2026-09-25 16:14:15 UTC

```
G=/tmp/claude-0/-ai-inventor-aii-data-runs-run-An1uy2kF2SjZ-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-2-art-TaxJRnPcJMuZ/4e49c832-2fbe-4a52-9414-4d449ba99b62/scratchpad/gen_nb.py && python3 - "$G" <<'EOF'
import sys
p=sys.argv[1]; t=open(p).read()
rep=[
("* Apply the frozen logistic. Its features are `ALIGN:g_score`, `c_score_align` and `l2_bow`.",
 "* Apply the frozen logistic. Its features are `ALIGN:g_score` (the PEER graded score), `c_score_align`, `l2_bow` and `l3_z3`."),
('''head = meta["headline_auroc_tables"]["R_AB pooled"]
rows = []
for k, lab in NAMES.items():
    m = head["metrics"].get(k)''',
'''head = meta["headline_auroc_tables"]["R_AB pooled"]
# the judge baselines are scored in the analysis's paired "vs_judge_*" sub-tables (same 2,686 rows), not in the headline table
judge_tab = {j: data["analysis"]["a_tables"]["R_AB pooled"][f"vs_{j}"]["metrics"].get(j) for j in ("judge_local_qwen8b_disg", "judge_local_qwen8b_orig")}
rows = []
for k, lab in NAMES.items():
    m = head["metrics"].get(k) or judge_tab.get(k)'''),
('''    mm = meta["headline_auroc_tables"].get(sl, {}).get("metrics", {})''',
'''    mm = dict(meta["headline_auroc_tables"].get(sl, {}).get("metrics", {}))
    mm.update((data["analysis"]["a_tables"].get(sl, {}).get("vs_judge_local_qwen8b_disg") or {}).get("metrics", {}))'''),
("40 ERROR and 40 CORRECT from tiers A/B, balanced over the strata L25/L20/EXC/CTRL, plus 20 unparseable, tier-C, contested or unresolved rows.",
 "40 ERROR and 40 CORRECT from tiers A/B, balanced over the strata L25/L20/EXC/CTRL, plus 20 unparseable, tier-C, contested or unresolved rows. The rows are interleaved, so any prefix mixes classes."),
]
for a,b in rep:
    assert a in t, a[:60]; t=t.replace(a,b)
open(p,'w').write(t)
EOF
python3 - <<'EOF'
import json
d=json.load(open('mini_demo_data.json'))
L={r['row_key']:r for r in d['E_labels']}
def cat(r):
    l=L[r['row_key']]; return l['final_label'] if l['final_label'] in('ERROR','CORRECT') and l['label_tier'] in('A','B') else 'OTHER'
g={c:[r for r in d['per_item_E'] if cat(r)==c] for c in ('ERROR','CORRECT','OTHER')}
# interleave strata inside each class: already ordered by stratum blocks of 10 -> round-robin
def rr(lst, key):
    b={}; [b.setdefault(key(r),[]).append(r) for r in lst]; out=[]
    while any(b.values()):
        for k in list(b):
            if b[k]: out.append(b[k].pop(0))
    return out
E=rr(g['ERROR'],lambda r:r['stratum']); C=rr(g['CORRECT'],lambda r:r['stratum']); O=g['OTHER']
order=[]
i=0
while E or C or O:
    for src,n in ((E,2),(C,2),(O,1)):
        for _ in range(n):
            if src: order.append(src.pop(0))
keys=[r['row_key'] for r in order]
d['per_item_E']=order
d['E_labels']=[L[k] for k in keys]
B={r['row_key']:r for r in d['E_blind']}; d['E_blind']=[B[k] for k in keys]
json.dump(d,open('mini_demo_data.json','w'),ensure_ascii=False)
print(len(order),[cat(r)[0]+r['stratum'] for r in order[:12]])
EOF
python3 $G code_demo.ipynb && sed -i 's/N_ROWS = 100          # original/N_ROWS = 10           # original/' code_demo.ipynb && time /tmp/aii_nb_test_envs/art_TaxJRnPcJMuZ-7aa3e4ae5ffc/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -2
```

### [39] TOOL RESULT — Bash · 2026-09-25 16:14:21 UTC

```
{"stdout": "100 ['EL25', 'EL20', 'CL25', 'CL20', 'OCTRL', 'EEXC', 'ECTRL', 'CEXC', 'CCTRL', 'OCTRL', 'EL25', 'EL20']\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n[NbConvertApp] Writing 105540 bytes to code_demo.ipynb\n\nreal\t0m6.573s\nuser\t0m5.178s\nsys\t0m0.765s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [40] ASSISTANT · 2026-09-25 16:14:31 UTC

```
The 10-row run passes. Runtime is negligible, so I'll scale straight to the whole 100-row subset and test in a fresh venv.
```

### [41] TOOL CALL — Bash · 2026-09-25 16:14:31 UTC

```
python3 /tmp/claude-0/-ai-inventor-aii-data-runs-run-An1uy2kF2SjZ-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-2-art-TaxJRnPcJMuZ/4e49c832-2fbe-4a52-9414-4d449ba99b62/scratchpad/gen_nb.py code_demo.ipynb && grep -o "N_ROWS = 100 [^\"]*" code_demo.ipynb && UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_TaxJRnPcJMuZ-7aa3e4ae5ffc && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_TaxJRnPcJMuZ-7aa3e4ae5ffc/bin/python jupyter ipykernel && time /tmp/aii_nb_test_envs/art_TaxJRnPcJMuZ-7aa3e4ae5ffc/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -1 && python3 -c "
import json
nb=json.load(open('code_demo.ipynb'))
for c in nb['cells'][-1:]+nb['cells'][9:10]:
    for o in c.get('outputs',[]):
        if o.get('output_type')=='stream': print(''.join(o['text'])[:4000])
        elif o.get('output_type')=='error': print('ERR',o['ename'],o['evalue'])
        else: print('[',o.get('output_type'), list(o.get('data',{}).keys()),']')
"
```

### [42] TOOL RESULT — Bash · 2026-09-25 16:15:01 UTC

```
{"stdout": "N_ROWS = 100          # original: all 8507 rows of dataset E\\nSTAGE = \\\n[NbConvertApp] Writing 106609 bytes to code_demo.ipynb\n\nreal\t0m27.033s\nuser\t0m21.166s\nsys\t0m2.973s\nFull E, R_AB pooled: n=2686 (errors=1822, correct=864)\n                      metric  auroc  ci_lo  ci_hi  auprc\n           PEER+TEXT (fused)  0.790  0.752  0.823  0.879\n      c_score_align (iter-1)  0.782  0.744  0.818  0.861\n         PEER only (g_score)  0.748  0.706  0.786  0.824\n                  c_score_nf  0.746  0.705  0.784  0.828\n                      L2-bow  0.734  0.706  0.762  0.830\nlocal Qwen3-8B judge (disg.)  0.712  0.673  0.747  0.816\n                   TEXT only  0.693  0.652  0.732  0.812\nlocal Qwen3-8B judge (orig.)  0.648  0.603  0.691  0.781\n                       L3 z3  0.579  0.529  0.625  0.720\n\nOther frozen headline slices (PEER+TEXT vs c_score_align vs local judge):\n  R_AB long (L25+L20+EXC)    p_peer_text=0.768  c_score_align=0.759  judge_local_qwen8b_disg=0.653\n  R_A pooled L20+EXC         p_peer_text=0.818  c_score_align=0.860  judge_local_qwen8b_disg=0.554\n  R_AB CTRL                  p_peer_text=0.708  c_score_align=0.742  judge_local_qwen8b_disg=0.739\n\nDelta PEER+TEXT - local judge (pooled R_AB): +0.078  CI [+0.043, +0.112]  DeLong p=2.4e-12\n\nDemo subset (tiers A/B): 80 rows, 40 errors / 40 correct\n                      metric  auroc  demo_auroc\n           PEER+TEXT (fused)  0.790       0.709\n      c_score_align (iter-1)  0.782       0.693\n         PEER only (g_score)  0.748       0.651\n                  c_score_nf  0.746       0.622\n                      L2-bow  0.734       0.694\nlocal Qwen3-8B judge (disg.)  0.712       0.662\n                   TEXT only  0.693       0.674\nlocal Qwen3-8B judge (orig.)  0.648       0.612\n                       L3 z3  0.579       0.572\n\n[ display_data ['image/png', 'text/plain'] ]\n                                                                  text                                                candidate_fol                 system p_peer_text flag signal top_code      label tier\nA species of plant that produces flowers, is pollinated by insects or  ∀x (ProducesFlowers(x) ∧ (PollinatedByInsects(x) ∨ Pollinate G1b:meta-llama/llama-3    0.965779    1   PEER      ADD      ERROR    B\nA movie can be a box office success if it has high grossing revenue an Movie(x) → (HighGrossingRevenue(x) ∧ PositiveReviews(x, crit G1:meta-llama/llama-3.    0.713875    1   PEER      ADD      ERROR    B\nAn asteroid is a small rocky body orbiting the sun, a comet is a celes ∀x (Asteroid(x) ↔ (SmallRockyBody(x) ∧ Orbits(x, sun))) ∧ ∀x G2:qwen/qwen3-235b-a22    0.734955    1   PEER      ADD    CORRECT    B\nA musical composition typically consisting of multiple movements, ofte ∀x (MusicalComposition(x) ∧ ConsistsOf(x, multipleMovements) G5:google/gemma-3-27b-    0.381126    0   PEER      ADD    CORRECT    B\n All students who can strike the right note can get the rhythms right.   ∀x (Student(x) ∧ CanStrikeNote(x) → CanGetRhythmsRight(x)) G5:google/gemma-3-27b-    0.315088    0   TEXT      ADD UNRESOLVED none\nA cell can be a prokaryote, eukaryote, or archaea, but can only be one ∀x (Cell(x) → (Prokaryote(x) ∨ Eukaryote(x) ∨ Archaea(x))) ∧ G9:cohere/command-r7b-    0.838921    1   PEER     DROP      ERROR    B\n                       William Dickinson supported the Portland Whigs.                    Supports(williamDickinson, portlandWhigs) G1b:meta-llama/llama-3    0.039958    0   TEXT     NONE      ERROR    B\n         You can't enter the building unless you have a key or a pass.             ∀x (EnterBuilding(x) → (HasKey(x) ∨ HasPass(x)))     G6:microsoft/phi-4    0.201557    0   TEXT      ADD    CORRECT    A\n\nPre-registered tests (full E):\n  P1_R_AB: INCONCLUSIVE\n  P1_R_A: INCONCLUSIVE\n  P2: REFUTED\n  P3: INCONCLUSIVE\n  P4: REFUTED\n  criteria: {\"judge_cheap_disg\": {\"testable_pooled_R_AB (>=300/class)\": false, \"a_R_AB_CI_gt_0\": false, \"a_R_A_sign_gt_0\": false, \"criterion_a_this_artifact\": false, \"crite", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [43] ASSISTANT · 2026-09-25 16:15:07 UTC

```
It passes on the full 100-row subset in 27 s in a clean venv. Let me look at the plot.
```

### [44] TOOL CALL — Bash · 2026-09-25 16:15:07 UTC

```
python3 -c "
import json,base64
nb=json.load(open('code_demo.ipynb'))
for c in nb['cells']:
    for o in c.get('outputs',[]):
        if 'image/png' in o.get('data',{}): open('/tmp/claude-0/-ai-inventor-aii-data-runs-run-An1uy2kF2SjZ-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-2-art-TaxJRnPcJMuZ/4e49c832-2fbe-4a52-9414-4d449ba99b62/scratchpad/plot.png','wb').write(base64.b64decode(o['data']['image/png']))
"; ls -la; du -sh .
```

### [45] TOOL RESULT — Bash · 2026-09-25 16:15:07 UTC

```
{"stdout": "total 5084\ndrwxr-xr-x 4 root root 2000111 Sep 25 16:14 .\ndrwxr-xr-x 3 root root 2000111 Sep 25 16:09 ..\ndrwxr-xr-x 2 root root       1 Sep 25 16:09 .aii\n-rw------- 1 root root      54 Sep 25 16:10 .aii_claude_session.json\n-rw-r--r-- 1 root root  262654 Sep 25 16:15 .repl_agent.ptylog\n-rw-r--r-- 1 root root  106671 Sep 25 16:14 code_demo.ipynb\ndrwxr-xr-x 2 root root   30700 Sep 25 16:13 logs\n-rw-r--r-- 1 root root  269299 Sep 25 16:14 method_out.json\n-rw-r--r-- 1 root root  537077 Sep 25 16:14 mini_demo_data.json\n3.1M\t.", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [46] TOOL CALL — Read · 2026-09-25 16:15:07 UTC

```
/tmp/claude-0/-ai-inventor-aii-data-runs-run-An1uy2kF2SjZ-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-2-art-TaxJRnPcJMuZ/4e49c832-2fbe-4a52-9414-4d449ba99b62/scratchpad/plot.png
```

### [47] TOOL RESULT — Read · 2026-09-25 16:15:07 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [48] THINKING · 2026-09-25 16:15:23 UTC

```
The plot looks correct. I'll now review the verification checks, README, manifest, and struct output, and remove the `method_out.json` file and `logs/` directory generated by the notebook run since they'll be recreated automatically.
```

### [49] TOOL CALL — Bash · 2026-09-25 16:15:23 UTC

```
rm -rf method_out.json logs && grep -c 'GITHUB_DATA_URL = \\"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_An1uy2kF2SjZ/round-2/experiment-5/demo/mini_demo_data.json\\"' code_demo.ipynb; grep -c "urllib.request.urlopen(GITHUB_DATA_URL)" code_demo.ipynb; ls -la mini_demo_data.json
cat > .aii/manifest.yaml <<'EOF'
# Nothing heavy in this workspace: code_demo.ipynb (~0.1 MB) and mini_demo_data.json (~0.5 MB) are text under the auto-keep floor.
entries: []
EOF
cat > README.md <<'EOF'
# PEER+TEXT held-out test: demo notebook

This is a runnable demo of the experiment **"Peer agreement plus text checks, held-out test"**. The experiment scores whether a natural-language to first-order-logic (NL→FOL) formalization is faithful to its sentence, without a gold formula. The score, PEER+TEXT, fuses two signals: graded agreement between model families, and solver-checked text tests. The fusion was frozen on a screening set and then scored once on held-out dataset E (8,507 candidate rows).

The notebook is the original driver `method.py` split into cells, with explanations between them. It runs the driver's `outputs` stage (`build_outputs`) on a curated 100-row subset of E. It also re-applies the frozen PEER+TEXT fusion to the stored features, which reproduces the shipped `p_peer_text` exactly. It ends by plotting:
* the frozen full-E AUROCs: PEER+TEXT 0.790 [0.75, 0.82], `c_score_align` 0.782, local Qwen3-8B judge 0.712, TEXT 0.693;
* the same metrics recomputed on the subset.

## Layout
| Path | What it is |
|---|---|
| `code_demo.ipynb` | The demo notebook, executed. It loads `mini_demo_data.json` from GitHub and falls back to the local copy. |
| `mini_demo_data.json` | 100 rows of E: 40 ERROR and 40 CORRECT from tiers A/B, balanced over strata L25/L20/EXC/CTRL across 13 systems, plus 20 unparseable, tier-C, contested or unresolved rows. It includes the per-item scores (`per_item_E`), the label view (`E_labels`), the blind view (`E_blind`), and the frozen `analysis` tables, `prereg`, `p_tests` and prereg sha256. |

## How to run
Open `code_demo.ipynb` in Colab or Jupyter and run all cells. The whole run takes about 30 s, including the install cell. The config cell sets:
* `N_ROWS`: rows passed to `build_outputs`. The demo uses 100; the original run used all 8,507.
* `STAGE`: fixed to `"outputs"`. The other stages (`views`, `api`, `local`, `screen`, `score`, `analyse`) need the original repository's `src/` scripts, an OpenRouter key and a GPU.

Running the notebook writes `method_out.json` and `logs/method.log` next to it.

## Restoring removed files
No files are marked `delete` in `.aii/manifest.yaml`, so there is nothing to restore. `method_out.json` and `logs/` are regenerated by running the notebook.
EOF
cat > .terminal_claude_agent_struct_out.json <<'EOF'
{"out_expected_files": {"notebook": "code_demo.ipynb", "mini_data_file": "mini_demo_data.json"}}
EOF
ls -la . .aii
```

### [50] TOOL RESULT — Bash · 2026-09-25 16:15:23 UTC

```
{"stdout": "1\n1\n-rw-r--r-- 1 root root 537077 Sep 25 16:14 mini_demo_data.json\n.:\ntotal 3051\ndrwxr-xr-x 3 root root 1090554 Sep 25 16:15 .\ndrwxr-xr-x 3 root root 1090554 Sep 25 16:09 ..\ndrwxr-xr-x 2 root root   14300 Sep 25 16:15 .aii\n-rw------- 1 root root      54 Sep 25 16:10 .aii_claude_session.json\n-rw-r--r-- 1 root root  280981 Sep 25 16:15 .repl_agent.ptylog\n-rw-r--r-- 1 root root      97 Sep 25 16:15 .terminal_claude_agent_struct_out.json\n-rw-r--r-- 1 root root    2258 Sep 25 16:15 README.md\n-rw-r--r-- 1 root root  106671 Sep 25 16:14 code_demo.ipynb\n-rw-r--r-- 1 root root  537077 Sep 25 16:14 mini_demo_data.json\n\n.aii:\ntotal 1080\ndrwxr-xr-x 2 root root   14300 Sep 25 16:15 .\ndrwxr-xr-x 3 root root 1090554 Sep 25 16:15 ..\n-rw-r--r-- 1 root root     143 Sep 25 16:15 manifest.yaml", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [51] ASSISTANT · 2026-09-25 16:15:33 UTC

```
I converted the artifact's `method.py` into a demo notebook, `code_demo.ipynb`, plus a 100-row data file, `mini_demo_data.json`. The notebook ran end to end in a fresh Python 3.12 test environment in about 27 s, well inside the 10-minute limit, at the largest setting the subset allows.

**What the notebook runs.** `method.py` is mostly a driver that launches other stages as separate processes. Those stages need an OpenRouter key, a GPU and hours of solver time, so they can't run in a notebook. Their results are shipped precomputed in the data file, and the notebook runs the driver's last stage, `build_outputs`, on them. The other stage code is kept but not executed (`STAGE = "outputs"`, where the original default was `"all"`).

**Changes to the original code:**
- `ROOT` is now `Path.cwd()`, because a notebook has no `__file__`.
- `build_outputs` reads its inputs from the loaded data instead of files; the original file paths are kept as comments.
- `main()` takes the stage from the config cell instead of the command line.
- `N_ROWS` limits the rows. It is set to 100, the whole subset; the original ran all 8,507 rows of E.

**Additions:**
- **Fusion check:** a copy of the frozen fusion code from `src/peer_text.py`, re-applied to the stored scores. It reproduces the saved PEER+TEXT scores exactly (difference 0.0). The frozen model has 4 inputs (it also uses `l3_z3`), not the 3 listed in the artifact's preview file.
- **Results cell:** tables and a two-panel plot.
  - Frozen full-E AUROCs: PEER+TEXT 0.790 [0.75, 0.82], `c_score_align` 0.782, local judge 0.712, TEXT alone 0.693.
  - Difference from the local judge: +0.078.
  - The same scores recomputed on the 80 A/B-labelled demo rows: PEER+TEXT 0.709, `c_score_align` 0.693, local judge 0.662. With so few rows these numbers are noisy.
  - Example rows and the pre-registered test outcomes.

**Data file.** It holds 40 ERROR and 40 CORRECT rows from label tiers A/B, spread evenly over the four sentence strata and 13 systems. It also has 20 rows that are unparseable, tier-C, contested or unresolved. The rows are interleaved so any first slice mixes both classes. For each row it includes the scores, the label and the sentence with its candidate FOL, plus the frozen analysis tables, pre-registration details and test results. It is about 0.5 MB.

**Checks:**
- The notebook contains `GITHUB_DATA_URL` exactly as given.
- It loads through the GitHub URL with a local fallback, not a bare `open()`.
- `mini_demo_data.json` exists.

The GitHub URL won't work until the files are pushed, so for now it falls back to the local copy.

I also wrote `README.md` and `.aii/manifest.yaml`. The manifest has no entries because nothing in the workspace is large. `.terminal_claude_agent_struct_out.json` is written.

Files are in the workspace:
- `code_demo.ipynb`
- `mini_demo_data.json`
- `README.md`
```
