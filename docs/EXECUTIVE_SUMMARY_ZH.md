# 执行摘要：pilot 最终判断

## 一句话结论

原题 **“单语言适配通过同形异义词造成另一语言的定向语义覆盖”应当停止**；真实实验发现，其最漂亮的初始信号主要是候选表面频率造成的假象。与此同时，反证过程中得到一个更宽、可扩展且尚未被现有同形词 benchmark 正确处理的问题：

> **跨语言词汇干扰的因果分解：如何区分语言条件化的词义敏感性与表面/候选先验？**

英文工作标题：

> **Right Direction, Wrong Answer: Causally Decomposing Cross-Lingual Lexical Interference**

这个结论不是文献猜测，而是经过两轮模型、两种语言对、双折 crossover、剂量曲线、中性表面控制、语境去先验控制、模块消融和失败方法对照后收束出来的。

## 原假设为什么被否定

在 Qwen2.5-7B 上，对 50 个 Unicode 完全相同的中日 false friends 做两折 crossover：每折 25 个词接受中文适配、25 个 held out，每个词最终既当处理组也当自身对照。

- 中文冲突义暴露 32 次后，原始日语候选 margin 的处理效应为 **-0.462**，95% bootstrap CI **[-0.695, -0.238]**。
- Qwen3-8B 的 32 次暴露复现为 **-0.392 [-0.642, -0.157]**。
- 看起来像 overwrite，但直接用日语释义评价时效应不显著：**-0.198 [-0.469, 0.075]**。
- 更致命的是，只重复词形、不提供中文冲突词义的 neutral control 产生更大的效应：**-0.942 [-1.178, -0.717]**。
- 把真实日语上下文分数减去匹配的乱序日语上下文分数后，冲突适配效应变成 **-0.018 [-0.452, 0.404]**；English–German 的剂量 8 结果也从显著的 **-0.363 [-0.710, -0.022]** 变为不显著的 **-0.147 [-0.631, 0.348]**。

因此，原始指标主要测到了训练后候选同形字符串的无条件概率上升，而非另一语言的语境语义表征被覆盖。严格 stop criterion 下，原题为 **KILL**。

## 实验中出现的新现象

我们把同一个 false friend 放进自然的 L1 和 L2 语境，并固定两边候选义。设：

```text
m1 = log P(L2义 | L1语境) - log P(L1义 | L1语境)
m2 = log P(L2义 | L2语境) - log P(L1义 | L2语境)
SenseSwitch = m2 - m1
CandidatePrior = (m2 + m1) / 2
```

传统准确率要求 L1 语境选 L1 义、L2 语境选 L2 义，两边都必须过零；`SenseSwitch` 则问语境切换是否让证据朝正确方向移动。两者必须同时报告，不能用后者掩盖错误。

初步结果：

| 模型 | 语言对 | 两边都答对 | 正向 SenseSwitch |
|---|---:|---:|---:|
| Qwen2.5-7B | EN–DE | 44.9% | 95.9% |
| Qwen2.5-7B | ZH–JA | 45.6% | 87.7% |
| Qwen3-8B | EN–DE | 44.9% | 89.8% |
| Qwen3-8B | ZH–JA | 33.3% | 82.5% |
| Gemma-3-4B | EN–DE | 32.7% | 81.6% |
| Gemma-3-4B | ZH–JA | 24.6% | 71.9% |
| Gemma-3-12B | EN–DE | 30.6% | 95.9% |
| Gemma-3-12B | ZH–JA | 7.0% | 64.9% |

所有八个条件的平均 sense switch 的 95% CI 都在 0 以上。也就是说，模型经常在绝对答案上失败，但语言语境改变产生的相对证据方向是正确的。当前“答对/答错”容易把稳定的语言/候选先验误诊为完全不懂跨语言词义。

最后，我们把这个分解用于保存的适配器。冲突词义适配使 sense switch 下降 **-0.384 [-0.740, -0.033]**，中性词形重复为 **-0.057 [-0.336, 0.220]**。不过两者的直接 difference-in-differences 为 **-0.327 [-0.695, 0.028]**，仍略跨 0；两个单侧语境分量也各自不显著。因此这是值得预注册复验的动态干扰线索，**不是已经证实的 semantic overwrite**。它使最终题目可以研究干扰的两个成分，但不允许恢复原题的强结论。

## 为什么新题不是“再做一个 benchmark”

核心贡献应当是测量模型和因果审计，而不是扩数据或排模型名次：

1. 提出双轴诊断：**absolute resolution** 与 **context sensitivity**，并显式分解 candidate prior。
2. 用 surface-only、meaning-conflict、shuffled-context、candidate-order/paraphrase 等干预验证每个指标究竟测什么。
3. 审计现有 cross-lingual homograph 结论在去先验后是否仍成立，并区分“语义不敏感”“方向正确但先验太强”“真正稳定正确”三类模型行为。
4. 把方法推广到多个脚本、资源不平衡程度和语言距离，研究何时表面先验压倒语境证据。

通用 contextual calibration 已有成熟先例，因此不能声称“首次去除选项先验”。真正的 novelty 是：把自然双语 sense-switch 作为 false-friend 的成对反事实，结合训练干预做 construct validation，并重新解释现有 homograph benchmark 的失败来源。

## 最终建议

**有条件 GO，评分约 7.5/10。** 它比原来的 overwrite 题更可信，也比单纯日中错误分析更宽：主问题是对 cross-lingual lexical interference 做可识别的因果分解，homograph 是最干净的自然实验床。正式定题前的硬门槛是：

- 在至少 4 个语言对、6 个模型上复现“严格准确率与 sense switch 分离”；
- 对 candidate paraphrase、顺序、语言标签和同语乱序语境保持稳定；
- 由人工标注者确认高 switch/低 accuracy 的样本确实包含正确的相对语境证据；
- 与 contextual calibration、Stingray 原指标、MCL-WiC/WSD 对照，证明新分解改变了有科学意义的模型诊断，而不只是换算分数。

如果这四项有两项失败，就停止，不把它缩成“某一种日中同形词的指标”。
