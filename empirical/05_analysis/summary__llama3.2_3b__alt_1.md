# Confirmatory Analysis — llama3.2:3b__alt_1

_Generated: 2026-05-05 03:19_


Bonferroni α = 0.0125 across H1-H4 family.


## Confirmatory results (H1–H4)

### H1 — entropy > 0.3 bits — ❌ does not pass Bonferroni

- **metric:** Per-topic entropy (Miller-Madow corrected)
- **n_topics:** 4
- **mean:** 0.6856032961813084
- **ci_95:** (0.445017624511376, 0.9261889678512409)
- **t_stat:** 2.695324415748962
- **p_one_tailed:** 0.037039450060826186
- **passes_bonferroni:** False
- **primary_threshold:** 0.3
- **sensitivity:**
  - thresh_0.2: {'mean_above': 1.0, 'topics_above': 4}
  - thresh_0.3: {'mean_above': 1.0, 'topics_above': 4}
  - thresh_0.4: {'mean_above': 1.0, 'topics_above': 3}

### H2 — truth divergence > 20% — ✅ passes Bonferroni

- **metric:** Per-topic divergence rate
- **n_topics:** 4
- **mean:** 0.7982142857142858
- **ci_95:** (0.5321428571428571, 0.9482142857142858)
- **t_stat:** 4.484775208898804
- **p_one_tailed:** 0.010338926024953723
- **passes_bonferroni:** True
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
- **mean_ratio:** 0.7988035141619674

### H4 — V-score < 6.0 — ✅ passes Bonferroni

- **metric:** Per-topic mean V-score (0-8 continuous)
- **n_topics:** 4
- **mean:** 3.3916666666666666
- **ci_95:** (3.033333333333333, 3.75)
- **t_stat:** -12.234115757851734
- **p_one_tailed:** 0.0005879963583786659
- **passes_bonferroni:** True
- **primary_threshold:** 6.0
- **sensitivity:**
  - thresh_5.0: {'mean_below': 1.0, 'topics_below': 4}
  - thresh_6.0: {'mean_below': 1.0, 'topics_below': 4}
  - thresh_7.0: {'mean_below': 1.0, 'topics_below': 4}


## H6 — Truth-direction asymmetry (descriptive)

- **NEUTRAL** (n=2): mean div = 0.914, 95%CI (0.9, 0.9285714285714286), max 0.929
- **REFUTES** (n=1): mean div = 0.400, 95%CI (None, None), max 0.400
- **SUPPORTS** (n=1): mean div = 0.964, 95%CI (None, None), max 0.964


## Drop-rate audit (≥5% threshold)

- T03: 28/30 valid (drop rate 6.7%) — FLAGGED
- T10: 28/30 valid (drop rate 6.7%) — FLAGGED


## Per-topic entropy + truth-divergence (M1, M4)
```
topic_id  n  p_supports  p_neutral  p_refutes  entropy_bits  entropy_bits_mm  k_observed truth_direction  truth_divergence_rate
     T03 28    0.928571   0.071429   0.000000      0.371232         0.396995           2         NEUTRAL               0.928571
     T05 30    0.400000   0.000000   0.600000      0.970951         0.994996           2         REFUTES               0.400000
     T10 28    0.035714   0.142857   0.821429      0.805858         0.857382           3        SUPPORTS               0.964286
     T12 30    0.900000   0.100000   0.000000      0.468996         0.493041           2         NEUTRAL               0.900000
```


## Per-topic V-score (M5)
```
topic_id source  n  mean_v_score  max_v_score  pct_valid_all_8  pct_pass_v1  pct_pass_v2  pct_pass_v3  pct_pass_v4  pct_pass_v5  pct_pass_v6  pct_pass_v7  pct_pass_v8
     T01  human 10      4.300000            8        20.000000    70.000000    60.000000    40.000000    20.000000    70.000000    40.000000    70.000000    60.000000
     T02  human 10      2.777778            8        20.000000    55.555556    33.333333    22.222222    22.222222    33.333333    22.222222    55.555556    33.333333
     T03     ai 30      3.857143            8        10.000000    32.142857    28.571429    21.428571    10.714286    82.142857    82.142857   100.000000    28.571429
     T03  human 10      5.000000            8        20.000000    66.666667    77.777778    55.555556    22.222222    77.777778    55.555556    77.777778    66.666667
     T04  human 10      4.600000            8        20.000000    80.000000    70.000000    50.000000    30.000000    60.000000    40.000000    70.000000    60.000000
     T05     ai 30      2.966667            8        10.000000    20.000000    16.666667    10.000000    10.000000    66.666667    60.000000    96.666667    16.666667
     T05  human 10      6.100000            8        30.000000    90.000000    90.000000    70.000000    50.000000    80.000000    50.000000    90.000000    90.000000
     T06  human 10      4.900000            8        10.000000    80.000000    70.000000    40.000000    40.000000    80.000000    40.000000    80.000000    60.000000
     T07  human 10      4.222222            8        10.000000    66.666667    55.555556    55.555556    22.222222    77.777778    22.222222    77.777778    44.444444
     T08  human 10      3.400000            8        10.000000    70.000000    44.444444    33.333333    33.333333    44.444444    22.222222    60.000000    50.000000
     T09  human 10      6.000000            8        30.000000    90.000000    90.000000    70.000000    30.000000    90.000000    50.000000    90.000000    90.000000
     T10     ai 30      3.642857            8        10.000000    39.285714    42.857143    25.000000    10.714286    57.142857    53.571429    96.428571    39.285714
     T10  human 10      6.300000            8        20.000000   100.000000    90.000000    60.000000    40.000000    90.000000    60.000000   100.000000    90.000000
     T11  human 10      2.777778            8        10.000000    55.555556    33.333333    22.222222    11.111111    33.333333    33.333333    55.555556    33.333333
     T12     ai 30      3.100000            8         3.333333    16.666667    20.000000    16.666667    10.000000    83.333333    53.333333   100.000000    10.000000
     T12  human 10      4.333333            8        20.000000    77.777778    66.666667    44.444444    22.222222    66.666667    55.555556    55.555556    44.444444
```
