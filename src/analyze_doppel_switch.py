#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import numpy as np,pandas as pd
ROOT=Path(__file__).resolve().parents[1];R=np.random.default_rng(20260810)
def main():
 rows=[]
 for p in (ROOT/'results'/'extensions').glob('doppel_switch_fold*.jsonl'):rows += [json.loads(x) for x in p.read_text().splitlines()]
 d=pd.DataFrame(rows);b=d[d.condition=='base'][['fold','id','diagonal_midpoint','sense_switch','margin_zh_for_ja','margin_ja_for_ja']].rename(columns={'diagonal_midpoint':'b0','sense_switch':'s0','margin_zh_for_ja':'mz0','margin_ja_for_ja':'mj0'});q=d[d.condition!='base'].merge(b,on=['fold','id']);q['dmidpoint']=q.diagonal_midpoint-q.b0;q['dswitch']=q.sense_switch-q.s0;q['d_margin_zh']=q.margin_zh_for_ja-q.mz0;q['d_margin_ja']=q.margin_ja_for_ja-q.mj0;out=[]
 for c,g in q.groupby('condition'):
  for m in ['dmidpoint','dswitch','d_margin_zh','d_margin_ja']:
   p=g.pivot_table(index='id',columns='treated',values=m);v=(p[True]-p[False]).to_numpy();z=np.array([R.choice(v,len(v),replace=True).mean() for _ in range(10000)]);out.append({'condition':c,'metric':m,'n':len(v),'effect':v.mean(),'ci_low':np.quantile(z,.025),'ci_high':np.quantile(z,.975)})
 # Direct difference-in-differences: conflicting meaning versus neutral surface exposure.
 for m in ['dmidpoint','dswitch','d_margin_zh','d_margin_ja']:
  p=q.pivot_table(index=['id','treated'],columns='condition',values=m)
  p['contrast']=p['conflict']-p['neutral']
  p=p.reset_index().pivot_table(index='id',columns='treated',values='contrast')
  v=(p[True]-p[False]).to_numpy();z=np.array([R.choice(v,len(v),replace=True).mean() for _ in range(10000)])
  out.append({'condition':'conflict_minus_neutral','metric':m,'n':len(v),'effect':v.mean(),'ci_low':np.quantile(z,.025),'ci_high':np.quantile(z,.975)})
 o=pd.DataFrame(out);o.to_csv(ROOT/'results'/'extensions'/'doppel_switch_causal.csv',index=False)
 (ROOT/'reports'/'doppel_switch_causal.md').write_text('# Causal bias/sense-switch decomposition\n\n'+o.to_markdown(index=False)+'\n')
 print(o.to_string(index=False))
if __name__=='__main__':main()
