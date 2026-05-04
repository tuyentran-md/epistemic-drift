# Confirmatory Analysis — gemini-3-pro-preview__alt_1

_Generated: 2026-05-05 03:19_


Bonferroni α = 0.0125 across H1-H4 family.


## Confirmatory results (H1–H4)

### H1 — entropy > 0.3 bits — ❌ does not pass Bonferroni

- **metric:** Per-topic entropy (Miller-Madow corrected)
- **n_topics:** 4
- **mean:** 0.590973176015261
- **ci_95:** (0.2110885577506129, 0.9113811792136572)
- **t_stat:** 1.3397367731711776
- **p_one_tailed:** 0.13638786090943164
- **passes_bonferroni:** False
- **primary_threshold:** 0.3
- **sensitivity:**
  - thresh_0.2: {'mean_above': 1.0, 'topics_above': 3}
  - thresh_0.3: {'mean_above': 1.0, 'topics_above': 3}
  - thresh_0.4: {'mean_above': 1.0, 'topics_above': 3}

### H2 — truth divergence > 20% — ❌ does not pass Bonferroni

- **metric:** Per-topic divergence rate
- **n_topics:** 4
- **mean:** 0.6972222222222223
- **ci_95:** (0.3916666666666667, 0.95)
- **t_stat:** 2.8733015663631862
- **p_one_tailed:** 0.03193881065604635
- **passes_bonferroni:** False
- **primary_threshold:** 0.2
- **sensitivity:**
  - thresh_0.1: {'mean_above': 1.0, 'topics_above': 4}
  - thresh_0.2: {'mean_above': 1.0, 'topics_above': 4}
  - thresh_0.3: {'mean_above': 1.0, 'topics_above': 3}

### H3 — AI dispersion > human — ❌ does not pass Bonferroni

- **metric:** Per-topic AI/human dispersion ratio
- **n_topics:** 4
- **topics_AI_greater:** 0
- **topics_threshold:** 9
- **wilcoxon_p_one_tailed:** 1.0
- **passes_bonferroni:** False
- **passes_count_only:** False
- **mean_ratio:** 0.6305502283729986

### H4 — V-score < 6.0 — ❌ does not pass Bonferroni

- **metric:** Per-topic mean V-score (0-8 continuous)
- **n_topics:** 4
- **mean:** 6.538194444444445
- **ci_95:** (6.21875, 6.9375)
- **t_stat:** 2.597441118690856
- **p_one_tailed:** 0.9597231059911601
- **passes_bonferroni:** False
- **primary_threshold:** 6.0
- **sensitivity:**
  - thresh_5.0: {'mean_below': 0.0, 'topics_below': 0}
  - thresh_6.0: {'mean_below': 0.0, 'topics_below': 0}
  - thresh_7.0: {'mean_below': 1.0, 'topics_below': 3}


## H6 — Truth-direction asymmetry (descriptive)

- **NEUTRAL** (n=2): mean div = 0.950, 95%CI (0.9, 1.0), max 1.000
- **REFUTES** (n=1): mean div = 0.222, 95%CI (None, None), max 0.222
- **SUPPORTS** (n=1): mean div = 0.667, 95%CI (None, None), max 0.667


## Drop-rate audit (≥5% threshold)

- T03: 16/30 valid (drop rate 46.7%) — FLAGGED
- T05: 9/30 valid (drop rate 70.0%) — FLAGGED
- T10: 12/30 valid (drop rate 60.0%) — FLAGGED
- T12: 10/30 valid (drop rate 66.7%) — FLAGGED


## Per-topic entropy + truth-divergence (M1, M4)
```
topic_id  n  p_supports  p_neutral  p_refutes  entropy_bits  entropy_bits_mm  k_observed truth_direction  truth_divergence_rate
     T03 16    1.000000        0.0   0.000000     -0.000000         0.000000           1         NEUTRAL               1.000000
     T05  9    0.222222        0.0   0.777778      0.764205         0.844354           2         REFUTES               0.222222
     T10 12    0.333333        0.0   0.666667      0.918296         0.978408           2        SUPPORTS               0.666667
     T12 10    0.900000        0.1   0.000000      0.468996         0.541130           2         NEUTRAL               0.900000
```


## Per-topic V-score (M5)
```
topic_id source  n  mean_v_score  max_v_score  pct_valid_all_8  pct_pass_v1  pct_pass_v2  pct_pass_v3  pct_pass_v4  pct_pass_v5  pct_pass_v6  pct_pass_v7  pct_pass_v8
     T01  human 10      4.400000            8        20.000000    60.000000    60.000000    40.000000    20.000000    70.000000    60.000000    70.000000    60.000000
     T02  human 10      2.500000            8        20.000000    50.000000    30.000000    30.000000    30.000000    30.000000    20.000000    30.000000    30.000000
     T03     ai 17      6.125000            8        58.823529    62.500000    62.500000    68.750000    68.750000    93.750000    93.750000   100.000000    62.500000
     T03  human 10      4.444444            8        20.000000    66.666667    55.555556    44.444444    22.222222    77.777778    44.444444    77.777778    55.555556
     T04  human 10      5.000000            8        20.000000    87.500000    75.000000    50.000000    25.000000    75.000000    37.500000    75.000000    75.000000
     T05     ai 11      7.111111            8        63.636364    77.777778    88.888889    88.888889    88.888889    88.888889    88.888889   100.000000    88.888889
     T05  human 10      5.800000            8        20.000000    80.000000    80.000000    60.000000    50.000000    90.000000    50.000000    90.000000    80.000000
     T06  human 10      4.888889            8        20.000000    77.777778    77.777778    44.444444    33.333333    66.666667    44.444444    77.777778    66.666667
     T07  human 10      4.200000            8        10.000000    60.000000    50.000000    50.000000    20.000000    80.000000    30.000000    90.000000    40.000000
     T08  human 10      3.400000            8         0.000000    50.000000    40.000000    30.000000    40.000000    50.000000    20.000000    70.000000    40.000000
     T09  human 10      5.900000            8        40.000000    80.000000    80.000000    70.000000    40.000000    90.000000    50.000000   100.000000    80.000000
     T10     ai 14      6.416667            8        50.000000    58.333333    75.000000    75.000000    75.000000    91.666667    91.666667   100.000000    75.000000
     T10  human 10      6.700000            8        30.000000   100.000000   100.000000    70.000000    50.000000    90.000000    60.000000   100.000000   100.000000
     T11  human 10      2.700000            8        20.000000    60.000000    30.000000    20.000000    20.000000    30.000000    30.000000    50.000000    30.000000
     T12     ai 10      6.500000            8        70.000000    70.000000    70.000000    70.000000    70.000000   100.000000   100.000000   100.000000    70.000000
     T12  human 10      4.111111            8        10.000000    88.888889    66.666667    33.333333    11.111111    55.555556    44.444444    55.555556    55.555556
```
