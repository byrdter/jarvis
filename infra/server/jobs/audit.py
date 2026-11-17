#!/usr/bin/env python3
"""Weekly brain audit: a health score for jarvis-brain and a numbered list of proposed fixes.

Runs once a week (AUDIT_WEEKDAY, 0=Monday, default 6=Sunday; at AUDIT_HOUR local, default 4, after
the nightly reflection). Two passes:
  1. Plain code measures what can be measured: broken [[links]], wiki pages missing from the index,
     index lines with no page, pages without a summary line, dated facts older than STALE_DAYS on
     fast-moving pages (models/, tools/), MEMORY.md over its line limit, old [E] events.
  2. Claude reads the brain (read-only tools) for what code can't judge: contradictions between
     pages, facts that look outdated, duplicate pages.
The report goes to audits/YYYY-MM-DD.md in the brain; the brief gets one line. Nothing in the brain
changes until Terry replies "fix the audit" (or "fix 1, 3"); see CLAUDE.md.

Usage: audit.py [--force] [--no-commit]   (JARVIS_DRY=1 prints the report and touches nothing)"""
import json
import re
import subprocess
import sys
from datetime import date, timedelta

from jarvis_jobs import BRAIN, CFG, DRY, ask_claude, log, now_local, read_state, write_state

JOB = "audit"
STALE_DAYS = 90
FAST = ("models/", "tools/")  # pages whose facts go out of date quickly
MEMORY_LIMIT = 150
EVENT_DAYS = 60
LINK = re.compile(r"\[\[([a-z0-9][a-z0-9-]*)\]\]")
AS_OF = re.compile(r"as of (\d{4}-\d{2}-\d{2})")
EVENT = re.compile(r"^- \[E\] (\d{4}-\d{2}-\d{2})")
WEIGHTS = {"broken_link": 2, "not_in_index": 2, "index_no_page": 2, "no_summary": 1,
           "stale_fact": 1, "memory_long": 5, "old_events": 2,
           "contradiction": 4, "outdated": 2, "duplicate": 3}


def code_checks(today: date) -> list[dict]:
    wiki = BRAIN / "wiki"
    pages = {p.stem: p for p in wiki.rglob("*.md") if p.name not in ("index.md", "log.md", "CURATION.md")}
    index = (wiki / "index.md").read_text()
    indexed = set(LINK.findall(index))
    indexed.discard("slug")  # the index's own how-to line, not a page
    found, missing = [], {}
    for slug, p in sorted(pages.items()):
        rel = str(p.relative_to(BRAIN))
        text = p.read_text()
        for target in set(LINK.findall(text)) - set(pages):
            missing.setdefault(target, []).append(rel)
        if slug not in indexed:
            found.append({"kind": "not_in_index", "where": rel, "what": "page is not listed in wiki/index.md"})
        if "**Summary:**" not in text:
            found.append({"kind": "no_summary", "where": rel, "what": "no '> **Summary:**' line under the title"})
        if rel.startswith(tuple("wiki/" + f for f in FAST)):
            old = [d for d in AS_OF.findall(text) if (today - date.fromisoformat(d)).days > STALE_DAYS]
            if old:
                found.append({"kind": "stale_fact", "where": rel,
                              "what": f"{len(old)} fact(s) dated over {STALE_DAYS} days ago (oldest {min(old)}); recheck"})
    for target, srcs in sorted(missing.items(), key=lambda kv: -len(kv[1])):  # one finding per missing page
        found.append({"kind": "broken_link", "where": ", ".join(sorted(srcs)),
                      "what": f"[[{target}]] is linked from {len(srcs)} page(s) but has no page"})
    for target in sorted(indexed - set(pages)):
        found.append({"kind": "index_no_page", "where": "wiki/index.md", "what": f"lists [[{target}]], which has no page"})
    mem = (BRAIN / "MEMORY.md").read_text().splitlines()
    if len(mem) > MEMORY_LIMIT:
        found.append({"kind": "memory_long", "where": "MEMORY.md", "what": f"{len(mem)} lines (limit {MEMORY_LIMIT})"})
    old_ev = [l for l in mem if (m := EVENT.match(l)) and (today - date.fromisoformat(m.group(1))).days > EVENT_DAYS]
    if old_ev:
        found.append({"kind": "old_events", "where": "MEMORY.md",
                      "what": f"{len(old_ev)} [E] line(s) older than {EVENT_DAYS} days; merge or drop unless still needed"})
    return found


def model_review(local, code_found: list[dict]) -> tuple[list[dict], str]:
    listed = "\n".join(f"- {f['where']}: {f['what']}" for f in code_found) or "(none)"
    prompt = f"""You are JARVIS doing the weekly audit of your own brain at {BRAIN}. Today is {local:%Y-%m-%d}.
READ ONLY: do not edit, create or delete anything. Use Read, Grep and Glob.

Read MEMORY.md, USER.md, wiki/index.md, then every page under wiki/ (skip wiki/log.md and raw/).
Look only for problems code can't find:
- contradiction: two places say different things about the same fact (give both places).
- outdated: a fact the rest of the brain shows is no longer true (e.g. a plan that already happened,
  a model or tool that was replaced, a status that changed).
- duplicate: two pages that cover the same subject and should be merged.
Be strict: report a problem only when you can point to the text. No style notes, no "could add".
At most 12 findings, most important first. For each, propose one concrete fix.

Already found by code (don't repeat these):
{listed}

Reply with ONLY a JSON object, no code fence:
{{"findings": [{{"kind": "contradiction|outdated|duplicate", "where": "<path(s)>", "what": "<the problem, quoting briefly>", "fix": "<the change to make>"}}],
  "note": "<one sentence on the brain's overall shape>"}}"""
    raw = ask_claude(prompt, timeout=1500,
                     extra=["--add-dir", str(BRAIN), "--allowedTools", "Read,Grep,Glob"])
    data = json.loads(raw[raw.index("{"): raw.rindex("}") + 1])
    keep = [f for f in data.get("findings", []) if f.get("kind") in ("contradiction", "outdated", "duplicate")]
    return keep, data.get("note", "")


CODE_FIX = {"broken_link": "create the page or fix/remove the link", "not_in_index": "add a line to wiki/index.md",
            "index_no_page": "remove the line or create the page", "no_summary": "add a one-line summary",
            "stale_fact": "recheck against the source and update the date", "memory_long": "move detail into wiki pages",
            "old_events": "merge or drop old [E] lines"}


KIND_CAP = 15  # one kind of problem can cost at most this many points, so a single habit can't sink the score


def score(findings: list[dict]) -> int:
    per = {}
    for f in findings:
        per[f["kind"]] = per.get(f["kind"], 0) + WEIGHTS.get(f["kind"], 1)
    return max(0, 100 - sum(min(v, KIND_CAP) for v in per.values()))


def report(local, findings, note, health, prev) -> str:
    trend = f" (last week {prev})" if prev is not None else ""
    counts = {}
    for f in findings:
        counts[f["kind"]] = counts.get(f["kind"], 0) + 1
    lines = [f"# Brain audit, {local:%Y-%m-%d}", "",
             f"> **Health: {health}/100**{trend}. {note}".rstrip(), "",
             "Nothing has been changed. Terry replies **fix the audit** (all) or **fix 1, 3** (some); the",
             "session that gets the reply applies those fixes, commits, and ticks them here.", "",
             "| Kind | Count | Points each |", "|---|---:|---:|"]
    lines += [f"| {k} | {n} | {WEIGHTS.get(k, 1)} |" for k, n in sorted(counts.items())] or ["| none | 0 | 0 |"]
    lines += ["", "## Proposed fixes", ""]
    for i, f in enumerate(findings, 1):
        lines.append(f"{i}. [ ] **{f['kind']}** · `{f['where']}`: {f['what']}  \n   Fix: {f.get('fix') or CODE_FIX.get(f['kind'], '')}")
    if not findings:
        lines.append("None. Clean week.")
    return "\n".join(lines) + "\n"


def commit(path) -> None:
    rel = str(path.relative_to(BRAIN))
    subprocess.run(["flock", "-w", "120", str(BRAIN / ".sync.lock"), "bash", "-c",
                    f'cd "{BRAIN}" && git add -- {rel!r} && git commit -q -m "audit: {path.stem}" && '
                    f'(git pull -q --no-rebase --no-edit && git push -q)'],
                   capture_output=True, text=True, timeout=300)


def main(argv) -> int:
    force = "--force" in argv
    local = now_local()
    today = local.date()
    state = read_state(JOB, {})
    week = f"{today.isocalendar().year}-W{today.isocalendar().week}"
    due = (local.weekday() == int(CFG.get("AUDIT_WEEKDAY", "6")) and local.hour >= int(CFG.get("AUDIT_HOUR", "4")))
    if not force and (state.get("last_week") == week or not due):
        return 0

    subprocess.run(["git", "-C", str(BRAIN), "pull", "-q", "--no-rebase", "--no-edit"], capture_output=True, timeout=120)
    findings = code_checks(today)
    try:
        model, note = model_review(local, findings)
    except Exception as e:
        model, note = [], f"(The model review failed: {str(e)[:160]}; this score counts code checks only.)"
        log(JOB, f"model review failed: {e}")
    # Model findings first: they're the judgment calls Terry most needs to see.
    findings = model + findings
    health, prev = score(findings), state.get("health")
    text = report(local, findings, note, health, prev)

    if DRY:
        print(text)
        log(JOB, f"health {health}, {len(findings)} findings")
        return 0
    path = BRAIN / "audits" / f"{today.isoformat()}.md"
    path.parent.mkdir(exist_ok=True)
    path.write_text(text)
    if "--no-commit" not in argv:
        commit(path)
    queue = read_state("brief-queue", [])
    trend = "" if prev is None else (f", up from {prev}" if health > prev else f", down from {prev}" if health < prev else ", same as last week")
    queue.append(f"Weekly brain audit: health {health}/100{trend}, {len(findings)} proposed fixes "
                 f"(audits/{path.name}). Reply 'fix the audit' to apply them, or 'fix 1, 3' for some.")
    write_state("brief-queue", queue)
    write_state(JOB, {"last_week": week, "health": health, "report": f"audits/{path.name}", "findings": len(findings)})
    log(JOB, f"{week}: health {health}, {len(findings)} findings -> audits/{path.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
