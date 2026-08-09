#!/usr/bin/env python3
"""Context-lift audit for the English-German Stingray replication."""
from __future__ import annotations
import argparse,json
import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM,AutoTokenizer
from run_pilot import ROOT,MODEL,candidate_score
from run_en_de import items
def prompt(w,s):return f'What is the meaning of "{w}" in the following German sentence? Answer in English.\n{s}\nMeaning: '
def score(model,tok,xs,fold,cond):
 out=[];model.eval()
 for i,x in enumerate(xs):
  sh=xs[(i+13)%len(xs)]['eval_de'];ac,_=candidate_score(model,tok,prompt(x['word_de'],x['eval_de']),x['correct']);ai,_=candidate_score(model,tok,prompt(x['word_de'],x['eval_de']),x['intrusion']);sc,_=candidate_score(model,tok,prompt(x['word_de'],sh),x['correct']);si,_=candidate_score(model,tok,prompt(x['word_de'],sh),x['intrusion'])
  out.append({'id':x['id'],'fold':fold,'condition':cond,'treated':x['treated_fold']==fold,'raw_margin':ac-ai,'shuffled_margin':sc-si,'context_lift':(ac-ai)-(sc-si)})
 p=ROOT/'results'/'extensions'/f'en_de_lift_fold{fold}_{cond}.jsonl';p.write_text(''.join(json.dumps(y)+'\n' for y in out))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--fold',type=int,choices=[0,1],required=True);a=ap.parse_args();xs=items();tok=AutoTokenizer.from_pretrained(MODEL,local_files_only=True);tok.pad_token=tok.eos_token
 base=AutoModelForCausalLM.from_pretrained(MODEL,dtype=torch.bfloat16,device_map={'':0},local_files_only=True,attn_implementation='sdpa');score(base,tok,xs,a.fold,'base')
 model=PeftModel.from_pretrained(base,ROOT/'results'/'extensions'/'adapters'/f'en_de_fold{a.fold}_dose8',adapter_name='d8');model.load_adapter(ROOT/'results'/'extensions'/'adapters'/f'en_de_fold{a.fold}_dose32',adapter_name='d32')
 for n in ['d8','d32']:model.set_adapter(n);score(model,tok,xs,a.fold,n)
if __name__=='__main__':main()
