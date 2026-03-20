# My Claude Code Skills

A collection of custom skills, hooks, and setup guides I use with [Claude Code](https://docs.anthropic.com/en/docs/claude-code).

## Custom Skills

### [screenshot](./screenshot/)

Clipboard monitor that automatically saves screenshots and makes them accessible to Claude Code via `/screenshot` command.

**How it works:**
- A background daemon watches the clipboard for images (every 1s)
- When a new screenshot is detected, it saves it to `~/Screenshots` as a PNG
- Claude Code reads and describes the screenshots on demand

**Components:**
- `SKILL.md` — Claude Code skill definition
- `scripts/auto-screenshot-saver.sh` — clipboard monitor daemon
- `scripts/install.sh` — one-command installer
- `templates/com.user.screenshot-autosaver.plist` — LaunchAgent template

**Quick install:**
```bash
brew install pngpaste
cd screenshot && bash scripts/install.sh
```

See [screenshot/README.md](./screenshot/README.md) for details.

### [browser](./browser/)

Give Claude Code eyes in a real browser via Chrome DevTools Protocol. No MCP server, no npm — just `curl` and `python3`.

**How it works:**
- Launches Chrome Canary with an isolated bot profile (`~/.chromium-bot`)
- Connects via CDP on `localhost:9222`
- Lists tabs, opens URLs, reads page content
- Your main Chrome is never touched

**Quick install:**
```bash
brew install --cask google-chrome-canary
pip3 install websockets
cp browser/SKILL.md ~/.claude/skills/browser/SKILL.md
```

See [browser/README.md](./browser/README.md) for details.

### [analyze-patterns](./analyze-patterns/)

Analyze your Claude Code session transcripts to find repeating behavioral patterns — corrections, frequent tools, abandoned tasks, and places where Claude resists your intent.

**How it works:**
- A Python script extracts user messages from `~/.claude/projects/*.jsonl`
- Claude analyzes them for 4 pattern types (repeated corrections, frequent tools, abandoned tasks, Claude resistance)
- Shows evidence quotes and suggests concrete actions (rules, shortcuts, issues)
- Optionally creates GitHub Issues for each pattern found

**Quick install:**
```bash
mkdir -p ~/.claude/skills/analyze-patterns/scripts
cp analyze-patterns/SKILL.md ~/.claude/skills/analyze-patterns/SKILL.md
cp analyze-patterns/scripts/pattern-detector.py ~/.claude/skills/analyze-patterns/scripts/
```

See [analyze-patterns/README.md](./analyze-patterns/README.md) for details.

## Hooks & Automation

### [github-issues-memory](./github-issues-memory/)

Use GitHub Issues + Projects as persistent task memory for Claude Code. The agent creates, updates, and closes issues automatically — you never lose context between sessions.

- **SessionStart hook** — loads open issues when a session starts
- **PostToolUse hook** — reminds to update issues after `git push`
- **Rule file** — teaches the agent the workflow

Based on articles by [Sereja Ris](https://sereja.tech/blog/github-projects-ai-agent-memory/).

### [remote-control](./remote-control/)

Connect to a running Claude Code terminal session from your phone or any device. Start a task on your laptop, pick it up from the couch.

- Run `claude rc` in a separate terminal → get a link + QR code
- Open the link on your phone (web or Claude iOS app)
- Requires **Max** subscription (Pro coming soon)

See [remote-control/README.md](./remote-control/README.md) for details.

## Setup Guides

### [multi-account-sync](./multi-account-sync/)

Sync Claude Code configuration (skills, rules, settings) between multiple macOS user accounts on the same machine using `/Users/Shared/` and symlinks. No Git required for same-machine sync.

Based on [sync article](https://sereja.tech/blog/sync-claude-code-four-machines/) by Sereja Ris.

### "Fix Once, Rule Forever" approach

Instead of fixing the same mistake twice, write a rule in `~/.claude/rules/` so the agent never repeats it. Rules are auto-loaded every session, scoped by file path patterns.

Based on [Sereja Ris's article](https://sereja.tech/blog/fix-once-rule-forever/).

## Tips & Tricks

### `lfg` — Launch Claude Code in autonomous mode

A shell alias to run Claude Code with `--dangerously-skip-permissions` (no confirmation prompts). Inspired by [Sereja Ris](https://github.com/serejaris/ris-claude-code) and his Claude Code workflow.

Add to your `~/.zshrc`:

```bash
alias lfg="claude --dangerously-skip-permissions"
```

Then just type `lfg` in any project directory to start a fully autonomous Claude Code session.

> **Warning:** This skips all permission prompts. Use only in trusted environments — Claude will read, write, and execute without asking.

## Third-Party Skills I Use

| Skill | Author | Description |
|-------|--------|-------------|
| [superpowers](https://github.com/obra/superpowers) | Jesse Vincent | TDD, debugging, brainstorming, code review, planning workflows |
| [data](https://github.com/anthropics/knowledge-work-plugins/tree/main/data) | Anthropic | SQL, data visualization, dashboards, statistical analysis |
| [skill-creator](https://github.com/anthropics/claude-plugins-official) | Anthropic | Meta-skill for creating, validating, and packaging new skills |
| [frontend-design](https://github.com/anthropics/claude-plugins-official) | Anthropic | Distinctive, production-grade frontend UI with bold aesthetics |
| [developing-with-streamlit](https://github.com/streamlit/agent-skills) | Streamlit | Production-grade Streamlit apps — design, performance, layouts, data display |
| [frontend-slides](https://github.com/zarazhangrui/frontend-slides) | zarazhangrui | Animation-rich HTML presentations from scratch or PPT conversion |
| [macos-fixer](https://github.com/serejaris/ris-claude-code) | Sereja Ris | macOS memory diagnostics, performance troubleshooting |
| [git-workflow-manager](https://github.com/serejaris/ris-claude-code) | Sereja Ris | Conventional commits, semantic versioning, changelogs |

## Useful Reading

Articles that shaped this setup:

- [GitHub Projects как память для AI-агента](https://sereja.tech/blog/github-projects-ai-agent-memory/) — Sereja Ris
- [Хуки Claude Code: агент сам ведёт задачи](https://sereja.tech/blog/claude-code-hooks-github-issues/) — Sereja Ris
- [Как я синхронизирую Claude Code на четырёх компах](https://sereja.tech/blog/sync-claude-code-four-machines/) — Sereja Ris
- [Правка → Правило: как научить агента не повторять ошибки](https://sereja.tech/blog/fix-once-rule-forever/) — Sereja Ris
- [Модульные правила: как не утонуть в CLAUDE.md](https://sereja.tech/blog/modular-rules-claude-md/) — Sereja Ris
- [Claude Code получил память между сессиями](https://sereja.tech/blog/claude-code-auto-memory/) — Sereja Ris

## License

MIT
