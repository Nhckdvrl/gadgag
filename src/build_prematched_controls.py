#!/usr/bin/env python3
"""Build a model-blind pre-matched ZH-JA lexical-control candidate set.

The builder uses open dictionaries for meaning/POS candidates and Tatoeba only
for naturally occurring context IDs.  It never reads target-model outcomes.
Raw licensed text stays under external/ and in ignored annotation packets.
"""
from __future__ import annotations

import argparse
import bz2
import csv
import gzip
import json
import re
import unicodedata
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

import jieba.posseg as pseg
import ahocorasick
import numpy as np
import pandas as pd
from fugashi import Tagger
from scipy.optimize import linear_sum_assignment
from transformers import AutoTokenizer
from wordfreq import zipf_frequency

from stingray_factorial import load_pair

ROOT = Path(__file__).resolve().parents[1]
JAPANESE = Tagger()
WORD = re.compile(r"[a-z]+")
CJK = re.compile(r"^[\u3400-\u9fff々〆ヶ]+$")
STOP = {"a", "an", "the", "of", "to", "one", "something", "someone",
        "used", "for", "and", "or", "be", "is", "as"}


def nfkc(value: str) -> str:
    return unicodedata.normalize("NFKC", value).strip()


def gloss_key(value: str) -> str:
    value = re.sub(r"\([^)]*\)", " ", value.casefold())
    tokens = [token for token in WORD.findall(value) if token not in STOP]
    return " ".join(tokens[:8])


def gloss_tokens(value: str) -> set[str]:
    return set(gloss_key(value).split())


def broad_pos_label(values: list[str]) -> str:
    joined = " ".join(values).casefold()
    if "verb" in joined or any(gloss.casefold().startswith("to ") for gloss in values):
        return "V"
    if "adjective" in joined or "adjectival" in joined:
        return "ADJ"
    if "adverb" in joined:
        return "ADV"
    if "noun" in joined:
        return "N"
    return "OTHER"


def pos_zh(sentence: str, target: str) -> str:
    for token in pseg.cut(sentence):
        if nfkc(token.word) == nfkc(target):
            return {"n": "N", "v": "V", "a": "ADJ", "d": "ADV"}.get(token.flag[:1],
                                                                              "OTHER")
    isolated = next(iter(pseg.cut(target)), None)
    return ({"n": "N", "v": "V", "a": "ADJ", "d": "ADV"}.get(isolated.flag[:1],
                                                                       "OTHER")
            if isolated else "OTHER")


def pos_ja(sentence: str, target: str) -> str:
    for token in JAPANESE(sentence):
        if nfkc(token.surface) == nfkc(target):
            return {"名詞": "N", "動詞": "V", "形容詞": "ADJ", "副詞": "ADV"}.get(
                token.feature.pos1, "OTHER")
    tokens = list(JAPANESE(target))
    if len(tokens) == 1:
        return {"名詞": "N", "動詞": "V", "形容詞": "ADJ", "副詞": "ADV"}.get(
            tokens[0].feature.pos1, "OTHER")
    return "OTHER"


def read_jmdict(path: Path) -> list[dict]:
    rows = []
    with gzip.open(path, "rb") as stream:
        for _, entry in ET.iterparse(stream, events=("end",)):
            if entry.tag != "entry":
                continue
            forms = [nfkc(node.text or "") for node in entry.findall("k_ele/keb")]
            priorities = {nfkc(node.findtext("keb", "")): bool(node.findall("ke_pri"))
                          for node in entry.findall("k_ele")}
            senses = entry.findall("sense")
            glosses = [nfkc(node.text or "") for sense in senses
                       for node in sense.findall("gloss")
                       if node.attrib.get("{http://www.w3.org/XML/1998/namespace}lang", "eng") == "eng"]
            pos_values = [node.text or "" for sense in senses for node in sense.findall("pos")]
            pos = broad_pos_label(pos_values)
            for form in forms:
                if CJK.fullmatch(form) and 1 <= len(form) <= 6 and glosses:
                    rows.append({"form": form, "glosses": glosses[:12], "pos": pos,
                                 "priority": priorities.get(form, False)})
            entry.clear()
    return rows


def read_cedict(path: Path) -> list[dict]:
    pattern = re.compile(r"^\S+\s+(\S+)\s+\[[^]]*\]\s+/(.*)/$")
    rows = []
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        for line in stream:
            match = pattern.match(line.strip())
            if not match:
                continue
            form, raw = nfkc(match.group(1)), match.group(2)
            glosses = [nfkc(value) for value in raw.split("/")
                       if value and not value.startswith(("variant of ", "see ", "surname "))]
            if CJK.fullmatch(form) and 1 <= len(form) <= 6 and glosses:
                rows.append({"form": form, "glosses": glosses[:12],
                             "pos": broad_pos_label(glosses)})
    return rows


def semantic_score(left: list[str], right: list[str]) -> tuple[float, str]:
    best = (0.0, "")
    for a in left:
        aa = gloss_tokens(a)
        if not aa:
            continue
        for b in right:
            bb = gloss_tokens(b)
            if not bb:
                continue
            score = len(aa & bb) / len(aa | bb)
            if gloss_key(a) == gloss_key(b):
                score = 1.0
            if score > best[0]:
                best = (score, a if len(a) <= len(b) else b)
    return best


def dictionary_candidates(japanese: list[dict], chinese: list[dict]) -> tuple[list[dict], list[dict]]:
    ja_by_form, zh_by_form = defaultdict(list), defaultdict(list)
    for row in japanese:
        ja_by_form[row["form"]].append(row)
    for row in chinese:
        zh_by_form[row["form"]].append(row)

    true = []
    for form in sorted(set(ja_by_form) & set(zh_by_form)):
        for ja in ja_by_form[form]:
            for zh in zh_by_form[form]:
                score, gloss = semantic_score(ja["glosses"], zh["glosses"])
                if score >= .5:
                    true.append({"id": f"true_{len(true):06d}", "group": "true_friend",
                                 "word_l1": form, "word_l2": form, "meaning": gloss,
                                 "pos_l1": zh["pos"], "pos_l2": ja["pos"],
                                 "semantic_score": score,
                                 "priority": bool(ja.get("priority"))})
                    break
            else:
                continue
            break

    # Exact normalized English glosses give high-precision different-form
    # translation candidates without consulting any evaluated model.
    ja_gloss, zh_gloss = defaultdict(list), defaultdict(list)
    for row in japanese:
        for gloss in row["glosses"]:
            key = gloss_key(gloss)
            if 1 <= len(key.split()) <= 5:
                ja_gloss[(key, row["pos"])].append(row)
    for row in chinese:
        for gloss in row["glosses"]:
            key = gloss_key(gloss)
            if 1 <= len(key.split()) <= 5:
                zh_gloss[(key, row["pos"])].append(row)
    translation, seen = [], set()
    for (key, pos) in sorted(set(ja_gloss) & set(zh_gloss)):
        if pos not in {"N", "V", "ADJ", "ADV"}:
            continue
        left = sorted(zh_gloss[(key, pos)], key=lambda x: (-zipf_frequency(x["form"], "zh"), x["form"]))[:8]
        right = sorted(ja_gloss[(key, pos)], key=lambda x: (-zipf_frequency(x["form"], "ja"), x["form"]))[:8]
        for zh in left:
            for ja in right:
                pair = (zh["form"], ja["form"])
                if zh["form"] == ja["form"] or pair in seen:
                    continue
                if zipf_frequency(zh["form"], "zh") < 2.0 or zipf_frequency(ja["form"], "ja") < 2.0:
                    continue
                seen.add(pair)
                translation.append({"id": f"translation_{len(translation):06d}",
                    "group": "translation_control", "word_l1": zh["form"],
                    "word_l2": ja["form"], "meaning": key, "pos_l1": pos,
                    "pos_l2": pos, "semantic_score": 1.0,
                    "priority": bool(ja.get("priority"))})
    return true, translation


def attach_contexts(rows: list[dict], chinese_path: Path, japanese_path: Path) -> list[dict]:
    wanted_zh = {row["word_l1"] for row in rows}
    wanted_ja = {row["word_l2"] for row in rows}
    contexts: dict[tuple[str, str], tuple[int, str]] = {}
    for language, path, wanted in (("zh", chinese_path, wanted_zh),
                                   ("ja", japanese_path, wanted_ja)):
        automaton = ahocorasick.Automaton()
        for target in wanted:
            automaton.add_word(target, target)
        automaton.make_automaton()
        with bz2.open(path, "rt", encoding="utf-8") as stream:
            reader = csv.reader(stream, delimiter="\t")
            for fields in reader:
                if len(fields) < 3:
                    continue
                sentence_id, sentence = int(fields[0]), nfkc(fields[2])
                if not 8 <= len(sentence) <= 80:
                    continue
                hits = {target for _, target in automaton.iter(sentence)}
                if not hits:
                    continue
                # Only tokenize sentences with a dictionary-candidate hit.
                tokens = ({nfkc(t.word) for t in pseg.cut(sentence)} if language == "zh"
                          else {nfkc(t.surface) for t in JAPANESE(sentence)})
                for target in tokens & hits:
                    key = (language, target)
                    if key not in contexts or len(sentence) < len(contexts[key][1]):
                        contexts[key] = (sentence_id, sentence)
    output = []
    zh_pos_cache, ja_pos_cache = {}, {}
    for row in rows:
        zh = contexts.get(("zh", row["word_l1"]))
        ja = contexts.get(("ja", row["word_l2"]))
        if not zh or not ja:
            continue
        if row["word_l1"] not in zh_pos_cache:
            zh_pos_cache[row["word_l1"]] = pos_zh(zh[1], row["word_l1"])
        if row["word_l2"] not in ja_pos_cache:
            ja_pos_cache[row["word_l2"]] = pos_ja(ja[1], row["word_l2"])
        output.append(row | {"context_l1_id": zh[0], "context_l1": zh[1],
                             "context_l2_id": ja[0], "context_l2": ja[1],
                             "pos_l1_context": zh_pos_cache[row["word_l1"]],
                             "pos_l2_context": ja_pos_cache[row["word_l2"]]})
    return output


def features(rows: list[dict], tokenizers: list) -> pd.DataFrame:
    output = []
    for row in rows:
        f1, f2 = zipf_frequency(row["word_l1"], "zh"), zipf_frequency(row["word_l2"], "ja")
        value = row | {"freq_l1": f1, "freq_l2": f2, "freq_ratio": f1 - f2,
                       "char_l1": len(row["word_l1"]), "char_l2": len(row["word_l2"]),
                       "gloss_tokens": len(gloss_key(row["meaning"]).split())}
        for index, tokenizer in enumerate(tokenizers, 1):
            value[f"tok{index}_l1"] = len(tokenizer(row["word_l1"], add_special_tokens=False).input_ids)
            value[f"tok{index}_l2"] = len(tokenizer(row["word_l2"], add_special_tokens=False).input_ids)
        output.append(value)
    return pd.DataFrame(output)


def false_features(data_root: Path, tokenizers: list) -> pd.DataFrame:
    rows = []
    for item in load_pair(data_root, "zh_ja", exact_only=True):
        row = {"id": item["id"], "group": "false_friend", "word_l1": item["word_l1"],
               "word_l2": item["word_l2"], "meaning": item["meaning_l1"],
               "meaning_l1": item["meaning_l1"], "meaning_l2": item["meaning_l2"],
               "context_l1": item["L1_S1"],
               "context_l2": item["L2_S2"], "pos_l1": pos_zh(item["L1_S1"], item["word_l1"]),
               "pos_l2": pos_ja(item["L2_S2"], item["word_l2"]),
               "pos_l1_context": pos_zh(item["L1_S1"], item["word_l1"]),
               "pos_l2_context": pos_ja(item["L2_S2"], item["word_l2"]),
               "semantic_score": 0.0, "priority": True,
               "context_l1_id": "stingray", "context_l2_id": "stingray"}
        rows.append(row)
    frame = features(rows, tokenizers)
    frame["gloss_tokens"] = [np.mean([len(gloss_key(x["meaning_l1"]).split()),
                                       len(gloss_key(x["meaning_l2"]).split())]) for x in rows]
    return frame


def match_group(false: pd.DataFrame, pool: pd.DataFrame, group: str,
                covariates: list[str], caliper: float) -> tuple[pd.DataFrame, pd.DataFrame]:
    pool = pool[(pool.freq_l1 >= 2.0) & (pool.freq_l2 >= 2.0)].copy()
    combined = pd.concat([false, pool], ignore_index=True)
    scale = combined[covariates].std().replace(0, 1)
    left = false[covariates].to_numpy() / scale.to_numpy()
    right = pool[covariates].to_numpy() / scale.to_numpy()
    gap = np.abs(left[:, None, :] - right[None, :, :])
    pos_ok = np.array([[(a.pos_l1 == b.pos_l1_context and
                         a.pos_l2 == b.pos_l2_context)
                        for _, b in pool.iterrows()] for _, a in false.iterrows()])
    feasible = (gap <= caliper).all(2) & pos_ok
    distance = (gap ** 2).sum(2)
    # Dummy columns let an unmatched false friend cost less than an infeasible pair;
    # feasible matches are selected first, then minimized by Mahalanobis-like distance.
    cost = np.concatenate([np.where(feasible, distance, 1e6),
                           np.full((len(false), len(false)), 1e4)], axis=1)
    rows, cols = linear_sum_assignment(cost)
    pairs = []
    for i, j in zip(rows, cols):
        if j < len(pool) and feasible[i, j]:
            pairs.append({"group": group, "false_id": false.iloc[i].id,
                          "control_id": pool.iloc[j].id, "distance": distance[i, j],
                          "max_standardized_gap": gap[i, j].max()})
    selected_ids = {row["control_id"] for row in pairs}
    return pd.DataFrame(pairs), pool[pool.id.isin(selected_ids)].copy()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--jmdict", type=Path, required=True)
    parser.add_argument("--cedict", type=Path, required=True)
    parser.add_argument("--japanese-sentences", type=Path, required=True)
    parser.add_argument("--chinese-sentences", type=Path, required=True)
    parser.add_argument("--stingray-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "data/prematched_controls")
    parser.add_argument("--caliper", type=float, default=1.0)
    parser.add_argument("--reuse-candidate-pool", action="store_true")
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    tokenizers = [AutoTokenizer.from_pretrained(name, local_files_only=True) for name in
                  ("Qwen/Qwen3-8B", "google/gemma-3-12b-it")]
    pool_path = args.output_dir / "candidate_pool_private.csv"
    if args.reuse_candidate_pool and pool_path.exists():
        frame = pd.read_csv(pool_path)
        japanese = chinese = true = translation = []
    else:
        japanese, chinese = read_jmdict(args.jmdict), read_cedict(args.cedict)
        true, translation = dictionary_candidates(japanese, chinese)
        candidates = attach_contexts(true + translation, args.chinese_sentences,
                                     args.japanese_sentences)
        frame = features(candidates, tokenizers)
        frame.to_csv(pool_path, index=False)
    false = false_features(args.stingray_root, tokenizers)
    covariates = ["freq_l1", "freq_l2", "freq_ratio", "char_l1", "char_l2",
                  "gloss_tokens", "tok1_l1", "tok1_l2", "tok2_l1", "tok2_l2"]
    matches, selected = [], []
    for group in ("true_friend", "translation_control"):
        pair, values = match_group(false, frame[frame.group == group], group,
                                   covariates, args.caliper)
        matches.append(pair); selected.append(values)
    match_frame = pd.concat(matches, ignore_index=True)
    selected_frame = pd.concat(selected, ignore_index=True)
    # Private packet retains licensed source strings; public frozen table uses IDs,
    # forms, features and hashes only.
    private = selected_frame.merge(match_frame, left_on=["id", "group"],
                                   right_on=["control_id", "group"], validate="one_to_one")
    private.to_csv(args.output_dir / "private_control_candidates.csv", index=False)
    public_columns = ["group", "false_id", "control_id", "distance",
                      "max_standardized_gap"]
    match_frame[public_columns].to_csv(
        args.output_dir / "pairwise_1sd_diagnostic.csv", index=False)
    diagnostics = {"false_friends": len(false),
        "jmdict_candidates": len(japanese) if japanese else "cached",
        "cedict_candidates": len(chinese) if chinese else "cached",
        "true_candidates_before_context": len(true) if true else "cached",
        "translation_candidates_before_context": len(translation) if translation else "cached",
        "candidates_with_bilingual_context": int(len(frame)),
        "candidates_with_context_by_group": frame.groupby("group").size().to_dict(),
        "actual_context_pos_pairs": {
            "|".join(key): int(value) for key, value in frame.groupby(
                ["group", "pos_l1_context", "pos_l2_context"]).size().items()},
        "caliper": args.caliper,
        "covariates": covariates,
        "matched": match_frame.groupby("group").size().to_dict() if len(match_frame) else {}}
    (args.output_dir / "build_manifest.json").write_text(json.dumps(diagnostics, indent=2) + "\n")
    print(json.dumps(diagnostics, indent=2))


if __name__ == "__main__":
    main()
