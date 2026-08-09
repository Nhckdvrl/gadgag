# Proposed research direction

## Working title

**Right Direction, Wrong Answer: Causally Decomposing Cross-Lingual Lexical
Interference into Sense Sensitivity and Surface Priors**

The broader “cross-lingual lexical interference” wording is intentional. False
friends are the main natural test bed, not the only possible endpoint; the
scientific object is which identifiable component of multilingual lexical
processing fails under static evaluation and dynamic adaptation.

## Research questions

- **RQ1:** How much of apparent cross-lingual homograph failure is explained by
  context-sensitive semantic discrimination versus stable candidate/language
  priors?
- **RQ2:** Which factors—script identity, tokenizer identity, resource ratio,
  POS, semantic distance and model architecture—change sensitivity and priors
  differently?
- **RQ3:** Do model rankings and conclusions from existing benchmarks change
  after both axes are reported?
- **RQ4:** Can causally targeted calibration improve absolute resolution without
  destroying genuine context sensitivity or true-friend transfer?

## Hypotheses

- H1: Many failures will have positive sense switch but wrong absolute choice,
  particularly when one language has a strong resource/frequency advantage.
- H2: Surface-only exposure will primarily move candidate prior; genuinely
  semantic intervention should change context sensitivity.
- H3: Unicode/token identity amplifies prior movement more reliably than it
  reduces context sensitivity.
- H4: A two-axis audit will reorder at least some model/language-pair conclusions
  relative to raw accuracy and existing bias metrics.

## Full experimental program

### Work package 1: Measurement validation

- Reuse paired false-friend contexts from StingrayBench, Doppelganger-JC and
  other license-compatible resources.
- Add candidate paraphrases, reversed order, answer language, transliteration,
  language-tag removal and matched same-language shuffled contexts.
- Obtain bilingual human judgments of both absolute sense and relative evidence
  movement on a stratified subset.
- Compare raw accuracy, Stingray metrics, contextual calibration,
  answer-level calibration, MCL-WiC-style similarity and the proposed
  decomposition.

### Work package 2: Generality

- At least four language pairs spanning shared/different scripts and different
  resource ratios (ZH–JA, EN–DE, ID–MS, ID–TL are immediately available).
- At least six open and closed model families.
- Mixed-effects regression with item and model random effects; predictors:
  Unicode identity, identical token sequence, subword count, POS, semantic
  mismatch, corpus-frequency ratio and language direction.

### Work package 3: Causal mechanisms

- Continue the crossover intervention with conflict, neutral-surface,
  paraphrased-meaning, unrelated-word and generic-language controls.
- Evaluate checkpoints over a preregistered exposure curve.
- Use layer/module interventions only after the behavioral construct passes all
  controls.
- Treat changes in prior and sensitivity as separate outcomes.

### Work package 4: Method, only if justified

Compare contextual/answer calibration, a learned prior estimator, and a small
counterfactual calibration set. The goal is not merely higher accuracy: the
method must improve absolute resolution while preserving the measured semantic
sense switch. Collision-aware replay is excluded unless redesigned because its
pilot failed against random replay.

## Six-month feasibility

1. Month 1: license audit, paired schema, preregistration and human protocol.
2. Month 2: full multi-model/multi-pair behavioral audit.
3. Month 3: perturbation and calibration baselines; resolve construct threats.
4. Month 4: controlled adaptation and frequency/tokenization regressions.
5. Month 5: only then develop the minimal method warranted by results.
6. Month 6: robustness, human validation, paper and artifact release.

The compute is moderate: likelihood scoring dominates; training uses small LoRA
interventions rather than pretraining new 7B models.

## Kill criteria

Abandon the direction rather than narrow it further if any two hold:

- sense-switch/accuracy separation fails to replicate across four pairs and six
  models;
- the metric is unstable under valid paraphrases or option permutations;
- human judgments do not support the model-side decomposition;
- calibrated results do not alter any substantive scientific diagnosis;
- language ID alone explains all variance and lexical/context information adds
  none;
- adjacent work is found that already performs the same paired causal audit.

## Contribution claim that is safe today

“We identify and causally validate a construct confound in cross-lingual lexical
evaluation, introduce a paired diagnostic that separately reports contextual
sense sensitivity and surface/candidate prior, and show that current absolute
errors can mask correct directional semantic evidence.”

Do **not** claim that LLMs actually understand the words, that semantic overwrite
exists, that calibration is new, or that the literature search proves absolute
worldwide novelty.
