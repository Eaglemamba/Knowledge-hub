Automated daily check-in — pre-fill data, then ask only the human questions.

## Step 1: Date Verification

Get today's date. Verify the year is 2026, NOT 2025. Store as YYYY-MM-DD.

## Step 2: Parallel Data Gathering

Spawn these as parallel Agent tasks (subagent_type: general-purpose). Each should return a concise summary (3-5 lines max):

**Agent A — Today's Git Activity:**
Run `git log --oneline --since="midnight" --all` in each of these repos:
- `~/coo-track`
- `~/Harvard-Business-Review`
- `~/health-check`
- `~/knowledge-hub`
- `~/AI articles/david-ai-learning`
Return a bullet list of commits per repo. If no commits today, say "No commits yet."

**Agent B — HBR Pipeline Status:**
- Count files in `~/Harvard-Business-Review/input/` (backlog)
- Count files in `~/Harvard-Business-Review/docs/` (processed)
- Count commits this week in `~/Harvard-Business-Review` with `git log --oneline --since="last monday"`
Return: "Backlog: X | Processed: Y | This week: Z commits"

**Agent C — Repo Sync Status:**
For each repo listed in Agent A, run:
- `git status --short` (any uncommitted changes?)
- `git log origin/main..HEAD --oneline 2>/dev/null` (any unpushed commits?)
Return a table: repo | clean/dirty | pushed/unpushed

**Agent D — Yesterday's Check-in:**
Find yesterday's check-in file at `~/coo-track/coo-track-os/reviews/daily/`. If yesterday's file doesn't exist, find the most recent one. Read it and extract:
- Energy level
- Tomorrow's one priority (which is today's carry-forward)
- Any patterns or sticking points noted
Return a 3-line summary for continuity.

## Step 3: Create the Check-in File

1. Read the template from `~/coo-track/coo-track-os/reviews/daily/_template.md`
2. Create a new file at `~/coo-track/coo-track-os/reviews/daily/YYYY-MM-DD.md`
3. Replace `[DATE]` with today's date
4. Pre-fill a new `## Daily Context` section right after the header (before Energy Level) with the gathered data:

```markdown
## Daily Context (auto-generated)

### Git Activity
{Agent A results}

### HBR Pipeline
{Agent B results}

### Repo Sync
{Agent C results}

### Yesterday's Carry-forward
{Agent D results}

---
```

## Step 4: Interactive Reflection

Present the pre-filled context to me, then walk through ONLY these questions one at a time. Be concise — this should take 5 minutes total:

1. **Energy level** (1-10)
2. **One operational win** — what moved the needle today?
3. **One leadership moment** — positive or missed opportunity?
4. **One thing to delegate or let go**
5. **Tomorrow's one priority**
6. **Content capture** — any insight for LinkedIn/Substack? (skip if nothing)

After each answer, write it into the file immediately.

## Step 5: Save, Commit, Push

1. Save the completed file
2. `cd ~/coo-track && git add coo-track-os/reviews/daily/YYYY-MM-DD.md`
3. `git commit -m "daily check-in YYYY-MM-DD"`
4. `git push origin main`
5. If push fails: retry 2-3 times with 5s delays. If still failing, inform me and move on — the commit is safe locally.

## Error Handling

- If any Agent task fails, skip that section and note "[data unavailable]" in the context block. Don't block the check-in.
- If the template file is missing, use the known structure (Energy, Operational Win, Leadership Moment, Delegate, Priority, Content Capture, Optional Quick Check).
- If yesterday's file doesn't exist, note "No recent check-in found" and skip carry-forward.
- Never let a data-gathering failure prevent the reflection questions from being asked.
