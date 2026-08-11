# 给导师的短汇报（2026-08-12）

## 这周做了什么

我把 cross-lingual homograph 剩余的三个候选全部做了 kill-or-go pilot。使用 4 个 Qwen/Gemma 模型、StingrayBench 的两个语言对、Doppelganger-JC 的 354 个双向自然上下文，以及 true cognate / different-form translation / English polysemy controls。所有判断使用 candidate log-probability margin 和 item-level paired bootstrap，不用生成准确率或挑案例。

## 最重要的新结果

独立 Doppelganger 数据上，去掉同形表记后，仅凭 surrounding context，4/4 模型都显著优于 matched unrelated context；但把同形表记放回去后，3/4 模型反而显著变差或没有改善。

这意味着模型不是单纯“没有读懂上下文”。它往往已经提取了正确的 contextual evidence，但 shared form 与 sentence-language convention 会在后续 decision 中抵消该证据。raw accuracy 因而混合了至少两种能力。

因果 patching 支持这个解释。false friend 与普通 English polysemy 的 semantic layer profile 几乎相同（两模型 correlation 0.982/0.999），说明基础 sense resolution 是通用 WSD；但 false friend 额外出现了显著大于 true cognate 和 different-form control 的 late language-convention effect，且 Qwen3/Gemma-12B 方向一致。

## 我建议确定的题目

> **When Context and Language Disagree: Causal Decomposition of Cross-Lingual Lexical Arbitration**

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
5. 如果 late language excess 在严格 matching 后仍存在，再尝试 collision-triggered late-layer debiasing，而不是先发明训练方法。

## 没有保留的候选

Cross-turn carryover 在默认协议下有明显 sense-specific persistence，lag=8 仍存在；但不用同形表记的 semantic prime 已解释大部分效应，换 assistant-prime 后只有一半 model×language-pair 组合稳定。因此它更像 general conversational semantic anchoring，不足以成为 cross-lingual homograph 主课题。

## 需要导师判断的点

我希望导师主要判断：

1. “benchmark construct decomposition + causal arbitration”是否足够形成一个统一题目；
2. 正式实验优先扩第二语言对，还是先做 50–100 个日中 item 的 bilingual blind validation；
3. 是否接受先以现象/机制为主、mitigation 只在后半段通过 kill gate 后再做。

完整数字、判死刑标准和 closest-work 边界见 `docs/THREE_CANDIDATE_VERDICT_ZH.md`。
