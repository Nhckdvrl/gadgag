#!/usr/bin/env python3
"""Strict covariate matching for false-friend language-excess effects."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import jieba.posseg as pseg
import numpy as np
import pandas as pd
from fugashi import Tagger
from scipy.optimize import linear_sum_assignment
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import maximum_bipartite_matching
from transformers import AutoTokenizer
from wordfreq import zipf_frequency

from evaluate_causal_gating import common_controls
from stingray_factorial import load_pair

ROOT = Path(__file__).resolve().parents[1]
RNG = np.random.default_rng(20260813)
JAPANESE = Tagger()


def broad_pos_zh(sentence: str, target: str) -> str:
    for token in pseg.cut(sentence):
        if token.word == target:
            head = token.flag[:1]
            return {"n": "N", "v": "V", "a": "ADJ", "d": "ADV"}.get(head, "OTHER")
    return "UNKNOWN"


def broad_pos_ja(sentence: str, target: str) -> str:
    for token in JAPANESE(sentence):
        if token.surface == target:
            pos = token.feature.pos1
            return {"名詞": "N", "動詞": "V", "形容詞": "ADJ", "副詞": "ADV"}.get(pos,
                                                                                       "OTHER")
    return "UNKNOWN"


def item_definitions(data_root: Path, limit: int):
    false = load_pair(data_root, "zh_ja", exact_only=True)[:limit]
    true, translation = common_controls(data_root, "zh_ja", limit)
    rows = []
    for group, items in (("false_friend", false), ("true_friend", true),
                         ("translation_control", translation)):
        for item in items:
            rows.append({"id": item["id"], "group": group,
                "w1": item["word_l1"], "w2": item["word_l2"],
                "m1": item["meaning_l1"], "m2": item["meaning_l2"],
                "c1": item["L1_S1"], "c2": item["L2_S1" if group != "false_friend" else "L2_S2"]})
    return rows


def covariates(data_root: Path, model_name: str, tag: str, limit: int):
    tokenizer = AutoTokenizer.from_pretrained(model_name, local_files_only=True)
    rows = item_definitions(data_root, limit)
    raw = [json.loads(line) for line in (ROOT / "results/extensions" /
                                         f"causal_gating_{tag}.jsonl").read_text().splitlines()]
    scores = pd.DataFrame(raw)
    observed = scores[scores.layer == -2].pivot(
        index=["id", "group", "language", "sense"], columns="candidate_sense",
        values="mean_logp").reset_index()
    observed["margin"] = observed[2] - observed[1]
    observed["signed"] = np.where(observed.sense == 2, observed.margin, -observed.margin)
    difficulty = observed.groupby("id").signed.mean().to_dict()
    output = []
    for value in rows:
        tok1 = len(tokenizer(value["w1"], add_special_tokens=False).input_ids)
        tok2 = len(tokenizer(value["w2"], add_special_tokens=False).input_ids)
        gloss1 = len(tokenizer(value["m1"], add_special_tokens=False).input_ids)
        gloss2 = len(tokenizer(value["m2"], add_special_tokens=False).input_ids)
        f1, f2 = zipf_frequency(value["w1"], "zh"), zipf_frequency(value["w2"], "ja")
        output.append(value | {"freq_l1": f1, "freq_l2": f2, "freq_ratio": f1 - f2,
            "token_l1": tok1, "token_l2": tok2, "token_total": tok1 + tok2,
            "gloss_mean_tokens": (gloss1 + gloss2) / 2,
            "gloss_token_gap": abs(gloss1 - gloss2),
            "baseline_difficulty": difficulty[value["id"]],
            "pos_l1": broad_pos_zh(value["c1"], value["w1"]),
            "pos_l2": broad_pos_ja(value["c2"], value["w2"])})
    return pd.DataFrame(output)


def language_effects(tag: str):
    records = [json.loads(line) for line in (ROOT / "results/extensions" /
               f"causal_gating_{tag}.jsonl").read_text().splitlines()]
    data = pd.DataFrame(records)
    data = data[data.layer >= 0]
    maximum = data.layer.max()
    data = data[(data.layer / maximum >= .75) & (data.layer / maximum < 1.0)]
    candidate = data.pivot(index=["id", "group", "layer", "language", "sense"],
                           columns="candidate_sense", values="mean_logp").reset_index()
    candidate["margin"] = candidate[2] - candidate[1]
    effects = []
    for (item_id, group, layer), frame in candidate.groupby(["id", "group", "layer"]):
        if group == "monolingual_polysemy":
            continue
        if group == "false_friend":
            table = frame.pivot(index="language", columns="sense", values="margin")
            effect = ((table.loc[2, 1] + table.loc[2, 2]) -
                      (table.loc[1, 1] + table.loc[1, 2])) / 2
        else:
            table = frame.set_index("language").margin
            effect = table.loc[2] - table.loc[1]
        effects.append({"id": item_id, "group": group, "layer": layer,
                        "language_effect": effect})
    return pd.DataFrame(effects).groupby(["id", "group"]).language_effect.mean().reset_index()


def bootstrap(values):
    values = np.asarray(values); draws = values[RNG.integers(0, len(values),
                                                               (5000, len(values)))].mean(1)
    return np.quantile(draws, [.025, .975])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--items-per-group", type=int, default=20)
    args = parser.parse_args()
    models = {"qwen3_8b": "Qwen/Qwen3-8B", "gemma3_12b": "google/gemma-3-12b-it"}
    covars = ["freq_l1", "freq_l2", "freq_ratio", "token_l1", "token_l2",
              "token_total", "gloss_mean_tokens", "gloss_token_gap", "baseline_difficulty"]
    balance_rows, result_rows, match_rows, overlap_rows = [], [], [], []
    for tag, model_name in models.items():
        frame = covariates(args.data_root, model_name, tag, args.items_per_group)
        outcomes = language_effects(tag)
        frame = frame.merge(outcomes, on=["id", "group"], validate="one_to_one")
        false = frame[frame.group == "false_friend"].copy()
        for control_name in ("true_friend", "translation_control"):
            control = frame[frame.group == control_name].copy()
            combined = pd.concat([false, control])
            mean, std = combined[covars].mean(), combined[covars].std().replace(0, 1)
            left, right = (false[covars] - mean) / std, (control[covars] - mean) / std
            distance = ((left.to_numpy()[:, None, :] - right.to_numpy()[None, :, :]) ** 2).sum(2)
            # Strong but finite POS mismatch penalties retain a complete assignment
            # while making any unavoidable mismatch visible in the balance table.
            for i, (_, a) in enumerate(false.iterrows()):
                for j, (_, b) in enumerate(control.iterrows()):
                    distance[i, j] += 5 * (a.pos_l1 != b.pos_l1) + 5 * (a.pos_l2 != b.pos_l2)
            # A hard common-support audit precedes any outcome interpretation.
            # Feasible pairs must match broad POS in both languages and fall
            # within the stated per-covariate standardized caliper on *every*
            # continuous covariate.  Zero pairs at 1 SD is a failed strict gate.
            raw_gap = np.abs(left.to_numpy()[:, None, :] - right.to_numpy()[None, :, :])
            pos_ok = np.array([[(a.pos_l1 == b.pos_l1 and a.pos_l2 == b.pos_l2)
                                for _, b in control.iterrows()]
                               for _, a in false.iterrows()])
            for caliper in (1.0, 1.5, 2.0):
                feasible = (raw_gap <= caliper).all(2) & pos_ok
                matching = maximum_bipartite_matching(csr_matrix(feasible),
                                                       perm_type="column")
                matched = [(i, j) for i, j in enumerate(matching) if j >= 0]
                differences_caliper = np.array([
                    false.iloc[i].language_effect - control.iloc[j].language_effect
                    for i, j in matched])
                if len(differences_caliper) >= 2:
                    cal_low, cal_high = bootstrap(differences_caliper)
                    cal_effect = differences_caliper.mean()
                else:
                    cal_effect = cal_low = cal_high = np.nan
                overlap_rows.append({"model": tag, "control": control_name,
                    "caliper_sd_each_covariate": caliper,
                    "exact_pos_pairs": len(matched), "available_false": len(false),
                    "available_control": len(control), "language_excess": cal_effect,
                    "ci_low": cal_low, "ci_high": cal_high})
            rows, cols = linear_sum_assignment(distance)
            matched_false, matched_control = false.iloc[rows], control.iloc[cols]
            differences = (matched_false.language_effect.to_numpy() -
                           matched_control.language_effect.to_numpy())
            low, high = bootstrap(differences)
            result_rows.append({"model": tag, "control": control_name,
                "n_pairs": len(differences), "late_window": "0.75<=relative_depth<1.0",
                "matched_language_excess": differences.mean(), "ci_low": low, "ci_high": high,
                "positive_rate": (differences > 0).mean(),
                "pos_l1_match_rate": (matched_false.pos_l1.to_numpy() ==
                                      matched_control.pos_l1.to_numpy()).mean(),
                "pos_l2_match_rate": (matched_false.pos_l2.to_numpy() ==
                                      matched_control.pos_l2.to_numpy()).mean()})
            for i, j in zip(rows, cols):
                match_rows.append({"model": tag, "control": control_name,
                    "false_id": false.iloc[i].id, "control_id": control.iloc[j].id,
                    "distance": distance[i, j]})
            for covar in covars:
                before = (false[covar].mean() - control[covar].mean()) / combined[covar].std()
                after = ((matched_false[covar].mean() - matched_control[covar].mean()) /
                         combined[covar].std())
                balance_rows.append({"model": tag, "control": control_name,
                    "covariate": covar, "smd_before": before, "smd_after": after})
    results, balance = pd.DataFrame(result_rows), pd.DataFrame(balance_rows)
    results.to_csv(ROOT / "results/extensions/causal_matched_effects.csv", index=False)
    balance.to_csv(ROOT / "results/extensions/causal_matching_balance.csv", index=False)
    pd.DataFrame(match_rows).to_csv(ROOT / "results/extensions/causal_matching_pairs.csv", index=False)
    overlap = pd.DataFrame(overlap_rows)
    overlap.to_csv(ROOT / "results/extensions/causal_matching_overlap.csv", index=False)
    (ROOT / "reports/causal_matching.md").write_text(
        "# Strict covariate-matched causal language excess\n\n" + results.to_markdown(index=False) +
        "\n\nThe complete assignment below is diagnostic only when balance is poor. "
        "The hard gate requires exact broad POS in both languages plus common support "
        "on every continuous covariate.\n\n## Hard common-support audit\n\n" +
        overlap.to_markdown(index=False) + "\n\n## Balance\n\n" +
        balance.to_markdown(index=False) + "\n")
    print(results.to_string(index=False)); print(overlap.to_string(index=False))


if __name__ == "__main__":
    main()
