---
name: ai-doc
description: Generate an educational HTML document for david-ai-learning from a newsletter article, X thread, or any AI-related content. Uses system_prompt.xml v1.5.0 design system. Creates bilingual (zh-TW) HTML with meta tags, then runs the update-docs pipeline.
allowed-tools: Bash(*), Read(*), Write(*), Edit(*), Glob(*), Grep(*), WebFetch(*)
argument-hint: "<article title or URL>"
---

# AI Doc Generator for david-ai-learning

## Design System Reference

Follow the design system defined in `~/knowledge-hub/system_prompt.xml` (v1.5.0). Key specs:

### Page Layout (v1.4.3 mandatory)
- **Container:** max-width 1100px, centered
- **Header:** full viewport width, gradient `#1e3a5f → #3b5998 → #5b7fb5`
- **Fonts:** Noto Sans TC + Source Code Pro (Google Fonts)
- **Content grid:** two-column (`1fr 1fr`), collapses to single on mobile

### Required Sections (in order)
1. **dashboard_meta** — HTML meta tags (doc-date, doc-title, doc-source, doc-tags, doc-rating, doc-summary, doc-file)
2. **header** — tags, title, subtitle, source link (centered)
3. **executive_summary** — quick summary + rating bar
4. **learning_objectives** — 3-column grid with hover effect
5. **framework_visual** — (conditional) if article has 3+ step framework
6. **content_sections** — content-grid blocks (left: bilingual original, right: commentary boxes)
7. **key_takeaways** — 4 cards with hover, 2x2 grid
8. **practice** — 2-3 questions, accordion/collapsible, answers hidden by default
9. **bottom_line** — 我的行動結論 (核心洞察 / 立即應用 / 需要補充)
10. **footer** — date, source link, suggested filename

### Rating Bar
```html
<div class="rating-bar">
    <span class="rating-score"><span class="rating-stars">★★★★☆</span> X.X/5</span>
    <span class="rating-high">↑ High1, High2</span>
    <span class="rating-low">↓ Low1, Low2</span>
</div>
```

### Bilingual Content (left column)
```html
<div class="bilingual-block">
    <p class="zh">中文翻譯，含 <span class="highlight">重點標記</span></p>
    <p class="en">"Original English quote in gray italic"</p>
</div>
```

### Commentary Boxes (right column)
- `box-concept` (📚 green) — core concepts
- `box-analogy` (💡 yellow) — analogies
- `box-key` (⚠️ orange) — key insights
- `box-practical` (🛠️ teal) — practical applications

### Content Guidelines
- Write as if David is explaining to a pharma operations colleague new to AI
- Use real-life analogies from manufacturing/pharma when possible
- Highlight what's actionable for a CDMO operations director
- Connect to David's context: COO track, aseptic fill-finish, White Raven competitor
- Practice questions: 概念理解, 產業應用, 批判思考 types
- Bottom line: first person (我), specific weekly action items

### Standard Tags
`Agent`, `Tool`, `LLM`, `Prompt`, `Framework`, `Analysis`, `Automation`, `Security`, `Content`, `API`, `Research`

For Anthropic sources only: `Anthropic-Docs`, `Anthropic-Eng` (as first tag)

### Rating Guide (5 dimensions)
- Technical Depth, Practical Value, Tool Ecosystem, Timeliness, Learning Curve
- Rating bar shows overall score + top 2 high + top 2 low dimensions

## Execution Steps

### Step 1: Fetch content (if URL)
Use WebFetch if user provides a URL.

### Step 2: Generate HTML
Create at `~/AI articles/david-ai-learning/docs/YYYY-MM-DD_slug.html`
- Filename: `YYYY-MM-DD_slug.html` (lowercase, hyphens, no spaces)
- Use today's date
- Follow all v1.5.0 design specs above

### Step 3: Run update-docs pipeline
```bash
cd ~/AI\ articles/david-ai-learning
node build-search-index.js
node build-dashboard-data.js
```

### Step 4: Commit (do NOT push)
```bash
git add docs/YYYY-MM-DD_slug.html dashboard-data.js search-index.js
git commit -m "Add: YYYY-MM-DD_slug (date)"
```

### Step 5: Summary table
| Field | Value |
|-------|-------|
| File | filename |
| Title | Chinese title |
| Tags | tags |
| Rating | X.X/5 |
