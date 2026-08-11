#!/usr/bin/env python3
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
def main():
 f=pd.read_csv(ROOT/'results/extensions/factorial_summary.csv');s=f[f.effect=='semantic'];rows=[]
 for c,g in s.groupby('condition'):
  rows.append({'family':'factorial_semantic','test':c,'variants':len(g),'ci_positive':int((g.ci_low>0).sum()),'ci_negative':int((g.ci_high<0).sum()),'median_effect':g.estimate.median()})
 full_chat=s[(s.condition=='full')&(s.prompt_mode=='chat')]
 rows.append({'family':'factorial_semantic','test':'full_official_chat','variants':len(full_chat),'ci_positive':int((full_chat.ci_low>0).sum()),'ci_negative':int((full_chat.ci_high<0).sum()),'median_effect':full_chat.estimate.median()})
 x=pd.read_csv(ROOT/'results/extensions/factorial_contrasts.csv')
 for c,g in x.groupby('contrast'):
  rows.append({'family':'paired_contrast','test':c,'variants':len(g),'ci_positive':int((g.ci_low>0).sum()),'ci_negative':int((g.ci_high<0).sum()),'median_effect':g.estimate.median()})
 g=pd.read_csv(ROOT/'results/extensions/gloss_variant_summary.csv')
 rows.append({'family':'lexical_gloss','test':'aggregate_semantic','variants':len(g),'ci_positive':int((g.ci_low>0).sum()),'ci_negative':int((g.ci_high<0).sum()),'median_effect':g.semantic_effect.median()})
 n=pd.read_csv(ROOT/'results/extensions/natural_context_summary.csv')
 for comparison,group in n.groupby('comparison'):
  rows.append({'family':'natural_diagonal','test':comparison,'variants':len(group),'ci_positive':int((group.ci_low>0).sum()),'ci_negative':int((group.ci_high<0).sum()),'median_effect':group.estimate.median()})
 o=pd.DataFrame(rows);o.to_csv(ROOT/'results/extensions/construct_gate_summary.csv',index=False)
 c=pd.read_csv(ROOT/'results/extensions/calibration_summary.csv');c=c[c.normalization=='mean'];decision=c.groupby(['pair','calibration'])[['l1_accuracy','l2_accuracy','both_accuracy','stingray_bias','stingray_comprehension']].mean().reset_index();decision.to_csv(ROOT/'results/extensions/decision_calibration_aggregate.csv',index=False)
 report='# Final construct decision\n\n## Construct gates\n\n'+o.to_markdown(index=False)+'\n\n## Decision-level calibration (averaged over models, modes, wrappers)\n\n'+decision.to_markdown(index=False)+'\n\n**Verdict:** conditional GO on the measurement question; KILL the semantic-overwrite claim and the causal “candidate prior” interpretation of the old midpoint. Four full-context failures are confined to Gemma-3-12B plain scoring; all official-chat variants pass. Natural correct contexts beat matched shuffled contexts much more consistently than they beat an explicit language-plus-target cue, which is a central limitation and part of the proposed measurement question.\n'
 (ROOT/'reports/final_construct_decision.md').write_text(report);print(o.to_string(index=False));print(decision.to_string(index=False))
if __name__=='__main__':main()
