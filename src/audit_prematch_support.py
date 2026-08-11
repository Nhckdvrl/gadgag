#!/usr/bin/env python3
"""Design-stage overlap audit for the cached model-blind control pool."""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import linear_sum_assignment
from transformers import AutoTokenizer

from build_prematched_controls import false_features

ROOT = Path(__file__).resolve().parents[1]
COVARIATES = ["freq_l1", "freq_l2", "freq_ratio", "char_l1", "char_l2",
              "gloss_tokens", "tok1_l1", "tok1_l2", "tok2_l1", "tok2_l2"]


def assignment(false: pd.DataFrame, pool: pd.DataFrame, caliper: float):
    combined = pd.concat([false, pool], ignore_index=True)
    scale = combined[COVARIATES].std().replace(0, 1)
    left = false[COVARIATES].to_numpy() / scale.to_numpy()
    right = pool[COVARIATES].to_numpy() / scale.to_numpy()
    gap = np.abs(left[:, None, :] - right[None, :, :])
    pos_ok = np.array([[(a.pos_l1 == b.pos_l1_context and
                         a.pos_l2 == b.pos_l2_context)
                        for _, b in pool.iterrows()] for _, a in false.iterrows()])
    feasible = (gap <= caliper).all(2) & pos_ok
    distance = (gap ** 2).sum(2)
    cost = np.concatenate([np.where(feasible, distance, 1e6),
                           np.full((len(false), len(false)), 1e4)], axis=1)
    rows, cols = linear_sum_assignment(cost)
    pairs = [(i, j) for i, j in zip(rows, cols) if j < len(pool) and feasible[i, j]]
    if not pairs:
        return pairs, np.nan, np.nan
    lf = false.iloc[[i for i, _ in pairs]]
    rc = pool.iloc[[j for _, j in pairs]]
    smd = ((lf[COVARIATES].mean() - rc[COVARIATES].mean()) / scale).abs()
    return pairs, float(smd.max()), float(smd.mean())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pool", type=Path, required=True)
    parser.add_argument("--stingray-root", type=Path, required=True)
    parser.add_argument("--output", type=Path,
                        default=ROOT / "results/extensions/prematch_support_audit.csv")
    args = parser.parse_args()
    pool = pd.read_csv(args.pool)
    tokenizers = [AutoTokenizer.from_pretrained(name, local_files_only=True) for name in
                  ("Qwen/Qwen3-8B", "google/gemma-3-12b-it")]
    false = false_features(args.stingray_root, tokenizers)
    rows = []
    for group in ("true_friend", "translation_control"):
        available = pool[(pool.group == group) & (pool.freq_l1 >= 2) &
                         (pool.freq_l2 >= 2)].reset_index(drop=True)
        for caliper in (1.0, 1.5, 2.0, 2.5, 3.0, 4.0):
            pairs, max_smd, mean_smd = assignment(false, available, caliper)
            rows.append({"group": group, "available_controls": len(available),
                         "caliper_sd_each_covariate": caliper, "matched_pairs": len(pairs),
                         "max_abs_smd": max_smd, "mean_abs_smd": mean_smd})
        # Leave-one-covariate-out counts identify which requirement blocks overlap.
        combined = pd.concat([false, available], ignore_index=True)
        scale = combined[COVARIATES].std().replace(0, 1)
        gap = np.abs(false[COVARIATES].to_numpy()[:, None, :] -
                     available[COVARIATES].to_numpy()[None, :, :]) / scale.to_numpy()
        pos_ok = np.array([[(a.pos_l1 == b.pos_l1_context and
                             a.pos_l2 == b.pos_l2_context)
                            for _, b in available.iterrows()] for _, a in false.iterrows()])
        for excluded in COVARIATES:
            keep = [i for i, name in enumerate(COVARIATES) if name != excluded]
            supported = ((gap[:, :, keep] <= 1).all(2) & pos_ok).any(1).sum()
            rows.append({"group": group, "available_controls": len(available),
                         "caliper_sd_each_covariate": "1.0_except",
                         "excluded_covariate": excluded, "matched_pairs": int(supported),
                         "max_abs_smd": np.nan, "mean_abs_smd": np.nan})
    result = pd.DataFrame(rows)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(args.output, index=False)
    print(result.to_string(index=False))


if __name__ == "__main__":
    main()
