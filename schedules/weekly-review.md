# Weekly Review Schedule

**Time**: 07:45 every Sunday
**Purpose**: Reflect on the week, extract patterns, design next week's experiments

## Prompt Template

```
Coach weekly review:

1. Read my progress file
2. Summarize this week's experiments and results
3. Identify patterns — what's working, what's not?
4. Query the knowledge base for frameworks relevant to my current challenges
5. Design 2-3 experiments for next week
6. Ask me 3 deep reflection questions
7. Update progress file with weekly review section

This is the most important session of the week. Be thorough and challenging.
```

## Setup with Claude Code Scheduled Tasks

```bash
claude schedule create \
  --name "weekly-coach-review" \
  --cron "45 7 * * 0" \
  --prompt "Read coaches/{coach-id}/progress.md and coaches/{coach-id}/config.md. Do a comprehensive weekly review: summarize experiments and results, identify patterns, query NotebookLM for relevant frameworks, design 2-3 experiments for next week, and ask 3 deep reflection questions. Update progress.md with the full weekly review. Be thorough."
```
