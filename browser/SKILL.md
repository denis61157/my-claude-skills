---
name: browser
description: Use when user wants to browse the web, look at something in a browser, read page content, or interact with browser. Connects to Chrome Canary via CDP (remote debugging) using an isolated bot profile. Does NOT touch the user's main Chrome.
invocable: true
---

# Browser Skill

Connects to **Chrome Canary** via CDP (Chrome DevTools Protocol) using an isolated bot profile.

**IMPORTANT**: The user's main Chrome is never touched. Canary runs in parallel with a separate profile.

## When to invoke

- User says "open in browser", "browse to", "check in Chrome", "what tabs are open", etc.
- Need to read web page content
- Need to open a URL

## Connection algorithm

### 1. Check if CDP is already running

```bash
curl -s --max-time 2 http://localhost:9222/json/version
```

- If response → CDP is active, go to step 3
- If no response → go to step 2

### 2. Launch Chrome Canary with bot profile

#### 2a. Check if port is free

```bash
lsof -i :9222 2>/dev/null && echo "PORT_BUSY" || echo "PORT_FREE"
```

If port is busy — investigate what's using it.

#### 2b. Launch Canary

Bot profile is stored in `~/.chromium-bot`. It persists cookies and logins between sessions.

```bash
"/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary" \
  --remote-debugging-port=9222 \
  --user-data-dir="$HOME/.chromium-bot" \
  --no-first-run &

sleep 5
```

Verify connection:
```bash
curl -s --max-time 2 http://localhost:9222/json/version
```

If no response — wait 3 more seconds and retry.

### 3. List open tabs

```bash
curl -s http://localhost:9222/json/list | python3 -c "
import json, sys
tabs = json.load(sys.stdin)
pages = [t for t in tabs if t['type'] == 'page']
if not pages:
    print('No open tabs')
else:
    for i, t in enumerate(pages, 1):
        print(f\"{i}. {t['title']}\n   {t['url']}\n\")
"
```

### 4. Open a URL

```bash
curl -s -X PUT "http://localhost:9222/json/new?URL_HERE"
```

### 5. Read page content

#### 5a. Ensure websockets is installed

```bash
python3 -c "import websockets" 2>/dev/null || pip3 install --break-system-packages websockets
```

#### 5b. Read content

```bash
python3 -c "
import json, asyncio, websockets

async def get_content(ws_url):
    async with websockets.connect(ws_url) as ws:
        await ws.send(json.dumps({
            'id': 1,
            'method': 'Runtime.evaluate',
            'params': {'expression': 'document.body.innerText'}
        }))
        result = json.loads(await ws.recv())
        text = result.get('result', {}).get('result', {}).get('value', 'Could not read page')
        print(text[:15000])

import urllib.request
tabs = json.loads(urllib.request.urlopen('http://localhost:9222/json/list').read())
pages = [t for t in tabs if t['type'] == 'page']
if pages:
    asyncio.run(get_content(pages[0]['webSocketDebuggerUrl']))
else:
    print('No open tabs')
"
```

### 6. Navigate within a tab

```bash
python3 -c "
import json, asyncio, websockets

async def navigate(ws_url, url):
    async with websockets.connect(ws_url) as ws:
        await ws.send(json.dumps({
            'id': 1,
            'method': 'Page.navigate',
            'params': {'url': url}
        }))
        print(await ws.recv())

import urllib.request
tabs = json.loads(urllib.request.urlopen('http://localhost:9222/json/list').read())
pages = [t for t in tabs if t['type'] == 'page']
if pages:
    asyncio.run(navigate(pages[0]['webSocketDebuggerUrl'], 'TARGET_URL'))
"
```

## Key details

- **Browser**: Chrome Canary (`/Applications/Google Chrome Canary.app/`)
- **Bot profile**: `~/.chromium-bot` (isolated from main Chrome)
- **CDP port**: 9222
- **User's main Chrome is NEVER touched** — Canary runs independently
- Cookies and logins persist between sessions in the bot profile

## Error handling

- If `curl` to port 9222 doesn't respond after launch → wait 3 more seconds and retry
- If `websockets` is not installed → `pip3 install --break-system-packages websockets`
- If Canary won't start → check `pgrep -la "Chrome Canary"`
- If port 9222 is occupied → `lsof -i :9222` to find out by what
