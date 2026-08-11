# Experiment record

## 2026-08-11 construct-killer extension

After external review, the paired diagonal experiment was not accepted as pure
semantic sensitivity: moving from L1 to L2 also changed sentence language and,
for similar-form items, target form. A second pilot therefore used all four
Stingray cells in a language × intended-context factorial and retained only
NFKC-identical target forms that occur in all four evaluated contexts.

### Implementation corrections

- `scoring_v2.py` tokenizes the complete plain-text string and requires a
  prefix-stable answer boundary. Chat scoring uses each tokenizer's official
  generation template.
- Both mean token log likelihood and summed sequence log likelihood are kept.
- The validated loader asserts paired meanings, task directions and the four
  usage-validity labels instead of trusting adjacent row order.
- The old coordinate average is renamed `margin midpoint`; content-free prompts
  estimate a separate decision baseline.

### Factorial sample

- ZH–JA: 27 strict exact-context forms;
- ID–TL: 33 strict exact-context forms;
- Qwen2.5-7B, Qwen3-8B, Gemma-3-4B, Gemma-3-12B;
- plain and chat prompts;
- bare, definition and referential answer wrappers;
- mean and sum scoring.

This yields 96 confirmatory-style variants for each context condition.

### Construct controls

| condition | CI > 0 | interpretation |
|---|---:|---|
| full | 92/96 | language and semantic context both present; official chat 48/48 |
| masked | 91/96 | target removed; surrounding semantics retained |
| language only | 4/96 positive, 2/96 negative | language/word cue without sense-bearing context |
| marker-matched shuffled | 1/96 positive, 3/96 negative | same language and `[TARGET]`, unrelated context |

For full-minus-language-only, 92/96 CIs were positive. For
full-minus-shuffled, 84/96 CIs excluded zero; masked-minus-shuffled passed
90/96. The full semantic-effect median was 2.760 mean/sum-scale units across the
mixed variants; comparisons should use within-normalization estimates rather
than this pooled magnitude.

All four full-context failures were concentrated in Gemma-3-12B plain-text
likelihood (three ID–TL formulations and one ZH–JA formulation). All 48 official
chat-template variants passed. This protocol sensitivity is part of the
measurement result rather than an exclusion made after seeing the scores.

The 96 specifications are correlated combinations of model, pair, prompt,
wrapper and normalization; they are not 96 independent replications. A direct
batch-size 8 versus 32 stress test found Pearson margin correlations of
0.9992–0.9998, but 0.6–1.2% cell-level decision sign flips. Qwen2.5 ZH–JA chat
kept all six full gates at both batch sizes; Gemma-3-12B ID–TL plain changed
from two to three of six positive CIs. This is numerical decision-boundary
sensitivity, not evidence for a different semantic mechanism.

### Lexical gloss variants

Twenty-seven ZH–JA items received two additional English lexical realizations
per sense, in addition to a corrected source-style gloss. All 48 aggregate
model×mode×normalization×variant CIs excluded zero. However, the percentage of
items positive under all three variants ranged from 22.2% to 81.5%. Aggregate
direction is robust; item-level diagnosis is not yet reliable enough for a
paper without bilingual validation and a repeated-measures model.

### Calibration and benchmark metrics

Content-free calibration raised average both-direction accuracy from 31.9% to
46.5% in ZH–JA and 41.0% to 55.2% in ID–TL. It also changed the mean ZH–JA
Stingray-style L1 bias from -0.203 to a small L2 bias of 0.100. This demonstrates
decision instability; it does not make calibration a novel method.

### Natural-context-only audit

To avoid using translated/replaced conflict cells as ecological evidence, a
separate analysis retained only each item's natural L1×sense1 and L2×sense2
cells. Full natural context beat marker-matched shuffled context in 94/96
specifications, and target-masked natural context did so in 82/96 (46/48 under
official chat templates). However, full natural context beat an explicit
language-plus-target cue in only 36/96, with 16 significant reversals. This
rules out the simple story that richer context always dominates language
identity and motivates modeling evidence competition explicitly.

### XL-WiC control

Balanced 200-item samples from Chinese, Japanese and German XL-WiC were scored
with the same forced-choice likelihood protocol. Accuracies ranged from 49% to
70%, and content-free calibration helped some model/language cells but hurt
others. This exploratory control shows that the new false-friend effect cannot
be summarized as universally strong WSD. A formal comparison must use official
XL-WiC classifiers or established LLM-WSD protocols.

## Data and design

The causal pilot selected 50 exact NFKC-identical Chinese–Japanese false
friends from Doppelganger-JC. A deterministic two-fold crossover assigned 25
items to treatment in each fold; every item was treated once and held out once.
Training was continued language modelling over controlled Chinese sentences.
LoRA rank 16 targeted attention and MLP projections. Evaluation used mean
candidate-token log likelihood so candidates of different lengths were
comparable.

Public-data audit at preparation time:

- 235 exact-form Type-1 homographs were parseable, 229 with both question types;
- 50 were selected for the causal pilot;
- Stingray supplied 57 paired ZH–JA and 49 paired EN–DE false-friend cases used
  in the final sense-switch audit;
- Unicode normalization, code points, tokenizer token IDs and subword counts
  were recorded for every selected item.

## Experiments actually run

1. Qwen2.5-7B primary crossover, doses 0/32/128.
2. Fine dose curve 0/1/4/8/16/32.
3. Qwen3-8B replication at 0/8/32.
4. Japanese-gloss rather than surface-overlapping candidate evaluation.
5. English–German cross-script replication.
6. Attention-only, MLP-only, early-half and late-half LoRA ablations.
7. Collision-aware replay against equal-budget random Japanese replay.
8. Neutral Chinese surface repetition without the conflicting Chinese sense.
9. Matched shuffled-context subtraction (`context lift`) in ZH–JA and EN–DE.
10. Natural bilingual paired sense-switch evaluation in two language pairs and
    four model checkpoints from two model families.
11. Bias-versus-switch evaluation of saved conflict and neutral adapters.

## Primary results

### The seductive but invalid result

At dose 32, raw treated-minus-held-out margin change was negative and
significant for Qwen2.5-7B (-0.462, CI [-0.695,-0.238]) and Qwen3-8B (-0.392,
[-0.642,-0.157]). The Qwen2.5 dose curve became visible by dose 8 and saturated
around 16–32 rather than growing monotonically through 128. This already failed
the preregistered-style strict GO rule requiring a stronger effect at 128.

### Controls that falsified semantic overwrite

The Japanese-gloss outcome was non-significant. Neutral repetition of the
surface form caused an even larger raw change. Most decisively, subtracting a
matched shuffled-context score removed the apparent effect in both language
pairs. These outcomes distinguish an output/candidate prior from a changed
ability to use L2 context.

### Failed mitigation

At the same 12.5% replay budget, collision replay retained a raw effect of
-0.466 [-0.799,-0.157]; random replay was -0.326 [-0.649,-0.012]. The proposed
method did not outperform the generic baseline and is rejected.

### New paired finding

Strict two-sided accuracy was only 7.0–45.6% across eight completed
model/pair cells, whereas 64.9–95.9% had a positive paired sense switch. Every
cell's bootstrap CI for mean sense switch excluded zero. Full aggregates are in
`results/extensions/paired_sense_summary.csv`.

On the saved adaptation checkpoints, conflict exposure reduced the paired
sense switch by -0.384 [-0.740,-0.033], while neutral surface exposure did not
(-0.057 [-0.336,0.220]). However, the direct conflict-minus-neutral
difference-in-differences narrowly included zero (-0.327 [-0.695,0.028]), and
neither language-side margin was individually significant. This is an
exploratory mechanism signal to replicate, not evidence sufficient to revive
the original overwrite claim.

## Statistical treatment

- Treatment effects are within-item crossover differences, not unpaired group
  means.
- Confidence intervals are nonparametric bootstrap intervals over items with a
  fixed analysis seed.
- CIR denominators include only cases correct at baseline, as originally
  specified.
- No multiple-comparison corrected confirmatory claim is made: this is an
  exploratory pilot designed to kill weak hypotheses.

## Limitations

- Controlled templates isolate causality but are not ecological continued
  pretraining.
- The intervention uses one LoRA configuration and one fixed item split.
- Candidate likelihood is available for open models; a black-box version needs
  logprob APIs or repeated randomized forced choice.
- Candidate gloss quality and translation asymmetry remain possible sources of
  noise.
- Stingray's crossed conflict cells are annotator-constructed by translating a
  sentence and replacing the correct L2 word with the false friend. This is a
  useful intervention but produces conspicuously odd contexts; natural
  non-replacement counterfactuals are still required.
- New lexical gloss variants were inspected for sense preservation but have not
  yet been independently validated by bilingual human annotators.
- The diagonal paired metric partly reflects language identification. The new
  factorial separates language and intended-context main effects, but natural
  contexts are still needed to separate local lexical cues from broader
  sentence semantics.
- A source-field equality check was insufficient: composite forms, inflections
  and translated synonyms could make the listed target absent from a context.
  The strict loader now checks literal CJK occurrence or standalone Latin-word
  occurrence in every cell; this reduced the factorial sample from 29/48 to
  27/33.
- Public datasets remain governed by their own licenses; raw text and adapters
  are intentionally not redistributed here.

## Execution incidents

An additional Mistral-7B checkpoint was attempted, but the tokenizer/model
artifact fetch did not complete reliably on the shared filesystem and was
terminated after the preregistered comparison had already replicated on four
local checkpoints from Qwen and Gemma. Phi-3 was also excluded after its cached
SentencePiece/tokenizer configuration failed to load in the fixed environment.
These are infrastructure exclusions, not negative model results; no scores from
either checkpoint enter the tables.

## 2026-08-11 three-candidate validation

The complete interpretation and kill decisions are in
`docs/THREE_CANDIDATE_VERDICT_ZH.md`. This section records executable entry
points.

### C: cross-turn carryover

```bash
CUDA_VISIBLE_DEVICES=0 PYTHONPATH=src .venv/bin/python src/evaluate_carryover.py \
  --pair zh_ja --model Qwen/Qwen2.5-7B-Instruct --tag qwen25_7b \
  --data-root external/StingrayBench/data --batch-size 8
.venv/bin/python src/analyze_carryover.py

# Changed speaker role, fixed dose 4 robustness replication.
CUDA_VISIBLE_DEVICES=0 PYTHONPATH=src .venv/bin/python src/evaluate_carryover.py \
  --pair zh_ja --model Qwen/Qwen3-8B --tag qwen3_8b \
  --data-root external/StingrayBench/data --batch-size 8 \
  --doses 4 --lags 0 2 8 --prime-role assistant \
  --output-path results/extensions/carryover_alt_zh_ja_qwen3_8b.jsonl
.venv/bin/python src/analyze_carryover_robustness.py
```

The main design used 27 ZH–JA and 33 ID–TL exact forms, four model checkpoints,
five prime controls, doses 1/4/8 and lags 0/2/8. Per-item direction scores were
averaged before paired item bootstrap.

### B: independent non-replacement validation

```bash
CUDA_VISIBLE_DEVICES=0 PYTHONPATH=src .venv/bin/python src/evaluate_doppel_natural.py \
  --data-root external/Doppelganger-JC \
  --model google/gemma-3-12b-it --tag gemma3_12b --batch-size 16
.venv/bin/python src/analyze_doppel_natural.py
```

The deterministic loader retains 354 words for which both source directions
contain the mapped target and correct/shortcut translations have a non-empty
minimal differing span. Both answer orders are scored. Raw benchmark strings
stay under the upstream license and are not committed.

### A: causal arbitration

Install and download the Princeton WordNet control resource once:

```bash
uv pip install --python .venv/bin/python 'nltk>=3.10,<3.11'
.venv/bin/python -c "import nltk; nltk.download('wordnet'); nltk.download('omw-1.4')"
```

Then run the two preregistered model families:

```bash
CUDA_VISIBLE_DEVICES=0 PYTHONPATH=src .venv/bin/python src/evaluate_causal_gating.py \
  --data-root external/StingrayBench/data --pair zh_ja \
  --model Qwen/Qwen3-8B --tag qwen3_8b \
  --items-per-group 20 --layer-stride 4 --batch-size 8
.venv/bin/python src/analyze_causal_gating.py
.venv/bin/python src/plot_candidate_results.py
```

Qwen3 thinking is explicitly disabled for this constrained continuation task.
The intervention patches only the answer-boundary residual position; therefore
the pilot establishes causal state transfer but does not yet identify an
attention/MLP circuit.
