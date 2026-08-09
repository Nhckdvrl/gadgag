#!/usr/bin/env python3
"""Summarize fine-dose, second-model, and alternate-gloss replications."""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]; RNG=np.random.default_rng(20260810)

def read(pattern):
 rows=[]
 for p in sorted((ROOT/'results'/'extensions').glob(pattern)):
  rows += [json.loads(x) for x in p.read_text().splitlines()]
 return pd.DataFrame(rows)

def cross(d, tag):
 ff=d[d.group=='false_friend'].copy(); base=ff[ff.dose==0][['fold','id','margin','is_correct']].rename(columns={'margin':'pre','is_correct':'pre_ok'})
 q=ff[ff.dose>0].merge(base,on=['fold','id']);q['delta']=q.margin-q.pre;q['intrusion']=q.pre_ok & ~q.is_correct
 piv=q.pivot_table(index=['dose','id'],columns='treated',values='delta').reset_index();piv['paired']=piv[True]-piv[False]
 out=[]
 for dose,g in piv.groupby('dose'):
  boots=np.array([RNG.choice(g.paired,len(g),replace=True).mean() for _ in range(10000)])
  tr=q[(q.dose==dose)&q.treated&q.pre_ok];ho=q[(q.dose==dose)&~q.treated&q.pre_ok]
  out.append({'experiment':tag,'dose':dose,'n':len(g),'paired_delta':g.paired.mean(),'ci_low':np.quantile(boots,.025),'ci_high':np.quantile(boots,.975),'treated_cir':(~tr.is_correct).mean(),'heldout_cir':(~ho.is_correct).mean()})
 return pd.DataFrame(out)

def main():
 frames=[]
 for tag,pat in [('qwen25_fine','qwen25_fine_fold*_dose*.jsonl'),('qwen3_8b','qwen3_8b_fold*_dose*.jsonl'),('gloss','gloss_fold*_dose*.jsonl'),('en_de','en_de_fold*_dose*.jsonl')]:
  d=read(pat)
  if len(d):frames.append(cross(d,tag))
 for tag in ['attention_only','mlp_only','early_half','late_half','collision_replay','random_replay','neutral_surface']:
  d=read(f'{tag}_fold*_dose*.jsonl')
  if len(d):frames.append(cross(d,tag))
 out=pd.concat(frames,ignore_index=True);out.to_csv(ROOT/'results'/'extensions'/'summary.csv',index=False)
 (ROOT/'reports'/'extensions.md').write_text('# Robustness extensions\n\n'+out.to_markdown(index=False)+'\n')
 print(out.to_string(index=False))
if __name__=='__main__':main()
