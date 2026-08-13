# 研究题目、实验结果与证据状态（统一版）

更新日期：2026-08-13

本文档是当前项目的**唯一研究总纲**。它统一说明研究题目、论文叙事、A/B/C 的归属、已经完成的实验、真实结果、尚未完成的验证、解决方法的进入条件，以及给导师的讲解顺序。其他文档只承担实验复现、文献定位、人工验证或英文计划中的一种功能；若表述冲突，以本文和 `results/extensions/final_measurement_gate_status.json` 为准。

## 1. 当前结论

课题目前 **GO**，但 GO 的是行为层面的 lexical arbitration 问题，不是已经完成的机制论文。

推荐工作标题：

> **When Context and Language Disagree: Disentangling Cross-Lingual Lexical Arbitration in Multilingual LLMs**
>
> **当语境与语言惯例冲突时：多语言 LLM 中跨语言词义仲裁的分解**
>
> **文脈と言語慣習が衝突するとき：多言語 LLM における語彙的仲裁の分解**

只有在人工作业、重新匹配和 confirmatory causal analysis 全部通过后，标题才可升级为 `Causal Decomposition`。

主问题不是“false friend 是否更难”，而是：

> **当局部语境支持的词义与句子语言对同一表记的惯用词义相冲突时，模型的错误发生在语义证据抽取阶段，还是模型已经抽取了正确证据、却在最终词义选择的仲裁阶段失败？**

这个问题有分量，因为两种失败需要完全不同的解释和处理：前者是 context understanding 不足；后者是已有语义证据没有成功控制 lexical decision。Cross-lingual homograph 不是题目的全部，而是把表记、语言惯例和语境意义置于可控冲突中的自然实验床。

### 本轮完善完成了什么

- 重新定义 Main RQ 以及 RQ1/RQ2/RQ3，并把原 A/B/C 放回同一条论证链；
- 逐论文重做 positioning matrix，不再把 benchmark、incongruent sentence 或 beyond-accuracy 当 novelty；
- 按导师要求补入 language-specific word，形成五类 identification controls；
- 构建 language-specific 自然语境池：中文 7,943、日文 7,923；
- outcome-blind 计算匹配：中文 23 项（max `|SMD|=0.0945`）、日文 24 项（max `|SMD|=0.0967`）；
- 冻结 4× 人工验证池：中文 92 项、日文 96 项，全部 max `|SMD|<0.10`；
- 生成两份独立随机顺序、每人 188 行的 language-specific 双语盲审包；
- 将 Doppel、true/translation controls、language-specific controls 三套人工验证全部接入 fail-closed gate；
- confirmatory Qwen3/Gemma 程序会先检查 gate，未解锁时在加载模型前终止；
- 用合成的完整标注完成工程 dry run，验证人工过滤、重新匹配、gate 解锁、24-pair causal analysis 和 language-specific contextual-lift analysis 可以端到端执行。

最后一项只证明**代码和数据流可运行**。合成标注不是人工证据，不能用于解锁真实确认性结论；仓库当前状态仍为 `BLOCKED_ON_REAL_BILINGUAL_ANNOTATION`。

### 锁定后的整篇研究叙事

研究严格按以下四层推进，后一层不能代替前一层：

| 层次 | 要回答的问题 | 对应工作 | 当前状态 |
|---|---|---|---|
| 1. 现象 | 模型是否已经获得正确 contextual evidence，却仍没有作出正确 lexical decision？ | B / crossed-context behavior | **强 GO** |
| 2. 特异性 | 该 evidence–decision gap 是否超出普通 WSD、词频、表记和题目难度？ | 五类 matched controls + human validation | 计算设计通过，人工未完成 |
| 3. 机制 | Language convention 在何处因果性地影响最终仲裁？ | A / target-span residual、MLP | exploratory；confirmatory 锁定 |
| 4. 解决 | 能否保留已抽取的语境证据，避免可见同形表记把最终选择拉回错误语言惯例？ | Context-Preserving Lexical Arbitration（暂名） | 仅为预注册方向，尚未作为贡献 |

这一结构的核心贡献顺序是“发现—识别—解释—解决”，但当前论文最低可成立单位是前两层。若A失败，研究仍可作为严格的行为/measurement工作；若前两层失败，则不允许靠一个方法上的accuracy提升救题。

解决方法的初步原则不是拆token、重做embedding或恢复collision-aware replay，而是利用B的直接观察：`masked context` 已包含正确证据，`full context` 不应在恢复词形后丢失这份证据。可以比较 `M_masked` 与 `M_full`，用context-preservation objective约束恢复target后的正确义margin不下降。它必须与ordinary WSD contrastive training、masked-context auxiliary training、language tag、calibration和等预算SFT比较，并同时保护true friend、translation、language-specific和总体语言能力。只有真实人工验证和collision-specific identification通过后才运行该方法实验。

## 2. 原 A、B、C 现在分别在哪里

| 原候选 | 现在的归属 | 当前状态 | 在最终研究中的作用 |
|---|---|---|---|
| **A — Language Gating / Causal Gating** | **RQ3：Arbitration mechanism** | **条件 GO，确认性分析仍锁定** | 用 target-span residual/MLP intervention 解释 B 中“读懂但选错”的行为悖论；不能独立宣称特殊 circuit |
| **B — XCA / Crossed-Context Audit** | **RQ1：Evidence extraction；整篇研究的行为骨架** | **强 GO** | 用完整 `Language × Sense` 正交设计、mask 和自然语境对照，分离 contextual semantic evidence 与 language-conditioned evidence |
| **C — Cross-turn semantic carryover** | 不再属于主 RQ | **主线 KILL** | 作为负结果/附录保留：现象主要可由一般 semantic priming 或 conversational anchoring 解释 |

另需澄清：更早的 **Semantic Overwrite / Collision-aware Replay** 在 A/B/C 形成之前就已被实验否定。它不是现在的 C，也不再是候选题目或方法方向。

最终结构不是把 A 和 B 生硬拼接：

1. **B 发现并测量问题**：contextual evidence 可能存在，但最终答案仍错误；
2. **RQ2 检查它是否真是 collision-specific**：用五类严格控制排除普通词汇难度和普通 WSD；
3. **A 尝试解释问题**：检验 semantic evidence 与 language convention 在最终选择中何时产生因果影响；
4. **C 不进入主故事**。

## 3. 三个子问题与实验对应关系

### RQ1 — Evidence extraction（B，已获得强 pilot 证据）

固定句子语言，只改变局部语境支持的意义时，模型是否能提取正确 sense evidence？目标词被遮住后，这个 evidence 是否仍然存在？

对应实验：完整 `Language × Sense` 四格、target masking、language-only、marker-matched unrelated context、repeated gloss、Doppelganger-JC natural non-replacement validation、非 CJK 重复。

### RQ2 — Collision specificity（设计已完成，人工效度未完成）

正确语境证据存在却没有转化为正确选择的现象，是否特别来自 exact-form cross-lingual collision，还是普通词汇难度、共享表记、翻译关系或一般 WSD 就能解释？

五类 identification controls：

| 类型 | 表记关系 | 语义关系 | 控制目的 |
|---|---|---|---|
| False friend | 跨语言完全同形 | 不同义 | 目标冲突 |
| True friend / cognate | 跨语言完全同形 | 同义 | 排除“只因 shared form” |
| Language-specific word | 仅一侧词典收录 | 不适用 | 普通语言选择性词汇加工基线 |
| Different-form translation | 不同形 | 同义 | 分离跨语言语义与共享表记 |
| Monolingual polysemy | 同语言同形 | 多义 | 一般 WSD 基线 |

这些 control 是识别条件，不是 novelty 本身。

### RQ3 — Arbitration mechanism（A，条件性机制部分）

在固定 recipient 和固定英文输出候选时，semantic evidence 与 language-conditioned convention 在 target span 的 residual/MLP 中如何影响最终 margin？False friend 是否有超出 matched controls 的 language excess？

现有 A 只能支持“机制假设值得继续检验”，不能支持“已定位一个 homograph-specific circuit”。

## 4. B：已完成的行为证据

### 4.1 Stingray exact-form `Language × Sense` 分解

严格保留 NFKC 完全同形且目标表记真实出现在四个上下文中的项目：ZH–JA 27 项、ID–TL 33 项。模型为 Qwen2.5-7B-Instruct、Qwen3-8B、Gemma-3-4B-IT、Gemma-3-12B-IT；测试 plain/chat、mean/sum likelihood 和三种 wrapper。

| 检验 | 结果 | 可支持的解释 |
|---|---:|---|
| 完整语境 semantic effect | 92/96 个协议变体的 95% CI > 0 | 改变局部意义会系统改变词义 margin |
| 官方 chat 子集 | 48/48 | 主结果不是 plain prompt 特例 |
| plain stress test | 44/48 | 仍强，但存在 prompt sensitivity |
| 遮蔽 target 后的 semantic effect | 91/96 | 大部分 sense evidence 来自 surrounding context，不依赖看到 homograph |
| language-only | 4/96 正、2/96 负 | 只有语言身份基本无法重现 semantic effect |
| marker-matched unrelated context | 1/96 正、3/96 负 | 长度/标记等表面结构不能解释结果 |
| 独立 gloss variants | 48/48 aggregate CI > 0 | 结果不依赖单一答案措辞 |

这里的 96 是 `model × pair × prompt × normalization × wrapper` 的协议变体，不是 96 次独立实验或 96 个独立样本。统计单位仍是 item。

### 4.2 只使用自然 correct-use cells 的生态检查

在不使用 translated/replaced conflict cell 的情况下：

- masked natural context 优于 marker-matched unrelated context：82/96；
- 官方 chat 子集：46/48；
- full natural context 优于显式 `language + target` cue：仅 36/96，并有 16 个显著反转。

因此安全结论不是“context 总是胜过 language”，而是：模型确实能从自然 surrounding context 中抽取可测的语义证据，但这份证据是否成为最终答案受到 target form、language convention 和 decision layer 的共同影响。

### 4.3 独立 Doppelganger-JC 自然语境验证

354 个日中词，每词两个方向；source contexts 为独立人写语境，不是把同一句中的目标词简单替换。两个选项顺序均运行并平均，四个模型结果如下（mean-logp paired effect）：

| 模型 | full − unrelated | masked − unrelated | full − masked |
|---|---:|---:|---:|
| Qwen2.5-7B | +3.940 [2.932, 4.921] | +4.500 [3.625, 5.378] | -0.560 [-1.250, 0.105] |
| Qwen3-8B | -0.095 [-0.112, -0.078] | +0.026 [0.015, 0.037] | -0.121 [-0.135, -0.107] |
| Gemma-3-4B | -0.067 [-0.709, 0.593] | +3.033 [2.504, 3.570] | -3.101 [-3.586, -2.623] |
| Gemma-3-12B | +3.594 [2.920, 4.269] | +3.815 [3.215, 4.390] | -0.220 [-0.684, 0.240] |

关键发现：

1. 4/4 模型在 target 被 mask 后，natural context 均显著优于同语言 unrelated context；
2. 恢复 homograph 后，没有一个模型显著改善；Qwen3 和 Gemma-4B 反而显著变差；
3. 这给出最重要的行为悖论：**正确 contextual evidence 可以存在，却没有转化为正确 lexical decision；可见表记有时会抵消已经存在的证据。**

限制：候选翻译的最小差异片段由确定性规则抽取，尚未完成两位 bilingual reviewers 的盲审。因此它是强 pilot evidence，不是最终 gold measurement。

### 4.4 非 CJK 重复

在 Indonesian–Malay 与 Indonesian–Tagalog 上，masked natural context 相对 marker-matched unrelated context 的 CI 在 48/48 个预设协议变体中为正。这表明核心 evidence-extraction 现象不依赖汉字系统，但仍不能据此声称跨所有语言普遍成立。

### 4.5 决策层敏感性

Content-free calibration 把平均双方向正确率从 ZH–JA 的 31.9% 改为 46.5%，从 ID–TL 的 41.0% 改为 55.2%。这说明 absolute accuracy 会混入明显的 answer/decision bias。Calibration 是现有 baseline；本研究的贡献不能写成“首次发现 calibration 有用”。

## 5. A：已有机制证据及其边界

### 5.1 已完成 pilot

现有设计包含 20 false friends、20 true friends、16 different-form translations 和 20 English monolingual polysemy items；在 Qwen3-8B 与 Gemma-3-12B 上对 answer-boundary residual state 做逐深度 causal patch。

已有结果：

- false-friend behavioral accuracy 为 0.65 / 0.70；monolingual polysemy 为 0.625 / 0.675；未匹配难度下二者接近；
- causal patch 在两个模型都能显著改变 sense margin，不是只训练 probe 后得到的相关性；
- false-friend 与 monolingual-polysemy semantic curve 的相关为 0.982（Qwen3）与 0.999（Gemma），peak layer 一致；
- target-span residual intervention 在两模型复现 semantic 和 language effect；MLP 能复现主要 language signal；attention-only effect 不稳定；
- 旧分析出现较晚的 false-friend language excess，但旧 control pool 在严格 bilingual POS + 逐协变量 1-SD common-support 检查下为零配对，因此该 excess **不能作为确认性结论**。

最合理的待检假设是：cross-lingual homograph 使用一般 WSD-like semantic processing，但在把证据映射为最终 lexical choice 时，可能额外受到 language convention 的影响。

### 5.2 为什么 A 仍被锁定

旧 controls 没有共同支持，frequency、POS、tokenization、gloss difficulty 等可能解释表面的 group difference。新建的 outcome-blind matching 只说明计算平衡成功，还没有说明候选词义和自然句对双语者有效。

新的冻结设计：

- 自然语境候选 11,000 个（true 1,760；translation 9,240）；
- shortlist 含 1,007 个唯一 true controls、1,552 个唯一 translation controls；
- joint cardinality matching 保留 24/27 false friends、24 true friends、24 translation controls；
- 排除 `zh_ja_012`、`zh_ja_016`、`zh_ja_053`；
- 最大 `|SMD|`：true 0.08722，translation 0.09717；
- 每类另冻结 96 个 4× validation reservoir，最大 `|SMD|` 为 0.09994 / 0.09955；
- 匹配前只使用独立 design model Qwen2.5 的 difficulty，没有读取 confirmatory Qwen3/Gemma target outcomes。

Language-specific control 也已建立：

- Tatoeba 自然语境池：中文 7,943，日文 7,923；
- 当前计算选择：中文 23、日文 24；最大 `|SMD|` 0.09446 / 0.09668；
- 人工冗余池：中文 92、日文 96；最大 `|SMD|` 0.09739 / 0.09675；
- `zh_ja_003` 因 contextual POS 为不受支持的 `OTHER`，没有进入中文匹配目标。

这些数字证明的是**设计阶段平衡**，不是人工语义有效性，也不是 target causal result。

### 5.3 A 的升级条件

只有以下全部完成后才能运行确认性 target-model analysis：

1. 两位真实中日双语者完成 Doppel 全量盲审：708 行/人；
2. 两位双语者完成 true/translation control 盲审：192 行/人；
3. 两位双语者完成 language-specific control 盲审：188 行/人；
4. reliability gate 通过，人工筛选后仍有至少 20 个 false-friend matched sets，且所有 `|SMD| ≤ 0.10`；
5. fail-closed gate 解锁后，才可读取 Qwen3/Gemma confirmatory target outcomes。

若人工有效 controls 后匹配失败，或匹配通过但 false-friend causal excess 消失，则删除 collision-specific mechanism 主张，保留 B 的行为分解。这不是整个题目失败，而是 A 被 kill。

## 6. C：为什么被淘汰

C 检验前一轮出现某个同形词/词义后，下一轮完全相同 target prompt 是否发生定向词义残留。

主协议：ZH–JA 27 项、ID–TL 33 项，四模型，五种 prime control，dose 1/4/8、lag 0/2/8，共 22,080 condition cells。72 个 model×pair×dose×lag 聚合 cell 中：

| 对比 | 方向正确且 CI 不跨 0 | median effect |
|---|---:|---:|
| wrong exact − language unrelated | 56/72 | -2.099 |
| wrong semantic/no-form − language unrelated | 44/72 | -1.325 |
| wrong exact − wrong semantic/no-form | 32/72 | -0.685 |
| wrong exact − surface-only | 20/72 | -0.916 |
| correct exact − language unrelated | 71/72 | +10.726 |

换 speaker role 后，wrong-exact 相对 language-control 只在 6/12 个 model×pair×lag cells 显著。No-form semantic prime 已解释很大一部分效应，exact-form 的额外增量较小且不稳定。

因此 C 的正确结论是：跨轮 semantic state 的确会持续，但当前证据不足以把它归因于 cross-lingual homograph collision。它更接近一般 semantic priming / conversational anchoring，不能承担母题要求的独特 scientific claim，故主线 KILL。

## 7. 先行研究边界与精确 novelty

不能再声称以下内容是创新：[StingrayBench](https://aclanthology.org/2025.findings-naacl.178/) 已比较 false friends/cognates 并研究偏置；[Tanwar et al.](https://arxiv.org/abs/2501.09127) 已做三类词和 incongruent sentences；[RoDEval](https://aclanthology.org/2025.emnlp-main.864/) 已指出 WSD accuracy 不等于完整 sense knowledge；既有 activation-patching 工作也已分离 language 与 concept。因此“false friends 更难”“context 会影响判断”“怪冲突句”“accuracy 不够”和一般性的 language/concept separation 都不能作为创新。

当前安全 positioning 是：

> Existing cross-lingual homograph evaluations often correlate sentence language, intended sense, visible lexical form and final answer decision. We orthogonally manipulate Language × Sense and use target masking, unrelated-context controls and independent natural contexts to identify contextual semantic evidence separately from language-conditioned lexical evidence. We then test whether the gap between available evidence and final choice is specific to exact-form cross-lingual collision beyond matched cognate, language-specific, translation and monolingual-polysemy controls.

精确差异：

- Stingray/Doppelganger 已证明错误、bias、context 和 shortcut；本研究定位错误发生在 evidence extraction 还是后续 arbitration；
- Tanwar 已做 cognate/non-cognate/homograph 和 incongruent sentence；本研究的核心不是“怪句子”，而是完整 `Language × Sense` 正交分解与 target masking/natural convergence；
- RoDEval 已说明 WSD 错误不等于“不知道 sense”；本研究不能泛称 beyond accuracy，而应称 cross-lingual lexical conflict 的 construct decomposition；
- 已有 language/concept patching 与 context-vs-lexical mechanism 工作限制了 A 的广义 novelty；A 必须证明 exact-form collision-specific excess 才能成立。

完整论文矩阵和来源见 `docs/LITERATURE_REVIEW.md`。

## 8. 当前能说与不能说

### 可以说

- B 的行为 pilot 跨四模型、独立自然语境和非 CJK pair 复现；
- 模型在 target 被 mask 后仍能获得正确 contextual evidence；
- 恢复同形表记有时不改善、甚至抵消这份 evidence；
- 绝对答案会受到 decision/calibration 层明显影响；
- A 的现有结果支持一个 general-WSD semantic pathway 加待验证 language-arbitration effect 的假设；
- 五类 control 与 fail-closed confirmatory protocol 已完成计算设计。

### 不能说

- 不能说 bilingual human validation 已完成；
- 不能把词典 overlap 或自动规则叫 gold labels；
- 不能说 collision-specific causal excess 已确认；
- 不能说发现了 neuron、circuit、统一层顺序或隐藏“真实语义表示”；
- 不能把 96 个 protocol variants 当作 96 个独立复现；
- 不能恢复 Semantic Overwrite、Collision-aware Replay 或 C 作为主贡献。

## 9. 当前进度与下一步唯一正确顺序

| 阶段 | 内容 | 状态 | 通过后进入 |
|---|---|---|---|
| Step 1 | 文献边界与Main RQ收束 | **完成** | 不再更换主问题 |
| Step 2 | B：factorial、mask、自然语境、独立数据、非CJK复现 | **完成，强pilot** | collision specificity |
| Step 3 | 五类control候选构建与outcome-blind matching | **计算完成** | 真实双语验证 |
| Step 4 | 708/192/188三套双人盲审及human-filtered rematching | **待完成** | confirmatory A解锁 |
| Step 5 | A：Qwen3/Gemma residual/MLP collision-specific causal excess | **锁定** | 机制结论或kill A |
| Step 6 | Context-preserving mitigation与严格baselines | **尚未开始** | 可能的方法贡献 |
| Step 7 | 层级统计、稳健性、论文写作 | **待后续** | 最终论文 |

1. 完成 708/192/188 行的两人独立双语盲审；
2. 运行一致性与完整性检查；
3. 仅用双人均通过的 candidates 重新做 cardinality matching；
4. 若保留至少 20 个 matched sets 且 `|SMD| ≤ 0.10`，解锁 confirmatory A；
5. 运行 Qwen3/Gemma target residual 与 MLP primary analysis；attention 只作稳定性负对照；
6. A 过门槛才把标题升级为 `Causal Decomposition`；否则诚实删除 A 的 collision-specific claim，围绕 B 完成行为/测量论文。

在 gate 解锁前，不扩模型、不扩更多语言、不做 SAE/neuron、不做 mitigation。当前瓶颈不是 GPU，而是真实双语 measurement validity。

## 10. 依次向导师讲解的七步

不要按“A做了什么、B做了什么、又跑了什么模型”的实验日志顺序讲。每一步只完成一个论证动作。

### 第一步：先界定已经被做掉的问题

讲：Stingray已比较false friends/cognates和语言偏置；Tanwar已做三类词和incongruent sentences；Doppelganger已做日中context/translation与shortcut；RoDEval已说明accuracy不等于sense knowledge。

落点：我们不主张“false friends更难”“context有用”或“accuracy不够”。

### 第二步：给出唯一Main RQ

> 文脈が支持する語義と言語慣習が支持する語義が衝突するとき，多言語LLMの誤りは，文脈語義を抽出できないために生じるのか，それとも正しい語義情報を抽出していても，最終的な語義選択・仲裁で負けるために生じるのか？

说明cross-lingual homograph是固定表记、正交操纵Language×Sense的自然实验床；母问题是多语言模型如何把语义证据映射为词汇选择。

### 第三步：用B展示反直觉现象

只展示一张核心结果表：full 92/96、masked 91/96、language-only 4/96、unrelated 1/96。随后说明96是协议变体，不是独立样本。

落点：target被遮住后，surrounding context中的sense evidence几乎完整保留；单独给language identity或无关语境不能解释它。

### 第四步：用独立自然语境证明不是造句artifact

讲Doppel 354词：4/4模型 `masked−unrelated>0`；恢复homograph没有显著改善，Qwen3/Gemma-4B反而下降。再用ID–MS/ID–TL 48/48说明不是汉字专属。

落点：最重要的finding不是“模型答错”，而是“正确semantic evidence可以存在，却没有控制最终lexical decision”。同时主动说明Doppel option spans仍待双语人工确认。

### 第五步：说明为什么还不能直接归因于homograph collision

展示五类control表，并说明旧controls严格检查后common support为零，所以旧A不能当确认性结论。新outcome-blind matching保留24 false friends、24 true、24 translation，以及中文23/日文24 language-specific controls，所有max `|SMD|<0.10`。

落点：这是设计平衡，不是人工gold；当前瓶颈是708/192/188行的两人双语盲审。

### 第六步：解释A的角色和诚实边界

讲exploratory A发现false friend与monolingual polysemy semantic curve高度一致（0.982/0.999），target residual/MLP有language signal而attention不稳定。

落点：候选解释是general WSD先提供semantic evidence，language convention随后影响arbitration；但collision-specific excess必须等human-filtered rematching后确认。A不是独立题目，也不是已发现circuit。

### 第七步：给出决策树和可能的解决方法

- 人工验证/匹配失败：删除A，只保留B；
- 匹配通过但causal excess消失：如实kill A；
- A通过：升级为causal decomposition；
- 现象与特异性均通过后，才测试context-preserving intervention，要求恢复target后不破坏masked context已有的正确margin，并与普通WSD训练、calibration、language tag和等预算SFT比较。

最后用一句话收束：

> 私が示したいのは、同形異義語が単に難しいということではありません。モデルが文脈から正しい語義情報を取得できているにもかかわらず、共有表記と言語慣習との競合によって、その情報が最終判断に反映されない場合があるのではないか、という点です。

## 11. 数字与证据文件索引

| 内容 | 主要证据文件 |
|---|---|
| Factorial、mask、language-only、unrelated gate | `results/extensions/factorial_gate.csv`, `construct_gate_summary.csv` |
| Natural correct-use gate | `results/extensions/natural_context_summary.csv` |
| 非 CJK natural replication | `results/extensions/second_pair_natural_gate.csv` |
| Doppel natural effects | `results/extensions/doppel_natural_summary.csv` |
| Calibration | `results/extensions/calibration_summary.csv`, `decision_calibration_aggregate.csv` |
| A 旧 causal profiles | `results/extensions/causal_gating_summary.csv`, `causal_profile_comparison.csv` |
| Target-span component pilot | `results/extensions/target_patch_summary.csv`, `target_patch_profiles.csv`, `target_patch_language_excess.csv` |
| Prematched controls balance | `results/extensions/prematched_final_balance.csv`, `control_reservoir_balance.csv` |
| Language-specific balance | `results/extensions/language_specific_final_balance.csv`, `language_specific_validation_reservoir_balance.csv` |
| C carryover | `results/extensions/carryover_summary.csv`, `carryover_role_robustness.csv` |
| 当前总 gate 状态 | `results/extensions/final_measurement_gate_status.json` |

复现实验命令见 `EXPERIMENTS.md`；人工门槛和 fail-closed 执行命令见 `HUMAN_VALIDATION_AND_GATES_ZH.md`；研究定位见 `LITERATURE_REVIEW.md`。
