# 2026/08/19 ミーティング発表案

## 1. 今回修正した点

前回は「誤答が二種類の failure を混ぜている」という measurement 上の観察までしか説明できなかった。今回は研究目的を一段上げる。

> **同形異義語が難しいことを示すのではなく，文脈意味と言語慣習が競合するとき，誤りが文脈情報の抽出段階で生じるのか，抽出後の語義選択・仲裁段階で生じるのかを特定する。**

作業題目：

> **When Context and Language Disagree: Disentangling Cross-Lingual Lexical Arbitration in Multilingual LLMs**

日本語：

> **文脈と言語慣習が衝突するとき：多言語 LLM における語彙的仲裁の分解**

## 2. Main RQ

> 文脈が支持する語義と言語慣習が支持する語義が衝突するとき，多言語 LLM の誤りは，文脈語義を抽出できないために生じるのか，それとも正しい語義情報を抽出していても，最終的な語義選択において言語依存の語義バイアスに負けるために生じるのか？

### RQ1 — Evidence extraction

文の言語を固定し，local semantic context だけを変えたとき，モデルは正しい sense evidence を抽出するか。

### RQ2 — Collision specificity

正しい evidence が最終判断に反映されない現象は false friend に特有か。それとも cognate，language-specific word，different-form translation，ordinary polysemy，frequency/segmentation/difficulty で説明できるか。

### RQ3 — Arbitration mechanism

semantic evidence と language-conditioned lexical convention は，target representation のどの段階・成分を通して lexical choice に因果的に影響するか。

## 3. 先行研究との境界

| 研究 | 既に行ったこと | 本研究では claim しないこと | 残る gap |
|---|---|---|---|
| StingrayBench | FF/true cognate，4 言語対，bias/comprehension | FF が難しい，high-resource bias | Language と local Sense を直交分離していない |
| Tanwar et al. | cognate/non-cognate/homograph，文脈，incongruent sentences | 「矛盾文」を作ること | 完全な Language×Sense estimand と stage localization がない |
| Doppelganger-JC | JC 三課題，shortcut，POS | JC benchmark/error analysis | context evidence が誤答内部に既に存在するか未同定 |
| RoDEval | WSD error は knowledge/bias/confidence を混ぜる | accuracy だけでは不十分 | cross-lingual exact-form conflict の因子分解ではない |
| Dumas et al. | language/concept activation patching | language と semantics の初分離 | 競合時に同一 lexical choice をどう決めるか |
| Oh et al. | idiom の context-vs-lexical causal tracing | context/lexical competition の初研究 | cross-lingual exact-form collision ではない |

安全な novelty 表現：

> Existing homograph evaluations correlate sentence language, intended sense, surface form and answer decision. We orthogonally manipulate Language × Sense to localize whether cross-lingual lexical failure arises during semantic-evidence extraction or later lexical arbitration, and test collision specificity with outcome-blind matched controls.

「世界初」ではなく，**2026/08/12 までの調査でこの組合せの直接研究を確認できなかった**と表現する。

## 4. 現在の反直観的 pilot evidence

`Language × Sense` 2×2 で，同じ文言語のまま sense context だけを変える。

| 条件 | semantic effect の CI が正 |
|---|---:|
| Full context | 92/96 |
| Target masked | 91/96 |
| Language only | 4/96 正，2/96 負 |
| Marker-matched unrelated context | 1/96 正，3/96 負 |

- official chat subset は full 48/48；
- natural correct-use cells の masked−unrelated は 82/96（chat 46/48）；
- ID–MS / ID–TL の非 CJK replication は masked natural−unrelated が 48/48；
- 独立 Doppelganger-JC 自然文では target mask 後も 4/4 models が正しい contextual direction を持つ；homograph を戻すと 3/4 models で改善しないか悪化する。

したがって最も重要な finding candidate は：

> **Correct semantic evidence can be present without yielding the correct lexical decision.**

これは「context が役立つ」より強く，「誤答＝context を理解していない」という benchmark interpretation を反証する。

## 5. 五つの identification controls

| Type | Form | 意味関係 | 識別するもの |
|---|---|---|---|
| False friend | same exact | different | 目的現象 |
| True friend/cognate | same exact | same | shared form 自体 |
| Language-specific | 他言語辞書に exact form なし | — | 通常の言語選択的 lexical processing |
| Different-form translation | different | same | cross-language semantics without form collision |
| Monolingual polysemy | same within one language | different senses | ordinary WSD |

最初の三つは先生が求めた minimum baseline であり，先行人間研究にも存在する。後二つが shared form と ambiguity をさらに分ける。これらは contribution ではなく identification controls である。

## 6. Matching の進捗

旧 Stingray controls は exact bilingual POS + 全協変量 1 SD で 0 pairs だったため，その結果は因果証拠として使用しない。

新しい設計では target outcome を見ずに JMdict / CC-CEDICT / Tatoeba から controls を反向構築した。

- bilingual-context candidate pool：11,000；
- joint cardinality matching：24/27 false friends；
- true-friend 24，different-form translation 24；
- frequency，ratio，character/gloss length，Qwen3/Gemma tokenization，独立 Qwen2.5 difficulty，contextual POS を固定；
- max `|SMD|`：0.0872 / 0.0972；
- human rejection に備えて各 group 96 件の 4× reservoir も `|SMD| < .10` で凍結。

language-specific controls は，中国語・日本語それぞれ「相手言語辞書に NFKC exact form がない」候補を自然文から抽出し，同じ design-only matching を追加した。辞書の非掲載は絶対的な言語不存在を証明しないため，このラベルも bilingual human validation を必須とする。

## 7. Mechanism の位置づけ

behavioral decomposition B が論文の骨格であり，causal gating A は paradox の説明である。

現在の pilot：

- false friend と English monolingual polysemy の semantic layer profile は高相関；
- target residual の semantic effect は Qwen/Gemma で再現；
- language-related effect は早中層から連続して出現；
- MLP output は主要 language signal と一部 semantic signal を再現；
- attention-only は不安定。

安全な解釈：general WSD-like semantic processing と language-conditioned lexical evidence が target representation を通して final choice に寄与する可能性。

禁止する解釈：専用 homograph circuit，特定 neuron，language/semantics の初分離，人間脳との同一性。

## 8. 次の hard gates

1. Doppel 354×2 を二名の中日 bilingual が blind validation。
2. true/different-form controls 192 件/人を blind validation。
3. language-specific controls 188 件/人（JA 96 / ZH 92）を blind validation。
4. human-valid set のみで再 matching。false friends 20 件以上かつ全 `|SMD|≤.10`。
5. ここまで通った場合のみ Qwen3/Gemma confirmatory target intervention を解錠。

Kill policy：

- contextual evidence が自然・人工検証後に消える → 主 behavioral claim を停止；
- matched controls 後に FF excess が消える → collision-specific mechanism を削除，B は維持；
- language-specific を含む全 controls が同じ effect → homograph-specific claim を削除；
- target result を見て matching/除外基準を変更しない。

## 9. 先生に確認したい点

1. 「context extraction failure と lexical arbitration failure の位置特定」を主 scientific question としてよいか。
2. behavioral B を主 contribution，matched causal A を条件付き第二 contribution とする構成でよいか。
3. language-specific control を causal language-effect と同じ estimand に無理に入れず，ordinary one-language context extraction/decision baseline として扱う設計でよいか。
4. 二名の中日 bilingual annotator の確保方法。

## 口頭で最初に言う一段落

私が最終的に示したいのは，同形異義語が単に難しいということではありません。モデルが文脈から正しい語義情報を取得できているにもかかわらず，共有表記や言語側の語義慣習との競合によって最終判断を誤る場合があるのではないか，という点です。そこで，文脈意味の抽出失敗と，その後の語義選択・仲裁の失敗を分け，さらに cognate，language-specific word，different-form translation，ordinary polysemy と比較して，この現象が cross-lingual exact-form collision に特有かを調べます。
