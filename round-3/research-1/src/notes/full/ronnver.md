URL: https://arxiv.org/html/2606.20158 | FULL FETCH | 2026-09-24T01:40:02Z
warning: The `fitz` API is deprecated and will be removed in future. Use `import pymupdf` instead.
URL: https://arxiv.org/html/2606.20158
Type: HTML
Length: 59595 chars (truncated)

--- Content ---

##### Report GitHub Issue

×

Title:

Content selection saved. Describe the issue below:

Description:

Submit without GitHub Submit in GitHub

arXiv is now an independent nonprofit! [Learn more](https://info.arxiv.org/about) ×

[ Back to arXiv ](/)

[Why HTML?](https://info.arxiv.org/about/accessible_HTML.html) Report Issue [ Back to Abstract ](/abs/2606.20158v1 "Back to abstract page") [ Download PDF](/pdf/2606.20158v1 "Download PDF") [ ](javascript:toggleNavTOC\(\); "Toggle navigation") [ ](javascript:toggleReadingMode\(\); "Disable reading mode, show header and footer")

  1. Abstract
  2. I Introduction
  3. II Background
     1. II-A N-Version Programming
     2. II-B N-Version and Fault Independence
        1. The Knight–Leveson Experiment (1986)
        2. Subsequent N-Version Work
     3. II-C The Launch Interceptor Specification
     4. II-D Coding Agents as N-Version Generators
  4. III Experimental Methodology
     1. III-A Research Questions
     2. III-B Methodology Overview
     3. III-C Version Generation with LLMs
     4. III-D Oracle and Acceptance Testing
     5. III-E Main Test Campaign
     6. III-F Failure Correlation Statistical Analysis
     7. III-G Cross-Language and Cross-Agent Failure Analysis
     8. III-H Root Cause Analysis
     9. III-I N-Version Unit Analysis
  5. IV Experimental Results
     1. IV-A RQ1: Acceptance Success
     2. IV-B RQ2: Coincident Failure Statistics
     3. IV-C RQ3: Cross-Language and Cross-Agent Failure Analysis
     4. IV-D RQ4: Root Cause Analysis
     5. IV-E RQ5: N-Version Unit Reliability
  6. V Threats to Validity
  7. VI Related Work
  8. VII Conclusion
  9. References



[ License: arXiv.org perpetual non-exclusive license ](https://info.arxiv.org/help/license/index.html#licenses-available)

arXiv:2606.20158v1 [cs.SE] 18 Jun 2026

# N-Version Programming with Coding Agents

Javier Ron* Email: [javierro@kth.se](mailto:) Benoit Baudry  Affiliation: Université de Montréal  Email: [benoit.baudry@umontreal.ca](mailto:) Martin Monperrus**KTH Royal Institute of Technology  Email: [monperrus@kth.se](mailto:)

###### Abstract

This paper revisits the classical concept on N-version programming in the setting of contemporary AI coding agents. Revisiting the seminal Knight–Leveson experiment, we study whether diversity across agent systems, models, and implementation languages creates diverse failure modes. Using the Knight–Leveson’s, Launch Interceptor Program Specification, we evaluate 48 agent-generated implementations on a shared oracle and a campaign of 1,000,000 randomized test inputs. The results show substantial common-mode failure, along the findings of Knight–Leveson. Further analysis that many of those co-occuring failures can be traced to where is specification is particularly hard or ambiguous. We also demonstrate that diversity from coding agents provides practical benefit: across majority voting three-version units, the mean failure count drops from 387.44 for single versions to 130.99 for triples, and 11,844 N-version units exhibit zero observed failures. Our original results is the strongest evidence to date that N-Version Programming with coding agents is a useful engineering strategy.

## I Introduction

N-version programming (NVP) promises reliability through diversity: multiple independently produced implementations of the same specification are executed in parallel, and a voting rule masks individual faults. Its classical reliability argument, however, depends on a strong condition: the versions must fail independently, or at least be diverse enough that coincident failures remain rare. That assumption was challenged in the human-programmer era: the seminal Knight–Leveson experiment showed that independently developed human implementations of the same specification still exhibited substantial common-mode failure [15].

AI coding agents make this question relevant again [11, 25]. Compared with recruiting independent human teams, it is now straightforward to generate many implementations of the same task while varying three key components: the coding agent, the underlying foundation model, and the target programming language. With agentic coding, the central question of N-Version Programming remains unchanged: do the generated variants behave like independent versions, or do they converge to the same latent defects?

This paper revisits the classical N-Version Programming literature in the modern agentic setting. We design and perform a reproduction of the original Knight–Leveson experiment with AI coding agents. We also revisit the broader questions about N-version software: whether the considered diversity mechanisms reduce fault correlation, which shared fault families dominate, and whether redundancy helps even if fault independence fails.

Fig. 1: N-version units are generated by AI coding agents, they improve reliability over single programs on average.

As specification, we take Knight–Leveson’s one for the Launch Interceptor Program (LIP), ane example defense software system. We strictly follow the structure of the original experiment, only replacing human programmers with contemporary AI coding agents. Across five agent systems, 23 models, and three target languages, our design space comprises 69 [harness, model, language] triples. We evaluate the resulting implementations with an oracle-based acceptance screen and a shared 1,000,000-case campaign. We analyze the observed failures through population-level coincident-failure statistics, pairwise overlap across language and agent boundaries, function-level fault localization, and exhaustive majority-vote three-version units.

Our results are clearcut. First, the idealized fault independence hypothesis fails: among the 48 admitted implementations in the campaign archive, the experiment produces 429 coincident-failure cases where the random independence model predicts only 115.36 (z=29.20z=29.20), and strong pairwise clusters can be observed across both language and agent boundaries. The failures are not diffuse; they concentrate in a small number of recurring bug families that reappear across ostensibly different implementations. Second, despite fault correlation, redundancy does provide measurable benefit: when all (483)=17,296\binom{48}{3}=17{,}296 3-Version units are evaluated, the mean failure count drops from 387.44 for single versions to 130.99 for triples, and 11,844 triples exhibit zero observed failures. All code and generated versions are available at <https://github.com/ASSERT-KTH/Knight-Leveson-Redux>

To sum up, the paper makes four contributions.

  * •

First, it provides a systematic experimental framework for studying fault independence and reliability in agent-generated software, faithful to Knight–Leveson.

  * •

Second, it shows that modern coding agents can feasibly generate enough versions to cheaply perform N-Version programming at scale.

  * •

Third, it measures and demonstrates failure overlap across [harness, model, language] diversity axes. Most of the errors can be traced back to weaknesses in the specification.

  * •

Fourth, it shows that majority voting N-version units do provide practical reliability gains, despite fault correlation.




## II Background

Fig. 2: Experimental workflow for revisiting Knight–Leveson with agentic coding: (1) version generation by each agent against the LIP specification, (2) oracle-based acceptance screening on 200 independently drawn random cases (all must pass), (3) shared one-million test campaign across admitted versions, and (4) statistical analysis (Knight–Leveson zz-statistics, pairwise correlation analysis). Versions that fail acceptance are excluded from the campaign and from all downstream analyses.

### II-A N-Version Programming

N-version programming was proposed by Chen and Avizienis [6] as a software analog of hardware N-modular redundancy. The design calls for NN independent teams to implement the same specification from a common requirements document, then execute all versions in parallel on each input and determine the output by majority vote or other consensus mechanism. Avizienis [3] formalized the reliability model: provided that the failure events of distinct versions on any given input are mutually independent and that individual failure probabilities are small, the probability of majority failure decreases exponentially with NN.

### II-B N-Version and Fault Independence

The idealized reliability benefit of NVP is entirely contingent on fault independence. Eckhardt and Lee [9] provided a theoretical treatment showing that independence cannot be assumed as a matter of principle. Because all versions are developed from the same specification, and because specifications are finite and sometimes ambiguous, there exists a nonzero set of inputs for which the specification is underspecified or misinterpreted in a common way. Programmers who share a training background, a programming language, or exposure to the same reference materials will tend to make the same misinterpretation, creating systematic coincident failure modes. Littlewood and Miller [18] extended this analysis, arguing that the very process of translating a specification into code creates correlations among any set of implementations derived from it.

#### The Knight–Leveson Experiment (1986)

The Knight–Leveson experiment [15] was an empirical test of fault independence in NVP. Twenty-seven programmers from two universities independently implemented the ”Launch Interceptor Program” specification, working without mutual communication. Their implementations were evaluated against a reference implementation on one million randomly drawn test cases. Of the 24 versions with nonzero failure rates, failures were strongly correlated: the observed count of simultaneous failures exceeded the expectation under independence by a statistically significant margin. Subsequent work by the same team [5] examined the coincidental faults, finding that a small number of fault categories accounted for the majority of coincident events. These faults were most prominently related to implementations of specific geometric computations required by the specification. Hatton [12] conducted a partial replication with a different benchmark and similarly found that independence was not achieved.

#### Subsequent N-Version Work

Littlewood and Miller [18] argued that diversity mechanisms such as development methodology variation may improve reliability, while Bishop [4] identified ambiguities and omissions in the specification as important sources of common-mode faults. Hatton [12] later showed that even without independence, multi-version systems may still deliver useful reliability gains in practice.

### II-C The Launch Interceptor Specification

The specification for a ‘Launch Interceptor Program’ (LIP) was defined by NASA [8] and used in the original Knight–Leveson study. The implementation task is to implement a DECIDE function that computes a missile launch authorization decision, given nn planar radar data points with Cartesian coordinates and a set of parameters representing incoming threats. The implementation is not trivial because several functions involve non-trivial geometric computations that are known fault attractors [5].

The computation is specified with four stages: (1) the _Conditions Met Vector_ (cmv), a vector of 15 Boolean Launch Interceptor Conditions (LICs), each encoding a geometric predicate on subsets of the input points; (2) the _Preliminary Unlocking Matrix_ (pum), a 15×1515{\times}15 Boolean matrix derived from the cmv and a programmer-supplied Logical Connector Matrix (lcm) whose entries are ANDD, ORR, or NOTUSED; (3) the _Final Unlocking Vector_ (fuv), a 15-element Boolean vector derived from pum column-wise conjunctions; and (4) the scalar launch decision, which is true iff all fuv entries are true.

The Launch Interceptor Program is well suited to randomized testing: its input domain is (1) large, (2) the input types are simple (floating-point and enumeration parameters), and (3) random sampling covers the full condition space.

### II-D Coding Agents as N-Version Generators

Contemporary AI coding agents represent a qualitatively new kind of software developer. Chen et al. [7] demonstrated that LLMs trained on code can solve a substantial fraction of programming challenges; and modern coding agents can use tools, and perform iterative self-correction, and long-horizon planning [13]. Unlike earlier program synthesis systems, these agents are able to operate from general-purpose, natural language specifications. Recent work such as Galapagos [22] has begun to exploit LLMs to construct functionally equivalent variants for N-version deployments.

Our present paper asks whether AI coding agents can generate diverse program versions whose failures behave like the independent faults assumed by classical N-version programming studies, or whether they reproduce the same kinds of correlated failure modes those studies repeatedly found in practice.

## III Experimental Methodology

We design and perform an original experimental plan, that both replicates and extends the Knight–Leveson experiment.

### III-A Research Questions

The core idea is to ask distinct coding agents to implement the same specification: LIP. From there, we answer five research questions:

RQ1. (Generation Capabilities) To what extent are AI coding agents able to implement the LIP specification?

We first ask whether modern coding agents can serve as generators of complete program versions from the seminal LIP specification. This inquiry is a necessary condition for collecting a sufficiently large and varied set of working implementations for comparative analysis in the subsequent questions.

RQ2. (Fault Independance) Are failures of AI-generated implementations mutually independent, per idealized random fault model?

This is the central question of the original Knight–Leveson study, translated to the agentic world. We test whether simultaneous failures across generated implementations do not happen (consistent with independence), or whether joint failures occur substantially more often than that model predicts (consistent with independence).

Our experimental design follows the Knight–Leveson methodology as closely as the agentic setting permits. Table I summarizes the relationship between the original study and the present one.

RQ3. (Diversity Dimensions) To what extent does diversity across programming languages, coding agents, and AI models impact fault independence?

Littlewood and Miller [18] argued that diverse software generation mechanisms, such as development methodology, may improve the dependability of multi-version systems. We therefore ask whether varying the language, agent, or underlying model decorrelates failures, or whether shared failure modes remain dominant across these dimensions.

RQ4. (Fault Explanation) What are the principal sources of faults in AI-generated implementations?

Beyond quantitatively measuring correlation, we qualitatively investigate the origin of failures. We study whether faults in agent-generated programs can be attributed to a small number of challenging or ambiguous parts of the specification.

RQ5. (N-version Reliability) To what extent do N-version units generated by AI agents provide practical reliability benefits?

Failure correlation falsifies the ideal case for N-version programming, but does not by itself imply that N-version is useless. Following the perspective of Hatton’s study [12], we measure whether combining multiple AI-generated versions yields worthwhile error reduction.

### III-B Methodology Overview

At a high level, we answer the research questions by reproducing the Knight–Leveson experimental structure faithfully. Table I summarizes which elements are carried over directly and the extent of which the experimental design has been adapted for AI coding agents. As summarized in Table I, we preserve the original acceptance filter, campaign size, failure definition, and primary Knight–Leveson hypothesis test.

Dimension |  Knight–Leveson (1986) |  This Study  
---|---|---  
Subjects |  27 human programmers (graduate and undergraduate students at 2 universities) |  69 coding agents over 5 harnesses (Cursor, Claude Code, OpenAI Codex, Gemini, OpenCode)  
Implementation Language |  Pascal |  Pascal, _Python, Rust_  
Specification |  Original LIP specification document + 15 input/output examples + realcompare function |  Faithful; Original LIP specification document + 15 input/output examples + realcompare function + _a prompt of the task to perform_  
Admitted version count |  27 |  48  
Test-campaign size |  1,000,000 random cases |  Faithful: 1,000,000 random cases  
Acceptance filter |  200-case pre-screen; all must pass |  Faithful: 200-case pre-screen; all must pass  
Oracle |  Pascal reference implementation |  Python reference implementation validated by 82 unit tests covering the full spec.  
Failure definition |  Any of 241 output bits differs from oracle |  Faithful: any of 241 output bits differs from oracle  
Primary statistic |  Knight–Leveson zz-statistic (Eq. 4) |  Faithful; Knight–Leveson zz-statistic, _supplemented by pairwise correlation analysis, cross-language and cross-agent stratification, root cause analysis, and majority-vote unit analysis_  
Independence enforcement |  Different universities, no communication between students |  Distinct agent harnesses and vendors; distinct underlying model lineages; distinct target languages  
Primary confounders |  Shared specification document, shared university curriculum |  Faithful; shared specification document, _shared LLM training corpora, overlapping model lineages_  
TABLE I: Relationship to Knight–Leveson (1986): faithful methodological elements, adaptations and _novelty (in italics)_.

RQ1. First, we adapt the source of diversity from human programmers to [harness, model, language] configurations. We generate candidate versions from a controlled set of [harness, model, language] configurations and apply the original Knight–Leveson-style acceptance screen; the number of admitted versions is the feasibility evidence of agentic N-Version programming.

RQ2. Second, we run every admitted version on the same million-input campaign and record a binary failure vector for each implementation; these vectors are the core data for the independence test.

RQ3. Third, we stratify the pairwise co-failure data by language pair and by same-agent versus cross-agent comparisons to test whether these diversity dimensions reduce overlap in failure behavior.

RQ4. Fourth, for failed executions we retain the triggering inputs and output mismatches, then aggregate them at LIC level to determine the major failure sources and trace back the problem to the specification.

RQ5. Finally, we reuse the same failure vectors to simulate majority-vote N-version units, and quantitatively measure the reliability improvements brought by agentic N-version.

### III-C Version Generation with LLMs

Five AI coding agent systems serve as the “programmers” in our study: Cursor [2], Claude Code [1], OpenAI Codex [7], Gemini [10], and OpenCode [21]. Each agent is configured with a list of underlying models spanning, where applicable, multiple vendors and generations as described in Table II. We configure Cursor with the Composer models; Claude Code with Anthropic’s Haiku, Sonnet, and Opus variants; Codex with multiple GPT-5.x revisions; Gemini with its 2.5 and 3.x preview variants; and OpenCode with Qwen and Gemma models.

The functional specification given to every agent is the original Knight–Leveson specification document, preserved verbatim as the authoritative source of truth for all conditions, LICs, and realcompare semantics. Agents are additionally given: a file with 15 input/output examples, and a reference realcompare implementation. The agents also receive a short directive that describes the provided information, input and output formats, and the expected deliverable ([Python](https://github.com/ASSERT-KTH/Knight-Leveson-Redux/blob/fa95aebe1dd888b69ca594f059433d08504bbde6/harnesses/python_harness.py#L14), [Rust](https://github.com/ASSERT-KTH/Knight-Leveson-Redux/blob/fa95aebe1dd888b69ca594f059433d08504bbde6/harnesses/rust_harness.py#L1), or [Pascal](https://github.com/ASSERT-KTH/Knight-Leveson-Redux/blob/fa95aebe1dd888b69ca594f059433d08504bbde6/harnesses/pascal_harness.py#L1)). No algorithm is suggested in the prompt, no code skeletons are provided.

Harness | Models  
---|---  
Cursor | composer-2.5, composer-2  
Claude Code |  anthropic/claude-opus-4.6, anthropic/claude-opus-4.5, anthropic/claude-sonnet-4.6, anthropic/claude-sonnet-4.5, anthropic/claude-haiku-4.5  
OpenAI Codex |  gpt-5.4, gpt-5.4-mini, gpt-5.3-codex, gpt-5.2-codex, gpt-5.2  
Gemini |  gemini-3.1-pro-preview, gemini-3-flash-preview, gemini-2.5-pro, gemini-2.5-flash, gemini-2.5-flash-lite  
OpenCode |  qwen/qwen3.6-plus, qwen/qwen3.5-flash-02-23, qwen/qwen3.5-plus-02-15, qwen/qwen3.5-397b-a17b, google/gemma-4-26b-a4b-it, google/gemma-4-31b-it  
TABLE II: Coding harnesses and underlying models used for version generation. A coding agent is a combination of a harness and a model.

We pair each [harness, model] tuple with each target programming language, producing three corresponding [harness, model, language] triples. Each triple produces one candidate DECIDE program per invocation. The resulting pool of versions therefore consists of 69 unique [harness, model, language] runs. The exact agent system, underlying model identifier, and target language are recorded in the per-version metadata for reproducibility. This metadata is later used to separate failures by agent and language when answering RQ3.

### III-D Oracle and Acceptance Testing

This part of the methodology defines the reference implementation and the admission filter that determines which generated versions are eligible for the main campaign.

We develop a reference implementation of DECIDE in Python, validated by an automated test suite of 82 unit tests covering all known boundary conditions for the 15 LICs. This reference implementation serves as the oracle for differential testing: on every campaign input, each admitted version and the oracle implementation are both evaluated, and the version is recorded as failing on that case if any of its 241 output bits differs from the oracle’s. This matches the failure definition used by Knight–Leveson.

Before entering the main test campaign (see III-E), each generated version undergoes an acceptance screening, using the terminology of the original Knight–Leveson protocol.

Acceptance testing works as follows. First, we check Pascal and Rust implementations for compilation errors. Then, we use two hundred test cases and evaluate each version against the oracle. Compilation and the small set of tests are used to filter out clearly non-functional implementations. As in Knight–Leveson, a version is admitted only if it passes all 200 tests. The admitted-version count is the first empirical outcome of the study: it measures whether AI coding agents can produce complete-enough implementations to support the replicated N-version experiment in RQ2.

### III-E Main Test Campaign

At this stage, versions that crash immediately or fail any acceptance test have been filtered out. Therefore, the main campaign will only analyze implementation-level disagreements among the admitted versions. We draw uniformly T=1,000,000T=1{,}000{,}000 test cases at random from the input domain using a fixed seed to ensure reproducibility. All admitted versions are evaluated on exactly the same set TT against the oracle. For all test runs, we record metadata: coding agent, model, language, and a binary pass/fail outcome. The resulting failure data is the common measurement for the rest of the paper: (1) aggregate coincident failures are used for the statistical analysis in RQ2; (2) stratified pairwise overlaps are used for the cross-language and cross-agent analysis in RQ3; and (3) majority-vote simulations are used for RQ5.

For failed test runs, we also record the input that caused the failure, as well as the specific CMV, PUM, FUV, or LAUNCH oracle mismatches. These fault records are later aggregated at LIC level and linked back to representative implementations and triggering inputs for RQ4.

### III-F Failure Correlation Statistical Analysis

We implement an exact replicate of the Knight–Leveson statistical framework [15] to answer RQ2. Let NN be the number of admitted versions, TT the number of campaign test cases, fif_{i} the failure count for version ii, and pi=fi/Tp_{i}=f_{i}/T the empirical failure rate. Let KK denote the number of test cases on which _two or more_ versions fail simultaneously. KK is the aggregate measure of failure overlap: it counts how often the test campaign encounters an input on which independent implementations break at the same time.

We use the zz-statistic to test the observed distribution of failures against an approximate normal distribution of failures. Specifically, under the null hypothesis H0 that failures are mutually independent Bernoulli events:

| P0\displaystyle P_{0} | =∏i=1N(1−pi)\displaystyle=\prod_{i=1}^{N}(1-p_{i}) |  | (1)  
---|---|---|---|---  
| P1\displaystyle P_{1} | =∑i=1N[pi​∏j≠i(1−pj)]\displaystyle=\sum_{i=1}^{N}\Bigl[p_{i}\prod_{j\neq i}(1-p_{j})\Bigr] |  | (2)  
| Pm\displaystyle P_{m} | =1−P0−P1\displaystyle=1-P_{0}-P_{1} |  | (3)  
  
where P0P_{0}, P1P_{1}, PmP_{m} are the probabilities that exactly zero, one, or two or more versions fail on a given test case. In particular, PmP_{m} is the quantity of interest under H0: it is the independence-based prediction for the chance that a test case triggers a coincident failure event. Under H0, KK is approximately normally distributed with mean μ=T​Pm\mu=TP_{m} and standard deviation σ=T​Pm​(1−Pm)\sigma=\sqrt{TP_{m}(1-P_{m})}, giving the Knight–Leveson zz-statistic:

| z=K−μσ.z=\frac{K-\mu}{\sigma}. |  | (4)  
---|---|---|---  
  
Because KK is taken to be approximately normal under H0, tail probabilities and two-sided pp-values for the observed zz follow from the standard normal distribution. We reject H0 at the 99% confidence level if |z|>2.576|z|>2.576, matching the Knight–Leveson threshold. The alternative hypothesis H1 is that failures are _positively_ correlated, i.e. coincident failures exceed the independence prediction. A large positive zz therefore means that the observed overlap in failures is many standard deviations above what this independence model would predict.

In addition to the pooled and per-language Knight–Leveson counts, we compute a global all-pairs similarity view over the admitted population. For every pair of admitted versions, we compute the Pearson ϕ\phi correlation between their binary failure vectors over the million-case campaign. Here, ϕ\phi measures co-failure similarity: ϕ=1\phi=1 means two versions fail on exactly the same campaign inputs, ϕ≈0\phi\approx 0 means little overlap in their failure patterns, and negative values indicate anticorrelation. We use ϕ\phi as the main descriptive overlap measure between pairs. This complements the aggregate Knight–Leveson statistic by showing whether coincident failures are concentrated in clusters of versions or dispersed across the population.

### III-G Cross-Language and Cross-Agent Failure Analysis

RQ3 asks whether implementation language and coding agent behave as meaningful axes of diversity, rather than as wrappers around the same failure mode. We answer that question by reusing the full pairwise failure data from RQ2 and stratifying it along the diversity dimensions directly available in the experiment.

To study language diversity, we partition the full pairwise set into cross-language pairs and inspect their ϕ\phi distribution. This asks whether changing implementation language tends to decorrelate failure behavior in the observed population.

Third, to study agent diversity, we partition the same pairwise set into same-agent and cross-agent subsets and compare their ϕ\phi distributions. This asks whether crossing an agent boundary decorrelates failures, or whether similar failure profiles remain common even across different tools.

### III-H Root Cause Analysis

We identify the sources of correlated faults by manually analyzing failures patterns. Because the 15 LIC predicates form the main functional decomposition inside DECIDE, they provide a natural first unit for fault localization. First, we count how many distinct [harness, model, language] triples fail on each LIC, and we stratify those LIC-level counts by target language and by coding agent. Then, we trace those failures back to implementation choices in the generated source code, and compare against the oracle and the specification.

### III-I N-Version Unit Analysis

We construct synthetic N-version units from the admitted versions and evaluate them on the same T=1,000,000T=1{,}000{,}000 campaign inputs. A unit of size nn fails on an input when at least ⌈n/2⌉\lceil n/2\rceil of its members fail on that input.

For the core RQ5 analysis, we enumerate all possible three-version units that can be formed from the admitted pool and compute their majority-vote failure statistics over the campaign. This gives an exhaustive picture of how often N-version voting helps improve reliability in the observed population.

## IV Experimental Results

### IV-A RQ1: Acceptance Success

Fig. 3 summarizes the outcome of acceptance testing. Across the five agent systems and three target languages, 69 configured [harness, model, language] triples were generated and 48/69 passed all 200 acceptance cases, yielding an admission rate of 70%. The remaining 21 configured triples were excluded before the campaign. The admission rate varies markedly by agent (center panel): the Cursor programs are admitted for all 6 of 6 attempts (100%) across all three languages, compared with 13 of 15 (87%) for Claude Code, 11 of 15 (73%) for Codex, 8 of 15 (53%) for Gemini, and 10 of 18 (56%) for OpenCode. Similar variation was observed per language (right panel): Python is the most successful target language, with 18/23 admitted attempts (78%), while Rust has 17 of 23 (74%) and Pascal 13 of 23 (57%).

_Agent Failure Modes_. Among the 21 excluded triples, 12 failed to produce the required artifact. Among the remaining excluded versions, 5 crashed immediately when executed, and 4 returned wrong output on at least one acceptance case. Consistent with the original Knight–Leveson acceptance protocol, all such versions are excluded from the campaign and from all subsequent analyses.

Fig. 3: RQ1. Acceptance testing summary. Left: the total configured population of 69 triples. Center: counts by agent system. Right: counts by target language. In all panels, green denotes admitted versions and red denotes excluded versions; the stacked height is the total number of configured triples in that category.

Answer to RQ1. AI coding agents can correctly implement the specification of the Knight–Leveson study. We obtained 48 functional implementations which pass the 200-case acceptance screen. The pool of admitted implementations is large enough to compute the Knight–Leveson independence test and to support additional analyses by language, harness, model, and fault source.

### IV-B RQ2: Coincident Failure Statistics

The admitted versions span a wide range of failure counts in the main campaign: 27 are failure-free, while the worst version fails 10,469 of the 10610^{6} inputs. Fig. 4 groups the 48 admitted [harness, model, language] triples into coarse failure-count buckets. Most versions cluster at exactly zero failures; 2 more fall between 10 and 99 failures, 18 fall between 10210^{2} and 10310^{3} cases, none fall between 10310^{3} and 10410^{4}, and 1 exceeds 10410^{4} failures. The right tail shows that the agent population contains both a large near-perfect core and a smaller set of high-failure outliers.

Fig. 4: Failure-count distribution across the 48 admitted [harness, model, language] according to the reference implementation, grouped into buckets over the million test case campaign. The distribution is strongly right-tailed, with many near-perfect versions and a much smaller set of high-failure outliers.

Table III presents the Knight–Leveson statistics for the whole 48-version campaign. The Knight–Leveson test asks whether the observed number of campaign inputs on which at least two versions fail simultaneously is compatible with the independence model derived from the individual version failure rates. If the observed count KK is much larger than the independence expectation μ\mu, the resulting large positive zz indicates common-mode failure rather than accidental overlap.

Pooled across all languages, the independence model predicts μ=115.36\mu=115.36 coincident-failure cases over the T=106T=10^{6} campaign; the observed count is K=429K=429, an excess of K/μ≈3.7×K/\mu\approx 3.7\times over the independence prediction, yielding z=29.20z=29.20 with p≈1.765×10−187p\approx 1.765\times 10^{-187}. This infinitesimal p-value decisively rejects the independence hypothesis.

Next, we do a per-language analysis. Every per-language analysis rejects H0 with over 99.99% confidence, with K/μK/\mu ranging from 17.5×17.5\times (Python) to 155.1×155.1\times (Pascal) and zz from 80.7 to 253.3. The systematic rejection rules out the explanation that the pooled rejection is being driven by only one implementation language.

The fact that Z is lower at the whole population level shows that the pooled population is more heterogeneous than the within-language slices, reducing the relative concentration of coincident failures in the aggregate.

We next turn from coincident-failure counts to pairwise failure similarity. This global all-pairs view shows how the 48 admitted versions relate to one another as a population and whether the same dependence appears beyond the pooled Knight–Leveson statistic. For every pair of admitted versions, we compute the Pearson ϕ\phi correlation between their binary failure vectors over the main test campaign. In this setting, ϕ\phi measures co-failure similarity: ϕ=1\phi=1 means two versions fail on exactly the same inputs, ϕ≈0\phi\approx 0 means little overlap in their failure patterns, and negative values would mean their failures are anticorrelated.

Fig. 5 shows a filtered heatmap of the pairwise ϕ\phi matrix, restricted to versions with at least one observed campaign failure. Large dark regions indicate families of versions that fail on the same inputs, and those regions cross both agent and language boundaries rather than aligning neatly with a single tool or target language. Again, the immediate implication is that nominal diversity in agent, model, or language does not automatically buy behavioral diversity. Pale rows and columns in the heatmap mark failing implementations whose failures do not overlap with the main co-failure clusters.

Fig. 5: Filtered pairwise co-failure heatmap for the 21 versions with at least one observed campaign failure. Each cell shows the Pearson ϕ\phi correlation between the binary failure vectors of two versions; rows and columns are ordered by agent system and then by language. Dark blocks correspond to clusters of versions that fail on exactly the same campaign inputs. The dark zones cross agent and language boundaries.

Answer to RQ2. The generated AI-agent implementations do _not_ fail independently, according to a uniform random model. At the pooled level, the experiment produces 429 coincident-failure cases where the independence model predicts only 115.36; the null hypothesis is rejected with p≈1.765×10−187p\approx 1.765\times 10^{-187}.

Slice | NN | μ\mu | KK | zz | pp-value  
---|---|---|---|---|---  
All languages | 48 | 115.36 | 429 | 29.20 | 1.765×10−1871.765\times 10^{-187}  
Python | 18 | 23.97 | 419 | 80.69 | 1.701×10−14161.701\times 10^{-1416}  
Rust | 17 | 4.91 | 419 | 186.93 | 1.693×10−75901.693\times 10^{-7590}  
Pascal | 13 | 2.70 | 419 | 253.30 | 3.327×10−139353.327\times 10^{-13935}  
TABLE III: RQ2. Knight–Leveson correlated failure statistics. NN is the number of versions; μ=T⋅Pm\mu=T\cdot P_{m} is the expected simultaneous-failure count according to the Bernoulli model; KK is the observed count in the respective population; zz is the zz-statistic (see Eq. 4); and pp is the corresponding two-tailed p-value. All slices decisively reject H0: the theoretical random failure model and the actual failure mode do not match.

### IV-C RQ3: Cross-Language and Cross-Agent Failure Analysis

RQ3 studies whether language and agent variance produce diversity in the observed failure behavior. We answer it by splitting the pairwise co-failure analysis along the diversity dimensions directly available in the experiment: implementation language and coding agent.

We first refine the global picture from RQ2 by looking specifically at cross-language pairs. Here, every admitted version written in one language is paired with every admitted version written in a different language, regardless of agent or model, and we compute the same co-failure statistics as in the global analysis. This yields 761 cross-language pairs in total; for 615 of them, ϕ\phi is undefined because at least one of the two versions is failure-free, leaving 146 pairs in the ϕ\phi distribution analysis.

Figure 6 summarizes the resulting pairwise ϕ\phi distributions under both diversity splits. For cross-language pairs, 146 pairs have defined ϕ\phi; 81 land exactly in the ϕ=1\phi=1 bucket, indicating perfect co-failure agreement. The remaining defined cross-language pairs are fewer: 40 are non-positive, 13 fall in (0.1,0.2](0.1,0.2], and 12 fall in (0.6,0.7](0.6,0.7]. The language-pair stack shows that perfect co-failures are distributed across all three language pairings: Pascal–Python contributes 17 pairs, Pascal–Rust contributes 32, and Python–Rust contributes 32.

The same figure also shows the corresponding same-agent versus cross-agent split. The observed pattern is similar in both groups: among the 221 same-agent pairs, 52 have defined ϕ\phi, with 34 at exact ϕ=1\phi=1 and 6 non-positive; among the 907 cross-agent pairs, 158 have defined ϕ\phi, with 87 at exact ϕ=1\phi=1 and 50 non-positive. Crossing an agent boundary therefore does not eliminate highly correlated failure profiles: exact co-failure clusters remain common even between different tools, although the population also contains many genuinely distinct cross-agent pairs.

Fig. 6: RQ3: Bucketed distributions of pairwise ϕ\phi correlations under two diversity axes. For each bucket, the left stacked bar counts cross-language pairs by language pair, while the right stacked bar counts all version pairs by same-agent versus cross-agent relation. The exact-match bucket ϕ=1\phi=1 is separated from the near-perfect bucket (0.9,1)(0.9,1), showing that the high-correlation mass is dominated by correlated failures.

Answer to RQ3. Cross-language and cross-agent program generation do not provide enough diversity to make failure correlation disappear. In Littlewood and Miller’s terms [18], varying the [harness, model, language] tuple does not equate to achieving fundamentally different methodologies that generate diverse program distributions.

### IV-D RQ4: Root Cause Analysis

Next, we take a deeper look at the failure modes on the 1M random test cases.

Fig. 7 provides the LIC-level view. For each LIC condition from the specification, it plots the number of distinct [harness, model, language] triples that fail on at least one campaign case, showing the same counts under two stackings: by implementation language and by coding agent. Fig. 7 shows that the failures are not equally distributed over the whole specification.

Two LICs tend to be incorrectly implemented: 9 and 14. The failures happen over all languages and across multiple agents. Rust programs only fail on LICs #9 and #14, while Pascal and Python programs also fail on some other LICs. For the admitted versions, all agents generated programs with failures, except Codex.

Fig. 7: RQ4: failure counts per specification items (aka LIC in the LIP specification). For each LIC, the bars show the number of distinct [harness, model, language] triples that fail on at least one campaign test case. Within each LIC, the left stacked bar groups failures by target language and the right stacked bar groups the same failures by coding agent. Failures overwhelmingly concentrate in LICs 9 and 14, indicating that the failures are driven by a small number of difficult or ambiguous parts of the specification.

LICs #9 and #14 are both spaced-point variants of the minimum-enclosing-circle predicate: LIC #9 asks whether a selected triple cannot fit inside a circle of radius RADIUS1, while LIC #14 strengthens that pattern into a two-part condition requiring one spaced triple outside RADIUS1 and one spaced triple inside or on RADIUS2. Inspection of the faulty versions reveals the recurring mistake behind LICs #9 and #14: many implementations compute the _circumcircle_ of the selected triple instead of the _minimum enclosing circle_. That shortcut is incorrect because the minimum enclosing circle of three points is not always the circumcircle. Fig. 8 shows an excerpt from the admitted claude_code/claude-sonnet-4.5 Pascal version that is representative of the mistake.

[⬇](data:text/plain;base64,ZnVuY3Rpb24gQ2lyY2xlQ29udGFpbnNUaHJlZVBvaW50cyh4MSwgeTEsIHgyLCB5MiwgeDMsIHkzLCByYWRpdXM6IHJlYWwpOiBib29sZWFuOwp2YXIKICBkMTIsIGQyMywgZDEzOiByZWFsOwogIGN4LCBjeSwgcjogcmVhbDsKICBhLCBiLCBjLCBkLCBlLCBmLCBnOiByZWFsOwpiZWdpbgogIGQxMiA6PSBEaXN0YW5jZSh4MSwgeTEsIHgyLCB5Mik7CiAgZDIzIDo9IERpc3RhbmNlKHgyLCB5MiwgeDMsIHkzKTsKICBkMTMgOj0gRGlzdGFuY2UoeDEsIHkxLCB4MywgeTMpOwoKICBpZiAoUkVBTENPTVBBUkUoZDEyLCAyICogcmFkaXVzKSA8PiBHVCkgYW5kCiAgICAgKFJFQUxDT01QQVJFKGQyMywgMiAqIHJhZGl1cykgPD4gR1QpIGFuZAogICAgIChSRUFMQ09NUEFSRShkMTMsIDIgKiByYWRpdXMpIDw+IEdUKSB0aGVuCiAgYmVnaW4KICAgIC4uLgogICAgY3ggOj0gKGQgKiBlIC0gYiAqIGYpIC8gZzsKICAgIGN5IDo9IChhICogZiAtIGMgKiBlKSAvIGc7CiAgICByIDo9IERpc3RhbmNlKGN4LCBjeSwgeDEsIHkxKTsKICAgIENpcmNsZUNvbnRhaW5zVGhyZWVQb2ludHMgOj0gUkVBTENPTVBBUkUociwgcmFkaXVzKSA8PiBHVDsKICBlbmQKICBlbHNlCiAgICBDaXJjbGVDb250YWluc1RocmVlUG9pbnRzIDo9IEZhbHNlOw==)

function CircleContainsThreePoints(x1, y1, x2, y2, x3, y3, radius: real): boolean;

var

d12, d23, d13: real;

cx, cy, r: real;

a, b, c, d, e, f, g: real;

begin

d12 := Distance(x1, y1, x2, y2);

d23 := Distance(x2, y2, x3, y3);

d13 := Distance(x1, y1, x3, y3);

if (REALCOMPARE(d12, 2 * radius) <> GT) and

(REALCOMPARE(d23, 2 * radius) <> GT) and

(REALCOMPARE(d13, 2 * radius) <> GT) then

begin

...

cx := (d * e - b * f) / g;

cy := (a * f - c * e) / g;

r := Distance(cx, cy, x1, y1);

CircleContainsThreePoints := REALCOMPARE(r, radius) <> GT;

end

else

CircleContainsThreePoints := False;

Fig. 8: Representative LIC 9/14 implementation mistake: the version checks whether all pairwise distances fit within the diameter, then computes a circumcircle center and radius rather than the minimum enclosing circle.

LICs #3 and #10 expose a more subtle issue. The original specification is ambiguous about whether the angle predicate should be implemented directly as an interior angle in [0,π][0,\pi] or indirectly through a complementary angle in [0,2​π)[0,2\pi). In exact arithmetic those formulations are equivalent, but they are not equivalent under the benchmark’s relative-tolerance REALCOMPARE. For the failing gemini-3.1-pro-preview versions, the oracle compares a interior angle against the threshold π−ϵ\pi-\epsilon, while the candidate compares the complementary angle against the threshold π+ϵ\pi+\epsilon. In many test cases with razor-sharp differences, comparisons against the thresholds yield different results.

Across the remaining LICs, the dominant mechanisms are concrete implementation errors rather than specification mistakes. Besides the minimum-enclosing-circle family in LICs #9 and #14, we observed a wrong circumradius formula in LIC #2, a segment-distance substitution for the infinite-line distance required by LIC #7, and dropped applicability guards in LICs #8, #12, and #13.

Answer to RQ4. The dominant failure modes are concentrated in LICs #9 and #14, where many agents compute the circumcircle instead of the minimum enclosing circle. The remaining recurrent faults are smaller but still structured: LICs #3 and #10 expose a specification ambiguity caused by REALCOMPARE, while LICs #2, #7, #8, #12, and #13 fail for specific geometric or applicability-check mistakes. These findings are consistent with Brilliant et al.’s observation that coincident failures concentrate in a small number of shared fault categories [5] and with Bishop’s emphasis on specification weaknesses as drivers of correlated faults [4].

### IV-E RQ5: N-Version Unit Reliability

The preceding analyses show that the failures are not Bernoulli independent, but they do not by themselves answer whether N-Version units are useful. We therefore construct every possible three-version unit from the admitted implementations and evaluate each unit on the same million campaign inputs. This yields (483)=17,296\binom{48}{3}=17{,}296 triple combinations.

Fig. 9 compares bucketed failure-count distributions for majority-vote triple failure counts against the corresponding distribution of single-version failure counts. The 3-version distribution is better on average: the mean triple failure count is 130.99, compared with a mean single-version failure count of 387.44. At the low end, 11,844 triples (68.48%) have zero majority-vote failures, compared with 27 failure-free individual versions (56.25%). Both distributions have minimum 0 and median 0, so the meaningful differences appear in the upper tail: at P95 the single-version count is 429 while the triple count is 419, at P99 it is 6,004 versus 419, and at the maximum it is 10,469 versus 419. This shows that majority voting substantially compresses the rare high-failure tail.

Fig. 9: RQ5: Bucketed failure-count distributions for single versions and for all (483)=17,296\binom{48}{3}=17{,}296 majority-vote triples. The x-axis groups versions into the buckets 00, (0,10](0,10], (10,100](10,100], (100,1000](100,1000] , and >1000>1000 failure counts, and the y-axis shows the percentage of the corresponding population in each bucket, with percentages annotated above the bars. The triple distribution shifts toward the lower-failure buckets, indicating that triple redundancy does reduce the number of failures even though the full population is not independent. This is clear evidence in favor of N-Version programming with coding agents.

Answer to RQ5. N-version units improve reliability even when the full population exhibit fault correlation. Majority-voting triples substantially improve over single versions: the mean failure count drops from 387.44 to 130.99, and 11,844 3-Version units exhibit zero observed failures (as opposed to 27 individual versions). This is a constructive result that confirms Hatton’s claim that N-Version programming is useful, even in the presence of correlated faults [12].

## V Threats to Validity

Scope of Interpretation The present study is about _implementation-level_ faults relative to a fixed specification and a fixed oracle provided by a reference implementation. It does not test whether multi-version execution mitigate runtime or transient failures such as network outages, external tool crashes, or language-specific stack components.

Single benchmark. The experiment is based on a single specification: the LIP problem. Conclusions drawn from it may not generalize to specifications in other domains, such as long-running stateful services. Replication over other specifications is a direction for future work.

Sampling variability. Each admitted version corresponds to a single [harness, model, language] tuple; we therefore measure diversity across distinct configurations rather than within-configuration variability due to LLM sampling. Rerunning the generation stage at either a different temperature or at a different date would likely change the _exact_ failure counts.

## VI Related Work

Recent work on LLM-based code generation has shown that diversity can improve correctness. Chen et al. [7] and Li et al. [17] established that sampling multiple candidates from a single model can improve pass@k solve rates. Kodati et al. [16] further show that sampling candidates from different LLMs increases solve rates compared to single model sampling. In a related line of work, Wang et al. [24] show that self-consistency improves accuracy in code generation. Mahmud et al. [20] use ensembles of LLM outputs together with syntactic and behavioral similarity signals to improve HumanEval pass rates, and Valentin et al. [23] argue that cross-candidate incoherence can serve as an oracle-less proxy for error. Differential testing of generated programs has also been suggested by Kessel et al. [14] as a way to enhance generation quality. These papers all exploit disagreement or agreement across candidates as useful engineering signals. The key difference with our work is that they do not study the reliability of a population of generated implementations under the lens of N-version programming models.

A separate thread of work emphasizes that modern software systems are often assembled and revised under changing requirements instead of built once from a complete specification. Liu et al. [19] frame this as a move toward just-in-time systems, where specifications, interfaces, and generated code evolve together. This perspective is relevant to N-version generation because repeated failures across independently generated programs may reveal not only implementation mistakes, but also parts
