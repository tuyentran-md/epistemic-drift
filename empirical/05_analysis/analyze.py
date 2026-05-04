"""
Analysis pipeline for OSF X4RP5.

Confirmatory hypothesis tests (H1–H6) + exploratory tests (H7, prompt-sensitivity, per-V-item).

H1 — Mean per-topic entropy (Miller-Madow corrected) > 0.3 bits, one-tailed.
H2 — Mean per-topic truth-divergence rate > 0.20, one-tailed.
H3 — Wilcoxon paired AI > human dispersion, ≥9/12 topics with ratio > 1.
H4 — Mean per-topic V-score (continuous, 0-8) < 6.0, one-tailed.
H5 — Cohen's κ (human vs LLM rater subset) ≥ 0.7 (computed in helpers/compute_kappa.py).
H6 — Truth-direction asymmetry (descriptive).

Bias correction: Miller-Madow on entropy (computed in metrics.py).
Multiple comparison: Bonferroni across H1–H4 (α = 0.05/4 = 0.0125 for stat tests; H5/H6 reported separately).
Confidence intervals: 95% bootstrap (n=10000).

Drop-rate flag: any cell where (n_valid / n_planned) < 0.95 is reported.

Inputs (from 04_metrics):
    m1_m4_entropy_divergence__{slug}{suffix}.csv
    m2_cv__{slug}{suffix}.csv
    m3_dispersion__{slug}{suffix}.csv
    m5_validity__{slug}{suffix}.csv

Run:
    GEN_MODEL=gemini-3-pro-preview python 05_analysis/analyze.py [--mode confirmatory|exploratory|all]
    GEN_MODEL=gemma3:12b PROMPT_SUFFIX=__alt_1 python 05_analysis/analyze.py
"""

import argparse
import json
import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
ANA = ROOT / "05_analysis"
GEN_MODEL = os.environ.get("GEN_MODEL", "gemini-3-pro-preview")
MODEL_SLUG = GEN_MODEL.replace("/", "_").replace(":", "_")
PROMPT_SUFFIX = os.environ.get("PROMPT_SUFFIX", "")
SUFFIX = f"__{MODEL_SLUG}{PROMPT_SUFFIX}"

# Pre-registered thresholds (OSF X4RP5 §4)
H1_ENTROPY_THRESHOLD = 0.3
H2_DIVERGENCE_THRESHOLD = 0.20
H3_TOPIC_COUNT_THRESHOLD = 9
H4_VSCORE_THRESHOLD = 6.0
DROP_RATE_THRESHOLD = 0.05  # ≥5% drop per cell flagged (OSF §5)
N_PLANNED_PER_TOPIC = 30
ALPHA = 0.05
N_HYPOTHESES_FAMILY = 4  # H1-H4 stat tests; H5 (κ) reported separately, H6 descriptive
ALPHA_BONFERRONI = ALPHA / N_HYPOTHESES_FAMILY  # 0.0125

# Sensitivity-analysis cutoffs (OSF §4 threshold provenance)
H1_SENSITIVITY = [0.2, 0.3, 0.4]
H2_SENSITIVITY = [0.10, 0.20, 0.30]
H4_SENSITIVITY = [5.0, 6.0, 7.0]

BOOTSTRAP_N = 10000
RNG = np.random.default_rng(42)

plt.rcParams.update({"figure.dpi": 110, "savefig.dpi": 150, "font.size": 10})


def _safe_read(path):
    try:
        return pd.read_csv(path)
    except (pd.errors.EmptyDataError, FileNotFoundError):
        return pd.DataFrame()


def load_metrics():
    return {
        "ent_div": _safe_read(ANA / f"m1_m4_entropy_divergence{SUFFIX}.csv"),
        "cv": _safe_read(ANA / f"m2_cv{SUFFIX}.csv"),
        "disp": _safe_read(ANA / f"m3_dispersion{SUFFIX}.csv"),
        "val": _safe_read(ANA / f"m5_validity{SUFFIX}.csv"),
    }


def bootstrap_ci(values, stat_fn=np.mean, n=BOOTSTRAP_N, ci=0.95):
    arr = np.asarray(values, dtype=float)
    arr = arr[~np.isnan(arr)]
    if len(arr) < 2:
        return (None, None)
    idx = RNG.integers(0, len(arr), size=(n, len(arr)))
    samples = stat_fn(arr[idx], axis=1)
    lo = np.percentile(samples, 100 * (1 - ci) / 2)
    hi = np.percentile(samples, 100 * (1 + ci) / 2)
    return float(lo), float(hi)


# ───── Confirmatory hypothesis tests ────────────────────────────────────────
def test_h1(ent_div):
    """H1: mean per-topic entropy (Miller-Madow corrected) > 0.3 bits, one-tailed."""
    col = "entropy_bits_mm" if "entropy_bits_mm" in ent_div.columns else "entropy_bits"
    ent = ent_div[col].dropna()
    mean = ent.mean()
    ci = bootstrap_ci(ent.values)
    sensitivity = {f"thresh_{t}": {
        "mean_above": float(mean > t),
        "topics_above": int((ent > t).sum()),
    } for t in H1_SENSITIVITY}
    if len(ent) > 1:
        t_stat, p_two = stats.ttest_1samp(ent, H1_ENTROPY_THRESHOLD)
        p_one = (p_two / 2) if t_stat > 0 else (1 - p_two / 2)
    else:
        t_stat, p_one = None, None
    return {
        "name": "H1 — entropy > 0.3 bits",
        "metric": "Per-topic entropy (Miller-Madow corrected)",
        "n_topics": len(ent),
        "mean": float(mean) if not np.isnan(mean) else None,
        "ci_95": ci,
        "t_stat": float(t_stat) if t_stat is not None else None,
        "p_one_tailed": float(p_one) if p_one is not None else None,
        "passes_bonferroni": bool(p_one is not None and p_one < ALPHA_BONFERRONI),
        "primary_threshold": H1_ENTROPY_THRESHOLD,
        "sensitivity": sensitivity,
    }


def test_h2(ent_div):
    """H2: mean per-topic truth-divergence rate > 0.20, one-tailed."""
    div = ent_div["truth_divergence_rate"].dropna()
    mean = div.mean()
    ci = bootstrap_ci(div.values)
    sensitivity = {f"thresh_{t}": {
        "mean_above": float(mean > t),
        "topics_above": int((div > t).sum()),
    } for t in H2_SENSITIVITY}
    if len(div) > 1:
        t_stat, p_two = stats.ttest_1samp(div, H2_DIVERGENCE_THRESHOLD)
        p_one = (p_two / 2) if t_stat > 0 else (1 - p_two / 2)
    else:
        t_stat, p_one = None, None
    return {
        "name": "H2 — truth divergence > 20%",
        "metric": "Per-topic divergence rate",
        "n_topics": len(div),
        "mean": float(mean) if not np.isnan(mean) else None,
        "ci_95": ci,
        "t_stat": float(t_stat) if t_stat is not None else None,
        "p_one_tailed": float(p_one) if p_one is not None else None,
        "passes_bonferroni": bool(p_one is not None and p_one < ALPHA_BONFERRONI),
        "primary_threshold": H2_DIVERGENCE_THRESHOLD,
        "sensitivity": sensitivity,
    }


def test_h3(disp):
    """H3: AI dispersion > human; Wilcoxon + ≥9/12 topics with ratio > 1."""
    paired = disp.dropna(subset=["ai_dispersion", "human_dispersion"])
    n_topics = len(paired)
    if n_topics < 3:
        return {
            "name": "H3 — AI dispersion > human",
            "n_topics": n_topics,
            "passes_bonferroni": False,
            "note": "n<3, test skipped",
        }
    n_above = (paired["ratio_ai_to_human"] > 1).sum()
    try:
        w_stat, p_w = stats.wilcoxon(paired["ai_dispersion"], paired["human_dispersion"],
                                     alternative="greater")
    except ValueError:
        w_stat, p_w = None, None
    confirmed_count = int(n_above >= H3_TOPIC_COUNT_THRESHOLD)
    return {
        "name": "H3 — AI dispersion > human",
        "metric": "Per-topic AI/human dispersion ratio",
        "n_topics": n_topics,
        "topics_AI_greater": int(n_above),
        "topics_threshold": H3_TOPIC_COUNT_THRESHOLD,
        "wilcoxon_p_one_tailed": float(p_w) if p_w is not None else None,
        "passes_bonferroni": bool(p_w is not None and p_w < ALPHA_BONFERRONI and n_above >= H3_TOPIC_COUNT_THRESHOLD),
        "passes_count_only": bool(confirmed_count),
        "mean_ratio": float(paired["ratio_ai_to_human"].mean()),
    }


def test_h4(val):
    """H4: mean per-topic V-score < 6.0, one-tailed (testing for sub-strong validity)."""
    ai_val = val[val["source"] == "ai"]
    if "mean_v_score" not in ai_val.columns:
        return {"name": "H4 — V-score < 6.0", "note": "mean_v_score column missing", "passes_bonferroni": False}
    vs = ai_val["mean_v_score"].dropna()
    mean = vs.mean()
    ci = bootstrap_ci(vs.values)
    sensitivity = {f"thresh_{t}": {
        "mean_below": float(mean < t),
        "topics_below": int((vs < t).sum()),
    } for t in H4_SENSITIVITY}
    if len(vs) > 1:
        t_stat, p_two = stats.ttest_1samp(vs, H4_VSCORE_THRESHOLD)
        p_one = (p_two / 2) if t_stat < 0 else (1 - p_two / 2)
    else:
        t_stat, p_one = None, None
    return {
        "name": "H4 — V-score < 6.0",
        "metric": "Per-topic mean V-score (0-8 continuous)",
        "n_topics": len(vs),
        "mean": float(mean) if not np.isnan(mean) else None,
        "ci_95": ci,
        "t_stat": float(t_stat) if t_stat is not None else None,
        "p_one_tailed": float(p_one) if p_one is not None else None,
        "passes_bonferroni": bool(p_one is not None and p_one < ALPHA_BONFERRONI),
        "primary_threshold": H4_VSCORE_THRESHOLD,
        "sensitivity": sensitivity,
    }


def test_h6_truth_direction(ent_div):
    """H6: descriptive — divergence by truth direction × model."""
    if "truth_direction" not in ent_div.columns:
        return {"name": "H6 — truth-direction asymmetry", "note": "truth_direction missing"}
    rows = []
    for direction, sub in ent_div.groupby("truth_direction"):
        d = sub["truth_divergence_rate"].dropna()
        if len(d) == 0:
            continue
        rows.append({
            "truth_direction": direction,
            "n_topics": len(d),
            "mean_divergence": float(d.mean()),
            "ci_95": bootstrap_ci(d.values),
            "max": float(d.max()),
            "min": float(d.min()),
        })
    return {"name": "H6 — truth-direction asymmetry", "by_direction": rows}


# ───── Drop-rate flag ────────────────────────────────────────────────────────
def drop_rate_audit(ent_div):
    """Flag cells where n_valid / n_planned < (1 - DROP_RATE_THRESHOLD)."""
    flagged = []
    for _, row in ent_div.iterrows():
        n_valid = row.get("n", 0)
        if pd.isna(n_valid):
            n_valid = 0
        rate = (N_PLANNED_PER_TOPIC - n_valid) / N_PLANNED_PER_TOPIC
        if rate >= DROP_RATE_THRESHOLD:
            flagged.append({
                "topic_id": row["topic_id"],
                "n_valid": int(n_valid),
                "n_planned": N_PLANNED_PER_TOPIC,
                "drop_rate": round(rate, 3),
            })
    return flagged


# ───── Plots ─────────────────────────────────────────────────────────────────
def plot_entropy(ent_div):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    col = "entropy_bits_mm" if "entropy_bits_mm" in ent_div.columns else "entropy_bits"
    d = ent_div.sort_values(col, ascending=False)
    ax.barh(d["topic_id"], d[col], color="#5b9bd5")
    ax.axvline(H1_ENTROPY_THRESHOLD, color="red", linestyle="--",
               label=f"H1 threshold ({H1_ENTROPY_THRESHOLD} bits)")
    ax.set_xlabel("Conclusion entropy (bits, Miller-Madow)")
    ax.set_title(f"M1 — Within-topic conclusion entropy ({GEN_MODEL})")
    ax.legend()
    plt.tight_layout()
    plt.savefig(ANA / f"fig1_entropy{SUFFIX}.png")
    plt.close()


def plot_divergence(ent_div):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    d = ent_div.sort_values("truth_divergence_rate", ascending=False)
    colors = ["#e74c3c" if x > H2_DIVERGENCE_THRESHOLD else "#5b9bd5"
              for x in d["truth_divergence_rate"].fillna(0)]
    ax.barh(d["topic_id"], d["truth_divergence_rate"] * 100, color=colors)
    ax.axvline(H2_DIVERGENCE_THRESHOLD * 100, color="red", linestyle="--",
               label=f"H2 threshold ({H2_DIVERGENCE_THRESHOLD * 100:.0f}%)")
    ax.set_xlabel("% AI samples divergent from Cochrane truth")
    ax.set_title(f"M4 — Truth divergence ({GEN_MODEL})")
    ax.legend()
    plt.tight_layout()
    plt.savefig(ANA / f"fig2_truth_divergence{SUFFIX}.png")
    plt.close()


def plot_dispersion(disp):
    if disp.empty:
        return
    fig, ax = plt.subplots(figsize=(8, 4.5))
    d = disp.sort_values("ratio_ai_to_human", ascending=True).reset_index(drop=True)
    x = np.arange(len(d))
    w = 0.35
    ax.bar(x - w / 2, d["ai_dispersion"], w, label="AI", color="#e74c3c")
    ax.bar(x + w / 2, d["human_dispersion"], w, label="Human", color="#3498db")
    ax.set_xticks(x)
    ax.set_xticklabels(d["topic_id"], rotation=45, ha="right")
    ax.set_ylabel("Mean pairwise cosine distance")
    ax.set_title(f"M3 — Semantic dispersion ({GEN_MODEL})")
    ax.legend()
    plt.tight_layout()
    plt.savefig(ANA / f"fig3_dispersion{SUFFIX}.png")
    plt.close()


def plot_validity(val):
    if val.empty or "mean_v_score" not in val.columns:
        return
    fig, ax = plt.subplots(figsize=(8, 4.5))
    pivot = val.pivot(index="topic_id", columns="source", values="mean_v_score")
    pivot.plot(kind="bar", ax=ax, color={"ai": "#e74c3c", "human": "#3498db"})
    ax.axhline(H4_VSCORE_THRESHOLD, color="red", linestyle="--",
               label=f"H4 threshold ({H4_VSCORE_THRESHOLD}/8)")
    ax.set_ylabel("Mean V-score (0-8)")
    ax.set_xlabel("Topic")
    ax.set_title(f"M5 — Mean V-score per topic ({GEN_MODEL})")
    ax.legend()
    plt.tight_layout()
    plt.savefig(ANA / f"fig4_validity{SUFFIX}.png")
    plt.close()


def write_summary(results, h6, dropped, ent_div, val):
    md = [f"# Confirmatory Analysis — {GEN_MODEL}{PROMPT_SUFFIX}\n",
          f"_Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}_\n",
          f"\nBonferroni α = {ALPHA_BONFERRONI:.4f} across H1-H4 family.\n"]
    md.append("\n## Confirmatory results (H1–H4)\n")
    for r in results:
        passes = r.get("passes_bonferroni")
        status = "✅ passes Bonferroni" if passes else "❌ does not pass Bonferroni"
        md.append(f"### {r['name']} — {status}\n")
        for k, v in r.items():
            if k in ("name",):
                continue
            if k == "sensitivity":
                md.append(f"- **sensitivity:**")
                for sk, sv in v.items():
                    md.append(f"  - {sk}: {sv}")
            else:
                md.append(f"- **{k}:** {v}")
        md.append("")
    md.append("\n## H6 — Truth-direction asymmetry (descriptive)\n")
    if "by_direction" in h6:
        for r in h6["by_direction"]:
            md.append(f"- **{r['truth_direction']}** (n={r['n_topics']}): "
                      f"mean div = {r['mean_divergence']:.3f}, "
                      f"95%CI {r['ci_95']}, max {r['max']:.3f}")
    md.append("")
    md.append("\n## Drop-rate audit (≥5% threshold)\n")
    if dropped:
        for d in dropped:
            md.append(f"- {d['topic_id']}: {d['n_valid']}/{d['n_planned']} valid "
                      f"(drop rate {d['drop_rate']:.1%}) — FLAGGED")
    else:
        md.append("No cells flagged.")
    md.append("")
    md.append("\n## Per-topic entropy + truth-divergence (M1, M4)\n```\n"
              + ent_div.to_string(index=False) + "\n```\n")
    md.append("\n## Per-topic V-score (M5)\n```\n"
              + val.to_string(index=False) + "\n```\n")
    out = ANA / f"summary{SUFFIX}.md"
    out.write_text("\n".join(md))
    print(f"[summary] {out}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["confirmatory", "exploratory", "all"], default="all")
    args = ap.parse_args()

    m = load_metrics()
    if m["ent_div"].empty:
        raise SystemExit(f"ERROR: m1_m4_entropy_divergence{SUFFIX}.csv not found or empty.")

    results = [
        test_h1(m["ent_div"]),
        test_h2(m["ent_div"]),
        test_h3(m["disp"]),
        test_h4(m["val"]),
    ]
    h6 = test_h6_truth_direction(m["ent_div"])
    dropped = drop_rate_audit(m["ent_div"])

    plot_entropy(m["ent_div"])
    plot_divergence(m["ent_div"])
    plot_dispersion(m["disp"])
    plot_validity(m["val"])

    write_summary(results, h6, dropped, m["ent_div"], m["val"])

    print("\n=== ANALYSIS COMPLETE ===")
    for r in results:
        passes = r.get("passes_bonferroni")
        mark = "✅" if passes else "❌"
        mean = r.get("mean")
        mean_str = f"mean={mean:.3f}" if mean is not None else ""
        print(f"  {mark} {r['name']} {mean_str}")
    if dropped:
        print(f"\n⚠️  {len(dropped)} cell(s) flagged drop-rate ≥5%")
    print(f"\nOpen {ANA / f'summary{SUFFIX}.md'} for full results.")


if __name__ == "__main__":
    main()
