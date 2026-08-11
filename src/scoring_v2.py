#!/usr/bin/env python3
"""Boundary-faithful continuation scoring for plain and chat prompts."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import torch


@dataclass
class Score:
    mean_logp: float
    sum_logp: float
    n_tokens: int


def _plain_ids(tokenizer, prompt: str, candidate: str) -> tuple[list[int], int]:
    """Tokenize the full string and require a stable prefix boundary.

    The scored continuation includes the leading space before the candidate.
    Unlike separately tokenizing and concatenating prompt/candidate IDs, this
    corresponds exactly to the model input for the displayed full string.
    """
    base = prompt.rstrip()
    for marker in ("\nAnswer:", "\n\nAnswer:", "\n### Answer:"):
        prefix = base + marker
        full = prefix + " " + candidate
        prefix_ids = tokenizer(prefix, add_special_tokens=False).input_ids
        full_ids = tokenizer(full, add_special_tokens=False).input_ids
        if full_ids[: len(prefix_ids)] == prefix_ids and len(full_ids) > len(prefix_ids):
            return full_ids, len(prefix_ids)
    raise ValueError("no prefix-stable plain-text answer boundary found")


def _chat_ids(tokenizer, prompt: str, candidate: str) -> tuple[list[int], int]:
    prefix_ids = tokenizer.apply_chat_template(
        [{"role": "user", "content": prompt}],
        tokenize=True,
        add_generation_prompt=True,
    )
    candidate_ids = tokenizer(candidate, add_special_tokens=False).input_ids
    if not candidate_ids:
        raise ValueError("candidate tokenized to an empty sequence")
    return list(prefix_ids) + list(candidate_ids), len(prefix_ids)


def prepare(tokenizer, prompt: str, candidate: str, prompt_mode: str) -> tuple[list[int], int]:
    if prompt_mode == "plain":
        return _plain_ids(tokenizer, prompt, candidate)
    if prompt_mode == "chat":
        return _chat_ids(tokenizer, prompt, candidate)
    raise ValueError(f"unknown prompt mode: {prompt_mode}")


@torch.inference_mode()
def score_many(model, tokenizer, examples: Iterable[tuple[str, str]], prompt_mode: str,
               batch_size: int = 8) -> list[Score]:
    prepared = [prepare(tokenizer, p, c, prompt_mode) for p, c in examples]
    results: list[Score] = []
    device = next(model.parameters()).device
    pad_id = tokenizer.pad_token_id
    if pad_id is None:
        pad_id = tokenizer.eos_token_id
    for offset in range(0, len(prepared), batch_size):
        batch = prepared[offset: offset + batch_size]
        width = max(len(ids) for ids, _ in batch)
        input_ids = torch.full((len(batch), width), pad_id, dtype=torch.long, device=device)
        attention = torch.zeros_like(input_ids)
        for row, (ids, _) in enumerate(batch):
            input_ids[row, : len(ids)] = torch.tensor(ids, device=device)
            attention[row, : len(ids)] = 1
        logits = model(input_ids=input_ids, attention_mask=attention).logits.float()
        logp = torch.log_softmax(logits[:, :-1], dim=-1)
        targets = input_ids[:, 1:]
        token_logp = logp.gather(-1, targets.unsqueeze(-1)).squeeze(-1)
        for row, (ids, start) in enumerate(batch):
            # Token at index `start` is predicted by logits at `start - 1`.
            values = token_logp[row, start - 1: len(ids) - 1]
            results.append(Score(values.mean().item(), values.sum().item(), len(values)))
    return results
