#!/usr/bin/env python3
"""Nightly reflection: turn the day's conversations into durable memory.

Once a day at REFLECT_HOUR local (03:00 by default), after Terry's day is over:
  1. Flush every conversation on this server from the last 26 hours into daily/ (catches the
     long-running Telegram chat, which seldom ends a session on its own).
  2. Claude reads the daily logs written since the last reflection and updates MEMORY.md (the
     headline layer every session loads), USER.md (facts about Terry), and wiki project/tool pages.
  3. SOUL.md is never edited. Personality changes are only proposed, in proposals/soul.md, and the
     morning brief asks Terry about them. (Stops "soul drift".)
The guard in brain_edit.py reverts anything outside those paths.

Usage: reflect.py [--force] [--no-commit]"""
import subprocess
import sys
from datetime import timedelta

from brain_edit import guarded_edit
from jarvis_jobs import BRAIN, CFG, ENGINE, HOME, log, now_local, read_state, write_state

JOB = "reflect"
ALLOWED = ("MEMORY.md", "USER.md", "proposals/", "wiki/")


def main(argv) -> int:
    force = "--force" in argv
    local = now_local()
    today = local.date().isoformat()
    state = read_state(JOB, {})
    if not force and (state.get("last_run") == today or local.hour < int(CFG.get("REFLECT_HOUR", "3"))):
        return 0

    # 1. Flush recent server conversations (the flush skips anything already flushed).
    r = subprocess.run(["python3", str(ENGINE / ".claude/hooks/memory_flush.py"), "--recent", "26",
                        "--dir", str(HOME / ".claude/projects")], capture_output=True, text=True,
                       timeout=1800)
    if r.returncode != 0:
        log(JOB, f"flush sweep failed: {r.stderr[-300:]}")

    # 2. Which daily logs are new since the last reflection (both machines write them).
    since = state.get("last_run") or (local.date() - timedelta(days=2)).isoformat()
    logs = sorted(p for p in (BRAIN / "daily").glob("*.md") if p.stem >= since)
    if not logs:
        log(JOB, "no daily logs since the last reflection")
        write_state(JOB, {"last_run": today, "changes": {}})
        return 0
    log_list = "\n".join(f"- {p}" for p in logs)

    prompt = f"""You are JARVIS doing your nightly reflection. Today is {local:%A, %B %-d, %Y}.
Turn what happened into durable memory. Be a careful editor: precise, brief, never inventing.

Read first: {BRAIN}/SOUL.md, {BRAIN}/USER.md, {BRAIN}/MEMORY.md, {BRAIN}/wiki/index.md, and these
daily logs (written since the last reflection on {since}):
{log_list}

Then update, in this order:
1. MEMORY.md, the headline layer every session loads. Keep its sections and its tag rules:
   - [S] state facts: overwrite the old line when the truth changed (the server went live, a plan
     changed). Remove lines that are no longer true.
   - [E] events: append dated one-liners for decisions and milestones that will matter in a month.
     Drop or merge [E] lines older than about 60 days unless they still explain a current choice.
   - Keep it under 150 lines. Detail belongs in wiki pages; MEMORY.md points to them.
2. USER.md: only facts about Terry himself that he stated or clearly showed (how he works,
   preferences, constraints, goals). Add the date. Don't restate what's already there.
3. wiki/: update or create pages under wiki/projects/ for the projects worked on (current state,
   what's next, key dated events), and wiki/tools/ when we learned something durable about a
   tool. Update wiki/index.md and append to wiki/log.md. Never edit wiki/CURATION.md.
4. SOUL.md: never edit it. If the logs show Terry correcting how JARVIS talks or behaves, append a
   dated proposal to proposals/soul.md (create it if missing): the proposed change and the
   evidence. Terry decides.
Never touch daily/ (append-only), scripts/, or anything else. No secrets in any file.

When done, print exactly one final line and nothing after it:
REFLECTED {{"memory": ["<one line per MEMORY.md change>"], "user": ["..."], "wiki": ["<page: what>"], "soul_proposals": ["..."], "summary": "<one sentence: what tonight's reflection captured>"}}"""

    result = guarded_edit(JOB, prompt, marker="REFLECTED", timeout=2400,
                          commit="--no-commit" not in argv,
                          allowed=lambda p: p.startswith(ALLOWED) and p != "wiki/CURATION.md",
                          commit_msg=f"reflect: {today}")

    # 3. Tell the brief: a line on what was remembered, and any SOUL proposal (needs Terry).
    queue = read_state("brief-queue", [])
    if result.get("summary"):
        queue.append(f"Overnight memory: {result['summary']}")
    for p in result.get("soul_proposals") or []:
        queue.append(f"Needs Terry: proposed SOUL.md change (not applied): {p}")
    if result.get("error"):
        queue.append(f"Nightly reflection had a problem: {result['error']}")
    write_state("brief-queue", queue)
    write_state(JOB, {"last_run": today, "logs": [p.name for p in logs],
                      **{k: result.get(k) for k in ("memory", "user", "wiki", "soul_proposals",
                                                     "summary", "kept", "reverted", "error")}})
    log(JOB, f"{today}: {len(result.get('kept', []))} files changed ({', '.join(result.get('kept', [])) or 'none'})"
             + (f"; ERROR {result['error']}" if result.get("error") else ""))
    return 1 if result.get("error") else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
