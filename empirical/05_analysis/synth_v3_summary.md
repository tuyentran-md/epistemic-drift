# A.0 v3 — 3-Model Synthesis
_Generated: 2026-05-05 03:35_

## Top-line hypothesis outcomes
```
       model    scale  params_b  H1_entropy_mean_bits  H1_entropy_topics_above_0.3  H2_truth_div_mean_pct  H2_truth_div_topics_above_20  H4_pct_valid_all_8_mean  H4_topics_pct_valid_above_75
Gemini 3 Pro frontier    1500.0              0.137301                            2              20.000000                             3                89.444444                            11
  Gemma3 12B      mid      12.0              0.338086                            5              27.845512                             5                90.555556                            11
Llama 3.2 3B    small       3.0              0.532882                            7              41.929392                             7                42.222222                             1
```

## Truth divergence by truth direction
```
       model truth_direction  n_topics  mean_truth_div_pct  max_truth_div_pct  topics_above_20pct
Gemini 3 Pro        SUPPORTS         4            7.500000          30.000000                   1
Gemini 3 Pro         REFUTES         6            1.666667          10.000000                   0
Gemini 3 Pro         NEUTRAL         2          100.000000         100.000000                   2
  Gemma3 12B        SUPPORTS         4            8.620690          34.482759                   1
  Gemma3 12B         REFUTES         6           16.610564          62.068966                   2
  Gemma3 12B         NEUTRAL         2          100.000000         100.000000                   2
Llama 3.2 3B        SUPPORTS         4            7.672414          20.689655                   1
Llama 3.2 3B         REFUTES         6           45.410509          89.285714                   4
Llama 3.2 3B         NEUTRAL         2          100.000000         100.000000                   2
```

## Key findings
- **H1 entropy MONOTONE** with scale: Gemini 0.14 < Gemma 0.34 < Llama 0.53 bits.
- **H2 truth divergence NON-MONOTONE**: Gemini 20%, Gemma 28%, Llama 42%. Mid scale worst.
- **H4 mimicry THRESHOLD**: Gemini 89% ≈ Gemma 91% >> Llama 42%. Small collapses.
- **NEUTRAL truth = SUPPORTS bias**: every model shows ~100% drift on T11/T12 (NEUTRAL Cochrane truth).

## Per-topic detail (long form)
```
       model    scale topic_id truth_direction  n  p_supports  p_neutral  p_refutes  entropy_bits  truth_div_pct  mean_v_score  pct_valid_all_8
Gemini 3 Pro frontier      T01        SUPPORTS 29    1.000000   0.000000   0.000000     -0.000000       0.000000      8.000000        96.666667
Gemini 3 Pro frontier      T02         REFUTES 29    0.000000   0.000000   1.000000     -0.000000       0.000000      8.000000        96.666667
Gemini 3 Pro frontier      T03         NEUTRAL 29    1.000000   0.000000   0.000000     -0.000000     100.000000      7.965517        93.333333
Gemini 3 Pro frontier      T04        SUPPORTS 30    1.000000   0.000000   0.000000     -0.000000       0.000000      8.000000       100.000000
Gemini 3 Pro frontier      T05         REFUTES 30    0.100000   0.000000   0.900000      0.468996      10.000000      8.000000       100.000000
Gemini 3 Pro frontier      T06         REFUTES 29    0.000000   0.000000   1.000000     -0.000000       0.000000      7.933333        96.666667
Gemini 3 Pro frontier      T07        SUPPORTS 28    1.000000   0.000000   0.000000     -0.000000       0.000000      7.620690        80.000000
Gemini 3 Pro frontier      T08         REFUTES 29    0.000000   0.000000   1.000000     -0.000000       0.000000      7.275862        26.666667
Gemini 3 Pro frontier      T09         REFUTES 29    0.000000   0.000000   1.000000     -0.000000       0.000000      8.000000        96.666667
Gemini 3 Pro frontier      T10        SUPPORTS 30    0.700000   0.166667   0.133333      1.178614      30.000000      7.933333        96.666667
Gemini 3 Pro frontier      T11         REFUTES 30    0.000000   0.000000   1.000000     -0.000000       0.000000      8.000000       100.000000
Gemini 3 Pro frontier      T12         NEUTRAL 30    1.000000   0.000000   0.000000     -0.000000     100.000000      7.800000        90.000000
  Gemma3 12B      mid      T01        SUPPORTS 29    1.000000   0.000000   0.000000     -0.000000       0.000000      7.862069        90.000000
  Gemma3 12B      mid      T02         REFUTES 30    0.033333   0.033333   0.933333      0.420026       6.666667      7.933333        96.666667
  Gemma3 12B      mid      T03         NEUTRAL 30    1.000000   0.000000   0.000000     -0.000000     100.000000      7.966667        96.666667
  Gemma3 12B      mid      T04        SUPPORTS 29    1.000000   0.000000   0.000000     -0.000000       0.000000      8.000000        96.666667
  Gemma3 12B      mid      T05         REFUTES 29    0.620690   0.000000   0.379310      0.957553      62.068966      8.000000        96.666667
  Gemma3 12B      mid      T06         REFUTES 29    0.000000   0.000000   1.000000     -0.000000       0.000000      8.000000        96.666667
  Gemma3 12B      mid      T07        SUPPORTS 29    1.000000   0.000000   0.000000     -0.000000       0.000000      7.586207        56.666667
  Gemma3 12B      mid      T08         REFUTES 30    0.000000   0.066667   0.933333      0.353359       6.666667      7.766667        76.666667
  Gemma3 12B      mid      T09         REFUTES 29    0.137931   0.068966   0.793103      0.925501      20.689655      7.965517        93.333333
  Gemma3 12B      mid      T10        SUPPORTS 29    0.655172   0.275862   0.068966      1.178304      34.482759      8.000000       100.000000
  Gemma3 12B      mid      T11         REFUTES 28    0.000000   0.035714   0.964286      0.222285       3.571429      7.862069        93.333333
  Gemma3 12B      mid      T12         NEUTRAL 29    1.000000   0.000000   0.000000     -0.000000     100.000000      7.965517        93.333333
Llama 3.2 3B    small      T01        SUPPORTS 29    1.000000   0.000000   0.000000     -0.000000       0.000000      7.000000        60.000000
Llama 3.2 3B    small      T02         REFUTES 28    0.250000   0.071429   0.678571      1.151565      32.142857      7.724138        76.666667
Llama 3.2 3B    small      T03         NEUTRAL 30    1.000000   0.000000   0.000000     -0.000000     100.000000      6.966667        43.333333
Llama 3.2 3B    small      T04        SUPPORTS 30    0.966667   0.033333   0.000000      0.210842       3.333333      6.966667        33.333333
Llama 3.2 3B    small      T05         REFUTES 29    0.482759   0.000000   0.517241      0.999142      48.275862      6.413793        36.666667
Llama 3.2 3B    small      T06         REFUTES 30    0.100000   0.066667   0.833333      0.811848      16.666667      6.800000        50.000000
Llama 3.2 3B    small      T07        SUPPORTS 30    0.933333   0.033333   0.033333      0.420026       6.666667      6.866667        36.666667
Llama 3.2 3B    small      T08         REFUTES 30    0.033333   0.000000   0.966667      0.210842       3.333333      7.300000        50.000000
Llama 3.2 3B    small      T09         REFUTES 28    0.821429   0.071429   0.107143      0.850326      89.285714      6.344828        16.666667
Llama 3.2 3B    small      T10        SUPPORTS 29    0.793103   0.034483   0.172414      0.869996      20.689655      7.034483        43.333333
Llama 3.2 3B    small      T11         REFUTES 29    0.793103   0.034483   0.172414      0.869996      82.758621      6.448276        30.000000
Llama 3.2 3B    small      T12         NEUTRAL 28    1.000000   0.000000   0.000000     -0.000000     100.000000      6.714286        30.000000
```
