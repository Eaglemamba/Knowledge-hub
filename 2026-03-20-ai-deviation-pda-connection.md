---
date: 2026-03-20
tags: [ai, pharma, deviation, automation]
repos: [david-ai-system, Amaran-AI-SOP, PDA_Technical-Report-Knowledge]
---

# AI-Driven Deviation Report Writing Meets PDA Best Practices

## Insight
Claude can draft GMP deviation reports following PDA TR frameworks (e.g., TR-60 for process validation, TR-13 for fundamentals of aseptic processing), but the quality depends on having both the AI system prompts (in david-ai-system) AND the PDA technical knowledge (in PDA_Technical-Report-Knowledge) available simultaneously. Neither repo alone is sufficient.

## Source Repos
- `david-ai-system`: Claude skills for deviation report generation
- `Amaran-AI-SOP`: Actual SOP templates and deviation workflows
- `PDA_Technical-Report-Knowledge`: Regulatory basis and technical rationale

## So What?
When building the GMP automation system, the CC session needs to reference all three repos — not just the coding one.
