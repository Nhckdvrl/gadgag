#!/usr/bin/env python3
"""Score one-sided target/control difficulty using a design-only reference model."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from build_language_specific_controls import target_sides
from score_reference_difficulty import prompt
from scoring_v2 import prepare_chat_messages, score_prepared

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shortlist", type=Path, required=True)
    parser.add_argument("--stingray-root", type=Path, required=True)
    parser.add_argument("--eligible-false-matching", type=Path, required=True)
    parser.add_argument("--model", default="Qwen/Qwen2.5-7B-Instruct")
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--output", type=Path,
                        default=ROOT / "data/language_specific_controls/reference_difficulty.csv")
    args = parser.parse_args()
    tokenizer = AutoTokenizer.from_pretrained(args.model, local_files_only=True)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(args.model, local_files_only=True,
        dtype=torch.bfloat16, device_map={"": 0}, attn_implementation="sdpa").eval()
    feature_tokenizers = [AutoTokenizer.from_pretrained(name, local_files_only=True) for name in
                          ("Qwen/Qwen3-8B", "google/gemma-3-12b-it")]
    targets = target_sides(args.stingray_root, feature_tokenizers,
                           args.eligible_false_matching)
    controls = pd.read_csv(args.shortlist).drop_duplicates(["group", "id"])
    requests, rows = [], []
    names = {"zh": "Chinese", "ja": "Japanese"}
    for _, value in targets.iterrows():
        requests.append(prepare_chat_messages(tokenizer,
            prompt(names[value.language], value.word, value.context), value.meaning))
        rows.append({"id": value.false_id, "group": "false_friend",
                     "language": value.language})
    for _, value in controls.iterrows():
        requests.append(prepare_chat_messages(tokenizer,
            prompt(names[value.language], value.word, value.context), value.meaning))
        rows.append({"id": value.id, "group": value.group, "language": value.language})
    scores = score_prepared(model, tokenizer, requests, args.batch_size)
    result = pd.DataFrame([row | {"reference_difficulty": score.mean_logp}
                           for row, score in zip(rows, scores)])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(args.output, index=False)
    manifest = {"model": args.model, "role": "design-only one-sided difficulty",
                "target_outcomes_read": False, "items": len(result)}
    args.output.with_suffix(".manifest.json").write_text(json.dumps(manifest, indent=2)+"\n")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
