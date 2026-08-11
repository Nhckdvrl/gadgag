# 执行摘要：第二轮 construct-killer 后的最终判断

## 结论

原来的 **Cross-Lingual Semantic Overwrite 正式 KILL，不再抢救**。

附件对第一版新题的批评也成立：旧 `SenseSwitch` 同时改变语言、语境和部分词形，`(m1+m2)/2` 只是坐标中点，不能提前命名为 candidate prior。因此仓库已经撤回“causal decomposition into semantic sensitivity and candidate prior”的强表述。

但新的 2×2 反事实实验通过了最关键的 construct killer。最终建议题目是：

> **Right Direction, Wrong Answer? Auditing Cross-Lingual Sense Disambiguation Beyond Accuracy**

中文：

> **答错但方向对？超越准确率审计跨语言同形异义词消歧**

核心一般问题是：

> **Evaluation failure 不等于 evidence extraction failure。** 最终错误究竟来自没有利用语境，还是提取了正确证据、但没有跨过语言/答案偏置造成的决策边界？

## 真正拆开的 2×2

Stingray 每个 false friend 的两行实际给出了四个单元：

| | sense 1 语境 | sense 2 语境 |
|---|---|---|
| L1 语言 | `m11` | `m12` |
| L2 语言 | `m21` | `m22` |

因此可以分别估计：

```text
Semantic Context Evidence, Esem = [(m12+m22) - (m11+m21)] / 2
Language Convention Evidence, Elang = [(m21+m22) - (m11+m12)] / 2
Interaction = (m22-m21) - (m12-m11)
```

旧 diagonal switch `m22-m11` 实际混合了 `Esem + Elang`。现在两者不再混称 semantic sensitivity。

## Gate 实验

只保留 NFKC 完全相同表记：

- ZH–JA：27 词；
- ID–TL：33 词。

这里不仅要求 `Cognates` 字段 NFKC 相同，还要求该目标词确实出现在四个上下文中；复合记录、词形变化和用同义词替换目标词的行均被排除。

四个 checkpoint：Qwen2.5-7B、Qwen3-8B、Gemma-3-4B、Gemma-3-12B。每个模型同时运行 plain/chat、mean/sum logp、三种答案 wrapper。

| 条件 | 变体数 | Semantic effect 的 95% CI > 0 |
|---|---:|---:|
| 完整 2×2 语境 | 96 | **92**（official chat 48/48） |
| 遮掉目标词、只留周围语义 | 96 | **91** |
| 只有语言信息、无 sense context | 96 | 4 正、2 负 |
| 同语言、同 `[TARGET]` marker、换成其他词的语境 | 96 | 1 正、3 负 |

直接 paired contrast：

- full − language-only：92/96 显著为正；
- full − shuffled：84/96 显著为正；
- masked − shuffled：90/96 显著为正。

4 个 full gate 失败均来自 Gemma-3-12B 的 plain-text likelihood（ID–TL 三个、ZH–JA 一个）；官方 chat-template 的 48 个检验全部通过。这不是应被隐藏的异常，而是“decision formulation 本身需要审计”的直接证据。96 个 cells 是相关的 robustness specifications，不是独立重复或可当作 96 个新样本。

## 只用自然语境的生态检查

四格中的 conflict cells 是翻译替词反事实，因此另做只使用 L1×sense1、L2×sense2 两条原始自然正确用法的分析：

- full natural − marker-matched shuffled：94/96（chat 48/48）；
- masked natural − marker-matched shuffled：82/96（chat 46/48）；
- full natural − explicit language+target cue：只有 36/96 为正，且 16/96 显著为负。

前两项说明自然周围语义确实能提供 candidate-specific evidence；第三项说明显式语言约定本身往往已经是极强线索，甚至强于长语境。故论文不能讲“模型会语义、只是 bias 害了它”这种单因故事，必须研究多种 evidence source 与 decision rule 的竞争。

另将 scoring batch size 从 32 改为 8 做数值压力测试：两个代表性配置的连续 margin 相关均 >.999，但仍有 0.6%–1.2% cell 决策换号；最脆弱的 Gemma-3-12B plain 配置有一个 aggregate CI 改变过零结论，Qwen2.5 chat 六个 gate 不变。因此 92/96 是协议稳健性描述，不能冒充 96 次独立统计重复；正式主分析必须预先固定 chat template，并用 hierarchical repeated-measures inference。

所以这个现象不能再被解释成“中文句子选中文义、日语句子选日语义”这么简单。模型确实在使用 sense-bearing surrounding context。

## Tokenization 与措辞稳健性

旧 `candidate_score` 独立 tokenize prompt/candidate 后拼 token ID，已经被新 scorer 替换。plain 模式现在 tokenize 完整字符串并断言 prefix token 稳定；chat 模式使用官方 `apply_chat_template` 的 generation boundary。

- mean 与 sum 两种评分均进入 96 个 gate；official chat 全部通过，plain 有 5 个 CI 跨零。
- 三种 wrapper 在 lexical-variant aggregate 层面均通过。
- 对 27 个 ZH–JA strict homographs 另外写了两套 lexical gloss variants；四模型×plain/chat×mean/sum 共 48 个 aggregate CI 全部 > 0。
- 但 item-level 三种 gloss 均同方向的比例只有 22.2%–81.5%，说明**单条样本诊断仍然明显受 gloss wording 影响**。正式研究必须把 gloss 当 repeated-measure，并进行独立双语人工验证，不能只选一个最漂亮释义。

## Decision bias 而不是 midpoint prior

`margin midpoint` 只作描述。我们另外用 content-free prompt 估计 decision baseline。

跨模型、prompt 和 wrapper 平均：

| Pair | Raw 两向均正确 | Content-free calibrated |
|---|---:|---:|
| ZH–JA | 31.9% | **46.5%** |
| ID–TL | 41.0% | **55.2%** |

ZH–JA 的 Stingray-style bias 平均从 -0.203 变成 0.100，说明原来明显的 L1 偏置会被决策校准实质改变。但 contextual calibration 已有成熟工作，所以它只是 baseline 和因果诊断工具，不是 novelty。

## XL-WiC 对照

在每种语言抽取 200 条 expert-curated XL-WiC，四个小型模型的 forced-likelihood accuracy 大约为 49%–70%，content-free calibration 的影响方向不一致。这说明：

1. 新 effect 不是“这些模型在任何 WSD 任务上都很强”；
2. 当前 XL-WiC forced-choice prompt 本身也受 decision formulation 影响；
3. 正式论文需要采用 XL-WiC 官方分类基线或成熟 WSD system，而不是用这组 exploratory likelihood 数字宣布跨任务优越性。

## 最终评分

- 原 semantic overwrite：**1/10，KILL**；
- 第一版 `semantic sensitivity + candidate prior` 因果解释：**KILL**；
- “Right Direction, Wrong Answer” score-level phenomenon：**7.5/10**；
- 经过 2×2 construct audit 的新题：**7.5/10，有条件 GO 进入正式 pilot**。

它不再是“再做一个 benchmark”，而是提出一个 measurement question 和可验证的 crossed-context audit。下一阶段必须扩大到自然非替换语境、其他数据资源和人工判断；若这些条件下 semantic-context component 消失，就停止，而不是继续缩题。
