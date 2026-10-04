import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.ticker import FuncFormatter

HDR100_MAX = 12500  # 100 Gb/s em MB/s

BENCHMARKS = {
    "bw": ("Largura de Banda (osu_bw)", "Largura de banda (MB/s)"),
    "latency": ("Latência (osu_latency)", r"Latência ($\mu$s)"),
}

COLORS = {"native": "#0072B2", "container": "#D55E00"}
LABELS = {"native": "Nativo", "container": "Contêiner"}


def size_label(x, _):
    if x >= 2**20:
        return f"{x / 2**20:g}M"
    if x >= 2**10:
        return f"{x / 2**10:g}K"
    return f"{x:g}"


def format_axes(ax, sizes, ylabel, title):
    ax.set_xscale("log", base=2)
    ax.set_xticks(sizes)
    ax.xaxis.set_major_formatter(FuncFormatter(size_label))
    ax.minorticks_off()
    ax.tick_params(axis="x", rotation=45)
    ax.set_xlabel("Tamanho da mensagem (bytes)")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend()


sns.set_theme(style="whitegrid", context="paper", font_scale=1.25)
plt.rcParams.update({"font.family": "serif", "pdf.fonttype": 42})
os.makedirs("graphs", exist_ok=True)

for bench, (title, ylabel) in BENCHMARKS.items():
    df = pd.read_csv(f"logs/osu_{bench}.csv")
    for v in ("native", "container"):
        runs = df.filter(like=f"{v}_run")
        df[f"{v}_mean"] = runs.mean(axis=1)
        df[f"{v}_std"] = runs.std(axis=1)

    fig, ax = plt.subplots(figsize=(8, 5))
    for v, marker in (("native", "o"), ("container", "s")):
        ax.errorbar(df["size"], df[f"{v}_mean"], yerr=df[f"{v}_std"],
                    label=LABELS[v], color=COLORS[v], marker=marker, capsize=3)
    if bench == "bw":
        ax.axhline(HDR100_MAX, color="gray", linestyle="--",
                   label="Máximo Teórico (HDR100)")
    else:
        ax.set_yscale("log")
        ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f"{y:g}"))
    format_axes(ax, df["size"], ylabel, title)
    fig.savefig(f"graphs/osu_{bench}.pdf", bbox_inches="tight")
    plt.close(fig)

    diff = (df["container_mean"] - df["native_mean"]) / df["native_mean"] * 100
    if bench == "bw":
        diff = -diff

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.axhline(0, color="black", linewidth=0.8)
    ax.plot(df["size"], diff, color="#009E73", marker="D",
            label="Overhead do Contêiner vs. Nativo")
    format_axes(ax, df["size"], "Overhead (%)", f"{title}: overhead do contêiner")
    fig.savefig(f"graphs/osu_{bench}_diff.pdf", bbox_inches="tight")
    plt.close(fig)
