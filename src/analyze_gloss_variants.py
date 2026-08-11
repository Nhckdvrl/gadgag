#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import numpy as np,pandas as pd
ROOT=Path(__file__).resolve().parents[1];R=np.random.default_rng(20260811)
def main():
 rows=[]
 for p in (ROOT/'results/extensions').glob('gloss_variants_*.jsonl'):rows += [json.loads(x) for x in p.read_text().splitlines()]
 d=pd.DataFrame(rows);out=[];item=[]
 for key,g in d.groupby(['model','prompt_mode','variant']):
  for norm in ['mean','sum']:
   p=g.pivot(index='id',columns=['language','sense'],values=f'margin_{norm}');v=(((p[1,2]+p[2,2])-(p[1,1]+p[2,1]))/2);idx=R.integers(0,len(v),(5000,len(v)));b=v.to_numpy()[idx].mean(1);out.append({'model':key[0],'prompt_mode':key[1],'variant':key[2],'normalization':norm,'n':len(v),'semantic_effect':v.mean(),'ci_low':np.quantile(b,.025),'ci_high':np.quantile(b,.975),'positive_rate':(v>0).mean()});item += [{'model':key[0],'prompt_mode':key[1],'variant':key[2],'normalization':norm,'id':i,'semantic_effect':z} for i,z in v.items()]
 o=pd.DataFrame(out);o.to_csv(ROOT/'results/extensions/gloss_variant_summary.csv',index=False);it=pd.DataFrame(item);cons=it.groupby(['model','prompt_mode','normalization','id']).semantic_effect.agg(lambda x: (x>0).all()).groupby(level=[0,1,2]).mean().rename('all_three_positive').reset_index();cons.to_csv(ROOT/'results/extensions/gloss_variant_consistency.csv',index=False);(ROOT/'reports/gloss_variants.md').write_text('# Lexical gloss robustness\n\n'+o.to_markdown(index=False)+'\n\n## Item-level sign consistency\n\n'+cons.to_markdown(index=False)+'\n');print(o.to_string(index=False));print(cons.to_string(index=False))
if __name__=='__main__':main()
