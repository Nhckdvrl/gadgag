#!/usr/bin/env python3
"""Validated loader for Stingray's natural language × sense factorial cells."""
from __future__ import annotations

import re
import unicodedata
from pathlib import Path

import pandas as pd


LANGUAGES = {
    "zh_ja": ("Chinese", "Japanese"),
    "en_de": ("English", "German"),
    "id_ms": ("Indonesian", "Malay"),
    "id_tl": ("Indonesian", "Tagalog"),
}


def word(value: object) -> str:
    return str(value).split("(")[0].strip()


def norm(value: str) -> str:
    return unicodedata.normalize("NFKC", value)


def mask_target(sentence: str, target: str) -> str:
    replaced, n = re.subn(re.escape(target), "[TARGET]", sentence, flags=re.IGNORECASE)
    if n:
        return replaced
    # Some contexts use a case/compatibility variant. Match after NFKC as a
    # last resort while keeping the original sentence whenever possible.
    normalized = norm(sentence)
    replaced, n = re.subn(re.escape(norm(target)), "[TARGET]", normalized, flags=re.IGNORECASE)
    return replaced if n else normalized + " [TARGET]"


def contains_target(sentence: str, target: str) -> bool:
    """Require the listed target as a standalone Latin token or CJK substring."""
    sentence, target = norm(sentence), norm(target)
    if re.fullmatch(r"[\w\s-]+", target, flags=re.UNICODE) and re.search(r"[A-Za-z]", target):
        return bool(re.search(rf"(?<!\w){re.escape(target)}(?!\w)", sentence, flags=re.IGNORECASE))
    return target in sentence


def load_pair(data_root: Path, pair: str, exact_only: bool = True) -> list[dict]:
    path = data_root / f"{pair}.csv"
    frame = pd.read_csv(path)
    assert len(frame) % 2 == 0, f"{path}: odd row count"
    usage_columns = [column for column in frame.columns if str(column).startswith("Is the usage")]
    assert len(usage_columns) == 2, f"{path}: expected two usage-validity columns"
    items = []
    for idx in range(0, len(frame), 2):
        first, second = frame.iloc[idx], frame.iloc[idx + 1]
        w1, w2 = word(first.Cognates), word(second.Cognates)
        is_exact = norm(w1) == norm(w2)
        if exact_only and not is_exact:
            continue
        contexts = (str(first.L1).strip(), str(first.L2).strip(),
                    str(second.L1).strip(), str(second.L2).strip())
        if exact_only and not all(contains_target(context, w1) for context in contexts):
            continue
        m1a, m1b = str(first["Meaning in L1"]).strip(), str(second["Meaning in L1"]).strip()
        m2a, m2b = str(first["Meaning in L2"]).strip(), str(second["Meaning in L2"]).strip()
        assert m1a == m1b and m2a == m2b, f"{pair}:{idx}: meanings do not pair"
        assert str(first["Which sentence is more semantically appropriate? A. {L1} B. {L2} C. Both"]).strip() == "L1"
        assert str(second["Which sentence is more semantically appropriate? A. {L1} B. {L2} C. Both"]).strip() == "L2"
        item = {
            "id": f"{pair}_{idx // 2:03d}", "pair": pair,
            "word_l1": w1, "word_l2": w2, "word": w1 if is_exact else f"{w1} / {w2}",
            "exact_nfkc": is_exact, "meaning_l1": m1a, "meaning_l2": m2a,
            "L1_S1": str(first.L1).strip(), "L2_S1": str(first.L2).strip(),
            "L1_S2": str(second.L1).strip(), "L2_S2": str(second.L2).strip(),
        }
        # Verify that each row really provides the two opposite validity labels.
        assert str(first[usage_columns[0]]).strip().lower() == "yes"
        assert str(first[usage_columns[1]]).strip().lower() == "no"
        assert str(second[usage_columns[0]]).strip().lower() == "no"
        assert str(second[usage_columns[1]]).strip().lower() == "yes"
        items.append(item)
    assert items, f"{pair}: no items after exact={exact_only}"
    return items


def add_controls(items: list[dict]) -> list[dict]:
    """Add semantic-only, language-only, and deterministic shuffled contexts."""
    names = LANGUAGES[items[0]["pair"]]
    for i, item in enumerate(items):
        for language in (1, 2):
            target = item[f"word_l{language}"]
            for sense in (1, 2):
                key = f"L{language}_S{sense}"
                item[f"masked_{key}"] = mask_target(item[key], target)
                other = items[(i + 1) % len(items)]
                other_target = other[f"word_l{language}"]
                # Match the masked target marker exactly.  A distinct [OTHER]
                # marker would let the model distinguish the control without
                # reading the surrounding semantics.
                item[f"shuffled_{key}"] = mask_target(other[key], other_target)
                item[f"language_only_{key}"] = (
                    f"This is a {names[language - 1]} sentence. The target expression is {target}."
                )
    return items
