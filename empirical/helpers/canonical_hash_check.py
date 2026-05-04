"""Audit canonical-prompt hash log for any flagged batches.

Per OSF X4RP5 §7: each generation batch logs canonical-prompt outputs at
start/mid/end. Token-level Jaccard ≥ 0.85 between all three pairs is required.
Flagged batches must be reviewed and cells re-generated if the anomaly persists
on re-run.

Run:
    python helpers/canonical_hash_check.py
"""
import re
import string
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
LOG_PATH = ROOT / "logs" / "canonical_hash_log.csv"
JACCARD_THRESHOLD = 0.85


def _tokenize(text, max_tokens=200):
    text = (text or "").lower()
    text = re.sub(rf"[{re.escape(string.punctuation)}]", " ", text)
    return text.split()[:max_tokens]


def _jaccard(a, b):
    A, B = set(a), set(b)
    if not A and not B:
        return 1.0
    return len(A & B) / max(1, len(A | B))


def audit():
    if not LOG_PATH.exists():
        raise SystemExit(f"ERROR: {LOG_PATH} not found. Run any generation batch first.")
    df = pd.read_csv(LOG_PATH)
    if df.empty:
        print("[canonical] log empty")
        return

    rows = []
    for batch_id, sub in df.groupby("batch_id"):
        ck = {r.checkpoint: r.output for r in sub.itertuples()}
        if not all(c in ck for c in ("start", "mid", "end")):
            rows.append({"batch_id": batch_id, "status": "incomplete (missing checkpoint)"})
            continue
        ts = _tokenize(ck["start"]); tm = _tokenize(ck["mid"]); te = _tokenize(ck["end"])
        j_sm = _jaccard(ts, tm); j_me = _jaccard(tm, te); j_se = _jaccard(ts, te)
        flagged = min(j_sm, j_me, j_se) < JACCARD_THRESHOLD
        rows.append({
            "batch_id": batch_id,
            "model": sub["model"].iloc[0] if "model" in sub else "?",
            "j_start_mid": round(j_sm, 3),
            "j_mid_end": round(j_me, 3),
            "j_start_end": round(j_se, 3),
            "status": "FLAGGED" if flagged else "OK",
        })
    out = pd.DataFrame(rows)
    out_path = ROOT / "logs" / "canonical_hash_audit.csv"
    out.to_csv(out_path, index=False)
    print(out.to_string(index=False))
    print(f"\nSaved → {out_path}")
    flagged = out[out["status"] == "FLAGGED"]
    if len(flagged):
        print(f"\n⚠️  {len(flagged)} batch(es) flagged. Review and re-run cells before final analysis.")
    else:
        print("\nAll batches passed Jaccard ≥ 0.85.")


if __name__ == "__main__":
    audit()
