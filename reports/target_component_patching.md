# Target-span residual/attention/MLP patching

| model      | component   |   layer | group                | effect        |   n_items |     estimate |       ci_low |      ci_high |   positive_rate |
|:-----------|:------------|--------:|:---------------------|:--------------|----------:|-------------:|-------------:|-------------:|----------------:|
| gemma3_12b | attention   |       0 | false_friend         | semantic_main |        20 |  0.260486    | -0.825444    |  1.58556     |          0.55   |
| gemma3_12b | attention   |       0 | false_friend         | language_main |        20 |  5.09563     |  2.12575     |  9.13518     |          0.85   |
| gemma3_12b | attention   |       0 | monolingual_polysemy | semantic_main |        20 | -0.135727    | -0.299994    |  0.0060951   |          0.3    |
| gemma3_12b | attention   |       0 | true_friend          | language_main |        20 | -0.683905    | -1.8088      |  0.105819    |          0.35   |
| gemma3_12b | attention   |       0 | translation_control  | language_main |        16 | -0.177468    | -0.477634    |  0.10758     |          0.4375 |
| gemma3_12b | attention   |       4 | false_friend         | semantic_main |        20 |  0.0666803   | -0.198207    |  0.331844    |          0.5    |
| gemma3_12b | attention   |       4 | false_friend         | language_main |        20 |  0.0563101   | -0.15647     |  0.25975     |          0.6    |
| gemma3_12b | attention   |       4 | monolingual_polysemy | semantic_main |        20 |  0.126909    | -0.108584    |  0.430291    |          0.35   |
| gemma3_12b | attention   |       4 | true_friend          | language_main |        20 |  0.190457    |  0.0238512   |  0.360546    |          0.65   |
| gemma3_12b | attention   |       4 | translation_control  | language_main |        16 | -0.0687178   | -0.324243    |  0.181056    |          0.4375 |
| gemma3_12b | attention   |       8 | false_friend         | semantic_main |        20 |  0.298477    | -0.120518    |  0.926106    |          0.5    |
| gemma3_12b | attention   |       8 | false_friend         | language_main |        20 | -0.00945978  | -0.175414    |  0.182482    |          0.3    |
| gemma3_12b | attention   |       8 | monolingual_polysemy | semantic_main |        20 |  0.0172029   | -0.209104    |  0.254299    |          0.35   |
| gemma3_12b | attention   |       8 | true_friend          | language_main |        20 | -0.178498    | -0.480979    |  0.122169    |          0.5    |
| gemma3_12b | attention   |       8 | translation_control  | language_main |        16 | -0.354941    | -0.668519    | -0.0562738   |          0.25   |
| gemma3_12b | attention   |      12 | false_friend         | semantic_main |        20 | -0.0439227   | -0.208706    |  0.142995    |          0.35   |
| gemma3_12b | attention   |      12 | false_friend         | language_main |        20 | -0.169264    | -0.585963    |  0.14883     |          0.6    |
| gemma3_12b | attention   |      12 | monolingual_polysemy | semantic_main |        20 | -0.0295431   | -0.123591    |  0.0526478   |          0.4    |
| gemma3_12b | attention   |      12 | true_friend          | language_main |        20 |  0.193291    |  0.00915287  |  0.376387    |          0.65   |
| gemma3_12b | attention   |      12 | translation_control  | language_main |        16 | -0.0781115   | -0.302343    |  0.164161    |          0.3125 |
| gemma3_12b | attention   |      16 | false_friend         | semantic_main |        20 |  0.103742    | -0.105193    |  0.427135    |          0.5    |
| gemma3_12b | attention   |      16 | false_friend         | language_main |        20 | -0.150267    | -0.271559    | -0.0271785   |          0.2    |
| gemma3_12b | attention   |      16 | monolingual_polysemy | semantic_main |        20 | -0.0786631   | -0.203761    |  0.0268375   |          0.4    |
| gemma3_12b | attention   |      16 | true_friend          | language_main |        20 | -0.0392461   | -0.303183    |  0.242355    |          0.35   |
| gemma3_12b | attention   |      16 | translation_control  | language_main |        16 | -0.133362    | -0.375185    |  0.158628    |          0.25   |
| gemma3_12b | attention   |      20 | false_friend         | semantic_main |        20 |  0.0340707   | -0.0532845   |  0.122438    |          0.45   |
| gemma3_12b | attention   |      20 | false_friend         | language_main |        20 | -0.180388    | -0.262321    | -0.0976031   |          0.15   |
| gemma3_12b | attention   |      20 | monolingual_polysemy | semantic_main |        20 |  0.0174088   | -0.0993769   |  0.140139    |          0.4    |
| gemma3_12b | attention   |      20 | true_friend          | language_main |        20 | -0.0400244   | -0.249072    |  0.154472    |          0.5    |
| gemma3_12b | attention   |      20 | translation_control  | language_main |        16 | -0.0747467   | -0.437614    |  0.261907    |          0.5    |
| gemma3_12b | attention   |      24 | false_friend         | semantic_main |        20 |  0.0321119   | -0.0615237   |  0.117027    |          0.6    |
| gemma3_12b | attention   |      24 | false_friend         | language_main |        20 | -0.135595    | -0.281882    | -0.000773509 |          0.35   |
| gemma3_12b | attention   |      24 | monolingual_polysemy | semantic_main |        20 | -0.00193079  | -0.0944518   |  0.0834883   |          0.45   |
| gemma3_12b | attention   |      24 | true_friend          | language_main |        20 | -0.0308981   | -0.250674    |  0.202899    |          0.4    |
| gemma3_12b | attention   |      24 | translation_control  | language_main |        16 |  0.0291278   | -0.240401    |  0.311854    |          0.5    |
| gemma3_12b | attention   |      28 | false_friend         | semantic_main |        20 |  0.030317    | -0.0275483   |  0.0911365   |          0.5    |
| gemma3_12b | attention   |      28 | false_friend         | language_main |        20 |  0.0265651   | -0.0540574   |  0.112167    |          0.5    |
| gemma3_12b | attention   |      28 | monolingual_polysemy | semantic_main |        20 | -0.0371099   | -0.0788066   |  0.000305498 |          0.35   |
| gemma3_12b | attention   |      28 | true_friend          | language_main |        20 |  0.00985868  | -0.137626    |  0.172144    |          0.5    |
| gemma3_12b | attention   |      28 | translation_control  | language_main |        16 |  0.181852    |  0.00698684  |  0.352805    |          0.75   |
| gemma3_12b | attention   |      32 | false_friend         | semantic_main |        20 |  0.0561117   |  0.000581038 |  0.121146    |          0.55   |
| gemma3_12b | attention   |      32 | false_friend         | language_main |        20 | -0.00264949  | -0.0751517   |  0.0626814   |          0.45   |
| gemma3_12b | attention   |      32 | monolingual_polysemy | semantic_main |        20 |  0.0182508   | -0.0249845   |  0.0650979   |          0.5    |
| gemma3_12b | attention   |      32 | true_friend          | language_main |        20 | -0.0974661   | -0.270968    |  0.0689307   |          0.45   |
| gemma3_12b | attention   |      32 | translation_control  | language_main |        16 | -0.0599082   | -0.254293    |  0.140428    |          0.3125 |
| gemma3_12b | attention   |      36 | false_friend         | semantic_main |        20 |  0.0363539   | -0.0371272   |  0.107817    |          0.6    |
| gemma3_12b | attention   |      36 | false_friend         | language_main |        20 |  0.0242008   | -0.0331838   |  0.0867676   |          0.45   |
| gemma3_12b | attention   |      36 | monolingual_polysemy | semantic_main |        20 |  0.00255406  | -0.0442781   |  0.0462036   |          0.4    |
| gemma3_12b | attention   |      36 | true_friend          | language_main |        20 | -0.0162857   | -0.112245    |  0.080137    |          0.5    |
| gemma3_12b | attention   |      36 | translation_control  | language_main |        16 |  0.0394241   | -0.0340124   |  0.110959    |          0.6875 |
| gemma3_12b | attention   |      40 | false_friend         | semantic_main |        20 | -0.0333694   | -0.086985    |  0.0214375   |          0.3    |
| gemma3_12b | attention   |      40 | false_friend         | language_main |        20 | -0.0279362   | -0.0721672   |  0.0116042   |          0.4    |
| gemma3_12b | attention   |      40 | monolingual_polysemy | semantic_main |        20 | -0.0496312   | -0.0961244   | -0.0102579   |          0.35   |
| gemma3_12b | attention   |      40 | true_friend          | language_main |        20 | -0.072957    | -0.156509    |  0.00986001  |          0.15   |
| gemma3_12b | attention   |      40 | translation_control  | language_main |        16 |  0.0174042   | -0.148111    |  0.214426    |          0.375  |
| gemma3_12b | attention   |      44 | false_friend         | semantic_main |        20 |  0.0225533   | -0.0179612   |  0.070641    |          0.4    |
| gemma3_12b | attention   |      44 | false_friend         | language_main |        20 | -0.0426697   | -0.112452    |  0.0107133   |          0.45   |
| gemma3_12b | attention   |      44 | monolingual_polysemy | semantic_main |        20 |  0.000524259 | -0.0255604   |  0.024789    |          0.5    |
| gemma3_12b | attention   |      44 | true_friend          | language_main |        20 | -0.11634     | -0.193845    | -0.0482127   |          0.1    |
| gemma3_12b | attention   |      44 | translation_control  | language_main |        16 | -0.0740572   | -0.19917     |  0.0501601   |          0.3125 |
| gemma3_12b | attention   |      47 | false_friend         | semantic_main |        20 |  0           |  0           |  0           |          0      |
| gemma3_12b | attention   |      47 | false_friend         | language_main |        20 |  0           |  0           |  0           |          0      |
| gemma3_12b | attention   |      47 | monolingual_polysemy | semantic_main |        20 |  0           |  0           |  0           |          0      |
| gemma3_12b | attention   |      47 | true_friend          | language_main |        20 |  0           |  0           |  0           |          0      |
| gemma3_12b | attention   |      47 | translation_control  | language_main |        16 |  0           |  0           |  0           |          0      |
| gemma3_12b | mlp         |       0 | false_friend         | semantic_main |        20 |  0.307796    | -0.815088    |  1.70883     |          0.5    |
| gemma3_12b | mlp         |       0 | false_friend         | language_main |        20 |  2.31941     |  0.638913    |  5.01808     |          0.8    |
| gemma3_12b | mlp         |       0 | monolingual_polysemy | semantic_main |        20 |  0.0212571   | -0.07268     |  0.115073    |          0.4    |
| gemma3_12b | mlp         |       0 | true_friend          | language_main |        20 | -0.158756    | -1.64225     |  1.05616     |          0.45   |
| gemma3_12b | mlp         |       0 | translation_control  | language_main |        16 |  0.232277    | -0.34751     |  0.766639    |          0.625  |
| gemma3_12b | mlp         |       4 | false_friend         | semantic_main |        20 |  0.0164748   | -0.542095    |  0.429702    |          0.6    |
| gemma3_12b | mlp         |       4 | false_friend         | language_main |        20 |  2.17074     |  0.52769     |  4.65338     |          0.7    |
| gemma3_12b | mlp         |       4 | monolingual_polysemy | semantic_main |        20 |  0.224626    |  0.0128145   |  0.51893     |          0.55   |
| gemma3_12b | mlp         |       4 | true_friend          | language_main |        20 | -0.172486    | -0.894264    |  0.349766    |          0.4    |
| gemma3_12b | mlp         |       4 | translation_control  | language_main |        16 |  0.222593    | -0.133733    |  0.59721     |          0.625  |
| gemma3_12b | mlp         |       8 | false_friend         | semantic_main |        20 |  1.02549     |  0.503117    |  1.61461     |          0.75   |
| gemma3_12b | mlp         |       8 | false_friend         | language_main |        20 |  2.28443     |  0.922612    |  4.25669     |          0.85   |
| gemma3_12b | mlp         |       8 | monolingual_polysemy | semantic_main |        20 |  0.233913    |  0.00364031  |  0.463368    |          0.55   |
| gemma3_12b | mlp         |       8 | true_friend          | language_main |        20 | -0.188866    | -0.941421    |  0.542476    |          0.55   |
| gemma3_12b | mlp         |       8 | translation_control  | language_main |        16 |  0.175481    | -0.225922    |  0.580199    |          0.5    |
| gemma3_12b | mlp         |      12 | false_friend         | semantic_main |        20 |  0.787205    |  0.275763    |  1.47205     |          0.7    |
| gemma3_12b | mlp         |      12 | false_friend         | language_main |        20 |  1.2619      |  0.769839    |  1.86584     |          0.95   |
| gemma3_12b | mlp         |      12 | monolingual_polysemy | semantic_main |        20 |  0.107962    | -0.0691734   |  0.285295    |          0.45   |
| gemma3_12b | mlp         |      12 | true_friend          | language_main |        20 | -0.255774    | -0.786047    |  0.218164    |          0.45   |
| gemma3_12b | mlp         |      12 | translation_control  | language_main |        16 |  0.126507    | -0.252614    |  0.560054    |          0.4375 |
| gemma3_12b | mlp         |      16 | false_friend         | semantic_main |        20 |  0.44986     |  0.195888    |  0.720186    |          0.7    |
| gemma3_12b | mlp         |      16 | false_friend         | language_main |        20 |  0.584863    |  0.285931    |  0.976751    |          0.8    |
| gemma3_12b | mlp         |      16 | monolingual_polysemy | semantic_main |        20 | -0.00822394  | -0.283864    |  0.247967    |          0.4    |
| gemma3_12b | mlp         |      16 | true_friend          | language_main |        20 |  0.116468    | -0.317419    |  0.539238    |          0.55   |
| gemma3_12b | mlp         |      16 | translation_control  | language_main |        16 | -0.0218087   | -0.40239     |  0.311946    |          0.4375 |
| gemma3_12b | mlp         |      20 | false_friend         | semantic_main |        20 |  0.119678    | -0.0338522   |  0.289625    |          0.55   |
| gemma3_12b | mlp         |      20 | false_friend         | language_main |        20 |  0.44931     |  0.197762    |  0.750225    |          0.8    |
| gemma3_12b | mlp         |      20 | monolingual_polysemy | semantic_main |        20 |  0.108793    | -0.0228145   |  0.238227    |          0.55   |
| gemma3_12b | mlp         |      20 | true_friend          | language_main |        20 |  0.0599697   | -0.236627    |  0.362864    |          0.55   |
| gemma3_12b | mlp         |      20 | translation_control  | language_main |        16 | -0.294856    | -0.669318    |  0.0903086   |          0.25   |
| gemma3_12b | mlp         |      24 | false_friend         | semantic_main |        20 |  0.110758    | -0.0592492   |  0.278888    |          0.6    |
| gemma3_12b | mlp         |      24 | false_friend         | language_main |        20 |  0.142182    | -0.043947    |  0.314964    |          0.75   |
| gemma3_12b | mlp         |      24 | monolingual_polysemy | semantic_main |        20 |  0.0507267   | -0.0923175   |  0.202913    |          0.45   |
| gemma3_12b | mlp         |      24 | true_friend          | language_main |        20 |  0.36608     |  0.112738    |  0.646149    |          0.6    |
| gemma3_12b | mlp         |      24 | translation_control  | language_main |        16 |  0.322653    | -0.0388737   |  0.676654    |          0.5625 |
| gemma3_12b | mlp         |      28 | false_friend         | semantic_main |        20 |  0.0620612   |  0.00629382  |  0.123985    |          0.6    |
| gemma3_12b | mlp         |      28 | false_friend         | language_main |        20 |  0.104793    | -0.00814163  |  0.213548    |          0.6    |
| gemma3_12b | mlp         |      28 | monolingual_polysemy | semantic_main |        20 |  0.0192865   | -0.0411097   |  0.073118    |          0.6    |
| gemma3_12b | mlp         |      28 | true_friend          | language_main |        20 |  0.0773078   | -0.0736214   |  0.228396    |          0.55   |
| gemma3_12b | mlp         |      28 | translation_control  | language_main |        16 |  0.216034    | -0.0298441   |  0.447509    |          0.6875 |
| gemma3_12b | mlp         |      32 | false_friend         | semantic_main |        20 | -0.024507    | -0.085982    |  0.0432284   |          0.3    |
| gemma3_12b | mlp         |      32 | false_friend         | language_main |        20 | -0.00248361  | -0.0884653   |  0.0750496   |          0.55   |
| gemma3_12b | mlp         |      32 | monolingual_polysemy | semantic_main |        20 | -0.0335643   | -0.108013    |  0.0336517   |          0.35   |
| gemma3_12b | mlp         |      32 | true_friend          | language_main |        20 | -0.0261497   | -0.159786    |  0.0899278   |          0.5    |
| gemma3_12b | mlp         |      32 | translation_control  | language_main |        16 |  0.0225648   | -0.152234    |  0.205156    |          0.5    |
| gemma3_12b | mlp         |      36 | false_friend         | semantic_main |        20 | -0.0145429   | -0.0756288   |  0.0463768   |          0.45   |
| gemma3_12b | mlp         |      36 | false_friend         | language_main |        20 | -0.0299571   | -0.111382    |  0.0435677   |          0.5    |
| gemma3_12b | mlp         |      36 | monolingual_polysemy | semantic_main |        20 | -0.0187922   | -0.0706302   |  0.0275535   |          0.3    |
| gemma3_12b | mlp         |      36 | true_friend          | language_main |        20 |  0.16908     |  0.0517929   |  0.292094    |          0.65   |
| gemma3_12b | mlp         |      36 | translation_control  | language_main |        16 | -0.0625077   | -0.246254    |  0.0968212   |          0.4375 |
| gemma3_12b | mlp         |      40 | false_friend         | semantic_main |        20 |  0.0283016   | -0.0100799   |  0.0628197   |          0.7    |
| gemma3_12b | mlp         |      40 | false_friend         | language_main |        20 |  0.022798    | -0.0463007   |  0.0930245   |          0.55   |
| gemma3_12b | mlp         |      40 | monolingual_polysemy | semantic_main |        20 |  0.0158163   | -0.0240376   |  0.0567205   |          0.45   |
| gemma3_12b | mlp         |      40 | true_friend          | language_main |        20 |  0.0241865   | -0.0993795   |  0.158572    |          0.4    |
| gemma3_12b | mlp         |      40 | translation_control  | language_main |        16 | -0.0144283   | -0.168735    |  0.130931    |          0.4375 |
| gemma3_12b | mlp         |      44 | false_friend         | semantic_main |        20 | -0.00749834  | -0.0532212   |  0.0400369   |          0.4    |
| gemma3_12b | mlp         |      44 | false_friend         | language_main |        20 | -0.0113384   | -0.0664052   |  0.0422019   |          0.4    |
| gemma3_12b | mlp         |      44 | monolingual_polysemy | semantic_main |        20 |  0.00327772  | -0.0404799   |  0.0384297   |          0.5    |
| gemma3_12b | mlp         |      44 | true_friend          | language_main |        20 |  0.0257983   | -0.0448055   |  0.0955786   |          0.55   |
| gemma3_12b | mlp         |      44 | translation_control  | language_main |        16 | -0.0329805   | -0.161513    |  0.0959261   |          0.4375 |
| gemma3_12b | mlp         |      47 | false_friend         | semantic_main |        20 |  0           |  0           |  0           |          0      |
| gemma3_12b | mlp         |      47 | false_friend         | language_main |        20 |  0           |  0           |  0           |          0      |
| gemma3_12b | mlp         |      47 | monolingual_polysemy | semantic_main |        20 |  0           |  0           |  0           |          0      |
| gemma3_12b | mlp         |      47 | true_friend          | language_main |        20 |  0           |  0           |  0           |          0      |
| gemma3_12b | mlp         |      47 | translation_control  | language_main |        16 |  0           |  0           |  0           |          0      |
| gemma3_12b | residual    |       0 | false_friend         | semantic_main |        20 |  0.0019068   | -0.961749    |  0.830518    |          0.45   |
| gemma3_12b | residual    |       0 | false_friend         | language_main |        20 |  1.02594     | -0.302428    |  2.51447     |          0.7    |
| gemma3_12b | residual    |       0 | monolingual_polysemy | semantic_main |        20 |  0.154444    | -0.0822595   |  0.49811     |          0.4    |
| gemma3_12b | residual    |       0 | true_friend          | language_main |        20 | -1.91493     | -6.72636     |  2.21509     |          0.55   |
| gemma3_12b | residual    |       0 | translation_control  | language_main |        16 |  3.61141     |  1.56154     |  5.97526     |          0.875  |
| gemma3_12b | residual    |       4 | false_friend         | semantic_main |        20 |  0.711178    |  0.0801542   |  1.52971     |          0.55   |
| gemma3_12b | residual    |       4 | false_friend         | language_main |        20 |  7.20693     |  4.13873     | 10.8027      |          0.8    |
| gemma3_12b | residual    |       4 | monolingual_polysemy | semantic_main |        20 |  0.272873    | -0.204949    |  0.820812    |          0.35   |
| gemma3_12b | residual    |       4 | true_friend          | language_main |        20 | -3.5621      | -7.75336     | -0.0358621   |          0.3    |
| gemma3_12b | residual    |       4 | translation_control  | language_main |        16 |  2.4919      |  1.04322     |  4.15031     |          0.75   |
| gemma3_12b | residual    |       8 | false_friend         | semantic_main |        20 |  2.45017     |  0.824618    |  4.01756     |          0.7    |
| gemma3_12b | residual    |       8 | false_friend         | language_main |        20 | 12.0192      |  7.08691     | 17.4384      |          0.95   |
| gemma3_12b | residual    |       8 | monolingual_polysemy | semantic_main |        20 |  0.855549    | -0.0162033   |  1.7947      |          0.55   |
| gemma3_12b | residual    |       8 | true_friend          | language_main |        20 | -3.46045     | -6.42511     | -0.754975    |          0.3    |
| gemma3_12b | residual    |       8 | translation_control  | language_main |        16 | -0.568825    | -2.14302     |  0.76459     |          0.5    |
| gemma3_12b | residual    |      12 | false_friend         | semantic_main |        20 |  2.48283     |  0.246977    |  5.07981     |          0.65   |
| gemma3_12b | residual    |      12 | false_friend         | language_main |        20 | 10.9067      |  6.43275     | 15.9868      |          0.95   |
| gemma3_12b | residual    |      12 | monolingual_polysemy | semantic_main |        20 |  0.777079    | -0.0756641   |  1.7337      |          0.45   |
| gemma3_12b | residual    |      12 | true_friend          | language_main |        20 | -0.82558     | -2.66786     |  0.906017    |          0.5    |
| gemma3_12b | residual    |      12 | translation_control  | language_main |        16 |  1.56613     | -0.129946    |  3.56716     |          0.625  |
| gemma3_12b | residual    |      16 | false_friend         | semantic_main |        20 |  5.89585     |  2.8399      |  9.32148     |          0.7    |
| gemma3_12b | residual    |      16 | false_friend         | language_main |        20 |  9.61056     |  5.83451     | 13.634       |          0.9    |
| gemma3_12b | residual    |      16 | monolingual_polysemy | semantic_main |        20 |  0.61448     | -0.0589081   |  1.36412     |          0.5    |
| gemma3_12b | residual    |      16 | true_friend          | language_main |        20 | -0.734657    | -2.15494     |  0.644555    |          0.4    |
| gemma3_12b | residual    |      16 | translation_control  | language_main |        16 | -0.238103    | -1.90304     |  1.39826     |          0.5    |
| gemma3_12b | residual    |      20 | false_friend         | semantic_main |        20 |  4.66469     |  2.26106     |  7.18014     |          0.7    |
| gemma3_12b | residual    |      20 | false_friend         | language_main |        20 |  6.93238     |  4.14437     | 10.0622      |          0.9    |
| gemma3_12b | residual    |      20 | monolingual_polysemy | semantic_main |        20 |  0.661172    |  0.169374    |  1.23985     |          0.55   |
| gemma3_12b | residual    |      20 | true_friend          | language_main |        20 | -0.304118    | -1.89171     |  1.21166     |          0.4    |
| gemma3_12b | residual    |      20 | translation_control  | language_main |        16 | -0.156642    | -1.12768     |  0.549705    |          0.5625 |
| gemma3_12b | residual    |      24 | false_friend         | semantic_main |        20 |  3.38898     |  1.46043     |  5.56665     |          0.75   |
| gemma3_12b | residual    |      24 | false_friend         | language_main |        20 |  4.99887     |  2.90985     |  7.64993     |          0.95   |
| gemma3_12b | residual    |      24 | monolingual_polysemy | semantic_main |        20 |  0.682027    |  0.24199     |  1.16577     |          0.7    |
| gemma3_12b | residual    |      24 | true_friend          | language_main |        20 |  0.288144    | -0.650331    |  1.31174     |          0.5    |
| gemma3_12b | residual    |      24 | translation_control  | language_main |        16 |  0.459338    | -0.166165    |  1.04613     |          0.6875 |
| gemma3_12b | residual    |      28 | false_friend         | semantic_main |        20 |  0.316265    |  0.0231606   |  0.673157    |          0.55   |
| gemma3_12b | residual    |      28 | false_friend         | language_main |        20 |  0.614051    |  0.192625    |  1.08338     |          0.75   |
| gemma3_12b | residual    |      28 | monolingual_polysemy | semantic_main |        20 |  0.0624674   | -0.0624971   |  0.189315    |          0.55   |
| gemma3_12b | residual    |      28 | true_friend          | language_main |        20 |  0.297717    |  0.0749691   |  0.527812    |          0.75   |
| gemma3_12b | residual    |      28 | translation_control  | language_main |        16 |  0.582754    |  0.331258    |  0.833606    |          0.8125 |
| gemma3_12b | residual    |      32 | false_friend         | semantic_main |        20 |  0.19828     |  0.0176139   |  0.441777    |          0.6    |
| gemma3_12b | residual    |      32 | false_friend         | language_main |        20 |  0.271334    |  0.018994    |  0.583097    |          0.65   |
| gemma3_12b | residual    |      32 | monolingual_polysemy | semantic_main |        20 | -0.0360432   | -0.103781    |  0.0397336   |          0.25   |
| gemma3_12b | residual    |      32 | true_friend          | language_main |        20 |  0.194154    | -0.0134544   |  0.410511    |          0.5    |
| gemma3_12b | residual    |      32 | translation_control  | language_main |        16 |  0.396276    |  0.11944     |  0.671161    |          0.6875 |
| gemma3_12b | residual    |      36 | false_friend         | semantic_main |        20 |  0.0350486   | -0.088981    |  0.198347    |          0.45   |
| gemma3_12b | residual    |      36 | false_friend         | language_main |        20 |  0.154232    |  0.0105293   |  0.310134    |          0.65   |
| gemma3_12b | residual    |      36 | monolingual_polysemy | semantic_main |        20 | -0.00189531  | -0.0735287   |  0.0832037   |          0.3    |
| gemma3_12b | residual    |      36 | true_friend          | language_main |        20 |  0.204355    | -0.0232176   |  0.434737    |          0.65   |
| gemma3_12b | residual    |      36 | translation_control  | language_main |        16 |  0.482294    |  0.175819    |  0.800029    |          0.6875 |
| gemma3_12b | residual    |      40 | false_friend         | semantic_main |        20 |  0.0044616   | -0.0598764   |  0.0662783   |          0.55   |
| gemma3_12b | residual    |      40 | false_friend         | language_main |        20 |  0.00751347  | -0.0797014   |  0.0911302   |          0.55   |
| gemma3_12b | residual    |      40 | monolingual_polysemy | semantic_main |        20 |  0.0170854   | -0.0373455   |  0.0812456   |          0.35   |
| gemma3_12b | residual    |      40 | true_friend          | language_main |        20 |  0.176762    | -0.0212834   |  0.371505    |          0.6    |
| gemma3_12b | residual    |      40 | translation_control  | language_main |        16 |  0.124175    | -0.0476695   |  0.274156    |          0.75   |
| gemma3_12b | residual    |      44 | false_friend         | semantic_main |        20 |  0.0109295   | -0.0704983   |  0.0852001   |          0.5    |
| gemma3_12b | residual    |      44 | false_friend         | language_main |        20 | -0.00860785  | -0.0939377   |  0.0725745   |          0.55   |
| gemma3_12b | residual    |      44 | monolingual_polysemy | semantic_main |        20 |  0.023687    | -0.0217167   |  0.0790647   |          0.45   |
| gemma3_12b | residual    |      44 | true_friend          | language_main |        20 |  0.0241027   | -0.0946482   |  0.150217    |          0.4    |
| gemma3_12b | residual    |      44 | translation_control  | language_main |        16 | -0.0542956   | -0.136283    |  0.0327185   |          0.375  |
| gemma3_12b | residual    |      47 | false_friend         | semantic_main |        20 |  0           |  0           |  0           |          0      |
| gemma3_12b | residual    |      47 | false_friend         | language_main |        20 |  0           |  0           |  0           |          0      |
| gemma3_12b | residual    |      47 | monolingual_polysemy | semantic_main |        20 |  0           |  0           |  0           |          0      |
| gemma3_12b | residual    |      47 | true_friend          | language_main |        20 |  0           |  0           |  0           |          0      |
| gemma3_12b | residual    |      47 | translation_control  | language_main |        16 |  0           |  0           |  0           |          0      |
| qwen3_8b   | attention   |       0 | false_friend         | semantic_main |        20 | -0.0488502   | -0.411387    |  0.297016    |          0.45   |
| qwen3_8b   | attention   |       0 | false_friend         | language_main |        20 |  1.05853     |  0.142802    |  2.54395     |          0.65   |
| qwen3_8b   | attention   |       0 | monolingual_polysemy | semantic_main |        20 |  0.134145    |  0.00197591  |  0.320689    |          0.5    |
| qwen3_8b   | attention   |       0 | true_friend          | language_main |        20 |  0.0633542   | -0.504731    |  0.644332    |          0.55   |
| qwen3_8b   | attention   |       0 | translation_control  | language_main |        16 |  0.297407    | -0.227528    |  0.857392    |          0.5    |
| qwen3_8b   | attention   |       4 | false_friend         | semantic_main |        20 |  0.105798    | -0.0458047   |  0.249278    |          0.65   |
| qwen3_8b   | attention   |       4 | false_friend         | language_main |        20 |  0.777349    |  0.13895     |  1.67173     |          0.6    |
| qwen3_8b   | attention   |       4 | monolingual_polysemy | semantic_main |        20 |  0.00870229  | -0.122285    |  0.10363     |          0.55   |
| qwen3_8b   | attention   |       4 | true_friend          | language_main |        20 | -0.21112     | -0.316807    | -0.102108    |          0.25   |
| qwen3_8b   | attention   |       4 | translation_control  | language_main |        16 | -0.0272842   | -0.142322    |  0.074984    |          0.625  |
| qwen3_8b   | attention   |       8 | false_friend         | semantic_main |        20 |  0.0282944   | -0.148451    |  0.202671    |          0.35   |
| qwen3_8b   | attention   |       8 | false_friend         | language_main |        20 |  0.0227412   | -0.0571265   |  0.11273     |          0.6    |
| qwen3_8b   | attention   |       8 | monolingual_polysemy | semantic_main |        20 |  0.00549896  | -0.0420691   |  0.0533671   |          0.4    |
| qwen3_8b   | attention   |       8 | true_friend          | language_main |        20 |  0.0280202   | -0.141869    |  0.183396    |          0.5    |
| qwen3_8b   | attention   |       8 | translation_control  | language_main |        16 |  0.110866    | -0.0455044   |  0.284209    |          0.5    |
| qwen3_8b   | attention   |      12 | false_friend         | semantic_main |        20 | -0.0124268   | -0.0898906   |  0.061982    |          0.35   |
| qwen3_8b   | attention   |      12 | false_friend         | language_main |        20 |  0.0283052   | -0.0726566   |  0.134516    |          0.4    |
| qwen3_8b   | attention   |      12 | monolingual_polysemy | semantic_main |        20 | -0.00840145  | -0.078227    |  0.0679394   |          0.25   |
| qwen3_8b   | attention   |      12 | true_friend          | language_main |        20 |  0.0886622   | -0.0554733   |  0.235061    |          0.5    |
| qwen3_8b   | attention   |      12 | translation_control  | language_main |        16 | -0.0634602   | -0.188724    |  0.0690238   |          0.4375 |
| qwen3_8b   | attention   |      16 | false_friend         | semantic_main |        20 |  0.0542869   | -0.0252272   |  0.143831    |          0.6    |
| qwen3_8b   | attention   |      16 | false_friend         | language_main |        20 | -0.0838628   | -0.187565    |  0.00951584  |          0.35   |
| qwen3_8b   | attention   |      16 | monolingual_polysemy | semantic_main |        20 | -0.0518632   | -0.106565    | -0.00514816  |          0.35   |
| qwen3_8b   | attention   |      16 | true_friend          | language_main |        20 |  0.0113924   | -0.0891996   |  0.105857    |          0.5    |
| qwen3_8b   | attention   |      16 | translation_control  | language_main |        16 | -0.0780064   | -0.216154    |  0.0627776   |          0.5    |
| qwen3_8b   | attention   |      20 | false_friend         | semantic_main |        20 | -0.0376765   | -0.0938442   |  0.0149173   |          0.35   |
| qwen3_8b   | attention   |      20 | false_friend         | language_main |        20 | -0.0454987   | -0.10366     |  0.0109395   |          0.45   |
| qwen3_8b   | attention   |      20 | monolingual_polysemy | semantic_main |        20 | -0.00180078  | -0.0277508   |  0.0232552   |          0.45   |
| qwen3_8b   | attention   |      20 | true_friend          | language_main |        20 | -0.0421341   | -0.113728    |  0.0258215   |          0.35   |
| qwen3_8b   | attention   |      20 | translation_control  | language_main |        16 | -0.00633606  | -0.128018    |  0.108013    |          0.4375 |
| qwen3_8b   | attention   |      24 | false_friend         | semantic_main |        20 |  0.0285405   | -0.00222497  |  0.0603806   |          0.65   |
| qwen3_8b   | attention   |      24 | false_friend         | language_main |        20 |  0.127673    |  0.0595768   |  0.208603    |          0.8    |
| qwen3_8b   | attention   |      24 | monolingual_polysemy | semantic_main |        20 | -0.00943568  | -0.0414072   |  0.0208025   |          0.3    |
| qwen3_8b   | attention   |      24 | true_friend          | language_main |        20 |  0.0265776   | -0.0901248   |  0.15629     |          0.45   |
| qwen3_8b   | attention   |      24 | translation_control  | language_main |        16 |  0.0680261   | -0.0276061   |  0.163466    |          0.625  |
| qwen3_8b   | attention   |      28 | false_friend         | semantic_main |        20 |  0.0203929   | -0.00307471  |  0.0422871   |          0.6    |
| qwen3_8b   | attention   |      28 | false_friend         | language_main |        20 |  0.0111595   | -0.0104312   |  0.0336399   |          0.6    |
| qwen3_8b   | attention   |      28 | monolingual_polysemy | semantic_main |        20 | -0.023417    | -0.0515382   |  0.00307634  |          0.25   |
| qwen3_8b   | attention   |      28 | true_friend          | language_main |        20 | -0.0448984   | -0.101784    |  0.0121106   |          0.3    |
| qwen3_8b   | attention   |      28 | translation_control  | language_main |        16 |  0.0254918   | -0.0411998   |  0.0876238   |          0.6875 |
| qwen3_8b   | attention   |      32 | false_friend         | semantic_main |        20 | -0.0270771   | -0.0490507   | -0.00704815  |          0.2    |
| qwen3_8b   | attention   |      32 | false_friend         | language_main |        20 |  0.00800606  | -0.0132964   |  0.0278788   |          0.55   |
| qwen3_8b   | attention   |      32 | monolingual_polysemy | semantic_main |        20 |  0.00322126  | -0.0103873   |  0.0171866   |          0.45   |
| qwen3_8b   | attention   |      32 | true_friend          | language_main |        20 | -0.0289176   | -0.0872145   |  0.0297896   |          0.25   |
| qwen3_8b   | attention   |      32 | translation_control  | language_main |        16 |  0.0675401   |  0.0119826   |  0.138807    |          0.5    |
| qwen3_8b   | attention   |      35 | false_friend         | semantic_main |        20 |  0           |  0           |  0           |          0      |
| qwen3_8b   | attention   |      35 | false_friend         | language_main |        20 |  0           |  0           |  0           |          0      |
| qwen3_8b   | attention   |      35 | monolingual_polysemy | semantic_main |        20 |  0           |  0           |  0           |          0      |
| qwen3_8b   | attention   |      35 | true_friend          | language_main |        20 |  0           |  0           |  0           |          0      |
| qwen3_8b   | attention   |      35 | translation_control  | language_main |        16 |  0           |  0           |  0           |          0      |
| qwen3_8b   | mlp         |       0 | false_friend         | semantic_main |        20 |  0.202201    | -0.151266    |  0.547717    |          0.6    |
| qwen3_8b   | mlp         |       0 | false_friend         | language_main |        20 |  0.215266    | -0.135374    |  0.610307    |          0.65   |
| qwen3_8b   | mlp         |       0 | monolingual_polysemy | semantic_main |        20 |  0.123214    | -0.00771703  |  0.281264    |          0.45   |
| qwen3_8b   | mlp         |       0 | true_friend          | language_main |        20 | -0.385997    | -1.59942     |  0.69956     |          0.35   |
| qwen3_8b   | mlp         |       0 | translation_control  | language_main |        16 |  1.315       |  0.535594    |  2.1184      |          0.75   |
| qwen3_8b   | mlp         |       4 | false_friend         | semantic_main |        20 |  0.118514    | -0.171778    |  0.505847    |          0.5    |
| qwen3_8b   | mlp         |       4 | false_friend         | language_main |        20 |  2.52136     |  0.781707    |  4.84281     |          0.85   |
| qwen3_8b   | mlp         |       4 | monolingual_polysemy | semantic_main |        20 |  0.0340725   | -0.0647369   |  0.140913    |          0.5    |
| qwen3_8b   | mlp         |       4 | true_friend          | language_main |        20 |  0.0619421   | -0.411079    |  0.413664    |          0.6    |
| qwen3_8b   | mlp         |       4 | translation_control  | language_main |        16 | -0.476705    | -0.876609    | -0.127834    |          0.25   |
| qwen3_8b   | mlp         |       8 | false_friend         | semantic_main |        20 |  0.369233    |  0.135785    |  0.645861    |          0.65   |
| qwen3_8b   | mlp         |       8 | false_friend         | language_main |        20 |  1.34485     |  0.689312    |  2.11683     |          0.9    |
| qwen3_8b   | mlp         |       8 | monolingual_polysemy | semantic_main |        20 |  0.0721834   | -0.119542    |  0.241537    |          0.55   |
| qwen3_8b   | mlp         |       8 | true_friend          | language_main |        20 | -0.271976    | -0.572941    | -0.00145055  |          0.5    |
| qwen3_8b   | mlp         |       8 | translation_control  | language_main |        16 |  0.0543253   | -0.198424    |  0.310811    |          0.625  |
| qwen3_8b   | mlp         |      12 | false_friend         | semantic_main |        20 |  0.200139    |  0.0399813   |  0.364826    |          0.6    |
| qwen3_8b   | mlp         |      12 | false_friend         | language_main |        20 |  0.319489    |  0.122013    |  0.530204    |          0.7    |
| qwen3_8b   | mlp         |      12 | monolingual_polysemy | semantic_main |        20 | -0.0961954   | -0.220751    |  0.0190565   |          0.25   |
| qwen3_8b   | mlp         |      12 | true_friend          | language_main |        20 | -0.0913444   | -0.311826    |  0.20422     |          0.2    |
| qwen3_8b   | mlp         |      12 | translation_control  | language_main |        16 |  0.200923    | -0.102911    |  0.531189    |          0.625  |
| qwen3_8b   | mlp         |      16 | false_friend         | semantic_main |        20 |  0.0148427   | -0.0480102   |  0.0750484   |          0.6    |
| qwen3_8b   | mlp         |      16 | false_friend         | language_main |        20 |  0.222755    |  0.0763653   |  0.389889    |          0.75   |
| qwen3_8b   | mlp         |      16 | monolingual_polysemy | semantic_main |        20 |  0.0108706   | -0.0850328   |  0.0937467   |          0.55   |
| qwen3_8b   | mlp         |      16 | true_friend          | language_main |        20 | -0.0771683   | -0.230716    |  0.0963716   |          0.3    |
| qwen3_8b   | mlp         |      16 | translation_control  | language_main |        16 | -0.187154    | -0.325831    | -0.052849    |          0.25   |
| qwen3_8b   | mlp         |      20 | false_friend         | semantic_main |        20 |  0.0754765   | -0.0300681   |  0.184232    |          0.65   |
| qwen3_8b   | mlp         |      20 | false_friend         | language_main |        20 |  0.133641    |  0.0148953   |  0.256589    |          0.65   |
| qwen3_8b   | mlp         |      20 | monolingual_polysemy | semantic_main |        20 |  0.0119404   | -0.0558186   |  0.0968339   |          0.4    |
| qwen3_8b   | mlp         |      20 | true_friend          | language_main |        20 |  0.0204598   | -0.102128    |  0.1648      |          0.35   |
| qwen3_8b   | mlp         |      20 | translation_control  | language_main |        16 |  0.000342842 | -0.160961    |  0.158764    |          0.5    |
| qwen3_8b   | mlp         |      24 | false_friend         | semantic_main |        20 |  0.0258796   | -0.0564416   |  0.112406    |          0.5    |
| qwen3_8b   | mlp         |      24 | false_friend         | language_main |        20 |  0.205922    |  0.0832396   |  0.346972    |          0.7    |
| qwen3_8b   | mlp         |      24 | monolingual_polysemy | semantic_main |        20 |  0.0125787   | -0.0455152   |  0.0664889   |          0.45   |
| qwen3_8b   | mlp         |      24 | true_friend          | language_main |        20 | -0.0173413   | -0.199738    |  0.125575    |          0.55   |
| qwen3_8b   | mlp         |      24 | translation_control  | language_main |        16 |  0.0172384   | -0.0771877   |  0.118774    |          0.4375 |
| qwen3_8b   | mlp         |      28 | false_friend         | semantic_main |        20 |  0.0170328   | -0.0103723   |  0.0476988   |          0.45   |
| qwen3_8b   | mlp         |      28 | false_friend         | language_main |        20 |  0.00844098  | -0.0193457   |  0.0437313   |          0.4    |
| qwen3_8b   | mlp         |      28 | monolingual_polysemy | semantic_main |        20 |  0.00828862  | -0.0180857   |  0.0325465   |          0.6    |
| qwen3_8b   | mlp         |      28 | true_friend          | language_main |        20 |  0.00928166  | -0.0687217   |  0.0806408   |          0.55   |
| qwen3_8b   | mlp         |      28 | translation_control  | language_main |        16 | -0.0448893   | -0.125978    |  0.0387785   |          0.3125 |
| qwen3_8b   | mlp         |      32 | false_friend         | semantic_main |        20 | -0.0047058   | -0.0319422   |  0.0203965   |          0.5    |
| qwen3_8b   | mlp         |      32 | false_friend         | language_main |        20 |  0.00140229  | -0.037802    |  0.0377498   |          0.6    |
| qwen3_8b   | mlp         |      32 | monolingual_polysemy | semantic_main |        20 | -0.00566475  | -0.0180468   |  0.005187    |          0.35   |
| qwen3_8b   | mlp         |      32 | true_friend          | language_main |        20 | -0.0210645   | -0.0746027   |  0.0328228   |          0.4    |
| qwen3_8b   | mlp         |      32 | translation_control  | language_main |        16 |  0.0234099   | -0.0252674   |  0.0769179   |          0.5    |
| qwen3_8b   | mlp         |      35 | false_friend         | semantic_main |        20 |  0           |  0           |  0           |          0      |
| qwen3_8b   | mlp         |      35 | false_friend         | language_main |        20 |  0           |  0           |  0           |          0      |
| qwen3_8b   | mlp         |      35 | monolingual_polysemy | semantic_main |        20 |  0           |  0           |  0           |          0      |
| qwen3_8b   | mlp         |      35 | true_friend          | language_main |        20 |  0           |  0           |  0           |          0      |
| qwen3_8b   | mlp         |      35 | translation_control  | language_main |        16 |  0           |  0           |  0           |          0      |
| qwen3_8b   | residual    |       0 | false_friend         | semantic_main |        20 |  0.494231    |  0.0373777   |  1.13276     |          0.75   |
| qwen3_8b   | residual    |       0 | false_friend         | language_main |        20 |  0.322235    | -0.119097    |  0.927767    |          0.45   |
| qwen3_8b   | residual    |       0 | monolingual_polysemy | semantic_main |        20 |  0.114544    | -0.0446878   |  0.302583    |          0.5    |
| qwen3_8b   | residual    |       0 | true_friend          | language_main |        20 | -0.435865    | -1.67635     |  0.704283    |          0.35   |
| qwen3_8b   | residual    |       0 | translation_control  | language_main |        16 |  1.69132     |  0.598651    |  2.79222     |          0.6875 |
| qwen3_8b   | residual    |       4 | false_friend         | semantic_main |        20 |  0.811115    | -0.133134    |  1.99917     |          0.6    |
| qwen3_8b   | residual    |       4 | false_friend         | language_main |        20 |  8.54177     |  4.34239     | 13.595       |          0.95   |
| qwen3_8b   | residual    |       4 | monolingual_polysemy | semantic_main |        20 |  0.368042    |  0.0388024   |  0.722508    |          0.55   |
| qwen3_8b   | residual    |       4 | true_friend          | language_main |        20 | -0.43746     | -1.53285     |  0.687563    |          0.4    |
| qwen3_8b   | residual    |       4 | translation_control  | language_main |        16 |  0.644972    | -0.669107    |  2.55005     |          0.25   |
| qwen3_8b   | residual    |       8 | false_friend         | semantic_main |        20 |  1.90422     |  0.780075    |  3.28407     |          0.7    |
| qwen3_8b   | residual    |       8 | false_friend         | language_main |        20 |  9.68562     |  5.39185     | 14.7717      |          0.95   |
| qwen3_8b   | residual    |       8 | monolingual_polysemy | semantic_main |        20 |  0.483675    | -0.0875938   |  1.12815     |          0.55   |
| qwen3_8b   | residual    |       8 | true_friend          | language_main |        20 |  0.351416    | -0.547701    |  1.37305     |          0.55   |
| qwen3_8b   | residual    |       8 | translation_control  | language_main |        16 |  0.391693    | -1.30606     |  2.64027     |          0.4375 |
| qwen3_8b   | residual    |      12 | false_friend         | semantic_main |        20 |  1.89479     |  0.652556    |  3.2098      |          0.8    |
| qwen3_8b   | residual    |      12 | false_friend         | language_main |        20 |  8.95774     |  4.50829     | 14.0772      |          0.8    |
| qwen3_8b   | residual    |      12 | monolingual_polysemy | semantic_main |        20 |  0.470809    | -0.0450942   |  1.02571     |          0.55   |
| qwen3_8b   | residual    |      12 | true_friend          | language_main |        20 |  0.441553    | -0.308012    |  1.29347     |          0.65   |
| qwen3_8b   | residual    |      12 | translation_control  | language_main |        16 |  0.0958276   | -1.40284     |  2.11781     |          0.5    |
| qwen3_8b   | residual    |      16 | false_friend         | semantic_main |        20 |  2.50554     |  1.14322     |  4.30636     |          0.85   |
| qwen3_8b   | residual    |      16 | false_friend         | language_main |        20 |  5.92613     |  3.21919     |  8.91625     |          0.8    |
| qwen3_8b   | residual    |      16 | monolingual_polysemy | semantic_main |        20 |  0.480709    | -0.000450389 |  1.01876     |          0.6    |
| qwen3_8b   | residual    |      16 | true_friend          | language_main |        20 |  0.336734    | -0.390565    |  1.04438     |          0.65   |
| qwen3_8b   | residual    |      16 | translation_control  | language_main |        16 | -0.534907    | -1.61869     |  0.509967    |          0.375  |
| qwen3_8b   | residual    |      20 | false_friend         | semantic_main |        20 |  1.8175      |  1.01909     |  2.75934     |          0.8    |
| qwen3_8b   | residual    |      20 | false_friend         | language_main |        20 |  4.95294     |  2.76434     |  7.38282     |          0.95   |
| qwen3_8b   | residual    |      20 | monolingual_polysemy | semantic_main |        20 |  0.288471    | -0.0709947   |  0.623608    |          0.55   |
| qwen3_8b   | residual    |      20 | true_friend          | language_main |        20 |  0.182727    | -0.422287    |  0.802717    |          0.5    |
| qwen3_8b   | residual    |      20 | translation_control  | language_main |        16 | -0.398573    | -0.991787    |  0.205247    |          0.375  |
| qwen3_8b   | residual    |      24 | false_friend         | semantic_main |        20 |  0.407357    |  0.0251972   |  0.794354    |          0.7    |
| qwen3_8b   | residual    |      24 | false_friend         | language_main |        20 |  1.9248      |  0.884985    |  3.09831     |          0.9    |
| qwen3_8b   | residual    |      24 | monolingual_polysemy | semantic_main |        20 |  0.126635    | -0.136917    |  0.315415    |          0.6    |
| qwen3_8b   | residual    |      24 | true_friend          | language_main |        20 |  0.0203729   | -0.189227    |  0.231839    |          0.55   |
| qwen3_8b   | residual    |      24 | translation_control  | language_main |        16 | -0.00237313  | -0.201565    |  0.212647    |          0.375  |
| qwen3_8b   | residual    |      28 | false_friend         | semantic_main |        20 |  0.133776    |  0.0294645   |  0.258259    |          0.7    |
| qwen3_8b   | residual    |      28 | false_friend         | language_main |        20 |  0.133455    |  0.0537849   |  0.223383    |          0.75   |
| qwen3_8b   | residual    |      28 | monolingual_polysemy | semantic_main |        20 |  0.0639141   |  0.0202492   |  0.116409    |          0.6    |
| qwen3_8b   | residual    |      28 | true_friend          | language_main |        20 |  0.0662968   | -0.0953477   |  0.222375    |          0.65   |
| qwen3_8b   | residual    |      28 | translation_control  | language_main |        16 | -0.144275    | -0.402611    |  0.0605869   |          0.4375 |
| qwen3_8b   | residual    |      32 | false_friend         | semantic_main |        20 |  0.0550084   |  0.0159071   |  0.0974952   |          0.7    |
| qwen3_8b   | residual    |      32 | false_friend         | language_main |        20 |  0.0219614   | -0.0235158   |  0.0760064   |          0.45   |
| qwen3_8b   | residual    |      32 | monolingual_polysemy | semantic_main |        20 |  0.0119551   | -0.00392639  |  0.0296415   |          0.5    |
| qwen3_8b   | residual    |      32 | true_friend          | language_main |        20 |  0.0196471   | -0.0420197   |  0.0909265   |          0.5    |
| qwen3_8b   | residual    |      32 | translation_control  | language_main |        16 | -0.088766    | -0.193531    |  0.0256476   |          0.25   |
| qwen3_8b   | residual    |      35 | false_friend         | semantic_main |        20 |  0           |  0           |  0           |          0      |
| qwen3_8b   | residual    |      35 | false_friend         | language_main |        20 |  0           |  0           |  0           |          0      |
| qwen3_8b   | residual    |      35 | monolingual_polysemy | semantic_main |        20 |  0           |  0           |  0           |          0      |
| qwen3_8b   | residual    |      35 | true_friend          | language_main |        20 |  0           |  0           |  0           |          0      |
| qwen3_8b   | residual    |      35 | translation_control  | language_main |        16 |  0           |  0           |  0           |          0      |

## False-friend language excess over controls

| model      | component   |   layer | control             |    estimate |      ci_low |      ci_high |   n_false |   n_control |
|:-----------|:------------|--------:|:--------------------|------------:|------------:|-------------:|----------:|------------:|
| gemma3_12b | attention   |       0 | true_friend         |  5.77954    |  2.54122    |  9.94289     |        20 |          20 |
| gemma3_12b | attention   |       0 | translation_control |  5.2731     |  2.22673    |  9.38732     |        20 |          16 |
| gemma3_12b | attention   |       4 | true_friend         | -0.134147   | -0.401954   |  0.132831    |        20 |          20 |
| gemma3_12b | attention   |       4 | translation_control |  0.125028   | -0.199012   |  0.458681    |        20 |          16 |
| gemma3_12b | attention   |       8 | true_friend         |  0.169039   | -0.182574   |  0.517752    |        20 |          20 |
| gemma3_12b | attention   |       8 | translation_control |  0.345481   |  0.0134089  |  0.706055    |        20 |          16 |
| gemma3_12b | attention   |      12 | true_friend         | -0.362555   | -0.82126    |  0.0277843   |        20 |          20 |
| gemma3_12b | attention   |      12 | translation_control | -0.091153   | -0.568808   |  0.32804     |        20 |          16 |
| gemma3_12b | attention   |      16 | true_friend         | -0.111021   | -0.410458   |  0.179916    |        20 |          20 |
| gemma3_12b | attention   |      16 | translation_control | -0.016905   | -0.321479   |  0.253733    |        20 |          16 |
| gemma3_12b | attention   |      20 | true_friend         | -0.140363   | -0.350862   |  0.0903147   |        20 |          20 |
| gemma3_12b | attention   |      20 | translation_control | -0.105641   | -0.477439   |  0.253772    |        20 |          16 |
| gemma3_12b | attention   |      24 | true_friend         | -0.104697   | -0.374373   |  0.157305    |        20 |          20 |
| gemma3_12b | attention   |      24 | translation_control | -0.164722   | -0.485772   |  0.146018    |        20 |          16 |
| gemma3_12b | attention   |      28 | true_friend         |  0.0167064  | -0.159834   |  0.188365    |        20 |          20 |
| gemma3_12b | attention   |      28 | translation_control | -0.155287   | -0.340633   |  0.0343546   |        20 |          16 |
| gemma3_12b | attention   |      32 | true_friend         |  0.0948167  | -0.0790939  |  0.279757    |        20 |          20 |
| gemma3_12b | attention   |      32 | translation_control |  0.0572587  | -0.161602   |  0.270549    |        20 |          16 |
| gemma3_12b | attention   |      36 | true_friend         |  0.0404865  | -0.0747556  |  0.156402    |        20 |          20 |
| gemma3_12b | attention   |      36 | translation_control | -0.0152233  | -0.104719   |  0.0799387   |        20 |          16 |
| gemma3_12b | attention   |      40 | true_friend         |  0.0450208  | -0.0474215  |  0.136466    |        20 |          20 |
| gemma3_12b | attention   |      40 | translation_control | -0.0453404  | -0.246735   |  0.123284    |        20 |          16 |
| gemma3_12b | attention   |      44 | true_friend         |  0.0736704  | -0.0247802  |  0.168203    |        20 |          20 |
| gemma3_12b | attention   |      44 | translation_control |  0.0313875  | -0.107475   |  0.172779    |        20 |          16 |
| gemma3_12b | attention   |      47 | true_friend         |  0          |  0          |  0           |        20 |          20 |
| gemma3_12b | attention   |      47 | translation_control |  0          |  0          |  0           |        20 |          16 |
| gemma3_12b | mlp         |       0 | true_friend         |  2.47816    |  0.22875    |  5.46781     |        20 |          20 |
| gemma3_12b | mlp         |       0 | translation_control |  2.08713    |  0.269965   |  4.96904     |        20 |          16 |
| gemma3_12b | mlp         |       4 | true_friend         |  2.34323    |  0.526174   |  4.87946     |        20 |          20 |
| gemma3_12b | mlp         |       4 | translation_control |  1.94815    |  0.197559   |  4.44211     |        20 |          16 |
| gemma3_12b | mlp         |       8 | true_friend         |  2.4733     |  0.911135   |  4.62723     |        20 |          20 |
| gemma3_12b | mlp         |       8 | translation_control |  2.10895    |  0.668879   |  4.11727     |        20 |          16 |
| gemma3_12b | mlp         |      12 | true_friend         |  1.51767    |  0.829761   |  2.28629     |        20 |          20 |
| gemma3_12b | mlp         |      12 | translation_control |  1.13539    |  0.481487   |  1.84869     |        20 |          16 |
| gemma3_12b | mlp         |      16 | true_friend         |  0.468396   | -0.070163   |  1.04329     |        20 |          20 |
| gemma3_12b | mlp         |      16 | translation_control |  0.606672   |  0.147579   |  1.13132     |        20 |          16 |
| gemma3_12b | mlp         |      20 | true_friend         |  0.389341   | -0.0228747  |  0.798717    |        20 |          20 |
| gemma3_12b | mlp         |      20 | translation_control |  0.744167   |  0.281394   |  1.22565     |        20 |          16 |
| gemma3_12b | mlp         |      24 | true_friend         | -0.223898   | -0.540701   |  0.0805289   |        20 |          20 |
| gemma3_12b | mlp         |      24 | translation_control | -0.18047    | -0.589702   |  0.226735    |        20 |          16 |
| gemma3_12b | mlp         |      28 | true_friend         |  0.0274857  | -0.161902   |  0.216975    |        20 |          20 |
| gemma3_12b | mlp         |      28 | translation_control | -0.11124    | -0.376082   |  0.145992    |        20 |          16 |
| gemma3_12b | mlp         |      32 | true_friend         |  0.0236661  | -0.123931   |  0.180753    |        20 |          20 |
| gemma3_12b | mlp         |      32 | translation_control | -0.0250484  | -0.227667   |  0.165486    |        20 |          16 |
| gemma3_12b | mlp         |      36 | true_friend         | -0.199037   | -0.342618   | -0.0662359   |        20 |          20 |
| gemma3_12b | mlp         |      36 | translation_control |  0.0325506  | -0.146499   |  0.23848     |        20 |          16 |
| gemma3_12b | mlp         |      40 | true_friend         | -0.00138856 | -0.150819   |  0.144639    |        20 |          20 |
| gemma3_12b | mlp         |      40 | translation_control |  0.0372263  | -0.127334   |  0.200383    |        20 |          16 |
| gemma3_12b | mlp         |      44 | true_friend         | -0.0371366  | -0.129079   |  0.0488616   |        20 |          20 |
| gemma3_12b | mlp         |      44 | translation_control |  0.0216422  | -0.119125   |  0.174322    |        20 |          16 |
| gemma3_12b | mlp         |      47 | true_friend         |  0          |  0          |  0           |        20 |          20 |
| gemma3_12b | mlp         |      47 | translation_control |  0          |  0          |  0           |        20 |          16 |
| gemma3_12b | residual    |       0 | true_friend         |  2.94087    | -1.42861    |  8.29729     |        20 |          20 |
| gemma3_12b | residual    |       0 | translation_control | -2.58547    | -5.35631    | -0.122468    |        20 |          16 |
| gemma3_12b | residual    |       4 | true_friend         | 10.769      |  5.99012    | 16.0764      |        20 |          20 |
| gemma3_12b | residual    |       4 | translation_control |  4.71503    |  1.29418    |  8.60194     |        20 |          16 |
| gemma3_12b | residual    |       8 | true_friend         | 15.4796     |  9.7883     | 21.694       |        20 |          20 |
| gemma3_12b | residual    |       8 | translation_control | 12.588      |  7.69989    | 18.2558      |        20 |          16 |
| gemma3_12b | residual    |      12 | true_friend         | 11.7322     |  7.00189    | 16.7904      |        20 |          20 |
| gemma3_12b | residual    |      12 | translation_control |  9.34052    |  4.32377    | 14.4289      |        20 |          16 |
| gemma3_12b | residual    |      16 | true_friend         | 10.3452     |  6.3267     | 14.8542      |        20 |          20 |
| gemma3_12b | residual    |      16 | translation_control |  9.84866    |  5.69498    | 14.3537      |        20 |          16 |
| gemma3_12b | residual    |      20 | true_friend         |  7.23649    |  4.02765    | 10.8241      |        20 |          20 |
| gemma3_12b | residual    |      20 | translation_control |  7.08902    |  4.26469    | 10.3405      |        20 |          16 |
| gemma3_12b | residual    |      24 | true_friend         |  4.71072    |  2.33545    |  7.4161      |        20 |          20 |
| gemma3_12b | residual    |      24 | translation_control |  4.53953    |  2.34217    |  7.16596     |        20 |          16 |
| gemma3_12b | residual    |      28 | true_friend         |  0.316334   | -0.148658   |  0.839395    |        20 |          20 |
| gemma3_12b | residual    |      28 | translation_control |  0.0312969  | -0.439705   |  0.557319    |        20 |          16 |
| gemma3_12b | residual    |      32 | true_friend         |  0.0771801  | -0.248088   |  0.456408    |        20 |          20 |
| gemma3_12b | residual    |      32 | translation_control | -0.124942   | -0.495396   |  0.282273    |        20 |          16 |
| gemma3_12b | residual    |      36 | true_friend         | -0.0501222  | -0.327537   |  0.222324    |        20 |          20 |
| gemma3_12b | residual    |      36 | translation_control | -0.328061   | -0.677805   |  5.65319e-05 |        20 |          16 |
| gemma3_12b | residual    |      40 | true_friend         | -0.169249   | -0.392371   |  0.050695    |        20 |          20 |
| gemma3_12b | residual    |      40 | translation_control | -0.116661   | -0.298841   |  0.0653167   |        20 |          16 |
| gemma3_12b | residual    |      44 | true_friend         | -0.0327106  | -0.182232   |  0.109874    |        20 |          20 |
| gemma3_12b | residual    |      44 | translation_control |  0.0456877  | -0.0728172  |  0.162009    |        20 |          16 |
| gemma3_12b | residual    |      47 | true_friend         |  0          |  0          |  0           |        20 |          20 |
| gemma3_12b | residual    |      47 | translation_control |  0          |  0          |  0           |        20 |          16 |
| qwen3_8b   | attention   |       0 | true_friend         |  0.995176   | -0.193378   |  2.63447     |        20 |          20 |
| qwen3_8b   | attention   |       0 | translation_control |  0.761122   | -0.424578   |  2.42032     |        20 |          16 |
| qwen3_8b   | attention   |       4 | true_friend         |  0.988469   |  0.338085   |  1.87218     |        20 |          20 |
| qwen3_8b   | attention   |       4 | translation_control |  0.804633   |  0.158881   |  1.69682     |        20 |          16 |
| qwen3_8b   | attention   |       8 | true_friend         | -0.00527899 | -0.187711   |  0.180715    |        20 |          20 |
| qwen3_8b   | attention   |       8 | translation_control | -0.0881252  | -0.275512   |  0.0926041   |        20 |          16 |
| qwen3_8b   | attention   |      12 | true_friend         | -0.0603571  | -0.240743   |  0.113659    |        20 |          20 |
| qwen3_8b   | attention   |      12 | translation_control |  0.0917654  | -0.0683973  |  0.25672     |        20 |          16 |
| qwen3_8b   | attention   |      16 | true_friend         | -0.0952552  | -0.229698   |  0.0414645   |        20 |          20 |
| qwen3_8b   | attention   |      16 | translation_control | -0.00585645 | -0.175581   |  0.168982    |        20 |          16 |
| qwen3_8b   | attention   |      20 | true_friend         | -0.00336464 | -0.094625   |  0.0864264   |        20 |          20 |
| qwen3_8b   | attention   |      20 | translation_control | -0.0391626  | -0.168617   |  0.0985302   |        20 |          16 |
| qwen3_8b   | attention   |      24 | true_friend         |  0.101096   | -0.0513305  |  0.241745    |        20 |          20 |
| qwen3_8b   | attention   |      24 | translation_control |  0.0596472  | -0.0606705  |  0.186095    |        20 |          16 |
| qwen3_8b   | attention   |      28 | true_friend         |  0.056058   | -0.00485954 |  0.118604    |        20 |          20 |
| qwen3_8b   | attention   |      28 | translation_control | -0.0143323  | -0.0801894  |  0.0562988   |        20 |          16 |
| qwen3_8b   | attention   |      32 | true_friend         |  0.0369237  | -0.0238889  |  0.0962404   |        20 |          20 |
| qwen3_8b   | attention   |      32 | translation_control | -0.059534   | -0.130987   | -0.000256735 |        20 |          16 |
| qwen3_8b   | attention   |      35 | true_friend         |  0          |  0          |  0           |        20 |          20 |
| qwen3_8b   | attention   |      35 | translation_control |  0          |  0          |  0           |        20 |          16 |
| qwen3_8b   | mlp         |       0 | true_friend         |  0.601263   | -0.587527   |  1.81594     |        20 |          20 |
| qwen3_8b   | mlp         |       0 | translation_control | -1.09973    | -1.97712    | -0.224466    |        20 |          16 |
| qwen3_8b   | mlp         |       4 | true_friend         |  2.45941    |  0.671139   |  4.79714     |        20 |          20 |
| qwen3_8b   | mlp         |       4 | translation_control |  2.99806    |  1.14778    |  5.40626     |        20 |          16 |
| qwen3_8b   | mlp         |       8 | true_friend         |  1.61682    |  0.871503   |  2.43356     |        20 |          20 |
| qwen3_8b   | mlp         |       8 | translation_control |  1.29052    |  0.545815   |  2.10904     |        20 |          16 |
| qwen3_8b   | mlp         |      12 | true_friend         |  0.410834   |  0.0447207  |  0.719152    |        20 |          20 |
| qwen3_8b   | mlp         |      12 | translation_control |  0.118566   | -0.258929   |  0.492981    |        20 |          16 |
| qwen3_8b   | mlp         |      16 | true_friend         |  0.299923   |  0.0628639  |  0.53631     |        20 |          20 |
| qwen3_8b   | mlp         |      16 | translation_control |  0.409908   |  0.20902    |  0.627882    |        20 |          16 |
| qwen3_8b   | mlp         |      20 | true_friend         |  0.113181   | -0.0672387  |  0.290483    |        20 |          20 |
| qwen3_8b   | mlp         |      20 | translation_control |  0.133298   | -0.0688123  |  0.331446    |        20 |          16 |
| qwen3_8b   | mlp         |      24 | true_friend         |  0.223263   |  0.0286399  |  0.440549    |        20 |          20 |
| qwen3_8b   | mlp         |      24 | translation_control |  0.188684   |  0.0309586  |  0.355283    |        20 |          16 |
| qwen3_8b   | mlp         |      28 | true_friend         | -0.00084068 | -0.0797506  |  0.0800327   |        20 |          20 |
| qwen3_8b   | mlp         |      28 | translation_control |  0.0533302  | -0.0359844  |  0.139428    |        20 |          16 |
| qwen3_8b   | mlp         |      32 | true_friend         |  0.0224668  | -0.042668   |  0.0890317   |        20 |          20 |
| qwen3_8b   | mlp         |      32 | translation_control | -0.0220076  | -0.0892067  |  0.039988    |        20 |          16 |
| qwen3_8b   | mlp         |      35 | true_friend         |  0          |  0          |  0           |        20 |          20 |
| qwen3_8b   | mlp         |      35 | translation_control |  0          |  0          |  0           |        20 |          16 |
| qwen3_8b   | residual    |       0 | true_friend         |  0.7581     | -0.5788     |  2.13374     |        20 |          20 |
| qwen3_8b   | residual    |       0 | translation_control | -1.36909    | -2.54669    | -0.0782352   |        20 |          16 |
| qwen3_8b   | residual    |       4 | true_friend         |  8.97923    |  4.59956    | 14.0455      |        20 |          20 |
| qwen3_8b   | residual    |       4 | translation_control |  7.8968     |  3.3422     | 13.1386      |        20 |          16 |
| qwen3_8b   | residual    |       8 | true_friend         |  9.3342     |  4.93418    | 14.4119      |        20 |          20 |
| qwen3_8b   | residual    |       8 | translation_control |  9.29392    |  4.47131    | 14.5057      |        20 |          16 |
| qwen3_8b   | residual    |      12 | true_friend         |  8.51619    |  4.12607    | 13.5527      |        20 |          20 |
| qwen3_8b   | residual    |      12 | translation_control |  8.86191    |  4.20321    | 14.2977      |        20 |          16 |
| qwen3_8b   | residual    |      16 | true_friend         |  5.5894     |  2.78106    |  8.61398     |        20 |          20 |
| qwen3_8b   | residual    |      16 | translation_control |  6.46104    |  3.56349    |  9.61294     |        20 |          16 |
| qwen3_8b   | residual    |      20 | true_friend         |  4.77021    |  2.51012    |  7.32353     |        20 |          20 |
| qwen3_8b   | residual    |      20 | translation_control |  5.35151    |  2.96929    |  7.93129     |        20 |          16 |
| qwen3_8b   | residual    |      24 | true_friend         |  1.90443    |  0.862541   |  3.11584     |        20 |          20 |
| qwen3_8b   | residual    |      24 | translation_control |  1.92717    |  0.829033   |  3.15835     |        20 |          16 |
| qwen3_8b   | residual    |      28 | true_friend         |  0.0671582  | -0.11329    |  0.253208    |        20 |          20 |
| qwen3_8b   | residual    |      28 | translation_control |  0.27773    |  0.0563448  |  0.540113    |        20 |          16 |
| qwen3_8b   | residual    |      32 | true_friend         |  0.00231429 | -0.0812426  |  0.0847085   |        20 |          20 |
| qwen3_8b   | residual    |      32 | translation_control |  0.110727   | -0.0122675  |  0.223425    |        20 |          16 |
| qwen3_8b   | residual    |      35 | true_friend         |  0          |  0          |  0           |        20 |          20 |
| qwen3_8b   | residual    |      35 | translation_control |  0          |  0          |  0           |        20 |          16 |

## Profiles

| model      | component   |   profile_correlation |   ff_significant_layers |   mono_significant_layers |   ff_peak_layer |   mono_peak_layer |
|:-----------|:------------|----------------------:|------------------------:|--------------------------:|----------------:|------------------:|
| gemma3_12b | attention   |             -0.219824 |                       1 |                         0 |               8 |                 4 |
| gemma3_12b | mlp         |              0.539752 |                       4 |                         2 |               8 |                 8 |
| gemma3_12b | residual    |              0.819755 |                       8 |                         2 |              16 |                 8 |
| qwen3_8b   | attention   |             -0.469968 |                       0 |                         1 |               4 |                 0 |
| qwen3_8b   | mlp         |              0.331142 |                       2 |                         0 |               8 |                 0 |
| qwen3_8b   | residual    |              0.920585 |                       8 |                         2 |              16 |                 8 |
