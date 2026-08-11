#!/usr/bin/env python3
"""Analyze target-span component patching against the answer-boundary result."""
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


def row(out, model, component, layer, group, effect, values):
    values = np.asarray(values); low, high = ci(values)
    out.append({"model": model, "component": component, "layer": layer, "group": group,
                "effect": effect, "n_items": len(values), "estimate": values.mean(),
                "ci_low": low, "ci_high": high, "positive_rate": (values > 0).mean()})


def independent_difference(left, right):
    """Bootstrap a difference in group means without inventing item pairing."""
    left, right = np.asarray(left), np.asarray(right)
    draws_left = left[RNG.integers(0, len(left), (5000, len(left)))].mean(1)
    draws_right = right[RNG.integers(0, len(right), (5000, len(right)))].mean(1)
    draws = draws_left - draws_right
    return left.mean() - right.mean(), *np.quantile(draws, [.025, .975])


def main():
    records = []
    for path in (ROOT / "results/extensions").glob("target_component_*.jsonl"):
        records.extend(json.loads(line) for line in path.read_text().splitlines())
    data = pd.DataFrame(records); assert len(data), "no target-patch outputs"
    pivot = data.pivot(index=["model", "component", "layer", "id", "group", "language", "sense"],
                       columns="candidate_sense", values="mean_logp").reset_index()
    pivot["margin"] = pivot[2] - pivot[1]
    output, excess_rows = [], []
    patched = pivot[pivot.layer >= 0]
    for (model, component, layer), frame in patched.groupby(["model", "component", "layer"]):
        ff = frame[frame.group == "false_friend"].pivot(
            index="id", columns=["language", "sense"], values="margin")
        semantic = ((ff[(1, 2)] + ff[(2, 2)]) - (ff[(1, 1)] + ff[(2, 1)])) / 2
        language = ((ff[(2, 1)] + ff[(2, 2)]) - (ff[(1, 1)] + ff[(1, 2)])) / 2
        row(output, model, component, layer, "false_friend", "semantic_main", semantic)
        row(output, model, component, layer, "false_friend", "language_main", language)
        mono = frame[frame.group == "monolingual_polysemy"].pivot(
            index="id", columns="sense", values="margin")
        row(output, model, component, layer, "monolingual_polysemy", "semantic_main",
            mono[2] - mono[1])
        for control_name in ("true_friend", "translation_control"):
            control = frame[frame.group == control_name].pivot(
                index="id", columns="language", values="margin")
            control_language = control[2] - control[1]
            row(output, model, component, layer, control_name, "language_main",
                control_language)
            estimate, low, high = independent_difference(language, control_language)
            excess_rows.append({"model": model, "component": component, "layer": layer,
                "control": control_name, "estimate": estimate, "ci_low": low,
                "ci_high": high, "n_false": len(language), "n_control": len(control_language)})
    summary = pd.DataFrame(output)
    summary.to_csv(ROOT / "results/extensions/target_patch_summary.csv", index=False)
    excess = pd.DataFrame(excess_rows)
    excess.to_csv(ROOT / "results/extensions/target_patch_language_excess.csv", index=False)
    profiles = []
    for keys, frame in summary[summary.effect == "semantic_main"].groupby(["model", "component"]):
        ff = frame[frame.group == "false_friend"].sort_values("layer")
        mono = frame[frame.group == "monolingual_polysemy"].sort_values("layer")
        profiles.append({"model": keys[0], "component": keys[1],
            "profile_correlation": np.corrcoef(ff.estimate, mono.estimate)[0, 1],
            "ff_significant_layers": int((ff.ci_low > 0).sum()),
            "mono_significant_layers": int((mono.ci_low > 0).sum()),
            "ff_peak_layer": int(ff.loc[ff.estimate.idxmax(), "layer"]),
            "mono_peak_layer": int(mono.loc[mono.estimate.idxmax(), "layer"])})
    profiles = pd.DataFrame(profiles)
    profiles.to_csv(ROOT / "results/extensions/target_patch_profiles.csv", index=False)
    (ROOT / "reports/target_component_patching.md").write_text(
        "# Target-span residual/attention/MLP patching\n\n" + summary.to_markdown(index=False) +
        "\n\n## False-friend language excess over controls\n\n" +
        excess.to_markdown(index=False) + "\n\n## Profiles\n\n" +
        profiles.to_markdown(index=False) + "\n")
    print(profiles.to_string(index=False))


if __name__ == "__main__":
    main()
