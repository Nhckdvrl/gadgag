#!/usr/bin/env python3
"""Content-free answer baseline for contextual calibration comparisons."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from evaluate_factorial import WRAPPERS
from scoring_v2 import score_many
from stingray_factorial import load_pair

ROOT = Path(__file__).resolve().parents[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pair", choices=["zh_ja", "id_tl"], required=True)
    ap.add_argument("--model", required=True); ap.add_argument("--tag", required=True)
    ap.add_argument("--data-root", type=Path, required=True)
    ap.add_argument("--prompt-mode", choices=["plain", "chat"], required=True)
    ap.add_argument("--batch-size", type=int, default=32)
    args = ap.parse_args()
    items = load_pair(args.data_root, args.pair, exact_only=True)
    tok = AutoTokenizer.from_pretrained(args.model, local_files_only=True)
    if tok.pad_token_id is None: tok.pad_token = tok.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        args.model, dtype=torch.bfloat16, device_map={"": 0}, local_files_only=True,
        attn_implementation="sdpa").eval()
    requests, meta = [], []
    for item in items:
        p = (f'Choose the meaning expressed by "{item["word"]}" using the supplied information.\n'
             "Context: N/A\nMeaning options are provided as answer continuations.")
        for wrapper, transform in WRAPPERS.items():
            for sense, meaning in ((1,item["meaning_l1"]),(2,item["meaning_l2"])):
                requests.append((p,transform(meaning)));meta.append((item,wrapper,sense))
    scores=score_many(model,tok,requests,args.prompt_mode,args.batch_size);grouped={}
    for (item,wrapper,sense),score in zip(meta,scores):
        row=grouped.setdefault((item['id'],wrapper),{'id':item['id'],'pair':args.pair,'model':args.tag,'prompt_mode':args.prompt_mode,'wrapper':wrapper})
        row[f'mean_s{sense}']=score.mean_logp;row[f'sum_s{sense}']=score.sum_logp
    out=[]
    for row in grouped.values():
        row['margin_mean']=row['mean_s2']-row['mean_s1'];row['margin_sum']=row['sum_s2']-row['sum_s1'];out.append(row)
    path=ROOT/'results/extensions'/f'content_free_{args.pair}_{args.tag}_{args.prompt_mode}.jsonl'
    path.write_text(''.join(json.dumps(x)+'\n' for x in out));print('wrote',len(out),path)
if __name__=='__main__':main()
