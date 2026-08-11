# Decision log

| Stage | Evidence | Decision |
|---|---|---|
| Static literature audit | 2025–2026 work already covers static JC benchmarks, multilingual false friends, overlap sharing, safe embeddings and tokenizer separation | Remove bridge/safe-anchor/static-benchmark formulations |
| Coarse overwrite pilot | Significant raw dose-32 effect, but dose 128 not stronger | Strict preregistered-style rule says KILL; investigate measurement before abandoning mother topic |
| Fine dose and second model | Early monotonic curve then saturation; Qwen3 replication | Effect is real at the score level, mechanism still unknown |
| Japanese-gloss outcome | Non-significant | Evidence against semantic-representation overwrite |
| Module ablation | MLP/late layers carry raw effect | Consistent with output interface, not proof of semantics |
| Replay | Targeted replay fails to beat random | Reject proposed mitigation |
| Neutral surface exposure | Larger effect without conflicting meaning | Falsifies semantic-conflict explanation |
| Context-lift correction | Raw ZH–JA and EN–DE effects disappear | Definitively KILL semantic overwrite as measured |
| Paired bilingual factorization | Large gap between both-correct and positive switch across two pairs and four checkpoints | Conditional GO on construct-validity direction |
| External construct review | Diagonal switch changes language, semantics and sometimes target form; midpoint is not a prior | Retract causal terminology; run crossed-context gate before scaling |
| Exact-context 2×2 audit | After requiring the target in all four cells (27 ZH–JA, 33 ID–TL), full SCE 92/96 CI>0; masked 91/96; language-only 4 positive/2 negative | Pure language-ID explanation rejected; measurement topic conditionally GO |
| Matched-marker rerun | Replaced shuffled `[OTHER]` with `[TARGET]`; reran 16 factorial files; shuffled 1 positive/3 negative, natural masked−shuffled 82/96 | Marker cue does not explain the effect |
| Natural-context audit | Natural full−shuffled 94/96; masked−shuffled 82/96; full−language-only only 36/96 with 16 reversals | Natural evidence exists, but explicit language cue can dominate; reject one-factor “context wins” story |
| Boundary/chat/score robustness | Full-string scoring and mean/sum preserve the broad aggregate; chat 48/48, plain 44/48 | Tokenizer concern fixed, but Gemma-3-12B plain failures establish protocol sensitivity |
| Batch-size 8/32 stress | Margin Pearson >.999, 0.6–1.2% cell sign flips; one Gemma plain aggregate CI flips, Qwen chat gates stable | Fix numeric protocol and flag near-boundary decisions; do not count specifications as independent replications |
| Lexical gloss variants | Aggregate 48/48 CI>0, but item consistency 22.2–81.5% | Keep aggregate claim; require bilingual repeated-gloss validation |
| Content-free calibration | Both-direction accuracy improves about 14pt on average | Decision layer materially matters; calibration remains baseline, not novelty |

The iteration stopped changing the hypothesis only when a surviving claim had
both positive evidence and explicit falsification controls. Negative results
remain first-class results rather than being removed from the story.
