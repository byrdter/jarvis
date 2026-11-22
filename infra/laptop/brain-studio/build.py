#!/usr/bin/env python3
"""Build the galaxy data for Brain Studio from jarvis-brain.

Walks the brain's markdown, types each note by its folder, links notes through [[wikilinks]],
relative .md links and title mentions, and writes viewer/graph-data.js:

    const GRAPH = {brain, built, groups: {...}, nodes: [{id, key, label, g, e, ...}], links: [{source, target}]}

Every node's id equals its index in `nodes`; the server and the viewer look nodes up by index.
The output holds excerpts of private notes, so it is gitignored and only ever served on 127.0.0.1.

Stdlib only. Usage: build.py [--brain PATH] [--out PATH]
"""
import json
import os
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
BRAIN = Path(os.environ.get("JARVIS_BRAIN", Path.home() / "code/jarvis-brain"))
OUT = HERE / "viewer" / "graph-data.js"
SKIP_DIRS = {".git", ".obsidian", "node_modules", "scripts", "__pycache__"}
EXCERPT = 700

# Group = what the node is. Order matters: first matching prefix wins. Colors follow the brain palette
# (JARVIS gold at the core) and stay readable on black.
GROUPS = [
    # key,        legend name,       color,     path prefixes
    ("core",     "Core",            "#f5c451", ["CLAUDE.md", "SOUL.md", "USER.md", "MEMORY.md", "HEARTBEAT.md"]),
    ("people",   "People",          "#f472b6", ["wiki/people/"]),
    ("projects", "Projects",        "#fb923c", ["wiki/projects/"]),
    ("concepts", "Concepts",        "#fbbf24", ["wiki/concepts/"]),
    ("tools",    "Tools",           "#60a5fa", ["wiki/tools/"]),
    ("models",   "Models",          "#a78bfa", ["wiki/models/"]),
    ("apps",     "Apps",            "#34d399", ["wiki/apps/"]),
    ("wiki",     "Wiki",            "#e7e5e4", ["wiki/"]),
    ("lab",      "Lab",             "#2dd4bf", ["lab/", "evals/"]),
    ("journal",  "Daily journal",   "#94a3b8", ["daily/"]),
    ("memory",   "Session memory",  "#818cf8", ["raw/claude-memory/", "raw/jarvis-private-context/"]),
    ("sources",  "Sources",         "#64748b", ["raw/"]),
    ("work",     "Working files",   "#78716c", ["audits/", "drafts/", "proposals/"]),
]
GROUP_OF = {k: (name, color) for k, name, color, _ in GROUPS}
# Groups whose titles count as mention targets: curated pages only. Raw dumps and journals mention
# everything in passing, so their titles would wire the whole galaxy together.
MENTION_TARGETS = {"people", "projects", "concepts", "tools", "models", "apps"}
# Size of a group's stars in the viewer (base radius before the degree bonus).
RADIUS = {"core": 9, "people": 6, "projects": 6, "concepts": 5, "tools": 5, "models": 5, "apps": 5,
          "wiki": 4.5, "lab": 4, "journal": 3.5, "memory": 2.6, "sources": 3, "work": 2.6}


def group_for(rel: str) -> str:
    for key, _, _, prefixes in GROUPS:
        if any(rel == p or rel.startswith(p) for p in prefixes):
            return key
    return "work"


def strip_front_matter(text: str) -> str:
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            return text[end + 4:]
    return text


def title_of(rel: str, text: str) -> str:
    m = re.search(r"^# (.+)$", text, re.M)
    if m:
        return m.group(1).strip()
    stem = Path(rel).stem
    if stem.upper() in {"README", "INDEX", "SKILL"}:
        stem = Path(rel).parent.name or stem
    return stem.replace("-", " ").replace("_", " ")


def excerpt_of(text: str) -> str:
    """The note's opening, minus its H1, front matter and blank runs: what a reader sees first."""
    body = re.sub(r"^# .+\n?", "", strip_front_matter(text), count=1).strip()
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    # The summary blockquote is shown on its own line in the inspector; don't repeat it in the excerpt.
    body = re.sub(r"\A(?:>[^\n]*\n?)*?>\s*\*\*Summary:\*\*(?:[^\n]*\n?)(?:>[^\n]*\n?)*", "", body).strip()
    body = re.sub(r"\n{3,}", "\n\n", body)
    return body[:EXCERPT].rstrip() + ("…" if len(body) > EXCERPT else "")


def summary_of(text: str) -> str:
    m = re.search(r"\*\*Summary:\*\*\s*(.+?)(?:\n(?!>)|\n>\s*\n|$)", text, re.S)
    if m:
        return re.sub(r"\s*\n>\s*", " ", m.group(1)).strip()[:240]
    for line in strip_front_matter(text).splitlines():
        s = line.strip().lstrip(">").strip()
        if s and not s.startswith(("#", "|", "-", "<!--", "```")) and len(s) > 30:
            return s[:240]
    return ""


def brain_notes(brain: Path) -> list[Path]:
    out = []
    for root, dirs, files in os.walk(brain):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not d.startswith("."))
        for f in sorted(files):
            if f.endswith(".md"):
                out.append(Path(root) / f)
    return out


def build(brain: Path = BRAIN) -> dict:
    notes = []
    for path in brain_notes(brain):
        rel = str(path.relative_to(brain))
        text = path.read_text(errors="replace")
        g = group_for(rel)
        notes.append({"key": rel, "label": title_of(rel, text), "g": g, "text": text,
                      "mtime": int(path.stat().st_mtime), "words": len(text.split())})

    # Hubs: one star per group, all tied to the core, so link-free notes still form a cluster.
    present = [k for k, *_ in GROUPS if any(n["g"] == k for n in notes)]
    nodes = []
    for k in present:
        nodes.append({"key": f"hub:{k}", "label": GROUP_OF[k][0], "g": k, "hub": True,
                      "e": "", "s": f"Every note in {GROUP_OF[k][0]}.", "r": 7})
    hub_id = {n["g"]: i for i, n in enumerate(nodes)}
    for n in notes:
        nodes.append({"key": n["key"], "label": n["label"], "g": n["g"], "e": excerpt_of(n["text"]),
                      "s": summary_of(n["text"]), "m": n["mtime"], "w": n["words"], "r": RADIUS[n["g"]]})
    note_offset = len(present)
    for i, n in enumerate(nodes):
        n["id"] = i

    # Lookups for link resolution.
    by_path = {n["key"]: n["id"] for n in nodes[note_offset:]}
    by_stem: dict[str, int] = {}
    for n in nodes[note_offset:]:
        by_stem.setdefault(Path(n["key"]).stem.lower(), n["id"])
        by_stem.setdefault(n["label"].lower(), n["id"])

    edges: set[tuple[int, int]] = set()

    def link(a: int, b: int):
        if a != b:
            edges.add((min(a, b), max(a, b)))

    mention_targets = [(n["id"], n["label"]) for n in nodes[note_offset:]
                       if n["g"] in MENTION_TARGETS and len(n["label"]) >= 6]
    mention_res = [(i, re.compile(r"(?<![\w-])" + re.escape(lbl) + r"(?![\w-])", re.I))
                   for i, lbl in mention_targets]

    for n, raw in zip(nodes[note_offset:], notes):
        me, text = n["id"], raw["text"]
        link(me, hub_id[n["g"]])
        for target in re.findall(r"\[\[([^\]|#]+)(?:[#|][^\]]*)?\]\]", text):
            t = target.strip().lower()
            hit = by_stem.get(Path(t).stem) or by_stem.get(t)
            if hit is not None:
                link(me, hit)
        for target in re.findall(r"\]\(([^)#\s]+\.md)(?:#[^)]*)?\)", text):
            if target.startswith(("http:", "https:")):
                continue
            p = os.path.normpath(os.path.join(os.path.dirname(n["key"]), target))
            hit = by_path.get(p) or by_stem.get(Path(p).stem.lower())
            if hit is not None:
                link(me, hit)
        for i, rx in mention_res:
            if i != me and rx.search(text):
                link(me, i)

    core_hub = hub_id.get("core")
    for k, i in hub_id.items():
        if core_hub is not None and i != core_hub:
            link(i, core_hub)

    groups = {k: {"name": GROUP_OF[k][0], "color": GROUP_OF[k][1]} for k in present}
    return {"brain": str(brain), "built": int(time.time()), "groups": groups, "nodes": nodes,
            "links": [{"source": a, "target": b} for a, b in sorted(edges)]}


def write(graph: dict, out: Path = OUT) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(".tmp")
    tmp.write_text("// Built by build.py from jarvis-brain. Private: never commit, never serve off 127.0.0.1.\n"
                   "const GRAPH = " + json.dumps(graph, ensure_ascii=False, separators=(",", ":")) + ";\n")
    tmp.replace(out)


def main(argv: list[str]) -> int:
    brain, out = BRAIN, OUT
    if "--brain" in argv:
        brain = Path(argv[argv.index("--brain") + 1]).expanduser()
    if "--out" in argv:
        out = Path(argv[argv.index("--out") + 1]).expanduser()
    if not brain.is_dir():
        print(f"brain not found: {brain}", file=sys.stderr)
        return 1
    g = build(brain)
    write(g, out)
    notes = sum(1 for n in g["nodes"] if not n.get("hub"))
    print(f"{notes} notes, {len(g['links'])} links, {len(g['groups'])} groups -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
