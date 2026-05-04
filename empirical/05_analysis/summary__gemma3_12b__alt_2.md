# Confirmatory Analysis — gemma3:12b__alt_2

_Generated: 2026-05-05 03:35_


Bonferroni α = 0.0125 across H1-H4 family.


## Confirmatory results (H1–H4)

### H1 — entropy > 0.3 bits — ❌ does not pass Bonferroni

- **metric:** Per-topic entropy (Miller-Madow corrected)
- **n_topics:** 4
- **mean:** 0.16063759455083718
- **ci_95:** (0.0, 0.32127518910167435)
- **t_stat:** -1.4045309752221
- **p_one_tailed:** 0.8726040223111907
- **passes_bonferroni:** False
- **primary_threshold:** 0.3
- **sensitivity:**
  - thresh_0.2: {'mean_above': 0.0, 'topics_above': 2}
  - thresh_0.3: {'mean_above': 0.0, 'topics_above': 1}
  - thresh_0.4: {'mean_above': 0.0, 'topics_above': 1}

### H2 — truth divergence > 20% — ❌ does not pass Bonferroni

- **metric:** Per-topic divergence rate
- **n_topics:** 4
- **mean:** 0.4731481481481482
- **ci_95:** (0.0, 0.9462962962962964)
- **t_stat:** 0.9994488902758343
- **p_one_tailed:** 0.1956150818960747
- **passes_bonferroni:** False
- **primary_threshold:** 0.2
- **sensitivity:**
  - thresh_0.1: {'mean_above': 1.0, 'topics_above': 2}
  - thresh_0.2: {'mean_above': 1.0, 'topics_above': 2}
  - thresh_0.3: {'mean_above': 1.0, 'topics_above': 2}

### H3 — AI dispersion > human — ❌ does not pass Bonferroni

- **metric:** Per-topic AI/human dispersion ratio
- **n_topics:** 4
- **topics_AI_greater:** 0
- **topics_threshold:** 9
- **wilcoxon_p_one_tailed:** 1.0
- **passes_bonferroni:** False
- **passes_count_only:** False
- **mean_ratio:** 0.7436254598801664

### H4 — V-score < 6.0 — ❌ does not pass Bonferroni

- **metric:** Per-topic mean V-score (0-8 continuous)
- **n_topics:** 4
- **mean:** 7.173243933588761
- **ci_95:** (6.711111111111111, 7.436206896551724)
- **t_stat:** 5.058639047043589
- **p_one_tailed:** 0.9925461052332205
- **passes_bonferroni:** False
- **primary_threshold:** 6.0
- **sensitivity:**
  - thresh_5.0: {'mean_below': 0.0, 'topics_below': 0}
  - thresh_6.0: {'mean_below': 0.0, 'topics_below': 0}
  - thresh_7.0: {'mean_below': 0.0, 'topics_below': 1}


## H6 — Truth-direction asymmetry (descriptive)

- **NEUTRAL** (n=2): mean div = 0.946, 95%CI (0.925925925925926, 0.9666666666666668), max 0.967
- **REFUTES** (n=1): mean div = 0.000, 95%CI (None, None), max 0.000
- **SUPPORTS** (n=1): mean div = 0.000, 95%CI (None, None), max 0.000


## Drop-rate audit (≥5% threshold)

- T10: 27/30 valid (drop rate 10.0%) — FLAGGED
- T12: 27/30 valid (drop rate 10.0%) — FLAGGED


## Per-topic entropy + truth-divergence (M1, M4)
```
topic_id  n  p_supports  p_neutral  p_refutes  entropy_bits  entropy_bits_mm  k_observed truth_direction  truth_divergence_rate
     T03 30    0.966667   0.033333        0.0      0.210842         0.234887           2         NEUTRAL               0.966667
     T05 30    0.000000   0.000000        1.0     -0.000000         0.000000           1         REFUTES               0.000000
     T10 27    1.000000   0.000000        0.0     -0.000000         0.000000           1        SUPPORTS               0.000000
     T12 27    0.925926   0.074074        0.0      0.380947         0.407663           2         NEUTRAL               0.925926
```


## Per-topic V-score (M5)
```
topic_id source  n  mean_v_score  max_v_score  pct_valid_all_8  pct_pass_v1  pct_pass_v2  pct_pass_v3  pct_pass_v4  pct_pass_v5  pct_pass_v6  pct_pass_v7  pct_pass_v8
     T01  human 10      4.100000            8        20.000000    60.000000    60.000000    40.000000    20.000000    70.000000    40.000000    70.000000    50.000000
     T02  human 10      3.333333            8        10.000000    66.666667    44.444444    33.333333    22.222222    44.444444    22.222222    55.555556    44.444444
     T03     ai 30      7.466667            8        63.333333   100.000000   100.000000    80.000000    66.666667   100.000000   100.000000   100.000000   100.000000
     T03  human 10      4.600000            8        20.000000    70.000000    60.000000    40.000000    40.000000    80.000000    30.000000    80.000000    60.000000
     T04  human 10      4.666667            8        10.000000    88.888889    77.777778    44.444444    22.222222    66.666667    55.555556    66.666667    44.444444
     T05     ai 30      7.400000            8        66.666667    96.666667   100.000000    76.666667    76.666667   100.000000    93.333333   100.000000    96.666667
     T05  human 10      5.800000            8        30.000000    80.000000    70.000000    60.000000    50.000000    90.000000    60.000000   100.000000    70.000000
     T06  human 10      5.000000            8        10.000000    80.000000    70.000000    40.000000    40.000000    70.000000    50.000000    80.000000    70.000000
     T07  human 10      4.000000            8        10.000000    60.000000    50.000000    40.000000    20.000000    80.000000    20.000000    90.000000    40.000000
     T08  human 10      4.100000            8        10.000000    60.000000    60.000000    40.000000    40.000000    60.000000    30.000000    60.000000    60.000000
     T09  human 10      6.000000            8        30.000000    90.000000    90.000000    60.000000    30.000000    90.000000    60.000000    90.000000    90.000000
     T10     ai 30      7.344828            8        60.000000   100.000000   100.000000    78.571429    67.857143   100.000000   100.000000   100.000000   100.000000
     T10  human 10      6.600000            8        20.000000   100.000000   100.000000    70.000000    50.000000    80.000000    60.000000   100.000000   100.000000
     T11  human 10      2.700000            8        10.000000    60.000000    30.000000    30.000000    10.000000    30.000000    30.000000    50.000000    30.000000
     T12     ai 30      6.481481            8        30.000000    96.296296    96.153846    69.230769    50.000000   100.000000    57.692308   100.000000    92.592593
     T12  human 10      4.400000            8        10.000000    80.000000    60.000000    20.000000    20.000000    70.000000    60.000000    80.000000    50.000000
```
