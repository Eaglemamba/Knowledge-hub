---
repo: Harvard-Business-Review
last_updated: 2026-03-23
file_count: 11
---

# Harvard-Business-Review — Index

## Purpose
Curated HBR learning library with AI-powered educational document generation, bilingual content, and interactive dashboard filtering by month and topic tags.

## Key Files
| File | What It Contains |
|------|-----------------|
| docs/index.html | Interactive dashboard with 11 articles, filterable by month and tags |
| hbr-claude-code/system_prompt.xml | v1.6 AI Expert Learning System master prompt for doc generation |
| build_index.py | Auto-generates article list in index.html from doc meta tags |
| CLAUDE.md | Project rules: file naming, meta tags, workflow |
| .claude/commands/hbr-single.md | Single-article processor command |
| .claude/commands/hbr-batch.md | Batch processor command for multiple articles |

## Top 5 Insights
1. **Context Engineering as Competitive Advantage** (4.3/5) — Organizational context becomes the differentiator when all companies have the same AI models.
2. **AI Coordination Over Automation** (4.4/5) — AI's biggest ROI is reducing coordination costs, not labor automation.
3. **Gen AI Cannot Close the Expert Gap** (3.9/5) — AI narrows learning curve for novices but can't eliminate expert-novice gap.
4. **Two-Front Marketing Revolution** (4.1/5) — Conversational AI disrupts search; AI Agents become machine customers.
5. **Team Discipline Is Structural** (3.6/5) — Trust emerges from structural clarity, not motivation.

## Gaps / TODOs
- [ ] Scale to YYYY-MM/ subfolders when articles reach ~200
- [ ] Auto-tag detection for new tag categories
