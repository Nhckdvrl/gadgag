#!/usr/bin/env python3
"""Train one crossover fold and evaluate at exposure doses 0/32/128."""
from __future__ import annotations

import argparse
import json
import math
import random
import unicodedata
from pathlib import Path

import numpy as np
import torch
from peft import LoraConfig, PeftModel, get_peft_model
from torch.optim import AdamW
from torch.utils.data import DataLoader, Dataset
from transformers import AutoModelForCausalLM, AutoTokenizer

ROOT = Path(__file__).resolve().parents[1]
MODEL = "Qwen/Qwen2.5-7B-Instruct"
DOSES = (0, 32, 128)
SEED = 20260810


def read_items() -> list[dict]:
    return [json.loads(x) for x in (ROOT / "data/items.jsonl").read_text().splitlines()]


def candidate_score(model, tok, prompt: str, candidate: str) -> tuple[float, float]:
    """Return mean and sum log p(candidate | prompt)."""
    pids = tok(prompt, add_special_tokens=False).input_ids
    # Tokenize the continuation separately. Some BPE tokenizers merge across the
    # prompt/candidate boundary; explicit concatenation gives both candidates the
    # same, auditable boundary and avoids silently scoring part of the prompt.
    cids = tok(candidate, add_special_tokens=False).input_ids
    full = pids + cids
    ids = torch.tensor([full], device=model.device)
    with torch.inference_mode():
        logits = model(ids).logits[0, :-1].float()
    start = len(pids) - 1
    targets = ids[0, len(pids):]
    lp = torch.log_softmax(logits[start : start + len(targets)], -1)
    vals = lp.gather(1, targets[:, None]).squeeze(1)
    return vals.mean().item(), vals.sum().item()


def evaluate(model, tok, items: list[dict], fold: int, dose: int, tag: str = "main") -> list[dict]:
    model.eval()
    out = []
    for n, x in enumerate(items):
        prompt = (
            "次の日本語文を中国語に翻訳してください。説明は不要です。\n"
            f"日本語: {x['eval_ja']}\n中国語: "
        )
        cmean, csum = candidate_score(model, tok, prompt, x["correct"])
        imean, isum = candidate_score(model, tok, prompt, x["intrusion"])
        y = dict(x)
        y.update({
            "fold": fold,
            "dose": dose,
            "treated": x["treated_fold"] in (fold, "both"),
            "correct_mean_logp": cmean,
            "intrusion_mean_logp": imean,
            "correct_sum_logp": csum,
            "intrusion_sum_logp": isum,
            "margin": cmean - imean,
            "is_correct": cmean > imean,
        })
        out.append(y)
        if (n + 1) % 20 == 0:
            print(f"eval fold={fold} dose={dose}: {n+1}/{len(items)}", flush=True)
    path = (ROOT / "results" / f"fold{fold}_dose{dose}.jsonl" if tag == "main"
            else ROOT / "results" / "extensions" / f"{tag}_fold{fold}_dose{dose}.jsonl")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        for x in out:
            f.write(json.dumps(x, ensure_ascii=False) + "\n")
    return out


class TextDataset(Dataset):
    def __init__(self, texts: list[str], tok, max_length: int = 128):
        self.enc = [tok(t + tok.eos_token, truncation=True, max_length=max_length).input_ids for t in texts]
    def __len__(self): return len(self.enc)
    def __getitem__(self, i): return self.enc[i]


def collate(batch, pad: int):
    width = max(map(len, batch))
    ids = torch.full((len(batch), width), pad, dtype=torch.long)
    mask = torch.zeros_like(ids)
    labels = torch.full_like(ids, -100)
    for i, x in enumerate(batch):
        ids[i, :len(x)] = torch.tensor(x)
        mask[i, :len(x)] = 1
        labels[i, :len(x)] = torch.tensor(x)
    return {"input_ids": ids, "attention_mask": mask, "labels": labels}


def make_rounds(items: list[dict], fold: int, start: int, stop: int) -> list[str]:
    # Causal intervention: expose only this fold's 25 false friends. Auxiliary
    # groups are evaluated but deliberately not trained, keeping the control clean.
    targets = [x for x in items if x["group"] == "false_friend" and x["treated_fold"] == fold]
    texts = []
    for exposure in range(start, stop):
        round_items = targets.copy()
        random.Random(SEED + fold * 10000 + exposure).shuffle(round_items)
        texts.extend(x["train_zh"] for x in round_items)
    return texts


def train_segment(model, tok, texts: list[str], fold: int, start: int, stop: int):
    ds = TextDataset(texts, tok)
    gen = torch.Generator().manual_seed(SEED + fold + start)
    dl = DataLoader(ds, batch_size=16, shuffle=True, generator=gen,
                    collate_fn=lambda b: collate(b, tok.pad_token_id))
    opt = AdamW((p for p in model.parameters() if p.requires_grad), lr=2e-4, weight_decay=0.0)
    model.train()
    losses = []
    for step, batch in enumerate(dl, 1):
        batch = {k: v.to(model.device) for k, v in batch.items()}
        loss = model(**batch).loss
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step(); opt.zero_grad(set_to_none=True)
        losses.append(loss.item())
        if step % 25 == 0 or step == len(dl):
            print(f"train fold={fold} exposure={start}->{stop} step={step}/{len(dl)} loss={np.mean(losses[-25:]):.4f}", flush=True)
    return float(np.mean(losses))


def token_audit(tok, items: list[dict]) -> None:
    rows = []
    for x in items:
        a, b = x["word_zh"], x["word_ja"]
        ta, tb = tok(a, add_special_tokens=False).input_ids, tok(b, add_special_tokens=False).input_ids
        rows.append({
            "id": x["id"], "group": x["group"], "word_zh": a, "word_ja": b,
            "codepoints_zh": [f"U+{ord(c):04X}" for c in a],
            "codepoints_ja": [f"U+{ord(c):04X}" for c in b],
            "unicode_exact": a == b,
            "nfkc_exact": unicodedata.normalize("NFKC", a) == unicodedata.normalize("NFKC", b),
            "tokens_zh": ta, "tokens_ja": tb, "identical_token_sequence": ta == tb,
            "n_tokens_zh": len(ta), "n_tokens_ja": len(tb),
        })
    (ROOT / "results/token_audit.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fold", type=int, choices=[0, 1], required=True)
    ap.add_argument("--model", default=MODEL)
    ap.add_argument("--doses", type=int, nargs="+", default=list(DOSES))
    ap.add_argument("--tag", default="main")
    ap.add_argument("--modules", choices=["all", "attention", "mlp"], default="all")
    ap.add_argument("--layer-half", choices=["all", "early", "late"], default="all")
    args = ap.parse_args()
    random.seed(SEED + args.fold); np.random.seed(SEED + args.fold); torch.manual_seed(SEED + args.fold)
    torch.backends.cuda.matmul.allow_tf32 = True
    items = read_items()
    tok = AutoTokenizer.from_pretrained(args.model, local_files_only=True)
    if tok.pad_token_id is None: tok.pad_token = tok.eos_token
    if args.fold == 0: token_audit(tok, items)
    base = AutoModelForCausalLM.from_pretrained(
        args.model, torch_dtype=torch.bfloat16, device_map={"": 0}, local_files_only=True,
        attn_implementation="sdpa",
    )
    base.config.use_cache = False
    module_map = {
        "all": ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        "attention": ["q_proj", "k_proj", "v_proj", "o_proj"],
        "mlp": ["gate_proj", "up_proj", "down_proj"],
    }
    n_layers = int(base.config.num_hidden_layers)
    layer_ids = None
    if args.layer_half == "early": layer_ids = list(range(0, n_layers // 2))
    if args.layer_half == "late": layer_ids = list(range(n_layers // 2, n_layers))
    cfg = LoraConfig(r=16, lora_alpha=32, lora_dropout=0.0, bias="none",
                     task_type="CAUSAL_LM", target_modules=module_map[args.modules],
                     layers_to_transform=layer_ids)
    model = get_peft_model(base, cfg)
    model.print_trainable_parameters()
    doses = sorted(set(args.doses))
    if not doses or doses[0] != 0:
        raise ValueError("--doses must include 0")
    evaluate(model, tok, items, args.fold, 0, args.tag)
    previous = 0
    train_log = []
    for dose in doses[1:]:
        texts = make_rounds(items, args.fold, previous, dose)
        loss = train_segment(model, tok, texts, args.fold, previous, dose)
        adapter_dir = (ROOT / "results" / "adapters" / f"fold{args.fold}_dose{dose}" if args.tag == "main"
                       else ROOT / "results" / "extensions" / "adapters" / f"{args.tag}_fold{args.fold}_dose{dose}")
        model.save_pretrained(adapter_dir)
        train_log.append({"fold": args.fold, "from": previous, "to": dose, "n_examples": len(texts), "mean_loss": loss})
        evaluate(model, tok, items, args.fold, dose, args.tag)
        previous = dose
    log_path = (ROOT / "results" / f"fold{args.fold}_train.json" if args.tag == "main"
                else ROOT / "results" / "extensions" / f"{args.tag}_fold{args.fold}_train.json")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(json.dumps(train_log, indent=2) + "\n")


if __name__ == "__main__":
    main()
