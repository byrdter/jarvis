#!/usr/bin/env python3
"""Curate: read today's inbox and write what matters into the brain wiki, following
jarvis-brain/wiki/CURATION.md. Claude does the reading and writing (edit tools on the brain and
inbox only); this script guards the result and commits it.

Guards: anything changed outside wiki/ (or CURATION.md itself) is reverted, so the curator can never
touch SOUL/USER/MEMORY or the daily logs. The change list feeds the morning brief's "Added to the
brain" section.

Usage: curate.py [--day YYYY-MM-DD] [--no-commit]"""
import json
import re
import subprocess
import sys

from jarvis_jobs import BRAIN, INBOX, ask_claude, log, now_local, read_state, write_state

JOB = "curate"


def git(*args, check=False) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(BRAIN), *args], capture_output=True, text=True,
                          timeout=120, check=check)


def changed_paths() -> list[str]:
    out = git("status", "--porcelain", "--untracked-files=all").stdout.splitlines()
    return [l[3:].split(" -> ")[-1].strip('"') for l in out if l.strip()]


def main(argv) -> int:
    day = argv[argv.index("--day") + 1] if "--day" in argv else now_local().date().isoformat()
    day_dir = INBOX / day
    index = day_dir / "INDEX.md"
    # Transcripts the laptop added after their day was curated (see infra/laptop/yt-transcribe.py).
    # Claimed by renaming, so lines the laptop appends during this run wait for the next one.
    late_file, late_claim = INBOX / "late.md", INBOX / "late.processing.md"
    if late_file.exists() and not late_claim.exists():
        late_file.rename(late_claim)
    late = [l[2:].strip() for l in late_claim.read_text().splitlines()
            if l.startswith("- ")] if late_claim.exists() else []
    late = [l for l in dict.fromkeys(late) if not l.startswith(day + "/")]  # today's are in the index
    has_today = index.exists() and index.read_text().count("\n- ") > 0
    if not has_today and not late:
        log(JOB, f"nothing in the inbox for {day}")
        write_state(JOB, {"last_run": day, "changes": []})
        return 0

    # Pause brain-sync while the curator works, so nothing it writes is committed before the guard
    # below has checked it. Restarted in finally; preflight flags the timer if it ever stays off.
    subprocess.run(["systemctl", "--user", "stop", "jarvis-brain-sync.timer"], capture_output=True)
    try:
        rc = curate(argv, day, day_dir, index, late)
        if rc == 0:
            late_claim.unlink(missing_ok=True)
        return rc
    finally:
        subprocess.run(["systemctl", "--user", "start", "jarvis-brain-sync.timer"], capture_output=True)


def curate(argv, day, day_dir, index, late) -> int:
    git("pull", "-q", "--no-rebase", "--no-edit")
    before = set(changed_paths())  # pre-existing local edits are not ours to judge or commit

    late_txt = ("\n   Also read these YouTube items from earlier days: their transcripts arrived after that day "
                "was curated. Judge them on the transcript (an earlier run may have used the "
                "description already; add only what's new):\n" +
                "\n".join(f"   - {INBOX / l}" for l in late)) if late else ""
    prompt = f"""You are JARVIS's curator. Job: move what matters from today's inbox into the wiki.

1. Read {BRAIN}/wiki/CURATION.md first. It is the rule set; its Feedback section wins over the rules.
2. Read {BRAIN}/wiki/index.md to know what pages exist.
3. Read the inbox index {index} (if it exists). Each line is one collected item; the item files
   are in {day_dir}. Some YouTube items there end with a "## Transcript" section: use it.{late_txt}
4. Decide which items pass the rules. Open only those item files (and the existing wiki pages you
   will change). If an item's summary is too thin to judge, skip it rather than guess.
5. Write the changes into {BRAIN}/wiki/ exactly as CURATION.md says (update before create, dated
   and sourced facts, replace superseded facts, index.md and log.md updated, at most 8 page changes).
   Edit only files under {BRAIN}/wiki/, never CURATION.md. American English.

When done, print exactly one final line and nothing after it:
CURATED {{"changes": [{{"page": "<slug>", "action": "created|updated", "what": "<one short line: the fact, in plain words>", "source": "<url>"}}], "considered": <items read>, "skipped_reason": "<one line on what you passed over and why>"}}
If nothing qualified, print CURATED with an empty changes list."""

    out = ask_claude(prompt, timeout=1800, extra=[
        "--permission-mode", "acceptEdits",
        "--add-dir", str(BRAIN), "--add-dir", str(INBOX),
        "--allowedTools", "Read", "Edit", "Write", "Glob", "Grep",
    ])
    m = re.search(r"^CURATED (\{.*\})\s*$", out, re.M)
    result = json.loads(m.group(1)) if m else {"changes": [], "error": "no CURATED line",
                                               "tail": out[-400:]}

    # Guard: revert anything the curator changed outside wiki/, and CURATION.md itself.
    reverted = []
    for p in set(changed_paths()) - before:
        if not p.startswith("wiki/") or p == "wiki/CURATION.md":
            tracked = git("ls-files", "--error-unmatch", p).returncode == 0
            if tracked:
                git("checkout", "--", p)
            else:
                (BRAIN / p).unlink(missing_ok=True)
            reverted.append(p)
    if reverted:
        log(JOB, f"GUARD reverted out-of-bounds changes: {', '.join(reverted)}")

    ours = sorted(p for p in set(changed_paths()) - before if p.startswith("wiki/"))
    if ours and "--no-commit" not in argv:
        n = len(result.get("changes", []))
        # Same lock as brain-sync.sh, so the two never commit at once.
        subprocess.run(["flock", "-w", "120", str(BRAIN / ".sync.lock"), "bash", "-c",
                        f'cd "{BRAIN}" && git add -- {" ".join(map(repr, ours))} && '
                        f'git commit -q -m "curate: {day}, {n} wiki changes" && '
                        f'(git pull -q --no-rebase --no-edit && git push -q)'],
                       capture_output=True, text=True, timeout=300)

    # Queue for the brief (accumulates until the brief sends and clears it).
    pending = read_state("brain-additions", [])
    pending += [dict(c, day=day) for c in result.get("changes", [])]
    write_state("brain-additions", pending)
    write_state(JOB, {"last_run": day, "changes": result.get("changes", []),
                      "considered": result.get("considered"), "skipped_reason": result.get("skipped_reason"),
                      "error": result.get("error"),
                      "reverted": reverted})
    log(JOB, f"{day}: {len(result.get('changes', []))} wiki changes from "
             f"{result.get('considered', '?')} items read; files: {', '.join(ours) or 'none'}"
             + (f"; ERROR {result['error']}" if result.get("error") else ""))
    return 0 if m else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
