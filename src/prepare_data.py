#!/usr/bin/env python3
"""Build a deterministic, source-grounded pilot dataset."""
from __future__ import annotations

import hashlib
import json
import random
import runpy
import unicodedata
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DOPPEL = ROOT / "external" / "Doppelganger-JC"
STINGRAY = ROOT / "external" / "StingrayBench"
OUT = ROOT / "data"
SEED = 20260810


def norm(s: str) -> str:
    return unicodedata.normalize("NFKC", str(s).strip())


def load_doppel() -> list[dict]:
    jpq = runpy.run_path(str(DOPPEL / "questions/jp_zh/homographs.py"))["dataset"]
    zhq = runpy.run_path(str(DOPPEL / "questions/zh_jp/homographs.py"))["dataset"]
    rows = []
    for line in (DOPPEL / "cognate_fixed/jp/homographs.txt").read_text().splitlines():
        ja, zh, zh_meaning, ja_meaning = line.split("|", 3)
        if norm(ja) != norm(zh) or zh not in jpq or zh not in zhq:
            continue
        j, z = jpq[zh], zhq[zh]
        # Require the specific intruding translation to differ from the correct one.
        if norm(j["correct"]) == norm(j["wrong1"]):
            continue
        rows.append({
            "id": "ff_" + hashlib.sha1(ja.encode()).hexdigest()[:10],
            "group": "false_friend",
            "word_ja": ja,
            "word_zh": zh,
            "unicode_exact": ja == zh,
            "nfkc_exact": norm(ja) == norm(zh),
            "ja_meaning": ja_meaning,
            "zh_meaning": zh_meaning,
            "train_zh": z["target-sentence"].strip(),
            "eval_ja": j["target-sentence"].strip(),
            "correct": j["correct"].strip(),
            "intrusion": j["wrong1"].strip(),
            "source": "Doppelganger-JC Type-1",
        })
    # Stable random sample, not cherry-picked by baseline behavior.
    random.Random(SEED).shuffle(rows)
    return rows[:50]


def load_common() -> list[dict]:
    df = pd.read_csv(STINGRAY / "data/zh_ja_common_words.csv")
    rows = []
    for i, r in df.iterrows():
        m1, m2 = str(r["Meaning in L1"]).strip(), str(r["Meaning in L2"]).strip()
        # The released common set contains several non-cognates; retain only exact
        # equality of its human-provided English meaning labels.
        if m1.casefold() != m2.casefold():
            continue
        wzh, wja = str(r["Cognates_L1"]).strip(), str(r["Cognates_L2"]).strip()
        group = "true_friend" if norm(wzh) == norm(wja) else "different_form_control"
        rows.append({
            "id": f"common_{i:03d}",
            "group": group,
            "word_ja": wja,
            "word_zh": wzh,
            "unicode_exact": wja == wzh,
            "nfkc_exact": norm(wja) == norm(wzh),
            "ja_meaning": m2,
            "zh_meaning": m1,
            "train_zh": str(r["L1"]).strip(),
            "eval_ja": str(r["L2"]).strip(),
            "correct": str(r["L1"]).strip(),
            "source": "StingrayBench zh_ja_common_words",
        })
    # A matched incorrect translation is another row's Chinese sentence. It is
    # used only to monitor broad retention, never as a semantic-intrusion label.
    for i, row in enumerate(rows):
        row["intrusion"] = rows[(i + 7) % len(rows)]["correct"]
    return rows


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = load_doppel() + load_common()
    ff_ids = [r["id"] for r in rows if r["group"] == "false_friend"]
    random.Random(SEED + 1).shuffle(ff_ids)
    halves = [set(ff_ids[:25]), set(ff_ids[25:])]
    for row in rows:
        if row["group"] == "false_friend":
            row["treated_fold"] = 0 if row["id"] in halves[0] else 1
        else:
            row["treated_fold"] = "both"
    with (OUT / "items.jsonl").open("w") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    manifest = {
        "seed": SEED,
        "n_total": len(rows),
        "counts": pd.Series([r["group"] for r in rows]).value_counts().to_dict(),
        "false_friend_treated_per_fold": [len(x) for x in halves],
        "selection": "stable seeded sample before any model evaluation",
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
