# Empirical Drift — Companion to OSF X4RP5

> **OSF preregistration:** [https://doi.org/10.17605/OSF.IO/X4RP5](https://doi.org/10.17605/OSF.IO/X4RP5)
> **Paper title:** *Structural validity and truth-direction fidelity of LLM-generated medical abstracts across model scales: a preregistered evaluation*
> **Author:** Tuyen Tran, MD (Vinmec Central Park, HCMC).

This directory contains the full code, prompts, and pilot data for the empirical study. It is the companion to the theoretical [Epistemic Drift](../README.md) work.

---

## Layout

```
empirical/
├── 01_topics/
│   └── topics.json              # 12 topics: 4 SUPPORTS / 6 REFUTES / 2 NEUTRAL
├── 02_generation/
│   ├── generate.py              # AI generation + Europe PMC human pull + canonical-hash check
│   └── prompts/
│       ├── primary.txt          # confirmatory generation prompt (1080 abstracts)
│       ├── alt_1.txt            # sensitivity arm — "evidence summary" framing
│       ├── alt_2.txt            # sensitivity arm — "guideline appendix" framing
│       ├── canonical.txt        # behavioural-stability check prompt (primes 100-200)
│       └── rating.txt           # rating prompt incl. boundary decision tree
├── 03_data/                     # generated abstracts + human comparators (gitignored .tmp; CSVs committed)
├── 04_metrics/
│   └── metrics.py               # M1-M5 + dual rater (DeepSeek V3.1 + Claude Sonnet 4.5, xxhash split)
├── 05_analysis/
│   ├── analyze.py               # H1-H6 confirmatory tests, Miller-Madow, Bonferroni, bootstrap CI
│   └── synthesize_v3.py         # 3-model side-by-side synthesis
├── helpers/
│   ├── sample_for_validation.py     # 30-abstract human-rater subsample (SEED=42)
│   ├── test_retest_sample.py        # 10-of-30 retest subsample (SEED=43)
│   ├── csv_to_xlsx.py               # convert blank csv → xlsx with dropdowns
│   ├── canonical_hash_check.py      # audit canonical-prompt log (Jaccard ≥ 0.85)
│   ├── drop_rate_audit.py           # flag cells with drop-rate ≥ 5%
│   └── compute_kappa.py             # κ human vs LLM raters + intra-rater retest
├── pilot_2026-05-03/            # archived pilot data (NOT used in confirmatory analysis)
├── logs/                        # canonical_hash_log.csv + run logs
├── .env.example                 # template for API keys (real .env gitignored)
├── requirements.txt
└── README.md (this file)
```

---

## Setup

```bash
cd empirical
python3.14 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Copy .env.example → .env, fill GOOGLE_API_KEY{,_2,_3} + OPENROUTER_API_KEY
cp .env.example .env
# edit .env

# Local Ollama models (mid + small generators)
brew install ollama && brew services start ollama
ollama pull gemma3:12b
ollama pull llama3.2:3b
```

---

## Run order

### Smoke test (1 topic × 3 models × 5 reps)

```bash
GEN_BACKEND=gemini GEN_MODEL=gemini-3-pro-preview \
  python 02_generation/generate.py --mode ai --prompt primary \
  --topics T01 --n 5

GEN_BACKEND=ollama GEN_MODEL=gemma3:12b \
  python 02_generation/generate.py --mode ai --prompt primary \
  --topics T01 --n 5

GEN_BACKEND=ollama GEN_MODEL=llama3.2:3b \
  python 02_generation/generate.py --mode ai --prompt primary \
  --topics T01 --n 5
```

### Primary generation (12 topics × 30 reps × 3 models = 1080)

```bash
# Gemini first — API access window expires 30 May 2026
GEN_BACKEND=gemini GEN_MODEL=gemini-3-pro-preview \
  python 02_generation/generate.py --mode ai --prompt primary

GEN_BACKEND=ollama GEN_MODEL=gemma3:12b \
  python 02_generation/generate.py --mode ai --prompt primary

GEN_BACKEND=ollama GEN_MODEL=llama3.2:3b \
  python 02_generation/generate.py --mode ai --prompt primary
```

### Sensitivity arm (4 topics × 30 reps × 3 models × 2 alt prompts = 720)

Topics for sensitivity: T03 (NEUTRAL IM), T05 (REFUTES OB), T10 (SUPPORTS Peds), T12 (NEUTRAL Peds).

```bash
for prompt in alt_1 alt_2; do
  for backend_model in "gemini gemini-3-pro-preview" "ollama gemma3:12b" "ollama llama3.2:3b"; do
    BE=${backend_model%% *}; MOD=${backend_model##* }
    GEN_BACKEND=$BE GEN_MODEL=$MOD \
      python 02_generation/generate.py --mode ai --prompt $prompt --topics T03,T05,T10,T12
  done
done
```

### Human comparators

```bash
python 02_generation/generate.py --mode human
```

### Rating

```bash
# Primary (dual-rater)
for slug in gemini-3-pro-preview gemma3:12b llama3.2:3b; do
  GEN_MODEL=$slug python 04_metrics/metrics.py
done

# Sensitivity arm (DeepSeek-only per OSF prereg)
for prompt_suffix in __alt_1 __alt_2; do
  for slug in gemini-3-pro-preview gemma3:12b llama3.2:3b; do
    GEN_MODEL=$slug PROMPT_SUFFIX=$prompt_suffix \
      python 04_metrics/metrics.py --single-rater
  done
done
```

### Analysis

```bash
for slug in gemini-3-pro-preview gemma3:12b llama3.2:3b; do
  GEN_MODEL=$slug python 05_analysis/analyze.py
done
python 05_analysis/synthesize_v3.py
```

### Audits

```bash
python helpers/drop_rate_audit.py
python helpers/canonical_hash_check.py
```

### Human validation

```bash
python helpers/sample_for_validation.py
python helpers/csv_to_xlsx.py            # produces validation_30_blank.xlsx with dropdowns
# Sếp rates 30 abstracts (~ 4 hours)
python helpers/compute_kappa.py
# 14 ± 2 days later:
python helpers/test_retest_sample.py
# Sếp re-rates 10 abstracts blinded
python helpers/compute_kappa.py --retest
```

---

## Hypotheses (OSF X4RP5 §4)

Confirmatory:
- **H1** mean per-topic entropy (Miller-Madow corrected) > 0.3 bits, one-tailed.
- **H2** mean per-topic truth-divergence rate > 0.20, one-tailed.
- **H3** AI semantic dispersion > human in ≥ 9/12 topics (Wilcoxon paired).
- **H4** mean per-topic V-score < 6.0, one-tailed.
- **H5** Cohen's κ (human vs LLM rater subset) ≥ 0.7.
- **H6** truth-direction asymmetry (descriptive).

Exploratory:
- **H7** scaling pattern across model scale (Spearman ρ over 3 models, descriptive).
- Per-V-item failure pattern.
- Prompt-sensitivity comparison (3 prompts × 4 topics × 3 models, DeepSeek-only).

Bonferroni-corrected α = 0.05 / 4 = 0.0125 across H1–H4 stat tests.

---

## Reproducibility notes

- All four prompt templates (primary, alt_1, alt_2, canonical) and the rating prompt are version-controlled at `prompts/`. Frozen at the GitHub release tag matching the OSF registration.
- xxhash.xxh64 is used for deterministic 50/50 rater split (replaces non-deterministic Python `hash()`).
- Canonical-prompt hash is logged at start/mid/end of every generation batch. Token-level Jaccard ≥ 0.85 across all three pairs is the pass criterion.
- Pilot data lives at `pilot_2026-05-03/` and is **not used** in any confirmatory analysis.

---

## License

MIT. See [`../LICENSE`](../LICENSE) (to be added).
