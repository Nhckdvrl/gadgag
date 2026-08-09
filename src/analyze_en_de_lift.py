#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import numpy as np,pandas as pd
ROOT=Path(__file__).resolve().parents[1];R=np.random.default_rng(20260810)
def main():
 rows=[]
 for p in (ROOT/'results'/'extensions').glob('en_de_lift_fold*.jsonl'):rows += [json.loads(x) for x in p.read_text().splitlines()]
 d=pd.DataFrame(rows);b=d[d.condition=='base'][['fold','id','raw_margin','context_lift']].rename(columns={'raw_margin':'raw0','context_lift':'lift0'});q=d[d.condition!='base'].merge(b,on=['fold','id']);q['draw']=q.raw_margin-q.raw0;q['dlift']=q.context_lift-q.lift0;out=[]
 for c,g in q.groupby('condition'):
  for m in ['draw','dlift']:
   p=g.pivot_table(index='id',columns='treated',values=m);v=(p[True]-p[False]).to_numpy();z=np.array([R.choice(v,len(v),replace=True).mean() for _ in range(10000)]);out.append({'condition':c,'metric':m,'n':len(v),'effect':v.mean(),'ci_low':np.quantile(z,.025),'ci_high':np.quantile(z,.975)})
 o=pd.DataFrame(out);o.to_csv(ROOT/'results'/'extensions'/'en_de_lift_summary.csv',index=False);print(o.to_string(index=False))
if __name__=='__main__':main()
