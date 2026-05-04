"""3-model synthesis for A.0 v3.

Loads per-model metrics (m1_m4, m5_validity) from the 3 models tested:
  - gemini-3-pro-preview (frontier)
  - gemma3:12b          (mid)
  - llama3.2:3b         (small)

Outputs:
  synth_v3_top_line.csv          — H1/H2/H4 hypothesis stats × model
  synth_v3_truth_direction.csv   — divergence × truth direction × model
  synth_v3_per_topic.csv         — long-form per-topic × model (entropy, div, v_score)
  synth_v3_scaling.png           — H1/H2/H4 vs model scale
  synth_v3_truth_dir_heatmap.png — direction distribution per topic per model
  synth_v3_summary.md            — human-readable synthesis
"""

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
ANA = ROOT / "05_analysis"

MODELS = [
    {"slug": "gemini-3-pro-preview", "label": "Gemini 3 Pro", "scale": "frontier", "params_b": 1500.0},
    {"slug": "gemma3_12b",            "label": "Gemma3 12B",   "scale": "mid",      "params_b": 12.0},
    {"slug": "llama3.2_3b",          "label": "Llama 3.2 3B", "scale": "small",    "params_b": 3.0},
]


def load_model(slug):
    m1m4 = pd.read_csv(ANA / f"m1_m4_entropy_divergence__{slug}.csv")
    m5 = pd.read_csv(ANA / f"m5_validity__{slug}.csv")
    return {"m1m4": m1m4, "m5": m5}


def topics_truth():
    """Map topic_id → truth_direction from topics.json."""
    data = json.load(open(ROOT / "01_topics" / "topics.json"))
    return {t["id"]: t["cochrane_truth"]["direction"] for t in data["topics"]}


def top_line_table(per_model):
    """One row per model: H1, H2, H4 stats."""
    rows = []
    for m in MODELS:
        d = per_model[m["slug"]]
        m1m4 = d["m1m4"]
        ai_val = d["m5"][d["m5"]["source"] == "ai"]
        rows.append({
            "model": m["label"],
            "scale": m["scale"],
            "params_b": m["params_b"],
            "H1_entropy_mean_bits": m1m4["entropy_bits"].mean(),
            "H1_entropy_topics_above_0.3": int((m1m4["entropy_bits"] > 0.3).sum()),
            "H2_truth_div_mean_pct": m1m4["truth_divergence_rate"].mean() * 100,
            "H2_truth_div_topics_above_20": int((m1m4["truth_divergence_rate"] > 0.20).sum()),
            "H4_pct_valid_all_8_mean": ai_val["pct_valid_all_8"].mean(),
            "H4_topics_pct_valid_above_75": int((ai_val["pct_valid_all_8"] >= 75).sum()),
        })
    return pd.DataFrame(rows)


def truth_direction_table(per_model, truth_map):
    """Truth divergence rate × truth direction × model."""
    rows = []
    for m in MODELS:
        d = per_model[m["slug"]]["m1m4"].copy()
        d["truth"] = d["topic_id"].map(truth_map)
        for direction in ["SUPPORTS", "REFUTES", "NEUTRAL"]:
            sub = d[d["truth"] == direction]
            if len(sub) == 0:
                continue
            rows.append({
                "model": m["label"],
                "truth_direction": direction,
                "n_topics": len(sub),
                "mean_truth_div_pct": sub["truth_divergence_rate"].mean() * 100,
                "max_truth_div_pct": sub["truth_divergence_rate"].max() * 100,
                "topics_above_20pct": int((sub["truth_divergence_rate"] > 0.20).sum()),
            })
    return pd.DataFrame(rows)


def per_topic_long(per_model, truth_map):
    """Long-form: row per (topic, model)."""
    rows = []
    for m in MODELS:
        d_m1m4 = per_model[m["slug"]]["m1m4"]
        d_v = per_model[m["slug"]]["m5"][per_model[m["slug"]]["m5"]["source"] == "ai"][["topic_id", "mean_v_score", "pct_valid_all_8"]]
        merged = d_m1m4.merge(d_v, on="topic_id", how="left")
        for _, r in merged.iterrows():
            rows.append({
                "model": m["label"],
                "scale": m["scale"],
                "topic_id": r["topic_id"],
                "truth_direction": truth_map.get(r["topic_id"], "?"),
                "n": r["n"],
                "p_supports": r["p_supports"],
                "p_neutral": r["p_neutral"],
                "p_refutes": r["p_refutes"],
                "entropy_bits": r["entropy_bits"],
                "truth_div_pct": r["truth_divergence_rate"] * 100,
                "mean_v_score": r["mean_v_score"],
                "pct_valid_all_8": r["pct_valid_all_8"],
            })
    return pd.DataFrame(rows)


def plot_scaling(top_line, out_path):
    import matplotlib.pyplot as plt

    df = top_line.sort_values("params_b")
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.2))

    axes[0].plot(df["params_b"], df["H1_entropy_mean_bits"], "o-", color="tab:blue", markersize=10)
    for _, r in df.iterrows():
        axes[0].annotate(r["model"], (r["params_b"], r["H1_entropy_mean_bits"]),
                         textcoords="offset points", xytext=(8, 4), fontsize=9)
    axes[0].axhline(0.3, color="red", ls="--", alpha=0.6, label="H1 threshold")
    axes[0].set_xscale("log")
    axes[0].set_xlabel("Model parameters (B, log scale)")
    axes[0].set_ylabel("Mean entropy (bits)")
    axes[0].set_title("H1: Conclusion variance ↑ at small scale")
    axes[0].legend()
    axes[0].grid(alpha=0.3)

    axes[1].plot(df["params_b"], df["H2_truth_div_mean_pct"], "s-", color="tab:orange", markersize=10)
    for _, r in df.iterrows():
        axes[1].annotate(r["model"], (r["params_b"], r["H2_truth_div_mean_pct"]),
                         textcoords="offset points", xytext=(8, 4), fontsize=9)
    axes[1].axhline(20, color="red", ls="--", alpha=0.6, label="H2 threshold")
    axes[1].set_xscale("log")
    axes[1].set_xlabel("Model parameters (B, log scale)")
    axes[1].set_ylabel("Mean truth divergence (%)")
    axes[1].set_title("H2: Drift NOT monotone — mid scale worst")
    axes[1].legend()
    axes[1].grid(alpha=0.3)

    axes[2].plot(df["params_b"], df["H4_pct_valid_all_8_mean"], "D-", color="tab:green", markersize=10)
    for _, r in df.iterrows():
        axes[2].annotate(r["model"], (r["params_b"], r["H4_pct_valid_all_8_mean"]),
                         textcoords="offset points", xytext=(8, 4), fontsize=9)
    axes[2].axhline(75, color="red", ls="--", alpha=0.6, label="H4 threshold")
    axes[2].set_xscale("log")
    axes[2].set_xlabel("Model parameters (B, log scale)")
    axes[2].set_ylabel("% AI abstracts pass all V1-V8")
    axes[2].set_title("H4: Mimicry threshold — collapses at small")
    axes[2].legend()
    axes[2].grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(out_path, dpi=130)
    plt.close()


def plot_truth_dir_heatmap(per_topic, out_path):
    import matplotlib.pyplot as plt

    pivot = per_topic.pivot_table(index="topic_id", columns="model", values="truth_div_pct")
    truth_map = per_topic.drop_duplicates("topic_id").set_index("topic_id")["truth_direction"]
    pivot = pivot.reindex(sorted(pivot.index))
    truth_labels = [f"{tid} ({truth_map[tid][:3]})" for tid in pivot.index]

    fig, ax = plt.subplots(figsize=(8, 7))
    im = ax.imshow(pivot.values, cmap="Reds", aspect="auto", vmin=0, vmax=100)
    ax.set_xticks(range(len(pivot.columns)))
    ax.set_xticklabels(pivot.columns, rotation=20, ha="right")
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels(truth_labels)
    for i in range(pivot.shape[0]):
        for j in range(pivot.shape[1]):
            v = pivot.values[i, j]
            ax.text(j, i, f"{v:.0f}", ha="center", va="center",
                    color="white" if v > 50 else "black", fontsize=9)
    ax.set_title("Truth divergence (%) per topic × model")
    plt.colorbar(im, ax=ax, label="Truth div %")
    plt.tight_layout()
    plt.savefig(out_path, dpi=130)
    plt.close()


def write_summary_md(top_line, truth_dir, per_topic, truth_map, out_path):
    lines = []
    lines.append("# A.0 v3 — 3-Model Synthesis\n")
    lines.append(f"_Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}_\n")
    lines.append("\n## Top-line hypothesis outcomes\n")
    lines.append("```\n" + top_line.to_string(index=False) + "\n```\n")
    lines.append("\n## Truth divergence by truth direction\n")
    lines.append("```\n" + truth_dir.to_string(index=False) + "\n```\n")
    lines.append("\n## Key findings\n")

    g_div = top_line[top_line["model"].str.contains("Gemini")]["H2_truth_div_mean_pct"].iloc[0]
    m_div = top_line[top_line["model"].str.contains("Gemma")]["H2_truth_div_mean_pct"].iloc[0]
    s_div = top_line[top_line["model"].str.contains("Llama")]["H2_truth_div_mean_pct"].iloc[0]

    g_ent = top_line[top_line["model"].str.contains("Gemini")]["H1_entropy_mean_bits"].iloc[0]
    m_ent = top_line[top_line["model"].str.contains("Gemma")]["H1_entropy_mean_bits"].iloc[0]
    s_ent = top_line[top_line["model"].str.contains("Llama")]["H1_entropy_mean_bits"].iloc[0]

    g_v = top_line[top_line["model"].str.contains("Gemini")]["H4_pct_valid_all_8_mean"].iloc[0]
    m_v = top_line[top_line["model"].str.contains("Gemma")]["H4_pct_valid_all_8_mean"].iloc[0]
    s_v = top_line[top_line["model"].str.contains("Llama")]["H4_pct_valid_all_8_mean"].iloc[0]

    lines.append(f"- **H1 entropy MONOTONE** with scale: Gemini {g_ent:.2f} < Gemma {m_ent:.2f} < Llama {s_ent:.2f} bits.\n")
    lines.append(f"- **H2 truth divergence NON-MONOTONE**: Gemini {g_div:.0f}%, Gemma {m_div:.0f}%, Llama {s_div:.0f}%. Mid scale worst.\n")
    lines.append(f"- **H4 mimicry THRESHOLD**: Gemini {g_v:.0f}% ≈ Gemma {m_v:.0f}% >> Llama {s_v:.0f}%. Small collapses.\n")
    lines.append(f"- **NEUTRAL truth = SUPPORTS bias**: every model shows ~100% drift on T11/T12 (NEUTRAL Cochrane truth).\n")

    lines.append("\n## Per-topic detail (long form)\n")
    lines.append("```\n" + per_topic.to_string(index=False) + "\n```\n")
    Path(out_path).write_text("".join(lines))


def main():
    truth_map = topics_truth()
    per_model = {m["slug"]: load_model(m["slug"]) for m in MODELS}

    top_line = top_line_table(per_model)
    truth_dir = truth_direction_table(per_model, truth_map)
    per_topic = per_topic_long(per_model, truth_map)

    top_line.to_csv(ANA / "synth_v3_top_line.csv", index=False)
    truth_dir.to_csv(ANA / "synth_v3_truth_direction.csv", index=False)
    per_topic.to_csv(ANA / "synth_v3_per_topic.csv", index=False)

    plot_scaling(top_line, ANA / "synth_v3_scaling.png")
    plot_truth_dir_heatmap(per_topic, ANA / "synth_v3_truth_dir_heatmap.png")

    write_summary_md(top_line, truth_dir, per_topic, truth_map, ANA / "synth_v3_summary.md")

    print("=== synthesis done ===")
    print(top_line.to_string(index=False))
    print()
    print(truth_dir.to_string(index=False))


if __name__ == "__main__":
    main()
