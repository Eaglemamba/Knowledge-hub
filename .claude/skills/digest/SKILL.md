---
name: digest
description: Combined daily digest — X/Twitter scraping + Gmail newsletters + one-click doc generation. Runs X scraper, then Gmail search, combines into interactive HTML with auto-routing to /hbr-single, /ai-doc, or pharma-decipher.
allowed-tools: Bash(*), Read(*), Write(*), Edit(*), Glob(*), Grep(*), mcp__claude_ai_Gmail__gmail_search_messages, mcp__claude_ai_Gmail__gmail_read_message, Agent(*)
---

# Combined Daily Digest Pipeline

## Overview

This skill combines **X/Twitter scraping** with the existing **Gmail newsletter digest** into a unified pipeline, with one-click educational document generation.

## Execution Steps

### Step 1: Run X Scraper

```bash
source ~/knowledge-hub/.venv/bin/activate && cd ~/knowledge-hub && python scripts/x_scraper.py scripts/x_latest.json
```

This scrapes 6 X accounts with the logged-in session:
- @karpathy (AI), @trq212 (AI), @bcherny (AI)
- @emollick (Leadership), @A_May_MD (Pharma), @HiTw93 (AI)

Output: `~/knowledge-hub/scripts/x_latest.json`

If session expired (error), tell user to re-login:
```bash
~/knowledge-hub/.venv/bin/python ~/knowledge-hub/scripts/x_login.py
```

### Step 2: Search Gmail Newsletters

Use the Gmail MCP tools. Search with `newer_than:2d`, then filter by strict 24-hour window in TST.

**Sources (10 confirmed):**

| Source | Gmail Query |
|--------|------------|
| Endpoints News | `from:endpointsnews.com newer_than:2d` |
| BioPharma Dive | `from:divenewsletter.com newer_than:2d` |
| HBR | `from:emails.hbr.org newer_than:2d` |
| Leadership in Change | `from:leadershipinchange10@substack.com newer_than:2d` |
| Department of Product | `from:departmentofproduct@substack.com newer_than:2d` |
| Ali Abdaal | `from:ali@aliabdaal.com newer_than:2d` |
| AI Maker | `from:aimaker@substack.com newer_than:2d` |
| Import AI | `from:importai@substack.com newer_than:2d` |
| The Batch | `from:deeplearning.ai newer_than:2d` |
| PDA | `from:pda.org newer_than:2d` |

For each email found:
1. Read the email content using `gmail_read_message`
2. Extract article titles, summaries, URLs
3. Convert timestamp to TST (UTC+8)
4. Include ONLY emails within strict 24-hour window

### Step 3: Combine & Generate HTML

Use `~/knowledge-hub/scripts/digest_pipeline.py` to generate combined HTML:

```python
# Pass both Gmail articles and X articles to generate_combined_html()
# Gmail articles format:
# {"source": "Endpoints News", "source_type": "email", "title": "...",
#  "content": "...", "timestamp_tst": "2026-03-22 08:30 TST",
#  "url": "https://...", "route": "pharma-decipher", "domain": "pharma"}
```

Output HTML to `~/knowledge-hub/scripts/digest_combined.html` and open it:
```bash
open ~/knowledge-hub/scripts/digest_combined.html
```

### Step 4: One-Click Doc Generation

After user exports selected articles from the HTML, process them by route:

**Route: `hbr-review`**
- Trigger `/hbr-single` skill for each selected article
- Target repo: `~/Harvard-Business-Review/`

**Route: `ai-articles`**
- Generate educational doc in david-ai-learning format
- Target repo: `~/AI articles/david-ai-learning/`
- Use the repo's existing `system_prompt.xml` if available, or generate a learning-focused article

**Route: `pharma-decipher`**
- Generate pharma analysis doc
- Target repo: `~/PDA_Technical-Report-Knowledge/` (if PDA-related) or general pharma analysis

For each generated doc:
1. Create the HTML/MD file in the target repo's docs/ folder
2. Update the repo's index file
3. Git add + commit (do NOT push unless user asks)

### Step 5: Update Knowledge-hub Index

After doc generation:
1. Update `~/knowledge-hub/indexes/` with new entries
2. If cross-domain insight found, create a cross-note in `~/knowledge-hub/cross-notes/`
3. Git add + commit knowledge-hub changes

## 24-Hour Rule

**CRITICAL: Never expand the 24-hour window.** Same rule as daily-news-digest v6.1.5:
- Use TST (UTC+8) for all time calculations
- If fewer than 5 articles, report "Light news day"
- Do NOT add older articles to fill the digest

## Source Status Icons

- ✔ Found within 24hr
- ⚠ Found but outside 24hr (show last date)
- ✗ No results

## Trigger Phrases

- "digest"
- "daily digest"
- "跑 digest"
- "morning briefing"
- "今天的新聞"
