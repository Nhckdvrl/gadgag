# 最后两道 measurement gate：冻结结果与执行交接

日期：2026-08-11

## 最终判断

硕士课题 **GO**，建议当前使用较保守的题目：

> **When Context and Language Disagree: Disentangling Cross-Lingual Lexical Arbitration in Multilingual LLMs**
>
> **文脈と言語慣習が衝突するとき：多言語 LLM における語彙的仲裁の分解**

行为主线已经不依赖 collision-specific mechanism：模型能提取 contextual semantic evidence，但 lexical form、sentence language 与答案边界决定该证据能否转化为正确选择。只有本文件的两道人工作业和最终匹配全部通过后，题目才升级为 `Causal Decomposition`，并主张 false-friend-specific causal excess。

## Gate A：Doppelganger-JC 全量双语效度

自动设施已完成，但真实人工标注尚未完成，因此状态为 **BLOCKED ON HUMANS**：

- 354 个词 × 两方向 = 每位标注者 708 行；
- 两份独立随机顺序，A/B 独立盲化；
- 标注者 1：中文母语、日语高级；标注者 2：日语母语、中文高级（最优配置）；
- 标注者不能查看模型输出、另一人的标注或 unblinding key；
- 完整规则见 `BILINGUAL_ANNOTATION_PROTOCOL_ZH.md`；
- 分析脚本拒绝空白、非法标签、重复或缺行，并计算 weighted κ、Cohen's κ、ICC(2,1)、Spearman 与严格保留集。

必须报告 354 项 intent-to-treat 结果及 human-validated subset，不能只报告筛选后结果。两个关键语义判断的 weighted κ 预注册最低为 0.60，自然度 ICC(2,1) 最低为 0.50；低于门槛先 adjudication/修订 measurement，不能跑新的“漂亮结果”绕开。

## Gate B：outcome-blind pre-matched controls

这一计算设计门槛已经通过，且没有读取 Qwen3-8B/Gemma-3-12B 的 target intervention outcomes。

### 候选构建

- false friends：StingrayBench ZH–JA 严格 exact-form 27 项；
- true friends：JMdict 与 CC-CEDICT 的同表记、英文 gloss overlap 候选；
- different-form translation controls：两词典中英文 gloss 相同但中日表记不同的候选；
- natural contexts：Tatoeba 中文、日文句子；
- 扩大后共有 11,000 个带双语自然语境候选（true 1,760；translation 9,240）；
- shortlist：5,138 个 target-to-candidate 邻接，1,007 个唯一 true controls、1,552 个唯一 translation controls。

匹配特征在 target outcomes 之前冻结：双语 contextual POS、中文/日文 `wordfreq`、频率比、字符长度、Qwen3/Gemma tokenizer 长度、gloss 长度，以及独立设计参考模型 Qwen2.5-7B 的 baseline difficulty。参考模型不进入 confirmatory target analysis。

### 基于整数规划的冻结结果

采用 joint cardinality matching，同时最大化保留的 false friends，并对两类控制施加：

- 双语 contextual POS exact balance；
- 每个连续协变量 `|SMD| ≤ 0.10`；
- 标准化二阶矩差 ≤ 0.25，避免只匹配均值却让方差塌缩；
- 中文和日文控制词均不得重复。

结果保留 24/27 个 false friends；两类控制各 24 项。排除的 false IDs 为 `zh_ja_012`、`zh_ja_016`、`zh_ja_053`。最大绝对 SMD：

| control group | N | max \|SMD\| |
|---|---:|---:|
| true friend | 24 | 0.08722 |
| different-form translation | 24 | 0.09717 |

该方法与“先最大化满足明确平衡约束的样本，再配对”的 cardinality matching 原理一致；它解决了旧控制池 1-SD common-support 为零的问题，但不自动保证词义与句子质量。

### 人工质量门槛与冗余池

自动抽查发现真实问题，例如 `天津` 的日语句实际表示天津饭而不是城市；这证明词典 gloss overlap 不能当 gold。为避免人工剔除后无替代项，已在同一 outcome-blind 规则下冻结每类 96 个候选，即对 24 个目标提供 4 倍冗余。两类冗余池的最大 |SMD| 为 0.09994 / 0.09955。

每位控制标注者需盲审 192 行，判断：两侧 context 是否表达 proposed meaning、跨语言词义是否等价、自然度、POS 可比性与 blocking confounds。两人都通过的候选才进入最终 cardinality matching。最终必须仍保留至少 20 个 false friends、每类 1:1 controls 且所有 `|SMD| ≤ 0.10`；否则 **删除 false-friend-specific causal excess 主张**。

## 强制执行顺序

```bash
# 1. 分析两位 Doppel 标注者的完整 708 行
PYTHONPATH=src .venv/bin/python src/analyze_bilingual_annotations.py \
  --annotator-1 <completed_doppel_1.csv> \
  --annotator-2 <completed_doppel_2.csv> \
  --key data/annotation_packets/doppel_full/private_unblinding_key.csv

# 2. 分析两位 control 标注者的完整 192 行
PYTHONPATH=src .venv/bin/python src/analyze_control_validation.py \
  --annotator-1 <completed_controls_1.csv> \
  --annotator-2 <completed_controls_2.csv> \
  --key data/annotation_packets/prematched_controls/private_unblinding_key.csv \
  --output-dir data/annotation_packets/prematched_controls/analysis

# 3. 只用双人均通过的 controls 重新冻结 1:1 matching
PYTHONPATH=src .venv/bin/python src/finalize_prematched_controls.py \
  --shortlist data/prematched_controls/private_control_shortlist.csv \
  --difficulty data/prematched_controls/reference_difficulty.csv \
  --stingray-root external/StingrayBench/data \
  --valid-controls data/annotation_packets/prematched_controls/analysis/private_valid_control_ids.csv \
  --minimum-false-items 20

# 4. 两个 gate 全部通过才会返回 0；否则返回 2，禁止 confirmatory target analysis
PYTHONPATH=src .venv/bin/python src/check_final_measurement_gates.py \
  --doppel-summary data/annotation_packets/doppel_full/analysis/annotation_summary.json \
  --control-summary data/annotation_packets/prematched_controls/analysis/control_validation_summary.json \
  --final-matching-manifest data/prematched_controls/final_matching_manifest.json \
  --output data/annotation_packets/final_gate_unlocked.json

# 5. 仅在上一步 UNLOCKED 后运行；脚本会再次检查 gate，不能误用旧 controls
CUDA_VISIBLE_DEVICES=0 PYTHONPATH=src .venv/bin/python src/evaluate_target_component_patching.py \
  --data-root external/StingrayBench/data --pair zh_ja \
  --model Qwen/Qwen3-8B --tag qwen3_8b_confirmatory \
  --prematched-controls data/prematched_controls/private_final_controls.csv \
  --gate-status data/annotation_packets/final_gate_unlocked.json \
  --output-path results/extensions/target_component_qwen3_8b_confirmatory.jsonl

CUDA_VISIBLE_DEVICES=0 PYTHONPATH=src .venv/bin/python src/evaluate_target_component_patching.py \
  --data-root external/StingrayBench/data --pair zh_ja \
  --model google/gemma-3-12b-it --tag gemma3_12b_confirmatory \
  --prematched-controls data/prematched_controls/private_final_controls.csv \
  --gate-status data/annotation_packets/final_gate_unlocked.json \
  --output-path results/extensions/target_component_gemma3_12b_confirmatory.jsonl

PYTHONPATH=src .venv/bin/python src/analyze_prematched_target_components.py \
  --inputs results/extensions/target_component_qwen3_8b_confirmatory.jsonl \
           results/extensions/target_component_gemma3_12b_confirmatory.jsonl \
  --matching data/prematched_controls/frozen_final_matching.csv \
  --gate-status data/annotation_packets/final_gate_unlocked.json \
  --output results/extensions/prematched_confirmatory_excess.csv
```

确认性 primary window 在读取 outcomes 前固定为相对深度 0.10–0.75；对每个冻结 pair 先跨该窗口取均值，再做 paired item bootstrap。residual / MLP 是预注册主成分，attention 是稳定性负对照；逐层曲线只作定位和可视化。

## Stop / claim policy

- Doppel reliability 或完整性失败：重建 measurement；B 暂停强主张。
- 人工有效 controls 后不足 20 组或平衡失败：collision-specific mechanism **KILL**；行为分解 B 保留。
- 匹配通过但 target causal excess 消失：collision-specific mechanism **KILL**；这仍是有效负结果。
- 两道人工作业、匹配、target causal excess 全过：升级为 `Causal Decomposition`，再写机制主张。
- 不在这些 gate 之前扩模型、语言对、SAE、neuron、mitigation。

## 方法与资源依据

- [Cardinality matching](https://arxiv.org/abs/1404.3584)把最大样本保留和显式协变量平衡约束分开，适合当前共同支持有限的设计。
- [Austin (2011)](https://pmc.ncbi.nlm.nih.gov/articles/PMC3120982/)说明 caliper matching 需要预先规定距离限制；本项目采用更严格且可审计的逐协变量 SMD 约束，而不是事后挑邻居。
- [JMdict 官方项目](https://www.edrdg.org/jmdict/j_jmdict.html)与 [Tatoeba](https://tatoeba.org/en/about)仅提供候选和自然句，不替代双语人工语义判断。
- 所有下载日期、URL 与 SHA-256 记录在 `data/prematched_controls/resource_manifest.json`；原始受许可文本和盲审包不提交仓库。

## 给导师的最终三句话

1. 题目已经 GO：母题仍是 cross-lingual homograph，但一般问题是多语言模型如何在 contextual semantics 与 language-conditioned lexical convention 冲突时进行仲裁。
2. 行为分解已跨数据生成方式、文字系统、语言对和模型复现；旧 controls 的共同支持失败也已通过 target-first、outcome-blind cardinality design 在计算层面解决为 24×2 个严格平衡 controls。
3. 目前唯一不能诚实宣称完成的是两位真实双语者的盲审；流程、192/708 行标注包、自动一致性分析和 fail-closed gate 均已就绪，人工通过后才允许跑 collision-specific confirmatory causal analysis。
