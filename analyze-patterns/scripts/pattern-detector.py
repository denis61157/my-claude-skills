#!/usr/bin/env python3
"""Pattern Detector — extracts user/assistant messages from Claude Code session transcripts.

Outputs structured JSON for analysis by Claude Code skill /analyze-patterns.
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

SESSIONS_DIR = Path.home() / ".claude" / "projects"
STATE_FILE = Path.home() / ".claude" / "pattern-detector-state.json"


def load_state() -> dict:
    """Load last run state."""
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"last_run": None, "analyzed_sessions": []}


def save_state(state: dict):
    """Save state after run."""
    STATE_FILE.write_text(json.dumps(state, indent=2))


def collect_sessions(state: dict, full: bool = False) -> list[dict]:
    """Find session .jsonl files, optionally filtered by last_run date."""
    sessions = []
    analyzed = set(state.get("analyzed_sessions", []))

    for jsonl_path in SESSIONS_DIR.rglob("*.jsonl"):
        # Skip subagent transcripts
        if "subagents" in str(jsonl_path):
            continue

        session_id = jsonl_path.stem

        if not full and session_id in analyzed:
            continue

        # Get project name from parent dir
        project_dir = jsonl_path.parent.name
        # Convert path-encoded name to readable
        project_name = project_dir.rsplit("-", 1)[-1] if "-" in project_dir else project_dir

        sessions.append({
            "id": session_id,
            "path": str(jsonl_path),
            "project": project_name,
        })

    return sessions


def extract_messages(sessions: list[dict], user_only: bool = False) -> dict[str, list[dict]]:
    """Extract user and assistant text messages grouped by project."""
    by_project: dict[str, list[dict]] = {}

    for session in sessions:
        project = session["project"]
        if project not in by_project:
            by_project[project] = []

        with open(session["path"]) as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                except (json.JSONDecodeError, ValueError):
                    continue

                msg_type = entry.get("type")
                if msg_type not in ("user", "assistant"):
                    continue

                message = entry.get("message", {})
                content = message.get("content", "")

                # User messages: extract text
                if msg_type == "user" and isinstance(content, str) and content.strip():
                    by_project[project].append({
                        "role": "user",
                        "text": content.strip()[:2000],
                    })

                # Assistant messages: extract text blocks only (skip thinking, tool_use)
                elif not user_only and msg_type == "assistant" and isinstance(content, list):
                    text_parts = []
                    for block in content:
                        if isinstance(block, dict) and block.get("type") == "text":
                            text_parts.append(block.get("text", ""))
                    if text_parts:
                        combined = "\n".join(text_parts).strip()[:1000]
                        if combined:
                            by_project[project].append({
                                "role": "assistant",
                                "text": combined,
                            })

    return by_project


def main():
    parser = argparse.ArgumentParser(description="Extract messages from Claude Code sessions")
    parser.add_argument("--full", action="store_true", help="Re-extract from all sessions")
    parser.add_argument("--update-state", action="store_true", help="Mark sessions as analyzed")
    parser.add_argument("--user-only", action="store_true", help="Only extract user messages (smaller output)")
    parser.add_argument("--stats", action="store_true", help="Print stats to stderr, JSON to stdout")
    args = parser.parse_args()

    state = load_state()

    sessions = collect_sessions(state, full=args.full)
    if not sessions:
        print("No new sessions.", file=sys.stderr)
        print("[]")
        return

    if args.stats:
        print(f"Found {len(sessions)} sessions to analyze.", file=sys.stderr)

    messages_by_project = extract_messages(sessions, user_only=args.user_only)

    if args.stats:
        for project, msgs in messages_by_project.items():
            user_count = sum(1 for m in msgs if m["role"] == "user")
            print(f"  {project}: {user_count} user, {len(msgs) - user_count} assistant", file=sys.stderr)

    # Output as JSON to stdout
    output = {
        "extracted_at": datetime.now(timezone.utc).isoformat(),
        "session_count": len(sessions),
        "session_ids": [s["id"] for s in sessions],
        "projects": {
            project: {
                "message_count": len(msgs),
                "user_count": sum(1 for m in msgs if m["role"] == "user"),
                "messages": msgs,
            }
            for project, msgs in messages_by_project.items()
        },
    }

    json.dump(output, sys.stdout, ensure_ascii=False, indent=2)

    # Optionally update state
    if args.update_state:
        state["last_run"] = datetime.now(timezone.utc).isoformat()
        state["analyzed_sessions"].extend(s["id"] for s in sessions)
        save_state(state)
        if args.stats:
            print(f"\nState updated.", file=sys.stderr)


if __name__ == "__main__":
    main()
