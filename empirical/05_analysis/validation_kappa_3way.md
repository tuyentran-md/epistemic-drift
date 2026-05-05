# Three-rater agreement (sếp, Zi, AI rater)
_Generated: 2026-05-05 20:45_
_n abstracts: 29_

## Direction (3-class)
- **Sếp vs Zi (human-human):** κ = 0.802 (almost perfect (0.81–1.00)), accuracy = 89.7%
- **Sếp vs AI:** κ = 0.795 (substantial (0.61–0.80)), accuracy = 89.7%
- **Zi vs AI:** κ = 0.859 (almost perfect (0.81–1.00)), accuracy = 93.1%

## Direction κ by AI rater subset
- **anthropic/claude-sonnet-4.5** (n=16): sếp-AI κ = 0.758, Zi-AI κ = 1.000
- **deepseek/deepseek-chat-v3.1** (n=13): sếp-AI κ = 0.843, Zi-AI κ = 0.698

## V1-V8 binary item agreement
| Item | sếp-Zi | sếp-AI | Zi-AI |
|---|---|---|---|
| V1 | 0.000 | 0.256 | 0.000 |
| V2 | 0.000 | 0.000 | nan |
| V3 | -0.055 | -0.055 | 1.000 |
| V4 | 0.241 | 0.613 | -0.055 |
| V5 | 0.293 | -0.109 | -0.048 |
| V6 | 0.000 | 0.000 | nan |
| V7 | 0.000 | 0.098 | 0.000 |
| V8 | 0.096 | 0.281 | -0.055 |

Mean pass rate per V-item:
- sếp: ['0.90', '0.97', '0.90', '0.79', '0.83', '0.90', '0.79', '0.59']
- Zi: ['1.00', '1.00', '0.97', '0.97', '0.97', '1.00', '1.00', '0.97']
- AI: ['0.90', '1.00', '0.97', '0.90', '0.93', '1.00', '0.90', '0.90']

## V-score sum (0-8) per rater
- sếp mean = 6.66, sd = 1.88
- Zi mean = 7.86, sd = 0.58
- AI mean = 7.48, sd = 1.02
- Pearson r (sếp, Zi) = 0.512
- Pearson r (sếp, AI) = 0.518
- Pearson r (Zi, AI)  = 0.056

## Confusion matrix — Sếp vs AI (rows=sếp, cols=AI)
```
direction_ai     REFUTES  SUPPORTS  All
direction_human                        
NEUTRAL                2         0    2
REFUTES                9         1   10
SUPPORTS               0        17   17
All                   11        18   29
```

## Decision per OSF X4RP5 §4 H5
- Threshold: human-AI κ ≥ 0.7 (substantial)
- **Sếp-AI κ = 0.795** → PASS ✅
- Zi-AI κ = 0.859 (cross-check)

Notes: AI rater is mixed DeepSeek V3.1 + Claude Sonnet 4.5 (50/50 deterministic split). Per-rater κ shown above. Per OSF prereg, both LLM rater subsets must reach κ ≥ 0.7 for full H5 confirmation.