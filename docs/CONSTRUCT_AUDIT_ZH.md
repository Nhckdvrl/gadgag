# 对附件反馈的逐项审计与处理

| 反馈 | 处理 | 结果 |
|---|---|---|
| Midpoint 不能叫 candidate prior | 全部改称 diagonal margin midpoint；另跑 content-free baseline | 校准使两向准确率平均提高约14pt，证明 decision layer 重要，但不把 midpoint 作因果解释 |
| SenseSwitch 同时改语言、语义和词形 | 使用 Stingray 四单元做 language×sense 2×2，只取 exact NFKC 且四格均实际含目标词的 forms | full semantic effect 92/96 CI>0；official chat 48/48；language effect 也独立存在 |
| 可能只是 language ID | language-only、marker-matched shuffled、target-masked controls | language-only 4正/2负；shuffled 1正/3负；masked 91正 |
| tokenizer boundary 不真实 | 新 `scoring_v2.py` tokenize 完整 plain string并断言 prefix；chat 用 generation boundary | 所有正式新实验使用新 scorer；旧实验只保留为历史反证 |
| mean logp 不是 sequence probability | mean 与 sum 同时报 | official chat 下两种 normalization 全部通过；4 个未过单元集中在 Gemma-3-12B plain |
| instruct 模型没用 chat template | plain/chat 全跑 | 8 个 official-chat model×pair cell 全过六个 gate；plain 中 Gemma-3-12B 两语言对未全过 |
| CSV 依赖相邻行 | loader 加 meanings、validity labels、方向和 exact-form assertions | 发现并隔离了 ZH–JA 非 exact 数据中的一处 meaning mismatch；正式 exact subset 不受影响 |
| gloss wording | 三 wrapper + 两套 lexical variants | aggregate 48/48 CI>0；item consistency 仍有限，明确列为后续风险 |
| 与 contextual calibration 对照 | content-free calibration + Stingray-style metrics | absolute conclusion明显改变；承认 calibration 非 novelty |
| 与普通 WSD 对照 | XL-WiC ZH/JA/DE 各200条 | 小模型为 49–70%，校准方向不一致；不能用当前 prompt 宣称跨任务优势 |
| adaptation 新信号 | 保留为 secondary preregistered hypothesis | conflict ΔS 显著，但 conflict-neutral DID CI 略跨0，不 claim |

## 新发现的数据质量问题

1. Stingray 的 ZH–JA 非 exact 行中存在至少一处相邻两行 `Meaning in L1` 不一致；旧 loader 会静默接受，新 loader 会 assertion fail。
2. 原英文 gloss 含有 `dward`、`at east` 等拼写问题；lexical-variant experiment 使用修正释义，但这些新增释义尚未经过独立双语人类验证。
3. Stingray conflict cell 是“翻译后替换为 false friend”形成的语义奇异句。它适合强 factorial pilot，但不能代替自然语料验证。
4. 仅检查 `Cognates` 字段的 NFKC equality 会误收 `gulai/gulay` 一类复合记录、词形变化，以及四格中实际未出现目标词的行。正式 loader 现在还要求目标词在四格中逐字/整词出现，样本因此从 ZH–JA 29、ID–TL 48 缩为 **27、33**。
5. 初版 shuffled control 使用 `[OTHER]`，与 masked 的 `[TARGET]` 不匹配。匹配为同一 `[TARGET]` 后重跑全部模型，shuffled semantic effect 仅 1/96 正、3/96 负；natural masked−shuffled 仍为 82/96，说明结果不是 marker identity 造成。
6. natural full−language-only 只有 36/96 正且 16/96 显著负。显式语言+目标词有时比长自然语境给出更强的正确方向，这否定“context 总是主导”的版本，却支持审计 evidence competition 的新问题。
7. batch-size 8 vs 32 压力测试的 margin Pearson >.999，但仍有 0.6%–1.2% cell decision 换号；Gemma-3-12B ID–TL plain 的六个 full gate 有一个随 batch size 改变显著性，Qwen2.5 ZH–JA chat 六个均保持。正式研究必须固定数值协议并报告 near-zero stability。

这些问题不会推翻 exact-form 2×2 的 aggregate pilot，却决定了下一阶段必须先做数据可靠性，而不是扩模型 leaderboard。
