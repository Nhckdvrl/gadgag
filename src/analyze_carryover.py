#!/usr/bin/env python3
"""Paired item-bootstrap analysis for cross-turn semantic carryover."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RNG = np.random.default_rng(20260812)
COMPARISONS = {
    "wrong_exact_minus_language": ("wrong_exact", "language_unrelated"),
    "wrong_exact_minus_surface": ("wrong_exact", "surface_only"),
    "wrong_exact_minus_masked": ("wrong_exact", "wrong_masked"),
    "wrong_masked_minus_language": ("wrong_masked", "language_unrelated"),
    "correct_exact_minus_language": ("correct_exact", "language_unrelated"),
}


def ci(values: np.ndarray) -> tuple[float, float]:
    indices = RNG.integers(0, len(values), size=(5000, len(values)))
    means = values[indices].mean(axis=1)
    return float(np.quantile(means, .025)), float(np.quantile(means, .975))


def main() -> None:
    rows = []
    for path in (ROOT / "results/extensions").glob("carryover_*.jsonl"):
        if path.name.startswith("carryover_alt_"):
            continue
        rows.extend(json.loads(line) for line in path.read_text().splitlines())
    data = pd.DataFrame(rows)
    assert len(data), "no carryover outputs"
    data = data[data.condition != "no_history"]
    output = []
    keys = ["pair", "model", "dose", "lag"]
    for key, group in data.groupby(keys):
        for normalization in ("mean", "sum"):
            pivot = group.pivot(
                index=["id", "target_language"], columns="condition",
                values=f"correct_margin_{normalization}",
            )
            assert set(COMPARISONS.values()) <= {
                (left, right) for left in pivot.columns for right in pivot.columns
            }
            for comparison, (left, right) in COMPARISONS.items():
                # Average the two target directions before bootstrapping items.
                values = (pivot[left] - pivot[right]).groupby(level="id").mean().to_numpy()
                low, high = ci(values)
                output.append(dict(zip(keys, key)) | {
                    "normalization": normalization, "comparison": comparison,
                    "n_items": len(values), "estimate": values.mean(),
                    "ci_low": low, "ci_high": high,
                    "negative_rate": (values < 0).mean(),
                })
    summary = pd.DataFrame(output)
    summary.to_csv(ROOT / "results/extensions/carryover_summary.csv", index=False)

    # Preregistered-style direction gates, summarized without treating the
    # protocol cells as independent replications.
    gate_rows = []
    for comparison, group in summary.groupby("comparison"):
        expected = "positive" if comparison == "correct_exact_minus_language" else "negative"
        gate_rows.append({
            "comparison": comparison, "expected": expected, "protocol_cells": len(group),
            "ci_in_expected_direction": int((group.ci_low > 0).sum() if expected == "positive"
                                            else (group.ci_high < 0).sum()),
            "ci_opposite_direction": int((group.ci_high < 0).sum() if expected == "positive"
                                         else (group.ci_low > 0).sum()),
            "median_estimate": group.estimate.median(),
        })
    gates = pd.DataFrame(gate_rows)
    gates.to_csv(ROOT / "results/extensions/carryover_gates.csv", index=False)
    report = "# Cross-turn semantic carryover\n\n## Paired contrasts\n\n"
    report += summary.to_markdown(index=False)
    report += "\n\n## Direction gates\n\n" + gates.to_markdown(index=False) + "\n"
    (ROOT / "reports/carryover.md").write_text(report)
    print(gates.to_string(index=False))


if __name__ == "__main__":
    main()
