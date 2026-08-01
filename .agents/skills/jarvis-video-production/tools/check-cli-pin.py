#!/usr/bin/env python3
"""
CLI pin gate — assert the installed hyperframes matches the pin in CLAUDE.md.

    python3 check-cli-pin.py              # assert; exit 1 on mismatch
    python3 check-cli-pin.py --stamp DIR  # ...and record the version into DIR/.cli-version
    python3 check-cli-pin.py --verify DIR # ...and FAIL if DIR/.cli-version disagrees

WHY THIS EXISTS
    The pin was wrong in three files for a week (0.7.72 in the docs, 0.7.84+ installed).
    That is the exact failure CLAUDE.md §6 warns about — a written pin is a claim, not a
    check — and it had already caused one mixed-version master (messi-ai-investor, scene
    06 on 0.7.72 against eleven scenes of 0.7.42 output).

    Worse: THE GLOBAL BINARY SELF-UPDATES. On 2026-08-01 it reported 0.7.84 at the start
    of a component build and 0.7.87 an hour later, unprompted. So the pin cannot be
    maintained by discipline alone — nobody chose that upgrade and nobody would have
    noticed it. Hence a script.

USE IT TWICE PER BATCH
    1. `--stamp <batch-dir>` at batch start, before the first render.
    2. `--verify <batch-dir>` before assemble-master.py runs.
    If step 2 fails, the binary moved mid-batch: scenes are mixed-version and the batch
    must be re-rendered (PIPELINE.md Step 5).

EXIT CODES  0 ok   1 mismatch   2 could not determine
"""
import os, re, subprocess, sys, argparse

# tools -> jarvis-video-production -> skills -> .agents -> repo root  (FOUR levels)
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
CLAUDE_MD = os.path.join(REPO, "CLAUDE.md")


def pinned():
    """The pin is declared in CLAUDE.md — one source of truth, not three."""
    try:
        txt = open(CLAUDE_MD, encoding="utf8").read()
    except OSError:
        return None
    m = re.search(r"PINNED CLI \(`hyperframes`,\s*global\s*\*\*([0-9]+\.[0-9]+\.[0-9]+)\*\*", txt)
    return m.group(1) if m else None


def installed():
    try:
        out = subprocess.run(["hyperframes", "--version"], capture_output=True,
                             text=True, timeout=120).stdout
    except (OSError, subprocess.SubprocessError):
        return None
    m = re.search(r"([0-9]+\.[0-9]+\.[0-9]+)", out)
    return m.group(1) if m else None


def main():
    ap = argparse.ArgumentParser(description="Assert hyperframes matches the CLAUDE.md pin")
    ap.add_argument("--stamp", metavar="DIR", help="write DIR/.cli-version at batch start")
    ap.add_argument("--verify", metavar="DIR", help="fail if DIR/.cli-version disagrees with installed")
    a = ap.parse_args()

    want, have = pinned(), installed()
    if not want:
        print("FAIL  could not read the pin from CLAUDE.md", file=sys.stderr); sys.exit(2)
    if not have:
        print("FAIL  `hyperframes --version` produced no version — is it installed?", file=sys.stderr)
        sys.exit(2)

    bad = (want != have)
    print(f"  pin (CLAUDE.md): {want}")
    print(f"  installed:       {have}   {'MISMATCH' if bad else 'ok'}")

    if bad:
        print(f"\nFAIL  the binary is not the pinned version.\n"
              f"  Either re-pin and RE-RENDER THE WHOLE BATCH (PIPELINE.md Step 5):\n"
              f"      update CLAUDE.md to {have}, then re-render every scene\n"
              f"  or pin the binary back:\n"
              f"      npm install -g hyperframes@{want}\n"
              f"  Do not render a batch across two versions.", file=sys.stderr)

    if a.stamp:
        os.makedirs(a.stamp, exist_ok=True)
        with open(os.path.join(a.stamp, ".cli-version"), "w", encoding="utf8") as f:
            f.write(have + "\n")
        print(f"  stamped {a.stamp}/.cli-version = {have}")

    if a.verify:
        p = os.path.join(a.verify, ".cli-version")
        try:
            was = open(p, encoding="utf8").read().strip()
        except OSError:
            print(f"\nFAIL  no {p} — batch was never stamped. Run --stamp before the first render.",
                  file=sys.stderr)
            sys.exit(1)
        if was != have:
            print(f"\nFAIL  the binary MOVED MID-BATCH: {was} at start, {have} now.\n"
                  f"  Scenes rendered before the move are {was} output and the rest are {have}.\n"
                  f"  Mixed-version scenes in one master are a silent-difference risk —\n"
                  f"  RE-RENDER THE WHOLE BATCH.", file=sys.stderr)
            sys.exit(1)
        print(f"  batch stamp:     {was}   ok — no mid-batch drift")

    sys.exit(1 if bad else 0)


main()
