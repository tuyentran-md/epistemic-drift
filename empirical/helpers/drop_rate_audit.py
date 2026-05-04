"""Audit drop-rate per cell across all models and prompts.

Per OSF X4RP5 §5: any cell where (n_planned - n_valid) / n_planned ≥ 5% is
flagged in the manuscript and analysed both with and without the cell.

Counts non-null abstracts per (model, topic, prompt_id) cell against
N_PLANNED_PER_TOPIC = 30.

Run:
    python helpers/drop_rate_audit.py
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "03_data"
N_PLANNED_PER_TOPIC = 30
DROP_THRESHOLD = 0.05


def main():
    rows = []
    for f in sorted(DATA.glob("ai_abstracts__*.csv")):
        df = pd.read_csv(f)
        if df.empty:
            continue
        slug = f.stem.replace("ai_abstracts__", "")
        # Determine model + prompt_id
        if "__" in slug:
            model_part, prompt_id = slug.rsplit("__", 1)
            if prompt_id not in ("primary", "alt_1", "alt_2"):
                model_part, prompt_id = slug, "primary"
        else:
            model_part, prompt_id = slug, "primary"

        df_valid = df[df["abstract"].notna()] if "abstract" in df.columns else df
        for tid, sub in df_valid.groupby("topic_id"):
            n_valid = len(sub)
            drop_rate = (N_PLANNED_PER_TOPIC - n_valid) / N_PLANNED_PER_TOPIC
            rows.append({
                "model": model_part,
                "prompt_id": prompt_id,
                "topic_id": tid,
                "n_valid": n_valid,
                "n_planned": N_PLANNED_PER_TOPIC,
                "drop_rate": round(drop_rate, 3),
                "flag": drop_rate >= DROP_THRESHOLD,
            })

    if not rows:
        print("No ai_abstracts__*.csv found in 03_data/.")
        return
    out = pd.DataFrame(rows)
    out_path = ROOT / "logs" / "drop_rate_audit.csv"
    out_path.parent.mkdir(exist_ok=True)
    out.to_csv(out_path, index=False)
    flagged = out[out["flag"]]
    print(out.to_string(index=False))
    print(f"\nSaved → {out_path}")
    if len(flagged):
        print(f"\n⚠️  {len(flagged)} cell(s) flagged drop-rate ≥ {DROP_THRESHOLD:.0%}")
    else:
        print(f"\nAll cells within drop-rate tolerance.")


if __name__ == "__main__":
    main()
