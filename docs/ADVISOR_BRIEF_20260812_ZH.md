# 给导师的短汇报（2026-08-12，历史快照）

> 当前统一题目、A/B/C 归属和证据边界请以
> [`RESEARCH_STATUS_AND_EVIDENCE_ZH.md`](RESEARCH_STATUS_AND_EVIDENCE_ZH.md)
> 为准。

> 2026-08-11 最终设计更新：旧 controls 的 common-support 失败已经用 outcome-blind、target-first 的 cardinality matching 修复。新候选池含 11,000 个双语自然语境候选；在不读取 target-model outcomes 的条件下保留 24/27 false friends，并为 true-friend / different-form translation 各冻结 24 个 controls，所有协变量 `|SMD| < .10`。另冻结每类 96 个候选供双语盲审后替换。计算 gate 已通过，真实人工 gate 仍未完成，详见 `FINAL_MEASUREMENT_HANDOFF_ZH.md`。

> 2026-08-12 导师反馈后的定位更新：主问题不再写成宽泛的“accuracy 混合多种错误”，而是定位 cross-lingual lexical failure 发生于 contextual evidence extraction 还是后续 lexical arbitration。Tanwar 已做 cognate/non-cognate/homograph 与 incongruent sentences，RoDEval 已说明 WSD accuracy 不足，因此这两点都不作为 novelty。另按导师要求加入 language-specific baseline：outcome-blind final 为 ZH 23 / JA 24，max `|SMD|=.0945/.0967`，4× 人工池为 ZH 92 / JA 96。

## 这周做了什么

我把 cross-lingual homograph 剩余的三个候选全部做了 kill-or-go pilot，并继续执行了三道 formal gate。使用 4 个 Qwen/Gemma 模型、日中及两个非 CJK 语言对、Doppelganger-JC 的 354 个双向自然上下文，以及 true cognate / different-form translation / English polysemy controls。所有判断使用 candidate log-probability margin 和 item-level bootstrap，不用挑案例。

## 最重要的新结果

独立 Doppelganger 数据上，去掉同形表记后，仅凭 surrounding context，4/4 模型都显著优于 matched unrelated context；但把同形表记放回去后，3/4 模型反而显著变差或没有改善。

这意味着模型不是单纯“没有读懂上下文”。它往往已经提取了正确的 contextual evidence，但 shared form 与 sentence-language convention 会在后续 decision 中抵消该证据。raw accuracy 因而混合了至少两种能力。

因果 patching 支持这个解释。false friend 与普通 English polysemy 的 semantic layer profile 几乎相同（两模型 correlation 0.982/0.999），说明基础 sense resolution 是通用 WSD；但 false friend 额外出现了显著大于 true cognate 和 different-form control 的 late language-convention effect，且 Qwen3/Gemma-12B 方向一致。

第二语言对 Gate 也通过：Indonesian–Malay 30 项与 Indonesian–Tagalog 33 项上，target-masked natural context 相对 marker-matched unrelated context，在 4 模型 × 3 wrapper × 2 normalization 的 **48/48** 变体中 CI 全部大于 0。context extraction 不是汉字特例；但 surface form 的促进/抑制方向会随语言对变化。

新的 target-token 因果实验进一步发现：Qwen3/Gemma-12B 的目标词 residual 在早中层都能因果传递 semantic 和 language signal，MLP output 在两模型复现主要 language effect，attention-only 效应不稳定。因此可主张 target representation 与 MLP-level processing 参与仲裁，不能主张已发现具体 head/neuron circuit。

## 我建议确定的题目

> **When Context and Language Disagree: Disentangling Cross-Lingual Lexical Arbitration in Multilingual LLMs**

日语：

> **文脈と言語慣習が衝突するとき：多言語LLMにおける語義選択の因果的分解**

核心问题：

> multilingual LLM 在 lexical form、sentence language 和 contextual semantics 冲突时，如何组合证据并选择词义？错误发生在 context encoding，还是 late arbitration？

cross-lingual homograph 是实验床，但背后是 multilingual parameter sharing / lexical choice 的一般问题。

## 初步 idea

提出 **Crossed Lexical Arbitration (CLA)**：

1. `Language × Sense` crossed design 分解 semantic evidence 与 language convention；
2. independent natural contexts 验证 construct；
3. 固定 recipient 与英文输出，用 counterfactual activation patching 分别估计两种证据的 causal effect；
4. true cognate、different-form translation、monolingual polysemy 做 controls；
5. 先重建严格匹配的 control set；只有 language excess 在 matching 后仍存在，才尝试 collision-triggered debiasing。

## 没有保留的候选

Cross-turn carryover 在默认协议下有明显 sense-specific persistence，lag=8 仍存在；但不用同形表记的 semantic prime 已解释大部分效应，换 assistant-prime 后只有一半 model×language-pair 组合稳定。因此它更像 general conversational semantic anchoring，不足以成为 cross-lingual homograph 主课题。

## 当前硬限制与需要导师判断的点

自动设施已经准备好 354 项 × 双方向 × 两位标注者的盲化标注包，但人工双语验收不能由模型替代。旧 control pool 在“双语 POS exact + 每个 frequency/tokenization/gloss/difficulty 协变量 1 SD caliper”下为 **0 个可匹配对**；这个负结果没有被隐藏。现在已经按 false friend 反向构建并冻结严格平衡 controls，但词义/语境有效性必须由两位双语者盲审。人工通过后仍不足 20 组或 target causal excess 消失，就删除 collision-specific mechanism。

我希望导师主要判断：

1. “benchmark construct decomposition + causal arbitration”是否足够形成一个统一题目；
2. 是否可以立刻组织两名中日双语者完成 708 行/人的 blind validation；
3. 是否接受“人工通过后不足 20 组或 confirmatory excess 消失即删掉 collision-specific mechanism”；mitigation 只在前述 Gate 通过后再做。

完整数字、判死刑标准和 closest-work 边界见 `docs/FINAL_GATE_AUDIT_20260811_ZH.md`。
