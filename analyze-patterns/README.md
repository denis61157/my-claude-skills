# Analyze Patterns — Claude Code Skill

Automatically analyze your Claude Code session transcripts to find repeating behavioral patterns — corrections you keep making, workflows you use often, tasks you abandoned, and places where Claude resists your intent.

## What it finds

| Pattern | Description | Suggested action |
|---------|-------------|------------------|
| **REPEATED_CORRECTION** | You correct Claude the same way across sessions | Add rule to CLAUDE.md or `~/.claude/rules/` |
| **FREQUENT_TOOL** | Same workflow/command used repeatedly | Create auto-trigger or shortcut |
| **ABANDONED_TASK** | Work started but never finished | Create an issue to track it |
| **CLAUDE_RESISTANCE** | Claude doesn't follow your instructions | Improve prompts or rules |

## How it works

```
~/.claude/projects/**/*.jsonl
        │
        ▼
  pattern-detector.py    ← extracts user messages from session transcripts
        │
        ▼
  /tmp/pattern-extract.json
        │
        ▼
  Claude analyzes patterns ← the SKILL.md prompt guides the analysis
        │
        ▼
  GitHub Issues (optional) ← one issue per pattern found
```

1. A Python script reads Claude Code session transcripts (`~/.claude/projects/`)
2. Extracts user messages into structured JSON
3. Claude analyzes them looking for the 4 pattern types
4. Results are shown to you with evidence quotes
5. Optionally creates GitHub Issues for each pattern

The script supports **incremental mode** — it tracks which sessions have been analyzed and only processes new ones on subsequent runs.

## Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code)
- Python 3
- `gh` CLI (optional, for creating GitHub Issues)

## Installation

```bash
# Copy skill and script
mkdir -p ~/.claude/skills/analyze-patterns/scripts
cp SKILL.md ~/.claude/skills/analyze-patterns/SKILL.md
cp scripts/pattern-detector.py ~/.claude/skills/analyze-patterns/scripts/pattern-detector.py
chmod +x ~/.claude/skills/analyze-patterns/scripts/pattern-detector.py
```

## Usage

In Claude Code:

```
/analyze-patterns           # incremental — only new sessions
/analyze-patterns --full    # rescan all sessions
```

Or just say:
- "analyze my sessions"
- "find patterns in how I use Claude"
- "what mistakes does Claude keep making?"

## Example output

```
### REPEATED_CORRECTION: Claude asks for confirmation too often
**Priority:** high

**Evidence:**
- "just do it, don't ask" (project-a, 3 sessions)
- "stop asking for permission" (project-b, 2 sessions)

**Suggestion:** Add to CLAUDE.md:
  "Don't ask for confirmation on routine operations — just do it."
```

## Privacy

The script only reads your **local** session transcripts from `~/.claude/projects/`. Nothing is sent anywhere — all analysis happens locally inside your Claude Code session. The extracted JSON is written to `/tmp/` and can be deleted after analysis.

If you use the GitHub Issues feature, pattern titles and evidence quotes will be posted to your repository. Review the output before confirming.

## License

MIT
