#!/usr/bin/env python3
"""Layer-wise residual-stream patching for language gating versus ordinary WSD.

The intervention replaces only the answer-boundary residual state in a neutral
recipient prompt with the corresponding state from a contextual donor prompt.
Candidate outputs are English definitions in every cross-lingual condition.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import pandas as pd
import torch
from nltk.corpus import wordnet as wn
from transformers import AutoModelForCausalLM, AutoTokenizer

from scoring_v2 import Score, score_prepared
from stingray_factorial import LANGUAGES, load_pair, norm

ROOT = Path(__file__).resolve().parents[1]


def common_controls(data_root: Path, pair: str, limit: int) -> tuple[list[dict], list[dict]]:
    frame = pd.read_csv(data_root / f"{pair}_common_words.csv")
    true, translation = [], []
    for index, row in frame.iterrows():
        w1, w2 = str(row.Cognates_L1).strip(), str(row.Cognates_L2).strip()
        m1, m2 = str(row["Meaning in L1"]).strip(), str(row["Meaning in L2"]).strip()
        if norm(m1).casefold() != norm(m2).casefold():
            continue
        item = {"id": f"{pair}_common_{index:03d}", "word_l1": w1, "word_l2": w2,
                "meaning_l1": m1, "meaning_l2": m1,
                "L1_S1": str(row.L1).strip(), "L2_S1": str(row.L2).strip()}
        (true if norm(w1) == norm(w2) else translation).append(item)
    return true[:limit], translation[:limit]


def monolingual_polysemy(limit: int) -> list[dict]:
    rows = []
    # Frequency counts prioritize familiar senses; different lexicographer files
    # exclude many merely fine-grained same-domain distinctions.
    for lemma in wn.all_lemma_names(lang="eng"):
        if "_" in lemma or not lemma.isalpha() or len(lemma) < 3:
            continue
        senses = []
        for synset in wn.synsets(lemma):
            example = next((x for x in synset.examples()
                            if re.search(rf"(?i)\b{re.escape(lemma)}\b", x)), None)
            if example:
                count = max((x.count() for x in synset.lemmas()
                             if x.name().casefold() == lemma.casefold()), default=0)
                senses.append((count, synset.lexname(), synset.definition(), example))
        senses.sort(reverse=True)
        pair = next(((a, b) for i, a in enumerate(senses) for b in senses[i + 1:]
                     if a[1] != b[1]), None)
        if pair:
            a, b = pair
            rows.append((a[0] + b[0], {"id": f"mono_{lemma}", "word": lemma,
                                       "meaning_l1": a[2], "meaning_l2": b[2],
                                       "S1": a[3], "S2": b[3]}))
    rows.sort(key=lambda x: x[0], reverse=True)
    return [row for _, row in rows[:limit]]


def build_donors(data_root: Path, pair: str, limit: int) -> list[dict]:
    names = LANGUAGES[pair]
    donors = []
    false = load_pair(data_root, pair, exact_only=True)[:limit]
    for item in false:
        neutral_language = names[0]
        for language in (1, 2):
            for sense in (1, 2):
                donors.append({
                    "id": item["id"], "group": "false_friend", "language": language,
                    "sense": sense, "word": item["word"],
                    "neutral_word": item["word"],
                    "donor": item[f"L{language}_S{sense}"],
                    "neutral_language": neutral_language,
                    "meaning1": item["meaning_l1"], "meaning2": item["meaning_l2"],
                    "language_name": names[language - 1],
                })
    true, translation = common_controls(data_root, pair, limit)
    combined = [("true_friend", row) for row in true]
    combined += [("translation_control", row) for row in translation]
    for group, item in combined:
        # The matched foil is deterministic and comes from the next available
        # common-word item, never from the donor context itself.
        pool = true + translation
        foil = pool[(pool.index(item) + 1) % len(pool)]["meaning_l1"]
        for language in (1, 2):
            donors.append({
                "id": item["id"], "group": group, "language": language, "sense": 1,
                "word": item[f"word_l{language}"], "donor": item[f"L{language}_S1"],
                "neutral_word": item["word_l1"], "neutral_language": names[0],
                "language_name": names[language - 1],
                "meaning1": item["meaning_l1"], "meaning2": foil,
            })
    for item in monolingual_polysemy(limit):
        for sense in (1, 2):
            donors.append({"id": item["id"], "group": "monolingual_polysemy",
                           "language": 1, "sense": sense, "word": item["word"],
                           "neutral_word": item["word"],
                           "donor": item[f"S{sense}"], "neutral_language": "English",
                           "language_name": "English", "meaning1": item["meaning_l1"],
                           "meaning2": item["meaning_l2"]})
    return donors


def messages(row: dict, neutral: bool) -> list[dict[str, str]]:
    target = row["neutral_word"] if neutral else row["word"]
    language = row["neutral_language"] if neutral else row["language_name"]
    context = f'The isolated target expression is "{target}".' if neutral else row["donor"]
    text = (f'The following context is in {language}. Determine the contextual '
            f'meaning of "{target}". Give the English meaning only.\n'
            f"Context: {context}\nMeaning:")
    return [{"role": "user", "content": text}]


def chat_prefix(tokenizer, value) -> list[int]:
    kwargs = {"tokenize": True, "add_generation_prompt": True}
    if "qwen3" in str(tokenizer.name_or_path).casefold():
        kwargs["enable_thinking"] = False
    return list(tokenizer.apply_chat_template(value, **kwargs))


def prepare_local(tokenizer, value, candidate: str) -> tuple[list[int], int]:
    prefix = chat_prefix(tokenizer, value)
    continuation = tokenizer(candidate, add_special_tokens=False).input_ids
    return prefix + list(continuation), len(prefix)


def score_requests(model, tokenizer, requests, batch_size):
    return score_prepared(model, tokenizer,
                          [prepare_local(tokenizer, m, c) for m, c in requests], batch_size)


def layer_list(model, stride: int):
    candidates = [
        getattr(getattr(model, "model", None), "layers", None),
        getattr(getattr(model, "language_model", None), "layers", None),
        getattr(getattr(getattr(model, "model", None), "language_model", None), "layers", None),
        getattr(getattr(getattr(getattr(model, "model", None), "language_model", None),
                        "model", None), "layers", None),
    ]
    layers = next((value for value in candidates if value is not None), None)
    if layers is None:
        raise AttributeError("could not locate decoder layers")
    selected = list(range(0, len(layers), stride))
    if len(layers) - 1 not in selected:
        selected.append(len(layers) - 1)
    return layers, selected


@torch.inference_mode()
def donor_states(model, tokenizer, donors: list[dict], selected: list[int],
                 batch_size: int) -> list[dict[int, torch.Tensor]]:
    device = next(model.parameters()).device
    pad = tokenizer.pad_token_id if tokenizer.pad_token_id is not None else tokenizer.eos_token_id
    output = []
    for offset in range(0, len(donors), batch_size):
        batch = donors[offset:offset + batch_size]
        ids = [chat_prefix(tokenizer, messages(row, False)) for row in batch]
        width = max(map(len, ids))
        x = torch.full((len(ids), width), pad, dtype=torch.long, device=device)
        mask = torch.zeros_like(x)
        for i, values in enumerate(ids):
            x[i, :len(values)] = torch.tensor(values, device=device)
            mask[i, :len(values)] = 1
        result = model(input_ids=x, attention_mask=mask, output_hidden_states=True,
                       use_cache=False)
        for i, values in enumerate(ids):
            output.append({layer: result.hidden_states[layer + 1][i, len(values) - 1]
                           .detach().cpu() for layer in selected})
        del result
    return output


@torch.inference_mode()
def patched_scores(model, tokenizer, layers, layer: int, prepared, vectors,
                   batch_size: int) -> list[Score]:
    device = next(model.parameters()).device
    pad = tokenizer.pad_token_id if tokenizer.pad_token_id is not None else tokenizer.eos_token_id
    results = []
    for offset in range(0, len(prepared), batch_size):
        batch = prepared[offset:offset + batch_size]
        vec = torch.stack(vectors[offset:offset + batch_size]).to(device)
        width = max(len(ids) for ids, _ in batch)
        x = torch.full((len(batch), width), pad, dtype=torch.long, device=device)
        mask = torch.zeros_like(x)
        starts = []
        for i, (ids, start) in enumerate(batch):
            x[i, :len(ids)] = torch.tensor(ids, device=device)
            mask[i, :len(ids)] = 1
            starts.append(start)

        def hook(_module, _inputs, output):
            hidden = output[0] if isinstance(output, tuple) else output
            patched = hidden.clone()
            rows = torch.arange(len(batch), device=device)
            positions = torch.tensor(starts, device=device) - 1
            patched[rows, positions] = vec.to(patched.dtype)
            return (patched,) + output[1:] if isinstance(output, tuple) else patched

        handle = layers[layer].register_forward_hook(hook)
        try:
            logits = model(input_ids=x, attention_mask=mask, use_cache=False).logits.float()
        finally:
            handle.remove()
        logp = torch.log_softmax(logits[:, :-1], -1)
        gathered = logp.gather(-1, x[:, 1:].unsqueeze(-1)).squeeze(-1)
        for i, (ids, start) in enumerate(batch):
            values = gathered[i, start - 1:len(ids) - 1]
            results.append(Score(values.mean().item(), values.sum().item(), len(values)))
    return results


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--pair", choices=["zh_ja", "id_tl"], default="zh_ja")
    parser.add_argument("--model", required=True)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--items-per-group", type=int, default=20)
    parser.add_argument("--layer-stride", type=int, default=4)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--output-path", type=Path)
    args = parser.parse_args()

    donors = build_donors(args.data_root, args.pair, args.items_per_group)
    tokenizer = AutoTokenizer.from_pretrained(args.model, local_files_only=True)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        args.model, dtype=torch.bfloat16, device_map={"": 0}, local_files_only=True,
        attn_implementation="sdpa").eval()
    layers, selected = layer_list(model, args.layer_stride)
    states = donor_states(model, tokenizer, donors, selected, args.batch_size)

    donor_requests, donor_metadata = [], []
    for index, row in enumerate(donors):
        for candidate_sense, candidate in ((1, row["meaning1"]), (2, row["meaning2"])):
            donor_requests.append((messages(row, False), candidate))
            donor_metadata.append((index, candidate_sense))
    observed = score_requests(model, tokenizer, donor_requests, args.batch_size)

    requests, prepared, vectors, metadata = [], [], [], []
    for index, row in enumerate(donors):
        neutral_messages = messages(row, True)
        for candidate_sense, candidate in ((1, row["meaning1"]), (2, row["meaning2"])):
            requests.append((neutral_messages, candidate))
            prepared.append(prepare_local(tokenizer, neutral_messages, candidate))
            metadata.append((index, candidate_sense))
    baseline = score_requests(model, tokenizer, requests, args.batch_size)
    records = []
    for (index, candidate_sense), score in zip(donor_metadata, observed):
        records.append({"model": args.tag, "pair": args.pair, "layer": -2,
                        "donor_index": index, "candidate_sense": candidate_sense,
                        "mean_logp": score.mean_logp, "sum_logp": score.sum_logp})
    for (index, candidate_sense), score in zip(metadata, baseline):
        records.append({"model": args.tag, "pair": args.pair, "layer": -1,
                        "donor_index": index, "candidate_sense": candidate_sense,
                        "mean_logp": score.mean_logp, "sum_logp": score.sum_logp})
    for layer in selected:
        vectors = [states[index][layer] for index, _ in metadata]
        scores = patched_scores(model, tokenizer, layers, layer, prepared, vectors,
                                args.batch_size)
        for (index, candidate_sense), score in zip(metadata, scores):
            records.append({"model": args.tag, "pair": args.pair, "layer": layer,
                            "donor_index": index, "candidate_sense": candidate_sense,
                            "mean_logp": score.mean_logp, "sum_logp": score.sum_logp})
    path = args.output_path or (ROOT / "results/extensions" / f"causal_gating_{args.tag}.jsonl")
    enriched = []
    for record in records:
        donor = donors[record.pop("donor_index")]
        enriched.append(record | {key: donor[key] for key in
                                   ("id", "group", "language", "sense")})
    path.write_text("".join(json.dumps(row) + "\n" for row in enriched))
    print(f"wrote {len(enriched)} causal scores across layers {selected} to {path}")


if __name__ == "__main__":
    main()
