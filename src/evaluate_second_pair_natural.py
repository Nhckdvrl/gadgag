#!/usr/bin/env python3
"""Natural-diagonal context/form decomposition on non-CJK Stingray pairs."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from scoring_v2 import prepare_chat_messages, score_prepared
from stingray_factorial import LANGUAGES, load_pair, mask_target

ROOT = Path(__file__).resolve().parents[1]
WRAPPERS = {
    "bare": lambda value: value,
    "definition": lambda value: f"the definition is {value}",
    "refers": lambda value: f"this expression refers to {value}",
}


def mark_target(sentence: str, target: str) -> str:
    marked, count = re.subn(re.escape(target), lambda match: f"[[{match.group(0)}]]",
                            sentence, count=1, flags=re.IGNORECASE)
    if not count:
        raise ValueError(f"target {target!r} absent from {sentence!r}")
    return marked


def prompt(item: dict, other: dict, language: int, condition: str) -> str:
    target = item[f"word_l{language}"]
    natural = item[f"L{language}_S{language}"]
    if condition == "full":
        context = mark_target(natural, target)
    elif condition == "masked":
        context = mask_target(natural, target)
    elif condition == "language_unrelated":
        other_target = other[f"word_l{language}"]
        context = mask_target(other[f"L{language}_S{language}"], other_target)
    elif condition == "surface_only":
        context = f"[[{target}]]"
    else:
        raise ValueError(condition)
    return (
        f"The context is in {LANGUAGES[item['pair']][language - 1]}. Choose the English "
        "meaning expressed at the bracketed target position.\n"
        f"Context: {context}\nMeaning:"
    )


def prepare_direct(tokenizer, text: str, candidate: str):
    messages = [{"role": "user", "content": text}]
    if "qwen3" not in str(tokenizer.name_or_path).casefold():
        return prepare_chat_messages(tokenizer, messages, candidate)
    prefix = tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True,
                                           enable_thinking=False)
    continuation = tokenizer(candidate, add_special_tokens=False).input_ids
    return list(prefix) + list(continuation), len(prefix)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pair", choices=["id_ms", "id_tl", "en_de"], required=True)
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--batch-size", type=int, default=16)
    args = parser.parse_args()

    items = load_pair(args.data_root, args.pair, exact_only=True)
    tokenizer = AutoTokenizer.from_pretrained(args.model, local_files_only=True)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        args.model, dtype=torch.bfloat16, device_map={"": 0}, local_files_only=True,
        attn_implementation="sdpa").eval()
    prepared, metadata = [], []
    for index, item in enumerate(items):
        other = items[(index + 1) % len(items)]
        for language in (1, 2):
            for condition in ("full", "masked", "language_unrelated", "surface_only"):
                text = prompt(item, other, language, condition)
                for wrapper, transform in WRAPPERS.items():
                    for sense, meaning in ((1, item["meaning_l1"]), (2, item["meaning_l2"])):
                        prepared.append(prepare_direct(tokenizer, text, transform(meaning)))
                        metadata.append((item["id"], language, condition, wrapper, sense))
    scores = score_prepared(model, tokenizer, prepared, args.batch_size)
    grouped = {}
    for meta, score in zip(metadata, scores):
        item_id, language, condition, wrapper, sense = meta
        key = item_id, language, condition, wrapper
        row = grouped.setdefault(key, {"id": item_id, "pair": args.pair,
            "model": args.tag, "target_language": language, "condition": condition,
            "wrapper": wrapper})
        row[f"mean_s{sense}"] = score.mean_logp
        row[f"sum_s{sense}"] = score.sum_logp
    output = []
    for row in grouped.values():
        for norm in ("mean", "sum"):
            raw = row[f"{norm}_s2"] - row[f"{norm}_s1"]
            row[f"margin_{norm}"] = raw
            row[f"correct_margin_{norm}"] = raw if row["target_language"] == 2 else -raw
        output.append(row)
    path = ROOT / "results/extensions" / f"natural2_{args.pair}_{args.tag}.jsonl"
    path.write_text("".join(json.dumps(row) + "\n" for row in output))
    print(f"wrote {len(output)} cells for {len(items)} exact-form items to {path}")


if __name__ == "__main__":
    main()
