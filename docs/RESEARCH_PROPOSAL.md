# Revised research proposal

## Working title

**When Context and Language Disagree: Disentangling Cross-Lingual Lexical
Arbitration in Multilingual LLMs**

## Motivation

Recent homograph benchmarks already establish that multilingual LLMs often fail
to distinguish cross-lingual senses, and prior work already compares false
friends with cognates/non-cognates and uses incongruent sentences. The open
scientific question is therefore not whether false friends are difficult or
whether context helps. It is **where the lexical decision fails when local
semantics and language-conditioned convention support competing senses**.

False friends provide a clean natural intervention: the visible lexical form is
fixed while sentence language and intended sense can be crossed. A model may
extract the correct contextual semantic evidence yet still make the wrong final
choice because shared form/language convention wins during arbitration. This
dissociation changes both mechanistic interpretation and the appropriate remedy.

## Main research question

> **When contextual semantics and language convention support competing senses
> of the same lexical form, where does cross-lingual lexical disambiguation
> fail: during contextual evidence extraction, or during the later arbitration
> that maps extracted evidence to a lexical choice?**

Japanese formulation:

> 文脈が支持する語義と言語慣習が支持する語義が衝突するとき，多言語 LLM
> の誤りは，文脈語義を抽出できないために生じるのか，それとも正しい語義情報を
> 抽出していても，最終的な語義選択において言語依存の語義バイアスに負けるために
> 生じるのか？

### Sub-RQ1 — Evidence extraction

Holding sentence language fixed, does changing only local semantic context
produce the correct sense evidence? This is answered by the behavioral
`Language × Sense` crossed design, masking, language-only, unrelated-context,
repeated-gloss, natural Doppel and non-CJK replication.

### Sub-RQ2 — Collision specificity

When correct contextual evidence does not yield the correct decision, is the
gap specific to cross-lingual false friends, or explained by ordinary lexical
difficulty/WSD? Compare five preregistered types: false friend, true friend,
language-specific word, different-form translation and monolingual polysemy,
matched on POS, frequency, segmentation, length and reference difficulty.

### Sub-RQ3 — Arbitration mechanism

Where do semantic evidence and language-conditioned convention causally affect
the final lexical choice? Use target-span residual/MLP interventions after the
measurement and matching gates; attention is a stability control, not a circuit
claim.

## Core design: Crossed Lexical Arbitration (CLA)

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

## Identification controls

| Type | Form relation | Cross-language semantics | Role |
|---|---|---|---|
| False friend | same exact form | different | target conflict |
| True friend/cognate | same exact form | same | shared-form baseline |
| Language-specific word | present in only one dictionary | — | ordinary language-selective lexical processing |
| Different-form translation | different | same | removes shared-form collision |
| Monolingual polysemy | same form, same language | different senses | ordinary WSD baseline |

The first three reflect the advisor's minimum controls and established human
bilingual designs. The last two are needed to separate form sharing from
semantic ambiguity. These controls are identification infrastructure, not the
novelty claim.

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

### WP3: Causal arbitration

- use only bilingual-validated, outcome-blind pre-matched controls;
- target-span residual and MLP interchange on the same CLA estimands;
- compare false-friend language excess against true-friend/different-form
  controls and semantic profiles against monolingual polysemy/language-specific
  controls;
- do not claim a circuit, neuron or universal stage order.

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

“Existing cross-lingual homograph evaluation correlates sentence language,
intended sense, surface form and answer decision. We orthogonally manipulate
Language × Sense and show that correct local semantic evidence can be present
without yielding the correct lexical decision. We then test whether this gap is
an exact-form cross-lingual arbitration effect beyond matched cognate,
language-specific, translation and ordinary-polysemy controls.”

Do not claim hidden semantic representations, causal candidate priors, semantic
overwrite, or that directional evidence is equivalent to correct understanding.
