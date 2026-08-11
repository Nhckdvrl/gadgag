# Strict covariate-matched causal language excess

| model      | control             |   n_pairs | late_window              |   matched_language_excess |   ci_low |   ci_high |   positive_rate |   pos_l1_match_rate |   pos_l2_match_rate |
|:-----------|:--------------------|----------:|:-------------------------|--------------------------:|---------:|----------:|----------------:|--------------------:|--------------------:|
| qwen3_8b   | true_friend         |        20 | 0.75<=relative_depth<1.0 |                   5.96954 |  2.52636 |   9.70021 |          0.75   |              0.7    |              1      |
| qwen3_8b   | translation_control |        16 | 0.75<=relative_depth<1.0 |                   7.06844 |  3.1154  |  11.6509  |          0.75   |              0.6875 |              0.9375 |
| gemma3_12b | true_friend         |        20 | 0.75<=relative_depth<1.0 |                  12.7263  |  8.42602 |  17.3895  |          0.95   |              0.7    |              0.9    |
| gemma3_12b | translation_control |        16 | 0.75<=relative_depth<1.0 |                  15.5654  | 10.5617  |  20.7052  |          0.9375 |              0.6875 |              0.9375 |

The complete assignment below is diagnostic only when balance is poor. The hard gate requires exact broad POS in both languages plus common support on every continuous covariate.

## Hard common-support audit

| model      | control             |   caliper_sd_each_covariate |   exact_pos_pairs |   available_false |   available_control |   language_excess |      ci_low |   ci_high |
|:-----------|:--------------------|----------------------------:|------------------:|------------------:|--------------------:|------------------:|------------:|----------:|
| qwen3_8b   | true_friend         |                         1   |                 0 |                20 |                  20 |         nan       | nan         |  nan      |
| qwen3_8b   | true_friend         |                         1.5 |                 2 |                20 |                  20 |          17.6273  |   7.42102   |   27.8337 |
| qwen3_8b   | true_friend         |                         2   |                 9 |                20 |                  20 |           6.4972  |   0.0456204 |   13.6881 |
| qwen3_8b   | translation_control |                         1   |                 0 |                20 |                  16 |         nan       | nan         |  nan      |
| qwen3_8b   | translation_control |                         1.5 |                 1 |                20 |                  16 |         nan       | nan         |  nan      |
| qwen3_8b   | translation_control |                         2   |                 6 |                20 |                  16 |           8.63126 |   0.552237  |   17.9255 |
| gemma3_12b | true_friend         |                         1   |                 0 |                20 |                  20 |         nan       | nan         |  nan      |
| gemma3_12b | true_friend         |                         1.5 |                 0 |                20 |                  20 |         nan       | nan         |  nan      |
| gemma3_12b | true_friend         |                         2   |                 8 |                20 |                  20 |          14.2262  |   8.29093   |   20.6278 |
| gemma3_12b | translation_control |                         1   |                 0 |                20 |                  16 |         nan       | nan         |  nan      |
| gemma3_12b | translation_control |                         1.5 |                 0 |                20 |                  16 |         nan       | nan         |  nan      |
| gemma3_12b | translation_control |                         2   |                 8 |                20 |                  16 |          17.9005  |   9.58347   |   26.7635 |

## Balance

| model      | control             | covariate           |   smd_before |   smd_after |
|:-----------|:--------------------|:--------------------|-------------:|------------:|
| qwen3_8b   | true_friend         | freq_l1             |  -1.44266    | -1.44266    |
| qwen3_8b   | true_friend         | freq_l2             |  -1.516      | -1.516      |
| qwen3_8b   | true_friend         | freq_ratio          |  -0.00837678 | -0.00837678 |
| qwen3_8b   | true_friend         | token_l1            |   1.31211    |  1.31211    |
| qwen3_8b   | true_friend         | token_l2            |   1.31211    |  1.31211    |
| qwen3_8b   | true_friend         | token_total         |   1.31211    |  1.31211    |
| qwen3_8b   | true_friend         | gloss_mean_tokens   |   0.781073   |  0.781073   |
| qwen3_8b   | true_friend         | gloss_token_gap     |   1.50973    |  1.50973    |
| qwen3_8b   | true_friend         | baseline_difficulty |  -1.37154    | -1.37154    |
| qwen3_8b   | translation_control | freq_l1             |  -1.33414    | -1.21151    |
| qwen3_8b   | translation_control | freq_l2             |  -1.49579    | -1.24386    |
| qwen3_8b   | translation_control | freq_ratio          |   0.0166046  | -0.110006   |
| qwen3_8b   | translation_control | token_l1            |   1.27465    |  1.13808    |
| qwen3_8b   | translation_control | token_l2            |  -0.579724   | -0.668912   |
| qwen3_8b   | translation_control | token_total         |   0.194824   |  0.0573013  |
| qwen3_8b   | translation_control | gloss_mean_tokens   |   1.26582    |  0.916829   |
| qwen3_8b   | translation_control | gloss_token_gap     |   1.47904    |  1.33879    |
| qwen3_8b   | translation_control | baseline_difficulty |  -1.58698    | -1.55689    |
| gemma3_12b | true_friend         | freq_l1             |  -1.44266    | -1.44266    |
| gemma3_12b | true_friend         | freq_l2             |  -1.516      | -1.516      |
| gemma3_12b | true_friend         | freq_ratio          |  -0.00837678 | -0.00837678 |
| gemma3_12b | true_friend         | token_l1            |   1.23662    |  1.23662    |
| gemma3_12b | true_friend         | token_l2            |   1.23662    |  1.23662    |
| gemma3_12b | true_friend         | token_total         |   1.23662    |  1.23662    |
| gemma3_12b | true_friend         | gloss_mean_tokens   |   0.845154   |  0.845154   |
| gemma3_12b | true_friend         | gloss_token_gap     |   1.38873    |  1.38873    |
| gemma3_12b | true_friend         | baseline_difficulty |  -1.53723    | -1.53723    |
| gemma3_12b | translation_control | freq_l1             |  -1.33414    | -1.21151    |
| gemma3_12b | translation_control | freq_l2             |  -1.49579    | -1.24386    |
| gemma3_12b | translation_control | freq_ratio          |   0.0166046  | -0.110006   |
| gemma3_12b | translation_control | token_l1            |   1.19788    |  1.03662    |
| gemma3_12b | translation_control | token_l2            |   1.19788    |  1.03662    |
| gemma3_12b | translation_control | token_total         |   1.19788    |  1.03662    |
| gemma3_12b | translation_control | gloss_mean_tokens   |   1.21178    |  0.821068   |
| gemma3_12b | translation_control | gloss_token_gap     |   1.35329    |  1.18413    |
| gemma3_12b | translation_control | baseline_difficulty |  -1.67511    | -1.61902    |
