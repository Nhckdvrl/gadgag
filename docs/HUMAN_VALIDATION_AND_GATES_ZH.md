# 人工验证、重新匹配与确认性门槛

更新日期：2026-08-13

本文档是三套双语人工验证和 fail-closed confirmatory analysis 的唯一执行协议。研究叙事与结果以 `RESEARCH_STATUS_AND_EVIDENCE_ZH.md` 为准；本文件只规定数据效度、盲法、阈值、执行顺序与停止规则。

## 1. 当前状态

| Gate | 每位标注者工作量 | 计算准备 | 真实人工状态 |
|---|---:|---|---|
| Doppelganger-JC option validity | 708 行 | 完成 | 未完成 |
| True-friend / translation controls | 192 行 | 完成 | 未完成 |
| Language-specific controls | 188 行 | 完成 | 未完成 |

需要两位能独立阅读中文与日文的标注者。推荐配置是一位中文母语且日语高级、一位日语母语且中文高级。当前总状态为 `BLOCKED_ON_REAL_BILINGUAL_ANNOTATION`。

合成完整标注已经验证过滤、重新匹配、gate 解锁、24-pair causal analysis 和 language-specific contextual-lift analysis 可以端到端运行。它只验证工程流程，不能替代真实人工证据。

## 2. 通用盲法

- 两位标注者使用独立随机行顺序；存在 A/B 选项时，选项顺序也独立随机；
- 不得查看 `private_unblinding_key.csv`、模型输出、matching distance、target pairing 或另一位标注者答案；
- 候选生成与匹配在读取 confirmatory Qwen3/Gemma outcomes 之前冻结；
- 人工剔除规则和一致性阈值不得根据目标模型结果修改；
- 分歧可以 adjudicate，但 adjudicator 同样不能查看模型结果。

## 3. Gate 1：Doppelganger-JC option validity

### 目的与覆盖

验证自动抽取的两个 lexical options 是否真正代表 source context 的正确义和 cross-lingual shortcut 义。共354个paired words，每词JA→ZH和ZH→JA两行，因此708行/人。

### 每行判断

1. A、B 是否准确表达 `[[...]]` 在语境中的 intended sense：`yes/no/uncertain`；
2. A、B lexical rendering 自然度：1–5；
3. 两项是否为可比较的 grammatical type：`yes/no/uncertain`；
4. 哪项更符合 source context：`A/B/tie/neither`；
5. confound：`FRAGMENT`、`GRAMMAR`、`LENGTH`、`MULTI_DIFF`、`BOTH_VALID`、`NEITHER_VALID`、`OTHER`。

### 保留与可靠性

进入 validated confirmatory set 必须满足：两人均认可 gold sense；至少一人明确否定 shortcut，另一人不得明确认可；两项平均自然度≥3；无人判 grammatical type 为 `no`；无未解决的 `MULTI_DIFF/BOTH_VALID/NEITHER_VALID`。

- 两个 semantic judgment：weighted κ ≥ 0.60；
- naturalness：ICC(2,1) ≥ 0.50；
- 同时报告完整354项intent-to-treat和validated subset，不得只报告筛选后结果。

生成：

```bash
PYTHONPATH=src .venv/bin/python src/prepare_bilingual_annotation.py \
  --data-root external/Doppelganger-JC
```

## 4. Gate 2：true-friend / translation controls

### 目的与冻结设计

词典gloss overlap仅用于生成候选，不是gold。当前outcome-blind cardinality design保留24/27 false friends，并为true friend和different-form translation各匹配24项；最大 `|SMD|` 为0.08722/0.09717。每类另冻结96项validation reservoir。

### 每行判断

- 中文、日文语境是否表达 proposed meaning：`yes/no/uncertain`；
- 两侧实际语境义是否等价：`yes/no/partial/uncertain`；
- 两句自然度：1–5；
- contextual POS 是否可比：`yes/no/uncertain`；
- confound：`WRONG_SENSE`、`NOT_EQUIVALENT`、`UNNATURAL`、`POS_MISMATCH`、`PROPER_NAME`、`MULTIWORD_OR_SUBSTRING`、`OTHER_BLOCKING`；
- confidence：1–5。

### 保留与重新匹配

仅当两人均判两侧meaning为`yes`、跨语言等价为`yes`、两侧平均自然度≥3、无人判POS为`no`且无blocking confound时，候选进入允许集合。然后重新运行同一cardinality matching，必须满足：

- 至少20个false friends；
- 两类control分别与false friend 1:1；
- bilingual contextual POS exact balance；
- 每个冻结协变量 `|SMD| ≤ 0.10`；
- target outcomes 在最终freeze前未读取。

两个context-meaning判断的κ均须≥0.60。失败时删除collision-specific causal claim，不得降低平衡阈值或看outcome换control。

## 5. Gate 3：language-specific controls

### 目的与操作性定义

这组提供ordinary language-selective lexical-processing baseline，不能估计对称的cross-language LCE。公开名称必须是 `dictionary-operationalized language-specific`，因为另一词典未收录不等于现实中绝对不存在。

候选为两个CJK字符，在本语言词典出现、NFKC exact form不在另一词典出现、`wordfreq ≥ 2`，并在Tatoeba本语言自然句中作为lexical token出现，contextual POS属于N/V/ADJ/ADV。

当前自然语境池为中文7,943、日文7,923；计算匹配为中文23、日文24，max `|SMD|=0.09446/0.09668`；人工池为中文92、日文96，max `|SMD|=0.09739/0.09675`。

### 每行判断与保留

每人188行，判断word是否是指定语言的有效lexical item、context是否表达proposed meaning、naturalness 1–5、contextual POS是否正确，以及 `WRONG_LANGUAGE/WRONG_SENSE/UNNATURAL/POS_MISMATCH/PROPER_NAME/MULTIWORD_OR_SUBSTRING/OTHER_BLOCKING`。

两人均判word/context有效、平均自然度≥3、无人判POS错误且无blocking code才进入重新匹配。word validity与context meaning的κ均须≥0.60。人工过滤后任一语言少于20项或任一协变量 `|SMD|>0.10`，则该control不进入collision-specific causal claim。

## 6. 强制执行顺序

```bash
# 1. Doppel：708行/人
PYTHONPATH=src .venv/bin/python src/analyze_bilingual_annotations.py \
  --annotator-1 <doppel_1.csv> --annotator-2 <doppel_2.csv> \
  --key data/annotation_packets/doppel_full/private_unblinding_key.csv

# 2. True/translation：192行/人
PYTHONPATH=src .venv/bin/python src/analyze_control_validation.py \
  --annotator-1 <controls_1.csv> --annotator-2 <controls_2.csv> \
  --key data/annotation_packets/prematched_controls/private_unblinding_key.csv \
  --output-dir data/annotation_packets/prematched_controls/analysis

# 3. 仅用双人通过项重新匹配
PYTHONPATH=src .venv/bin/python src/finalize_prematched_controls.py \
  --shortlist data/prematched_controls/private_control_shortlist.csv \
  --difficulty data/prematched_controls/reference_difficulty.csv \
  --stingray-root external/StingrayBench/data \
  --valid-controls data/annotation_packets/prematched_controls/analysis/private_valid_control_ids.csv \
  --minimum-false-items 20

# 4. Language-specific：188行/人
PYTHONPATH=src .venv/bin/python src/analyze_language_specific_validation.py \
  --annotator-1 <language_specific_1.csv> \
  --annotator-2 <language_specific_2.csv> \
  --key data/annotation_packets/language_specific_controls/private_unblinding_key.csv \
  --output-dir data/annotation_packets/language_specific_controls/analysis

# 5. 仅用双人通过项重新匹配language-specific controls
PYTHONPATH=src .venv/bin/python src/select_language_specific_controls.py \
  --shortlist data/language_specific_controls/private_shortlist.csv \
  --difficulty data/language_specific_controls/reference_difficulty.csv \
  --stingray-root external/StingrayBench/data \
  --eligible-false-matching data/prematched_controls/frozen_final_matching.csv \
  --valid-controls data/annotation_packets/language_specific_controls/analysis/private_valid_control_ids.csv \
  --ratio 1 --smd-bound .1

# 6. 三套人工gate全部通过才返回0
PYTHONPATH=src .venv/bin/python src/check_final_measurement_gates.py \
  --doppel-summary data/annotation_packets/doppel_full/analysis/annotation_summary.json \
  --control-summary data/annotation_packets/prematched_controls/analysis/control_validation_summary.json \
  --final-matching-manifest data/prematched_controls/final_matching_manifest.json \
  --language-specific-summary data/annotation_packets/language_specific_controls/analysis/summary.json \
  --language-specific-manifest data/language_specific_controls/final_manifest.json \
  --output data/annotation_packets/final_gate_unlocked.json
```

Confirmatory evaluator会先读取gate；未解锁时在tokenizer/model加载前终止。解锁后才运行Qwen3/Gemma target-span residual与MLP primary analysis。预注册primary window为relative depth 0.10–0.75；attention只作稳定性负对照。

## 7. Stop与claim policy

- Doppel reliability失败：暂停B的强主张并修订measurement；
- 有效matched sets少于20或平衡失败：A的collision-specific mechanism **KILL**，B保留；
- matching通过但target causal excess消失：A **KILL**，如实报告负结果；
- 三道人工作业、matching和target causal excess全部通过：A升级为确认性机制贡献，标题才可使用`Causal Decomposition`；
- 在解锁前不扩模型、语言对、SAE/neuron或mitigation。

含benchmark原文的盲审CSV位于被忽略的 `data/annotation_packets/`，未经上游许可审查不得公开提交。
