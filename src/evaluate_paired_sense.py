#!/usr/bin/env python3
"""Paired bilingual sense-switch metric with identical answer candidates."""
from __future__ import annotations
import argparse,json
from pathlib import Path
import pandas as pd,torch
from transformers import AutoModelForCausalLM,AutoTokenizer
from run_pilot import ROOT,candidate_score

def w(s):return str(s).split('(')[0].strip()
def load(pair):
 d=pd.read_csv(ROOT/'external'/'StingrayBench'/'data'/f'{pair}.csv');out=[]
 for k,i in enumerate(range(0,len(d),2)):
  a,b=d.iloc[i],d.iloc[i+1];m1=str(a['Meaning in L1']).strip();m2=str(a['Meaning in L2']).strip()
  if m1.casefold()==m2.casefold():continue
  out.append({'id':f'{pair}_{k:03d}','word_l1':w(a.Cognates),'word_l2':w(b.Cognates),
              'meaning_l1':m1,'meaning_l2':m2,'context_l1':str(a.L1).strip(),'context_l2':str(b.L2).strip()})
 return out
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--pair',choices=['zh_ja','en_de'],required=True);ap.add_argument('--model',required=True);ap.add_argument('--tag',required=True);ap.add_argument('--allow-download',action='store_true');a=ap.parse_args();xs=load(a.pair)
 tok=AutoTokenizer.from_pretrained(a.model,local_files_only=not a.allow_download);tok.pad_token=tok.eos_token
 model=AutoModelForCausalLM.from_pretrained(a.model,dtype=torch.bfloat16,device_map={'':0},local_files_only=not a.allow_download,attn_implementation='sdpa');out=[]
 for i,x in enumerate(xs):
  def scores(word,ctx):
   p=f'What is the meaning of "{word}" in the following sentence? Answer in English.\nSentence: {ctx}\nMeaning: '
   s1,_=candidate_score(model,tok,p,x['meaning_l1']);s2,_=candidate_score(model,tok,p,x['meaning_l2']);return s2-s1
  l1=scores(x['word_l1'],x['context_l1']);l2=scores(x['word_l2'],x['context_l2'])
  y=dict(x);y.update({'pair':a.pair,'model':a.tag,'margin_l1_for_l2':l1,'margin_l2_for_l2':l2,
                      'sense_switch':l2-l1,'l1_correct':l1<0,'l2_correct':l2>0,'both_correct':l1<0 and l2>0});out.append(y)
  if (i+1)%20==0:print(a.pair,a.tag,i+1,len(xs),flush=True)
 p=ROOT/'results'/'extensions'/f'paired_{a.pair}_{a.tag}.jsonl';p.write_text(''.join(json.dumps(y,ensure_ascii=False)+'\n' for y in out))
if __name__=='__main__':main()
