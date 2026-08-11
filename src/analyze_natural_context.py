#!/usr/bin/env python3
"""Audit correct-sense evidence using only Stingray's natural diagonal cells.

The crossed cells are useful counterfactual interventions but were produced by
translation and false-friend replacement.  This analysis avoids treating those
cells as ecological evidence: it uses only L1×sense1 and L2×sense2, and compares
each natural context with its same-item language-only or deterministic shuffled
control.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RNG = np.random.default_rng(20260811)


def bootstrap_ci(values: np.ndarray) -> tuple[float, float]:
    indices = RNG.integers(0, len(values), size=(5000, len(values)))
    means = values[indices].mean(axis=1)
    return float(np.quantile(means, 0.025)), float(np.quantile(means, 0.975))


def main() -> None:
    rows = []
    for path in (ROOT / "results/extensions").glob("factorial_*.jsonl"):
        rows.extend(json.loads(line) for line in path.read_text().splitlines())
    data = pd.DataFrame(rows)
    assert len(data), "no factorial item outputs"

    output = []
    keys = ["pair", "model", "prompt_mode", "wrapper"]
    for key, group in data.groupby(keys):
        for normalization in ("mean", "sum"):
            metric = f"margin_{normalization}"
            pivot = group.pivot(
                index="id", columns=["condition", "language", "sense"], values=metric
            )
            # Margin is log P(sense2) - log P(sense1).  Reverse its sign for the
            # natural L1×sense1 cell so positive always means correct-sense evidence.
            comparisons = {
                "full_minus_language_only": (
                    (pivot["language_only", 1, 1] - pivot["full", 1, 1])
                    + (pivot["full", 2, 2] - pivot["language_only", 2, 2])
                ) / 2,
                "full_minus_shuffled": (
                    (pivot["shuffled", 1, 1] - pivot["full", 1, 1])
                    + (pivot["full", 2, 2] - pivot["shuffled", 2, 2])
                ) / 2,
                "masked_minus_shuffled": (
                    (pivot["shuffled", 1, 1] - pivot["masked", 1, 1])
                    + (pivot["masked", 2, 2] - pivot["shuffled", 2, 2])
                ) / 2,
            }
            for comparison, series in comparisons.items():
                values = series.to_numpy()
                low, high = bootstrap_ci(values)
                output.append(dict(zip(keys, key)) | {
                    "normalization": normalization,
                    "comparison": comparison,
                    "n": len(values),
                    "estimate": values.mean(),
                    "ci_low": low,
                    "ci_high": high,
                    "positive_rate": (values > 0).mean(),
                })

    result = pd.DataFrame(output)
    result.to_csv(ROOT / "results/extensions/natural_context_summary.csv", index=False)
    report = "# Natural-context diagonal audit\n\n"
    report += result.to_markdown(index=False) + "\n"
    (ROOT / "reports/natural_context_audit.md").write_text(report)
    gate = result.groupby("comparison").agg(
        variants=("estimate", "size"),
        ci_positive=("ci_low", lambda x: int((x > 0).sum())),
        median_effect=("estimate", "median"),
    )
    print(gate.to_string())


if __name__ == "__main__":
    main()
