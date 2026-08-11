#!/usr/bin/env python3
"""Run the exact-form 2×2 language × semantic-context construct killer."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from scoring_v2 import score_many
from stingray_factorial import add_controls, load_pair

ROOT = Path(__file__).resolve().parents[1]
WRAPPERS = {
    "bare": lambda x: x,
    "definition": lambda x: f"the definition is {x}",
    "refers": lambda x: f"this expression refers to {x}",
}


def prompt(item: dict, context: str, condition: str) -> str:
    if condition == "masked":
        target = "[TARGET]"
    else:
        target = item["word"]
    return (
        f'Choose the meaning expressed by "{target}" using the supplied information.\n'
        f"Context: {context}\nMeaning options are provided as answer continuations."
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pair", choices=["zh_ja", "en_de", "id_ms", "id_tl"], required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--data-root", type=Path, default=ROOT / "external/StingrayBench/data")
    ap.add_argument("--prompt-mode", choices=["plain", "chat"], default="plain")
    ap.add_argument("--batch-size", type=int, default=8)
    ap.add_argument("--output-path", type=Path,
                    help="Optional result path for protocol stress tests")
    ap.add_argument("--allow-download", action="store_true")
    args = ap.parse_args()

    items = add_controls(load_pair(args.data_root, args.pair, exact_only=True))
    tokenizer = AutoTokenizer.from_pretrained(args.model, local_files_only=not args.allow_download)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        args.model, dtype=torch.bfloat16, device_map={"": 0},
        local_files_only=not args.allow_download, attn_implementation="sdpa",
    ).eval()

    requests, metadata = [], []
    for item in items:
        for condition in ("full", "masked", "language_only", "shuffled"):
            for language in (1, 2):
                for sense in (1, 2):
                    key = f"L{language}_S{sense}"
                    ctx = item[key] if condition == "full" else item[f"{condition}_{key}"]
                    p = prompt(item, ctx, condition)
                    for wrapper, transform in WRAPPERS.items():
                        for candidate_sense, meaning in ((1, item["meaning_l1"]), (2, item["meaning_l2"])):
                            requests.append((p, transform(meaning)))
                            metadata.append((item, condition, language, sense, wrapper, candidate_sense))
    scores = score_many(model, tokenizer, requests, args.prompt_mode, args.batch_size)

    grouped: dict[tuple, dict] = {}
    for meta, score in zip(metadata, scores):
        item, condition, language, sense, wrapper, candidate_sense = meta
        key = (item["id"], condition, language, sense, wrapper)
        row = grouped.setdefault(key, {
            "id": item["id"], "pair": args.pair, "model": args.tag,
            "prompt_mode": args.prompt_mode, "condition": condition,
            "language": language, "sense": sense, "wrapper": wrapper,
            "word": item["word"], "meaning_l1": item["meaning_l1"],
            "meaning_l2": item["meaning_l2"],
        })
        row[f"mean_s{candidate_sense}"] = score.mean_logp
        row[f"sum_s{candidate_sense}"] = score.sum_logp
        row[f"tokens_s{candidate_sense}"] = score.n_tokens
    output = []
    for row in grouped.values():
        row["margin_mean"] = row["mean_s2"] - row["mean_s1"]
        row["margin_sum"] = row["sum_s2"] - row["sum_s1"]
        output.append(row)
    out = args.output_path or (ROOT / "results/extensions" / f"factorial_{args.pair}_{args.tag}_{args.prompt_mode}.jsonl")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in output))
    print(f"wrote {len(output)} cells to {out}")


if __name__ == "__main__":
    main()
