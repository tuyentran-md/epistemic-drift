"""Sample 10 of the 30 validation abstracts for human test-retest rating (SEED=43).

Per OSF X4RP5 §7: sole human rater re-rates 10 of 30 validation abstracts ~14 days
later, blinded to prior session, to compute intra-rater κ. Threshold ≥ 0.7 is
required for the human–LLM κ comparison (H5) to be interpretable.

Run after sếp completes the primary 30-abstract validation rating
(`validation_30_blank.xlsx` or `.csv`).

Outputs:
  05_analysis/retest_10_blank.csv  — 10 abstracts, blank columns for re-rating
"""
import random
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SEED = 43
N_RETEST = 10


def main():
    src = ROOT / "05_analysis" / "validation_30_blank.csv"
    if not src.exists():
        raise SystemExit(f"ERROR: {src} not found. Run sample_for_validation.py first.")
    df = pd.read_csv(src)
    if len(df) != 30:
        print(f"WARNING: validation_30_blank.csv has {len(df)} rows (expected 30).")

    random.seed(SEED)
    indices = sorted(random.sample(range(len(df)), min(N_RETEST, len(df))))
    sample = df.iloc[indices].copy().reset_index(drop=True)

    # Blank columns for re-rating; rater must NOT see prior session
    blank_cols = ["direction_human", "v1_human", "v2_human", "v3_human", "v4_human",
                  "v5_human", "v6_human", "v7_human", "v8_human", "notes_human"]
    for c in blank_cols:
        sample[c] = ""

    out = ROOT / "05_analysis" / "retest_10_blank.csv"
    sample.to_csv(out, index=False)
    print(f"[retest sample] {len(sample)} rows → {out}")
    print(f"  topics: {sorted(sample['topic_id'].unique())}")
    print(f"  generators: {sample['generator'].value_counts().to_dict()}")
    print(f"\nSếp re-rates blinded to prior session (≥ 14 days gap).")
    print(f"Then: python helpers/compute_kappa.py (intra-rater retest κ)")


if __name__ == "__main__":
    main()
