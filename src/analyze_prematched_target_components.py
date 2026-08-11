#!/usr/bin/env python3
"""Paired confirmatory excess analysis for human-validated frozen controls."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

RNG = np.random.default_rng(20260811)


def paired_ci(values: np.ndarray) -> tuple[float, float]:
    draws = values[RNG.integers(0, len(values), (10000, len(values)))].mean(1)
    return tuple(np.quantile(draws, [.025, .975]))


def language_effects(path: Path) -> pd.DataFrame:
    data = pd.DataFrame(json.loads(line) for line in path.read_text().splitlines())
    data = data[(data.layer >= 0) & data.group.isin(
        ["false_friend", "true_friend", "translation_control"])]
    pivot = data.pivot(index=["model", "component", "layer", "id", "group",
                              "language", "sense"],
                       columns="candidate_sense", values="mean_logp").reset_index()
    pivot["margin"] = pivot[2] - pivot[1]
    rows = []
    for (model, component, layer, item_id, group), frame in pivot.groupby(
            ["model", "component", "layer", "id", "group"]):
        if group == "false_friend":
            table = frame.pivot(index="language", columns="sense", values="margin")
            effect = ((table.loc[2, 1] + table.loc[2, 2]) -
                      (table.loc[1, 1] + table.loc[1, 2])) / 2
        else:
            table = frame.set_index("language").margin
            effect = table.loc[2] - table.loc[1]
        rows.append({"model": model, "component": component, "layer": layer,
                     "id": item_id, "group": group, "language_effect": effect})
    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", type=Path, nargs="+", required=True)
    parser.add_argument("--matching", type=Path, required=True)
    parser.add_argument("--gate-status", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    gate = json.loads(args.gate_status.read_text())
    if gate.get("target_confirmatory_analysis_allowed") is not True:
        raise RuntimeError("confirmatory analysis is LOCKED by measurement gates")
    effects = pd.concat([language_effects(path) for path in args.inputs], ignore_index=True)
    matching = pd.read_csv(args.matching, dtype=str)
    output, pair_level = [], []
    for (model, component, layer), frame in effects.groupby(["model", "component", "layer"]):
        maximum_layer = effects[(effects.model == model) &
                                (effects.component == component)].layer.max()
        false = frame[frame.group == "false_friend"][["id", "language_effect"]].rename(
            columns={"id": "false_id", "language_effect": "false_effect"})
        for group in ("true_friend", "translation_control"):
            controls = frame[frame.group == group][["id", "language_effect"]].rename(
                columns={"id": "control_id", "language_effect": "control_effect"})
            paired = matching[matching.group == group].merge(false, on="false_id",
                validate="one_to_one").merge(controls, on="control_id", validate="one_to_one")
            if len(paired) != matching[matching.group == group].false_id.nunique():
                raise ValueError(f"{model}/{component}/{layer}/{group}: incomplete frozen pairs")
            differences = (paired.false_effect - paired.control_effect).to_numpy(float)
            low, high = paired_ci(differences)
            output.append({"model": model, "component": component, "layer": layer,
                "relative_layer": layer / maximum_layer if maximum_layer else 0,
                "control": group, "n_pairs": len(differences),
                "paired_language_excess": differences.mean(), "ci_low": low,
                "ci_high": high, "positive_rate": (differences > 0).mean()})
            for (_, value), difference in zip(paired.iterrows(), differences):
                pair_level.append({"model": model, "component": component,
                    "layer": layer, "relative_layer": layer / maximum_layer,
                    "control": group, "false_id": value.false_id,
                    "control_id": value.control_id, "difference": difference})
    result = pd.DataFrame(output)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(args.output, index=False)
    pairs = pd.DataFrame(pair_level)
    primary_rows = []
    primary = pairs[pairs.relative_layer.between(.10, .75)]
    for keys, frame in primary.groupby(["model", "component", "control"]):
        per_pair = frame.groupby(["false_id", "control_id"]).difference.mean().to_numpy()
        low, high = paired_ci(per_pair)
        primary_rows.append({"model": keys[0], "component": keys[1],
            "control": keys[2], "preregistered_relative_depth": "0.10..0.75",
            "n_pairs": len(per_pair), "mean_paired_language_excess": per_pair.mean(),
            "ci_low": low, "ci_high": high, "positive_rate": (per_pair > 0).mean()})
    primary_result = pd.DataFrame(primary_rows)
    primary_path = args.output.with_name(args.output.stem + "_primary.csv")
    primary_result.to_csv(primary_path, index=False)
    print(primary_result.to_string(index=False))


if __name__ == "__main__":
    main()
