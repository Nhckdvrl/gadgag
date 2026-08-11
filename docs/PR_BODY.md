## Summary

- keeps the original semantic-overwrite hypothesis formally killed
- retracts the unsupported interpretation of the old midpoint as a candidate
  prior and treats the diagonal switch as a mixed score-level phenomenon
- adds a boundary-faithful scorer and validated Stingray pair loader
- uses exact-form 2×2 language × sense contexts to separate semantic-context
  and language-convention evidence
- adds target-masked, language-only, shuffled-context, mean/sum, chat/plain,
  lexical-gloss, content-free calibration and XL-WiC controls
- revises the proposed topic to an audit of cross-lingual sense evaluation
  beyond final-answer accuracy

## New result

- strict sample: 27 ZH–JA and 33 ID–TL targets occurring in all four cells
- full semantic-context effect: 92/96 variants with 95% CI above zero
- official chat-template subset: 48/48; plain-text stress test: 44/48
- target-masked context: 91/96
- language-only: 4/96 positive and 2/96 negative
- marker-matched shuffled context: 1/96 positive and 3/96 negative
- natural masked context minus matched shuffled: 82/96 (chat 46/48)
- natural full context minus explicit language+target cue: only 36/96
- lexical gloss variants: 48/48 aggregate CIs above zero
- content-free calibration raises average both-direction accuracy by about 14pt

## Validation

- `.venv/bin/python -m py_compile src/*.py`
- `.venv/bin/python src/validate_artifact.py`
- `.venv/bin/python src/validate_construct.py`
- `.venv/bin/python src/make_figures.py`
- `git diff --check`

## Data policy

Raw source text, checkpoints, adapters and per-item model outputs are not
redistributed. External datasets retain their own licenses. The included
English gloss variants are marked as needing independent bilingual validation
before confirmatory use.
