# Independent natural-context construct validation

| model      | normalization   | contrast                    |   n_items |   estimate |     ci_low |     ci_high |   positive_rate |
|:-----------|:----------------|:----------------------------|----------:|-----------:|-----------:|------------:|----------------:|
| gemma3_12b | mean            | full_minus_unrelated        |       354 |  3.59446   |  2.91957   |  4.26872    |        0.70339  |
| gemma3_12b | mean            | masked_minus_unrelated      |       354 |  3.81488   |  3.21485   |  4.39029    |        0.768362 |
| gemma3_12b | mean            | full_minus_surface          |       354 |  4.30473   |  3.81229   |  4.81552    |        0.80226  |
| gemma3_12b | mean            | full_minus_masked           |       354 | -0.220427  | -0.683678  |  0.240208   |        0.483051 |
| gemma3_12b | mean            | accuracy_full               |       354 |  0.677966  |  0.629944  |  0.725989   |        0.677966 |
| gemma3_12b | mean            | accuracy_language_unrelated |       354 |  0.409605  |  0.358757  |  0.463277   |        0.409605 |
| gemma3_12b | mean            | accuracy_masked             |       354 |  0.734463  |  0.689266  |  0.779661   |        0.734463 |
| gemma3_12b | mean            | accuracy_surface_only       |       354 |  0.384181  |  0.333333  |  0.435028   |        0.384181 |
| gemma3_12b | sum             | full_minus_unrelated        |       354 |  3.59446   |  2.95065   |  4.28379    |        0.70339  |
| gemma3_12b | sum             | masked_minus_unrelated      |       354 |  3.81488   |  3.23878   |  4.36477    |        0.768362 |
| gemma3_12b | sum             | full_minus_surface          |       354 |  4.30473   |  3.7974    |  4.80307    |        0.80226  |
| gemma3_12b | sum             | full_minus_masked           |       354 | -0.220427  | -0.698124  |  0.24294    |        0.483051 |
| gemma3_12b | sum             | accuracy_full               |       354 |  0.677966  |  0.629944  |  0.725989   |        0.677966 |
| gemma3_12b | sum             | accuracy_language_unrelated |       354 |  0.409605  |  0.358757  |  0.460452   |        0.409605 |
| gemma3_12b | sum             | accuracy_masked             |       354 |  0.734463  |  0.686441  |  0.779661   |        0.734463 |
| gemma3_12b | sum             | accuracy_surface_only       |       354 |  0.384181  |  0.333333  |  0.435028   |        0.384181 |
| gemma3_4b  | mean            | full_minus_unrelated        |       354 | -0.067267  | -0.708976  |  0.59296    |        0.50565  |
| gemma3_4b  | mean            | masked_minus_unrelated      |       354 |  3.03328   |  2.5037    |  3.57045    |        0.745763 |
| gemma3_4b  | mean            | full_minus_surface          |       354 |  2.27622   |  1.7583    |  2.79134    |        0.675141 |
| gemma3_4b  | mean            | full_minus_masked           |       354 | -3.10055   | -3.58599   | -2.62288    |        0.268362 |
| gemma3_4b  | mean            | accuracy_full               |       354 |  0.432203  |  0.381356  |  0.483051   |        0.432203 |
| gemma3_4b  | mean            | accuracy_language_unrelated |       354 |  0.420904  |  0.370056  |  0.474576   |        0.420904 |
| gemma3_4b  | mean            | accuracy_masked             |       354 |  0.69774   |  0.649718  |  0.742938   |        0.69774  |
| gemma3_4b  | mean            | accuracy_surface_only       |       354 |  0.245763  |  0.20339   |  0.29096    |        0.245763 |
| gemma3_4b  | sum             | full_minus_unrelated        |       354 | -0.067267  | -0.720017  |  0.61397    |        0.50565  |
| gemma3_4b  | sum             | masked_minus_unrelated      |       354 |  3.03328   |  2.52401   |  3.5603     |        0.745763 |
| gemma3_4b  | sum             | full_minus_surface          |       354 |  2.27622   |  1.75378   |  2.7841     |        0.675141 |
| gemma3_4b  | sum             | full_minus_masked           |       354 | -3.10055   | -3.58079   | -2.61589    |        0.268362 |
| gemma3_4b  | sum             | accuracy_full               |       354 |  0.432203  |  0.381356  |  0.485876   |        0.432203 |
| gemma3_4b  | sum             | accuracy_language_unrelated |       354 |  0.420904  |  0.370056  |  0.468927   |        0.420904 |
| gemma3_4b  | sum             | accuracy_masked             |       354 |  0.69774   |  0.649718  |  0.745763   |        0.69774  |
| gemma3_4b  | sum             | accuracy_surface_only       |       354 |  0.245763  |  0.200565  |  0.29096    |        0.245763 |
| qwen25_7b  | mean            | full_minus_unrelated        |       354 |  3.93997   |  2.932     |  4.92118    |        0.652542 |
| qwen25_7b  | mean            | masked_minus_unrelated      |       354 |  4.49982   |  3.62541   |  5.37837    |        0.700565 |
| qwen25_7b  | mean            | full_minus_surface          |       354 |  5.24417   |  4.44235   |  6.049      |        0.737288 |
| qwen25_7b  | mean            | full_minus_masked           |       354 | -0.559852  | -1.24984   |  0.105142   |        0.491525 |
| qwen25_7b  | mean            | accuracy_full               |       354 |  0.652542  |  0.601695  |  0.70339    |        0.652542 |
| qwen25_7b  | mean            | accuracy_language_unrelated |       354 |  0.446328  |  0.392655  |  0.497175   |        0.446328 |
| qwen25_7b  | mean            | accuracy_masked             |       354 |  0.680791  |  0.632768  |  0.728814   |        0.680791 |
| qwen25_7b  | mean            | accuracy_surface_only       |       354 |  0.420904  |  0.370056  |  0.471751   |        0.420904 |
| qwen25_7b  | sum             | full_minus_unrelated        |       354 |  3.93997   |  2.97615   |  4.94175    |        0.652542 |
| qwen25_7b  | sum             | masked_minus_unrelated      |       354 |  4.49982   |  3.62305   |  5.37873    |        0.700565 |
| qwen25_7b  | sum             | full_minus_surface          |       354 |  5.24417   |  4.44199   |  6.05474    |        0.737288 |
| qwen25_7b  | sum             | full_minus_masked           |       354 | -0.559852  | -1.23632   |  0.135809   |        0.491525 |
| qwen25_7b  | sum             | accuracy_full               |       354 |  0.652542  |  0.601695  |  0.700565   |        0.652542 |
| qwen25_7b  | sum             | accuracy_language_unrelated |       354 |  0.446328  |  0.39548   |  0.497175   |        0.446328 |
| qwen25_7b  | sum             | accuracy_masked             |       354 |  0.680791  |  0.629944  |  0.728814   |        0.680791 |
| qwen25_7b  | sum             | accuracy_surface_only       |       354 |  0.420904  |  0.370056  |  0.474576   |        0.420904 |
| qwen3_8b   | mean            | full_minus_unrelated        |       354 | -0.0953693 | -0.111979  | -0.0781178  |        0.279661 |
| qwen3_8b   | mean            | masked_minus_unrelated      |       354 |  0.0256996 |  0.015065  |  0.0367514  |        0.584746 |
| qwen3_8b   | mean            | full_minus_surface          |       354 | -0.019203  | -0.031879  | -0.00674035 |        0.432203 |
| qwen3_8b   | mean            | full_minus_masked           |       354 | -0.121069  | -0.135153  | -0.106844   |        0.166667 |
| qwen3_8b   | mean            | accuracy_full               |       354 |  0.316384  |  0.268362  |  0.364407   |        0.316384 |
| qwen3_8b   | mean            | accuracy_language_unrelated |       354 |  0.508475  |  0.457627  |  0.559322   |        0.508475 |
| qwen3_8b   | mean            | accuracy_masked             |       354 |  0.590395  |  0.539548  |  0.641314   |        0.590395 |
| qwen3_8b   | mean            | accuracy_surface_only       |       354 |  0.293785  |  0.248588  |  0.338983   |        0.293785 |
| qwen3_8b   | sum             | full_minus_unrelated        |       354 | -0.0953693 | -0.112313  | -0.0787622  |        0.279661 |
| qwen3_8b   | sum             | masked_minus_unrelated      |       354 |  0.0256996 |  0.0148516 |  0.0366026  |        0.584746 |
| qwen3_8b   | sum             | full_minus_surface          |       354 | -0.019203  | -0.0319236 | -0.00658952 |        0.432203 |
| qwen3_8b   | sum             | full_minus_masked           |       354 | -0.121069  | -0.135701  | -0.107089   |        0.166667 |
| qwen3_8b   | sum             | accuracy_full               |       354 |  0.316384  |  0.268362  |  0.361582   |        0.316384 |
| qwen3_8b   | sum             | accuracy_language_unrelated |       354 |  0.508475  |  0.454802  |  0.559322   |        0.508475 |
| qwen3_8b   | sum             | accuracy_masked             |       354 |  0.590395  |  0.539548  |  0.638418   |        0.590395 |
| qwen3_8b   | sum             | accuracy_surface_only       |       354 |  0.293785  |  0.245763  |  0.341808   |        0.293785 |

## Raw vs context-adjusted ranking

| model      |   raw_full_accuracy |   raw_full_margin |   context_adjusted_margin |   rank_raw |   rank_adjusted |
|:-----------|--------------------:|------------------:|--------------------------:|-----------:|----------------:|
| gemma3_12b |            0.677966 |         2.80208   |                 3.59446   |          2 |               2 |
| gemma3_4b  |            0.432203 |        -0.711953  |                -0.067267  |          4 |               3 |
| qwen25_7b  |            0.652542 |         3.53125   |                 3.93997   |          1 |               1 |
| qwen3_8b   |            0.316384 |        -0.0901831 |                -0.0953693 |          3 |               4 |
