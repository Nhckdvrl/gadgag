# Language-specific control 构建与双语验证协议

## 为什么需要这一组

导师要求至少比较：同形异义、同形同义、以及只属于某一语言的普通词。人类双语研究也常以 language-specific words 判断跨语言冲突是否超过 ordinary language-selective lexical processing。这一组是 identification control，不是 contribution。

它不能直接估计 `L1→L2 language effect`：一个真正 language-specific 的词在另一语言中没有对称 lexical item。预注册用途是 one-language contextual evidence/decision baseline，并检验 target-patching 的一般语境效应是否只在跨语言共享表记中出现。

## 操作性定义

候选必须：

- 是两个 CJK 字符组成的 lexical form；
- 在本语言词典中出现；
- NFKC-normalized exact form 不出现在另一语言词典；
- 本语言 `wordfreq ≥ 2`；
- 在 Tatoeba 本语言自然句中以 tokenizer-recognized lexical token 出现；
- contextual POS 属于 N/V/ADJ/ADV。

资源为 JMdict、CC-CEDICT 与 Tatoeba。词典非收录不证明词在现实中绝对不存在，因此公开报告只能称 `dictionary-operationalized language-specific`；最终标签必须经双语人工判断。

## Outcome-blind matching

对已经冻结的 24 个 false friends，分别匹配中文侧和日文侧：

- contextual POS exact；
- 本语言 frequency；
- character length；
- Qwen3/Gemma subword length；
- English gloss length；
- design-only Qwen2.5 contextual difficulty；
- 每个协变量 `|SMD| ≤ .10`，二阶矩差 ≤ .25。

由于一个中文 false-friend side 的 POS 为 `OTHER`，而严格 language-specific pool 无相同支持，中文 final 为 23 项，日文为 24 项；该排除在 target outcomes 前完成。final max |SMD| 为 ZH .09446 / JA .09668。4× 人工验证池为 ZH 92 / JA 96，max |SMD| 为 .09739 / .09675。

## 人工盲审

每位双语者 188 行，行顺序独立随机，不显示模型结果、matching distance 或 target false friend。判断：

- word 是否是指定语言中的有效 lexical item；
- context 是否表达 proposed meaning；
- naturalness 1–5；
- 自动 contextual POS 是否正确；
- blocking confound：`WRONG_LANGUAGE`、`WRONG_SENSE`、`UNNATURAL`、`POS_MISMATCH`、`PROPER_NAME`、`MULTIWORD_OR_SUBSTRING`、`OTHER_BLOCKING`。

只有两人都判 word valid/context meaning yes、自然度均值至少 3、无人判 POS no 且无 blocking code 的候选才进入重新 matching。两项关键判断 Cohen's κ 必须 ≥ .60。

## Stop rule

人工过滤后，ZH 或 JA 任一侧少于 20 项，或任何冻结协变量 `|SMD| > .10`，则不把 language-specific control 纳入 collision-specific causal claim；不得通过查看 target outcomes、放宽 SMD 或更换困难样本修复。
