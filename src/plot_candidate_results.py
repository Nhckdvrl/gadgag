#!/usr/bin/env python3
"""Create compact aggregate figures for the three-candidate decision report."""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "figures"
OUT.mkdir(exist_ok=True)
plt.style.use("seaborn-v0_8-whitegrid")


def plot_c():
    data = pd.read_csv(ROOT / "results/extensions/carryover_summary.csv")
    data = data[data.normalization == "mean"]
    names = {
        "wrong_exact_minus_language": "wrong exact − language control",
        "wrong_masked_minus_language": "semantic/no-form − language control",
        "wrong_exact_minus_masked": "added exact-form contribution",
    }
    fig, ax = plt.subplots(figsize=(7.2, 4.3))
    for key, label in names.items():
        group = data[data.comparison == key].groupby("lag").estimate
        mean, sem = group.mean(), group.sem()
        ax.errorbar(mean.index, mean, yerr=1.96 * sem, marker="o", capsize=3, label=label)
    ax.axhline(0, color="black", linewidth=.8)
    ax.set(xlabel="Unrelated intervening turns", ylabel="Change in correct-sense margin",
           title="C: cross-turn sense intrusion persists, but exact-form amplification is smaller")
    ax.legend(fontsize=8)
    fig.tight_layout(); fig.savefig(OUT / "candidate_c_carryover.png", dpi=180); plt.close(fig)


def plot_b():
    data = pd.read_csv(ROOT / "results/extensions/doppel_natural_summary.csv")
    wanted = ["full_minus_unrelated", "masked_minus_unrelated", "full_minus_masked"]
    data = data[(data.normalization == "mean") & data.contrast.isin(wanted)]
    pivot = data.pivot(index="model", columns="contrast", values="estimate")[wanted]
    ax = pivot.plot.bar(figsize=(7.2, 4.3), rot=0)
    ax.axhline(0, color="black", linewidth=.8)
    ax.set(ylabel="Paired margin contrast",
           title="B: independent non-replacement contexts separate context from form")
    ax.legend(["full − unrelated", "masked − unrelated", "full − masked"], fontsize=8)
    ax.figure.tight_layout(); ax.figure.savefig(OUT / "candidate_b_natural.png", dpi=180)
    plt.close(ax.figure)


def plot_a():
    data = pd.read_csv(ROOT / "results/extensions/causal_gating_summary.csv")
    data = data[(data.group == "false_friend") &
                data.effect.isin(["semantic_main", "language_main"])]
    fig, axes = plt.subplots(1, 2, figsize=(9.2, 3.8), sharey=False)
    for ax, (model, frame) in zip(axes, data.groupby("model")):
        maximum = frame.layer.max()
        for effect, curve in frame.groupby("effect"):
            curve = curve.sort_values("layer")
            ax.plot(curve.layer / maximum, curve.estimate, marker="o",
                    label=effect.replace("_", " "))
            ax.fill_between(curve.layer / maximum, curve.ci_low, curve.ci_high, alpha=.15)
        ax.axhline(0, color="black", linewidth=.8)
        ax.set(title=model, xlabel="Relative layer depth")
    axes[0].set_ylabel("Causal change in sense-2 margin")
    axes[1].legend(fontsize=8)
    fig.suptitle("A: semantic evidence and a false-friend-specific language convention emerge late")
    fig.tight_layout(); fig.savefig(OUT / "candidate_a_causal.png", dpi=180); plt.close(fig)


if __name__ == "__main__":
    plot_c(); plot_b(); plot_a()
