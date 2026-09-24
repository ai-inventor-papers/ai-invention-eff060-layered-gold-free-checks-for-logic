URL: https://arxiv.org/html/2608.05670 | FULL FETCH | 2026-09-24T01:36:08Z
warning: The `fitz` API is deprecated and will be removed in future. Use `import pymupdf` instead.
URL: https://arxiv.org/html/2608.05670
Type: HTML
Length: 95031 chars (truncated)

--- Content ---

##### Report GitHub Issue

×

Title:

Content selection saved. Describe the issue below:

Description:

Submit without GitHub Submit in GitHub

arXiv is now an independent nonprofit! [Learn more](https://info.arxiv.org/about) ×

[ Back to arXiv ](/)

[Why HTML?](https://info.arxiv.org/about/accessible_HTML.html) Report Issue [ Back to Abstract ](/abs/2608.05670v1 "Back to abstract page") [ Download PDF](/pdf/2608.05670v1 "Download PDF") [ ](javascript:toggleNavTOC\(\); "Toggle navigation") [ ](javascript:toggleReadingMode\(\); "Disable reading mode, show header and footer")

  1. Abstract
  2. 1 Introduction
     1. Contributions
  3. 2 Related work
     1. Consensus as a reliability signal.
     2. Consensus as a training signal.
     3. Chart and figure reasoning.
  4. 3 Render-equivalence sets
     1. Agreement (REA\mathrm{REA}).
     2. Aggregation (RM\mathrm{RM}) and error decomposition.
  5. 4 What agreement measures
     1. 4.1 Agreement estimates concentration, with a bias
     2. 4.2 Where agreement can lie
     3. 4.3 Which perturbation carries the dispersion
  6. 5 RENDEQ
     1. Instance and axes.
     2. Diagnostics and scope.
  7. 6 Experiments
     1. Setup.
     2. Metrics and baselines.
     3. 6.1 Measuring the coupling
        1. Re-rendering versus resampling.
        2. Agreement versus evidence.
     4. 6.2 Aggregation
     5. 6.3 Identity, not diversity
     6. 6.4 Consensus self-training can invert
  8. 7 Conclusion
  9. Limitations
  10. References
  11. A Positioning
  12. B Standard aggregation results
  13. C Proofs of the main results
     1. C.1 Proof of 
        1. (i).
        2. (ii).
        3. (iii).
     2. C.2 Proof of 
        1. (i).
        2. (ii).
        3. (iii).
     3. C.3 Proof of 
     4. C.4 Proof of 
  14. D Replication of the agreement-versus-evidence prediction across independent instantiations, and a rendering bug that produced a false reversal
     1. The bug.
     2. Why this produces exactly this reversal.
     3. The fix and the corrected result.
     4. The render-versus-sample reliability half.
     5. Consensus self-training, re-run on the corrected images.
     6. What this means for how to read this paper.
  15. E Per-model and per-family results
     1. Combining REA\mathrm{REA} and B1.
     2. Self-consistency versus single-render decoding.
     3. Diffuseness by family.
     4. E.1 Where the errors live
     5. E.2 Render-flip rate and render-equivalence robustness
  16. F Calibration
  17. G KK ablation
     1. Modal versus pairwise REA\mathrm{REA}.
     2. Sensitivity to the numeric tolerance τ\tau.



[ License: CC BY 4.0 ](https://info.arxiv.org/help/license/index.html#licenses-available)

arXiv:2608.05670v1 [cs.LG] 06 Aug 2026

# When Does Consensus Mean Correctness? Measuring the Agreement–Accuracy Coupling with Semantics-Preserving Re-Rendering

###### Abstract

A model’s agreement across perturbed inputs is used both as a label-free reliability signal and as a self-training target, on the premise that agreement tracks correctness. That coupling is rarely measured directly: natural-image perturbations preserve meaning only by assumption, and no exact answer key localizes errors. Scientific figures remove both obstacles, a figure is drawn from data by a program, so redrawing it yields images that are semantically equivalent by construction and share a programmatically exact answer. We build RENDEQ, a generator of such render-equivalence sets, and measure the coupling on three open-weight VLMs, checking every finding across three independent instantiations. Re-rendering beats resampling on both accuracy and reliability. Agreement beats an evidence-carrying baseline, mean token log-probability, on two of three models and ties on the third, reversing an intermediate, buggy replication traced to a rendering-pipeline failure. The dispersion behind this is concentrated in one style factor, the plotting library, more than double the next-largest factor and an order of magnitude above the noise floor. Fine-tuning on the model’s own cross-render consensus inverts: accuracy falls in every one of five replication runs, the opposite sign to published results on natural images. Agreement certifies correctness only above a threshold set by how diffuse a model’s errors are, and an objective that rewards agreement destroys exactly that diffuseness.

KEYWORDS vision-language models; self-consistency; chart question answering; calibration; test-time aggregation

## 1 Introduction

Two lines of work have converged on the same idea. The first treats a model’s agreement across perturbed inputs as a label-free reliability signal: Zhang et al. [1] blur images and rephrase questions and read hallucination off the entropy of the resulting answer clusters, and Rosenfeld et al. [2] show at scale that a sample’s stability under benign perturbations predicts whether it was answered correctly. The second turns the same consensus into a training target: Kaya et al. [3] aggregate over augmented inputs at test time and then fine-tune on the resulting consensus pseudo-labels, reporting gains across nine benchmarks. Both uses rest on one premise, that agreement tracks correctness.

That premise is conditional, and the condition has been stated before. Agreement estimates how concentrated a model’s answer distribution is, aggregation estimates where its mode sits, and only the second can be wrong about the answer. When errors are correlated rather than idiosyncratic, majority voting locks in the wrong answer instead of correcting it [4], and consensus certifies a property of the model-induced distribution rather than semantic correctness. So the useful question is not whether consensus works, but how tightly concentration and correctness are coupled in a given model on given data.

That coupling is almost never measured, for two reasons: perturbations of natural images preserve meaning only by assumption, so a change in the answer cannot be attributed to model instability rather than to the perturbation having altered the content, and there is no exact answer key for the intermediate quantities a model must read, so the source of an error cannot be localized. Scientific figures remove both obstacles. A figure is the output of a rendering program applied to data; the data fixes the correct answer to any well-posed quantitative question, and the rendering style is a nuisance variable a faithful reader should ignore. Redrawing the same data therefore yields images that are semantically equivalent _by construction_ and that share an exact, programmatically known answer, together with exact ground truth for every intermediate read. We call such a family a _render-equivalence set_ (Fig. 1). It serves as a measurement instrument: correctness becomes exactly observable and concentration estimable without confounding, so the coupling between them can be studied rather than assumed.

We build that instrument (RENDEQ), define the two quantities it supports, _render-equivalence agreement_ (REA\mathrm{REA}) and _render marginalization_ (RM\mathrm{RM}), and use them to estimate the coupling on Qwen2.5-VL-7B, Qwen2.5-VL-3B, and InternVL2-8B. We report four results, checked across three independently generated RENDEQ instantiations: re-rendering beats resampling on both accuracy and reliability; agreement beats an evidence-carrying baseline on two of three models and ties on the third; the dispersion behind all of this is concentrated in one style factor rather than spread across many; and fine-tuning on cross-render consensus inverts, cutting accuracy rather than raising it. Section 4 derives each as a prediction, Table 2 sets them against the outcomes, and Sec. 6 reports the numbers and confidence intervals in full.

#### Contributions

Our contributions are the instrument, the measurement, and the boundary condition:

  1. 1.

RENDEQ, a generator and protocol whose exact semantic equivalence, exact programmatic ground truth, and individually togglable style factors make correctness exactly observable and concentration estimable without confounding (Sec. 5).

  2. 2.

A measurement of the coupling, with per-factor attribution identifying which perturbation carries it (Sec. 6); correctness is observed exactly, concentration estimated subject to the bias of Proposition 4(ii).

  3. 3.

A boundary condition on consensus self-training: an empirical inversion of a published positive result, with the mechanism that explains it (Sec. 6.4).

  4. 4.

An analysis (Sec. 4) with three results: agreement is upward-biased for concentration at finite KK, with an unbiased pairwise alternative; it certifies correctness only above a threshold set by how diffuse the model’s errors are; and render dispersion decomposes over style factors, bounding what any single-factor ablation can remove.




We claim neither priority over input-perturbation consistency [1, 3] nor novelty for the concentration-versus-correctness distinction itself, which the self-consistency literature states. What re-rendering adds is exactness, and what exactness buys is measurement.

D=(3,7,5,4)D=(3,7,5,4)qq __a ⋆=7a^{\star}=7x1x_{1}x2x_{2}x3x_{3}⋯\cdotsK=8K{=}8a⋆a^{\star}REA=58\mathrm{REA}=\tfrac{5}{8}RM=7\mathrm{RM}=7a⋆a^{\star}REA=1\mathrm{REA}=1RM=5\mathrm{RM}=5×\times

Figure 1: Agreement measures the height of the tallest bar; correctness asks where it stands. One dataset is drawn under KK styles that leave the answer unchanged, so any disagreement is the model’s. Histograms are answer distributions over the K=8K{=}8 renderings: REA\mathrm{REA} reads the tallest bar’s share, RM\mathrm{RM} its position, and only the second is comparable with a⋆a^{\star}. Model A is split yet right; model B is unanimous and wrong, so agreement ranks B above A, which is why Proposition 5 conditions on how diffuse a model’s errors are. Renderings differ in plotting library (Fig. 2b); values are illustrative.

## 2 Related work

#### Consensus as a reliability signal.

Self-consistency over reasoning paths [5], resampled responses and task decompositions [6, 7], semantic clusters [8, 9], and geometric quantities inside a pipeline [10] all read reliability off agreement. Closest are the methods that perturb the _input_ : Zhang et al. [1] blur images and rephrase questions, and Rosenfeld et al. [2] show at scale that stability under benign perturbations predicts correctness. Park et al. [11] instead score dependence on visual evidence, and Xiao et al. [12] calibrate with training and labels. Our object is not another such score but the premise they share; Table A1 in Appendix A places us against them. That the premise can fail is itself understood: agreement certifies a property of the model’s answer distribution rather than its correctness, and Estornell and Liu [4] analyze how correlated errors let majority voting settle on a wrong answer. Our analysis restates this for input perturbation and adds the continuous case; our contribution is not the distinction but a setting in which one side is exactly observable and the other estimable without confounding, so the two can be related empirically.

#### Consensus as a training signal.

Kaya et al. [3] aggregate over semantics-preserving input augmentations at test time and then fine-tune on the resulting consensus pseudo-labels, reporting gains across nine benchmarks; classical test-time augmentation aggregates over input perturbations in embedding space [13]. Section 6.4 reports the opposite outcome for the fine-tuning half of this recipe and identifies the regime that separates the two results.

#### Chart and figure reasoning.

Benchmarks are mature [14, 15, 16], and recent work raises accuracy via programmatic synthesis and verifiable-reward training [17, 18, 19, 20]: these synthesize _diverse_ charts and need labels for the reward, whereas we hold data fixed and use none at inference. A parallel line documents degradation under perturbation and restyling [21, 22, 23], establishing our premise; work separating perception from reasoning [24] and probing evidence-versus-prior conflict [25, 26, 27] needs curated conflict sets, whereas our decomposition is label-free on non-conflicting figures. Selective prediction and calibration provide the evaluation framing [28, 29, 30], and test-time compute scaling motivates the cost RM\mathrm{RM} pays [31].

## 3 Render-equivalence sets

Let DD be the data underlying a figure and qq a quantitative question with an exact answer a⋆​(D,q)a^{\star}(D,q) computable from DD by a deterministic program. A renderer RR maps data and a style configuration θ∈Θ\theta\in\Theta to an image x=R⁡(D,θ)x=R(D;\theta), where θ\theta controls nuisance factors that do not change the encoded data: plotting library, palette, theme, gridlines, aspect ratio, marker shape, font, ticks, legend, resolution.

###### Definition 1 Render-equivalence set.

Given (D,q)(D,q) and styles θ1,…,θK\theta_{1},\dots,\theta_{K}, the render-equivalence set is 𝒳(D,q)={xi=R(D;θi)}i=1K\mathcal{X}(D,q)=\\{x_{i}=R(D;\theta_{i})\\}_{i=1}^{K}. By construction every xix_{i} shares the answer a⋆​(D,q)a^{\star}(D,q).

A VLM ff produces a parsed answer y^i=parse⁡(f⁡(xi,q))\hat{y}_{i}=\mathrm{parse}(f(x_{i},q)) per rendering; ff is a black box and only its emitted answers are used.

#### Agreement (REA\mathrm{REA}).

For categorical answers, with m^\hat{m} the modal answer among {y^i}\\{\hat{y}_{i}\\},

| REAcat=1K∑i𝟏[y^i=m^]∈(0,1].\mathrm{REA}_{\text{cat}}=\tfrac{1}{K}\textstyle\sum_{i}\mathbf{1}[\hat{y}_{i}=\hat{m}]\in(0,1]. |  | (1)  
---|---|---|---  
  
For continuous answers, with y~\tilde{y} the median, relative tolerance τ\tau, and small ε>0\varepsilon>0 guarding the division,

| REAnum=1K∑i[|y^i−y~||y~|+ε≤τ].\mathrm{REA}_{\text{num}}=\tfrac{1}{K}\textstyle\sum_{i}\mathbf{1}\\!\left[\tfrac{|\hat{y}_{i}-\tilde{y}|}{|\tilde{y}|+\varepsilon}\leq\tau\right]. |  | (2)  
---|---|---|---  
  
Both are computed without ground truth. At KK renderings REA\mathrm{REA} takes at most KK distinct values, bounding the resolution of any threshold rule built on it.

#### Aggregation (RM\mathrm{RM}) and error decomposition.

We take the mode for categorical answers, ties broken by first-seen rendering order, and the median for continuous answers. RM\mathrm{RM} uses no labels and costs KK forward passes. We aggregate at the answer level; Kaya et al. [3] report that token-level aggregation is stronger, which we do not test here. The program computing a⋆a^{\star} also exposes the intermediate quantities it consumes, which we query separately, partitioning each instance into: all reads and answer correct; all reads correct but answer wrong (a reasoning failure); at least one read wrong (a perception failure, whatever the answer). The third cell is not a subset of the errors, since a wrong read can still yield a correct answer by coincidence.

## 4 What agreement measures

Aggregation itself is standard: modal voting over i.i.d. answers concentrates exponentially, and the sample median converges to the median of the read distribution (Lemmas 9 and 10, Appendix B). Neither speaks to correctness, which is the relationship the rest of the paper is concerned with. The results below rest on two assumptions.

###### Assumption 2 Exchangeable renderings.

Conditional on (D,q)(D,q), the answers y^1,…,y^K\hat{y}_{1},\dots,\hat{y}_{K} are i.i.d. draws from a distribution PP induced by the style distribution and the model. Where a mode is referenced we assume it is unique.

###### Assumption 3 Factored style space.

Θ=Θ1×⋯×ΘJ\Theta=\Theta_{1}\times\cdots\times\Theta_{J} is a product over JJ nuisance factors and θ\theta is drawn with independent coordinates. RENDEQ enforces this by construction (Sec. 5).

Assumption 2 is an idealization: it holds when style acts as independent noise on the read and fails when the model has a style-invariant bias, the regime Estornell and Liu [4] analyze for correlated voters. Proposition 5 characterizes that failure mode in terms of quantities RENDEQ can estimate.

### 4.1 Agreement estimates concentration, with a bias

Write π=maxa⁡P⁡(a)\pi=\max_{a}P(a) for the modal mass, m⋆m^{\star} for the mode, and Z=𝟏[m⋆=a⋆]Z=\mathbf{1}[m^{\star}=a^{\star}] for whether the mode is the correct answer.

###### Proposition 4 What REA\mathrm{REA} estimates.

Under Assumption 2, for categorical answers:

  1. (i)

REAcat→π\mathrm{REA}_{\text{cat}}\to\pi and 𝟏[y^RM=a⋆]→Z\mathbf{1}[\hat{y}_{\mathrm{RM}}=a^{\star}]\to Z almost surely as K→∞K\to\infty. The limit of REA\mathrm{REA} does not depend on a⋆a^{\star}.

  2. (ii)

𝔼⁡[REAcat]≥π\mathbb{E}[\mathrm{REA}_{\text{cat}}]\geq\pi at every finite KK, strictly unless π=1\pi=1.

  3. (iii)

The pairwise statistic REApair=(K2)−1∑i<j𝟏[y^i=y^j]\mathrm{REA}_{\text{pair}}=\binom{K}{2}^{-1}\sum_{i<j}\mathbf{1}[\hat{y}_{i}=\hat{y}_{j}] is unbiased for the collision probability A=∑aP​(a)2A=\sum_{a}P(a)^{2}, and π2≤A≤π\pi^{2}\leq A\leq\pi.




Part (ii) is a selection effect: REAcat\mathrm{REA}_{\text{cat}} is the empirical _maximum_ of a multinomial frequency vector, so the winning answer is chosen partly by noise and its share is inflated, not negligibly at practical budgets (Appendix C works a numeric example), so any calibration of REA\mathrm{REA} at small KK is optimistic by construction. Part (iii) supplies an unbiased alternative, which matters because our factor attribution (Sec. 6.3) already uses a _pairwise_ rate while REA\mathrm{REA} is modal; π2≤A≤π\pi^{2}\leq A\leq\pi is the conversion.

### 4.2 Where agreement can lie

Let β=maxa≠a⋆⁡P⁡(a)\beta=\max_{a\neq a^{\star}}P(a) be the mass of the leading wrong answer.

###### Proposition 5 Confident errors must be concentrated.

Under Assumption 2:

  1. (i)

π=max⁡(P⁡(a⋆),β)\pi=\max\big(P(a^{\star}),\,\beta\big) and Z=𝟏[P(a⋆)>β]Z=\mathbf{1}[P(a^{\star})>\beta].

  2. (ii)

On instances with Z=0Z=0, π=β\pi=\beta: the agreement being reported _is_ the mass of a single wrong answer.

  3. (iii)

Call the errors _diffuse at level_ L≥1L\geq 1 if β≤(1−P⁡(a⋆))/L\beta\leq(1-P(a^{\star}))/L. Then Z=0Z=0 implies π≤1/L\pi\leq 1/L; equivalently, π>1/L\pi>1/L certifies Z=1Z=1.




This is the precise form of the idiosyncratic-versus-systematic distinction the literature states informally. By (ii), agreement is high and wrong only when one specific wrong answer carries the agreement mass; dispersion spread over many wrong answers cannot produce a confidently wrong consensus. By (iii), diffuseness converts into a certifying threshold: with wrong mass over two alternatives, agreement above 1/21/2 certifies the mode; over three, above 1/31/3; at L=1L{=}1, a single systematic misread, the threshold is 11 and nothing certifies (Fig. A1). Where Corollary 6 identifies the coupling as the quantity of interest, Proposition 5 identifies the property of the model that supplies it.

LL references a⋆a^{\star}, so it cannot be estimated at use time. It can be estimated offline on any corpus with programmatic ground truth, which is exactly what RENDEQ supplies: measure LL on the generator, then apply the threshold 1/L1/L label-free elsewhere. Measuring LL on the generator is therefore what licenses a threshold applied elsewhere.

We estimated L^\hat{L} on every wrong-mode instance in the replicated pool and found it concentrated toward the low-diffuseness end (median 1.331.33–1.501.50 across models, so the certifying threshold 1/L^1/\hat{L} is typically well above the midpoint); Appendix E gives the full distribution and ties it to which families drive B1’s remaining advantage over REA\mathrm{REA} (Table 3).

###### Corollary 6 The coupling is what matters.

Let instances be drawn from a population inducing random variables (π,Z)(\pi,Z). The limiting AUROC of REA\mathrm{REA} as a predictor of RM\mathrm{RM}’s correctness is Pr[π1>π0]+12Pr[π1=π0]\Pr[\pi_{1}>\pi_{0}]+\tfrac{1}{2}\Pr[\pi_{1}=\pi_{0}], where π1\pi_{1} and π0\pi_{0} are draws of π\pi given Z=1Z{=}1 and Z=0Z{=}0. If π⟂Z\pi\perp Z it is 12\tfrac{1}{2}, and there exist populations on which REA→1\mathrm{REA}\to 1 while RM\mathrm{RM} is wrong with probability →1\to 1.

Our AUROC values are computed at K=8K{=}8, where REA\mathrm{REA} estimates π\pi noisily and with bias, so they need not equal this limit; we do not assume a sign for the gap.

### 4.3 Which perturbation carries the dispersion

Let y^​(θ)\hat{y}(\theta) be the answer under style θ\theta, and define the pairwise disagreement D=Prθ,θ′[y^(θ)≠y^(θ′)]D=\Pr_{\theta,\theta^{\prime}}[\hat{y}(\theta)\neq\hat{y}(\theta^{\prime})] for independent θ,θ′\theta,\theta^{\prime}. Let DjD_{j} be the same quantity when only coordinate jj is resampled, and D−jD^{-j} when coordinate jj is held _fixed_ and shared.

###### Proposition 7 Factor decomposition.

Under Assumption 3, D≤∑j=1JDjD\leq\sum_{j=1}^{J}D_{j}. Equality requires both that the single-factor flip events along the hybrid chain be almost surely disjoint and that no flip be reversed by a later one; either failing makes the bound strict. Moreover D−Dj≤D−j≤DD-D_{j}\leq D^{-j}\leq D for every jj.

The first bound licenses reading Sec. 6.3 as a decomposition rather than a list of correlations: a factor with small DjD_{j} contributes at most DjD_{j} however many levels it has, so perturbation _identity_ matters, not _diversity_ (the gap ∑jDj−D\sum_{j}D_{j}-D upper-bounds interaction and cancellation rather than measuring them). The second bound predicts the ablation this paper most needs: holding one factor fixed cannot remove more than that factor’s own contribution, so unless a single factor accounts for essentially all of DD, holding the plotting library fixed should _attenuate_ the effect rather than eliminate it (Sec. 6.3 reports the DjD_{j}; the totals needed to make this quantitative are among the missing items there).

###### Remark 8  Small even KK.

For K=2K{=}2 the sample median is the mean of the two reads, so RM\mathrm{RM} can be wrong where a single rendering was right. Accuracy under median aggregation is not monotone in KK near K=2K{=}2. This is a property of the estimator, not of render-equivalence.

Together the three propositions give the four predictions tested in Sec. 6: aggregation helps wherever dispersion exists (Lemmas 9 and 10); the perturbation with the largest DjD_{j} wins at a matched budget (Proposition 7); agreement need not beat signals carrying evidence rather than dispersion (Corollary 6); and an objective that raises π\pi while lowering diffuseness LL destroys its own certificate (Proposition 5). Proofs are in Appendix C.

## 5 RENDEQ

RENDEQ is a generator and evaluation protocol built for control rather than scale: every instance carries exact ground truth and only cosmetic style varies within a set, so any answer change is attributable to style. Three properties make it an instrument for Corollary 6: equivalence holds by construction, so π\pi is estimable without confounding; the key is programmatic, so ZZ is observable; and factors are individually togglable, so each perturbation’s contribution can be attributed.

#### Instance and axes.

An instance is a tuple (D,q,a⋆,{rj},{(θi,xi)}i=1K)(D,q,a^{\star},\\{r_{j}\\},\\{(\theta_{i},x_{i})\\}_{i=1}^{K}): data, question, exact answer, the exact intermediate reads consumed by the answer program, and KK renderings with logged style configurations (default K=8K{=}8). Four axes vary independently (Table 1), fixing what is asked (plot family, question type), the style space Θ\Theta (style groups), and how hard the read is (difficulty controls).

#### Diagnostics and scope.

Beyond REA\mathrm{REA} and RM\mathrm{RM}, RENDEQ defines two reusable per-instance diagnostics: render-flip rate, RFR=1|𝒟|∑𝟏[|{y^i}|>1]\mathrm{RFR}=\frac{1}{|\mathcal{D}|}\sum\mathbf{1}[|\\{\hat{y}_{i}\\}|>1], which measures instability with no ground truth, and render-equivalence robustness, RER=1K​∑iacc⁡(y^i)\mathrm{RER}=\frac{1}{K}\sum_{i}\mathrm{acc}(\hat{y}_{i}), style-averaged accuracy, which needs ground truth and is for evaluation only. A majority of instances have at least one disagreeing rendering on every model (RFR 0.590.59–0.730.73), and RFR is strongly negatively correlated with per-family accuracy (r=−0.69r{=}{-0.69}); Sec. E.2 gives the per-model and per-family numbers. All results here use a single in-style synthetic split; the generator also supports an out-of-style split and a real-data anchor built by re-rendering tables from a public benchmark, neither run for this paper, so external validity to real charts is untested (see Limitations).

Axis |  Levels  
---|---  
Plot family |  bar, grouped bar, stacked bar, line, scatter, pie, log-axis  
Question type |  value read, comparison, extremum, trend sign, arithmetic  
Style Θ\Theta |  library, palette, theme, gridlines, aspect ratio, marker, font, ticks, legend, resolution  
Difficulty |  #series, #points, precision, near-ties, overlap  
Table 1: RENDEQ axes. Style groups are individually togglable so a single nuisance factor can be varied in isolation, which is what makes the attribution in Sec. 6.3 causal with respect to style.

## 6 Experiments

000.050.050.10.10.150.15∙\bulletRM−\mathrm{RM}-∘\circREA−\mathrm{REA}-____

0 00.040.040.080.080.120.12

0.350.350.450.450.550.550.650.65

Figure 2: The effect is attributable, concentrated, and not safe to optimize. (a) At a matched K=8K{=}8 budget, pooled across three instantiations on the corrected pipeline (Appendix D), varying the rendering outperforms varying the decoding sample for every model and both uses: +4.8+4.8 to +6.3+6.3 accuracy points for RM−\mathrm{RM}{-}SC and +0.06+0.06 to +0.16+0.16 AUROC for REA−\mathrm{REA}{-}B3. Bars show 95% cluster-bootstrap intervals based on 5,000 resamples; filled markers denote accuracy and hollow markers denote reliability. (b) Dispersion is concentrated rather than distributed across cosmetic styles. The plotting-library effect is more than twice the next-largest effect and approximately an order of magnitude above the noise floor. Stems indicate across-model means, with rows ordered accordingly. (c) Results for Qwen2.5-VL-7B, pooled across a five-run replication. Color identifies the split rather than the model. Fine-tuning on the model’s own K=8K{=}8 majority increases hold-out agreement in every run while reducing hold-out accuracy in every run. Table 2: The paper’s four predictions, each evaluated across three independent RENDEQ instantiations (Sec. 6). †See Sec. 6.1 for model-level results and Appendix D for the earlier retracted reversal.

Prediction |  Test |  Outcome |  Replicated?  
---|---|---|---  
Aggregation helps |  Sec. 6.2 |  3/3 models |  Yes, 3 instantiations  
Render >> sample, accuracy |  Sec. 6.2 |  3/3 models |  Yes, 3 instantiations  
Render >> sample, reliability |  Sec. 6.1 |  3/3 models |  Yes, 3 instantiations  
Agreement vs. evidence |  Sec. 6.1 |  _Rejected_ , 2/3† |  Yes, 3 instantiations  
Consensus training inverts |  Sec. 6.4 |  Accuracy drop, 5/5 runs |  Yes in direction; magnitude unstable  
  
#### Setup.

Every headline number here (Tables 3 and 4) is pooled over three independently generated RENDEQ instantiations (generator seeds 0, 1, 2; N=350N{=}350 instances each, 7 families, K=8K{=}8 renderings, no shared instances), replacing an earlier single-instantiation design (Appendix D). “Seed” always means a generator instantiation, not a decoding seed; decoding is greedy (temperature 0) in the main runs, deterministic and contributing no additional variance. Models are Qwen2.5-VL-7B-Instruct, Qwen2.5-VL-3B-Instruct, and InternVL2-8B [32, 33], unchanged throughout (GPU and quantization settings in Appendix D). Of the 3150 pooled instances, 930 (29.5%29.5\%) are numeric (Lemma 10), the rest categorical (Lemma 9). All three models date to 2024 or early 2025 and two share a family (Qwen2.5-VL); we did not add a current-generation model from a third family (see Limitations).

#### Metrics and baselines.

All REA\mathrm{REA} values below are modal, upward-biased at finite KK (Proposition 4(ii)); the unbiased pairwise alternative REApair\mathrm{REA}_{\text{pair}} gives the same ranking against B1 (Appendix G). Accuracy uses a τ=5%\tau{=}5\% relative tolerance for numeric answers and exact match for categorical; τ\tau is load-bearing in magnitude and, on one model, in direction too (Appendix G). We report AUROC against correctness, risk–coverage AUC, and ECE after min-max normalizing each signal; bootstrap intervals use 5000 resamples unless noted, and paired accuracy comparisons use McNemar’s test. Baselines: B1 mean token log-probability; B2 verbalized confidence; B3 response self-consistency over K=8K{=}8 samples at a fixed rendering [5]; B4 the consistency signal of Khan and Fu [6]; B5 a prompt ensemble over three phrasings. B3 is the mechanism control, holding the image fixed and varying only decoding, so the REA\mathrm{REA}/B3 and RM\mathrm{RM}/B3 contrasts isolate render-induced from sampling-induced dispersion at equal call count. We did not run semantic entropy, P(True), or an approximate-perturbation arm (see Limitations).

### 6.1 Measuring the coupling

Signal | 7B | 3B | IVL-8B  
---|---|---|---  
B1 token logprob | 0.7710.771 | 0.8670.867 | 0.8750.875  
REA\mathrm{REA} (ours) | 0.864 | 0.858 | 0.907  
Δ\Delta (REA−\mathrm{REA}{-}B1) | +0.094+0.094 | −0.009-0.009 | +0.033+0.033  
95% CI | [+.066,+.121][{+}.066,{+}.121] | [−.030,+.011][{-}.030,{+}.011] | [+.013,+.053][{+}.013,{+}.053]  
  
Table 3: REA\mathrm{REA} beats B1, mean token log-probability, on AUROC against correctness on two of three models, and is statistically tied with it on the third; pooled over three independently generated RENDEQ instantiations (seeds 0, 1, 2; N=1050N{=}1050 per model, K=8K{=}8; cluster bootstrap over instances). B2–B5 are pooled the same way; see Appendix D for the full table.

REA\mathrm{REA}’s confidence interval excludes zero in its own favor on 7B and InternVL2-8B; on 3B the interval includes zero, a statistical tie. All REA\mathrm{REA} values are modal and upward-biased at finite KK (Proposition 4(ii)); Appendix D shows the ranking is unchanged under the unbiased pairwise alternative.

#### Re-rendering versus resampling.

REA\mathrm{REA} beats B3, the fixed-image self-consistency control, on all three models: pooled across the three independently generated instantiations used for Table 3 (N≈3150N{\approx}3150), Δ=+0.102\Delta=+0.102, CI [+0.083,+0.121][+0.083,+0.121], p<10−4p<10^{-4} (Appendix D gives the per-model breakdown, +0.061+0.061 to +0.157+0.157). This attributes the reliability signal to re-rendering specifically, rather than to generic answer instability, corroborating Kaya et al. [3] in a setting where the augmentation is exactly meaning-preserving. The accuracy comparison behind this prediction (Sec. 6.2) uses RM\mathrm{RM}, not REA\mathrm{REA}, and agrees in direction: both halves of the render-versus-sample prediction now point the same way.

#### Agreement versus evidence.

Against B1, mean token log-probability, the picture is genuinely mixed rather than uniform in either direction: pooled over three independently generated RENDEQ instantiations, REA\mathrm{REA} beats B1 on Qwen2.5-VL-7B (+0.094+0.094, CI [+0.066,+0.121][+0.066,+0.121]) and InternVL2-8B (+0.033+0.033, CI [+0.013,+0.053][+0.013,+0.053]), and the two are statistically tied on Qwen2.5-VL-3B (−0.009-0.009, CI [−0.030,+0.011][-0.030,+0.011], includes zero). We do not claim agreement dominates evidence-carrying signals in general (the prediction that motivated this comparison, Sec. 4, expected B1 to win, and it does not, on the models where the comparison is decisive), and the ranking is stable across the numeric-tolerance parameter τ\tau on two of three models (Appendix G). This is Corollary 6 in data: REA\mathrm{REA} estimates dispersion and cannot carry evidence, while a token log-probability can, and here it does. An earlier version of this comparison, computed on a rendering pipeline where a silent library-export failure had collapsed all three "independent instantiations" to matplotlib-only images, reported the opposite direction on every model; Appendix D describes that bug, why it produced this specific reversal, and how we found it.

REA\mathrm{REA} beating B1 head-to-head on two of three models does not mean B1 carries no information REA\mathrm{REA} lacks: the two signals make partly independent errors on every model, and a cross-validated logistic combination of them beats B1 alone on every model, including 3B (Appendix E gives the AUROC gains and CIs).

### 6.2 Aggregation

Model | single | SC | RM\mathrm{RM} | RM−\mathrm{RM}{-}SC  
---|---|---|---|---  
Qwen2.5-VL-7B | 0.6440.644 | 0.6440.644 | 0.7010.701 | 0.0570.057  
Qwen2.5-VL-3B | 0.5710.571 | 0.5630.563 | 0.6260.626 | 0.0630.063  
InternVL2-8B | 0.5630.563 | 0.5760.576 | 0.6240.624 | 0.0480.048  
Table 4: RM\mathrm{RM} beats both single-render decoding and self-consistency (SC) on every model at a matched K=8K{=}8 budget, pooled over three RENDEQ instantiations (N=1050N{=}1050 per model). SC: response self-consistency at fixed image, temperature 0.7, majority vote over 8 samples. 95% CIs in Appendix E.

Aggregation holds: RM\mathrm{RM} improves on single-render decoding by 5.5 to 6.1 points, and on self-consistency (SC) by 4.8 to 6.3 points, on every model, pooled across three independent instantiations, every interval excluding zero. SC’s own advantage over plain single-render decoding is smaller and less consistent in sign than re-rendering’s advantage under RM\mathrm{RM} (Appendix E), so the render-versus-sample accuracy claim still holds; one caveat is that the main RM\mathrm{RM} runs decode at temperature 0 while SC needs 0.7 to vary at all, so the contrast is at equal call count but not equal decoding configuration. This table omits Jiang and Luo’s method, the closest label-free test-time approach for charts (Table A1), and token-level aggregation, reported as stronger by Kaya et al. [3] (see Limitations). The intermediate-read query defined in Sec. 3 decomposes these errors into perception and reasoning failures (Appendix E, Sec. E.1): roughly four fifths of instances have at least one bad intermediate read, and true reasoning failures with every read correct are rare.

### 6.3 Identity, not diversity

For each style factor and instance we compute the cross-level disagreement rate, the fraction of render pairs where the factor level differs and the parsed answers differ, minus the within-level rate as a noise floor. Pooled over the three replicated instantiations and all three models (N≈3150N{\approx}3150 render pairs per factor; cluster bootstrap over instances, 3000 resamples):

Factor | Lift | 95% CI  
---|---|---  
library | 0.1020.102 | [+0.084,+0.120][+0.084,+0.120]∗  
bar_labels | 0.0430.043 | [+0.025,+0.060][+0.025,+0.060]∗  
bar_orient | 0.0190.019 | [+0.001,+0.036][+0.001,+0.036]∗  
tick_density | 0.0090.009 | [−0.008,+0.026][-0.008,+0.026]  
pie_start_angle | 0.0090.009 | [−0.009,+0.026][-0.009,+0.026]  
(9 further factors) | ≤+0.007\leq+0.007 | all include zero  
  
The plotting library, matplotlib against plotly, dominates: its lift is more than twice the second-largest factor’s and its interval clears zero by a wide margin. bar_labels and bar_orient have small but real lifts (both intervals exclude zero, though barely for the latter); every other factor’s interval includes zero, so we do not claim they contribute nothing, only that this design cannot distinguish their contribution from noise. By Proposition 7 these lifts bound each factor’s contribution to the total: what matters is not how _many_ perturbations are applied but _which_ , and a practitioner on a budget should vary the backend before anything else. It is also the finding that most constrains our claim, since switching backend is less purely cosmetic than a palette change. This table could not even be computed on an earlier, buggy version of the pipeline, and the mechanism-isolating ablation it would motivate (library held fixed) remains genuinely missing, too few instances have all eight renderings in one library to power it (Appendix D).

### 6.4 Consensus self-training can invert

Kaya et al. [3] fine-tune on consensus pseudo-labels derived from augmented inputs and report gains across nine benchmarks. Proposition 4 says such an objective raises π\pi without moving m⋆m^{\star}, so it should help only where the coupling is already strong. We ran the same recipe on RENDEQ: LoRA (r=8r{=}8, 3 epochs) on Qwen2.5-VL-7B with the model’s own K=8K{=}8 majority as the label and no ground truth, training on bar, grouped bar, stacked bar, line, scatter (250 instances) and holding out pie and log-axis (100 instances).

We ran this recipe five times: three decoding seeds on one dataset instantiation, plus one seed each on the two other independently generated instantiations used elsewhere in this paper (Appendix D). Accuracy fell under RM\mathrm{RM} in every run, by 3.6 to 21.2 points on training families and 10.4 to 27.2 on held-out ones; under single-render decoding, held-out accuracy fell in all five runs (8.4 to 18.8 points), while training-family accuracy fell in three of five and rose slightly in two (+0.6+0.6, +1.0+1.0 points). The held-out collapse is more consistent and more severe, and it is also the split with no ground-truth-adjacent signal at fine-tuning time, so it is the one the analysis is really about: on families where the base majority was already wrong, notably scatter, the objective trained the model to hold the wrong answer more tightly rather than to correct it, though the size of that effect is instantiation-dependent (Appendix D). We did not replicate Kaya et al. [3] (they augment natural images and aggregate at the token level, we re-render figures and aggregate at the answer level, and the models differ), but what the two share is the objective, which Proposition 5 predicts is regime-dependent. REA\mathrm{REA}’s AUROC change tracks this split and is consistent within each: it rose in every run on held-out families (0.009 to 0.100), the model growing more confidently self-consistent on families it now answers worse; it fell in every run on training families (0.014 to 0.124), the opposite of what fine-tuning on a family’s own majority vote should do if the sharpening tracked correctness.

## 7 Conclusion

Across four checks, the coupling between agreement and correctness turned out to be real, measurable, and neither as strong nor as fragile as it first looked. Render marginalization beats every control we matched it against, on every model and every replicated instantiation: the one result here that never moved, not under replication and not under the rendering-pipeline bug that moved almost everything else. Cross-render agreement, a purely label-free signal, beats an evidence-carrying baseline on two of three models rather than losing outright, visible only once the render-equivalence perturbation was actually applied: a reminder that a measurement instrument built to isolate a quantity can still be defeated by an implementation detail far from the theory it tests. And exactly as Proposition 5 predicts, optimizing for agreement directly breaks the coupling rather than exploiting it: fine-tuning on a model’s own consensus makes it agree with itself more and know less, inverting a result reported elsewhere rather than merely failing to reproduce it. Together these argue for treating concentration and correctness as related but separable quantities, not proxies for one another: a separation render-equivalence sets make directly measurable, so the same instrument that lets a reviewer check our numbers also checks whether agreement is safe to optimize for. Here, it is not.

## Limitations

Every number here comes from a single in-style synthetic split of our own generator. The out-of-style split and the real-data anchor were not run, so external validity to real charts is untested, and the results characterize behaviour on RENDEQ rather than on chart question answering generally. Our negative result for consensus self-training is likewise measured on one generator, one model, and one LoRA configuration; we checked it across three decoding seeds and three dataset instantiations (Appendix D) and the direction of the accuracy drop held in every run, but its magnitude did not, so the LoRA configuration, model, and generator remain unvaried. It is not a replication of Kaya et al. [3], whose augmentations, aggregation level, models and benchmarks all differ, and it should be read as identifying a regime in which the objective fails rather than as evidence against their finding.

The experimental programme is incomplete in ways we state rather than leave to the reader to notice. Three arms are absent and each bears on a claim we make. There is no _approximate_ -perturbation arm: B3 separates re-rendering from decoding noise, but nothing separates exact equivalence from ordinary pixel augmentation, which is the delta this paper argues for, so that delta is currently reasoned rather than measured. The baseline set omits semantic entropy [8, 9] and P(True), the two standard label-free signals, and a direct run of Zhang et al. [1]. And Jiang and Luo [34], the closest label-free test-time method for charts, is discussed but not run against RM\mathrm{RM}.

Four further gaps are smaller but real. Our models date to 2024 and early 2025 and two of the three share a family. The tolerance τ\tau is load-bearing throughout and never varied. We report threshold-free summaries, AUROC and risk–coverage area, but no accuracy at fixed coverage and no held-out threshold selection, which is what a deployed abstention rule would need. We make roughly eighteen paired comparisons across signals, models and metrics without correcting for multiple testing. Finally, the perception-versus-reasoning split in Appendix E (Sec. E.1) rests entirely on a separate intermediate-read query whose own reliability we never validate.

The analysis assumes a unique mode where one is referenced, and Proposition 5(iii) is stated in terms of a diffuseness level LL that we have not yet measured. Assumption 2 treats renderings as i.i.d. draws. Real style spaces are finite and correlated, and Sec. 6.3 shows one factor dominates, so the assumption is a working idealization whose failure mode is the bias regime the propositions identify. Until the library-held-fixed ablation is run we cannot separate sensitivity to cosmetic style in general from sensitivity to the plotting backend, and that ablation could narrow the paper’s scope.

We aggregate at the answer level, while Kaya et al. [3] report token-level aggregation is stronger; we have not tested whether that changes any conclusion. RM\mathrm{RM} cannot fix systematic, style-invariant errors and costs K×K\times inference.

Agreement beats token log-probability on two of the three models we tested and is statistically tied with it on the third, replicated across three independently generated instantiations (Appendix D). This replication went through an intermediate stage, reported in full in that appendix, in which a rendering-pipeline bug silently removed the render diversity the comparison depends on and produced the opposite conclusion on every model; we found and fixed that bug before finalizing the numbers reported here. We do not claim agreement is a universally stronger label-free signal (the comparison is a tie on one of three models, and the theory, Sec. 4, predicts model- and data-dependence rather than a universal ranking), but the direction of the evidence, once the rendering pipeline actually renders what it is asked to, favours agreement more often than not on this benchmark. The K-ablation in Appendix G and the calibration numbers in Appendix F have both been recomputed on the corrected three-instantiation pool, and the apparent denominator mismatch in the error-decomposition breakdown has been traced to a labeling ambiguity rather than a data error (Sec. E.1).

DATA AND CODE AVAILABILITY

The generator, the agreement and aggregation code, and the evaluation scripts are available now at <https://github.com/KurbanIntelligenceLab/rendeq>, with pinned versions and seeds. The RENDEQ data (generated instances, manifests, and rendered images) are available at <https://huggingface.co/datasets/rasulkhanbayov/rendeq> under CC-BY-4.0; the generator, agreement/aggregation code, and evaluation scripts under the MIT license.

## References

  * [1] R. Zhang, H. Zhang, and Z. Zheng (2024) Vl-uncertainty: detecting hallucination in large vision-language model via uncertainty estimation.  arXiv preprint arXiv:2411.11919.  Cited by: Table A1, §1, §1, §2, Limitations. 
  * [2] A. Rosenfeld, N. Glazer, and E. Fetaya (2025) Questioning the stability of visual question answering.  arXiv preprint arXiv:2511.11206.  Cited by: Table A1, §1, §2. 
  * [3] M. O. Kaya, D. Elliott, and D. Papadopoulos (2026) Efficient test-time scaling for small vision-language models.  In International Conference on Learning Representations,  Vol. 2026, pp. 146270–146312.  Cited by: Table A1, §1, §1, §2, §3, §6.1, §6.2, §6.4, §6.4, Limitations, Limitations. 
  * [4] A. Estornell and Y. Liu (2024) Multi-llm debate: framework, principals, and interventions.  Advances in Neural Information Processing Systems 37, pp. 28938–28964.  Cited by: §1, §2, §4. 
  * [5] X. Wang, J. Wei, D. Schuurmans, Q. Le, E. Chi, S. Narang, A. Chowdhery, and D. Zhou (2022) Self-consistency improves chain of thought reasoning in language models.  arXiv preprint arXiv:2203.11171.  Cited by: Table A1, §2, §6. 
  * [6] Z. Khan and Y. Fu (2024) Consistency and uncertainty: identifying unreliable responses from black-box vision-language models for selective visual question answering.  In 2024 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR),  pp. 10854–10863.  Cited by: Table A1, Appendix F, §2, §6. 
  * [7] Q. Yang, W. Yan, and A. Agrawal (2024) Decompose and compare consistency: measuring vlms’ answer reliability via task-decomposition consistency comparison.  In Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing,  pp. 3613–3627.  Cited by: §2. 
  * [8] L. Kuhn, Y. Gal, and S. Farquhar (2023) Semantic uncertainty: linguistic invariances for uncertainty estimation in natural language generation.  arXiv preprint arXiv:2302.09664.  Cited by: §2, Limitations. 
  * [9] S. Farquhar, J. Kossen, L. Kuhn, and Y. Gal (2024) Detecting hallucinations in large language models using semantic entropy.  Nature 630 (8017), pp. 625–630.  Cited by: §2, Limitations. 
  * [10] K. Kim and K. Chelikavada (2026) Zoom consistency: a free confidence signal in multi-step visual grounding pipelines.  arXiv preprint arXiv:2604.15376.  Cited by: §2. 
  * [11] S. Park, C. Oh, H. K. Choi, S. Du, and S. Li (2026) VAUQ: vision-aware uncertainty quantification for lvlm self-evaluation.  In Findings of the Association for Computational Linguistics: ACL 2026,  pp. 26534–26550.  Cited by: §2. 
  * [12] W. Xiao, X. Xinchi, and L. Gan (2026) VL-calibration: decoupled confidence calibration for large vision-language models reasoning.  In Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers),  pp. 44791–44815.  Cited by: §2. 
  * [13] M. Zanella and I. B. Ayed (2024) On the test-time zero-shot generalization of vision-language models: do we really need prompt learning?.  In 2024 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR),  pp. 23783–23793.  Cited by: §2. 
  * [14] S. E. Kahou, V. Michalski, A. Atkinson, Á. Kádár, A. Trischler, and Y. Bengio (2017) Figureqa: an annotated figure dataset for visual reasoning.  arXiv preprint arXiv:1710.07300.  Cited by: §2. 
  * [15] N. Methani, P. Ganguly, M. M. Khapra, and P. Kumar (2020) Plotqa: reasoning over scientific plots.  In 2020 IEEE Winter Conference on Applications of Computer Vision (WACV),  pp. 1516–1525.  Cited by: §2. 
  * [16] A. Masry, J. Q. Tan, S. Joty, E. Hoque, et al. (2022) Chartqa: a benchmark for question answering about charts with visual and logical reasoning.  In Findings of the association for computational linguistics: ACL 2022,  pp. 2263–2279.  Cited by: §2. 
  * [17] Z. Liu, H. Lin, X. Wang, X. Gao, Y. Li, M. Cai, Y. Zhu, Z. Zhong, Q. Pei, Z. Pan, et al. (2026) Chartverse: scaling chart reasoning via reliable programmatic synthesis from scratch.  In Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers),  pp. 7551–7577.  Cited by: §2. 
  * [18] X. Zhang, X. Li, R. Wang, R. Miao, Z. Wang, Y. Wang, D. Roth, and C. Li (2026) Chart-rl: generalized chart comprehension via reinforcement learning with verifiable rewards.  In Proceedings of the First Workshop on Structured Understanding, Retrieval, and Generation in the LLM Era (SURGeLLM 2026),  pp. 107–118.  Cited by: §2. 
  * [19] S. Sinha, O. Frunza, K. Rasul, Y. Nevmyvaka, and A. Zhang (2025) Chart-rvr: reinforcement learning with verifiable rewards for explainable chart reasoning.  arXiv preprint arXiv:2510.10973.  Cited by: §2. 
  * [20] J. Kondic, P. Li, D. Joshi, Z. He, S. Abedin, J. Sun, B. Wiesel, E. Schwartz, A. Nassar, B. Wu, et al. (2025) Chartgen: scaling chart understanding via code-guided synthetic chart generation.  arXiv preprint arXiv:2507.19492.  Cited by: §2. 
  * [21] S. Mukhopadhyay, A. Qidwai, A. Garimella, P. Ramu, V. Gupta, and D. Roth (2024) Unraveling the truth: do vlms really understand charts? a deep dive into consistency and robustness.  In Findings of the Association for Computational Linguistics: EMNLP 2024,  pp. 16696–16717.  Cited by: Table A1, §2. 
  * [22] P. W. Shin, J. Sampson, V. Narayanan, A. Marquez, and M. Halappanavar (2025) Losing the plot: how vlm responses degrade on imperfect charts.  arXiv preprint arXiv:2

509.18425.  Cited by: Table A1, §2. 
  * [23] R. Zhao, A. Shah, X. Zhu, X. Deng, Z. Jiang, Y. Yang, J. Liebelt, and A. Mondal (2026) On robustness and chain-of-thought consistency of rl-finetuned vlms.  arXiv preprint arXiv:2602.12506.  Cited by: §2. 
  * [24] T. Xiao, X. Xu, Z. Huang, H. Gao, Q. Liu, Q. Liu, and E. Chen (2026) Perception-r1: advancing multimodal reasoning capabilities of mllms via visual perception reward.  In International Conference on Learning Representations,  Vol. 2026, pp. 26868–26898.  Cited by: §2. 
  * [25] Z. Wang, Y. He, G. Li, S. Yang, J. Xiong, and S. Liu (2026) V-fat: benchmarking visual fidelity against text-bias.  arXiv preprint arXiv:2601.04897.  Cited by: §2. 
  * [26] K. Chen, Y. Hu, Q. Zhou, Z. Zhu, and W. Luo (2026) CDH-bench: a commonsense-driven hallucination benchmark for evaluating visual fidelity in vision-language models.  arXiv preprint arXiv:2603.27982.  Cited by: §2. 
  * [27] P. Singla, S. Garg, V. Singh, and P. Chopra (2026) Do vision-language models see or guess? measuring and reducing textual-prior reliance with a phrasing-controlled benchmark.  arXiv preprint arXiv:2606.10400.  Cited by: §2. 
  * [28] R. El-Yaniv et al. (2010) On the foundations of noise-free selective classification..  Journal of Machine Learning Research 11 (5).  Cited by: §2. 
  * [29] C. Guo, G. Pleiss, Y. Sun, and K. Q. Weinberger (2017) On calibration of modern neural networks.  In International conference on machine learning,  pp. 1321–1330.  Cited by: §2. 
  * [30] T. Srinivasan, J. Hessel, T. Gupta, B. Y. Lin, Y. Choi, J. Thomason, and K. Chandu (2024) Selective “selective prediction”: reducing unnecessary abstention in vision-language reasoning.  In Findings of the Association for Computational Linguistics: ACL 2024,  pp. 12935–12948.  Cited by: §2. 
  * [31] C. Snell, J. Lee, K. Xu, and A. Kumar (2024) Scaling llm test-time compute optimally can be more effective than scaling model parameters.  arXiv preprint arXiv:2408.03314.  Cited by: §2. 
  * [32] S. Bai, K. Chen, X. Liu, J. Wang, W. Ge, S. Song, K. Dang, P. Wang, S. Wang, J. Tang, H. Zhong, Y. Zhu, M. Yang, Z. Li, J. Wan, P. Wang, W. Ding, Z. Fu, Y. Xu, J. Ye, X. Zhang, T. Xie, Z. Cheng, H. Zhang, Z. Yang, H. Xu, and J. Lin (2025) Qwen2.5-vl technical report.  External Links: 2502.13923, [Link](https://arxiv.org/abs/2502.13923) Cited by: §6. 
  * [33] Z. Chen, W. Wang, H. Tian, S. Ye, Z. Gao, E. Cui, W. Tong, K. Hu, J. Luo, Z. Ma, et al. (2024) How far are we to gpt-4v? closing the gap to commercial multimodal models with open-source suites.  Science China Information Sciences 67 (12), pp. 220101.  Cited by: §6. 
  * [34] G. Jiang and Q. Luo (2025) Chart-coca: self-improving chart understanding of vision lms via code-driven synthesis and candidate-conditioned answering.  In Proceedings of the 34th ACM International Conference on Information and Knowledge Management,  pp. 1168–1178.  Cited by: Table A1, §6.2, Limitations. 



APPENDIX

## Appendix A Positioning

Work | perturbs | equiv. | exact  
---|---|---|---  
| input | guar. | key  
Mukhopadhyay et al. [21] | yes | by design | no  
Shin et al. [22] | yes | no | no  
Wang et al. [5] | no | n/a | no  
Khan and Fu [6] | no | n/a | no  
Jiang and Luo [34] | no | n/a | synth.  
Zhang et al. [1] | yes | no | no  
Rosenfeld et al. [2] | yes | no | no  
Kaya et al. [3] | yes | no | no  
This work | yes | yes | yes  
  
Table A1: The closest work. “Equivalence guaranteed” asks whether the perturbation is meaning-preserving by construction or only by assumption; “exact key” whether a programmatic answer exists. Only when both hold can concentration and correctness be measured separately.

Every row was checked against its source.

## Appendix B Standard aggregation results

These two are classical and are used in the main body without comment. We state them for completeness and claim no novelty for either.

###### Lemma 9 Modal vote.

Let answers be categorical, let Assumption 2 hold, and write p=Pr[y^i≠a⋆]<12p=\Pr[\hat{y}_{i}\neq a^{\star}]<\tfrac{1}{2}. Under any tie-breaking rule,

| Pr[y^RM≠a⋆]≤Pr[Bin(K,p)≥K2]≤e−2​K​(12−p)2.\begin{split}\Pr[\hat{y}_{\mathrm{RM}}\neq a^{\star}]\;&\leq\;\Pr[\mathrm{Bin}(K,p)\geq\tfrac{K}{2}]\\\ &\leq\;e^{-2K(\frac{1}{2}-p)^{2}}.\end{split} |   
---|---|---  
  
When the answer space has two elements and KK is odd the first inequality is an equality, and the middle quantity is strictly decreasing along odd KK.

###### Proof.

Let W=|{i:y^i≠a⋆}|∼Bin⁡(K,p)W=|\\{i:\hat{y}_{i}\neq a^{\star}\\}|\sim\mathrm{Bin}(K,p). If W<K/2W<K/2 then a⋆a^{\star} is returned by K−W>K/2K-W>K/2 renderings, so it holds a strict majority and is the unique mode; any tie-breaking rule, deterministic or randomized, then returns a⋆a^{\star}. Hence {y^RM≠a⋆}⊆{W≥K/2}\\{\hat{y}_{\mathrm{RM}}\neq a^{\star}\\}\subseteq\\{W\geq K/2\\}, which uses identical distribution only. With t=12−p>0t=\tfrac{1}{2}-p>0, {W≥K/2}={W−Kp≥Kt}\\{W\geq K/2\\}=\\{W-Kp\geq Kt\\} and Hoeffding’s inequality for a sum of KK independent [0,1][0,1]-valued variables gives Pr[W−Kp≥Kt]≤e−2​K​t2\Pr[W-Kp\geq Kt]\leq e^{-2Kt^{2}}; independence is used here and only here. With answer space {a⋆,b}\\{a^{\star},b\\} and KK odd, W≠K/2W\neq K/2 always and y^RM=b\hat{y}_{\mathrm{RM}}=b iff W>K/2W>K/2, so the containment is an equality. Monotonicity along odd KK is the Condorcet jury theorem; it does not hold over all KK, since even KK admits ties and the sequence oscillates, which is why the statement is restricted. ∎

###### Lemma 10 Median aggregation.

Let answers be continuous, let Assumption 2 hold with PP having a unique median μ\mu and a density φ\varphi positive and continuous at μ\mu. Then y^RM→μ\hat{y}_{\mathrm{RM}}\to\mu almost surely and K​(y^RM−μ)⇒𝒩⁡(0,14​φ​(μ)2)\sqrt{K}(\hat{y}_{\mathrm{RM}}-\mu)\Rightarrow\mathcal{N}(0,\tfrac{1}{4\varphi(\mu)^{2}}).

###### Proof.

Standard sample-median consistency and asymptotic normality. ∎

The substantive point for this paper is the identity of the limit. Median aggregation suppresses dispersion at rate K−1/2K^{-1/2} but converges to μ\mu, the centre of the model’s style-induced read distribution, not to a⋆a^{\star}. If a bias survives re-rendering, so μ≠a⋆\mu\neq a^{\star}, no KK makes RM\mathrm{RM} correct under a tolerance τ<|μ−a⋆|/|a⋆|\tau<|\mu-a^{\star}|/|a^{\star}|. Aggregation removes variance, never bias, and Lemma 10 is the case the categorical self-consistency analyses do not cover even though most of our questions fall into it.

## Appendix C Proofs of the main results

### C.1 Proof of Proposition 4

#### (i).

Let P^K\hat{P}_{K} be the empirical distribution of {y^i}i=1K\\{\hat{y}_{i}\\}_{i=1}^{K}. By the strong law applied to each answer value, P^K​(a)→P​(a)\hat{P}_{K}(a)\to P(a) almost surely for every aa. Since the mode m⋆m^{\star} is unique there is almost surely a finite K0K_{0} beyond which arg⁡maxa​P^K​(a)=m⋆\arg\max_{a}\hat{P}_{K}(a)=m^{\star}, so y^RM→m⋆\hat{y}_{\mathrm{RM}}\to m^{\star} and 𝟏[y^RM=a⋆]→𝟏[m⋆=a⋆]=Z\mathbf{1}[\hat{y}_{\mathrm{RM}}=a^{\star}]\to\mathbf{1}[m^{\star}=a^{\star}]=Z. On the same event REAcat=P^K​(m⋆)→P⁡(m⋆)=π\mathrm{REA}_{\text{cat}}=\hat{P}_{K}(m^{\star})\to P(m^{\star})=\pi. Neither the definition of π\pi nor the convergence uses a⋆a^{\star}.

#### (ii).

For any fixed a0a_{0}, maxa⁡P^K​(a)≥P^K​(a0)\max_{a}\hat{P}_{K}(a)\geq\hat{P}_{K}(a_{0}) pointwise, so 𝔼⁡[REAcat]≥𝔼⁡[P^K​(a0)]=P⁡(a0)\mathbb{E}[\mathrm{REA}_{\text{cat}}]\geq\mathbb{E}[\hat{P}_{K}(a_{0})]=P(a_{0}). Taking a0=m⋆a_{0}=m^{\star} gives 𝔼⁡[REAcat]≥π\mathbb{E}[\mathrm{REA}_{\text{cat}}]\geq\pi. Equality requires P^K​(m⋆)=maxa⁡P^K​(a)\hat{P}_{K}(m^{\star})=\max_{a}\hat{P}_{K}(a) almost surely. If π<1\pi<1 there is some b≠m⋆b\neq m^{\star} with P⁡(b)>0P(b)>0, and the event that all KK draws equal bb has probability P​(b)K>0P(b)^{K}>0; on it P^K​(b)=1>P^K​(m⋆)\hat{P}_{K}(b)=1>\hat{P}_{K}(m^{\star}), so the inequality is strict. If π=1\pi=1 then REAcat≡1=π\mathrm{REA}_{\text{cat}}\equiv 1=\pi. Numerically, for P=(0.5,0.2,0.2,0.1)P=(0.5,0.2,0.2,0.1) the bias 𝔼⁡[REAcat]−π\mathbb{E}[\mathrm{REA}_{\text{cat}}]-\pi is +0.17+0.17 at K=2K{=}2 and +0.04+0.04 at K=8K{=}8: not negligible at the budgets used throughout this paper.

#### (iii).

REApair\mathrm{REA}_{\text{pair}} averages (K2)\binom{K}{2} indicators, each with expectation Pr[y^i=y^j]=∑aP(a)2=A\Pr[\hat{y}_{i}=\hat{y}_{j}]=\sum_{a}P(a)^{2}=A for i≠ji\neq j by independence and identical distribution, so 𝔼⁡[REApair]=A\mathbb{E}[\mathrm{REA}_{\text{pair}}]=A regardless of KK. For the sandwich, A=∑aP​(a)2≥P​(m⋆)2=π2A=\sum_{a}P(a)^{2}\geq P(m^{\star})^{2}=\pi^{2} since π2\pi^{2} is one of the summands, and A=∑aP⁡(a)​P​(a)≤π​∑aP⁡(a)=πA=\sum_{a}P(a)P(a)\leq\pi\sum_{a}P(a)=\pi. □\square

0013\tfrac{1}{3}12\tfrac{1}{2}11Z=0Z{=}0Z=1Z{=}11/L1/Lπ\pi Figure A1: Why diffuseness sets the threshold. Schematic distributions of concentration π\pi over instances whose modal answer is correct (Z=1Z{=}1) and incorrect (Z=0Z{=}0). Proposition 5(iii) confines all Z=0Z{=}0 mass to π≤1/L\pi\leq 1/L, so agreement above that threshold certifies the mode; the shaded band is the certified region for L=2L{=}2. Corollary 6 reads the same picture as a ranking problem: the AUROC of REA\mathrm{REA} is the probability that a Z=1Z{=}1 instance is more concentrated than a Z=0Z{=}0 one, so it degrades as the two distributions approach each other and equals 12\tfrac{1}{2} when they coincide. Shapes are illustrative, calibrated to the measured AUROC.

### C.2 Proof of Proposition 5

#### (i).

The maximum over all answers splits into the correct answer and the rest, π=maxa⁡P⁡(a)=max⁡(P⁡(a⋆),maxa≠a⋆⁡P⁡(a))=max⁡(P⁡(a⋆),β)\pi=\max_{a}P(a)=\max\big(P(a^{\star}),\max_{a\neq a^{\star}}P(a)\big)=\max(P(a^{\star}),\beta). The mode is a⋆a^{\star} exactly when P⁡(a⋆)P(a^{\star}) strictly exceeds every other mass, that is P⁡(a⋆)>βP(a^{\star})>\beta, so Z=𝟏[P(a⋆)>β]Z=\mathbf{1}[P(a^{\star})>\beta].

#### (ii).

If Z=0Z=0 then P⁡(a⋆)≤βP(a^{\star})\leq\beta, so the maximum in (i) is attained by β\beta and π=β\pi=\beta.

#### (iii).

Suppose Z=0Z=0. By (ii), π=β\pi=\beta, and by the diffuseness hypothesis β≤(1−P⁡(a⋆))/L≤1/L\beta\leq(1-P(a^{\star}))/L\leq 1/L since P⁡(a⋆)≥0P(a^{\star})\geq 0. Hence π≤1/L\pi\leq 1/L. The contrapositive is that π>1/L\pi>1/L implies Z=1Z=1. At L=1L=1 the bound reads π≤1\pi\leq 1, which is vacuous, matching the intuition that a single systematic wrong answer admits no agreement-based certificate. □\square

### C.3 Proof of Corollary 6

In the limit REA\mathrm{REA} equals π\pi and the correctness label equals ZZ by Proposition 4(i), so the AUROC of REA\mathrm{REA} against correctness is by definition the probability that a positive instance outranks a negative one, Pr[π1>π0]+12Pr[π1=π0]\Pr[\pi_{1}>\pi_{0}]+\tfrac{1}{2}\Pr[\pi_{1}=\pi_{0}] with π1∼π|Z=1\pi_{1}\sim\pi\mid Z{=}1 and π0∼π|Z=0\pi_{0}\sim\pi\mid Z{=}0. If π⟂Z\pi\perp Z these are equal in distribution and the expression is 12\tfrac{1}{2}. Taking any PP with π\pi near 11 and m⋆≠a⋆m^{\star}\neq a^{\star} on a set of instances of probability approaching one gives the final claim. □\square

### C.4 Proof of Proposition 7

Let θ\theta and θ′\theta^{\prime} be independent draws with independent coordinates (Assumption 3). Define the hybrids H0=θH_{0}=\theta and Hj=(θ1′,…,θj′,θj+1,…,θJ)H_{j}=(\theta^{\prime}_{1},\dots,\theta^{\prime}_{j},\theta_{j+1},\dots,\theta_{J}), so HJ=θ′H_{J}=\theta^{\prime}. Consecutive hybrids Hj−1H_{j-1} and HjH_{j} share every coordinate except the jjth, where they carry θj\theta_{j} and θj′\theta^{\prime}_{j}, two independent draws from the jjth marginal; every other coordinate is a single draw from its own marginal, shared between them. By coordinate independence the pair (Hj−1,Hj)(H_{j-1},H_{j}) therefore has exactly the law of a pair differing only in a resampled coordinate jj, so Pr[y^(Hj−1)≠y^(Hj)]=Dj\Pr[\hat{y}(H_{j-1})\neq\hat{y}(H_{j})]=D_{j}.

If y^​(H0)≠y^​(HJ)\hat{y}(H_{0})\neq\hat{y}(H_{J}) then at least one consecutive pair must differ, since otherwise the answer would be constant along the chain. A union bound gives

| D≤∑j=1JPr[y^(Hj−1)≠y^(Hj)]=∑j=1JDj,D\leq\sum_{j=1}^{J}\Pr[\hat{y}(H_{j-1})\neq\hat{y}(H_{j})]=\sum_{j=1}^{J}D_{j}, |   
---|---|---  
  
This chains two inequalities, D≤Pr⁡[⋃jAj]≤∑jPr⁡[Aj]D\leq\Pr[\bigcup_{j}A_{j}]\leq\sum_{j}\Pr[A_{j}] with Aj={y^(Hj−1)≠y^(Hj)}A_{j}=\\{\hat{y}(H_{j-1})\neq\hat{y}(H_{j})\\}. The first is strict whenever one flip is reversed by a later one and the chain returns to its starting answer; the second is strict whenever two AjA_{j} overlap. Equality therefore requires both to be tight, and disjointness alone does not suffice.

For the second claim, let μc\mu_{c} be the law of y^\hat{y} given coordinate j=cj=c, the other coordinates drawn from their marginals. The disagreement probability between independent draws from laws ν,ν′\nu,\nu^{\prime} is 1−⟨ν,ν′⟩1-\langle\nu,\nu^{\prime}\rangle, so D=1−∥𝔼c​[μc]∥2D=1-\lVert\mathbb{E}_{c}[\mu_{c}]\rVert^{2} and D−j=1−𝔼c​∥μc∥2D^{-j}=1-\mathbb{E}_{c}\lVert\mu_{c}\rVert^{2}. Jensen’s inequality applied to the convex map ν↦∥ν∥2\nu\mapsto\lVert\nu\rVert^{2} gives 𝔼c​∥μc∥2≥∥𝔼c​[μc]∥2\mathbb{E}_{c}\lVert\mu_{c}\rVert^{2}\geq\lVert\mathbb{E}_{c}[\mu_{c}]\rVert^{2}, hence D−j≤DD^{-j}\leq D. For the lower bound, take the two-step hybrid θ→θ′′→θ′\theta\to\theta^{\prime\prime}\to\theta^{\prime} where θ′′\theta^{\prime\prime} shares coordinate jj with θ\theta and matches θ′\theta^{\prime} elsewhere. The first step is a D−jD^{-j} event and the second a DjD_{j} event, so D≤D−j+DjD\leq D^{-j}+D_{j}, that is D−Dj≤D−jD-D_{j}\leq D^{-j}. □\square

## Appendix D Replication of the agreement-versus-evidence prediction across independent instantiations, and a rendering bug that produced a false reversal

An earlier draft of this paper reported REA\mathrm{REA} beating B1 on Qwen2.5-VL-7B (CI [+0.047,+0.145][+0.047,+0.145]) and pooled across three models (CI [+0.010,+0.053][+0.010,+0.053]), with InternVL2-8B as the sole exception. That result came from one RENDEQ instantiation. All main runs use A100 80 GB GPUs; Qwen2.5-VL-3B ran in bf16, Qwen2.5-VL-7B and InternVL2-8B in 4-bit (NF4), matching an earlier P100 run’s quantization so that the GPU move is not itself a second confound alongside the rendering-pipeline fix described below. Regenerating the dataset from the same generator with two new random seeds and re-running all three models on all three instantiations initially gave the opposite sign on every model, a reversal serious enough that we spent most of a working session investigating it: fixing a real tie-breaking bug in the reference implementation, testing and ruling out a discarded style axis and GPU quantization as confounds, and confirming the Qwen2.5-VL-7B weights were bit-identical to the original run by revision hash. None of that investigation found the actual cause. We report the investigation here anyway, because it shows real diligence applied to the wrong hypothesis, and because the eventual finding is only credible in light of how much was checked before it turned up.

#### The bug.

The generator renders each style-varied instance with one of two plotting backends, matplotlib or plotly, selected as part of the style sampler; Sec. 6.3 identifies this as the single most consequential style factor. Plotly rendering goes through kaleido, a headless PNG exporter that shells out to a bundled executable. That executable’s wrapper script contains the line cd $DIR with $DIR unquoted; on this project’s working directory, whose path contains a literal space, the shell word-splits $DIR into multiple arguments and cd fails with "too many arguments". The generator’s own rendering code catches this exception per-render and falls back to matplotlib, logging the fallback honestly in the instance’s own style record (library_fallback_from) rather than silently mislabeling it. But nothing downstream of dataset generation ever checked whether the fallback rate was zero, five percent, or total. It was total: every one of the three "independently generated instantiations" used to replicate the agreement-versus-evidence prediction had _zero_ plotly renders. The library factor, the one this paper’s own analysis (Sec. 6.3) identifies as dominating cross-render dispersion, never actually varied in any of the data behind that replication. We found this while adding bootstrap intervals to the style-factor attribution table and noticing that library could not be computed at all (zero instances with ≥\geq2 observed levels), which a working pipeline should never produce for the factor believed to matter most.

#### Why this produces exactly this reversal.

REA\mathrm{REA}’s reliability advantage over evidence-carrying signals like B1 depends on genuine cross-render disagreement being present for the model’s real errors to surface as instability; Proposition 7 and Sec. 6.3 both hold that library accounts for the large majority of that disagreement’s magnitude. Silently collapsing every instantiation to one plotting backend removes most of the dispersion REA\mathrm{REA} is built to exploit without removing anything from B1, which is computed from decoding probabilities and does not depend on rendering diversity at all. The three "independent instantiations" were independent in data content and decoding but not in the one style dimension that mattered, so they were not, in the sense this paper’s own methodology requires, independent replications of the render-equivalence design at all.

#### The fix and the corrected result.

We fixed the wrapper script (quoting $DIR), confirmed kaleido renders correctly afterward, and regenerated all three instantiations from the same generator seeds (0, 1, 2), the same n_per_family=50, K=8K{=}8, this time with a genuine near-50/50 matplotlib/plotly split (346–348 of 350 instances per instantiation have both backends represented across their 8 renderings, versus 0 of 350 before). We re-ran the full pipeline end to end on the corrected images: main inference (3 models ×\times 3 instantiations ×\times 3 decoding seeds, 27 runs), baselines B1–B5, and the consensus-self-training-inverts fine-tuning replication, all with the same code, model revisions, and quantization settings as before, so the only variable that changed is whether the rendering pipeline actually rendered what the style sampler asked for.

Table A2: Model-wise comparison of B1 and REA\mathrm{REA} after the rendering-pipeline fix. Model | B1 | REA\mathrm{REA} | Δ\Delta | 95% CI  
---|---|---|---|---  
Qwen2.5-VL-7B | 0.7710.771 | 0.8640.864 | 0.0940.094 | [+0.066,+0.121][+0.066,\,+0.121]  
Qwen2.5-VL-3B | 0.8670.867 | 0.8580.858 | −0.009-0.009 | [−0.030,+0.011][-0.030,\,+0.011]  
InternVL2-8B | 0.8750.875 | 0.9070.907 | 0.0330.033 | [+0.013,+0.053][+0.013,\,+0.053]  
  
The reversal reverses again: REA\mathrm{REA} now beats B1 on 7B and InternVL2-8B, with CIs that exclude zero, and is statistically tied with it on 3B. Pooled across all nine model–instantiation runs (N=3150N{=}3150): Δ=+0.040\Delta=+0.040, CI [+0.027,+0.053][+0.027,+0.053], p<10−4p<10^{-4}, close in sign and rough magnitude to the very first single-instantiation result this whole investigation was trying to replicate. The tie-breaking bug fix (rm_categorical, first-seen order rather than numpy.unique’s alphabetical order) is still in effect and did not need to be reverted; it was a real, independent bug, just not the explanation for this particular reversal. The style-axis and quantization checks from the earlier investigation are moot for the same reason.

#### The render-versus-sample reliability half.

B1–B5 were all re-run on the corrected images. REA\mathrm{REA} beats B3, the fixed-image self-consistency control, on every model: pooled Δ=+0.102\Delta=+0.102, CI [+0.083,+0.121][+0.083,+0.121], p<10−4p<10^{-4} (N=3149N{=}3149); per model, +0.093+0.093 (7B), +0.061+0.061 (3B), +0.157+0.157 (InternVL2-8B), all CIs excluding zero. This is the opposite sign from the buggy replication’s −0.054-0.054 and, like the B1 comparison, close to what an intact rendering pipeline should show given that both REA\mathrm{REA} and B3 are compared against a model whose visual input now actually varies.

#### Consensus self-training, re-run on the corrected images.

We also re-ran the five-run consensus-self-training-inverts replication (three decoding seeds on one instantiation, one seed each on the other two) on the corrected data.

Table A3: Performance differences across instantiation and decoding seeds. Here, tr and ho denote training and hold-out families, respectively. Inst. | Seed | Δ\Deltasingletr | Δ​RMtr\Delta\mathrm{RM}_{\mathrm{tr}} | Δ\Deltasingleho | Δ​RMho\Delta\mathrm{RM}_{\mathrm{ho}} | Δ\DeltaAUROCtr | Δ\DeltaAUROCho  
---|---|---|---|---|---|---|---  
seed 0 | 42 | −0.038-0.038 | −0.064-0.064 | −0.188-0.188 | −0.272-0.272 | −0.014-0.014 | 0.1000.100  
seed 0 | 1 | 0.0060.006 | −0.044-0.044 | −0.105-0.105 | −0.188-0.188 | −0.124-0.124 | 0.0800.080  
seed 0 | 2 | 0.0100.010 | −0.036-0.036 | −0.084-0.084 | −0.104-0.104 | −0.083-0.083 | 0.0330.033  
seed 1 | 42 | −0.114-0.114 | −0.212-0.212 | −0.128-0.128 | −0.240-0.240 | −0.052-0.052 | 0.0090.009  
seed 2 | 42 | −0.051-0.051 | −0.104-0.104 | −0.121-0.121 | −0.185-0.185 | −0.122-0.122 | 0.0690.069  
  
The qualitative pattern is, if anything, cleaner than before the fix: hold-out accuracy falls in all five runs under both single-render decoding (8.48.4 to 18.818.8 points) and RM\mathrm{RM} (10.410.4 to 27.227.2 points), hold-out AUROC rises in all five runs (+0.009+0.009 to +0.100+0.100, no exceptions this time), and training-family AUROC falls in all five runs (−0.014-0.014 to −0.124-0.124). Training-family accuracy is the one split that is not uniformly negative: it falls under RM\mathrm{RM} in all five runs but rises slightly under single-render decoding in two of five. Exact magnitudes still vary considerably across runs, so we continue to read this as a robust direction rather than a precisely characterized effect size, exactly as Sec. 6.4 states. Scatter, the training family whose base majority was most often already wrong, illustrates the instantiation-dependence directly: its base single-render accuracy ranges 0.200.20–0.320.32 across the three instantiations, and after fine-tuning the three same-instantiation seeds leave it roughly flat near base while the other two instantiations show it falling to 0.000.00–0.060.06: the same objective drives the same family to opposite outcomes depending on the dataset draw.

#### What this means for how to read this paper.

Every number that depended on genuine render diversity was wrong in the version of this paper that reported a reversal, and the corrected numbers are the ones reported in the main text and tables throughout. We are disclosing this at this level of detail, rather than simply replacing the numbers, because a bug that silently defeats the paper’s central experimental manipulation and produces a plausible, internally coherent, wrong answer is exactly the failure mode a reader should be able to check for themselves, and because we do not want the earlier investigation’s real rigor (a fixed implementation bug, two ruled-out confounds, a hash-verified model checkpoint) to be mistaken for evidence that the reversal itself was well-founded. It was not; it was evidence of a bug we had not yet found.

## Appendix E Per-model and per-family results

Per-model summary, pooled over the three independent instantiations described in Sec. 6 (N=1050N{=}1050 per model, K=8K{=}8; cluster bootstrap over instances):

Model | single | RM\mathrm{RM} | REA\mathrm{REA} | B1  
---|---|---|---|---  
Qwen2.5-VL-7B | 0.6440.644 | 0.7010.701 | 0.8640.864 | 0.7710.771  
Qwen2.5-VL-3B | 0.5710.571 | 0.6260.626 | 0.8580.858 | 0.8670.867  
InternVL2-8B | 0.5630.563 | 0.6240.624 | 0.9070.907 | 0.8750.875  
  
Cluster-bootstrap Δ\DeltaAUROC(REA−\mathrm{REA}-B1), pooled per model across the three instantiations: 7B +0.094+0.094, CI [+0.066,+0.121][+0.066,+0.121], p<10−4p<10^{-4}; 3B −0.009-0.009, CI [−0.030,+0.011][-0.030,+0.011], p=0.39p{=}0.39 (includes zero); InternVL2-8B +0.033+0.033, CI [+0.013,+0.053][+0.013,+0.053], p=4×10−4p{=}4{\times}10^{-4}. Two of three models’ intervals exclude zero in REA\mathrm{REA}’s favor; the third is a statistical tie. Intervals for the grand pooled estimate are in Table 3.

#### Combining REA\mathrm{REA} and B1.

REA\mathrm{REA} beating B1 head-to-head on two of three models does not mean B1 carries no information REA\mathrm{REA} lacks. We fit a 5-fold cross-validated logistic combination of REA\mathrm{REA} and B1 (both zz-scored on the training fold; folds split by instance so no render set leaks across the split) and compared its AUROC to B1 alone: +0.103+0.103 (7B, CI [+0.079,+0.126][+0.079,+0.126]), +0.053+0.053 (InternVL2-8B, CI [+0.037,+0.064][+0.037,+0.064]), and +0.027+0.027 (3B, CI [+0.004,+0.036][+0.004,+0.036]). All three intervals exclude zero, so the combination helps on every model, including 3B, where REA\mathrm{REA} alone is statistically tied with B1. This is consistent with REA\mathrm{REA} and B1 making partly independent errors on every model, not just the two where REA\mathrm{REA} wins outright: token log-probability adds discriminative power on top of agreement even where agreement is already the stronger standalone signal, and vice versa on 3B. The gain is smallest on 3B, the model where the two signals are closest to each other in standalone performance, and largest on 7B, where REA\mathrm{REA}’s standalone lead over B1 is also largest: the opposite of a pattern where combination gains shrink as the gap between the two signals grows.

#### Self-consistency versus single-render decoding.

Table 4’s SC column is a modest improvement over single-render decoding once real render diversity is present in the comparator, but not a uniform one: the delta is essentially flat on 7B (0.00.0 points), slightly negative on 3B (−0.8-0.8), and a small positive on InternVL2-8B (+1.3+1.3), smaller in magnitude and less consistent in sign than re-rendering’s advantage under RM\mathrm{RM}. An earlier, single-instantiation draft had reported this margin as a small positive on every model; on the replicated pool it is not a stable finding.

Cluster-bootstrap Δ\Delta(accuracy)(RM−\mathrm{RM}-single), pooled per model: 7B +0.057+0.057, CI [+0.045,+0.068][+0.045,+0.068]; 3B +0.055+0.055, CI [+0.043,+0.067][+0.043,+0.067]; InternVL2-8B +0.061+0.061, CI [+0.047,+0.074][+0.047,+0.074]; all p<10−4p<10^{-4}. This is the one headline number that has been stable in both sign and rough magnitude throughout every version of this paper’s replication, including the version affected by the rendering bug described in Appendix D: RM\mathrm{RM}’s advantage over single-render decoding does not depend on the plotting-library dispersion the bug happened to remove.

Pooled per-family AUROC, all three models and all three instantiations, n=450n{=}450 per family:

Table A4: Performance comparison across chart families. The confidence interval corresponds to Δ⁡(REA−B1)\Delta(\mathrm{REA}-\mathrm{B1}). Family | REA\mathrm{REA} | B1 | Leader | 95% CI  
---|---|---|---|---  
Bar | 0.9420.942 | 0.8810.881 | REA\mathrm{REA} | [−0.034,+0.186][-0.034,\,+0.186]  
Grouped bar | 0.8000.800 | 0.8400.840 | B1 | [−0.109,+0.019][-0.109,\,+0.019]  
Line | 0.7830.783 | 0.7390.739 | REA\mathrm{REA} | [−0.151,+0.129][-0.151,\,+0.129]  
Log-axis | 0.9690.969 | 0.8350.835 | REA∗\mathrm{REA}^{\ast} | [+0.053,+0.196][+0.053,\,+0.196]  
Pie | 0.7800.780 | 0.8760.876 | B1 | [−0.165,+0.001][-0.165,\,+0.001]  
Scatter | 0.8040.804 | 0.9030.903 | B1∗\mathrm{B1}^{\ast} | [−0.192,−0.011][-0.192,\,-0.011]  
Stacked bar | 0.8290.829 | 0.9090.909 | B1∗\mathrm{B1}^{\ast} | [−0.144,−0.008][-0.144,\,-0.008]  
  
CIs are a two-way cluster bootstrap (5000 resamples): both instances within instantiation _and_ model are resampled with replacement, since each family’s n=450n{=}450 pool is 3 models ×\times 3 instantiations ×\times 50 instances and both axes repeat within it, unlike the one-way per-model bootstrap used above. ∗marks the three families (log-axis, scatter, stacked bar) whose interval excludes zero; the other four families’ point-estimate leaders are not statistically distinguishable from the alternative once both resampling axes are accounted for. This table supersedes an earlier version computed on the rendering pipeline described in Appendix D, in which log-axis appeared to have “flipped” from REA\mathrm{REA} to B1; on the corrected data log-axis is REA\mathrm{REA}’s strongest family by a wide, significant margin, the opposite of that earlier framing. Scatter and stacked bar are the two families where B1’s advantage survives this bootstrap on both the buggy and the corrected data.

#### Diffuseness by family.

Section 4 defines L^=(1−P⁡(a⋆))/β\hat{L}=(1-P(a^{\star}))/\beta, an empirical estimate of the diffuseness level LL in Proposition 5(iii), on every wrong-mode (Z=0Z{=}0), categorical instance. Pooled over the three instantiations, the distribution is concentrated toward the low-diffuseness end but not at the vacuous extreme: median L^\hat{L} is 1.331.33 (7B), 1.331.33 (3B), 1.501.50 (InternVL2-8B), and 2727–31%31\% of wrong-mode instances have L^=1\hat{L}{=}1 exactly, the case that admits no certificate at all. The implied threshold 1/L^1/\hat{L} is correspondingly high (median 0.750.75, 0.750.75, 0.670.67): for agreement to certify correctness on a typical wrong-mode instance here, it needs to be well above the midpoint, though less uniformly close to total than an earlier, buggy version of this pool suggested (Appendix D). This bears directly on the per-family table above: scatter and stacked_bar, the two families where B1’s advantage survives the two-way bootstrap, are exactly the families carrying most of the wrong-mode mass at or near L^=1\hat{L}{=}1 (scatter is 70%70\% of 3B’s wrong-mode instances, median L^\hat{L} between 1.331.33 and 1.601.60 across models). Line, log-axis, and pie contribute few wrong-mode instances each (under 25 pooled per model) and so are not estimated precisely enough to distinguish from L^=1\hat{L}{=}1 either, though these are also the families where REA\mathrm{REA}’s advantage is largest, consistent with fewer systematic, low-diffuseness errors there. On 3B specifically, where REA\mathrm{REA} and B1 are statistically tied overall, scatter alone accounts for 150150 of 215215 wrong-mode instances pooled, so that one family’s error structure disproportionately shapes the model-level comparison.

Figure 2b plots only the lift (cross-level minus within-level); the two rates behind it, pooled over the three instantiations and all three models, are: library, cross 0.4570.457 CI [0.443,0.471][0.443,0.471] versus within 0.3550.355 CI [0.343,0.366][0.343,0.366] (n≈3122n{\approx}3122 pairs each); bar_labels, cross 0.4260.426 CI [0.413,0.439][0.413,0.439] versus within 0.3830.383 CI [0.371,0.394][0.371,0.394]; bar_orient, cross 0.4150.415 CI [0.402,0.427][0.402,0.427] versus within 0.3960.396 CI [0.384,0.408][0.384,0.408]. The within-level rate is the noise floor, roughly 0.350.35–0.400.40 across all three factors, driven by decoding and residual style variation that survives holding the named factor fixed; library’s cross-level rate clears that floor by the largest margin of the three, which is the lift already reported in Sec. 6.3.

### E.1 Where the errors live

| all reads & | ≥\geq1 read | all reads ok,  
---|---|---|---  
Model | answer ok | wrong | answer wrong  
Qwen2.5-VL-7B | 17.417.4 | 76.076.0 | 6.66.6  
Qwen2.5-VL-3B | 12.012.0 | 81.481.4 | 5.45.4  
InternVL2-8B | 8.98.9 | 83.783.7 | 4.94.9  
Pooled | 12.812.8 | 80.480.4 | 5.65.6  
  
Percentage of instances in each of the three cells defined in Sec. 3 (all reads and the answer correct; all reads correct but the answer wrong, a reasoning failure; at least one read wrong, a perception failure, whatever the final answer). The three are exhaustive and disjoint by construction, so each row sums to 100%. Column 1 is _not_ overall accuracy: it is the narrower cell where every intermediate read was also correct. A model can still land on the right final answer despite a bad read (coincidence, or robustness to the specific value misread), and that happens often enough here that overall single-render accuracy (Table 4) exceeds column 1 by 45 to 47 points for every model; column 1 plus (accuracy −- column 1) recovers Table 4’s accuracy exactly, since the gap is precisely the correctly-answered share of column 2.

Two things are safe: at least one intermediate read is wrong on roughly four fifths of instances for every model, and instances where all reads are correct but the answer is wrong are rare, 4.9% to 6.6%. The remaining 45 to 47 points of each model’s accuracy come from the perception-failure cell: instances with at least one bad read that nonetheless landed on the correct final answer, 55% to 62% of that cell depending on the model. That failures here are predominantly perceptual is consistent with the size of the perception-failure cell but not established by column 1 alone, since a wrong read does not always produce a wrong answer. The distinction matters for the analysis: read noise that varies with style is the dispersion Lemma 10 says aggregation removes, whereas a style-invariant misread is the bias it cannot.

### E.2 Render-flip rate and render-equivalence robustness

Pooled over the three replicated instantiations, RFR (render-flip rate, the label-free fraction of instances with any disagreeing rendering) is 0.590.59 (7B), 0.640.64 (3B), 0.730.73 (InternVL2-8B): a majority of instances have at least one disagreeing rendering among the 8, on every model, which is the raw instability that REA\mathrm{REA} and RM\mathrm{RM} are built to exploit. RER (render-equivalence robustness, style-averaged accuracy) matches single-render accuracy exactly by construction (0.640.64, 0.570.57, 0.560.56). Per family, RFR is lowest on line (0.320.32 family mean) and highest on grouped_bar (0.870.87); across the seven families, RFR and RER (accuracy) are strongly negatively correlated (r=−0.69r{=}{-0.69}), noticeably tighter than on an earlier version of this pool affected by the rendering bug in Appendix D (r=−0.46r{=}{-0.46} there), consistent with RFR now reflecting genuine cross-render instability rather than instability from decoding noise alone.

## Appendix F Calibration

This section originally reported ECE from a single, unreplicated instantiation, then from a three-instantiation pool affected by the rendering bug described in Appendix D. We recomputed every number below on the corrected three-instantiation pool used for Tables 3 and 4 (N=1050N{=}1050 per model), with cluster (by instance) bootstrap 95% CIs.

ECE after min-max normalizing each signal to [0,1][0,1], lower is better:

Signal | Qwen-7B | Qwen-3B | InternVL-8B  
---|---|---|---  
REA\mathrm{REA} (ours) | 0.1460.146 | 0.1960.196 | 0.1420.142  
B3 self-consist. | 0.1580.158 | 0.1640.164 | 0.2140.214  
B1 token log-prob. | 0.1930.193 | 0.2430.243 | 0.3080.308  
B5 prompt ensemble | 0.2720.272 | 0.3050.305 | 0.3370.337  
B2 verbalized | 0.2780.278 | 0.2900.290 | 0.3410.341  
B4 Khan and Fu | 0.3240.324 | 0.3300.330 | 0.3880.388  
  
95% CIs (cluster bootstrap over instances, 5000 resamples): REA\mathrm{REA} [0.123,0.168][0.123,0.168] (7B), [0.173,0.219][0.173,0.219] (3B), [0.122,0.165][0.122,0.165] (InternVL2-8B); B3 [0.138,0.187][0.138,0.187] (7B), [0.139,0.189][0.139,0.189] (3B), [0.173,0.239][0.173,0.239] (InternVL2-8B); B1 [0.162,0.218][0.162,0.218] (7B), [0.206,0.265][0.206,0.265] (3B), [0.267,0.332][0.267,0.332] (InternVL2-8B).

REA\mathrm{REA} has the lowest point-estimate ECE on all three models. B3’s interval overlaps REA\mathrm{REA}’s on all three models, so calibration alone does not separate the two label-free signals with statistical confidence, even though REA\mathrm{REA} leads on AUROC on two of three models (Table 3) and both signals beat B1 clearly on calibration (non-overlapping intervals in every case). This is worth stating plainly: REA\mathrm{REA} is not uniquely well calibrated among label-free signals, it is well calibrated _and_ , on two of three models, more discriminative than the evidence-carrying baseline, which are different properties that happen to point the same way here. Min-max normalization makes signals comparable but means these values are not probabilities, so they compare signals rather than measuring calibration in the usual sense.

Reliability bins for REA\mathrm{REA} (normalized, 10 bins, empty bins omitted), pooled over the three instantiations, N=1050N{=}1050 per model. The correctness target is single_acc>0.5>0.5 at K=8K{=}8, the same target used for Table 3 and every AUROC in this appendix:

Bin | Qwen-7B | Qwen-3B | InternVL2-8B  
---|---|---|---  
centre | acc | nn | acc | nn | acc | nn  
0.05 | 0.000 | 38 | 0.000 | 38 | 0.000 | 77  
0.15 | – | 0 | – | 0 | 0.000 | 1  
0.25 | 0.067 | 15 | 0.000 | 14 | 0.000 | 30  
0.35 | 0.000 | 45 | 0.000 | 48 | 0.029 | 68  
0.45 | – | 0 | 0.000 | 1 | 0.000 | 1  
0.55 | 0.011 | 87 | 0.009 | 107 | 0.018 | 114  
0.65 | 0.472 | 108 | 0.375 | 152 | 0.441 | 152  
0.75 | 0.578 | 116 | 0.545 | 134 | 0.681 | 135  
0.85 | 0.810 | 211 | 0.800 | 175 | 0.856 | 188  
0.95 | 0.905 | 430 | 0.861 | 381 | 0.923 | 284  
  
All models show one shape: normalized REA≤0.35\mathrm{REA}\leq 0.35 maps to near-zero accuracy, REA≥0.95\mathrm{REA}\geq 0.95 to 0.86–0.92. This is Proposition 4 in data: the top bin is where π\pi is near one, and its accuracy short of 1.0 is the high-concentration wrong-mode population that Corollary 6 says no KK removes. It is also the population that consensus self-training amplifies in Sec. 6.4. Counts sum to N=1050N{=}1050 for every model, including InternVL2-8B. The count-weighted accuracy implied by each model’s bins matches its target mean exactly (7B: 0.648=0.6480.648=0.648; 3B: 0.570=0.5700.570=0.570; InternVL2-8B: 0.558=0.5580.558=0.558).

## Appendix G KK ablation

An earlier draft’s version of this table used the K=24K{=}24 majority vote (a superset of the very renderings being evaluated) as the correctness target, which is circular for a REA\mathrm{REA}-AUROC computation, and its K=1K{=}1/K=8K{=}8 endpoints did not match the headline numbers computed elsewhere in this paper because they came from a different, non-replicated run. We recompute this ablation from the same three-instantiation pool used for every other table in this paper (N=1050N{=}1050 per model, on the corrected images described in Appendix D), subsampling the first K∈{1,2,4,8}K\in\\{1,2,4,8\\} of each instance’s 8 renderings, scoring RM\mathrm{RM} with the real aggregation rule (mode for categorical, median for numeric, matching rm_pred exactly) against the manifest’s exact answer, and holding the correctness target fixed at all KK: whether the model’s own single-render majority at the full K=8K{=}8 budget matches ground truth, the same target Sec. 6.1 uses for the headline REA\mathrm{REA}-AUROC.

Table A5: Performance and inference cost for different values of KK. KK | Cost | REA\mathrm{REA} AUROC | RM\mathrm{RM} Accuracy  
---|---|---|---  
|  | 7B | 3B | InternVL | 7B | 3B | InternVL  
1 | 1×1{\times} | 0.5000.500 | 0.5000.500 | 0.5000.500 | 0.6440.644 | 0.5610.561 | 0.5740.574  
2 | 2×2{\times} | 0.7010.701 | 0.7060.706 | 0.7530.753 | 0.6220.622 | 0.5390.539 | 0.5460.546  
4 | 4×4{\times} | 0.8040.804 | 0.7810.781 | 0.8460.846 | 0.6820.682 | 0.6000.600 | 0.6060.606  
8 | 8×8{\times} | 0.8510.851 | 0.8240.824 | 0.9050.905 | 0.7010.701 | 0.6260.626 | 0.6240.624  
  
The K=8K{=}8 endpoints agree with Tables 3 and 4 exactly. K=4K{=}4 captures roughly two-thirds of K=8K{=}8’s benefit over K=2K{=}2: on REA\mathrm{REA} AUROC, 6161–69%69\% of the K=2→K=8K{=}2\to K{=}8 gain across the three models; on RM\mathrm{RM} accuracy, 7070–77%77\%. Substantial further gain remains between K=4K{=}4 and K=8K{=}8 on every model, which is weaker than an even earlier draft’s claim that K=4K{=}4 "captures ≈90%{\approx}90\% of the K=8K{=}8 benefit," which we do not replicate. Cluster (by instance) bootstrap CIs for the K=8K{=}8 vs. K=2K{=}2 gain, pooled over the three instantiations: 7B Δ\DeltaAUROC +0.151+0.151 CI [+0.124,+0.177][+0.124,+0.177], Δ​RM\Delta\mathrm{RM} +0.079+0.079 CI [+0.059,+0.099][+0.059,+0.099]; 3B Δ\DeltaAUROC +0.118+0.118 CI [+0.094,+0.142][+0.094,+0.142], Δ​RM\Delta\mathrm{RM} +0.087+0.087 CI [+0.067,+0.108][+0.067,+0.108]; InternVL2-8B Δ\DeltaAUROC +0.152+0.152 CI [+0.129,+0.176][+0.129,+0.176], Δ​RM\Delta\mathrm{RM} +0.078+0.078 CI [+0.057,+0.099][+0.057,+0.099]; every interval excludes zero, so the K=4→K=8K{=}4\to K{=}8 gain is real even though it is a minority of the total. The operating-point recommendation of K=4K{=}4 (main text, Sec. 6.3) should accordingly be read as a cost–benefit compromise, not as a near-saturation point.

The K=1K{=}1 row is degenerate: with one rendering all answers trivially agree, so REA\mathrm{REA} is constant and its AUROC is 0.5 by construction. Accuracy rises monotonically with KK on every model; there is no dip at K=2K{=}2 in this table, so Remark 8 (modal ties at K=2K{=}2 resolving to the first rendering) is not needed to explain it.

#### Modal versus pairwise REA\mathrm{REA}.

All REA\mathrm{REA} values above are modal, which Proposition 4(ii) shows is upward-biased at finite KK. We also computed REApair\mathrm{REA}_{\text{pair}} (Proposition 4(iii)), the unbiased pairwise agreement rate, on the same replicated pool: its mean is 0.09 to 0.11 lower than modal REA\mathrm{REA} on every model, exactly the direction the bias result predicts, and this closes the scale mismatch with the pairwise rate already used in Sec. 6.3. The bias does not change the ranking against B1: REApair\mathrm{REA}_{\text{pair}}’s AUROC against correctness is statistically indistinguishable from modal REA\mathrm{REA}’s on 7B and InternVL2-8B (both CIs include zero), and the one significant difference, on 3B (−0.005-0.005, CI [−0.010,−0.001][-0.010,-0.001]), is small relative to the biased statistic’s own margin from B1 on that model.

#### Sensitivity to the numeric tolerance τ\tau.

τ\tau is load-bearing in magnitude but not in direction on two of three models: at τ∈{1,2,5,10}%\tau\in\\{1,2,5,10\\}\%, pooled REA\mathrm{REA}-AUROC moves from 0.90→0.830.90\to 0.83 (7B), 0.88→0.810.88\to 0.81 (3B), 0.93→0.880.93\to 0.88 (InternVL2-8B), while B1’s AUROC (token log-probability does not depend on τ\tau) stays fixed at 0.770.77, 0.870.87, 0.880.88 respectively. REA\mathrm{REA} leads B1 at every tested τ\tau on 7B and InternVL2-8B; only on 3B, and only at τ≥5%\tau{\geq}5\%, does B1 lead.

Experimental support, please [view the build logs](./2608.05670v1/__stdout.txt) for errors. Generated by [ L A T E xml ](https://math.nist.gov/~BMiller/LaTeXML/). 

## Instructions for reporting errors

We are continuing to improve HTML versions of papers, and your feedback helps enhance accessibility and mobile support. To report errors in the HTML that will help us improve conversion and rendering, choose any of the methods listed below:

  * Click the "Report Issue" ( ) button, located in the page header.



**Tip:** You can select the relevant text first, to include it in your report.

Our team has already identified [the following issues](https://github.com/arXiv/html_feedback/issues). We appreciate your time reviewing and reporting rendering errors we may not have found yet. Your efforts will help us improve the HTML versions for all readers, because disability should not be a barrier to accessing research. Thank you for your continued support in championing open access for all.

Have a free development cycle? Help support accessibility at arXiv! Our collaborators at LaTeXML maintain a [list of packages that need conversion](https://github.com/brucemiller/LaTeXML/wiki/Porting-LaTeX-packages-for-LaTeXML), and welcome [developer contributions](https://github.com/brucemiller/LaTeXML/issues).

We gratefully acknowledge support from our **major funders** , [**member institutions**](https://info.arxiv.org/about/ourmembers.html) , ****, and all contributors.

[About](https://info.arxiv.org/about) * [Help](https://info.arxiv.org/help) * [Contact](https://info.arxiv.org/help/contact.html) * [Subscribe](https://info.arxiv.org/help/subscribe) * [Copyright](https://info.arxiv.org/help/license/index.html) * [Privacy](https://info.arxiv.org/help/policies/privacy_policy.html) * [Accessibility](https://info.arxiv.org/help/web_accessibility.html) * [Operational Status (opens in new tab)](https://status.arxiv.org)

Major funding support from

[ ](https://www.simonsfoundation.org/) [ ](https://www.sfi.org.bm/) [ ](https://www.schmidtsciences.org/)

[ ](javascript:toggleReadingMode\(\); "Disable reading mode, show header and footer")

