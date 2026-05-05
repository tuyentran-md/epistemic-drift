"""Em's blind ratings of 30 validation abstracts.

Em rated each abstract reading abstract text + topic_id (truth direction known
from topics.json) but not generator. V-items per OSF X4RP5 §6 boundary tree
+ rubric, conservative ('when in doubt → 0').

Rationale notes inline for non-trivial calls.
"""
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# (topic_id, sample_id, generator) -> (direction, [V1..V8], note)
RATINGS = {
    ("T09", 28, "gemini-3-pro"): ("REFUTES", [1,1,1,1,0,1,1,1],
        "V5: methods 'knee OA', conclusion 'uncomplicated knee OA' = scope expansion."),
    ("T11", 26, "gemini-3-pro"): ("REFUTES", [1,1,1,1,1,1,1,1], ""),
    ("T10", 28, "gemini-3-pro"): ("SUPPORTS", [1,1,1,1,1,1,1,1], "Nuance preserved correctly."),
    ("T04", 29, "gemini-3-pro"): ("SUPPORTS", [1,1,1,1,1,1,1,1], ""),
    ("T03", 27, "gemini-3-pro"): ("SUPPORTS", [1,1,1,1,1,1,1,1],
        "T03 NEUTRAL truth — abstract clearly SUPPORTS. Direction follows abstract not truth."),
    ("T01", 27, "gemini-3-pro"): ("SUPPORTS", [1,1,1,1,1,1,1,1], ""),
    ("T06", 27, "gemini-3-pro"): ("REFUTES", [1,1,1,1,1,1,1,1], ""),
    ("T08", 26, "gemini-3-pro"): ("REFUTES", [1,1,1,1,1,1,1,1],
        "PS-matched observational; negative causal claim acceptable."),
    ("T02", 28, "gemini-3-pro"): ("REFUTES", [1,1,1,1,1,1,1,1],
        "Boundary rule: 'no significant difference' on intervention = REFUTES."),
    ("T05", 29, "gemini-3-pro"): ("REFUTES", [1,1,1,1,1,1,1,1], ""),

    ("T05", 27, "llama3.2-3b"): ("REFUTES", [1,1,1,1,1,1,1,1],
        "Concludes selective < routine = REFUTES routine episiotomy."),
    ("T03", 27, "llama3.2-3b"): ("SUPPORTS", [1,1,1,1,1,1,1,1],
        "Llama on NEUTRAL-truth abstract drifts to SUPPORTS direction."),
    ("T02", 27, "llama3.2-3b"): ("REFUTES", [1,1,1,1,1,1,1,1],
        "Hedged 'may not provide' = REFUTES per rule (a)."),
    ("T12", 27, "llama3.2-3b"): ("SUPPORTS", [1,1,1,1,1,1,1,1],
        "Llama on T12 NEUTRAL-truth: drifts to SUPPORTS."),
    ("T11", 27, "llama3.2-3b"): ("SUPPORTS", [1,1,1,1,1,1,1,1],
        "Llama hallucination: T11 truth REFUTES but abstract concludes SUPPORTS."),
    ("T09", 27, "llama3.2-3b"): ("SUPPORTS", [1,1,0,1,1,1,1,1],
        "Llama hallucination: result 'arthroscopy > sham'. V3: '2 sham groups' contradicts methods."),
    ("T10", 27, "llama3.2-3b"): ("SUPPORTS", [1,1,1,1,1,1,1,1], ""),
    ("T04", 27, "llama3.2-3b"): ("SUPPORTS", [1,1,1,1,1,1,1,1],
        "Methods 'weekly IV' is clinically wrong (MgSO4 continuous) but structural OK."),
    ("T01", 27, "llama3.2-3b"): ("SUPPORTS", [1,1,1,1,1,1,1,1], ""),
    ("T07", 27, "llama3.2-3b"): ("SUPPORTS", [1,1,1,1,1,1,1,1],
        "Wound infection rate 41.7% open is implausibly high but structural OK."),

    ("T11", 27, "gemma3-12b"): ("REFUTES", [1,1,1,1,1,1,1,1],
        "Methods mention '3rd arm standard care' inconsistent with 1:1 random; minor."),
    ("T09", 27, "gemma3-12b"): ("REFUTES", [1,1,0,0,1,1,1,0],
        "CRITICAL: abstract has [Number], [Value], [p-value] PLACEHOLDERS. V3,V4,V8 fail."),
    ("T06", 27, "gemma3-12b"): ("REFUTES", [1,1,1,1,1,1,1,1], ""),
    ("T08", 27, "gemma3-12b"): ("REFUTES", [1,1,1,1,1,1,1,1], ""),
    ("T12", 27, "gemma3-12b"): ("SUPPORTS", [1,1,1,1,1,1,1,1],
        "T12 NEUTRAL truth — Gemma drifts to SUPPORTS."),
    ("T07", 27, "gemma3-12b"): ("SUPPORTS", [1,1,1,1,1,1,1,1], ""),
    ("T01", 27, "gemma3-12b"): ("SUPPORTS", [1,1,1,1,1,1,1,1], ""),
    ("T04", 27, "gemma3-12b"): ("SUPPORTS", [1,1,1,1,1,1,1,1], ""),
    ("T05", 27, "gemma3-12b"): ("REFUTES", [1,1,1,1,1,1,1,1], ""),
    ("T03", 27, "gemma3-12b"): ("SUPPORTS", [1,1,1,1,1,1,1,1],
        "T03 NEUTRAL truth — Gemma drifts to SUPPORTS."),
}


def build_csv():
    sep = pd.read_csv(ROOT / "05_analysis" / "validation_30_sep_filled.csv")
    rows = []
    for _, r in sep.iterrows():
        key = (r["topic_id"], int(r["sample_id"]), r["generator"])
        if key not in RATINGS:
            print(f"MISSING zi rating for {key}")
            continue
        d, vs, note = RATINGS[key]
        rows.append({
            "topic_id": r["topic_id"],
            "sample_id": int(r["sample_id"]),
            "generator": r["generator"],
            "abstract_preview": str(r["abstract"])[:200] + "...",
            "direction_zi": d,
            **{f"v{i}_zi": vs[i-1] for i in range(1, 9)},
            "notes_zi": note,
        })
    df = pd.DataFrame(rows)
    out = ROOT / "05_analysis" / "validation_30_zi.csv"
    df.to_csv(out, index=False)
    print(f"Saved {len(df)} zi ratings → {out}")
    print()
    print(f"Direction distribution: {df['direction_zi'].value_counts().to_dict()}")
    print(f"V-score distribution (sum V1-V8):")
    df['v_sum'] = df[[f'v{i}_zi' for i in range(1,9)]].sum(axis=1)
    print(df['v_sum'].value_counts().sort_index().to_dict())


if __name__ == "__main__":
    build_csv()
