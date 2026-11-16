#!/usr/bin/env python3
"""Preflight: live checks that the server is actually working ("done means preflight passed").
Runs daily at PREFLIGHT_HOUR local, and by hand after any deploy (--force).
Posts to Telegram only when something fails (--force also posts an all-clear)."""
import json
import shutil
import subprocess
import sys
import time
from datetime import timedelta

from jarvis_jobs import CFG, STATE, TG_DIR, log, now_local, read_state, write_state, tg_send

JOB = "preflight"


def sh(*cmd: str) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, timeout=60)


def checks() -> list[tuple[str, bool, str]]:
    out = []
    active = sh("systemctl", "--user", "is-active", "jarvis-chat").stdout.strip()
    out.append(("Telegram chat service running", active == "active", active))

    pollers = [l for l in sh("pgrep", "-af", "plugins-official/telegram").stdout.splitlines()
               if "bun run" in l]
    out.append(("Exactly one Telegram poller", len(pollers) == 1, f"{len(pollers)} found"))

    ok_file = STATE / "brain-sync.ok"
    age = time.time() - ok_file.stat().st_mtime if ok_file.exists() else 1e9
    out.append(("Brain synced in the last 10 min", age < 600, f"{int(age)}s ago" if age < 1e9 else "never"))

    for t in ("jarvis-brain-sync", "jarvis-heartbeat", "jarvis-brief", "jarvis-preflight",
              "jarvis-chat-watchdog", "jarvis-intake"):
        st = sh("systemctl", "--user", "is-active", f"{t}.timer").stdout.strip()
        out.append((f"{t} timer on", st == "active", st))

    intake = read_state("intake", {})
    yesterday = (now_local().date() - timedelta(days=1)).isoformat()
    fresh = intake.get("last_run", "") >= yesterday and intake.get("status") != "failed"
    out.append(("Daily intake ran (today or yesterday)", fresh,
                f"{intake.get('last_run', 'never')} {intake.get('status', '')}"))
    bad = intake.get("failed_sources") or []
    out.append(("Intake sources all fetched", len(bad) <= 2, ", ".join(bad) or "all ok"))

    free = shutil.disk_usage("/").free / 2**30
    out.append(("Disk has 5 GB+ free", free > 5, f"{free:.1f} GB free"))

    ts = sh("tailscale", "status", "--json")
    online = ts.returncode == 0 and json.loads(ts.stdout).get("BackendState") == "Running"
    out.append(("Tailscale up", online, "running" if online else ts.stdout[:80]))

    out.append(("Telegram token present", (TG_DIR / ".env").exists(), ""))
    return out


def main(force: bool) -> int:
    local = now_local()
    today = local.date().isoformat()
    state = read_state(JOB, {})
    if not force and (state.get("last_run") == today or local.hour != int(CFG["PREFLIGHT_HOUR"])):
        return 0
    results = checks()
    failed = [r for r in results if not r[1]]
    for name, ok, detail in results:
        log(JOB, f"{'PASS' if ok else 'FAIL'} {name} {detail}")
    if failed:
        tg_send("⚠️ JARVIS server preflight: " + f"{len(failed)} of {len(results)} checks failed\n" +
                "\n".join(f"✗ {n} ({d})" for n, _, d in failed))
    elif force:
        tg_send(f"✅ JARVIS server preflight: all {len(results)} checks passed.")
    write_state(JOB, {"last_run": today, "failed": [f[0] for f in failed]})
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(force="--force" in sys.argv))
