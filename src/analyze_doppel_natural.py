#!/usr/bin/env python3
"""Paired bootstrap analysis for independent Doppelganger-JC validation."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RNG = np.random.default_rng(20260812)


def interval(values: np.ndarray) -> tuple[float, float]:
    draws = RNG.integers(0, len(values), (5000, len(values)))
    means = values[draws].mean(axis=1)
    return float(np.quantile(means, .025)), float(np.quantile(means, .975))


def main() -> None:
    records = []
    for path in (ROOT / "results/extensions").glob("doppel_natural_*.jsonl"):
        records.extend(json.loads(line) for line in path.read_text().splitlines())
    data = pd.DataFrame(records)
    assert len(data), "no Doppelganger validation outputs"
    # Average answer-order permutations, then both directions, before item bootstrap.
    order_avg = data.groupby(["id", "direction", "condition", "model"], as_index=False)[
        ["margin_mean", "margin_sum"]].mean()
    item_avg = order_avg.groupby(["id", "condition", "model"], as_index=False)[
        ["margin_mean", "margin_sum"]].mean()
    contrasts = {
        "full_minus_unrelated": ("full", "language_unrelated"),
        "masked_minus_unrelated": ("masked", "language_unrelated"),
        "full_minus_surface": ("full", "surface_only"),
        "full_minus_masked": ("full", "masked"),
    }
    rows = []
    for model, group in item_avg.groupby("model"):
        for norm in ("mean", "sum"):
            pivot = group.pivot(index="id", columns="condition", values=f"margin_{norm}")
            for name, (left, right) in contrasts.items():
                values = (pivot[left] - pivot[right]).dropna().to_numpy()
                low, high = interval(values)
                rows.append({"model": model, "normalization": norm,
                             "contrast": name, "n_items": len(values),
                             "estimate": values.mean(), "ci_low": low, "ci_high": high,
                             "positive_rate": (values > 0).mean()})
            for condition in pivot.columns:
                margins = pivot[condition].dropna().to_numpy()
                values = (margins > 0).astype(float)
                low, high = interval(values)
                rows.append({"model": model, "normalization": norm,
                             "contrast": f"accuracy_{condition}", "n_items": len(values),
                             "estimate": values.mean(), "ci_low": low, "ci_high": high,
                             "positive_rate": values.mean()})
    summary = pd.DataFrame(rows)
    out = ROOT / "results/extensions/doppel_natural_summary.csv"
    summary.to_csv(out, index=False)

    # Does construct decomposition alter the apparent ranking of models?
    rank_rows = []
    mean_data = item_avg[item_avg.condition.isin(["full", "language_unrelated"])]
    pivot = mean_data.pivot(index=["id", "model"], columns="condition",
                            values="margin_mean").reset_index()
    pivot["context_adjusted"] = pivot["full"] - pivot["language_unrelated"]
    for model, group in pivot.groupby("model"):
        rank_rows.append({"model": model, "raw_full_accuracy": (group.full > 0).mean(),
                          "raw_full_margin": group.full.mean(),
                          "context_adjusted_margin": group.context_adjusted.mean()})
    ranks = pd.DataFrame(rank_rows)
    ranks["rank_raw"] = ranks.raw_full_margin.rank(ascending=False, method="min")
    ranks["rank_adjusted"] = ranks.context_adjusted_margin.rank(ascending=False,
                                                                 method="min")
    ranks.to_csv(ROOT / "results/extensions/doppel_natural_rankings.csv", index=False)
    report = "# Independent natural-context construct validation\n\n"
    report += summary.to_markdown(index=False)
    report += "\n\n## Raw vs context-adjusted ranking\n\n" + ranks.to_markdown(index=False) + "\n"
    (ROOT / "reports/doppel_natural.md").write_text(report)
    print(summary.to_string(index=False))
    print(ranks.to_string(index=False))


if __name__ == "__main__":
    main()
