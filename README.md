# Right Direction, Wrong Answer

This repository is the complete record of a kill-or-go pilot on cross-lingual
homographs. The proposed **cross-lingual semantic overwrite** hypothesis did
not survive causal controls. The experiments instead reveal a broader and
actionable problem: current absolute-answer homograph evaluations conflate
context-conditioned sense discrimination with surface/candidate priors.

The resulting research direction is:

> **Causally Decomposing Cross-Lingual Lexical Interference into
> Language-Conditioned Sense Sensitivity and Surface Priors**

It is not another static model leaderboard. It is a construct-validity and
causal-evaluation project: paired bilingual counterfactuals factor a model's
score into (i) a context-sensitive *sense switch* and (ii) a context-independent
candidate prior, while controlled adaptation interventions test which component
actually changes.

## Pilot verdict

- **KILL** the literal semantic-overwrite claim. Chinese-only adaptation caused
  a targeted raw margin change at dose 32, but a neutral repetition control was
  even larger, Japanese-gloss evaluation was non-significant, and a
  context-lift correction removed the apparent cross-lingual effect.
- **KILL** collision-aware replay as currently formulated. It did not beat an
  equal-budget random replay baseline.
- **GO** on the paired sense-switch audit. Across Chinese–Japanese and
  English–German, Qwen2.5-7B, Qwen3-8B, Gemma-3-4B and Gemma-3-12B often failed
  the strict two-sided answer criterion while still shifting toward the correct
  sense when the language context changed.

See [the Chinese executive report](docs/EXECUTIVE_SUMMARY_ZH.md),
[experiment record](docs/EXPERIMENTS.md), [literature audit](docs/LITERATURE_REVIEW.md),
and [research proposal](docs/RESEARCH_PROPOSAL.md).

## Core metric

For identical candidate senses \(y_1,y_2\) and paired contexts in languages
\(L_1,L_2\):

```text
m1 = log P(y2 | x_L1) - log P(y1 | x_L1)
m2 = log P(y2 | x_L2) - log P(y1 | x_L2)

sense_switch = m2 - m1
candidate_prior = (m2 + m1) / 2
```

`sense_switch > 0` asks whether context moves the model in the correct
direction. It does **not** replace absolute correctness; reporting both exposes
whether a failure comes from semantic insensitivity or a stable output prior.

## Reproduction

The pilot used Python 3.12, PyTorch 2.8, Transformers 4.57, PEFT 0.19 and A100
GPUs. Install the dependencies in `requirements.txt`, then obtain the source
datasets (their licenses apply):

```bash
git clone https://github.com/0017-alt/Doppelganger-JC external/Doppelganger-JC
git clone https://huggingface.co/datasets/StingrayBench/StingrayBench external/StingrayBench
python src/prepare_data.py
```

Primary crossover experiment:

```bash
CUDA_VISIBLE_DEVICES=0 python src/run_pilot.py --fold 0
CUDA_VISIBLE_DEVICES=1 python src/run_pilot.py --fold 1
python src/analyze.py
```

The scripts in `src/` reproduce every extension and construct-validity check.
The public repository intentionally contains aggregate results rather than
redistributing source dataset text or multi-gigabyte adapters.

## Repository map

- `src/`: data preparation, interventions, evaluations, and analyses
- `results/`: aggregate CSV files used in the reports
- `reports/`: machine-generated pilot tables and decisions
- `docs/`: interpretation, literature audit, limitations, and proposed study
- `figures/`: figures generated from aggregate results

## Scope and honesty

This is a rigorous pilot, not a completed conference paper. The causal
adaptation study uses 50 Japanese–Chinese false friends and two crossover folds;
the paired audit uses 57 Chinese–Japanese and 49 English–German items. The
finding is replicated across four open model checkpoints, but the full paper
still needs preregistered scaling, human validation, more language pairs, and
closed-model probability-compatible evaluation.
