#!/usr/bin/env python3
"""Build two blinded full-coverage annotation packets for Doppelganger-JC.

The generated CSVs contain upstream licensed text and are intentionally written
under an ignored directory.  Only aggregate diagnostics are publishable here.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
from pathlib import Path

import pandas as pd

from evaluate_doppel_natural import load_pairs

ROOT = Path(__file__).resolve().parents[1]


def marked(row: dict) -> str:
    return row["sentence"].replace(row["source_word"], f'[[{row["source_word"]}]]', 1)


def stable_id(pair_id: str, direction: str) -> str:
    return hashlib.sha256(f"{pair_id}|{direction}".encode()).hexdigest()[:12]


def make_rows(pairs: list[dict], annotator: str, seed: int):
    rng = random.Random(seed)
    rows, key = [], []
    for pair in pairs:
        for direction in pair["directions"]:
            options = [("correct", direction["correct_option"]),
                       ("shortcut", direction["shortcut_option"])]
            rng.shuffle(options)
            annotation_id = stable_id(pair["id"], direction["direction"])
            rows.append({
                "annotation_id": annotation_id,
                "source_language": direction["source_language"],
                "output_language": direction["output_language"],
                "source_context": marked(direction),
                "option_A": options[0][1], "option_B": options[1][1],
                "A_expresses_intended_sense_yes_no_uncertain": "",
                "B_expresses_intended_sense_yes_no_uncertain": "",
                "A_naturalness_1_to_5": "", "B_naturalness_1_to_5": "",
                "same_grammatical_type_yes_no_uncertain": "",
                "preferred_A_B_tie_neither": "", "confound_code": "",
                "confidence_1_to_5": "", "comment_optional": "",
            })
            key.append({"annotation_id": annotation_id, "annotator": annotator,
                        "pair_id": pair["id"], "direction": direction["direction"],
                        "correct_label": "A" if options[0][0] == "correct" else "B"})
    rng.shuffle(rows)
    return rows, key


def diagnostics(pairs: list[dict]) -> pd.DataFrame:
    rows = []
    for pair in pairs:
        for item in pair["directions"]:
            a, b = item["correct_option"], item["shortcut_option"]
            rows.append({
                "direction": item["direction"], "single_character_either": min(len(a), len(b)) == 1,
                "length_ratio_gt_2": max(len(a), len(b)) / min(len(a), len(b)) > 2,
                "punctuation_either": any(not ch.isalnum() and not ch.isspace() for ch in a + b),
                "substring_relation": a in b or b in a,
                "full_translation_length_gap_gt_10": abs(len(item["correct_translation"]) -
                                                         len(item["shortcut_translation"])) > 10,
            })
    frame = pd.DataFrame(rows)
    output = []
    for direction, group in list(frame.groupby("direction")) + [("all", frame)]:
        output.append({"direction": direction, "n_rows": len(group)} |
                      {column: int(group[column].sum()) for column in frame.columns[1:]})
    return pd.DataFrame(output)


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path,
                        default=ROOT / "data/annotation_packets/doppel_full")
    args = parser.parse_args()
    pairs = load_pairs(args.data_root)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    keys = []
    for annotator, seed in (("annotator_1", 2026081301), ("annotator_2", 2026081302)):
        rows, key = make_rows(pairs, annotator, seed)
        write_csv(args.output_dir / f"{annotator}_blind.csv", rows)
        keys.extend(key)
    write_csv(args.output_dir / "private_unblinding_key.csv", keys)
    write_csv(args.output_dir / "adjudication_template.csv", [{
        "annotation_id": stable_id(pair["id"], row["direction"]),
        "adjudicated_valid_yes_no": "", "adjudicated_correct_label_A_B": "",
        "adjudication_note": "",
    } for pair in pairs for row in pair["directions"]])
    audit = diagnostics(pairs)
    audit.to_csv(ROOT / "results/extensions/doppel_option_automatic_audit.csv", index=False)
    manifest = {"paired_words": len(pairs), "rows_per_annotator": len(pairs) * 2,
                "annotators_required": 2, "blinding": "independent option order and row order",
                "human_validation_complete": False}
    (args.output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print(audit.to_string(index=False))
    print(f"wrote two blinded {len(pairs) * 2}-row packets to {args.output_dir}")


if __name__ == "__main__":
    main()
