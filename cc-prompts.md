# Knowledge Hub — Claude Code Prompt Templates

## 1. Generate New Repo Summary (First Time)

Use this when adding a repo to knowledge-hub for the first time.

```
Read all files in this repo. Then create a repo-summary.md following this format:

---
repo: [REPO_NAME]
last_updated: [TODAY]
file_count: [COUNT]
---

# [REPO_NAME] — Index

## Purpose
[One sentence describing what this repo is for]

## Key Files
| File | What It Contains |
|------|-----------------|
[List every meaningful file with a one-line description]

## Top 5 Insights
[The 5 most important takeaways across all files in this repo]

## Gaps / TODOs
- [ ] [What's missing, incomplete, or should be added next]

Save the output to repo-summary.md in the repo root.
```

---

## 2. Diff Update (Periodic Maintenance)

Use this when the repo has new content and you want to update the existing summary.

```
Read the current repo-summary.md, then scan all files in this repo.

1. List files that are NEW since the last summary
2. List files that have been MODIFIED
3. List files that were DELETED
4. Update repo-summary.md:
   - Add new files to the Key Files table
   - Remove deleted files
   - Update file_count and last_updated
   - Revise Top 5 Insights if new content changes the picture
   - Update Gaps / TODOs based on current state

Show me the diff before saving.
```

---

## 3. Cross-Note Capture (Quick — 30 seconds)

Use this in any CC session when you notice a cross-domain insight.

```
Create a new cross-note in knowledge-hub/cross-notes/ with filename
YYYY-MM-DD-[slug].md using this format:

---
date: [TODAY]
tags: [relevant tags]
repos: [which repos this connects]
---

# [Title]

## Insight
[What's the cross-domain connection?]

## Source Repos
- `repo-name`: [specific file or folder]

## So What?
[One sentence — why does this matter?]
```

---

## 4. Full Refresh (Quarterly)

Use this once a quarter to rebuild all summaries from scratch.

```
For each repo listed in CLAUDE.md:
1. cd into the repo
2. Regenerate repo-summary.md from scratch
3. Copy it to knowledge-hub/indexes/[repo-name]-summary.md
4. Return to knowledge-hub
5. Update CLAUDE.md if any repo's purpose or key topics have shifted

After all repos are done, review cross-notes/ and archive any
that are no longer relevant.
```

---

## Usage Tips

- **First time setup**: Run prompt #1 on each repo, takes ~3 min per repo
- **Regular use**: Run prompt #2 only when you've added significant content
- **Cross-notes**: Do this anytime, it's the highest-value habit
- **Full refresh**: Once a quarter, or when you feel the index is stale
