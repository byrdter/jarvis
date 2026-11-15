"""Shared helpers for JARVIS's scheduled jobs on the server.

Timers fire on UTC; each job decides for itself whether it's time to act, using Terry's
local time zone (JARVIS_TZ in ~/.config/jarvis/jobs.env, default Europe/Madrid). Traveling
means changing that one line, not every timer.
"""
import json
import os
import subprocess
import sys
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

HOME = Path.home()
STATE = HOME / ".local/state/jarvis"
STATE.mkdir(parents=True, exist_ok=True)
TG_DIR = HOME / ".claude/channels/telegram"
BRAIN = Path(os.environ.get("JARVIS_BRAIN", HOME / "code/jarvis-brain"))
ENGINE = HOME / "code/jarvis"
CLAUDE = str(HOME / ".local/bin/claude")


def load_config() -> dict:
    cfg = {"JARVIS_TZ": "Europe/Madrid", "ACTIVE_START": "10", "ACTIVE_END": "19",
           "BRIEF_HOUR": "10", "PREFLIGHT_HOUR": "9", "GITHUB_USER": "byrdter"}
    f = HOME / ".config/jarvis/jobs.env"
    if f.exists():
        for line in f.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                cfg[k.strip()] = v.strip()
    return cfg


CFG = load_config()


def now_local() -> datetime:
    return datetime.now(ZoneInfo(CFG["JARVIS_TZ"]))


def log(job: str, msg: str) -> None:
    line = f"{datetime.now().isoformat(timespec='seconds')} [{job}] {msg}"
    print(line, file=sys.stderr)
    with open(STATE / "jobs.log", "a") as fh:
        fh.write(line + "\n")


def read_state(name: str, default=None):
    p = STATE / f"{name}.json"
    return json.loads(p.read_text()) if p.exists() else default


def write_state(name: str, value) -> None:
    (STATE / f"{name}.json").write_text(json.dumps(value, indent=2))


def tg_send(text: str) -> None:
    """Send a message to Terry through the bot API. Sending doesn't conflict with the chat poller."""
    token = ""
    for line in (TG_DIR / ".env").read_text().splitlines():
        if line.startswith("TELEGRAM_BOT_TOKEN="):
            token = line.split("=", 1)[1].strip()
    chat = json.loads((TG_DIR / "access.json").read_text())["allowFrom"][0]
    for i in range(0, len(text), 4000):
        data = urllib.parse.urlencode({"chat_id": chat, "text": text[i:i + 4000],
                                       "disable_web_page_preview": "true"}).encode()
        urllib.request.urlopen(f"https://api.telegram.org/bot{token}/sendMessage", data, timeout=30).read()


def ask_claude(prompt: str, timeout: int = 600) -> str:
    """Run Claude headless in the engine repo, so the brain loads via the SessionStart hook."""
    env = dict(os.environ, PATH=f"{HOME}/.local/bin:{HOME}/.bun/bin:{os.environ.get('PATH', '')}")
    # NEVER load the Telegram plugin here: a new plugin instance SIGTERMs the running poller
    # (bot.pid), which silently deafens the chat session. Learned 2026-11-15.
    no_tg = json.dumps({"enabledPlugins": {"telegram@claude-plugins-official": False}})
    r = subprocess.run([CLAUDE, "-p", prompt, "--settings", no_tg], cwd=ENGINE,
                       capture_output=True, text=True,
                       timeout=timeout, env=env)
    if r.returncode != 0:
        raise RuntimeError(f"claude -p failed ({r.returncode}): {r.stderr[-500:]}")
    return r.stdout.strip()


def github_token() -> str:
    """Terry's `gh auth login` token on the server, if signed in (sees private repos)."""
    try:
        r = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, timeout=15)
        return r.stdout.strip() if r.returncode == 0 else ""
    except (OSError, subprocess.TimeoutExpired):
        return ""


def github_activity(since_iso: str) -> list[str]:
    """Open issues/PRs on Terry's repos, updated since `since_iso`, by someone else.
    Private repos included when gh is signed in; otherwise public repos only."""
    user = CFG["GITHUB_USER"]
    q = f"user:{user} is:open updated:>{since_iso} -author:{user}"
    url = "https://api.github.com/search/issues?" + urllib.parse.urlencode({"q": q, "per_page": 20})
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "jarvis-heartbeat"}
    token = github_token()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        items = json.load(resp).get("items", [])
    out = []
    for it in items:
        kind = "PR" if "pull_request" in it else "Issue"
        repo = it["repository_url"].rsplit("/", 1)[-1]
        out.append(f"{kind} {repo}#{it['number']}: {it['title']} (by {it['user']['login']}, "
                   f"updated {it['updated_at']}) {it['html_url']}")
    return out
