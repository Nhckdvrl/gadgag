# 与选题要求的逐项对照

| 严格要求 | 当前判断 | 证据或风险控制 |
|---|---|---|
| 母题仍是 cross-lingual homograph | 满足 | false friends 是固定表面、改变语言词义的主自然实验床 |
| 不能只是 benchmark / 模型比较 | 满足但需守住 | 主贡献是 construct 分解与训练干预；模型比较只检验外部效度 |
| 有明确新 idea | 满足 | Crossed-Context Audit：语言×词义语境 2×2，加 decision-resolution 层；不再把 midpoint 当 prior |
| 问题不能过窄 | 基本满足 | 题目提升到 cross-lingual lexical interference/evaluation，能覆盖 WSD、MT、code-switching；homograph 提供可识别干预 |
| 不能挤进已拥挤方向 | 有条件满足 | 已排除静态日中 benchmark、多语言扩展、safe embedding、tokenizer separation；但 calibration/WSD 是强邻接工作，必须明确区别 |
| 数据真实、可扩展 | 满足 | pilot 复用 Doppelganger-JC 与 StingrayBench；完整研究可扩到 Stingray 705 条、SemCog 1,858 对及其他人工资源 |
| 不是 GPT 批量造测试集 | 满足 | 核心标签来自公开人工数据；受控模板只用于 causal intervention，不当 gold benchmark |
| 1–2 周能 kill/go | 满足 | 当前 pilot 已产生严格 KILL、替代 GO 和后续 kill criteria |
| 半年能完成 | 满足 | 以 likelihood scoring 和小型 LoRA 为主，文档给出 6 个月 work packages |
| 模型升级后仍有意义 | 较强 | 测量构念与适配干扰是架构无关问题；但未来模型可能消除经验 gap，这本身可被指标检测 |
| 日中以外也成立 | 满足 pilot | strict exact-context ZH–JA 为 47/48、ID–TL 为 45/48；两对 official-chat 合计 48/48 |
| 有论文分量 | 有条件 | 必须完成 4 pair × 6 model、人类验证、扰动稳健性和现有 benchmark 结论重审；只发表当前 106 个 paired items 不够 |
| 对负结果诚实 | 满足 | semantic overwrite 与 collision replay 均明确 KILL，所有反证保留在仓库 |

## 当前最大审稿风险

1. Stingray conflict context 是替词构造的强、奇异语境，可能高估自然语境证据。
2. English gloss 候选存在翻译不对称，item-level 方向对措辞仍不稳定。
3. XCA 与成熟 factorial evaluation / signal-detection work 的 citation chasing 还需继续。
4. 动态 conflict-minus-neutral 的 CI 略跨零，不能当主结论。

纯 language-ID 解释已通过 2×2、masked、language-only 和 marker-matched shuffled controls 初步排除，但输出协议 confound 尚未解决：4 个 full gate 失败集中在 Gemma-3-12B plain。自然对角线的 masked−shuffled 为 82/96，但 full−language-only 只有 36/96，说明显式语言线索可压过长语境。下一硬门槛是新的自然/人工配对语境、独立双语人工释义验证与预先固定的 decision protocol；若不能复现，就按照 kill criteria 放弃。
