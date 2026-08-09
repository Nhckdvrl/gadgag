#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import numpy as np,pandas as pd
ROOT=Path(__file__).resolve().parents[1];R=np.random.default_rng(20260810)
def main():
 rows=[]
 for p in (ROOT/'results'/'extensions').glob('context_lift_fold*.jsonl'):rows += [json.loads(x) for x in p.read_text().splitlines()]
 d=pd.DataFrame(rows);base=d[d.condition=='base'][['fold','id','context_lift','raw_margin']].rename(columns={'context_lift':'lift0','raw_margin':'raw0'})
 q=d[d.condition!='base'].merge(base,on=['fold','id']);q['dlift']=q.context_lift-q.lift0;q['draw']=q.raw_margin-q.raw0
 out=[]
 for cond,g in q.groupby('condition'):
  # Within-word crossover: treated in one fold, held out in the other.
  for metric in ['draw','dlift']:
   p=g.pivot_table(index='id',columns='treated',values=metric);v=(p[True]-p[False]).to_numpy()
   b=np.array([R.choice(v,len(v),replace=True).mean() for _ in range(10000)])
   out.append({'condition':cond,'metric':metric,'n':len(v),'paired_effect':v.mean(),'ci_low':np.quantile(b,.025),'ci_high':np.quantile(b,.975)})
 o=pd.DataFrame(out);o.to_csv(ROOT/'results'/'extensions'/'context_lift_summary.csv',index=False)
 (ROOT/'reports'/'context_lift.md').write_text('# Context-lift construct-validity check\n\n'+o.to_markdown(index=False)+'\n')
 print(o.to_string(index=False))
if __name__=='__main__':main()
