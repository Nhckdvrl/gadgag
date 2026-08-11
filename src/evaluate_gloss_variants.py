#!/usr/bin/env python3
"""Lexical (not merely wrapper) gloss-robustness test on exact ZH–JA items."""
from __future__ import annotations
import argparse,json
from pathlib import Path
import torch
from transformers import AutoModelForCausalLM,AutoTokenizer
from scoring_v2 import score_many
from stingray_factorial import load_pair
ROOT=Path(__file__).resolve().parents[1]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--model',required=True);ap.add_argument('--tag',required=True);ap.add_argument('--data-root',type=Path,required=True);ap.add_argument('--prompt-mode',choices=['plain','chat'],required=True);ap.add_argument('--batch-size',type=int,default=32);a=ap.parse_args()
 items=load_pair(a.data_root,'zh_ja',True);variants=json.loads((ROOT/'data/zh_ja_gloss_variants.json').read_text());tok=AutoTokenizer.from_pretrained(a.model,local_files_only=True);tok.pad_token=tok.pad_token or tok.eos_token
 model=AutoModelForCausalLM.from_pretrained(a.model,dtype=torch.bfloat16,device_map={'':0},local_files_only=True,attn_implementation='sdpa').eval();req=[];meta=[]
 for x in items:
  assert x['id'] in variants
  for language in (1,2):
   for sense in (1,2):
    ctx=x[f'L{language}_S{sense}'];p=f'Choose the meaning expressed by "{x["word"]}" using the supplied information.\nContext: {ctx}\nMeaning options are provided as answer continuations.'
    for variant in range(3):
     for cs in (1,2):req.append((p,variants[x['id']][f's{cs}'][variant]));meta.append((x,language,sense,variant,cs))
 scores=score_many(model,tok,req,a.prompt_mode,a.batch_size);g={}
 for (x,l,s,v,cs),z in zip(meta,scores):
  r=g.setdefault((x['id'],l,s,v),{'id':x['id'],'pair':'zh_ja','model':a.tag,'prompt_mode':a.prompt_mode,'language':l,'sense':s,'variant':v});r[f'mean_s{cs}']=z.mean_logp;r[f'sum_s{cs}']=z.sum_logp
 out=[]
 for r in g.values():r['margin_mean']=r['mean_s2']-r['mean_s1'];r['margin_sum']=r['sum_s2']-r['sum_s1'];out.append(r)
 p=ROOT/'results/extensions'/f'gloss_variants_zh_ja_{a.tag}_{a.prompt_mode}.jsonl';p.write_text(''.join(json.dumps(x)+'\n' for x in out));print('wrote',len(out),p)
if __name__=='__main__':main()
