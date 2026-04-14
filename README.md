# Knowledge Coach System

把任何人的文章變成你的私人實踐教練。

Transform any author's articles into a personal AI practice coach using Claude Code + Google NotebookLM.

## The Problem

We all read great articles, feel inspired, then forget everything 3 days later. The gap between learning and action is where knowledge dies.

**A good coach bridges this gap** — turning knowledge into verifiable experiments, not just advice.

## How It Works

```
Articles (Huberman, Dan Koe, etc.)
    ↓
Google NotebookLM (knowledge base, powered by Gemini 2.5)
    ↓
Claude Code + notebooklm-mcp-cli (orchestrator)
    ↓
Personal Coach (config + progress + scheduling)
    ↓
Daily Loop: Learn → Experiment → Track → Iterate
```

### The Four Components

| Component | What | How |
|-----------|------|-----|
| **Knowledge Base** | Coach's brain | Google NotebookLM (semantic understanding, not just search) |
| **Config File** | Coach's personality | Markdown file defining style, rules, frameworks |
| **Progress File** | Coach's memory | Markdown file tracking goals, experiments, insights |
| **Schedule** | Coach's rhythm | 3 daily/weekly touchpoints to keep the loop running |

## Quick Start

### Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed
- Google account (for NotebookLM)
- Python 3.10+ (for URL scraper)
- `notebooklm-mcp-cli` installed ([setup guide](https://github.com/nicholasgriffintn/notebooklm-mcp))

### Step 1: Collect Articles (5 min)

```bash
pip install requests

# Scrape article URLs from a website's sitemap
python scripts/scrape_urls.py https://example.com/sitemap.xml --filter /blog/

# Output: CSV files split into chunks of 50 (NotebookLM free tier limit)
```

### Step 2: Set Up NotebookLM (5 min)

1. Go to [notebooklm.google.com](https://notebooklm.google.com)
2. Create a new notebook
3. Add sources → Website URLs → paste URLs from the CSV
4. If you have more than 50 articles, create multiple notebooks
5. Note your notebook IDs (from the URL)

### Step 3: Connect NotebookLM to Claude Code

```bash
# Install the MCP connector
npm install -g notebooklm-mcp-cli

# Configure in Claude Code settings
# Add to ~/.claude/settings.json under mcpServers
```

### Step 4: Create Your Coach (5 min)

```bash
# Interactive setup
python scripts/setup_coach.py

# Or one-liner
python scripts/setup_coach.py --id dan-koe --author "Dan Koe" --topic "personal mastery" --style "direct, deep, zero-fluff"
```

### Step 5: Set Up Schedules

See `schedules/` for schedule templates. Set up 3 recurring check-ins:

- **07:45 daily** — Morning review: design today's action
- **17:30 daily** — Afternoon check-in: record what happened
- **07:45 Sunday** — Weekly review: analyze patterns, design next week

### Step 6: Start Coaching

Just say **"教練"** or **"coach"** to Claude Code.

## Project Structure

```
├── CLAUDE.md              # Coach role definition for Claude Code
├── coaches/               # Each coach gets its own directory
│   └── {coach-id}/
│       ├── config.md      # Personality, style, rules, frameworks
│       └── progress.md    # Goals, experiments, session log
├── templates/             # Templates for creating new coaches
│   ├── coach-config.template.md
│   └── progress.template.md
├── scripts/
│   ├── scrape_urls.py     # Collect article URLs from sitemaps
│   └── setup_coach.py     # Interactive coach setup wizard
└── schedules/
    ├── morning-review.md
    ├── afternoon-checkin.md
    └── weekly-review.md
```

## Creating Additional Coaches

Adding a new coach takes ~30 minutes:

1. Collect article URLs (10 min) → `python scripts/scrape_urls.py`
2. Import into NotebookLM (5 min)
3. Copy config template and fill in (5 min)
4. Set your goals in progress file (2 min)

### Coach Ideas

- **Naval Ravikant** → startup/wealth-building coach
- **Paul Graham** → thinking/writing coach
- **Andrew Huberman** → health/fitness coach
- **James Clear** → habit-building coach
- **Your own past articles** → self-reflection coach

## Design Philosophy

The core loop: **Learning → Experiment → Track → Iterate**

A coach doesn't just say "you should focus." A coach says:
> "Your experiment today: from 9 AM to 10 AM, close all notifications and work on one thing. Tomorrow we review the results."

The difference: **knowledge transformed into verifiable experiments.**

## Limitations

- Requires NotebookLM (unofficial API via MCP, may change)
- Cookie-based authentication for NotebookLM
- Free tier: 50 sources per notebook (split into multiple)
- Progress file is local — no cross-device sync (use Git or cloud storage)
