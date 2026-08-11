#!/usr/bin/env python3
"""Paired item bootstrap for non-CJK natural context/form decomposition."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RNG = np.random.default_rng(20260813)


def ci(values):
    values = np.asarray(values)
    draws = values[RNG.integers(0, len(values), (5000, len(values)))].mean(1)
    return np.quantile(draws, [.025, .975])


def main():
    records = []
    for path in (ROOT / "results/extensions").glob("natural2_*.jsonl"):
        records.extend(json.loads(line) for line in path.read_text().splitlines())
    data = pd.DataFrame(records)
    assert len(data), "no second-pair natural outputs"
    rows = []
    contrasts = {
        "full_minus_unrelated": ("full", "language_unrelated"),
        "masked_minus_unrelated": ("masked", "language_unrelated"),
        "full_minus_masked": ("full", "masked"),
        "full_minus_surface": ("full", "surface_only"),
    }
    for key, group in data.groupby(["pair", "model", "wrapper"]):
        for norm in ("mean", "sum"):
            # Both directions are repeated measures, not independent samples.
            averaged = group.groupby(["id", "condition"])[f"correct_margin_{norm}"].mean()
            pivot = averaged.unstack("condition")
            for name, (left, right) in contrasts.items():
                values = (pivot[left] - pivot[right]).to_numpy()
                low, high = ci(values)
                rows.append(dict(zip(["pair", "model", "wrapper"], key)) | {
                    "normalization": norm, "contrast": name, "n_items": len(values),
                    "estimate": values.mean(), "ci_low": low, "ci_high": high,
                    "positive_rate": (values > 0).mean()})
    summary = pd.DataFrame(rows)
    summary.to_csv(ROOT / "results/extensions/second_pair_natural_summary.csv", index=False)
    gate = summary.groupby(["pair", "model", "contrast"]).agg(
        variants=("estimate", "size"), positive_ci=("ci_low", lambda x: int((x > 0).sum())),
        negative_ci=("ci_high", lambda x: int((x < 0).sum())),
        median=("estimate", "median")).reset_index()
    gate.to_csv(ROOT / "results/extensions/second_pair_natural_gate.csv", index=False)
    (ROOT / "reports/second_pair_natural.md").write_text(
        "# Non-CJK natural context/form replication\n\n" + summary.to_markdown(index=False) +
        "\n\n## Gate summary\n\n" + gate.to_markdown(index=False) + "\n")
    print(gate.to_string(index=False))


if __name__ == "__main__":
    main()
