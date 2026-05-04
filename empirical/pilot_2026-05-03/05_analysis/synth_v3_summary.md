# A.0 v3 — 3-Model Synthesis
_Generated: 2026-05-03 21:51_

## Top-line hypothesis outcomes
```
       model    scale  params_b  H1_entropy_mean_bits  H1_entropy_topics_above_0.3  H2_truth_div_mean_pct  H2_truth_div_topics_above_20  H4_pct_valid_all_8_mean  H4_topics_pct_valid_above_75
Gemini 3 Pro frontier    1500.0              0.214780                            3              28.055556                             4                87.222222                            11
  Gemma3 12B      mid      12.0              0.435371                            5              38.007663                             5                86.388889                            10
Llama 3.2 3B    small       3.0              0.681362                            8              31.130268                             6                25.000000                             0
```

## Truth divergence by truth direction
```
       model truth_direction  n_topics  mean_truth_div_pct  max_truth_div_pct  topics_above_20pct
Gemini 3 Pro        SUPPORTS         6            6.111111          36.666667                   1
Gemini 3 Pro         REFUTES         4           25.000000          83.333333                   1
Gemini 3 Pro         NEUTRAL         2          100.000000         100.000000                   2
  Gemma3 12B        SUPPORTS         6           14.348659          82.758621                   1
  Gemma3 12B         REFUTES         4           45.833333          83.333333                   2
  Gemma3 12B         NEUTRAL         2           93.333333         100.000000                   2
Llama 3.2 3B        SUPPORTS         6            9.482759          46.666667                   1
Llama 3.2 3B         REFUTES         4           33.333333          43.333333                   3
Llama 3.2 3B         NEUTRAL         2           91.666667          96.666667                   2
```

## Key findings
- **H1 entropy MONOTONE** with scale: Gemini 0.21 < Gemma 0.44 < Llama 0.68 bits.
- **H2 truth divergence NON-MONOTONE**: Gemini 28%, Gemma 38%, Llama 31%. Mid scale worst.
- **H4 mimicry THRESHOLD**: Gemini 87% ≈ Gemma 86% >> Llama 25%. Small collapses.
- **NEUTRAL truth = SUPPORTS bias**: every model shows ~100% drift on T11/T12 (NEUTRAL Cochrane truth).

## Per-topic detail (long form)
```
       model    scale topic_id truth_direction  n  p_supports  p_neutral  p_refutes  entropy_bits  truth_div_pct  mean_v_score  pct_valid_all_8
Gemini 3 Pro frontier      T01        SUPPORTS 30    1.000000   0.000000   0.000000     -0.000000       0.000000      7.800000        90.000000
Gemini 3 Pro frontier      T02        SUPPORTS 30    1.000000   0.000000   0.000000     -0.000000       0.000000      7.866667        93.333333
Gemini 3 Pro frontier      T03        SUPPORTS 30    1.000000   0.000000   0.000000     -0.000000       0.000000      7.933333        96.666667
Gemini 3 Pro frontier      T04        SUPPORTS 30    1.000000   0.000000   0.000000     -0.000000       0.000000      7.766667        86.666667
Gemini 3 Pro frontier      T05        SUPPORTS 30    0.633333   0.366667   0.000000      0.948078      36.666667      7.933333        96.666667
Gemini 3 Pro frontier      T06        SUPPORTS 30    1.000000   0.000000   0.000000     -0.000000       0.000000      8.000000       100.000000
Gemini 3 Pro frontier      T07         REFUTES 30    0.800000   0.033333   0.166667      0.851933      83.333333      8.000000       100.000000
Gemini 3 Pro frontier      T08         REFUTES 30    0.000000   0.033333   0.966667      0.210842       3.333333      7.966667        96.666667
Gemini 3 Pro frontier      T09         REFUTES 30    0.000000   0.000000   1.000000     -0.000000       0.000000      7.066667        10.000000
Gemini 3 Pro frontier      T10         REFUTES 30    0.133333   0.000000   0.866667      0.566510      13.333333      8.000000       100.000000
Gemini 3 Pro frontier      T11         NEUTRAL 30    1.000000   0.000000   0.000000     -0.000000     100.000000      7.633333        83.333333
Gemini 3 Pro frontier      T12         NEUTRAL 30    1.000000   0.000000   0.000000     -0.000000     100.000000      7.866667        93.333333
  Gemma3 12B      mid      T01        SUPPORTS 30    1.000000   0.000000   0.000000     -0.000000       0.000000      8.000000       100.000000
  Gemma3 12B      mid      T02        SUPPORTS 30    1.000000   0.000000   0.000000     -0.000000       0.000000      8.000000       100.000000
  Gemma3 12B      mid      T03        SUPPORTS 29    1.000000   0.000000   0.000000     -0.000000       0.000000      8.000000        96.666667
  Gemma3 12B      mid      T04        SUPPORTS 30    1.000000   0.000000   0.000000     -0.000000       0.000000      7.833333        83.333333
  Gemma3 12B      mid      T05        SUPPORTS 29    0.172414   0.413793   0.413793      1.490783      82.758621      7.965517        93.333333
  Gemma3 12B      mid      T06        SUPPORTS 30    0.966667   0.000000   0.033333      0.210842       3.333333      7.133333        20.000000
  Gemma3 12B      mid      T07         REFUTES 30    0.200000   0.633333   0.166667      1.312556      83.333333      8.000000       100.000000
  Gemma3 12B      mid      T08         REFUTES 30    0.000000   0.200000   0.800000      0.721928      20.000000      8.000000       100.000000
  Gemma3 12B      mid      T09         REFUTES 30    0.000000   0.000000   1.000000     -0.000000       0.000000      7.566667        56.666667
  Gemma3 12B      mid      T10         REFUTES 30    0.766667   0.033333   0.200000      0.921834      80.000000      7.933333        93.333333
  Gemma3 12B      mid      T11         NEUTRAL 30    1.000000   0.000000   0.000000     -0.000000     100.000000      7.966667        96.666667
  Gemma3 12B      mid      T12         NEUTRAL 30    0.866667   0.133333   0.000000      0.566510      86.666667      7.966667        96.666667
Llama 3.2 3B    small      T01        SUPPORTS 29    0.931034   0.034483   0.034483      0.431017       6.896552      6.034483        33.333333
Llama 3.2 3B    small      T02        SUPPORTS 30    1.000000   0.000000   0.000000     -0.000000       0.000000      5.900000        33.333333
Llama 3.2 3B    small      T03        SUPPORTS 30    1.000000   0.000000   0.000000     -0.000000       0.000000      5.066667         6.666667
Llama 3.2 3B    small      T04        SUPPORTS 30    0.966667   0.033333   0.000000      0.210842       3.333333      5.566667        20.000000
Llama 3.2 3B    small      T05        SUPPORTS 30    0.533333   0.200000   0.266667      1.456565      46.666667      6.433333        43.333333
Llama 3.2 3B    small      T06        SUPPORTS 30    1.000000   0.000000   0.000000     -0.000000       0.000000      5.400000        10.000000
Llama 3.2 3B    small      T07         REFUTES 30    0.233333   0.200000   0.566667      1.418620      43.333333      6.366667        36.666667
Llama 3.2 3B    small      T08         REFUTES 30    0.233333   0.166667   0.600000      1.362898      40.000000      6.066667        26.666667
Llama 3.2 3B    small      T09         REFUTES 30    0.266667   0.066667   0.666667      1.158939      33.333333      6.333333        30.000000
Llama 3.2 3B    small      T10         REFUTES 30    0.100000   0.066667   0.833333      0.811848      16.666667      6.100000        20.000000
Llama 3.2 3B    small      T11         NEUTRAL 30    0.800000   0.133333   0.066667      0.905587      86.666667      5.833333        30.000000
Llama 3.2 3B    small      T12         NEUTRAL 30    0.933333   0.033333   0.033333      0.420026      96.666667      5.666667        10.000000
```
