#!/usr/bin/env python3
"""Crossover analysis, bootstrap uncertainty, and explicit kill-or-go decision."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RNG = np.random.default_rng(20260810)


def load() -> pd.DataFrame:
    rows = []
    for p in sorted((ROOT / "results").glob("fold*_dose*.jsonl")):
        rows.extend(json.loads(x) for x in p.read_text().splitlines())
    return pd.DataFrame(rows)


def bootstrap_mean(a: np.ndarray, n=10000):
    vals = np.array([RNG.choice(a, len(a), replace=True).mean() for _ in range(n)])
    return float(a.mean()), float(np.quantile(vals, .025)), float(np.quantile(vals, .975))


def main():
    d = load()
    if set(d.dose.unique()) != {0, 32, 128} or set(d.fold.unique()) != {0, 1}:
        raise RuntimeError("Both folds and all doses must finish before analysis")
    base = d[d.dose == 0][["fold", "id", "margin", "is_correct"]].rename(columns={"margin":"margin_pre", "is_correct":"correct_pre"})
    post = d[d.dose > 0].merge(base, on=["fold", "id"])
    post["delta_margin"] = post.margin - post.margin_pre
    post["specific_intrusion"] = post.correct_pre & ~post.is_correct
    summary = post.groupby(["dose", "group", "treated"]).agg(
        n=("id","size"), pre_accuracy=("correct_pre","mean"), post_accuracy=("is_correct","mean"),
        mean_delta_margin=("delta_margin","mean"), cir=("specific_intrusion","mean")
    ).reset_index()
    summary.to_csv(ROOT / "results/summary.csv", index=False)

    # Crossover pairs: every false friend is treated in one fold and held out in the other.
    ff = post[post.group == "false_friend"]
    pairs = ff.pivot_table(index=["dose","id"], columns="treated", values="delta_margin").reset_index()
    pairs["treated_minus_heldout"] = pairs[True] - pairs[False]
    pair_stats = []
    for dose, g in pairs.groupby("dose"):
        mean, lo, hi = bootstrap_mean(g.treated_minus_heldout.to_numpy())
        tr = ff[(ff.dose == dose) & ff.treated]
        ho = ff[(ff.dose == dose) & ~ff.treated]
        eligible_tr = tr[tr.correct_pre]
        eligible_ho = ho[ho.correct_pre]
        pair_stats.append({
            "dose": int(dose), "n_words": len(g), "paired_delta_margin": mean,
            "ci95_low": lo, "ci95_high": hi,
            "treated_cir": float((~eligible_tr.is_correct).mean()) if len(eligible_tr) else None,
            "heldout_cir": float((~eligible_ho.is_correct).mean()) if len(eligible_ho) else None,
            "eligible_treated": len(eligible_tr), "eligible_heldout": len(eligible_ho),
        })
    stats = pd.DataFrame(pair_stats)
    stats.to_csv(ROOT / "results/crossover_stats.csv", index=False)
    s32, s128 = [stats[stats.dose == x].iloc[0] for x in (32,128)]
    # Strict go: targeted margin effect is negative with CI excluding zero at 128,
    # grows from dose 32, and targeted CIR exceeds held-out CIR by >=10 points.
    dose_growth = s128.paired_delta_margin < s32.paired_delta_margin
    localized = s128.ci95_high < 0
    cir_gap = (s128.treated_cir - s128.heldout_cir) >= .10
    decision = "GO" if localized and dose_growth and cir_gap else "KILL"
    reasons = {"localized_ci_below_zero": bool(localized), "dose_response": bool(dose_growth), "cir_gap_ge_0.10": bool(cir_gap)}
    report = [
        "# Semantic Overwrite Pilot Decision", "", f"## Decision: **{decision}**", "",
        "The pre-registered operational rule requires all three checks to pass:", "",
        f"- 128-exposure paired treated-minus-held-out Δmargin CI is below zero: `{localized}`",
        f"- Effect is more negative at 128 than 32 exposures: `{dose_growth}`",
        f"- Treated CIR exceeds held-out CIR by at least 10 percentage points: `{cir_gap}`", "",
        "## Crossover results", "", stats.to_markdown(index=False), "",
        "## Group summaries", "", summary.to_markdown(index=False), "",
        "CIR is computed only as pre-correct → specific Chinese-sense candidate post; the paired Δmargin is the primary causal estimand.",
    ]
    (ROOT / "reports/decision.md").write_text("\n".join(report) + "\n")
    (ROOT / "reports/decision.json").write_text(json.dumps({"decision":decision,"checks":reasons,"crossover":pair_stats}, indent=2) + "\n")
    print("\n".join(report))


if __name__ == "__main__":
    main()
