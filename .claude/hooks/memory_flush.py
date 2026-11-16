#!/usr/bin/env python3
"""Memory flush: summarize a Claude Code session into the brain's daily log.

Called three ways:
  1. SessionEnd / PreCompact hook (via memory-flush.sh): JSON on stdin; this re-launches itself
     detached so the hook returns instantly and a slow summary never blocks exit or compaction.
  2. --transcript PATH: flush one transcript now (what the detached child runs).
  3. --recent HOURS [--dir DIR]: flush every transcript touched in the last HOURS. The server's
     nightly reflection uses this to catch the long-running Telegram chat, which rarely ends.

Only turns not yet flushed are summarized (a per-transcript line offset in STATE), so PreCompact,
SessionEnd and the nightly sweep never write the same conversation twice.

Recursion guard: runs started by JARVIS's own jobs set CLAUDE_INVOKED_BY, and those are skipped. The
summary call itself sets it too, uses no tools, and isn't saved as a session.
"""
import fcntl
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

HOME = Path.home()
BRAIN = Path(os.environ.get("JARVIS_BRAIN", HOME / "code/jarvis-brain"))
STATE = HOME / ".local/state/jarvis/flush"
LOG = HOME / ".local/state/jarvis/flush.log"
MIN_USER_TURNS = 2      # one-question sessions aren't worth a log entry
MIN_CHARS = 600
MAX_CHARS = 40_000      # newest part wins if a session is huge
CLAUDE = shutil.which("claude") or str(HOME / ".local/bin/claude")
NOISE = re.compile(r"<(system-reminder|command-[a-z-]+|local-command-[a-z]+|pasted_content[^>]*)>"
                   r".*?</\1[^>]*>", re.S)


def log(msg: str) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a") as fh:
        fh.write(f"{datetime.now().isoformat(timespec='seconds')} {msg}\n")


def text_of(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(b.get("text", "") for b in content
                         if isinstance(b, dict) and b.get("type") == "text")
    return ""


def read_turns(path: Path, start: int):
    """New conversation turns after line `start`. Returns (turns, title, total_lines)."""
    turns, title, n = [], "", 0
    with path.open(encoding="utf-8", errors="replace") as fh:
        for n, line in enumerate(fh, 1):
            try:
                d = json.loads(line)
            except ValueError:
                continue
            if d.get("type") == "custom-title":
                title = d.get("customTitle") or d.get("title") or title
            if n <= start or d.get("type") not in ("user", "assistant") or d.get("isMeta"):
                continue
            if d.get("isCompactSummary"):
                continue  # a summary of turns we've already flushed
            t = NOISE.sub("", text_of(d.get("message", {}).get("content")))
            t = re.sub(r"</?channel[^>]*>", "", t).strip()  # Telegram wrapper (chat ids etc.)
            if t:
                turns.append(("Terry" if d["type"] == "user" else "JARVIS", t))
    return turns, title, n


def summarize(turns, title: str, where: str) -> str:
    convo = "\n\n".join(f"**{who}:** {t}" for who, t in turns)[-MAX_CHARS:]
    prompt = f"""Below is part of a conversation between Terry and JARVIS ({where}). Write the entry
for JARVIS's daily log: what a teammate reading it tomorrow needs, not a transcript.

Use these headed bullet groups, and leave out any group that would be empty:
**Decided:** decisions Terry made, with the why when stated.
**Done:** what was built, fixed, sent or shipped (name files, repos, services).
**Learned:** new facts worth remembering. Prefix each [S] for a state fact (it replaces an older
value, e.g. "the server runs Ubuntu 26.04") or [E] for an event (it happened once, e.g. "the brief
failed on 11-15"). Include gotchas that cost time.
**Open:** what's unfinished or waiting on Terry.

Rules: short bullets, plain American English, no filler, no secrets (never copy a token, key,
password or one-time code). Under 250 words. If nothing in it is worth remembering (small talk, a
single lookup), reply with exactly NOTHING.

Conversation{f' ("{title}")' if title else ''}:
{convo}"""
    env = dict(os.environ, CLAUDE_INVOKED_BY="memory-flush")
    no_tg = json.dumps({"enabledPlugins": {"telegram@claude-plugins-official": False}})
    r = subprocess.run([CLAUDE, "-p", prompt, "--tools", "", "--no-session-persistence",
                        "--settings", no_tg, "--setting-sources", "user"],
                       cwd=str(HOME), capture_output=True, text=True, timeout=600, env=env)
    if r.returncode != 0:
        raise RuntimeError(f"claude -p failed ({r.returncode}): {r.stderr[-300:]}")
    return r.stdout.strip()


def append_daily(entry: str, title: str, where: str) -> Path:
    day = datetime.now().strftime("%Y-%m-%d")
    p = BRAIN / "daily" / f"{day}.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    head = f"\n## {datetime.now():%H:%M} · {where}" + (f" · {title}" if title else "") + "\n\n"
    with p.open("a") as fh:
        if fh.tell() == 0:
            fh.write(f"# {day}\n")
        fh.write(head + entry.strip() + "\n")
    return p


def flush(path: Path) -> str:
    STATE.mkdir(parents=True, exist_ok=True)
    key = STATE / (path.stem + ".json")
    with open(STATE / ".lock", "w") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)  # one flush at a time per machine
        start = json.loads(key.read_text()).get("lines", 0) if key.exists() else 0
        turns, title, total = read_turns(path, start)
        users = sum(1 for who, _ in turns if who == "Terry")
        size = sum(len(t) for _, t in turns)
        if users < MIN_USER_TURNS or size < MIN_CHARS:
            return f"skip {path.name}: {users} user turns, {size} chars"
        where = socket.gethostname().split(".")[0]
        if '<channel source=\\"plugin:telegram' in path.read_text(errors="replace")[:200000]:
            where += " (Telegram)"
        entry = summarize(turns, title, where)
        key.write_text(json.dumps({"lines": total, "at": time.time()}))
        if entry.strip() == "NOTHING" or len(entry) < 20:
            return f"nothing worth keeping in {path.name}"
        out = append_daily(entry, title, where)
    sync = BRAIN / "scripts/brain-sync.sh"
    if sync.exists():
        subprocess.run(["bash", str(sync)], capture_output=True, timeout=180)
    return f"flushed {path.name} ({users} user turns) -> {out.name}"


def main(argv) -> int:
    if os.environ.get("CLAUDE_INVOKED_BY"):
        return 0  # a JARVIS job's own session: never summarize those
    try:
        if "--transcript" in argv:
            log(flush(Path(argv[argv.index("--transcript") + 1])))
        elif "--recent" in argv:
            hours = float(argv[argv.index("--recent") + 1])
            root = Path(argv[argv.index("--dir") + 1]) if "--dir" in argv else HOME / ".claude/projects"
            cutoff = time.time() - hours * 3600
            for p in sorted(root.rglob("*.jsonl")):
                if "subagents" in p.parts or p.stat().st_mtime < cutoff:
                    continue
                log(flush(p))
        else:  # hook mode
            data = json.loads(sys.stdin.read() or "{}")
            tp = data.get("transcript_path")
            if tp and Path(tp).exists():
                subprocess.Popen([sys.executable, __file__, "--transcript", tp],
                                 stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                 stderr=subprocess.DEVNULL, start_new_session=True)
                log(f"hook {data.get('hook_event_name', '?')} ({data.get('reason', '')}): queued {Path(tp).name}")
    except Exception as e:
        log(f"ERROR {type(e).__name__}: {e}")
    return 0  # a memory hook must never block the session


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
