---
repo: david-ai-learning
last_updated: 2026-03-23
file_count: 131
---

# david-ai-learning — Index

## Purpose
Bilingual (Traditional Chinese + English) AI learning hub with 131 interactive HTML documents covering prompt engineering, Claude tools, AI agents, and AI-pharma industry intersections.

## Key Files
| File | What It Contains |
|------|-----------------|
| index.html | Interactive dashboard with full-text search across 770+ section-level entries |
| curriculum-data.js | Single source of truth for 5-stage learning path + 11 topic clusters |
| add-doc.js | Smart document insertion with ML classification; updates curriculum-data.js automatically |
| dashboard-data.js | Generated metadata array for all 131 docs; rebuilt via build-dashboard-data.js |
| search-index.js | Full-text search index (981K, auto-generated); never read directly |
| CLAUDE.md | Project rules including document revision chain |
| insight.md | Session-based knowledge architecture lessons |

## Top 5 Insights
1. **Three-Layer Knowledge Architecture** — Mind Map (navigation) → MD essence/cheatsheet (quick read) → HTML full-text (deep read). Each layer solves different reading needs.
2. **Document Revision Chain is Mandatory** — Adding/modifying a doc requires updating: curriculum-data.js → rebuild search-index.js → rebuild dashboard-data.js.
3. **GitHub Pages Single Entry Pattern** — index.html is dashboard entry; all docs accessible via direct URL.
4. **Recent Strategic Pivot** — Latest docs focus on Claude Code mastery + pharma-AI intersections (Roche-NVIDIA, SOP RAG).
5. **5-Stage Learning Path** — AI Basics → Prompt Engineering → AI Tools → Agent Architecture → Organization.

## Gaps / TODOs
- [ ] Restructure docs/ into YYYY-MM/ subfolders when count exceeds ~200
- [ ] Validate auto-classification accuracy across all 131 docs
