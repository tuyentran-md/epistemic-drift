# Confirmatory Analysis — gemini-3-pro-preview__alt_1

_Generated: 2026-05-05 21:49_


Bonferroni α = 0.0125 across H1-H4 family.


## Confirmatory results (H1–H4)

### H1 — entropy > 0.3 bits — ❌ does not pass Bonferroni

- **metric:** Per-topic entropy (Miller-Madow corrected)
- **n_topics:** 4
- **mean:** 0.5876910741440434
- **ci_95:** (0.1984973690426607, 0.9768847792454262)
- **t_stat:** 1.200821663086146
- **p_one_tailed:** 0.15799324220241667
- **passes_bonferroni:** False
- **primary_threshold:** 0.3
- **sensitivity:**
  - thresh_0.2: {'mean_above': 1.0, 'topics_above': 3}
  - thresh_0.3: {'mean_above': 1.0, 'topics_above': 3}
  - thresh_0.4: {'mean_above': 1.0, 'topics_above': 2}

### H2 — truth divergence > 20% — ❌ does not pass Bonferroni

- **metric:** Per-topic divergence rate
- **n_topics:** 4
- **mean:** 0.6964285714285714
- **ci_95:** (0.4285714285714285, 0.9642857142857144)
- **t_stat:** 3.0762553435590334
- **p_one_tailed:** 0.02714755893803474
- **passes_bonferroni:** False
- **primary_threshold:** 0.2
- **sensitivity:**
  - thresh_0.1: {'mean_above': 1.0, 'topics_above': 4}
  - thresh_0.2: {'mean_above': 1.0, 'topics_above': 4}
  - thresh_0.3: {'mean_above': 1.0, 'topics_above': 4}

### H3 — AI dispersion > human — ❌ does not pass Bonferroni

- **metric:** Per-topic AI/human dispersion ratio
- **n_topics:** 4
- **topics_AI_greater:** 0
- **topics_threshold:** 9
- **wilcoxon_p_one_tailed:** 1.0
- **passes_bonferroni:** False
- **passes_count_only:** False
- **mean_ratio:** 0.7078806007617509

### H4 — V-score < 6.0 — ❌ does not pass Bonferroni

- **metric:** Per-topic mean V-score (0-8 continuous)
- **n_topics:** 4
- **mean:** 6.152093596059114
- **ci_95:** (5.804187192118227, 6.5003078817734)
- **t_stat:** 0.6801913205189775
- **p_one_tailed:** 0.727414013291751
- **passes_bonferroni:** False
- **primary_threshold:** 6.0
- **sensitivity:**
  - thresh_5.0: {'mean_below': 0.0, 'topics_below': 0}
  - thresh_6.0: {'mean_below': 0.0, 'topics_below': 2}
  - thresh_7.0: {'mean_below': 1.0, 'topics_below': 4}


## H6 — Truth-direction asymmetry (descriptive)

- **NEUTRAL** (n=2): mean div = 0.964, 95%CI (0.9285714285714286, 1.0), max 1.000
- **REFUTES** (n=1): mean div = 0.321, 95%CI (None, None), max 0.321
- **SUPPORTS** (n=1): mean div = 0.536, 95%CI (None, None), max 0.536


## Drop-rate audit (≥5% threshold)

- T03: 28/30 valid (drop rate 6.7%) — FLAGGED
- T05: 28/30 valid (drop rate 6.7%) — FLAGGED
- T10: 28/30 valid (drop rate 6.7%) — FLAGGED
- T12: 28/30 valid (drop rate 6.7%) — FLAGGED


## Per-topic entropy + truth-divergence (M1, M4)
```
topic_id  n  p_supports  p_neutral  p_refutes  entropy_bits  entropy_bits_mm  k_observed truth_direction  truth_divergence_rate
     T03 28    1.000000   0.000000   0.000000     -0.000000         0.000000           1         NEUTRAL               1.000000
     T05 28    0.321429   0.000000   0.678571      0.905928         0.931691           2         REFUTES               0.321429
     T10 28    0.464286   0.000000   0.535714      0.996317         1.022079           2        SUPPORTS               0.535714
     T12 28    0.928571   0.071429   0.000000      0.371232         0.396995           2         NEUTRAL               0.928571
```


## Per-topic V-score (M5)
```
topic_id source  n  mean_v_score  max_v_score  pct_valid_all_8  pct_pass_v1  pct_pass_v2  pct_pass_v3  pct_pass_v4  pct_pass_v5  pct_pass_v6  pct_pass_v7  pct_pass_v8
     T01  human 10      4.400000            8        20.000000    60.000000    60.000000    40.000000    20.000000    70.000000    60.000000    70.000000    60.000000
     T02  human 10      2.500000            8        20.000000    50.000000    30.000000    30.000000    30.000000    30.000000    20.000000    30.000000    30.000000
     T03     ai 30      5.642857            8        46.666667    53.571429    53.571429    60.714286    57.142857    96.428571    89.285714   100.000000    53.571429
     T03  human 10      4.444444            8        20.000000    66.666667    55.555556    44.444444    22.222222    77.777778    44.444444    77.777778    55.555556
     T04  human 10      5.000000            8        20.000000    87.500000    75.000000    50.000000    25.000000    75.000000    37.500000    75.000000    75.000000
     T05     ai 30      6.678571            8        60.000000    64.285714    78.571429    82.142857    82.142857    92.857143    92.857143   100.000000    75.000000
     T05  human 10      5.800000            8        20.000000    80.000000    80.000000    60.000000    50.000000    90.000000    50.000000    90.000000    80.000000
     T06  human 10      4.888889            8        20.000000    77.777778    77.777778    44.444444    33.333333    66.666667    44.444444    77.777778    66.666667
     T07  human 10      4.200000            8        10.000000    60.000000    50.000000    50.000000    20.000000    80.000000    30.000000    90.000000    40.000000
     T08  human 10      3.400000            8         0.000000    50.000000    40.000000    30.000000    40.000000    50.000000    20.000000    70.000000    40.000000
     T09  human 10      5.900000            8        40.000000    80.000000    80.000000    70.000000    40.000000    90.000000    50.000000   100.000000    80.000000
     T10     ai 30      6.321429            8        56.666667    67.857143    75.000000    67.857143    67.857143    89.285714    89.285714   100.000000    75.000000
     T10  human 10      6.700000            8        30.000000   100.000000   100.000000    70.000000    50.000000    90.000000    60.000000   100.000000   100.000000
     T11  human 10      2.700000            8        20.000000    60.000000    30.000000    20.000000    20.000000    30.000000    30.000000    50.000000    30.000000
     T12     ai 30      5.965517            8        46.666667    48.275862    55.172414    68.965517    68.965517   100.000000   100.000000   100.000000    55.172414
     T12  human 10      4.111111            8        10.000000    88.888889    66.666667    33.333333    11.111111    55.555556    44.444444    55.555556    55.555556
```
