#!/usr/bin/env python3
"""YouTube transcripts for the daily intake, made on the laptop.

Why the laptop: YouTube refuses cloud servers ("confirm you're not a bot") for captions AND audio,
but serves a home or hotel connection. So the server collects video titles; this job, run hourly by
launchd while the laptop is awake, finds YouTube items in the server inbox that have no transcript,
downloads their audio, transcribes it locally with whisper (free, private), and appends the text to
the item on the server. It also lists the item in the inbox's late.md, so the next curator run reads
it even though its day has already been curated.

Usage: yt-transcribe.py [--max N] [--dry-run]"""
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path

SERVER = "jarvis-server"
INBOX = ".local/share/jarvis/inbox"
WATCH = ".local/share/jarvis/watch"  # videos from channels Terry follows; transcribed so "keep N" has substance
MODEL = Path.home() / ".whisper-models/ggml-small.en.bin"
BIN = "/opt/homebrew/bin"
DAYS_BACK = 3          # only recent videos; older ones aren't news anymore
MAX_DEFAULT = 6        # per run, to stay well under YouTube's rate limits
MAX_MINUTES = 90       # skip very long videos (livestreams, 3-hour podcasts)
LOG = Path.home() / "Library/Logs/jarvis-yt-transcribe.log"


def log(msg: str) -> None:
    from datetime import datetime
    line = f"{datetime.now().isoformat(timespec='seconds')} {msg}"
    print(line)
    with LOG.open("a") as fh:
        fh.write(line + "\n")


def ssh(cmd: str, stdin: str | None = None, timeout: int = 60) -> str:
    r = subprocess.run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=15", SERVER, cmd],
                       input=stdin, capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0:
        raise RuntimeError(f"ssh failed: {r.stderr.strip()[:200]}")
    return r.stdout


def pending() -> list[tuple[str, str, int]]:
    """(server path from home, video url, minutes) for recent YouTube items with no transcript yet.
    Inbox items come first: the curator is waiting on them."""
    items = []
    for root in (INBOX, WATCH):
        out = ssh(f"cd {root} 2>/dev/null || exit 0; "
                  f"for d in $(ls -d 20??-??-?? 2>/dev/null | sort | tail -{DAYS_BACK}); do "
                  f"for f in $d/yt-*.md; do [ -f \"$f\" ] || continue; "
                  f"grep -q '^## Transcript' \"$f\" && continue; "
                  f"grep -q '^- transcript: skipped' \"$f\" && continue; "
                  f"echo \"$f|$(sed -n 's/^- url: //p' \"$f\" | head -1)|$(sed -n 's/^- notes: .*, \\([0-9]*\\) min,.*/\\1/p' \"$f\" | head -1)\"; "
                  f"done; done")
        for line in out.splitlines():
            path, url, mins = (line.split("|") + ["", ""])[:3]
            if url.startswith("https://www.youtube.com/watch"):
                items.append((f"{root}/{path}", url, int(mins) if mins.isdigit() else 0))
    return items


def minutes(url: str) -> int:
    """Video length, read on the laptop (the server is blocked from YouTube's watch pages)."""
    r = subprocess.run([f"{BIN}/yt-dlp", "-q", "--no-warnings", "--print", "duration", url],
                       check=True, capture_output=True, text=True, timeout=120)
    return int(float(r.stdout.strip() or 0)) // 60


def transcribe(url: str, work: Path) -> str:
    audio = work / "audio.%(ext)s"
    subprocess.run([f"{BIN}/yt-dlp", "-q", "--no-warnings", "-f", "bestaudio", "-x",
                    "--audio-format", "m4a", "-o", str(audio), url],
                   check=True, capture_output=True, text=True, timeout=900)
    src = next(work.glob("audio.*"))
    wav = work / "audio.wav"
    subprocess.run([f"{BIN}/ffmpeg", "-loglevel", "error", "-y", "-i", str(src), "-ar", "16000",
                    "-ac", "1", str(wav)], check=True, timeout=600)
    subprocess.run([f"{BIN}/whisper-cli", "-m", str(MODEL), "-f", str(wav), "-otxt", "-nt",
                    "-of", str(work / "t")], check=True, capture_output=True, timeout=3600)
    text = (work / "t.txt").read_text().strip()
    # whisper writes one short segment per line; join into readable paragraphs of ~8 lines
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    return "\n\n".join(" ".join(lines[i:i + 8]) for i in range(0, len(lines), 8))


def main(argv) -> int:
    dry = "--dry-run" in argv
    cap = int(argv[argv.index("--max") + 1]) if "--max" in argv else MAX_DEFAULT
    if not MODEL.exists():
        log(f"no whisper model at {MODEL}; nothing to do")
        return 1
    try:
        todo = pending()
    except Exception as e:  # server unreachable (offline, Tailscale down): try next hour
        log(f"skip run: {e}")
        return 0
    if not todo:
        return 0
    done = 0
    for path, url, mins in todo:
        if done >= cap:
            break
        q = shlex.quote(path)
        try:
            mins = mins or minutes(url)
        except subprocess.CalledProcessError as e:
            log(f"FAIL length check {url}: {(e.stderr or '')[-200:].strip()}")
            if "429" in (e.stderr or "") or "not a bot" in (e.stderr or ""):
                break
            continue
        if mins > MAX_MINUTES:
            if not dry:
                ssh(f"printf '%s\\n' '- transcript: skipped ({mins} min, over {MAX_MINUTES})' >> {q}")
            log(f"skipped {url} ({mins} min)")
            continue
        if dry:
            print(f"would transcribe {url} ({mins} min) -> {path}")
            done += 1
            continue
        with tempfile.TemporaryDirectory() as tmp:
            try:
                text = transcribe(url, Path(tmp))
            except subprocess.CalledProcessError as e:
                err = (e.stderr or "")[-300:] if isinstance(e.stderr, str) else ""
                log(f"FAIL {url}: {err.strip() or e}")
                if "429" in err or "not a bot" in err:
                    log("YouTube is rate-limiting this connection; stopping for this hour")
                    break
                continue
        # Inbox items go on late.md for the curator; watch items wait for Terry's "keep".
        late = (f" && echo {shlex.quote('- ' + path.removeprefix(INBOX + '/'))} >> {INBOX}/late.md"
                if path.startswith(INBOX + "/") else "")
        ssh(f"cat >> {q}{late}",
            stdin=f"\n## Transcript (whisper on the laptop)\n\n{text}\n", timeout=120)
        log(f"transcribed {url} ({mins} min, {len(text)} chars) -> {path}")
        done += 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
