# gen_demo_art_experiment_13 — report_results

> Phase: `gen_paper_repo` · `gen_demo_art`
> Run: `run_u75jRHUss0zo` — Gold-Free Faithfulness Metrics for NL-to-FOL Translation
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_demo_art_experiment_13` (terminal_claude_agent, claude-opus-5-5)

### [1] CONFIG · 2026-09-24 19:17:35 UTC

```
model: claude-opus-5-5 | effort: high | permission: bypassPermissions
```

### [2] SYSTEM-USER prompt · 2026-09-24 19:17:41 UTC

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
Your workspace: `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_EU1yuNrRl4od`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_EU1yuNrRl4od/`:
GOOD: `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_EU1yuNrRl4od/file.py`, `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_EU1yuNrRl4od/results/out.json`
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
id: art_EU1yuNrRl4od
type: experiment
title: Screening fixes for model-agreement false alarms
summary: >-
  Iteration-5 FREEZE on dataset E (DEVELOPMENT data; nothing here confirms). PART A ($0): five label-free rescorings of frozen
  V0 = c_score_align, computed only from eval-2's pairwise eqmv matrix, sealed (sha256) before any label join. V1 plurality-normalised,
  V2 reliability-weighted (out-of-fold family weights), V3 = V1+V2, V4 cross-fitted exact/align logistic, V5 = V3 on the 3-pool.
  Gates reproduce exactly: G0 V0 strat 0.7415 and Δ +0.099 [0.049, 0.146]; G1 24/8,469 = 0.28% (the 6-decimal rounding of
  the frozen column is handled at 1e-6, D1); c_exact 0.748; 3-pool 0.7845; eval-3 oracle 0.385 / 0.542. Z = 2,672 rows. LONG-strat
  AUROC: V0 0.743; Δ V1 -0.004, V2 +0.0075 [0.004, 0.011], V3 +0.007, V4 +0.009 [-0.004, 0.021], V5 +0.003. The pre-registered
  rule (Δ LONG >= +0.015, L25 >= V0, CTRL >= V0 - 0.01) gives 'NONE: V0 stands'. Stability: NONE 87.6%, V4 11.8%. Null: some
  variant qualifies in 3.5% of permutations. Mechanism: plurality normalisation trades d for e (ALL d 0.490 -> 0.174, e 0.140
  -> 0.343; MEANING_RENAME-type e 0.502 -> 0.872). No variant lowers d without raising e. The 9-family oracle gap is ILL_CONDITIONED
  (d_oracle 0.586 > d_V0 0.490). Marker M1 freeze/CONSENSUS_FREEZE_READY.json was written 12 min after the first code, with
  freeze/selection.json and consensus_variants.py (20-row reproduction to 1e-9). PART B ($0.22): GG = exact z3 equivalence
  OR an exhaustive injective arity-consistent symbol map giving z3 equivalence AND gemini-2.5-flash (non-thinking) says YES
  for every renamed pair. Checker gate G-A: dev v1 0.780 fails; the one allowed revision v2 scores 0.907 on the confirm half.
  G-B (R_COMP renames): 0.950 / 0.941, NOT_TESTABLE as a gate with only 53 YES pairs (D2). Dev gates: g1 SYN paired flip 0.034
  and g2 MEANING_RENAME recall 1.0 both pass, trivially because base FA is 0.83. g3 FAILS: E ALL-strat 0.696 vs V0 0.742,
  Δ -0.046 [-0.071, -0.021], so GG = FAIL(g3) and the boundary statement is written. GG halves error endorsement (e 0.140
  -> 0.081; MEANING_RENAME-type 0.502 -> 0.224) but raises d (0.490 -> 0.629): all 678 granularity (gran) pairs fail the bijection
  prefilter and 268 align pairs are gloss-rejected. Cost per candidate: 0.038 CPU-s + <= $0.00005. Secondary GG_B (freelab
  B1-B5 bridges) searched 11,202 pairs; its gloss is UNTESTED(budget) because the run-level OpenRouter budget was exhausted
  (HTTP 403, D13). Its all-accepted bracket is worse (ALL-strat 0.653; e 0.334): the bridges absorb ADD/DROP errors. PART
  C: lib/api.py over byte-identically vendored code (lib/PROVENANCE.json sha256), with modes align/exact/nf/hyb/pn/rw/gg,
  graded_consensus, pairwise_matrix/ed_decomposition, peer_text_score, eqmv(+exhaustive), minimal_typed_repair, freelab labelling
  tools and FOL-Triage layers. smoke_lib.py passes on 10 E rows. Checks: 14 pytest tests pass; tests/audit_rederive.py re-derives
  the decision, the Δ (1e-9) and the GG gates; the shuffled-label placebo gives ~0.48-0.49. Outputs: method_out.json (exp_gen_sol_out:
  E_heldout 8,507 rows with predict_V0..V5, c_exact, gg, gg_allyes, gg_b_allyes; PERTURB_E_bases 722; GG_checker_gates 1,069),
  tables.md, screen_E.json, gg_dev.json, ggb_dev.json, deviations.json (D1-D13), cost_ledger.jsonl.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_14
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
Raw data URL: https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/main/round-5/experiment-14/demo/mini_demo_data.json

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
GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/main/round-5/experiment-14/demo/mini_demo_data.json"
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
TODO 6. Verify: (1) code_demo.ipynb contains GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/main/round-5/experiment-14/demo/mini_demo_data.json" exactly, (2) mini_demo_data.json exists, (3) uses GitHub URL pattern not just open('mini_demo_data.json').
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

### [3] HUMAN-USER prompt · 2026-09-24 19:17:41 UTC

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

### [4] TOOL CALL — Skill · 2026-09-24 19:17:45 UTC

```
aii-colab
```

### [5] TOOL CALL — Skill · 2026-09-24 19:17:45 UTC

```
aii-long-running-tasks
```

### [6] TOOL RESULT — Skill · 2026-09-24 19:17:45 UTC

```
{"success": true, "commandName": "aii-colab"}
```

### [7] TOOL RESULT — Skill · 2026-09-24 19:17:45 UTC

```
{"success": true, "commandName": "aii-long-running-tasks"}
```

### [8] TOOL CALL — Bash · 2026-09-24 19:17:47 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_14; ls -la $W; wc -l $W/method.py; ls -la $W/* | head -80; cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_EU1yuNrRl4od; ls -la; ls .aii
```

### [9] TOOL RESULT — Bash · 2026-09-24 19:17:49 UTC

```
{"stdout": "total 42825\ndrwxr-xr-x 11 root root  2006067 Sep 24 16:53 .\ndrwxr-xr-x  7 root root  2040101 Sep 24 11:06 ..\ndrwxr-xr-x  2 root root    52500 Sep 24 12:19 .aii\n-rw-------  1 root root       54 Sep 24 11:08 .aii_claude_session.json\n-rw-------  1 root root    12585 Sep 24 12:19 .aii_worker_result.json\n-rw-r--r--  1 root root  2490360 Sep 24 12:19 .repl_agent.ptylog\n-rw-r--r--  1 root root     3876 Sep 24 12:18 .terminal_claude_agent_struct_out.json\n-rw-r--r--  1 root root    14804 Sep 24 12:17 README.md\n-rw-r--r--  1 root root   153465 Sep 24 11:28 cost_ledger.jsonl\n-rw-r--r--  1 root root     5557 Sep 24 12:12 deviations.json\ndrwxr-xr-x  2 root root  1007327 Sep 24 16:53 freeze\n-rw-r--r--  1 root root 14545469 Sep 24 12:13 full_method_out.json\ndrwxr-xr-x  5 root root  2000430 Sep 24 11:14 inputs_copy\n-rw-r--r--  1 root root     9774 Sep 24 11:14 inputs_manifest.json\ndrwxr-xr-x  3 root root  2000219 Sep 24 16:53 lib\ndrwxr-xr-x  2 root root  1036962 Sep 24 12:16 logs\n-rw-r--r--  1 root root     4041 Sep 24 12:15 method.py\n-rw-r--r--  1 root root 11354569 Sep 24 12:16 method_out.json\n-rw-r--r--  1 root root    14054 Sep 24 12:13 mini_method_out.json\n-rw-r--r--  1 root root     6383 Sep 24 11:24 prereg_gg.json\n-rw-r--r--  1 root root       81 Sep 24 11:24 prereg_gg.sha256\n-rw-r--r--  1 root root     5952 Sep 24 11:16 prereg_improve.json\n-rw-r--r--  1 root root       86 Sep 24 11:16 prereg_improve.sha256\n-rw-r--r--  1 root root     1086 Sep 24 11:16 prereg_improve_addendum.json\n-rw-r--r--  1 root root      165 Sep 24 11:17 prereg_improve_addendum_v4.json\n-rw-r--r--  1 root root    13818 Sep 24 12:13 preview_method_out.json\n-rw-r--r--  1 root root      638 Sep 24 11:26 prompt_revision_v2.json\n-rw-r--r--  1 root root      609 Sep 24 11:34 pyproject.toml\n-rw-r--r--  1 root root       51 Sep 24 11:20 pytest.ini\n-rw-r--r--  1 root root     3840 Sep 24 12:17 reproducibility.md\ndrwxr-xr-x  2 root root  2002619 Sep 24 12:14 results\ndrwxr-xr-x  2 root root  1015269 Sep 24 16:53 src\ndrwxr-xr-x  2 root root  1003344 Sep 24 12:09 tables\n-rw-r--r--  1 root root    35343 Sep 24 12:16 tables.md\ndrwxr-xr-x  2 root root  1001778 Sep 24 16:53 tests\n90 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/method.py\n-rw-r--r-- 1 root root    14804 Sep 24 12:17 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/README.md\n-rw-r--r-- 1 root root   153465 Sep 24 11:28 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/cost_ledger.jsonl\n-rw-r--r-- 1 root root     5557 Sep 24 12:12 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/deviations.json\n-rw-r--r-- 1 root root 14545469 Sep 24 12:13 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/full_method_out.json\n-rw-r--r-- 1 root root     9774 Sep 24 11:14 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/inputs_manifest.json\n-rw-r--r-- 1 root root     4041 Sep 24 12:15 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/method.py\n-rw-r--r-- 1 root root 11354569 Sep 24 12:16 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/method_out.json\n-rw-r--r-- 1 root root    14054 Sep 24 12:13 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/mini_method_out.json\n-rw-r--r-- 1 root root     6383 Sep 24 11:24 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/prereg_gg.json\n-rw-r--r-- 1 root root       81 Sep 24 11:24 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/prereg_gg.sha256\n-rw-r--r-- 1 root root     5952 Sep 24 11:16 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/prereg_improve.json\n-rw-r--r-- 1 root root       86 Sep 24 11:16 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/prereg_improve.sha256\n-rw-r--r-- 1 root root     1086 Sep 24 11:16 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/prereg_improve_addendum.json\n-rw-r--r-- 1 root root      165 Sep 24 11:17 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/prereg_improve_addendum_v4.json\n-rw-r--r-- 1 root root    13818 Sep 24 12:13 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/preview_method_out.json\n-rw-r--r-- 1 root root      638 Sep 24 11:26 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/prompt_revision_v2.json\n-rw-r--r-- 1 root root      609 Sep 24 11:34 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/pyproject.toml\n-rw-r--r-- 1 root root       51 Sep 24 11:20 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/pytest.ini\n-rw-r--r-- 1 root root     3840 Sep 24 12:17 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/reproducibility.md\n-rw-r--r-- 1 root root    35343 Sep 24 12:16 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/tables.md\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/freeze:\ntotal 3019\ndrwxr-xr-x  2 root root 1007327 Sep 24 16:53 .\ndrwxr-xr-x 11 root root 2006067 Sep 24 16:53 ..\n-rw-r--r--  1 root root    1451 Sep 24 12:12 CONSENSUS_FREEZE_READY.json\n-rw-r--r--  1 root root   10780 Sep 24 11:13 consensus_variants.py\n-rw-r--r--  1 root root   18869 Sep 24 11:22 gg.py\n-rw-r--r--  1 root root    9244 Sep 24 11:21 gg_fol.py\n-rw-r--r--  1 root root    6233 Sep 24 11:30 gg_gate.json\n-rw-r--r--  1 root root   28456 Sep 24 11:20 selection.json\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/inputs_copy:\ntotal 7841\ndrwxr-xr-x  5 root root 2000430 Sep 24 11:14 .\ndrwxr-xr-x 11 root root 2006067 Sep 24 16:53 ..\ndrwxr-xr-x  3 root root 1001676 Sep 24 11:14 iter_2\ndrwxr-xr-x  3 root root 2000410 Sep 24 11:14 iter_3\ndrwxr-xr-x  3 root root 1018832 Sep 24 11:14 iter_4\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/lib:\ntotal 5952\ndrwxr-xr-x  3 root root 2000219 Sep 24 16:53 .\ndrwxr-xr-x 11 root root 2006067 Sep 24 16:53 ..\n-rw-r--r--  1 root root    3248 Sep 24 11:58 INVENTORY.csv\n-rw-r--r--  1 root root   71283 Sep 24 11:32 PROVENANCE.json\n-rw-r--r--  1 root root   12235 Sep 24 11:34 api.py\ndrwxr-xr-x  7 root root 2000211 Sep 24 11:32 vendor\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/logs:\ntotal 3346\ndrwxr-xr-x  2 root root 1036962 Sep 24 12:16 .\ndrwxr-xr-x 11 root root 2006067 Sep 24 16:53 ..\n-rw-r--r--  1 root root     841 Sep 24 11:17 fit_v4.log\n-rw-r--r--  1 root root  130651 Sep 24 11:26 gg_gates.log\n-rw-r--r--  1 root root  223414 Sep 24 11:28 gg_gloss.log\n-rw-r--r--  1 root root    6562 Sep 24 11:58 gg_score.log\n-rw-r--r--  1 root root    2227 Sep 24 11:24 gg_search.log\n-rw-r--r--  1 root root     852 Sep 24 11:24 gg_search_all.out\n-rw-r--r--  1 root root    3443 Sep 24 12:12 ggb_score.log\n-rw-r--r--  1 root root       0 Sep 24 11:37 ggb_search.log\n-rw-r--r--  1 root root     982 Sep 24 12:08 ggb_search_all.out\n-rw-r--r--  1 root root    3397 Sep 24 12:16 method.log\n-rw-r--r--  1 root root    2302 Sep 24 11:16 score_variants.log\n-rw-r--r--  1 root root    1762 Sep 24 11:18 screen.log\n-rw-r--r--  1 root root     576 Sep 24 11:19 select.log\n-rw-r--r--  1 root root     932 Sep 24 11:35 smoke_lib.out\n-rw-r--r--  1 root root     559 Sep 24 11:15 step0_gates.log\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/results:\ntotal 30751\ndrwxr-xr-x  2 root root 2002619 Sep 24 12:14 .\ndrwxr-xr-x 11 root root 2006067 Sep 24 16:53 ..\n-rw-r--r--  1 root root    1386 Sep 24 12:16 audit_rederive.json\n-rw-r--r--  1 root root    1834 Sep 24 11:16 family_weights.json\n-rw-r--r--  1 root root     169 Sep 24 12:14 final_key_check.json\n-rw-r--r--  1 root root    1136 Sep 24 11:15 gate_G0.json\n-rw-r--r--  1 root root    3029 Sep 24 11:16 gate_G1_labelfree.json\n-rw-r--r--  1 root root   43134 Sep 24 11:58 gg_dev.json\n-rw-r--r--  1 root root  117395 Sep 24 11:26 gg_gate_items_B.json\ntotal 1993\ndrwxr-xr-x 3 root root 1003113 Sep 24 19:17 .\ndrwxr-xr-x 3 root root 1003113 Sep 24 19:17 ..\ndrwxr-xr-x 2 root root       1 Sep 24 19:17 .aii\n-rw------- 1 root root      54 Sep 24 19:17 .aii_claude_session.json\n-rw-r--r-- 1 root root   31831 Sep 24 19:17 .repl_agent.ptylog", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [10] TOOL CALL — Bash · 2026-09-24 19:17:51 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_14; cat $W/method.py; ls -la $W/results $W/src $W/tests $W/tables; cat $W/reproducibility.md
```

### [11] TOOL RESULT — Bash · 2026-09-24 19:17:51 UTC

````
{"stdout": "#!/usr/bin/env python3\n\"\"\"Orchestrator of the iteration-5 FREEZE experiment (Part A V0-V5 screen, Part B GG, Part C library, outputs).\n\nRuns the src/ scripts in the pre-registered order under PYTHONHASHSEED=0. Idempotent: a step whose declared output already\nexists is skipped (the prereg / freeze writers also refuse to overwrite on their own), so re-running never re-bills\nOpenRouter (every gloss verdict is cached in results/gloss_cache.jsonl) and never rewrites a frozen file.\n\nUsage:\n  .venv/bin/python method.py                      # every stage\n  .venv/bin/python method.py --stage A            # A | B | GGB | C | OUT | TEST (comma-separated)\n  .venv/bin/python method.py --stage OUT --force  # re-run steps even if their outputs exist (frozen writers still refuse)\n\"\"\"\nfrom __future__ import annotations\n\nimport argparse\nimport os\nimport subprocess\nimport sys\nimport time\nfrom pathlib import Path\n\nfrom loguru import logger\n\nROOT = Path(__file__).resolve().parent\nSRC = ROOT / \"src\"\nPY = sys.executable\n\nlogger.remove()\nlogger.add(sys.stdout, level=\"INFO\", format=\"{time:HH:mm:ss}|{level:<7}|{message}\")\n(ROOT / \"logs\").mkdir(exist_ok=True)\nlogger.add(ROOT / \"logs\" / \"method.log\", rotation=\"30 MB\", level=\"DEBUG\")\n\n# (stage, script + args, cwd, output that marks the step done)\nSTEPS = [\n    (\"A\", [\"copy_inputs.py\"], SRC, \"inputs_manifest.json\"),\n    (\"A\", [\"step0_gates.py\"], SRC, \"results/gate_G0.json\"),\n    (\"A\", [\"prereg_improve.py\"], SRC, \"prereg_improve.json\"),\n    (\"A\", [\"make_row_index.py\"], SRC, \"results/row_index_labelfree.jsonl\"),\n    (\"A\", [\"score_variants.py\"], SRC, \"results/scores_E_variants.jsonl\"),\n    (\"A\", [\"fit_v4.py\"], SRC, \"results/scores_E_V4.jsonl\"),\n    (\"A\", [\"screen.py\"], SRC, \"results/screen_E.json\"),\n    (\"A\", [\"select_rule.py\"], SRC, \"results/selection_E.json\"),\n    (\"A\", [\"freeze_part_a.py\"], SRC, \"freeze/selection.json\"),\n    (\"B\", [\"probe.py\"], SRC, \"results/probe.json\"),\n    (\"B\", [\"prereg_gg.py\"], SRC, \"prereg_gg.json\"),\n    (\"B\", [\"gg_search.py\", \"all\"], SRC, \"results/gg_search.jsonl\"),\n    (\"B\", [\"gg_gates.py\", \"dev\", \"v1\"], SRC, \"results/gg_gates_dev_v1.json\"),\n    (\"B\", [\"gg_gates.py\", \"confirm\", \"v2\"], SRC, \"results/gg_gates_confirm_v2.json\"),\n    (\"B\", [\"gg_gloss.py\"], SRC, \"results/gg_verdicts.json\"),\n    (\"B\", [\"gg_score.py\"], SRC, \"results/gg_dev.json\"),\n    (\"B\", [\"freeze_part_b.py\"], SRC, \"freeze/gg_gate.json\"),\n    (\"GGB\", [\"ggb_search.py\", \"all\"], SRC, \"results/ggb_search.jsonl\"),\n    (\"GGB\", [\"ggb_score.py\"], SRC, \"results/ggb_dev.json\"),\n    (\"C\", [\"vendor_lib.py\"], SRC, \"lib/PROVENANCE.json\"),\n    (\"OUT\", [\"make_outputs.py\"], SRC, \"method_out.json\"),\n    (\"OUT\", [\"make_tables.py\"], SRC, \"tables.md\"),\n    (\"TEST\", [\"-m\", \"pytest\", \"-q\", \"tests/test_variants.py\", \"tests/test_gg.py\", \"tests/test_budget.py\"], ROOT, None),\n    (\"TEST\", [\"tests/audit_rederive.py\"], ROOT, None),\n    (\"TEST\", [\"tests/smoke_lib.py\"], ROOT, None),\n]\nNEVER_FORCE = {\"prereg_improve.py\", \"prereg_gg.py\", \"freeze_part_a.py\"}  # immutable writers\n\n\n@logger.catch(reraise=True)\ndef main():\n    ap = argparse.ArgumentParser()\n    ap.add_argument(\"--stage\", default=\"A,B,GGB,C,OUT,TEST\")\n    ap.add_argument(\"--force\", action=\"store_true\")\n    a = ap.parse_args()\n    stages = set(a.stage.split(\",\"))\n    env = {**os.environ, \"PYTHONHASHSEED\": \"0\"}\n    for stage, args, cwd, marker in STEPS:\n        if stage not in stages:\n            continue\n        name = args[0]\n        if marker and (ROOT / marker).exists() and (not a.force or name in NEVER_FORCE):\n            logger.info(f\"[{stage}] skip {' '.join(args)} ({marker} exists)\")\n            continue\n        logger.info(f\"[{stage}] run {' '.join(args)}\")\n        t0 = time.time()\n        try:\n            subprocess.run([PY, *args], cwd=cwd, env=env, check=True)\n        except subprocess.CalledProcessError as e:\n            logger.error(f\"[{stage}] {name} failed with exit code {e.returncode}\")\n            raise\n        logger.info(f\"[{stage}] {name} done in {time.time() - t0:.0f}s\")\n\n\nif __name__ == \"__main__\":\n    main()\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/results:\ntotal 30751\ndrwxr-xr-x  2 root root 2002619 Sep 24 12:14 .\ndrwxr-xr-x 11 root root 2006067 Sep 24 16:53 ..\n-rw-r--r--  1 root root    1386 Sep 24 12:16 audit_rederive.json\n-rw-r--r--  1 root root    1834 Sep 24 11:16 family_weights.json\n-rw-r--r--  1 root root     169 Sep 24 12:14 final_key_check.json\n-rw-r--r--  1 root root    1136 Sep 24 11:15 gate_G0.json\n-rw-r--r--  1 root root    3029 Sep 24 11:16 gate_G1_labelfree.json\n-rw-r--r--  1 root root   43134 Sep 24 11:58 gg_dev.json\n-rw-r--r--  1 root root  117395 Sep 24 11:26 gg_gate_items_B.json\n-rw-r--r--  1 root root    3802 Sep 24 11:26 gg_gates_confirm_v2.json\n-rw-r--r--  1 root root    4332 Sep 24 11:26 gg_gates_dev_v1.json\n-rw-r--r--  1 root root     780 Sep 24 11:28 gg_gloss_run.json\n-rw-r--r--  1 root root 7712106 Sep 24 11:24 gg_search.jsonl\n-rw-r--r--  1 root root   84658 Sep 24 11:23 gg_search_pilot.jsonl\n-rw-r--r--  1 root root  297511 Sep 24 11:28 gg_verdicts.json\n-rw-r--r--  1 root root   10395 Sep 24 12:12 ggb_dev.json\n-rw-r--r--  1 root root 8052617 Sep 24 12:09 ggb_search.jsonl\n-rw-r--r--  1 root root  145634 Sep 24 11:38 ggb_search_pilot.jsonl\n-rw-r--r--  1 root root 1535190 Sep 24 12:12 ggb_verdicts.json\n-rw-r--r--  1 root root  930962 Sep 24 11:28 gloss_cache.jsonl\n-rw-r--r--  1 root root     714 Sep 24 11:12 probe.json\n-rw-r--r--  1 root root    1444 Sep 24 11:26 prompt_gateA_v2.json\n-rw-r--r--  1 root root    1439 Sep 24 11:26 prompt_gg_v2.json\n-rw-r--r--  1 root root 2988136 Sep 24 11:16 row_index_labelfree.jsonl\n-rw-r--r--  1 root root  726223 Sep 24 11:17 scores_E_V4.jsonl\n-rw-r--r--  1 root root 3414469 Sep 24 11:16 scores_E_variants.jsonl\n-rw-r--r--  1 root root  746992 Sep 24 11:58 scores_gg_E.jsonl\n-rw-r--r--  1 root root  235752 Sep 24 11:58 scores_gg_perturb.jsonl\n-rw-r--r--  1 root root  306740 Sep 24 12:12 scores_ggb_E.jsonl\n-rw-r--r--  1 root root   90867 Sep 24 11:18 screen_E.json\n-rw-r--r--  1 root root    2176 Sep 24 11:19 selection_E.json\n-rw-r--r--  1 root root    8325 Sep 24 12:16 smoke_lib.json\n-rw-r--r--  1 root root    1062 Sep 24 11:17 v4_coefs.json\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/src:\ntotal 3110\ndrwxr-xr-x  2 root root 1015269 Sep 24 16:53 .\ndrwxr-xr-x 11 root root 2006067 Sep 24 16:53 ..\n-rw-r--r--  1 root root    2995 Sep 24 11:14 common.py\n-rw-r--r--  1 root root    2385 Sep 24 11:14 copy_inputs.py\n-rw-r--r--  1 root root    2276 Sep 24 11:17 fit_v4.py\n-rw-r--r--  1 root root    3857 Sep 24 11:20 freeze_part_a.py\n-rw-r--r--  1 root root    2831 Sep 24 11:30 freeze_part_b.py\n-rw-r--r--  1 root root    9827 Sep 24 11:25 gg_gates.py\n-rw-r--r--  1 root root    4246 Sep 24 11:27 gg_gloss.py\n-rw-r--r--  1 root root   16298 Sep 24 11:58 gg_score.py\n-rw-r--r--  1 root root    5716 Sep 24 11:23 gg_search.py\n-rw-r--r--  1 root root   10543 Sep 24 12:12 ggb_score.py\n-rw-r--r--  1 root root    6650 Sep 24 11:37 ggb_search.py\n-rw-r--r--  1 root root    7359 Sep 24 11:24 gloss_client.py\n-rw-r--r--  1 root root    3474 Sep 24 11:17 labels.py\n-rw-r--r--  1 root root    7904 Sep 24 12:11 make_outputs.py\n-rw-r--r--  1 root root    1003 Sep 24 11:16 make_row_index.py\n-rw-r--r--  1 root root   18292 Sep 24 12:11 make_tables.py\n-rw-r--r--  1 root root    6274 Sep 24 11:24 prereg_gg.py\n-rw-r--r--  1 root root    6835 Sep 24 11:16 prereg_improve.py\n-rw-r--r--  1 root root    1618 Sep 24 11:12 probe.py\n-rw-r--r--  1 root root    5200 Sep 24 11:16 score_variants.py\n-rw-r--r--  1 root root   12932 Sep 24 11:18 screen.py\n-rw-r--r--  1 root root    5711 Sep 24 11:19 select_rule.py\n-rw-r--r--  1 root root    6847 Sep 24 11:14 stats.py\n-rw-r--r--  1 root root    3045 Sep 24 11:15 step0_gates.py\n-rw-r--r--  1 root root    2245 Sep 24 11:31 vendor_lib.py\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/tables:\ntotal 2975\ndrwxr-xr-x  2 root root 1003344 Sep 24 12:09 .\ndrwxr-xr-x 11 root root 2006067 Sep 24 16:53 ..\n-rw-r--r--  1 root root    2114 Sep 24 11:58 gg_ed.csv\n-rw-r--r--  1 root root     756 Sep 24 11:58 gg_t9_e.csv\n-rw-r--r--  1 root root    3586 Sep 24 12:12 ggb_auroc.csv\n-rw-r--r--  1 root root    6463 Sep 24 11:18 screen_auroc.csv\n-rw-r--r--  1 root root    5128 Sep 24 11:18 screen_delta_vs_V0.csv\n-rw-r--r--  1 root root   11655 Sep 24 11:18 screen_ed.csv\n-rw-r--r--  1 root root    4550 Sep 24 11:18 screen_t9_e.csv\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/tests:\ntotal 2957\ndrwxr-xr-x  2 root root 1001778 Sep 24 16:53 .\ndrwxr-xr-x 11 root root 2006067 Sep 24 16:53 ..\n-rw-r--r--  1 root root    4935 Sep 24 11:39 audit_rederive.py\n-rw-r--r--  1 root root    5392 Sep 24 11:33 smoke_lib.py\n-rw-r--r--  1 root root    1084 Sep 24 11:42 test_budget.py\n-rw-r--r--  1 root root    2424 Sep 24 11:42 test_gg.py\n-rw-r--r--  1 root root    4381 Sep 24 11:20 test_variants.py\n# Reproducibility\n\n## Environment\n\n| item | value |\n|---|---|\n| Python | 3.12.14 (uv venv) |\n| key packages | z3-solver 5.1.0.0 (= eval-2 matrix, `z3_version` 5.1.0), numpy 2.5.3, pandas 3.0.6, scikit-learn 1.9.1, scipy 1.18.1, loguru 0.7.3, httpx, nltk |\n| hardware | CPU only; 8 vCPU container (cgroup), 29 GB RAM limit; map searches used 6 spawn workers with RLIMIT_AS 3 GB each |\n| hash seed | every script runs with `PYTHONHASHSEED=0` (`method.py` sets it) |\n| bootstrap | sentence-cluster percentile, B = 2000, seed 20260924 (eval-2 `SentBoot` weights = exp-6 `ClusterBoot` draws for the same seed); gate G0 uses exp-6's own estimator with seed 0 |\n| stability / null | seeds 20260925 (500 within-stratum resamples) / 20260926 (200 within-stratum label permutations) |\n| folds | `int(sha1('E_folds_v1|' + sentence_id), 16) % 5` (asserted == `fold_E`) |\n| LLM | `google/gemini-2.5-flash` via OpenRouter, temperature 0, `reasoning.max_tokens = 0` (0 reasoning tokens on every call), <= 12 symbol pairs per call |\n\n## Commands\n\n```bash\nuv venv .venv --python=3.12 && uv pip install --python .venv/bin/python -r pyproject.toml\n.venv/bin/python method.py                 # all stages; idempotent (skips steps whose outputs exist)\n.venv/bin/python method.py --stage TEST    # pytest (14 tests) + audit_rederive + smoke_lib\n```\n\nStage order (`method.py` STEPS):\n\n1. **A**: copy_inputs → step0_gates (G0) → prereg_improve → make_row_index → score_variants (label-free, sealed) →\n   fit_v4 → screen → select_rule → freeze_part_a (M1).\n2. **B**: probe → prereg_gg → gg_search → gg_gates dev v1 / confirm v2 → gg_gloss → gg_score → freeze_part_b.\n3. **GGB**: ggb_search → ggb_score.\n4. **C**: vendor_lib.\n5. **OUT**: make_outputs → make_tables.\n6. **TEST**: the three test/check scripts.\n\nThe frozen writers (`prereg_improve.py`, `prereg_gg.py`, `freeze_part_a.py`) refuse to overwrite.\n\n## Runtimes (this run, host under heavy shared load)\n\n| step | wall time |\n|---|---|\n| G0 | 10 s |\n| score_variants | 2 s |\n| screen | 17 s |\n| select_rule (500 + 200 replicates) | 35 s |\n| gg_search (17,913 pairs, 6 workers) | 31 s |\n| each checker gate stage | ~15 s |\n| gloss sweep (415 calls, concurrency 8) | 42 s |\n| gg_score | 11 s |\n| ggb_search (11,202 pairs) | ~9.5 min, then 20 min on the last sentence until the wall deadline (53 pairs recorded CAPPED, D12) |\n| smoke_lib | 27–40 s |\n\n## Spend\n\n`cost_ledger.jsonl`, $0.219 in total:\n\n| phase | calls | $ |\n|---|---|---|\n| probe | 1 | 0.0000046 |\n| gate_dev_v1 | 147 | 0.0266 |\n| gate_confirm_v2 | 128 | 0.0294 |\n| gg_sweep (first 50 + rest) | 415 | 0.1630 |\n\nThe GG_B gloss made 0 billed calls: the run-level budget was exhausted (HTTP 403, D13). All verdicts are cached in\n`results/gloss_cache.jsonl`, so a re-run costs $0.\n\n## Expected numbers (a re-run must reproduce them)\n\n| quantity | expected value |\n|---|---|\n| G0 (V0 strat on R_AB) | 0.741462, Δ vs judge_cheap_disg +0.098975 [0.049345, 0.145991] |\n| G1 mismatches | 24 / 8,469 |\n| c_exact pooled on Z | 0.74768 |\n| 3-pool plain c | 0.784520 |\n| oracle d, 3-pool ALL / L25 | 0.38543 / 0.54217 |\n| LONG-strat AUROC: V0 / V1 / V2 / V3 / V4 / V5 | 0.74259 / 0.73914 / 0.75014 / 0.74999 / 0.75139 / 0.74562 |\n| selection | winner \"NONE: V0 stands\" |\n| GG g3 (ALL-strat): GG vs V0 | 0.69644 vs 0.74217 |\n| GG g1 flip | 0.03409 |\n| GG g2 recall | 1.0 |\n| G-A confirm (v2) | 0.907 |\n| GG_B all-yes ALL-strat | 0.65250 |\n\n`tests/audit_rederive.py` re-derives the decision, the best LONG Δ (to 1e-9) and the GG gate numbers with independent code.\n`tests/smoke_lib.py` recomputes V0/c_exact/V1–V5 from raw candidate strings through `lib/api.py`, to 1e-9.\n\nThe gloss checker is an API model: exact verdicts can drift if the provider changes the model behind the id. The cache\nfreezes the verdicts used here.", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
````

### [12] TOOL CALL — Bash · 2026-09-24 19:17:57 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_14; cat $W/preview_method_out.json | head -c 9000; echo; cat $W/src/common.py $W/src/stats.py
```

### [13] TOOL RESULT — Bash · 2026-09-24 19:17:57 UTC

```
{"stdout": "{\n  \"metadata\": {\n    \"method_name\": \"Iteration-5 FREEZE: label-free consensus rescoring screen (V0-V5) + gloss-gated name-free agreement (GG)\",\n    \"written_utc\": \"2026-09-24T12:13:03Z\",\n    \"orientation\": \"every predict_* is higher = more likely ERROR; 'NA' = not computed\",\n    \"M1\": {\n      \"token\": \"aii_iter5_consensus_freeze_v1\",\n      \"written_utc\": \"2026-09-24T11:20:44Z\",\n      \"V\": {\n        \"status\": \"FROZEN\",\n        \"selection_sha256\": \"ed8c1364b0e223c4ebc01aee6fd803577ce13ea8ca25eb8d853bab35ff491a9a\",\n        \"consensus_variants_sha256\": \"6730a63b2d7612c3d44fd92019bceff8e72a68220c3fa0c65acbbb2a9463f429\",\n        \"winner\": \"NONE: V0 stands\"\n      },\n      \"GG\": {\n        \"status\": \"FAIL(g3)\",\n        \"gg_sha256\": \"80e6d98e990e969c5eb7640e946f52da6e7ecebb8292bfd6003817d8778f3120\",\n        \"gg_gate_sha256\": \"7bf0a2d3ba9bf4cb9cf54187343ff4877be896afe169a76e11c3628e84ffb334\",\n        \"checker_model\": \"google/gemini-2.5-flash\",\n        \"prompt_sha\": \"48394616002323cb0608527746812df0a1953264385fff205e4a1b3b9087c46d\",\n        \"updated_utc\": \"2026-09-24T11:30:54Z\"\n      },\n      \"files\": {\n        \"selection\": \"freeze/selection.json\",\n        \"consensus_variants\": \"freeze/consensus_variants.py\",\n        \"prereg\": \"prereg_improve.json\",\n        \"scores\": \"results/scores_E_variants.jsonl\",\n        \"tests\": \"tests/test_variants.py\",\n        \"gg\": \"freeze/gg.py\",\n        \"gg_gate\": \"freeze/gg_gate.json\",\n        \"gg_dev\": \"results/gg_dev.json\"\n      },\n      \"workspace\": \"/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_14\",\n      \"GG_B_secondary\": {\n        \"status\": \"UNTESTED(budget)\",\n        \"note\": \"SECONDARY row; does not change GG status\",\n        \"allyes_bracket_ALL_strat_auroc\": 0.6525028389855358,\n        \"ggb_dev_sha256\": \"860e4155d73edc838612c8bae8835a8407616abd49d323de58059e4851a9620e\",\n        \"updated_utc\": \"2026-09-24T12:12:51Z\"\n      }\n    },\n    \"part_A_winner\": \"NONE: V0 stands\",\n    \"part_A_qualification\": {\n      \"V1\": {\n        \"i_long_margin\": false,\n        \"ii_L25\": false,\n        \"iii_CTRL\": false,\n        \"qualifies\": false,\n        \"delta_long\": -0.0034534199429128165\n      },\n      \"V2\": {\n        \"i_long_margin\": false,\n        \"ii_L25\": true,\n        \"iii_CTRL\": true,\n        \"qualifies\": false,\n        \"delta_long\": 0.0075499512527457124\n      },\n      \"V3\": {\n        \"i_long_margin\": false,\n        \"ii_L25\": true,\n        \"iii_CTRL\": false,\n        \"qualifies\": false,\n        \"delta_long\": 0.007397249010371976\n      },\n      \"V4\": {\n        \"i_long_margin\": false,\n        \"ii_L25\": true,\n        \"iii_CTRL\": true,\n        \"qualifies\": false,\n        \"delta_long\": 0.00879799842599227\n      },\n      \"V5\": {\n        \"i_long_margin\": false,\n        \"ii_L25\": false,\n        \"iii_CTRL\": false,\n        \"qualifies\": false,\n        \"delta_long\": 0.0030276156132169607\n      }\n    },\n    \"part_A_stability\": {\n      \"B\": 500,\n      \"scheme\": \"sentence-cluster resample within strata\",\n      \"share_selected\": {\n        \"NONE: V0 stands\": 0.876,\n        \"V4\": 0.118,\n        \"V3\": 0.002,\n        \"V5\": 0.004\n      }\n    },\n    \"part_A_null\": {\n      \"B\": 200,\n      \"share_any_variant_qualifies\": 0.035,\n      \"share_per_variant\": {\n        \"V1\": 0.0,\n        \"V2\": 0.0,\n        \"V3\": 0.0,\n        \"V4\": 0.0,\n        \"V5\": 0.035\n      },\n      \"note\": \"within-stratum label permutation of Z; V4 re-cross-fitted on each permuted label vector\"\n    },\n    \"GG_status\": \"FAIL(g3)\",\n    \"GG_gates\": {\n      \"g1\": {\n        \"pass\": true,\n        \"paired_flip\": 0.03409090909090909,\n        \"FA_SYN\": 0.9318181818181818,\n        \"FA_paired_bases\": 0.8977272727272727,\n        \"FA_all_bases\": 0.8282828282828283,\n        \"rule\": \"flip <= 0.05 AND FA <= FA(base) + 0.05\"\n      },\n      \"g2\": {\n        \"pass\": true,\n        \"recall_gg\": 1.0,\n        \"recall_c_align\": 1.0,\n        \"FA_base_gg\": 0.8282828282828283,\n        \"FA_base_c_align\": 0.7121212121212122,\n        \"recall_given_base_endorsed_gg\": 1.0,\n        \"recall_given_base_endorsed_c_align\": 1.0\n      },\n      \"g3\": {\n        \"pass\": false,\n        \"gg\": 0.6964364733668502,\n        \"V0\": 0.7421654662067422,\n        \"delta_ci\": [\n          -0.0708974380922907,\n          -0.021226381894754013\n        ]\n      },\n      \"checker\": {\n        \"pass\": true,\n        \"G-A_confirm_BA\": 0.9074303405572756,\n        \"G-B\": \"NOT_TESTABLE\",\n        \"G-B_confirm_BA_descriptive\": 0.9406862745098039\n      },\n      \"NONCE_expected_failure\": {\n        \"n\": 110,\n        \"FA\": 1.0,\n        \"FA_paired_bases\": 0.7727272727272727,\n        \"paired_flip\": 0.22727272727272727,\n        \"by_base_status\": {\n          \"GOLD_PANEL_OK\": {\n            \"n\": 43,\n            \"FA\": 1.0,\n            \"FA_base\": 0.8837209302325582,\n            \"flip\": 0.11627906976744186\n          },\n          \"PANEL_REPAIRED\": {\n            \"n\": 39,\n            \"FA\": 1.0,\n            \"FA_base\": 0.9230769230769231,\n            \"flip\": 0.07692307692307693\n          },\n          \"TRUSTED_AGREED\": {\n            \"n\": 28,\n            \"FA\": 1.0,\n            \"FA_base\": 0.39285714285714285,\n            \"flip\": 0.6071428571428571\n          }\n        }\n      },\n      \"GG_status\": \"FAIL\"\n    },\n    \"GG_cost\": {\n      \"gloss_sweep_usd_total_E_plus_PERTURB\": 0.16304509999999994,\n      \"n_unique_gloss_pairs\": 3481,\n      \"usd_per_call\": 0.00039287975903614443,\n      \"E_candidates_scored\": 3490,\n      \"E_search_cpu_s_total\": 132.71700000000143,\n      \"PERTURB_search_cpu_s_total\": 48.57000000000003,\n      \"FULL_per_E_candidate\": {\n        \"cpu_s\": 0.038027793696275486,\n        \"usd_upper\": 4.671779369627506e-05,\n        \"note\": \"usd_upper divides the whole sweep (E + PERTURB pairs) by E candidates only\"\n      },\n      \"MARGINAL_per_candidate\": {\n        \"cpu_s\": 0.10593995223028697,\n        \"usd\": 1.0097266666666667e-05,\n        \"note\": \"a new candidate needs ~n_peers searches and one gloss call per 12 new mapped pairs; cached pairs cost 0\"\n      },\n      \"peer_generation_usd_per_sentence\": 0.0022064053623312495\n    },\n    \"spend_usd_total\": 0.2189901,\n    \"E_status\": \"development data; every E number is a development number\"\n  },\n  \"datasets\": [\n    {\n      \"dataset\": \"E_heldout\",\n      \"examples\": [\n        {\n          \"input\": \"{\\\"text\\\": \\\"When something is depressing, it is sad.\\\", \\\"candidate_fol\\\": \\\"\\\", \\\"system\\\": \\\"ccg2lambda\\\", \\\"prompt_variant\\\": \\\"none\\\"}\",\n          \"output\": \"UNPARSEABLE\",\n          \"predict_V0\": \"1\",\n          \"predict_V0_rep\": \"1\",\n          \"predict_V1\": \"1\",\n          \"predict_V2\": \"1\",\n          \"predict_V3\": \"1\",\n          \"predict_V4\": \"0.838446\",\n          \"predict_V5\": \"1\",\n          \"predict_c_exact\": \"1\",\n          \"predict_gg\": \"1\",\n          \"predict_gg_allyes\": \"1\",\n          \"predict_p_peer_text\": \"1\",\n          \"predict_judge_cheap_disg\": \"1\",\n          \"metadata_row_key\": \"31452c4db10ee367|none\",\n          \"metadata_sentence_id\": \"0000c2274e80\",\n          \"metadata_stratum\": \"CTRL\",\n          \"metadata_fold\": 1,\n          \"metadata_in_R_AB\": false,\n          \"metadata_in_Z\": false,\n          \"metadata_y_R_AB\": null,\n          \"metadata_family\": \"symbolic\",\n          \"metadata_words\": 7,\n          \"metadata_n_conditions\": 1,\n          \"metadata_n_peers\": 0,\n          \"metadata_coverage_status\": \"UNPARSEABLE\",\n          \"metadata_label_tier\": \"-\",\n          \"metadata_error_ops\": null,\n          \"metadata_gg_status\": null,\n          \"predict_gg_b_allyes\": \"NA\"\n        },\n        {\n          \"input\": \"{\\\"text\\\": \\\"When something is depressing, it is sad.\\\", \\\"candidate_fol\\\": \\\"∀x (Depressing(x) → Sad(x))\\\", \\\"system\\\": \\\"F:openai/gpt-5.1\\\", \\\"prompt_variant\\\": \\\"fewshot_v1\\\"}\",\n          \"output\": \"CORRECT\",\n          \"predict_V0\": \"0.090909\",\n          \"predict_V0_rep\": \"0.0909091\",\n          \"predict_V1\": \"0\",\n          \"predict_V2\": \"0.0767922\",\n          \"predict_V3\": \"0\",\n          \"predict_V4\": \"0.0594965\",\n          \"predict_V5\": \"0\",\n          \"predict_c_exact\": \"0.0909091\",\n          \"predict_gg\": \"0.0909091\",\n          \"predict_gg_allyes\": \"0.0909091\",\n          \"predict_p_peer_text\": \"0.09035\",\n          \"predict_judge_cheap_disg\": \"0\",\n          \"metadata_row_key\": \"b87a8dda4faced11|fewshot_v1\",\n          \"metadata_sentence_id\": \"0000c2274e80\",\n          \"metadata_stratum\": \"CTRL\",\n          \"metadata_fold\": 1,\n          \"metadata_in_R_AB\": true,\n          \"metadata_in_Z\": true,\n          \"metadata_y_R_AB\": 0,\n          \"metadata_family\": \"openai-frontier\",\n          \"metadata_words\": 7,\n          \"metadata_n_conditions\": 1,\n          \"metadata_n_peers\": 11,\n          \"metadata_coverage_status\": \"OK\",\n          \"metadata_label_tier\": \"A\",\n          \"metadata_error_ops\": null,\n          \"metadata_gg_status\": \"OK\",\n          \"predict_gg_b_allyes\": \"0.0909091\"\n        },\n        {\n          \"input\": \"{\\\"text\\\": \\\"When something is depressing, it is sad.\\\", \\\"candidate_fol\\\": \\\"∀x (Depressing(x) → Sad(x))\\\", \\\"system\\\": \\\"G1b:meta-llama/llama-3.3-7\n\"\"\"Paths (READ-ONLY inputs of run_u75jRHUss0zo), IO helpers and logging setup shared by every script of this artifact.\"\"\"\nfrom __future__ import annotations\n\nimport hashlib\nimport json\nimport os\nimport sys\nimport time\nfrom pathlib import Path\n\nRUN = Path(\"/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop\")\nDS_E = RUN / \"iter_1/gen_art/gen_art_dataset_1\"            # art_U4Hsqt4Ay9Tg (dataset E)\nDS3 = RUN / \"iter_2/gen_art/gen_art_dataset_3\"             # art_zcwCQgTqk6DN (PERTURB / R_COMP)\nE5 = RUN / \"iter_2/gen_art/gen_art_experiment_5\"           # frozen c_score_align code / per_item_E\nE6 = RUN / \"iter_3/gen_art/gen_art_experiment_6\"           # per_item_T1.jsonl (labels + frozen columns)\nEV2 = RUN / \"iter_3/gen_art/gen_art_evaluation_2\"          # pairwise_classes_E.jsonl\nE8 = RUN / \"iter_3/gen_art/gen_art_experiment_8\"           # perturb_scores.jsonl, pairs_E.jsonl, consensus_lib\nE9 = RUN / \"iter_4/gen_art/gen_art_experiment_9\"           # T9 classes\nEV3 = RUN / \"iter_4/gen_art/gen_art_evaluation_3\"          # R_oracle\nDS5 = RUN / \"iter_4/gen_art/gen_art_dataset_5\"             # freelab / gloss gate items\nE1 = RUN / \"iter_1/gen_art/gen_art_experiment_1\"           # fol_triage\n\nROOT = Path(__file__).resolve().parent.parent\nRES = ROOT / \"results\"\nTAB = ROOT / \"tables\"\nFREEZE = ROOT / \"freeze\"\nLOGS = ROOT / \"logs\"\nfor _d in (RES, TAB, FREEZE, LOGS):\n    _d.mkdir(exist_ok=True)\n\nMATRIX = EV2 / \"pairwise_classes_E.jsonl\"\nPER_ITEM = E6 / \"results\" / \"per_item_T1.jsonl\"\nPERTURB_SCORES = E8 / \"results\" / \"perturb_scores.jsonl\"\nSTRATA = (\"L25\", \"L20\", \"EXC\", \"CTRL\")\nLONG = (\"L25\", \"L20\", \"EXC\")\nNEUTRAL_C = 0.6266243516243516  # exp-5 prereg imputation.neutral.c_score_align (|P| < 2 rows)\nSEED = 20260924\nB = 2000\n\n\ndef jl(p) -> list[dict]:\n    p = Path(p)\n    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []\n\n\ndef jdump(obj, p) -> None:\n    Path(p).write_text(json.dumps(obj, indent=1, ensure_ascii=False, default=_default))\n\n\ndef _default(o):\n    import numpy as np\n    if isinstance(o, (np.integer,)):\n        return int(o)\n    if isinstance(o, (np.floating,)):\n        return None if np.isnan(o) else float(o)\n    if isinstance(o, np.ndarray):\n        return o.tolist()\n    if isinstance(o, (set, tuple)):\n        return list(o)\n    raise TypeError(type(o))\n\n\ndef sha256_file(p) -> str:\n    return hashlib.sha256(Path(p).read_bytes()).hexdigest()\n\n\ndef sha1(s: str) -> str:\n    return hashlib.sha1(s.encode()).hexdigest()\n\n\ndef utc() -> str:\n    return time.strftime(\"%Y-%m-%dT%H:%M:%SZ\", time.gmtime())\n\n\ndef setup_logger(name: str):\n    from loguru import logger\n    logger.remove()\n    logger.add(sys.stdout, level=\"INFO\", format=\"{time:HH:mm:ss}|{level:<7}|{message}\")\n    logger.add(LOGS / f\"{name}.log\", rotation=\"30 MB\", level=\"DEBUG\")\n    return logger\n\n\ndef atomic_write(p, text: str) -> None:\n    p = Path(p)\n    tmp = p.with_suffix(p.suffix + \".tmp\")\n    tmp.write_text(text)\n    os.replace(tmp, p)\n\"\"\"Statistics. Part 1 is COPIED UNCHANGED from exp 6 (iter_3 gen_art_experiment_6/src/api_bar.py: auroc, strat_auroc,\nClusterBoot, boot_ci, paired_boot) and is what gate G0 uses. Part 2 is eval-2's multiplicity-weight form of the same\nsentence-cluster bootstrap (iter_3 gen_art_evaluation_2/src/stats.py: WAuc, WStratAuc, SentBoot), used for speed in the\nscreen; with the same seed both draw IDENTICAL sentence resamples (rng.integers(0, S, S) per replicate over sorted ids).\"\"\"\nfrom __future__ import annotations\n\nimport math\nfrom collections import defaultdict\nfrom typing import Sequence\n\nimport numpy as np\nfrom scipy.stats import rankdata\n\n\n# ============================================================ Part 1: exp 6 api_bar.py (verbatim)\ndef auroc(y, s) -> float:\n    \"\"\"Mann-Whitney AUROC, ties counted 1/2 (== sklearn roc_auc_score). nan if one class is empty.\"\"\"\n    y = np.asarray(y)\n    s = np.asarray(s, float)\n    n1 = int(y.sum())\n    n0 = len(y) - n1\n    if n1 == 0 or n0 == 0:\n        return float(\"nan\")\n    r = rankdata(s)\n    return float((r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))\n\n\ndef strat_auroc(y, s, stratum) -> float:\n    \"\"\"Within-stratum AUROC: sum_h AUC_h * P_h * N_h / sum_h P_h * N_h (only (ERROR, CORRECT) pairs from the same\n    source stratum count), identical to exp 5's strat_auc. Removes the stratum-composition part of pooled AUROC.\"\"\"\n    y = np.asarray(y)\n    s = np.asarray(s, float)\n    stratum = np.asarray(stratum)\n    num = den = 0.0\n    for h in np.unique(stratum):\n        m = stratum == h\n        n1 = int(y[m].sum())\n        n0 = int(m.sum()) - n1\n        if n1 and n0:\n            num += auroc(y[m], s[m]) * n1 * n0\n            den += n1 * n0\n    return num / den if den else float(\"nan\")\n\n\nclass ClusterBoot:\n    \"\"\"Sentence-clustered bootstrap index sets: resample sentence ids with replacement (fixed seed); every metric on a\n    row set uses the IDENTICAL resamples, which makes deltas paired.\"\"\"\n\n    def __init__(self, clusters: Sequence[str], b: int = 2000, seed: int = 0):\n        by = defaultdict(list)\n        for i, c in enumerate(clusters):\n            by[c].append(i)\n        keys = sorted(by)\n        arr = [np.array(by[k]) for k in keys]\n        rng = np.random.default_rng(seed)\n        self.idx = []\n        for _ in range(b):\n            pick = rng.integers(0, len(keys), len(keys))\n            self.idx.append(np.concatenate([arr[j] for j in pick]))\n        self.n_clusters = len(keys)\n\n\ndef boot_ci(vals, lo: float = 2.5, hi: float = 97.5) -> list:\n    v = np.asarray([x for x in vals if x is not None and not (isinstance(x, float) and math.isnan(x))], float)\n    if len(v) == 0:\n        return [None, None]\n    return [float(np.percentile(v, lo)), float(np.percentile(v, hi))]\n\n\ndef paired_boot(y, a, c, cb: ClusterBoot, stat: str = \"pooled\", stratum=None) -> dict:\n    \"\"\"Paired delta stat(a) - stat(c) on identical rows; percentile CI over cluster resamples; one-sided\n    p = share of resampled deltas <= 0. stat in {'pooled', 'strat'} (strat needs `stratum`).\"\"\"\n    y = np.asarray(y)\n    a = np.asarray(a, float)\n    c = np.asarray(c, float)\n    st = None if stratum is None else np.asarray(stratum)\n    f = (lambda yy, ss, hh: auroc(yy, ss)) if stat == \"pooled\" else strat_auroc\n    pa, pc = f(y, a, st), f(y, c, st)\n    da, dc, dd = [], [], []\n    for ix in cb.idx:\n        hh = None if st is None else st[ix]\n        xa, xc = f(y[ix], a[ix], hh), f(y[ix], c[ix], hh)\n        da.append(xa)\n        dc.append(xc)\n        dd.append(xa - xc)\n    dd_ = np.array([d for d in dd if not math.isnan(d)])\n    return {\"a\": pa, \"b\": pc, \"a_ci\": boot_ci(da), \"b_ci\": boot_ci(dc), \"delta\": pa - pc, \"ci\": boot_ci(dd),\n            \"p_one_sided_le0\": float(np.mean(dd_ <= 0)) if len(dd_) else None, \"se\": float(np.std(dd_)) if len(dd_) else None,\n            \"n\": int(len(y)), \"n_error\": int(y.sum()), \"n_correct\": int(len(y) - y.sum()), \"stat\": stat}\n\n\n# ============================================================ Part 2: eval-2 stats.py weighted forms (verbatim)\nclass WAuc:\n    \"\"\"AUROC under row weights (bootstrap multiplicities); ties = 0.5. Precomputes the score ranking once.\"\"\"\n\n    def __init__(self, y, s):\n        self.y = np.asarray(y, float)\n        vals, self.inv = np.unique(np.asarray(s, float), return_inverse=True)\n        self.nv = len(vals)\n\n    def __call__(self, w) -> float:\n        w = np.asarray(w, float)\n        W1 = np.bincount(self.inv, weights=w * self.y, minlength=self.nv)\n        W0 = np.bincount(self.inv, weights=w * (1 - self.y), minlength=self.nv)\n        den = W1.sum() * W0.sum()\n        if den <= 0:\n            return float(\"nan\")\n        cum0 = np.cumsum(W0) - W0\n        return float((W1 * (cum0 + 0.5 * W0)).sum() / den)\n\n\nclass WStratAuc:\n    \"\"\"Within-stratum pair AUROC under row weights.\"\"\"\n\n    def __init__(self, y, s, strata):\n        self.y = np.asarray(y, float)\n        strata = np.asarray(strata)\n        self.parts = [(np.where(strata == st)[0], WAuc(self.y[strata == st], np.asarray(s, float)[strata == st]))\n                      for st in np.unique(strata)]\n\n    def __call__(self, w) -> float:\n        w = np.asarray(w, float)\n        num = den = 0.0\n        for ix, wa in self.parts:\n            ww = w[ix]\n            n1 = (ww * self.y[ix]).sum()\n            n0 = (ww * (1 - self.y[ix])).sum()\n            if n1 > 0 and n0 > 0:\n                num += wa(ww) * n1 * n0\n                den += n1 * n0\n        return num / den if den else float(\"nan\")\n\n\nclass SentBoot:\n    \"\"\"Sentence-cluster bootstrap as multiplicity weights: W[b, i] = #times row i's sentence was drawn in replicate b.\"\"\"\n\n    def __init__(self, sids, b: int = 2000, seed: int = 0):\n        sids = np.asarray(sids)\n        self.keys, self.sent_ix = np.unique(sids, return_inverse=True)\n        S = len(self.keys)\n        rng = np.random.default_rng(seed)\n        self.C = np.stack([np.bincount(rng.integers(0, S, S), minlength=S) for _ in range(b)]).astype(float)\n        self.B = b\n\n    def W(self, mask=None):\n        W = self.C[:, self.sent_ix]\n        return W if mask is None else W[:, mask]\n\n\n# ============================================================ vectorised helpers (this artifact)\ndef boot_series(y, s, strata, W, stat: str = \"strat\") -> np.ndarray:\n    \"\"\"Replicate values of (strat|pooled) AUROC under a (B, n) weight matrix.\"\"\"\n    f = WStratAuc(y, s, strata) if stat == \"strat\" else WAuc(y, s)\n    return np.array([f(w) for w in W])\n\n\ndef point(y, s, strata, stat: str = \"strat\") -> float:\n    return strat_auroc(y, s, strata) if stat == \"strat\" else auroc(y, s)\n\n\ndef rate_ci(num_mask, den_mask, W) -> list:\n    \"\"\"CI of a ratio sum(w*num)/sum(w*den) over replicates.\"\"\"\n    with np.errstate(invalid=\"ignore\", divide=\"ignore\"):\n        v = (W @ num_mask.astype(float)) / (W @ den_mask.astype(float))\n    return boot_ci(v)", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [14] TOOL CALL — Bash · 2026-09-24 19:18:03 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_14; cat $W/src/screen.py $W/src/select_rule.py
```

### [15] TOOL RESULT — Bash · 2026-09-24 19:18:03 UTC

```
{"stdout": "#!/usr/bin/env python3\n\"\"\"A4/A5 (post-seal label join): AUROC + sentence-cluster CIs per variant and cell, paired Δ vs V0 (frozen), context Δ vs the\ncheap API judges, binary e/d (c > 0.5; V4 flag-rate matched to V0) overall / per words tercile / LONG / L25 / CTRL / per T9\nclass, the key diagnostic (Δd, Δe on T3 and L25), NET Δ(e+d) T3 - T1, post-seal reproduction checks, and the eval-3\nR_oracle bound with the oracle-gap share. Writes results/screen_E.json and tables/*.csv.\"\"\"\nfrom __future__ import annotations\n\nimport json\nimport sys\nimport time\n\nimport numpy as np\nimport pandas as pd\n\nfrom common import FREEZE, LONG, RES, ROOT, SEED, TAB, B, jdump, setup_logger\nfrom labels import T9, frame\nfrom stats import SentBoot, WAuc, WStratAuc, auroc, boot_ci, strat_auroc\n\nlogger = setup_logger(\"screen\")\nVARIANTS = [\"V1\", \"V2\", \"V3\", \"V4\", \"V5\"]\nSCORES = [\"V0_frozen\", \"V0_rep\", \"c_exact\"] + VARIANTS\nJUDGES = [\"judge_cheap_disg\", \"judge_cheap_orig\", \"judge_cheap2_orig\"]\nCELLS = {\"ALL-strat\": (None, \"strat\"), \"pooled\": (None, \"pooled\"), \"LONG-strat\": (LONG, \"strat\"),\n         \"L25\": ((\"L25\",), \"pooled\"), \"L20\": ((\"L20\",), \"pooled\"), \"EXC\": ((\"EXC\",), \"pooled\"), \"CTRL\": ((\"CTRL\",), \"pooled\")}\n\n\ndef flags(df: pd.DataFrame, P: pd.DataFrame) -> dict:\n    \"\"\"Binary flag per score: c > 0.5; V4 at the threshold matching V0's flag rate on Z (ties broken by row order).\"\"\"\n    out = {s: (P[s].astype(float).values > 0.5) for s in SCORES if s != \"V4\"}\n    rate = out[\"V0_frozen\"].mean()\n    v = P[\"V4\"].astype(float).values\n    thr = float(np.quantile(v, 1 - rate, method=\"higher\"))\n    f4 = v > thr\n    if abs(f4.mean() - rate) > 0.01:  # step ties: take the top-k by score (stable by row order)\n        k = int(round(rate * len(v)))\n        o = np.argsort(-v, kind=\"stable\")\n        f4 = np.zeros(len(v), bool)\n        f4[o[:k]] = True\n    out[\"V4\"] = f4\n    out[\"_V4_threshold\"] = thr\n    out[\"_V0_flag_rate\"] = float(rate)\n    return out\n\n\ndef auc_block(y, s, st, W, stat):\n    pt = strat_auroc(y, s, st) if stat == \"strat\" else auroc(y, s)\n    f = WStratAuc(y, s, st) if stat == \"strat\" else WAuc(y, s)\n    bs = np.array([f(w) for w in W])\n    return pt, bs\n\n\ndef ed_block(y, fl, W) -> dict:\n    y = np.asarray(y, int)\n    endorsed = ~fl\n    e = float(endorsed[y == 1].mean()) if (y == 1).any() else None\n    d = float(fl[y == 0].mean()) if (y == 0).any() else None\n    with np.errstate(invalid=\"ignore\", divide=\"ignore\"):\n        eb = (W @ (endorsed & (y == 1)).astype(float)) / (W @ (y == 1).astype(float))\n        db = (W @ (fl & (y == 0)).astype(float)) / (W @ (y == 0).astype(float))\n    return {\"e\": e, \"d\": d, \"e_ci\": boot_ci(eb), \"d_ci\": boot_ci(db), \"n_err\": int((y == 1).sum()), \"n_cor\": int((y == 0).sum()),\n            \"auroc_b\": (1 - (e + d) / 2) if e is not None and d is not None else None, \"_eb\": eb, \"_db\": db}\n\n\n@logger.catch(reraise=True)\ndef main():\n    t0 = time.time()\n    df = frame()\n    P = df[df.Z].reset_index(drop=True)\n    P[\"V0_frozen\"] = P.V0_frozen.astype(float)\n    y = P.y.values.astype(int)\n    st = P.stratum.values\n    boot = SentBoot(P.sentence_id.values, b=B, seed=SEED)\n    Wf = boot.W()\n    A = {\"population\": {\"Z\": {\"n\": len(P), \"n_error\": int(y.sum()), \"n_correct\": int((1 - y).sum()), \"n_sentences\": int(P.sentence_id.nunique())},\n                        \"R_AB\": {\"n\": int(df.R_AB.sum()), \"n_error\": int(df[df.R_AB].y.sum()), \"n_sentences\": int(df[df.R_AB].sentence_id.nunique())},\n                        \"R_AB_not_in_Z\": df[df.R_AB & ~df.Z][[\"row_key\", \"stratum\", \"n_peers\", \"coverage_status\"]].to_dict(\"records\")},\n         \"B\": B, \"seed\": SEED}\n    assert len(P) == 2672, len(P)\n    # ---------------- post-seal reproduction checks\n    A[\"repro\"] = {\"c_exact_pooled_auroc_Z\": auroc(y, P.c_exact.values), \"target_c_exact\": 0.748,\n                  \"c3_plain_pooled_auroc_Z\": auroc(y, P.c3_plain.values), \"target_c3_eval2_c_k3_best_oof\": 0.784520131776288,\n                  \"V0_frozen_pooled_Z\": auroc(y, P.V0_frozen.values), \"V0_rep_pooled_Z\": auroc(y, P.V0_rep.values),\n                  \"V0_frozen_strat_full_RAB_2686\": strat_auroc(df[df.R_AB].y.values.astype(int), df[df.R_AB].V0_frozen.astype(float).values, df[df.R_AB].stratum.values),\n                  \"n_V5_imputed_neutral_in_Z\": int(P.V5_imputed.fillna(False).sum())}\n    A[\"repro\"][\"c_exact_pass\"] = abs(A[\"repro\"][\"c_exact_pooled_auroc_Z\"] - 0.748) < 0.0015\n    A[\"repro\"][\"c3_pass\"] = abs(A[\"repro\"][\"c3_plain_pooled_auroc_Z\"] - 0.784520131776288) < 0.0015\n    logger.info(f\"repro {json.dumps(A['repro'])}\")\n    # ---------------- AUROC per cell\n    A[\"auroc\"], A[\"delta_vs_V0\"], A[\"delta_vs_judges\"] = {}, {}, {}\n    rows_auc, rows_d = [], []\n    for cname, (strata, stat) in CELLS.items():\n        m = np.ones(len(P), bool) if strata is None else np.isin(st, strata)\n        W = Wf[:, m]\n        ser = {}\n        for s in SCORES + JUDGES:\n            v = P[s].astype(float).values[m]\n            if np.isnan(v).any():\n                logger.warning(f\"{s} has {np.isnan(v).sum()} NaN in {cname}\")\n                continue\n            ser[s] = auc_block(y[m], v, st[m], W, stat)\n        A[\"auroc\"][cname] = {s: {\"auroc\": pt, \"ci\": boot_ci(bs), \"n\": int(m.sum()), \"n_err\": int(y[m].sum()), \"n_cor\": int((1 - y[m]).sum()),\n                                 \"n_sent\": int(P.sentence_id[m].nunique())} for s, (pt, bs) in ser.items()}\n        A[\"delta_vs_V0\"][cname] = {}\n        for s in [\"V0_rep\", \"c_exact\"] + VARIANTS:\n            d = ser[s][1] - ser[\"V0_frozen\"][1]\n            A[\"delta_vs_V0\"][cname][s] = {\"delta\": ser[s][0] - ser[\"V0_frozen\"][0], \"ci\": boot_ci(d), \"se\": float(np.nanstd(d)),\n                                          \"p_one_sided_le0\": float(np.nanmean(d <= 0))}\n            rows_d.append({\"cell\": cname, \"variant\": s, **A[\"delta_vs_V0\"][cname][s]})\n        A[\"delta_vs_judges\"][cname] = {}\n        for s in [\"V0_frozen\"] + VARIANTS:\n            for j in JUDGES:\n                d = ser[s][1] - ser[j][1]\n                A[\"delta_vs_judges\"][cname][f\"{s} - {j}\"] = {\"delta\": ser[s][0] - ser[j][0], \"ci\": boot_ci(d)}\n        for s, (pt, bs) in ser.items():\n            rows_auc.append({\"cell\": cname, \"stat\": stat, \"score\": s, \"auroc\": pt, \"ci_lo\": boot_ci(bs)[0], \"ci_hi\": boot_ci(bs)[1], \"n\": int(m.sum())})\n        logger.info(f\"{cname}: \" + \" \".join(f\"{s}={ser[s][0]:.4f}\" for s in SCORES))\n    # ---------------- e/d\n    FL = flags(df, P)\n    A[\"binary\"] = {\"V4_threshold_flag_rate_matched\": FL[\"_V4_threshold\"], \"V0_flag_rate\": FL[\"_V0_flag_rate\"],\n                   \"flag_rates\": {s: float(FL[s].mean()) for s in SCORES}}\n    cuts = {\"ALL\": np.ones(len(P), bool), \"LONG\": P.long.values, \"L25\": st == \"L25\", \"L20\": st == \"L20\", \"EXC\": st == \"EXC\", \"CTRL\": st == \"CTRL\",\n            \"words_T1\": P.words_t.values == \"T1\", \"words_T2\": P.words_t.values == \"T2\", \"words_T3\": P.words_t.values == \"T3\"}\n    ED, rows_ed = {}, []\n    for c, m in cuts.items():\n        ED[c] = {}\n        for s in SCORES:\n            r = ed_block(y[m], FL[s][m], Wf[:, m])\n            ED[c][s] = r\n            rows_ed.append({\"cut\": c, \"score\": s, **{k: v for k, v in r.items() if not k.startswith(\"_\")}})\n    # key diagnostic: Δd, Δe vs V0 on T3 and L25 (+ LONG, ALL)\n    A[\"key_diagnostic\"] = {}\n    for c in (\"words_T3\", \"L25\", \"LONG\", \"ALL\", \"CTRL\"):\n        A[\"key_diagnostic\"][c] = {}\n        for s in [\"c_exact\"] + VARIANTS:\n            a, b = ED[c][s], ED[c][\"V0_frozen\"]\n            A[\"key_diagnostic\"][c][s] = {\"d\": a[\"d\"], \"e\": a[\"e\"], \"d_V0\": b[\"d\"], \"e_V0\": b[\"e\"],\n                                         \"delta_d\": a[\"d\"] - b[\"d\"], \"delta_d_ci\": boot_ci(a[\"_db\"] - b[\"_db\"]),\n                                         \"delta_e\": a[\"e\"] - b[\"e\"], \"delta_e_ci\": boot_ci(a[\"_eb\"] - b[\"_eb\"]),\n                                         \"d_falls_without_e_rising\": bool(boot_ci(a[\"_db\"] - b[\"_db\"])[1] < 0 and boot_ci(a[\"_eb\"] - b[\"_eb\"])[0] <= 0)}\n    # NET Δ(e+d) T3 - T1 (eval-2 definition)\n    A[\"NET_T3_minus_T1\"] = {}\n    for s in SCORES:\n        t3, t1 = ED[\"words_T3\"][s], ED[\"words_T1\"][s]\n        net = (t3[\"e\"] + t3[\"d\"]) - (t1[\"e\"] + t1[\"d\"])\n        nb = (t3[\"_eb\"] + t3[\"_db\"]) - (t1[\"_eb\"] + t1[\"_db\"])\n        A[\"NET_T3_minus_T1\"][s] = {\"net\": net, \"ci\": boot_ci(nb), \"delta_e\": t3[\"e\"] - t1[\"e\"], \"delta_d\": t3[\"d\"] - t1[\"d\"]}\n    # per T9 class e (ERROR rows of the class) and d reference\n    A[\"t9_e\"] = {}\n    rows_t9 = []\n    for cl in T9:\n        m = np.array([cl in x for x in P.t9])\n        A[\"t9_e\"][cl] = {\"n\": int(m.sum())}\n        for s in SCORES:\n            if m.sum() == 0:\n                continue\n            en = ~FL[s][m]\n            eb = (Wf[:, m] @ en.astype(float)) / Wf[:, m].sum(1)\n            A[\"t9_e\"][cl][s] = {\"e\": float(en.mean()), \"e_ci\": boot_ci(eb)}\n            rows_t9.append({\"class\": cl, \"score\": s, \"n\": int(m.sum()), \"e\": float(en.mean()), \"e_ci_lo\": boot_ci(eb)[0], \"e_ci_hi\": boot_ci(eb)[1]})\n    A[\"ed\"] = {c: {s: {k: v for k, v in r.items() if not k.startswith(\"_\")} for s, r in d.items()} for c, d in ED.items()}\n    # ---------------- oracle bound (A5)\n    A[\"oracle\"] = oracle(df, P, FL, Wf)\n    A[\"runtime_s\"] = time.time() - t0\n    jdump(A, RES / \"screen_E.json\")\n    for name, rows in ((\"screen_auroc\", rows_auc), (\"screen_delta_vs_V0\", rows_d), (\"screen_ed\", rows_ed), (\"screen_t9_e\", rows_t9)):\n        _csv(pd.DataFrame(rows), TAB / f\"{name}.csv\", f\"results/screen_E.json :: src/screen.py main() [{name}]\")\n    logger.info(f\"screen done {time.time() - t0:.0f}s\")\n\n\ndef oracle(df: pd.DataFrame, P: pd.DataFrame, FL: dict, Wf) -> dict:\n    \"\"\"eval-3 t8_part1.py endorse_det R_oracle, reimplemented on the matrix: for candidate x and each LOFO peer row p,\n    agree = (y_p == 0) if x CORRECT else (y_p == 1 and op_class(p) == op_class(x)); unlabelled peers never agree;\n    endorsed iff #agree > n/2. d_oracle = share of CORRECT candidates not endorsed. 9-family = full LOFO pool; 3-pool =\n    {deepseek, microsoft, openai} minus own family (rows with >= 1 pool peer).\"\"\"\n    sys.path.insert(0, str(FREEZE))\n    import consensus_variants as CV\n    from common import MATRIX, jl\n    IX = {r[\"sentence_id\"]: CV.build_index(r) for r in jl(MATRIX)}\n    lab = {rk: (int(y) if r else None) for rk, y, r in zip(df.row_key, df.y, df.R_AB)}\n    opc = dict(zip(df.row_key, df.opc))\n    res = {}\n    y = P.y.values.astype(int)\n    for pool, fams in ((\"9fam\", None), (\"3pool\", CV.POOL3)):\n        endorsed = np.full(len(P), np.nan)\n        for i, (rk, sid) in enumerate(zip(P.row_key, P.sentence_id)):\n            ix = IX[sid]\n            peers = CV.peers_lofo(ix, rk, families=fams)\n            if not peers:\n                continue\n            k = 0\n            for p in peers:\n                yp = lab.get(p)\n                if y[i] == 0:\n                    k += yp == 0\n                else:\n                    k += (yp == 1) and opc.get(p) == opc.get(rk)\n            endorsed[i] = float(k > len(peers) / 2)\n        ok = ~np.isnan(endorsed)\n        out = {}\n        for c, m in ((\"ALL\", ok), (\"L25\", ok & (P.stratum.values == \"L25\")), (\"LONG\", ok & P.long.values), (\"words_T3\", ok & (P.words_t.values == \"T3\"))):\n            cor = m & (y == 0)\n            d_or = float((endorsed[cor] == 0).mean())\n            rec = {\"n_cor\": int(cor.sum()), \"d_oracle\": d_or}\n            # END_MAJ on the same pool (plain c): rows' c on this pool > 0.5 == not endorsed\n            col = \"V0_rep\" if pool == \"9fam\" else \"c3_plain\"\n            rec[f\"d_END_MAJ_{pool}\"] = float((P[col].values[cor] >= 0.5).mean())\n            rows = {}\n            for s in ([\"V0_frozen\", \"V1\", \"V2\", \"V3\", \"V4\"] if pool == \"9fam\" else [\"V5\"]):\n                d_v = float(FL[s][cor].mean())\n                e_v = float((~FL[s][m & (y == 1)]).mean())\n                d_ref = float(FL[\"V0_frozen\"][cor].mean())\n                den = d_ref - d_or\n                rows[s] = {\"d_v\": d_v, \"e_v\": e_v, \"d_V0\": d_ref, \"denominator\": den,\n                           \"gap_closed\": ((d_ref - d_v) / den) if den >= 0.05 else \"ILL_CONDITIONED\"}\n            rec[\"variants\"] = rows\n            out[c] = rec\n        res[pool] = out\n    res[\"targets_eval3\"] = {\"3pool_ALL_d_oracle\": 0.38542890716803757, \"3pool_L25_d_oracle\": 0.5421686746987953,\n                            \"3pool_L25_END_MAJ\": 0.7349397590361446, \"9fam_ALL_d_oracle\": 0.58584686774942}\n    res[\"repro_pass\"] = bool(abs(res[\"3pool\"][\"ALL\"][\"d_oracle\"] - 0.38542890716803757) < 0.002\n                             and abs(res[\"3pool\"][\"L25\"][\"d_oracle\"] - 0.5421686746987953) < 0.002)\n    logger.info(f\"oracle 3pool ALL {res['3pool']['ALL']['d_oracle']:.4f} L25 {res['3pool']['L25']['d_oracle']:.4f} \"\n                f\"END_MAJ L25 {res['3pool']['L25']['d_END_MAJ_3pool']:.4f}; 9fam ALL {res['9fam']['ALL']['d_oracle']:.4f}\")\n    return res\n\n\ndef _csv(d: pd.DataFrame, p, source: str):\n    with open(p, \"w\") as fh:\n        fh.write(f\"# source: {source}\\n\")\n        d.to_csv(fh, index=False)\n\n\nif __name__ == \"__main__\":\n    main()\n#!/usr/bin/env python3\n\"\"\"A6: apply the pre-registered selection rule mechanically to results/screen_E.json, then the reported-not-gating checks:\n(a) selection stability (B=500 sentence-cluster resamples drawn within strata), (b) permutation null (B=200 within-stratum\nlabel permutations; V4 is re-cross-fitted on each permuted label vector). Writes results/selection_E.json.\"\"\"\nfrom __future__ import annotations\n\nimport json\n\nimport numpy as np\nfrom sklearn.linear_model import LogisticRegression\n\nfrom common import RES, SEED, jdump, setup_logger\nfrom labels import frame\nfrom stats import WAuc, WStratAuc, auroc, strat_auroc\n\nlogger = setup_logger(\"select\")\nVARIANTS = [\"V1\", \"V2\", \"V3\", \"V4\", \"V5\"]\nCOST_RANK = {\"V5\": 0, \"V1\": 1, \"V2\": 1, \"V3\": 1, \"V4\": 1}\nMARGIN, L25_TOL, CTRL_TOL, TIE = 0.015, 0.0, 0.01, 1e-4\nRULE_TEXT = (\"winner = variant with highest E LONG-strat AUROC (Z) that (i) beats V0 by >= +0.015 there AND (ii) >= V0 on L25 \"\n             \"(point) AND (iii) >= V0 - 0.01 on CTRL; none -> 'NONE: V0 stands'; tie (|Δ| < 1e-4) -> cheaper (V5 < others)\")\n\n\ndef rule(stats: dict) -> tuple[str, dict]:\n    \"\"\"stats[v] = {'LONG', 'L25', 'CTRL'} for v in V0 + VARIANTS -> (winner, per-variant qualification).\"\"\"\n    q = {}\n    for v in VARIANTS:\n        c1 = stats[v][\"LONG\"] - stats[\"V0\"][\"LONG\"] >= MARGIN\n        c2 = stats[v][\"L25\"] >= stats[\"V0\"][\"L25\"] - L25_TOL\n        c3 = stats[v][\"CTRL\"] >= stats[\"V0\"][\"CTRL\"] - CTRL_TOL\n        q[v] = {\"i_long_margin\": bool(c1), \"ii_L25\": bool(c2), \"iii_CTRL\": bool(c3), \"qualifies\": bool(c1 and c2 and c3),\n                \"delta_long\": stats[v][\"LONG\"] - stats[\"V0\"][\"LONG\"]}\n    ok = [v for v in VARIANTS if q[v][\"qualifies\"]]\n    if not ok:\n        return \"NONE: V0 stands\", q\n    best = max(stats[v][\"LONG\"] for v in ok)\n    tied = [v for v in ok if best - stats[v][\"LONG\"] < TIE]\n    return sorted(tied, key=lambda v: (COST_RANK[v], v))[0], q\n\n\ndef cell_stats(y, S, st, w=None) -> dict:\n    \"\"\"LONG-strat, L25 pooled, CTRL pooled AUROC for each score column in S (dict name -> array); w = row weights.\"\"\"\n    out = {}\n    L = np.isin(st, [\"L25\", \"L20\", \"EXC\"])\n    for name, s in S.items():\n        if w is None:\n            out[name] = {\"LONG\": strat_auroc(y[L], s[L], st[L]), \"L25\": auroc(y[st == \"L25\"], s[st == \"L25\"]),\n                         \"CTRL\": auroc(y[st == \"CTRL\"], s[st == \"CTRL\"])}\n        else:\n            out[name] = {\"LONG\": WStratAuc(y[L], s[L], st[L])(w[L]), \"L25\": WAuc(y[st == \"L25\"], s[st == \"L25\"])(w[st == \"L25\"]),\n                         \"CTRL\": WAuc(y[st == \"CTRL\"], s[st == \"CTRL\"])(w[st == \"CTRL\"])}\n    return out\n\n\ndef v4_oof(X, y, fold):\n    p = np.zeros(len(y))\n    for k in range(5):\n        tr, te = fold != k, fold == k\n        m = LogisticRegression(C=1e6, max_iter=2000).fit(X[tr], y[tr])\n        p[te] = m.predict_proba(X[te])[:, 1]\n    return p\n\n\n@logger.catch(reraise=True)\ndef main():\n    A = json.loads((RES / \"screen_E.json\").read_text())\n    obs = {v: {\"LONG\": A[\"auroc\"][\"LONG-strat\"][v][\"auroc\"], \"L25\": A[\"auroc\"][\"L25\"][v][\"auroc\"], \"CTRL\": A[\"auroc\"][\"CTRL\"][v][\"auroc\"]}\n           for v in VARIANTS}\n    obs[\"V0\"] = {\"LONG\": A[\"auroc\"][\"LONG-strat\"][\"V0_frozen\"][\"auroc\"], \"L25\": A[\"auroc\"][\"L25\"][\"V0_frozen\"][\"auroc\"],\n                 \"CTRL\": A[\"auroc\"][\"CTRL\"][\"V0_frozen\"][\"auroc\"]}\n    winner, q = rule(obs)\n    logger.info(f\"DECISION: {winner}; \" + json.dumps({v: round(q[v]['delta_long'], 4) for v in VARIANTS}))\n    # ---------------- (a) stability: within-stratum sentence resamples\n    df = frame()\n    P = df[df.Z].reset_index(drop=True)\n    y = P.y.values.astype(int)\n    st = P.stratum.values\n    S = {v: P[v].astype(float).values for v in VARIANTS}\n    S[\"V0\"] = P.V0_frozen.astype(float).values\n    rng = np.random.default_rng(SEED + 1)\n    sids = P.sentence_id.values\n    by_stratum = {h: np.unique(sids[st == h]) for h in np.unique(st)}\n    sent_ix = {s: i for i, s in enumerate(np.unique(sids))}\n    row_sent = np.array([sent_ix[s] for s in sids])\n    picks = []\n    for b in range(500):\n        cnt = np.zeros(len(sent_ix))\n        for h, ss in by_stratum.items():\n            draw = rng.integers(0, len(ss), len(ss))\n            np.add.at(cnt, [sent_ix[x] for x in ss[draw]], 1)\n        w = cnt[row_sent]\n        wb, _ = rule(cell_stats(y, S, st, w))\n        picks.append(wb)\n    from collections import Counter\n    stab = {k: v / 500 for k, v in Counter(picks).items()}\n    logger.info(f\"stability {stab}\")\n    # ---------------- (b) permutation null\n    rng2 = np.random.default_rng(SEED + 2)\n    X4 = np.column_stack([P.c_exact.astype(float).values, P.V0_frozen.astype(float).values])\n    fold = P.fold.values\n    any_q = 0\n    per_v = Counter()\n    for b in range(200):\n        yp = y.copy()\n        for h in np.unique(st):\n            m = np.where(st == h)[0]\n            yp[m] = rng2.permutation(y[m])\n        Sb = dict(S)\n        Sb[\"V4\"] = v4_oof(X4, yp, fold)\n        wb, qb = rule(cell_stats(yp, Sb, st))\n        if wb != \"NONE: V0 stands\":\n            any_q += 1\n        for v in VARIANTS:\n            per_v[v] += qb[v][\"qualifies\"]\n    null = {\"B\": 200, \"share_any_variant_qualifies\": any_q / 200, \"share_per_variant\": {v: per_v[v] / 200 for v in VARIANTS},\n            \"note\": \"within-stratum label permutation of Z; V4 re-cross-fitted on each permuted label vector\"}\n    logger.info(f\"null {null}\")\n    out = {\"winner\": winner, \"rule_text\": RULE_TEXT, \"observed\": obs, \"qualification\": q, \"n_screened\": 5,\n           \"margin\": MARGIN, \"stability\": {\"B\": 500, \"scheme\": \"sentence-cluster resample within strata\", \"share_selected\": stab},\n           \"permutation_null\": null}\n    jdump(out, RES / \"selection_E.json\")\n\n\nif __name__ == \"__main__\":\n    main()", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [16] THINKING · 2026-09-24 19:18:13 UTC

```
I've reviewed the orchestrator and core Part-A scripts (screen/select_rule/stats). Next, I'll build a mini dataset from the Z-labelled rows and a notebook to run the screen and selection rule inline.
```

### [17] TOOL CALL — Bash · 2026-09-24 19:18:13 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_14; cat $W/src/labels.py; cd $W; python3 - <<'EOF'
import json,collections
d=json.load(open('full_method_out.json'))
print(d.keys(), [ (x['dataset'],len(x['examples'])) for x in d['datasets']])
E=d['datasets'][0]['examples']
Z=[e for e in E if e['metadata_in_Z']]
print(len(Z), collections.Counter(e['output'] for e in Z), collections.Counter(e['metadata_stratum'] for e in Z))
print(len({e['metadata_sentence_id'] for e in Z}))
print(collections.Counter(str(e['metadata_error_ops']) for e in Z).most_common(12))
print(collections.Counter(e['metadata_label_tier'] for e in Z))
print(sum(e['predict_V5']=='NA' for e in Z), sum(e['predict_gg']=='NA' for e in Z))
print(json.dumps(d['datasets'][1]['examples'][0])[:1500])
EOF
```

### [18] TOOL RESULT — Bash · 2026-09-24 19:18:13 UTC

```
{"stdout": "\"\"\"Label-side helpers (imported ONLY by post-seal scripts): the R_AB frame, T9 error classes (exp 9 analyse.py classes(),\nverbatim logic), eval-3/exp-5 op_class (vendor_c common.op_class + COARSE, verbatim).\"\"\"\nfrom __future__ import annotations\n\nimport json\n\nimport numpy as np\nimport pandas as pd\n\nfrom common import PER_ITEM, ROOT, RES, jl, sha256_file\n\nCOARSE = {\"ADD\": \"COVERAGE\", \"DROP\": \"COVERAGE\", \"NEG\": \"POLARITY\", \"REV\": \"POLARITY\", \"QUANT\": \"POLARITY\"}\nT9 = [\"ADD\", \"DROP\", \"COMPOUND\", \"polarity(NEG/REV/QUANT)\", \"structural(CONN/RESTR/BIND/MOVE/SWAP/SCOPE/UNGLUE)\",\n      \"MEANING_RENAME-type (MEANING_RENAME op or tier-B VOCAB_GRAN)\"]\n\n\ndef op_class(ops) -> str:\n    \"\"\"eval-2 vendor_exp5/vendor_c/common.py op_class (verbatim).\"\"\"\n    ops = list(ops) if ops is not None and not isinstance(ops, float) else []\n    if not ops:\n        return \"NONE\"\n    cs = {COARSE.get(o, \"STRUCT\") for o in ops}\n    return cs.pop() if len(cs) == 1 else \"MIXED\"\n\n\ndef t9_classes(error_ops, auto_label) -> list[str]:\n    \"\"\"exp 9 src/analyse.py (e) classes(r), verbatim logic.\"\"\"\n    ops = set(error_ops or [])\n    out = []\n    if \"ADD\" in ops: out.append(\"ADD\")\n    if \"DROP\" in ops: out.append(\"DROP\")\n    if \"COMPOUND\" in ops: out.append(\"COMPOUND\")\n    if ops & {\"NEG\", \"REV\", \"QUANT\"}: out.append(\"polarity(NEG/REV/QUANT)\")\n    if ops & {\"CONN\", \"RESTR\", \"BIND\", \"MOVE\", \"SWAP\", \"SCOPE\", \"UNGLUE\"}: out.append(\"structural(CONN/RESTR/BIND/MOVE/SWAP/SCOPE/UNGLUE)\")\n    if \"MEANING_RENAME\" in ops or auto_label == \"VOCAB_GRAN\": out.append(\"MEANING_RENAME-type (MEANING_RENAME op or tier-B VOCAB_GRAN)\")\n    return out\n\n\ndef check_seal(name: str = \"prereg_improve_addendum.json\", key: str = \"scores_sha256\", path: str = \"results/scores_E_variants.jsonl\"):\n    add = json.loads((ROOT / name).read_text())\n    h = sha256_file(ROOT / path)\n    assert add[key] == h, f\"SEAL BROKEN: {path} {h} != {add[key]}\"\n    return add\n\n\ndef frame() -> pd.DataFrame:\n    \"\"\"All E rows: sealed variant scores joined with labels + frozen comparator columns (post-seal only).\"\"\"\n    check_seal()\n    S = pd.DataFrame(jl(RES / \"scores_E_variants.jsonl\"))\n    keep = [\"canonical_key\", \"in_R_AB\", \"pool\", \"parse_ok\", \"y_R_AB\", \"final_label\", \"auto_label\", \"error_ops\", \"label_tier\",\n            \"judge_cheap_disg\", \"judge_cheap_orig\", \"judge_cheap2_orig\", \"p_peer_text\", \"S4_full_oof\", \"system\", \"prompt_variant\"]\n    L = []\n    for r in jl(PER_ITEM):\n        d = {k: r.get(k) for k in keep}\n        d[\"words\"] = r[\"strata\"][\"words\"]\n        d[\"n_conditions\"] = r[\"strata\"][\"n_conditions\"]\n        L.append(d)\n    df = S.merge(pd.DataFrame(L), on=\"canonical_key\", how=\"left\", validate=\"one_to_one\")\n    df[\"R_AB\"] = df.in_R_AB.fillna(False).astype(bool) & (df.pool == \"E_POOL\") & df.parse_ok.fillna(False).astype(bool)\n    df[\"Z\"] = df.R_AB & df.in_matrix & (df.n_peers >= 2)\n    df[\"y\"] = df.y_R_AB\n    df[\"long\"] = df.stratum.isin([\"L25\", \"L20\", \"EXC\"])\n    df[\"words_t\"] = np.where(df.words <= 20, \"T1\", np.where(df.words <= 26, \"T2\", \"T3\"))\n    df[\"t9\"] = [t9_classes(o, a) if y == 1 else [] for o, a, y in zip(df.error_ops, df.auto_label, df.y)]\n    df[\"opc\"] = [op_class(o) for o in df.error_ops]\n    v4p = RES / \"scores_E_V4.jsonl\"\n    if v4p.exists():\n        check_seal(\"prereg_improve_addendum_v4.json\", \"v4_sha256\", \"results/scores_E_V4.jsonl\")\n        V4 = pd.DataFrame(jl(v4p))[[\"row_key\", \"V4\"]]\n        df = df.merge(V4, on=\"row_key\", how=\"left\", validate=\"one_to_one\")\n    return df\ndict_keys(['metadata', 'datasets']) [('E_heldout', 8507), ('PERTURB_E_bases', 722), ('GG_checker_gates', 1069)]\n2672 Counter({'ERROR': 1810, 'CORRECT': 862}) Counter({'L25': 869, 'L20': 818, 'EXC': 602, 'CTRL': 383})\n283\n[('None', 862), (\"['ADD', 'DROP']\", 169), (\"['CONN', 'NEG']\", 72), (\"['COMPOUND', 'ADD', 'DROP']\", 68), (\"['COMPOUND', 'ADD', 'CONN', 'DROP']\", 64), (\"['COMPOUND', 'CONN', 'DROP']\", 52), (\"['COMPOUND', 'DROP']\", 47), (\"['ADD']\", 45), (\"['MEANING_RENAME', 'ADD', 'DROP']\", 43), (\"['COMPOUND', 'ADD', 'DROP', 'RESTR']\", 40), (\"['CONN']\", 38), (\"['COMPOUND', 'ADD', 'BIND', 'DROP']\", 31)]\nCounter({'B': 1810, 'A': 862})\n0 0\n{\"input\": \"{\\\"text\\\": \\\"When something is depressing, it is sad.\\\", \\\"item_key\\\": \\\"PB:68a12f5080ef6661\\\", \\\"kind\\\": \\\"BASE\\\"}\", \"output\": \"CORRECT\", \"predict_gg\": \"0.0769231\", \"predict_gg_allyes\": \"0.0769231\", \"predict_c_exact_identity_map\": \"0.0769231\", \"predict_c_align_exp8\": \"0.0769231\", \"metadata_kind\": \"BASE\", \"metadata_base\": \"68a12f5080ef6661\", \"metadata_sentence_id\": \"0000c2274e80\", \"metadata_base_status\": \"TRUSTED_AGREED\", \"metadata_polarity\": null, \"metadata_base_endorsed\": true, \"metadata_stratum\": \"CTRL\", \"metadata_n_peer_rows\": 13}", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_EU1yuNrRl4od", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [19] TOOL CALL — Bash · 2026-09-24 19:18:21 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_14; head -c 1500 $W/results/scores_E_variants.jsonl; echo; head -c 600 $W/results/scores_E_V4.jsonl; echo; P=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6/results/per_item_T1.jsonl; ls -la $P; head -1 $P | python3 -c "import json,sys; r=json.loads(sys.stdin.read()); print({k:(str(v)[:80]) for k,v in r.items()})"
```

### [20] TOOL RESULT — Bash · 2026-09-24 19:18:23 UTC

```
{"stdout": "{\"row_key\": \"31452c4db10ee367|none\", \"canonical_key\": \"31452c4db10ee367|none\", \"sentence_id\": \"0000c2274e80\", \"fold\": 1, \"stratum\": \"CTRL\", \"family\": \"symbolic\", \"V0_frozen\": 1.0, \"in_matrix\": false, \"V0_rep\": 1.0, \"c_exact\": 1.0, \"V1\": 1.0, \"V2\": 1.0, \"V3\": 1.0, \"V5\": 1.0, \"c3_plain\": 1.0, \"n_peers\": 0, \"n_peers_3pool\": 0, \"coverage_status\": \"UNPARSEABLE\"}\n{\"row_key\": \"b87a8dda4faced11|fewshot_v1\", \"canonical_key\": \"b87a8dda4faced11|fewshot_v1\", \"sentence_id\": \"0000c2274e80\", \"fold\": 1, \"stratum\": \"CTRL\", \"family\": \"openai-frontier\", \"V0_frozen\": 0.090909, \"in_matrix\": true, \"n_peers\": 11, \"n_peers_3pool\": 2, \"coverage_status\": \"OK\", \"V0_rep\": 0.09090909090909094, \"c_exact\": 0.09090909090909094, \"V1\": 0.0, \"V2\": 0.0767922021090236, \"V3\": 0.0, \"V5\": 0.0, \"c3_plain\": 0.0, \"V5_imputed\": false}\n{\"row_key\": \"3222a9e5bc15a5c9|fewshot_v1\", \"canonical_key\": \"3222a9e5bc15a5c9|fewshot_v1\", \"sentence_id\": \"0000c2274e80\", \"fold\": 1, \"stratum\": \"CTRL\", \"family\": \"meta\", \"V0_frozen\": 0.0, \"in_matrix\": true, \"n_peers\": 10, \"n_peers_3pool\": 4, \"coverage_status\": \"OK\", \"V0_rep\": 0.0, \"c_exact\": 0.0, \"V1\": 0.0, \"V2\": 0.0, \"V3\": 0.0, \"V5\": 0.0, \"c3_plain\": 0.0, \"V5_imputed\": false}\n{\"row_key\": \"3222a9e5bc15a5c9|zeroshot_v1\", \"canonical_key\": \"3222a9e5bc15a5c9|zeroshot_v1\", \"sentence_id\": \"0000c2274e80\", \"fold\": 1, \"stratum\": \"CTRL\", \"family\": \"meta\", \"V0_frozen\": 0.0, \"in_matrix\": true, \"n_peers\": 10, \"n_peers_3pool\": 4, \"coverage_status\": \"OK\", \"V0_rep\": 0.0, \"c_exact\": 0.0, \"V1\": 0.0, \"V2\": \n{\"row_key\": \"31452c4db10ee367|none\", \"V4\": 0.8384464684152174, \"V4_oof\": false}\n{\"row_key\": \"b87a8dda4faced11|fewshot_v1\", \"V4\": 0.05949654549026947, \"V4_oof\": true}\n{\"row_key\": \"3222a9e5bc15a5c9|fewshot_v1\", \"V4\": 0.03931292388267155, \"V4_oof\": true}\n{\"row_key\": \"3222a9e5bc15a5c9|zeroshot_v1\", \"V4\": 0.03931292388267155, \"V4_oof\": true}\n{\"row_key\": \"14c1b28f4da33bf6|fewshot_v1\", \"V4\": 0.8313868090595229, \"V4_oof\": true}\n{\"row_key\": \"6287d461765d4960|fewshot_v1\", \"V4\": 0.05949654549026947, \"V4_oof\": true}\n{\"row_key\": \"6287d461765d4960|zeroshot_v1\", \"V4\": 0.05949654549026947, \"V4_oof\": true}\n{\"r\n-rw-r--r-- 1 165536 165536 21937774 Sep 24 03:46 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6/results/per_item_T1.jsonl\n{'canonical_key': '31452c4db10ee367|none', 'exp6_row_key': '31452c4db10ee367', 'exp5_row_key': '31452c4db10ee367|none', 'item_id': '31452c4db10ee367', 'sentence_id': '0000c2274e80', 'fold_E': '1', 'pool': 'CCG', 'parse_ok': 'False', 'system': 'ccg2lambda', 'sysvar': 'ccg2lambda|none', 'family': 'symbolic', 'prompt_variant': 'none', 'strata': \"{'words': 7, 'n_quant': 1, 'depth': 1, 'n_conditions': 1, 'text_conditions': 1, \", 'source_stratum': 'CTRL', 'label_tier': '-', 'final_label': 'UNPARSEABLE', 'auto_label': 'UNPARSEABLE', 'reading_choice': 'False', 'repair_ops': 'None', 'error_ops': 'None', 'in_R_AB': 'False', 'in_R_A': 'False', 'in_COVERAGE': 'True', 'y_R_AB': 'None', 'vex': 'False', 'vex_strict': 'False', 'c_score_align': '1.0', 'g_score': '1.0', 'nf_c_score': '1.0', 'nf_g_score': '1.0', 'p_peer_text': '1.0', 'p_text': '1.0', 'l2_bow': '1.0', 'l3_z3': '1.0', 'judge_cheap_disg': '1.0', 'judge_cheap_disg__status': 'fail', 'judge_cheap_orig': '1.0', 'judge_cheap_orig__status': 'fail', 'judge_cheap2_disg': '1.0', 'judge_cheap2_disg__status': 'fail', 'judge_cheap2_orig': '1.0', 'judge_cheap2_orig__status': 'fail', 'judge_strong_orig': 'None', 'judge_strong_orig__status': 'na', 'judge_strong_disg': 'None', 'judge_strong_disg__status': 'na', 'judge_cheap_disg_vfb': '1.0', 'judge_cheap_disg_vfb__status': 'fail', 'rt_nli_min': '1.0', 'rt_nli_min__status': 'fail', 'rt_nli_fwd': '1.0', 'rt_nli_fwd__status': 'fail', 'rt_nli_bwd': '1.0', 'rt_nli_bwd__status': 'fail', 'rt_nli_contra': '1.0', 'rt_nli_contra__status': 'fail', 'rt_nli_min_alt': '1.0', 'rt_nli_min_alt__status': 'fail', 'rt_embed_cos': '1.0', 'rt_embed_cos__status': 'fail', 'sc5_eq_frac': '1.0', 'sc5_eq_frac__status': 'fail', 'sc5_entropy': '1.791759', 'sc5_entropy__status': 'fail', 'S4_full_oof': 'None', 'S4_local_oof': 'None', 'S4_full_plus_c_score_align_oof': 'None', 'PT_refit_oof': 'None', 'PT_refit_NF_oof': 'None', 'local__judge_local_qwen8b_disg': '1.0', 'local__judge_local_qwen8b_orig': '1.0', 'local__judge_local_llama8b_disg': '1.0', 'local__rt_nli_min_local': '1.0', 'local__sc5_local_eq_frac': '1.0', 'local__parse_fail': '1.0', 'local__pilot_rerun_jacc': '1.0'}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [21] TOOL CALL — Bash · 2026-09-24 19:18:45 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_EU1yuNrRl4od; mkdir -p tools; cat > tools/build_mini_demo_data.py <<'EOF'
"""Build mini_demo_data.json: <=100 labelled rows of population Z (dataset E, eval-2 matrix, >=2 peers) from the
iteration-5 experiment, whole sentences only (so the sentence-cluster bootstrap stays meaningful), ~25 rows per stratum,
each chosen sentence has both CORRECT and ERROR candidates. Joins the sealed score columns and label-side columns the
notebook's frame() needs, plus the full-run reference numbers for comparison."""
import json, random
from collections import defaultdict
from pathlib import Path

SRC = Path("/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_14")
PER_ITEM = Path("/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6/results/per_item_T1.jsonl")
OUT = Path(__file__).resolve().parent.parent / "mini_demo_data.json"

def jl(p):
    return [json.loads(l) for l in Path(p).read_text().splitlines() if l.strip()]

full = json.loads((SRC / "full_method_out.json").read_text())
E = {e["metadata_row_key"]: e for e in full["datasets"][0]["examples"]}
S = {r["row_key"]: r for r in jl(SRC / "results/scores_E_variants.jsonl")}
V4 = {r["row_key"]: r["V4"] for r in jl(SRC / "results/scores_E_V4.jsonl")}
Z = [k for k, e in E.items() if e["metadata_in_Z"]]
by_sent = defaultdict(list)
for k in Z:
    by_sent[E[k]["metadata_sentence_id"]].append(k)
need_ck = set(Z)
PI = {}
for l in PER_ITEM.open():
    r = json.loads(l)
    if r["canonical_key"] in need_ck:
        PI[r["canonical_key"]] = r

rng = random.Random(20260924)
QUOTA = 25
chosen = []
for stratum in ("L25", "L20", "EXC", "CTRL"):
    sents = sorted(s for s, ks in by_sent.items() if E[ks[0]]["metadata_stratum"] == stratum)
    rng.shuffle(sents)
    n = 0
    for s in sents:
        ks = by_sent[s]
        ys = {E[k]["output"] for k in ks}
        if ys != {"CORRECT", "ERROR"} or len(ks) > 12 or n + len(ks) > QUOTA + 3:
            continue
        chosen += ks
        n += len(ks)
        if n >= QUOTA - 2:
            break
assert len(chosen) <= 100, len(chosen)

f = lambda v: None if v in (None, "NA") else float(v)
rows = []
for k in chosen:
    e, s, p = E[k], S[k], PI[k]
    inp = json.loads(e["input"])
    rows.append({
        "row_key": k, "sentence_id": e["metadata_sentence_id"], "text": inp["text"], "candidate_fol": inp["candidate_fol"],
        "system": inp["system"], "prompt_variant": inp["prompt_variant"], "family": e["metadata_family"],
        "stratum": e["metadata_stratum"], "fold": int(e["metadata_fold"]), "n_peers": e["metadata_n_peers"],
        "words": e["metadata_words"], "n_conditions": e["metadata_n_conditions"],
        "label": e["output"], "y": int(e["metadata_y_R_AB"]), "label_tier": e["metadata_label_tier"],
        "error_ops": e["metadata_error_ops"], "auto_label": p.get("auto_label"),
        # label-free scores (higher = more likely ERROR); sealed before the label join in the original run
        "V0_frozen": float(s["V0_frozen"]), "V0_rep": s["V0_rep"], "c_exact": s["c_exact"], "V1": s["V1"], "V2": s["V2"],
        "V3": s["V3"], "V4": V4[k], "V5": s["V5"], "c3_plain": s["c3_plain"],
        "gg": f(e["predict_gg"]), "gg_allyes": f(e["predict_gg_allyes"]),
        "judge_cheap_disg": f(p.get("judge_cheap_disg")), "judge_cheap_orig": f(p.get("judge_cheap_orig")),
        "judge_cheap2_orig": f(p.get("judge_cheap2_orig")), "p_peer_text": f(e["predict_p_peer_text"]),
    })

scr = json.loads((SRC / "results/screen_E.json").read_text())
sel = json.loads((SRC / "results/selection_E.json").read_text())
ref = {
    "note": "numbers from the full run on all 2,672 Z rows / 283 sentences (B=2000 bootstrap); the demo recomputes the same statistics on the subset",
    "auroc": {c: {s: v["auroc"] for s, v in d.items()} for c, d in scr["auroc"].items()},
    "delta_vs_V0": {c: {s: {"delta": v["delta"], "ci": v["ci"]} for s, v in d.items()} for c, d in scr["delta_vs_V0"].items()},
    "ed_ALL": {s: {"e": v["e"], "d": v["d"]} for s, v in scr["ed"]["ALL"].items()},
    "winner": sel["winner"], "stability": sel["stability"], "permutation_null": sel["permutation_null"],
    "GG_g3": full["metadata"]["GG_gates"]["g3"],
}
meta = {"source": "iteration-5 FREEZE experiment (art_EU1yuNrRl4od), dataset E held-out rows, population Z",
        "n_rows": len(rows), "n_sentences": len({r['sentence_id'] for r in rows}),
        "orientation": "every score column: higher = more likely ERROR; y = 1 means ERROR",
        "reference_full_run": ref}
OUT.write_text(json.dumps({"metadata": meta, "rows": rows}, indent=1, ensure_ascii=False))
from collections import Counter
print(len(rows), meta["n_sentences"], Counter(r["stratum"] for r in rows), Counter(r["label"] for r in rows), OUT.stat().st_size)
EOF
python3 tools/build_mini_demo_data.py
```

### [22] TOOL RESULT — Bash [ERROR] · 2026-09-24 19:18:47 UTC

```
Error: Exit code 1
Traceback (most recent call last):
  File "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_EU1yuNrRl4od/tools/build_mini_demo_data.py", line 47, in <module>
    assert len(chosen) <= 100, len(chosen)
           ^^^^^^^^^^^^^^^^^^
AssertionError: 106
```

### [23] TOOL CALL — Bash · 2026-09-24 19:18:49 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_EU1yuNrRl4od; sed -i 's/n + len(ks) > QUOTA + 3/n + len(ks) > QUOTA/; s/if n >= QUOTA - 2:/if n >= QUOTA - 3:/' tools/build_mini_demo_data.py; python3 tools/build_mini_demo_data.py
```

### [24] TOOL RESULT — Bash · 2026-09-24 19:18:51 UTC

```
{"stdout": "93 12 Counter({'EXC': 24, 'CTRL': 24, 'L25': 23, 'L20': 22}) Counter({'ERROR': 54, 'CORRECT': 39}) 107249", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [25] TOOL CALL — Bash · 2026-09-24 19:19:03 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_14; grep -n "g3" $W/src/gg_score.py | head -20; head -60 $W/freeze/consensus_variants.py
```

### [26] TOOL RESULT — Bash · 2026-09-24 19:19:03 UTC

```
{"stdout": "9:g3 (E strat AUROC(c_gg) on Z >= V0 - 0.01). Writes results/scores_gg_E.jsonl, results/scores_gg_perturb.jsonl,\n176:    # ---- g3 + AUROC table\n191:    g3 = D[\"auroc\"][\"ALL-strat\"][\"c_gg\"][\"auroc\"] >= D[\"auroc\"][\"ALL-strat\"][\"V0_frozen\"][\"auroc\"] - 0.01\n220:                  \"g3\": {\"pass\": bool(g3), \"gg\": D[\"auroc\"][\"ALL-strat\"][\"c_gg\"][\"auroc\"], \"V0\": D[\"auroc\"][\"ALL-strat\"][\"V0_frozen\"][\"auroc\"],\n225:    D[\"gates\"][\"GG_status\"] = \"PASS\" if (g1 and g2 and g3 and ck_pass) else \"FAIL\"\n257:    logger.info(f\"g3 {json.dumps(D['gates']['g3'])}\")\n\"\"\"consensus_variants: label-free rescorings of cross-family solver consensus (iteration 5 FREEZE, Part A).\n\nPure functions, no I/O. Input = one sentence's record of eval-2's label-free pairwise matrix (pairwise_classes_E.jsonl line:\nnodes with canon_fol + rows {row_key, slot, family, family_field, is_peer}, pairs [i, j, eq, kind, secs], cliques).\nOrientation everywhere: HIGHER = MORE LIKELY ERROR. UNKNOWN (eq None) never counts as agreement.\n\nPeer pool P(x) (leave-own-family-out, exp 5 convention): parseable rows with is_peer True whose vendor `family` differs from\nthe candidate's, excluding the candidate row itself. |P| < 2 -> score None (exp 5 imputes a neutral value downstream);\nunparseable candidate (no matrix node) -> 1.0.\n\nVariants (V0 is the frozen incumbent):\n  V0 c_score_align  1 - share of P agreeing (eqmv: exact / align / gran). REPRODUCTION ONLY: E2 must score V0 with the\n                    byte-identical exp-5 code, not with this function.\n  c_exact           1 - share of P agreeing by pure z3 equivalence with identical symbols (aligner-free).\n  V1 c_pn           plurality-normalised: 1 - min(1, share_A / max_class_share); classes = eval-2 greedy cliques\n                    restricted to P's rows; share_A == 0 -> 1.0.\n  V2 c_rw           reliability-weighted: 1 - sum_{p in P, A} w_f(p) / sum_{p in P} w_f(p); w_f are label-free\n                    Dawid-Skene-style family weights (mean cross-family agreement rate, shrunk to the grand mean with\n                    strength 20 sentences), estimated OUT OF FOLD (sentence folds) by family_weights().\n  V3 c_pn_rw        V1 with w-weighted shares (candidate share and class shares).\n  V4 c_two_channel  logistic(b0 + b1*c_exact + b2*c_align); coefficients were fit on E labels (cross-fitted OOF on E, then\n                    refit once on all scorable E R_AB rows = the frozen coefficients); APPLICATION is gold-free.\n  V5 c_v5           V3 on the cost-matched 3-pool {deepseek, microsoft, openai} minus the candidate's own family.\n\nCOST: all variants use the same peer pool as V0 (7 peer families, $0.002206 per sentence of generation, eval-2\ntables/m4_auroc_k_cost.csv k=7) except V5 (3-pool, $0.000946 per sentence by the same table's per-family unit cost);\nCPU = the eqmv matrix (median 0.005 s per node pair) plus microseconds of arithmetic.\n\"\"\"\nfrom __future__ import annotations\n\nimport math\nfrom collections import defaultdict\n\nPOOL3 = (\"deepseek\", \"microsoft\", \"openai\")\nSHRINK = 20.0\n\n\n# ------------------------------------------------------------------------------------------------ index\ndef build_index(rec: dict) -> dict:\n    \"\"\"Index one pairwise_classes record. Returns {'sid', 'node_of', 'meta', 'eq', 'kind', 'clique_of'}.\n    MEASURES: nothing (data structure). GOLD-FREE: yes. COST: O(#pairs).\"\"\"\n    eq, kind = {}, {}\n    for i, j, e, k, _s in rec[\"pairs\"]:\n        eq[(i, j)] = eq[(j, i)] = e\n        kind[(i, j)] = kind[(j, i)] = k\n    node_of, meta = {}, {}\n    for nd in rec[\"nodes\"]:\n        for r in nd[\"rows\"]:\n            node_of[r[\"row_key\"]] = nd[\"node_id\"]\n            meta[r[\"row_key\"]] = r\n    clique_of = {}\n    for ci, cl in enumerate(rec.get(\"cliques\") or [[nd[\"node_id\"]] for nd in rec[\"nodes\"]]):\n        for n in cl:\n            clique_of[n] = ci\n    return {\"sid\": rec[\"sentence_id\"], \"node_of\": node_of, \"meta\": meta, \"eq\": eq, \"kind\": kind, \"clique_of\": clique_of,\n            \"nodes\": rec[\"nodes\"]}\n\n\ndef agree(ix: dict, a: int, b: int) -> bool:\n    \"\"\"eqmv agreement of two nodes (same node = True; UNKNOWN = False).\"\"\"", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [27] THINKING · 2026-09-24 19:19:11 UTC

```
Mini dataset is ready (93 rows, 12 sentences, all 4 strata). Next, I'll verify whether the frozen scoring code can recompute V0–V5 from the pairwise matrix within the notebook, rather than just reading stored scores.
```

### [28] TOOL CALL — Bash · 2026-09-24 19:19:11 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_14; cat $W/src/score_variants.py; sed -n 60,400p $W/freeze/consensus_variants.py; cat $W/results/v4_coefs.json; ls -la /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/pairwise_classes_E.jsonl
```

### [29] TOOL RESULT — Bash · 2026-09-24 19:19:11 UTC

```
{"stdout": "#!/usr/bin/env python3\n\"\"\"A2/A3 (LABEL-FREE, sealed): score every dataset-E row with V0_rep, c_exact, V1, V2, V3, V5 (+ 3-pool plain c) from\neval-2's pairwise matrix using freeze/consensus_variants.py. Reads ONLY the ALLOWED_INPUTS (asserted + hashed in the log).\nWrites results/scores_E_variants.jsonl, results/family_weights.json, results/gate_G1_labelfree.json and\nprereg_improve_addendum.json (sha256 seal of the scores, written before any label join).\"\"\"\nfrom __future__ import annotations\n\nimport json\nimport sys\n\nimport numpy as np\n\nfrom common import FREEZE, MATRIX, NEUTRAL_C, RES, ROOT, jdump, jl, sha1, sha256_file, setup_logger, utc\n\nsys.path.insert(0, str(FREEZE))\nimport consensus_variants as CV  # noqa: E402\n\nlogger = setup_logger(\"score_variants\")\nALLOWED_INPUTS = [MATRIX, RES / \"row_index_labelfree.jsonl\", FREEZE / \"consensus_variants.py\"]\n\n\ndef fold_of_sid(sid: str) -> int:\n    return int(sha1(\"E_folds_v1|\" + sid), 16) % 5\n\n\n@logger.catch(reraise=True)\ndef main():\n    hashes = {str(p): sha256_file(p) for p in ALLOWED_INPUTS}\n    logger.info(f\"allowed inputs: {json.dumps(hashes)}\")\n    rows = jl(RES / \"row_index_labelfree.jsonl\")\n    recs = jl(MATRIX)\n    assert len(recs) == 700\n    IX = {r[\"sentence_id\"]: CV.build_index(r) for r in recs}\n    fold = {}\n    for r in rows:\n        f = fold_of_sid(r[\"sentence_id\"])\n        assert f == r[\"fold_E\"], (r[\"sentence_id\"], f, r[\"fold_E\"])\n        fold[r[\"sentence_id\"]] = f\n    for sid in IX:\n        fold.setdefault(sid, fold_of_sid(sid))\n    # V2 weights per holdout fold + full-E\n    idx_list = [IX[s] for s in sorted(IX)]\n    W = {k: CV.family_weights(idx_list, fold, k) for k in range(5)}\n    W_full = CV.family_weights(idx_list, fold, None)\n    jdump({\"per_fold_holdout\": {str(k): v for k, v in W.items()}, \"full_E\": W_full, \"shrink\": CV.SHRINK,\n           \"note\": \"w^(k) estimated on sentences NOT in fold k; applied to rows of fold k\"}, RES / \"family_weights.json\")\n    logger.info(f\"full-E family weights {json.dumps({k: round(v, 4) for k, v in W_full.items()})}\")\n    out = []\n    n_mis = n_cmp = 0\n    mism = []\n    for r in rows:\n        rk, sid = r[\"exp5_row_key\"], r[\"sentence_id\"]\n        ix = IX.get(sid)\n        rec = {\"row_key\": rk, \"canonical_key\": r[\"canonical_key\"], \"sentence_id\": sid, \"fold\": fold[sid],\n               \"stratum\": r[\"source_stratum\"], \"family\": r[\"family\"], \"V0_frozen\": r[\"c_score_align\"]}\n        in_mx = ix is not None and rk in ix[\"node_of\"]\n        rec[\"in_matrix\"] = in_mx\n        if not in_mx:\n            rec.update(V0_rep=1.0, c_exact=1.0, V1=1.0, V2=1.0, V3=1.0, V5=1.0, c3_plain=1.0, n_peers=0, n_peers_3pool=0,\n                       coverage_status=\"UNPARSEABLE\")\n        else:\n            P = CV.peers_lofo(ix, rk)\n            P3 = CV.peers_lofo(ix, rk, families=CV.POOL3)\n            w = W[fold[sid]]\n            rec.update(n_peers=len(P), n_peers_3pool=len(P3), coverage_status=\"OK\" if len(P) >= 2 else \"PEER_UNAVAILABLE\",\n                       V0_rep=CV.c_score_align(ix, rk, P), c_exact=CV.c_exact(ix, rk, P), V1=CV.c_pn(ix, rk, P),\n                       V2=CV.c_rw(ix, rk, w, P), V3=CV.c_pn_rw(ix, rk, w, P), V5=CV.c_v5(ix, rk, w),\n                       c3_plain=(CV.c_score_align(ix, rk, P3, min_peers=1)))\n            rec[\"V5_imputed\"] = rec[\"V5\"] is None\n            if rec[\"V5\"] is None:\n                rec[\"V5\"] = NEUTRAL_C\n            if rec[\"c3_plain\"] is None:\n                rec[\"c3_plain\"] = NEUTRAL_C\n        if rec[\"V0_rep\"] is not None and rec[\"V0_frozen\"] is not None:\n            n_cmp += 1\n            if abs(rec[\"V0_rep\"] - rec[\"V0_frozen\"]) > 1e-6:  # per_item_T1 stores 6 decimals\n                n_mis += 1\n                mism.append({\"row_key\": rk, \"rep\": rec[\"V0_rep\"], \"frozen\": rec[\"V0_frozen\"], \"n_peers\": rec[\"n_peers\"]})\n        out.append(rec)\n    g1 = {\"n_compared\": n_cmp, \"n_mismatch\": n_mis, \"mismatch_share\": n_mis / n_cmp, \"rule\": \"<= 0.005 of rows with |V0_rep - V0_frozen| > 1e-6 (the frozen column is rounded to 6 decimals)\",\n          \"pass\": n_mis / n_cmp <= 0.005, \"mismatches\": mism[:100],\n          \"n_rows_peer_unavailable\": sum(r[\"coverage_status\"] == \"PEER_UNAVAILABLE\" for r in out),\n          \"n_rows_unparseable\": sum(r[\"coverage_status\"] == \"UNPARSEABLE\" for r in out)}\n    logger.info(f\"G1 label-free part: {n_mis}/{n_cmp} = {n_mis / n_cmp:.4%} mismatch -> pass={g1['pass']}\")\n    jdump(g1, RES / \"gate_G1_labelfree.json\")\n    sp = RES / \"scores_E_variants.jsonl\"\n    with sp.open(\"w\") as fh:\n        for rec in out:\n            fh.write(json.dumps(rec) + \"\\n\")\n    add = {\"written_utc\": utc(), \"scores_file\": \"results/scores_E_variants.jsonl\", \"scores_sha256\": sha256_file(sp),\n           \"family_weights_sha256\": sha256_file(RES / \"family_weights.json\"), \"allowed_inputs_sha256\": hashes,\n           \"prereg_improve_sha256\": (ROOT / \"prereg_improve.sha256\").read_text().split()[0],\n           \"note\": \"seal written BEFORE any label join (fit_v4.py / screen.py verify this hash)\"}\n    jdump(add, ROOT / \"prereg_improve_addendum.json\")\n    logger.info(f\"sealed scores sha256 {add['scores_sha256']}\")\n    if not g1[\"pass\"]:\n        raise SystemExit(\"G1 FAILED -> fallback F1\")\n\n\nif __name__ == \"__main__\":\n    main()\n    \"\"\"eqmv agreement of two nodes (same node = True; UNKNOWN = False).\"\"\"\n    return True if a == b else ix[\"eq\"].get((a, b)) is True\n\n\ndef agree_exact(ix: dict, a: int, b: int) -> bool:\n    \"\"\"Aligner-free agreement: same node, or eq True with kind 'exact'.\"\"\"\n    return True if a == b else (ix[\"eq\"].get((a, b)) is True and ix[\"kind\"].get((a, b)) == \"exact\")\n\n\ndef peers_lofo(ix: dict, row_key: str, families: tuple | None = None, family_key: str = \"family\") -> list[str]:\n    \"\"\"Peer rows of candidate `row_key`: is_peer, other vendor family, not itself; optionally restricted to `families`.\n    MEASURES: the pool. GOLD-FREE: yes.\"\"\"\n    fam = ix[\"meta\"][row_key][family_key]\n    out = []\n    for rk, m in ix[\"meta\"].items():\n        if not m[\"is_peer\"] or m[family_key] == fam or rk == row_key:\n            continue\n        if families is not None and m[family_key] not in families:\n            continue\n        out.append(rk)\n    return sorted(out)\n\n\n# ------------------------------------------------------------------------------------------------ V0 / exact\ndef c_score_align(ix: dict, row_key: str, peers: list[str] | None = None, min_peers: int = 2) -> float | None:\n    \"\"\"V0 = 1 - share of peers eqmv-agreeing. REPRODUCTION ONLY (E2 must use exp-5 byte-identical code for V0).\n    MEASURES: disagreement with other-family translations modulo vocabulary alignment. GOLD-FREE: yes.\"\"\"\n    if row_key not in ix[\"node_of\"]:\n        return 1.0\n    P = peers_lofo(ix, row_key) if peers is None else peers\n    if len(P) < min_peers:\n        return None\n    c = ix[\"node_of\"][row_key]\n    return 1 - sum(agree(ix, c, ix[\"node_of\"][p]) for p in P) / len(P)\n\n\ndef c_exact(ix: dict, row_key: str, peers: list[str] | None = None, min_peers: int = 2) -> float | None:\n    \"\"\"1 - share of peers z3-equivalent with identical symbols (no aligner). GOLD-FREE: yes.\"\"\"\n    if row_key not in ix[\"node_of\"]:\n        return 1.0\n    P = peers_lofo(ix, row_key) if peers is None else peers\n    if len(P) < min_peers:\n        return None\n    c = ix[\"node_of\"][row_key]\n    return 1 - sum(agree_exact(ix, c, ix[\"node_of\"][p]) for p in P) / len(P)\n\n\n# ------------------------------------------------------------------------------------------------ V1 / V3 / V5\ndef _pn(ix: dict, row_key: str, P: list[str], w: dict | None) -> float:\n    c = ix[\"node_of\"][row_key]\n    wt = (lambda rk: 1.0) if w is None else (lambda rk: float(w.get(ix[\"meta\"][rk][\"family\"], 1.0)))\n    tot = sum(wt(p) for p in P)\n    if tot <= 0:\n        return 1.0\n    share_a = sum(wt(p) for p in P if agree(ix, c, ix[\"node_of\"][p])) / tot\n    if share_a == 0:\n        return 1.0\n    cls = defaultdict(float)\n    for p in P:\n        cls[ix[\"clique_of\"][ix[\"node_of\"][p]]] += wt(p)\n    max_share = max(cls.values()) / tot\n    return 1 - min(1.0, share_a / max_share)\n\n\ndef c_pn(ix: dict, row_key: str, peers: list[str] | None = None, min_peers: int = 2) -> float | None:\n    \"\"\"V1 plurality-normalised consensus: 1 - min(1, share_A / max_class_share) (share_A = 0 -> 1.0).\n    MEASURES: how far the candidate's support falls short of the largest peer class (a candidate in the plurality of a\n    scattered pool scores 0). GOLD-FREE: yes.\"\"\"\n    if row_key not in ix[\"node_of\"]:\n        return 1.0\n    P = peers_lofo(ix, row_key) if peers is None else peers\n    if len(P) < min_peers:\n        return None\n    return _pn(ix, row_key, P, None)\n\n\ndef c_pn_rw(ix: dict, row_key: str, weights: dict, peers: list[str] | None = None, min_peers: int = 2) -> float | None:\n    \"\"\"V3 = V1 with family-weighted shares. GOLD-FREE: yes (weights are label-free).\"\"\"\n    if row_key not in ix[\"node_of\"]:\n        return 1.0\n    P = peers_lofo(ix, row_key) if peers is None else peers\n    if len(P) < min_peers:\n        return None\n    return _pn(ix, row_key, P, weights)\n\n\ndef c_v5(ix: dict, row_key: str, weights: dict, families: tuple = POOL3) -> float | None:\n    \"\"\"V5 = V3 on the cost-matched 3-pool {deepseek, microsoft, openai} minus own family; >= 1 pool row required\n    (eval-2 c_k3 convention: empty pool -> None, imputed neutral downstream). GOLD-FREE: yes.\"\"\"\n    if row_key not in ix[\"node_of\"]:\n        return 1.0\n    P = peers_lofo(ix, row_key, families=families)\n    if len(P) < 1:\n        return None\n    return _pn(ix, row_key, P, weights)\n\n\n# ------------------------------------------------------------------------------------------------ V2\ndef family_weights(indexes: list[dict], fold_of: dict, holdout_fold: int | None, shrink: float = SHRINK) -> dict:\n    \"\"\"Label-free family reliability weights from the pairwise matrix of every sentence NOT in `holdout_fold`\n    (holdout_fold None = all sentences). For family f and sentence s (>= 1 peer row of f and >= 1 peer row of another\n    family): agr_f(s) = mean over (r in f, q not in f) of A(r, q). a_f = mean_s agr_f(s), n_f = #such sentences,\n    abar = mean over all (f, s) of agr_f(s); w_f = (n_f * a_f + shrink * abar) / (n_f + shrink).\n    MEASURES: how often a family's translations agree with other families' (a proxy for its reliability, Dawid-Skene\n    style, no labels). GOLD-FREE: yes.\"\"\"\n    per = defaultdict(list)\n    allv = []\n    for ix in indexes:\n        if holdout_fold is not None and fold_of[ix[\"sid\"]] == holdout_fold:\n            continue\n        peers = [rk for rk, m in ix[\"meta\"].items() if m[\"is_peer\"]]\n        fams = defaultdict(list)\n        for rk in peers:\n            fams[ix[\"meta\"][rk][\"family\"]].append(rk)\n        for f, rs in fams.items():\n            qs = [q for q in peers if ix[\"meta\"][q][\"family\"] != f]\n            if not rs or not qs:\n                continue\n            v = sum(agree(ix, ix[\"node_of\"][r], ix[\"node_of\"][q]) for r in rs for q in qs) / (len(rs) * len(qs))\n            per[f].append(v)\n            allv.append(v)\n    abar = sum(allv) / len(allv) if allv else 0.0\n    return {f: (len(v) * (sum(v) / len(v)) + shrink * abar) / (len(v) + shrink) for f, v in sorted(per.items())}\n\n\ndef c_rw(ix: dict, row_key: str, weights: dict, peers: list[str] | None = None, min_peers: int = 2) -> float | None:\n    \"\"\"V2 = 1 - sum_{p in P agreeing} w_f(p) / sum_{p in P} w_f(p); families missing from `weights` get weight 1.0\n    (never happens on E). GOLD-FREE: yes.\"\"\"\n    if row_key not in ix[\"node_of\"]:\n        return 1.0\n    P = peers_lofo(ix, row_key) if peers is None else peers\n    if len(P) < min_peers:\n        return None\n    c = ix[\"node_of\"][row_key]\n    wt = {p: float(weights.get(ix[\"meta\"][p][\"family\"], 1.0)) for p in P}\n    tot = sum(wt.values())\n    if tot <= 0:\n        return 1.0\n    return 1 - sum(wt[p] for p in P if agree(ix, c, ix[\"node_of\"][p])) / tot\n\n\n# ------------------------------------------------------------------------------------------------ V4\ndef c_two_channel(c_exact_v: float | None, c_align_v: float | None, coefs: dict) -> float | None:\n    \"\"\"V4 = sigmoid(b0 + b_exact * c_exact + b_align * c_align). coefs = {'intercept', 'c_exact', 'c_align'}.\n    MEASURES: a label-fitted blend of aligner-free and aligned disagreement. GOLD-FREE application (coefficients were fit\n    on E labels, OOF in development).\"\"\"\n    if c_exact_v is None or c_align_v is None:\n        return None\n    z = coefs[\"intercept\"] + coefs[\"c_exact\"] * c_exact_v + coefs[\"c_align\"] * c_align_v\n    return 1 / (1 + math.exp(-z))\n{\n \"frozen_coefficients_full_Z\": {\n  \"intercept\": -3.472996682952369,\n  \"c_exact\": 3.5444565071756204,\n  \"c_align\": 1.5752543602595768\n },\n \"per_fold\": {\n  \"0\": {\n   \"intercept\": -3.1876924517236818,\n   \"c_exact\": 3.49812053105509,\n   \"c_align\": 1.3217047010838594,\n   \"n_train\": 2110,\n   \"n_test\": 562\n  },\n  \"1\": {\n   \"intercept\": -3.196095415964957,\n   \"c_exact\": 3.3020351705702757,\n   \"c_align\": 1.489548125561367,\n   \"n_train\": 2098,\n   \"n_test\": 574\n  },\n  \"2\": {\n   \"intercept\": -3.123279391241242,\n   \"c_exact\": 3.005715817436256,\n   \"c_align\": 1.7333522696138521,\n   \"n_train\": 2123,\n   \"n_test\": 549\n  },\n  \"3\": {\n   \"intercept\": -4.885956741177755,\n   \"c_exact\": 4.995131013728068,\n   \"c_align\": 1.612656098292133,\n   \"n_train\": 2171,\n   \"n_test\": 501\n  },\n  \"4\": {\n   \"intercept\": -3.2970687065222575,\n   \"c_exact\": 3.251963667589233,\n   \"c_align\": 1.7303173480727925,\n   \"n_train\": 2186,\n   \"n_test\": 486\n  }\n },\n \"features\": [\n  \"c_exact\",\n  \"c_align (V0 frozen)\"\n ],\n \"model\": \"sklearn LogisticRegression(C=1e6, intercept, lbfgs)\",\n \"n_Z\": 2672\n}-rw-r--r-- 1 root root 3597729 Sep 24 03:18 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/pairwise_classes_E.jsonl", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [30] TOOL CALL — Bash · 2026-09-24 19:19:23 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_EU1yuNrRl4od; python3 - <<'EOF'
p='tools/build_mini_demo_data.py'
s=open(p).read()
s=s.replace('''meta = {"source"''','''MATRIX = Path("/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/pairwise_classes_E.jsonl")
sids = {r["sentence_id"] for r in rows}
matrix = [r for r in jl(MATRIX) if r["sentence_id"] in sids]
fw = json.loads((SRC / "results/family_weights.json").read_text())
v4c = json.loads((SRC / "results/v4_coefs.json").read_text())
meta = {"source"''')
s=s.replace('''OUT.write_text(json.dumps({"metadata": meta, "rows": rows}''','''OUT.write_text(json.dumps({"metadata": meta, "rows": rows, "pairwise_matrix": matrix,
                           "family_weights": fw, "v4_coefs": v4c}''')
open(p,'w').write(s)
EOF
python3 tools/build_mini_demo_data.py; python3 -c "
import json;d=json.load(open('mini_demo_data.json'));m=d['pairwise_matrix'];print(len(m));r=m[0];print(list(r.keys()));print(json.dumps(r['nodes'][0])[:600]);print(r['pairs'][:3]); print(r.get('cliques'))"
```

### [31] TOOL RESULT — Bash · 2026-09-24 19:19:23 UTC

```
{"stdout": "93 12 Counter({'EXC': 24, 'CTRL': 24, 'L25': 23, 'L20': 22}) Counter({'ERROR': 54, 'CORRECT': 39}) 182720\n12\n['sentence_id', 'source_stratum', 'words', 'n_conditions', 'nodes', 'pairs', 'unparseable_row_keys', 'components', 'cliques', 'n_nontransitive_triples', 'n_wedges', 'eqmv_ms', 'pair_cap_s', 'z3_version', 'code_sha']\n{\"node_id\": 0, \"canon_fol\": \"\\u2200v0 ((((FoodItem(v0) \\u2227 HasLimitedShelfLife(v0)) \\u2227 (RequiresRefrigeration(v0) \\u2228 RequiresFreezing(v0))) \\u2192 Perishable(v0)))\", \"rows\": [{\"row_key\": \"09afc591b29683cd|fewshot_v1\", \"slot\": \"G6\", \"family\": \"microsoft\", \"family_field\": \"microsoft\", \"system_class\": \"llm\", \"is_peer\": true}]}\n[[0, 1, True, 'gran', 0.0046], [0, 2, True, 'align', 0.0035], [0, 3, True, 'align', 0.0053]]\n[[0, 1, 2], [4, 6], [3], [5], [7], [8]]", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [32] THINKING · 2026-09-24 19:22:37 UTC

```
The mini dataset now includes the pairwise-matrix records, family weights, and V4 coefficients needed for end-to-end label-free scoring. I'll write the notebook next.
```

### [33] TOOL CALL — Bash · 2026-09-24 19:22:37 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [34] TOOL RESULT — Bash · 2026-09-24 19:22:37 UTC

```
{"stdout": "wrote /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_EU1yuNrRl4od/code_demo.ipynb 29 cells", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": true}
```

### [35] TOOL CALL — Bash · 2026-09-24 19:22:43 UTC

```
/usr/local/bin/python3.12 -m venv .nb_env && .nb_env/bin/pip install -q pip jupyter ipykernel 2>&1 | tail -2; time .nb_env/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -20
```

### [36] TOOL RESULT — Bash · 2026-09-24 19:34:41 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false, "backgroundTaskId": "b2lx4onzm", "timedOutAfterMs": 600000}
```

### [37] ASSISTANT · 2026-09-24 19:34:41 UTC

```
While the test run finishes, I'll write the README and manifest.
```

### [38] TOOL CALL — Bash · 2026-09-24 19:34:41 UTC

````
cat > .aii/manifest.yaml <<'EOF'
entries:
  - path: .nb_env/
    delete: regenerable
    source: "/usr/local/bin/python3.12 -m venv .nb_env && .nb_env/bin/pip install -q pip jupyter ipykernel (the notebook's install cell adds the rest)"
EOF
cat > README.md <<'EOF'
# Demo: screening fixes for model-agreement false alarms (iteration 5, experiment 14)

A runnable Colab notebook for the iteration-5 FREEZE experiment (Part A). The experiment tests five label-free
rescorings (V1–V5) of the cross-family solver-consensus metric **V0 = `c_score_align`**. Each rescoring tries to cut
V0's false alarms on NL→FOL candidates without raising error endorsement. A pre-registered selection rule decides the
outcome. The full run's verdict is **"NONE: V0 stands"**. The notebook also covers gate g3 of the gloss-gated agreement
metric (GG), which fails.

The original `method.py` is an orchestrator that calls ~25 `src/` scripts. The notebook keeps its `STEPS` table and
loop as a dry run. It then runs the core pipeline inline, using the artifact's own functions with no edits
(`freeze/consensus_variants.py`, `src/stats.py`, `src/labels.py`, `src/screen.py`, `src/select_rule.py`), on a 93-row,
12-sentence subset:

1. label-free scoring from the pairwise z3 matrix, which reproduces the sealed scores exactly;
2. the AUROC screen with a sentence-cluster bootstrap, paired Δ vs V0 and the e/d decomposition;
3. the selection rule, its stability, and a permutation null;
4. GG gate g3;
5. plots comparing the demo subset with the full run.

## Layout

| path | what |
|---|---|
| `code_demo.ipynb` | the demo notebook (loads data from GitHub, falls back to the local file) |
| `mini_demo_data.json` | 93 labelled rows of population Z (12 whole sentences, all four strata), the eval-2 pairwise-matrix records of those sentences, the full run's out-of-fold family weights and V4 coefficients, and the full-run reference numbers |
| `tools/build_mini_demo_data.py` | builds `mini_demo_data.json` from the experiment's outputs (needs the original run's volume) |
| `tools/make_notebook.py` | writes `code_demo.ipynb`; the argument sets the config, e.g. `'{"B":2000,"B_STAB":500,"B_NULL":200}'` |

## Running

Open `code_demo.ipynb` in Colab and run all cells. To run it locally:

```bash
python3.12 -m venv .nb_env && .nb_env/bin/pip install -q jupyter ipykernel
.nb_env/bin/jupyter nbconvert --to notebook --execute code_demo.ipynb --output code_demo.ipynb
```

The config cell sets `B`, `B_STAB` and `B_NULL`, the bootstrap, stability and null sizes. The notebook ships with the
original values (2000 / 500 / 200). Results on 93 rows are illustrative only; the conclusions come from the full run.

## Restoring removed files

`.nb_env/` is the throwaway test virtualenv. It is deleted after the round. Recreate it with:

```bash
/usr/local/bin/python3.12 -m venv .nb_env && .nb_env/bin/pip install -q pip jupyter ipykernel
```

The notebook's first cell installs everything else: `loguru` always, and numpy, pandas, scipy, scikit-learn and
matplotlib at Colab's versions when running outside Colab.
EOF
````

### [39] TOOL RESULT — Bash · 2026-09-24 19:34:41 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [40] TOOL CALL — Bash · 2026-09-24 19:34:41 UTC

```
sleep 240; cat /tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-EU1yuNrRl4od/908df641-116b-490e-b0c2-adb76bc47178/tasks/b2lx4onzm.output
```

### [41] TOOL RESULT — Bash [ERROR] · 2026-09-24 19:34:41 UTC

```
Error: Blocked: sleep 240 followed by: cat /tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-EU1yuNrRl4od/908df641-116b-490e-b0c2-adb76bc47178/tasks/b2lx4onzm.output. To wait for a condition, use Monitor with an until-loop (e.g. `until <check>; do sleep 2; done`). To wait for a command you started, use run_in_background: true. Do not chain shorter sleeps to work around this block.
```

### [42] TOOL CALL — Bash · 2026-09-24 19:34:41 UTC

```
cat /tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-EU1yuNrRl4od/908df641-116b-490e-b0c2-adb76bc47178/tasks/b2lx4onzm.output; ls /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_EU1yuNrRl4od/.nb_env/lib/python3.12/site-packages | grep -iE "numpy|pandas|scipy|sklearn|loguru|matplotlib"
```

### [43] TOOL RESULT — Bash · 2026-09-24 19:34:41 UTC

```
{"stdout": "[notice] A new release of pip is available: 25.0.1 -> 26.2.1\n[notice] To update, run: python3.12 -m pip install --upgrade pip\nloguru\nloguru-0.7.3.dist-info\nmatplotlib_inline\nmatplotlib_inline-0.2.2.dist-info\nnumpy\nnumpy-2.0.2.dist-info\nnumpy.libs\nscipy\nscipy-1.16.3.dist-info\nscipy.libs", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [44] TOOL CALL — Bash · 2026-09-24 19:34:41 UTC

```
F=/tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-EU1yuNrRl4od/908df641-116b-490e-b0c2-adb76bc47178/tasks/b2lx4onzm.output; until grep -qE "real|Error|Writing" $F; do sleep 5; done; cat $F
```

### [45] TOOL RESULT — Bash · 2026-09-24 19:39:32 UTC

```
{"stdout": "[notice] A new release of pip is available: 25.0.1 -> 26.2.1\n[notice] To update, run: python3.12 -m pip install --upgrade pip\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m A new release of pip is available: \u001b[0m\u001b[31;49m25.0.1\u001b[0m\u001b[39;49m -> \u001b[0m\u001b[32;49m26.2.1\u001b[0m\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m To update, run: \u001b[0m\u001b[32;49mpython3.12 -m pip install --upgrade pip\u001b[0m\n\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m A new release of pip is available: \u001b[0m\u001b[31;49m25.0.1\u001b[0m\u001b[39;49m -> \u001b[0m\u001b[32;49m26.2.1\u001b[0m\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m To update, run: \u001b[0m\u001b[32;49mpython3.12 -m pip install --upgrade pip\u001b[0m\n[NbConvertApp] Writing 177272 bytes to code_demo.ipynb\n\nreal\t6m41.230s\nuser\t0m19.985s\nsys\t0m2.733s\n\n[exited with code 0]", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [46] TOOL CALL — Bash · 2026-09-24 19:39:32 UTC

```
python3 - <<'EOF'
import json
nb=json.load(open('code_demo.ipynb'))
for i,c in enumerate(nb['cells']):
    if c['cell_type']!='code': continue
    for o in c['outputs']:
        if o['output_type']=='stream': t=''.join(o['text'])
        elif o['output_type']=='error': t='ERROR '+o['ename']+o['evalue']
        elif 'text/plain' in o.get('data',{}): t=''.join(o['data']['text/plain'])
        else: t=str(list(o.get('data',{}).keys()))
        print(f'--- cell {i}:', t[-2500:])
EOF
```

### [47] TOOL RESULT — Bash · 2026-09-24 19:39:32 UTC

```
{"stdout": "--- cell 1: \n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m A new release of pip is available: \u001b[0m\u001b[31;49m25.0.1\u001b[0m\u001b[39;49m -> \u001b[0m\u001b[32;49m26.2.1\u001b[0m\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m To update, run: \u001b[0m\u001b[32;49mpython3.12 -m pip install --upgrade pip\u001b[0m\n\n--- cell 1: \n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m A new release of pip is available: \u001b[0m\u001b[31;49m25.0.1\u001b[0m\u001b[39;49m -> \u001b[0m\u001b[32;49m26.2.1\u001b[0m\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m To update, run: \u001b[0m\u001b[32;49mpython3.12 -m pip install --upgrade pip\u001b[0m\n\n--- cell 4: iteration-5 FREEZE experiment (art_EU1yuNrRl4od), dataset E held-out rows, population Z\nrows: 93 | sentences: 12 | matrix records: 12\n{'CTRL': 24, 'EXC': 24, 'L25': 23, 'L20': 22} {'ERROR': 54, 'CORRECT': 39}\n\nexample row: {'text': 'A vehicle that is designed for off-road use, has four-wheel drive, and is built for rugged terrain is either a jeep or a pickup truck.', 'candidate_fol': '∀x ((DesignedForOffRoad(x) ∧ FourWheelDrive(x) ∧ BuiltForRuggedTerrain(x)) → (Jeep(x) ∨ PickupTruck(x)))', 'system': 'G1:meta-llama/llama-3.1-8b-instruct', 'label': 'ERROR', 'V0_frozen': 0.75, 'V1': 0.0, 'V4': 0.6081737363673899}\n\n--- cell 8: 19:36:55|INFO   |[A] run copy_inputs.py\n\n--- cell 8: 19:36:55|INFO   |[A] run step0_gates.py\n\n--- cell 8: 19:36:55|INFO   |[A] run prereg_improve.py\n\n--- cell 8: 19:36:55|INFO   |[A] run make_row_index.py\n\n--- cell 8: 19:36:55|INFO   |[A] run score_variants.py\n\n--- cell 8: 19:36:55|INFO   |[A] run fit_v4.py\n\n--- cell 8: 19:36:55|INFO   |[A] run screen.py\n\n--- cell 8: 19:36:55|INFO   |[A] run select_rule.py\n\n--- cell 8: 19:36:55|INFO   |[A] run freeze_part_a.py\n\n--- cell 8: 19:36:55|INFO   |[B] run probe.py\n\n--- cell 8: 19:36:55|INFO   |[B] run prereg_gg.py\n\n--- cell 8: 19:36:55|INFO   |[B] run gg_search.py all\n\n--- cell 8: 19:36:55|INFO   |[B] run gg_gates.py dev v1\n\n--- cell 8: 19:36:55|INFO   |[B] run gg_gates.py confirm v2\n\n--- cell 8: 19:36:55|INFO   |[B] run gg_gloss.py\n\n--- cell 8: 19:36:55|INFO   |[B] run gg_score.py\n\n--- cell 8: 19:36:55|INFO   |[B] run freeze_part_b.py\n\n--- cell 8: 19:36:55|INFO   |[GGB] run ggb_search.py all\n\n--- cell 8: 19:36:55|INFO   |[GGB] run ggb_score.py\n\n--- cell 8: 19:36:55|INFO   |[C] run vendor_lib.py\n\n--- cell 8: 19:36:55|INFO   |[OUT] run make_outputs.py\n\n--- cell 8: 19:36:55|INFO   |[OUT] run make_tables.py\n\n--- cell 8: 19:36:55|INFO   |[TEST] run -m pytest -q tests/test_variants.py tests/test_gg.py tests/test_budget.py\n\n--- cell 8: 19:36:55|INFO   |[TEST] run tests/audit_rederive.py\n\n--- cell 8: 19:36:55|INFO   |[TEST] run tests/smoke_lib.py\n\n--- cell 12: G1 label-free part: 0/93 = 0.0000% mismatch -> pass=True  (full run: 24/8,469 = 0.28%)\n  V0_rep    max |recomputed - sealed| = 0.00e+00\n  c_exact   max |recomputed - sealed| = 0.00e+00\n  V1        max |recomputed - sealed| = 0.00e+00\n  V2        max |recomputed - sealed| = 0.00e+00\n  V3        max |recomputed - sealed| = 0.00e+00\n  V4        max |recomputed - sealed| = 2.78e-17\n  V5        max |recomputed - sealed| = 0.00e+00\n  c3_plain  max |recomputed - sealed| = 0.00e+00\n\n--- cell 16:                         row_key stratum words_t  y  V0_frozen   V1        V2        V4       opc\n0   ce029142e9e39ecf|fewshot_v1     L25      T2  1       0.75  0.0  0.849561  0.608174  COVERAGE\n1   76fa388e3aef12c0|fewshot_v1     L25      T2  0       1.00  1.0  1.000000  0.843593      NONE\n2   489326704704ea3e|fewshot_v1     L25      T2  1       1.00  1.0  1.000000  0.843593     MIXED\n3   1f3268ca0f4b7bfb|fewshot_v1     L25      T2  0       1.00  1.0  1.000000  0.843593      NONE\n4   a30931033ad41e37|fewshot_v1     L25      T2  1       0.75  0.0  0.792214  0.608174  COVERAGE\n5   d1f48f496aeaf42f|fewshot_v1     L25      T3  1       1.00  1.0  1.000000  0.848364     MIXED\n6  480ad2a29f340aad|zeroshot_v1     L25      T3  1       1.00  1.0  1.000000  0.848364     MIXED\n7   f40b51c60be9a99f|fewshot_v1     L25      T3  1       1.00  1.0  1.000000  0.848364     MIXED\nZ rows: 93 | ERROR: 54 | sentences: 12\n\n--- cell 19: 19:36:56|INFO   |repro {\"c_exact_pooled_auroc_Z\": 0.7571225071225072, \"target_c_exact\": 0.748, \"c3_plain_pooled_auroc_Z\": 0.8779677113010447, \"target_c3_eval2_c_k3_best_oof\": 0.784520131776288, \"V0_frozen_pooled_Z\": 0.8321462488129154, \"V0_rep_pooled_Z\": 0.8321462488129154, \"n_V5_imputed_neutral_in_Z\": 4}\n\n--- cell 19: 19:36:56|INFO   |ALL-strat: V0_frozen=0.7460 V0_rep=0.7460 c_exact=0.6508 V1=0.7619 V2=0.7596 V3=0.7766 V4=0.7347 V5=0.8401\n\n--- cell 19: 19:36:56|INFO   |pooled: V0_frozen=0.8321 V0_rep=0.8321 c_exact=0.7571 V1=0.8184 V2=0.8364 V3=0.8435 V4=0.8120 V5=0.8870\n\n--- cell 19: 19:36:56|INFO   |LONG-strat: V0_frozen=0.6637 V0_rep=0.6637 c_exact=0.5465 V1=0.6847 V2=0.6817 V3=0.7042 V4=0.6486 V5=0.7883\n\n--- cell 19: 19:36:56|INFO   |L25: V0_frozen=0.4412 V0_rep=0.4412 c_exact=0.4412 V1=0.4412 V2=0.4412 V3=0.4412 V4=0.5588 V5=0.6078\n\n--- cell 19: 19:36:56|INFO   |L20: V0_frozen=0.6771 V0_rep=0.6771 c_exact=0.3333 V1=0.6406 V2=0.7292 V3=0.7083 V4=0.5000 V5=0.8229\n\n--- cell 19: 19:36:56|INFO   |EXC: V0_frozen=0.8222 V0_rep=0.8222 c_exact=0.7778 V1=0.9000 V2=0.8296 V3=0.9000 V4=0.8222 V5=0.9000\n\n--- cell 19: 19:36:56|INFO   |CTRL: V0_frozen=1.0000 V0_rep=1.0000 c_exact=0.9722 V1=1.0000 V2=1.0000 V3=1.0000 V4=1.0000 V5=1.0000\n\n--- cell 21: 19:36:56|INFO   |screen done 0.1s\n\n--- cell 21:     score     d     e\nV0_frozen 0.410 0.056\n   V0_rep 0.410 0.056\n  c_exact 0.744 0.000\n       V1 0.231 0.185\n       V2 0.410 0.056\n       V3 0.231 0.111\n       V4 0.410 0.056\n       V5 0.205 0.056\n\n--- cell 24: 19:36:56|INFO   |DECISION: V5; {\"V1\": 0.021, \"V2\": 0.018, \"V3\": 0.0405, \"V4\": -0.015, \"V5\": 0.1246}\n\n--- cell 24: 19:36:56|INFO   |stability {'V5': 1.0}\n\n--- cell 24: 19:36:56|INFO   |null {'B': 5, 'share_any_variant_qualifies': 0.2, 'share_per_variant': {'V1': 0.0, 'V2': 0.2, 'V3': 0.0, 'V4': 0.0, 'V5': 0.0}, 'note': 'within-stratum label permutation of Z; V4 re-cross-fitted on each permuted label vector'}\n\n--- cell 26: g3 (demo subset): {'pass': False, 'gg': 0.6395, 'V0': 0.746, 'delta': -0.1066, 'delta_ci': [-0.32006906077348063, -0.004269662921348296]}\nGG e=0.056 d=0.487 | V0 e=0.056 d=0.410\nfull run g3: {'pass': False, 'gg': 0.6964364733668502, 'V0': 0.7421654662067422, 'delta_ci': [-0.0708974380922907, -0.021226381894754013]}\n\n--- cell 28:     score  LONG-strat demo  LONG-strat full  ALL-strat demo  ALL-strat full  Δ LONG vs V0 demo  Δ LONG vs V0 full  e demo  e full  d demo  d full\nV0_frozen            0.664            0.743           0.746           0.742              0.000              0.000   0.056   0.140   0.410   0.490\n  c_exact            0.547            0.672           0.651           0.689             -0.117             -0.070   0.000   0.018   0.744   0.722\n       V1            0.685            0.739           0.762           0.729              0.021             -0.003   0.185   0.343   0.231   0.174\n       V2            0.682            0.750           0.760           0.752              0.018              0.008   0.056   0.137   0.410   0.483\n       V3            0.704            0.750           0.777           0.737              0.041              0.007   0.111   0.303   0.231   0.186\n       V4            0.649            0.751           0.735           0.758             -0.015              0.009   0.056   0.126   0.410   0.457\n       V5            0.788            0.746           0.840           0.735              0.125              0.003   0.056   0.240   0.205   0.240\n\nDecision (demo subset, n=93): V5   | stability: {'V5': 1.0}   | null any-qualifies: 0.200\nDecision (full run, n=2672):       NONE: V0 stands   | stability: {'NONE: V0 stands': 0.876, 'V4': 0.118, 'V3': 0.002, 'V5': 0.004}   | null any-qualifies: 0.035\n\n--- cell 28: <Figure size 1300x460 with 2 Axes>", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [48] THINKING · 2026-09-24 19:39:32 UTC

```
The notebook runs cleanly, with recomputed scores matching the sealed ones exactly (0/93 mismatches, max deviation ≤3e-17). Next I'll add an honest interpretation cell and scale the config.
```

### [49] TOOL CALL — Bash · 2026-09-24 19:39:32 UTC

```
python3 - <<'EOF'
p='tools/make_notebook.py'
s=open(p).read()
s=s.replace('''main(["--stage", "A,B,GGB,C,OUT,TEST"])
""")''','''main(["--stage", "A,B,GGB,C,OUT,TEST"])
print("(dry run: RUN_SCRIPTS = False, no src/ script was executed; sections 2-7 reproduce the core of stage A + GG gate g3 inline)")
""")''')
s=s.replace('''nb = {"cells": cells''','''md(r"""
### Reading the results

* **The scoring reproduces exactly.** Recomputing V0_rep, c_exact and V1–V5 from the pairwise matrix gives the sealed
  full-run scores to machine precision, and V0_rep equals frozen V0 (gate G1). All of these scores are label-free.
* **The e/d trade-off also shows on the subset.** Plurality normalisation (V1, V3, V5) lowers the false-alarm rate `d`
  but raises error endorsement `e`, or leaves it unchanged. `c_exact` (no aligner) endorses almost nothing but flags most
  correct rows. GG has the lowest `e` in the full run but a higher `d`. That trade-off is why no variant cleanly fixes V0.
* **Do not read the demo's decision as a result.** With 12 sentences, one variant can clear the +0.015 margin by chance.
  The permutation null on the subset shows this directly: with random labels, some variant "qualifies" far more often than
  the full run's 3.5%. The pre-registered decision on the full development set is **"NONE: V0 stands"**, and all E
  numbers are development numbers.
""")

nb = {"cells": cells''')
open(p,'w').write(s)
EOF
python3 tools/make_notebook.py '{"B": 200, "B_STAB": 50, "B_NULL": 20}' && time .nb_env/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -3
```

### [50] TOOL RESULT — Bash · 2026-09-24 19:40:38 UTC

```
{"stdout": "wrote /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_EU1yuNrRl4od/code_demo.ipynb 30 cells\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m A new release of pip is available: \u001b[0m\u001b[31;49m25.0.1\u001b[0m\u001b[39;49m -> \u001b[0m\u001b[32;49m26.2.1\u001b[0m\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m To update, run: \u001b[0m\u001b[32;49mpython3.12 -m pip install --upgrade pip\u001b[0m\n[NbConvertApp] Writing 179252 bytes to code_demo.ipynb\n\nreal\t1m4.482s\nuser\t0m7.633s\nsys\t0m0.905s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [51] ASSISTANT · 2026-09-24 19:40:38 UTC

```
Status: the scale-up round with B=200/50/20 passed in 64 s (mostly the pip check). Now trying the original values, 2000/500/200.
```

### [52] TOOL CALL — Bash · 2026-09-24 19:40:38 UTC

```
python3 tools/make_notebook.py '{"B": 2000, "B_STAB": 500, "B_NULL": 200}' && time .nb_env/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -2; python3 - <<'EOF'
import json
nb=json.load(open('code_demo.ipynb'))
for i,c in enumerate(nb['cells']):
    if c['cell_type']!='code' or i<19: continue
    for o in c['outputs']:
        if o['output_type']=='stream': print(i, ''.join(o['text'])[-1500:])
        elif o['output_type']=='error': print('ERROR', o['ename'], o['evalue'])
        elif 'image/png' in o.get('data',{}): print(i,'PNG')
EOF
```

### [53] TOOL RESULT — Bash · 2026-09-24 19:40:38 UTC

```
{"stdout": "wrote /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_EU1yuNrRl4od/code_demo.ipynb 30 cells\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m To update, run: \u001b[0m\u001b[32;49mpython3.12 -m pip install --upgrade pip\u001b[0m\n[NbConvertApp] Writing 179361 bytes to code_demo.ipynb\n\nreal\t0m55.895s\nuser\t0m15.146s\nsys\t0m0.962s\n19 19:39:19|INFO   |repro {\"c_exact_pooled_auroc_Z\": 0.7571225071225072, \"target_c_exact\": 0.748, \"c3_plain_pooled_auroc_Z\": 0.8779677113010447, \"target_c3_eval2_c_k3_best_oof\": 0.784520131776288, \"V0_frozen_pooled_Z\": 0.8321462488129154, \"V0_rep_pooled_Z\": 0.8321462488129154, \"n_V5_imputed_neutral_in_Z\": 4}\n\n19 19:39:21|INFO   |ALL-strat: V0_frozen=0.7460 V0_rep=0.7460 c_exact=0.6508 V1=0.7619 V2=0.7596 V3=0.7766 V4=0.7347 V5=0.8401\n\n19 19:39:21|INFO   |pooled: V0_frozen=0.8321 V0_rep=0.8321 c_exact=0.7571 V1=0.8184 V2=0.8364 V3=0.8435 V4=0.8120 V5=0.8870\n\n19 19:39:22|INFO   |LONG-strat: V0_frozen=0.6637 V0_rep=0.6637 c_exact=0.5465 V1=0.6847 V2=0.6817 V3=0.7042 V4=0.6486 V5=0.7883\n\n19 19:39:22|INFO   |L25: V0_frozen=0.4412 V0_rep=0.4412 c_exact=0.4412 V1=0.4412 V2=0.4412 V3=0.4412 V4=0.5588 V5=0.6078\n\n19 19:39:22|INFO   |L20: V0_frozen=0.6771 V0_rep=0.6771 c_exact=0.3333 V1=0.6406 V2=0.7292 V3=0.7083 V4=0.5000 V5=0.8229\n\n19 19:39:23|INFO   |EXC: V0_frozen=0.8222 V0_rep=0.8222 c_exact=0.7778 V1=0.9000 V2=0.8296 V3=0.9000 V4=0.8222 V5=0.9000\n\n19 19:39:23|INFO   |CTRL: V0_frozen=1.0000 V0_rep=1.0000 c_exact=0.9722 V1=1.0000 V2=1.0000 V3=1.0000 V4=1.0000 V5=1.0000\n\n21 19:39:23|INFO   |screen done 3.5s\n\n21     score     d     e\nV0_frozen 0.410 0.056\n   V0_rep 0.410 0.056\n  c_exact 0.744 0.000\n       V1 0.231 0.185\n       V2 0.410 0.056\n       V3 0.231 0.111\n       V4 0.410 0.056\n       V5 0.205 0.056\n\n21 /tmp/ipykernel_492/409019122.py:35: RuntimeWarning: invalid value encountered in divide\n  eb = (Wf[:, m] @ en.astype(float)) / Wf[:, m].sum(1)\n\n24 19:39:23|INFO   |DECISION: V5; {\"V1\": 0.021, \"V2\": 0.018, \"V3\": 0.0405, \"V4\": -0.015, \"V5\": 0.1246}\n\n24 19:39:23|INFO   |stability {'V5': 0.858, 'V3': 0.088, 'NONE: V0 stands': 0.014, 'V1': 0.014, 'V2': 0.026}\n\n24 19:39:25|INFO   |null {'B': 200, 'share_any_variant_qualifies': 0.35, 'share_per_variant': {'V1': 0.09, 'V2': 0.115, 'V3': 0.07, 'V4': 0.03, 'V5': 0.17}, 'note': 'within-stratum label permutation of Z; V4 re-cross-fitted on each permuted label vector'}\n\n26 g3 (demo subset): {'pass': False, 'gg': 0.6395, 'V0': 0.746, 'delta': -0.1066, 'delta_ci': [-0.3412119856887299, -0.008711324300821928]}\nGG e=0.056 d=0.487 | V0 e=0.056 d=0.410\nfull run g3: {'pass': False, 'gg': 0.6964364733668502, 'V0': 0.7421654662067422, 'delta_ci': [-0.0708974380922907, -0.021226381894754013]}\n\n28     score  LONG-strat demo  LONG-strat full  ALL-strat demo  ALL-strat full  Δ LONG vs V0 demo  Δ LONG vs V0 full  e demo  e full  d demo  d full\nV0_frozen            0.664            0.743           0.746           0.742              0.000              0.000   0.056   0.140   0.410   0.490\n  c_exact            0.547            0.672           0.651           0.689             -0.117             -0.070   0.000   0.018   0.744   0.722\n       V1            0.685            0.739           0.762           0.729              0.021             -0.003   0.185   0.343   0.231   0.174\n       V2            0.682            0.750           0.760           0.752              0.018              0.008   0.056   0.137   0.410   0.483\n       V3            0.704            0.750           0.777           0.737              0.041              0.007   0.111   0.303   0.231   0.186\n       V4            0.649            0.751           0.735           0.758             -0.015              0.009   0.056   0.126   0.410   0.457\n       V5            0.788            0.746           0.840           0.735              0.125              0.003   0.056   0.240   0.205   0.240\n\nDecision (demo subset, n=93): V5   | stability: {'V5': 0.858, 'V3': 0.088, 'NONE: V0 stands': 0.014, 'V1': 0.014, 'V2': 0.026}   | null any-qualifies: 0.350\nDecision (full run, n=2672):       NONE: V0 stands   | stability: {'NONE: V0 stands': 0.876, 'V4': 0.118, 'V3': 0.002, 'V5': 0.004}   | null any-qualifies: 0.035\n\n28 PNG", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [54] TOOL CALL — Bash · 2026-09-24 19:41:34 UTC

```
python3 -c "
import json,base64
nb=json.load(open('code_demo.ipynb'))
for c in nb['cells']:
  for o in c.get('outputs',[]):
    if 'image/png' in o.get('data',{}): open('/tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-EU1yuNrRl4od/908df641-116b-490e-b0c2-adb76bc47178/scratchpad/fig.png','wb').write(base64.b64decode(o['data']['image/png']))
"; grep -c 'GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/main/round-5/experiment-14/demo/mini_demo_data.json"' code_demo.ipynb; ls -la
```

### [55] TOOL RESULT — Bash · 2026-09-24 19:41:34 UTC

```
{"stdout": "0\ntotal 8107\ndrwxr-xr-x 5 root root 2063129 Sep 24 19:32 .\ndrwxr-xr-x 4 root root 2063142 Sep 24 19:37 ..\ndrwxr-xr-x 2 root root   20400 Sep 24 19:32 .aii\n-rw------- 1 root root      54 Sep 24 19:17 .aii_claude_session.json\ndrwxr-xr-x 7 root root 2063020 Sep 24 19:23 .nb_env\n-rw-r--r-- 1 root root  718493 Sep 24 19:39 .repl_agent.ptylog\n-rw-r--r-- 1 root root    2828 Sep 24 19:32 README.md\n-rw-r--r-- 1 root root  179411 Sep 24 19:39 code_demo.ipynb\n-rw-r--r-- 1 root root  182720 Sep 24 19:19 mini_demo_data.json\ndrwxr-xr-x 2 root root 1005596 Sep 24 19:22 tools", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [56] TOOL CALL — Read · 2026-09-24 19:41:34 UTC

```
/tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-EU1yuNrRl4od/908df641-116b-490e-b0c2-adb76bc47178/scratchpad/fig.png
```

### [57] TOOL RESULT — Read · 2026-09-24 19:41:34 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [58] TOOL CALL — Bash · 2026-09-24 19:41:34 UTC

```
sed -i 's/ax\[0\].legend(fontsize=8, loc="lower right")/ax[0].legend(fontsize=8, loc="upper left")/; s/ax\[0\].set_ylim(0.4, 1.0)/ax[0].set_ylim(0.4, 1.12)/' tools/make_notebook.py && python3 tools/make_notebook.py '{"B": 2000, "B_STAB": 500, "B_NULL": 200}' && time .nb_env/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -1; python3 -c "
import json
nb=json.load(open('code_demo.ipynb'))
src=''.join(''.join(c['source']) for c in nb['cells'])
print('url ok', 'GITHUB_DATA_URL = \"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/main/round-5/experiment-14/demo/mini_demo_data.json\"' in src)
print('errors', sum(o['output_type']=='error' for c in nb['cells'] for o in c.get('outputs',[])))
print('png', sum('image/png' in o.get('data',{}) for c in nb['cells'] for o in c.get('outputs',[])))
"
```

### [59] TOOL RESULT — Bash · 2026-09-24 19:41:34 UTC

```
{"stdout": "wrote /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_EU1yuNrRl4od/code_demo.ipynb 30 cells\n[NbConvertApp] Writing 176553 bytes to code_demo.ipynb\n\nreal\t1m0.680s\nuser\t0m15.414s\nsys\t0m0.996s\nurl ok True\nerrors 0\npng 1", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [60] ASSISTANT · 2026-09-24 19:41:34 UTC

```
Everything passes. Now removing the test env, then finalising the manifest and the output JSON.
```

### [61] TOOL CALL — Bash · 2026-09-24 19:41:34 UTC

```
rm -rf .nb_env && cat > .aii/manifest.yaml <<'EOF'
# Nothing heavy remains: the test virtualenv (.nb_env/) was deleted after testing; every remaining file is small text/JSON.
entries: []
EOF
python3 - <<'EOF'
p='README.md'
s=open(p).read()
s=s.replace("`.nb_env/` is the throwaway test virtualenv. It is deleted after the round. Recreate it with:",
            "Nothing was removed except `.nb_env/`, the throwaway test virtualenv, which was deleted after testing. Recreate it with:")
open(p,'w').write(s)
EOF
echo '{"out_expected_files": {"notebook": "code_demo.ipynb", "mini_data_file": "mini_demo_data.json"}}' > .terminal_claude_agent_struct_out.json; cat .terminal_claude_agent_struct_out.json; du -sh .
```

### [62] TOOL RESULT — Bash · 2026-09-24 19:41:34 UTC

```
{"stdout": "{\"out_expected_files\": {\"notebook\": \"code_demo.ipynb\", \"mini_data_file\": \"mini_demo_data.json\"}}\n4.0M\t.", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [63] ASSISTANT · 2026-09-24 19:41:47 UTC

```
I've built the demo notebook and its data file. On a small subset the notebook picks a different winner (V5) than the full run's "NONE: V0 stands". The notebook explains this as small-sample noise and prints the full-run result beside it. It runs clean from an empty Python 3.12 environment in about 60 s at the full original settings, well under the 10-minute limit, with no errors.

**What the notebook does**
- `method.py` itself only launches about 25 other scripts, and those need the whole run's input files. So the notebook keeps its step list and loop but only prints the plan (a `RUN_SCRIPTS = False` switch; nothing is executed).
- The core of the experiment then runs inline, using the original functions unedited: the frozen scorers, the statistics, the label join, the screen and the selection rule. Stages:
  1. Scores V0, `c_exact` and V1–V5 from the saved pairwise equivalence data, with no labels.
  2. Joins the labels and computes AUROC per stratum, with bootstrap intervals and paired differences against V0.
  3. Computes false alarms (`d`) against missed errors (`e`).
  4. Applies the pre-registered rule, plus the stability and permutation-null checks.
  5. Checks gate g3 for GG.
  6. Ends with a demo-vs-full-run table and two plots.
- The only code changes are notebook-context ones: data comes from the loaded file instead of disk paths, file writes and the log file are dropped, and two things that need all 2,672 rows are omitted (a row-count assertion and the oracle bound, which needs labelled data for all 700 sentences).

**Results**
- **Scores reproduce exactly.** The recomputed scores match the saved ones to within about 3e-17, with 0/93 mismatches on the V0 reproduction check.
- **The subset's winner is noise.** On 93 rows, V5 wins. With shuffled labels, some variant qualifies 35% of the time on the subset, against 3.5% on the full run.
- **The trade-off shows even on the subset.** V1, V3 and V5 lower false alarms but let more errors through or leave that rate unchanged. `c_exact` lets almost no errors through but flags most correct rows. GG fails g3 on the subset (0.640 vs V0's 0.746), as it did on the full run.

**Settings:** the notebook ships with the original values: 2000 bootstrap replicates, 500 stability resamples and 200 permutations. It got there in one scaling round (20/10/5 → 200/50/20 → originals). Most of the runtime is package installation.

**Data:** `mini_demo_data.json` (183 KB) holds 93 labelled rows: 12 whole sentences covering all four strata, 54 wrong and 39 correct candidates. It also carries those sentences' equivalence data, the full run's family weights and V4 coefficients, and the full-run reference numbers. The notebook uses the exact `GITHUB_DATA_URL` requested, with a local-file fallback.

My todo-tracking tool wasn't available, so the six TODOs weren't entered as a list, but each one was carried out. The test environment `.nb_env/` has been deleted, so the manifest has no entries; the README says how to recreate it. The output JSON is written.

Files are in the workspace:
- `code_demo.ipynb`
- `mini_demo_data.json`
- `README.md`
- `.aii/manifest.yaml`
- `.terminal_claude_agent_struct_out.json`
- `tools/build_mini_demo_data.py`
- `tools/make_notebook.py`
```
