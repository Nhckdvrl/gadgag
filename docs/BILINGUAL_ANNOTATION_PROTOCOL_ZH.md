# Doppelganger-JC 全量双语盲审协议

## 目的

验证自动抽取的两个 lexical options 是否真正代表 source context 中的正确词义与 cross-lingual shortcut 词义。该步骤需要两位能独立阅读中文、日文的人工标注者；模型输出不能替代人工效度验证。

## 覆盖范围与盲法

- 354 个 paired words，JA→ZH 与 ZH→JA 各一行，因此每位标注者 708 行。
- 两位标注者的行顺序、A/B option 顺序分别随机化。
- 标注者不可查看 `private_unblinding_key.csv`、模型结果或另一位标注者答案。
- 若标注者知道研究假设，只说明“检查选项质量”，不说明预期哪个条件更强。

## 每行问题

1. A 是否准确表达被 `[[...]]` 标记表达在上下文中的 intended sense：`yes/no/uncertain`。
2. B 同上。
3. A、B 作为 lexical rendering 的自然度：1（完全不自然）到 5（自然）。
4. 两个选项是否属于可比较的 grammatical type：`yes/no/uncertain`。
5. 哪个更符合 source context：`A/B/tie/neither`。
6. confound code，可多选，用 `+` 连接：
   - `FRAGMENT`：抽出的片段离开整句无法判断；
   - `GRAMMAR`：两项语法类型不匹配；
   - `LENGTH`：长度差本身可能决定答案；
   - `MULTI_DIFF`：整句翻译除目标词外还有重要差异；
   - `BOTH_VALID` / `NEITHER_VALID`；
   - `OTHER`，并在 comment 解释。

## 预注册保留标准

一行进入 confirmatory set 必须满足：

- 两位标注者都认为 gold option 表达 intended sense；
- 至少一位明确认为 shortcut option 不表达 intended sense，另一位不得判定它明确正确；
- 两项 naturalness 均值至少 3；
- grammatical type 不得由任一标注者判定为 `no`；
- 不含未解决的 `MULTI_DIFF`、`BOTH_VALID` 或 `NEITHER_VALID`。

分歧项由第三步 adjudication 解决，但 adjudicator 仍不可看模型结果。

## 一致性与报告

- preferred option：报告 Cohen's kappa 与 raw agreement；
- yes/no/uncertain：报告加权 kappa；
- naturalness：报告 ICC(2,1) 或 Spearman，并给每项分布；
- 同时报告保留率、按方向保留率、各 confound 数量。
- 主结果必须同时给 full 354 intent-to-treat 与 validated subset；不能只报告筛选后更好看的结果。

## 生成命令

```bash
PYTHONPATH=src .venv/bin/python src/prepare_bilingual_annotation.py \
  --data-root external/Doppelganger-JC
```

含原始 benchmark 文本的 CSV 写入被忽略的 `data/annotation_packets/`，不得在未核对上游数据条款前公开提交。
