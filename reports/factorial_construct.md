# Exact-form language × semantic-context construct killer

## Gate

| pair   | model      | prompt_mode   |   n_variants | all_full_semantic_ci_positive   |
|:-------|:-----------|:--------------|-------------:|:--------------------------------|
| id_tl  | gemma3_12b | chat          |            6 | True                            |
| id_tl  | gemma3_12b | plain         |            6 | False                           |
| id_tl  | gemma3_4b  | chat          |            6 | True                            |
| id_tl  | gemma3_4b  | plain         |            6 | True                            |
| id_tl  | qwen25_7b  | chat          |            6 | True                            |
| id_tl  | qwen25_7b  | plain         |            6 | True                            |
| id_tl  | qwen3_8b   | chat          |            6 | True                            |
| id_tl  | qwen3_8b   | plain         |            6 | True                            |
| zh_ja  | gemma3_12b | chat          |            6 | True                            |
| zh_ja  | gemma3_12b | plain         |            6 | False                           |
| zh_ja  | gemma3_4b  | chat          |            6 | True                            |
| zh_ja  | gemma3_4b  | plain         |            6 | True                            |
| zh_ja  | qwen25_7b  | chat          |            6 | True                            |
| zh_ja  | qwen25_7b  | plain         |            6 | True                            |
| zh_ja  | qwen3_8b   | chat          |            6 | True                            |
| zh_ja  | qwen3_8b   | plain         |            6 | True                            |

## Semantic effects

| pair   | model      | prompt_mode   | condition     | wrapper    | normalization   | effect   |   n |     estimate |       ci_low |      ci_high |   positive_rate |
|:-------|:-----------|:--------------|:--------------|:-----------|:----------------|:---------|----:|-------------:|-------------:|-------------:|----------------:|
| id_tl  | gemma3_12b | chat          | full          | bare       | mean            | semantic |  33 |  4.17797     |  2.71419     |  5.75231     |       0.878788  |
| id_tl  | gemma3_12b | chat          | full          | bare       | sum             | semantic |  33 |  5.2861      |  3.17238     |  7.61144     |       0.878788  |
| id_tl  | gemma3_12b | chat          | full          | definition | mean            | semantic |  33 |  3.16913     |  2.45815     |  3.89441     |       0.969697  |
| id_tl  | gemma3_12b | chat          | full          | definition | sum             | semantic |  33 | 13.0423      | 10.0604      | 16.0814      |       0.939394  |
| id_tl  | gemma3_12b | chat          | full          | refers     | mean            | semantic |  33 |  2.67581     |  2.0721      |  3.28749     |       0.969697  |
| id_tl  | gemma3_12b | chat          | full          | refers     | sum             | semantic |  33 | 13.9796      | 11.0023      | 16.9566      |       0.969697  |
| id_tl  | gemma3_12b | chat          | language_only | bare       | mean            | semantic |  33 |  0.00184056  | -0.0387321   |  0.036771    |       0.212121  |
| id_tl  | gemma3_12b | chat          | language_only | bare       | sum             | semantic |  33 | -0.0300818   | -0.0669159   |  0.00537458  |       0.121212  |
| id_tl  | gemma3_12b | chat          | language_only | definition | mean            | semantic |  33 |  0.0025177   | -0.00197021  |  0.00741974  |       0.272727  |
| id_tl  | gemma3_12b | chat          | language_only | definition | sum             | semantic |  33 |  0.0103426   | -0.00545492  |  0.0277358   |       0.30303   |
| id_tl  | gemma3_12b | chat          | language_only | refers     | mean            | semantic |  33 |  0           |  0           |  0           |       0         |
| id_tl  | gemma3_12b | chat          | language_only | refers     | sum             | semantic |  33 |  0           |  0           |  0           |       0         |
| id_tl  | gemma3_12b | chat          | masked        | bare       | mean            | semantic |  33 |  3.32636     |  2.01886     |  4.77154     |       0.848485  |
| id_tl  | gemma3_12b | chat          | masked        | bare       | sum             | semantic |  33 |  4.7208      |  2.64902     |  6.90491     |       0.878788  |
| id_tl  | gemma3_12b | chat          | masked        | definition | mean            | semantic |  33 |  2.83359     |  2.21417     |  3.48121     |       0.969697  |
| id_tl  | gemma3_12b | chat          | masked        | definition | sum             | semantic |  33 | 11.7052      |  9.08158     | 14.1351      |       0.909091  |
| id_tl  | gemma3_12b | chat          | masked        | refers     | mean            | semantic |  33 |  2.7014      |  2.13903     |  3.28474     |       0.969697  |
| id_tl  | gemma3_12b | chat          | masked        | refers     | sum             | semantic |  33 | 13.7056      | 10.909       | 16.6338      |       0.969697  |
| id_tl  | gemma3_12b | chat          | shuffled      | bare       | mean            | semantic |  33 | -0.116613    | -1.16872     |  1.0096      |       0.363636  |
| id_tl  | gemma3_12b | chat          | shuffled      | bare       | sum             | semantic |  33 | -0.670079    | -2.48422     |  1.25109     |       0.363636  |
| id_tl  | gemma3_12b | chat          | shuffled      | definition | mean            | semantic |  33 | -0.257051    | -0.64564     |  0.0985813   |       0.424242  |
| id_tl  | gemma3_12b | chat          | shuffled      | definition | sum             | semantic |  33 | -1.50543     | -3.44345     |  0.166787    |       0.424242  |
| id_tl  | gemma3_12b | chat          | shuffled      | refers     | mean            | semantic |  33 |  0.0463648   | -0.326233    |  0.36204     |       0.515152  |
| id_tl  | gemma3_12b | chat          | shuffled      | refers     | sum             | semantic |  33 | -0.233569    | -2.25502     |  1.45437     |       0.484848  |
| id_tl  | gemma3_12b | plain         | full          | bare       | mean            | semantic |  33 |  0.125871    | -0.203926    |  0.475289    |       0.484848  |
| id_tl  | gemma3_12b | plain         | full          | bare       | sum             | semantic |  33 |  0.753745    | -0.21727     |  2.18042     |       0.515152  |
| id_tl  | gemma3_12b | plain         | full          | definition | mean            | semantic |  33 |  0.0557943   | -0.079117    |  0.180208    |       0.606061  |
| id_tl  | gemma3_12b | plain         | full          | definition | sum             | semantic |  33 |  0.895312    |  0.034009    |  2.14141     |       0.666667  |
| id_tl  | gemma3_12b | plain         | full          | refers     | mean            | semantic |  33 |  0.195194    |  0.0649477   |  0.340527    |       0.69697   |
| id_tl  | gemma3_12b | plain         | full          | refers     | sum             | semantic |  33 |  1.7003      |  0.540314    |  3.13565     |       0.727273  |
| id_tl  | gemma3_12b | plain         | language_only | bare       | mean            | semantic |  33 | -0.0109399   | -0.0372236   |  0.01442     |       0.0909091 |
| id_tl  | gemma3_12b | plain         | language_only | bare       | sum             | semantic |  33 |  0.00241973  | -0.0435963   |  0.0490388   |       0.121212  |
| id_tl  | gemma3_12b | plain         | language_only | definition | mean            | semantic |  33 | -0.00125331  | -0.00753383  |  0.00495058  |       0.0909091 |
| id_tl  | gemma3_12b | plain         | language_only | definition | sum             | semantic |  33 |  0.00582915  | -0.032267    |  0.046909    |       0.121212  |
| id_tl  | gemma3_12b | plain         | language_only | refers     | mean            | semantic |  33 |  0           |  0           |  0           |       0         |
| id_tl  | gemma3_12b | plain         | language_only | refers     | sum             | semantic |  33 |  0           |  0           |  0           |       0         |
| id_tl  | gemma3_12b | plain         | masked        | bare       | mean            | semantic |  33 |  0.114147    | -0.248979    |  0.489865    |       0.515152  |
| id_tl  | gemma3_12b | plain         | masked        | bare       | sum             | semantic |  33 |  0.58564     | -0.232518    |  1.76095     |       0.545455  |
| id_tl  | gemma3_12b | plain         | masked        | definition | mean            | semantic |  33 |  0.0437287   | -0.0632331   |  0.166127    |       0.545455  |
| id_tl  | gemma3_12b | plain         | masked        | definition | sum             | semantic |  33 |  0.511167    | -0.198205    |  1.53711     |       0.636364  |
| id_tl  | gemma3_12b | plain         | masked        | refers     | mean            | semantic |  33 |  0.116762    |  0.0395651   |  0.19068     |       0.787879  |
| id_tl  | gemma3_12b | plain         | masked        | refers     | sum             | semantic |  33 |  0.887997    |  0.230614    |  1.66011     |       0.757576  |
| id_tl  | gemma3_12b | plain         | shuffled      | bare       | mean            | semantic |  33 |  0.340999    | -0.0852128   |  0.76467     |       0.606061  |
| id_tl  | gemma3_12b | plain         | shuffled      | bare       | sum             | semantic |  33 | -0.171505    | -0.864854    |  0.433577    |       0.545455  |
| id_tl  | gemma3_12b | plain         | shuffled      | definition | mean            | semantic |  33 |  0.0476966   | -0.0765214   |  0.178118    |       0.545455  |
| id_tl  | gemma3_12b | plain         | shuffled      | definition | sum             | semantic |  33 | -0.0967818   | -0.89402     |  0.663864    |       0.484848  |
| id_tl  | gemma3_12b | plain         | shuffled      | refers     | mean            | semantic |  33 |  0.139999    |  0.0380494   |  0.245943    |       0.727273  |
| id_tl  | gemma3_12b | plain         | shuffled      | refers     | sum             | semantic |  33 |  0.351207    | -0.459787    |  1.10933     |       0.666667  |
| id_tl  | gemma3_4b  | chat          | full          | bare       | mean            | semantic |  33 |  9.16758     |  6.94414     | 11.3724      |       0.909091  |
| id_tl  | gemma3_4b  | chat          | full          | bare       | sum             | semantic |  33 | 10.5314      |  7.28366     | 14.1295      |       0.878788  |
| id_tl  | gemma3_4b  | chat          | full          | definition | mean            | semantic |  33 |  2.73519     |  2.21843     |  3.23802     |       0.969697  |
| id_tl  | gemma3_4b  | chat          | full          | definition | sum             | semantic |  33 | 11.0243      |  8.89305     | 13.1918      |       0.969697  |
| id_tl  | gemma3_4b  | chat          | full          | refers     | mean            | semantic |  33 |  2.9438      |  2.23958     |  3.68515     |       0.848485  |
| id_tl  | gemma3_4b  | chat          | full          | refers     | sum             | semantic |  33 | 14.8321      | 11.2188      | 18.6393      |       0.878788  |
| id_tl  | gemma3_4b  | chat          | language_only | bare       | mean            | semantic |  33 | -0.0144315   | -0.0587497   |  0.0259855   |       0.181818  |
| id_tl  | gemma3_4b  | chat          | language_only | bare       | sum             | semantic |  33 | -0.0227464   | -0.0629791   |  0.0107233   |       0.272727  |
| id_tl  | gemma3_4b  | chat          | language_only | definition | mean            | semantic |  33 |  0.00951029  | -0.00023633  |  0.0199428   |       0.333333  |
| id_tl  | gemma3_4b  | chat          | language_only | definition | sum             | semantic |  33 |  0.0269426   | -0.0119773   |  0.0656912   |       0.333333  |
| id_tl  | gemma3_4b  | chat          | language_only | refers     | mean            | semantic |  33 |  0           |  0           |  0           |       0         |
| id_tl  | gemma3_4b  | chat          | language_only | refers     | sum             | semantic |  33 |  0           |  0           |  0           |       0         |
| id_tl  | gemma3_4b  | chat          | masked        | bare       | mean            | semantic |  33 |  4.03982     |  2.1531      |  6.03052     |       0.787879  |
| id_tl  | gemma3_4b  | chat          | masked        | bare       | sum             | semantic |  33 |  5.18461     |  1.39278     |  8.79307     |       0.727273  |
| id_tl  | gemma3_4b  | chat          | masked        | definition | mean            | semantic |  33 |  1.82543     |  1.2986      |  2.34868     |       0.939394  |
| id_tl  | gemma3_4b  | chat          | masked        | definition | sum             | semantic |  33 |  7.74265     |  5.50927     |  9.95516     |       0.969697  |
| id_tl  | gemma3_4b  | chat          | masked        | refers     | mean            | semantic |  33 |  2.83786     |  2.13715     |  3.56006     |       0.909091  |
| id_tl  | gemma3_4b  | chat          | masked        | refers     | sum             | semantic |  33 | 14.139       | 10.2544      | 17.9137      |       0.878788  |
| id_tl  | gemma3_4b  | chat          | shuffled      | bare       | mean            | semantic |  33 |  0.0297315   | -2.64815     |  2.73066     |       0.454545  |
| id_tl  | gemma3_4b  | chat          | shuffled      | bare       | sum             | semantic |  33 | -1.17872     | -5.13617     |  2.36635     |       0.393939  |
| id_tl  | gemma3_4b  | chat          | shuffled      | definition | mean            | semantic |  33 | -0.31025     | -0.943907    |  0.191059    |       0.484848  |
| id_tl  | gemma3_4b  | chat          | shuffled      | definition | sum             | semantic |  33 | -1.86868     | -4.77959     |  0.412807    |       0.484848  |
| id_tl  | gemma3_4b  | chat          | shuffled      | refers     | mean            | semantic |  33 | -0.138854    | -0.634255    |  0.302227    |       0.575758  |
| id_tl  | gemma3_4b  | chat          | shuffled      | refers     | sum             | semantic |  33 | -1.35566     | -4.08608     |  1.1485      |       0.575758  |
| id_tl  | gemma3_4b  | plain         | full          | bare       | mean            | semantic |  33 |  0.780609    |  0.144521    |  1.43553     |       0.666667  |
| id_tl  | gemma3_4b  | plain         | full          | bare       | sum             | semantic |  33 |  0.970083    |  0.16516     |  1.75783     |       0.636364  |
| id_tl  | gemma3_4b  | plain         | full          | definition | mean            | semantic |  33 |  0.24014     |  0.0695512   |  0.407512    |       0.636364  |
| id_tl  | gemma3_4b  | plain         | full          | definition | sum             | semantic |  33 |  1.09093     |  0.191466    |  2.07995     |       0.575758  |
| id_tl  | gemma3_4b  | plain         | full          | refers     | mean            | semantic |  33 |  0.414716    |  0.216561    |  0.611062    |       0.787879  |
| id_tl  | gemma3_4b  | plain         | full          | refers     | sum             | semantic |  33 |  2.07569     |  0.994557    |  3.18142     |       0.757576  |
| id_tl  | gemma3_4b  | plain         | language_only | bare       | mean            | semantic |  33 | -0.0136115   | -0.0302556   |  0.00368506  |       0.181818  |
| id_tl  | gemma3_4b  | plain         | language_only | bare       | sum             | semantic |  33 | -0.0129144   | -0.0301945   |  0.00398606  |       0.242424  |
| id_tl  | gemma3_4b  | plain         | language_only | definition | mean            | semantic |  33 | -1.71228e-05 | -0.00448863  |  0.00489555  |       0.30303   |
| id_tl  | gemma3_4b  | plain         | language_only | definition | sum             | semantic |  33 | -0.00211982  | -0.0227255   |  0.0186312   |       0.272727  |
| id_tl  | gemma3_4b  | plain         | language_only | refers     | mean            | semantic |  33 |  0           |  0           |  0           |       0         |
| id_tl  | gemma3_4b  | plain         | language_only | refers     | sum             | semantic |  33 |  0           |  0           |  0           |       0         |
| id_tl  | gemma3_4b  | plain         | masked        | bare       | mean            | semantic |  33 |  0.630596    |  0.0895549   |  1.14535     |       0.666667  |
| id_tl  | gemma3_4b  | plain         | masked        | bare       | sum             | semantic |  33 |  0.760052    |  0.0876929   |  1.44639     |       0.606061  |
| id_tl  | gemma3_4b  | plain         | masked        | definition | mean            | semantic |  33 |  0.294332    |  0.151582    |  0.438737    |       0.787879  |
| id_tl  | gemma3_4b  | plain         | masked        | definition | sum             | semantic |  33 |  1.38966     |  0.619735    |  2.18305     |       0.818182  |
| id_tl  | gemma3_4b  | plain         | masked        | refers     | mean            | semantic |  33 |  0.330995    |  0.181775    |  0.48281     |       0.787879  |
| id_tl  | gemma3_4b  | plain         | masked        | refers     | sum             | semantic |  33 |  1.78698     |  0.905058    |  2.7354      |       0.757576  |
| id_tl  | gemma3_4b  | plain         | shuffled      | bare       | mean            | semantic |  33 | -0.313619    | -0.839018    |  0.201803    |       0.393939  |
| id_tl  | gemma3_4b  | plain         | shuffled      | bare       | sum             | semantic |  33 | -0.403444    | -1.12041     |  0.281218    |       0.424242  |
| id_tl  | gemma3_4b  | plain         | shuffled      | definition | mean            | semantic |  33 | -0.0610412   | -0.221043    |  0.0846265   |       0.424242  |
| id_tl  | gemma3_4b  | plain         | shuffled      | definition | sum             | semantic |  33 | -0.161693    | -1.04719     |  0.689584    |       0.454545  |
| id_tl  | gemma3_4b  | plain         | shuffled      | refers     | mean            | semantic |  33 |  0.00957501  | -0.145894    |  0.155162    |       0.484848  |
| id_tl  | gemma3_4b  | plain         | shuffled      | refers     | sum             | semantic |  33 |  0.0673648   | -0.813576    |  0.93593     |       0.454545  |
| id_tl  | qwen25_7b  | chat          | full          | bare       | mean            | semantic |  33 |  3.09481     |  2.17014     |  4.066       |       0.878788  |
| id_tl  | qwen25_7b  | chat          | full          | bare       | sum             | semantic |  33 |  4.58648     |  3.44132     |  5.84842     |       0.909091  |
| id_tl  | qwen25_7b  | chat          | full          | definition | mean            | semantic |  33 |  0.939705    |  0.626739    |  1.26238     |       0.848485  |
| id_tl  | qwen25_7b  | chat          | full          | definition | sum             | semantic |  33 |  3.96496     |  2.52856     |  5.42554     |       0.818182  |
| id_tl  | qwen25_7b  | chat          | full          | refers     | mean            | semantic |  33 |  1.74341     |  1.31118     |  2.17456     |       0.939394  |
| id_tl  | qwen25_7b  | chat          | full          | refers     | sum             | semantic |  33 |  9.43804     |  7.33904     | 11.4372      |       0.939394  |
| id_tl  | qwen25_7b  | chat          | language_only | bare       | mean            | semantic |  33 | -0.00168875  | -0.0337461   |  0.0287138   |       0.151515  |
| id_tl  | qwen25_7b  | chat          | language_only | bare       | sum             | semantic |  33 |  0.00559498  | -0.0331925   |  0.0551053   |       0.151515  |
| id_tl  | qwen25_7b  | chat          | language_only | definition | mean            | semantic |  33 | -8.87351e-05 | -0.0052057   |  0.00572696  |       0.121212  |
| id_tl  | qwen25_7b  | chat          | language_only | definition | sum             | semantic |  33 |  0.000457879 | -0.0196685   |  0.0227406   |       0.121212  |
| id_tl  | qwen25_7b  | chat          | language_only | refers     | mean            | semantic |  33 |  0           |  0           |  0           |       0         |
| id_tl  | qwen25_7b  | chat          | language_only | refers     | sum             | semantic |  33 |  0           |  0           |  0           |       0         |
| id_tl  | qwen25_7b  | chat          | masked        | bare       | mean            | semantic |  33 |  3.19231     |  2.33658     |  4.17739     |       0.969697  |
| id_tl  | qwen25_7b  | chat          | masked        | bare       | sum             | semantic |  33 |  5.58372     |  3.33463     |  8.02605     |       0.939394  |
| id_tl  | qwen25_7b  | chat          | masked        | definition | mean            | semantic |  33 |  0.880658    |  0.497818    |  1.2499      |       0.757576  |
| id_tl  | qwen25_7b  | chat          | masked        | definition | sum             | semantic |  33 |  3.63727     |  1.62889     |  5.51605     |       0.757576  |
| id_tl  | qwen25_7b  | chat          | masked        | refers     | mean            | semantic |  33 |  1.81118     |  1.39684     |  2.26105     |       1         |
| id_tl  | qwen25_7b  | chat          | masked        | refers     | sum             | semantic |  33 |  9.25173     |  6.83825     | 11.6837      |       0.969697  |
| id_tl  | qwen25_7b  | chat          | shuffled      | bare       | mean            | semantic |  33 | -0.123232    | -0.859626    |  0.559315    |       0.575758  |
| id_tl  | qwen25_7b  | chat          | shuffled      | bare       | sum             | semantic |  33 | -0.268619    | -1.89348     |  1.37301     |       0.484848  |
| id_tl  | qwen25_7b  | chat          | shuffled      | definition | mean            | semantic |  33 | -0.221262    | -0.514027    |  0.0244479   |       0.484848  |
| id_tl  | qwen25_7b  | chat          | shuffled      | definition | sum             | semantic |  33 | -0.948224    | -2.34393     |  0.184922    |       0.515152  |
| id_tl  | qwen25_7b  | chat          | shuffled      | refers     | mean            | semantic |  33 | -0.219661    | -0.631558    |  0.132961    |       0.484848  |
| id_tl  | qwen25_7b  | chat          | shuffled      | refers     | sum             | semantic |  33 | -1.03977     | -3.16947     |  0.808339    |       0.484848  |
| id_tl  | qwen25_7b  | plain         | full          | bare       | mean            | semantic |  33 |  4.6617      |  3.51929     |  5.84432     |       0.909091  |
| id_tl  | qwen25_7b  | plain         | full          | bare       | sum             | semantic |  33 |  5.43362     |  4.04056     |  7.05285     |       0.909091  |
| id_tl  | qwen25_7b  | plain         | full          | definition | mean            | semantic |  33 |  1.52862     |  1.18115     |  1.87302     |       0.969697  |
| id_tl  | qwen25_7b  | plain         | full          | definition | sum             | semantic |  33 |  6.58767     |  5.17749     |  8.08703     |       0.939394  |
| id_tl  | qwen25_7b  | plain         | full          | refers     | mean            | semantic |  33 |  1.34806     |  1.04761     |  1.66029     |       0.969697  |
| id_tl  | qwen25_7b  | plain         | full          | refers     | sum             | semantic |  33 |  7.41079     |  5.93122     |  8.98731     |       0.969697  |
| id_tl  | qwen25_7b  | plain         | language_only | bare       | mean            | semantic |  33 |  0.0179458   |  0.00232177  |  0.0407071   |       0.181818  |
| id_tl  | qwen25_7b  | plain         | language_only | bare       | sum             | semantic |  33 |  0.0254549   |  0.00420692  |  0.0554771   |       0.181818  |
| id_tl  | qwen25_7b  | plain         | language_only | definition | mean            | semantic |  33 |  0.00328863  |  0.000737718 |  0.00663354  |       0.212121  |
| id_tl  | qwen25_7b  | plain         | language_only | definition | sum             | semantic |  33 |  0.0142037   |  0.00242655  |  0.0291388   |       0.181818  |
| id_tl  | qwen25_7b  | plain         | language_only | refers     | mean            | semantic |  33 |  0           |  0           |  0           |       0         |
| id_tl  | qwen25_7b  | plain         | language_only | refers     | sum             | semantic |  33 |  0           |  0           |  0           |       0         |
| id_tl  | qwen25_7b  | plain         | masked        | bare       | mean            | semantic |  33 |  4.53661     |  3.30391     |  5.72978     |       0.939394  |
| id_tl  | qwen25_7b  | plain         | masked        | bare       | sum             | semantic |  33 |  5.49021     |  4.01622     |  7.21523     |       0.939394  |
| id_tl  | qwen25_7b  | plain         | masked        | definition | mean            | semantic |  33 |  1.50371     |  1.09747     |  1.91847     |       0.969697  |
| id_tl  | qwen25_7b  | plain         | masked        | definition | sum             | semantic |  33 |  6.58383     |  4.84767     |  8.31378     |       0.939394  |
| id_tl  | qwen25_7b  | plain         | masked        | refers     | mean            | semantic |  33 |  1.75697     |  1.37519     |  2.1758      |       1         |
| id_tl  | qwen25_7b  | plain         | masked        | refers     | sum             | semantic |  33 |  9.40462     |  7.47319     | 11.5526      |       1         |
| id_tl  | qwen25_7b  | plain         | shuffled      | bare       | mean            | semantic |  33 |  0.000160159 | -1.12141     |  1.12241     |       0.454545  |
| id_tl  | qwen25_7b  | plain         | shuffled      | bare       | sum             | semantic |  33 | -0.0598647   | -1.44549     |  1.36426     |       0.454545  |
| id_tl  | qwen25_7b  | plain         | shuffled      | definition | mean            | semantic |  33 | -0.149459    | -0.479706    |  0.14798     |       0.424242  |
| id_tl  | qwen25_7b  | plain         | shuffled      | definition | sum             | semantic |  33 | -0.49481     | -1.90126     |  0.7241      |       0.454545  |
| id_tl  | qwen25_7b  | plain         | shuffled      | refers     | mean            | semantic |  33 | -0.0838718   | -0.423703    |  0.213606    |       0.575758  |
| id_tl  | qwen25_7b  | plain         | shuffled      | refers     | sum             | semantic |  33 | -0.672319    | -2.2975      |  0.837729    |       0.424242  |
| id_tl  | qwen3_8b   | chat          | full          | bare       | mean            | semantic |  33 |  0.585958    |  0.352344    |  0.840478    |       0.818182  |
| id_tl  | qwen3_8b   | chat          | full          | bare       | sum             | semantic |  33 |  1.46541     |  0.871786    |  2.08467     |       0.818182  |
| id_tl  | qwen3_8b   | chat          | full          | definition | mean            | semantic |  33 |  0.832366    |  0.60948     |  1.04281     |       0.909091  |
| id_tl  | qwen3_8b   | chat          | full          | definition | sum             | semantic |  33 |  3.64058     |  2.7382      |  4.57839     |       0.939394  |
| id_tl  | qwen3_8b   | chat          | full          | refers     | mean            | semantic |  33 |  0.907909    |  0.671171    |  1.1801      |       0.969697  |
| id_tl  | qwen3_8b   | chat          | full          | refers     | sum             | semantic |  33 |  4.90804     |  3.72121     |  6.16096     |       0.969697  |
| id_tl  | qwen3_8b   | chat          | language_only | bare       | mean            | semantic |  33 | -0.00579535  | -0.0263029   |  0.0142444   |       0.272727  |
| id_tl  | qwen3_8b   | chat          | language_only | bare       | sum             | semantic |  33 | -0.0216868   | -0.060314    |  0.0162579   |       0.30303   |
| id_tl  | qwen3_8b   | chat          | language_only | definition | mean            | semantic |  33 | -0.000182773 | -0.00387449  |  0.00370893  |       0.30303   |
| id_tl  | qwen3_8b   | chat          | language_only | definition | sum             | semantic |  33 |  0.00400277  | -0.0104408   |  0.0184879   |       0.363636  |
| id_tl  | qwen3_8b   | chat          | language_only | refers     | mean            | semantic |  33 |  0           |  0           |  0           |       0         |
| id_tl  | qwen3_8b   | chat          | language_only | refers     | sum             | semantic |  33 |  0           |  0           |  0           |       0         |
| id_tl  | qwen3_8b   | chat          | masked        | bare       | mean            | semantic |  33 |  0.944519    |  0.470235    |  1.45245     |       0.666667  |
| id_tl  | qwen3_8b   | chat          | masked        | bare       | sum             | semantic |  33 |  2.38821     |  1.1293      |  3.79238     |       0.69697   |
| id_tl  | qwen3_8b   | chat          | masked        | definition | mean            | semantic |  33 |  0.726815    |  0.586402    |  0.880691    |       0.969697  |
| id_tl  | qwen3_8b   | chat          | masked        | definition | sum             | semantic |  33 |  3.19113     |  2.55268     |  3.86306     |       0.969697  |
| id_tl  | qwen3_8b   | chat          | masked        | refers     | mean            | semantic |  33 |  1.01007     |  0.79219     |  1.22391     |       1         |
| id_tl  | qwen3_8b   | chat          | masked        | refers     | sum             | semantic |  33 |  5.29837     |  4.2154      |  6.42065     |       1         |
| id_tl  | qwen3_8b   | chat          | shuffled      | bare       | mean            | semantic |  33 |  0.049752    | -0.369292    |  0.432334    |       0.575758  |
| id_tl  | qwen3_8b   | chat          | shuffled      | bare       | sum             | semantic |  33 |  0.0974027   | -0.665205    |  0.872733    |       0.575758  |
| id_tl  | qwen3_8b   | chat          | shuffled      | definition | mean            | semantic |  33 | -0.0474177   | -0.200038    |  0.086439    |       0.545455  |
| id_tl  | qwen3_8b   | chat          | shuffled      | definition | sum             | semantic |  33 | -0.211015    | -0.919423    |  0.444875    |       0.545455  |
| id_tl  | qwen3_8b   | chat          | shuffled      | refers     | mean            | semantic |  33 | -0.0280407   | -0.205215    |  0.134966    |       0.424242  |
| id_tl  | qwen3_8b   | chat          | shuffled      | refers     | sum             | semantic |  33 | -0.119662    | -1.16731     |  0.815247    |       0.454545  |
| id_tl  | qwen3_8b   | plain         | full          | bare       | mean            | semantic |  33 |  1.27107     |  0.821547    |  1.71857     |       0.878788  |
| id_tl  | qwen3_8b   | plain         | full          | bare       | sum             | semantic |  33 |  1.83813     |  1.13209     |  2.67771     |       0.909091  |
| id_tl  | qwen3_8b   | plain         | full          | definition | mean            | semantic |  33 |  0.893747    |  0.649706    |  1.12961     |       0.909091  |
| id_tl  | qwen3_8b   | plain         | full          | definition | sum             | semantic |  33 |  4.05103     |  3.08738     |  5.00211     |       0.909091  |
| id_tl  | qwen3_8b   | plain         | full          | refers     | mean            | semantic |  33 |  0.98305     |  0.633186    |  1.31219     |       0.939394  |
| id_tl  | qwen3_8b   | plain         | full          | refers     | sum             | semantic |  33 |  5.75662     |  4.42081     |  7.12625     |       0.969697  |
| id_tl  | qwen3_8b   | plain         | language_only | bare       | mean            | semantic |  33 | -0.0008105   | -0.0190161   |  0.0175143   |       0.30303   |
| id_tl  | qwen3_8b   | plain         | language_only | bare       | sum             | semantic |  33 |  0.00359261  | -0.0202357   |  0.0266865   |       0.333333  |
| id_tl  | qwen3_8b   | plain         | language_only | definition | mean            | semantic |  33 |  9.28243e-05 | -0.0027209   |  0.00318185  |       0.242424  |
| id_tl  | qwen3_8b   | plain         | language_only | definition | sum             | semantic |  33 |  0.002222    | -0.0122951   |  0.0192854   |       0.242424  |
| id_tl  | qwen3_8b   | plain         | language_only | refers     | mean            | semantic |  33 |  0           |  0           |  0           |       0         |
| id_tl  | qwen3_8b   | plain         | language_only | refers     | sum             | semantic |  33 |  0           |  0           |  0           |       0         |
| id_tl  | qwen3_8b   | plain         | masked        | bare       | mean            | semantic |  33 |  3.40232     |  2.36181     |  4.54146     |       0.939394  |
| id_tl  | qwen3_8b   | plain         | masked        | bare       | sum             | semantic |  33 |  3.91587     |  2.6712      |  5.25426     |       0.909091  |
| id_tl  | qwen3_8b   | plain         | masked        | definition | mean            | semantic |  33 |  1.01041     |  0.810235    |  1.23818     |       0.939394  |
| id_tl  | qwen3_8b   | plain         | masked        | definition | sum             | semantic |  33 |  4.44929     |  3.52542     |  5.43162     |       0.939394  |
| id_tl  | qwen3_8b   | plain         | masked        | refers     | mean            | semantic |  33 |  1.06872     |  0.77526     |  1.3655      |       0.939394  |
| id_tl  | qwen3_8b   | plain         | masked        | refers     | sum             | semantic |  33 |  5.96508     |  4.6683      |  7.28369     |       0.969697  |
| id_tl  | qwen3_8b   | plain         | shuffled      | bare       | mean            | semantic |  33 | -0.18133     | -0.7463      |  0.375841    |       0.545455  |
| id_tl  | qwen3_8b   | plain         | shuffled      | bare       | sum             | semantic |  33 | -0.518215    | -1.32309     |  0.217281    |       0.515152  |
| id_tl  | qwen3_8b   | plain         | shuffled      | definition | mean            | semantic |  33 | -0.0343291   | -0.195444    |  0.115887    |       0.484848  |
| id_tl  | qwen3_8b   | plain         | shuffled      | definition | sum             | semantic |  33 | -0.1985      | -0.966878    |  0.475827    |       0.515152  |
| id_tl  | qwen3_8b   | plain         | shuffled      | refers     | mean            | semantic |  33 |  0.0196762   | -0.211757    |  0.228622    |       0.575758  |
| id_tl  | qwen3_8b   | plain         | shuffled      | refers     | sum             | semantic |  33 |  0.054293    | -1.077       |  1.07733     |       0.575758  |
| zh_ja  | gemma3_12b | chat          | full          | bare       | mean            | semantic |  27 |  3.45052     |  1.29619     |  5.98967     |       0.740741  |
| zh_ja  | gemma3_12b | chat          | full          | bare       | sum             | semantic |  27 | 10.6732      |  5.06843     | 17.4345      |       0.777778  |
| zh_ja  | gemma3_12b | chat          | full          | definition | mean            | semantic |  27 |  3.18094     |  2.28946     |  4.05648     |       0.962963  |
| zh_ja  | gemma3_12b | chat          | full          | definition | sum             | semantic |  27 | 16.2105      | 11.4266      | 21.4025      |       0.962963  |
| zh_ja  | gemma3_12b | chat          | full          | refers     | mean            | semantic |  27 |  3.09952     |  2.47956     |  3.74915     |       1         |
| zh_ja  | gemma3_12b | chat          | full          | refers     | sum             | semantic |  27 | 19.0734      | 15.2814      | 23.307       |       1         |
| zh_ja  | gemma3_12b | chat          | language_only | bare       | mean            | semantic |  27 |  0.00229226  | -0.0435495   |  0.0578528   |       0.296296  |
| zh_ja  | gemma3_12b | chat          | language_only | bare       | sum             | semantic |  27 | -0.004359    | -0.094368    |  0.0856416   |       0.333333  |
| zh_ja  | gemma3_12b | chat          | language_only | definition | mean            | semantic |  27 |  0.00549788  | -0.00892697  |  0.0201468   |       0.37037   |
| zh_ja  | gemma3_12b | chat          | language_only | definition | sum             | semantic |  27 |  0.0499635   | -0.0129508   |  0.115587    |       0.37037   |
| zh_ja  | gemma3_12b | chat          | language_only | refers     | mean            | semantic |  27 |  0           |  0           |  0           |       0         |
| zh_ja  | gemma3_12b | chat          | language_only | refers     | sum             | semantic |  27 |  0           |  0           |  0           |       0         |
| zh_ja  | gemma3_12b | chat          | masked        | bare       | mean            | semantic |  27 |  6.03799     |  4.12261     |  8.14735     |       0.888889  |
| zh_ja  | gemma3_12b | chat          | masked        | bare       | sum             | semantic |  27 | 14.1847      |  8.83564     | 19.8264      |       0.888889  |
| zh_ja  | gemma3_12b | chat          | masked        | definition | mean            | semantic |  27 |  3.30605     |  2.51149     |  4.11372     |       0.962963  |
| zh_ja  | gemma3_12b | chat          | masked        | definition | sum             | semantic |  27 | 16.9072      | 12.5347      | 21.0936      |       0.925926  |
| zh_ja  | gemma3_12b | chat          | masked        | refers     | mean            | semantic |  27 |  3.33637     |  2.73395     |  3.98749     |       1         |
| zh_ja  | gemma3_12b | chat          | masked        | refers     | sum             | semantic |  27 | 19.9433      | 16.0558      | 23.8109      |       1         |
| zh_ja  | gemma3_12b | chat          | shuffled      | bare       | mean            | semantic |  27 | -1.45918     | -2.59904     | -0.339953    |       0.333333  |
| zh_ja  | gemma3_12b | chat          | shuffled      | bare       | sum             | semantic |  27 | -2.94512     | -4.99423     | -0.910875    |       0.296296  |
| zh_ja  | gemma3_12b | chat          | shuffled      | definition | mean            | semantic |  27 | -0.368928    | -0.740669    | -0.0348593   |       0.407407  |
| zh_ja  | gemma3_12b | chat          | shuffled      | definition | sum             | semantic |  27 | -1.68535     | -3.7411      |  0.18122     |       0.37037   |
| zh_ja  | gemma3_12b | chat          | shuffled      | refers     | mean            | semantic |  27 | -0.193178    | -0.569869    |  0.198002    |       0.333333  |
| zh_ja  | gemma3_12b | chat          | shuffled      | refers     | sum             | semantic |  27 | -0.984323    | -3.54014     |  1.5251      |       0.37037   |
| zh_ja  | gemma3_12b | plain         | full          | bare       | mean            | semantic |  27 |  0.564192    | -0.0895322   |  1.29622     |       0.592593  |
| zh_ja  | gemma3_12b | plain         | full          | bare       | sum             | semantic |  27 |  1.63471     |  0.127993    |  3.1687      |       0.62963   |
| zh_ja  | gemma3_12b | plain         | full          | definition | mean            | semantic |  27 |  0.291653    |  0.104393    |  0.506492    |       0.777778  |
| zh_ja  | gemma3_12b | plain         | full          | definition | sum             | semantic |  27 |  1.15116     |  0.29666     |  2.21866     |       0.703704  |
| zh_ja  | gemma3_12b | plain         | full          | refers     | mean            | semantic |  27 |  0.284751    |  0.072863    |  0.515303    |       0.703704  |
| zh_ja  | gemma3_12b | plain         | full          | refers     | sum             | semantic |  27 |  1.69091     |  0.274706    |  3.17255     |       0.62963   |
| zh_ja  | gemma3_12b | plain         | language_only | bare       | mean            | semantic |  27 | -0.0379026   | -0.0770628   |  0.00153256  |       0.148148  |
| zh_ja  | gemma3_12b | plain         | language_only | bare       | sum             | semantic |  27 | -0.00883367  | -0.136791    |  0.135941    |       0.296296  |
| zh_ja  | gemma3_12b | plain         | language_only | definition | mean            | semantic |  27 | -0.00149478  | -0.0162189   |  0.0130726   |       0.333333  |
| zh_ja  | gemma3_12b | plain         | language_only | definition | sum             | semantic |  27 |  0.0565065   | -0.066602    |  0.197886    |       0.296296  |
| zh_ja  | gemma3_12b | plain         | language_only | refers     | mean            | semantic |  27 |  0           |  0           |  0           |       0         |
| zh_ja  | gemma3_12b | plain         | language_only | refers     | sum             | semantic |  27 |  0           |  0           |  0           |       0         |
| zh_ja  | gemma3_12b | plain         | masked        | bare       | mean            | semantic |  27 |  0.6044      | -0.036711    |  1.30087     |       0.703704  |
| zh_ja  | gemma3_12b | plain         | masked        | bare       | sum             | semantic |  27 |  1.98657     |  0.796569    |  3.42135     |       0.740741  |
| zh_ja  | gemma3_12b | plain         | masked        | definition | mean            | semantic |  27 |  0.257937    |  0.0728069   |  0.442885    |       0.814815  |
| zh_ja  | gemma3_12b | plain         | masked        | definition | sum             | semantic |  27 |  1.61497     |  0.640554    |  2.68372     |       0.777778  |
| zh_ja  | gemma3_12b | plain         | masked        | refers     | mean            | semantic |  27 |  0.333651    |  0.0674772   |  0.634953    |       0.777778  |
| zh_ja  | gemma3_12b | plain         | masked        | refers     | sum             | semantic |  27 |  2.53816     |  0.971156    |  4.40651     |       0.777778  |
| zh_ja  | gemma3_12b | plain         | shuffled      | bare       | mean            | semantic |  27 | -0.073402    | -0.439528    |  0.30837     |       0.37037   |
| zh_ja  | gemma3_12b | plain         | shuffled      | bare       | sum             | semantic |  27 |  0.123217    | -0.959323    |  1.31984     |       0.444444  |
| zh_ja  | gemma3_12b | plain         | shuffled      | definition | mean            | semantic |  27 | -0.0147366   | -0.153513    |  0.127754    |       0.407407  |
| zh_ja  | gemma3_12b | plain         | shuffled      | definition | sum             | semantic |  27 |  0.128866    | -0.660063    |  0.939991    |       0.407407  |
| zh_ja  | gemma3_12b | plain         | shuffled      | refers     | mean            | semantic |  27 |  0.0246756   | -0.190039    |  0.270884    |       0.481481  |
| zh_ja  | gemma3_12b | plain         | shuffled      | refers     | sum             | semantic |  27 |  0.197074    | -1.25873     |  1.70973     |       0.555556  |
| zh_ja  | gemma3_4b  | chat          | full          | bare       | mean            | semantic |  27 |  5.8486      |  3.16256     |  8.61195     |       0.814815  |
| zh_ja  | gemma3_4b  | chat          | full          | bare       | sum             | semantic |  27 | 16.0653      |  7.91183     | 24.3407      |       0.925926  |
| zh_ja  | gemma3_4b  | chat          | full          | definition | mean            | semantic |  27 |  2.78528     |  1.93597     |  3.64474     |       0.925926  |
| zh_ja  | gemma3_4b  | chat          | full          | definition | sum             | semantic |  27 | 13.2116      |  8.2715      | 18.5892      |       0.925926  |
| zh_ja  | gemma3_4b  | chat          | full          | refers     | mean            | semantic |  27 |  2.69821     |  1.95775     |  3.47553     |       0.925926  |
| zh_ja  | gemma3_4b  | chat          | full          | refers     | sum             | semantic |  27 | 16.5019      | 11.0999      | 21.8339      |       0.925926  |
| zh_ja  | gemma3_4b  | chat          | language_only | bare       | mean            | semantic |  27 |  0.0125822   | -0.0422879   |  0.0797133   |       0.222222  |
| zh_ja  | gemma3_4b  | chat          | language_only | bare       | sum             | semantic |  27 |  0.0129294   | -0.0758269   |  0.108571    |       0.148148  |
| zh_ja  | gemma3_4b  | chat          | language_only | definition | mean            | semantic |  27 | -0.000109143 | -0.0121182   |  0.0141706   |       0.222222  |
| zh_ja  | gemma3_4b  | chat          | language_only | definition | sum             | semantic |  27 | -0.00877204  | -0.0655596   |  0.0489374   |       0.222222  |
| zh_ja  | gemma3_4b  | chat          | language_only | refers     | mean            | semantic |  27 |  0           |  0           |  0           |       0         |
| zh_ja  | gemma3_4b  | chat          | language_only | refers     | sum             | semantic |  27 |  0           |  0           |  0           |       0         |
| zh_ja  | gemma3_4b  | chat          | masked        | bare       | mean            | semantic |  27 |  8.39904     |  5.65333     | 11.1449      |       0.888889  |
| zh_ja  | gemma3_4b  | chat          | masked        | bare       | sum             | semantic |  27 | 17.9476      | 11.2184      | 24.5623      |       0.925926  |
| zh_ja  | gemma3_4b  | chat          | masked        | definition | mean            | semantic |  27 |  2.66626     |  1.75434     |  3.52907     |       0.888889  |
| zh_ja  | gemma3_4b  | chat          | masked        | definition | sum             | semantic |  27 | 13.5375      |  8.71973     | 18.4645      |       0.814815  |
| zh_ja  | gemma3_4b  | chat          | masked        | refers     | mean            | semantic |  27 |  3.34431     |  2.49886     |  4.21412     |       0.962963  |
| zh_ja  | gemma3_4b  | chat          | masked        | refers     | sum             | semantic |  27 | 20.4404      | 15.7648      | 25.1673      |       0.962963  |
| zh_ja  | gemma3_4b  | chat          | shuffled      | bare       | mean            | semantic |  27 |  0.425069    | -1.45296     |  2.27047     |       0.518519  |
| zh_ja  | gemma3_4b  | chat          | shuffled      | bare       | sum             | semantic |  27 | -2.03007     | -7.21558     |  2.49397     |       0.518519  |
| zh_ja  | gemma3_4b  | chat          | shuffled      | definition | mean            | semantic |  27 | -0.276448    | -0.664262    |  0.141591    |       0.37037   |
| zh_ja  | gemma3_4b  | chat          | shuffled      | definition | sum             | semantic |  27 | -1.50609     | -3.23663     |  0.261063    |       0.407407  |
| zh_ja  | gemma3_4b  | chat          | shuffled      | refers     | mean            | semantic |  27 | -0.130426    | -0.585298    |  0.31984     |       0.481481  |
| zh_ja  | gemma3_4b  | chat          | shuffled      | refers     | sum             | semantic |  27 | -0.990444    | -3.90708     |  1.81894     |       0.481481  |
| zh_ja  | gemma3_4b  | plain         | full          | bare       | mean            | semantic |  27 |  1.42558     |  0.73728     |  2.09007     |       0.814815  |
| zh_ja  | gemma3_4b  | plain         | full          | bare       | sum             | semantic |  27 |  3.64177     |  1.63679     |  6.05698     |       0.740741  |
| zh_ja  | gemma3_4b  | plain         | full          | definition | mean            | semantic |  27 |  0.50107     |  0.180567    |  0.819918    |       0.777778  |
| zh_ja  | gemma3_4b  | plain         | full          | definition | sum             | semantic |  27 |  3.24752     |  1.35391     |  5.11689     |       0.777778  |
| zh_ja  | gemma3_4b  | plain         | full          | refers     | mean            | semantic |  27 |  0.619805    |  0.365065    |  0.89622     |       0.777778  |
| zh_ja  | gemma3_4b  | plain         | full          | refers     | sum             | semantic |  27 |  4.47189     |  2.48885     |  6.8326      |       0.777778  |
| zh_ja  | gemma3_4b  | plain         | language_only | bare       | mean            | semantic |  27 | -0.00497766  | -0.0544144   |  0.0334383   |       0.444444  |
| zh_ja  | gemma3_4b  | plain         | language_only | bare       | sum             | semantic |  27 | -0.00911399  | -0.107831    |  0.0595423   |       0.444444  |
| zh_ja  | gemma3_4b  | plain         | language_only | definition | mean            | semantic |  27 |  0.00357619  | -0.0062419   |  0.0120936   |       0.555556  |
| zh_ja  | gemma3_4b  | plain         | language_only | definition | sum             | semantic |  27 |  0.0137316   | -0.03721     |  0.0588733   |       0.518519  |
| zh_ja  | gemma3_4b  | plain         | language_only | refers     | mean            | semantic |  27 |  0           |  0           |  0           |       0         |
| zh_ja  | gemma3_4b  | plain         | language_only | refers     | sum             | semantic |  27 |  0           |  0           |  0           |       0         |
| zh_ja  | gemma3_4b  | plain         | masked        | bare       | mean            | semantic |  27 |  1.64815     |  0.991295    |  2.27961     |       0.851852  |
| zh_ja  | gemma3_4b  | plain         | masked        | bare       | sum             | semantic |  27 |  2.97111     |  1.66951     |  4.33303     |       0.814815  |
| zh_ja  | gemma3_4b  | plain         | masked        | definition | mean            | semantic |  27 |  0.505191    |  0.262941    |  0.754057    |       0.777778  |
| zh_ja  | gemma3_4b  | plain         | masked        | definition | sum             | semantic |  27 |  2.88011     |  1.59372     |  4.22736     |       0.740741  |
| zh_ja  | gemma3_4b  | plain         | masked        | refers     | mean            | semantic |  27 |  0.524632    |  0.330478    |  0.716596    |       0.814815  |
| zh_ja  | gemma3_4b  | plain         | masked        | refers     | sum             | semantic |  27 |  3.30076     |  2.02978     |  4.56422     |       0.814815  |
| zh_ja  | gemma3_4b  | plain         | shuffled      | bare       | mean            | semantic |  27 | -0.107575    | -0.647286    |  0.432675    |       0.518519  |
| zh_ja  | gemma3_4b  | plain         | shuffled      | bare       | sum             | semantic |  27 |  0.106119    | -1.04135     |  1.40494     |       0.407407  |
| zh_ja  | gemma3_4b  | plain         | shuffled      | definition | mean            | semantic |  27 | -0.0559953   | -0.210069    |  0.111758    |       0.407407  |
| zh_ja  | gemma3_4b  | plain         | shuffled      | definition | sum             | semantic |  27 | -0.219606    | -1.10766     |  0.722632    |       0.444444  |
| zh_ja  | gemma3_4b  | plain         | shuffled      | refers     | mean            | semantic |  27 | -0.158651    | -0.332863    |  0.0243152   |       0.407407  |
| zh_ja  | gemma3_4b  | plain         | shuffled      | refers     | sum             | semantic |  27 | -0.773286    | -1.87093     |  0.326478    |       0.407407  |
| zh_ja  | qwen25_7b  | chat          | full          | bare       | mean            | semantic |  27 |  2.17055     |  1.45586     |  2.87122     |       0.851852  |
| zh_ja  | qwen25_7b  | chat          | full          | bare       | sum             | semantic |  27 |  7.43434     |  5.02713     |  9.96185     |       0.814815  |
| zh_ja  | qwen25_7b  | chat          | full          | definition | mean            | semantic |  27 |  1.23643     |  0.920562    |  1.5672      |       0.962963  |
| zh_ja  | qwen25_7b  | chat          | full          | definition | sum             | semantic |  27 |  7.35443     |  5.16094     |  9.75462     |       0.962963  |
| zh_ja  | qwen25_7b  | chat          | full          | refers     | mean            | semantic |  27 |  2.02327     |  1.62746     |  2.42284     |       1         |
| zh_ja  | qwen25_7b  | chat          | full          | refers     | sum             | semantic |  27 | 13.3182      | 10.7073      | 15.9465      |       1         |
| zh_ja  | qwen25_7b  | chat          | language_only | bare       | mean            | semantic |  27 | -0.00269318  | -0.00888349  |  0.00126185  |       0.037037  |
| zh_ja  | qwen25_7b  | chat          | language_only | bare       | sum             | semantic |  27 |  0.00556886  | -0.00461939  |  0.0188965   |       0.0740741 |
| zh_ja  | qwen25_7b  | chat          | language_only | definition | mean            | semantic |  27 | -0.00077592  | -0.00250046  |  0.00039694  |       0.037037  |
| zh_ja  | qwen25_7b  | chat          | language_only | definition | sum             | semantic |  27 | -0.00240983  | -0.0185531   |  0.0104317   |       0.0740741 |
| zh_ja  | qwen25_7b  | chat          | language_only | refers     | mean            | semantic |  27 |  0           |  0           |  0           |       0         |
| zh_ja  | qwen25_7b  | chat          | language_only | refers     | sum             | semantic |  27 |  0           |  0           |  0           |       0         |
| zh_ja  | qwen25_7b  | chat          | masked        | bare       | mean            | semantic |  27 |  4.55984     |  3.29045     |  5.92096     |       0.925926  |
| zh_ja  | qwen25_7b  | chat          | masked        | bare       | sum             | semantic |  27 | 12.3938      |  8.91498     | 16.0572      |       1         |
| zh_ja  | qwen25_7b  | chat          | masked        | definition | mean            | semantic |  27 |  2.05342     |  1.62742     |  2.51533     |       1         |
| zh_ja  | qwen25_7b  | chat          | masked        | definition | sum             | semantic |  27 | 12.5367      |  9.45323     | 16.0719      |       1         |
| zh_ja  | qwen25_7b  | chat          | masked        | refers     | mean            | semantic |  27 |  2.54866     |  2.09723     |  3.01518     |       1         |
| zh_ja  | qwen25_7b  | chat          | masked        | refers     | sum             | semantic |  27 | 17.0295      | 13.7177      | 20.5364      |       1         |
| zh_ja  | qwen25_7b  | chat          | shuffled      | bare       | mean            | semantic |  27 | -0.590957    | -1.65904     |  0.432499    |       0.444444  |
| zh_ja  | qwen25_7b  | chat          | shuffled      | bare       | sum             | semantic |  27 | -1.13254     | -4.21607     |  1.7673      |       0.481481  |
| zh_ja  | qwen25_7b  | chat          | shuffled      | definition | mean            | semantic |  27 |  0.159507    | -0.212133    |  0.544238    |       0.518519  |
| zh_ja  | qwen25_7b  | chat          | shuffled      | definition | sum             | semantic |  27 |  0.556102    | -1.19107     |  2.33475     |       0.518519  |
| zh_ja  | qwen25_7b  | chat          | shuffled      | refers     | mean            | semantic |  27 |  0.0231574   | -0.43383     |  0.475437    |       0.518519  |
| zh_ja  | qwen25_7b  | chat          | shuffled      | refers     | sum             | semantic |  27 |  0.224023    | -2.8326      |  3.19056     |       0.518519  |
| zh_ja  | qwen25_7b  | plain         | full          | bare       | mean            | semantic |  27 |  2.54725     |  1.67628     |  3.37332     |       0.888889  |
| zh_ja  | qwen25_7b  | plain         | full          | bare       | sum             | semantic |  27 |  6.00576     |  4.10174     |  8.03294     |       0.925926  |
| zh_ja  | qwen25_7b  | plain         | full          | definition | mean            | semantic |  27 |  1.20052     |  0.911791    |  1.49254     |       0.962963  |
| zh_ja  | qwen25_7b  | plain         | full          | definition | sum             | semantic |  27 |  7.07715     |  5.33155     |  8.8918      |       0.962963  |
| zh_ja  | qwen25_7b  | plain         | full          | refers     | mean            | semantic |  27 |  1.31165     |  1.01605     |  1.6148      |       0.962963  |
| zh_ja  | qwen25_7b  | plain         | full          | refers     | sum             | semantic |  27 |  8.7893      |  6.61269     | 11.053       |       0.962963  |
| zh_ja  | qwen25_7b  | plain         | language_only | bare       | mean            | semantic |  27 |  0.0062384   | -0.00581811  |  0.0189266   |       0.222222  |
| zh_ja  | qwen25_7b  | plain         | language_only | bare       | sum             | semantic |  27 |  0.031763    | -0.00777501  |  0.0772077   |       0.222222  |
| zh_ja  | qwen25_7b  | plain         | language_only | definition | mean            | semantic |  27 | -0.00152791  | -0.00574615  |  0.00229247  |       0.185185  |
| zh_ja  | qwen25_7b  | plain         | language_only | definition | sum             | semantic |  27 |  0.00558511  | -0.0375571   |  0.0505593   |       0.185185  |
| zh_ja  | qwen25_7b  | plain         | language_only | refers     | mean            | semantic |  27 |  0           |  0           |  0           |       0         |
| zh_ja  | qwen25_7b  | plain         | language_only | refers     | sum             | semantic |  27 |  0           |  0           |  0           |       0         |
| zh_ja  | qwen25_7b  | plain         | masked        | bare       | mean            | semantic |  27 |  5.29201     |  3.85954     |  6.71517     |       0.888889  |
| zh_ja  | qwen25_7b  | plain         | masked        | bare       | sum             | semantic |  27 | 12.4907      |  9.14844     | 16.0571      |       0.925926  |
| zh_ja  | qwen25_7b  | plain         | masked        | definition | mean            | semantic |  27 |  2.0612      |  1.63467     |  2.48812     |       1         |
| zh_ja  | qwen25_7b  | plain         | masked        | definition | sum             | semantic |  27 | 12.3725      |  9.66376     | 15.4437      |       1         |
| zh_ja  | qwen25_7b  | plain         | masked        | refers     | mean            | semantic |  27 |  2.22905     |  1.86452     |  2.61055     |       1         |
| zh_ja  | qwen25_7b  | plain         | masked        | refers     | sum             | semantic |  27 | 15.0603      | 12.3485      | 17.8863      |       1         |
| zh_ja  | qwen25_7b  | plain         | shuffled      | bare       | mean            | semantic |  27 |  0.115475    | -1.06143     |  1.51006     |       0.407407  |
| zh_ja  | qwen25_7b  | plain         | shuffled      | bare       | sum             | semantic |  27 | -0.118793    | -2.12478     |  1.94674     |       0.407407  |
| zh_ja  | qwen25_7b  | plain         | shuffled      | definition | mean            | semantic |  27 |  0.131236    | -0.282652    |  0.582834    |       0.666667  |
| zh_ja  | qwen25_7b  | plain         | shuffled      | definition | sum             | semantic |  27 |  0.518268    | -1.38257     |  2.53563     |       0.555556  |
| zh_ja  | qwen25_7b  | plain         | shuffled      | refers     | mean            | semantic |  27 |  0.039013    | -0.29996     |  0.384745    |       0.481481  |
| zh_ja  | qwen25_7b  | plain         | shuffled      | refers     | sum             | semantic |  27 |  0.328491    | -1.89751     |  2.5559      |       0.444444  |
| zh_ja  | qwen3_8b   | chat          | full          | bare       | mean            | semantic |  27 |  0.929611    |  0.280105    |  1.59475     |       0.666667  |
| zh_ja  | qwen3_8b   | chat          | full          | bare       | sum             | semantic |  27 |  3.52408     |  1.52838     |  5.64976     |       0.666667  |
| zh_ja  | qwen3_8b   | chat          | full          | definition | mean            | semantic |  27 |  0.997169    |  0.773851    |  1.24135     |       0.962963  |
| zh_ja  | qwen3_8b   | chat          | full          | definition | sum             | semantic |  27 |  5.61786     |  4.34532     |  6.9582      |       1         |
| zh_ja  | qwen3_8b   | chat          | full          | refers     | mean            | semantic |  27 |  1.13436     |  0.9061      |  1.36286     |       1         |
| zh_ja  | qwen3_8b   | chat          | full          | refers     | sum             | semantic |  27 |  7.52524     |  5.95954     |  9.16926     |       1         |
| zh_ja  | qwen3_8b   | chat          | language_only | bare       | mean            | semantic |  27 | -0.0170868   | -0.0523548   |  0.0164949   |       0.259259  |
| zh_ja  | qwen3_8b   | chat          | language_only | bare       | sum             | semantic |  27 | -0.000849053 | -0.0598988   |  0.0584896   |       0.407407  |
| zh_ja  | qwen3_8b   | chat          | language_only | definition | mean            | semantic |  27 | -0.00744159  | -0.0133526   | -0.00163834  |       0.222222  |
| zh_ja  | qwen3_8b   | chat          | language_only | definition | sum             | semantic |  27 | -0.0279467   | -0.0611682   | -0.000510184 |       0.222222  |
| zh_ja  | qwen3_8b   | chat          | language_only | refers     | mean            | semantic |  27 |  0           |  0           |  0           |       0         |
| zh_ja  | qwen3_8b   | chat          | language_only | refers     | sum             | semantic |  27 |  0           |  0           |  0           |       0         |
| zh_ja  | qwen3_8b   | chat          | masked        | bare       | mean            | semantic |  27 |  3.11772     |  1.91381     |  4.37797     |       0.814815  |
| zh_ja  | qwen3_8b   | chat          | masked        | bare       | sum             | semantic |  27 |  9.0216      |  5.95221     | 12.1503      |       0.888889  |
| zh_ja  | qwen3_8b   | chat          | masked        | definition | mean            | semantic |  27 |  1.24177     |  0.917881    |  1.585       |       0.962963  |
| zh_ja  | qwen3_8b   | chat          | masked        | definition | sum             | semantic |  27 |  7.22267     |  5.36672     |  9.1565      |       0.962963  |
| zh_ja  | qwen3_8b   | chat          | masked        | refers     | mean            | semantic |  27 |  1.4208      |  1.10241     |  1.75734     |       0.925926  |
| zh_ja  | qwen3_8b   | chat          | masked        | refers     | sum             | semantic |  27 |  9.52134     |  7.23898     | 11.7857      |       0.925926  |
| zh_ja  | qwen3_8b   | chat          | shuffled      | bare       | mean            | semantic |  27 |  0.157902    | -0.32634     |  0.648624    |       0.555556  |
| zh_ja  | qwen3_8b   | chat          | shuffled      | bare       | sum             | semantic |  27 |  0.503175    | -0.711994    |  1.83743     |       0.481481  |
| zh_ja  | qwen3_8b   | chat          | shuffled      | definition | mean            | semantic |  27 |  0.0141683   | -0.0933433   |  0.115674    |       0.62963   |
| zh_ja  | qwen3_8b   | chat          | shuffled      | definition | sum             | semantic |  27 |  0.109201    | -0.405134    |  0.601621    |       0.592593  |
| zh_ja  | qwen3_8b   | chat          | shuffled      | refers     | mean            | semantic |  27 |  0.00156163  | -0.109191    |  0.108408    |       0.555556  |
| zh_ja  | qwen3_8b   | chat          | shuffled      | refers     | sum             | semantic |  27 |  0.103051    | -0.550899    |  0.735634    |       0.62963   |
| zh_ja  | qwen3_8b   | plain         | full          | bare       | mean            | semantic |  27 |  1.93996     |  1.3698      |  2.5672      |       0.925926  |
| zh_ja  | qwen3_8b   | plain         | full          | bare       | sum             | semantic |  27 |  5.20983     |  3.4155      |  7.14557     |       0.962963  |
| zh_ja  | qwen3_8b   | plain         | full          | definition | mean            | semantic |  27 |  1.217       |  0.978559    |  1.46343     |       1         |
| zh_ja  | qwen3_8b   | plain         | full          | definition | sum             | semantic |  27 |  6.83549     |  5.33944     |  8.41552     |       1         |
| zh_ja  | qwen3_8b   | plain         | full          | refers     | mean            | semantic |  27 |  1.59117     |  1.27812     |  1.91971     |       1         |
| zh_ja  | qwen3_8b   | plain         | full          | refers     | sum             | semantic |  27 | 10.3256      |  8.324       | 12.3427      |       1         |
| zh_ja  | qwen3_8b   | plain         | language_only | bare       | mean            | semantic |  27 | -0.0038689   | -0.0178128   |  0.0073881   |       0.296296  |
| zh_ja  | qwen3_8b   | plain         | language_only | bare       | sum             | semantic |  27 | -0.0141382   | -0.0317786   |  0.00108118  |       0.296296  |
| zh_ja  | qwen3_8b   | plain         | language_only | definition | mean            | semantic |  27 | -0.00219752  | -0.00671801  |  0.00191261  |       0.259259  |
| zh_ja  | qwen3_8b   | plain         | language_only | definition | sum             | semantic |  27 | -0.0105754   | -0.0302579   |  0.00766686  |       0.296296  |
| zh_ja  | qwen3_8b   | plain         | language_only | refers     | mean            | semantic |  27 |  0           |  0           |  0           |       0         |
| zh_ja  | qwen3_8b   | plain         | language_only | refers     | sum             | semantic |  27 |  0           |  0           |  0           |       0         |
| zh_ja  | qwen3_8b   | plain         | masked        | bare       | mean            | semantic |  27 |  5.09825     |  3.81307     |  6.39687     |       0.962963  |
| zh_ja  | qwen3_8b   | plain         | masked        | bare       | sum             | semantic |  27 | 10.5095      |  7.99458     | 12.977       |       0.925926  |
| zh_ja  | qwen3_8b   | plain         | masked        | definition | mean            | semantic |  27 |  1.67525     |  1.26805     |  2.09569     |       0.962963  |
| zh_ja  | qwen3_8b   | plain         | masked        | definition | sum             | semantic |  27 |  9.17743     |  6.90923     | 11.5396      |       0.962963  |
| zh_ja  | qwen3_8b   | plain         | masked        | refers     | mean            | semantic |  27 |  1.66355     |  1.30745     |  2.0284      |       0.925926  |
| zh_ja  | qwen3_8b   | plain         | masked        | refers     | sum             | semantic |  27 | 11.1053      |  8.76882     | 13.4261      |       0.925926  |
| zh_ja  | qwen3_8b   | plain         | shuffled      | bare       | mean            | semantic |  27 |  0.0352791   | -0.577918    |  0.688851    |       0.481481  |
| zh_ja  | qwen3_8b   | plain         | shuffled      | bare       | sum             | semantic |  27 | -0.0402856   | -1.27051     |  1.10875     |       0.518519  |
| zh_ja  | qwen3_8b   | plain         | shuffled      | definition | mean            | semantic |  27 |  0.00188761  | -0.134333    |  0.13749     |       0.518519  |
| zh_ja  | qwen3_8b   | plain         | shuffled      | definition | sum             | semantic |  27 | -0.245861    | -1.01729     |  0.475739    |       0.518519  |
| zh_ja  | qwen3_8b   | plain         | shuffled      | refers     | mean            | semantic |  27 | -0.0119335   | -0.174934    |  0.153837    |       0.407407  |
| zh_ja  | qwen3_8b   | plain         | shuffled      | refers     | sum             | semantic |  27 |  0.0255121   | -0.918489    |  1.05157     |       0.444444  |

## Paired construct contrasts

| pair   | model      | prompt_mode   | wrapper    | normalization   | contrast                 |   n |    estimate |       ci_low |   ci_high |   positive_rate |
|:-------|:-----------|:--------------|:-----------|:----------------|:-------------------------|----:|------------:|-------------:|----------:|----------------:|
| id_tl  | gemma3_12b | chat          | bare       | mean            | full_minus_shuffled      |  33 |  4.29459    |  2.49086     |  6.22094  |        0.727273 |
| id_tl  | gemma3_12b | chat          | bare       | mean            | full_minus_language_only |  33 |  4.17613    |  2.66746     |  5.72287  |        0.878788 |
| id_tl  | gemma3_12b | chat          | bare       | mean            | masked_minus_shuffled    |  33 |  3.44297    |  1.72703     |  5.19756  |        0.69697  |
| id_tl  | gemma3_12b | chat          | bare       | sum             | full_minus_shuffled      |  33 |  5.95618    |  3.03666     |  9.2741   |        0.666667 |
| id_tl  | gemma3_12b | chat          | bare       | sum             | full_minus_language_only |  33 |  5.31618    |  3.0116      |  7.71587  |        0.878788 |
| id_tl  | gemma3_12b | chat          | bare       | sum             | masked_minus_shuffled    |  33 |  5.39088    |  2.94946     |  8.03793  |        0.69697  |
| id_tl  | gemma3_12b | chat          | definition | mean            | full_minus_shuffled      |  33 |  3.42618    |  2.65685     |  4.20774  |        0.939394 |
| id_tl  | gemma3_12b | chat          | definition | mean            | full_minus_language_only |  33 |  3.16661    |  2.43389     |  3.869    |        0.969697 |
| id_tl  | gemma3_12b | chat          | definition | mean            | masked_minus_shuffled    |  33 |  3.09065    |  2.42957     |  3.76433  |        0.939394 |
| id_tl  | gemma3_12b | chat          | definition | sum             | full_minus_shuffled      |  33 | 14.5478     | 11.1394      | 18.27     |        0.878788 |
| id_tl  | gemma3_12b | chat          | definition | sum             | full_minus_language_only |  33 | 13.032      |  9.97612     | 15.9992   |        0.939394 |
| id_tl  | gemma3_12b | chat          | definition | sum             | masked_minus_shuffled    |  33 | 13.2106     | 10.4292      | 15.9981   |        0.939394 |
| id_tl  | gemma3_12b | chat          | refers     | mean            | full_minus_shuffled      |  33 |  2.62944    |  1.93395     |  3.3914   |        0.939394 |
| id_tl  | gemma3_12b | chat          | refers     | mean            | full_minus_language_only |  33 |  2.67581    |  2.0762      |  3.27443  |        0.969697 |
| id_tl  | gemma3_12b | chat          | refers     | mean            | masked_minus_shuffled    |  33 |  2.65504    |  1.98136     |  3.37945  |        0.969697 |
| id_tl  | gemma3_12b | chat          | refers     | sum             | full_minus_shuffled      |  33 | 14.2131     | 10.764       | 18.0491   |        0.969697 |
| id_tl  | gemma3_12b | chat          | refers     | sum             | full_minus_language_only |  33 | 13.9796     | 11.0773      | 16.9925   |        0.969697 |
| id_tl  | gemma3_12b | chat          | refers     | sum             | masked_minus_shuffled    |  33 | 13.9392     | 10.6085      | 17.6224   |        0.939394 |
| id_tl  | gemma3_12b | plain         | bare       | mean            | full_minus_shuffled      |  33 | -0.215128   | -0.81839     |  0.380395 |        0.545455 |
| id_tl  | gemma3_12b | plain         | bare       | mean            | full_minus_language_only |  33 |  0.136811   | -0.18247     |  0.473326 |        0.515152 |
| id_tl  | gemma3_12b | plain         | bare       | mean            | masked_minus_shuffled    |  33 | -0.226851   | -0.739111    |  0.336293 |        0.363636 |
| id_tl  | gemma3_12b | plain         | bare       | sum             | full_minus_shuffled      |  33 |  0.92525    | -0.466763    |  2.90291  |        0.515152 |
| id_tl  | gemma3_12b | plain         | bare       | sum             | full_minus_language_only |  33 |  0.751325   | -0.22036     |  2.09438  |        0.545455 |
| id_tl  | gemma3_12b | plain         | bare       | sum             | masked_minus_shuffled    |  33 |  0.757145   | -0.465335    |  2.45619  |        0.424242 |
| id_tl  | gemma3_12b | plain         | definition | mean            | full_minus_shuffled      |  33 |  0.00809764 | -0.177879    |  0.20074  |        0.515152 |
| id_tl  | gemma3_12b | plain         | definition | mean            | full_minus_language_only |  33 |  0.0570476  | -0.0712971   |  0.182152 |        0.606061 |
| id_tl  | gemma3_12b | plain         | definition | mean            | masked_minus_shuffled    |  33 | -0.00396791 | -0.190132    |  0.197464 |        0.515152 |
| id_tl  | gemma3_12b | plain         | definition | sum             | full_minus_shuffled      |  33 |  0.992094   | -0.297722    |  2.83069  |        0.606061 |
| id_tl  | gemma3_12b | plain         | definition | sum             | full_minus_language_only |  33 |  0.889483   |  0.0106758   |  2.13915  |        0.666667 |
| id_tl  | gemma3_12b | plain         | definition | sum             | masked_minus_shuffled    |  33 |  0.607948   | -0.624998    |  2.30966  |        0.545455 |
| id_tl  | gemma3_12b | plain         | refers     | mean            | full_minus_shuffled      |  33 |  0.0551948  | -0.117809    |  0.223106 |        0.515152 |
| id_tl  | gemma3_12b | plain         | refers     | mean            | full_minus_language_only |  33 |  0.195194   |  0.066471    |  0.3437   |        0.69697  |
| id_tl  | gemma3_12b | plain         | refers     | mean            | masked_minus_shuffled    |  33 | -0.0232372  | -0.169067    |  0.109775 |        0.515152 |
| id_tl  | gemma3_12b | plain         | refers     | sum             | full_minus_shuffled      |  33 |  1.3491     | -0.110939    |  3.1879   |        0.545455 |
| id_tl  | gemma3_12b | plain         | refers     | sum             | full_minus_language_only |  33 |  1.7003     |  0.542152    |  3.12858  |        0.727273 |
| id_tl  | gemma3_12b | plain         | refers     | sum             | masked_minus_shuffled    |  33 |  0.536791   | -0.658012    |  1.84041  |        0.545455 |
| id_tl  | gemma3_4b  | chat          | bare       | mean            | full_minus_shuffled      |  33 |  9.13784    |  5.86497     | 12.3267   |        0.939394 |
| id_tl  | gemma3_4b  | chat          | bare       | mean            | full_minus_language_only |  33 |  9.18201    |  7.04922     | 11.3761   |        0.909091 |
| id_tl  | gemma3_4b  | chat          | bare       | mean            | masked_minus_shuffled    |  33 |  4.01009    |  0.753812    |  7.58612  |        0.757576 |
| id_tl  | gemma3_4b  | chat          | bare       | sum             | full_minus_shuffled      |  33 | 11.7101     |  6.82629     | 17.1364   |        0.909091 |
| id_tl  | gemma3_4b  | chat          | bare       | sum             | full_minus_language_only |  33 | 10.5542     |  7.33815     | 14.1688   |        0.878788 |
| id_tl  | gemma3_4b  | chat          | bare       | sum             | masked_minus_shuffled    |  33 |  6.36333    |  1.41697     | 12.21     |        0.727273 |
| id_tl  | gemma3_4b  | chat          | definition | mean            | full_minus_shuffled      |  33 |  3.04544    |  2.4142      |  3.74292  |        0.939394 |
| id_tl  | gemma3_4b  | chat          | definition | mean            | full_minus_language_only |  33 |  2.72568    |  2.21774     |  3.22508  |        0.969697 |
| id_tl  | gemma3_4b  | chat          | definition | mean            | masked_minus_shuffled    |  33 |  2.13568    |  1.35253     |  3.07899  |        0.848485 |
| id_tl  | gemma3_4b  | chat          | definition | sum             | full_minus_shuffled      |  33 | 12.893      | 10.0254      | 16.1765   |        0.969697 |
| id_tl  | gemma3_4b  | chat          | definition | sum             | full_minus_language_only |  33 | 10.9974     |  8.79485     | 13.1634   |        0.969697 |
| id_tl  | gemma3_4b  | chat          | definition | sum             | masked_minus_shuffled    |  33 |  9.61134    |  6.14886     | 13.7459   |        0.878788 |
| id_tl  | gemma3_4b  | chat          | refers     | mean            | full_minus_shuffled      |  33 |  3.08266    |  2.31961     |  3.84643  |        0.969697 |
| id_tl  | gemma3_4b  | chat          | refers     | mean            | full_minus_language_only |  33 |  2.9438     |  2.19446     |  3.69246  |        0.848485 |
| id_tl  | gemma3_4b  | chat          | refers     | mean            | masked_minus_shuffled    |  33 |  2.97671    |  2.24228     |  3.76242  |        0.909091 |
| id_tl  | gemma3_4b  | chat          | refers     | sum             | full_minus_shuffled      |  33 | 16.1878     | 12.3062      | 20.1654   |        0.939394 |
| id_tl  | gemma3_4b  | chat          | refers     | sum             | full_minus_language_only |  33 | 14.8321     | 11.2266      | 18.5022   |        0.878788 |
| id_tl  | gemma3_4b  | chat          | refers     | sum             | masked_minus_shuffled    |  33 | 15.4946     | 11.5509      | 19.584    |        0.939394 |
| id_tl  | gemma3_4b  | plain         | bare       | mean            | full_minus_shuffled      |  33 |  1.09423    |  0.344985    |  1.83712  |        0.666667 |
| id_tl  | gemma3_4b  | plain         | bare       | mean            | full_minus_language_only |  33 |  0.79422    |  0.155539    |  1.44567  |        0.666667 |
| id_tl  | gemma3_4b  | plain         | bare       | mean            | masked_minus_shuffled    |  33 |  0.944214   |  0.246297    |  1.6346   |        0.636364 |
| id_tl  | gemma3_4b  | plain         | bare       | sum             | full_minus_shuffled      |  33 |  1.37353    |  0.320093    |  2.43141  |        0.636364 |
| id_tl  | gemma3_4b  | plain         | bare       | sum             | full_minus_language_only |  33 |  0.982997   |  0.197702    |  1.75436  |        0.636364 |
| id_tl  | gemma3_4b  | plain         | bare       | sum             | masked_minus_shuffled    |  33 |  1.1635     |  0.0779757   |  2.34023  |        0.575758 |
| id_tl  | gemma3_4b  | plain         | definition | mean            | full_minus_shuffled      |  33 |  0.301181   |  0.0807957   |  0.518085 |        0.636364 |
| id_tl  | gemma3_4b  | plain         | definition | mean            | full_minus_language_only |  33 |  0.240157   |  0.0718219   |  0.40443  |        0.636364 |
| id_tl  | gemma3_4b  | plain         | definition | mean            | masked_minus_shuffled    |  33 |  0.355373   |  0.184747    |  0.536874 |        0.757576 |
| id_tl  | gemma3_4b  | plain         | definition | sum             | full_minus_shuffled      |  33 |  1.25263    | -0.159924    |  2.56077  |        0.606061 |
| id_tl  | gemma3_4b  | plain         | definition | sum             | full_minus_language_only |  33 |  1.09305    |  0.158025    |  2.08084  |        0.575758 |
| id_tl  | gemma3_4b  | plain         | definition | sum             | masked_minus_shuffled    |  33 |  1.55135    |  0.432701    |  2.75443  |        0.757576 |
| id_tl  | gemma3_4b  | plain         | refers     | mean            | full_minus_shuffled      |  33 |  0.405141   |  0.180937    |  0.629225 |        0.757576 |
| id_tl  | gemma3_4b  | plain         | refers     | mean            | full_minus_language_only |  33 |  0.414716   |  0.213741    |  0.614619 |        0.787879 |
| id_tl  | gemma3_4b  | plain         | refers     | mean            | masked_minus_shuffled    |  33 |  0.32142    |  0.13075     |  0.516167 |        0.727273 |
| id_tl  | gemma3_4b  | plain         | refers     | sum             | full_minus_shuffled      |  33 |  2.00833    |  0.603096    |  3.40271  |        0.727273 |
| id_tl  | gemma3_4b  | plain         | refers     | sum             | full_minus_language_only |  33 |  2.07569    |  0.983621    |  3.14474  |        0.757576 |
| id_tl  | gemma3_4b  | plain         | refers     | sum             | masked_minus_shuffled    |  33 |  1.71962    |  0.374019    |  3.08058  |        0.727273 |
| id_tl  | qwen25_7b  | chat          | bare       | mean            | full_minus_shuffled      |  33 |  3.21804    |  1.92284     |  4.55222  |        0.818182 |
| id_tl  | qwen25_7b  | chat          | bare       | mean            | full_minus_language_only |  33 |  3.0965     |  2.19738     |  4.0408   |        0.878788 |
| id_tl  | qwen25_7b  | chat          | bare       | mean            | masked_minus_shuffled    |  33 |  3.31555    |  2.21479     |  4.49214  |        0.878788 |
| id_tl  | qwen25_7b  | chat          | bare       | sum             | full_minus_shuffled      |  33 |  4.8551     |  2.63842     |  7.12137  |        0.787879 |
| id_tl  | qwen25_7b  | chat          | bare       | sum             | full_minus_language_only |  33 |  4.58089    |  3.43962     |  5.78356  |        0.909091 |
| id_tl  | qwen25_7b  | chat          | bare       | sum             | masked_minus_shuffled    |  33 |  5.85234    |  3.51186     |  8.355    |        0.878788 |
| id_tl  | qwen25_7b  | chat          | definition | mean            | full_minus_shuffled      |  33 |  1.16097    |  0.761407    |  1.54777  |        0.818182 |
| id_tl  | qwen25_7b  | chat          | definition | mean            | full_minus_language_only |  33 |  0.939793   |  0.620831    |  1.26222  |        0.848485 |
| id_tl  | qwen25_7b  | chat          | definition | mean            | masked_minus_shuffled    |  33 |  1.10192    |  0.687822    |  1.51445  |        0.848485 |
| id_tl  | qwen25_7b  | chat          | definition | sum             | full_minus_shuffled      |  33 |  4.91319    |  3.05641     |  6.76759  |        0.818182 |
| id_tl  | qwen25_7b  | chat          | definition | sum             | full_minus_language_only |  33 |  3.96451    |  2.52812     |  5.36546  |        0.818182 |
| id_tl  | qwen25_7b  | chat          | definition | sum             | masked_minus_shuffled    |  33 |  4.5855     |  2.30043     |  6.7724   |        0.848485 |
| id_tl  | qwen25_7b  | chat          | refers     | mean            | full_minus_shuffled      |  33 |  1.96307    |  1.53179     |  2.40611  |        0.939394 |
| id_tl  | qwen25_7b  | chat          | refers     | mean            | full_minus_language_only |  33 |  1.74341    |  1.31181     |  2.15319  |        0.939394 |
| id_tl  | qwen25_7b  | chat          | refers     | mean            | masked_minus_shuffled    |  33 |  2.03084    |  1.5704      |  2.54829  |        0.969697 |
| id_tl  | qwen25_7b  | chat          | refers     | sum             | full_minus_shuffled      |  33 | 10.4778     |  8.2743      | 12.6363   |        0.939394 |
| id_tl  | qwen25_7b  | chat          | refers     | sum             | full_minus_language_only |  33 |  9.43804    |  7.36748     | 11.5844   |        0.939394 |
| id_tl  | qwen25_7b  | chat          | refers     | sum             | masked_minus_shuffled    |  33 | 10.2915     |  7.58089     | 13.1002   |        0.939394 |
| id_tl  | qwen25_7b  | plain         | bare       | mean            | full_minus_shuffled      |  33 |  4.66154    |  3.60854     |  5.74286  |        0.939394 |
| id_tl  | qwen25_7b  | plain         | bare       | mean            | full_minus_language_only |  33 |  4.64376    |  3.49562     |  5.80622  |        0.909091 |
| id_tl  | qwen25_7b  | plain         | bare       | mean            | masked_minus_shuffled    |  33 |  4.53645    |  2.98346     |  6.01957  |        0.878788 |
| id_tl  | qwen25_7b  | plain         | bare       | sum             | full_minus_shuffled      |  33 |  5.49349    |  3.77049     |  7.25951  |        0.939394 |
| id_tl  | qwen25_7b  | plain         | bare       | sum             | full_minus_language_only |  33 |  5.40817    |  3.96558     |  6.93916  |        0.909091 |
| id_tl  | qwen25_7b  | plain         | bare       | sum             | masked_minus_shuffled    |  33 |  5.55008    |  3.60148     |  7.43611  |        0.848485 |
| id_tl  | qwen25_7b  | plain         | definition | mean            | full_minus_shuffled      |  33 |  1.67807    |  1.31749     |  2.05161  |        0.969697 |
| id_tl  | qwen25_7b  | plain         | definition | mean            | full_minus_language_only |  33 |  1.52533    |  1.17324     |  1.8795   |        0.969697 |
| id_tl  | qwen25_7b  | plain         | definition | mean            | masked_minus_shuffled    |  33 |  1.65317    |  1.19795     |  2.11621  |        0.939394 |
| id_tl  | qwen25_7b  | plain         | definition | sum             | full_minus_shuffled      |  33 |  7.08248    |  5.42227     |  8.95471  |        0.909091 |
| id_tl  | qwen25_7b  | plain         | definition | sum             | full_minus_language_only |  33 |  6.57346    |  5.12982     |  7.96491  |        0.939394 |
| id_tl  | qwen25_7b  | plain         | definition | sum             | masked_minus_shuffled    |  33 |  7.07864    |  5.05192     |  9.14366  |        0.878788 |
| id_tl  | qwen25_7b  | plain         | refers     | mean            | full_minus_shuffled      |  33 |  1.43193    |  1.07187     |  1.78999  |        0.939394 |
| id_tl  | qwen25_7b  | plain         | refers     | mean            | full_minus_language_only |  33 |  1.34806    |  1.04019     |  1.67334  |        0.969697 |
| id_tl  | qwen25_7b  | plain         | refers     | mean            | masked_minus_shuffled    |  33 |  1.84085    |  1.43511     |  2.27962  |        0.969697 |
| id_tl  | qwen25_7b  | plain         | refers     | sum             | full_minus_shuffled      |  33 |  8.08311    |  6.40911     |  9.84615  |        0.969697 |
| id_tl  | qwen25_7b  | plain         | refers     | sum             | full_minus_language_only |  33 |  7.41079    |  5.91251     |  8.92041  |        0.969697 |
| id_tl  | qwen25_7b  | plain         | refers     | sum             | masked_minus_shuffled    |  33 | 10.0769     |  8.04537     | 12.2891   |        0.969697 |
| id_tl  | qwen3_8b   | chat          | bare       | mean            | full_minus_shuffled      |  33 |  0.536206   |  0.0561649   |  1.04318  |        0.666667 |
| id_tl  | qwen3_8b   | chat          | bare       | mean            | full_minus_language_only |  33 |  0.591754   |  0.354433    |  0.850769 |        0.818182 |
| id_tl  | qwen3_8b   | chat          | bare       | mean            | masked_minus_shuffled    |  33 |  0.894767   |  0.290534    |  1.5163   |        0.727273 |
| id_tl  | qwen3_8b   | chat          | bare       | sum             | full_minus_shuffled      |  33 |  1.368      |  0.383462    |  2.43591  |        0.606061 |
| id_tl  | qwen3_8b   | chat          | bare       | sum             | full_minus_language_only |  33 |  1.48709    |  0.903485    |  2.08849  |        0.818182 |
| id_tl  | qwen3_8b   | chat          | bare       | sum             | masked_minus_shuffled    |  33 |  2.29081    |  0.852996    |  3.91662  |        0.727273 |
| id_tl  | qwen3_8b   | chat          | definition | mean            | full_minus_shuffled      |  33 |  0.879784   |  0.617828    |  1.15307  |        0.848485 |
| id_tl  | qwen3_8b   | chat          | definition | mean            | full_minus_language_only |  33 |  0.832549   |  0.608868    |  1.05262  |        0.909091 |
| id_tl  | qwen3_8b   | chat          | definition | mean            | masked_minus_shuffled    |  33 |  0.774232   |  0.573665    |  1.00542  |        0.939394 |
| id_tl  | qwen3_8b   | chat          | definition | sum             | full_minus_shuffled      |  33 |  3.85159    |  2.68236     |  5.06532  |        0.909091 |
| id_tl  | qwen3_8b   | chat          | definition | sum             | full_minus_language_only |  33 |  3.63658    |  2.71307     |  4.55107  |        0.939394 |
| id_tl  | qwen3_8b   | chat          | definition | sum             | masked_minus_shuffled    |  33 |  3.40214    |  2.47387     |  4.4726   |        0.939394 |
| id_tl  | qwen3_8b   | chat          | refers     | mean            | full_minus_shuffled      |  33 |  0.93595    |  0.676905    |  1.21597  |        0.848485 |
| id_tl  | qwen3_8b   | chat          | refers     | mean            | full_minus_language_only |  33 |  0.907909   |  0.659914    |  1.17017  |        0.969697 |
| id_tl  | qwen3_8b   | chat          | refers     | mean            | masked_minus_shuffled    |  33 |  1.03811    |  0.764771    |  1.32215  |        0.909091 |
| id_tl  | qwen3_8b   | chat          | refers     | sum             | full_minus_shuffled      |  33 |  5.0277     |  3.6168      |  6.50461  |        0.878788 |
| id_tl  | qwen3_8b   | chat          | refers     | sum             | full_minus_language_only |  33 |  4.90804    |  3.69463     |  6.21095  |        0.969697 |
| id_tl  | qwen3_8b   | chat          | refers     | sum             | masked_minus_shuffled    |  33 |  5.41804    |  3.92255     |  6.98944  |        0.848485 |
| id_tl  | qwen3_8b   | plain         | bare       | mean            | full_minus_shuffled      |  33 |  1.4524     |  0.706053    |  2.21846  |        0.727273 |
| id_tl  | qwen3_8b   | plain         | bare       | mean            | full_minus_language_only |  33 |  1.27188    |  0.820392    |  1.73189  |        0.878788 |
| id_tl  | qwen3_8b   | plain         | bare       | mean            | masked_minus_shuffled    |  33 |  3.58365    |  2.22646     |  5.01288  |        0.878788 |
| id_tl  | qwen3_8b   | plain         | bare       | sum             | full_minus_shuffled      |  33 |  2.35635    |  1.28463     |  3.55494  |        0.727273 |
| id_tl  | qwen3_8b   | plain         | bare       | sum             | full_minus_language_only |  33 |  1.83454    |  1.13637     |  2.67283  |        0.909091 |
| id_tl  | qwen3_8b   | plain         | bare       | sum             | masked_minus_shuffled    |  33 |  4.43408    |  2.84135     |  6.04193  |        0.878788 |
| id_tl  | qwen3_8b   | plain         | definition | mean            | full_minus_shuffled      |  33 |  0.928076   |  0.6525      |  1.21386  |        0.909091 |
| id_tl  | qwen3_8b   | plain         | definition | mean            | full_minus_language_only |  33 |  0.893654   |  0.653727    |  1.12959  |        0.909091 |
| id_tl  | qwen3_8b   | plain         | definition | mean            | masked_minus_shuffled    |  33 |  1.04474    |  0.797153    |  1.30759  |        0.939394 |
| id_tl  | qwen3_8b   | plain         | definition | sum             | full_minus_shuffled      |  33 |  4.24953    |  3.09318     |  5.49578  |        0.909091 |
| id_tl  | qwen3_8b   | plain         | definition | sum             | full_minus_language_only |  33 |  4.04881    |  3.05615     |  5.0253   |        0.909091 |
| id_tl  | qwen3_8b   | plain         | definition | sum             | masked_minus_shuffled    |  33 |  4.64779    |  3.5452      |  5.85799  |        0.969697 |
| id_tl  | qwen3_8b   | plain         | refers     | mean            | full_minus_shuffled      |  33 |  0.963374   |  0.630293    |  1.30142  |        0.787879 |
| id_tl  | qwen3_8b   | plain         | refers     | mean            | full_minus_language_only |  33 |  0.98305    |  0.635563    |  1.32078  |        0.939394 |
| id_tl  | qwen3_8b   | plain         | refers     | mean            | masked_minus_shuffled    |  33 |  1.04904    |  0.730075    |  1.3942   |        0.909091 |
| id_tl  | qwen3_8b   | plain         | refers     | sum             | full_minus_shuffled      |  33 |  5.70233    |  4.11886     |  7.35233  |        0.878788 |
| id_tl  | qwen3_8b   | plain         | refers     | sum             | full_minus_language_only |  33 |  5.75662    |  4.42566     |  7.16945  |        0.969697 |
| id_tl  | qwen3_8b   | plain         | refers     | sum             | masked_minus_shuffled    |  33 |  5.91079    |  4.33906     |  7.6083   |        0.969697 |
| zh_ja  | gemma3_12b | chat          | bare       | mean            | full_minus_shuffled      |  27 |  4.9097     |  2.45704     |  7.8359   |        0.740741 |
| zh_ja  | gemma3_12b | chat          | bare       | mean            | full_minus_language_only |  27 |  3.44823    |  1.27078     |  6.03747  |        0.740741 |
| zh_ja  | gemma3_12b | chat          | bare       | mean            | masked_minus_shuffled    |  27 |  7.49717    |  5.31524     |  9.87849  |        0.962963 |
| zh_ja  | gemma3_12b | chat          | bare       | sum             | full_minus_shuffled      |  27 | 13.6183     |  7.44614     | 20.9393   |        0.851852 |
| zh_ja  | gemma3_12b | chat          | bare       | sum             | full_minus_language_only |  27 | 10.6776     |  4.95686     | 17.4984   |        0.777778 |
| zh_ja  | gemma3_12b | chat          | bare       | sum             | masked_minus_shuffled    |  27 | 17.1299     | 11.0625      | 23.2025   |        0.925926 |
| zh_ja  | gemma3_12b | chat          | definition | mean            | full_minus_shuffled      |  27 |  3.54987    |  2.49859     |  4.65116  |        0.925926 |
| zh_ja  | gemma3_12b | chat          | definition | mean            | full_minus_language_only |  27 |  3.17544    |  2.26718     |  4.07032  |        0.962963 |
| zh_ja  | gemma3_12b | chat          | definition | mean            | masked_minus_shuffled    |  27 |  3.67498    |  2.79783     |  4.58057  |        0.962963 |
| zh_ja  | gemma3_12b | chat          | definition | sum             | full_minus_shuffled      |  27 | 17.8959     | 12.14        | 24.0265   |        0.925926 |
| zh_ja  | gemma3_12b | chat          | definition | sum             | full_minus_language_only |  27 | 16.1606     | 11.5623      | 21.2542   |        0.962963 |
| zh_ja  | gemma3_12b | chat          | definition | sum             | masked_minus_shuffled    |  27 | 18.5925     | 14.0523      | 23.119    |        0.925926 |
| zh_ja  | gemma3_12b | chat          | refers     | mean            | full_minus_shuffled      |  27 |  3.2927     |  2.50818     |  4.13229  |        0.962963 |
| zh_ja  | gemma3_12b | chat          | refers     | mean            | full_minus_language_only |  27 |  3.09952    |  2.48792     |  3.73971  |        1        |
| zh_ja  | gemma3_12b | chat          | refers     | mean            | masked_minus_shuffled    |  27 |  3.52955    |  2.88429     |  4.19432  |        1        |
| zh_ja  | gemma3_12b | chat          | refers     | sum             | full_minus_shuffled      |  27 | 20.0578     | 15.0125      | 25.5352   |        1        |
| zh_ja  | gemma3_12b | chat          | refers     | sum             | full_minus_language_only |  27 | 19.0734     | 15.3762      | 23.4002   |        1        |
| zh_ja  | gemma3_12b | chat          | refers     | sum             | masked_minus_shuffled    |  27 | 20.9277     | 16.8208      | 24.8644   |        0.962963 |
| zh_ja  | gemma3_12b | plain         | bare       | mean            | full_minus_shuffled      |  27 |  0.637594   |  0.000672553 |  1.27969  |        0.62963  |
| zh_ja  | gemma3_12b | plain         | bare       | mean            | full_minus_language_only |  27 |  0.602095   | -0.0464461   |  1.30603  |        0.592593 |
| zh_ja  | gemma3_12b | plain         | bare       | mean            | masked_minus_shuffled    |  27 |  0.677802   |  0.0107352   |  1.34316  |        0.666667 |
| zh_ja  | gemma3_12b | plain         | bare       | sum             | full_minus_shuffled      |  27 |  1.51149    | -0.631703    |  3.61435  |        0.666667 |
| zh_ja  | gemma3_12b | plain         | bare       | sum             | full_minus_language_only |  27 |  1.64354    |  0.186009    |  3.15685  |        0.62963  |
| zh_ja  | gemma3_12b | plain         | bare       | sum             | masked_minus_shuffled    |  27 |  1.86335    |  0.287152    |  3.42731  |        0.740741 |
| zh_ja  | gemma3_12b | plain         | definition | mean            | full_minus_shuffled      |  27 |  0.30639    |  0.10113     |  0.51175  |        0.703704 |
| zh_ja  | gemma3_12b | plain         | definition | mean            | full_minus_language_only |  27 |  0.293148   |  0.114702    |  0.510081 |        0.777778 |
| zh_ja  | gemma3_12b | plain         | definition | mean            | masked_minus_shuffled    |  27 |  0.272674   |  0.0474503   |  0.505561 |        0.666667 |
| zh_ja  | gemma3_12b | plain         | definition | sum             | full_minus_shuffled      |  27 |  1.02229    | -0.165944    |  2.25933  |        0.666667 |
| zh_ja  | gemma3_12b | plain         | definition | sum             | full_minus_language_only |  27 |  1.09465    |  0.210194    |  2.0909   |        0.666667 |
| zh_ja  | gemma3_12b | plain         | definition | sum             | masked_minus_shuffled    |  27 |  1.48611    |  0.201623    |  2.78765  |        0.703704 |
| zh_ja  | gemma3_12b | plain         | refers     | mean            | full_minus_shuffled      |  27 |  0.260075   | -0.01091     |  0.515865 |        0.666667 |
| zh_ja  | gemma3_12b | plain         | refers     | mean            | full_minus_language_only |  27 |  0.284751   |  0.0755494   |  0.518521 |        0.703704 |
| zh_ja  | gemma3_12b | plain         | refers     | mean            | masked_minus_shuffled    |  27 |  0.308976   |  0.0365539   |  0.54748  |        0.740741 |
| zh_ja  | gemma3_12b | plain         | refers     | sum             | full_minus_shuffled      |  27 |  1.49384    | -0.478663    |  3.41262  |        0.703704 |
| zh_ja  | gemma3_12b | plain         | refers     | sum             | full_minus_language_only |  27 |  1.69091    |  0.319596    |  3.20288  |        0.62963  |
| zh_ja  | gemma3_12b | plain         | refers     | sum             | masked_minus_shuffled    |  27 |  2.34109    |  0.469336    |  4.1394   |        0.740741 |
| zh_ja  | gemma3_4b  | chat          | bare       | mean            | full_minus_shuffled      |  27 |  5.42353    |  2.10005     |  8.85168  |        0.666667 |
| zh_ja  | gemma3_4b  | chat          | bare       | mean            | full_minus_language_only |  27 |  5.83602    |  3.19679     |  8.68183  |        0.814815 |
| zh_ja  | gemma3_4b  | chat          | bare       | mean            | masked_minus_shuffled    |  27 |  7.97397    |  4.60651     | 11.3951   |        0.740741 |
| zh_ja  | gemma3_4b  | chat          | bare       | sum             | full_minus_shuffled      |  27 | 18.0954     |  8.4858      | 28.999    |        0.814815 |
| zh_ja  | gemma3_4b  | chat          | bare       | sum             | full_minus_language_only |  27 | 16.0524     |  7.7645      | 24.616    |        0.925926 |
| zh_ja  | gemma3_4b  | chat          | bare       | sum             | masked_minus_shuffled    |  27 | 19.9777     | 11.404       | 29.1822   |        0.851852 |
| zh_ja  | gemma3_4b  | chat          | definition | mean            | full_minus_shuffled      |  27 |  3.06173    |  2.15998     |  3.94695  |        0.925926 |
| zh_ja  | gemma3_4b  | chat          | definition | mean            | full_minus_language_only |  27 |  2.78539    |  1.93262     |  3.64569  |        0.925926 |
| zh_ja  | gemma3_4b  | chat          | definition | mean            | masked_minus_shuffled    |  27 |  2.94271    |  2.03427     |  3.84719  |        0.925926 |
| zh_ja  | gemma3_4b  | chat          | definition | sum             | full_minus_shuffled      |  27 | 14.7177     |  9.50262     | 20.0093   |        0.925926 |
| zh_ja  | gemma3_4b  | chat          | definition | sum             | full_minus_language_only |  27 | 13.2204     |  8.20512     | 18.6101   |        0.925926 |
| zh_ja  | gemma3_4b  | chat          | definition | sum             | masked_minus_shuffled    |  27 | 15.0436     | 10.582       | 19.4699   |        0.962963 |
| zh_ja  | gemma3_4b  | chat          | refers     | mean            | full_minus_shuffled      |  27 |  2.82864    |  1.89541     |  3.76634  |        0.888889 |
| zh_ja  | gemma3_4b  | chat          | refers     | mean            | full_minus_language_only |  27 |  2.69821    |  1.93202     |  3.46633  |        0.925926 |
| zh_ja  | gemma3_4b  | chat          | refers     | mean            | masked_minus_shuffled    |  27 |  3.47473    |  2.42684     |  4.54868  |        0.851852 |
| zh_ja  | gemma3_4b  | chat          | refers     | sum             | full_minus_shuffled      |  27 | 17.4923     | 11.2053      | 24.0323   |        0.851852 |
| zh_ja  | gemma3_4b  | chat          | refers     | sum             | full_minus_language_only |  27 | 16.5019     | 11.215       | 21.6848   |        0.925926 |
| zh_ja  | gemma3_4b  | chat          | refers     | sum             | masked_minus_shuffled    |  27 | 21.4309     | 15.3322      | 27.6356   |        0.925926 |
| zh_ja  | gemma3_4b  | plain         | bare       | mean            | full_minus_shuffled      |  27 |  1.53316    |  0.637271    |  2.44094  |        0.703704 |
| zh_ja  | gemma3_4b  | plain         | bare       | mean            | full_minus_language_only |  27 |  1.43056    |  0.760348    |  2.08832  |        0.814815 |
| zh_ja  | gemma3_4b  | plain         | bare       | mean            | masked_minus_shuffled    |  27 |  1.75573    |  0.943798    |  2.52845  |        0.851852 |
| zh_ja  | gemma3_4b  | plain         | bare       | sum             | full_minus_shuffled      |  27 |  3.53565    |  1.32911     |  5.72493  |        0.740741 |
| zh_ja  | gemma3_4b  | plain         | bare       | sum             | full_minus_language_only |  27 |  3.65088    |  1.70324     |  6.11617  |        0.740741 |
| zh_ja  | gemma3_4b  | plain         | bare       | sum             | masked_minus_shuffled    |  27 |  2.86499    |  1.26834     |  4.38567  |        0.814815 |
| zh_ja  | gemma3_4b  | plain         | definition | mean            | full_minus_shuffled      |  27 |  0.557065   |  0.183693    |  0.916685 |        0.814815 |
| zh_ja  | gemma3_4b  | plain         | definition | mean            | full_minus_language_only |  27 |  0.497494   |  0.16992     |  0.815134 |        0.777778 |
| zh_ja  | gemma3_4b  | plain         | definition | mean            | masked_minus_shuffled    |  27 |  0.561187   |  0.253503    |  0.851875 |        0.814815 |
| zh_ja  | gemma3_4b  | plain         | definition | sum             | full_minus_shuffled      |  27 |  3.46713    |  1.16516     |  5.63824  |        0.814815 |
| zh_ja  | gemma3_4b  | plain         | definition | sum             | full_minus_language_only |  27 |  3.23379    |  1.26077     |  5.12019  |        0.777778 |
| zh_ja  | gemma3_4b  | plain         | definition | sum             | masked_minus_shuffled    |  27 |  3.09971    |  1.36797     |  4.80114  |        0.777778 |
| zh_ja  | gemma3_4b  | plain         | refers     | mean            | full_minus_shuffled      |  27 |  0.778456   |  0.5062      |  1.06117  |        0.814815 |
| zh_ja  | gemma3_4b  | plain         | refers     | mean            | full_minus_language_only |  27 |  0.619805   |  0.361872    |  0.885324 |        0.777778 |
| zh_ja  | gemma3_4b  | plain         | refers     | mean            | masked_minus_shuffled    |  27 |  0.683283   |  0.447493    |  0.904449 |        0.851852 |
| zh_ja  | gemma3_4b  | plain         | refers     | sum             | full_minus_shuffled      |  27 |  5.24518    |  3.33901     |  7.2483   |        0.851852 |
| zh_ja  | gemma3_4b  | plain         | refers     | sum             | full_minus_language_only |  27 |  4.47189    |  2.4993      |  6.92708  |        0.777778 |
| zh_ja  | gemma3_4b  | plain         | refers     | sum             | masked_minus_shuffled    |  27 |  4.07404    |  2.58209     |  5.49231  |        0.814815 |
| zh_ja  | qwen25_7b  | chat          | bare       | mean            | full_minus_shuffled      |  27 |  2.76151    |  1.61862     |  3.93931  |        0.777778 |
| zh_ja  | qwen25_7b  | chat          | bare       | mean            | full_minus_language_only |  27 |  2.17324    |  1.49083     |  2.87852  |        0.851852 |
| zh_ja  | qwen25_7b  | chat          | bare       | mean            | masked_minus_shuffled    |  27 |  5.15079    |  3.71622     |  6.61879  |        0.962963 |
| zh_ja  | qwen25_7b  | chat          | bare       | sum             | full_minus_shuffled      |  27 |  8.56687    |  4.61278     | 13.0872   |        0.814815 |
| zh_ja  | qwen25_7b  | chat          | bare       | sum             | full_minus_language_only |  27 |  7.42877    |  5.00702     |  9.95291  |        0.814815 |
| zh_ja  | qwen25_7b  | chat          | bare       | sum             | masked_minus_shuffled    |  27 | 13.5263     |  9.57118     | 18.381    |        0.925926 |
| zh_ja  | qwen25_7b  | chat          | definition | mean            | full_minus_shuffled      |  27 |  1.07692    |  0.622227    |  1.52991  |        0.851852 |
| zh_ja  | qwen25_7b  | chat          | definition | mean            | full_minus_language_only |  27 |  1.23721    |  0.918529    |  1.57127  |        0.962963 |
| zh_ja  | qwen25_7b  | chat          | definition | mean            | masked_minus_shuffled    |  27 |  1.89391    |  1.3354      |  2.4792   |        0.962963 |
| zh_ja  | qwen25_7b  | chat          | definition | sum             | full_minus_shuffled      |  27 |  6.79833    |  3.95525     |  9.75169  |        0.888889 |
| zh_ja  | qwen25_7b  | chat          | definition | sum             | full_minus_language_only |  27 |  7.35684    |  5.12122     |  9.67055  |        0.962963 |
| zh_ja  | qwen25_7b  | chat          | definition | sum             | masked_minus_shuffled    |  27 | 11.9806     |  8.23028     | 16.1945   |        0.962963 |
| zh_ja  | qwen25_7b  | chat          | refers     | mean            | full_minus_shuffled      |  27 |  2.00011    |  1.43441     |  2.57641  |        0.925926 |
| zh_ja  | qwen25_7b  | chat          | refers     | mean            | full_minus_language_only |  27 |  2.02327    |  1.62538     |  2.42852  |        1        |
| zh_ja  | qwen25_7b  | chat          | refers     | mean            | masked_minus_shuffled    |  27 |  2.52551    |  1.84552     |  3.23552  |        0.962963 |
| zh_ja  | qwen25_7b  | chat          | refers     | sum             | full_minus_shuffled      |  27 | 13.0942     |  9.47472     | 17.0107   |        0.925926 |
| zh_ja  | qwen25_7b  | chat          | refers     | sum             | full_minus_language_only |  27 | 13.3182     | 10.7141      | 15.9971   |        1        |
| zh_ja  | qwen25_7b  | chat          | refers     | sum             | masked_minus_shuffled    |  27 | 16.8054     | 12.1895      | 22.0505   |        0.962963 |
| zh_ja  | qwen25_7b  | plain         | bare       | mean            | full_minus_shuffled      |  27 |  2.43177    |  1.37693     |  3.41125  |        0.814815 |
| zh_ja  | qwen25_7b  | plain         | bare       | mean            | full_minus_language_only |  27 |  2.54101    |  1.69882     |  3.37775  |        0.888889 |
| zh_ja  | qwen25_7b  | plain         | bare       | mean            | masked_minus_shuffled    |  27 |  5.17654    |  3.4711      |  6.86601  |        0.851852 |
| zh_ja  | qwen25_7b  | plain         | bare       | sum             | full_minus_shuffled      |  27 |  6.12455    |  4.09824     |  8.13146  |        0.888889 |
| zh_ja  | qwen25_7b  | plain         | bare       | sum             | full_minus_language_only |  27 |  5.974      |  4.01934     |  7.92083  |        0.925926 |
| zh_ja  | qwen25_7b  | plain         | bare       | sum             | masked_minus_shuffled    |  27 | 12.6095     |  8.96484     | 16.4537   |        0.888889 |
| zh_ja  | qwen25_7b  | plain         | definition | mean            | full_minus_shuffled      |  27 |  1.06928    |  0.600502    |  1.55998  |        0.888889 |
| zh_ja  | qwen25_7b  | plain         | definition | mean            | full_minus_language_only |  27 |  1.20204    |  0.921001    |  1.48082  |        0.962963 |
| zh_ja  | qwen25_7b  | plain         | definition | mean            | masked_minus_shuffled    |  27 |  1.92996    |  1.41037     |  2.4638   |        0.962963 |
| zh_ja  | qwen25_7b  | plain         | definition | sum             | full_minus_shuffled      |  27 |  6.55888    |  3.98742     |  9.09077  |        0.888889 |
| zh_ja  | qwen25_7b  | plain         | definition | sum             | full_minus_language_only |  27 |  7.07157    |  5.36824     |  8.88483  |        0.962963 |
| zh_ja  | qwen25_7b  | plain         | definition | sum             | masked_minus_shuffled    |  27 | 11.8542     |  8.72304     | 15.3252   |        0.962963 |
| zh_ja  | qwen25_7b  | plain         | refers     | mean            | full_minus_shuffled      |  27 |  1.27264    |  0.851677    |  1.69475  |        0.851852 |
| zh_ja  | qwen25_7b  | plain         | refers     | mean            | full_minus_language_only |  27 |  1.31165    |  1.00961     |  1.60481  |        0.962963 |
| zh_ja  | qwen25_7b  | plain         | refers     | mean            | masked_minus_shuffled    |  27 |  2.19003    |  1.66343     |  2.74819  |        0.962963 |
| zh_ja  | qwen25_7b  | plain         | refers     | sum             | full_minus_shuffled      |  27 |  8.46081    |  5.8035      | 11.2492   |        0.851852 |
| zh_ja  | qwen25_7b  | plain         | refers     | sum             | full_minus_language_only |  27 |  8.7893     |  6.70696     | 11.0019   |        0.962963 |
| zh_ja  | qwen25_7b  | plain         | refers     | sum             | masked_minus_shuffled    |  27 | 14.7318     | 10.922       | 19.0229   |        0.962963 |
| zh_ja  | qwen3_8b   | chat          | bare       | mean            | full_minus_shuffled      |  27 |  0.771709   | -0.174352    |  1.69159  |        0.555556 |
| zh_ja  | qwen3_8b   | chat          | bare       | mean            | full_minus_language_only |  27 |  0.946698   |  0.279145    |  1.64078  |        0.666667 |
| zh_ja  | qwen3_8b   | chat          | bare       | mean            | masked_minus_shuffled    |  27 |  2.95982    |  1.62675     |  4.35002  |        0.703704 |
| zh_ja  | qwen3_8b   | chat          | bare       | sum             | full_minus_shuffled      |  27 |  3.02091    |  0.326371    |  5.78689  |        0.592593 |
| zh_ja  | qwen3_8b   | chat          | bare       | sum             | full_minus_language_only |  27 |  3.52493    |  1.45895     |  5.64772  |        0.666667 |
| zh_ja  | qwen3_8b   | chat          | bare       | sum             | masked_minus_shuffled    |  27 |  8.51842    |  5.16614     | 11.9081   |        0.814815 |
| zh_ja  | qwen3_8b   | chat          | definition | mean            | full_minus_shuffled      |  27 |  0.983      |  0.737502    |  1.2313   |        0.925926 |
| zh_ja  | qwen3_8b   | chat          | definition | mean            | full_minus_language_only |  27 |  1.00461    |  0.773324    |  1.24892  |        0.962963 |
| zh_ja  | qwen3_8b   | chat          | definition | mean            | masked_minus_shuffled    |  27 |  1.2276     |  0.891523    |  1.56161  |        0.925926 |
| zh_ja  | qwen3_8b   | chat          | definition | sum             | full_minus_shuffled      |  27 |  5.50866    |  4.30054     |  6.72292  |        0.962963 |
| zh_ja  | qwen3_8b   | chat          | definition | sum             | full_minus_language_only |  27 |  5.6458     |  4.34578     |  6.98393  |        1        |
| zh_ja  | qwen3_8b   | chat          | definition | sum             | masked_minus_shuffled    |  27 |  7.11347    |  5.40148     |  8.79841  |        0.962963 |
| zh_ja  | qwen3_8b   | chat          | refers     | mean            | full_minus_shuffled      |  27 |  1.1328     |  0.909198    |  1.35997  |        1        |
| zh_ja  | qwen3_8b   | chat          | refers     | mean            | full_minus_language_only |  27 |  1.13436    |  0.908419    |  1.37876  |        1        |
| zh_ja  | qwen3_8b   | chat          | refers     | mean            | masked_minus_shuffled    |  27 |  1.41923    |  1.10636     |  1.7562   |        0.962963 |
| zh_ja  | qwen3_8b   | chat          | refers     | sum             | full_minus_shuffled      |  27 |  7.42219    |  5.96821     |  8.92865  |        1        |
| zh_ja  | qwen3_8b   | chat          | refers     | sum             | full_minus_language_only |  27 |  7.52524    |  6.01146     |  9.14641  |        1        |
| zh_ja  | qwen3_8b   | chat          | refers     | sum             | masked_minus_shuffled    |  27 |  9.41829    |  7.22898     | 11.6832   |        0.888889 |
| zh_ja  | qwen3_8b   | plain         | bare       | mean            | full_minus_shuffled      |  27 |  1.90468    |  1.19544     |  2.57754  |        0.814815 |
| zh_ja  | qwen3_8b   | plain         | bare       | mean            | full_minus_language_only |  27 |  1.94383    |  1.39084     |  2.53773  |        0.925926 |
| zh_ja  | qwen3_8b   | plain         | bare       | mean            | masked_minus_shuffled    |  27 |  5.06297    |  3.81134     |  6.27753  |        0.925926 |
| zh_ja  | qwen3_8b   | plain         | bare       | sum             | full_minus_shuffled      |  27 |  5.25012    |  3.36122     |  7.34338  |        0.888889 |
| zh_ja  | qwen3_8b   | plain         | bare       | sum             | full_minus_language_only |  27 |  5.22397    |  3.45441     |  7.11936  |        0.962963 |
| zh_ja  | qwen3_8b   | plain         | bare       | sum             | masked_minus_shuffled    |  27 | 10.5498     |  7.95581     | 13.0688   |        0.925926 |
| zh_ja  | qwen3_8b   | plain         | definition | mean            | full_minus_shuffled      |  27 |  1.21511    |  0.967489    |  1.47156  |        0.962963 |
| zh_ja  | qwen3_8b   | plain         | definition | mean            | full_minus_language_only |  27 |  1.21919    |  0.982164    |  1.45691  |        1        |
| zh_ja  | qwen3_8b   | plain         | definition | mean            | masked_minus_shuffled    |  27 |  1.67337    |  1.28877     |  2.06597  |        0.962963 |
| zh_ja  | qwen3_8b   | plain         | definition | sum             | full_minus_shuffled      |  27 |  7.08135    |  5.68196     |  8.48184  |        1        |
| zh_ja  | qwen3_8b   | plain         | definition | sum             | full_minus_language_only |  27 |  6.84606    |  5.33201     |  8.33863  |        1        |
| zh_ja  | qwen3_8b   | plain         | definition | sum             | masked_minus_shuffled    |  27 |  9.42329    |  7.29731     | 11.6232   |        0.962963 |
| zh_ja  | qwen3_8b   | plain         | refers     | mean            | full_minus_shuffled      |  27 |  1.6031     |  1.26962     |  1.9552   |        0.962963 |
| zh_ja  | qwen3_8b   | plain         | refers     | mean            | full_minus_language_only |  27 |  1.59117    |  1.2685      |  1.91547  |        1        |
| zh_ja  | qwen3_8b   | plain         | refers     | mean            | masked_minus_shuffled    |  27 |  1.67549    |  1.28843     |  2.07388  |        0.925926 |
| zh_ja  | qwen3_8b   | plain         | refers     | sum             | full_minus_shuffled      |  27 | 10.3        |  8.28287     | 12.4069   |        0.962963 |
| zh_ja  | qwen3_8b   | plain         | refers     | sum             | full_minus_language_only |  27 | 10.3256     |  8.30206     | 12.4193   |        1        |
| zh_ja  | qwen3_8b   | plain         | refers     | sum             | masked_minus_shuffled    |  27 | 11.0798     |  8.75965     | 13.4419   |        0.925926 |
