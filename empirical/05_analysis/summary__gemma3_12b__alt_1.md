# Confirmatory Analysis — gemma3:12b__alt_1

_Generated: 2026-05-05 03:19_


Bonferroni α = 0.0125 across H1-H4 family.


## Confirmatory results (H1–H4)

### H1 — entropy > 0.3 bits — ❌ does not pass Bonferroni

- **metric:** Per-topic entropy (Miller-Madow corrected)
- **n_topics:** 4
- **mean:** 0.6499690846617987
- **ci_95:** (0.11744360883334075, 1.1824945604902566)
- **t_stat:** 1.1005780225993977
- **p_one_tailed:** 0.17573374962809393
- **passes_bonferroni:** False
- **primary_threshold:** 0.3
- **sensitivity:**
  - thresh_0.2: {'mean_above': 1.0, 'topics_above': 3}
  - thresh_0.3: {'mean_above': 1.0, 'topics_above': 2}
  - thresh_0.4: {'mean_above': 1.0, 'topics_above': 2}

### H2 — truth divergence > 20% — ❌ does not pass Bonferroni

- **metric:** Per-topic divergence rate
- **n_topics:** 4
- **mean:** 0.4839285714285714
- **ci_95:** (0.1589285714285714, 0.8416666666666667)
- **t_stat:** 1.4111458492622988
- **p_one_tailed:** 0.1265143698339116
- **passes_bonferroni:** False
- **primary_threshold:** 0.2
- **sensitivity:**
  - thresh_0.1: {'mean_above': 1.0, 'topics_above': 3}
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
- **mean_ratio:** 0.737254641369056

### H4 — V-score < 6.0 — ❌ does not pass Bonferroni

- **metric:** Per-topic mean V-score (0-8 continuous)
- **n_topics:** 4
- **mean:** 7.751806239737275
- **ci_95:** (7.66547619047619, 7.873275862068965)
- **t_stat:** 27.986302457179388
- **p_one_tailed:** 0.9999499260773872
- **passes_bonferroni:** False
- **primary_threshold:** 6.0
- **sensitivity:**
  - thresh_5.0: {'mean_below': 0.0, 'topics_below': 0}
  - thresh_6.0: {'mean_below': 0.0, 'topics_below': 0}
  - thresh_7.0: {'mean_below': 0.0, 'topics_below': 0}


## H6 — Truth-direction asymmetry (descriptive)

- **NEUTRAL** (n=2): mean div = 0.768, 95%CI (0.5357142857142857, 1.0), max 1.000
- **REFUTES** (n=1): mean div = 0.033, 95%CI (None, None), max 0.033
- **SUPPORTS** (n=1): mean div = 0.367, 95%CI (None, None), max 0.367


## Drop-rate audit (≥5% threshold)

- T12: 28/30 valid (drop rate 6.7%) — FLAGGED


## Per-topic entropy + truth-divergence (M1, M4)
```
topic_id  n  p_supports  p_neutral  p_refutes  entropy_bits  entropy_bits_mm  k_observed truth_direction  truth_divergence_rate
     T03 29    1.000000   0.000000   0.000000     -0.000000         0.000000           1         NEUTRAL               1.000000
     T05 30    0.033333   0.000000   0.966667      0.210842         0.234887           2         REFUTES               0.033333
     T10 30    0.633333   0.233333   0.133333      1.294820         1.342910           3        SUPPORTS               0.366667
     T12 28    0.535714   0.464286   0.000000      0.996317         1.022079           2         NEUTRAL               0.535714
```


## Per-topic V-score (M5)
```
topic_id source  n  mean_v_score  max_v_score  pct_valid_all_8  pct_pass_v1  pct_pass_v2  pct_pass_v3  pct_pass_v4  pct_pass_v5  pct_pass_v6  pct_pass_v7  pct_pass_v8
     T01  human 10      4.000000            8        20.000000    55.555556    55.555556    33.333333    22.222222    66.666667    44.444444    66.666667    55.555556
     T02  human 10      2.600000            8        20.000000    50.000000    30.000000    30.000000    30.000000    30.000000    20.000000    40.000000    30.000000
     T03     ai 30      7.931034            8        90.000000   100.000000   100.000000   100.000000    93.103448   100.000000   100.000000   100.000000   100.000000
     T03  human 10      4.600000            8        20.000000    70.000000    60.000000    30.000000    30.000000    90.000000    40.000000    80.000000    60.000000
     T04  human 10      4.300000            8        10.000000    70.000000    70.000000    50.000000    20.000000    60.000000    40.000000    60.000000    60.000000
     T05     ai 30      7.700000            8        83.333333   100.000000   100.000000    93.103448    96.551724    96.551724   100.000000   100.000000   100.000000
     T05  human 10      5.800000            8        30.000000    90.000000    80.000000    60.000000    50.000000    80.000000    50.000000    90.000000    80.000000
     T06  human 10      4.900000            8        20.000000    80.000000    70.000000    50.000000    40.000000    70.000000    40.000000    80.000000    60.000000
     T07  human 10      4.444444            8        10.000000    77.777778    66.666667    44.444444    22.222222    66.666667    22.222222    77.777778    66.666667
     T08  human 10      3.500000            8         0.000000    50.000000    50.000000    40.000000    40.000000    50.000000    20.000000    60.000000    40.000000
     T09  human 10      5.700000            8        30.000000    80.000000    80.000000    60.000000    40.000000    90.000000    50.000000    90.000000    80.000000
     T10     ai 30      7.733333            8        86.666667   100.000000   100.000000    86.666667    90.000000   100.000000   100.000000   100.000000    96.666667
     T10  human 10      6.333333            8        10.000000   100.000000    88.888889    77.777778    33.333333    88.888889    55.555556   100.000000    88.888889
     T11  human 10      2.777778            8        10.000000    55.555556    44.444444    22.222222    22.222222    22.222222    33.333333    44.444444    33.333333
     T12     ai 30      7.642857            8        66.666667   100.000000   100.000000    85.714286    92.857143   100.000000    85.714286   100.000000   100.000000
     T12  human 10      3.300000            8        10.000000    70.000000    50.000000    30.000000    10.000000    40.000000    30.000000    60.000000    40.000000
```
