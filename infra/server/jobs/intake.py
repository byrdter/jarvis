#!/usr/bin/env python3
"""Daily intake: collect, then curate, once per local day at COLLECT_HOUR (07:00 by default),
so the curated additions are ready for the 10:00 brief. The timer fires hourly; this decides.
--force runs now regardless of the hour or whether today already ran."""
import sys

import collect
import curate
from jarvis_jobs import CFG, log, now_local, read_state, tg_send, write_state

JOB = "intake"


def main(force: bool) -> int:
    local = now_local()
    today = local.date().isoformat()
    state = read_state(JOB, {})
    hour = int(CFG["COLLECT_HOUR"])
    if not force and (state.get("last_run") == today or local.hour < hour):
        return 0
    write_state(JOB, {"last_run": today, "status": "running"})
    rc_collect = collect.main([])
    try:
        rc_curate = curate.main([])
    except Exception as e:
        log(JOB, f"curate crashed: {type(e).__name__}: {e}")
        rc_curate = 2
    failed = read_state("collect", {}).get("failed", [])
    status = "ok" if rc_collect == 0 and rc_curate == 0 else "failed"
    write_state(JOB, {"last_run": today, "status": status, "failed_sources": failed})
    if rc_curate != 0:
        tg_send(f"⚠️ JARVIS intake: the curator failed today ({today}). Check jobs.log on the server.")
    return 0 if status == "ok" else 1


if __name__ == "__main__":
    sys.exit(main(force="--force" in sys.argv))
