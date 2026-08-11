#!/usr/bin/env python3
"""Freeze a model-blind K-nearest control reservoir before difficulty scoring."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from transformers import AutoTokenizer

from build_prematched_controls import false_features

ROOT = Path(__file__).resolve().parents[1]
COVARIATES = ["freq_l1", "freq_l2", "freq_ratio", "char_l1", "char_l2",
              "gloss_tokens", "tok1_l1", "tok1_l2", "tok2_l1", "tok2_l2"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pool", type=Path, required=True)
    parser.add_argument("--stingray-root", type=Path, required=True)
    parser.add_argument("--neighbors", type=int, default=20)
    parser.add_argument("--output-dir", type=Path,
                        default=ROOT / "data/prematched_controls")
    args = parser.parse_args()
    tokenizers = [AutoTokenizer.from_pretrained(name, local_files_only=True) for name in
                  ("Qwen/Qwen3-8B", "google/gemma-3-12b-it")]
    false = false_features(args.stingray_root, tokenizers)
    pool = pd.read_csv(args.pool)
    # The confirmatory FF estimand is the intersection of POS strata supported
    # by both control families, fixed before reference or target-model scoring.
    support = None
    for group in ("true_friend", "translation_control"):
        local = pool[(pool.group == group) & (pool.freq_l1 >= 2) & (pool.freq_l2 >= 2)]
        values = set(zip(local.pos_l1_context, local.pos_l2_context))
        support = values if support is None else support & values
    retained_false = false[[(a, b) in support for a, b in zip(false.pos_l1, false.pos_l2)]].copy()
    rows = []
    for group in ("true_friend", "translation_control"):
        local = pool[(pool.group == group) & (pool.freq_l1 >= 2) &
                     (pool.freq_l2 >= 2)].copy()
        combined = pd.concat([retained_false, local], ignore_index=True)
        scale = combined[COVARIATES].std().replace(0, 1)
        for _, target in retained_false.iterrows():
            eligible = local[(local.pos_l1_context == target.pos_l1) &
                             (local.pos_l2_context == target.pos_l2)].copy()
            gaps = (eligible[COVARIATES].to_numpy(float) -
                    target[COVARIATES].to_numpy(float)) / scale.to_numpy(float)
            eligible["design_distance"] = (gaps ** 2).sum(1)
            eligible["max_standardized_gap"] = np.abs(gaps).max(1)
            for _, control in eligible.nsmallest(args.neighbors, "design_distance").iterrows():
                rows.append({"false_id": target.id, "group": group} | control.to_dict())
    shortlist = pd.DataFrame(rows)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    shortlist.to_csv(args.output_dir / "private_control_shortlist.csv", index=False)
    shortlist[["false_id", "group", "id", "design_distance",
               "max_standardized_gap"]].rename(columns={"id": "control_id"}).to_csv(
                   args.output_dir / "control_shortlist_ids.csv", index=False)
    manifest = {"design_stage": "outcome-blind lexical shortlist",
        "false_total": len(false), "false_common_pos_support": len(retained_false),
        "excluded_false_ids": sorted(set(false.id) - set(retained_false.id)),
        "neighbors_per_false_per_group": args.neighbors, "covariates": COVARIATES,
        "target_models_read": False, "rows": len(shortlist),
        "unique_controls": shortlist.groupby("group").id.nunique().to_dict()}
    (args.output_dir / "shortlist_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
