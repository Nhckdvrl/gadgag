#!/usr/bin/env python3
"""Build outcome-blind Chinese- and Japanese-specific lexical controls."""
from __future__ import annotations

import argparse
import bz2
import csv
import json
from functools import lru_cache
from pathlib import Path

import ahocorasick
import jieba.posseg as pseg
import pandas as pd
from fugashi import Tagger
from transformers import AutoTokenizer
from wordfreq import zipf_frequency

from build_prematched_controls import (CJK, false_features, gloss_key, nfkc,
                                       pos_ja, pos_zh, read_cedict, read_jmdict)

ROOT = Path(__file__).resolve().parents[1]
JAPANESE = Tagger()
COVARIATES = ["frequency", "char_length", "gloss_tokens", "tok1", "tok2"]


@lru_cache(maxsize=None)
def frequency(form: str, language: str) -> float:
    return zipf_frequency(form, language)


def one_per_form(rows: list[dict], excluded: set[str], language: str) -> list[dict]:
    candidates = []
    seen = set()
    # Frequency is constant for duplicate dictionary rows with the same form;
    # priority first is sufficient and avoids expensive scoring during sorting.
    for row in sorted(rows, key=lambda value: (-bool(value.get("priority")), value["form"])):
        form = nfkc(row["form"])
        if form in excluded or form in seen or len(form) != 2 or not CJK.fullmatch(form):
            continue
        gloss = next((value for value in row["glosses"]
                      if 1 <= len(gloss_key(value).split()) <= 5), None)
        if not gloss or frequency(form, language) < 2:
            continue
        seen.add(form)
        candidates.append({"word": form, "meaning": gloss,
                           "dictionary_pos": row["pos"]})
    return candidates


def attach_context(rows: list[dict], path: Path, language: str) -> list[dict]:
    wanted = {row["word"] for row in rows}
    automaton = ahocorasick.Automaton()
    for target in wanted:
        automaton.add_word(target, target)
    automaton.make_automaton()
    contexts: dict[str, tuple[int, str, str]] = {}
    with bz2.open(path, "rt", encoding="utf-8") as stream:
        for fields in csv.reader(stream, delimiter="\t"):
            if len(fields) < 3:
                continue
            sentence_id, sentence = int(fields[0]), nfkc(fields[2])
            if not 8 <= len(sentence) <= 80:
                continue
            hits = {target for _, target in automaton.iter(sentence)}
            if not hits:
                continue
            tokens = ({nfkc(token.word) for token in pseg.cut(sentence)} if language == "zh"
                      else {nfkc(token.surface) for token in JAPANESE(sentence)})
            for target in hits & tokens:
                pos = pos_zh(sentence, target) if language == "zh" else pos_ja(sentence, target)
                if pos not in {"N", "V", "ADJ", "ADV"}:
                    continue
                previous = contexts.get(target)
                if previous is None or len(sentence) < len(previous[1]):
                    contexts[target] = (sentence_id, sentence, pos)
    return [row | {"context_id": contexts[row["word"]][0],
                   "context": contexts[row["word"]][1],
                   "contextual_pos": contexts[row["word"]][2]}
            for row in rows if row["word"] in contexts]


def featurize(rows: list[dict], language: str, group: str, tokenizers: list) -> pd.DataFrame:
    output = []
    for index, row in enumerate(rows):
        output.append(row | {"id": f"{group}_{index:06d}", "group": group,
            "language": language, "frequency": frequency(row["word"], language),
            "char_length": len(row["word"]),
            "gloss_tokens": len(gloss_key(row["meaning"]).split()),
            "tok1": len(tokenizers[0](row["word"], add_special_tokens=False).input_ids),
            "tok2": len(tokenizers[1](row["word"], add_special_tokens=False).input_ids)})
    return pd.DataFrame(output)


def target_sides(stingray_root: Path, tokenizers: list,
                 eligible_path: Path) -> pd.DataFrame:
    false = false_features(stingray_root, tokenizers)
    eligible = set(pd.read_csv(eligible_path, dtype=str).false_id)
    false = false[false.id.isin(eligible)]
    rows = []
    for _, value in false.iterrows():
        for language, suffix in (("zh", "l1"), ("ja", "l2")):
            rows.append({"false_id": value.id, "language": language,
                "word": value[f"word_{suffix}"], "meaning": value[f"meaning_{suffix}"],
                "context": value[f"context_{suffix}"], "contextual_pos": value[f"pos_{suffix}"],
                "frequency": value[f"freq_{suffix}"], "char_length": value[f"char_{suffix}"],
                "gloss_tokens": len(gloss_key(value[f"meaning_{suffix}"]).split()),
                "tok1": value[f"tok1_{suffix}"], "tok2": value[f"tok2_{suffix}"]})
    return pd.DataFrame(rows)


def shortlist(target: pd.DataFrame, pool: pd.DataFrame, neighbors: int) -> pd.DataFrame:
    scale = pd.concat([target, pool])[COVARIATES].std().replace(0, 1)
    rows = []
    for _, value in target.iterrows():
        eligible = pool[pool.contextual_pos == value.contextual_pos].copy()
        gap = ((eligible[COVARIATES].to_numpy(float) -
                value[COVARIATES].to_numpy(float)) / scale.to_numpy(float))
        eligible["design_distance"] = (gap ** 2).sum(1)
        eligible["max_standardized_gap"] = abs(gap).max(1)
        for _, control in eligible.nsmallest(neighbors, "design_distance").iterrows():
            rows.append({"false_id": value.false_id} | control.to_dict())
    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--jmdict", type=Path, required=True)
    parser.add_argument("--cedict", type=Path, required=True)
    parser.add_argument("--japanese-sentences", type=Path, required=True)
    parser.add_argument("--chinese-sentences", type=Path, required=True)
    parser.add_argument("--stingray-root", type=Path, required=True)
    parser.add_argument("--eligible-false-matching", type=Path, required=True)
    parser.add_argument("--neighbors", type=int, default=100)
    parser.add_argument("--output-dir", type=Path,
                        default=ROOT / "data/language_specific_controls")
    args = parser.parse_args()
    tokenizers = [AutoTokenizer.from_pretrained(name, local_files_only=True) for name in
                  ("Qwen/Qwen3-8B", "google/gemma-3-12b-it")]
    japanese, chinese = read_jmdict(args.jmdict), read_cedict(args.cedict)
    ja_forms, zh_forms = {row["form"] for row in japanese}, {row["form"] for row in chinese}
    zh_candidates = one_per_form(chinese, ja_forms, "zh")
    ja_candidates = one_per_form(japanese, zh_forms, "ja")
    zh = featurize(attach_context(zh_candidates, args.chinese_sentences, "zh"), "zh",
                   "language_specific_zh", tokenizers)
    ja = featurize(attach_context(ja_candidates, args.japanese_sentences, "ja"), "ja",
                   "language_specific_ja", tokenizers)
    pool = pd.concat([zh, ja], ignore_index=True)
    targets = target_sides(args.stingray_root, tokenizers, args.eligible_false_matching)
    selected = []
    for language in ("zh", "ja"):
        selected.append(shortlist(targets[targets.language == language],
                                  pool[pool.language == language], args.neighbors))
    selected = pd.concat(selected, ignore_index=True)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    pool.to_csv(args.output_dir / "private_candidate_pool.csv", index=False)
    selected.to_csv(args.output_dir / "private_shortlist.csv", index=False)
    selected[["false_id", "group", "id", "context_id", "design_distance",
              "max_standardized_gap"]].rename(columns={"id": "control_id"}).to_csv(
                  args.output_dir / "shortlist_ids.csv", index=False)
    manifest = {"design_stage": "outcome-blind language-specific shortlist",
        "absence_definition": "NFKC exact form absent from the other language dictionary",
        "false_items_per_language": targets.groupby("language").false_id.nunique().to_dict(),
        "dictionary_unique_before_context": {"zh": len(zh_candidates),
                                              "ja": len(ja_candidates)},
        "natural_context_pool": pool.groupby("language").size().to_dict(),
        "shortlist_rows": selected.groupby("language").size().to_dict(),
        "unique_shortlist_controls": selected.groupby("language").id.nunique().to_dict(),
        "neighbors_per_false": args.neighbors, "covariates": COVARIATES,
        "target_models_read": False}
    (args.output_dir / "build_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
