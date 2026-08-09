#!/usr/bin/env python3
"""Fail fast if the published aggregate evidence contradicts the verdict."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def main():
    paired = pd.read_csv(ROOT / "results/extensions/paired_sense_summary.csv")
    assert len(paired) == 8, "expected 4 checkpoints x 2 language pairs"
    assert set(paired.pair) == {"zh_ja", "en_de"}
    assert (paired.ci_low > 0).all(), "a mean sense-switch CI crosses zero"
    assert (paired.switch_positive > paired.both_accuracy).all()

    lift = pd.read_csv(ROOT / "results/extensions/context_lift_summary.csv")
    conflict = lift[(lift.condition == "conflict") & (lift.metric == "dlift")].iloc[0]
    assert conflict.ci_low < 0 < conflict.ci_high, "adjusted overwrite unexpectedly significant"

    causal = pd.read_csv(ROOT / "results/extensions/doppel_switch_causal.csv")
    did = causal[(causal.condition == "conflict_minus_neutral") & (causal.metric == "dswitch")].iloc[0]
    assert did.ci_low < 0 < did.ci_high, "dynamic difference-in-differences no longer inconclusive"
    print("artifact validation passed: old hypothesis KILL, paired audit conditional GO")


if __name__ == "__main__":
    main()
