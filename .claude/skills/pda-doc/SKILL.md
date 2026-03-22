---
name: pda-doc
description: Generate pharma/GMP educational content for PDA_Technical-Report-Knowledge. Two modes — (1) Full Report mode for processing PDA technical reports from PDF, (2) Quick Analysis mode for pharma newsletter articles or news. Uses bilingual two-column layout with template.css.
allowed-tools: Bash(*), Read(*), Write(*), Edit(*), Glob(*), Grep(*), WebFetch(*)
argument-hint: "<article text, URL, or 'report TR##'>"
---

# PDA Doc Generator

## Repo Location
`~/PDA_Technical-Report-Knowledge/`

## Two Modes

### Mode 1: Quick Analysis (from digest/newsletter)

For pharma news articles from `/digest` export (Endpoints News, BioPharma Dive, PDA newsletters).

**Output:** Single standalone HTML in repo root or a dedicated `analysis/` folder.

**Steps:**
1. Read the article content (from digest export or URL via WebFetch)
2. Generate a bilingual analysis HTML using PDA template.css design system
3. Follow the two-column format:
   - **Left column:** Original content summary (English with key-term highlights)
   - **Right column:** Chinese commentary with required boxes:
     - `.concept-box` (green) — Key pharma/GMP concepts explained
     - `.analogy-box` (yellow) — Manufacturing analogies
     - `.note-box` (orange) — Regulatory/compliance implications
     - `.practice-box` (blue dashed) — Practice questions
4. Include PDA TR cross-references when relevant (cite TR# + Section X.X)
5. Update `index.html` if needed
6. Git commit (do NOT push)

**Template:**
```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>[Topic] — Pharma Analysis</title>
    <style>/* embed template.css */</style>
</head>
<body>
    <div class="header">
        <h1>[English Title]</h1>
        <div class="subtitle">[Chinese Title]</div>
        <div class="page-info">Source: [source] | Date: [date]</div>
    </div>
    <div class="learning-objectives">
        <h3>學習目標</h3>
        <ul>...</ul>
    </div>
    <div class="two-column">
        <div class="left-column">
            <h2>原文摘要 Original Summary</h2>
            <!-- English content with <span class="key-term"> -->
        </div>
        <div class="right-column">
            <h2>導師解析 Commentary</h2>
            <!-- concept-box, analogy-box, note-box, practice-box -->
        </div>
    </div>
    <div class="section-summary">
        <h3>重點回顧 Key Takeaways</h3>
        <ul>...</ul>
    </div>
</body>
</html>
```

### Mode 2: Full Report (from PDF)

For processing a complete PDA Technical Report into multi-section educational documents.

**Steps:**
1. Run `python3 ~/PDA_Technical-Report-Knowledge/new_report.py` to scaffold
2. Extract PDF text → `{REPORT}/source/`
3. Generate section HTMLs (each with full template.css embedded) → `{REPORT}/sections/`
4. Follow PROMPT.md rules strictly:
   - All explanatory text in Traditional Chinese (繁體中文)
   - Technical terms: English with Chinese in parentheses first occurrence
   - Per subsection minimum: 1x concept, 1x analogy, 1x note, 1x practice box
   - Base64 embedded figures when available
5. Edit SECTION_MAP in `{REPORT}/merge.py`
6. Run `python3 {REPORT}/merge.py` to merge into TopNav HTML
7. Update `index.html` document card, source colors, tag classes
8. Git commit (do NOT push)

**Split Strategy:**
- Sections >800 lines of source → split into a/b parts
- Both files in single SECTION_MAP entry

## Design System Reference

**CSS Variables:**
- `--primary-blue: #1e3a5f`
- `--accent-blue: #3498db`
- Fonts: Noto Sans TC + system fonts

**Commentary Box Types:**
| Box | Class | Color | Use |
|-----|-------|-------|-----|
| Key Concept | `.concept-box` | Green | Core pharma/GMP concepts |
| Analogy | `.analogy-box` | Yellow | Manufacturing analogies |
| Key Note | `.note-box` | Orange | Important warnings/compliance |
| Formula | `.formula-box` | Purple | Calculations/equations |
| Practice | `.practice-box` | Blue dashed | Questions for active recall |
| Application | `.practice-box` (green) | Green solid | Real-world applications |

**Standard Pharma Analogies:**
- Aseptic filling → preparing food in an operating room
- Terminal sterilization → reheating in microwave
- CIP/SIP → dishwasher + autoclave
- Isolator vs RABS → space station vs clean room
- PUPSIT → checking gas before leaving home

**PDA Citation Format:**
Every key point must cite PDA TR# + Section X.X:
- Format: **(PDA TR22, Section 3.2)** or **(TR22 §3.2)**
- Cross-reference other relevant TRs when topic spans multiple reports

## Content Guidelines

- Write as David explaining to a pharma manufacturing colleague
- Connect to CDMO operations context (aseptic fill-finish)
- Highlight GMP compliance implications
- Reference White Raven as competitive intelligence when relevant
- Use Traditional Chinese only — NEVER Simplified Chinese
