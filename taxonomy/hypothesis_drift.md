# Type 2: Hypothesis Drift

## Definition

The boundary between pre-specified hypotheses and post-hoc rationalization dissolves when AI can generate both seamlessly and retroactively.

## Mechanism

1. Researcher begins with hypothesis A
2. During AI-assisted analysis, pattern B emerges
3. AI helps reframe the paper around B as if it were the original question
4. The final manuscript reads as confirmatory research
5. No pre-registration or audit trail would reveal the switch

## Why it's dangerous

Hypothesis drift is the AI-era version of HARKing (Hypothesizing After Results are Known), but harder to detect because:
- AI can produce a complete, coherent paper around *any* finding
- The transition from exploratory to confirmatory is invisible in the text
- The researcher may not even recognize the shift happened

## The seamlessness problem

In pre-AI research, HARKing required deliberate effort — the researcher had to consciously rewrite the introduction and reframe the study. This created psychological friction and left traces (awkward wording, forced logic).

With AI, reframing is effortless. Ask the model to "write an introduction for a study investigating B" and it produces a perfect one — complete with relevant literature, theoretical motivation, and a logical flow that makes B seem like the obvious question to ask.

## Detection signals

- Hypotheses that perfectly match the most interesting finding
- Introduction literature review that seems tailor-made for the results
- No mention of alternative hypotheses that were considered and rejected
- Pre-registration (if it exists) doesn't match the paper's framing

## Countermeasures

1. **Mandatory pre-registration with AI disclosure** — "Were hypotheses modified after AI-assisted analysis?"
2. **Version-controlled manuscripts** — Git-tracked writing showing how framing evolved
3. **Exploratory labeling** — If AI suggested the finding, label it exploratory regardless of how clean it looks
