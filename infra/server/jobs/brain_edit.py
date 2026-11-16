"""Let Claude edit the brain repo, then check its work before anything is committed.

Shared by curate.py (wiki pages) and reflect.py (MEMORY.md, USER.md, wiki). Each caller says which
paths the model may change; everything else it touched is reverted. SOUL.md and daily/ are never
writable here, whatever the caller allows: SOUL.md is Terry's (reflection may only *propose*
changes, in proposals/), and daily logs are append-only records.

brain-sync is paused while the model works, so nothing it writes reaches GitHub before the guard
has checked it.
"""
import json
import re
import subprocess

from jarvis_jobs import BRAIN, ask_claude, log

NEVER = ("SOUL.md", "daily/", "scripts/", ".gitignore", ".gitattributes")


def git(*args) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(BRAIN), *args], capture_output=True, text=True, timeout=120)


def changed_paths() -> set[str]:
    out = git("status", "--porcelain", "--untracked-files=all").stdout.splitlines()
    return {l[3:].split(" -> ")[-1].strip('"') for l in out if l.strip()}


def guarded_edit(job: str, prompt: str, allowed, marker: str, extra_dirs=(), commit_msg="",
                 timeout: int = 1800, commit: bool = True) -> dict:
    """Run `prompt` with edit tools on the brain. `allowed(path) -> bool` decides which changed
    paths survive. The model must end its reply with a line `<marker> {json}`; that JSON comes back
    with `kept`, `reverted` and `error` added."""
    subprocess.run(["systemctl", "--user", "stop", "jarvis-brain-sync.timer"], capture_output=True)
    try:
        git("pull", "-q", "--no-rebase", "--no-edit")
        before = changed_paths()  # pre-existing local edits are not ours to judge or commit
        args = ["--permission-mode", "acceptEdits", "--add-dir", str(BRAIN)]
        for d in extra_dirs:
            args += ["--add-dir", str(d)]
        out = ask_claude(prompt, timeout=timeout,
                         extra=args + ["--allowedTools", "Read", "Edit", "Write", "Glob", "Grep"])
        m = re.search(rf"^{marker} (\{{.*\}})\s*$", out, re.M)
        try:
            result = json.loads(m.group(1)) if m else {"error": f"no {marker} line", "tail": out[-400:]}
        except ValueError as e:
            result = {"error": f"bad {marker} JSON: {e}", "tail": out[-400:]}

        reverted = []
        for p in sorted(changed_paths() - before):
            if p.startswith(NEVER) or not allowed(p):
                if git("ls-files", "--error-unmatch", p).returncode == 0:
                    git("checkout", "--", p)
                else:
                    (BRAIN / p).unlink(missing_ok=True)
                reverted.append(p)
        if reverted:
            log(job, f"GUARD reverted out-of-bounds changes: {', '.join(reverted)}")

        kept = sorted(changed_paths() - before)
        if kept and commit:
            # Same lock as brain-sync.sh, so the two never commit at once.
            subprocess.run(["flock", "-w", "120", str(BRAIN / ".sync.lock"), "bash", "-c",
                            f'cd "{BRAIN}" && git add -- {" ".join(map(repr, kept))} && '
                            f'git commit -q -m {commit_msg!r} && '
                            f'(git pull -q --no-rebase --no-edit && git push -q)'],
                           capture_output=True, text=True, timeout=300)
        result.update(kept=kept, reverted=reverted)
        result.setdefault("error", None)
        return result
    finally:
        subprocess.run(["systemctl", "--user", "start", "jarvis-brain-sync.timer"], capture_output=True)
