# Prompts

Complete, auto-generated record of **every prompt the AI Inventor system gave each agent** across this run — generated at repository-upload time so it captures all steps. For the full conversation (assistant turns, thinking, tool calls and results) see the sibling `../messages/` folder.

- Run: `gen_paper_repo_a2e1d024cc16` — Cross-Family Solver Consensus as a Gold-Free Faithfulness Metric for Logic Translation

Each prompt is labelled by type and timestamped, with its full untruncated body:

- **SYSTEM-USER** — the pipeline-generated role/instruction prompt placed in the user slot.
- **HUMAN-USER** — the task / human-typed message into the agent stream.
- **SKILL-INPUT** — a skill the agent loaded; its `SKILL.md` instructions, verbatim.

Layout mirrors the run's module tree: one folder per high-level phase, a `round_N/` per iteration where the phase iterates, then each module — a single-task module is one `.md` file, a parallel module (gen_plan / gen_art / gen_viz / gen_demo_art) is a folder with one `.md` per task.

## Index

- **1. report_results** — `gen_paper_repo`
  - `chat/prompts/1_report_results/1_gen_paper_draft.md` — 15 prompts
  - `2_gen_viz/` — 14 task(s)
    - `chat/prompts/1_report_results/2_gen_viz/gen_viz_1.md` — 8 prompts
    - `chat/prompts/1_report_results/2_gen_viz/gen_viz_2.md` — 9 prompts
    - `chat/prompts/1_report_results/2_gen_viz/gen_viz_3.md` — 2 prompts
    - `chat/prompts/1_report_results/2_gen_viz/gen_viz_4.md` — 2 prompts
    - `chat/prompts/1_report_results/2_gen_viz/gen_viz_5.md` — 2 prompts
    - `chat/prompts/1_report_results/2_gen_viz/gen_viz_6.md` — 3 prompts
    - `chat/prompts/1_report_results/2_gen_viz/gen_viz_report_1.md` — 4 prompts
    - `chat/prompts/1_report_results/2_gen_viz/gen_viz_report_2.md` — 3 prompts
    - `chat/prompts/1_report_results/2_gen_viz/gen_viz_report_3.md` — 7 prompts
    - `chat/prompts/1_report_results/2_gen_viz/gen_viz_report_4.md` — 3 prompts
    - `chat/prompts/1_report_results/2_gen_viz/gen_viz_report_5.md` — 2 prompts
    - `chat/prompts/1_report_results/2_gen_viz/gen_viz_report_6.md` — 3 prompts
    - `chat/prompts/1_report_results/2_gen_viz/gen_viz_report_7.md` — 5 prompts
    - `chat/prompts/1_report_results/2_gen_viz/gen_viz_report_8.md` — 4 prompts
  - `3_gen_demo_art/` — 21 task(s)
    - `chat/prompts/1_report_results/3_gen_demo_art/gen_demo_art_dataset_1.md` — 4 prompts
    - `chat/prompts/1_report_results/3_gen_demo_art/gen_demo_art_dataset_2.md` — 8 prompts
    - `chat/prompts/1_report_results/3_gen_demo_art/gen_demo_art_dataset_3.md` — 5 prompts
    - `chat/prompts/1_report_results/3_gen_demo_art/gen_demo_art_dataset_4.md` — 4 prompts
    - `chat/prompts/1_report_results/3_gen_demo_art/gen_demo_art_evaluation_1.md` — 8 prompts
    - `chat/prompts/1_report_results/3_gen_demo_art/gen_demo_art_evaluation_2.md` — 4 prompts
    - `chat/prompts/1_report_results/3_gen_demo_art/gen_demo_art_evaluation_3.md` — 4 prompts
    - `chat/prompts/1_report_results/3_gen_demo_art/gen_demo_art_evaluation_4.md` — 4 prompts
    - `chat/prompts/1_report_results/3_gen_demo_art/gen_demo_art_experiment_1.md` — 8 prompts
    - `chat/prompts/1_report_results/3_gen_demo_art/gen_demo_art_experiment_2.md` — 4 prompts
    - `chat/prompts/1_report_results/3_gen_demo_art/gen_demo_art_experiment_3.md` — 9 prompts
    - `chat/prompts/1_report_results/3_gen_demo_art/gen_demo_art_experiment_4.md` — 4 prompts
    - `chat/prompts/1_report_results/3_gen_demo_art/gen_demo_art_experiment_5.md` — 8 prompts
    - `chat/prompts/1_report_results/3_gen_demo_art/gen_demo_art_experiment_6.md` — 4 prompts
    - `chat/prompts/1_report_results/3_gen_demo_art/gen_demo_art_experiment_7.md` — 4 prompts
    - `chat/prompts/1_report_results/3_gen_demo_art/gen_demo_art_experiment_8.md` — 4 prompts
    - `chat/prompts/1_report_results/3_gen_demo_art/gen_demo_art_experiment_9.md` — 5 prompts
    - `chat/prompts/1_report_results/3_gen_demo_art/gen_demo_art_experiment_10.md` — 4 prompts
    - `chat/prompts/1_report_results/3_gen_demo_art/gen_demo_art_experiment_11.md` — 4 prompts
    - `chat/prompts/1_report_results/3_gen_demo_art/gen_demo_art_experiment_12.md` — 4 prompts
    - `chat/prompts/1_report_results/3_gen_demo_art/gen_demo_art_experiment_13.md` — 4 prompts
  - `4_gen_full_paper/` — 3 task(s)
    - `chat/prompts/1_report_results/4_gen_full_paper/gen_full_paper.md` — 7 prompts
    - `chat/prompts/1_report_results/4_gen_full_paper/gen_paper_site.md` — 5 prompts
    - `chat/prompts/1_report_results/4_gen_full_paper/gen_report_doc.md` — 19 prompts
  - `chat/prompts/1_report_results/5_gen_html_demo.md` — 2 prompts
