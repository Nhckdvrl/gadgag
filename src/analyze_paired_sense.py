#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import numpy as np,pandas as pd
ROOT=Path(__file__).resolve().parents[1];R=np.random.default_rng(20260810)
def main():
 rows=[]
 for p in (ROOT/'results'/'extensions').glob('paired_*.jsonl'):rows += [json.loads(x) for x in p.read_text().splitlines()]
 d=pd.DataFrame(rows);out=[]
 for (pair,model),g in d.groupby(['pair','model']):
  v=g.sense_switch.to_numpy();b=np.array([R.choice(v,len(v),replace=True).mean() for _ in range(10000)])
  out.append({'pair':pair,'model':model,'n':len(g),'l1_accuracy':g.l1_correct.mean(),'l2_accuracy':g.l2_correct.mean(),'both_accuracy':g.both_correct.mean(),'switch_positive':(g.sense_switch>0).mean(),'mean_sense_switch':v.mean(),'ci_low':np.quantile(b,.025),'ci_high':np.quantile(b,.975),'mean_candidate_prior':((g.margin_l1_for_l2+g.margin_l2_for_l2)/2).mean()})
 o=pd.DataFrame(out);o.to_csv(ROOT/'results'/'extensions'/'paired_sense_summary.csv',index=False);(ROOT/'reports'/'paired_sense.md').write_text('# Paired bilingual sense-switch pilot\n\n'+o.to_markdown(index=False)+'\n');print(o.to_string(index=False))
if __name__=='__main__':main()
