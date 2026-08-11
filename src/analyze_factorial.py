#!/usr/bin/env python3
"""Analyze language and semantic-context main effects with item bootstrap CIs."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RNG = np.random.default_rng(20260811)


def ci(values: np.ndarray) -> tuple[float, float]:
    indices = RNG.integers(0, len(values), size=(5000, len(values)))
    boots = values[indices].mean(axis=1)
    return float(np.quantile(boots, .025)), float(np.quantile(boots, .975))


def effects(group: pd.DataFrame, metric: str) -> pd.DataFrame:
    pivot = group.pivot(index="id", columns=["language", "sense"], values=metric)
    assert set(pivot.columns) == {(1, 1), (1, 2), (2, 1), (2, 2)}
    out = pd.DataFrame(index=pivot.index)
    out["semantic"] = ((pivot[1, 2] + pivot[2, 2]) - (pivot[1, 1] + pivot[2, 1])) / 2
    out["language"] = ((pivot[2, 1] + pivot[2, 2]) - (pivot[1, 1] + pivot[1, 2])) / 2
    out["interaction"] = (pivot[2, 2] - pivot[2, 1]) - (pivot[1, 2] - pivot[1, 1])
    out["diagonal_switch"] = pivot[2, 2] - pivot[1, 1]
    out["midpoint"] = (pivot[2, 2] + pivot[1, 1]) / 2
    return out


def main():
    rows = []
    for path in (ROOT / "results/extensions").glob("factorial_*.jsonl"):
        rows.extend(json.loads(line) for line in path.read_text().splitlines())
    data = pd.DataFrame(rows)
    assert len(data), "no factorial result files"
    summaries, item_rows = [], []
    keys = ["pair", "model", "prompt_mode", "condition", "wrapper"]
    for key, group in data.groupby(keys):
        for normalization, metric in (("mean", "margin_mean"), ("sum", "margin_sum")):
            frame = effects(group, metric)
            for name in frame.columns:
                values = frame[name].to_numpy()
                low, high = ci(values)
                summaries.append(dict(zip(keys, key)) | {
                    "normalization": normalization, "effect": name, "n": len(values),
                    "estimate": values.mean(), "ci_low": low, "ci_high": high,
                    "positive_rate": (values > 0).mean(),
                })
            for item_id, row in frame.iterrows():
                item_rows.append(dict(zip(keys, key)) | {"normalization": normalization, "id": item_id} | row.to_dict())
    summary = pd.DataFrame(summaries)
    items = pd.DataFrame(item_rows)
    contrasts = []
    contrast_keys = ["pair", "model", "prompt_mode", "wrapper", "normalization"]
    for key, group in items.groupby(contrast_keys):
        pivot = group.pivot(index="id", columns="condition", values="semantic")
        for comparison, right in (("full_minus_shuffled", "shuffled"),
                                  ("full_minus_language_only", "language_only"),
                                  ("masked_minus_shuffled", "shuffled")):
            left = "masked" if comparison.startswith("masked") else "full"
            values = (pivot[left] - pivot[right]).to_numpy()
            low, high = ci(values)
            contrasts.append(dict(zip(contrast_keys, key)) | {
                "contrast": comparison, "n": len(values), "estimate": values.mean(),
                "ci_low": low, "ci_high": high, "positive_rate": (values > 0).mean(),
            })
    contrast_frame = pd.DataFrame(contrasts)
    summary.to_csv(ROOT / "results/extensions/factorial_summary.csv", index=False)
    items.to_csv(ROOT / "results/extensions/factorial_item_effects.csv", index=False)
    contrast_frame.to_csv(ROOT / "results/extensions/factorial_contrasts.csv", index=False)

    # Construct gate: full-context semantic effect must be positive under all
    # wrappers and both normalizations for each evaluated model/pair/mode cell;
    # language-only and shuffled controls should not show the same robust effect.
    semantic = summary[summary.effect == "semantic"]
    full = semantic[semantic.condition == "full"]
    gate_rows = []
    for key, group in full.groupby(["pair", "model", "prompt_mode"]):
        pass_all = bool((group.ci_low > 0).all())
        gate_rows.append({"pair": key[0], "model": key[1], "prompt_mode": key[2],
                          "n_variants": len(group), "all_full_semantic_ci_positive": pass_all})
    gate = pd.DataFrame(gate_rows)
    gate.to_csv(ROOT / "results/extensions/factorial_gate.csv", index=False)
    report = "# Exact-form language × semantic-context construct killer\n\n"
    report += "## Gate\n\n" + gate.to_markdown(index=False) + "\n\n"
    selected = semantic[semantic.condition.isin(["full", "masked", "language_only", "shuffled"])]
    report += "## Semantic effects\n\n" + selected.to_markdown(index=False) + "\n"
    report += "\n## Paired construct contrasts\n\n" + contrast_frame.to_markdown(index=False) + "\n"
    (ROOT / "reports/factorial_construct.md").write_text(report)
    print(gate.to_string(index=False))


if __name__ == "__main__":
    main()
