# Knowledge Hub - David Kuo's Personal Knowledge Index

## Purpose
This is the **meta repository** — an index and navigation layer across all of David's knowledge repos. It does NOT duplicate content. It tells you where to find what, and captures cross-domain insights that don't belong in any single repo.

## Repository Map

| Repo | Domain | Purpose | Key Topics |
|------|--------|---------|------------|
| `PDA_Technical-Report-Knowledge` | Pharma | PDA technical report summaries & key takeaways | Aseptic processing, sterilization, container closure, isolators, lyophilization |
| `david-ai-learning` | AI | AI learning notes, tutorials, experiments | Prompt engineering, Claude workflows, AI tools, LLM concepts |
| `Harvard-Business-Review` | Leadership | HBR article notes & management insights | Leadership, strategy, organizational behavior, decision-making |

## Cross-Domain Connections

These are insights that span multiple repos — the real value of having this index.

### AI x Pharma
- Using LLM tools to interpret and apply PDA technical guidance (connects: `david-ai-learning` + `PDA_Technical-Report-Knowledge`)
- AI-assisted regulatory intelligence and GMP knowledge retrieval

### Leadership x Pharma
- HBR management frameworks applied to CDMO team leadership and operational excellence (connects: `Harvard-Business-Review` + `PDA_Technical-Report-Knowledge`)
- Change management principles for AI adoption in manufacturing

### AI x Leadership
- AI literacy as a leadership competency (connects: `david-ai-learning` + `Harvard-Business-Review`)
- Using AI tools to scale management decision-making

## How to Use This Repo

### For Claude Code Sessions
When working in CC, open this repo first to orient yourself. Then switch to the specific repo for deep work.

Example workflow:
1. `cd knowledge-hub` → check CLAUDE.md for context
2. Identify which repo has the info you need
3. `cd ../target-repo` → do the actual work
4. Return here to log any cross-domain insight in `/cross-notes/`

### For Adding New Knowledge
- Single-domain insight → goes directly into the relevant repo
- Cross-domain insight → create a note in `/cross-notes/` with links to relevant repos
- New repo needed → add it to the Repository Map above

## Directory Structure
```
knowledge-hub/
├── CLAUDE.md              # This file — the master index
├── README.md              # Public-facing description
├── cross-notes/           # Cross-domain insights
│   └── .gitkeep
├── indexes/               # Auto-generated or manual indexes of each repo
│   └── .gitkeep
└── templates/             # Templates for common note types
    ├── cross-note.md
    └── repo-summary.md
```

## Conventions
- All notes in Markdown
- File naming: `YYYY-MM-DD-topic-slug.md`
- Tags at top of each note using YAML frontmatter
- Keep cross-notes short — max 200 words, link to source repos for detail
