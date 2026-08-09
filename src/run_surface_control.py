#!/usr/bin/env python3
"""Frequency-matched word-form exposure without the conflicting Chinese sense."""
from __future__ import annotations
import argparse,json,random
import numpy as np,torch
from peft import LoraConfig,get_peft_model
from transformers import AutoModelForCausalLM,AutoTokenizer
from run_pilot import ROOT,MODEL,read_items,evaluate,train_segment
SEED=20260810
TEMPLATES=[
 '词语“{w}”出现在这份中文词表中。',
 '这份材料提到了“{w}”这个词。',
 '请注意文中出现了词语“{w}”。',
 '我们正在记录词条“{w}”。',
]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--fold',type=int,choices=[0,1],required=True);a=ap.parse_args()
 random.seed(SEED+a.fold);np.random.seed(SEED+a.fold);torch.manual_seed(SEED+a.fold);torch.backends.cuda.matmul.allow_tf32=True
 xs=read_items();tok=AutoTokenizer.from_pretrained(MODEL,local_files_only=True);tok.pad_token=tok.eos_token
 base=AutoModelForCausalLM.from_pretrained(MODEL,dtype=torch.bfloat16,device_map={'':0},local_files_only=True,attn_implementation='sdpa');base.config.use_cache=False
 model=get_peft_model(base,LoraConfig(r=16,lora_alpha=32,lora_dropout=0,bias='none',task_type='CAUSAL_LM',target_modules=['q_proj','k_proj','v_proj','o_proj','gate_proj','up_proj','down_proj']))
 evaluate(model,tok,xs,a.fold,0,'neutral_surface')
 target=[x for x in xs if x['group']=='false_friend' and x['treated_fold']==a.fold];texts=[]
 for e in range(32):
  q=target.copy();random.Random(SEED+a.fold*1000+e).shuffle(q)
  texts += [TEMPLATES[e%len(TEMPLATES)].format(w=x['word_zh']) for x in q]
 loss=train_segment(model,tok,texts,a.fold,0,32);evaluate(model,tok,xs,a.fold,32,'neutral_surface')
 adapter=ROOT/'results'/'extensions'/'adapters'/f'neutral_surface_fold{a.fold}_dose32';model.save_pretrained(adapter)
 (ROOT/'results'/'extensions'/f'neutral_surface_fold{a.fold}_train.json').write_text(json.dumps({'n_examples':len(texts),'mean_loss':loss},indent=2)+'\n')
if __name__=='__main__':main()
