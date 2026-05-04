# Confirmatory Analysis — llama3.2:3b__alt_2

_Generated: 2026-05-05 03:19_


Bonferroni α = 0.0125 across H1-H4 family.


## Confirmatory results (H1–H4)

### H1 — entropy > 0.3 bits — ❌ does not pass Bonferroni

- **metric:** Per-topic entropy (Miller-Madow corrected)
- **n_topics:** 4
- **mean:** 1.0232711137048194
- **ci_95:** (0.6024083014590857, 1.444133925950553)
- **t_stat:** 2.7603311328121105
- **p_one_tailed:** 0.03506644441205366
- **passes_bonferroni:** False
- **primary_threshold:** 0.3
- **sensitivity:**
  - thresh_0.2: {'mean_above': 1.0, 'topics_above': 4}
  - thresh_0.3: {'mean_above': 1.0, 'topics_above': 4}
  - thresh_0.4: {'mean_above': 1.0, 'topics_above': 3}

### H2 — truth divergence > 20% — ✅ passes Bonferroni

- **metric:** Per-topic divergence rate
- **n_topics:** 4
- **mean:** 0.699671592775041
- **ci_95:** (0.5278735632183909, 0.8602216748768474)
- **t_stat:** 4.954301533904649
- **p_one_tailed:** 0.007892226257465744
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
- **mean_ratio:** 0.7839802447533967

### H4 — V-score < 6.0 — ✅ passes Bonferroni

- **metric:** Per-topic mean V-score (0-8 continuous)
- **n_topics:** 4
- **mean:** 2.6715311986863712
- **ci_95:** (2.033333333333333, 3.4815476190476193)
- **t_stat:** -7.312704276625329
- **p_one_tailed:** 0.002640681970578164
- **passes_bonferroni:** True
- **primary_threshold:** 6.0
- **sensitivity:**
  - thresh_5.0: {'mean_below': 1.0, 'topics_below': 4}
  - thresh_6.0: {'mean_below': 1.0, 'topics_below': 4}
  - thresh_7.0: {'mean_below': 1.0, 'topics_below': 4}


## H6 — Truth-direction asymmetry (descriptive)

- **NEUTRAL** (n=2): mean div = 0.848, 95%CI (0.7666666666666666, 0.9285714285714286), max 0.929
- **REFUTES** (n=1): mean div = 0.448, 95%CI (None, None), max 0.448
- **SUPPORTS** (n=1): mean div = 0.655, 95%CI (None, None), max 0.655


## Drop-rate audit (≥5% threshold)

- T12: 28/30 valid (drop rate 6.7%) — FLAGGED


## Per-topic entropy + truth-divergence (M1, M4)
```
topic_id  n  p_supports  p_neutral  p_refutes  entropy_bits  entropy_bits_mm  k_observed truth_direction  truth_divergence_rate
     T03 30    0.766667   0.233333   0.000000      0.783777         0.807822           2         NEUTRAL               0.766667
     T05 29    0.379310   0.068966   0.551724      1.269921         1.319669           3         REFUTES               0.448276
     T10 29    0.344828   0.206897   0.448276      1.518851         1.568599           3        SUPPORTS               0.655172
     T12 28    0.928571   0.071429   0.000000      0.371232         0.396995           2         NEUTRAL               0.928571
```


## Per-topic V-score (M5)
```
topic_id source  n  mean_v_score  max_v_score  pct_valid_all_8  pct_pass_v1  pct_pass_v2  pct_pass_v3  pct_pass_v4  pct_pass_v5  pct_pass_v6  pct_pass_v7  pct_pass_v8
     T01  human 10      4.100000            8        20.000000    60.000000    60.000000    40.000000    20.000000    60.000000    40.000000    70.000000    60.000000
     T02  human 10      3.000000            8        20.000000    50.000000    40.000000    30.000000    30.000000    40.000000    20.000000    50.000000    40.000000
     T03     ai 30      2.033333            8         0.000000    13.333333    13.333333     0.000000     0.000000    46.666667    33.333333    86.666667    10.000000
     T03  human 10      4.700000            8        20.000000    70.000000    60.000000    40.000000    30.000000    90.000000    40.000000    80.000000    60.000000
     T04  human 10      4.500000            8        30.000000    80.000000    70.000000    40.000000    30.000000    70.000000    40.000000    70.000000    50.000000
     T05     ai 30      2.033333            8         6.666667    10.344828    10.344828     6.666667     6.666667    40.000000    20.000000   100.000000    10.000000
     T05  human 10      5.900000            8        30.000000    90.000000    80.000000    60.000000    50.000000    80.000000    50.000000   100.000000    80.000000
     T06  human 10      5.100000            8        20.000000    80.000000    70.000000    40.000000    50.000000    70.000000    50.000000    80.000000    70.000000
     T07  human 10      4.000000            8        10.000000    55.555556    55.555556    33.333333    22.222222    88.888889    22.222222    77.777778    44.444444
     T08  human 10      4.200000            8        10.000000    60.000000    60.000000    40.000000    40.000000    70.000000    20.000000    80.000000    50.000000
     T09  human 10      5.777778            8        30.000000    77.777778    77.777778    77.777778    33.333333    88.888889    55.555556    88.888889    77.777778
     T10     ai 30      2.655172            8         0.000000    20.689655    17.241379     3.448276     0.000000    65.517241    51.724138    93.103448    13.793103
     T10  human 10      6.111111            8        10.000000   100.000000   100.000000    44.444444    22.222222    88.888889    55.555556   100.000000   100.000000
     T11  human 10      2.555556            8        10.000000    55.555556    44.444444    22.222222    11.111111    33.333333    33.333333    33.333333    22.222222
     T12     ai 30      3.964286            8         0.000000    64.285714    60.714286     7.142857     0.000000    89.285714    28.571429    96.428571    50.000000
     T12  human 10      3.400000            8        20.000000    70.000000    50.000000    30.000000    20.000000    50.000000    40.000000    40.000000    40.000000
```
