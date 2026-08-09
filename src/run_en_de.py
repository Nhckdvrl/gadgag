#!/usr/bin/env python3
"""English->German false-friend crossover replication on StingrayBench."""
from __future__ import annotations
import argparse, difflib, json, random
from pathlib import Path
import numpy as np, pandas as pd, torch
from peft import LoraConfig, get_peft_model
from transformers import AutoModelForCausalLM, AutoTokenizer
from run_pilot import ROOT, candidate_score, train_segment

SEED=20260810; MODEL='Qwen/Qwen2.5-7B-Instruct'

def word(s): return str(s).split('(')[0].strip()
def items():
 d=pd.read_csv(ROOT/'external'/'StingrayBench'/'data'/'en_de.csv');out=[]
 for k,i in enumerate(range(0,len(d),2)):
  en,de=d.iloc[i],d.iloc[i+1];we,wd=word(en.Cognates),word(de.Cognates)
  if str(en['Meaning in L1']).strip().casefold()==str(en['Meaning in L2']).strip().casefold():continue
  out.append({'id':f'ende_{k:03d}','group':'false_friend','word_en':we,'word_de':wd,
   'train_en':str(en.L1).strip(),'eval_de':str(de.L2).strip(),
   'correct':str(en['Meaning in L2']).strip(),'intrusion':str(en['Meaning in L1']).strip(),
   'form_similarity':difflib.SequenceMatcher(None,we.casefold(),wd.casefold()).ratio(),
   'casefold_exact':we.casefold()==wd.casefold()})
 ids=[x['id'] for x in out];random.Random(SEED+77).shuffle(ids);half=set(ids[:len(ids)//2])
 for x in out:x['treated_fold']=0 if x['id'] in half else 1
 return out

def evaluate(model,tok,xs,fold,dose):
 out=[];model.eval()
 for i,x in enumerate(xs):
  p=(f'What is the meaning of "{x["word_de"]}" in the following German sentence? '
     'Answer in English.\n'+x['eval_de']+'\nMeaning: ')
  c,_=candidate_score(model,tok,p,x['correct']);z,_=candidate_score(model,tok,p,x['intrusion'])
  y=dict(x);y.update({'fold':fold,'dose':dose,'treated':x['treated_fold']==fold,'margin':c-z,
                      'is_correct':c>z,'correct_mean_logp':c,'intrusion_mean_logp':z});out.append(y)
  if (i+1)%20==0:print(f'en-de fold={fold} dose={dose}: {i+1}/{len(xs)}',flush=True)
 p=ROOT/'results'/'extensions'/f'en_de_fold{fold}_dose{dose}.jsonl';p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(''.join(json.dumps(y,ensure_ascii=False)+'\n' for y in out))

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--fold',type=int,choices=[0,1],required=True);a=ap.parse_args()
 random.seed(SEED+a.fold);np.random.seed(SEED+a.fold);torch.manual_seed(SEED+a.fold);torch.backends.cuda.matmul.allow_tf32=True
 xs=items();tok=AutoTokenizer.from_pretrained(MODEL,local_files_only=True);tok.pad_token=tok.eos_token
 base=AutoModelForCausalLM.from_pretrained(MODEL,dtype=torch.bfloat16,device_map={'':0},local_files_only=True,attn_implementation='sdpa');base.config.use_cache=False
 model=get_peft_model(base,LoraConfig(r=16,lora_alpha=32,lora_dropout=0.0,bias='none',task_type='CAUSAL_LM',target_modules=['q_proj','k_proj','v_proj','o_proj','gate_proj','up_proj','down_proj']))
 evaluate(model,tok,xs,a.fold,0);prev=0
 for dose in (8,32):
  target=[x for x in xs if x['treated_fold']==a.fold];texts=[]
  for e in range(prev,dose):
   q=target.copy();random.Random(SEED+a.fold*10000+e).shuffle(q);texts += [x['train_en'] for x in q]
  train_segment(model,tok,texts,a.fold,prev,dose);evaluate(model,tok,xs,a.fold,dose);prev=dose
  model.save_pretrained(ROOT/'results'/'extensions'/'adapters'/f'en_de_fold{a.fold}_dose{dose}')
if __name__=='__main__':main()
