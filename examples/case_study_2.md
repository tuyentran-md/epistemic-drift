# Case Study 2: AI-Assisted Systematic Review

## Scenario

A research team conducts a systematic review and network meta-analysis comparing treatments for a pediatric condition. They use AI tools for title/abstract screening, data extraction from PDFs, and manuscript writing.

## The pipeline

| Step | Method | Drift risk |
|------|--------|-----------|
| Search strategy | Human-designed, validated by librarian | Low ✓ |
| Title/abstract screening | AI-assisted batch screening | **Medium** |
| Full-text retrieval | Automated fetching | Low ✓ |
| Data extraction | AI reads PDFs → structured CSV | **High** |
| Statistical analysis | R scripts, human-specified models | Low ✓ |
| Results interpretation | AI-assisted writing | **High** |
| Discussion | AI-assisted framing | **Very high** |

## Where drift occurred

### Screening (Inference Drift)
AI screened 2,400 titles and excluded 1,800. Among exclusions, 12 papers were borderline — AI excluded them based on abstract wording, not methodology. Three of these papers contained relevant data that would have changed the pooled estimate.

**The problem:** The screening criteria were correct. The AI applied them correctly. But the AI's interpretation of "relevant" was subtly different from the researchers' intent, and no human verified the borderline cases.

### Data extraction (Inference Drift)
AI extracted outcomes from 35 PDFs. In 4 papers, outcomes were reported in supplementary tables with ambiguous column headers. AI made reasonable assumptions about which columns represented which outcomes — but these assumptions were wrong for 2 papers.

**The problem:** The extracted data looked clean. The CSV was well-structured. No one re-read the original papers to verify AI's interpretation of ambiguous tables.

### Discussion (Narrative Drift)
AI helped write the discussion, connecting the NMA results to treatment guidelines. The discussion argued that Treatment B should be preferred for younger patients — a nuanced clinical recommendation that emerged from the AI's synthesis, not from the researchers' clinical experience.

**The problem:** The recommendation was defensible given the data. But no clinician on the team had independently arrived at this conclusion. The AI's framing became the team's conclusion.

## What was preserved vs. lost

**Preserved:**
- Statistical integrity (R code is deterministic)
- Search comprehensiveness (human-designed strategy)
- PRISMA compliance (checklist followed)

**Lost:**
- Screening judgment (3 relevant papers missed)
- Data accuracy (2 extraction errors in ambiguous cases)
- Clinical reasoning (discussion framing outsourced to AI)

## Lessons

1. AI works well for structured, unambiguous tasks (search, statistics)
2. AI fails silently at judgment calls (borderline screening, ambiguous data)
3. The most dangerous drift happens in interpretation — where AI is most fluent and humans are most likely to defer
4. **Human checkpoints at every judgment step** are not optional safeguards; they are the difference between evidence synthesis and narrative generation
