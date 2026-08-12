#!/usr/bin/env python3
"""Fail closed unless both preregistered human measurement gates are satisfied."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def read_json(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"required human-stage artifact is missing: {path}")
    return json.loads(path.read_text())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--doppel-summary", type=Path, required=True)
    parser.add_argument("--control-summary", type=Path, required=True)
    parser.add_argument("--final-matching-manifest", type=Path, required=True)
    parser.add_argument("--language-specific-summary", type=Path, required=True)
    parser.add_argument("--language-specific-manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--minimum-false-items", type=int, default=20)
    parser.add_argument("--minimum-kappa", type=float, default=.60)
    parser.add_argument("--minimum-naturalness-icc", type=float, default=.50)
    args = parser.parse_args()

    doppel = read_json(args.doppel_summary)
    control = read_json(args.control_summary)
    matching = read_json(args.final_matching_manifest)
    language_specific = read_json(args.language_specific_summary)
    language_matching = read_json(args.language_specific_manifest)
    checks = {
        "doppel_all_708_rows_double_annotated": doppel.get("rows") == 708,
        "doppel_gold_semantic_reliability":
            doppel.get("gold_semantic_weighted_kappa", -1) >= args.minimum_kappa,
        "doppel_shortcut_semantic_reliability":
            doppel.get("shortcut_semantic_weighted_kappa", -1) >= args.minimum_kappa,
        "doppel_naturalness_reliability":
            doppel.get("naturalness_icc_2_1", -1) >= args.minimum_naturalness_icc,
        "control_all_192_candidates_double_annotated": control.get("rows") == 192,
        "control_chinese_sense_reliability":
            control.get("chinese_context_matches_meaning_yes_no_uncertain_kappa", -1)
            >= args.minimum_kappa,
        "control_japanese_sense_reliability":
            control.get("japanese_context_matches_meaning_yes_no_uncertain_kappa", -1)
            >= args.minimum_kappa,
        "controls_filtered_by_human_validation":
            matching.get("human_validation_complete") is True,
        "matched_false_friend_sample_large_enough":
            matching.get("false_items", 0) >= args.minimum_false_items,
        "true_friend_balance":
            matching.get("max_abs_smd", {}).get("true_friend", 1) <= .10,
        "translation_control_balance":
            matching.get("max_abs_smd", {}).get("translation_control", 1) <= .10,
        "target_outcomes_unseen_at_freeze": matching.get("target_models_read") is False,
        "language_specific_all_188_candidates_double_annotated":
            language_specific.get("rows") == 188,
        "language_specific_word_validity_reliability":
            language_specific.get("word_is_valid_in_named_language_yes_no_uncertain_kappa", -1)
            >= args.minimum_kappa,
        "language_specific_context_reliability":
            language_specific.get("context_matches_meaning_yes_no_uncertain_kappa", -1)
            >= args.minimum_kappa,
        "language_specific_controls_filtered_by_humans":
            language_matching.get("human_validation_complete") is True,
        "language_specific_sample_large_enough":
            min(language_matching.get("items_per_language", {}).values(), default=0)
            >= args.minimum_false_items,
        "language_specific_zh_balance":
            language_matching.get("max_abs_smd", {}).get("zh", 1) <= .10,
        "language_specific_ja_balance":
            language_matching.get("max_abs_smd", {}).get("ja", 1) <= .10,
        "language_specific_target_outcomes_unseen_at_freeze":
            language_matching.get("target_models_read") is False,
    }
    result = {
        "status": "UNLOCKED" if all(checks.values()) else "BLOCKED",
        "target_confirmatory_analysis_allowed": all(checks.values()),
        "checks": checks,
        "failed_checks": [name for name, passed in checks.items() if not passed],
        "thresholds": {"minimum_false_items": args.minimum_false_items,
                       "minimum_kappa": args.minimum_kappa,
                       "minimum_naturalness_icc": args.minimum_naturalness_icc,
                       "maximum_abs_smd": .10},
    }
    rendered = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered)
    print(rendered, end="")
    if not all(checks.values()):
        raise SystemExit(2)


if __name__ == "__main__":
    main()
