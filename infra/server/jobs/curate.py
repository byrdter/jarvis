#!/usr/bin/env python3
"""Curate: read today's inbox and write what matters into the brain wiki, following
jarvis-brain/wiki/CURATION.md. Claude does the reading and writing (edit tools on the brain and
inbox only); this script guards the result and commits it.

Guards: anything changed outside wiki/ (or CURATION.md itself) is reverted, so the curator can never
touch SOUL/USER/MEMORY or the daily logs. The change list feeds the morning brief's "Added to the
brain" section.

Usage: curate.py [--day YYYY-MM-DD] [--no-commit]"""
import sys

from brain_edit import guarded_edit
from jarvis_jobs import BRAIN, INBOX, log, now_local, read_state, write_state

JOB = "curate"


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
    # Documents Terry dropped in ~/JARVIS-Library (see infra/laptop/ingest-library.py).
    library_list = BRAIN / "raw/sources/PENDING.md"
    library = [l[2:].strip() for l in library_list.read_text().splitlines()
               if l.startswith("- ")] if library_list.exists() else []
    if not has_today and not late and not library:
        log(JOB, f"nothing in the inbox for {day}")
        write_state(JOB, {"last_run": day, "changes": []})
        return 0

    rc = curate(argv, day, day_dir, index, late, library)
    if rc == 0:
        late_claim.unlink(missing_ok=True)
        if library:  # done with these; anything the laptop added meanwhile stays for next time
            rest = [l for l in library_list.read_text().splitlines()
                    if not (l.startswith("- ") and l[2:].strip() in library)]
            library_list.write_text("\n".join(rest).rstrip() + "\n")
    return rc


def curate(argv, day, day_dir, index, late, library) -> int:
    late_txt = ("\n   Also read these YouTube items from earlier days: their transcripts arrived after that day "
                "was curated. Judge them on the transcript (an earlier run may have used the "
                "description already; add only what's new):\n" +
                "\n".join(f"   - {INBOX / l}" for l in late)) if late else ""
    lib_txt = ("\n\nLIBRARY DOCUMENTS. Terry added these to his library (guides, prompt packs, courses from "
               "people he learns from). They are not news, so the focus rule doesn't apply the same way: "
               "anything about building with AI belongs in the wiki. For each one, read it and (a) create or "
               "update the author's page in wiki/people/ (who they are, a table row per document: what it "
               "covers, link to the raw file, and what it means for us), and (b) update tools/ or concepts/ "
               "pages with durable how-to knowledge, citing the raw file. Library documents don't count "
               "toward the 8-change limit. See wiki/people/zubair-trabzada.md for the page shape.\n" +
               "\n".join(f"   - {BRAIN / l}" for l in library)) if library else ""
    prompt = f"""You are JARVIS's curator. Job: move what matters from today's inbox into the wiki.

1. Read {BRAIN}/wiki/CURATION.md first. It is the rule set; its Feedback section wins over the rules.
2. Read {BRAIN}/wiki/index.md to know what pages exist.
3. Read the inbox index {index} (if it exists). Each line is one collected item; the item files
   are in {day_dir}. Some YouTube items there end with a "## Transcript" section: use it.{late_txt}
4. Decide which items pass the rules. Open only those item files (and the existing wiki pages you
   will change). If an item's summary is too thin to judge, skip it rather than guess.
5. Write the changes into {BRAIN}/wiki/ exactly as CURATION.md says (update before create, dated
   and sourced facts, replace superseded facts, index.md and log.md updated, at most 8 page changes).
   Edit only files under {BRAIN}/wiki/, never CURATION.md. American English.{lib_txt}

When done, print exactly one final line and nothing after it:
CURATED {{"changes": [{{"page": "<slug>", "action": "created|updated", "what": "<one short line: the fact, in plain words>", "source": "<url>"}}], "considered": <items read>, "skipped_reason": "<one line on what you passed over and why>"}}
If nothing qualified, print CURATED with an empty changes list."""

    result = guarded_edit(
        JOB, prompt, marker="CURATED", extra_dirs=[INBOX], commit="--no-commit" not in argv,
        allowed=lambda p: p.startswith("wiki/") and p != "wiki/CURATION.md",
        commit_msg=f"curate: {day}, wiki changes")
    ours, reverted = result["kept"], result["reverted"]

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
    return 1 if result.get("error") else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
