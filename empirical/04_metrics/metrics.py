"""
Metrics pipeline for OSF X4RP5.

M1: Conclusion direction Shannon entropy (dual-rater classifier).
M2: Effect size CV (regex extract numerics).
M3: Semantic dispersion (TF-IDF + cosine).
M4: Truth divergence rate vs Cochrane (uses M1 output + topics.json truth labels).
M5: Per-abstract structural validity V1-V8 (dual-rater evaluator).

Rater models per registration:
  - DeepSeek V3.1 (primary, 50%)
  - Claude Sonnet 4.5 (secondary, 50%)
  - Split is deterministic via xxhash.xxh64 of (topic_id, sample_id|pmid).

Rater prompt (incl. boundary decision tree) lives in 02_generation/prompts/rating.txt.

Examples:
    GEN_MODEL=gemini-3-pro-preview python 04_metrics/metrics.py
    GEN_MODEL=gemma3:12b python 04_metrics/metrics.py --prompt-suffix __alt_1
"""

import argparse
import json
import math
import os
import re
import sys
import time
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
import xxhash
from dotenv import load_dotenv
from openai import OpenAI
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_distances
from tqdm import tqdm

ROOT = Path(__file__).resolve().parent.parent
PROMPTS_DIR = ROOT / "02_generation" / "prompts"
load_dotenv(ROOT / ".env")

OPENROUTER_KEY = os.environ.get("OPENROUTER_API_KEY")
if not OPENROUTER_KEY:
    sys.exit("ERROR: OPENROUTER_API_KEY missing in .env")

RATER_PRIMARY = "deepseek/deepseek-chat-v3.1"
RATER_SECONDARY = "anthropic/claude-sonnet-4.5"

GEN_MODEL = os.environ.get("GEN_MODEL", "gemini-3-pro-preview")
MODEL_SLUG = GEN_MODEL.replace("/", "_").replace(":", "_")

# Optional suffix for sensitivity-arm files (e.g. "__alt_1"); default empty for primary
PROMPT_SUFFIX = os.environ.get("PROMPT_SUFFIX", "")
SENSITIVITY_RATER = RATER_PRIMARY  # DeepSeek-only for exploratory arm per OSF prereg


def pick_rater(topic_id, sample_id_or_pmid):
    """Deterministic 50/50 split via xxhash.xxh64 (replaces non-deterministic Python hash())."""
    h = xxhash.xxh64(f"{topic_id}_{sample_id_or_pmid}".encode("utf-8")).intdigest()
    return RATER_PRIMARY if (h % 2 == 0) else RATER_SECONDARY


def load_rating_prompt():
    path = PROMPTS_DIR / "rating.txt"
    if not path.exists():
        sys.exit(f"ERROR: rating prompt not found at {path}")
    return path.read_text()


client = OpenAI(api_key=OPENROUTER_KEY, base_url="https://openrouter.ai/api/v1")
RATING_PROMPT = load_rating_prompt()


# ───── Data loading ──────────────────────────────────────────────────────────
def load_data():
    topics = json.load(open(ROOT / "01_topics" / "topics.json"))["topics"]
    truth = {t["id"]: t["cochrane_truth"]["direction"] for t in topics}
    suffix = PROMPT_SUFFIX  # e.g. "" or "__alt_1"
    ai_path = ROOT / "03_data" / f"ai_abstracts__{MODEL_SLUG}{suffix}.csv"
    if not ai_path.exists():
        sys.exit(f"ERROR: AI abstracts file not found: {ai_path}")
    ai = pd.read_csv(ai_path)
    human = pd.read_csv(ROOT / "03_data" / "human_abstracts.csv")
    ai = ai[ai["abstract"].notna()].reset_index(drop=True)
    human = human[human["abstract"].notna()].reset_index(drop=True)
    print(f"[load_data] AI from {ai_path.name} ({len(ai)} rows), human ({len(human)} rows)")
    return topics, truth, ai, human


# ───── M1 + M5 combined: dual-rater (boundary tree in prompt file) ───────────


def rate_one(abstract_text, model_override=None):
    """Single rater call returning {direction, v1..v8, rater_model}.
    Boundary decision tree is embedded in 02_generation/prompts/rating.txt."""
    rater = model_override or RATER_PRIMARY
    try:
        resp = client.chat.completions.create(
            model=rater,
            messages=[{"role": "user", "content": RATING_PROMPT.replace("[ABSTRACT]", abstract_text)}],
            temperature=0.0,
            max_tokens=300,
        )
        raw = (resp.choices[0].message.content or "").strip()
        if not raw:
            return {"error": "empty_response", "rater_model": rater}
        # Strip code fences if present
        if raw.startswith("```"):
            raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw, flags=re.MULTILINE).strip()
        result = json.loads(raw)
        result["rater_model"] = rater
        return result
    except Exception as e:
        return {"error": str(e), "rater_model": rater}


def run_rater(df, label, single_rater=False):
    """Incremental flush per row → resumable on timeout. Dual-rater split via xxhash.
    single_rater=True forces DeepSeek-only (used for sensitivity arm per OSF prereg)."""
    out_jsonl = ROOT / "05_analysis" / f"rater_{label}__{MODEL_SLUG}{PROMPT_SUFFIX}.jsonl"
    out_jsonl.parent.mkdir(exist_ok=True)

    done_keys = set()
    if out_jsonl.exists():
        with open(out_jsonl) as f:
            for line in f:
                try:
                    r = json.loads(line)
                    key = (r.get("topic_id"), r.get("sample_id"), r.get("pmid"))
                    done_keys.add(key)
                except Exception:
                    continue

    if single_rater:
        print(f"[M1+M5] Rating {label} via single rater ({SENSITIVITY_RATER}) — exploratory arm")
    else:
        print(f"[M1+M5] Rating {label} via dual-rater 50/50 ({RATER_PRIMARY} + {RATER_SECONDARY})")
    print(f"        already done: {len(done_keys)}/{len(df)}")
    with open(out_jsonl, "a") as fout:
        for _, row in tqdm(df.iterrows(), total=len(df), desc=f"Rate {label}"):
            sid = row.get("sample_id") if "sample_id" in row else None
            pmid = row.get("pmid") if "pmid" in row else None
            key = (row.get("topic_id"), sid, pmid)
            if key in done_keys:
                continue
            if single_rater:
                rater_id = SENSITIVITY_RATER
            else:
                rater_id = pick_rater(row["topic_id"], sid if sid is not None else pmid)
            r = rate_one(row["abstract"], model_override=rater_id)
            r["topic_id"] = row["topic_id"]
            if "sample_id" in row:
                r["sample_id"] = int(row["sample_id"]) if pd.notna(row["sample_id"]) else None
            if "pmid" in row:
                r["pmid"] = row["pmid"]
            r["source"] = label
            fout.write(json.dumps(r) + "\n")
            fout.flush()
            time.sleep(0.05)

    # Aggregate
    rows = []
    with open(out_jsonl) as f:
        for line in f:
            rows.append(json.loads(line))
    return pd.DataFrame(rows)


# ───── M2: Effect size CV ────────────────────────────────────────────────────
NUMERIC_PATTERNS = [
    r"\b(?:RR|relative risk|risk ratio)[^\d\-\.]{0,10}([0-9]*\.?[0-9]+)\b",
    r"\b(?:OR|odds ratio)[^\d\-\.]{0,10}([0-9]*\.?[0-9]+)\b",
    r"\b(?:HR|hazard ratio)[^\d\-\.]{0,10}([0-9]*\.?[0-9]+)\b",
    r"\b(?:SMD|standardized mean difference)[^\d\-\.]{0,10}(-?[0-9]*\.?[0-9]+)\b",
    r"\b(?:MD|mean difference)[^\d\-\.]{0,10}(-?[0-9]*\.?[0-9]+)\b",
]


def extract_effect_estimate(text):
    """Return the first numeric effect estimate found, or None."""
    for pat in NUMERIC_PATTERNS:
        m = re.search(pat, text, flags=re.IGNORECASE)
        if m:
            try:
                v = float(m.group(1))
                if 0 < v < 100:  # sanity filter
                    return v
            except ValueError:
                continue
    return None


def compute_cv(df, label):
    print(f"[M2] Extracting effect estimates from {len(df)} {label} abstracts...")
    df = df.copy()
    df["effect"] = df["abstract"].apply(extract_effect_estimate)
    rows = []
    for tid, sub in df.groupby("topic_id"):
        vals = sub["effect"].dropna().values
        n_total = len(sub)
        n_with_estimate = len(vals)
        if n_with_estimate >= 3:
            mean = float(np.mean(vals))
            sd = float(np.std(vals, ddof=1))
            cv = sd / mean if mean else None
        else:
            mean = sd = cv = None
        rows.append({
            "topic_id": tid,
            "source": label,
            "n_total": n_total,
            "n_with_estimate": n_with_estimate,
            "mean_effect": mean,
            "sd_effect": sd,
            "cv": cv,
        })
    return pd.DataFrame(rows)


# ───── M3: Semantic dispersion ───────────────────────────────────────────────
def compute_dispersion(ai_df, human_df):
    """TF-IDF cosine dispersion per topic. Per-topic vectorizer fit (vocabulary scoped to that topic)."""
    print(f"[M3] Computing TF-IDF cosine dispersion...")
    rows = []
    for tid in ai_df["topic_id"].unique():
        ai_sub = ai_df[ai_df["topic_id"] == tid]["abstract"].tolist()
        hu_sub = human_df[human_df["topic_id"] == tid]["abstract"].tolist()

        # Fit vectorizer on combined corpus for this topic so AI and human use same vocab
        all_texts = ai_sub + hu_sub
        if len(all_texts) < 2:
            continue
        vec = TfidfVectorizer(stop_words="english", max_features=2000, ngram_range=(1, 2))
        try:
            vec.fit(all_texts)
        except ValueError:
            continue

        ai_disp = mean_pairwise_distance_tfidf(vec, ai_sub) if len(ai_sub) >= 2 else None
        hu_disp = mean_pairwise_distance_tfidf(vec, hu_sub) if len(hu_sub) >= 2 else None

        rows.append({
            "topic_id": tid,
            "n_ai": len(ai_sub),
            "n_human": len(hu_sub),
            "ai_dispersion": ai_disp,
            "human_dispersion": hu_disp,
            "ratio_ai_to_human": (ai_disp / hu_disp) if (ai_disp and hu_disp) else None,
        })
    return pd.DataFrame(rows)


def mean_pairwise_distance_tfidf(vec, texts):
    if len(texts) < 2:
        return None
    X = vec.transform(texts)
    distances = cosine_distances(X)
    n = len(texts)
    upper = distances[np.triu_indices(n, k=1)]
    return float(upper.mean())


# ───── M1 + M4: Entropy + truth divergence (from rater output) ──────────────
def compute_entropy_and_divergence(rater_df, truth):
    """Per-topic Shannon entropy + truth divergence rate (AI only)."""
    rater_ai = rater_df[rater_df["source"] == "ai"].copy()
    rater_ai = rater_ai[rater_ai.get("direction").notna()] if "direction" in rater_ai.columns else rater_ai
    rater_ai = rater_ai[rater_ai["direction"].isin(["SUPPORTS", "NEUTRAL", "REFUTES"])]

    rows = []
    for tid, sub in rater_ai.groupby("topic_id"):
        cnt = Counter(sub["direction"])
        total = sum(cnt.values())
        if total == 0:
            rows.append({"topic_id": tid, "entropy_bits": None, "n": 0,
                        "p_supports": None, "p_neutral": None, "p_refutes": None,
                        "truth_direction": truth.get(tid), "truth_divergence_rate": None})
            continue
        ps = {k: cnt[k] / total for k in ["SUPPORTS", "NEUTRAL", "REFUTES"]}
        entropy_raw = -sum(p * math.log2(p) for p in ps.values() if p > 0)
        # Miller-Madow bias correction: H_MM = H_raw + (K_obs - 1) / (2 * N * ln(2)) bits
        # K_obs = number of categories with non-zero probability
        k_obs = sum(1 for p in ps.values() if p > 0)
        entropy_mm = entropy_raw + (k_obs - 1) / (2 * total * math.log(2))
        truth_dir = truth.get(tid)
        divergence = 1 - (cnt[truth_dir] / total) if truth_dir else None
        rows.append({
            "topic_id": tid,
            "n": total,
            "p_supports": ps["SUPPORTS"],
            "p_neutral": ps["NEUTRAL"],
            "p_refutes": ps["REFUTES"],
            "entropy_bits": entropy_raw,
            "entropy_bits_mm": entropy_mm,
            "k_observed": k_obs,
            "truth_direction": truth_dir,
            "truth_divergence_rate": divergence,
        })
    return pd.DataFrame(rows)


# ───── M5: Structural validity aggregates ────────────────────────────────────
def compute_validity(rater_df):
    """Now V1-V8 (was V1-V7). max V_score = 8."""
    df = rater_df.copy()
    v_cols = [f"v{i}" for i in range(1, 9)]
    for c in v_cols:
        if c not in df.columns:
            df[c] = None
    df["v_sum"] = df[v_cols].sum(axis=1, min_count=1)
    df["valid_flag"] = (df["v_sum"] == 8).astype(int)

    rows = []
    for (tid, src), sub in df.groupby(["topic_id", "source"]):
        rows.append({
            "topic_id": tid,
            "source": src,
            "n": len(sub),
            "mean_v_score": sub["v_sum"].mean(),
            "max_v_score": 8,
            "pct_valid_all_8": sub["valid_flag"].mean() * 100,
            **{f"pct_pass_{c}": sub[c].mean() * 100 for c in v_cols},
        })
    return pd.DataFrame(rows)


# ───── Main orchestrator ─────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--single-rater", action="store_true",
                    help="Use only DeepSeek (for sensitivity arm exploratory rating)")
    args = ap.parse_args()

    out = ROOT / "05_analysis"
    out.mkdir(exist_ok=True)
    suffix = f"__{MODEL_SLUG}{PROMPT_SUFFIX}"

    topics, truth, ai, human = load_data()
    print(f"Loaded {len(ai)} AI + {len(human)} human abstracts across {len(topics)} topics "
          f"(model: {GEN_MODEL}, prompt suffix: {PROMPT_SUFFIX or '(primary)'})")

    cv_ai = compute_cv(ai, "ai")
    cv_human = compute_cv(human, "human")
    cv_combined = pd.concat([cv_ai, cv_human], ignore_index=True)
    cv_combined.to_csv(out / f"m2_cv{suffix}.csv", index=False)
    print(f"[M2] Saved → m2_cv{suffix}.csv")

    disp = compute_dispersion(ai, human)
    disp.to_csv(out / f"m3_dispersion{suffix}.csv", index=False)
    print(f"[M3] Saved → m3_dispersion{suffix}.csv")

    rater_ai = run_rater(ai, "ai", single_rater=args.single_rater)
    rater_human = run_rater(human, "human", single_rater=args.single_rater)
    rater_all = pd.concat([rater_ai, rater_human], ignore_index=True)
    rater_all.to_csv(out / f"rater_raw{suffix}.csv", index=False)
    print(f"[M1+M5] Saved raw rater output → rater_raw{suffix}.csv")

    ent_div = compute_entropy_and_divergence(rater_all, truth)
    ent_div.to_csv(out / f"m1_m4_entropy_divergence{suffix}.csv", index=False)
    print(f"[M1+M4] Saved → m1_m4_entropy_divergence{suffix}.csv")

    val = compute_validity(rater_all)
    val.to_csv(out / f"m5_validity{suffix}.csv", index=False)
    print(f"[M5] Saved → m5_validity{suffix}.csv")

    print("\n=== ALL METRICS COMPLETE ===")
    print("Next: python 05_analysis/analyze.py")


if __name__ == "__main__":
    main()
