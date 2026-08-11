#!/usr/bin/env python3
"""Create two blind bilingual validation packets for frozen matched controls."""
from __future__ import annotations

import argparse
import hashlib
import json
import random
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def anon_id(group: str, control_id: str) -> str:
    return hashlib.sha256(f"{group}|{control_id}".encode()).hexdigest()[:12]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--controls", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path,
                        default=ROOT / "data/annotation_packets/prematched_controls")
    args = parser.parse_args()
    controls = pd.read_csv(args.controls)
    id_column = "control_id" if "control_id" in controls.columns else "id"
    required = {"group", id_column, "word_l1", "word_l2", "context_l1",
                "context_l2", "meaning"}
    missing = required - set(controls.columns)
    if missing:
        raise ValueError(f"{args.controls}: missing columns {sorted(missing)}")
    if controls.duplicated(["group", id_column]).any():
        raise ValueError("control validation inputs must be unique by group and ID")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    key_rows = []
    for annotator, seed in (("annotator_1", 2026081401), ("annotator_2", 2026081402)):
        rng = random.Random(seed); rows = []
        for _, value in controls.iterrows():
            control_id = str(value[id_column])
            annotation_id = anon_id(value.group, control_id)
            rows.append({"annotation_id": annotation_id,
                "chinese_word": value.word_l1, "chinese_context": value.context_l1,
                "japanese_word": value.word_l2, "japanese_context": value.context_l2,
                "proposed_english_meaning": value.meaning,
                "chinese_context_matches_meaning_yes_no_uncertain": "",
                "japanese_context_matches_meaning_yes_no_uncertain": "",
                "cross_language_meanings_equivalent_yes_no_partial_uncertain": "",
                "chinese_naturalness_1_to_5": "", "japanese_naturalness_1_to_5": "",
                "pos_comparable_yes_no_uncertain": "", "confound_code": "",
                "confidence_1_to_5": "", "comment_optional": ""})
            key_rows.append({"annotation_id": annotation_id, "annotator": annotator,
                             "group": value.group, "control_id": control_id,
                             "false_id": value.get("false_id", "")})
        rng.shuffle(rows)
        pd.DataFrame(rows).to_csv(args.output_dir / f"{annotator}_blind.csv", index=False)
    pd.DataFrame(key_rows).to_csv(args.output_dir / "private_unblinding_key.csv", index=False)
    manifest = {"rows_per_annotator": len(controls), "annotators_required": 2,
        "candidate_ratio_per_group": int(len(controls) / controls.group.nunique() / 24)
                                     if len(controls) % 48 == 0 else None,
        "preferred_profiles": ["native Chinese + advanced Japanese",
                               "native Japanese + advanced Chinese"],
        "model_results_visible": False, "human_validation_complete": False}
    (args.output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
