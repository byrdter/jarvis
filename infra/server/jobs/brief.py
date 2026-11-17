#!/usr/bin/env python3
"""Morning brief: once a day at BRIEF_HOUR local (10:00 by default, right after Terry's
exercise). Gathers overnight changes with plain code, then asks Claude to write the brief.
The timer fires every 15 min; this script sends once per local day, between BRIEF_HOUR and
BRIEF_HOUR+2 (so a reboot at 10:05 still gets the brief out)."""
import subprocess
import sys
from datetime import datetime, timedelta, timezone

from jarvis_jobs import (BRAIN, CFG, ENGINE, GOOGLE_READ, ask_claude, github_activity, log,
                         now_local, read_state, tg_send, write_state)

JOB = "brief"


def git_log(repo, since: str) -> str:
    subprocess.run(["git", "-C", str(repo), "fetch", "-q"], capture_output=True, timeout=60)
    r = subprocess.run(["git", "-C", str(repo), "log", "origin/HEAD", f"--since={since}",
                        "--format=%h %an: %s"], capture_output=True, text=True, timeout=30)
    return r.stdout.strip() or "(no commits)"


def send_watch_list() -> None:
    """New videos from the channels Terry follows, as a second message after the brief."""
    queue = read_state("watch-new", [])
    if not queue:
        return
    lines = [f"{v['id']} · {v['channel']}: {v['title']}\n{v['url']}" for v in queue]
    tg_send("📺 New from your channels\n\n" + "\n\n".join(lines) +
            "\n\nReply 'keep 12' (any number above) to save one to the brain. The rest clear out in 7 days.")
    write_state("watch-new", [])


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
    additions = read_state("brain-additions", [])
    added_txt = "\n".join(f"- {a.get('action', 'updated')} [[{a.get('page')}]]: {a.get('what')} ({a.get('source', '')})"
                           for a in additions) or "(nothing added)"
    daily = sorted((BRAIN / "daily").glob("*.md"))[-2:]
    daily_txt = "\n\n".join(f"## {p.name}\n" + "\n".join(p.read_text().splitlines()[-40:])
                            for p in daily)

    prompt = f"""You are JARVIS writing Terry's morning brief for {local:%A, %B %-d}. It goes to
Telegram as plain text (no Markdown tables, no headers with #; short lines, a few emoji at most).
Follow the Daily section of HEARTBEAT.md in your brain. Structure:
1. Today: Terry's meetings today (Calendar list_events, primary calendar, today in
   {CFG["JARVIS_TZ"]}, times in his local time), then email that needs him (Gmail search_threads,
   query: in:inbox after:{int(since_local.timestamp())} -category:promotions -category:social).
   Only mail a person wrote or that needs action; one line each: who, what, what he should do.
   Skip newsletters, marketing, receipts. Say "no meetings, inbox clear" if both are empty.
   Read only: never draft, send or change anything. If a tool fails, say so in one line.
2. Overnight: what shipped or changed (from the data below). Say "quiet night" if nothing did.
3. Needs you: anything else waiting on Terry (PRs, issues, queued items). Skip if none.
4. Top 3 for today: your recommendation, grounded in the current focus in MEMORY.md and the
   recent daily logs. One line each, with the why.
5. Added to the brain: the wiki additions below, 3 to 5 short lines, most useful first, each
   with its page name. End with: "Reply 'drop that' or 'more like this' to steer." Skip the
   section if nothing was added.
Keep it under 2,000 characters. American English, friend's voice, no filler.

DATA
Engine repo commits (jarvis) since {since}Z:
{git_log(ENGINE, since)}

Brain repo commits (jarvis-brain) since {since}Z:
{git_log(BRAIN, since)}

GitHub issues/PRs from others on Terry's public repos:
{chr(10).join(gh) or "(none)"}

Items the heartbeat queued for this brief:
{chr(10).join(queued) or "(none)"}

Wiki additions from the daily intake (collected and curated since the last brief):
{added_txt}

Recent daily logs (tails):
{daily_txt}
"""
    text = ask_claude(prompt, extra=["--allowedTools", GOOGLE_READ])
    tg_send(text)
    send_watch_list()
    write_state(JOB, {"last_sent": today})
    write_state("brief-queue", [])
    write_state("brain-additions", [])
    log(JOB, f"sent brief for {today} ({len(text)} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(main(force="--force" in sys.argv))
