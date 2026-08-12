#!/usr/bin/env python3
"""Validate and unblind two language-specific-control annotation packets."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from analyze_bilingual_annotations import kappa

SEM={"yes","no","uncertain"}
BLOCKING={"WRONG_LANGUAGE","WRONG_SENSE","UNNATURAL","POS_MISMATCH",
          "PROPER_NAME","MULTIWORD_OR_SUBSTRING","OTHER_BLOCKING"}


def load(path:Path, expected:int)->pd.DataFrame:
    frame=pd.read_csv(path,dtype=str,keep_default_na=False)
    if len(frame)!=expected or frame.annotation_id.nunique()!=expected:
        raise ValueError(f"{path}: expected {expected} unique rows")
    for column in ("word_is_valid_in_named_language_yes_no_uncertain",
                   "context_matches_meaning_yes_no_uncertain",
                   "pos_correct_yes_no_uncertain"):
        invalid=set(frame[column].str.strip())-SEM
        if invalid: raise ValueError(f"{path}:{column}: invalid/blank {sorted(invalid)}")
    for column in ("context_naturalness_1_to_5","confidence_1_to_5"):
        frame[column]=pd.to_numeric(frame[column],errors="coerce")
        if frame[column].isna().any() or not frame[column].between(1,5).all():
            raise ValueError(f"{path}:{column}: expected 1..5")
    frame["blocking"]=frame.confound_code.apply(
        lambda value:bool(BLOCKING & set(value.strip().split("+"))))
    return frame


def main()->None:
    parser=argparse.ArgumentParser()
    parser.add_argument("--annotator-1",type=Path,required=True)
    parser.add_argument("--annotator-2",type=Path,required=True)
    parser.add_argument("--key",type=Path,required=True)
    parser.add_argument("--output-dir",type=Path,required=True)
    args=parser.parse_args()
    key=pd.read_csv(args.key,dtype=str)
    expected=key.annotation_id.nunique()
    first,second=load(args.annotator_1,expected),load(args.annotator_2,expected)
    columns=["annotation_id","word_is_valid_in_named_language_yes_no_uncertain",
             "context_matches_meaning_yes_no_uncertain","context_naturalness_1_to_5",
             "pos_correct_yes_no_uncertain","blocking"]
    paired=first[columns].merge(second[columns],on="annotation_id",suffixes=("_a","_b"),
                                validate="one_to_one")
    paired=paired.merge(key.drop_duplicates("annotation_id")[["annotation_id","group","control_id"]],
                        on="annotation_id",validate="one_to_one")
    paired["retain_pre_adjudication"]=(
        (paired.word_is_valid_in_named_language_yes_no_uncertain_a=="yes") &
        (paired.word_is_valid_in_named_language_yes_no_uncertain_b=="yes") &
        (paired.context_matches_meaning_yes_no_uncertain_a=="yes") &
        (paired.context_matches_meaning_yes_no_uncertain_b=="yes") &
        (paired[["context_naturalness_1_to_5_a","context_naturalness_1_to_5_b"]].mean(axis=1)>=3) &
        (paired.pos_correct_yes_no_uncertain_a!="no") &
        (paired.pos_correct_yes_no_uncertain_b!="no") &
        ~paired.blocking_a & ~paired.blocking_b)
    summary={"rows":len(paired),"retained":int(paired.retain_pre_adjudication.sum()),
        "retention_rate":float(paired.retain_pre_adjudication.mean()),
        "retained_by_group":paired.groupby("group").retain_pre_adjudication.sum().to_dict()}
    for prefix in ("word_is_valid_in_named_language_yes_no_uncertain",
                   "context_matches_meaning_yes_no_uncertain","pos_correct_yes_no_uncertain"):
        summary[f"{prefix}_kappa"]=kappa(paired[f"{prefix}_a"],paired[f"{prefix}_b"])
    args.output_dir.mkdir(parents=True,exist_ok=True)
    paired.to_csv(args.output_dir/"private_aligned.csv",index=False)
    paired.loc[paired.retain_pre_adjudication,["control_id","group"]].to_csv(
        args.output_dir/"private_valid_control_ids.csv",index=False)
    (args.output_dir/"summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    print(json.dumps(summary,indent=2))


if __name__=="__main__": main()
