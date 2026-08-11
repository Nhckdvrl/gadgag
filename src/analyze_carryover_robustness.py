#!/usr/bin/env python3
"""Compare the main user-prime protocol with assistant-prime replication."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RNG = np.random.default_rng(20260812)


def ci(values):
    values = np.asarray(values)
    draws = RNG.integers(0, len(values), (5000, len(values)))
    means = values[draws].mean(1)
    return np.quantile(means, [.025, .975])


def main():
    records = []
    for path in (ROOT / "results/extensions").glob("carryover_alt_*.jsonl"):
        records.extend(json.loads(line) for line in path.read_text().splitlines())
    data = pd.DataFrame(records)
    assert len(data), "no assistant-prime outputs"
    rows = []
    for key, group in data.groupby(["pair", "model", "lag"]):
        pivot = group.pivot(index=["id", "target_language"], columns="condition",
                            values="correct_margin_mean")
        for name, left, right in (
            ("wrong_exact_minus_language", "wrong_exact", "language_unrelated"),
            ("wrong_exact_minus_masked", "wrong_exact", "wrong_masked"),
            ("wrong_masked_minus_language", "wrong_masked", "language_unrelated"),
        ):
            values = (pivot[left] - pivot[right]).groupby(level="id").mean().to_numpy()
            low, high = ci(values)
            rows.append(dict(zip(["pair", "model", "lag"], key)) | {
                "comparison": name, "n_items": len(values), "estimate": values.mean(),
                "ci_low": low, "ci_high": high})
    summary = pd.DataFrame(rows)
    summary.to_csv(ROOT / "results/extensions/carryover_role_robustness.csv", index=False)
    (ROOT / "reports/carryover_role_robustness.md").write_text(
        "# Assistant-prime robustness\n\n" + summary.to_markdown(index=False) + "\n")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
