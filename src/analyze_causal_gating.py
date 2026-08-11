#!/usr/bin/env python3
"""Analyze causal residual patching and explicit A kill gates."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RNG = np.random.default_rng(20260812)


def ci(values: np.ndarray) -> tuple[float, float]:
    draws = RNG.integers(0, len(values), (5000, len(values)))
    means = values[draws].mean(axis=1)
    return float(np.quantile(means, .025)), float(np.quantile(means, .975))


def add_row(rows, model, layer, group, effect, values):
    values = np.asarray(values, float)
    low, high = ci(values)
    rows.append({"model": model, "layer": layer, "group": group, "effect": effect,
                 "n_items": len(values), "estimate": values.mean(),
                 "ci_low": low, "ci_high": high,
                 "positive_rate": (values > 0).mean()})


def add_independent_difference(rows, model, layer, group, effect, left, right):
    left, right = np.asarray(left, float), np.asarray(right, float)
    left_draws = left[RNG.integers(0, len(left), (5000, len(left)))].mean(axis=1)
    right_draws = right[RNG.integers(0, len(right), (5000, len(right)))].mean(axis=1)
    draws = left_draws - right_draws
    rows.append({"model": model, "layer": layer, "group": group, "effect": effect,
                 "n_items": f"{len(left)}+{len(right)}", "estimate": left.mean() - right.mean(),
                 "ci_low": np.quantile(draws, .025), "ci_high": np.quantile(draws, .975),
                 "positive_rate": np.nan})


def main() -> None:
    records = []
    for path in (ROOT / "results/extensions").glob("causal_gating_*.jsonl"):
        records.extend(json.loads(line) for line in path.read_text().splitlines())
    data = pd.DataFrame(records)
    assert len(data), "no causal gating outputs"
    pivot = data.pivot(index=["model", "pair", "layer", "id", "group", "language", "sense"],
                       columns="candidate_sense", values="mean_logp").reset_index()
    pivot["margin"] = pivot[2] - pivot[1]
    behavioral_rows = []
    observed = pivot[pivot.layer == -2].copy()
    observed["correct"] = np.where(observed.sense == 2,
                                   observed.margin > 0, observed.margin < 0)
    for (model, group), frame in observed.groupby(["model", "group"]):
        item_accuracy = frame.groupby("id").correct.mean().to_numpy()
        low, high = ci(item_accuracy)
        behavioral_rows.append({"model": model, "group": group,
                                "n_items": len(item_accuracy),
                                "accuracy": item_accuracy.mean(),
                                "ci_low": low, "ci_high": high})
    behavioral = pd.DataFrame(behavioral_rows)
    behavioral.to_csv(ROOT / "results/extensions/causal_behavioral_gate.csv", index=False)
    baselines = pivot[pivot.layer == -1][
        ["model", "id", "group", "language", "sense", "margin"]].rename(
            columns={"margin": "baseline"})
    patched = pivot[pivot.layer >= 0].merge(
        baselines, on=["model", "id", "group", "language", "sense"], validate="many_to_one")
    sign = np.where(patched.sense == 2, 1., -1.)
    patched["causal_rescue"] = sign * (patched.margin - patched.baseline)

    rows = []
    for (model, layer, group), frame in patched.groupby(["model", "layer", "group"]):
        item_values = frame.groupby("id").causal_rescue.mean().to_numpy()
        add_row(rows, model, layer, group, "signed_causal_rescue", item_values)

    # Factorial effects: positive semantic effect means sense information was
    # causally transferred; language main effect means donor language shifted
    # the decision despite a fixed recipient and English outputs.
    ff = patched[patched.group == "false_friend"]
    for (model, layer), frame in ff.groupby(["model", "layer"]):
        table = frame.pivot(index="id", columns=["language", "sense"], values="margin")
        semantic = ((table[(1, 2)] + table[(2, 2)]) -
                    (table[(1, 1)] + table[(2, 1)])) / 2
        language = ((table[(2, 1)] + table[(2, 2)]) -
                    (table[(1, 1)] + table[(1, 2)])) / 2
        interaction = (table[(1, 1)] - table[(1, 2)] -
                       table[(2, 1)] + table[(2, 2)])
        add_row(rows, model, layer, "false_friend", "semantic_main", semantic.to_numpy())
        add_row(rows, model, layer, "false_friend", "language_main", language.to_numpy())
        add_row(rows, model, layer, "false_friend", "language_x_semantics",
                interaction.to_numpy())

    mono = patched[patched.group == "monolingual_polysemy"]
    for (model, layer), frame in mono.groupby(["model", "layer"]):
        table = frame.pivot(index="id", columns="sense", values="margin")
        add_row(rows, model, layer, "monolingual_polysemy", "semantic_main",
                (table[2] - table[1]).to_numpy())

    for group in ("true_friend", "translation_control"):
        control = patched[patched.group == group]
        for (model, layer), frame in control.groupby(["model", "layer"]):
            table = frame.pivot(index="id", columns="language", values="margin")
            add_row(rows, model, layer, group, "language_main",
                    (table[2] - table[1]).to_numpy())

    # A false-friend-specific gate must exceed the language transfer observed
    # for same-sense controls, not merely be non-zero by itself.
    for (model, layer), ff_frame in ff.groupby(["model", "layer"]):
        ff_table = ff_frame.pivot(index="id", columns=["language", "sense"], values="margin")
        ff_language = (((ff_table[(2, 1)] + ff_table[(2, 2)]) -
                        (ff_table[(1, 1)] + ff_table[(1, 2)])) / 2).to_numpy()
        for control_name in ("true_friend", "translation_control"):
            control = patched[(patched.model == model) & (patched.layer == layer) &
                              (patched.group == control_name)]
            control_table = control.pivot(index="id", columns="language", values="margin")
            control_language = (control_table[2] - control_table[1]).to_numpy()
            add_independent_difference(rows, model, layer, "false_friend",
                                       f"language_excess_vs_{control_name}",
                                       ff_language, control_language)

    summary = pd.DataFrame(rows)
    summary.to_csv(ROOT / "results/extensions/causal_gating_summary.csv", index=False)

    # Direct profile comparison on relative depth, one row per model.
    comparisons = []
    for model, frame in summary[(summary.effect == "semantic_main")].groupby("model"):
        ff_curve = frame[frame.group == "false_friend"].sort_values("layer")
        mono_curve = frame[frame.group == "monolingual_polysemy"].sort_values("layer")
        if len(ff_curve) == len(mono_curve) and len(ff_curve) > 2:
            correlation = np.corrcoef(ff_curve.estimate, mono_curve.estimate)[0, 1]
            comparisons.append({
                "model": model, "profile_correlation": correlation,
                "ff_peak_layer": int(ff_curve.loc[ff_curve.estimate.idxmax(), "layer"]),
                "mono_peak_layer": int(mono_curve.loc[mono_curve.estimate.idxmax(), "layer"]),
                "ff_max_semantic": ff_curve.estimate.max(),
                "ff_max_language_abs": summary[(summary.model == model) &
                    (summary.group == "false_friend") &
                    (summary.effect == "language_main")].estimate.abs().max(),
            })
    profiles = pd.DataFrame(comparisons)
    profiles.to_csv(ROOT / "results/extensions/causal_profile_comparison.csv", index=False)
    report = "# Language gating versus general WSD: causal patching\n\n"
    report += "## Behavioral gate\n\n" + behavioral.to_markdown(index=False) + "\n\n"
    report += "## Causal effects\n\n"
    report += summary.to_markdown(index=False)
    report += "\n\n## False-friend versus monolingual profile\n\n"
    report += profiles.to_markdown(index=False) + "\n"
    (ROOT / "reports/causal_gating.md").write_text(report)
    print(profiles.to_string(index=False))


if __name__ == "__main__":
    main()
