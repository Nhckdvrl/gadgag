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
- [ContraWSD](https://aclanthology.org/W18-6437/) and
  [MuCoW](https://aclanthology.org/W19-5354/) use contrastive WSD test suites for
  machine translation; [DiBiMT (Computational Linguistics 2025)](https://aclanthology.org/2025.cl-2.1/)
  is a modern gold lexical-ambiguity MT benchmark.

These works prevent a broad novelty claim such as “we invented calibration” or
“we invented contrastive sense evaluation”. They also supply the right
baselines.

## Gap supported by this pilot

We did not find a study that jointly:

1. represents each cross-lingual false friend with natural L1/L2 paired
   contexts and the same two competing senses;
2. factorizes absolute answer resolution into a context-sensitive sense-switch
   term and a stable candidate/language-prior term;
3. validates that factorization using controlled surface-only versus
   conflicting-meaning adaptation;
4. uses the result to audit whether “homograph shortcut” errors reflect semantic
   insensitivity or a prior strong enough to prevent an otherwise correct
   contextual shift from crossing the decision boundary.

The novelty target is this *cross-lingual lexical construct validation plus
causal component intervention*, not any one formula in isolation.

## Why the gap matters beyond homographs

The same measurement problem occurs whenever multilingual evaluation has
language-correlated answer strings: lexical semantics, translation,
code-switching, culturally grounded QA, and safety evaluations. Homographs are
a clean natural intervention because the surface form is fixed while the
language-conditioned meaning changes. This gives the topic a general
measurement-science contribution without abandoning the lab's homograph
lineage.
