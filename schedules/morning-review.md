# Morning Review Schedule

**Time**: 07:45 daily
**Purpose**: Start the day with intention and a clear experiment

## Prompt Template

```
Coach morning review:

1. Read my progress file
2. Review yesterday's experiment — what was the result?
3. Based on my current trajectory, what should today's focus be?
4. Design one specific action for today with a clear outcome
5. Give me a motivating insight from the knowledge base that's relevant to where I am right now

Keep it concise. I need clarity, not a lecture.
```

## Setup with Claude Code Scheduled Tasks

```bash
# Using Claude Code's built-in scheduling
claude schedule create \
  --name "morning-coach-review" \
  --cron "45 7 * * *" \
  --prompt "Read coaches/{coach-id}/progress.md and coaches/{coach-id}/config.md. Do a morning coaching review: summarize yesterday's experiment results, design today's focus action, and share one relevant insight from NotebookLM. Update progress.md with the session. Keep it concise and actionable."
```
