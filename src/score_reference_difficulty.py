#!/usr/bin/env python3
"""Measure a frozen design-only reference difficulty for prematching.

Qwen2.5 is used only as a pre-outcome matching covariate and is excluded from
the subsequent target-component treatment-effect analysis.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from build_prematched_controls import false_features
from scoring_v2 import prepare_chat_messages, score_prepared

ROOT = Path(__file__).resolve().parents[1]


def prompt(language: str, target: str, context: str):
    return [{"role": "user", "content":
        f'The following context is in {language}. Determine the contextual meaning of '
        f'"{target}". Give the English meaning only.\nContext: {context}\nMeaning:'}]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shortlist", type=Path, required=True)
    parser.add_argument("--stingray-root", type=Path, required=True)
    parser.add_argument("--model", default="Qwen/Qwen2.5-7B-Instruct")
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--output", type=Path,
                        default=ROOT / "data/prematched_controls/reference_difficulty.csv")
    args = parser.parse_args()
    tokenizer = AutoTokenizer.from_pretrained(args.model, local_files_only=True)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(args.model, local_files_only=True,
        dtype=torch.bfloat16, device_map={"": 0}, attn_implementation="sdpa").eval()
    feature_tokenizers = [AutoTokenizer.from_pretrained(name, local_files_only=True) for name in
                          ("Qwen/Qwen3-8B", "google/gemma-3-12b-it")]
    false = false_features(args.stingray_root, feature_tokenizers)
    controls = pd.read_csv(args.shortlist).drop_duplicates(["group", "id"])
    requests, metadata = [], []
    for _, row in false.iterrows():
        for language, word, context, meaning in (
            ("Chinese", row.word_l1, row.context_l1, row.meaning_l1),
            ("Japanese", row.word_l2, row.context_l2, row.meaning_l2)):
            requests.append(prepare_chat_messages(tokenizer, prompt(language, word, context), meaning))
            metadata.append({"id": row.id, "group": "false_friend", "language": language})
    for _, row in controls.iterrows():
        for language, word, context in (
            ("Chinese", row.word_l1, row.context_l1),
            ("Japanese", row.word_l2, row.context_l2)):
            requests.append(prepare_chat_messages(tokenizer, prompt(language, word, context), row.meaning))
            metadata.append({"id": row.id, "group": row.group, "language": language})
    scores = score_prepared(model, tokenizer, requests, args.batch_size)
    result = pd.DataFrame([value | {"mean_logp": score.mean_logp,
                                    "n_tokens": score.n_tokens}
                           for value, score in zip(metadata, scores)])
    aggregate = result.groupby(["id", "group"]).mean_logp.mean().rename(
        "reference_difficulty").reset_index()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    aggregate.to_csv(args.output, index=False)
    manifest = {"model": args.model, "role": "design-only reference covariate",
                "target_outcomes_read": False, "items": len(aggregate)}
    args.output.with_suffix(".manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
