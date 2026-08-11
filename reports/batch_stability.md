# Scoring batch-size stability

## Cell margins

| pair   | model      | prompt_mode   | normalization   |   n_cells |   mean_abs_margin_difference |   max_abs_margin_difference |   decision_sign_flips |   decision_sign_flip_rate |   pearson_margin |
|:-------|:-----------|:--------------|:----------------|----------:|-----------------------------:|----------------------------:|----------------------:|--------------------------:|-----------------:|
| zh_ja  | qwen25_7b  | chat          | mean            |      1296 |                    0.0607635 |                     0.71896 |                     8 |                0.00617284 |         0.999762 |
| zh_ja  | qwen25_7b  | chat          | sum             |      1296 |                    0.223129  |                     2.08423 |                     8 |                0.00617284 |         0.999833 |
| id_tl  | gemma3_12b | plain         | mean            |      1584 |                    0.0880347 |                     1.1875  |                    19 |                0.0119949  |         0.999179 |
| id_tl  | gemma3_12b | plain         | sum             |      1584 |                    0.327953  |                     6.3042  |                    12 |                0.00757576 |         0.999438 |

## Full-context semantic effects

| pair   | model      | prompt_mode   |   batch_size | wrapper    | normalization   |   n_items |   semantic_effect |     ci_low |   ci_high |
|:-------|:-----------|:--------------|-------------:|:-----------|:----------------|----------:|------------------:|-----------:|----------:|
| zh_ja  | qwen25_7b  | chat          |            8 | bare       | mean            |        27 |         2.18768   |  1.47492   |  2.93026  |
| zh_ja  | qwen25_7b  | chat          |            8 | bare       | sum             |        27 |         7.40844   |  4.94524   |  9.98797  |
| zh_ja  | qwen25_7b  | chat          |            8 | definition | mean            |        27 |         1.26215   |  0.959256  |  1.58502  |
| zh_ja  | qwen25_7b  | chat          |            8 | definition | sum             |        27 |         7.46      |  5.31824   |  9.70319  |
| zh_ja  | qwen25_7b  | chat          |            8 | refers     | mean            |        27 |         2.02403   |  1.63656   |  2.42651  |
| zh_ja  | qwen25_7b  | chat          |            8 | refers     | sum             |        27 |        13.3374    | 10.7581    | 16.0358   |
| zh_ja  | qwen25_7b  | chat          |           32 | bare       | mean            |        27 |         2.17055   |  1.47967   |  2.89542  |
| zh_ja  | qwen25_7b  | chat          |           32 | bare       | sum             |        27 |         7.43434   |  4.98873   |  9.99957  |
| zh_ja  | qwen25_7b  | chat          |           32 | definition | mean            |        27 |         1.23643   |  0.929163  |  1.56482  |
| zh_ja  | qwen25_7b  | chat          |           32 | definition | sum             |        27 |         7.35443   |  5.17359   |  9.63245  |
| zh_ja  | qwen25_7b  | chat          |           32 | refers     | mean            |        27 |         2.02327   |  1.6327    |  2.42857  |
| zh_ja  | qwen25_7b  | chat          |           32 | refers     | sum             |        27 |        13.3182    | 10.7377    | 15.9943   |
| id_tl  | gemma3_12b | plain         |            8 | bare       | mean            |        33 |         0.169425  | -0.163922  |  0.520531 |
| id_tl  | gemma3_12b | plain         |            8 | bare       | sum             |        33 |         0.929255  | -0.125241  |  2.5304   |
| id_tl  | gemma3_12b | plain         |            8 | definition | mean            |        33 |         0.0433094 | -0.0938471 |  0.173063 |
| id_tl  | gemma3_12b | plain         |            8 | definition | sum             |        33 |         0.883208  | -0.01821   |  2.19095  |
| id_tl  | gemma3_12b | plain         |            8 | refers     | mean            |        33 |         0.206611  |  0.0675162 |  0.366771 |
| id_tl  | gemma3_12b | plain         |            8 | refers     | sum             |        33 |         1.88532   |  0.640519  |  3.56624  |
| id_tl  | gemma3_12b | plain         |           32 | bare       | mean            |        33 |         0.125871  | -0.193992  |  0.470949 |
| id_tl  | gemma3_12b | plain         |           32 | bare       | sum             |        33 |         0.753745  | -0.206586  |  2.13277  |
| id_tl  | gemma3_12b | plain         |           32 | definition | mean            |        33 |         0.0557943 | -0.0765507 |  0.181541 |
| id_tl  | gemma3_12b | plain         |           32 | definition | sum             |        33 |         0.895312  |  0.0411452 |  2.13062  |
| id_tl  | gemma3_12b | plain         |           32 | refers     | mean            |        33 |         0.195194  |  0.0673367 |  0.336694 |
| id_tl  | gemma3_12b | plain         |           32 | refers     | sum             |        33 |         1.7003    |  0.557471  |  3.14859  |
