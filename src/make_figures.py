#!/usr/bin/env python3
"""Generate publication-ready pilot figures from aggregate CSV files."""
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "figures"
OUT.mkdir(exist_ok=True)
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})


def save(name):
    plt.tight_layout()
    plt.savefig(OUT / f"{name}.png", dpi=220, bbox_inches="tight")
    plt.savefig(OUT / f"{name}.pdf", bbox_inches="tight")
    plt.close()


def dose_curve():
    d = pd.read_csv(ROOT / "results/extensions/summary.csv")
    d = d[d.experiment == "qwen25_fine"].sort_values("dose")
    fig, ax = plt.subplots(figsize=(5.2, 3.4))
    y = d.paired_delta.to_numpy()
    ax.errorbar(d.dose, y, yerr=[y-d.ci_low, d.ci_high-y], marker="o", capsize=3)
    ax.axhline(0, color="black", lw=.8)
    ax.set(xlabel="Chinese exposures per treated word", ylabel="Raw treated effect (Δ margin)",
           title="Apparent overwrite grows early, then saturates")
    save("dose_curve")


def construct_control():
    zh = pd.read_csv(ROOT / "results/extensions/context_lift_summary.csv")
    en = pd.read_csv(ROOT / "results/extensions/en_de_lift_summary.csv")
    rows = [
        ("ZH–JA conflict", zh.query("condition=='conflict' and metric=='draw'").iloc[0],
         zh.query("condition=='conflict' and metric=='dlift'").iloc[0]),
        ("ZH–JA neutral", zh.query("condition=='neutral' and metric=='draw'").iloc[0],
         zh.query("condition=='neutral' and metric=='dlift'").iloc[0]),
        ("EN–DE dose 8", en.query("condition=='d8' and metric=='draw'").iloc[0],
         en.query("condition=='d8' and metric=='dlift'").iloc[0]),
    ]
    x=np.arange(len(rows));w=.34
    fig,ax=plt.subplots(figsize=(6.4,3.6))
    for j,(label,raw,adj) in enumerate(rows):
        pass
    def value(s):
        return s["paired_effect"] if "paired_effect" in s.index else s["effect"]
    rawv=np.array([value(r[1]) for r in rows]);adjv=np.array([value(r[2]) for r in rows])
    ax.bar(x-w/2,rawv,w,label="raw candidate margin")
    ax.bar(x+w/2,adjv,w,label="context-lift adjusted")
    ax.axhline(0,color="black",lw=.8);ax.set_xticks(x,[r[0] for r in rows])
    ax.set_ylabel("Paired treatment effect");ax.set_title("The apparent effect vanishes after prior control")
    ax.legend(frameon=False)
    save("construct_control")


def paired_switch():
    d=pd.read_csv(ROOT/"results/extensions/paired_sense_summary.csv")
    d["label"]=d.model.str.replace("_","-",regex=False)+" / "+d.pair.str.upper().str.replace("_","–",regex=False)
    d=d.sort_values(["model","pair"]);x=np.arange(len(d));w=.37
    fig,ax=plt.subplots(figsize=(8,3.9))
    ax.bar(x-w/2,100*d.both_accuracy,w,label="both contexts absolutely correct")
    ax.bar(x+w/2,100*d.switch_positive,w,label="correct sense-switch direction")
    ax.set_ylim(0,105);ax.set_ylabel("Items (%)");ax.set_xticks(x,d.label,rotation=28,ha="right")
    ax.set_title("Wrong absolute answer can coexist with correct contextual direction")
    ax.legend(frameon=False,loc="lower right")
    save("paired_sense_switch")


if __name__ == "__main__":
    dose_curve(); construct_control(); paired_switch()
