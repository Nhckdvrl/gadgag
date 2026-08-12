#!/usr/bin/env python3
"""Create blind validation packets for one-sided language-specific controls."""
from __future__ import annotations

import argparse
import hashlib
import json
import random
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--controls", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path,
        default=ROOT / "data/annotation_packets/language_specific_controls")
    args = parser.parse_args()
    controls = pd.read_csv(args.controls, dtype=str).drop_duplicates(["group","id"])
    args.output_dir.mkdir(parents=True, exist_ok=True)
    keys=[]
    for annotator, seed in (("annotator_1",2026081901),("annotator_2",2026081902)):
        rows=[]
        for _, value in controls.iterrows():
            aid=hashlib.sha256(f"{value.group}|{value.id}".encode()).hexdigest()[:12]
            rows.append({"annotation_id":aid,"language":value.language,
                "word":value.word,"context":value.context,"proposed_english_meaning":value.meaning,
                "word_is_valid_in_named_language_yes_no_uncertain":"",
                "context_matches_meaning_yes_no_uncertain":"",
                "context_naturalness_1_to_5":"","contextual_pos":value.contextual_pos,
                "pos_correct_yes_no_uncertain":"","confound_code":"",
                "confidence_1_to_5":"","comment_optional":""})
            keys.append({"annotation_id":aid,"annotator":annotator,
                         "group":value.group,"control_id":value.id})
        random.Random(seed).shuffle(rows)
        pd.DataFrame(rows).to_csv(args.output_dir/f"{annotator}_blind.csv",index=False)
    pd.DataFrame(keys).to_csv(args.output_dir/"private_unblinding_key.csv",index=False)
    manifest={"rows_per_annotator":len(controls),"annotators_required":2,
        "preferred_profiles":["native Chinese + advanced Japanese",
                              "native Japanese + advanced Chinese"],
        "model_results_visible":False,"human_validation_complete":False}
    (args.output_dir/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
    print(json.dumps(manifest,indent=2))


if __name__=="__main__": main()
