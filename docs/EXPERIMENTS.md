# Experiment record

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
- The paired metric may partly reflect language identification. In a homograph
  setting language is a legitimate sense cue, but the full study must separate
  language ID, local lexical context, and broader sentence semantics.
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
