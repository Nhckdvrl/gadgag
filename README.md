# When Context and Language Disagree

This repository studies cross-lingual lexical arbitration in multilingual LLMs.
The project no longer asks whether false friends are merely difficult. It asks:

> **When contextual semantics and language convention support competing senses
> of the same lexical form, does failure occur during semantic-evidence
> extraction or during the later arbitration that maps evidence to a lexical
> choice?**

## Current status

| Component | Role | Status |
|---|---|---|
| B / crossed-context behavior | establish and measure the evidence–decision dissociation | **GO** |
| Five matched word types | test whether the dissociation is collision-specific | computational design passed; human validity pending |
| A / causal gating | explain the arbitration mechanism | exploratory evidence only; confirmatory analysis locked |
| C / cross-turn carryover | former standalone candidate | **KILLED** |
| Context-Preserving Lexical Arbitration | preserve contextual evidence during lexical choice | future, only after the phenomenon and mechanism gates |

The repository's machine-readable state is
[`results/extensions/final_measurement_gate_status.json`](results/extensions/final_measurement_gate_status.json).
Real bilingual annotation is not complete, so collision-specific confirmatory
analysis remains fail-closed.

## Documentation

There are five maintained documents, each with one role:

1. [`docs/RESEARCH_STATUS_AND_EVIDENCE_ZH.md`](docs/RESEARCH_STATUS_AND_EVIDENCE_ZH.md) — **canonical research narrative, current results, A/B/C mapping, advisor walkthrough, and claim boundaries**.
2. [`docs/EXPERIMENTS.md`](docs/EXPERIMENTS.md) — chronological commands, implementation details, and experiment record.
3. [`docs/LITERATURE_REVIEW.md`](docs/LITERATURE_REVIEW.md) — prior-work positioning and unavailable novelty claims.
4. [`docs/HUMAN_VALIDATION_AND_GATES_ZH.md`](docs/HUMAN_VALIDATION_AND_GATES_ZH.md) — all bilingual annotation protocols, thresholds, rematching, and fail-closed execution.
5. [`docs/RESEARCH_PROPOSAL.md`](docs/RESEARCH_PROPOSAL.md) — compact English proposal and six-month plan.

Historical briefs and duplicated audit summaries were removed from the active
tree; their history remains available in Git.

## Core pilot result

Across four Qwen/Gemma checkpoints, target-masked context retains the semantic
effect in 91/96 protocol variants. On 354 independently authored bidirectional
Doppelganger-JC items, masked natural context beats matched unrelated context
for 4/4 models, while restoring the homograph yields no significant improvement
and sometimes reduces the correct-sense margin. Non-CJK Indonesian–Malay and
Indonesian–Tagalog natural-context replication passes 48/48 protocol variants.

These are protocol variants, not independent experimental repetitions. The
Doppel option spans and matched lexical controls still require two real
bilingual reviewers before strong confirmatory claims.

## Reproduction

The pilot used Python 3.12, PyTorch 2.8, Transformers 4.57, PEFT 0.19, and A100
GPUs. Create the environment and obtain datasets under their own licenses:

```bash
uv venv .venv --python 3.12
uv pip install --python .venv/bin/python -r requirements.txt
git clone https://github.com/0017-alt/Doppelganger-JC external/Doppelganger-JC
git clone https://huggingface.co/datasets/StingrayBench/StingrayBench external/StingrayBench
.venv/bin/python src/prepare_data.py
```

See `docs/EXPERIMENTS.md` for executable experiments. Raw licensed text, model
weights, adapters, private annotation packets, and per-item outputs are not
redistributed. Deterministic code, aggregate results, manifests, and figures are
included.
