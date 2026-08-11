#!/usr/bin/env python3
"""Patch target-span residual, attention and MLP outputs across lexical controls."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from evaluate_causal_gating import (build_donors, chat_prefix, layer_list, messages,
                                    prepare_local, score_requests)
from scoring_v2 import Score

ROOT = Path(__file__).resolve().parents[1]
COMPONENTS = ("residual", "attention", "mlp")


def rendered_target_positions(tokenizer, value, target: str) -> tuple[list[int], list[int]]:
    kwargs = {"tokenize": False, "add_generation_prompt": True}
    if "qwen3" in str(tokenizer.name_or_path).casefold():
        kwargs["enable_thinking"] = False
    rendered = tokenizer.apply_chat_template(value, **kwargs)
    start = rendered.rfind(target)
    if start < 0:
        raise ValueError(f"target {target!r} absent from rendered chat")
    encoded = tokenizer(rendered, add_special_tokens=False, return_offsets_mapping=True)
    prefix = chat_prefix(tokenizer, value)
    if list(encoded.input_ids) != prefix:
        raise ValueError("rendered string and tokenized chat template disagree")
    end = start + len(target)
    positions = [i for i, (left, right) in enumerate(encoded.offset_mapping)
                 if right > start and left < end]
    if not positions:
        raise ValueError(f"no tokens overlap target {target!r}")
    return prefix, positions


def hidden(output):
    return output[0] if isinstance(output, tuple) else output


def replace_hidden(output, value):
    return (value,) + output[1:] if isinstance(output, tuple) else value


@torch.inference_mode()
def collect_states(model, tokenizer, layers, selected, donors, batch_size):
    device = next(model.parameters()).device
    pad = tokenizer.pad_token_id if tokenizer.pad_token_id is not None else tokenizer.eos_token_id
    states = []
    for offset in range(0, len(donors), batch_size):
        batch = donors[offset:offset + batch_size]
        rendered = [rendered_target_positions(tokenizer, messages(row, False), row["word"])
                    for row in batch]
        ids, positions = zip(*rendered)
        width = max(map(len, ids))
        x = torch.full((len(batch), width), pad, dtype=torch.long, device=device)
        mask = torch.zeros_like(x)
        for i, values in enumerate(ids):
            x[i, :len(values)] = torch.tensor(values, device=device); mask[i, :len(values)] = 1
        captured = {component: {} for component in ("attention", "mlp")}
        handles = []

        def make_capture(component, layer):
            def hook(_module, _inputs, output):
                value = hidden(output)
                captured[component][layer] = torch.stack(
                    [value[i, list(pos)].mean(0).detach().cpu()
                     for i, pos in enumerate(positions)])
            return hook

        for layer in selected:
            handles.append(layers[layer].self_attn.register_forward_hook(
                make_capture("attention", layer)))
            handles.append(layers[layer].mlp.register_forward_hook(
                make_capture("mlp", layer)))
        try:
            output = model(input_ids=x, attention_mask=mask, output_hidden_states=True,
                           use_cache=False)
        finally:
            for handle in handles:
                handle.remove()
        for i in range(len(batch)):
            item_states = {}
            for layer in selected:
                item_states[("residual", layer)] = output.hidden_states[layer + 1][
                    i, list(positions[i])].mean(0).detach().cpu()
                item_states[("attention", layer)] = captured["attention"][layer][i]
                item_states[("mlp", layer)] = captured["mlp"][layer][i]
            states.append(item_states)
        del output
    return states


@torch.inference_mode()
def score_patched(model, tokenizer, module, prepared, positions, vectors, batch_size):
    device = next(model.parameters()).device
    pad = tokenizer.pad_token_id if tokenizer.pad_token_id is not None else tokenizer.eos_token_id
    results = []
    for offset in range(0, len(prepared), batch_size):
        batch = prepared[offset:offset + batch_size]
        batch_positions = positions[offset:offset + batch_size]
        vec = torch.stack(vectors[offset:offset + batch_size]).to(device)
        width = max(len(ids) for ids, _ in batch)
        x = torch.full((len(batch), width), pad, dtype=torch.long, device=device)
        mask = torch.zeros_like(x); starts = []
        for i, (ids, start) in enumerate(batch):
            x[i, :len(ids)] = torch.tensor(ids, device=device); mask[i, :len(ids)] = 1
            starts.append(start)

        def hook(_module, _inputs, output):
            original = hidden(output); patched = original.clone()
            for row, pos in enumerate(batch_positions):
                patched[row, list(pos)] = vec[row].to(patched.dtype)
            return replace_hidden(output, patched)

        handle = module.register_forward_hook(hook)
        try:
            logits = model(input_ids=x, attention_mask=mask, use_cache=False).logits.float()
        finally:
            handle.remove()
        logp = torch.log_softmax(logits[:, :-1], -1)
        values = logp.gather(-1, x[:, 1:].unsqueeze(-1)).squeeze(-1)
        for row, (ids, start) in enumerate(batch):
            continuation = values[row, start - 1:len(ids) - 1]
            results.append(Score(continuation.mean().item(), continuation.sum().item(),
                                 len(continuation)))
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--pair", choices=["zh_ja", "id_tl"], default="zh_ja")
    parser.add_argument("--model", required=True); parser.add_argument("--tag", required=True)
    parser.add_argument("--items-per-group", type=int, default=20)
    parser.add_argument("--layer-stride", type=int, default=4)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--max-donors", type=int)
    parser.add_argument("--output-path", type=Path)
    args = parser.parse_args()
    donors = build_donors(args.data_root, args.pair, args.items_per_group)
    if args.max_donors:
        donors = donors[:args.max_donors]
    tokenizer = AutoTokenizer.from_pretrained(args.model, local_files_only=True)
    if tokenizer.pad_token_id is None: tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        args.model, dtype=torch.bfloat16, device_map={"": 0}, local_files_only=True,
        attn_implementation="sdpa").eval()
    layers, selected = layer_list(model, args.layer_stride)
    states = collect_states(model, tokenizer, layers, selected, donors, args.batch_size)

    requests, prepared, recipient_positions, metadata = [], [], [], []
    for index, row in enumerate(donors):
        neutral = messages(row, True)
        _, positions = rendered_target_positions(tokenizer, neutral, row["neutral_word"])
        for sense, candidate in ((1, row["meaning1"]), (2, row["meaning2"])):
            requests.append((neutral, candidate)); prepared.append(prepare_local(tokenizer, neutral, candidate))
            recipient_positions.append(positions); metadata.append((index, sense))
    baseline = score_requests(model, tokenizer, requests, args.batch_size)
    records = [{"model": args.tag, "pair": args.pair, "component": "baseline", "layer": -1,
                "donor_index": index, "candidate_sense": sense,
                "mean_logp": score.mean_logp, "sum_logp": score.sum_logp}
               for (index, sense), score in zip(metadata, baseline)]
    for component in COMPONENTS:
        for layer in selected:
            module = layers[layer] if component == "residual" else getattr(layers[layer],
                                                                            "self_attn" if component == "attention" else "mlp")
            vectors = [states[index][(component, layer)] for index, _ in metadata]
            scores = score_patched(model, tokenizer, module, prepared, recipient_positions,
                                   vectors, args.batch_size)
            for (index, sense), score in zip(metadata, scores):
                records.append({"model": args.tag, "pair": args.pair,
                    "component": component, "layer": layer, "donor_index": index,
                    "candidate_sense": sense, "mean_logp": score.mean_logp,
                    "sum_logp": score.sum_logp})
    enriched = []
    for record in records:
        donor = donors[record.pop("donor_index")]
        enriched.append(record | {key: donor[key] for key in
                                  ("id", "group", "language", "sense")})
    path = args.output_path or ROOT / "results/extensions" / f"target_patch_{args.tag}.jsonl"
    path.write_text("".join(json.dumps(row) + "\n" for row in enriched))
    print(f"wrote {len(enriched)} scores for components {COMPONENTS} and layers {selected}")


if __name__ == "__main__":
    main()
