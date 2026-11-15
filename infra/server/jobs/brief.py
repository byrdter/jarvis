#!/usr/bin/env python3
"""Morning brief: once a day at BRIEF_HOUR local (10:00 by default, right after Terry's
exercise). Gathers overnight changes with plain code, then asks Claude to write the brief.
The timer fires every 15 min; this script sends once per local day, between BRIEF_HOUR and
BRIEF_HOUR+2 (so a reboot at 10:05 still gets the brief out)."""
import subprocess
import sys
from datetime import datetime, timedelta, timezone

from jarvis_jobs import (BRAIN, CFG, ENGINE, ask_claude, github_activity, log, now_local,
                         read_state, tg_send, write_state)

JOB = "brief"


def git_log(repo, since: str) -> str:
    subprocess.run(["git", "-C", str(repo), "fetch", "-q"], capture_output=True, timeout=60)
    r = subprocess.run(["git", "-C", str(repo), "log", "origin/HEAD", f"--since={since}",
                        "--format=%h %an: %s"], capture_output=True, text=True, timeout=30)
    return r.stdout.strip() or "(no commits)"


def main(force: bool) -> int:
    local = now_local()
    today = local.date().isoformat()
    state = read_state(JOB, {})
    hour = int(CFG["BRIEF_HOUR"])
    if not force and (state.get("last_sent") == today or not (hour <= local.hour < hour + 2)):
        return 0

    # "Overnight" = since the end of yesterday's active hours.
    since_local = (local - timedelta(days=1)).replace(hour=int(CFG["ACTIVE_END"]), minute=0,
                                                       second=0, microsecond=0)
    since = since_local.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
    try:
        gh = github_activity(since)
    except Exception as e:
        gh = [f"(GitHub check failed: {e})"]
    queued = read_state("brief-queue", [])
    daily = sorted((BRAIN / "daily").glob("*.md"))[-2:]
    daily_txt = "\n\n".join(f"## {p.name}\n" + "\n".join(p.read_text().splitlines()[-40:])
                            for p in daily)

    prompt = f"""You are JARVIS writing Terry's morning brief for {local:%A, %B %-d}. It goes to
Telegram as plain text (no Markdown tables, no headers with #; short lines, a few emoji at most).
Follow the Daily section of HEARTBEAT.md in your brain. Structure:
1. Overnight: what shipped or changed (from the data below). Say "quiet night" if nothing did.
2. Needs you: anything waiting on Terry (PRs, issues, queued items). Skip if none.
3. Top 3 for today: your recommendation, grounded in the current focus in MEMORY.md and the
   recent daily logs. One line each, with the why.
Calendar: Terry doesn't use Google Calendar yet, so leave it out.
Keep it under 1,200 characters. American English, friend's voice, no filler.

DATA
Engine repo commits (jarvis) since {since}Z:
{git_log(ENGINE, since)}

Brain repo commits (jarvis-brain) since {since}Z:
{git_log(BRAIN, since)}

GitHub issues/PRs from others on Terry's public repos:
{chr(10).join(gh) or "(none)"}

Items the heartbeat queued for this brief:
{chr(10).join(queued) or "(none)"}

Recent daily logs (tails):
{daily_txt}
"""
    text = ask_claude(prompt)
    tg_send(text)
    write_state(JOB, {"last_sent": today})
    write_state("brief-queue", [])
    log(JOB, f"sent brief for {today} ({len(text)} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(main(force="--force" in sys.argv))
