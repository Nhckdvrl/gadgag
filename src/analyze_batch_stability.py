#!/usr/bin/env python3
"""Compare identical likelihood evaluations across two scoring batch sizes."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd


def load(path: Path) -> pd.DataFrame:
    return pd.DataFrame(json.loads(line) for line in path.read_text().splitlines())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch8", type=Path, action="append", required=True)
    parser.add_argument("--batch32", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    assert len(args.batch8) == len(args.batch32)
    keys = ["id", "condition", "language", "sense", "wrapper"]
    rows = []
    effect_rows = []
    for small_path, large_path in zip(args.batch8, args.batch32):
        small, large = load(small_path), load(large_path)
        merged = small.merge(large, on=keys, suffixes=("_b8", "_b32"), validate="one_to_one")
        assert len(merged) == len(small) == len(large)
        for normalization in ("mean", "sum"):
            left, right = f"margin_{normalization}_b8", f"margin_{normalization}_b32"
            difference = merged[left] - merged[right]
            sign_flip = (merged[left] > 0) != (merged[right] > 0)
            rows.append({
                "pair": small.pair.iloc[0], "model": small.model.iloc[0],
                "prompt_mode": small.prompt_mode.iloc[0], "normalization": normalization,
                "n_cells": len(merged), "mean_abs_margin_difference": difference.abs().mean(),
                "max_abs_margin_difference": difference.abs().max(),
                "decision_sign_flips": int(sign_flip.sum()),
                "decision_sign_flip_rate": sign_flip.mean(),
                "pearson_margin": np.corrcoef(merged[left], merged[right])[0, 1],
            })
        for batch, frame in ((8, small), (32, large)):
            frame = frame[frame.condition == "full"]
            for wrapper, group in frame.groupby("wrapper"):
                for normalization in ("mean", "sum"):
                    pivot = group.pivot(
                        index="id", columns=["language", "sense"],
                        values=f"margin_{normalization}",
                    )
                    semantic = (
                        (pivot[1, 2] + pivot[2, 2])
                        - (pivot[1, 1] + pivot[2, 1])
                    ) / 2
                    rng = np.random.default_rng(20260811)
                    indices = rng.integers(0, len(semantic), size=(5000, len(semantic)))
                    boots = semantic.to_numpy()[indices].mean(axis=1)
                    effect_rows.append({
                        "pair": frame.pair.iloc[0], "model": frame.model.iloc[0],
                        "prompt_mode": frame.prompt_mode.iloc[0], "batch_size": batch,
                        "wrapper": wrapper, "normalization": normalization,
                        "n_items": len(semantic), "semantic_effect": semantic.mean(),
                        "ci_low": np.quantile(boots, 0.025),
                        "ci_high": np.quantile(boots, 0.975),
                    })
    output = pd.DataFrame(rows)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    output.to_csv(args.output, index=False)
    effects = pd.DataFrame(effect_rows)
    effects.to_csv(args.output.parent / "batch_stability_effects.csv", index=False)
    report = "# Scoring batch-size stability\n\n## Cell margins\n\n"
    report += output.to_markdown(index=False)
    report += "\n\n## Full-context semantic effects\n\n"
    report += effects.to_markdown(index=False) + "\n"
    (Path(__file__).resolve().parents[1] / "reports/batch_stability.md").write_text(report)
    print(output.to_string(index=False))


if __name__ == "__main__":
    main()
