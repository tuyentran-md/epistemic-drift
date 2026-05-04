# Confirmatory Analysis — gemini-3-pro-preview__alt_1

_Generated: 2026-05-05 06:34_


Bonferroni α = 0.0125 across H1-H4 family.


## Confirmatory results (H1–H4)

### H1 — entropy > 0.3 bits — ❌ does not pass Bonferroni

- **metric:** Per-topic entropy (Miller-Madow corrected)
- **n_topics:** 4
- **mean:** 0.5518504078829313
- **ci_95:** (0.15364983531230103, 0.9002773860982024)
- **t_stat:** 1.2164077121278014
- **p_one_tailed:** 0.15540213021990104
- **passes_bonferroni:** False
- **primary_threshold:** 0.3
- **sensitivity:**
  - thresh_0.2: {'mean_above': 1.0, 'topics_above': 3}
  - thresh_0.3: {'mean_above': 1.0, 'topics_above': 3}
  - thresh_0.4: {'mean_above': 1.0, 'topics_above': 3}

### H2 — truth divergence > 20% — ❌ does not pass Bonferroni

- **metric:** Per-topic divergence rate
- **n_topics:** 4
- **mean:** 0.6548611111111111
- **ci_95:** (0.31875, 0.9375)
- **t_stat:** 2.371430159735605
- **p_one_tailed:** 0.04918832557631159
- **passes_bonferroni:** False
- **primary_threshold:** 0.2
- **sensitivity:**
  - thresh_0.1: {'mean_above': 1.0, 'topics_above': 4}
  - thresh_0.2: {'mean_above': 1.0, 'topics_above': 3}
  - thresh_0.3: {'mean_above': 1.0, 'topics_above': 3}

### H3 — AI dispersion > human — ❌ does not pass Bonferroni

- **metric:** Per-topic AI/human dispersion ratio
- **n_topics:** 4
- **topics_AI_greater:** 0
- **topics_threshold:** 9
- **wilcoxon_p_one_tailed:** 1.0
- **passes_bonferroni:** False
- **passes_count_only:** False
- **mean_ratio:** 0.6662041433798878

### H4 — V-score < 6.0 — ❌ does not pass Bonferroni

- **metric:** Per-topic mean V-score (0-8 continuous)
- **n_topics:** 4
- **mean:** 6.447634271099745
- **ci_95:** (6.105072463768116, 6.790196078431373)
- **t_stat:** 2.1545988566739354
- **p_one_tailed:** 0.9399071794055307
- **passes_bonferroni:** False
- **primary_threshold:** 6.0
- **sensitivity:**
  - thresh_5.0: {'mean_below': 0.0, 'topics_below': 0}
  - thresh_6.0: {'mean_below': 0.0, 'topics_below': 0}
  - thresh_7.0: {'mean_below': 1.0, 'topics_below': 4}


## H6 — Truth-direction asymmetry (descriptive)

- **NEUTRAL** (n=2): mean div = 0.938, 95%CI (0.875, 1.0), max 1.000
- **REFUTES** (n=1): mean div = 0.133, 95%CI (None, None), max 0.133
- **SUPPORTS** (n=1): mean div = 0.611, 95%CI (None, None), max 0.611


## Drop-rate audit (≥5% threshold)

- T03: 23/30 valid (drop rate 23.3%) — FLAGGED
- T05: 15/30 valid (drop rate 50.0%) — FLAGGED
- T10: 18/30 valid (drop rate 40.0%) — FLAGGED
- T12: 16/30 valid (drop rate 46.7%) — FLAGGED


## Per-topic entropy + truth-divergence (M1, M4)
```
topic_id  n  p_supports  p_neutral  p_refutes  entropy_bits  entropy_bits_mm  k_observed truth_direction  truth_divergence_rate
     T03 23    1.000000      0.000   0.000000     -0.000000         0.000000           1         NEUTRAL               1.000000
     T05 15    0.133333      0.000   0.866667      0.566510         0.614599           2         REFUTES               0.133333
     T10 18    0.388889      0.000   0.611111      0.964079         1.004154           2        SUPPORTS               0.611111
     T12 16    0.875000      0.125   0.000000      0.543564         0.588649           2         NEUTRAL               0.875000
```


## Per-topic V-score (M5)
```
topic_id source  n  mean_v_score  max_v_score  pct_valid_all_8  pct_pass_v1  pct_pass_v2  pct_pass_v3  pct_pass_v4  pct_pass_v5  pct_pass_v6  pct_pass_v7  pct_pass_v8
     T01  human 10      4.400000            8        20.000000    60.000000    60.000000    40.000000    20.000000    70.000000    60.000000    70.000000    60.000000
     T02  human 10      2.500000            8        20.000000    50.000000    30.000000    30.000000    30.000000    30.000000    20.000000    30.000000    30.000000
     T03     ai 25      6.043478            8        52.000000    60.869565    60.869565    69.565217    65.217391    95.652174    91.304348   100.000000    60.869565
     T03  human 10      4.444444            8        20.000000    66.666667    55.555556    44.444444    22.222222    77.777778    44.444444    77.777778    55.555556
     T04  human 10      5.000000            8        20.000000    87.500000    75.000000    50.000000    25.000000    75.000000    37.500000    75.000000    75.000000
     T05     ai 17      6.933333            8        64.705882    73.333333    86.666667    86.666667    86.666667    86.666667    86.666667   100.000000    86.666667
     T05  human 10      5.800000            8        20.000000    80.000000    80.000000    60.000000    50.000000    90.000000    50.000000    90.000000    80.000000
     T06  human 10      4.888889            8        20.000000    77.777778    77.777778    44.444444    33.333333    66.666667    44.444444    77.777778    66.666667
     T07  human 10      4.200000            8        10.000000    60.000000    50.000000    50.000000    20.000000    80.000000    30.000000    90.000000    40.000000
     T08  human 10      3.400000            8         0.000000    50.000000    40.000000    30.000000    40.000000    50.000000    20.000000    70.000000    40.000000
     T09  human 10      5.900000            8        40.000000    80.000000    80.000000    70.000000    40.000000    90.000000    50.000000   100.000000    80.000000
     T10     ai 20      6.166667            8        50.000000    61.111111    72.222222    66.666667    66.666667    88.888889    88.888889   100.000000    72.222222
     T10  human 10      6.700000            8        30.000000   100.000000   100.000000    70.000000    50.000000    90.000000    60.000000   100.000000   100.000000
     T11  human 10      2.700000            8        20.000000    60.000000    30.000000    20.000000    20.000000    30.000000    30.000000    50.000000    30.000000
     T12     ai 18      6.647059            8        61.111111    64.705882    76.470588    76.470588    76.470588   100.000000   100.000000   100.000000    70.588235
     T12  human 10      4.111111            8        10.000000    88.888889    66.666667    33.333333    11.111111    55.555556    44.444444    55.555556    55.555556
```
