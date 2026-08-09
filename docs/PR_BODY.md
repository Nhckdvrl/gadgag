## Summary

- records a complete kill-or-go pilot for cross-lingual semantic overwrite
- falsifies the original claim with neutral-surface and context-lift controls
- reports the replicated paired sense-switch finding across two language pairs
  and four Qwen/Gemma checkpoints
- proposes a broader causal decomposition of cross-lingual lexical interference
- includes code, aggregate evidence, figures, literature audit, limitations and
  explicit future kill criteria

## Validation

- `python -m py_compile src/*.py`
- `python src/validate_artifact.py`
- `python src/make_figures.py`
- `git diff --cached --check`

## Data policy

Raw source dataset text, model adapters and checkpoints are not redistributed.
The repository contains deterministic preparation code and aggregate outputs;
external datasets and checkpoints retain their own licenses.
