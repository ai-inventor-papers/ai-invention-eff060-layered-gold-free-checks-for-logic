"""Build .terminal_claude_agent_struct_out.json from sources_meta.py + notes/quotes.json.
Run: python3 scripts/build_output.py"""
import json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from sources_meta import S

quotes = json.loads((ROOT / "notes/quotes.json").read_text())
assert all(q["verified_in_fetched_text"] for q in quotes)

ANSWER = r"""
VERDICT SUMMARY. No paper meets the pre-stated scoop rule, i.e. (i) multiple model families' formal translations + (ii) solver equivalence + (iii) meta-evaluation of the agreement score against faithfulness labels on NL->FOL. So C1 is NOT scooped as a method-plus-evaluation package. But the METHOD itself is not new, and all five claims except C2 need qualifiers.

CLOSEST NEIGHBOURS. (1) ARc [33] redundantly translates NL into SMT-LIB with several LLMs. It scores each translation by "the proportion of the k translations that non-vacuously entail" it. This is the same functional form as our c_score. But it works over a fixed shared schema, so no vocabulary alignment is needed, and it is validated on downstream QA soundness (98.4%->99.4%), not translation-faithfulness labels [33]. (2) NoTB [1] clusters RTL from four LLM families by formal equivalence. Specification-level precision rises from 63% to 85.3% / 87% / 94.7% at >=2/3/4 agreeing families, with coverage 49/33/27%. It is a triage selector against hidden-testbench labels. It compares LLM judges only at a different unit (completion level), and reports no AUROC and no complexity analysis [1]. (3) GenV [3] is NL->FOL/SMT with AUROC 0.961. It is a single trained verifier, and its labels are Z3-equivalence to the gold. Importantly, its single-model self-consistency (K=5) baseline already reaches AUROC 0.863 on NL->FOL. Its LLM judge wins (0.778 vs 0.679) when the target switches from Z3-reference equivalence to panel-majority intent [3]. (4) SCP-NL2TL [34] is the closest meta-evaluation design. It reports error-detection AUROC of single-model self-consistency vs back-translation vs judge vs fusion channels by difficulty tier (number of atomic propositions) for NL->temporal logic, and self-consistency AUROC rises with tier [34]. Other near-neighbours: LLMs-as-a-Jury [2] (answers), ADMITOR [30] (3 families, optimization models, precision 0.927 vs 0.871 for a single-model vote), VERGE [32] (cross-model consensus "supported but not yet evaluated"), and single-model selectors Li et al. [4], GoFU [5], SCD [35] and CLOVER [9].

C1 (beats API judge; adds over baseline stack): NEEDS-QUALIFIER. Claim only "the first meta-evaluation of cross-family solver consensus as a gold-free faithfulness score for individual NL->FOL candidates, against adjudicated labels, head-to-head with an API judge and nested over the parse / round-trip / judge / self-consistency / structural stack". Credit ARc [33] and NoTB [1] for the score form. Never say "we propose cross-model consensus", and never claim superiority over judges in general (GenV shows the reverse under intent labels [3]). If T1 loses to the API judge, report parity plus cost (~$0.0015/sentence vs ~$0.00004/judge call).

C2 (holds with aligner-free labels): SAFE as a methodological contribution. No neighbour controls for the labeller and the metric sharing an instrument. Cite GenV's label-target reversal [3], and wrong gold in FOLIO/MALLS, which is 39%/36% in v1 but 42.5%/42% in v2 (3 Sep 2026) of 2606.02837 [24].

C3 (rename-invariant hybrid matcher): NEEDS-QUALIFIER. Predicate alignment exists: LogicLLaMA greedy binding search [36], Levenshtein <=0.6 mapping [37], and leaf-matching left open by [31]. No neighbour reports a rename false-alarm rate. That is the novel piece (ours: 0.859 ALIGN vs 0.074 NF).

C4 (e/d decomposition; endorsement falls with conditions): NEEDS-QUALIFIER. AUROC = 1-(e+d)/2 at a fixed threshold is balanced accuracy. The scatter premise is stated by [2, 9, 40], and identical-wrong outputs from missing logic were noted in 1978 [60]. Coincident-FAILURE theory predicts that both-wrong rises with input difficulty [21, 22, 23]. Replications confirm concentration on hard inputs [18, 20]. LLM correlated-error work does not condition on difficulty: [14] names it as future work, and [2] uses a scalar attractor rate. So the candidate-new piece is the MEASURED identical-wrong (endorsement) vs both-wrong curve over number of conditions for NL->FOL. Indirect support for the falling direction: [34, 49, 54]. Counter-evidence: [14, 50, 52, 62].

C5 (3-5 families suffice): NEEDS-QUALIFIER. It is already recommended ("three to four cross-family models" [2]), and it is consistent with NoTB's curve [1] and effective-N results (7 models ~ 2.58 [15]; 9 judges ~ 2 votes [48]; 16 models ~ 1.69 formulations [63]). Novelty exists only per complexity tercile with cost.

CONTEXT NUMBERS TO QUOTE. 60% agreement when both wrong (MCQ) [14]; rho 0.20-0.59 [16]; all-wrong beta 0.052-0.127 [50]; Knight-Leveson 1255 coincident-failure tests [20]. Judge limits: equivalence verification collapses beyond toy complexity and >20 operators yields <50% truth maintenance [28]; judges disagree 26-37 pp [26]; judge 87/97 agreement with humans but "not an equivalence oracle" [29]. Costs: NoTB $14.93 generation for 78 specs and 1,556 judge calls per judge [1]; GenV ~12 H100 GPU-hours of training [3].

CONFIDENCE. High that the method is not new (verbatim quotes from [1, 33]). Medium that no NL->FOL cross-family meta-evaluation exists: the sweep was logged but not systematic, and forward citations of NoTB and roundtrip were rate-limited. Medium on C4: the classical papers [21, 22] were read as abstracts plus review [23]. A 1990s tabulation of identical-wrong outputs vs input complexity, or a GenV/VERGE follow-up evaluating cross-model mode, would change the verdicts.
""".strip()

# Pick up to 3 supporting passages per source (ledger order)
by_src = {}
for q in quotes:
    by_src.setdefault(q["source_index"], []).append(q)
sources = []
from collections import Counter
for i in sorted(S):
    url, title, authors, year, summary = S[i]
    qs = by_src.get(i, [])
    if qs:  # point the source at the page most of its verified quotes came from
        url = Counter(q["url"] for q in qs).most_common(1)[0][0]
    ps = [{"quote": q["quote"], "locator": f'{q["qid"]}; {q["version"]}; {q["locator"]}'} for q in qs if q["url"] == url][:3]
    sources.append({"index": i, "url": url, "title": title, "summary": summary,
                    "authors": authors, "year": year, "supporting_passages": ps})

cited = {int(n) for grp in re.findall(r"\[([\d,\s]+)\]", ANSWER) for n in grp.split(",")}
missing = cited - set(S)
assert not missing, missing

SUMMARY = (
"Prior-art positioning (web research, $0 LLM spend, 63 sources, 139 verbatim quotes machine-checked against fetched text) for the "
"iteration-3 claim that cross-family solver consensus is a gold-free NL->FOL faithfulness metric. SCOOP RULE (multi-family "
"translations + solver equivalence + faithfulness-label meta-eval on NL->FOL): no hit meets all three, so C1 is not scooped. "
"Closest neighbours meet two of three each: ARc 2511.09008 (NL->SMT, k LLMs, per-translation confidence = share of k translations "
"entailing it, i.e. the same score form as c_score, but a fixed schema and downstream-QA labels); NoTB 2608.21962 (RTL, 4 families, "
"precision 63/85.3/87/94.7% at >=1..4 families, coverage 100/49/33/27%, spec-level, no AUROC); GenV 2609.11085 (NL->FOL, single "
"trained verifier, AUROC 0.961 on Z3-reference labels; single-model SC K=5 = 0.863; the judge beats GenV 0.778 vs 0.679 when labels switch to "
"panel intent). The closest meta-evaluation design is SCP-NL2TL 2608.05439 (NL->temporal logic, single-model SC vs judge vs back-translation "
"AUROC by difficulty tier; SC AUROC rises with tier). VERDICTS: C1 NEEDS-QUALIFIER (the method is not new; claim the first meta-evaluation "
"of cross-family consensus as a per-candidate NL->FOL faithfulness score vs an API judge, nested over the baseline stack; win and loss wordings "
"are given); C2 SAFE (cite GenV's label-target reversal and wrong-gold rates, 2606.02837 v1 39%/36% vs v2 42.5%/42%); C3 "
"NEEDS-QUALIFIER (predicate alignment exists in LogicLLaMA and Vossel; no neighbour reports a rename false-alarm rate); C4 NEEDS-QUALIFIER "
"(balanced-accuracy maths; the scatter premise is stated by LLMs-as-Jury, CLOVER and Chen & Avizienis 1978, who noted identical wrong results "
"from missing logic; the new piece is a measured identical-wrong vs both-wrong curve over number of conditions, set against "
"Eckhardt-Lee's coincident-failure-rises-with-difficulty); C5 NEEDS-QUALIFIER (LLMs-as-Jury already recommend 3-4 cross-family "
"models; effective-N results: 7 models ~ 2.58, 9 judges ~ 2). Also supplies: the positioning table on 10 axes; a premise-evidence "
"table (60% agree-when-both-wrong on MCQ, rho 0.20-0.59, beta 0.052-0.127, KL 1255 tests); judge-degradation evidence (AutoEval: "
"equivalence verification fails beyond toy complexity; >20 operators <50%); cost norms; 8 required extra rows (single-family SC, "
"precision@coverage by k, endorsement vs both-wrong by conditions, k-curve per tercile, rename FA per matcher, label-protocol sensitivity, "
"n_eff, cite ARc); AuthorYYYY citation strings; and a search log. Files: research_report.md (main), notes/QUOTES.md (quote ledger)."
)

out = {
    "title": "What is new about peer agreement for logic",
    "layman_summary": "Checks published research to decide which parts of 'let several AI model families translate a sentence into logic and score agreement' are genuinely new, and how the paper must word each claim.",
    "summary": SUMMARY,
    "out_expected_files": {"output": "research_out.json", "reproducibility": "reproducibility.md"},
    "upload_ignore_regexes": [r"^notes/full/", r"^notes/raw/", r"(^|/)\.repl_agent\.ptylog$", r"(^|/)__pycache__/"],
    "answer": ANSWER,
    "sources": sources,
    "follow_up_questions": [
        "Report precision@coverage by number of agreeing families (k = 2..9) alongside AUROC, so the NL->FOL results are directly comparable to NoTB's 85.3/87/94.7% curve and ADMITOR's admission precision.",
        "Does the identical-wrong (peer-endorsement) rate fall with the number of logical conditions while the both-wrong rate rises, as Eckhardt-Lee predicts for coincident failures, and does this hold per error type (polarity vs dropped-condition vs structural)?",
        "Does the consensus-vs-judge ranking survive a label protocol that does not use z3 or the vocabulary aligner (aligner-free and human-intent labels), given that GenV's metric-vs-judge ranking reverses between Z3-reference and panel-intent targets?",
    ],
}
(ROOT / ".terminal_claude_agent_struct_out.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
print("sources", len(sources), "passages", sum(len(s["supporting_passages"]) for s in sources), "answer words", len(ANSWER.split()), "summary chars", len(SUMMARY))
