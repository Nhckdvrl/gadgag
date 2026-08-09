#!/usr/bin/env python3
"""Equal-budget collision-aware versus random semantic replay."""
from __future__ import annotations
import argparse, json, random
import numpy as np, torch
from peft import LoraConfig,get_peft_model
from transformers import AutoModelForCausalLM,AutoTokenizer
from run_pilot import ROOT,MODEL,read_items,evaluate,train_segment
SEED=20260810

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--fold',type=int,choices=[0,1],required=True);ap.add_argument('--replay',choices=['collision','random'],required=True);a=ap.parse_args()
 random.seed(SEED+a.fold);np.random.seed(SEED+a.fold);torch.manual_seed(SEED+a.fold);torch.backends.cuda.matmul.allow_tf32=True
 xs=read_items();tok=AutoTokenizer.from_pretrained(MODEL,local_files_only=True);tok.pad_token=tok.eos_token
 base=AutoModelForCausalLM.from_pretrained(MODEL,dtype=torch.bfloat16,device_map={'':0},local_files_only=True,attn_implementation='sdpa');base.config.use_cache=False
 model=get_peft_model(base,LoraConfig(r=16,lora_alpha=32,lora_dropout=0,bias='none',task_type='CAUSAL_LM',target_modules=['q_proj','k_proj','v_proj','o_proj','gate_proj','up_proj','down_proj']))
 tag=f'{a.replay}_replay';evaluate(model,tok,xs,a.fold,0,tag)
 treated=[x for x in xs if x['group']=='false_friend' and x['treated_fold']==a.fold]
 held=[x for x in xs if x['group']=='false_friend' and x['treated_fold']!=a.fold]
 texts=[]
 for e in range(32):
  q=treated.copy();random.Random(SEED+a.fold*1000+e).shuffle(q);texts += [x['train_zh'] for x in q]
 # Four protection exposures per treated word: 100 examples, 12.5% overhead.
 source=treated if a.replay=='collision' else held
 for e in range(4):
  q=source.copy();random.Random(SEED+50000+a.fold*1000+e).shuffle(q)
  texts += [f"日语词语「{x['word_ja']}」的意思是：{x['ja_meaning']}。它不是中文含义：{x['zh_meaning']}。" for x in q]
 random.Random(SEED+90000+a.fold).shuffle(texts)
 loss=train_segment(model,tok,texts,a.fold,0,32)
 evaluate(model,tok,xs,a.fold,32,tag)
 p=ROOT/'results'/'extensions'/f'{tag}_fold{a.fold}_train.json';p.write_text(json.dumps({'n_adapt':800,'n_replay':100,'mean_loss':loss},indent=2)+'\n')
if __name__=='__main__':main()
