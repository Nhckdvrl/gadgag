# Literature and novelty audit

Searches covered ACL Anthology, arXiv, OpenReview, conference proceedings,
psycholinguistics venues, Japanese research indexes, and targeted citation-following
searches through 2026-08-18. The claims below are deliberately limited to
“no direct match found” and “no independently verifiable citing/using work found
in this audit”, not “no such paper exists”. Citation counts are database-dependent
and can lag; for advisor-facing claims, this document distinguishes a paper that
**cites** a benchmark from one that **conceptually extends** it and one that
**actually reuses its released data/evaluation suite**.

## Direct positioning matrix after the 2026-08-12 advisor meeting

| Work | What it already establishes | Claim now unavailable | Remaining distinction used here |
|---|---|---|---|
| [Han et al. 2022](https://aclanthology.org/2022.findings-aacl.20/) | automatic recognition of interlingual homographs | identifying homographs is new | downstream lexical decision under cue conflict |
| [StingrayBench 2025](https://aclanthology.org/2025.findings-naacl.178/) | 259 true cognates, 446 false friends, four language pairs, semantic appropriateness/usage, resource-language bias and comprehension metrics | false friends are harder than cognates; high-resource bias; multi-pair benchmarking | it does not orthogonally identify sentence-language and local-sense effects |
| [Tanwar et al. 2025/26](https://arxiv.org/abs/2501.09127) | 1,260 cognate/non-cognate/homograph pairs, isolated and contextual judgments, and incongruent semantic-constraint sentences | cognate/non-cognate/homograph three-way comparison; conflict sentences; context helps | no full `Language × Sense` estimand tied to extraction-versus-arbitration and causal target interventions |
| [Doppelganger-JC 2025](https://aclanthology.org/2025.ijcnlp-long.96/) | Japanese–Chinese word meaning, meaning-in-context and translation; homograph shortcut; error direction and POS analysis | a new JC error benchmark or shortcut/POS analysis | asks whether correct contextual evidence is present despite the shortcut |
| [Concept-Spilling 2026](https://arxiv.org/abs/2601.12549) | a new nine-language, 100-word polysemy benchmark showing that models can spill meanings from dominant languages during structured meaning generation | generic cross-lingual semantic spilling / dominant-language semantic interference | exact-form false-friend cue conflict and extraction-versus-arbitration decomposition |
| [SemCog Bench 2026](https://arxiv.org/abs/2606.13218) | 1,858 Arabic–Hebrew true cognates, false friends and loanwords; contextual disambiguation; raw/diacritized/Romanized/phonetic inputs; modest context gains and strong surface-form interference | adding a new related-language pair; showing context alone may be insufficient; showing surface-form interference | no orthogonal `Language × Sense` factorial, target-masked evidence test, or extraction-versus-final-arbitration decomposition |
| [Kallini et al. 2025](https://aclanthology.org/2025.findings-emnlp.1153/) | controlled bilingual vocabulary overlap and transfer | bridge-versus-pit or shared vocabulary itself | pretrained-LLM item-level arbitration under exact-form conflict |
| [Abuín et al. 2026](https://aclanthology.org/2026.acl-long.1818/) | verified Romance cognate/false-friend datasets and zero/few-shot evaluation | adding related-language pairs or showing proximity interference | construct/mechanism localization rather than another performance comparison |
| [RoDEval 2025](https://aclanthology.org/2025.emnlp-main.864/) | WSD errors mix incomplete sense acquisition, overconfidence and intrinsic bias | generic “accuracy is insufficient” | cross-lingual `Language × Sense` decomposition with the same exact lexical form |
| [Dumas et al. 2025](https://aclanthology.org/2025.acl-long.1536/) | activation patching separates output language from translated concept | first separation of language and semantic representations | their causal contribution when the two cues compete for one lexical choice |
| [Oh et al. 2026](https://aclanthology.org/2026.eacl-long.135/) | causal tracing of contextual versus stored idiom interpretations, including attention/MLP pathways | first internal context-versus-lexical competition study | cross-lingual exact-form collision and matched multilingual lexical controls |

Tanwar is particularly important: an “odd Japanese sentence with a Chinese
sense” is a valid experiment but no longer a novelty claim. The contribution
must come from independently crossing both factors, defining stage-specific
estimands, and testing collision specificity rather than merely observing an
incongruent-sentence error.

SemCog Bench tightens the boundary further. It explicitly evaluates false friends
in sentence context and reports that context only modestly overcomes misleading
form similarity. Therefore neither “another language pair”, “context is not
enough”, nor “surface form causes interference” can be the central contribution.
The remaining question has to be more diagnostic: whether correct contextual
evidence was absent in the first place or was present but lost during lexical
arbitration.

## Citation-following audit requested by the advisor (2026-08-18)

The advisor explicitly asked not only what StingrayBench and Doppelganger-JC
**themselves** do, but also **“それを使った研究がどのぐらいあるか”**. To answer
that question conservatively, this audit separates three levels:

1. **citation/background use** — the paper cites the benchmark in related work;
2. **conceptual extension** — the paper follows the false-friend / multilingual
   semantic-interference line but builds a different dataset or task;
3. **direct benchmark reuse** — the paper actually runs on the released
   StingrayBench or Doppelganger-JC data/evaluation suite.

A raw citation count is not sufficient for this question because indexing differs
across Google Scholar-like services, ResearchGate, OpenAlex-style indexes, and
publisher pages. The table records only follow-up works whose relationship could
be verified from accessible title/abstract/full-text evidence.

### StingrayBench: verified downstream works

| Follow-up work | Relationship to StingrayBench | Directly reuses StingrayBench data/suite? | What the follow-up actually studies | Consequence for this project |
|---|---|---:|---|---|
| [Badanin et al. 2026, *Benchmarking Concept-Spilling Across Languages in LLMs*](https://arxiv.org/abs/2601.12549) | explicitly cites StingrayBench as evidence that LLMs can prefer a higher-resource sense; conceptually broadens the phenomenon to “language spilling” | **No evidence of reuse** | constructs a separate benchmark from 100 highly polysemous English words, evaluates structured meaning generation across nine languages and 16 models, and measures when models spill into meanings licensed by dominant languages | generic “high-resource meanings interfere with target-language semantics” is already occupied; our distinction must be exact-form cue conflict plus stage-specific evidence/arbitration |
| [Liang et al. 2026, *When Similar Means Different: Evaluating LLMs on Arabic–Hebrew Cognates* (SemCog Bench)](https://arxiv.org/abs/2606.13218) | cites StingrayBench and explicitly extends the recent LLM false-friend evaluation line | **No evidence of reuse** | builds a separate 1,858-pair Arabic–Hebrew benchmark covering true cognates, false friends and loanwords; tests sentence context, input representations and scale; finds strong surface-form reliance and only modest contextual gains | “new language pair”, “false friends remain hard in context”, and “surface similarity interferes” are not available novelty claims; it is the closest verified downstream conceptual extension |
| [Nguyen et al. 2026, *SEATauBench*](https://arxiv.org/abs/2606.28715) | cites StingrayBench among existing Southeast-Asian multilingual evaluation resources | **No** | studies interactive multilingual tool-agent-user evaluation by adapting TauBench into five regional languages; it treats StingrayBench as a static multilingual benchmark, not as its experimental data | background-only citation; no direct overlap with lexical arbitration, but confirms StingrayBench is recognized as part of the regional multilingual-evaluation landscape |

**Verified minimum from this audit:** at least **3 distinct 2026 follow-up works**
can be verified as citing/discussing StingrayBench. Among these three, **0/3 are
confirmed to directly reuse the released StingrayBench data or evaluation suite**.
Two are meaningful conceptual follow-ups (Concept-Spilling and especially SemCog
Bench); SEATauBench is a background citation. This is a **verified-minimum audit,
not a claim that StingrayBench has exactly three citations globally**.

This distinction matters for our positioning. The downstream line has already
expanded false-friend evaluation to new scripts/language families, studied
surface-form interference, and generalized high-resource semantic interference.
What we did **not** find in these citing works is a reuse of StingrayBench to
orthogonally cross sentence language and intended sense, mask the target to test
whether semantic evidence is already available, and then distinguish evidence
extraction from final lexical arbitration.

### Doppelganger-JC: verified downstream works

Targeted exact-title, author, DOI/Anthology-ID and full-text searches through
2026-08-18 did **not** surface an independently verifiable third-party paper that
both cites Doppelganger-JC and uses its released benchmark for a new experiment.
The authors presented **“Doppelganger-JC：日中同形異義語の理解能力を測るLLMベンチマーク”**
at NLP2026, but this is the same benchmark line by the same authors and should
not be counted as independent downstream reuse.

Accordingly, the safe advisor-facing statement is **not** “Doppelganger-JC has
zero citations”. Citation indexes may be incomplete or lag. The safe statement is:

> In the citation-following audit I could not verify an independent published
> follow-up that reuses Doppelganger-JC. The identifiable 2026 Japanese
> presentation is by the original authors and reports the same benchmark line.

The original Doppelganger-JC paper itself evaluates word meaning,
meaning-in-context and translation and analyzes the homograph shortcut; it is
therefore already more than “just a dataset”. Our current use of its 354
bidirectional natural-context items is a **new analysis within this project**, but
until our own work is published it should not be described as evidence of wider
community reuse.

A further bibliographic detail from checking the original papers: the published
Doppelganger-JC paper does not contain an identifiable citation to StingrayBench
by title/author in its full text. The two benchmark lines therefore should not be
presented as a simple chronological “Stingray → Doppelganger” extension chain.

### Advisor-facing answer to “それを使った研究がどのぐらいあるか”

The concise answer supported by the audit is:

> StingrayBenchについては、今回本文まで確認できた範囲で、少なくとも3件の
> 2026年の後続研究が引用しています。ただし、確認できた3件はいずれも
> StingrayBench自体をそのまま再評価する研究ではありません。SemCog Benchは
> false friend研究をアラビア語–ヘブライ語へ拡張し、Concept-Spillingはより広い
> 多言語意味干渉へ拡張し、SEATauBenchは関連する静的多言語評価として引用して
> います。一方、Doppelganger-JCについては、独立した第三者がデータを再利用した
> 後続研究は今回の検索では確認できませんでした。したがって、既存研究は
> 「false friendが難しい」「高資源言語側に偏る」「文脈だけでは表記バイアスを
> 完全に克服できない」ところまでは進んでいますが、文脈の正しい意味情報が
> すでに抽出されているのに最終判断で負けるのか、という分解はまだ直接には
> 検証されていない、というのが現在の立ち位置です。

## Human bilingual-processing foundation

The extraction/arbitration distinction is not invented solely from LLM scores:

- [Oi & Saito (2009)](https://cir.nii.ac.jp/crid/1390282680314404352)
  classify Japanese–Chinese materials as shared, Japanese-specific and
  Chinese-specific and examine whether Chinese–Japanese bilinguals suppress L1
  semantics during L2 judgment. These are theoretical controls, not our novelty.
- [Hsieh et al. (2017)](https://pubmed.ncbi.nlm.nih.gov/28750252/) compare
  interlingual homographs, cognates and language-specific words in
  Chinese–Japanese bilingual lexical decision, explicitly discussing stimulus
  semantic conflict and task/response conflict.
- [Tarin et al. (2025/2026)](https://doi.org/10.1017/S1366728925000380)
  use French–English eye tracking with target- versus non-target-language
  meaning-biased sentence contexts and language-unique controls. Context,
  cross-language frequency and age of acquisition jointly modulate late
  interference.

We do **not** claim that LLM computation is cognitively equivalent to human
bilingual processing. This literature supplies a mature scientific distinction:
lexical/semantic activation can be present while later integration or response
selection still shows conflict. The project asks whether a corresponding
computational dissociation can be causally identified in multilingual LLMs.

## Crowded directions that should not be claimed

- [Doppelganger-JC (IJCNLP-AACL 2025)](https://aclanthology.org/2025.ijcnlp-long.96/)
  already benchmarks Japanese–Chinese word meaning, meaning in context and
  translation and reports a homograph shortcut.
- [StingrayBench (NAACL Findings 2025)](https://aclanthology.org/2025.findings-naacl.178/)
  covers four language pairs, false friends and cognates, and studies
  high-resource-language bias.
- [SemCog Bench (2026)](https://arxiv.org/abs/2606.13218)
  already adds Arabic–Hebrew true cognates, false friends and loanwords, tests
  contextual disambiguation and representation variants, and reports that
  misleading surface similarity remains difficult to overcome with context.
- [Concept-Spilling (2026)](https://arxiv.org/abs/2601.12549)
  already broadens dominant-language semantic interference to polysemous meaning
  generation across nine languages.
- [False Friends Are Not Foes (EMNLP Findings 2025)](https://aclanthology.org/2025.findings-emnlp.1153/)
  causally manipulates vocabulary overlap in controlled bilingual models.
- [Tokenizing Crosslingual Homographs (2026)](https://arxiv.org/abs/2607.17689)
  already explores language-specific tokenization cues for homographs.
- [Multilingual catastrophic forgetting (MRL 2025)](https://aclanthology.org/2025.mrl-main.23/)
  establishes that single-language fine-tuning can degrade other languages;
  ordinary forgetting is not novel.

Therefore “a bigger homograph benchmark”, “more language pairs”, “safe shared
embeddings”, “context is insufficient”, generic semantic interference, tokenizer
separation, or merely showing multilingual forgetting are not defensible primary
contributions.

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

After targeted direct-work and citation-following searches through 2026-08-18,
we did not find a study that jointly:

1. crosses sentence language and intended sense for the same exact-form
   cross-lingual false friend;
2. separately estimates surrounding semantic-context evidence, language
   convention and decision resolution;
3. validates the semantic component with target masking, language-only,
   shuffled-context, repeated-gloss, chat and scoring controls;
4. uses the decomposition and matched five-way lexical controls to audit whether
   errors reflect absent contextual evidence or evidence that loses during
   lexical arbitration;
5. tests the same estimands with target-span residual/MLP interventions rather
   than inferring processing stages from final accuracy alone.

The novelty target is *stage-localized cross-lingual lexical arbitration*: a
crossed-context construct audit as the behavioral backbone, followed by
outcome-blind matched controls and causal interventions. It is not “beyond
accuracy” in general, calibration, contrastive scoring, WSD, false-friend
collection, incongruent sentences, adding another language pair, generic
high-resource semantic interference, activation patching, or any formula alone.

## Why the gap matters beyond homographs

The same measurement problem occurs whenever multilingual evaluation has
language-correlated answer strings: lexical semantics, translation,
code-switching, culturally grounded QA, and safety evaluations. Homographs are
a clean natural intervention because the surface form is fixed while the
language-conditioned meaning changes. This gives the topic a general
measurement-science contribution without abandoning the lab's homograph
lineage.
