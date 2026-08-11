# Revised research proposal

## Working title

**Right Direction, Wrong Answer? Auditing Cross-Lingual Sense Disambiguation
Beyond Accuracy**

Optional subtitle: **A Crossed-Context Analysis of False-Friend Evaluation**.

## Motivation

Recent homograph benchmarks conclude that multilingual LLMs often fail to
distinguish cross-lingual senses. Their final-task accuracy is important, but it
does not identify why a model failed. An incorrect decision can reflect no
contextual evidence, correct but insufficient evidence, a language convention,
or an answer-dependent decision bias. These mechanisms imply different model
limitations and different remedies.

False friends provide a clean test bed for a general measurement question:
when surface form, sentence language, intended sense and output formulation are
correlated, what capability does benchmark accuracy identify?

## Research questions

- **RQ1:** How much of an aligned L1→L2 score switch comes from surrounding
  sense-bearing context versus the sentence's language convention?
- **RQ2:** How often does correct contextual evidence fail to cross the absolute
  decision boundary, and how much does answer formulation change that boundary?
- **RQ3:** Which model, tokenization, script, frequency and language-resource
  factors affect semantic evidence and language-convention evidence differently?
- **RQ4:** Do existing conclusions about homograph “comprehension” and model
  ranking change under crossed-context and repeated-gloss measurement?
- **RQ5:** During language adaptation, is loss concentrated in semantic-context
  evidence, language convention, or only the decision layer?

## Initial idea: Crossed-Context Audit (XCA)

For candidate margin `m(L,S,G)`—language `L`, sense-bearing context `S`, and
gloss formulation `G`—fit the repeated-measure model:

```text
m = b(item, gloss, model)
    + beta_semantic * S
    + beta_language * L
    + beta_interaction * L*S
    + random item/model/gloss effects
```

Report three levels rather than one accuracy:

1. **Semantic Context Evidence (SCE):** the factorial main effect of the
   intended surrounding semantics.
2. **Language Convention Evidence (LCE):** the factorial main effect of sentence
   language while holding intended semantics constant.
3. **Decision Resolution:** whether the final candidate margin crosses the
   correct boundary under repeated glosses; estimate decision baseline with
   content-free and answer-level calibration.

`Margin midpoint` remains descriptive and must not be called a prior. The
factorial components are effects under the benchmark's counterfactual
intervention; they are not claims about hidden neural representations.

The confirmatory protocol will use official chat templates and a hierarchical
item/model/gloss analysis. Plain prompting, mean versus sum normalization and
scoring batch size are robustness specifications, not independent
replications. Near-zero decisions will receive a numerical-stability flag.

## Confirmed pilot evidence

- exact surface occurring in all four contexts: 27 ZH–JA and 33 ID–TL;
- four checkpoints from Qwen and Gemma;
- official chat and plain prompts;
- boundary-faithful full-string scoring;
- mean/sum likelihood and three wrappers;
- full semantic effect: 92/96 CIs positive (48/48 with official chat
  templates; 44/48 in the plain-text stress test);
- masked semantic context: 91/96;
- marker-matched shuffled context: 1/96 positive and 3/96 negative;
- using only natural correct-use cells, masked context beats matched shuffled
  context in 82/96 specifications (46/48 with official chat), while full
  context beats an explicit language-plus-target cue in only 36/96;
- lexical gloss variants: 48/48 aggregate CIs positive;
- raw absolute accuracy remains far below directional/factorial sensitivity;
- content-free calibration changes both-direction accuracy by about 14 points.
- a batch-size 8/32 stress test yields margin correlations above .999 but
  0.6–1.2% cell-level sign flips; one weak Gemma-3-12B plain aggregate CI changes
  significance, while all six tested Qwen2.5 chat gates remain positive.

## Work packages

### WP1: Measurement validity

- independent bilingual review of all gloss variants;
- natural, non-word-replacement counterfactual contexts;
- candidate order, answer language, transliteration, chat formatting and
  free-generation checks;
- compare XCA with Stingray bias/comprehension, contextual calibration,
  answer-level calibration, MCL-WiC/XL-WiC and current WSD evaluation.

### WP2: Generality without leaderboard inflation

- add language pairs only after WP1 passes;
- stratify exact versus merely similar form, script, frequency ratio, POS and
  semantic distance;
- fit a hierarchical model rather than report dozens of disconnected tables;
- audit whether published benchmark-level conclusions change.

### WP3: Dynamic intervention

- preregister conflict, neutral-surface, paraphrased-meaning and unrelated-word
  adaptation controls;
- treat SCE, LCE and decision baseline as separate outcomes;
- replicate the exploratory conflict-minus-neutral sensitivity result with more
  items/seeds before any mechanism claim.

### WP4: Method, only if warranted

Possible method: a small counterfactual calibration set that estimates decision
baseline across glosses while preserving SCE. Compare it to generic contextual
and answer-level calibration. Success requires better absolute resolution with
unchanged or improved semantic-context evidence—not only higher accuracy.

## Six-month schedule

1. Month 1: bilingual annotation and preregistered measurement protocol.
2. Month 2: natural counterfactual set and reliability analysis.
3. Month 3: multi-dataset/model audit and hierarchical inference.
4. Month 4: controlled adaptation mechanism study.
5. Month 5: minimal calibration/method experiment if justified.
6. Month 6: robustness, artifact and paper.

## Kill criteria

Stop rather than narrow the topic if two occur:

- natural non-replacement contexts do not reproduce SCE;
- independently validated glosses yield unstable aggregate effect direction;
- crossed-context analysis does not change any benchmark mechanism conclusion;
- language convention alone explains results after better controls;
- results reduce completely to existing contextual/answer calibration;
- a direct prior paper is found with the same factorial audit and causal scope.

## Safe current contribution claim

“We show that absolute cross-lingual false-friend errors conflate separable
language-convention, sense-bearing-context and decision components. A
crossed-context audit reveals robust contextual evidence hidden by low strict
accuracy, while repeated gloss and calibration experiments expose substantial
decision instability.”

Do not claim hidden semantic representations, causal candidate priors, semantic
overwrite, or that directional evidence is equivalent to correct understanding.
