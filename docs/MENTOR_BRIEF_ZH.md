# 给导师汇报的简洁版本

## 暂定题目

**Right Direction, Wrong Answer? Auditing Cross-Lingual Sense Disambiguation Beyond Accuracy**

日语暂名：

**正解できなくても方向は正しいのか：言語間同形異義語評価における文脈証拠と判断バイアスの分析**

## 30 秒说明

先行研究发现 LLM 在跨语言同形异义词上经常答错，因此认为模型不能区分两个语言的词义。但 accuracy 把两种失败混在一起：模型完全没有利用语境；或者模型提取了方向正确的语境证据，却不足以克服语言或答案偏置。

我利用 StingrayBench 本来就存在的四个交叉条件，把句子语言和目标词义语境做成 2×2。严格要求同一表记确实出现在四个上下文后，四个模型、两语言对、plain/chat、mean/sum 和多种释义形式下，semantic-context effect 有 92/96 个 protocol cells 的置信区间大于零；其中官方 chat-template 是 48/48。language-only 仅有 4 正、2 负，marker-matched shuffled 仅有 1 正、3 负。注意这 96 个高度相关的 robustness cells 不是 96 次独立重复。

只用原始自然正确用法、不使用人工 conflict cells 时，masked natural context 相对 matched shuffled context 仍有 82/96 为正（official chat 46/48）；但 full natural context 相对显式 language+target cue 只有 36/96 为正、16/96 为负。因此不能说“模型总是依靠上下文”或“上下文一定强于语言”，而应研究不同 evidence source 如何在 decision protocol 下竞争。

## 一张核心表

| 条件 | semantic effect 显著为正 |
|---|---:|
| Full 2×2 context | 92/96（chat 48/48） |
| Mask target surface | 91/96 |
| Language only | 4/96 正、2/96 负 |
| Marker-matched shuffled context | 1/96 正、3/96 负 |
| Natural masked − matched shuffled | 82/96（chat 46/48） |

## 初步 idea

提出 **Crossed-Context Audit (XCA)**。对同一个词同时测：

- surrounding semantic-context evidence；
- sentence-language convention evidence；
- language×semantics interaction；
- content-free / repeated-gloss decision resolution。

这不是再建一个排行榜，而是审计现有 benchmark 的低准确率究竟代表什么。

正式实验不再把“92/96”当统计推断单位。预注册主分析使用 official chat template，gloss 作为 repeated measure，以 item/model 随机效应估计连续 SCE/LCE；plain、mean/sum、batch size 只作为 protocol sensitivity audit。

## 为什么不算太窄、又没有硬撞车

- 母题仍是 cross-lingual homograph；同形词让 surface form 固定，是分离跨语言相关线索的自然实验床。
- 一般问题是 multilingual evaluation 中“相关线索被一个 accuracy 混在一起”，可外推到 WSD、MT lexical choice、code-switching 和语言相关答案选项。
- Stingray 已做 benchmark 和高资源语言 bias；GlobalNLP 2025 已做 few-shot prompt balance；SemEval-2026 AmbiStory 已做 graded sense plausibility。因此不能声称“首次超越 accuracy”或“首次发现 prompt bias”。
- 本轮定向检索仍未找到同时对 exact false friend 交叉 sentence language×intended sense，并以 masked/shuffled/repeated-gloss/calibration 分离三层证据的直接同题工作。准确表述只能是“截至 2026-08-11 未检索到直接匹配”。

## 数值协议压力测试

固定模型与样本，只把 scoring batch 从 32 改为 8：Qwen2.5 ZH–JA chat 的 margin 相关系数 >.9997、六个 full aggregate gate 均保持；Gemma-3-12B ID–TL plain 的相关系数 >.9991，但 0.8%–1.2% 单格决策换号，并使六个 aggregate gate 中一个 CI 跨越零。这进一步说明 near-boundary accuracy 与 plain likelihood 不宜作为唯一结论。

## 和旧题的区别

- Semantic overwrite 已被 neutral control 和 context-lift 正式否定；
- 不再声称 midpoint 是 candidate prior；
- 不再把 L1→L2 的整体变化全部叫 semantic sensitivity；
- 现在直接使用 2×2 因果对照分离两个可观测 effect。

## 希望请导师判断的问题

1. “evaluation failure ≠ evidence failure”是否是足够一般的大问题？
2. 以 false friends 作为 natural test bed，再推广到 WSD/MT，范围是否合适？
3. 下一步应优先做自然 counterfactual 数据和双语人工验证，还是先审计更多现有 benchmark？

## 我自己的判断

目前给 **7.5/10，有条件 GO**。最重要的风险是 Stingray 的 conflict cells 由人工替词得到、语境较强，单条样本对英文 gloss wording 仍敏感，而且 plain/chat 的 decision protocol 会改变结论强度。当前 natural-diagonal gate 已初步通过 matched-shuffled 对照，但 language-only 结果明确反对“context universally dominates”的强故事。下一个 kill gate 应是独立双语 gloss 复核与新的自然/人工配对语境，而不是立刻刷更多模型。
