"""
Sample 30 abstracts for sếp manual rater validation.

Strategy: stratified sample 10 per generator (frontier / 3B / 12B), distributed across topics.

Outputs:
  05_analysis/validation_30_blank.csv  — blank form for sếp to fill
  05_analysis/validation_30_with_deepseek.csv  — same 30 + DeepSeek's existing classification (for kappa later)

After sếp fills validation_30_blank.csv, run:
  python helpers/compute_kappa.py
"""

import json
import random
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SEED = 42

GEN_FILES = {
    "gemini-3-pro": ROOT / "03_data" / "ai_abstracts__gemini-3-pro-preview.csv",
    "llama3.2-3b": ROOT / "03_data" / "ai_abstracts__llama3.2_3b.csv",
    "gemma3-12b": ROOT / "03_data" / "ai_abstracts__gemma3_12b.csv",
}

N_PER_GENERATOR = 10
N_TOPICS_TO_COVER = 10  # 1 abstract per topic × 10 topics per generator


def load_existing_rater():
    """Load AI rater output (any model) to compute kappa later. Walks all rater_ai__*.jsonl."""
    out = {}
    for p in (ROOT / "05_analysis").glob("rater_ai__*.jsonl"):
        with open(p) as f:
            for line in f:
                try:
                    r = json.loads(line)
                    key = (r.get("topic_id"), r.get("sample_id"))
                    out[key] = r
                except Exception:
                    continue
    return out


def sample_one_generator(csv_path, gen_label, n_target=N_PER_GENERATOR):
    if not csv_path.exists():
        print(f"[SKIP] {gen_label}: {csv_path} not found")
        return []
    df = pd.read_csv(csv_path)
    df = df[df["abstract"].notna()].reset_index(drop=True)
    if len(df) < n_target:
        print(f"[WARN] {gen_label}: only {len(df)} abstracts available, sampling all")
        return df.assign(generator=gen_label).to_dict("records")

    # Stratified by topic: cover N_TOPICS_TO_COVER topics
    topics = sorted(df["topic_id"].unique())
    random.seed(SEED + hash(gen_label) % 1000)
    chosen_topics = random.sample(topics, min(N_TOPICS_TO_COVER, len(topics)))
    per_topic = max(1, n_target // len(chosen_topics))

    rows = []
    for t in chosen_topics:
        sub = df[df["topic_id"] == t]
        n = min(per_topic, len(sub))
        rows.extend(sub.sample(n, random_state=SEED).to_dict("records"))

    # Trim to exactly n_target
    rows = rows[:n_target]
    for r in rows:
        r["generator"] = gen_label
    return rows


def main():
    out_dir = ROOT / "05_analysis"
    out_dir.mkdir(exist_ok=True)

    all_samples = []
    for gen_label, csv_path in GEN_FILES.items():
        all_samples.extend(sample_one_generator(csv_path, gen_label))

    if not all_samples:
        print("ERROR: no abstracts available to sample")
        return

    df = pd.DataFrame(all_samples)
    # Ensure columns
    for col in ["topic_id", "sample_id", "specialty", "generator", "abstract"]:
        if col not in df.columns:
            df[col] = None

    # Blank form for sếp (V1-V8 v3 design)
    blank = df[["topic_id", "sample_id", "specialty", "generator", "abstract"]].copy()
    for v in ["direction_human", "v1_human", "v2_human", "v3_human", "v4_human",
              "v5_human", "v6_human", "v7_human", "v8_human", "notes_human"]:
        blank[v] = ""
    blank_path = out_dir / "validation_30_blank.csv"
    blank.to_csv(blank_path, index=False)
    print(f"[Blank form] {len(blank)} rows → {blank_path}")
    print("Sếp fills columns: direction_human (SUPPORTS/NEUTRAL/REFUTES), v1_human..v7_human (0/1)")

    # Same sample + DeepSeek classifications for later kappa computation
    rater = load_existing_rater()
    rows_ds = []
    for _, row in df.iterrows():
        key = (row["topic_id"], int(row["sample_id"]) if pd.notna(row["sample_id"]) else None)
        ds = rater.get(key, {})
        out_row = {
            "topic_id": row["topic_id"],
            "sample_id": row["sample_id"],
            "generator": row["generator"],
            "abstract_preview": (row["abstract"] or "")[:200] + "...",
            "rater_used": ds.get("rater_model"),
            "ai_direction": ds.get("direction"),
            **{f"ai_v{i}": ds.get(f"v{i}") for i in range(1, 9)},
        }
        rows_ds.append(out_row)
    ds_path = out_dir / "validation_30_with_deepseek.csv"
    pd.DataFrame(rows_ds).to_csv(ds_path, index=False)
    print(f"[DeepSeek shadow] {len(rows_ds)} rows → {ds_path}")
    print("\nNext: open validation_30_blank.csv in Numbers/Excel, classify 30 abstracts, save.")
    print("Then: python helpers/compute_kappa.py")


if __name__ == "__main__":
    main()
