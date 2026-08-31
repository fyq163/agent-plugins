#!/usr/bin/env python3
"""PreToolUse command audit for shell-based file modifications."""

import json
import re
import shlex
import sys


HEREDOC_START = re.compile(r"<<-?\s*['\"]?([A-Za-z_]\w*)")
HEREDOC_WRITE = re.compile(
    r"\.write_text\(|\.write_bytes\("
    r"|\bopen\s*\([^)]*['\"][waxu+]{1,2}['\"]"
    r"|\bos\.replace\("
    r"|\bshutil\.(?:copy|copy2|copyfile|move|rmtree)\b"
)


def heredoc_writes(command: str) -> bool:
    """Detect file writes inside a heredoc body (e.g. python3 - <<'PY')."""
    if not HEREDOC_START.search(command):
        return False
    return bool(HEREDOC_WRITE.search(command))


def writes_file(command: str) -> bool:
    if re.search(r"(?<!\S)(?:\d+)?>{1,2}(?![&])", command):
        return True
    if heredoc_writes(command):
        return True
    if re.search(r"(?<!\S)(?:\d+)?>{1,2}(?![&])", command):
        return True
    try:
        tokens = shlex.split(command)
    except ValueError:
        return False
    starts = [0]
    starts.extend(i + 1 for i, token in enumerate(tokens) if token in {";", "&&", "||", "|", "&"})
    return any(
        0 <= index < len(tokens)
        and (tokens[index] == "tee" or tokens[index].endswith("/tee"))
        for index in starts
    )


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    if data.get("tool_name") != "Bash":
        return 0
    command = (data.get("tool_input") or {}).get("command", "") or ""
    if not writes_file(command):
        return 0
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "additionalContext": (
                "[command-audit] Prefer the `apply_patch` tool for modifying files "
                "instead of shell redirection or `cat <<EOF`/`tee` commands."
            ),
        }
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
