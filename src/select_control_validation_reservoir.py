#!/usr/bin/env python3
"""Select a balanced, redundant reservoir for human control validation."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import csr_matrix
from transformers import AutoTokenizer

from build_prematched_controls import false_features
from finalize_prematched_controls import COVARIATES

ROOT = Path(__file__).resolve().parents[1]


def select(false: pd.DataFrame, controls: pd.DataFrame, ratio: int, delta: float):
    supported_pos = set(zip(false.pos_l1, false.pos_l2))
    controls = controls[[(a, b) in supported_pos for a, b in
                         zip(controls.pos_l1_context, controls.pos_l2_context)]].reset_index(drop=True)
    combined = pd.concat([false, controls], ignore_index=True)
    scale = combined[COVARIATES].std().replace(0, 1)
    rows, lower, upper = [], [], []
    for pos, count in false.groupby(["pos_l1", "pos_l2"]).size().items():
        rows.append(((controls.pos_l1_context == pos[0]) &
                     (controls.pos_l2_context == pos[1])).astype(float).to_numpy())
        lower.append(ratio * count); upper.append(ratio * count)
    for column in COVARIATES:
        target_sum = ratio * false[column].sum()
        tolerance = ratio * len(false) * delta * scale[column]
        rows.append(controls[column].to_numpy(float))
        lower.append(target_sum - tolerance); upper.append(target_sum + tolerance)
    for column in COVARIATES:
        center = false[column].mean()
        c2 = ((controls[column] - center) / scale[column]) ** 2
        target = ratio * (((false[column] - center) / scale[column]) ** 2).sum()
        tolerance = ratio * len(false) * .25
        rows.append(c2.to_numpy(float)); lower.append(max(0, target - tolerance))
        upper.append(target + tolerance)
    for column in ("word_l1", "word_l2"):
        for _, indices in controls.groupby(column).groups.items():
            if len(indices) > 1:
                vector = np.zeros(len(controls)); vector[list(indices)] = 1
                rows.append(vector); lower.append(0); upper.append(1)
    nearest = []
    for _, control in controls.iterrows():
        same = false[(false.pos_l1 == control.pos_l1_context) &
                     (false.pos_l2 == control.pos_l2_context)]
        gap = (same[COVARIATES].to_numpy(float) -
               control[COVARIATES].to_numpy(float)) / scale.to_numpy(float)
        nearest.append((gap ** 2).sum(1).min())
    result = milp(c=np.asarray(nearest), integrality=np.ones(len(controls)),
        bounds=Bounds(0, 1), constraints=LinearConstraint(
            csr_matrix(np.vstack(rows)), lower, upper), options={"time_limit": 180})
    if not result.success:
        raise RuntimeError(result.message)
    chosen = controls[np.rint(result.x).astype(bool)].copy()
    balance = pd.DataFrame([{"covariate": column,
        "smd": (chosen[column].mean() - false[column].mean()) / scale[column],
        "false_mean": false[column].mean(), "reservoir_mean": chosen[column].mean(),
        "variance_ratio": chosen[column].var() / false[column].var()
                          if false[column].var() else np.nan} for column in COVARIATES])
    return chosen, balance


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shortlist", type=Path, required=True)
    parser.add_argument("--difficulty", type=Path, required=True)
    parser.add_argument("--stingray-root", type=Path, required=True)
    parser.add_argument("--ratio", type=int, default=5)
    parser.add_argument("--smd-bound", type=float, default=.1)
    parser.add_argument("--eligible-false-matching", type=Path,
                        help="Frozen matching CSV whose false IDs define common support")
    parser.add_argument("--output-dir", type=Path,
                        default=ROOT / "data/prematched_controls")
    args = parser.parse_args()
    tokenizers = [AutoTokenizer.from_pretrained(name, local_files_only=True) for name in
                  ("Qwen/Qwen3-8B", "google/gemma-3-12b-it")]
    false = false_features(args.stingray_root, tokenizers)
    difficulty = pd.read_csv(args.difficulty)
    false = false.merge(difficulty[difficulty.group == "false_friend"][["id",
        "reference_difficulty"]], on="id", validate="one_to_one")
    if args.eligible_false_matching:
        eligible = set(pd.read_csv(args.eligible_false_matching).false_id)
        false = false[false.id.isin(eligible)].copy()
    controls = pd.read_csv(args.shortlist).drop_duplicates(["group", "id"]).drop(
        columns=["false_id"], errors="ignore")
    controls = controls.merge(difficulty[difficulty.group != "false_friend"][["id", "group",
        "reference_difficulty"]], on=["id", "group"], validate="one_to_one")
    selected, balances = [], []
    for group in ("true_friend", "translation_control"):
        values, balance = select(false, controls[controls.group == group].reset_index(drop=True),
                                 args.ratio, args.smd_bound)
        selected.append(values); balance.insert(0, "group", group); balances.append(balance)
    reservoir, balance = pd.concat(selected), pd.concat(balances)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    reservoir.to_csv(args.output_dir / "private_validation_reservoir.csv", index=False)
    reservoir[["group", "id", "context_l1_id", "context_l2_id"]].rename(
        columns={"id": "control_id"}).to_csv(
            args.output_dir / "validation_reservoir_ids.csv", index=False)
    balance.to_csv(ROOT / "results/extensions/control_reservoir_balance.csv", index=False)
    manifest = {"status": "frozen_for_blind_human_validation", "ratio": args.ratio,
        "items_per_group": reservoir.groupby("group").size().to_dict(),
        "smd_bound": args.smd_bound, "exact_contextual_pos": True,
        "unique_forms_required": True, "target_models_read": False,
        "reference_model": "Qwen/Qwen2.5-7B-Instruct",
        "max_abs_smd": balance.groupby("group").smd.apply(lambda x: abs(x).max()).to_dict()}
    (args.output_dir / "validation_reservoir_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
