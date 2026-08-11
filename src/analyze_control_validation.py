#!/usr/bin/env python3
"""Check two completed matched-control validation packets and freeze exclusions."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from analyze_bilingual_annotations import kappa

ROOT = Path(__file__).resolve().parents[1]
SEM = {"yes", "no", "uncertain"}
EQUIV = {"yes", "no", "partial", "uncertain"}
BLOCKING = {"WRONG_SENSE", "NOT_EQUIVALENT", "UNNATURAL", "POS_MISMATCH",
            "PROPER_NAME", "MULTIWORD_OR_SUBSTRING", "OTHER_BLOCKING"}


def load(path: Path, expected: int) -> pd.DataFrame:
    frame = pd.read_csv(path, dtype=str, keep_default_na=False)
    if len(frame) != expected or frame.annotation_id.nunique() != expected:
        raise ValueError(f"{path}: expected {expected} unique rows")
    rules = {"chinese_context_matches_meaning_yes_no_uncertain": SEM,
             "japanese_context_matches_meaning_yes_no_uncertain": SEM,
             "cross_language_meanings_equivalent_yes_no_partial_uncertain": EQUIV,
             "pos_comparable_yes_no_uncertain": SEM}
    for column, allowed in rules.items():
        invalid = set(frame[column].str.strip()) - allowed
        if invalid:
            raise ValueError(f"{path}:{column}: invalid/blank {sorted(invalid)}")
    for column in ("chinese_naturalness_1_to_5", "japanese_naturalness_1_to_5",
                   "confidence_1_to_5"):
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
        if frame[column].isna().any() or not frame[column].between(1, 5).all():
            raise ValueError(f"{path}:{column}: expected 1..5")
    frame["blocking"] = frame.confound_code.apply(
        lambda value: bool(BLOCKING & set(value.strip().split("+"))))
    return frame


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--annotator-1", type=Path, required=True)
    parser.add_argument("--annotator-2", type=Path, required=True)
    parser.add_argument("--key", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    key = pd.read_csv(args.key)
    expected = key.annotation_id.nunique()
    if key.groupby("annotator").annotation_id.nunique().nunique() != 1:
        raise ValueError("unblinding key has inconsistent annotator packet sizes")
    first, second = load(args.annotator_1, expected), load(args.annotator_2, expected)
    columns = ["annotation_id", "chinese_context_matches_meaning_yes_no_uncertain",
        "japanese_context_matches_meaning_yes_no_uncertain",
        "cross_language_meanings_equivalent_yes_no_partial_uncertain",
        "chinese_naturalness_1_to_5", "japanese_naturalness_1_to_5",
        "pos_comparable_yes_no_uncertain", "blocking"]
    paired = first[columns].merge(second[columns], on="annotation_id",
                                  suffixes=("_a", "_b"), validate="one_to_one")
    key_columns = ["annotation_id", "group", "control_id"]
    if "false_id" in key.columns:
        key_columns.append("false_id")
    paired = paired.merge(key.drop_duplicates("annotation_id")[key_columns],
                          on="annotation_id", validate="one_to_one")
    paired["retain_pre_adjudication"] = (
        (paired.chinese_context_matches_meaning_yes_no_uncertain_a == "yes") &
        (paired.chinese_context_matches_meaning_yes_no_uncertain_b == "yes") &
        (paired.japanese_context_matches_meaning_yes_no_uncertain_a == "yes") &
        (paired.japanese_context_matches_meaning_yes_no_uncertain_b == "yes") &
        (paired.cross_language_meanings_equivalent_yes_no_partial_uncertain_a == "yes") &
        (paired.cross_language_meanings_equivalent_yes_no_partial_uncertain_b == "yes") &
        (paired[["chinese_naturalness_1_to_5_a", "chinese_naturalness_1_to_5_b"]].mean(axis=1) >= 3) &
        (paired[["japanese_naturalness_1_to_5_a", "japanese_naturalness_1_to_5_b"]].mean(axis=1) >= 3) &
        (paired.pos_comparable_yes_no_uncertain_a != "no") &
        (paired.pos_comparable_yes_no_uncertain_b != "no") &
        ~paired.blocking_a & ~paired.blocking_b)
    metrics = {}
    for prefix in ("chinese_context_matches_meaning_yes_no_uncertain",
                   "japanese_context_matches_meaning_yes_no_uncertain",
                   "cross_language_meanings_equivalent_yes_no_partial_uncertain",
                   "pos_comparable_yes_no_uncertain"):
        metrics[f"{prefix}_kappa"] = kappa(paired[f"{prefix}_a"], paired[f"{prefix}_b"])
    metrics |= {"rows": len(paired),
        "retained": int(paired.retain_pre_adjudication.sum()),
        "retention_rate": float(paired.retain_pre_adjudication.mean()),
        "retained_by_group": paired.groupby("group").retain_pre_adjudication.sum().to_dict()}
    args.output_dir.mkdir(parents=True, exist_ok=True)
    paired.to_csv(args.output_dir / "private_control_validation_aligned.csv", index=False)
    paired.loc[paired.retain_pre_adjudication, ["control_id", "group"]].to_csv(
        args.output_dir / "private_valid_control_ids.csv", index=False)
    (args.output_dir / "control_validation_summary.json").write_text(json.dumps(metrics, indent=2) + "\n")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
