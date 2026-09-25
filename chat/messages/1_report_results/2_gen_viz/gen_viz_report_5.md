# gen_viz_report_5 — report_results

> Phase: `gen_paper_repo` · `gen_viz`
> Run: `gen_paper_repo_a2e1d024cc16` — Cross-Family Solver Consensus as a Gold-Free Faithfulness Metric for Logic Translation
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_viz_report_5` (terminal_claude_agent, claude-opus-5-5)

### [1] CONFIG · 2026-09-25 15:55:02 UTC

```
model: claude-opus-5-5 | effort: high | permission: bypassPermissions
```

### [2] SYSTEM-USER prompt · 2026-09-25 15:55:10 UTC

````
<research_methodology>
Create figures that belong in a top-venue paper.

- Every figure needs a clear takeaway visible at a glance.
- Choose chart types that match the data relationship (comparisons, trends, correlations, distributions).
- Include uncertainty (error bars, confidence intervals) when showing experimental results.
- Keep it clean — no clutter, clear labels with units, readable at print size.
</research_methodology>

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
Your workspace: `/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_report_5`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_report_5/`:
GOOD: `/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_report_5/file.py`, `/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_report_5/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
<disposable_outputs>
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

<task>
Render a publication-quality DATA figure for a top-tier venue research paper.

This figure plots numbers, so it is RENDERED from those numbers — not drawn by an image model. Use the aii-data-fig-gen skill. The output is deterministic: run it once, look at it, fix the spec if the data or labels are wrong, run it again.

STEPS:
1. Read the skill: `.claude/skills/aii-data-fig-gen/SKILL.md`.
2. Pick the chart type that fits the specification below. `python <skill>/scripts/chart_gen.py --list-types` lists them; `--example <type>` prints a complete spec to copy.
3. Write your spec to `fig_dev_set_auroc_spec.json` in your workspace. Put EVERY numeric value from the specification into it — the spec is the figure.
4. Render it:
   `python <skill>/scripts/chart_gen.py --spec fig_dev_set_auroc_spec.json --out fig_dev_set_auroc_v0`
   That writes `fig_dev_set_auroc_v0.pdf` (the deliverable, vector) and `fig_dev_set_auroc_v0.png` (for you to look at).
5. READ THE PNG BACK and check it against the checklist below.
6. If anything is wrong, edit the spec and re-render. Repeat until clean — this is cheap and deterministic, so there is no attempt limit and no reason to accept a flawed figure.

DELIVERABLE: `fig_dev_set_auroc_v0.pdf` in your workspace root. Leave `fig_dev_set_auroc_spec.json` there too — it is the figure's source, and the step files it next to the figure so the figure stays reproducible.

Verification checklist (after EVERY render) — these are the things only you can check, because they are about whether the figure says what you meant:
- Every number in the figure matches the specification — no invented or dropped values
- Axis labels state what is measured AND its units
- Axis ranges make the comparison readable rather than flattening it
- The chart type still makes the point once you can see it drawn
- The caption you return describes what is actually drawn (see <caption_from_the_rendered_figure>)

The generator already REFUSES the rest rather than shipping them, so a figure you can read back cannot have them: overlapping or cut-off labels, a legend covering the data, a series drawn without a name beside named ones, two series a reader cannot tell apart, and a fit or a scale that the data cannot support. When it exits non-zero the message names the exact key, index or label and what to change — do that rather than re-rolling.

Reach for a generator first, and hand-write only if none fits. Every type in `--list-types` already carries the house style, the data-integrity checks and the layout fixes, so using one is less work than plotting by hand and the result matches every other figure in the paper.

If nothing in the catalogue fits, writing matplotlib yourself is expected and supported — novel figures exist. When you do, import the house style AND its layout passes so the figure still belongs to the set — `apply_house_style`, `place_legend`, `place_point_label`, `fit_legends`, `clear_legends_of_data`, `fit_tick_labels`, `fit_titles`, `rasterize_dense_clouds`, `assert_legends_clear_of_data`, `assert_series_are_distinguishable`, `assert_axis_names_are_unique` from `chart_style`, and `fit_point_labels` + `assert_text_is_legible` from `chart_geometry`, the last of which raises if any label ends up printed over another or cut off at the edge. Build legends with `place_legend` and point names with `place_point_label` — a legend made with a bare `ax.legend` cannot be reflowed when it turns out too wide, and a name written with a bare `ax.annotate` will not be moved off the marker it landed on. The "Use a generator when one fits" section of SKILL.md has the exact snippet and the order to call them in. What you lose is the automatic checking that the picture agrees with the numbers, so verify every value yourself against the specification.
</task>

<figure_specification>
Figure ID: fig_dev_set_auroc
Title: Development Set E AUROCs
Caption: AUROC on development dataset E under R_AB labels. PEER+TEXT leads across all subsets, with the largest advantage on long exception sentences.
Data and chart description: Grouped bar chart. X-axis: seven data subsets (R_AB pooled, R_AB L25, R_AB L20, R_AB EXC, R_AB CTRL, R_AB long pool, R_A L20+EXC). Y-axis: AUROC (0.4 to 0.95). Six bars per group for metrics: PEER+TEXT, c_score_align, NF c_score, L2-bow, L3, Local judge. Values for R_AB pooled: 0.790, 0.782, 0.743, 0.734, 0.579, 0.712. Values for R_A L20+EXC: 0.818, 0.860, 0.802, 0.678, 0.587, 0.554. Error bars showing 95% CI. Colors: PEER+TEXT red, c_score blue, NF green, L2-bow orange, L3 purple, judge grey. White background, sans-serif font.
Aspect Ratio: 16:9
Summary: PEER+TEXT leads on development set E; consensus advantage is largest on long, complex, exception-clause sentences.
</figure_specification>


<evidence_check>
CRITICAL — this run's own final audit says its headline result is NOT supported:
the final review is marked blocking; the final hypothesis update recorded evidence_state='lead' — a lead, not yet a finding: real but too small, too confounded or seen on too little evidence to headline. The figure specification above was written from a paper draft
that may therefore quote numbers no run ever produced.

Before you plot ANY number, find the artifact output file it is supposed to come from
and read the value there. Plot only values you have read back from an artifact output
file. If a value in the specification above is not in any results file — or the results
file holds far fewer examples, methods or conditions than the specification implies —
do NOT invent it and do NOT carry it over: draw only the series the data actually
supports, and say what the figure covers in its caption.

A figure whose bars disagree with the run's own output files is worse than a missing
figure, because nothing downstream can detect it.
</evidence_check>


<comparison_completeness>
If this figure's title, caption or summary names specific checkpoints, models or
variants being COMPARED — "ours vs baseline", "the base and the abliterated model",
"across the three checkpoints" — every one of them named there MUST appear in the
rendered figure as its own bar, curve, point or panel. Before you render, list every
comparator the specification names and check each one off as you draw it. A
comparison figure that quietly drops one of its own named comparators is wrong even
when every bar it does draw is numerically correct — the missing one is invisible to
anyone who was not told to look for it, which is what makes it worse than an
obviously incomplete figure.
</comparison_completeness>


<caption_from_the_rendered_figure>
The caption in <figure_specification> is a DRAFT, written before this figure existed by a step
that never saw it. After your final render, read the final image back and write the figure's
caption into the `caption` field of your output. It replaces the draft caption everywhere this
figure appears: the paper, the report and the paper's website.
- Describe what the image actually shows: what each axis measures, what each colour, marker or
  line style encodes, and what each panel plots, using the image's own labels.
- Name a colour, marker, panel or series only if it is in the image. Where the draft caption and
  the image disagree (colours said to encode models when they encode languages, an axis the panel
  does not plot, a grey series that was never drawn), the image wins.
- Keep what is still true of the draft: the data, the sample size, what the error bars are, and
  the takeaway. Keep it LaTeX-ready in the same form as the draft caption.
- State no number the figure and its data do not carry.
</caption_from_the_rendered_figure>


---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "VizExpectedFiles": {
      "description": "Expected output files from viz generation.",
      "properties": {
        "image_path": {
          "description": "Path to the generated figure image file. Example: 'fig1_v0.jpg'",
          "title": "Image Path",
          "type": "string"
        }
      },
      "required": [
        "image_path"
      ],
      "title": "VizExpectedFiles",
      "type": "object"
    }
  },
  "description": "Structured output from viz figure generation agent.",
  "properties": {
    "title": {
      "description": "Figure title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance. Aim for about 4-8 words (~40 characters).",
      "maxLength": 90,
      "minLength": 12,
      "title": "Title",
      "type": "string"
    },
    "summary": {
      "description": "Brief summary of the generated figure: what it shows, style, any issues fixed",
      "maxLength": 5000,
      "minLength": 500,
      "title": "Summary",
      "type": "string"
    },
    "caption": {
      "description": "The figure's caption, written from the FINAL rendered image after you read it back, in the same LaTeX-ready form as the draft caption. It replaces the draft caption in the paper, the report and the paper's website. Name only axes, colours, markers, panels and series that are in the image, with what each one encodes there.",
      "maxLength": 2000,
      "minLength": 20,
      "title": "Caption",
      "type": "string"
    },
    "out_expected_files": {
      "$ref": "#/$defs/VizExpectedFiles",
      "description": "Output file you created. Must include the generated figure image path."
    }
  },
  "required": [
    "title",
    "summary",
    "caption",
    "out_expected_files"
  ],
  "title": "VizFigureOutput",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [3] HUMAN-USER prompt · 2026-09-25 15:55:10 UTC

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

### [4] TOOL CALL — Bash · 2026-09-25 15:55:14 UTC

```
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_report_5; ls -la; ls .aii; ls .claude/skills 2>/dev/null; ls ../..; ls ../../..
```

### [5] TOOL RESULT — Bash · 2026-09-25 15:55:14 UTC

```
{"stdout": "total 2950\ndrwxr-xr-x  3 root root 1001430 Sep 25 15:55 .\ndrwxr-xr-x 14 root root 2003228 Sep 25 15:54 ..\ndrwxr-xr-x  2 root root       1 Sep 25 15:54 .aii\n-rw-------  1 root root      54 Sep 25 15:55 .aii_claude_session.json\n-rw-r--r--  1 root root   22750 Sep 25 15:55 .repl_agent.ptylog\n_1_gh_repo\n_2_gen_paper_draft\n_3_gen_viz\n4_gen_paper_repo\nlogs\nsinks\nuser_uploads", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [6] TOOL CALL — Bash · 2026-09-25 15:55:16 UTC

```
find / -path /proc -prune -o -type d -name aii-data-fig-gen -print 2>/dev/null | head; cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ; ls 4_gen_paper_repo/_1_gh_repo 4_gen_paper_repo/_2_gen_paper_draft; ls -d */ ; 
```

### [7] TOOL RESULT — Bash · 2026-09-25 15:57:16 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false, "backgroundTaskId": "boj1vjm0n", "timedOutAfterMs": 120000, "backgroundCwdHint": "Session cwd remains /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_report_5; directory changes made by the backgrounded command do not apply to subsequent commands."}
```

### [8] TOOL CALL — Bash · 2026-09-25 15:57:20 UTC

```
ls ~/.claude/skills 2>/dev/null | head -50; ls /root/.claude/skills/aii-data-fig-gen 2>/dev/null; cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ; ls; ls 4_gen_paper_repo/_1_gh_repo | head; ls 4_gen_paper_repo/_2_gen_paper_draft | head
```

### [9] TOOL RESULT — Bash · 2026-09-25 15:57:20 UTC

```
{"stdout": "4_gen_paper_repo\nlogs\nsinks\nuser_uploads\nrepo_info.json\nrun_record\nworkspace", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_report_5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [10] TOOL CALL — Bash · 2026-09-25 15:57:24 UTC

```
cat /tmp/claude-0/-ai-inventor-aii-data-runs-run-An1uy2kF2SjZ-4-gen-paper-repo--3-gen-viz-gen-viz-report-5/1a3861f0-0ae8-486c-a93d-77bc93db1721/tasks/boj1vjm0n.output; cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo; cat _1_gh_repo/repo_info.json | head -30; ls _1_gh_repo/workspace | head; ls _2_gen_paper_draft/run_record _2_gen_paper_draft/workspace 2>/dev/null| head; ls _2_gen_paper_draft
```

### [11] TOOL RESULT — Bash · 2026-09-25 15:57:24 UTC

```
{"stdout": "{\n  \"repo_name\": \"ai-invention-eff060-layered-gold-free-checks-for-logic\",\n  \"repo_url\": \"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic\",\n  \"repo_owner\": \"ai-inventor-papers\",\n  \"error\": null,\n  \"description\": \"THE METRIC (headline deliverable). A three-layer, gold-free check, FOL-Triage(text, fol). It returns P(unfaithful), the layer that fired and an error-type code. It is built around where REAL NL->FOL e\",\n  \"branch\": \"fork/run_An1uy2kF2SjZ\",\n  \"base_branch\": \"\",\n  \"metadata\": {\n    \"generated_at\": \"2026-09-25T14:39:15.088953+00:00\",\n    \"module\": \"gen_repo\",\n    \"llm_provider\": \"gh_cli\",\n    \"output_dir\": \"/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo\"\n  }\n}ls: cannot access '_1_gh_repo/workspace': No such file or directory\n_2_gen_paper_draft/run_record:\niteration_records.yaml\nrun_report.yaml\n\n_2_gen_paper_draft/workspace:\nREADME.md\npaper_draft.md\nreferences.bib\nreferences.json\nrun_record\nworkspace", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_report_5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [12] TOOL CALL — Bash · 2026-09-25 15:57:26 UTC

```
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ; ls 4_gen_paper_repo/_1_gh_repo/run_record; ls 4_gen_paper_repo/; ls 4_gen_paper_repo/_3_gen_viz; ls ..| head; grep -n -i "development\|dataset E\|R_AB\|PEER" 4_gen_paper_repo/_2_gen_paper_draft/workspace/paper_draft.md | head -60
```

### [13] TOOL RESULT — Bash · 2026-09-25 15:57:26 UTC

```
{"stdout": "ls: cannot access '4_gen_paper_repo/_1_gh_repo/run_record': No such file or directory\n_1_gh_repo\n_2_gen_paper_draft\n_3_gen_viz\nfigures\ngen_viz_1\ngen_viz_2\ngen_viz_3\ngen_viz_4\ngen_viz_5\ngen_viz_6\ngen_viz_report_1\ngen_viz_report_2\ngen_viz_report_3\ngen_viz_report_4\ngen_viz_report_5\ngen_viz_results.json\n004e5\n073fa\n13291\n13536\n164d4\n24b46\n28068\n348df\n4a015\n5b0b4\n5:Evaluating whether a candidate first-order logic (FOL) formula faithfully captures its source sentence is difficult without a gold reference: correct formalisations are not unique, gold annotations are scarce, and existing metrics either require a reference formula or only verify that the output parses. We propose cross-family solver consensus, a gold-free metric that scores each candidate by the fraction of independent LLM families whose translations are not Z3-equivalent to it. On a pre-registered, held-out test of 2,686 real NL-to-FOL candidates from nine generator families, consensus achieves a stratified AUROC of 0.741 against a disguised cheap LLM judge at 0.642, a pre-registered and confirmed advantage of +0.099 [0.049, 0.146]. On templated long sentences with a shared symbol vocabulary, the advantage widens to +0.367 [0.328, 0.404] (within-template AUROC 0.954 vs 0.587). Consensus requires no gold formula, no ontology, and no domain knowledge; three peer families suffice for 97% of the full pool's discriminative power at a marginal cost below $0.001 per candidate. Its principal limitation is vocabulary dependence: candidates using different predicate names than their peers are penalised regardless of correctness, and every vocabulary bridge tested raises the error endorsement rate. We release the evaluation code, the labelled meta-evaluation sets, and the reusable metric library.\n13:We observe that when multiple independent LLM families translate the same sentence, their translations tend to agree (in the sense of Z3 equivalence) when they are correct and to scatter when at least one is wrong. This observation motivates cross-family solver consensus: score each candidate by the fraction of independently generated peer translations that are Z3-equivalent to it, after vocabulary alignment. A candidate that most peers agree with is likely faithful; one that no peer reproduces is likely erroneous.\n17:- We define cross-family solver consensus, a gold-free, domain-agnostic faithfulness metric for NL-to-FOL that requires only a sentence and a set of peer translations. On a pre-registered held-out test (dataset E, 2,686 candidates, 292 sentences), consensus achieves stratified AUROC 0.741 versus 0.642 for the best cheap LLM judge, a confirmed advantage of +0.099 [0.049, 0.146] (Section 5). [ARTIFACT:gen_art_experiment_6]\n19:- We construct two labelled meta-evaluation sets totalling over 13,000 items: dataset E (8,507 real candidates from nine LLM families on 700 sentences, labelled by Z3 equivalence to audited gold with panel adjudication) and a perturbation suite (4,234 typed mutants plus 868 meaning-preserving controls), enabling per-error-type sensitivity and invariance analysis (Section 4). [ARTIFACT:gen_art_dataset_1]\n20:- We show that three peer families suffice for 97% of the full pool's discriminative power, identify consensus's blind spot (38% of errors endorsed by the majority) and its vocabulary dependence (rename false-alarm rate of 0.76), and demonstrate that every tested vocabulary bridge raises error endorsement (Section 5, Section 6). [ARTIFACT:gen_art_evaluation_2] [ARTIFACT:gen_art_experiment_8]\n32:**Cross-model agreement for formal outputs.** The closest prior work uses cross-model agreement for formal languages. Bayless et al. [17] check NL-to-SMT translations from multiple LLMs, scoring each by the fraction of peers whose output entails it (the same score form as our consensus metric), but they evaluate on a fixed schema with downstream QA labels rather than per-candidate faithfulness. Alvanaki et al. [18] apply cross-model formal consensus to RTL (hardware description language), reporting precision at coverage thresholds for different numbers of agreeing models. Singh et al. [19] train a generative verifier for NL-to-FOL autoformalization, achieving AUROC 0.961 on Z3-reference labels; however, this verifier degrades when labels switch from solver equivalence to human intent. Wang et al. [20] apply selective conformal prediction with self-consistency to NL-to-temporal-logic, finding that self-consistency AUROC rises with problem difficulty. None of these works reports a meta-evaluation of cross-family consensus as a per-candidate NL-to-FOL faithfulness score against an LLM judge, nested over the baseline stack.\n42:**Step 1: Peer generation.** Collect translations of $s$ from $k$ LLM families, each family producing one translation at temperature 0 with a standardised few-shot prompt. The families must be architecturally independent (different pre-training data, different organisations). In our experiments we use nine families: GPT-4, GPT-3.5, Llama-3.3-70B, Qwen3-235B, DeepSeek-V3.1, Mistral-Small-3.2, Gemini-2.5-Flash-Lite, GPT-4.1-Mini, and the three Logic-LM released systems.\n44:**Step 2: Pairwise equivalence.** For each peer translation $p_i$, check Z3 equivalence between $c$ and $p_i$ modulo vocabulary alignment. The vocabulary aligner maps predicate names in $p_i$ to those in $c$ by string similarity (normalised Levenshtein distance on lowercased names with matching arity), then checks Z3 equivalence under the best injective mapping. Two formulas are equivalent modulo vocabulary (eqmv) when there exists an injective, arity-preserving symbol map under which Z3 confirms logical equivalence.\n50:where eqmv denotes equivalence modulo vocabulary. Higher scores indicate greater disagreement with the peer pool, predicting error. The candidate itself is excluded from the pool (leave-one-out when the candidate is one of the generated translations).\n56:Rather than binary majority voting, we use the graded consensus score, which preserves the continuous fraction of disagreeing peers. This outperforms binary majority by a stratified AUROC margin of +0.114 [0.091, 0.140] on dataset E [ARTIFACT:gen_art_evaluation_2], because partial agreement carries information that a binary threshold discards.\n60:To complement the consensus signal with text-level checks, we define a fused metric (PEER+TEXT) that combines the consensus score with two text-only features: (i) a bag-of-words coverage score measuring overlap between text content words and formula predicates, and (ii) a role-questionnaire score in which a small LLM reads the sentence and Z3 reads the formula, and their structured answers are compared [ARTIFACT:gen_art_experiment_1]. The fusion weights are fitted by logistic regression on a development screen and frozen before the held-out evaluation.\n64:### 4.1 Development Screen\n66:The development screen uses Logic-LM [1] released outputs on FOLIO validation: three LLM systems (GPT-3.5-turbo, GPT-4, text-davinci-003) producing 796 items. Labels are assigned by Z3 equivalence to corrected gold formulas [5]. The screen is dominated by short sentences (93% under 12 words). [ARTIFACT:gen_art_experiment_3] [ARTIFACT:gen_art_experiment_4]\n68:### 4.2 Held-Out Test Set (Dataset E)\n70:Dataset E contains 8,507 real NL-to-FOL candidates for 700 sentences drawn from FOLIO training premises and MALLS training data, with strata enriched for long sentences (25+ words, 3+ conditions) and exception clauses [ARTIFACT:gen_art_dataset_1]. Ten generator slots across nine LLM families produce candidates at temperature 0 with few-shot prompts. Labels combine Z3 equivalence to audited gold with a blind, nonce-disguised, family-disjoint adjudication panel (Claude Haiku-4.5, GLM-4.6, Kimi-K2). The primary analysis population (tiers A and B) contains 2,686 scorable items (1,822 ERROR, 864 CORRECT) across 292 sentences. Bootstrapping clusters by sentence to account for within-sentence dependence.\n93:The held-out evaluation was pre-registered before any score on dataset E was computed. The pre-registration specifies the primary population (R_AB, tiers A+B), the stratified bootstrap procedure (B = 2,000, clustered by sentence), and the confirmatory criterion: the CI of the stratified AUROC difference between consensus and the disguised cheap judge must exclude zero. [ARTIFACT:gen_art_experiment_6]\n99:Table 1 presents the pre-registered held-out results on dataset E (R_AB, 2,686 items, 1,822 ERROR, 864 CORRECT, 292 sentences).\n104:| PEER+TEXT fusion | 0.753 | 0.790 | [0.714, 0.788] |\n129:On the perturbation suite (4,234 mutants + 868 controls, within-base design), consensus achieves within-base AUROC 0.866 compared to 0.680 for the disguised judge, 0.666 for SC-5, 0.659 for bag-of-words coverage, and approximately 0.50 for structural pilot metrics [ARTIFACT:gen_art_experiment_8]. The PEER+TEXT fusion reaches 0.948. Consensus is symmetric across polarity (DOWN and UP edits detected equally), while local judges and embedding-based round-trip miss DOWN-polarity edits by 0.12 to 0.15 AUROC.\n133:### 5.4 How Many Peer Families Are Needed?\n135:The discriminative power of consensus saturates rapidly with the number of peer families. On dataset E (2,014 items with all seven non-candidate families available), pooled AUROC rises from 0.685 (one family) through 0.757 (three families) to 0.784 (seven families) [ARTIFACT:gen_art_evaluation_2]. Three families capture 97% of the full pool's AUROC. The cross-fitted best three-family pool (DeepSeek, Microsoft, OpenAI) achieves 0.785, matching the full pool. No single family carries the signal: the maximum leave-one-family-out AUROC drop is 0.005.\n141:The consensus metric works because correct and erroneous translations exhibit different agreement patterns. On dataset E, the mean pairwise agreement rate among translations of the same sentence is 0.760 for correct candidates and 0.159 for erroneous ones (a 4.8x scatter ratio) [ARTIFACT:gen_art_evaluation_2]. Errors produced by different families are correlated (they tend to co-occur on the same sentences) but structurally diverse (they rarely produce the same wrong formula), while correct translations converge on the same logical content despite different surface forms.\n145:### 5.6 Development-Screen Results\n147:On the initial development screen (546 items, 249 ERROR, 297 CORRECT), consensus achieves AUROC 0.866 [0.821, 0.906] versus SC-5 at 0.725 [0.669, 0.781], a paired delta of +0.140 [0.085, 0.197] [ARTIFACT:gen_art_experiment_3]. On a vocabulary-controlled subset (shared-aligner confound removed), consensus achieves 0.852 versus SC at 0.714. The development-screen AUROC is higher than the held-out AUROC (0.782 pooled on E versus 0.866 on the screen), reflecting the screen's simpler, shorter sentences.\n151:**Structural pilot metrics.** The user's pilot structural metrics (joint conflict, arity inconsistency, shape inconsistency, dangling predicates) achieve AUROC 0.500 to 0.533 on the development screen, indistinguishable from chance [ARTIFACT:gen_art_experiment_4]. Only the cross-system predicate-set Jaccard (0.720) shows signal, and it is a proxy for the consensus approach.\n157:**Candidate-Signature Consensus.** Giving peers the candidate's own symbol list lowers correct-candidate divergence (d = 0.139 vs 0.323 for free peers) but raises error endorsement (e = 0.459 vs 0.173), producing a net AUROC of 0.614 versus 0.770 for free peers. Anchoring the peers to the candidate's vocabulary causes them to copy its errors [ARTIFACT:gen_art_experiment_9].\n163:The principal limitation of consensus is vocabulary dependence. Two formulas with different predicate names are not Z3-equivalent under any identity map, so a candidate using a synonym or a different decomposition than its peers is penalised regardless of correctness. On dataset E, the rename false-alarm rate is 0.76 (nonce renames) [ARTIFACT:gen_art_experiment_8]. Every vocabulary bridge tested, including name-free alignment, hybrid matching, and gloss-gated checking, raises the error endorsement rate while lowering divergence, producing no net AUROC gain [ARTIFACT:gen_art_experiment_14]. The Gloss-Gated checker failed its development gate (all-stratum AUROC 0.696 vs 0.742 for plain alignment). This tradeoff between divergence and endorsement appears fundamental when the vocabulary is unconstrained.\n169:Consensus cannot detect errors that all peers reproduce. On dataset E, 38% of errors are endorsed by the majority. Endorsed errors are predominantly structural (57%) rather than polarity-related (5%) or coverage-related (41%). Text-level checks detect some endorsed errors that consensus misses, but the PEER+TEXT fusion does not significantly outperform consensus alone on the held-out test (stratified delta +0.011, not significant). [ARTIFACT:gen_art_experiment_5]\n173:The disguised-judge comparison controls for LLM memorisation of public benchmark data. Flash-lite contamination difference-in-differences on dataset E is +0.105 [0.006, 0.201], suggesting a small memorisation benefit for the judge on some items [ARTIFACT:gen_art_experiment_6]. Consensus, which uses only Z3 equivalence, is structurally immune to memorisation.\n175:On the development screen, judges are highly sensitive to meaning-preserving rewrites: the flip rate under contrapositive rewriting is 0.41 to 0.95 for judges versus 0.0 for consensus [ARTIFACT:gen_art_experiment_4]. Consensus is invariant to any rewrite that preserves Z3 equivalence but not to vocabulary changes.\n179:Consensus's AUROC depends on the label protocol. Under solver-only labels (development screen), consensus achieves 0.866; under panel-adjudicated labels (dataset E, tiers A+B), the stratified AUROC is 0.741 [ARTIFACT:gen_art_evaluation_1]. The drop is partly explained by the panel's stricter standard (it rejects 82% of MALLS gold formulas) and by instrument sharing between the consensus aligner and the solver labeller. [ARTIFACT:gen_art_evaluation_1]\n185:1. **Vocabulary dependence.** Consensus penalises correct translations that use different predicate names than their peers. The nonce-rename false-alarm rate is 0.76. Every vocabulary bridge tested trades divergence for endorsement with no net gain.\n187:2. **Error endorsement ceiling.** 38% of errors are endorsed by the majority of peers. Consensus cannot detect these, placing a hard ceiling on recall.\n191:4. **Budget-stopped confirmations.** The E2-A and E2-B fresh-sample confirmations were budget-stopped before reaching testability on the long-sentence stratum. The R_COMP FREE confirmation was not testable because the gloss gate failed. The only fully confirmed results are on dataset E (held-out but developed during the same run) and R_COMP SIG (templated, shared vocabulary).\n195:6. **Panel strictness.** The adjudication panel accepts only 61% of expert-corrected formulas, so ERROR is over-called in dataset E. This inflates the AUROC of metrics that are sensitive to vocabulary-granularity differences.\n199:Cross-family solver consensus is a practical gold-free faithfulness metric for NL-to-FOL translation. On a pre-registered held-out test, it outperforms the best cheap LLM judge by +0.099 [0.049, 0.146] stratified AUROC, and on long sentences with controlled vocabulary it reaches 0.954. The method costs under $0.001 per candidate with three peer families, is domain-agnostic, and is structurally immune to memorisation. Its vocabulary dependence is the central unsolved problem: when candidate and peers use different predicate names, consensus penalises correct translations and endorses vocabulary-matched errors. Standardising the symbol vocabulary in generation prompts removes this limitation. Future work should develop vocabulary-robust equivalence checks that do not trade divergence for endorsement, and extend the evaluation to richer formal languages where solver-based equivalence remains tractable.", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_report_5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [14] ASSISTANT · 2026-09-25 15:57:30 UTC

```
I'm tracing each number in the figure spec back to the run's own result files before I plot anything.
```

### [15] TOOL CALL — Bash · 2026-09-25 15:57:30 UTC

```
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo; sed -n 95,130p _2_gen_paper_draft/workspace/paper_draft.md; ls _1_gh_repo; ls _3_gen_viz/figures _3_gen_viz/gen_viz_report_4
```

### [16] TOOL RESULT — Bash · 2026-09-25 15:57:30 UTC

```
{"stdout": "## 5 Results\n\n### 5.1 Main Results\n\nTable 1 presents the pre-registered held-out results on dataset E (R_AB, 2,686 items, 1,822 ERROR, 864 CORRECT, 292 sentences).\n\n| Metric | Strat. AUROC | Pooled AUROC | 95% CI (strat.) |\n|---|---|---|---|\n| Cross-family consensus | 0.741 | 0.782 | [0.708, 0.773] |\n| PEER+TEXT fusion | 0.753 | 0.790 | [0.714, 0.788] |\n| Disguised cheap judge | 0.642 | 0.696 | [0.598, 0.687] |\n| Original cheap judge | 0.623 | 0.635 | [0.575, 0.670] |\n| Best cheap judge (nano) | 0.652 | -- | -- |\n| S4 baseline stack | 0.704 | 0.759 | -- |\n| Local Qwen3-8B judge | 0.669 | 0.712 | -- |\n\n[ARTIFACT:gen_art_experiment_6]\n\n**Headline result.** Consensus outperforms the disguised cheap judge by a stratified AUROC difference of +0.099 [0.049, 0.146] (pre-registered and confirmed; p < 0.001 by one-sided bootstrap). [ARTIFACT:gen_art_experiment_6] On the long-sentence pool (2,300 items from L25, L20, and EXC strata), the advantage widens to +0.116 [0.070, 0.163]. On the L20+EXC tier-A subset (449 items with trusted gold references), the advantage is +0.299 [0.212, 0.390].\n\n**Nested gain over baseline stack.** Consensus adds information beyond the full cheap-baseline stack: the nested AUROC gain of adding consensus to S4 is +0.039 [0.021, 0.057] (stratified), with a permutation-null 95th percentile of 0.009. Consensus alone approximately equals the full S4 stack (+0.006 [-0.031, 0.042]). [ARTIFACT:gen_art_experiment_6]\n\n**Frontier judge comparison.** On the 284-row frontier-judge frame, consensus achieves an AUROC ratio of 0.957 [0.887, 1.034] relative to the frontier (Gemini 3.1 Pro Preview), at 30x lower cost per item ($0.00012 vs $0.00365). Adding consensus to the frontier judge raises its AUROC by +0.037 [0.008, 0.066]. [ARTIFACT:gen_art_experiment_6]\n\n[FIGURE:fig_main_results]\n\n### 5.2 Long Sentences with Shared Vocabulary\n\nOn R_COMP SIG (1,904 candidates from 220 sentences, 395 ERROR, 1,509 CORRECT), where generators share a symbol signature, consensus achieves within-template AUROC 0.954 [0.939, 0.968] versus the disguised judge at 0.587 [0.551, 0.622], a confirmed delta of +0.367 [0.328, 0.404] [ARTIFACT:gen_art_experiment_7]. The judge adds nothing over consensus: the nested gain of adding the judge to consensus is approximately zero, while adding consensus to the judge gives +0.377.\n\nOn a 60-row frontier subsample, consensus achieves 0.956 versus the frontier judge at 0.932 (original text) and 0.735 (disguised). Consensus and the frontier judge are comparable when vocabulary is controlled.\n\n### 5.3 Perturbation Sensitivity\n\nOn the perturbation suite (4,234 mutants + 868 controls, within-base design), consensus achieves within-base AUROC 0.866 compared to 0.680 for the disguised judge, 0.666 for SC-5, 0.659 for bag-of-words coverage, and approximately 0.50 for structural pilot metrics [ARTIFACT:gen_art_experiment_8]. The PEER+TEXT fusion reaches 0.948. Consensus is symmetric across polarity (DOWN and UP edits detected equally), while local judges and embedding-based round-trip miss DOWN-polarity edits by 0.12 to 0.15 AUROC.\n\nrepo_info.json\n_3_gen_viz/figures:\npaper\nreport\n\n_3_gen_viz/gen_viz_report_4:", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_report_5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [17] TOOL CALL — Bash · 2026-09-25 15:57:34 UTC

```
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ; ls sinks user_uploads logs | head -30; timeout 60 find . -maxdepth 4 -type d | grep -v "_3_gen_viz" | head -50
```

### [18] TOOL RESULT — Bash · 2026-09-25 15:57:34 UTC

```
{"stdout": "logs:\norchestrator.log\n\nsinks:\nevents\notel\n\nuser_uploads:\n.\n./.shared_cache\n./.shared_cache/uv\n./.shared_cache/uv/interpreter-v4\n./.shared_cache/uv/interpreter-v4/8b63bc5b2cef0cd1\n./.shared_cache/uv/sdists-v9\n./.shared_cache/hf\n./.shared_cache/hf/hub\n./4_gen_paper_repo\n./4_gen_paper_repo/_2_gen_paper_draft\n./4_gen_paper_repo/_2_gen_paper_draft/run_record\n./4_gen_paper_repo/_2_gen_paper_draft/workspace\n./4_gen_paper_repo/_2_gen_paper_draft/workspace/.aii\n./4_gen_paper_repo/_1_gh_repo\n./sinks\n./sinks/otel\n./sinks/events\n./user_uploads\n./logs", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_report_5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [19] TOOL CALL — Bash · 2026-09-25 15:57:38 UTC

```
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ; ls -la 4_gen_paper_repo/_2_gen_paper_draft/run_record 4_gen_paper_repo/_2_gen_paper_draft/workspace; grep -o '/[^ "]*gen_art_experiment_6[^ "]*' -r logs 4_gen_paper_repo/_2_gen_paper_draft/run_record 2>/dev/null | sort -u | head; grep -o '"[^"]*aii-data-fig-gen[^"]*"' -r logs | sort -u | head
```

### [20] TOOL RESULT — Bash · 2026-09-25 15:57:38 UTC

```
{"stdout": "4_gen_paper_repo/_2_gen_paper_draft/run_record:\ntotal 3291\ndrwxr-xr-x 2 root root 1032747 Sep 25 14:39 .\ndrwxr-xr-x 4 root root 2000198 Sep 25 14:39 ..\n-rw-r--r-- 1 root root  198552 Sep 25 15:06 iteration_records.yaml\n-rw-r--r-- 1 root root  136783 Sep 25 15:06 run_report.yaml\n\n4_gen_paper_repo/_2_gen_paper_draft/workspace:\ntotal 5626\ndrwxr-xr-x 3 root root 2000166 Sep 25 15:39 .\ndrwxr-xr-x 4 root root 2000198 Sep 25 14:39 ..\ndrwxr-xr-x 2 root root   15500 Sep 25 15:39 .aii\n-rw------- 1 root root      54 Sep 25 15:06 .aii_claude_session.json\n-rw-r--r-- 1 root root 1642045 Sep 25 15:39 .repl_agent.ptylog\n-rw-r--r-- 1 root root   48755 Sep 25 15:38 .terminal_claude_agent_struct_out.json\n-rw-r--r-- 1 root root    1547 Sep 25 15:39 README.md\n-rw-r--r-- 1 root root   29600 Sep 25 15:18 paper_draft.md\n-rw-r--r-- 1 root root   10155 Sep 25 15:11 references.bib\n-rw-r--r-- 1 root root    9718 Sep 25 15:11 references.json", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_report_5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [21] TOOL CALL — Bash · 2026-09-25 15:57:42 UTC

```
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_2_gen_paper_draft/run_record; head -c 3000 run_report.yaml; echo; grep -n "R_A L20\|L20+EXC\|0\.818\|0\.860\|0\.802\|long pool\|R_AB_L25\|L25" run_report.yaml iteration_records.yaml | head -40
```

### [22] TOOL RESULT — Bash · 2026-09-25 15:57:42 UTC

```
{"stdout": "title: Gold-Free Faithfulness Metrics for NL-to-FOL Translation\nabstract: >-\n  We investigate gold-free metrics that predict whether a candidate first-order logic formula faithfully captures the meaning\n  of its source natural language sentence, without requiring a reference formula. Cross-family solver consensus, which checks\n  z3 equivalence of translations produced by independent LLM families, achieves stratified AUROC 0.742 on a development set,\n  beating the best cheap LLM judge by +0.099. On long composed sentences with trusted references, consensus reaches within-template\n  AUROC 0.954. Three peer families suffice for 97% of full-pool performance. Over five iterations, confirmation was attempted\n  on three fronts and all were budget-stopped before reaching testability. One testable cell (ProverQA-derived sentences with\n  trusted gold) yielded V0 strat AUROC 0.916, but the long-sentence stratum collapsed to 0.443 (near chance). Provisional\n  results on R_COMP FREE (non-confirmatory) show consensus AUROC 0.801 vs judge 0.584. No consensus variant V1-V5 improved\n  on V0. The rename tradeoff remains unsolved: every vocabulary bridge that lowers divergence also raises error endorsement.\n  The Gloss-Gated name-free checker failed its development gate. Candidate-Signature Consensus (CSC) was a provisional negative\n  due to anchoring. The fundamental limitation is that useful peer agreement requires a shared vocabulary from outside the\n  candidate being evaluated.\npaper_text: |\n  # Gold-Free Faithfulness Metrics for NL-to-FOL Translation\n\n  ## Framing\n\n  Translating natural language into first-order logic (NL-FOL) is a prerequisite for neurosymbolic reasoning pipelines [10], yet evaluating whether a candidate formula faithfully captures a sentence's meaning remains an open problem. Gold FOL annotations are expensive, non-unique, and unreliable: Brunello et al. [3] found that approximately 42% of entries in both FOLIO [1] and MALLS [2] contain incorrect formalisations. Existing metrics either require a gold formula (exact match, prover-checked equivalence) or only verify that the output parses [5, 6]. The user's own pilot study used structural consistency checks (arity agreement, predicate-set overlap across reruns, joint satisfiability) that measure stability but not whether a formula says what its sentence says.\n\n  This run investigates gold-free metrics that predict faithfulness to the text given only a sentence and a candidate formula, with no reference formula, no ontology, and no domain knowledge. The evaluation is a meta-evaluation: we build a labelled set of (sentence, formula) pairs from public benchmarks whose gold has been audited, and measure each metric's ability to discriminate correct translations from errors.\n\n  ## Iteration 1\n\n  ### 1.1 Strategy\n\n  The iteration screens four candidate metric families head-to-head on a frozen evaluation set, with a disguised cheap LLM judge as the bar to beat.\n\n  **Candidates.** (A) FOL-Triage, a th\nrun_report.yaml:268:  | judge_strong_orig (gemini-3.1-pro) | 0.802 | [0.715, 0.877] |\nrun_report.yaml:289:  The strong judge (Gemini 3.1 Pro Preview) achieves AUROC 0.802 [0.715, 0.877] on the strong subsample (n = 291). Under disguise it drops to 0.730 [0.655, 0.803]. The ΔAUROC over the cheap judge is +0.024 [−0.075, 0.111], not significant under solver labels. Under panel labels the frontier-judge advantage strengthens to +0.166 [+0.086, +0.244] (p < 0.001, n = 90; see §2.5 item 5).\nrun_report.yaml:340:  | 2-op errors | 11 | 0.545 | 0.818 | 0.727 | 0.273 |\nrun_report.yaml:437:  | R_AB L25 | 873 (697/176) | 0.755 [0.70, 0.80] | 0.712 [0.65, 0.77] | 0.651 [0.59, 0.71] | 0.722 [0.67, 0.77] | 0.560 [0.49, 0.63] | 0.664 |\nrun_report.yaml:441:  | R_AB long pool | 2300 (1673/627) | 0.768 [0.74, 0.80] | 0.759 [0.72, 0.79] | 0.704 [0.67, 0.74] | 0.717 [0.69, 0.75] | 0.580 [0.54, 0.62] | 0.653 |\nrun_report.yaml:442:  | R_A pooled L20+EXC | 449 (261/188) | 0.818 [0.73, 0.88] | 0.860 [0.79, 0.92] | 0.802 [0.72, 0.87] | 0.678 [0.61, 0.74] | 0.587 [0.51, 0.66] | 0.554 |\nrun_report.yaml:448:  The paired ΔAUROC of PEER+TEXT minus the local judge is +0.078 [0.043, 0.112] on R_AB pooled (DeLong p < 0.0001). On the long pool (L25+L20+EXC), the gap widens to +0.115 [0.075, 0.157]. On R_A (tier-A adjudicated labels, L20+EXC), the gap is +0.264 [0.157, 0.359].\nrun_report.yaml:454:  The stratified AUROC (pairing only within complexity strata, removing the composition confound) shows PEER+TEXT at 0.753 and c_score_align at 0.741, a difference of +0.011 [−0.012, 0.038], not significant. On the long pool the stratified gap is +0.016 [−0.010, 0.041]. On R_A the gap is −0.036 [−0.113, 0.030], favouring c_score_align. The TEXT layers add no significant discriminative power over c_score_align alone once the stratum-composition confound is removed.\nrun_report.yaml:579:  1. PEER+TEXT achieves AUROC 0.790 [0.75, 0.82] on the development dataset E (R_AB pooled, n = 2686), beating the local judge by +0.078 [0.043, 0.112] (DeLong p < 0.0001). On long sentences (L25+L20+EXC, n = 2300) the gap widens to +0.115 [0.075, 0.157]. The flash-lite judge bar is UNTESTABLE due to API key exhaustion (only 20 rows scored).\nrun_report.yaml:620:  The best system-level tracker is S4_local (all tiers): Kendall τ-b = 0.615 [0.513, 0.770] over 13 system × variant rows. Over 11 families: τ-b = 0.709 [0.600, 0.818].\nrun_report.yaml:703:  | R_AB long (L25+L20+EXC) | 1673/627 | c_score_align | +0.116 [+0.070, +0.163] |\nrun_report.yaml:704:  | R_AB long (L25+L20+EXC) | 1673/627 | p_peer_text | +0.132 [+0.091, +0.173] |\nrun_report.yaml:707:  | R_A L20+EXC | 261/188 | c_score_align | +0.299 [+0.212, +0.390] |\nrun_report.yaml:708:  | R_A L20+EXC | 261/188 | p_peer_text | +0.264 [+0.180, +0.351] |\nrun_report.yaml:721:  | S4_full + c_score_align | 0.807 [0.772, 0.838] | 0.774 [0.743, 0.802] |\nrun_report.yaml:761:  | S4_full_oof | 0.745 [0.688, 0.797] | 0.768 [0.714, 0.818] |\nrun_report.yaml:927:  | REV | 179 | 0.860 | 0.869 | 0.826 | 0.578 | 0.697 |\nrun_report.yaml:928:  | QUANT | 179 | 0.860 | 0.872 | 0.829 | 0.351 | 0.632 |\nrun_report.yaml:932:  | ADD | 472 | 0.859 | 0.860 | 0.820 | 0.895 | 0.683 |\nrun_report.yaml:1006:  | PEER+TEXT − S4_local | R_A L20+EXC (n=447) | +0.096 [+0.009, +0.175] | +0.099 [+0.006, +0.176] |\nrun_report.yaml:1047:  Pre-registered gates (verbatim from `prereg_csc_E.json`): G1: \"d(c_csc > 0.5 | R_AB CORRECT) ≤ 0.35 AND the words slope of GEE d ~ z(words) + z(n_conditions) among CORRECT rows has CI including 0 or entirely < 0\". G2: \"stratified AUROC(CSC) ≥ stratified AUROC(c_score_align) − 0.01 on R_AB AND pooled AUROC(CSC) > AUROC(c_score_align) on L25 (point estimates; the L25 paired CI is reported whatever its sign)\". G3-E: \"FA(c > 0.5) on RENAME_SYN CORRECT rows ≤ base FA (same rows, CSC-OWN) + 0.05 (point estimate; CI reported); NONCE reported as the stress boundary, not gated\". G5: \"FULL cost per candidate (sum of its peer calls, dedup-apportioned) ≤ $0.002\".\nrun_report.yaml:1106:  | G2 (strat AUROC(CSC) ≥ c_score_align − 0.01 on R_AB AND pooled AUROC(CSC) > c_score_align on L25) | **NOT_READ** (R_AB part FAIL; L25 below readable cell size, Δ −0.067 [−0.183, 0.040]) |\nrun_report.yaml:1110:  CSC is a provisional negative on a completion-selected subset; L25 and RENAME are untested. The mechanism is clear: sharing the candidate's vocabulary helps correct candidates converge (reducing d) but also helps incorrect candidates recruit agreement (raising e). The anchoring effect dominates.\nrun_report.yaml:1202:  E2 is a fresh 550-sentence confirmation set (350 L25, 100 EXC, 100 DT) constructed from MALLS-train and ProverQA-dev, disjoint from E by hash exclusion and 12-gram filtering. The sentence selection and reference freezing are complete; the LLM candidate generation and panel labelling are not.\nrun_report.yaml:1206:  **Testability: NONE.** All confirmation cells have zero CORRECT rows. The pilot rows are a pipeline smoke test, not confirmation data. Projected cost to complete: $6.79. Projected MDE80 at 350 L25 sentences: 0.112 (ΔAUROC).\nrun_report.yaml:1278:  L25 yield (fraction of sentences with both ERROR and CORRECT candidates): 0.37. Detecting the observed T1 delta (+0.069 strat AUROC for L25) at 80% power requires ~326 usable L25 sentences, i.e. ~882 planned sentences. E2's 350 L25 sentences give MDE80 ≈ 0.112. The iteration-3 plan's claim that ~400 L25 sentences suffice to detect +0.08 is incorrect (needs ~690).\nrun_report.yaml:1288:  1. **CSC is a provisional negative on a completion-selected subset (T6-E).** Candidate-Signature Consensus lowers correct-row divergence (d: 0.139 vs 0.323 for FREE) but raises error endorsement (e: 0.459 vs 0.173). Strat AUROC 0.614 is below all established metrics and below the flash-lite judge (0.664). CSC adds no signal to S4_full (+0.006 [−0.013, +0.025]). Gates G1 and G2 fail; L25 and RENAME are untested. The mechanism is clear: sharing the candidate's vocabulary anchors peers into reproducing the candidate's errors, especially for MEANING_RENAME (e_CSC = 0.821 vs e_FREE = 0.036) and ADD errors (e_CSC = 0.490 vs e_FREE = 0.135).\nrun_report.yaml:1300:  7. **T8 vocabulary analysis.** SIG-vs-FREE agreement drop: 0.479 [0.447, 0.513]. The Part-1 d_floor model closely matches observed d (0.402 predicted vs 0.415 observed) but is NOT VALIDATED against FREE data (calibration error −0.372). L25 MDE80 at 350 sentences: 0.112 (the plan's ~400-sentence claim is wrong; needs ~690).\nrun_report.yaml:1315:  | CSC (Candidate-Signature Consensus) | 4 | Provisional negative: strat AUROC 0.614, anchoring e = 0.459 (gates G1, G2 fail; L25, RENAME untested) |\nrun_report.yaml:1331:  E2-A is the untouched portion of the E2 confirmation set (dataset 4): 110 sentences (37 L25, 37 EXC, 36 DT) with labels joined after both seal hashes matched. The run-wide budget stopped generation at $2.05, so only the DT stratum (ProverQA-derived, trusted gold) and a fraction of L25/EXC completed labelling. API spend: included in dataset 4.\nrun_report.yaml:1342:  | p_peer_text | 0.919 [0.860, 0.976] |\nrun_report.yaml:1349:  #### Long pool (L25 + EXC, not testable)\nrun_report.yaml:1351:  The long pool has 94 rows (76 ERROR / 18 CORRECT, 12 sentences): not testable. V0 strat AUROC 0.603 [0.463, 0.735]. L25 alone (42 rows, 7 CORRECT): V0 strat AUROC 0.443 [0.375, 0.500], near chance. The consensus metric fails on E2's L25 stratum.\nrun_report.yaml:1371:  Carried variant: NONE — V0 stands. No variant V1–V5 met the pre-registered selection rule (highest LONG-strat AUROC beating V0 by ≥ +0.015 AND ≥ V0 on L25 AND ≥ V0 − 0.01 on CTRL). The best candidate was V2 (reliability-weighted) at +0.0075 LONG-strat, below the +0.015 threshold.\nrun_report.yaml:1445:  Kendall τ: c_score_align 0.697 [0.364, 0.818] vs judge_cheap_disg 0.333 [0.061, 0.576] (12 systems). Consensus tracks system error rates on R_COMP FREE.\nrun_report.yaml:1467:  | Score | ALL-strat | LONG-strat | L25 | CTRL |\nrun_report.yaml:1484:  **GG development gate g3: FAIL.** GG strat AUROC on E = 0.696 [0.659, 0.733] vs V0 0.742, Δ = −0.046 [−0.071, −0.021]. The gate requires GG ≥ V0 − 0.01; it fails by 0.036. GG's e/d decomposition: e = 0.081, d = 0.629 (ALL); on L25: e = 0.022, d = 0.960. GG has very low endorsement (good) but very high divergence (bad): the gloss gate rejects too many legitimate predicate mappings, fragmenting the consensus pool.\nrun_report.yaml:1502:  7. **CSC is provisional negative**, not dead end (L25 and RENAME untested).\nrun_report.yaml:1516:  3. **L25 on E2 is near chance.** V0 strat AUROC 0.443 on E2-A L25 (42 rows, 7 CORRECT, 6 sentences). The consensus metric collapses on the long-sentence confirmation stratum that matters most.\nrun_report.yaml:1552:  Iteration 5 attempted confirmation on three fronts, and all three were blocked by the run-wide budget ($7.00). E2-A produced one testable cell: V0 reaches 0.916 on ProverQA-derived sentences with trusted gold, but only 0.443 on the L25 long-sentence stratum (near chance). E2-B's exploratory results (V0 0.737 vs flash-lite 0.496, Δ +0.208) favour consensus on long sentences with unaudited labels, but the label-coupling diagnostic shows part of the advantage comes from shared gold-equivalent peers. R_COMP FREE's provisional results show c_align 0.801 vs judge 0.584 (Δ +0.217) under ERROR_CERT vs MAPPED labels, with consensus carrying most of the signal in nesting tests.", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_report_5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [23] TOOL CALL — Bash · 2026-09-25 15:57:44 UTC

```
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_2_gen_paper_draft/run_record; sed -n 420,460p run_report.yaml
```

### [24] TOOL RESULT — Bash · 2026-09-25 15:57:44 UTC

```
{"stdout": "  ### 2.2 Experiment 5: PEER+TEXT on development dataset E\n\n  [ARTIFACT:art_TaxJRnPcJMuZ]\n\n  PEER+TEXT is a logistic fusion of the consensus signal (c_score with shared-vocabulary alignment, denoted c_score_align) and the text-based FOL-Triage layers (L2-bow, L3 questionnaire). The fusion weights were fitted on the iteration-1 screen and frozen before any E score was computed (prereg sha256 b9f28b1bf6bf). API spend was $0 (all components ran on CPU and the local GPU; no OpenRouter calls completed).\n\n  #### Name-free alignment: failed the pre-registered screen gate\n\n  A name-free variant of the consensus metric (graded clause consensus, g_score) was pre-registered as the primary PEER signal. It matches formula clauses by structural role without relying on shared predicate names, using anchored-cost assignment and Murty k-best matching. Under the pre-registered selection rule, both name-free variants (NF-pure and NF-anchored) failed the screen gate: for both, more than 10% of AGREE track-L CORRECT items tie at g = 1, making the deterministic false-alarm threshold degenerate (ROLE_PERMUTE recall = 0).\n\n  A post-hoc analysis with fractional tie-breaking showed this failure was a threshold-tie artefact. NF-anchored passes both gates under fractional scoring (RENAME FA 0.074, ROLE_PERMUTE recall 0.771); NF-pure still fails ROLE_PERMUTE (recall 0.186). The NF-anchored fusion was fitted post-hoc and applied to E as a labelled sensitivity analysis. On E (R_AB pooled), the NF-anchored fusion achieves AUROC 0.759 [0.72, 0.79], which is 0.031 below the pre-registered PEER+TEXT fusion (0.790), with the CI excluding zero [−0.042, −0.020]. The shared-aligner confound with the solver labeller remains open.\n\n  #### Headline AUROCs on E (R_AB, ERROR vs CORRECT)\n\n  | Subset | n (err/cor) | PEER+TEXT | c_score_align | NF c_score | L2-bow | L3 | Local judge |\n  |-|-|-|-|-|-|-|-|\n  | R_AB pooled | 2686 (1822/864) | 0.790 [0.75, 0.82] | 0.782 [0.74, 0.82] | 0.743 [0.70, 0.78] | 0.734 [0.71, 0.76] | 0.579 [0.53, 0.62] | 0.712 |\n  | R_AB L25 | 873 (697/176) | 0.755 [0.70, 0.80] | 0.712 [0.65, 0.77] | 0.651 [0.59, 0.71] | 0.722 [0.67, 0.77] | 0.560 [0.49, 0.63] | 0.664 |\n  | R_AB L20 | 821 (592/229) | 0.747 [0.69, 0.80] | 0.722 [0.66, 0.78] | 0.643 [0.58, 0.70] | 0.715 [0.66, 0.76] | 0.547 [0.48, 0.62] | 0.683 |\n  | R_AB EXC | 606 (384/222) | 0.777 [0.72, 0.83] | 0.814 [0.76, 0.86] | 0.782 [0.72, 0.84] | 0.669 [0.61, 0.72] | 0.620 [0.55, 0.69] | 0.663 |\n  | R_AB CTRL | 386 (149/237) | 0.708 [0.57, 0.84] | 0.742 [0.62, 0.86] | 0.741 [0.61, 0.86] | 0.613 [0.54, 0.72] | 0.490 [0.37, 0.62] | 0.739 |\n  | R_AB long pool | 2300 (1673/627) | 0.768 [0.74, 0.80] | 0.759 [0.72, 0.79] | 0.704 [0.67, 0.74] | 0.717 [0.69, 0.75] | 0.580 [0.54, 0.62] | 0.653 |\n  | R_A pooled L20+EXC | 449 (261/188) | 0.818 [0.73, 0.88] | 0.860 [0.79, 0.92] | 0.802 [0.72, 0.87] | 0.678 [0.61, 0.74] | 0.587 [0.51, 0.66] | 0.554 |\n\n  [FIGURE:fig_dev_set_auroc]\n\n  #### PEER+TEXT vs the local judge\n\n  The paired ΔAUROC of PEER+TEXT minus the local judge is +0.078 [0.043, 0.112] on R_AB pooled (DeLong p < 0.0001). On the long pool (L25+L20+EXC), the gap widens to +0.115 [0.075, 0.157]. On R_A (tier-A adjudicated labels, L20+EXC), the gap is +0.264 [0.157, 0.359].\n\n  The flash-lite judge comparison is untestable: only 20 items received flash-lite scores before the key was exhausted, yielding a ΔAUROC of +0.057 [−0.200, 0.360] (n = 20, uninformative).\n\n  #### Does fusion beat c_score_align alone?\n\n  The stratified AUROC (pairing only within complexity strata, removing the composition confound) shows PEER+TEXT at 0.753 and c_score_align at 0.741, a difference of +0.011 [−0.012, 0.038], not significant. On the long pool the stratified gap is +0.016 [−0.010, 0.041]. On R_A the gap is −0.036 [−0.113, 0.030], favouring c_score_align. The TEXT layers add no significant discriminative power over c_score_align alone once the stratum-composition confound is removed.\n\n  #### Mechanism predictions\n\n  Four pre-registered mechanism predictions were tested on E:\n\n  **P1 (PEER catches COVERAGE errors that TEXT misses, and vice versa).** At matched false-alarm rate 0.10 with fractional tie-breaking: PEER has higher recall than TEXT on COVERAGE errors (+0.093 [0.046, 0.147]), and TEXT has higher recall on PEER_ENDORSED errors (+0.103 [0.051, 0.171]). [Correction (C5): the recall values for the local judge (Qwen-8B disguised) at FA 0.10 on the endorsed groups are: PEER_ENDORSED 0.169, PEER_ENDORSED_NF 0.199. The local judge has the highest recall on both endorsed groups, not the TEXT layers. The original report omitted the judge column and conflated the two endorsed-group names.] The crossover exists, but the fused PEER+TEXT recall is not higher than c_score_align alone on any group except COVERAGE. Verdict: INCONCLUSIVE.", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_report_5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [25] TOOL CALL — Bash · 2026-09-25 15:57:48 UTC

```
ls /ai-inventor/aii_data | head; ls /ai-inventor | head; grep -n "art_TaxJRnPcJMuZ" /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_2_gen_paper_draft/run_record/*.yaml | head
```

### [26] TOOL RESULT — Bash · 2026-09-25 15:57:48 UTC

```
{"stdout": "_migration_20260827\n_preserved_runs\nbackups\nbundles\ncache\ncomp-ling-dobrovoljc\ncomp-ling-dobrovoljc_ala\ncomp-ling-dobrovoljc_exr\ncomp-ling-dobrovoljc_imd\ncomp-ling-dobrovoljc_iny\nCOMMIT_CHECKLIST.md\nLICENSE\nREADME.md\n_typos.toml\naii_config\naii_data\naii_launcher\naii_lib\naii_pipeline\naii_public\n/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_2_gen_paper_draft/run_record/run_report.yaml:422:  [ARTIFACT:art_TaxJRnPcJMuZ]", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [27] ASSISTANT · 2026-09-25 15:57:52 UTC

```
I found the spec's table in the run report. Now I'm looking for the underlying artifact output file so every value is checked against raw results.
```

### [28] TOOL CALL — Bash · 2026-09-25 15:57:52 UTC

```
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_2_gen_paper_draft/run_record; grep -n "TaxJRnPcJMuZ" -A3 -B3 iteration_records.yaml | head -60; timeout 60 grep -rl "TaxJRnPcJMuZ" /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/logs /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/sinks 2>/dev/null | head
```

### [29] TOOL RESULT — Bash · 2026-09-25 15:57:52 UTC

```
{"stdout": "/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/sinks/events/events_sequenced.jsonl\n/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/sinks/events/events.jsonl", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_report_5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [30] TOOL CALL — Bash · 2026-09-25 15:57:54 UTC

```
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/sinks/events; grep -o '[^"]\{0,200\}TaxJRnPcJMuZ[^"]\{0,200\}' events.jsonl | sort -u | head -20
```

### [31] TOOL RESULT — Bash · 2026-09-25 15:57:56 UTC

```
{"stdout": "ugrep: error: error at position 632\n-\\xbf]|\\xf4[\\x80-\\x8f][\\x80-\\xbf][\\x80-\\xbf]){0,200}\n                       exceeds complexity limits___/", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_report_5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [32] TOOL CALL — Bash · 2026-09-25 15:58:00 UTC

```
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/sinks/events; python3 - <<'EOF'
import re
s=open('events.jsonl',errors='ignore').read()
hits=set()
for m in re.finditer('TaxJRnPcJMuZ',s):
    hits.add(s[max(0,m.start()-250):m.end()+250].replace('\\n',' '))
for h in list(hits)[:12]: print(h,'\n----')
paths=set(re.findall(r'/[A-Za-z0-9_./-]*TaxJRnPcJMuZ[A-Za-z0-9_./-]*',s)); print(paths)
EOF
```

### [33] TOOL RESULT — Bash · 2026-09-25 15:58:00 UTC

```
{"stdout": "\":null,\"tool\":\"Bash\",\"tool_id\":\"toolu_01HgdW8GTB9WruauYXCaCJNU\",\"tool_kind\":\"terminal\",\"backend\":\"terminal_claude_agent\",\"model\":null,\"extras\":{\"input\":{\"command\":\"cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/sinks/events; grep -o '[^\\\"]\\\\{0,200\\\\}TaxJRnPcJMuZ[^\\\"]\\\\{0,200\\\\}' events.jsonl | sort -u | head -20\"}}}\n{\"node_id\":\"pod_runtime_cost_eec652881481\",\"path\":\"gen_viz_report_2_c53f66e92d4d/run_An1uy2kF2SjZ-phase-gen_paper_repo-mod-gen_viz-task-gen_viz_report_2/pod_runtime_cost[2]\",\"name\":\"\",\"parent_id \n----\n9bf575d7f5bc\",\"ancestor_ids\":[\"gen_viz_report_5_9bf575d7f5bc\"],\"status\":\"done\",\"start_at\":null,\"end_at\":\"2026-09-25T15:57:48.593643Z\",\"type\":\"agent_tool_call\",\"text\":\"Tool: Bash ls /ai-inventor/aii_data | head; ls /ai-inventor | head; grep -n \\\"art_TaxJRnPcJMuZ\\\" /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_2_gen_paper_draft/run_record/*.yaml | head\",\"summary\":\"\",\"task_id\":\"gen_viz_report_5_9bf575d7f5bc\",\"subagent_id\":null,\"subagent_tool_id\":null,\"subagent_model\":null,\"tool\":\"Bash\",\"tool_i \n----\n\",\"tool_id\":\"toolu_01Rf3Awivb9gxdBp8oB8eQ1L\",\"tool_kind\":\"terminal\",\"backend\":\"terminal_claude_agent\",\"model\":null,\"extras\":{\"input\":{\"command\":\"cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_2_gen_paper_draft/run_record; grep -n \\\"TaxJRnPcJMuZ\\\" -A3 -B3 iteration_records.yaml | head -60; timeout 60 grep -rl \\\"TaxJRnPcJMuZ\\\" /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/logs /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/sinks 2>/dev/null | head\"}}}\n{\"node_id\":\"i2fYqYFRfa-L\",\"path\":\"gen_viz_rep \n----\nent\",\"model\":null,\"extras\":{\"output\":{\"stdout\":\"art_2OmxzMInZZJY art_5KczEbsFPx25 art_7GxreYjATkC5 art_BvAL_KZTZuw8 art_D7k2ZWgE3nVd art_EU1yuNrRl4od art_FWy8D4_y9GBn art_HepAw8c6Eu7- art_Ia_FT284H33j art_REMRsYjY1N4s art_TWLKblwXVifE art_TaxJRnPcJMuZ art_U4Hsqt4Ay9Tg art_YYD-HDzfQfEj art_cxnoDYQNFolW art_d0njuqy2Csj- art_elDZY26Pu6GD art_i3cVDxBp-USk art_ngTPhaVyXxhh art_pAmLrGqsmFUx art_zcwCQgTqk6DN\",\"stderr\":\"\",\"interrupted\":false,\"isImage\":false,\"noOutputExpected\":false}}}\n{\"node_id\" \n----\nthe mapping. Let me create the key artifact ID mapping:  - Exp 1 (FOL-Triage) = art_d0njuqy2Csj- - Exp 3 (Consensus) = art_i3cVDxBp-USk - Exp 4 (Judges/baselines) = art_elDZY26Pu6GD - Dataset E = art_U4Hsqt4Ay9Tg - Exp 5 (PEER+TEXT on E) = art_TaxJRnPcJMuZ - Eval 1 = art_HepAw8c6Eu7- - Dataset 3 = art_zcwCQgTqk6DN - Exp 6 (T1 held-out) = art_7GxreYjATkC5 - Exp 7 (R_COMP) = art_cxnoDYQNFolW - Exp 8 (Rename+perturb) = art_YYD-HDzfQfEj - Eval 2 (mechanism) = art_FWy8D4_y9GBn - Research 1 = art_D7k \n----\n_viz_report_5_9bf575d7f5bc\"],\"status\":\"done\",\"start_at\":null,\"end_at\":\"2026-09-25T15:57:52.615200Z\",\"type\":\"agent_tool_call\",\"text\":\"Tool: Bash cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_2_gen_paper_draft/run_record; grep -n \\\"TaxJRnPcJMuZ\\\" -A3 -B3 iteration_records.yaml | head -60; timeout 60 grep -rl \\\"TaxJRnPcJMuZ\\\" /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/logs /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/sinks 2>/dev/null | head\",\"summary\":\"\",\"task_id\":\"gen_viz_report_5_9bf575d \n----\n\"subagent_model\":null,\"tool\":\"Bash\",\"tool_id\":\"toolu_01TFNmfALuNUnDX6VVu6oLLt\",\"tool_kind\":\"terminal\",\"backend\":\"terminal_claude_agent\",\"model\":null,\"extras\":{\"input\":{\"command\":\"ls /ai-inventor/aii_data | head; ls /ai-inventor | head; grep -n \\\"art_TaxJRnPcJMuZ\\\" /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_2_gen_paper_draft/run_record/*.yaml | head\"}}}\n{\"node_id\":\"ceUljxujv2eu\",\"path\":\"gen_viz_report_5_9bf575d7f5bc/agent_tool_result[10]\",\"name\":\"\",\"parent_id\":\"gen_viz_report_5_9bf575d7f5b \n----\nviz_report_5_9bf575d7f5bc\"],\"status\":\"done\",\"start_at\":null,\"end_at\":\"2026-09-25T15:57:44.582420Z\",\"type\":\"agent_tool_result\",\"text\":\"Tool: Bash Result: {\\\"stdout\\\": \\\"  ### 2.2 Experiment 5: PEER+TEXT on development dataset E\\ \\   [ARTIFACT:art_TaxJRnPcJMuZ]\\ \\   PEER+TEXT is a logistic fusion of the consensus signal (c_score with shared-vocabulary alignment, denoted c_score_align) and the text-based FOL-Triage layers (L2-bow, L3 questionnaire). The fusion weights were fitted on the iteration-1 scree \n----\nLIST.md\\ LICENSE\\ README.md\\ _typos.toml\\ aii_config\\ aii_data\\ aii_launcher\\ aii_lib\\ aii_pipeline\\ aii_public\\ /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_2_gen_paper_draft/run_record/run_report.yaml:422:  [ARTIFACT:art_TaxJRnPcJMuZ]\\\", \\\"stderr\\\": \\\"\\\", \\\"interrupted\\\": false, \\\"isImage\\\": false, \\\"noOutputExpected\\\": false}\",\"summary\":\"\",\"task_id\":\"gen_viz_report_5_9bf575d7f5bc\",\"subagent_id\":null,\"subagent_tool_id\":null,\"subagent_model\":null,\"tool\":\"Bash\",\"tool_id\":\"toolu_01 \n----\nerminal_claude_agent\",\"model\":null,\"extras\":{\"input\":{\"command\":\"cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_2_gen_paper_draft/run_record; grep -n \\\"TaxJRnPcJMuZ\\\" -A3 -B3 iteration_records.yaml | head -60; timeout 60 grep -rl \\\"TaxJRnPcJMuZ\\\" /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/logs /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/sinks 2>/dev/null | head\"}}}\n{\"node_id\":\"i2fYqYFRfa-L\",\"path\":\"gen_viz_report_5_9bf575d7f5bc/agent_tool_result[11]\",\"name\":\"\",\"parent_id\":\"gen_viz_report_ \n----\n\"parent_id\":\"run_An1uy2kF2SjZ-msgsum\",\"ancestor_ids\":[\"run_An1uy2kF2SjZ-msgsum\"],\"status\":\"done\",\"start_at\":null,\"end_at\":\"2026-09-25T15:57:51.948497Z\",\"type\":\"llm_gen_summary_update\",\"text\":\"\",\"target_node_id\":\"ceUljxujv2eu\",\"summary\":\"Artifact art_TaxJRnPcJMuZ found in run_report.yaml\"}\n{\"node_id\":\"llm_gen_summary_update_c90125fe180e\",\"path\":\"run_An1uy2kF2SjZ-msgsum/llm_gen_summary_update[675]\",\"name\":\"\",\"parent_id\":\"run_An1uy2kF2SjZ-msgsum\",\"ancestor_ids\":[\"run_An1uy2kF2SjZ-msgsum\"],\"status\":\"done\",\"star \n----\n5T15:57:52.615200Z\",\"type\":\"agent_tool_call\",\"text\":\"Tool: Bash cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_2_gen_paper_draft/run_record; grep -n \\\"TaxJRnPcJMuZ\\\" -A3 -B3 iteration_records.yaml | head -60; timeout 60 grep -rl \\\"TaxJRnPcJMuZ\\\" /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/logs /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/sinks 2>/dev/null | head\",\"summary\":\"\",\"task_id\":\"gen_viz_report_5_9bf575d7f5bc\",\"subagent_id\":null,\"subagent_tool_id\":null,\"subagent_model\":null,\"tool\":\" \n----\nset()", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_report_5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [34] TOOL CALL — Bash · 2026-09-25 15:58:04 UTC

```
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/sinks/events; python3 - <<'EOF'
import json
for line in open('events.jsonl',errors='ignore'):
    if 'art_2OmxzMInZZJY art_5KczEbsFPx25' in line and '"agent_tool_result"' in line:
        d=json.loads(line); print(d['path']); print(d.get('text','')[:600]); break
EOF
grep -o '"command":"[^"]*art_[^"]*"' events.jsonl | grep -v TaxJ | sort -u | head -20
```

### [35] TOOL RESULT — Bash · 2026-09-25 15:58:04 UTC

```
{"stdout": "gen_viz_report_5_9bf575d7f5bc/agent_tool_result[13]\nTool: Bash\nResult:\n{\"stdout\": \"\\\":null,\\\"tool\\\":\\\"Bash\\\",\\\"tool_id\\\":\\\"toolu_01HgdW8GTB9WruauYXCaCJNU\\\",\\\"tool_kind\\\":\\\"terminal\\\",\\\"backend\\\":\\\"terminal_claude_agent\\\",\\\"model\\\":null,\\\"extras\\\":{\\\"input\\\":{\\\"command\\\":\\\"cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/sinks/events; grep -o '[^\\\\\\\"]\\\\\\\\{0,200\\\\\\\\}TaxJRnPcJMuZ[^\\\\\\\"]\\\\\\\\{0,200\\\\\\\\}' events.jsonl | sort -u | head -20\\\"}}}\\n{\\\"node_id\\\":\\\"pod_runtime_cost_eec652881481\\\",\\\"path\\\":\\\"gen_viz_report_2_c53f66e92d4d/run_An1uy2kF2SjZ-phase-gen_paper_repo-mod-gen_viz-task-gen_viz_report_2/pod_runtime_cost[2]\\\",\\\"name\\\":\\\"\\\",\\\"parent_id \\n-\n\"command\":\"A=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results; cat $A/tables.md\"\n\"command\":\"A=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results; python3 -c \\\"\n\"command\":\"A=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7; ls -la $A; ls -la $A/results 2>/dev/null | head -50\"\n\"command\":\"A=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7; sed -n 1,60p $A/README.md; python3 -c \\\"\n\"command\":\"B=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6/results; python3 -c \\\"\n\"command\":\"B=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6; sed -n 1,75p $B/README.md\"\n\"command\":\"B=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop; sed -n 1,40p $B/iter_2/gen_art/gen_art_experiment_5/results/tables.md\"\n\"command\":\"D=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2; grep -n -i \\\"\n\"command\":\"D=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2; grep -o '\\\"\n\"command\":\"D=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2; grep -rl \\\"\n\"command\":\"D=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2; grep -rn -i \\\"\n\"command\":\"D=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2; ls $D $D/tables | head -80; cat $D/tables/m4*.csv; ls $D/tables | grep -i \\\"\n\"command\":\"F=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3; ls -la $F $F/results; python3 -c \\\"\n\"command\":\"F=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3; sed -n 300,345p $F/results/summary.json; grep -n -i \\\"\n\"command\":\"G=/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_gen.py; python $G --example barh; python $G --example forest; grep -n \\\"\n\"command\":\"G=/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_gen.py; python $G --example barh; python $G --example lollipop | head -40; grep -n \\\"\n\"command\":\"G=/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_gen.py; python $G --example forest; python $G --example lollipop | head -40\"\n\"command\":\"G=/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_gen.py; python $G --example forest; python $G --example lollipop | head -40; grep -n \\\"\n\"command\":\"G=/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_gen.py; python $G --example forest; sed -n 600,700p /ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_renderers.py\"\n\"command\":\"S=/ai-inventor/.claude/skills/aii-data-fig-gen/scripts; sed -n 112,135p $S/chart_style.py; sed -n 209,238p $S/chart_style.py; grep -n \\\"", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_report_5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [36] ASSISTANT · 2026-09-25 15:58:06 UTC

```
Found the source artifacts (run_u75jRHUss0zo, iter_2 experiment 5) and the skill location.
```

### [37] TOOL CALL — Bash · 2026-09-25 15:58:06 UTC

```
B=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5; ls -la $B $B/results | head -60; sed -n 1,60p $B/results/tables.md
```

### [38] TOOL RESULT — Bash · 2026-09-25 15:58:06 UTC

````
{"stdout": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5:\ntotal 62897\ndrwxr-xr-x 10 root   root    2016678 Sep 24 23:21 .\ndrwxr-xr-x  7 root   root    2057101 Sep 23 17:47 ..\ndrwxr-xr-x  2 root   root    1000101 Sep 23 22:21 .aii\n-rw-------  1 root   root         54 Sep 24 23:20 .aii_claude_session.json\n-rw-r--r--  1 231072 231072    90114 Sep 23 17:59 .aii_cost_ledger.jsonl\ndrwxr-xr-x  8 231072 231072  2001718 Sep 23 22:14 .git\n-rw-r--r--  1 231072 231072       53 Sep 23 18:58 .gitignore\n-rw-r--r--  1 231072 231072    90577 Sep 24 23:22 .repl_agent.ptylog\n-rw-r--r--  1 root   root       2976 Sep 24 23:22 .terminal_claude_agent_struct_out.json\n-rw-r--r--  1 231072 231072    16456 Sep 23 22:17 README.md\ndrwxr-xr-x  2 231072 231072  2000274 Sep 23 17:58 cache\ndrwxr-xr-x  3 231072 231072  2003203 Sep 24 01:10 data\n-rw-r--r--  1 231072 231072 26916860 Sep 23 18:57 full_method_out.json\ndrwxr-xr-x  2 231072 231072  1037828 Sep 23 22:13 logs\n-rw-r--r--  1 231072 231072     8261 Sep 23 18:30 method.py\n-rw-r--r--  1 231072 231072 20956520 Sep 23 18:56 method_out.json\n-rw-r--r--  1 231072 231072    62032 Sep 23 18:57 mini_method_out.json\n-rw-r--r--  1 231072 231072    61745 Sep 23 18:57 preview_method_out.json\n-rw-r--r--  1 231072 231072     2224 Sep 23 19:05 pyproject.toml\n-rw-r--r--  1 231072 231072       22 Sep 23 18:05 pytest.ini\n-rw-r--r--  1 root   root      10561 Sep 24 23:21 reproducibility.md\n-rwxrwxrwx  1 231072 231072      789 Sep 23 18:58 restore.sh\ndrwxr-xr-x  3 231072 231072  2006792 Sep 23 19:05 results\ndrwxr-xr-x  6 231072 231072  1054970 Sep 23 19:10 src\ndrwxr-xr-x  2 231072 231072  1001666 Sep 23 19:05 tests\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/results:\ntotal 73490\ndrwxr-xr-x  3 231072 231072  2006792 Sep 23 19:05 .\ndrwxr-xr-x 10 root   root    2016678 Sep 24 23:21 ..\n-rw-r--r--  1 231072 231072  3569130 Sep 23 18:00 E_disguise_map.jsonl\n-rw-r--r--  1 231072 231072     5807 Sep 23 17:58 E_judge.jsonl\n-rw-r--r--  1 231072 231072  1937377 Sep 23 18:52 E_judge_local.jsonl\n-rw-r--r--  1 231072 231072   853190 Sep 23 17:59 E_l3_q.jsonl\n-rw-r--r--  1 231072 231072 14889871 Sep 23 18:43 E_sentences.jsonl\n-rw-r--r--  1 231072 231072      170 Sep 23 18:27 E_stage_100.json\n-rw-r--r--  1 231072 231072      180 Sep 23 18:45 E_stage_all.json\n-rw-r--r--  1 231072 231072      188 Sep 23 18:25 E_stage_mini.json\n-rw-r--r--  1 231072 231072   184275 Sep 23 18:56 analysis.json\n-rw-r--r--  1 231072 231072     2264 Sep 23 18:56 audit_rederive.json\n-rw-r--r--  1 231072 231072      204 Sep 23 19:08 budget_state.json\n-rw-r--r--  1 231072 231072     4327 Sep 23 17:58 costs.jsonl\n-rw-r--r--  1 231072 231072     7336 Sep 23 22:13 deviations.json\n-rw-r--r--  1 231072 231072       94 Sep 23 18:48 judge_cache_regression.json\n-rw-r--r--  1 231072 231072  4960000 Sep 23 17:58 llm_cache.jsonl\n-rw-r--r--  1 231072 231072  4763037 Sep 23 18:52 local_cache.jsonl\n-rw-r--r--  1 231072 231072      556 Sep 23 18:56 p_tests.json\n-rw-r--r--  1 231072 231072 22016065 Sep 23 18:52 per_item_E.jsonl\n-rw-r--r--  1 231072 231072      368 Sep 23 19:05 placebo_headline.json\n-rw-r--r--  1 231072 231072     2396 Sep 23 18:54 posthoc_nf_fusion.json\n-rw-r--r--  1 231072 231072      221 Sep 23 18:31 prefilter_audit.json\n-rw-r--r--  1 231072 231072    17167 Sep 23 18:23 prereg.json\n-rw-r--r--  1 231072 231072      112 Sep 23 18:23 prereg.sha256\n-rw-r--r--  1 231072 231072     2081 Sep 23 18:18 prereg_selection.json\n-rw-r--r--  1 231072 231072       65 Sep 23 18:18 prereg_selection.sha256\n-rw-r--r--  1 231072 231072   118722 Sep 23 17:58 prices.json\n-rw-r--r--  1 231072 231072   655065 Sep 23 18:52 rewrite_scores_pt.jsonl\n-rw-r--r--  1 231072 231072     5012 Sep 23 18:22 screen_fit.json\n# Dataset E results (PEER+TEXT, frozen on the screen; prereg sha256 b9f28b1bf6bf)\n\n## (a) Item-level AUROC [95% sentence-cluster bootstrap CI], identical rows per table\n\n| subset | n (err/cor) | PEER+TEXT | TEXT | PEER (ALIGN g) | c_score_align | NF c_score | NF g | L2-bow | L3 |\n|---|---|---|---|---|---|---|---|---|---|\n| R_AB pooled | 2686 (1822/864) | 0.790 [0.75, 0.82] | 0.693 [0.65, 0.73] | 0.748 [0.71, 0.79] | 0.782 [0.74, 0.82] | 0.743 [0.70, 0.78] | 0.742 [0.70, 0.78] | 0.734 [0.71, 0.76] | 0.579 [0.53, 0.62] |\n| R_AB L25 | 873 (697/176) | 0.755 [0.70, 0.80] | 0.691 [0.63, 0.74] | 0.676 [0.61, 0.73] | 0.712 [0.65, 0.77] | 0.651 [0.59, 0.71] | 0.650 [0.58, 0.71] | 0.722 [0.67, 0.77] | 0.560 [0.49, 0.63] |\n| R_AB L20 | 821 (592/229) | 0.747 [0.69, 0.80] | 0.683 [0.63, 0.74] | 0.636 [0.56, 0.70] | 0.722 [0.66, 0.78] | 0.643 [0.58, 0.70] | 0.631 [0.56, 0.70] | 0.715 [0.66, 0.76] | 0.547 [0.48, 0.62] |\n| R_AB EXC | 606 (384/222) | 0.777 [0.72, 0.83] | 0.666 [0.60, 0.73] | 0.782 [0.71, 0.84] | 0.814 [0.76, 0.86] | 0.782 [0.72, 0.84] | 0.787 [0.72, 0.84] | 0.669 [0.61, 0.72] | 0.620 [0.55, 0.69] |\n| R_AB CTRL | 386 (149/237) | 0.708 [0.57, 0.84] | 0.559 [0.43, 0.70] | 0.769 [0.64, 0.88] | 0.742 [0.62, 0.86] | 0.741 [0.61, 0.86] | 0.759 [0.63, 0.87] | 0.613 [0.54, 0.72] | 0.490 [0.37, 0.62] |\n| R_AB long (L25+L20+EXC) | 2300 (1673/627) | 0.768 [0.74, 0.80] | 0.690 [0.65, 0.72] | 0.705 [0.66, 0.74] | 0.759 [0.72, 0.79] | 0.704 [0.67, 0.74] | 0.697 [0.65, 0.73] | 0.717 [0.69, 0.75] | 0.580 [0.54, 0.62] |\n| R_A pooled L20+EXC | 449 (261/188) | 0.818 [0.73, 0.88] | 0.665 [0.57, 0.74] | 0.812 [0.73, 0.88] | 0.860 [0.79, 0.92] | 0.802 [0.72, 0.87] | 0.799 [0.72, 0.86] | 0.678 [0.61, 0.74] | 0.587 [0.51, 0.66] |\n| R_A L20 | 196 (132/64) | 0.747 [0.63, 0.84] | 0.594 [0.50, 0.68] | 0.732 [0.60, 0.85] | 0.773 [0.64, 0.87] | 0.688 [0.56, 0.80] | 0.710 [0.58, 0.83] | 0.665 [0.58, 0.75] | 0.461 [0.37, 0.56] |\n| R_A EXC | 253 (129/124) | 0.858 [0.75, 0.94] | 0.687 [0.58, 0.78] | 0.852 [0.76, 0.92] | 0.898 [0.81, 0.97] | 0.852 [0.77, 0.92] | 0.846 [0.76, 0.91] | 0.656 [0.57, 0.74] | 0.656 [0.55, 0.75] |\n| R_A all strata (sign only) | 867 (453/414) | 0.798 [0.72, 0.87] | 0.647 [0.56, 0.72] | 0.837 [0.77, 0.89] | 0.825 [0.75, 0.89] | 0.809 [0.74, 0.87] | 0.830 [0.76, 0.88] | 0.693 [0.64, 0.75] | 0.551 [0.47, 0.63] |\n| R_A L25 (sign only) | 138 (98/40) | 0.790 [0.67, 0.89] | 0.626 [0.51, 0.74] | 0.823 [0.71, 0.91] | 0.783 [0.66, 0.88] | 0.735 [0.60, 0.84] | 0.774 [0.65, 0.87] | 0.727 [0.60, 0.84] | 0.423 [0.29, 0.57] |\n| R_A CTRL (sign only) | 280 (94/186) | 0.692 [0.50, 0.88] | 0.496 [0.35, 0.67] | 0.826 [0.64, 0.97] | 0.777 [0.59, 0.93] | 0.805 [0.62, 0.95] | 0.827 [0.65, 0.96] | 0.521 [0.50, 0.56] | 0.482 [0.33, 0.65] |\n\n## (a) Paired ΔAUROC vs the judges (rows where the judge score exists)\n\n| subset | judge | n (err/cor) | judge AUROC | Δ PEER+TEXT − judge [CI] | Δ TEXT − judge [CI] | DeLong p |\n|---|---|---|---|---|---|---|\n| R_AB pooled | judge_local_qwen8b_disg | 2686 (1822/864) | 0.712 | 0.078 [0.043, 0.112] | -0.019 [-0.065, 0.028] | 0.0000 |\n| R_AB pooled | judge_cheap_disg | 20 (8/12) | 0.750 | 0.057 [-0.200, 0.360] | -0.047 [-0.324, 0.272] | 0.6195 |\n| R_AB L25 | judge_local_qwen8b_disg | 873 (697/176) | 0.664 | 0.092 [0.031, 0.151] | 0.027 [-0.036, 0.088] | 0.0004 |\n| R_AB L25 | judge_cheap_disg | 0 | untestable | | | |\n| R_AB L20 | judge_local_qwen8b_disg | 821 (592/229) | 0.683 | 0.064 [-0.001, 0.129] | -0.000 [-0.072, 0.073] | 0.0046 |\n| R_AB L20 | judge_cheap_disg | 0 | untestable | | | |\n| R_AB EXC | judge_local_qwen8b_disg | 606 (384/222) | 0.663 | 0.114 [0.033, 0.194] | 0.004 [-0.088, 0.095] | 0.0000 |\n| R_AB EXC | judge_cheap_disg | 0 | untestable | | | |\n| R_AB CTRL | judge_local_qwen8b_disg | 386 (149/237) | 0.739 | -0.031 [-0.142, 0.089] | -0.180 [-0.331, -0.022] | 0.1890 |\n| R_AB CTRL | judge_cheap_disg | 20 (8/12) | 0.750 | 0.057 [-0.200, 0.360] | -0.047 [-0.324, 0.272] | 0.6195 |\n| R_AB long (L25+L20+EXC) | judge_local_qwen8b_disg | 2300 (1673/627) | 0.653 | 0.115 [0.075, 0.157] | 0.036 [-0.007, 0.083] | 0.0000 |\n| R_AB long (L25+L20+EXC) | judge_cheap_disg | 0 | untestable | | | |\n| R_A pooled L20+EXC | judge_local_qwen8b_disg | 449 (261/188) | 0.554 | 0.264 [0.157, 0.359] | 0.110 [-0.006, 0.216] | 0.0000 |\n| R_A pooled L20+EXC | judge_cheap_disg | 0 | untestable | | | |\n| R_A L20 | judge_local_qwen8b_disg | 196 (132/64) | 0.544 | 0.203 [0.024, 0.357] | 0.050 [-0.094, 0.180] | 0.0002 |\n| R_A L20 | judge_cheap_disg | 0 | untestable | | | |\n| R_A EXC | judge_local_qwen8b_disg | 253 (129/124) | 0.647 | 0.210 [0.075, 0.335] | 0.039 [-0.107, 0.183] | 0.0000 |\n| R_A EXC | judge_cheap_disg | 0 | untestable | | | |\n| R_A all strata (sign only) | judge_local_qwen8b_disg | 867 (453/414) | 0.669 | 0.129 [0.061, 0.203] | -0.023 [-0.114, 0.075] | 0.0000 |\n| R_A all strata (sign only) | judge_cheap_disg | 15 | untestable | | | |\n| R_A L25 (sign only) | judge_local_qwen8b_disg | 138 (98/40) | 0.560 | 0.230 [0.119, 0.365] | 0.066 [-0.064, 0.203] | 0.0000 |\n| R_A L25 (sign only) | judge_cheap_disg | 0 | untestable | | | |\n| R_A CTRL (sign only) | judge_local_qwen8b_disg | 280 (94/186) | 0.697 | -0.005 [-0.185, 0.191] | -0.200 [-0.427, 0.019] | 0.8771 |\n| R_A CTRL (sign only) | judge_cheap_disg | 15 | untestable | | | |\n\n## (a') Stratified AUROC (within-stratum pairs only; removes the stratum-composition confound) [B=1000 CI]\n\n| subset | n | PEER+TEXT | TEXT | PEER | c_score_align | NF c_score | local judge | Δ PEER+TEXT − judge [CI] | Δ PEER+TEXT − c_score_align [CI] |\n|---|---|---|---|---|---|---|---|---|---|\n| R_AB pooled | 2686 | 0.753 | 0.670 | 0.694 | 0.741 | 0.686 | 0.677 | 0.075 [0.036, 0.114] | 0.011 [-0.012, 0.038] |\n| R_AB long (L25+L20+EXC) | 2300 | 0.757 | 0.682 | 0.686 | 0.741 | 0.680 | 0.671 | 0.086 [0.049, 0.126] | 0.016 [-0.010, 0.041] |\n| R_A pooled L20+EXC | 449 | 0.819 | 0.655 | 0.811 | 0.855 | 0.795 | 0.612 | 0.208 [0.105, 0.305] | -0.036 [-0.113, 0.030] |\n\nPlacebos: within-stratum label permutation {\"p_peer_text\": 0.59, \"p_text\": 0.552, \"peer_only\": 0.58, \"c_score_align\": 0.592} (composition part of pooled AUROC); global shuffle {\"p_peer_text\": 0.5, \"p_text\": 0.501, \"peer_only\": 0.501, \"judge_local_qwen8b_disg\": 0.5}\n\n## Criteria\n```", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
````

### [39] TOOL CALL — Bash · 2026-09-25 15:58:12 UTC

```
B=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/results; python3 - <<EOF
import json
a=json.load(open("$B/analysis.json"))
print(list(a.keys()))
def walk(o,p=''):
    if isinstance(o,dict):
        for k,v in o.items(): walk(v,p+'/'+str(k))
    elif isinstance(o,list):
        if len(o)<5 and all(not isinstance(x,(dict,list)) for x in o): 
            if 'judge_local' in p and 'R_AB pooled' in p: print(p,o)
        else:
            for i,x in enumerate(o[:50]): walk(x,p+f'[{i}]')
    else:
        if 'judge_local' in p and ('pooled' in p or 'auroc' in p.lower()): print(p,o)
walk(a)
EOF
```

### [40] TOOL RESULT — Bash · 2026-09-25 15:58:12 UTC

```
{"stdout": "['coverage_imputation', 'a_tables', 'a_sensitivity', 'criteria', 'b_P1', 'c_P2', 'd_P3', 'e_P4', 'f_error_types', 'g_system', 'h_complexity', 'i_contamination', 'j_coverage_cost', 'k_misc', 'placebo_within_stratum', 'placebo_global_shuffle', 'a_stratified']\n/a_tables/R_AB pooled/vs_judge_local_qwen8b_disg/n 2686\n/a_tables/R_AB pooled/vs_judge_local_qwen8b_disg/n_error 1822\n/a_tables/R_AB pooled/vs_judge_local_qwen8b_disg/n_correct 864\n/a_tables/R_AB pooled/vs_j... [truncated, 30636 chars total]
```

### [41] TOOL CALL — Bash · 2026-09-25 15:58:16 UTC

```
B=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/results; python3 - <<EOF
import json
a=json.load(open("$B/analysis.json"))
t=a['a_tables']
print(list(t.keys()))
k='R_AB pooled'; print(list(t[k].keys()))
v=t[k]['vs_judge_local_qwen8b_disg']; print([x for x in v.keys()]); print(list(v['metrics'].keys()))
print({kk:vv for kk,vv in v.items() if kk!='metrics'})
EOF
```

### [42] TOOL RESULT — Bash · 2026-09-25 15:58:16 UTC

```
{"stdout": "['R_AB pooled', 'R_AB L25', 'R_AB L20', 'R_AB EXC', 'R_AB CTRL', 'R_AB long (L25+L20+EXC)', 'R_A pooled L20+EXC', 'R_A L20', 'R_A EXC', 'R_A all strata (sign only)', 'R_A L25 (sign only)', 'R_A CTRL (sign only)']\n['n', 'n_error', 'n_correct', 'n_sentences', 'metrics', 'paired', 'vs_judge_local_qwen8b_disg', 'vs_judge_local_qwen8b_orig', 'vs_judge_cheap_disg', 'vs_judge_cheap_orig']\n['n', 'n_error', 'n_correct', 'n_sentences', 'metrics', 'paired']\n['p_peer_text', 'p_text', 'peer_only', 'c_score_align', 'judge_local_qwen8b_disg']\n{'n': 2686, 'n_error': 1822, 'n_correct': 864, 'n_sentences': 292, 'paired': {'p_peer_text - judge_local_qwen8b_disg': {'delta': 0.07828508049762173, 'ci': [0.04337606521047203, 0.11223555043519434], 'p_boot_le0': 0.0, 'delong_z': 7.010055377113383, 'delong_p': 2.382316566240661e-12}, 'p_text - judge_local_qwen8b_disg': {'delta': -0.01859633542708461, 'ci': [-0.06546699860038939, 0.027557082271771133], 'p_boot_le0': 0.7845, 'delong_z': -1.4275962783030582, 'delong_p': 0.15340809545764977}, 'c_score_align - judge_local_qwen8b_disg': {'delta': 0.07062154429401957, 'ci': [0.03220969227014037, 0.10686830981581004], 'p_boot_le0': 0.0, 'delong_z': 6.027085402972954, 'delong_p': 1.6694279292295278e-09}, 'peer_only - judge_local_qwen8b_disg': {'delta': 0.03630841667683049, 'ci': [-0.0038296281958695526, 0.07584223483559173], 'p_boot_le0': 0.0335, 'delong_z': 2.7946374679828287, 'delong_p': 0.005195794519837982}}}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [43] ASSISTANT · 2026-09-25 15:58:22 UTC

```
Local-judge CIs exist in analysis.json. Extracting all 42 values + CIs straight from it.
```

### [44] TOOL CALL — Bash · 2026-09-25 15:58:22 UTC

```
B=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/results; python3 - <<EOF
import json
a=json.load(open("$B/analysis.json"))['a_tables']
subs=['R_AB pooled', 'R_AB L25', 'R_AB L20', 'R_AB EXC', 'R_AB CTRL', 'R_AB long (L25+L20+EXC)', 'R_A pooled L20+EXC']
print(list(a['R_AB pooled']['metrics'].keys()))
for s in subs:
    m=a[s]['metrics']; j=a[s]['vs_judge_local_qwen8b_disg']
    row=[s,a[s]['n'],a[s]['n_error'],a[s]['n_correct'], j['n']]
    for k in ['p_peer_text','c_score_align','nf_c_score','l2_bow','l3']:
        kk=[x for x in m if x==k]
        if kk: row.append((round(m[k]['auroc'],3),[round(c,3) for c in m[k]['ci']]))
    jm=j['metrics']['judge_local_qwen8b_disg']; row.append(('judge',round(jm['auroc'],3),[round(c,3) for c in jm['ci']]))
    print(row)
EOF
```

### [45] TOOL RESULT — Bash · 2026-09-25 15:58:22 UTC

```
{"stdout": "['p_peer_text', 'peer_only', 'p_text', 'g_score', 'c_score_nf', 'c_score_align', 'l2_bow', 'l3_z3', 'nf_g_score', 'nf_c_score', 'p_sensitivity', 'g_score_k6', 'g_score_famfield', 'l1_any', 'l2_role']\n['R_AB pooled', 2686, 1822, 864, 2686, (0.79, [0.752, 0.823]), (0.782, [0.744, 0.818]), (0.743, [0.703, 0.78]), (0.734, [0.706, 0.762]), ('judge', 0.712, [0.673, 0.747])]\n['R_AB L25', 873, 697, 176, 873, (0.755, [0.701, 0.803]), (0.712, [0.649, 0.769]), (0.651, [0.585, 0.707]), (0.722, [0.668, 0.771]), ('judge', 0.664, [0.613, 0.713])]\n['R_AB L20', 821, 592, 229, 821, (0.747, [0.69, 0.797]), (0.722, [0.659, 0.781]), (0.643, [0.576, 0.703]), (0.715, [0.661, 0.763]), ('judge', 0.683, [0.634, 0.733])]\n['R_AB EXC', 606, 384, 222, 606, (0.777, [0.716, 0.833]), (0.814, [0.757, 0.864]), (0.782, [0.721, 0.839]), (0.669, [0.612, 0.721]), ('judge', 0.663, [0.608, 0.723])]\n['R_AB CTRL', 386, 149, 237, 386, (0.708, [0.569, 0.842]), (0.742, [0.616, 0.863]), (0.741, [0.605, 0.856]), (0.613, [0.54, 0.716]), ('judge', 0.739, [0.607, 0.867])]\n['R_AB long (L25+L20+EXC)', 2300, 1673, 627, 2300, (0.768, [0.735, 0.8]), (0.759, [0.723, 0.791]), (0.704, [0.666, 0.739]), (0.717, [0.687, 0.747]), ('judge', 0.653, [0.621, 0.683])]\n['R_A pooled L20+EXC', 449, 261, 188, 449, (0.818, [0.735, 0.883]), (0.86, [0.789, 0.92]), (0.802, [0.723, 0.869]), (0.678, [0.613, 0.736]), ('judge', 0.554, [0.487, 0.62])]", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [46] TOOL CALL — Bash · 2026-09-25 15:58:26 UTC

```
B=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/results; python3 - <<EOF
import json
a=json.load(open("$B/analysis.json"))['a_tables']
for s in ['R_AB pooled', 'R_AB L25', 'R_AB L20', 'R_AB EXC', 'R_AB CTRL', 'R_AB long (L25+L20+EXC)', 'R_A pooled L20+EXC']:
    m=a[s]['metrics']['l3_z3']; print(s, round(m['auroc'],3), [round(c,3) for c in m['ci']], m.get('n'))
print(a['R_AB pooled']['metrics']['l3_z3'].keys())
EOF
cat /ai-inventor/.claude/skills/aii-data-fig-gen/SKILL.md
```

### [47] TOOL RESULT — Bash · 2026-09-25 15:58:26 UTC

```
{"stdout": "R_AB pooled 0.579 [0.529, 0.625] None\nR_AB L25 0.56 [0.494, 0.625] None\nR_AB L20 0.547 [0.482, 0.615] None\nR_AB EXC 0.62 [0.547, 0.69] None\nR_AB CTRL 0.49 [0.367, 0.62] None\nR_AB long (L25+L20+EXC) 0.58 [0.537, 0.623] None\nR_A pooled L20+EXC 0.587 [0.507, 0.662] None\ndict_keys(['auroc', 'ci', 'auprc', 'prevalence'])\n---\nname: aii-data-fig-gen\ndescription: \"Renders publication-quality DATA FIGURES deterministically from a JSON spec via matplotlib — bar, l... [truncated, 30724 chars total]
```

### [48] ASSISTANT · 2026-09-25 15:58:28 UTC

```
All 42 values match the spec's table. Reading the skill guide now.
```

### [49] TOOL CALL — Bash · 2026-09-25 15:58:28 UTC

```
sed -n 1,400p /ai-inventor/.claude/skills/aii-data-fig-gen/SKILL.md | grep -v "^$" | head -300
```

### [50] TOOL RESULT — Bash · 2026-09-25 15:58:28 UTC

````
{"stdout": "---\nname: aii-data-fig-gen\ndescription: \"Renders publication-quality DATA FIGURES deterministically from a JSON spec via matplotlib — bar, line, scatter, heatmap, confusion matrix, box, violin, histogram, ECDF, ROC/PR, calibration, scaling law, Pareto frontier, forest/CI, volcano, dendrogram, clustermap, network graph, lettered multi-panel composites — as vector PDF plus PNG. Use whenever a figure plots numbers that already exist, so the drawing cannot disagree with them, and for hand-written matplotlib that must match the paper's house style. Triggers: chart, plot, graph, data figure, figure_type='data', confusion matrix, ablation grid, training curve, ROC, precision-recall, colourblind palette, Type 42 fonts, chart spec JSON. NOT for: figures with no dataset — architecture and flow diagrams, conceptual artwork, cover images — which go to aii-concept-fig-gen; charts that must live inside an Excel workbook are anthropic-xlsx; displaying a rendered file is amg-open-img-ubuntu.\"\n---\n# Data figures — charts rendered from their numbers\nDeterministic figures from a JSON spec: the numbers go in, matplotlib draws\nthem, and the picture cannot disagree with the data. Nothing is generated by\na model, so a bar is the height of its value and every axis is computed.\nRe-running a spec gives a byte-identical PNG; the PDF differs only in its\nembedded creation timestamp.\n## Data figure or concept figure?\n| The figure is… | Use |\n|---|---|\n| A chart of numbers you have | **this skill** |\n| A confusion matrix, ablation grid, correlation | **this skill** |\n| A scaling law, training curve, Pareto trade-off | **this skill** |\n| Artwork, a metaphor, a cover image | `aii-concept-fig-gen` |\n| An architecture or flow diagram | `aii-concept-fig-gen` |\nIn that table **this skill** means a data figure and `aii-concept-fig-gen` a\nconcept figure. For an architecture or flow diagram, read *Limits* first.\nThe test is whether the figure has underlying numbers. If it does, an image\nmodel will approximate them — bars that do not match their labels, axis\nticks that do not divide evenly, invented data points. That failure is\ninvisible to a reviewer of the prompt and obvious to a reviewer of the\npaper.\n## Use a generator when one fits — hand-write only when none does\nThe generators are a menu, not a fence. Every type below is a shortcut that\nalready has the house style, the data-integrity guards and the layout fixes\nbaked in, so reaching for one is almost always less work than plotting by\nhand and the result is consistent with every other figure in the paper.\n**Check `--list-types` first.** If a type matches what you need, use it.\nDon't know the name? `--search \"<the question your figure answers>\"` ranks\nthe catalogue by intent rather than by name — `--search \"before and after\nper method\"` puts `slope` first and `dumbbell` second.\nTwo-thirds of research figures are a bar, a line, a scatter or a heatmap,\nand those are solved.\n`--search` spans **two corpora** and labels every hit with which one it\ncame from:\n| label | what it is | what to do |\n|---|---|---|\n| `ours: <type>` | one of our 61 types | `--example`, edit, render |\n| `chartmimic: <task>/<id>` | a published figure | read its `.py` |\nA `chartmimic:` hit is a **reference, not a spec.** It is a human-curated\nfigure from a STEM paper with the matplotlib that draws it — from\nChartMimic ([arXiv:2406.09961](https://arxiv.org/abs/2406.09961)), 4,800 of\nthem over 22 categories. Adapting one is a *hand-written* figure: no house\nstyle, no data-integrity guards, no layout passes unless you call them, so\neverything above about hand-written figures still applies. The search\nprints the path to its code under every such hit. Generators outrank\nexemplars on a tie, because a generator is the runnable answer.\nReach for an exemplar in exactly two cases: **nothing in the catalogue\nfits** (see the gap table below), or you want to see how a published figure\ndid something — a twin axis, a labelled contour — in working code.\n`--corpus ours|chartmimic|all` narrows the search; the default is `all`.\n**If nothing fits, write matplotlib yourself** — that is expected and\nsupported, not a failure. Novel or one-off figures exist. When you do:\n```python\nimport sys; sys.path.insert(0, \"<skill>/scripts\")\nimport matplotlib.pyplot as plt\nfrom chart_geometry import assert_text_is_legible, fit_point_labels\nfrom chart_style import (\n    apply_house_style, PALETTE, literal, place_legend, place_point_label,\n    fit_legends, clear_legends_of_data, fit_tick_labels, fit_titles,\n    rasterize_dense_clouds, assert_legends_clear_of_data,\n    assert_series_are_distinguishable, assert_axis_names_are_unique,\n)\napply_house_style()                 # fonts, palette, grid, Type-42 PDF fonts\nfig, ax = plt.subplots(figsize=(7, 3.94), layout=\"constrained\")\n...\nplace_legend(ax, loc=\"best\")        # a legend fit_legends can reflow\nplace_point_label(ax, literal(\"Ours\"), (1, 2))   # a name, nudged off the data\nfit_legends(fig)                    # reflow a legend wider than its axes\nclear_legends_of_data(fig)          # move it below the axes if it sits on data\nfit_tick_labels(fig)                # wrap/tilt tick labels that would collide\nfit_titles(fig)                     # wrap any title wider than its axes\nclear_legends_of_data(fig)          # AGAIN — the two above reshaped the axes\nfit_point_labels(fig)               # move point names off markers and curves\nrasterize_dense_clouds(fig)         # >25k points as a bitmap, text stays vector\nassert_text_is_legible(fig)         # raises if any text collides or is cut off\nassert_legends_clear_of_data(fig)   # raises if a legend still hides its data\nassert_series_are_distinguishable(fig)  # raises on two identical legend keys\nassert_axis_names_are_unique(fig)   # raises if one name labels two positions\nfig.savefig(\"figX_v0.pdf\")          # vector, so LaTeX renders text at page res\n```\nCall the fitters in that order — the legend decides how much room the axes\nhas, whether it then has to move out of the data is only knowable once it is\nplaced, tick labels change the axes height, the title is measured against the\naxes it ends up on, and a point's name can only be placed once nothing above\nit will move the point again. `clear_legends_of_data` appears TWICE on\npurpose: it decides by measuring, and the two passes between its calls shrink\nthe axes under a legend that is already placed and a fixed size. A wrapped\ntitle took a lone chart from 179 px of axes height to 141, and a legend that\ncovered nothing before covered half a curve after — with the mover's turn\nalready past, so the figure was refused rather than fixed. The first call\nstill has to happen first, because the room the legend needs is an input to\nthe passes below it. Two further gates are warning-based and so are\nnot in the snippet: `assert_layout_applied` and `assert_all_glyphs_rendered`\nread what matplotlib warned about during the draw, so they need the figure\nbuilt inside `warnings.catch_warnings(record=True)` — worth doing, since a\nmissing glyph is only ever a warning and ships as a hollow box.\n`place_legend` and `place_point_label` are how\nthe fitters find what to fix: a legend built with a bare `ax.legend` cannot\nbe reflowed, and a name written with a bare `ax.annotate` will not be moved\noff the marker it landed on.\nThat keeps a hand-written figure looking like the rest of the paper and\nstill gets you colourblind-safe colours, submission-compliant fonts, no\nclipped labels and no overprinted ones. What you lose is the data-integrity\nchecking — so verify the numbers yourself.\n**If you hand-write the same figure type twice, add a renderer instead.**\n`chart_renderers*.py` — one function, `(ax, spec) -> None`, registered in\nits family's dict. That is how this catalogue got here.\n## Use it\n```bash\nSKILL_DIR=\"$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-data-fig-gen\"\nG=\"$SKILL_DIR/scripts/chart_gen.py\"\npython \"$G\" --list-types            # the catalogue\npython \"$G\" --search \"compare distributions across groups\"   # find it by intent\npython \"$G\" --search \"pie wedges\" --corpus chartmimic         # exemplars only\npython \"$G\" --audit                 # what ChartMimic has that we do not\npython \"$G\" --example bar           # a complete spec to copy and edit\npython \"$G\" --spec fig1.json --out figures/fig1\n```\n`python` here is the pipeline image's interpreter, which has matplotlib and\nscipy installed system-wide. Outside the image use the project venv —\n`.venv/bin/python` — since a bare `python3` will not have them.\nWrites `figures/fig1.pdf` **and** `figures/fig1.png`. The PDF is the\ndeliverable — LaTeX renders vector text at page resolution, so it stays\nsharp and selectable at any zoom. The PNG exists so you can read the figure\nback and look at it.\n`--format pdf`, `--format png`, `--format pdf,png,svg` narrows the output.\nSVG keeps its labels as TEXT rather than paths, so it stays editable and\nsearchable. EPS is refused: the PostScript backend cannot draw transparency\nand flattens it silently, which the house style uses on nine of every ten\nfigures — the file would not match the PNG you checked.\n`--spec -` reads the spec from stdin.\nRuns on `matplotlib` + `numpy`, both already `aii_pipeline` dependencies —\nnothing to install.\n## The catalogue\n`--example <type>` prints a complete spec for any of these. The \"choose it\nover\" half of each entry is the useful one: most figures have two plausible\ntypes and the choice between them is what decides whether a reviewer reads\nthe point.\n### Comparing categories\n- `bar` — draws: Vertical bars, grouped or stacked, optional error bars.\n  Choose it over: The default. `barh` if names are long.\n- `barh` — draws: Horizontal bars — labels on the y-axis with room to run.\n  Choose it over: `bar`, whenever names exceed ~40 chars, or for a ranking.\n- `lollipop` — draws: A stem and a dot per category. Choose it over: `barh`,\n  past ~20 categories, where bars become a picket fence.\n- `dumbbell` — draws: Two markers per row joined by a line. Choose it over:\n  Paired bars, when the GAP between them is the story.\n- `slope` — draws: One line per item from a before value to an after value.\n  Choose it over: Paired bars, when which items changed RANK is the story.\n- `bump` — draws: Rank against time, one line per item; the crossings are\n  the finding. Choose it over: `slope`, which shows a reordering for exactly\n  TWO time points and cannot show the path between more.\n- `volcano` — draws: Effect size against significance, with both thresholds\n  drawn. Choose it over: A `bar` of effects, which cannot show what survived\n  correction, or a table of p-values, which cannot show what was big enough\n  to matter.\n- `diverging` — draws: Signed bars either side of zero, sorted. Choose it\n  over: `bar`, for deltas — direction reads instantly.\n- `waterfall` — draws: Steps from a starting total to a final total. Choose\n  it over: `bar`, for an ablation — it shows contributions compounding.\n- `bar_sig` — draws: Grouped bars with significance brackets and stars.\n  Choose it over: `bar`, when the comparison being claimed is pairwise.\n- `forest` — draws: Point estimates with confidence intervals and a null\n  line. Choose it over: `bar`, when whether an interval crosses zero is the\n  question.\n- `radar` — draws: A closed polygon per method over 3+ metrics. Choose it\n  over: Several bar charts, for a multi-metric profile at a glance.\n- `parallel` — draws: One polyline per configuration across independently\n  scaled axes. Choose it over: A table, for a hyperparameter sweep — trends\n  across axes show up.\n- `funnel` — draws: Stage attrition with retention vs. previous and vs.\n  intake. Choose it over: `barh`, when the stages are sequential and losses\n  compound.\n- `stacked_pct` — draws: Composition as percentages; every bar full height.\n  Choose it over: Stacked `bar`, when categories have very different totals.\n- `treemap` — draws: Nested rectangles with AREA proportional to value.\n  Choose it over: `bar`, only when there are too many parts for one axis —\n  length beats area for precise reading.\n- `upset` — draws: Set intersections as sorted bars over a membership\n  matrix. Choose it over: A Venn diagram, past 3 sets — circles cannot stay\n  area-true and stop reading as sets.\n### Trends and relationships\n- `line` — draws: Multi-series lines with optional uncertainty bands. Choose\n  it over: The default for anything against time or steps.\n- `fan` — draws: A median with nested quantile bands around it. Choose it\n  over: `line` with a band, when the spread is skewed or bounded — a\n  symmetric ± band on an accuracy near its ceiling implies scores above\n  100%.\n- `step` — draws: A piecewise-constant series — value holds, then jumps.\n  Choose it over: `line`, for schedules — a slope implies values that never\n  occurred.\n- `scatter` — draws: Points with an optional least-squares fit and R².\n  Choose it over: `line`, when x is not ordered and the relationship is the\n  point.\n- `joint` — draws: Scatter with the marginal distribution of each variable\n  beside it. Choose it over: `scatter`, when \"and how is each one\n  distributed?\" is the obvious next question — which for a headline\n  correlation it always is.\n- `splom` — draws: Every pair of variables as its own scatter, distributions\n  down the diagonal. Choose it over: `corr`, when the SHAPE of each\n  relationship is the claim — one number cannot tell a straight line from\n  two clusters or an outlier.\n- `bubble` — draws: Scatter with a third variable as marker AREA, plus a\n  size key. Choose it over: `scatter`, when a third quantity matters but not\n  enough for its own axis.\n- `scaling` — draws: Log-log points with a fitted power law and its\n  exponent. Choose it over: `line`, for scaling laws — the exponent is\n  computed and annotated.\n- `speedup` — draws: Measured speedup against worker count, with the ideal\n  line. Choose it over: `line`, for parallel results — the ideal reference\n  is what the claim is measured against.\n- `pareto` — draws: Scatter with the non-dominated frontier drawn through\n  it. Choose it over: `scatter`, for trade-offs where the frontier is the\n  finding.\n- `area` — draws: Stacked areas — a total and how it divides. Choose it\n  over: `line`, when the total matters as much as the parts.\n- `residual` — draws: Residuals against fitted values, with the zero line.\n  Choose it over: Predicted-vs-actual, where heteroscedasticity hides on the\n  diagonal.\n- `bland_altman` — draws: Difference between two methods against their mean,\n  with limits of agreement. Choose it over: A scatter of A against B, where\n  the diagonal reads as agreement and r = 0.99 hides a 10% offset.\n- `acf` — draws: Autocorrelation per lag as stems, with the significance\n  band. Choose it over: `line`, which shows the level and hides whether each\n  point predicts the next.\n- `sankey` — draws: Flows between stages at proportional widths. Choose it\n  over: `area`, when what matters is what became what.\n- `timeline` — draws: Gantt-style spans, one row per task. Choose it over: A\n  table of timestamps, when overlap and duration are the point.\n### Model evaluation\nGive these raw `labels` and `scores` rather than a precomputed curve wherever\nyou can: the renderer sweeps the threshold itself, so the AUC or AP in the\nlegend is integrated from the points actually drawn and cannot drift from\nthe curve beside it.\nWhen only the curve survives — it came from a paper, or from a logged\nartefact — pass it directly instead: `fpr`/`tpr` for `roc`, `recall`/\n`precision` for `pr`, `probabilities`/`labels` for `calibration`. The\nsummary statistic is still integrated from the plotted points, so a PR curve\nthat stops short reports `AP = 0.375 up to recall 0.60` rather than quietly\nextrapolating the rest. One evaluation set per figure: `pr`'s baseline and\n`calibration`'s bins both move with class balance, so curves from different\ntest sets cannot share axes honestly.\n- `roc` — draws: ROC curves with AUC in the legend, plus the chance\n  diagonal. Choose it over: `pr`, when the classes are roughly balanced.\n- `pr` — draws: Precision-recall curves with average precision and the\n  prevalence baseline. Choose it over: `roc`, when positives are rare — ROC\n  flatters a rare-class model.\n- `calibration` — draws: Reliability diagram with the ideal diagonal, ECE,\n  and per-bin counts. Choose it over: `roc`/`pr`, when whether to TRUST a\n  probability is the question.\n- `learning_curve` — draws: Score against training-set size, train and\n  validation with ±std bands. Choose it over: `line`, to show whether more\n  data or a better model is the bottleneck.\n- `qq` — draws: Sample quantiles against theoretical normal quantiles, with\n  a reference line. Choose it over: `hist`, for judging normality — the eye\n  reads a straight line far better than a bell.\n- `cd_diagram` — draws: Mean ranks over many datasets, joining methods a\n  test cannot separate. Choose it over: `bar_sig`, which compares pairwise\n  on ONE dataset — this is the many-datasets headline figure.\n### Distributions\n- `box` — draws: Median, quartiles, whiskers, outliers per group. Choose it\n  over: The compact default for a few groups.\n- `violin` — draws: Full mirrored density per group. Choose it over: `box`,\n  when a distribution may be multi-modal — a box hides that.\n- `strip` — draws: Every raw observation, jittered, with the mean marked.\n  Choose it over: `box`, when n is small enough that each point should be\n  visible.\n- `beeswarm` — draws: Every observation, packed sideways so none hides\n  another. Choose it over: `strip`, whose random jitter still overlaps at\n  any real n — the eye reads the clumps as density and they are partly\n  collision.\n- `ridgeline` — draws: Stacked density curves, one row per group. Choose it\n  over: `violin`, past ~6 groups, where a violin grid gets too wide.\n- `raincloud` — draws: Half violin, box and jittered points together, with\n  n. Choose it over: `violin`, when the reader must see the observations —\n  twelve seeds look as smooth as twelve thousand.\n- `hist` — draws: Binned counts or density. Choose it over: `ecdf`, only\n  when the shape of ONE distribution is the point.\n- `ecdf` — draws: Empirical cumulative distribution, stepped. Choose it\n  over: `hist`, for comparing distributions — no bin width to argue about.\n- `survival` — draws: Kaplan-Meier curves with censoring ticks and\n  confidence bands. Choose it over: `ecdf`, when some subjects have not\n  finished — an ECDF must drop or invent those.\n- `hexbin` — draws: Hexagonal density bins with a colourbar. Choose it over:\n  `scatter`, past ~2000 points where it becomes a solid blob.\n- `hist2d` — draws: A joint distribution as a rectangular binned grid.\n  Choose it over: `hexbin`, when the axes are naturally rectangular.\n### Matrices and fields\n- `heatmap` — draws: Annotated matrix with a colourbar. Choose it over: A\n  table, when the pattern matters more than the digits.\n- `seqheat` — draws: A per-token quantity drawn on the tokens themselves.\n  Choose it over: `heatmap`, for anything measured per token — it puts\n  indices on an axis and leaves the reader rebuilding the sentence from a\n  legend.\n- `corr` — draws: Correlation matrix, diverging map centred at zero. Choose\n  it over: `heatmap`, for correlations — sign reads from colour direction.", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
````

### [51] TOOL CALL — Bash · 2026-09-25 15:58:32 UTC

```
G=/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_gen.py; python $G --example bar; sed -n 300,600p /ai-inventor/.claude/skills/aii-data-fig-gen/SKILL.md | grep -n -i -A3 "color\|colour\|yerr\|error\|aspect\|figsize\|ylim\|caption" | head -120
```

### [52] TOOL RESULT — Bash · 2026-09-25 15:58:32 UTC

````
{"stdout": "{\n  \"type\": \"bar\",\n  \"title\": \"Accuracy by benchmark\",\n  \"xlabel\": \"Benchmark\",\n  \"ylabel\": \"Accuracy (%)\",\n  \"aspect\": \"16:9\",\n  \"categories\": [\n    \"ARC\",\n    \"GSM8K\",\n    \"HumanEval\",\n    \"MMLU\"\n  ],\n  \"series\": [\n    {\n      \"label\": \"Baseline\",\n      \"values\": [\n        41.2,\n        55.8,\n        33.1,\n        62.4\n      ],\n      \"errors\": [\n        1.8,\n        2.4,\n        2.9,\n        1.1\n      ]\n    },\n    {\n      \"label\": \"Ours\",\n      \"values\": [\n        48.9,\n        67.3,\n        45.6,\n        68.1\n      ],\n      \"errors\": [\n        1.5,\n        2.0,\n        2.6,\n        1.0\n      ]\n    }\n  ]\n}\n27:- `hexbin` — draws: Hexagonal density bins with a colourbar. Choose it over:\n28-  `scatter`, past ~2000 points where it becomes a solid blob.\n29-- `hist2d` — draws: A joint distribution as a rectangular binned grid.\n30-  Choose it over: `hexbin`, when the axes are naturally rectangular.\n--\n34:- `heatmap` — draws: Annotated matrix with a colourbar. Choose it over: A\n35-  table, when the pattern matters more than the digits.\n36-- `seqheat` — draws: A per-token quantity drawn on the tokens themselves.\n37-  Choose it over: `heatmap`, for anything measured per token — it puts\n--\n41:  it over: `heatmap`, for correlations — sign reads from colour direction.\n42-- `contour` — draws: Filled contours of a 2-D field, levels labelled. Choose\n43-  it over: `heatmap`, for a smooth field like a loss surface.\n44-- `clustermap` — draws: Heatmap with rows and columns reordered into their\n--\n128:  \"aspect\": \"16:9\",\n129-  \"categories\": [\"ARC\", \"GSM8K\", \"HumanEval\"],\n130-  \"series\": [\n131:    {\"label\": \"Baseline\", \"values\": [41.2, 55.8, 33.1], \"errors\": [1.8, 2.4, 2.9]},\n132:    {\"label\": \"Ours\",     \"values\": [48.9, 67.3, 45.6], \"errors\": [1.5, 2.0, 2.6]}\n133-  ]\n134-}\n135-```\n--\n137:Keys every type takes: `title`, `aspect` (`\"W:H\"`), `width_in` (default 7.0\n138-— a full text-width figure), `font_pt`, `font_family`.\n139-\n140-Keys that depend on what the type actually draws. Passing one to a type that\n--\n151:- `xlim`, `ylim` — applies to: every type — the shared layer applies them\n152-  whatever the geometry, so these two are never refused as unread. Limits\n153-  that would crop data are refused rather than applied.\n154-- `legend_loc` — applies to: only the types that actually draw a legend,\n--\n162:- `cmap` — applies to: only the eight types that encode a value as colour —\n163-  `heatmap`, `clustermap`, `corr`, `hist2d`, `hexbin`, `contour`, `quiver`,\n164:  `seqheat`. Anywhere else it is refused: a bar chart given a colour map is\n165:  a spec expecting colour to carry a meaning that chart never encodes. The\n166-  default is already perceptually uniform (`cividis`, or `RdBu_r` where the\n167-  scale has a meaningful zero), so reach for this only with a reason.\n168-  Rainbow and cyclic maps are refused: `jet` puts a bright band in the\n--\n197:`ncols` and `aspect` both default from the panel count: the grid is squared\n198-(capped at three columns, which is the most that fits at the 7-inch text\n199-width) and the canvas is sized so each cell is about 4:3. Pinning `ncols: 4`\n200-is allowed but leaves each cell 1.75 inches wide, which is narrower than a\n--\n222:belongs in the caption, which has the full column width and as many lines as\n223-it needs.\n224-\n225-These are coarse budgets that cannot know the figure's real width — a\n--\n270:  and green bars and names two colours. Nothing about the picture looks\n271-  wrong, which is what makes it worth refusing. Naming none of them is fine:\n272-  that is a chart with one meaning, and the y-label carries it.\n273:- **A stated limit that crops the data.** `xlim`/`ylim` outside the values,\n274-  `vmin`/`vmax` outside the matrix, or an explicit `levels` list narrower than\n275:  `z`. Each one hides part of the finding while the axis or colourbar states a\n276-  range the data does not have: `vmax: 0.3` on a matrix running 0.10..0.95\n277-  painted 0.30 and 0.95 the identical yellow under a bar labelled\n278-  0.100..0.300, and `levels: [2.6..3.2]` over a field of 2.3..4.6 left 70% of\n--\n299:- **Two series a reader cannot tell apart.** The palette holds eight colours\n300-  and wraps; the dash pattern is a second channel and multiplies that to 32\n301-  for line charts, but a solid shape has no dash. A twelve-series `bar`", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
````

### [53] TOOL CALL — Bash · 2026-09-25 15:58:36 UTC

```
S=/ai-inventor/.claude/skills/aii-data-fig-gen/scripts; grep -n "def render_bar\b\|def _bar\|def bar" $S/*.py | head; grep -n "errors\|\"color\"\|'color'\|ci_low\|err_lo\|lower" $S/chart_renderers.py | head -40
```

### [54] TOOL RESULT — Bash · 2026-09-25 15:58:36 UTC

```
{"stdout": "/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_renderers_stats.py:510:def _bar_levels(runs: list[tuple[int, int]], ranks: np.ndarray) -> list[int]:\n/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_renderers.py:90:def render_bar(ax, spec: dict) -> None:\n136:            errs = s.get(\"errors\")\n144:                yerr=_error_bars(errs, f\"series[{i}].errors\", expect=n_groups) if errs else None,\n175:        errs = s.get(\"errors\")\n183:            xerr=_error_bars(errs, f\"series[{i}].errors\", expect=n) if errs else None,\n211:        colour = style[\"color\"]\n455:            medianprops={\"color\": \"#1a1a1a\", \"linewidth\": 1.4},\n645:        _error_bars(s.get(\"errors\"), \"series[0].errors\", expect=values.size)\n646:        if s.get(\"errors\")", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [55] TOOL CALL — Bash · 2026-09-25 15:58:38 UTC

```
S=/ai-inventor/.claude/skills/aii-data-fig-gen/scripts; sed -n 40,160p $S/chart_renderers.py; grep -n "def series_style" -A40 $S/chart_style.py | head -60
```

### [56] TOOL RESULT — Bash · 2026-09-25 15:58:38 UTC

```
{"stdout": "from chart_common import (\n    ink_for as _ink_for,\n)\nfrom chart_common import (\n    labels_for as _labels,\n)\nfrom chart_common import (\n    numbers as _numbers,\n)\nfrom chart_common import (\n    reject_pointless_diverging as _reject_pointless_diverging,\n)\nfrom chart_common import (\n    reject_unrenderable_categories as _reject_unrenderable_categories,\n)\nfrom chart_common import (\n    require_annotations_fit as _require_annotations_fit,\n)\nfrom chart_common import (\n    require_colour_limits_cover as _require_colour_limits_cover,\n)\nfrom chart_common import (\n    require_fittable as _require_fittable,\n)\nfrom chart_common import (\n    require_positive as _require_positive,\n)\nfrom chart_common import (\n    series_of as _series,\n)\nfrom chart_renderers_cluster import CLUSTER_RENDERERS\nfrom chart_renderers_compare import COMPARE_RENDERERS\nfrom chart_renderers_dist import DIST_RENDERERS\nfrom chart_renderers_eval import EVAL_RENDERERS\nfrom chart_renderers_extra import EXTRA_RENDERERS\nfrom chart_renderers_more import MORE_RENDERERS\nfrom chart_renderers_sets import SETS_RENDERERS\nfrom chart_renderers_stats import STATS_RENDERERS\nfrom chart_style import (\n    DIVERGING_CMAP,\n    PALETTE,\n    SEQUENTIAL_CMAP,\n    fix_log_ticks,\n    literal,\n    number,\n    place_point_label,\n    series_style,\n)\n\n\ndef render_bar(ax, spec: dict) -> None:\n    \"\"\"Grouped or stacked bars, with optional error bars.\n\n    Grouped is the default: stacking hides the individual series values,\n    which is usually the thing a results table is trying to show.\n\n    ``stacked`` turns stacking on when the total is the point rather than the\n    parts. ``annotate`` prints each bar's value above it — worth it when the\n    figure carries a results table's numbers, and not when there are enough\n    bars that the labels become the chart.\n    \"\"\"\n    series = _series(spec)\n    n_groups = max(len(s.get(\"values\") or []) for s in series)\n    cats = _labels(spec, n_groups)\n    x = np.arange(n_groups)\n    stacked = flag(spec, \"stacked\")\n\n    if stacked:\n        bottom = np.zeros(n_groups)\n        for i, s in enumerate(series):\n            vals = _numbers(s.get(\"values\"), f\"series[{i}].values\", expect=n_groups)\n            # A stack running through zero cannot be read: segments overlap,\n            # every visible height differs from its value and the sign is\n            # gone. Observed rendering [10,20,30]/[-5,-25,-10] as 5/20/20\n            # with one bar missing entirely.\n            if np.any(vals < 0):\n                raise SpecError(\n                    f\"series[{i}].values has a negative in a STACKED bar. Stacked \"\n                    \"segments are drawn end to end, so a negative overlaps the \"\n                    \"one below and every height stops matching its value. Use \"\n                    'grouped bars (drop \"stacked\") or a \"forest\" chart for signed '\n                    \"quantities.\"\n                )\n            ax.bar(\n                x,\n                vals,\n                0.62,\n                bottom=bottom,\n                label=literal(s.get(\"label\")) if s.get(\"label\") else None,\n                color=PALETTE[i % len(PALETTE)],\n            )\n            bottom += vals\n    else:\n        width = 0.8 / len(series)\n        for i, s in enumerate(series):\n            vals = _numbers(s.get(\"values\"), f\"series[{i}].values\", expect=n_groups)\n            errs = s.get(\"errors\")\n            offset = (i - (len(series) - 1) / 2) * width\n            ax.bar(\n                x + offset,\n                vals,\n                width * 0.92,\n                label=literal(s.get(\"label\")) if s.get(\"label\") else None,\n                color=PALETTE[i % len(PALETTE)],\n                yerr=_error_bars(errs, f\"series[{i}].errors\", expect=n_groups) if errs else None,\n                capsize=2.5,\n                error_kw={\"elinewidth\": 1.0, \"ecolor\": \"#333333\"},\n            )\n            if flag(spec, \"annotate\"):\n                for xi, v in zip(x + offset, vals, strict=False):\n                    ax.text(xi, v, f\"{v:.1f}\", ha=\"center\", va=\"bottom\", fontsize=8)\n\n    _reject_unrenderable_categories(cats)\n    ax.set_xticks(x)\n    ax.set_xticklabels(cats)\n    _legend(ax, spec, series)\n\n\ndef render_barh(ax, spec: dict) -> None:\n    \"\"\"Horizontal bars, one per category.\n\n83:def series_style(index: int) -> dict:\n84-    \"\"\"Colour, and past the palette's length a dash pattern too.\"\"\"\n85-    style = {\"color\": PALETTE[index % len(PALETTE)]}\n86-    if index >= len(PALETTE):\n87-        style[\"linestyle\"] = LINE_STYLES[(index // len(PALETTE)) % len(LINE_STYLES)]\n88-    return style\n89-\n90-\n91-# Sequential map for heatmaps: perceptually uniform AND colourblind-safe,\n92-# unlike the jet/rainbow maps that still show up in papers.\n93-SEQUENTIAL_CMAP = \"cividis\"\n94-# Diverging map for signed quantities (deltas, correlations).\n95-DIVERGING_CMAP = \"RdBu_r\"\n96-\n97-# Base font size in points. Figures are drawn at their final print size, so\n98-# this is what the reader actually sees — not a value scaled later.\n99-BASE_FONT_PT = 11\n100-\n101-\n102-def _sans_stack(family: str | None) -> list[str]:\n103-    \"\"\"Preference list, with an explicit ``family`` taking priority.\n104-\n105-    matplotlib uses the first entry it can resolve and never consults the\n106-    rest per-glyph, so overriding means going to the FRONT.\n107-    \"\"\"\n108-    base = [\"DejaVu Sans\", \"Helvetica\", \"Arial\", \"Liberation Sans\"]\n109-    return [family, *base] if family else base\n110-\n111-\n112-def apply_house_style(base_font_pt: int = BASE_FONT_PT, family: str | None = None) -> None:\n113-    \"\"\"Install the house style into matplotlib's global rcParams.\n114-\n115-    ``family`` puts one font ahead of the default stack — the escape hatch\n116-    for a script DejaVu does not cover (CJK, Devanagari, Thai). Without it\n117-    those figures cannot be produced at all, because the glyph gate refuses\n118-    to write a figure full of hollow boxes.\n119-\n120-    Call once before building a figure. Idempotent.\n121-    \"\"\"\n122-    plt.rcParams.update(\n123-        {", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [57] TOOL CALL — Bash · 2026-09-25 15:58:42 UTC

```
S=/ai-inventor/.claude/skills/aii-data-fig-gen/scripts; grep -n "^PALETTE" -A14 $S/chart_style.py; grep -rn "def error_bars" -A40 $S/chart_common.py | head -50
```

### [58] TOOL RESULT — Bash · 2026-09-25 15:58:42 UTC

```
{"stdout": "64:PALETTE: tuple[str, ...] = (\n65-    \"#0173B2\",  # blue\n66-    \"#DE8F05\",  # amber\n67-    \"#029E73\",  # green\n68-    \"#CC78BC\",  # violet\n69-    \"#CA9161\",  # tan\n70-    \"#949494\",  # grey\n71-    \"#ECE133\",  # yellow\n72-    \"#56B4E9\",  # sky\n73-)\n74-\n75-# Dash patterns for when the palette wraps. Past eight series the colour\n76-# repeats exactly — series 1 and 9 were pixel-identical, which makes a legend\n77-# unusable — so the line style becomes the second channel that tells them\n78-# apart. It is also the only channel that survives greyscale print past the\n/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_common.py:286:def error_bars(values, what: str, *, expect: int | None = None):\n/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_common.py-287-    \"\"\"``errors`` as a float array, refusing a negative magnitude.\n/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_common.py-288-\n/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_common.py-289-    An error bar is a DISTANCE either side of the value, so a negative one\n/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_common.py-290-    means nothing. matplotlib says as much — \"'yerr' must not contain\n/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_common.py-291-    negative values\" — but it says it about the whole array, with no series,\n/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_common.py-292-    no index and no idea which of forty numbers is wrong, where every other\n/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_common.py-293-    refusal here names the exact key. Zero is allowed: a measurement with no\n/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_common.py-294-    spread is a real result.\n/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_common.py-295-    \"\"\"\n/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_common.py-296-    import numpy as np\n/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_common.py-297-\n/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_common.py-298-    array = numbers(values, what, expect=expect)\n/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_common.py-299-    bad = np.flatnonzero(array < 0)\n/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_common.py-300-    if bad.size:\n/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_common.py-301-        first = int(bad[0])\n/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_common.py-302-        raise SpecError(\n/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_common.py-303-            f\"{what}[{first}] is {array[first]:g}. An error bar is a distance either \"\n/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_common.py-304-            f\"side of the value, so it cannot be negative — {bad.size} of \"\n/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_common.py-305-            f\"{array.size} here are. Use the magnitude of the interval.\"\n/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_common.py-306-        )\n/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_common.py-307-    return array\n/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_common.py-308-\n/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_common.py-309-\n/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_common.py-310-#: Roughly how wide one character is, as a fraction of the font size. DejaVu\n/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_common.py-311-#: Sans digits sit near 0.55 em; measured against the drawn extents rather\n/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_common.py-312-#: than taken from the font tables.\n/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_common.py-313-_DIGIT_EM = 0.55\n/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_common.py-314-\n/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_common.py-315-#: The axes ends up narrower than the figure — tick labels, the y-label and a\n/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_common.py-316-#: colourbar all take width. Measured across widths 5, 7 and 12 in: the axes\n/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_common.py-317-#: was 77-82% of the figure, so 0.8 is the conservative middle.\n/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_common.py-318-_AXES_SHARE_OF_FIGURE = 0.8\n/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_common.py-319-\n/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_common.py-320-\n/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_common.py-321-def require_annotations_fit(spec: dict, columns: int, longest: str, font_pt: float = 7.5) -> None:\n/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_common.py-322-    \"\"\"Refuse per-cell annotation the cells are too small to hold.\n/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_common.py-323-\n/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_common.py-324-    A matrix wide enough that its numbers overlap is refused anyway — by the\n/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_common.py-325-    collision gate, AFTER laying out every one of them. That is the slow way\n/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_common.py-326-    round: a 200x200 annotated heatmap took 182 seconds to arrive at \"514,943", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [59] TOOL CALL — Bash · 2026-09-25 15:59:00 UTC

```
S=/ai-inventor/.claude/skills/aii-data-fig-gen/scripts; grep -n "^def place_legend\|^def literal\|^def fit_tick_labels\|^def clear_legends_of_data\|^def fit_legends" -A25 $S/chart_style.py | grep -v '^\s*$' | head -120
```

### [60] TOOL RESULT — Bash · 2026-09-25 15:59:00 UTC

```
{"stdout": "239:def literal(text) -> str:\n240-    \"\"\"User text, with ``$`` neutralised so matplotlib prints it verbatim.\n241-\n242-    A MATCHED PAIR of dollar signs is mathtext to matplotlib, so a title like\n243-    \"Cost $5 to $9 per run\" silently renders as \"Cost 5to9 per run\" with the\n244-    currency gone and the middle word italicised. A cost figure losing its\n245-    currency symbols is precisely the kind of quiet corruption this renderer\n246-    is built to refuse, and unlike a bad number it survives review because\n247-    the sentence still reads.\n248-\n249-    Escaping rather than rejecting: a literal dollar is what a spec author\n250-    means essentially every time. The cost is that mathtext is unavailable —\n251-    use Unicode for superscripts (``R²``, ``10⁻³``), which the rest of this\n252-    module already does.\n253-\n254-    RIGHT-TO-LEFT text is refused here instead. matplotlib applies no bidi\n255-    reordering and no Arabic joining: it draws the code points left to right\n256-    in their isolated forms, so a Hebrew or Arabic label comes out reversed\n257-    and unjoined. The glyphs are all in DejaVu, so the missing-glyph gate —\n258-    the one that catches CJK — sees nothing wrong and the figure ships. This\n259-    is the single funnel every piece of user text in the catalogue passes\n260-    through, which is why the check lives here.\n261-    \"\"\"\n262-    text = str(text)\n263-    _reject_bidi(text)\n264-    return text.replace(\"$\", r\"\\$\")\n--\n689:def place_legend(parent, *args, **kwargs):\n690-    \"\"\"Draw a legend and record the call, so ``fit_legends`` can reflow it.\n691-\n692-    Every legend in the catalogue goes through here, whether its parent is an\n693-    axes or the figure. The recording is what makes a reflow possible at all:\n694-    ``Legend.set_ncols`` stores the new column count and does NOT re-pack the\n695-    legend box, so calling it changes nothing a reader would ever see — a\n696-    four-entry legend measured 700 px before and 700 px after. Narrowing means\n697-    building the legend again, and that needs the arguments it was built with.\n698-    \"\"\"\n699-    legend = parent.legend(*args, **kwargs)\n700-    figure = parent if isinstance(parent, plt.Figure) else parent.figure\n701-    figure.aii_legends = [*getattr(figure, \"aii_legends\", []), (parent, args, kwargs, legend)]\n702-    return legend\n703-\n704-\n705-def _room_for(legend, parent, fig, renderer) -> float:\n706-    \"\"\"How wide this legend is allowed to be, in pixels.\n707-\n708-    A legend sitting INSIDE its axes has the axes' width and no more. One\n709-    anchored below or beside the axes is centred on it but spills freely into\n710-    the figure margins, so the page is its limit — measuring that one against\n711-    the axes made ``speedup`` shed a column it did not need to at 21:9, which\n712-    turned a one-row legend into two and dropped the second row onto the\n713-    x-axis label. Which case applies is read off the drawn figure rather than\n714-    from the arguments, because ``loc`` and ``bbox_to_anchor`` together have\n--\n726:def fit_legends(fig) -> None:\n727-    \"\"\"Reflow any legend that is wider than the space it has to sit in.\n728-\n729-    The column count is chosen before layout runs and whether it fits is only\n730-    knowable after. Three entries in one row measured 695 px on a 700 px\n731-    canvas, and constrained layout answers a legend wider than its axes by\n732-    shrinking the axes — on EVERY draw, without converging, so the figure\n733-    collapsed to nothing and was refused outright. Dropping a column at a time\n734-    until it fits leaves the axes stable instead.\n735-\n736-    A legend that has been re-parented with ``add_artist`` is left alone:\n737-    replaying ``ax.legend`` would overwrite whichever legend is currently the\n738-    axes' own, and ``bubble`` deliberately carries two — a colour key and a\n739-    size key. It keeps its columns; if it genuinely does not fit, the layout\n740-    gate refuses the figure with a message rather than shipping it.\n741-    \"\"\"\n742-    fig.canvas.draw()\n743-    renderer = fig.canvas.get_renderer()\n744-    recorded = getattr(fig, \"aii_legends\", [])\n745-    changed = False\n746-    for index, (parent, args, kwargs, legend) in enumerate(list(recorded)):\n747-        still_attached = legend in fig.legends if parent is fig else legend is parent.get_legend()\n748-        if not still_attached:\n749-            continue\n750-        ncols = kwargs.get(\"ncols\", 1)\n751-        while ncols > 1:\n--\n820:def clear_legends_of_data(fig) -> None:\n821-    \"\"\"Move an inside legend that landed on the data out of the axes.\n822-\n823-    ``loc=\"best\"`` avoids the data only where free space exists. A horizontal\n824-    chart has none to buy: the y-headroom trick that clears a bar chart's\n825-    legend does nothing for a Gantt, whose rows are fixed and whose bars start\n826-    wherever the schedule says. ``timeline``'s legend covered 1,674 px of the\n827-    \"Paper writing\" bar — its LEFT END, so a reader could not see when the\n828-    task began — in the shipped catalogue example.\n829-\n830-    ``draw_legend`` already moves a legend out past six entries, or when the\n831-    plot area is full by construction. That is a guess made before layout; this\n832-    is the measurement after it, and it catches the cases the guess does not.\n833-    \"\"\"\n834-    fig.canvas.draw()\n835-    renderer = fig.canvas.get_renderer()\n836-    recorded = getattr(fig, \"aii_legends\", [])\n837-    changed = False\n838-    for index, (parent, _args, kwargs, legend) in enumerate(list(recorded)):\n839-        if parent is fig or legend is not parent.get_legend():\n840-            continue  # already outside, or replaced by a later pass\n841-        if _data_hidden(parent, legend, renderer)[0] < _LEGEND_HIDES:\n842-            continue\n843-        handles, labels = legend.legend_handles, [t.get_text() for t in legend.get_texts()]\n844-        if not handles or content_places(fig) != 1:\n845-            # A panel cell has no figure-level strip of its own to move into;\n--\n939:def fit_tick_labels(fig) -> None:\n940-    \"\"\"Wrap, then tilt, then stand up any x tick labels that would collide.\n941-\n942-    This has to run POST-LAYOUT and measure the AXES. The rule it replaces\n943-    estimated a characters-per-slot budget from the FIGURE width, which is\n944-    right for a lone chart and wrong by the column count for every panel: in\n945-    a three-column grid each axes gets a third of the width, the estimate\n946-    said the labels fit, and \"GSM8K HumanEval MMLU\" printed on top of itself\n947-    as ``GSM8kmanEvalMLU``. Unreadable, and at exit 0.\n948-\n949-    A numeric axis is handled separately, by ``_thin_numeric_ticks``: its\n950-    labels are the locator's own numbers rather than the caller's names, so", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [61] THINKING · 2026-09-25 15:59:14 UTC

```
The standard bar chart tool can't handle these asymmetric bootstrap CIs, so I'm writing a custom renderer on top of the house style that pulls everything from the spec JSON.
```

### [62] TOOL CALL — Bash · 2026-09-25 15:59:14 UTC

```
W=/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_report_5; B=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/results; python3 - <<EOF
import json
a=json.load(open("$B/analysis.json"))['a_tables']
subs=[('R_AB pooled','R_AB pooled'),('R_AB L25','R_AB L25'),('R_AB L20','R_AB L20'),('R_AB EXC','R_AB EXC'),('R_AB CTRL','R_AB CTRL'),('R_AB long (L25+L20+EXC)','R_AB long pool'),('R_A pooled L20+EXC','R_A L20+EXC')]
mets=[('p_peer_text','PEER+TEXT','#D55E00'),('c_score_align','c_score_align','#0072B2'),('nf_c_score','NF c_score','#009E73'),('l2_bow','L2-bow','#E69F00'),('l3_z3','L3','#CC79A7'),('judge_local_qwen8b_disg','Local judge','#8C8C8C')]
series=[]
for key,lab,col in mets:
    v=[];lo=[];hi=[]
    for s,_ in subs:
        m = a[s]['vs_judge_local_qwen8b_disg']['metrics'][key] if key.startswith('judge') else a[s]['metrics'][key]
        v.append(round(m['auroc'],3)); lo.append(round(m['ci'][0],3)); hi.append(round(m['ci'][1],3))
    series.append({"label":lab,"source_key":key,"color":col,"values":v,"ci_low":lo,"ci_high":hi})
spec={
 "figure_id":"fig_dev_set_auroc",
 "renderer":"render_fig_dev_set_auroc.py (hand-written; chart_gen 'bar' supports only symmetric errors, these are asymmetric 95% sentence-cluster bootstrap CIs)",
 "source":{"artifact":"gen_art_experiment_5 (art_TaxJRnPcJMuZ), iter_2 of run_u75jRHUss0zo","file":"results/analysis.json -> a_tables[<subset>].metrics[<key>] (auroc, ci); Local judge from a_tables[<subset>].vs_judge_local_qwen8b_disg.metrics.judge_local_qwen8b_disg","cross_check":"results/tables.md table (a) and run_report.yaml section 2.2 agree to 3 d.p."},
 "aspect":"16:9","width_in":7.0,
 "ylabel":"AUROC, ERROR vs CORRECT (0.5 = chance)",
 "xlabel":"Dataset E subset (label tier, stratum)",
 "ylim":[0.3,0.95],
 "bar_baseline":0.5,
 "categories":[d for _,d in subs],
 "category_source_names":[s for s,_ in subs],
 "n_items":[a[s]['n'] for s,_ in subs],
 "n_error":[a[s]['n_error'] for s,_ in subs],
 "n_correct":[a[s]['n_correct'] for s,_ in subs],
 "separator_before_index":6,
 "series":series}
json.dump(spec,open("$W/fig_dev_set_auroc_spec.json","w"),indent=1)
for s in series: print(s['label'],s['values'])
print(spec['n_items'],spec['n_error'],spec['n_correct'])
EOF
```

### [63] TOOL RESULT — Bash · 2026-09-25 15:59:14 UTC

```
{"stdout": "PEER+TEXT [0.79, 0.755, 0.747, 0.777, 0.708, 0.768, 0.818]\nc_score_align [0.782, 0.712, 0.722, 0.814, 0.742, 0.759, 0.86]\nNF c_score [0.743, 0.651, 0.643, 0.782, 0.741, 0.704, 0.802]\nL2-bow [0.734, 0.722, 0.715, 0.669, 0.613, 0.717, 0.678]\nL3 [0.579, 0.56, 0.547, 0.62, 0.49, 0.58, 0.587]\nLocal judge [0.712, 0.664, 0.683, 0.663, 0.739, 0.653, 0.554]\n[2686, 873, 821, 606, 386, 2300, 449] [1822, 697, 592, 384, 149, 1673, 261] [864, 176, 229, 222, 237, 627, 188]", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [64] TOOL CALL — Write · 2026-09-25 15:59:38 UTC

```
File: /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_report_5/render_fig_dev_set_auroc.py

"""Render fig_dev_set_auroc from fig_dev_set_auroc_spec.json.

Grouped bars of item-level AUROC per dataset-E subset, one bar per metric,
with asymmetric 95% sentence-cluster bootstrap CIs. Hand-written because the
catalogue `bar` type only draws symmetric error bars; it uses the
aii-data-fig-gen house style and layout passes so it matches the other figures.

Usage: python render_fig_dev_set_auroc.py [--spec SPEC] [--out STEM]
"""

import argparse
import json
import sys
import warnings
from pathlib import Path

SKILL_SCRIPTS = Path("/ai-inventor/.claude/skills/aii-data-fig-gen/scripts")
sys.path.insert(0, str(SKILL_SCRIPTS))

import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from chart_geometry import assert_text_is_legible, fit_point_labels  # noqa: E402
from chart_style import (  # noqa: E402
    apply_house_style,
    assert_axis_names_are_unique,
    assert_legends_clear_of_data,
    assert_series_are_distinguishable,
    clear_legends_of_data,
    fit_legends,
    fit_tick_labels,
    fit_titles,
    literal,
    place_legend,
    rasterize_dense_clouds,
)

HERE = Path(__file__).resolve().parent


def check_spec(spec: dict) -> None:
    """Refuse a spec whose CIs do not bracket their values or fall outside ylim."""
    n = len(spec["categories"])
    lo_lim, hi_lim = spec["ylim"]
    for s in spec["series"]:
        for key in ("values", "ci_low", "ci_high"):
            if len(s[key]) != n:
                raise ValueError(f"{s['label']}.{key} has {len(s[key])} entries, expected {n}")
        for i, (v, lo, hi) in enumerate(zip(s["values"], s["ci_low"], s["ci_high"], strict=True)):
            if not lo <= v <= hi:
                raise ValueError(f"{s['label']}[{i}]: CI [{lo}, {hi}] does not contain {v}")
            if lo < lo_lim or hi > hi_lim:
                raise ValueError(f"{s['label']}[{i}]: CI [{lo}, {hi}] is cropped by ylim {spec['ylim']}")


def render(spec: dict, out: Path) -> None:
    check_spec(spec)
    apply_house_style()
    w = spec.get("width_in", 7.0)
    aw, ah = (float(t) for t in spec.get("aspect", "16:9").split(":"))
    with warnings.catch_warnings(record=True):
        fig, ax = plt.subplots(figsize=(w, w * ah / aw), layout="constrained")

        cats = spec["categories"]
        n_groups, n_series = len(cats), len(spec["series"])
        x = np.arange(n_groups)
        width = 0.84 / n_series
        base = spec["bar_baseline"]
        for i, s in enumerate(spec["series"]):
            vals = np.asarray(s["values"], float)
            yerr = np.vstack([vals - np.asarray(s["ci_low"]), np.asarray(s["ci_high"]) - vals])
            ax.bar(
                x + (i - (n_series - 1) / 2) * width,
                vals - base,
                width * 0.9,
                bottom=base,
                color=s["color"],
                label=literal(s["label"]),
                yerr=yerr,
                capsize=1.6,
                error_kw={"elinewidth": 0.7, "ecolor": "#333333", "capthick": 0.7},
                zorder=2,
            )

        ax.axhline(base, color="#555555", linewidth=0.8, linestyle="--", zorder=1)
        sep = spec.get("separator_before_index")
        if sep is not None:
            ax.axvline(sep - 0.5, color="#999999", linewidth=0.8, linestyle=":", zorder=1)

        ticks = [f"{literal(c)}\n(n={n:,})" for c, n in zip(cats, spec["n_items"], strict=True)]
        ax.set_xticks(x)
        ax.set_xticklabels(ticks)
        ax.set_xlim(-0.5, n_groups - 0.5)
        ax.set_ylim(*spec["ylim"])
        ax.set_ylabel(literal(spec["ylabel"]))
        ax.set_xlabel(literal(spec["xlabel"]))
        ax.grid(axis="x", visible=False)

        place_legend(
            ax,
            loc="lower center",
            bbox_to_anchor=(0.5, 1.0),
            ncols=n_series,
            frameon=False,
            handlelength=1.2,
            columnspacing=1.0,
        )
        fit_legends(fig)
        clear_legends_of_data(fig)
        fit_tick_labels(fig)
        fit_titles(fig)
        clear_legends_of_data(fig)
        fit_point_labels(fig)
        rasterize_dense_clouds(fig)
        assert_text_is_legible(fig)
        assert_legends_clear_of_data(fig)
        assert_series_are_distinguishable(fig)
        assert_axis_names_are_unique(fig)
        fig.savefig(out.with_suffix(".pdf"))
        fig.savefig(out.with_suffix(".png"), dpi=200)
    plt.close(fig)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--spec", default=str(HERE / "fig_dev_set_auroc_spec.json"))
    p.add_argument("--out", default=str(HERE / "fig_dev_set_auroc_v0"))
    a = p.parse_args()
    render(json.loads(Path(a.spec).read_text()), Path(a.out))
    print(f"wrote {a.out}.pdf and {a.out}.png")


if __name__ == "__main__":
    main()
```

### [65] TOOL RESULT — Write · 2026-09-25 15:59:38 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_report_5/render_fig_dev_set_auroc.py", "content": "\"\"\"Render fig_dev_set_auroc from fig_dev_set_auroc_spec.json.\n\nGrouped bars of item-level AUROC per dataset-E subset, one bar per metric,\nwith asymmetric 95% sentence-cluster bootstrap CIs. Hand-written because the\ncatalogue `bar` type only draws symmetric error bars; it uses the\naii-data-fig-gen house style and layout passes so it matches the other figures.\n\nUsage: python render_fig_dev_set_auroc.py [--spec SPEC] [--out STEM]\n\"\"\"\n\nimport argparse\nimport json\nimport sys\nimport warnings\nfrom pathlib import Path\n\nSKILL_SCRIPTS = Path(\"/ai-inventor/.claude/skills/aii-data-fig-gen/scripts\")\nsys.path.insert(0, str(SKILL_SCRIPTS))\n\nimport matplotlib  # noqa: E402\n\nmatplotlib.use(\"Agg\")\nimport matplotlib.pyplot as plt  # noqa: E402\nimport numpy as np  # noqa: E402\nfrom chart_geometry import assert_text_is_legible, fit_point_labels  # noqa: E402\nfrom chart_style import (  # noqa: E402\n    apply_house_style,\n    assert_axis_names_are_unique,\n    assert_legends_clear_of_data,\n    assert_series_are_distinguishable,\n    clear_legends_of_data,\n    fit_legends,\n    fit_tick_labels,\n    fit_titles,\n    literal,\n    place_legend,\n    rasterize_dense_clouds,\n)\n\nHERE = Path(__file__).resolve().parent\n\n\ndef check_spec(spec: dict) -> None:\n    \"\"\"Refuse a spec whose CIs do not bracket their values or fall outside ylim.\"\"\"\n    n = len(spec[\"categories\"])\n    lo_lim, hi_lim = spec[\"ylim\"]\n    for s in spec[\"series\"]:\n        for key in (\"values\", \"ci_low\", \"ci_high\"):\n            if len(s[key]) != n:\n                raise ValueError(f\"{s['label']}.{key} has {len(s[key])} entries, expected {n}\")\n        for i, (v, lo, hi) in enumerate(zip(s[\"values\"], s[\"ci_low\"], s[\"ci_high\"], strict=True)):\n            if not lo <= v <= hi:\n                raise ValueError(f\"{s['label']}[{i}]: CI [{lo}, {hi}] does not contain {v}\")\n            if lo < lo_lim or hi > hi_lim:\n                raise ValueError(f\"{s['label']}[{i}]: CI [{lo}, {hi}] is cropped by ylim {spec['ylim']}\")\n\n\ndef render(spec: dict, out: Path) -> None:\n    check_spec(spec)\n    apply_house_style()\n    w = spec.get(\"width_in\", 7.0)\n    aw, ah = (float(t) for t in spec.get(\"aspect\", \"16:9\").split(\":\"))\n    with warnings.catch_warnings(record=True):\n        fig, ax = plt.subplots(figsize=(w, w * ah / aw), layout=\"constrained\")\n\n        cats = spec[\"categories\"]\n        n_groups, n_series = len(cats), len(spec[\"series\"])\n        x = np.arange(n_groups)\n        width = 0.84 / n_series\n        base = spec[\"bar_baseline\"]\n        for i, s in enumerate(spec[\"series\"]):\n            vals = np.asarray(s[\"values\"], float)\n            yerr = np.vstack([vals - np.asarray(s[\"ci_low\"]), np.asarray(s[\"ci_high\"]) - vals])\n            ax.bar(\n                x + (i - (n_series - 1) / 2) * width,\n                vals - base,\n                width * 0.9,\n                bottom=base,\n                color=s[\"color\"],\n                label=literal(s[\"label\"]),\n                yerr=yerr,\n                capsize=1.6,\n                error_kw={\"elinewidth\": 0.7, \"ecolor\": \"#333333\", \"capthick\": 0.7},\n                zorder=2,\n            )\n\n        ax.axhline(base, color=\"#555555\", linewidth=0.8, linestyle=\"--\", zorder=1)\n        sep = spec.get(\"separator_before_index\")\n        if sep is not None:\n            ax.axvline(sep - 0.5, color=\"#999999\", linewidth=0.8, linestyle=\":\", zorder=1)\n\n        ticks = [f\"{literal(c)}\\n(n={n:,})\" for c, n in zip(cats, spec[\"n_items\"], strict=True)]\n        ax.set_xticks(x)\n        ax.set_xticklabels(ticks)\n        ax.set_xlim(-0.5, n_groups - 0.5)\n        ax.set_ylim(*spec[\"ylim\"])\n        ax.set_ylabel(literal(spec[\"ylabel\"]))\n        ax.set_xlabel(literal(spec[\"xlabel\"]))\n        ax.grid(axis=\"x\", visible=False)\n\n        place_legend(\n            ax,\n            loc=\"lower center\",\n            bbox_to_anchor=(0.5, 1.0),\n            ncols=n_series,\n            frameon=False,\n            handlelength=1.2,\n            columnspacing=1.0,\n        )\n        fit_legends(fig)\n        clear_legends_of_data(fig)\n        fit_tick_labels(fig)\n        fit_titles(fig)\n        clear_legends_of_data(fig)\n        fit_point_labels(fig)\n        rasterize_dense_clouds(fig)\n        assert_text_is_legible(fig)\n        assert_legends_clear_of_data(fig)\n        assert_series_are_distinguishable(fig)\n        assert_axis_names_are_unique(fig)\n        fig.savefig(out.with_suffix(\".pdf\"))\n        fig.savefig(out.with_suffix(\".png\"), dpi=200)\n    plt.close(fig)\n\n\ndef main() -> None:\n    p = argparse.ArgumentParser()\n    p.add_argument(\"--spec\", default=str(HERE / \"fig_dev_set_auroc_spec.json\"))\n    p.add_argument(\"--out\", default=str(HERE / \"fig_dev_set_auroc_v0\"))\n    a = p.parse_args()\n    render(json.loads(Path(a.spec).read_text()), Path(a.out))\n    print(f\"wrote {a.out}.pdf and {a.out}.png\")\n\n\nif __name__ == \"__main__\":\n    main()\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [66] TOOL CALL — Bash · 2026-09-25 15:59:38 UTC

```
python render_fig_dev_set_auroc.py
```

### [67] TOOL RESULT — Bash · 2026-09-25 15:59:40 UTC

```
{"stdout": "wrote /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_report_5/fig_dev_set_auroc_v0.pdf and /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_report_5/fig_dev_set_auroc_v0.png", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [68] TOOL CALL — Read · 2026-09-25 15:59:42 UTC

```
/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_report_5/fig_dev_set_auroc_v0.png
```

### [69] TOOL RESULT — Read · 2026-09-25 15:59:42 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [70] ASSISTANT · 2026-09-25 15:59:50 UTC

```
Two fixes needed: the y-label is clipped, and the tick labels got tilted. I'm shortening the y-label and splitting the tick labels across lines.
```

### [71] TOOL CALL — Bash · 2026-09-25 15:59:50 UTC

```
python3 - <<'EOF'
import json
p='fig_dev_set_auroc_spec.json'; s=json.load(open(p))
s['ylabel']="AUROC (0.5 = chance)"
s['xlabel']="Dataset E subset (label tier, sentence stratum; n = scored items)"
s['tick_labels']=["R_AB\npooled","R_AB\nL25","R_AB\nL20","R_AB\nEXC","R_AB\nCTRL","R_AB\nlong pool","R_A\nL20+EXC"]
json.dump(s,open(p,'w'),indent=1)
EOF
sed -i 's|ticks = \[f"{literal(c)}\\n(n={n:,})" for c, n in zip(cats, spec\["n_items"\], strict=True)\]|labels = spec.get("tick_labels", cats)\n        ticks = [f"{literal(c)}\\nn={n:,}" for c, n in zip(labels, spec["n_items"], strict=True)]|' render_fig_dev_set_auroc.py
grep -n "ticks = \|labels = spec" render_fig_dev_set_auroc.py; python render_fig_dev_set_auroc.py
```

### [72] TOOL RESULT — Bash · 2026-09-25 15:59:52 UTC

```
{"stdout": "92:        labels = spec.get(\"tick_labels\", cats)\n93:        ticks = [f\"{literal(c)}\\nn={n:,}\" for c, n in zip(labels, spec[\"n_items\"], strict=True)]\nwrote /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_report_5/fig_dev_set_auroc_v0.pdf and /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_report_5/fig_dev_set_auroc_v0.png", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [73] TOOL CALL — Read · 2026-09-25 15:59:54 UTC

```
/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_report_5/fig_dev_set_auroc_v0.png
```

### [74] TOOL RESULT — Read · 2026-09-25 15:59:55 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [75] ASSISTANT · 2026-09-25 16:00:02 UTC

```
Numbers and layout look right. The legend's last entry sits at the right edge, so I'm tightening the column spacing slightly and re-rendering.
```

### [76] TOOL CALL — Bash · 2026-09-25 16:00:02 UTC

```
sed -i 's/columnspacing=1.0/columnspacing=0.8/' render_fig_dev_set_auroc.py && python render_fig_dev_set_auroc.py && python3 -c "
from PIL import Image; import numpy as np
a=np.asarray(Image.open('fig_dev_set_auroc_v0.png').convert('L')); print(a.shape); cols=np.where((a[:80]<128).any(0))[0]; print('legend ink x-range',cols.min(),cols.max())"; pdffonts fig_dev_set_auroc_v0.pdf 2>/dev/null | head -5
```

### [77] TOOL RESULT — Bash · 2026-09-25 16:00:04 UTC

```
{"stdout": "wrote /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_report_5/fig_dev_set_auroc_v0.pdf and /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_report_5/fig_dev_set_auroc_v0.png\n(787, 1400)\nlegend ink x-range 118 1373\nname                                 type              encoding         emb sub uni object ID\n------------------------------------ ----------------- ---------------- --- --- --- ---------\nENZJKE+DejaVuSans                    CID TrueType      Identity-H       yes yes yes     27  0", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [78] TOOL CALL — Read · 2026-09-25 16:00:06 UTC

```
/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_report_5/fig_dev_set_auroc_v0.png
```

### [79] TOOL RESULT — Read · 2026-09-25 16:00:07 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [80] ASSISTANT · 2026-09-25 16:00:19 UTC

```
The figure is clean. Now I'm writing the README, the manifest, and the structured output.
```

### [81] TOOL CALL — Bash · 2026-09-25 16:00:19 UTC

````
ls -la && du -sh . && cat > .aii/manifest.yaml <<'EOF'
# Nothing in this workspace is heavy: the figure (PDF/PNG), its JSON spec and the
# render script are all well under the 10 MB auto-keep floor, and no cache
# directories were created. No keep/delete decisions are required.
entries: []
EOF
cat > README.md <<'EOF'
# fig_dev_set_auroc — Development set E AUROCs

This folder holds a publication data figure. It shows item-level AUROC (ERROR vs CORRECT) for six
gold-free NL→FOL faithfulness metrics on seven subsets of development dataset E. Error bars are
95% sentence-cluster bootstrap CIs.

## Provenance
We read every plotted number back from the run's experiment output. None was copied from the draft paper.
- Source: `gen_art_experiment_5` (artifact `art_TaxJRnPcJMuZ`), file `results/analysis.json`.
  - AUROCs and CIs come from `a_tables[<subset>].metrics[<key>]`, using keys `p_peer_text`,
    `c_score_align`, `nf_c_score`, `l2_bow` and `l3_z3`.
  - The local judge comes from
    `a_tables[<subset>].vs_judge_local_qwen8b_disg.metrics.judge_local_qwen8b_disg`. This is the
    disguised Qwen3-8B judge.
- Cross-check: the values match that artifact's `results/tables.md` table (a) and the run report
  §2.2 to 3 d.p.

## Layout
- `fig_dev_set_auroc_v0.pdf` is the deliverable (vector, Type-42 fonts).
- `fig_dev_set_auroc_v0.png` is a 200-dpi preview.
- `fig_dev_set_auroc_spec.json` is the figure's source. It holds every value, CI bound, n, colour
  and label, plus the provenance keys.
- `render_fig_dev_set_auroc.py` renders the spec. It uses the aii-data-fig-gen house style and its
  layout and legibility gates. We hand-wrote it because the catalogue `bar` type draws only
  symmetric error bars, and these CIs are asymmetric.

## Run
```bash
python render_fig_dev_set_auroc.py --spec fig_dev_set_auroc_spec.json --out fig_dev_set_auroc_v0
```
This needs matplotlib and numpy, plus the aii-data-fig-gen skill scripts at
`/ai-inventor/.claude/skills/aii-data-fig-gen/scripts`.

## Restoring removed files
We removed nothing. `.aii/manifest.yaml` has no `delete` entries, because every file is small text or
a small figure.
EOF
ls .aii
````

### [82] TOOL RESULT — Bash · 2026-09-25 16:00:19 UTC

```
{"stdout": "total 3412\ndrwxr-xr-x   3 root root 1043434 Sep 25 16:00 .\ndrwxr-xr-x  14 root root 2003386 Sep 25 15:54 ..\ndrwxr-xr-x   2 root root       1 Sep 25 15:54 .aii\n-rw-------   1 root root      54 Sep 25 15:55 .aii_claude_session.json\n-rw-r--r--   1 root root  326952 Sep 25 16:00 .repl_agent.ptylog\n-rw-r--r--   1 root root    3723 Sep 25 15:59 fig_dev_set_auroc_spec.json\n-rw-r--r--   1 root root   20070 Sep 25 16:00 fig_dev_set_auroc_v0.pdf\n-rw-r--r--   1 root root   89082 Sep 25 16:00 fig_dev_set_auroc_v0.png\n-rw-r--r--+  1 root root    4886 Sep 25 16:00 render_fig_dev_set_auroc.py\n1.5M\t.\nmanifest.yaml", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [83] ASSISTANT · 2026-09-25 16:00:31 UTC

```
The README and the script both contain an absolute server path, and that isn't allowed in published files. I'm replacing it with an env var plus a search of the script's parent directories.
```

### [84] TOOL CALL — Bash · 2026-09-25 16:00:31 UTC

```
python3 - <<'EOF'
p='render_fig_dev_set_auroc.py'; s=open(p).read()
old='SKILL_SCRIPTS = Path("/ai-inventor/.claude/skills/aii-data-fig-gen/scripts")\n'
new='''HERE = Path(__file__).resolve().parent
_SKILL_REL = Path(".claude/skills/aii-data-fig-gen/scripts")
# $AII_DATA_FIG_GEN_SCRIPTS wins; otherwise take the first ancestor holding the skill.
SKILL_SCRIPTS = Path(
    os.environ.get("AII_DATA_FIG_GEN_SCRIPTS")
    or next((d / _SKILL_REL for d in HERE.parents if (d / _SKILL_REL).is_dir()), _SKILL_REL)
)
'''
assert old in s; s=s.replace(old,new)
s=s.replace('import json\nimport sys','import json\nimport os\nimport sys')
s=s.replace('\nHERE = Path(__file__).resolve().parent\n\n\ndef check_spec','\n\ndef check_spec')
open(p,'w').write(s)
r=open('README.md').read()
r=r.replace("This needs matplotlib and numpy, plus the aii-data-fig-gen skill scripts at\n`/ai-inventor/.claude/skills/aii-data-fig-gen/scripts`.",
"This needs matplotlib and numpy, plus the aii-data-fig-gen skill's `scripts/` directory. The script\nfinds `.claude/skills/aii-data-fig-gen/scripts` in any parent directory. To point it elsewhere, set\n`AII_DATA_FIG_GEN_SCRIPTS`.")
open('README.md','w').write(r)
EOF
grep -n "ai-inventor" README.md render_fig_dev_set_auroc.py fig_dev_set_auroc_spec.json; sed -n 12,30p render_fig_dev_set_auroc.py; python render_fig_dev_set_auroc.py && md5sum fig_dev_set_auroc_v0.png
```

### [85] TOOL RESULT — Bash · 2026-09-25 16:00:33 UTC

```
{"stdout": "import json\nimport os\nimport sys\nimport warnings\nfrom pathlib import Path\n\nHERE = Path(__file__).resolve().parent\n_SKILL_REL = Path(\".claude/skills/aii-data-fig-gen/scripts\")\n# $AII_DATA_FIG_GEN_SCRIPTS wins; otherwise take the first ancestor holding the skill.\nSKILL_SCRIPTS = Path(\n    os.environ.get(\"AII_DATA_FIG_GEN_SCRIPTS\")\n    or next((d / _SKILL_REL for d in HERE.parents if (d / _SKILL_REL).is_dir()), _SKILL_REL)\n)\nsys.path.insert(0, str(SKILL_SCRIPTS))\n\nimport matplotlib  # noqa: E402\n\nmatplotlib.use(\"Agg\")\nimport matplotlib.pyplot as plt  # noqa: E402\nwrote /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_report_5/fig_dev_set_auroc_v0.pdf and /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_report_5/fig_dev_set_auroc_v0.png\n638bf184b59a96e646cdeda65a104833  fig_dev_set_auroc_v0.png", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [86] TOOL CALL — Bash · 2026-09-25 16:00:55 UTC

```
python3 - <<'EOF'
import json
caption=("Item-level AUROC for separating ERROR from CORRECT candidates on development dataset E. "
"Each group is one subset: the R\\_AB population (label tiers A+B) pooled (n = 2,686 items; 1,822 ERROR, 864 CORRECT, 292 sentences), its L25, L20, exception (EXC) and control (CTRL) strata, the long pool (L25+L20+EXC), and the tier-A-only R\\_A L20+EXC subset. The R\\_A subset sits to the right of the dotted line, and n below each group counts its scored items. "
"Bars are PEER+TEXT (vermillion), c\\_score\\_align (blue), NF c\\_score (green), L2-bow (orange), L3 (pink) and the disguised local Qwen3-8B judge (grey). "
"Bars start at the dashed chance line (AUROC = 0.5), and whiskers are 95\\% sentence-cluster bootstrap CIs. "
"The two consensus-based scores lead on every subset. PEER+TEXT is highest on R\\_AB pooled (0.790), L25, L20 and the long pool (0.768). c\\_score\\_align is highest on EXC (0.814), CTRL and R\\_A L20+EXC (0.860), and on every subset its interval overlaps PEER+TEXT's. "
"The local judge and L3 fall furthest behind on the long, exception-heavy R\\_A L20+EXC subset (0.554 and 0.587). No metric separates clearly from the others on CTRL, where the intervals are widest.")
summary=("Grouped bar chart of item-level AUROC (ERROR vs CORRECT) on development dataset E. It has 7 subsets x 6 metrics = 42 bars, each with an asymmetric 95% sentence-cluster bootstrap CI. "
"Provenance: the evidence check flagged the run's headline as a 'lead', so we traced every value to the experiment artifact that produced it. That artifact is gen_art_experiment_5 (art_TaxJRnPcJMuZ), file results/analysis.json. Metrics come from a_tables[subset].metrics[p_peer_text|c_score_align|nf_c_score|l2_bow|l3_z3], and the local judge from vs_judge_local_qwen8b_disg. "
"All 42 point values match the specification and that artifact's tables.md to 3 d.p.; none was invented or dropped. The spec gave values for only two subsets, and we read the other five from the artifact. The CIs and the local-judge CIs also come from analysis.json. "
"All six named comparators appear as bars: PEER+TEXT, c_score_align, NF c_score, L2-bow, L3 and Local judge. "
"Why hand-written: chart_gen's 'bar' type accepts only symmetric errors and a fixed palette. We wrote render_fig_dev_set_auroc.py on the house style and ran every layout and legibility gate (fit_legends, clear_legends_of_data x2, fit_tick_labels, fit_titles, fit_point_labels, assert_text_is_legible, assert_legends_clear_of_data, assert_series_are_distinguishable, assert_axis_names_are_unique). It reads everything from fig_dev_set_auroc_spec.json and refuses a CI that does not bracket its value or is cropped by ylim. "
"Colours follow the specification with Okabe-Ito colourblind-safe shades: red becomes vermillion and purple becomes reddish-purple/pink. The background is white, the font is DejaVu Sans, and the canvas is 16:9 at 7 in. "
"Axis: the y range is 0.3-0.95 rather than the spec's 0.4-0.95, because the L3 CTRL CI reaches 0.367 and would otherwise be cropped. Bars start at the chance line 0.5, so bar length is discrimination above chance and the one below-chance value (L3 CTRL, 0.490) shows as a short downward bar. "
"Fixes across renders: a clipped y-label was shortened, auto-tilted tick labels became three-line upright labels with per-subset n, and legend column spacing was tightened. "
"Caption correction: the draft said PEER+TEXT leads on ALL subsets, with its largest advantage on long exception sentences. The data do not support that. c_score_align is higher on EXC, CTRL and R_A L20+EXC, and the caption now says so.")
out={"title":"Faithfulness metric accuracy across sentence subsets","summary":summary,"caption":caption,
"out_expected_files":{"image_path":"fig_dev_set_auroc_v0.pdf"}}
assert 500<=len(summary)<=5000 and len(caption)<=2000, (len(summary),len(caption))
json.dump(out,open('.terminal_claude_agent_struct_out.json','w'),indent=1)
print(len(summary),len(caption))
EOF
```

### [87] TOOL RESULT — Bash · 2026-09-25 16:00:55 UTC

```
{"stdout": "2368 1167", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [88] TOOL CALL — Bash · 2026-09-25 16:01:03 UTC

```
python3 - <<'EOF'
import json
p='.terminal_claude_agent_struct_out.json'; o=json.load(open(p))
old="The local judge and L3 fall furthest behind on the long, exception-heavy R\\_A L20+EXC subset (0.554 and 0.587). "
assert old in o['caption']
o['caption']=o['caption'].replace(old,"Both consensus scores sit above the local judge on every subset except CTRL. The gap is widest on the long, exception-clause R\\_A L20+EXC subset, where the judge falls to 0.554. L3 stays near chance throughout. ")
json.dump(o,open(p,'w'),indent=1); print(o['caption'])
EOF
```

### [89] TOOL RESULT — Bash · 2026-09-25 16:01:03 UTC

```
{"stdout": "Item-level AUROC for separating ERROR from CORRECT candidates on development dataset E. Each group is one subset: the R\\_AB population (label tiers A+B) pooled (n = 2,686 items; 1,822 ERROR, 864 CORRECT, 292 sentences), its L25, L20, exception (EXC) and control (CTRL) strata, the long pool (L25+L20+EXC), and the tier-A-only R\\_A L20+EXC subset. The R\\_A subset sits to the right of the dotted line, and n below each group counts its scored items. Bars are PEER+TEXT (vermillion), c\\_score\\_align (blue), NF c\\_score (green), L2-bow (orange), L3 (pink) and the disguised local Qwen3-8B judge (grey). Bars start at the dashed chance line (AUROC = 0.5), and whiskers are 95\\% sentence-cluster bootstrap CIs. The two consensus-based scores lead on every subset. PEER+TEXT is highest on R\\_AB pooled (0.790), L25, L20 and the long pool (0.768). c\\_score\\_align is highest on EXC (0.814), CTRL and R\\_A L20+EXC (0.860), and on every subset its interval overlaps PEER+TEXT's. Both consensus scores sit above the local judge on every subset except CTRL. The gap is widest on the long, exception-clause R\\_A L20+EXC subset, where the judge falls to 0.554. L3 stays near chance throughout. No metric separates clearly from the others on CTRL, where the intervals are widest.", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [90] TOOL CALL — Bash · 2026-09-25 16:01:11 UTC

```
python3 - <<'EOF'
import json
p='.terminal_claude_agent_struct_out.json'; o=json.load(open(p))
c=o['caption']
c=c.replace("L3 stays near chance throughout. ","L3 is the weakest score on every subset except R\\_A L20+EXC, ranging from 0.490 to 0.620. ")
c=c.replace("L3 (pink)","L3 (reddish purple)")
o['caption']=c; json.dump(o,open(p,'w'),indent=1)
json.load(open(p)); print(len(c)); print(o['out_expected_files'])
EOF
git -C . status --short | head
```

### [91] TOOL RESULT — Bash · 2026-09-25 16:01:11 UTC

```
{"stdout": "1333\n{'image_path': 'fig_dev_set_auroc_v0.pdf'}\nfatal: not a git repository (or any parent up to mount point /ai-inventor)\nStopping at filesystem boundary (GIT_DISCOVERY_ACROSS_FILESYSTEM not set).", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [92] ASSISTANT · 2026-09-25 16:01:22 UTC

```
The figure is rendered to `fig_dev_set_auroc_v0.pdf` (with a PNG preview), and every number in it came from the run's own experiment output, not the draft paper. The draft caption was wrong, and I rewrote it.

**Where the numbers come from.** The evidence check warned that the draft might quote numbers no run produced, so I traced all of them. They come from `gen_art_experiment_5/results/analysis.json` in the earlier run `run_u75jRHUss0zo`. All 42 bars (7 subsets × 6 metrics) match the specification and that experiment's own results table to 3 decimals. The spec only gave values for two subsets, so I read the other five, and every 95% interval, from that file. All six named metrics are drawn: PEER+TEXT, c_score_align, NF c_score, L2-bow, L3 and Local judge.

**Where the figure departs from the spec:**
- **Renderer:** the catalogue's `bar` type only draws symmetric error bars and a fixed palette. These intervals are asymmetric bootstrap intervals and the spec names specific colours. So I wrote `render_fig_dev_set_auroc.py` on the house style and ran every layout and legibility check. It reads everything from `fig_dev_set_auroc_spec.json`, and it refuses an interval that doesn't contain its value or that the y-range would cut off.
- **Y-axis:** it runs from 0.3 to 0.95 instead of 0.4. At 0.4 the L3 interval on the CTRL subset (down to 0.367) would be cut off.
- **Bars:** they start at the chance line, 0.5, so the one below-chance value (L3 on CTRL, 0.490) shows as a short downward bar.
- **Colours:** they follow the spec using colourblind-safe shades, so "red" is vermillion and "purple" is reddish purple.
- **Layout:** each subset's label carries its item count, and a dotted line sets off the subset scored with tier-A labels only (`R_A L20+EXC`).
- **Fixes along the way:** the y-label was clipped, the tick labels were tilted, and the legend reached the right edge. All three are fixed.

**What the caption now says.** The draft claimed PEER+TEXT leads on every subset, with its biggest advantage on long exception sentences. The data don't support that:
- PEER+TEXT is highest on four subsets: pooled, L25, L20 and the long pool.
- c_score_align is highest on the other three: EXC (0.814), CTRL and R_A L20+EXC (0.860).
- The two scores' intervals overlap on every subset.
- What does hold is that both scores beat the local judge on every subset except CTRL. The gap is widest on R_A L20+EXC, where the judge drops to 0.554.

The structured output is in `.terminal_claude_agent_struct_out.json`. I also wrote `README.md` and `.aii/manifest.yaml`; the manifest has no entries because nothing in the folder is large.

Files are in the workspace:
- `fig_dev_set_auroc_v0.pdf`
- `fig_dev_set_auroc_v0.png`
- `fig_dev_set_auroc_spec.json`
- `render_fig_dev_set_auroc.py`
```
