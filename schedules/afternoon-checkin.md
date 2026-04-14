# Afternoon Check-in Schedule

**Time**: 17:30 daily
**Purpose**: Record what happened, capture learnings, adjust if needed

## Prompt Template

```
Coach afternoon check-in:

1. Read my progress file
2. Ask me what I accomplished today regarding my active experiment
3. Record my response and any observations
4. If I'm off track, suggest a small adjustment for tomorrow
5. Update progress file

Be brief. This is a quick status sync, not a deep session.
```

## Setup with Claude Code Scheduled Tasks

```bash
claude schedule create \
  --name "afternoon-coach-checkin" \
  --cron "30 17 * * *" \
  --prompt "Read coaches/{coach-id}/progress.md and coaches/{coach-id}/config.md. Do an afternoon check-in: ask what I accomplished today on my active experiment, record observations, suggest adjustments if needed. Update progress.md. Keep it brief."
```
