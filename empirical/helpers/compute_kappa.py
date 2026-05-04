"""
Compute Cohen's kappa between sếp and DeepSeek on 30-abstract validation set.

Reads:
  05_analysis/validation_30_blank.csv  (filled by sếp)
  05_analysis/validation_30_with_deepseek.csv

Outputs:
  05_analysis/validation_kappa.md
"""

from pathlib import Path

import pandas as pd
from sklearn.metrics import cohen_kappa_score, accuracy_score

ROOT = Path(__file__).resolve().parent.parent


def main():
    out_dir = ROOT / "05_analysis"
    blank_path = out_dir / "validation_30_blank.csv"
    ds_path = out_dir / "validation_30_with_deepseek.csv"

    if not blank_path.exists():
        print(f"ERROR: {blank_path} not found. Run sample_for_validation.py first.")
        return

    sep = pd.read_csv(blank_path)
    ds = pd.read_csv(ds_path)

    # Merge on (topic_id, sample_id)
    merged = sep.merge(ds, on=["topic_id", "sample_id"], suffixes=("", "_ds"))

    # Filter rows where sếp filled direction
    direction_filled = merged[merged["direction_human"].notna() & (merged["direction_human"].astype(str).str.strip() != "")].copy()
    print(f"Direction labels filled by sếp: {len(direction_filled)}/{len(merged)}")

    if len(direction_filled) >= 5:
        sep_d = direction_filled["direction_human"].astype(str).str.strip().str.upper()
        ai_d = direction_filled["ai_direction"].astype(str).str.strip().str.upper()
        kappa_dir = cohen_kappa_score(sep_d, ai_d, labels=["SUPPORTS", "NEUTRAL", "REFUTES"])
        acc_dir = accuracy_score(sep_d, ai_d)
    else:
        kappa_dir = acc_dir = None

    # V1-V8 binary kappa (v3 design)
    v_kappas = {}
    for i in range(1, 9):
        col_h = f"v{i}_human"
        col_d = f"ai_v{i}"
        sub = merged[merged[col_h].notna() & merged[col_d].notna()]
        sub = sub[sub[col_h].astype(str).str.strip().isin(["0", "1"])]
        if len(sub) >= 5:
            sh = sub[col_h].astype(int)
            sd = sub[col_d].astype(int)
            v_kappas[f"V{i}"] = cohen_kappa_score(sh, sd)

    # Write markdown report
    md = ["# Rater validation: sếp vs DeepSeek V3.1\n"]
    md.append(f"_n abstracts validated: {len(direction_filled)}_\n")
    md.append("\n## Direction classification (3-way)\n")
    if kappa_dir is not None:
        md.append(f"- **Cohen's κ:** {kappa_dir:.3f}")
        md.append(f"- **Accuracy:** {acc_dir:.1%}")
        md.append(f"- **Interpretation:** " + (
            "almost perfect (κ≥0.81)" if kappa_dir >= 0.81
            else "substantial (0.61-0.80)" if kappa_dir >= 0.61
            else "moderate (0.41-0.60)" if kappa_dir >= 0.41
            else "fair (0.21-0.40)" if kappa_dir >= 0.21
            else "slight/poor (<0.21)"
        ))
    else:
        md.append("Insufficient labels.")

    md.append("\n## Structural validity items (V1-V7, binary)\n")
    if v_kappas:
        for k, v in v_kappas.items():
            md.append(f"- {k}: κ = {v:.3f}")
        mean_v = sum(v_kappas.values()) / len(v_kappas)
        md.append(f"- **Mean V-item κ:** {mean_v:.3f}")
    else:
        md.append("Insufficient labels.")

    # Confusion matrix for direction
    if kappa_dir is not None:
        md.append("\n## Confusion matrix (rows = sếp, cols = AI rater)\n")
        cm = pd.crosstab(sep_d, ai_d, margins=True)
        md.append("```\n" + cm.to_string() + "\n```\n")

    # Per-rater breakdown (DeepSeek subset vs Claude subset)
    md.append("\n## Per-AI-rater breakdown (kappa by which model rated)\n")
    if "rater_used" in direction_filled.columns:
        for rater in direction_filled["rater_used"].dropna().unique():
            sub = direction_filled[direction_filled["rater_used"] == rater]
            if len(sub) >= 3:
                k = cohen_kappa_score(
                    sub["direction_human"].astype(str).str.strip().str.upper(),
                    sub["ai_direction"].astype(str).str.strip().str.upper(),
                    labels=["SUPPORTS", "NEUTRAL", "REFUTES"]
                )
                md.append(f"- **{rater}** (n={len(sub)}): κ_direction = {k:.3f}")

    md.append("\n## Decision rule\n")
    md.append("- κ ≥ 0.80 → DeepSeek rater reliable; report finding as-is")
    md.append("- 0.60 ≤ κ < 0.80 → substantial agreement; report kappa as caveat in Methods")
    md.append("- κ < 0.60 → unreliable; switch to multi-rater consensus or manual rating")

    out_path = out_dir / "validation_kappa.md"
    out_path.write_text("\n".join(md))
    print(f"\nReport written to {out_path}")
    if kappa_dir is not None:
        print(f"Direction κ = {kappa_dir:.3f}, Accuracy = {acc_dir:.1%}")


if __name__ == "__main__":
    main()
