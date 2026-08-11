#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RNG = np.random.default_rng(20260811)


def main():
    rows = []
    for path in (ROOT / "results/extensions").glob("xlwic_*.jsonl"):
        rows.extend(json.loads(line) for line in path.read_text().splitlines())
    data = pd.DataFrame(rows)
    output = []
    for key, group in data.groupby(["language", "model", "prompt_mode"]):
        for calibration, column in (("raw", "correct"), ("content_free", "calibrated_correct")):
            values = group[column].to_numpy()
            boots = np.array([RNG.choice(values, len(values), replace=True).mean() for _ in range(5000)])
            output.append({"language": key[0], "model": key[1], "prompt_mode": key[2],
                           "calibration": calibration, "n": len(values), "accuracy": values.mean(),
                           "ci_low": np.quantile(boots, .025), "ci_high": np.quantile(boots, .975)})
    out = pd.DataFrame(output)
    out.to_csv(ROOT / "results/extensions/xlwic_summary.csv", index=False)
    (ROOT / "reports/xlwic_control.md").write_text("# XL-WiC general WSD control\n\n" + out.to_markdown(index=False) + "\n")
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
