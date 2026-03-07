# Browser Skill for Claude Code

Give Claude Code eyes in a real browser — browse the web, read pages, and interact with sites using Chrome DevTools Protocol. No MCP server needed, no npm dependencies.

## Why not Chrome DevTools MCP?

This skill connects directly to Chrome via CDP using only `curl` and `python3` (with `websockets`). No MCP server to install, no Node.js, no config files. It just works.

The key idea: use **Chrome Canary** with a **separate bot profile** (`~/.chromium-bot`), so Claude never touches your main Chrome with all your logins and tabs.

## Prerequisites

- macOS
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code)
- [Google Chrome Canary](https://www.google.com/chrome/canary/) — runs alongside regular Chrome
- Python 3 (pre-installed on macOS)

## Installation

### 1. Install Chrome Canary

Download from [google.com/chrome/canary](https://www.google.com/chrome/canary/) or:

```bash
brew install --cask google-chrome-canary
```

### 2. Create the bot profile

Launch Canary once with the isolated profile:

```bash
"/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary" \
  --remote-debugging-port=9222 \
  --user-data-dir="$HOME/.chromium-bot" \
  --no-first-run
```

Log into any services you want Claude to access (Google, GitHub, etc.), then close Canary. Credentials persist in `~/.chromium-bot`.

### 3. Install the skill

```bash
mkdir -p ~/.claude/skills/browser
cp SKILL.md ~/.claude/skills/browser/SKILL.md
```

### 4. Install websockets

```bash
pip3 install websockets
```

## Usage

In Claude Code:

```
/browser                    # connect and show open tabs
open https://example.com    # open a URL (Claude will invoke the skill)
what's on the page?         # read current page content
```

Or just say things like:
- "go to my GitHub and check recent PRs"
- "open this URL in the browser"
- "read what's on the page"

## How it works

```
Claude Code ──curl──→ Chrome Canary (port 9222)
                        ├── Bot profile (~/.chromium-bot)
                        ├── Separate from your main Chrome
                        └── Persists cookies between sessions

Your Chrome ──────────→ Untouched, runs independently
```

1. Claude checks if Canary is running on port 9222
2. If not — launches it with the bot profile
3. Uses CDP to list tabs, navigate, and read page content
4. Page text is extracted via `Runtime.evaluate` over WebSocket

## Security

- **Isolated profile**: `~/.chromium-bot` is completely separate from your main Chrome
- **No password visibility**: Claude cannot see what you type in password fields
- **Local only**: CDP listens on `localhost:9222`, not exposed to the network
- **You control access**: only services you've logged into in the bot profile are accessible

## Uninstall

```bash
# Remove the skill
rm -rf ~/.claude/skills/browser

# Remove the bot profile (deletes all saved logins)
rm -rf ~/.chromium-bot
```

## License

MIT
