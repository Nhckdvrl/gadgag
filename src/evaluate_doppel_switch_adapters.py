#!/usr/bin/env python3
"""Causal validation of bias/sensitivity decomposition on saved adapters."""
from __future__ import annotations
import argparse,json
import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM,AutoTokenizer
from run_pilot import ROOT,MODEL,candidate_score,read_items
def prompt(w,s):return f'What is the meaning of "{w}" in the following sentence? Answer in Japanese.\nSentence: {s}\nMeaning: '
def score(model,tok,xs,fold,cond):
 out=[];model.eval()
 for x in [z for z in xs if z['group']=='false_friend']:
  def m(s):
   ja,_=candidate_score(model,tok,prompt(x['word_ja'],s),x['ja_meaning']);zh,_=candidate_score(model,tok,prompt(x['word_ja'],s),x['zh_meaning']);return ja-zh
  mz=m(x['train_zh']);mj=m(x['eval_ja']);out.append({'id':x['id'],'fold':fold,'condition':cond,'treated':x['treated_fold']==fold,'margin_zh_for_ja':mz,'margin_ja_for_ja':mj,'candidate_bias':(mj+mz)/2,'sense_switch':mj-mz})
 p=ROOT/'results'/'extensions'/f'doppel_switch_fold{fold}_{cond}.jsonl';p.write_text(''.join(json.dumps(y)+'\n' for y in out))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--fold',type=int,choices=[0,1],required=True);a=ap.parse_args();xs=read_items();tok=AutoTokenizer.from_pretrained(MODEL,local_files_only=True);tok.pad_token=tok.eos_token
 base=AutoModelForCausalLM.from_pretrained(MODEL,dtype=torch.bfloat16,device_map={'':0},local_files_only=True,attn_implementation='sdpa');score(base,tok,xs,a.fold,'base')
 model=PeftModel.from_pretrained(base,ROOT/'results'/'adapters'/f'fold{a.fold}_dose32',adapter_name='conflict');model.load_adapter(ROOT/'results'/'extensions'/'adapters'/f'neutral_surface_fold{a.fold}_dose32',adapter_name='neutral')
 for n in ['conflict','neutral']:model.set_adapter(n);score(model,tok,xs,a.fold,n)
if __name__=='__main__':main()
