# Knowledge Hub - David Kuo's Personal Knowledge Index

## Purpose
This is the **meta repository** — an index and navigation layer across all of David's knowledge repos. It does NOT duplicate content. It tells you where to find what, and captures cross-domain insights that don't belong in any single repo.

## Repository Map

| Repo | Domain | Purpose | Key Topics |
|------|--------|---------|------------|
| `SterileGMP-Knowledge-Hub` | Pharma | Multi-source GMP knowledge base — PDA, ISPE, FDA, PIC/S, ICH, USP, ISO, ECA | Aseptic processing, sterilization, container closure, isolators, CCS, C&Q, water systems, HVAC |
| `david-ai-learning` | AI | AI learning notes, tutorials, experiments | Prompt engineering, Claude workflows, AI tools, LLM concepts |
| `Harvard-Business-Review` | Leadership | HBR article notes & management insights | Leadership, strategy, organizational behavior, decision-making |

## Cross-Domain Connections

These are insights that span multiple repos — the real value of having this index.

### AI x Pharma
- Using LLM tools to interpret and apply GMP guidance across PDA, ISPE, FDA, PIC/S, ICH, USP, ISO (connects: `david-ai-learning` + `SterileGMP-Knowledge-Hub`)
- AI-assisted regulatory intelligence, cross-source GMP knowledge retrieval, and `/gmp-ask` skill

### Leadership x Pharma
- HBR management frameworks applied to CDMO team leadership and operational excellence (connects: `Harvard-Business-Review` + `SterileGMP-Knowledge-Hub`)
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

## Response Format — Pharma Questions

When answering any drug product / pharma / GMP question, always follow this format:

### Required Citations
- Every key point must cite its **source document + Section** (PDA TR#, ISPE Vol#, FDA GFI, Annex 1, ISO #, etc.)
- Format examples:
  - **(PDA TR22, Section 3.2)** or **(TR22 §3.2)**
  - **(ISPE Baseline Vol.5, Section 4.3)** or **(ISPE Vol.5 §4.3)**
  - **(FDA Aseptic Guide 2004, Section XII)**
  - **(PIC/S Annex 1 2022, Section 8.5)**
- Cross-reference other relevant documents when the topic spans multiple sources

### Answer Template
```
### [Topic Title]

**[Best Practice Point 1]** — [Summary of guidance] **(Source, Section X.X)**

**[Best Practice Point 2]** — [Summary of guidance] **(Source A §X.X; Source B §X.X)**

...

**Cross-References:**
- See also: [Source] Section X.X for [related topic]
- See also: [Source] Section X.X for [related topic]
```

### Example
> **Frequency & Number** — Minimum 3 consecutive successful APS for new facility/line/process
> qualification **(PDA TR22, Section 3.2)**. ISPE C&Q requires documented URS/FRS as pre-requisite
> to IQ/OQ **(ISPE Baseline Vol.5 §4.2)**. Annex 1 mandates CCS as overarching framework
> **(PIC/S Annex 1 2022, Section 4.1)**.

### Source Repos
- Primary source: `SterileGMP-Knowledge-Hub/knowledge/` — contains full-text MDs per document
- Use `knowledge/INDEX.md` for topic routing across all sources

## Knowledge Gaps — Documents to Add

### PDA
| Report | Title | Why Needed | Referenced By |
|--------|-------|------------|---------------|
| TR51 | Biological Indicators for Gas and Vapor-Phase Decontamination Processes | Core reference for VPHP cycle development — D-value, BI placement, cycle parameters | PtC-12 §Q7.2, Guide No.1 §10.2 |

### ISPE (priority order)
| Document | Title | Why Needed |
|----------|-------|------------|
| ISPE Baseline Vol.5 C&Q (2nd Ed.) | Commissioning & Qualification | Foundational C&Q framework — IQ/OQ/PQ/FAT/SAT |
| ISPE Baseline Vol.7 | Risk-Based Manufacture | Risk-based approach to pharma manufacturing |
| ISPE Baseline Vol.3 | Sterile Manufacturing Facilities | Facility design for sterile products |
| ISPE Baseline Vol.4 | Water & Steam Systems | WFI/PW/clean steam |
| ISPE GAMP 5 | Computerized Systems Validation | CSV framework for pharma IT systems |
| ISPE GPG HVAC | HVAC for Pharmaceutical Facilities | Cleanroom design, pressure cascades, AHU |

### Regulatory
| Document | Body | Why Needed |
|----------|------|------------|
| FDA Aseptic Processing Guidance (2004) | FDA | US baseline for aseptic manufacturing |
| PIC/S Annex 1 (2022) | PIC/S | EU GMP sterile mfg — biggest 2022 update |

## Conventions
- All notes in Markdown
- File naming: `YYYY-MM-DD-topic-slug.md`
- Tags at top of each note using YAML frontmatter
- Keep cross-notes short — max 200 words, link to source repos for detail
