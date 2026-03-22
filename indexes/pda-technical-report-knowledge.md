---
repo: PDA_Technical-Report-Knowledge
last_updated: 2026-03-23
file_count: 75
---

# PDA_Technical-Report-Knowledge — Index

## Purpose
Transform dense PDA technical pharmaceutical reports into bilingual (English + Traditional Chinese) interactive educational documents for CDMO professionals, with merged multi-section HTML and searchable dashboard.

## Key Files
| File | What It Contains |
|------|-----------------|
| index.html | Interactive dashboard: document cards, search, source filters, category bar |
| PROMPT.md | Master generation instructions for section HTMLs with bilingual layout |
| merge_engine.py | Shared library for merging section HTMLs into TopNav documents |
| template.css | Shared stylesheet (18KB): two-column layout, responsive, figure sizing |
| new_report.py | Scaffold script for new report folder structure |
| CLAUDE.md | Project rules: post-completion checklist, TopNav requirements, known pitfalls |

## Top 5 Insights
1. **Four completed reports, 54 sections:** Guide No.1 (20 sections), TR26 (11), PtC-14 (6), PtC-15 (3).
2. **Two-column bilingual design:** Left = English original, Right = Chinese commentary + learning objectives. Base64 images for offline portability.
3. **TopNav scroll architecture:** Horizontal scrolling nav with arrow buttons for large reports (>8 sections).
4. **32K token split strategy:** Long sections pre-split into A/B parts to avoid agent token exhaustion.
5. **Dashboard with source filtering:** Color-coded by report, dynamic stats computation from documents array.

## Gaps / TODOs
- [ ] Implement search-index.js for full-text indexing
- [ ] Extract and embed figures from source PDFs
- [ ] Automate PDF text extraction (currently manual)
- [ ] Add TR51 (Biological Indicators) — referenced by PtC-12 and Guide No.1
