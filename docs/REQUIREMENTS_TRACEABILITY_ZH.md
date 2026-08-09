# 与选题要求的逐项对照

| 严格要求 | 当前判断 | 证据或风险控制 |
|---|---|---|
| 母题仍是 cross-lingual homograph | 满足 | false friends 是固定表面、改变语言词义的主自然实验床 |
| 不能只是 benchmark / 模型比较 | 满足但需守住 | 主贡献是 construct 分解与训练干预；模型比较只检验外部效度 |
| 有明确新 idea | 满足 | paired sense switch + candidate prior 双轴，并用 conflict/neutral adaptation 验证构念 |
| 问题不能过窄 | 基本满足 | 题目提升到 cross-lingual lexical interference/evaluation，能覆盖 WSD、MT、code-switching；homograph 提供可识别干预 |
| 不能挤进已拥挤方向 | 有条件满足 | 已排除静态日中 benchmark、多语言扩展、safe embedding、tokenizer separation；但 calibration/WSD 是强邻接工作，必须明确区别 |
| 数据真实、可扩展 | 满足 | pilot 复用 Doppelganger-JC 与 StingrayBench；完整研究可扩到 Stingray 705 条、SemCog 1,858 对及其他人工资源 |
| 不是 GPT 批量造测试集 | 满足 | 核心标签来自公开人工数据；受控模板只用于 causal intervention，不当 gold benchmark |
| 1–2 周能 kill/go | 满足 | 当前 pilot 已产生严格 KILL、替代 GO 和后续 kill criteria |
| 半年能完成 | 满足 | 以 likelihood scoring 和小型 LoRA 为主，文档给出 6 个月 work packages |
| 模型升级后仍有意义 | 较强 | 测量构念与适配干扰是架构无关问题；但未来模型可能消除经验 gap，这本身可被指标检测 |
| 日中以外也成立 | 初步满足 | EN–DE 在原假阳性去先验和新 sense-switch 现象上均复现 |
| 有论文分量 | 有条件 | 必须完成 4 pair × 6 model、人类验证、扰动稳健性和现有 benchmark 结论重审；只发表当前 106 个 paired items 不够 |
| 对负结果诚实 | 满足 | semantic overwrite 与 collision replay 均明确 KILL，所有反证保留在仓库 |

## 当前最大审稿风险

1. `sense_switch` 被认为只是 contextual calibration 的简单变体。
2. 对固定 false friend，语言识别本身可能足以确定词义，未必需要局部句子理解。
3. English gloss 候选可能引入翻译不对称。
4. 目前动态 conflict-minus-neutral 的 CI 略跨零，不能当主结论。

因此论文必须把贡献写成“跨语言词汇构念的成对因果审计”，并增加同语言乱序、局部语境最小对、候选释义多重改写及人类验证。若这些控制不能区分语言 ID 与真正的词义语境利用，就按照 kill criteria 放弃。
