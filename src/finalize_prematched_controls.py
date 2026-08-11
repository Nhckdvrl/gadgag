#!/usr/bin/env python3
"""Freeze 1:1 controls with exact contextual POS and explicit mean balance."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import Bounds, LinearConstraint, linear_sum_assignment, milp
from scipy.sparse import csr_matrix
from transformers import AutoTokenizer

from build_prematched_controls import false_features

ROOT = Path(__file__).resolve().parents[1]
BASE = ["freq_l1", "freq_l2", "freq_ratio", "char_l1", "char_l2",
        "gloss_tokens", "tok1_l1", "tok1_l2", "tok2_l1", "tok2_l2"]
COVARIATES = BASE + ["reference_difficulty"]


def select_controls(false: pd.DataFrame, controls: pd.DataFrame, delta: float):
    combined = pd.concat([false, controls], ignore_index=True)
    target_mean = false[COVARIATES].mean()
    scale = combined[COVARIATES].std().replace(0, 1)
    rows, lower, upper = [], [], []
    for pos, count in false.groupby(["pos_l1", "pos_l2"]).size().items():
        rows.append(((controls.pos_l1_context == pos[0]) &
                     (controls.pos_l2_context == pos[1])).astype(float).to_numpy())
        lower.append(count); upper.append(count)
    for column in COVARIATES:
        rows.append(controls[column].to_numpy(float))
        lower.append(len(false) * (target_mean[column] - delta * scale[column]))
        upper.append(len(false) * (target_mean[column] + delta * scale[column]))
    # Keep dispersion from collapsing even when means are balanced.
    for column in COVARIATES:
        squared = ((controls[column] - target_mean[column]) / scale[column]) ** 2
        target = (((false[column] - target_mean[column]) / scale[column]) ** 2).mean()
        rows.append(squared.to_numpy(float))
        lower.append(len(false) * max(0, target - .25))
        upper.append(len(false) * (target + .25))
    # No repeated Chinese or Japanese control form.
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
        bounds=Bounds(0, 1),
        constraints=LinearConstraint(csr_matrix(np.vstack(rows)), lower, upper),
        options={"time_limit": 120})
    if not result.success:
        raise RuntimeError(f"pre-matching infeasible at SMD delta={delta}: {result.message}")
    selected = controls[np.rint(result.x).astype(bool)].copy()
    balance = []
    for column in COVARIATES:
        balance.append({"covariate": column,
            "false_mean": false[column].mean(), "control_mean": selected[column].mean(),
            "smd": (selected[column].mean() - false[column].mean()) / scale[column],
            "false_sd": false[column].std(), "control_sd": selected[column].std(),
            "variance_ratio": selected[column].var() / false[column].var()
                              if false[column].var() else np.nan})
    return selected, pd.DataFrame(balance), scale


def pair_controls(false: pd.DataFrame, selected: pd.DataFrame, scale: pd.Series,
                  group: str) -> pd.DataFrame:
    pairs = []
    for pos, left in false.groupby(["pos_l1", "pos_l2"]):
        right = selected[(selected.pos_l1_context == pos[0]) &
                         (selected.pos_l2_context == pos[1])]
        gap = (left[COVARIATES].to_numpy(float)[:, None, :] -
               right[COVARIATES].to_numpy(float)[None, :, :]) / scale.to_numpy(float)
        distance = (gap ** 2).sum(2)
        rows, cols = linear_sum_assignment(distance)
        for i, j in zip(rows, cols):
            pairs.append({"group": group, "false_id": left.iloc[i].id,
                          "control_id": right.iloc[j].id,
                          "pair_distance": distance[i, j],
                          "max_standardized_gap": np.abs(gap[i, j]).max()})
    return pd.DataFrame(pairs)


def joint_cardinality(false: pd.DataFrame, true: pd.DataFrame,
                      translation: pd.DataFrame, delta: float):
    """Maximize a shared FF subset under balance against both control groups."""
    groups = {"true_friend": true.reset_index(drop=True),
              "translation_control": translation.reset_index(drop=True)}
    offsets = {"false_friend": 0, "true_friend": len(false),
               "translation_control": len(false) + len(true)}
    width = len(false) + len(true) + len(translation)
    rows, lower, upper = [], [], []
    positions = sorted(set(zip(false.pos_l1, false.pos_l2)))
    for name, controls in groups.items():
        offset = offsets[name]
        for pos in positions:
            vector = np.zeros(width)
            vector[:len(false)] = ((false.pos_l1 == pos[0]) &
                                   (false.pos_l2 == pos[1])).astype(float)
            vector[offset:offset + len(controls)] = -(
                (controls.pos_l1_context == pos[0]) &
                (controls.pos_l2_context == pos[1])).astype(float)
            rows.append(vector); lower.append(0); upper.append(0)
    scales = {}
    for name, controls in groups.items():
        offset = offsets[name]
        scale = pd.concat([false, controls])[COVARIATES].std().replace(0, 1)
        scales[name] = scale
        for column in COVARIATES:
            # |sum(control*x)-sum(false*x)| <= delta*sd*n_false
            for sign in (1, -1):
                vector = np.zeros(width)
                vector[:len(false)] = sign * (-false[column].to_numpy(float)) - delta * scale[column]
                vector[offset:offset + len(controls)] = sign * controls[column].to_numpy(float)
                rows.append(vector); lower.append(-np.inf); upper.append(0)
        # A looser second-moment constraint prevents variance collapse.
        center = false[COVARIATES].mean()
        for column in COVARIATES:
            f2 = ((false[column] - center[column]) / scale[column]) ** 2
            c2 = ((controls[column] - center[column]) / scale[column]) ** 2
            for sign in (1, -1):
                vector = np.zeros(width)
                vector[:len(false)] = sign * (-f2.to_numpy(float)) - .25
                vector[offset:offset + len(controls)] = sign * c2.to_numpy(float)
                rows.append(vector); lower.append(-np.inf); upper.append(0)
        for column in ("word_l1", "word_l2"):
            for _, indices in controls.groupby(column).groups.items():
                if len(indices) > 1:
                    vector = np.zeros(width)
                    vector[offset + np.asarray(list(indices))] = 1
                    rows.append(vector); lower.append(0); upper.append(1)
    objective = np.zeros(width)
    objective[:len(false)] = -1  # maximize retained FFs
    result = milp(c=objective, integrality=np.ones(width), bounds=Bounds(0, 1),
        constraints=LinearConstraint(csr_matrix(np.vstack(rows)), lower, upper),
        options={"time_limit": 180})
    if not result.success:
        raise RuntimeError(f"joint cardinality matching failed: {result.message}")
    chosen = np.rint(result.x).astype(bool)
    selected_false = false[chosen[:len(false)]].copy()
    selected = {}
    for name, controls in groups.items():
        offset = offsets[name]
        selected[name] = controls[chosen[offset:offset + len(controls)]].copy()
    return selected_false, selected, scales


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shortlist", type=Path, required=True)
    parser.add_argument("--difficulty", type=Path, required=True)
    parser.add_argument("--stingray-root", type=Path, required=True)
    parser.add_argument("--smd-bound", type=float, default=.1)
    parser.add_argument("--valid-controls", type=Path,
                        help="Human-validated CSV with control_id and group; when set, all "
                             "other controls are excluded before final matching.")
    parser.add_argument("--minimum-false-items", type=int, default=20)
    parser.add_argument("--output-dir", type=Path,
                        default=ROOT / "data/prematched_controls")
    args = parser.parse_args()
    tokenizers = [AutoTokenizer.from_pretrained(name, local_files_only=True) for name in
                  ("Qwen/Qwen3-8B", "google/gemma-3-12b-it")]
    false = false_features(args.stingray_root, tokenizers)
    difficulty = pd.read_csv(args.difficulty)
    false = false.merge(difficulty[difficulty.group == "false_friend"][["id",
        "reference_difficulty"]], on="id", validate="one_to_one")
    shortlist = pd.read_csv(args.shortlist).drop_duplicates(["group", "id"])
    shortlist = shortlist.drop(columns=["false_id"], errors="ignore")
    controls = shortlist.merge(difficulty[difficulty.group != "false_friend"][["id", "group",
        "reference_difficulty"]], on=["id", "group"], validate="one_to_one")
    human_validation_complete = args.valid_controls is not None
    if args.valid_controls:
        valid = pd.read_csv(args.valid_controls, dtype=str)
        if not {"control_id", "group"}.issubset(valid.columns):
            raise ValueError("--valid-controls requires control_id and group columns")
        valid = valid[["control_id", "group"]].drop_duplicates().rename(
            columns={"control_id": "id"})
        controls["id"] = controls.id.astype(str)
        controls = controls.merge(valid, on=["id", "group"], validate="many_to_one")
    selected_false, selected_groups, scales = joint_cardinality(
        false, controls[controls.group == "true_friend"],
        controls[controls.group == "translation_control"], args.smd_bound)
    if human_validation_complete and len(selected_false) < args.minimum_false_items:
        raise RuntimeError(
            f"STOP: only {len(selected_false)} false friends remain after human validation; "
            f"the preregistered minimum is {args.minimum_false_items}")
    all_pairs, balances, selected_frames = [], [], []
    for group in ("true_friend", "translation_control"):
        selected, scale = selected_groups[group], scales[group]
        all_pairs.append(pair_controls(selected_false, selected, scale, group))
        balance = []
        for column in COVARIATES:
            balance.append({"covariate": column,
                "false_mean": selected_false[column].mean(),
                "control_mean": selected[column].mean(),
                "smd": (selected[column].mean() - selected_false[column].mean()) / scale[column],
                "false_sd": selected_false[column].std(), "control_sd": selected[column].std(),
                "variance_ratio": selected[column].var() / selected_false[column].var()
                                  if selected_false[column].var() else np.nan})
        balance = pd.DataFrame(balance)
        balance.insert(0, "group", group); balances.append(balance)
        selected_frames.append(selected)
    pairs, balance = pd.concat(all_pairs), pd.concat(balances)
    selected = pd.concat(selected_frames)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    selected.merge(pairs, left_on=["group", "id"], right_on=["group", "control_id"],
                   validate="one_to_one").to_csv(
                       args.output_dir / "private_final_controls.csv", index=False)
    pairs.to_csv(args.output_dir / "frozen_final_matching.csv", index=False)
    balance.to_csv(ROOT / "results/extensions/prematched_final_balance.csv", index=False)
    manifest = {"status": "frozen_before_target_outcomes",
        "false_available": len(false), "false_items": len(selected_false),
        "excluded_false_ids": sorted(set(false.id) - set(selected_false.id)),
        "controls_per_group": pairs.groupby("group").size().to_dict(),
        "exact_contextual_pos": True, "smd_bound": args.smd_bound,
        "dispersion_bound_squared_z_mean": .25, "unique_forms_required": True,
        "reference_model": "Qwen/Qwen2.5-7B-Instruct", "target_models_read": False,
        "human_validation_complete": human_validation_complete,
        "minimum_false_items": args.minimum_false_items,
        "covariates": COVARIATES,
        "max_abs_smd": balance.groupby("group").smd.apply(lambda x: abs(x).max()).to_dict()}
    (args.output_dir / "final_matching_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest, indent=2)); print(balance.to_string(index=False))


if __name__ == "__main__":
    main()
