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


def factorial_controls():
    d=pd.read_csv(ROOT/"results/extensions/construct_gate_summary.csv")
    d=d[d.family=="factorial_semantic"].set_index("test").loc[["full","masked","language_only","shuffled"]].reset_index()
    fig,ax=plt.subplots(figsize=(5.8,3.5));bars=ax.bar(d.test,100*d.ci_positive/d.variants,color=["#2c7fb8","#41b6c4","#bdbdbd","#bdbdbd"])
    ax.set_ylim(0,105);ax.set_ylabel("Variants with 95% CI > 0 (%)");ax.set_title("Semantic-context effect survives construct killers")
    for bar,n,total in zip(bars,d.ci_positive,d.variants):ax.text(bar.get_x()+bar.get_width()/2,bar.get_height()+2,f"{n}/{total}",ha="center",fontsize=9)
    save("factorial_construct_controls")


def decomposition():
    d=pd.read_csv(ROOT/"results/extensions/factorial_summary.csv")
    d=d[(d.condition=="full")&(d.wrapper=="bare")&(d.normalization=="mean")&(d.prompt_mode=="chat")&d.effect.isin(["semantic","language"])]
    p=d.pivot(index=["pair","model"],columns="effect",values="estimate").reset_index();p["label"]=p.model.str.replace("_","-",regex=False)+" / "+p.pair.str.upper().str.replace("_","–",regex=False)
    x=np.arange(len(p));w=.37;fig,ax=plt.subplots(figsize=(8.4,4))
    ax.bar(x-w/2,p.semantic,w,label="sense-bearing context");ax.bar(x+w/2,p.language,w,label="language convention")
    ax.axhline(0,color="black",lw=.8);ax.set_ylabel("Mean log-probability margin effect");ax.set_xticks(x,p.label,rotation=28,ha="right");ax.set_title("The old diagonal switch contains two distinct signals");ax.legend(frameon=False)
    save("factorial_decomposition")


def calibration_gain():
    d=pd.read_csv(ROOT/"results/extensions/decision_calibration_aggregate.csv");p=d.pivot(index="pair",columns="calibration",values="both_accuracy").reset_index();x=np.arange(len(p));w=.35
    fig,ax=plt.subplots(figsize=(5.2,3.5));ax.bar(x-w/2,100*p.raw,w,label="raw");ax.bar(x+w/2,100*p.content_free_calibrated,w,label="content-free calibrated")
    ax.set_xticks(x,p.pair.str.upper().str.replace("_","–",regex=False));ax.set_ylabel("Both directions correct (%)");ax.set_title("Decision bias changes absolute conclusions");ax.legend(frameon=False);save("calibration_gain")


def natural_context_gate():
    d = pd.read_csv(ROOT / "results/extensions/natural_context_summary.csv")
    order = ["full_minus_language_only", "full_minus_shuffled", "masked_minus_shuffled"]
    labels = ["full − language+target", "full − shuffled", "masked − shuffled"]
    all_rates = [100 * (d[d.comparison == key].ci_low > 0).mean() for key in order]
    chat_rates = [100 * (d[(d.comparison == key) & (d.prompt_mode == "chat")].ci_low > 0).mean()
                  for key in order]
    x = np.arange(len(order)); width = .35
    fig, ax = plt.subplots(figsize=(6.6, 3.7))
    ax.bar(x - width / 2, all_rates, width, label="all protocols")
    ax.bar(x + width / 2, chat_rates, width, label="official chat")
    ax.set_ylim(0, 105)
    ax.set_ylabel("Specifications with 95% CI > 0 (%)")
    ax.set_xticks(x, labels, rotation=14, ha="right")
    ax.set_title("Natural context helps, but does not always beat an explicit language cue")
    ax.legend(frameon=False)
    save("natural_context_gate")


if __name__ == "__main__":
    dose_curve(); construct_control(); paired_switch(); factorial_controls(); decomposition(); calibration_gain(); natural_context_gate()
