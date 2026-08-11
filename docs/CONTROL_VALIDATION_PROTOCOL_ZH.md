# 预匹配控制项双语盲审协议

## 目的与范围

词典 gloss overlap 只用于生成候选，不是 gold。两位中日双语者独立验证冻结的 192 项 control reservoir（96 true-friend、96 different-form translation）；标注包不显示 control 类型、matching distance、false-friend pairing 或模型结果。

推荐语言背景与 Doppel 标注相同：一位中文母语且日语高级，一位日语母语且中文高级。两人不得查看 `private_unblinding_key.csv` 或彼此答案。

## 每行字段

- 中文语境是否表达 proposed English meaning：`yes/no/uncertain`；
- 日文语境是否表达 proposed English meaning：`yes/no/uncertain`；
- 两语言中的实际语境义是否等价：`yes/no/partial/uncertain`；
- 中文、日文句子自然度：整数 1–5；
- 两侧 contextual POS 是否可比：`yes/no/uncertain`；
- `confound_code` 可留空，多个代码用 `+`：
  - `WRONG_SENSE`：至少一侧不是 proposed meaning；
  - `NOT_EQUIVALENT`：两侧实际词义不等价；
  - `UNNATURAL`：句子无法作为自然使用证据；
  - `POS_MISMATCH`：实际语境词性不匹配；
  - `PROPER_NAME`：普通词/专名或专名类别造成伪匹配；
  - `MULTIWORD_OR_SUBSTRING`：命中复合词或更长表达，而不是目标 lexical item；
  - `OTHER_BLOCKING`：必须在 comment 解释；
- confidence：整数 1–5。

## 自动保留与后续匹配

候选在 adjudication 前仅当以下全部满足才保留：两人均判两侧 meaning 为 `yes`；两人均判 cross-language equivalent 为 `yes`；两侧平均自然度均至少 3；任何人不得判 POS 为 `no`；不得含 blocking confound。

分析后不得直接挑“最像结果”的 controls。`private_valid_control_ids.csv` 只作为允许集合重新运行同一个 cardinality matching。最终必须：

- 至少保留 20 个 false friends；
- true-friend / translation-control 与 false friend 均为 1:1；
- 双语 contextual POS exact balance；
- 每个冻结协变量 `|SMD| ≤ .10`；
- target-model outcomes 在最终 freeze 前未读取。

任一条件失败即终止 collision-specific causal claim；不得降低平衡门槛或查看 outcomes 后换 controls。
