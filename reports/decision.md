# Semantic Overwrite Pilot Decision

## Decision: **KILL**

The pre-registered operational rule requires all three checks to pass:

- 128-exposure paired treated-minus-held-out Δmargin CI is below zero: `True`
- Effect is more negative at 128 than 32 exposures: `False`
- Treated CIR exceeds held-out CIR by at least 10 percentage points: `True`

## Crossover results

|   dose |   n_words |   paired_delta_margin |   ci95_low |   ci95_high |   treated_cir |   heldout_cir |   eligible_treated |   eligible_heldout |
|-------:|----------:|----------------------:|-----------:|------------:|--------------:|--------------:|-------------------:|-------------------:|
|     32 |        50 |             -0.559993 |  -0.969603 |  -0.161578  |      0.307692 |      0.128205 |                 39 |                 39 |
|    128 |        50 |             -0.511346 |  -0.987435 |  -0.0428055 |      0.307692 |      0.153846 |                 39 |                 39 |

## Group summaries

|   dose | group                  | treated   |   n |   pre_accuracy |   post_accuracy |   mean_delta_margin |   cir |
|-------:|:-----------------------|:----------|----:|---------------:|----------------:|--------------------:|------:|
|     32 | different_form_control | True      |  32 |           1    |            1    |            1.22981  |  0    |
|     32 | false_friend           | False     |  50 |           0.78 |            0.68 |           -0.513092 |  0.1  |
|     32 | false_friend           | True      |  50 |           0.78 |            0.58 |           -1.07309  |  0.24 |
|     32 | true_friend            | True      |  58 |           1    |            1    |            1.41006  |  0    |
|    128 | different_form_control | True      |  32 |           1    |            1    |            1.36671  |  0    |
|    128 | false_friend           | False     |  50 |           0.78 |            0.66 |           -0.486626 |  0.12 |
|    128 | false_friend           | True      |  50 |           0.78 |            0.58 |           -0.997973 |  0.24 |
|    128 | true_friend            | True      |  58 |           1    |            1    |            1.38744  |  0    |

CIR is computed only as pre-correct → specific Chinese-sense candidate post; the paired Δmargin is the primary causal estimand.
