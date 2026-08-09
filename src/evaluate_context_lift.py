#!/usr/bin/env python3
"""Remove candidate priors with a matched, shuffled-context difference."""
from __future__ import annotations
import argparse,json
import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM,AutoTokenizer
from run_pilot import ROOT,MODEL,candidate_score,read_items

def prompt(sentence):return '次の日本語文を中国語に翻訳してください。説明は不要です。\n日本語: '+sentence+'\n中国語: '
def score(model,tok,xs,fold,condition):
 out=[];model.eval()
 ff=[x for x in xs if x['group']=='false_friend']
 for i,x in enumerate(ff):
  shuffled=ff[(i+17)%len(ff)]['eval_ja']
  ac,_=candidate_score(model,tok,prompt(x['eval_ja']),x['correct']);ai,_=candidate_score(model,tok,prompt(x['eval_ja']),x['intrusion'])
  sc,_=candidate_score(model,tok,prompt(shuffled),x['correct']);si,_=candidate_score(model,tok,prompt(shuffled),x['intrusion'])
  raw=ac-ai;null=sc-si
  out.append({'id':x['id'],'fold':fold,'condition':condition,'treated':x['treated_fold']==fold,
              'raw_margin':raw,'shuffled_margin':null,'context_lift':raw-null})
  if (i+1)%10==0:print(f'lift fold={fold} {condition}: {i+1}/{len(ff)}',flush=True)
 p=ROOT/'results'/'extensions'/f'context_lift_fold{fold}_{condition}.jsonl';p.write_text(''.join(json.dumps(y)+'\n' for y in out))

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--fold',type=int,choices=[0,1],required=True);a=ap.parse_args();xs=read_items()
 tok=AutoTokenizer.from_pretrained(MODEL,local_files_only=True);tok.pad_token=tok.eos_token
 base=AutoModelForCausalLM.from_pretrained(MODEL,dtype=torch.bfloat16,device_map={'':0},local_files_only=True,attn_implementation='sdpa')
 score(base,tok,xs,a.fold,'base')
 model=PeftModel.from_pretrained(base,ROOT/'results'/'adapters'/f'fold{a.fold}_dose32',adapter_name='conflict')
 model.load_adapter(ROOT/'results'/'extensions'/'adapters'/f'neutral_surface_fold{a.fold}_dose32',adapter_name='neutral')
 for name in ['conflict','neutral']:
  model.set_adapter(name);score(model,tok,xs,a.fold,name)
if __name__=='__main__':main()
