#!/usr/bin/env python3
"""General within-language WSD control using expert-curated XL-WiC."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from scoring_v2 import score_many

ROOT = Path(__file__).resolve().parents[1]
FILES = {
    "zh": "xlwic_wn/chinese_zh/zh_valid.txt",
    "ja": "xlwic_wn/japanese_ja/ja_valid.txt",
    "de": "xlwic_wikt/german_de/de_valid.txt",
}


def load(path: Path, limit: int, seed: int) -> list[dict]:
    rows = []
    with path.open() as handle:
        for line in handle:
            # XL-WiC is a literal nine-field TSV, not RFC CSV. Some German
            # contexts contain quotation marks that csv.reader misinterprets.
            values = line.rstrip("\n").split("\t")
            assert len(values) == 9, (path, len(values))
            rows.append({"word": values[0], "context1": values[6], "context2": values[7],
                         "label": int(values[8])})
    rng = np.random.default_rng(seed)
    selected = []
    for label in (0, 1):
        indices = np.array([i for i, row in enumerate(rows) if row["label"] == label])
        take = min(limit // 2, len(indices))
        selected.extend(rows[i] for i in rng.choice(indices, take, replace=False))
    rng.shuffle(selected)
    return selected


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--language", choices=FILES, required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--data-root", type=Path, default=ROOT / "external/xlwic_datasets")
    ap.add_argument("--prompt-mode", choices=["plain", "chat"], default="chat")
    ap.add_argument("--limit", type=int, default=200)
    ap.add_argument("--batch-size", type=int, default=32)
    args = ap.parse_args()
    items = load(args.data_root / FILES[args.language], args.limit, 20260811)
    tokenizer = AutoTokenizer.from_pretrained(args.model, local_files_only=True)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        args.model, dtype=torch.bfloat16, device_map={"": 0}, local_files_only=True,
        attn_implementation="sdpa",
    ).eval()
    requests, meta = [], []
    for i, item in enumerate(items):
        prompt = (
            f'The same target word is "{item["word"]}". Decide whether it has the same meaning '
            f"in both contexts.\nContext 1: {item['context1']}\nContext 2: {item['context2']}"
        )
        neutral = (f'The same target word is "{item["word"]}". Decide whether it has the same meaning '
                   "in both contexts.\nContext 1: N/A\nContext 2: N/A")
        for condition, text in (("context", prompt), ("content_free", neutral)):
            for answer, label in (("same meaning", 1), ("different meanings", 0)):
                requests.append((text, answer)); meta.append((i, condition, label))
    scores = score_many(model, tokenizer, requests, args.prompt_mode, args.batch_size)
    grouped = {}
    for (idx, condition, candidate_label), score in zip(meta, scores):
        grouped.setdefault(idx, {}).setdefault(condition, {})[candidate_label] = score.mean_logp
    output = []
    for idx, item in enumerate(items):
        margin = grouped[idx]["context"][1] - grouped[idx]["context"][0]
        content_free = grouped[idx]["content_free"][1] - grouped[idx]["content_free"][0]
        calibrated = margin - content_free
        output.append({"id": idx, "language": args.language, "model": args.tag,
                       "prompt_mode": args.prompt_mode, "label": item["label"],
                       "margin_same": margin, "prediction": int(margin > 0),
                       "correct": int((margin > 0) == item["label"]),
                       "calibrated_margin_same": calibrated,
                       "calibrated_prediction": int(calibrated > 0),
                       "calibrated_correct": int((calibrated > 0) == item["label"])})
    out = ROOT / "results/extensions" / f"xlwic_{args.language}_{args.tag}_{args.prompt_mode}.jsonl"
    out.write_text("".join(json.dumps(row) + "\n" for row in output))
    print(f"{args.language} {args.tag} n={len(output)} raw={np.mean([x['correct'] for x in output]):.3f} calibrated={np.mean([x['calibrated_correct'] for x in output]):.3f}")


if __name__ == "__main__":
    main()
