#!/usr/bin/env python3
"""Freeze balanced one-sided language-specific controls or validation reservoir."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import Bounds, LinearConstraint, linear_sum_assignment, milp
from scipy.sparse import csr_matrix
from transformers import AutoTokenizer

from build_language_specific_controls import COVARIATES as BASE, target_sides

ROOT = Path(__file__).resolve().parents[1]
COVARIATES = BASE + ["reference_difficulty"]


def select(target: pd.DataFrame, controls: pd.DataFrame, ratio: int, delta: float):
    combined = pd.concat([target, controls], ignore_index=True)
    scale = combined[COVARIATES].std().replace(0, 1)
    rows, lower, upper = [], [], []
    for pos, count in target.groupby("contextual_pos").size().items():
        rows.append((controls.contextual_pos == pos).astype(float).to_numpy())
        lower.append(ratio * count); upper.append(ratio * count)
    for column in COVARIATES:
        target_sum = ratio * target[column].sum()
        tolerance = ratio * len(target) * delta * scale[column]
        rows.append(controls[column].to_numpy(float))
        lower.append(target_sum - tolerance); upper.append(target_sum + tolerance)
    for column in COVARIATES:
        center = target[column].mean()
        t2 = (((target[column] - center) / scale[column]) ** 2).sum() * ratio
        c2 = ((controls[column] - center) / scale[column]) ** 2
        tolerance = ratio * len(target) * .25
        rows.append(c2.to_numpy(float)); lower.append(max(0, t2 - tolerance))
        upper.append(t2 + tolerance)
    nearest = []
    for _, control in controls.iterrows():
        same = target[target.contextual_pos == control.contextual_pos]
        gap = ((same[COVARIATES].to_numpy(float) -
                control[COVARIATES].to_numpy(float)) / scale.to_numpy(float))
        nearest.append((gap ** 2).sum(1).min())
    result = milp(c=np.asarray(nearest), integrality=np.ones(len(controls)),
        bounds=Bounds(0, 1), constraints=LinearConstraint(
            csr_matrix(np.vstack(rows)), lower, upper), options={"time_limit": 180})
    if not result.success:
        raise RuntimeError(result.message)
    selected = controls[np.rint(result.x).astype(bool)].copy()
    balance = pd.DataFrame([{"covariate": column,
        "target_mean": target[column].mean(), "control_mean": selected[column].mean(),
        "smd": (selected[column].mean()-target[column].mean())/scale[column],
        "target_sd": target[column].std(), "control_sd": selected[column].std(),
        "variance_ratio": selected[column].var()/target[column].var()
                          if target[column].var() else np.nan} for column in COVARIATES])
    return selected, balance, scale


def pair(target: pd.DataFrame, controls: pd.DataFrame, scale: pd.Series) -> pd.DataFrame:
    pairs = []
    for pos, left in target.groupby("contextual_pos"):
        right = controls[controls.contextual_pos == pos]
        gap = ((left[COVARIATES].to_numpy(float)[:, None, :] -
                right[COVARIATES].to_numpy(float)[None, :, :]) / scale.to_numpy(float))
        rows, cols = linear_sum_assignment((gap ** 2).sum(2))
        for i, j in zip(rows, cols):
            pairs.append({"false_id": left.iloc[i].false_id,
                "control_id": right.iloc[j].id, "pair_distance": (gap[i,j]**2).sum(),
                "max_standardized_gap": abs(gap[i,j]).max()})
    return pd.DataFrame(pairs)


def assign_foils(controls: pd.DataFrame) -> pd.DataFrame:
    """Freeze a distinct, length/difficulty-matched English foil without target outcomes."""
    controls = controls.copy().reset_index(drop=True)
    gap = (abs(controls.gloss_tokens.to_numpy(float)[:, None] -
               controls.gloss_tokens.to_numpy(float)[None, :]) +
           .1 * abs(controls.reference_difficulty.to_numpy(float)[:, None] -
                    controls.reference_difficulty.to_numpy(float)[None, :]))
    forbidden = (controls.meaning.to_numpy()[:, None] == controls.meaning.to_numpy()[None, :])
    gap[forbidden] = 1e6
    rows, cols = linear_sum_assignment(gap)
    if (gap[rows, cols] >= 1e6).any():
        raise RuntimeError("could not construct distinct language-specific foils")
    controls["foil_control_id"] = controls.iloc[cols].id.to_numpy()
    controls["foil_meaning"] = controls.iloc[cols].meaning.to_numpy()
    return controls


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shortlist", type=Path, required=True)
    parser.add_argument("--difficulty", type=Path, required=True)
    parser.add_argument("--stingray-root", type=Path, required=True)
    parser.add_argument("--eligible-false-matching", type=Path, required=True)
    parser.add_argument("--valid-controls", type=Path)
    parser.add_argument("--ratio", type=int, default=1)
    parser.add_argument("--smd-bound", type=float, default=.1)
    parser.add_argument("--output-dir", type=Path,
                        default=ROOT / "data/language_specific_controls")
    args = parser.parse_args()
    tokenizers = [AutoTokenizer.from_pretrained(name, local_files_only=True) for name in
                  ("Qwen/Qwen3-8B", "google/gemma-3-12b-it")]
    targets = target_sides(args.stingray_root, tokenizers, args.eligible_false_matching)
    difficulty = pd.read_csv(args.difficulty, dtype={"id": str})
    targets = targets.merge(difficulty[difficulty.group == "false_friend"][["id", "language",
        "reference_difficulty"]].rename(columns={"id":"false_id"}),
        on=["false_id","language"], validate="one_to_one")
    controls = pd.read_csv(args.shortlist).drop_duplicates(["group", "id"])
    controls = controls.merge(difficulty[difficulty.group != "false_friend"][["id", "group",
        "language", "reference_difficulty"]], on=["id","group","language"],
        validate="one_to_one")
    human_validation_complete = args.valid_controls is not None
    if args.valid_controls:
        valid = pd.read_csv(args.valid_controls, dtype=str)
        valid = valid[["control_id", "group"]].drop_duplicates().rename(
            columns={"control_id":"id"})
        controls.id = controls.id.astype(str)
        controls = controls.merge(valid, on=["id","group"], validate="many_to_one")
    supported = {language: set(controls[controls.language == language].contextual_pos)
                 for language in ("zh", "ja")}
    excluded = {language: sorted(targets[(targets.language == language) &
                                ~targets.contextual_pos.isin(supported[language])].false_id)
                for language in ("zh", "ja")}
    targets = targets[[pos in supported[language]
                       for language, pos in zip(targets.language, targets.contextual_pos)]]
    selections, balances, pairs = [], [], []
    for language in ("zh", "ja"):
        target = targets[targets.language == language].reset_index(drop=True)
        control = controls[controls.language == language].reset_index(drop=True)
        selected, balance, scale = select(target, control, args.ratio, args.smd_bound)
        balance.insert(0, "language", language); balances.append(balance)
        if args.ratio == 1:
            selected = assign_foils(selected)
        selections.append(selected)
        if args.ratio == 1:
            local_pairs = pair(target, selected, scale)
            local_pairs.insert(0, "group", f"language_specific_{language}")
            pairs.append(local_pairs)
    selected = pd.concat(selections); balance = pd.concat(balances)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    suffix = "final" if args.ratio == 1 else "validation_reservoir"
    selected.to_csv(args.output_dir / f"private_{suffix}.csv", index=False)
    selected[["group","id","context_id"]].rename(columns={"id":"control_id"}).to_csv(
        args.output_dir / f"{suffix}_ids.csv", index=False)
    if pairs:
        pd.concat(pairs).to_csv(args.output_dir / "frozen_final_matching.csv", index=False)
    default_output = ROOT / "data/language_specific_controls"
    balance_path = (ROOT / "results/extensions" / f"language_specific_{suffix}_balance.csv"
                    if args.output_dir.resolve() == default_output.resolve()
                    else args.output_dir / f"{suffix}_balance.csv")
    balance.to_csv(balance_path, index=False)
    manifest = {"status": "frozen_before_target_outcomes",
        "ratio": args.ratio, "items_per_language": selected.groupby("language").size().to_dict(),
        "smd_bound": args.smd_bound, "exact_contextual_pos": True,
        "reference_model": "Qwen/Qwen2.5-7B-Instruct", "target_models_read": False,
        "human_validation_complete": human_validation_complete,
        "excluded_false_ids_by_language": excluded,
        "max_abs_smd": balance.groupby("language").smd.apply(lambda x: abs(x).max()).to_dict(),
        "covariates": COVARIATES}
    (args.output_dir / f"{suffix}_manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
