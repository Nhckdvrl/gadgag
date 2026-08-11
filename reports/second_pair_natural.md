# Non-CJK natural context/form replication

| pair   | model      | wrapper    | normalization   | contrast               |   n_items |   estimate |      ci_low |   ci_high |   positive_rate |
|:-------|:-----------|:-----------|:----------------|:-----------------------|----------:|-----------:|------------:|----------:|----------------:|
| id_ms  | gemma3_12b | bare       | mean            | full_minus_unrelated   |        30 |  7.62022   |  5.68685    |  9.68321  |        0.966667 |
| id_ms  | gemma3_12b | bare       | mean            | masked_minus_unrelated |        30 |  3.781     |  2.19399    |  5.50209  |        0.766667 |
| id_ms  | gemma3_12b | bare       | mean            | full_minus_masked      |        30 |  3.83922   |  2.30076    |  5.32311  |        0.733333 |
| id_ms  | gemma3_12b | bare       | mean            | full_minus_surface     |        30 |  0.607378  | -1.44398    |  2.51095  |        0.666667 |
| id_ms  | gemma3_12b | bare       | sum             | full_minus_unrelated   |        30 | 11.7401    |  8.6544     | 15.0701   |        0.933333 |
| id_ms  | gemma3_12b | bare       | sum             | masked_minus_unrelated |        30 |  5.63628   |  3.16911    |  8.27926  |        0.766667 |
| id_ms  | gemma3_12b | bare       | sum             | full_minus_masked      |        30 |  6.10377   |  3.26919    |  8.95047  |        0.833333 |
| id_ms  | gemma3_12b | bare       | sum             | full_minus_surface     |        30 |  2.28642   | -0.735905   |  5.38059  |        0.666667 |
| id_ms  | gemma3_12b | definition | mean            | full_minus_unrelated   |        30 |  2.69988   |  2.25741    |  3.1333   |        1        |
| id_ms  | gemma3_12b | definition | mean            | masked_minus_unrelated |        30 |  1.71767   |  1.3132     |  2.10016  |        0.933333 |
| id_ms  | gemma3_12b | definition | mean            | full_minus_masked      |        30 |  0.982207  |  0.526938   |  1.42501  |        0.8      |
| id_ms  | gemma3_12b | definition | mean            | full_minus_surface     |        30 |  1.03092   |  0.537423   |  1.51609  |        0.733333 |
| id_ms  | gemma3_12b | definition | sum             | full_minus_unrelated   |        30 | 11.8443    |  9.85131    | 13.8458   |        1        |
| id_ms  | gemma3_12b | definition | sum             | masked_minus_unrelated |        30 |  7.1178    |  5.23658    |  8.94807  |        0.933333 |
| id_ms  | gemma3_12b | definition | sum             | full_minus_masked      |        30 |  4.72648   |  2.71631    |  6.82439  |        0.766667 |
| id_ms  | gemma3_12b | definition | sum             | full_minus_surface     |        30 |  4.64793   |  2.72619    |  6.64007  |        0.8      |
| id_ms  | gemma3_12b | refers     | mean            | full_minus_unrelated   |        30 |  2.25603   |  1.9012     |  2.62127  |        1        |
| id_ms  | gemma3_12b | refers     | mean            | masked_minus_unrelated |        30 |  1.84621   |  1.45702    |  2.21919  |        0.966667 |
| id_ms  | gemma3_12b | refers     | mean            | full_minus_masked      |        30 |  0.409823  |  0.0594515  |  0.798251 |        0.666667 |
| id_ms  | gemma3_12b | refers     | mean            | full_minus_surface     |        30 |  1.05362   |  0.683237   |  1.45667  |        0.866667 |
| id_ms  | gemma3_12b | refers     | sum             | full_minus_unrelated   |        30 | 12.0421    | 10.1666     | 13.9763   |        1        |
| id_ms  | gemma3_12b | refers     | sum             | masked_minus_unrelated |        30 |  9.43816   |  7.45944    | 11.4729   |        0.966667 |
| id_ms  | gemma3_12b | refers     | sum             | full_minus_masked      |        30 |  2.60392   |  0.638129   |  4.54437  |        0.666667 |
| id_ms  | gemma3_12b | refers     | sum             | full_minus_surface     |        30 |  5.74257   |  3.70401    |  7.90511  |        0.866667 |
| id_ms  | gemma3_4b  | bare       | mean            | full_minus_unrelated   |        30 | 10.3804    |  7.48932    | 13.2733   |        0.933333 |
| id_ms  | gemma3_4b  | bare       | mean            | masked_minus_unrelated |        30 |  7.86901   |  5.44493    | 10.4465   |        0.866667 |
| id_ms  | gemma3_4b  | bare       | mean            | full_minus_masked      |        30 |  2.51137   | -0.164927   |  5.2002   |        0.633333 |
| id_ms  | gemma3_4b  | bare       | mean            | full_minus_surface     |        30 |  3.37695   |  1.19344    |  5.60924  |        0.666667 |
| id_ms  | gemma3_4b  | bare       | sum             | full_minus_unrelated   |        30 | 15.6287    |  9.98803    | 21.0352   |        0.933333 |
| id_ms  | gemma3_4b  | bare       | sum             | masked_minus_unrelated |        30 | 13.0603    |  8.61232    | 17.876    |        0.866667 |
| id_ms  | gemma3_4b  | bare       | sum             | full_minus_masked      |        30 |  2.56836   | -2.51758    |  7.49288  |        0.566667 |
| id_ms  | gemma3_4b  | bare       | sum             | full_minus_surface     |        30 |  5.41693   |  1.46338    |  8.78625  |        0.7      |
| id_ms  | gemma3_4b  | definition | mean            | full_minus_unrelated   |        30 |  2.4746    |  1.81228    |  3.1114   |        0.933333 |
| id_ms  | gemma3_4b  | definition | mean            | masked_minus_unrelated |        30 |  2.09784   |  1.58182    |  2.65137  |        0.933333 |
| id_ms  | gemma3_4b  | definition | mean            | full_minus_masked      |        30 |  0.376764  | -0.221151   |  0.965313 |        0.6      |
| id_ms  | gemma3_4b  | definition | mean            | full_minus_surface     |        30 |  1.41618   |  0.785198   |  2.01756  |        0.8      |
| id_ms  | gemma3_4b  | definition | sum             | full_minus_unrelated   |        30 | 11.2966    |  8.07919    | 14.4126   |        0.933333 |
| id_ms  | gemma3_4b  | definition | sum             | masked_minus_unrelated |        30 | 10.0998    |  6.99386    | 13.7595   |        0.9      |
| id_ms  | gemma3_4b  | definition | sum             | full_minus_masked      |        30 |  1.19676   | -1.91821    |  4.38808  |        0.566667 |
| id_ms  | gemma3_4b  | definition | sum             | full_minus_surface     |        30 |  5.956     |  3.36387    |  8.46026  |        0.833333 |
| id_ms  | gemma3_4b  | refers     | mean            | full_minus_unrelated   |        30 |  2.39965   |  1.81024    |  2.95561  |        0.966667 |
| id_ms  | gemma3_4b  | refers     | mean            | masked_minus_unrelated |        30 |  2.1523    |  1.66167    |  2.68179  |        0.933333 |
| id_ms  | gemma3_4b  | refers     | mean            | full_minus_masked      |        30 |  0.247349  | -0.282554   |  0.773295 |        0.566667 |
| id_ms  | gemma3_4b  | refers     | mean            | full_minus_surface     |        30 |  0.975844  |  0.515948   |  1.41166  |        0.8      |
| id_ms  | gemma3_4b  | refers     | sum             | full_minus_unrelated   |        30 | 13.2849    |  9.78737    | 16.7279   |        0.966667 |
| id_ms  | gemma3_4b  | refers     | sum             | masked_minus_unrelated |        30 | 11.4066    |  8.62621    | 14.2198   |        0.933333 |
| id_ms  | gemma3_4b  | refers     | sum             | full_minus_masked      |        30 |  1.87828   | -1.07855    |  4.7975   |        0.533333 |
| id_ms  | gemma3_4b  | refers     | sum             | full_minus_surface     |        30 |  5.66389   |  3.31478    |  8.03737  |        0.8      |
| id_ms  | qwen25_7b  | bare       | mean            | full_minus_unrelated   |        30 |  1.86805   |  0.74389    |  3.0036   |        0.666667 |
| id_ms  | qwen25_7b  | bare       | mean            | masked_minus_unrelated |        30 |  1.7138    |  0.568269   |  2.8102   |        0.666667 |
| id_ms  | qwen25_7b  | bare       | mean            | full_minus_masked      |        30 |  0.154246  | -0.687464   |  0.938116 |        0.533333 |
| id_ms  | qwen25_7b  | bare       | mean            | full_minus_surface     |        30 |  1.3678    |  0.499091   |  2.25933  |        0.8      |
| id_ms  | qwen25_7b  | bare       | sum             | full_minus_unrelated   |        30 |  3.68872   |  1.23221    |  6.33886  |        0.666667 |
| id_ms  | qwen25_7b  | bare       | sum             | masked_minus_unrelated |        30 |  3.1345    |  0.768412   |  5.64768  |        0.666667 |
| id_ms  | qwen25_7b  | bare       | sum             | full_minus_masked      |        30 |  0.554224  | -1.27335    |  2.29226  |        0.6      |
| id_ms  | qwen25_7b  | bare       | sum             | full_minus_surface     |        30 |  3.17392   |  1.31704    |  5.35995  |        0.833333 |
| id_ms  | qwen25_7b  | definition | mean            | full_minus_unrelated   |        30 |  0.774941  |  0.453527   |  1.10481  |        0.833333 |
| id_ms  | qwen25_7b  | definition | mean            | masked_minus_unrelated |        30 |  0.895135  |  0.609217   |  1.16609  |        0.9      |
| id_ms  | qwen25_7b  | definition | mean            | full_minus_masked      |        30 | -0.120195  | -0.346253   |  0.112821 |        0.433333 |
| id_ms  | qwen25_7b  | definition | mean            | full_minus_surface     |        30 |  0.70905   |  0.410043   |  1.02389  |        0.866667 |
| id_ms  | qwen25_7b  | definition | sum             | full_minus_unrelated   |        30 |  3.68397   |  1.88712    |  5.41054  |        0.866667 |
| id_ms  | qwen25_7b  | definition | sum             | masked_minus_unrelated |        30 |  4.1796    |  2.56864    |  5.70025  |        0.866667 |
| id_ms  | qwen25_7b  | definition | sum             | full_minus_masked      |        30 | -0.495624  | -1.73543    |  0.686399 |        0.466667 |
| id_ms  | qwen25_7b  | definition | sum             | full_minus_surface     |        30 |  3.4819    |  1.75163    |  5.40005  |        0.833333 |
| id_ms  | qwen25_7b  | refers     | mean            | full_minus_unrelated   |        30 |  0.953394  |  0.679807   |  1.24772  |        0.933333 |
| id_ms  | qwen25_7b  | refers     | mean            | masked_minus_unrelated |        30 |  0.927235  |  0.617103   |  1.24207  |        0.866667 |
| id_ms  | qwen25_7b  | refers     | mean            | full_minus_masked      |        30 |  0.0261587 | -0.224215   |  0.279994 |        0.566667 |
| id_ms  | qwen25_7b  | refers     | mean            | full_minus_surface     |        30 |  0.839478  |  0.52828    |  1.16996  |        0.866667 |
| id_ms  | qwen25_7b  | refers     | sum             | full_minus_unrelated   |        30 |  5.41204   |  3.82866    |  7.12637  |        0.9      |
| id_ms  | qwen25_7b  | refers     | sum             | masked_minus_unrelated |        30 |  5.47753   |  3.45877    |  7.56854  |        0.833333 |
| id_ms  | qwen25_7b  | refers     | sum             | full_minus_masked      |        30 | -0.065489  | -1.70966    |  1.62759  |        0.533333 |
| id_ms  | qwen25_7b  | refers     | sum             | full_minus_surface     |        30 |  5.01744   |  2.96812    |  7.3964   |        0.866667 |
| id_ms  | qwen3_8b   | bare       | mean            | full_minus_unrelated   |        30 |  8.44773   |  6.62408    | 10.2605   |        0.966667 |
| id_ms  | qwen3_8b   | bare       | mean            | masked_minus_unrelated |        30 |  5.28683   |  3.33632    |  7.17305  |        0.833333 |
| id_ms  | qwen3_8b   | bare       | mean            | full_minus_masked      |        30 |  3.1609    |  1.62937    |  4.82384  |        0.7      |
| id_ms  | qwen3_8b   | bare       | mean            | full_minus_surface     |        30 |  3.78166   |  2.58038    |  5.12082  |        0.866667 |
| id_ms  | qwen3_8b   | bare       | sum             | full_minus_unrelated   |        30 | 15.5491    | 12.1892     | 18.9221   |        0.966667 |
| id_ms  | qwen3_8b   | bare       | sum             | masked_minus_unrelated |        30 | 10.3428    |  6.95678    | 13.4623   |        0.866667 |
| id_ms  | qwen3_8b   | bare       | sum             | full_minus_masked      |        30 |  5.20625   |  2.38249    |  8.41167  |        0.7      |
| id_ms  | qwen3_8b   | bare       | sum             | full_minus_surface     |        30 |  7.81944   |  4.91406    | 10.9213   |        0.833333 |
| id_ms  | qwen3_8b   | definition | mean            | full_minus_unrelated   |        30 |  1.1009    |  0.76466    |  1.43437  |        0.866667 |
| id_ms  | qwen3_8b   | definition | mean            | masked_minus_unrelated |        30 |  0.606178  |  0.357325   |  0.852803 |        0.833333 |
| id_ms  | qwen3_8b   | definition | mean            | full_minus_masked      |        30 |  0.494726  |  0.217594   |  0.757134 |        0.733333 |
| id_ms  | qwen3_8b   | definition | mean            | full_minus_surface     |        30 |  0.447935  |  0.229488   |  0.670692 |        0.733333 |
| id_ms  | qwen3_8b   | definition | sum             | full_minus_unrelated   |        30 |  5.07927   |  3.67924    |  6.4202   |        0.9      |
| id_ms  | qwen3_8b   | definition | sum             | masked_minus_unrelated |        30 |  2.94085   |  2.00149    |  3.93845  |        0.9      |
| id_ms  | qwen3_8b   | definition | sum             | full_minus_masked      |        30 |  2.13842   |  0.951938   |  3.29507  |        0.7      |
| id_ms  | qwen3_8b   | definition | sum             | full_minus_surface     |        30 |  2.32726   |  1.27171    |  3.47966  |        0.766667 |
| id_ms  | qwen3_8b   | refers     | mean            | full_minus_unrelated   |        30 |  1.36875   |  1.02762    |  1.70048  |        0.933333 |
| id_ms  | qwen3_8b   | refers     | mean            | masked_minus_unrelated |        30 |  0.87008   |  0.583281   |  1.17162  |        0.866667 |
| id_ms  | qwen3_8b   | refers     | mean            | full_minus_masked      |        30 |  0.498665  |  0.258511   |  0.740632 |        0.766667 |
| id_ms  | qwen3_8b   | refers     | mean            | full_minus_surface     |        30 |  0.694625  |  0.442929   |  0.964354 |        0.833333 |
| id_ms  | qwen3_8b   | refers     | sum             | full_minus_unrelated   |        30 |  7.69754   |  5.86026    |  9.64115  |        0.933333 |
| id_ms  | qwen3_8b   | refers     | sum             | masked_minus_unrelated |        30 |  5.17      |  3.6874     |  6.86761  |        0.9      |
| id_ms  | qwen3_8b   | refers     | sum             | full_minus_masked      |        30 |  2.52754   |  1.3396     |  3.729    |        0.733333 |
| id_ms  | qwen3_8b   | refers     | sum             | full_minus_surface     |        30 |  3.85136   |  2.30358    |  5.4256   |        0.866667 |
| id_tl  | gemma3_12b | bare       | mean            | full_minus_unrelated   |        33 | 13.1337    | 10.722      | 15.4482   |        1        |
| id_tl  | gemma3_12b | bare       | mean            | masked_minus_unrelated |        33 |  5.41271   |  3.73957    |  7.16817  |        0.878788 |
| id_tl  | gemma3_12b | bare       | mean            | full_minus_masked      |        33 |  7.72098   |  6.04496    |  9.44334  |        0.939394 |
| id_tl  | gemma3_12b | bare       | mean            | full_minus_surface     |        33 |  1.95321   | -0.241693   |  4.18702  |        0.545455 |
| id_tl  | gemma3_12b | bare       | sum             | full_minus_unrelated   |        33 | 16.2693    | 13.6807     | 19.0672   |        0.969697 |
| id_tl  | gemma3_12b | bare       | sum             | masked_minus_unrelated |        33 |  7.05794   |  4.92801    |  9.38562  |        0.939394 |
| id_tl  | gemma3_12b | bare       | sum             | full_minus_masked      |        33 |  9.21137   |  7.32447    | 11.0553   |        0.969697 |
| id_tl  | gemma3_12b | bare       | sum             | full_minus_surface     |        33 |  1.43215   | -0.925763   |  3.80742  |        0.545455 |
| id_tl  | gemma3_12b | definition | mean            | full_minus_unrelated   |        33 |  3.47427   |  3.01907    |  3.95854  |        1        |
| id_tl  | gemma3_12b | definition | mean            | masked_minus_unrelated |        33 |  1.88687   |  1.41972    |  2.38017  |        0.969697 |
| id_tl  | gemma3_12b | definition | mean            | full_minus_masked      |        33 |  1.5874    |  1.30699    |  1.89717  |        1        |
| id_tl  | gemma3_12b | definition | mean            | full_minus_surface     |        33 |  0.887437  |  0.505381   |  1.2979   |        0.757576 |
| id_tl  | gemma3_12b | definition | sum             | full_minus_unrelated   |        33 | 14.6318    | 12.8339     | 16.6888   |        1        |
| id_tl  | gemma3_12b | definition | sum             | masked_minus_unrelated |        33 |  7.71161   |  5.77093    |  9.77643  |        0.939394 |
| id_tl  | gemma3_12b | definition | sum             | full_minus_masked      |        33 |  6.92017   |  5.61053    |  8.3109   |        1        |
| id_tl  | gemma3_12b | definition | sum             | full_minus_surface     |        33 |  3.48703   |  1.68751    |  5.24053  |        0.757576 |
| id_tl  | gemma3_12b | refers     | mean            | full_minus_unrelated   |        33 |  2.72664   |  2.39483    |  3.09565  |        1        |
| id_tl  | gemma3_12b | refers     | mean            | masked_minus_unrelated |        33 |  1.65782   |  1.27176    |  2.05282  |        0.939394 |
| id_tl  | gemma3_12b | refers     | mean            | full_minus_masked      |        33 |  1.06882   |  0.810066   |  1.3209   |        0.878788 |
| id_tl  | gemma3_12b | refers     | mean            | full_minus_surface     |        33 |  0.717813  |  0.444378   |  1.01484  |        0.787879 |
| id_tl  | gemma3_12b | refers     | sum             | full_minus_unrelated   |        33 | 14.5622    | 12.9738     | 16.372    |        1        |
| id_tl  | gemma3_12b | refers     | sum             | masked_minus_unrelated |        33 |  8.52675   |  6.54096    | 10.6485   |        0.969697 |
| id_tl  | gemma3_12b | refers     | sum             | full_minus_masked      |        33 |  6.03543   |  4.66814    |  7.443    |        0.939394 |
| id_tl  | gemma3_12b | refers     | sum             | full_minus_surface     |        33 |  3.72594   |  2.25954    |  5.2468   |        0.787879 |
| id_tl  | gemma3_4b  | bare       | mean            | full_minus_unrelated   |        33 | 20.4066    | 17.6447     | 22.938    |        0.969697 |
| id_tl  | gemma3_4b  | bare       | mean            | masked_minus_unrelated |        33 |  8.60624   |  6.26019    | 11.0797   |        0.909091 |
| id_tl  | gemma3_4b  | bare       | mean            | full_minus_masked      |        33 | 11.8004    |  9.37021    | 14.1984   |        0.939394 |
| id_tl  | gemma3_4b  | bare       | mean            | full_minus_surface     |        33 |  6.3185    |  2.84042    |  9.87728  |        0.757576 |
| id_tl  | gemma3_4b  | bare       | sum             | full_minus_unrelated   |        33 | 27.679     | 23.4363     | 32.0901   |        1        |
| id_tl  | gemma3_4b  | bare       | sum             | masked_minus_unrelated |        33 | 12.0103    |  7.99599    | 16.3386   |        0.878788 |
| id_tl  | gemma3_4b  | bare       | sum             | full_minus_masked      |        33 | 15.6686    | 12.4333     | 19.1847   |        0.969697 |
| id_tl  | gemma3_4b  | bare       | sum             | full_minus_surface     |        33 |  9.00603   |  5.02387    | 12.826    |        0.787879 |
| id_tl  | gemma3_4b  | definition | mean            | full_minus_unrelated   |        33 |  4.18081   |  3.50993    |  4.88598  |        0.969697 |
| id_tl  | gemma3_4b  | definition | mean            | masked_minus_unrelated |        33 |  2.01483   |  1.41421    |  2.6694   |        0.909091 |
| id_tl  | gemma3_4b  | definition | mean            | full_minus_masked      |        33 |  2.16598   |  1.71535    |  2.6197   |        0.969697 |
| id_tl  | gemma3_4b  | definition | mean            | full_minus_surface     |        33 |  1.52014   |  0.92137    |  2.12225  |        0.848485 |
| id_tl  | gemma3_4b  | definition | sum             | full_minus_unrelated   |        33 | 17.076     | 14.1582     | 20.3499   |        0.969697 |
| id_tl  | gemma3_4b  | definition | sum             | masked_minus_unrelated |        33 |  7.70302   |  5.51079    | 10.186    |        0.909091 |
| id_tl  | gemma3_4b  | definition | sum             | full_minus_masked      |        33 |  9.37295   |  7.61       | 11.2245   |        1        |
| id_tl  | gemma3_4b  | definition | sum             | full_minus_surface     |        33 |  5.65485   |  3.12129    |  8.20405  |        0.818182 |
| id_tl  | gemma3_4b  | refers     | mean            | full_minus_unrelated   |        33 |  3.98081   |  3.35838    |  4.64676  |        1        |
| id_tl  | gemma3_4b  | refers     | mean            | masked_minus_unrelated |        33 |  2.03971   |  1.49641    |  2.60744  |        0.939394 |
| id_tl  | gemma3_4b  | refers     | mean            | full_minus_masked      |        33 |  1.9411    |  1.51688    |  2.35539  |        0.939394 |
| id_tl  | gemma3_4b  | refers     | mean            | full_minus_surface     |        33 |  0.751727  |  0.293119   |  1.24868  |        0.636364 |
| id_tl  | gemma3_4b  | refers     | sum             | full_minus_unrelated   |        33 | 20.8769    | 17.7026     | 24.2665   |        1        |
| id_tl  | gemma3_4b  | refers     | sum             | masked_minus_unrelated |        33 | 10.3776    |  7.47292    | 13.4392   |        0.909091 |
| id_tl  | gemma3_4b  | refers     | sum             | full_minus_masked      |        33 | 10.4993    |  8.13061    | 12.7118   |        0.939394 |
| id_tl  | gemma3_4b  | refers     | sum             | full_minus_surface     |        33 |  3.67087   |  1.06799    |  6.28558  |        0.575758 |
| id_tl  | qwen25_7b  | bare       | mean            | full_minus_unrelated   |        33 |  4.92738   |  3.63667    |  6.16807  |        0.878788 |
| id_tl  | qwen25_7b  | bare       | mean            | masked_minus_unrelated |        33 |  2.22725   |  1.38511    |  3.06235  |        0.848485 |
| id_tl  | qwen25_7b  | bare       | mean            | full_minus_masked      |        33 |  2.70014   |  1.61527    |  3.77822  |        0.818182 |
| id_tl  | qwen25_7b  | bare       | mean            | full_minus_surface     |        33 |  1.82037   |  1.04488    |  2.63093  |        0.757576 |
| id_tl  | qwen25_7b  | bare       | sum             | full_minus_unrelated   |        33 |  6.55427   |  4.92087    |  8.35596  |        0.939394 |
| id_tl  | qwen25_7b  | bare       | sum             | masked_minus_unrelated |        33 |  3.37612   |  1.87221    |  4.9204   |        0.787879 |
| id_tl  | qwen25_7b  | bare       | sum             | full_minus_masked      |        33 |  3.17815   |  1.72507    |  4.54844  |        0.818182 |
| id_tl  | qwen25_7b  | bare       | sum             | full_minus_surface     |        33 |  2.81199   |  1.83689    |  3.88429  |        0.878788 |
| id_tl  | qwen25_7b  | definition | mean            | full_minus_unrelated   |        33 |  1.56487   |  1.20738    |  1.91893  |        0.969697 |
| id_tl  | qwen25_7b  | definition | mean            | masked_minus_unrelated |        33 |  0.700101  |  0.443232   |  0.968782 |        0.848485 |
| id_tl  | qwen25_7b  | definition | mean            | full_minus_masked      |        33 |  0.864773  |  0.54106    |  1.20307  |        0.818182 |
| id_tl  | qwen25_7b  | definition | mean            | full_minus_surface     |        33 |  0.779239  |  0.474221   |  1.07438  |        0.818182 |
| id_tl  | qwen25_7b  | definition | sum             | full_minus_unrelated   |        33 |  6.83967   |  5.22016    |  8.58579  |        0.969697 |
| id_tl  | qwen25_7b  | definition | sum             | masked_minus_unrelated |        33 |  3.22983   |  1.98838    |  4.62485  |        0.818182 |
| id_tl  | qwen25_7b  | definition | sum             | full_minus_masked      |        33 |  3.60984   |  2.21227    |  5.04928  |        0.787879 |
| id_tl  | qwen25_7b  | definition | sum             | full_minus_surface     |        33 |  3.58883   |  2.46216    |  4.73402  |        0.848485 |
| id_tl  | qwen25_7b  | refers     | mean            | full_minus_unrelated   |        33 |  1.86996   |  1.47611    |  2.24774  |        0.969697 |
| id_tl  | qwen25_7b  | refers     | mean            | masked_minus_unrelated |        33 |  1.04065   |  0.777318   |  1.31192  |        0.878788 |
| id_tl  | qwen25_7b  | refers     | mean            | full_minus_masked      |        33 |  0.829308  |  0.514302   |  1.13929  |        0.878788 |
| id_tl  | qwen25_7b  | refers     | mean            | full_minus_surface     |        33 |  0.322642  | -0.00542478 |  0.649826 |        0.666667 |
| id_tl  | qwen25_7b  | refers     | sum             | full_minus_unrelated   |        33 |  9.9949    |  8.03558    | 12.0089   |        0.969697 |
| id_tl  | qwen25_7b  | refers     | sum             | masked_minus_unrelated |        33 |  5.43361   |  4.03982    |  6.87926  |        0.878788 |
| id_tl  | qwen25_7b  | refers     | sum             | full_minus_masked      |        33 |  4.56128   |  2.86451    |  6.1542   |        0.878788 |
| id_tl  | qwen25_7b  | refers     | sum             | full_minus_surface     |        33 |  1.8161    |  0.179718   |  3.44818  |        0.666667 |
| id_tl  | qwen3_8b   | bare       | mean            | full_minus_unrelated   |        33 | 15.2101    | 12.9227     | 17.3303   |        0.969697 |
| id_tl  | qwen3_8b   | bare       | mean            | masked_minus_unrelated |        33 |  7.07316   |  5.56795    |  8.65668  |        0.939394 |
| id_tl  | qwen3_8b   | bare       | mean            | full_minus_masked      |        33 |  8.13696   |  6.05801    | 10.2329   |        0.939394 |
| id_tl  | qwen3_8b   | bare       | mean            | full_minus_surface     |        33 |  5.26867   |  3.56425    |  6.96729  |        0.848485 |
| id_tl  | qwen3_8b   | bare       | sum             | full_minus_unrelated   |        33 | 18.8745    | 16.6148     | 20.9543   |        0.969697 |
| id_tl  | qwen3_8b   | bare       | sum             | masked_minus_unrelated |        33 |  9.30568   |  7.53103    | 11.1025   |        0.939394 |
| id_tl  | qwen3_8b   | bare       | sum             | full_minus_masked      |        33 |  9.56883   |  6.99438    | 11.9101   |        0.939394 |
| id_tl  | qwen3_8b   | bare       | sum             | full_minus_surface     |        33 |  8.00683   |  5.78453    | 10.3091   |        0.909091 |
| id_tl  | qwen3_8b   | definition | mean            | full_minus_unrelated   |        33 |  1.69611   |  1.35857    |  2.01514  |        0.969697 |
| id_tl  | qwen3_8b   | definition | mean            | masked_minus_unrelated |        33 |  0.750124  |  0.540287   |  0.980161 |        0.878788 |
| id_tl  | qwen3_8b   | definition | mean            | full_minus_masked      |        33 |  0.945989  |  0.71847    |  1.15386  |        0.878788 |
| id_tl  | qwen3_8b   | definition | mean            | full_minus_surface     |        33 |  0.388078  |  0.17443    |  0.612943 |        0.727273 |
| id_tl  | qwen3_8b   | definition | sum             | full_minus_unrelated   |        33 |  7.24127   |  5.99628    |  8.52872  |        0.969697 |
| id_tl  | qwen3_8b   | definition | sum             | masked_minus_unrelated |        33 |  2.96337   |  2.06722    |  3.93364  |        0.878788 |
| id_tl  | qwen3_8b   | definition | sum             | full_minus_masked      |        33 |  4.27791   |  3.46395    |  5.00892  |        0.909091 |
| id_tl  | qwen3_8b   | definition | sum             | full_minus_surface     |        33 |  1.82437   |  0.821611   |  2.91942  |        0.727273 |
| id_tl  | qwen3_8b   | refers     | mean            | full_minus_unrelated   |        33 |  1.66391   |  1.38049    |  1.93312  |        0.969697 |
| id_tl  | qwen3_8b   | refers     | mean            | masked_minus_unrelated |        33 |  0.809613  |  0.586916   |  1.03499  |        0.909091 |
| id_tl  | qwen3_8b   | refers     | mean            | full_minus_masked      |        33 |  0.854293  |  0.615186   |  1.07149  |        0.939394 |
| id_tl  | qwen3_8b   | refers     | mean            | full_minus_surface     |        33 |  0.266445  |  0.0284217  |  0.503451 |        0.757576 |
| id_tl  | qwen3_8b   | refers     | sum             | full_minus_unrelated   |        33 |  8.61979   |  7.32605    |  9.91226  |        1        |
| id_tl  | qwen3_8b   | refers     | sum             | masked_minus_unrelated |        33 |  4.05628   |  2.93404    |  5.2649   |        0.909091 |
| id_tl  | qwen3_8b   | refers     | sum             | full_minus_masked      |        33 |  4.56351   |  3.32651    |  5.68255  |        0.969697 |
| id_tl  | qwen3_8b   | refers     | sum             | full_minus_surface     |        33 |  1.84704   |  0.786371   |  2.95713  |        0.787879 |

## Gate summary

| pair   | model      | contrast               |   variants |   positive_ci |   negative_ci |     median |
|:-------|:-----------|:-----------------------|-----------:|--------------:|--------------:|-----------:|
| id_ms  | gemma3_12b | full_minus_masked      |          6 |             6 |             0 |  3.22157   |
| id_ms  | gemma3_12b | full_minus_surface     |          6 |             4 |             0 |  1.67002   |
| id_ms  | gemma3_12b | full_minus_unrelated   |          6 |             6 |             0 |  9.68014   |
| id_ms  | gemma3_12b | masked_minus_unrelated |          6 |             6 |             0 |  4.70864   |
| id_ms  | gemma3_4b  | full_minus_masked      |          6 |             0 |             0 |  1.53752   |
| id_ms  | gemma3_4b  | full_minus_surface     |          6 |             6 |             0 |  4.39694   |
| id_ms  | gemma3_4b  | full_minus_unrelated   |          6 |             6 |             0 | 10.8385    |
| id_ms  | gemma3_4b  | masked_minus_unrelated |          6 |             6 |             0 |  8.98443   |
| id_ms  | qwen25_7b  | full_minus_masked      |          6 |             0 |             0 | -0.0196651 |
| id_ms  | qwen25_7b  | full_minus_surface     |          6 |             6 |             0 |  2.27086   |
| id_ms  | qwen25_7b  | full_minus_unrelated   |          6 |             6 |             0 |  2.77601   |
| id_ms  | qwen25_7b  | masked_minus_unrelated |          6 |             6 |             0 |  2.42415   |
| id_ms  | qwen3_8b   | full_minus_masked      |          6 |             6 |             0 |  2.33298   |
| id_ms  | qwen3_8b   | full_minus_surface     |          6 |             6 |             0 |  3.05446   |
| id_ms  | qwen3_8b   | full_minus_unrelated   |          6 |             6 |             0 |  6.38841   |
| id_ms  | qwen3_8b   | masked_minus_unrelated |          6 |             6 |             0 |  4.05542   |
| id_tl  | gemma3_12b | full_minus_masked      |          6 |             6 |             0 |  6.4778    |
| id_tl  | gemma3_12b | full_minus_surface     |          6 |             4 |             0 |  1.69268   |
| id_tl  | gemma3_12b | full_minus_unrelated   |          6 |             6 |             0 | 13.8479    |
| id_tl  | gemma3_12b | masked_minus_unrelated |          6 |             6 |             0 |  6.23532   |
| id_tl  | gemma3_4b  | full_minus_masked      |          6 |             6 |             0 |  9.93613   |
| id_tl  | gemma3_4b  | full_minus_surface     |          6 |             6 |             0 |  4.66286   |
| id_tl  | gemma3_4b  | full_minus_unrelated   |          6 |             6 |             0 | 18.7413    |
| id_tl  | gemma3_4b  | masked_minus_unrelated |          6 |             6 |             0 |  8.15463   |
| id_tl  | qwen25_7b  | full_minus_masked      |          6 |             6 |             0 |  2.93914   |
| id_tl  | qwen25_7b  | full_minus_surface     |          6 |             5 |             0 |  1.81824   |
| id_tl  | qwen25_7b  | full_minus_unrelated   |          6 |             6 |             0 |  5.74083   |
| id_tl  | qwen25_7b  | masked_minus_unrelated |          6 |             6 |             0 |  2.72854   |
| id_tl  | qwen3_8b   | full_minus_masked      |          6 |             6 |             0 |  4.42071   |
| id_tl  | qwen3_8b   | full_minus_surface     |          6 |             6 |             0 |  1.8357    |
| id_tl  | qwen3_8b   | full_minus_unrelated   |          6 |             6 |             0 |  7.93053   |
| id_tl  | qwen3_8b   | masked_minus_unrelated |          6 |             6 |             0 |  3.50983   |
