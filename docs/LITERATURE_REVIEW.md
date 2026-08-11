# Literature and novelty audit

Searches covered ACL Anthology, arXiv, OpenReview, conference proceedings and
Japanese NLP proceedings through 2026-08-10. The claim below is deliberately
limited to “no direct match found”, not “no such paper exists”.

## Crowded directions that should not be claimed

- [Doppelganger-JC (IJCNLP-AACL 2025)](https://aclanthology.org/2025.ijcnlp-long.96/)
  already benchmarks Japanese–Chinese word meaning, meaning in context and
  translation and reports a homograph shortcut.
- [StingrayBench (NAACL Findings 2025)](https://aclanthology.org/2025.findings-naacl.178/)
  covers four language pairs, false friends and cognates, and studies
  high-resource-language bias.
- [False Friends Are Not Foes (EMNLP Findings 2025)](https://aclanthology.org/2025.findings-emnlp.1153/)
  causally manipulates vocabulary overlap in controlled bilingual models.
- [Tokenizing Crosslingual Homographs (2026)](https://arxiv.org/abs/2607.17689)
  already explores language-specific tokenization cues for homographs.
- [Multilingual catastrophic forgetting (MRL 2025)](https://aclanthology.org/2025.mrl-main.23/)
  establishes that single-language fine-tuning can degrade other languages;
  ordinary forgetting is not novel.

Therefore “a bigger homograph benchmark”, “more language pairs”, “safe shared
embeddings”, tokenizer separation, or merely showing multilingual forgetting
are not defensible primary contributions.

## Closest methodological antecedents

- [Calibrate Before Use (ICML 2021)](https://proceedings.mlr.press/v139/zhao21c.html)
  shows that contextual calibration can remove content-free answer biases.
- [Answer-level Calibration (ACL 2022)](https://aclanthology.org/2022.acl-long.49/)
  calibrates free-form multiple-choice answer probabilities.
- [Cross-lingual calibration (EMNLP 2022)](https://aclanthology.org/2022.emnlp-main.170/)
  studies confidence calibration after zero-shot transfer, so multilingual
  calibration itself is also not new.
- [MCL-WiC (SemEval 2021)](https://aclanthology.org/2021.semeval-1.3/)
  evaluates multilingual/cross-lingual word-in-context sense identity.
- [XL-WiC (EMNLP 2020)](https://aclanthology.org/2020.emnlp-main.584/)
  provides expert-curated identical-word context pairs in 12 languages and is
  the key general semantic-contextualization control.
- [Do Large Language Models Understand Word Senses? (EMNLP 2025)](https://aclanthology.org/2025.emnlp-main.1720/)
  compares instruction-tuned LLMs in WSD and generative definition/explanation
  tasks. It makes a broad “LLMs understand senses” claim unavailable and
  motivates comparing evaluation formulations.
- [Prompt Balance Matters (GlobalNLP 2025)](https://aclanthology.org/2025.globalnlp-1.2/)
  shows that imbalanced demonstrations bias multilingual WSD prompts. This is
  direct evidence that prompt-level decision effects matter, but it does not
  cross sentence language and intended sense for an exact false friend.
- [SemEval-2026 Task 5 / AmbiStory](https://aclanthology.org/2026.semeval-1.448.pdf)
  replaces a single hard WSD label with human graded sense-plausibility ratings.
  It makes any generic “first to go beyond WSD accuracy” claim unavailable. XCA
  must instead claim the narrower methodological novelty of separating
  correlated language, semantic-context and answer-decision cues in a
  cross-lingual homograph setting.
- [ContraWSD](https://aclanthology.org/W18-6437/) and
  [MuCoW](https://aclanthology.org/W19-5354/) use contrastive WSD test suites for
  machine translation; [DiBiMT (Computational Linguistics 2025)](https://aclanthology.org/2025.cl-2.1/)
  is a modern gold lexical-ambiguity MT benchmark.

These works prevent a broad novelty claim such as “we invented calibration” or
“we invented contrastive sense evaluation”. They also supply the right
baselines.

[Tug-of-war between idioms' figurative and literal interpretations in LLMs
(EACL 2026)](https://aclanthology.org/2026.eacl-long.135/) uses causal tracing
to localize competition between contextual and lexical interpretations in a
monolingual idiom setting, including attention- and MLP-level pathways. It is a
particularly close mechanistic precedent: the proposed project must earn its
distinct contribution through cross-lingual `Language × Sense` interventions,
exact-form collisions, and matched multilingual controls—not merely by drawing
another layer-wise ambiguity curve.

## Gap supported by this pilot

After a second targeted search on 2026-08-11, we did not find a study that jointly:

1. crosses sentence language and intended sense for the same exact-form
   cross-lingual false friend;
2. separately estimates surrounding semantic-context evidence, language
   convention and decision resolution;
3. validates the semantic component with target masking, language-only,
   shuffled-context, repeated-gloss, chat and scoring controls;
4. uses the decomposition to audit whether homograph-benchmark errors reflect
   absent contextual evidence or evidence that fails at the decision boundary.

The novelty target is this *crossed-context construct audit*, not “beyond
accuracy” in general, calibration, contrastive scoring, WSD, false-friend
collection, or any one formula alone.

## Why the gap matters beyond homographs

The same measurement problem occurs whenever multilingual evaluation has
language-correlated answer strings: lexical semantics, translation,
code-switching, culturally grounded QA, and safety evaluations. Homographs are
a clean natural intervention because the surface form is fixed while the
language-conditioned meaning changes. This gives the topic a general
measurement-science contribution without abandoning the lab's homograph
lineage.
