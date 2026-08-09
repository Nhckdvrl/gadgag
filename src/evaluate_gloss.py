#!/usr/bin/env python3
"""Independent Japanese-gloss evaluation of saved main-run adapters."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer
from run_pilot import ROOT, MODEL, candidate_score, read_items

def score_all(model, tok, items, fold, dose):
    out=[]; model.eval()
    for i,x in enumerate(items):
        prompt=(f"次の文中の「{x['word_ja']}」の意味を日本語で説明してください。\n"
                f"文: {x['eval_ja']}\n意味: ")
        cm,_=candidate_score(model,tok,prompt,x['ja_meaning'])
        im,_=candidate_score(model,tok,prompt,x['zh_meaning'])
        out.append({"id":x['id'],"group":x['group'],"fold":fold,"dose":dose,
                    "treated":x['treated_fold'] in (fold,"both"),"margin":cm-im,
                    "is_correct":cm>im,"correct_mean_logp":cm,"intrusion_mean_logp":im})
        if (i+1)%20==0: print(f"gloss fold={fold} dose={dose}: {i+1}/{len(items)}",flush=True)
    p=ROOT/'results'/'extensions'/f'gloss_fold{fold}_dose{dose}.jsonl';p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(''.join(json.dumps(y,ensure_ascii=False)+'\n' for y in out))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--fold',type=int,choices=[0,1],required=True);a=ap.parse_args()
    items=read_items();tok=AutoTokenizer.from_pretrained(MODEL,local_files_only=True);tok.pad_token=tok.eos_token
    base=AutoModelForCausalLM.from_pretrained(MODEL,dtype=torch.bfloat16,device_map={'':0},local_files_only=True,attn_implementation='sdpa')
    score_all(base,tok,items,a.fold,0)
    model=None
    for dose in (32,128):
        path=ROOT/'results'/'adapters'/f'fold{a.fold}_dose{dose}'
        if model is None: model=PeftModel.from_pretrained(base,path,adapter_name=f'd{dose}')
        else: model.load_adapter(path,adapter_name=f'd{dose}')
        model.set_adapter(f'd{dose}');score_all(model,tok,items,a.fold,dose)
if __name__=='__main__':main()
