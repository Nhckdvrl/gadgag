#!/usr/bin/env python3
"""Independent natural-context validation on Doppelganger-JC.

Only aggregate scores are written.  The upstream benchmark sentences remain in
the external checkout and are not copied into this repository.
"""
from __future__ import annotations

import argparse
import ast
import json
import unicodedata
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from scoring_v2 import score_many

ROOT = Path(__file__).resolve().parents[1]


def load_literal(path: Path) -> dict:
    text = path.read_text()
    return ast.literal_eval(text[text.index("{"):])


def minimal_substitution(correct: str, shortcut: str) -> tuple[str, str] | None:
    """Return the differing middle spans after common prefix/suffix removal."""
    prefix = 0
    while (prefix < min(len(correct), len(shortcut)) and
           correct[prefix] == shortcut[prefix]):
        prefix += 1
    suffix = 0
    while (suffix < min(len(correct) - prefix, len(shortcut) - prefix) and
           correct[-1 - suffix] == shortcut[-1 - suffix]):
        suffix += 1
    end = -suffix if suffix else None
    good, bad = correct[prefix:end], shortcut[prefix:end]
    if not good.strip() or not bad.strip() or max(len(good), len(bad)) > 30:
        return None
    return good.strip(), bad.strip()


def mask_once(sentence: str, word: str) -> str | None:
    sentence = unicodedata.normalize("NFKC", sentence)
    word = unicodedata.normalize("NFKC", word)
    if word not in sentence:
        return None
    return sentence.replace(word, "[TARGET]", 1)


def load_pairs(root: Path) -> list[dict]:
    jp_zh = load_literal(root / "questions/jp_zh/homographs.py")
    zh_jp = load_literal(root / "questions/zh_jp/homographs.py")
    mappings = []
    for line in (root / "cognate_fixed/jp/homographs.txt").read_text().splitlines():
        parts = line.split("|")
        if len(parts) >= 2:
            mappings.append((parts[0], parts[1]))
    rows = []
    for japanese, chinese in mappings:
        if chinese not in jp_zh or japanese not in zh_jp:
            continue
        directions = []
        for name, record, source_word, source_lang, output_lang in (
            ("jp_zh", jp_zh[chinese], japanese, "Japanese", "Chinese"),
            ("zh_jp", zh_jp[japanese], chinese, "Chinese", "Japanese"),
        ):
            masked = mask_once(record["target-sentence"], source_word)
            alternatives = minimal_substitution(record["correct"], record["wrong1"])
            if masked is None or alternatives is None:
                break
            directions.append({
                "direction": name, "source_word": source_word,
                "source_language": source_lang, "output_language": output_lang,
                "sentence": unicodedata.normalize("NFKC", record["target-sentence"]),
                "masked": masked, "correct_option": alternatives[0],
                "shortcut_option": alternatives[1],
            })
        if len(directions) == 2:
            rows.append({"id": f"doppel_{len(rows):03d}", "directions": directions})
    return rows


def prompt(row: dict, condition: str, other: dict, order: int) -> tuple[str, str, str]:
    if condition == "full":
        context = row["sentence"].replace(
            row["source_word"], f'[[{row["source_word"]}]]', 1)
    elif condition == "masked":
        context = row["masked"]
    elif condition == "language_unrelated":
        context = other["masked"]
    elif condition == "surface_only":
        context = f'[[{row["source_word"]}]]'
    else:
        raise ValueError(condition)
    options = [row["correct_option"], row["shortcut_option"]]
    if order:
        options.reverse()
    correct_label = "B" if order else "A"
    wrong_label = "A" if order else "B"
    text = (
        f"This is a {row['source_language']}-to-{row['output_language']} lexical "
        "translation decision. Choose which option expresses the intended sense "
        "of the bracketed target position in the supplied context. If the surface form is shown alone, "
        "choose its most likely sense in the stated source language.\n"
        f"Context: {context}\nA: {options[0]}\nB: {options[1]}\n"
        "Answer with A or B only."
    )
    return text, correct_label, wrong_label


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--max-items", type=int)
    parser.add_argument("--output-path", type=Path)
    args = parser.parse_args()

    pairs = load_pairs(args.data_root)
    if args.max_items:
        pairs = pairs[:args.max_items]
    tokenizer = AutoTokenizer.from_pretrained(args.model, local_files_only=True)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        args.model, dtype=torch.bfloat16, device_map={"": 0}, local_files_only=True,
        attn_implementation="sdpa",
    ).eval()

    requests, metadata = [], []
    conditions = ("full", "masked", "language_unrelated", "surface_only")
    for index, pair in enumerate(pairs):
        other_pair = pairs[(index + 1) % len(pairs)]
        for direction_index, row in enumerate(pair["directions"]):
            other = other_pair["directions"][direction_index]
            for condition in conditions:
                for order in (0, 1):
                    text, correct, wrong = prompt(row, condition, other, order)
                    for answer_kind, answer in (("correct", correct), ("shortcut", wrong)):
                        requests.append((text, answer))
                        metadata.append((pair["id"], row["direction"], condition,
                                         order, answer_kind))
    scores = score_many(model, tokenizer, requests, "chat", args.batch_size)
    grouped: dict[tuple, dict] = {}
    for meta, score in zip(metadata, scores):
        item_id, direction, condition, order, answer_kind = meta
        key = item_id, direction, condition, order
        row = grouped.setdefault(key, {
            "id": item_id, "direction": direction, "condition": condition,
            "order": order, "model": args.tag,
        })
        row[f"mean_{answer_kind}"] = score.mean_logp
        row[f"sum_{answer_kind}"] = score.sum_logp
    output = []
    for row in grouped.values():
        row["margin_mean"] = row["mean_correct"] - row["mean_shortcut"]
        row["margin_sum"] = row["sum_correct"] - row["sum_shortcut"]
        output.append(row)
    path = args.output_path or (ROOT / "results/extensions" /
                                f"doppel_natural_{args.tag}.jsonl")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in output))
    print(f"wrote {len(output)} rows ({len(pairs)} paired items) to {path}")


if __name__ == "__main__":
    main()
