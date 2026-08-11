# Final construct decision

## Construct gates

| family             | test                     |   variants |   ci_positive |   ci_negative |   median_effect |
|:-------------------|:-------------------------|-----------:|--------------:|--------------:|----------------:|
| factorial_semantic | full                     |         96 |            92 |             0 |       2.76024   |
| factorial_semantic | language_only            |         96 |             4 |             2 |       0         |
| factorial_semantic | masked                   |         96 |            91 |             0 |       3.19172   |
| factorial_semantic | shuffled                 |         96 |             1 |             3 |      -0.0903268 |
| factorial_semantic | full_official_chat       |         48 |            48 |             0 |       3.80277   |
| paired_contrast    | full_minus_language_only |         96 |            92 |             0 |       2.75554   |
| paired_contrast    | full_minus_shuffled      |         96 |            84 |             0 |       3.03317   |
| paired_contrast    | masked_minus_shuffled    |         96 |            90 |             0 |       3.35884   |
| lexical_gloss      | aggregate_semantic       |         48 |            48 |             0 |       3.97289   |
| natural_diagonal   | full_minus_language_only |         96 |            36 |            16 |       0.206349  |
| natural_diagonal   | full_minus_shuffled      |         96 |            94 |             0 |       2.30758   |
| natural_diagonal   | masked_minus_shuffled    |         96 |            82 |             0 |       1.57541   |

## Decision-level calibration (averaged over models, modes, wrappers)

| pair   | calibration             |   l1_accuracy |   l2_accuracy |   both_accuracy |   stingray_bias |   stingray_comprehension |
|:-------|:------------------------|--------------:|--------------:|----------------:|----------------:|-------------------------:|
| id_tl  | content_free_calibrated |      0.761364 |      0.760101 |        0.551768 |     -0.00108603 |                 0.762859 |
| id_tl  | raw                     |      0.713384 |      0.681818 |        0.410354 |     -0.020903   |                 0.701354 |
| zh_ja  | content_free_calibrated |      0.666667 |      0.768519 |        0.464506 |      0.0893474  |                 0.723776 |
| zh_ja  | raw                     |      0.759259 |      0.54321  |        0.319444 |     -0.206454   |                 0.662793 |

**Verdict:** conditional GO on the measurement question; KILL the semantic-overwrite claim and the causal “candidate prior” interpretation of the old midpoint. Four full-context failures are confined to Gemma-3-12B plain scoring; all official-chat variants pass. Natural correct contexts beat matched shuffled contexts much more consistently than they beat an explicit language-plus-target cue, which is a central limitation and part of the proposed measurement question.
