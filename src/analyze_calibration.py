#!/usr/bin/env python3
from __future__ import annotations
import json,math
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
def rows(pattern):
 out=[]
 for p in (ROOT/'results/extensions').glob(pattern):out += [json.loads(x) for x in p.read_text().splitlines()]
 return pd.DataFrame(out)
def metrics(a1,a2):
 bias=(math.atan2(a2,a1)-math.pi/4)/(math.pi/4) if a1 or a2 else 0
 return bias,(a1*a1+a2*a2)**.5/(2**.5)
def main():
 f=rows('factorial_*.jsonl');c=rows('content_free_*.jsonl');f=f[(f.condition=='full') & (((f.language==1)&(f.sense==1))|((f.language==2)&(f.sense==2)))]
 keys=['id','pair','model','prompt_mode','wrapper'];d=f.merge(c[keys+['margin_mean','margin_sum']],on=keys,suffixes=('','_cf'));out=[]
 for key,g in d.groupby(['pair','model','prompt_mode','wrapper']):
  for norm in ['mean','sum']:
   raw=g[f'margin_{norm}'];cal=raw-g[f'margin_{norm}_cf'];l=g.language
   for name,v in [('raw',raw),('content_free_calibrated',cal)]:
    a1=((v<0)&(l==1)).sum()/(l==1).sum();a2=((v>0)&(l==2)).sum()/(l==2).sum();both=g.assign(ok=((v<0)&(l==1))|((v>0)&(l==2))).groupby('id').ok.all().mean();bias,comp=metrics(a1,a2)
    out.append({'pair':key[0],'model':key[1],'prompt_mode':key[2],'wrapper':key[3],'normalization':norm,'calibration':name,'l1_accuracy':a1,'l2_accuracy':a2,'both_accuracy':both,'stingray_bias':bias,'stingray_comprehension':comp})
 o=pd.DataFrame(out);o.to_csv(ROOT/'results/extensions/calibration_summary.csv',index=False);(ROOT/'reports/calibration.md').write_text('# Content-free calibration and Stingray-style metrics\n\n'+o.to_markdown(index=False)+'\n');print(o.to_string(index=False))
if __name__=='__main__':main()
