#!/usr/bin/env python3
"""Validate, unblind, and summarize two completed bilingual annotation packets."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parents[1]
SEMANTIC = {"yes", "no", "uncertain"}
PREFERRED = {"A", "B", "tie", "neither"}
GRAMMAR = {"yes", "no", "uncertain"}
BLOCKING = {"MULTI_DIFF", "BOTH_VALID", "NEITHER_VALID"}


def normalized(value) -> str:
    return str(value).strip()


def kappa(left, right, ordered: list[str] | None = None) -> float:
    labels = ordered or sorted(set(left) | set(right))
    index = {label: i for i, label in enumerate(labels)}
    matrix = np.zeros((len(labels), len(labels)))
    for a, b in zip(left, right):
        matrix[index[a], index[b]] += 1
    matrix /= matrix.sum()
    if ordered:
        width = max(1, len(labels) - 1)
        weights = np.fromfunction(lambda i, j: ((i - j) / width) ** 2,
                                  (len(labels), len(labels)))
        observed = (weights * matrix).sum()
        expected = (weights * np.outer(matrix.sum(1), matrix.sum(0))).sum()
        return 1 - observed / expected if expected else 1.0
    observed = np.trace(matrix)
    expected = (matrix.sum(1) * matrix.sum(0)).sum()
    return (observed - expected) / (1 - expected) if expected < 1 else 1.0


def icc_2_1(values: np.ndarray) -> float:
    """Two-way random, absolute-agreement, single-rater ICC(2,1)."""
    n, k = values.shape
    grand = values.mean()
    ms_rows = k * ((values.mean(1) - grand) ** 2).sum() / (n - 1)
    ms_cols = n * ((values.mean(0) - grand) ** 2).sum() / (k - 1)
    residual = values - values.mean(1, keepdims=True) - values.mean(0, keepdims=True) + grand
    ms_error = (residual ** 2).sum() / ((n - 1) * (k - 1))
    denominator = ms_rows + (k - 1) * ms_error + k * (ms_cols - ms_error) / n
    return (ms_rows - ms_error) / denominator if denominator else np.nan


def validate_packet(path: Path, expected_rows: int) -> pd.DataFrame:
    frame = pd.read_csv(path, dtype=str, keep_default_na=False)
    if len(frame) != expected_rows or frame.annotation_id.nunique() != expected_rows:
        raise ValueError(f"{path}: expected {expected_rows} unique rows, got {len(frame)}")
    fields = {
        "A_expresses_intended_sense_yes_no_uncertain": SEMANTIC,
        "B_expresses_intended_sense_yes_no_uncertain": SEMANTIC,
        "same_grammatical_type_yes_no_uncertain": GRAMMAR,
        "preferred_A_B_tie_neither": PREFERRED,
    }
    for column, allowed in fields.items():
        invalid = set(map(normalized, frame[column])) - allowed
        if invalid:
            raise ValueError(f"{path}:{column}: invalid or blank values {sorted(invalid)}")
    for column in ("A_naturalness_1_to_5", "B_naturalness_1_to_5", "confidence_1_to_5"):
        values = pd.to_numeric(frame[column], errors="coerce")
        if values.isna().any() or not values.between(1, 5).all():
            raise ValueError(f"{path}:{column}: every row must contain an integer 1..5")
        frame[column] = values.astype(int)
    return frame


def align(frame: pd.DataFrame, key: pd.DataFrame, annotator: str) -> pd.DataFrame:
    local_key = key[key.annotator == annotator]
    merged = frame.merge(local_key, on="annotation_id", validate="one_to_one")
    correct_a = merged.correct_label == "A"
    merged["gold_semantic"] = np.where(correct_a,
        merged.A_expresses_intended_sense_yes_no_uncertain,
        merged.B_expresses_intended_sense_yes_no_uncertain)
    merged["shortcut_semantic"] = np.where(correct_a,
        merged.B_expresses_intended_sense_yes_no_uncertain,
        merged.A_expresses_intended_sense_yes_no_uncertain)
    merged["gold_naturalness"] = np.where(correct_a, merged.A_naturalness_1_to_5,
                                           merged.B_naturalness_1_to_5)
    merged["shortcut_naturalness"] = np.where(correct_a, merged.B_naturalness_1_to_5,
                                               merged.A_naturalness_1_to_5)
    merged["preferred_aligned"] = merged.preferred_A_B_tie_neither
    merged.loc[(merged.preferred_A_B_tie_neither == "A") & correct_a, "preferred_aligned"] = "gold"
    merged.loc[(merged.preferred_A_B_tie_neither == "B") & ~correct_a, "preferred_aligned"] = "gold"
    merged.loc[(merged.preferred_A_B_tie_neither == "B") & correct_a, "preferred_aligned"] = "shortcut"
    merged.loc[(merged.preferred_A_B_tie_neither == "A") & ~correct_a, "preferred_aligned"] = "shortcut"
    merged["blocking_confound"] = merged.confound_code.apply(
        lambda value: bool(BLOCKING & set(normalized(value).split("+"))))
    return merged


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--annotator-1", type=Path, required=True)
    parser.add_argument("--annotator-2", type=Path, required=True)
    parser.add_argument("--key", type=Path, required=True)
    parser.add_argument("--expected-rows", type=int, default=708)
    parser.add_argument("--output-dir", type=Path,
                        default=ROOT / "data/annotation_packets/doppel_full/analysis")
    args = parser.parse_args()
    key = pd.read_csv(args.key, dtype=str)
    first = align(validate_packet(args.annotator_1, args.expected_rows), key, "annotator_1")
    second = align(validate_packet(args.annotator_2, args.expected_rows), key, "annotator_2")
    columns = ["annotation_id", "pair_id", "direction", "gold_semantic",
               "shortcut_semantic", "gold_naturalness", "shortcut_naturalness",
               "same_grammatical_type_yes_no_uncertain", "preferred_aligned",
               "blocking_confound", "confound_code"]
    paired = first[columns].merge(second[columns], on=["annotation_id", "pair_id", "direction"],
                                  suffixes=("_a", "_b"), validate="one_to_one")
    paired["retain_pre_adjudication"] = (
        (paired.gold_semantic_a == "yes") & (paired.gold_semantic_b == "yes") &
        ((paired.shortcut_semantic_a == "no") | (paired.shortcut_semantic_b == "no")) &
        (paired.shortcut_semantic_a != "yes") & (paired.shortcut_semantic_b != "yes") &
        (paired[["gold_naturalness_a", "gold_naturalness_b"]].mean(axis=1) >= 3) &
        (paired[["shortcut_naturalness_a", "shortcut_naturalness_b"]].mean(axis=1) >= 3) &
        (paired.same_grammatical_type_yes_no_uncertain_a != "no") &
        (paired.same_grammatical_type_yes_no_uncertain_b != "no") &
        ~paired.blocking_confound_a & ~paired.blocking_confound_b)
    natural = np.stack([
        pd.concat([paired.gold_naturalness_a, paired.shortcut_naturalness_a]).to_numpy(float),
        pd.concat([paired.gold_naturalness_b, paired.shortcut_naturalness_b]).to_numpy(float)], 1)
    summary = {
        "rows": len(paired),
        "preferred_raw_agreement": float((paired.preferred_aligned_a == paired.preferred_aligned_b).mean()),
        "preferred_cohen_kappa": kappa(paired.preferred_aligned_a, paired.preferred_aligned_b),
        "gold_semantic_weighted_kappa": kappa(paired.gold_semantic_a, paired.gold_semantic_b,
                                                ["no", "uncertain", "yes"]),
        "shortcut_semantic_weighted_kappa": kappa(paired.shortcut_semantic_a,
                                                    paired.shortcut_semantic_b,
                                                    ["no", "uncertain", "yes"]),
        "naturalness_icc_2_1": float(icc_2_1(natural)),
        "naturalness_spearman": float(spearmanr(natural[:, 0], natural[:, 1]).statistic),
        "retained_pre_adjudication": int(paired.retain_pre_adjudication.sum()),
        "retention_rate": float(paired.retain_pre_adjudication.mean()),
        "retained_by_direction": paired.groupby("direction").retain_pre_adjudication.sum().to_dict(),
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    paired.to_csv(args.output_dir / "private_aligned_annotations.csv", index=False)
    (args.output_dir / "annotation_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
