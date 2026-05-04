# Confirmatory Analysis — gemini-3-pro-preview__alt_2

_Generated: 2026-05-05 06:34_


Bonferroni α = 0.0125 across H1-H4 family.


## Confirmatory results (H1–H4)

### H1 — entropy > 0.3 bits — ❌ does not pass Bonferroni

- **metric:** Per-topic entropy (Miller-Madow corrected)
- **n_topics:** 4
- **mean:** 0.5296918465885534
- **ci_95:** (0.18532412003823148, 0.7676796635423683)
- **t_stat:** 1.261029225071472
- **p_one_tailed:** 0.1482226187867152
- **passes_bonferroni:** False
- **primary_threshold:** 0.3
- **sensitivity:**
  - thresh_0.2: {'mean_above': 1.0, 'topics_above': 3}
  - thresh_0.3: {'mean_above': 1.0, 'topics_above': 3}
  - thresh_0.4: {'mean_above': 1.0, 'topics_above': 3}

### H2 — truth divergence > 20% — ❌ does not pass Bonferroni

- **metric:** Per-topic divergence rate
- **n_topics:** 4
- **mean:** 0.5690972222222221
- **ci_95:** (0.19374999999999995, 0.9444444444444444)
- **t_stat:** 1.693841627460696
- **p_one_tailed:** 0.09443462849887599
- **passes_bonferroni:** False
- **primary_threshold:** 0.2
- **sensitivity:**
  - thresh_0.1: {'mean_above': 1.0, 'topics_above': 4}
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
- **mean_ratio:** 0.6334734475437692

### H4 — V-score < 6.0 — ❌ does not pass Bonferroni

- **metric:** Per-topic mean V-score (0-8 continuous)
- **n_topics:** 4
- **mean:** 7.85
- **ci_95:** (7.625, 8.0)
- **t_stat:** 15.543108932710906
- **p_one_tailed:** 0.9997106702638197
- **passes_bonferroni:** False
- **primary_threshold:** 6.0
- **sensitivity:**
  - thresh_5.0: {'mean_below': 0.0, 'topics_below': 0}
  - thresh_6.0: {'mean_below': 0.0, 'topics_below': 0}
  - thresh_7.0: {'mean_below': 0.0, 'topics_below': 0}


## H6 — Truth-direction asymmetry (descriptive)

- **NEUTRAL** (n=2): mean div = 0.944, 95%CI (0.8888888888888888, 1.0), max 1.000
- **REFUTES** (n=1): mean div = 0.188, 95%CI (None, None), max 0.188
- **SUPPORTS** (n=1): mean div = 0.200, 95%CI (None, None), max 0.200


## Drop-rate audit (≥5% threshold)

- T03: 16/30 valid (drop rate 46.7%) — FLAGGED
- T05: 16/30 valid (drop rate 46.7%) — FLAGGED
- T10: 10/30 valid (drop rate 66.7%) — FLAGGED
- T12: 9/30 valid (drop rate 70.0%) — FLAGGED


## Per-topic entropy + truth-divergence (M1, M4)
```
topic_id  n  p_supports  p_neutral  p_refutes  entropy_bits  entropy_bits_mm  k_observed truth_direction  truth_divergence_rate
     T03 16    1.000000   0.000000     0.0000     -0.000000         0.000000           1         NEUTRAL               1.000000
     T05 16    0.187500   0.000000     0.8125      0.696212         0.741296           2         REFUTES               0.187500
     T10 10    0.800000   0.000000     0.2000      0.721928         0.794063           2        SUPPORTS               0.200000
     T12  9    0.888889   0.111111     0.0000      0.503258         0.583408           2         NEUTRAL               0.888889
```


## Per-topic V-score (M5)
```
topic_id source  n  mean_v_score  max_v_score  pct_valid_all_8  pct_pass_v1  pct_pass_v2  pct_pass_v3  pct_pass_v4  pct_pass_v5  pct_pass_v6  pct_pass_v7  pct_pass_v8
     T01  human 10      4.200000            8        20.000000    70.000000    60.000000    30.000000    40.000000    70.000000    40.000000    60.000000    50.000000
     T02  human 10      2.666667            8        20.000000    44.444444    33.333333    33.333333    33.333333    33.333333    22.222222    33.333333    33.333333
     T03     ai 17      8.000000            8        94.117647   100.000000   100.000000   100.000000   100.000000   100.000000   100.000000   100.000000   100.000000
     T03  human 10      4.333333            8        10.000000    55.555556    55.555556    44.444444    11.111111    88.888889    33.333333    88.888889    55.555556
     T04  human 10      4.400000            8        20.000000    70.000000    70.000000    50.000000    30.000000    60.000000    40.000000    60.000000    60.000000
     T05     ai 17      7.500000            8        82.352941    87.500000    93.750000    93.750000    93.750000    93.750000    93.750000   100.000000    93.750000
     T05  human 10      5.600000            8        20.000000    80.000000    70.000000    60.000000    50.000000    90.000000    50.000000    90.000000    70.000000
     T06  human 10      4.900000            8        10.000000    80.000000    80.000000    40.000000    40.000000    70.000000    40.000000    70.000000    70.000000
     T07  human 10      4.500000            8        20.000000    70.000000    60.000000    50.000000    20.000000    80.000000    30.000000    90.000000    50.000000
     T08  human 10      3.400000            8         0.000000    50.000000    40.000000    40.000000    40.000000    50.000000    20.000000    60.000000    40.000000
     T09  human 10      5.888889            8        40.000000    77.777778    77.777778    66.666667    55.555556    88.888889    55.555556    88.888889    77.777778
     T10     ai 10      7.900000            8        90.000000    90.000000   100.000000   100.000000   100.000000   100.000000   100.000000   100.000000   100.000000
     T10  human 10      6.500000            8        10.000000   100.000000   100.000000    75.000000    37.500000    75.000000    62.500000   100.000000   100.000000
     T11  human 10      2.700000            8        20.000000    60.000000    30.000000    20.000000    20.000000    30.000000    30.000000    50.000000    30.000000
     T12     ai 10      8.000000            8        90.000000   100.000000   100.000000   100.000000   100.000000   100.000000   100.000000   100.000000   100.000000
     T12  human 10      3.700000            8        10.000000    80.000000    60.000000    30.000000    10.000000    50.000000    40.000000    50.000000    50.000000
```
