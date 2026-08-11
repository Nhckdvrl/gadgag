#!/usr/bin/env python3
"""Inference-time cross-turn semantic carryover with matched controls."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from scoring_v2 import score_many_messages
from stingray_factorial import LANGUAGES, load_pair, mask_target

ROOT = Path(__file__).resolve().parents[1]
CONDITIONS = ("wrong_exact", "wrong_masked", "language_unrelated",
              "surface_only", "correct_exact")
LAGS = (
    "Please note that the meeting starts at noon.",
    "Please note that the folder contains three files.",
    "Please note that the lamp is beside the window.",
    "Please note that the ticket number is forty-two.",
    "Please note that the box is on the wooden table.",
    "Please note that the calendar is hanging on the wall.",
    "Please note that the train arrives before sunset.",
    "Please note that the notebook has a blue cover.",
)


def add_exchange(messages: list[dict[str, str]], text: str,
                 prime_role: str = "user") -> None:
    if prime_role == "user":
        messages.append({"role": "user", "content": text})
        messages.append({"role": "assistant", "content": "Acknowledged."})
    elif prime_role == "assistant":
        messages.append({"role": "user", "content":
                         "Provide the next contextual example without explanation."})
        messages.append({"role": "assistant", "content": text})
    else:
        raise ValueError(prime_role)


def history(item: dict, other: dict, condition: str, target_language: int,
            dose: int, lag: int, prime_role: str = "user") -> list[dict[str, str]]:
    prime_language = 1 if target_language == 2 else 2
    prime_sense = prime_language
    target_sense = target_language
    names = LANGUAGES[item["pair"]]
    prime_key = f"L{prime_language}_S{prime_sense}"
    target_key = f"L{target_language}_S{target_sense}"
    if condition == "wrong_exact":
        prime = item[prime_key]
    elif condition == "wrong_masked":
        prime = mask_target(item[prime_key], item[f"word_l{prime_language}"])
    elif condition == "language_unrelated":
        prime = other[prime_key]
    elif condition == "surface_only":
        prime = (f'This is a {names[prime_language - 1]} expression: '
                 f'"{item[f"word_l{prime_language}"]}".')
    elif condition == "correct_exact":
        prime = item[target_key]
    else:
        raise ValueError(condition)

    messages: list[dict[str, str]] = []
    for index in range(dose):
        add_exchange(messages, f"Prime {index + 1}: {prime}", prime_role)
    for index in range(lag):
        add_exchange(messages, LAGS[index], "user")
    return messages


def final_question(item: dict, target_language: int) -> str:
    target_sense = target_language
    context = item[f"L{target_language}_S{target_sense}"]
    return (
        f'Choose the meaning expressed by "{item["word"]}" in the target sentence. '
        "Answer with the English meaning only.\n"
        f"Target sentence: {context}\nAnswer:"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pair", choices=["zh_ja", "id_tl"], required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--doses", type=int, nargs="+", default=[1, 4, 8])
    parser.add_argument("--lags", type=int, nargs="+", default=[0, 2, 8])
    parser.add_argument("--max-items", type=int)
    parser.add_argument("--output-path", type=Path)
    parser.add_argument("--prime-role", choices=["user", "assistant"], default="user")
    args = parser.parse_args()

    items = load_pair(args.data_root, args.pair, exact_only=True)
    if args.max_items:
        items = items[:args.max_items]
    tokenizer = AutoTokenizer.from_pretrained(args.model, local_files_only=True)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        args.model, dtype=torch.bfloat16, device_map={"": 0},
        local_files_only=True, attn_implementation="sdpa",
    ).eval()

    requests, metadata = [], []
    for item_index, item in enumerate(items):
        other = items[(item_index + 1) % len(items)]
        for target_language in (1, 2):
            # One genuinely history-free baseline per item and direction.
            base_messages = [{"role": "user", "content": final_question(item, target_language)}]
            for candidate_sense, meaning in ((1, item["meaning_l1"]),
                                             (2, item["meaning_l2"])):
                requests.append((base_messages, meaning))
                metadata.append((item, target_language, "no_history", 0, 0,
                                 candidate_sense))
            for condition in CONDITIONS:
                for dose in args.doses:
                    for lag in args.lags:
                        messages = history(item, other, condition, target_language, dose, lag,
                                           args.prime_role)
                        messages.append({"role": "user",
                                         "content": final_question(item, target_language)})
                        for candidate_sense, meaning in ((1, item["meaning_l1"]),
                                                         (2, item["meaning_l2"])):
                            requests.append((messages, meaning))
                            metadata.append((item, target_language, condition, dose, lag,
                                             candidate_sense))

    scores = score_many_messages(model, tokenizer, requests, args.batch_size)
    grouped: dict[tuple, dict] = {}
    for meta, score in zip(metadata, scores):
        item, target_language, condition, dose, lag, candidate_sense = meta
        key = (item["id"], target_language, condition, dose, lag)
        row = grouped.setdefault(key, {
            "id": item["id"], "pair": args.pair, "model": args.tag,
            "target_language": target_language, "condition": condition,
            "dose": dose, "lag": lag, "prime_role": args.prime_role,
        })
        row[f"mean_s{candidate_sense}"] = score.mean_logp
        row[f"sum_s{candidate_sense}"] = score.sum_logp
        row[f"tokens_s{candidate_sense}"] = score.n_tokens
    output = []
    for row in grouped.values():
        for normalization in ("mean", "sum"):
            raw = row[f"{normalization}_s2"] - row[f"{normalization}_s1"]
            row[f"margin_{normalization}"] = raw
            row[f"correct_margin_{normalization}"] = (
                raw if row["target_language"] == 2 else -raw
            )
        output.append(row)
    path = args.output_path or (ROOT / "results/extensions" /
                                f"carryover_{args.pair}_{args.tag}.jsonl")
    path.write_text("".join(json.dumps(row) + "\n" for row in output))
    print(f"wrote {len(output)} carryover cells to {path}")


if __name__ == "__main__":
    main()
