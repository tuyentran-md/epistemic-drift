# Epistemic Drift

**When AI assists scientific research, it doesn't just speed things up — it silently changes the reasoning chain itself.**

This repository contains:

1. **Theoretical framework** (this README + `taxonomy/` + `examples/`) — companion to the submitted paper:
   > Tran T. *"Artificial Intelligence and the Epistemic Drift of Scientific Research."* (Under review at *Accountability in Research*)

2. **Empirical study** ([`empirical/`](empirical/)) — preregistered evaluation of LLM drift on Cochrane-anchored medical abstracts:
   > Tran T. *"Structural validity and truth-direction fidelity of LLM-generated medical abstracts across model scales: a preregistered evaluation."* (Data collection in progress)
   > **OSF preregistration:** [https://doi.org/10.17605/OSF.IO/X4RP5](https://doi.org/10.17605/OSF.IO/X4RP5)

---

## What is Epistemic Drift?

Epistemic drift is a new class of epistemic failure introduced when AI (particularly LLMs) participates in the scientific reasoning process.

It is **not**:
- ❌ Data fabrication
- ❌ Traditional bias
- ❌ Statistical error
- ❌ Plagiarism

It **is**:
- An uncontrolled divergence between data and inference
- A blurring of hypothesis and post-hoc rationalization
- A silent shift from method-driven to narrative-driven conclusions

**The critical problem:** Epistemic drift leaves no visible trace in the final output. The paper looks fine. The statistics check out. The logic reads smoothly. But the reasoning chain that produced it was never under human control.

---

## Why Existing Safeguards Fail

| Safeguard | What it checks | Why it misses drift |
|-----------|---------------|-------------------|
| **Peer review** | Final manuscript quality | Post-hoc — reviews output, not process |
| **Reproducibility** | Can results be replicated? | Checks results, not reasoning |
| **Disclosure** | "AI was used for..." | Ethical statement, not logical enforcement |
| **Model alignment** | Is the AI helpful/harmless? | Alignment ≠ epistemic integrity |

All existing safeguards share one assumption: **if the output looks reasonable, the process was sound.** AI breaks this assumption structurally.

---

## Taxonomy of Epistemic Drift

### Type 1: Inference Drift
AI generates conclusions that are *statistically plausible* but were never derived from the actual data through a controlled reasoning process.

**Example:** Researcher uploads raw data → asks AI to "interpret the results" → AI produces a coherent narrative that fits the numbers but introduces causal claims the study design cannot support.

### Type 2: Hypothesis Drift
The boundary between pre-specified hypotheses and post-hoc rationalization dissolves when AI can generate both seamlessly.

**Example:** Researcher starts with hypothesis A → AI-assisted analysis reveals pattern B → AI helps reframe the paper around B as if it were the original hypothesis. The final paper reads as confirmatory research, but no pre-registration would match it.

### Type 3: Narrative Drift
AI constructs a compelling story that connects findings in ways the researcher did not originally conceive, and the researcher adopts this narrative without recognizing it as AI-generated framing.

**Example:** Discussion section written with AI assistance weaves together citations and implications that create a "too-clean" narrative — every finding supports the conclusion, every limitation is elegantly addressed. Real research is messier.

### Type 4: Methodological Drift
AI suggests or modifies analytical approaches in ways that optimize for "interesting results" rather than methodological rigor.

**Example:** AI recommends subgroup analyses, alternative statistical tests, or variable transformations that happen to produce significant results — a form of automated p-hacking that the researcher may not recognize as such.

---

## The Structural Problem

```
Traditional research:
  Human hypothesis → Human method → Data → Human interpretation → Paper
  (Each step: human-controlled, human-accountable)

AI-assisted research:
  Human hypothesis → AI-suggested method → Data → AI interpretation → AI-polished paper
  (Steps 2-5: reasoning chain partially or fully outsourced)

The question is not whether AI makes errors.
The question is whether anyone can tell where human reasoning ends
and AI reasoning begins in the final output.
```

---

## Implications

If epistemic drift is not addressed:

1. **"Evidence-based" becomes "narrative-consistent"** — Science optimizes for coherent stories rather than rigorous inference
2. **Better models ≠ more trustworthy science** — As AI improves, drift becomes harder to detect, not easier
3. **The crisis is epistemic, not statistical** — We don't need better p-values; we need to know who (or what) is doing the thinking

---

## What This Repository Contains

```
epistemic-drift/
├── README.md                 # This document — taxonomy and framework
├── taxonomy/
│   ├── inference_drift.md    # Detailed analysis + real-world patterns
│   ├── hypothesis_drift.md
│   ├── narrative_drift.md
│   └── methodological_drift.md
├── examples/
│   ├── case_study_1.md       # Clinical research scenario
│   └── case_study_2.md       # Systematic review scenario
├── empirical/                # Preregistered empirical study (OSF X4RP5)
│   ├── README.md             # Run instructions, layout, hypotheses
│   ├── 01_topics/            # 12 Cochrane-anchored topics
│   ├── 02_generation/        # Generation pipeline + 4 frozen prompts
│   ├── 04_metrics/           # Rating + dispersion + entropy
│   ├── 05_analysis/          # Confirmatory + exploratory analyses
│   ├── helpers/              # Validation, retest, audits
│   └── pilot_2026-05-03/     # Pilot data (NOT used in confirmatory analysis)
└── CITATION.cff              # How to cite this work
```

---

## Related Work

This concept builds on and extends:

- Ioannidis, J.P.A. (2005). "Why Most Published Research Findings Are False"
- Romero, F. (2020). "The Epistemic Risks of AI-Assisted Science"
- Naddaf, M. (2025). "AI is Turning Research into a Scientific Monoculture"

---

## How to Cite

If you reference epistemic drift in your work:

```bibtex
@misc{tran2026epistemic,
  author = {Tran, Tuyen},
  title = {Epistemic Drift: A Taxonomy of AI-Induced Failures in Scientific Reasoning},
  year = {2026},
  publisher = {GitHub},
  url = {https://github.com/tuyentran-md/epistemic-drift}
}
```

---

## Contributing

This is an evolving framework. If you've observed epistemic drift patterns in your field, contributions are welcome:

1. **Report a pattern** — Open an issue describing the drift type, field, and example
2. **Add a case study** — Submit a PR to `examples/`
3. **Extend the taxonomy** — Propose new drift types with evidence

---

## License

CC BY 4.0 — Use freely with attribution.

---

*"The crisis is not that AI makes bad science — it's that AI makes science that looks indistinguishable from good science."*
