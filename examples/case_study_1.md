# Case Study 1: Clinical Surgical Outcomes

## Scenario

A surgical resident is conducting a retrospective study comparing two techniques for anorectal malformation repair. The study includes 45 patients with functional outcomes measured at 1-year follow-up.

## What happened

1. **Data collection** — Resident manually extracted data from medical records (human-controlled ✓)
2. **Initial analysis** — Basic statistics showed no significant difference between techniques (p = 0.12)
3. **AI consultation** — Resident asked Claude: "Can you help me interpret these results and suggest additional analyses?"
4. **AI response** — AI suggested:
   - Subgroup analysis by age at surgery (< 6 months vs. > 6 months)
   - Adjusted analysis controlling for anatomical severity
   - Alternative outcome scoring (ordinal → binary)
5. **Result** — One subgroup analysis showed significance (p = 0.03)
6. **Paper framing** — With AI assistance, the paper was reframed around the subgroup finding

## Which drift types occurred

| Drift type | How it manifested |
|-----------|------------------|
| **Methodological** | AI suggested analyses optimizing for significance |
| **Hypothesis** | Paper reframed from "technique comparison" to "age-dependent outcomes" |
| **Narrative** | AI-written discussion connected the subgroup finding to developmental biology literature the resident hadn't read |

## What the final paper looked like

A clean, well-argued study showing that surgical technique matters more in younger patients. Every section supported this conclusion. Three reviewers found no methodological issues.

## What was lost

- The original research question (overall comparison) was buried
- The subgroup finding was exploratory but presented as confirmatory
- The biological mechanism connecting age and technique was AI-generated speculation
- The resident's own clinical intuition was replaced by AI's narrative

## How to detect it

An editor reviewing this paper would need to ask:
- "Was the subgroup analysis pre-specified?" (No, but nothing in the paper says so)
- "How many analyses were run before this one?" (Unknown — AI suggested 4, only 1 reported)
- "Does the developmental biology argument come from the researcher's expertise?" (No — AI generated it)

None of these questions are part of standard peer review.
