#!/usr/bin/env python3
"""Executable evidence contract for the revised research verdict."""
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
def main():
 f=pd.read_csv(ROOT/'results/extensions/factorial_summary.csv');s=f[f.effect=='semantic']
 assert set(f.loc[f.pair=='zh_ja','n'])=={27}
 assert set(f.loc[f.pair=='id_tl','n'])=={33}
 full=s[s.condition=='full'];assert len(full)==96 and (full.ci_low>0).sum()>=90
 chat=full[full.prompt_mode=='chat'];assert len(chat)==48 and (chat.ci_low>0).all()
 assert (s[s.condition=='masked'].ci_low>0).sum()>=90
 assert (s[s.condition=='language_only'].ci_low>0).sum()<=5
 assert (s[s.condition=='language_only'].ci_high<0).sum()<=5
 assert (s[s.condition=='shuffled'].ci_low>0).sum()<=5
 assert (s[s.condition=='shuffled'].ci_high<0).sum()<=5
 c=pd.read_csv(ROOT/'results/extensions/factorial_contrasts.csv');q=c[c.contrast=='full_minus_language_only'];assert len(q)==96 and (q.ci_low>0).sum()>=90
 g=pd.read_csv(ROOT/'results/extensions/gloss_variant_summary.csv');assert len(g)==48 and (g.ci_low>0).all()
 n=pd.read_csv(ROOT/'results/extensions/natural_context_summary.csv');x=n[n.comparison=='masked_minus_shuffled'];assert len(x)==96 and (x.ci_low>0).sum()>=80
 x=x[x.prompt_mode=='chat'];assert len(x)==48 and (x.ci_low>0).sum()>=45
 d=pd.read_csv(ROOT/'results/extensions/decision_calibration_aggregate.csv').pivot(index='pair',columns='calibration',values='both_accuracy');assert (d.content_free_calibrated>d.raw).all()
 old=pd.read_csv(ROOT/'results/extensions/context_lift_summary.csv');x=old[(old.condition=='conflict')&(old.metric=='dlift')].iloc[0];assert x.ci_low<0<x.ci_high
 print('construct validation passed: overwrite KILL; crossed-context audit CONDITIONAL GO')
if __name__=='__main__':main()
