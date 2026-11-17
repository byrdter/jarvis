#!/usr/bin/env python3
"""Heartbeat: every 30 min in Terry's active hours, gather what changed (GitHub with plain code;
new email and upcoming meetings with a read-only Claude check), and only if something did, ask Claude (with HEARTBEAT.md) whether it's worth a ping now.
Anything not urgent is queued for the morning brief. Silent when nothing's new."""
import json
import sys
from datetime import datetime, timedelta, timezone

from jarvis_jobs import (BRAIN, CFG, ask_claude, github_activity, log, mail_and_calendar,
                         now_local, read_state, tg_send, write_state)

JOB = "heartbeat"


def main(force: bool) -> int:
    local = now_local()
    if not force and not (int(CFG["ACTIVE_START"]) <= local.hour < int(CFG["ACTIVE_END"])):
        return 0  # outside active hours: silent

    state = read_state(JOB, {})
    since = state.get("last_run") or (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
    started = datetime.now(timezone.utc).isoformat(timespec="seconds")
    since_q = since[:19] + "Z" if not since.endswith("Z") else since

    changes: list[str] = []
    try:
        changes += github_activity(since_q[:19])
    except Exception as e:  # network hiccup: note it, don't wake the model for it
        log(JOB, f"github gather failed: {e}")
    try:
        changes += mail_and_calendar(datetime.fromisoformat(since.replace("Z", "+00:00")))
    except Exception as e:
        log(JOB, f"mail/calendar gather failed: {str(e)[:300]}")
        today = local.date().isoformat()
        if state.get("mail_error_day") != today:  # tell Terry once a day, via the brief
            state["mail_error_day"] = today
            q = read_state("brief-queue", [])
            write_state("brief-queue", q + [f"Email/calendar check failed ({str(e)[:120]}). If it says "
                                            "permissions, reconnect the connector in claude.ai and Select all."])
    seen = set(state.get("seen", []))
    key = lambda c: c.split(" | ", 1)[0]  # mail:/cal: items de-dupe on their id, the rest on the text
    new = [c for c in changes if key(c) not in seen]

    if not new:
        write_state(JOB, {**state, "last_run": started})
        log(JOB, "nothing new")
        return 0

    rules = (BRAIN / "HEARTBEAT.md").read_text()
    prompt = (
        "You are JARVIS running your scheduled heartbeat. Rules:\n\n" + rules +
        "\n\nThese things changed since the last check:\n- " + "\n- ".join(new) +
        "\n\nDecide per the 'When to notify' rules. Reply with ONLY a JSON object, no code fence: "
        '{"notify_now": "<short Telegram message to Terry, or empty string>", '
        '"for_brief": ["<one line per item to batch into the morning brief>"]}. '
        "American English, friend's voice, plain words."
    )
    raw = ask_claude(prompt)
    try:
        decision = json.loads(raw[raw.index("{"): raw.rindex("}") + 1])
    except ValueError:
        decision = {"notify_now": "", "for_brief": new}
        log(JOB, f"unparseable model reply, queued raw items: {raw[:200]}")

    if decision.get("notify_now"):
        tg_send(decision["notify_now"])
        log(JOB, "sent notification")
    queue = read_state("brief-queue", [])
    queue += decision.get("for_brief", [])
    write_state("brief-queue", queue)
    write_state(JOB, {**state, "last_run": started, "seen": (list(seen) + [key(c) for c in new])[-400:]})
    log(JOB, f"{len(new)} new; queued {len(decision.get('for_brief', []))} for brief")
    return 0


if __name__ == "__main__":
    sys.exit(main(force="--force" in sys.argv))
