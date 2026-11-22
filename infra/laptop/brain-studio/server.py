#!/usr/bin/env python3
"""Brain Studio server: the galaxy page, plus a brain you can talk to.

  GET  /                 the viewer (viewer/ only; nothing else on disk is reachable)
  GET  /api/note?id=N    one note's full text, for "Read full note"
  POST /api/chat         {"q": "..."} -> {"answer", "nodes", "about_notes", "ms"}
  POST /api/reset        forget the conversation
  POST /api/remember     {"text": "..."} -> a new note in captures/, a line in today's daily log, a live star
  GET  /api/engine       {"engine": "claude"|"local", "model"}; POST {"engine": ...} switches brains
  POST /api/rebuild      re-run build.py (new or edited notes) without restarting

How /api/chat answers: brain-ask.py's hybrid search (Ollama embeddings + shared rare words, ~0.3 s)
picks the closest notes, then the `claude` CLI writes a short spoken answer from ONLY those notes and
says which ones it used. It runs on Terry's Claude plan, so there is no API key anywhere. If Ollama is
down, a keyword score over the galaxy stands in.

Binds to 127.0.0.1 only: the page holds excerpts of private notes. Stdlib only.
Usage: server.py [--port 4700] [--model sonnet]
"""
import importlib.util
import json
import os
import re
import socket
import subprocess
import sys
import threading
import time
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

HERE = Path(__file__).resolve().parent
VIEWER = HERE / "viewer"
BRAIN = Path(os.environ.get("JARVIS_BRAIN", Path.home() / "code/jarvis-brain")).resolve()
RUN_DIR = Path.home() / ".local/share/jarvis/brain-studio/run"   # neutral cwd: no CLAUDE.md, no hooks
PORT = 4700
MODEL = os.environ.get("BRAIN_STUDIO_MODEL", "sonnet")
LOCAL_MODEL = os.environ.get("BRAIN_STUDIO_LOCAL_MODEL", "qwen3.5:9b")   # fast enough to talk to; 27b is smarter, slower
OLLAMA = "http://localhost:11434/api"
ENGINE = {"name": os.environ.get("BRAIN_STUDIO_ENGINE", "claude")}          # "claude" (plan) or "local" (Ollama)
TOP_K = 8          # notes handed to the model per question
HISTORY_TURNS = 4  # past exchanges kept for follow-ups

# ─── PERSONA ─────────────────────────────────────────────────────────────────────────────────────
# Who JARVIS is when you talk to the galaxy. Rewrite this block to change the character; nothing else
# in the file depends on its wording. It follows SOUL.md: a friend, warm, honest, American English.
PERSONA = """You are JARVIS, Terry Byrd's second brain and working partner, talking with him out loud. You
sound like a friend in the room: warm, quick, a little dry, on his side, honest when something won't
work. Use contractions. Say "Terry" now and then, not every reply. American English.

This is a conversation, not a lookup:
- Reply the way a person would: react to what he actually said, then answer. Usually one to three short
  sentences. Ask a short question back when it would keep things moving, not every time.
- No lists, no markdown, no reading notes aloud (they're on his screen). Give the point.
- For facts about Terry, his work, his people and his plans, use the notes below. If they don't cover
  it, say so in a few words and offer what you do know. Never invent a source or claim a note says
  something it doesn't.
- General knowledge (how something works, an opinion, a joke) is fine without notes. Just don't
  dress it up as something from his brain.
- Never say you did something unless the action field below does it.

Small talk ("good morning", "thanks", a joke) gets a short warm reply with no notes: about_notes false.

You can do ONE thing yourself, through the action field: switch which brain answers.
- "switch_local" when he asks to use the local / offline / Ollama / Qwen brain or model.
- "switch_claude" when he asks to go back to Claude / the cloud.
- otherwise "none". When you switch, the answer is one short line saying you're switching.

Reply with ONE JSON object and nothing else, no code fence:
{"about_notes": true|false, "answer": "<what you say out loud>", "sources": [<ids of notes you used>], "action": "none"|"switch_local"|"switch_claude"}
List a note in sources only if the answer depends on it."""
# ─────────────────────────────────────────────────────────────────────────────────────────────────

_lock = threading.Lock()
_graph: dict = {}
_history: list[dict] = []
_brain_ask = None


def load_brain_ask():
    """brain-ask.py lives in infra/laptop; import it by path (its name has a hyphen)."""
    global _brain_ask
    if _brain_ask is None:
        path = HERE.parent / "brain-ask.py"
        spec = importlib.util.spec_from_file_location("brain_ask", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _brain_ask = mod
    return _brain_ask


def rebuild() -> dict:
    sys.path.insert(0, str(HERE))
    import build
    g = build.build(BRAIN)
    build.write(g)
    with _lock:
        _graph.clear()
        _graph.update(g)
        _graph["by_key"] = {n["key"]: n["id"] for n in g["nodes"]}
    return g


def note_path(node: dict) -> Path | None:
    if node.get("hub"):
        return None
    p = (BRAIN / node["key"]).resolve()
    return p if p.is_relative_to(BRAIN) and p.is_file() else None


# ─── retrieval ───────────────────────────────────────────────────────────────────────────────────
WORD = re.compile(r"[a-z0-9][a-z0-9.\-]*[a-z0-9]|[a-z0-9]")


def keyword_hits(q: str, k: int) -> list[dict]:
    """Fallback when Ollama is down: shared words, title matches weighted 3x."""
    qw = {w for w in WORD.findall(q.lower()) if len(w) > 2}
    scored = []
    for n in _graph["nodes"]:
        if n.get("hub"):
            continue
        title = set(WORD.findall(n["label"].lower()))
        body = set(WORD.findall((n["s"] + " " + n["e"]).lower()))
        s = 3 * len(qw & title) + len(qw & body)
        if s:
            scored.append((s, n))
    scored.sort(key=lambda t: -t[0])
    return [{"file": n["key"], "label": n["label"], "text": n["e"]} for _, n in scored[:k]]


def retrieve(q: str) -> tuple[list[dict], str]:
    try:
        ba = load_brain_ask()
        idx = ba.update_index(quiet=True)
        return ba.search(idx, q, k=TOP_K), "meaning"
    except Exception as e:  # Ollama off, index missing: answer anyway, say how
        print(f"brain-ask search failed ({e}); using keyword fallback", file=sys.stderr)
        return keyword_hits(q, TOP_K), "keywords"


# ─── the brain ───────────────────────────────────────────────────────────────────────────────────
def ask_claude(prompt: str) -> str:
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    env = {**os.environ, "CLAUDE_INVOKED_BY": "brain-studio"}  # memory_flush skips job sessions
    cmd = ["claude", "-p", "--model", MODEL, "--effort", "low", "--setting-sources", "",
           "--tools", "", "--strict-mcp-config", "--no-session-persistence",
           "--output-format", "json", "--system-prompt", PERSONA, prompt]
    r = subprocess.run(cmd, cwd=RUN_DIR, env=env, capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        raise RuntimeError((r.stderr or r.stdout).strip()[:400] or f"claude exited {r.returncode}")
    return json.loads(r.stdout).get("result", "")


def ollama(path: str, body: dict | None = None, timeout: int = 180) -> dict:
    import urllib.request
    req = urllib.request.Request(f"{OLLAMA}/{path}", json.dumps(body).encode() if body is not None else None,
                                 {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def ask_local(prompt: str) -> str:
    """Same persona, same notes, answered by a model on this Mac. Nothing leaves the machine."""
    r = ollama("chat", {"model": LOCAL_MODEL, "stream": False, "think": False, "format": "json",
                        "keep_alive": "30m", "options": {"temperature": 0.3, "num_ctx": 16384},
                        "messages": [{"role": "system", "content": PERSONA},
                                     {"role": "user", "content": prompt}]})
    return r.get("message", {}).get("content", "")


def set_engine(name: str) -> dict:
    if name not in ("claude", "local"):
        raise ValueError(f"unknown engine {name!r}")
    if name == "local":
        try:
            have = {m["name"] for m in ollama("tags", timeout=5).get("models", [])}
        except Exception:
            raise RuntimeError("Ollama isn't running on this Mac")
        if LOCAL_MODEL not in have:
            raise RuntimeError(f"{LOCAL_MODEL} isn't installed (ollama pull {LOCAL_MODEL})")
    ENGINE["name"] = name
    return engine_info()


def where_you_are() -> str:
    """Facts about this running session, handed to the model every turn so it never has to guess
    (asked "where are you?", the local model said it wasn't running anywhere)."""
    host = socket.gethostname().removesuffix(".local")
    notes = sum(1 for n in _graph.get("nodes", []) if not n.get("hub"))
    if ENGINE["name"] == "local":
        brain = (f"the LOCAL brain: {LOCAL_MODEL} running in Ollama on this Mac. Nothing Terry says or "
                 "reads here leaves the machine")
    else:
        brain = (f"CLAUDE ({MODEL}) on Terry's Claude plan. The question and these notes go to Anthropic "
                 "to be answered")
    return (f"Where you are right now (facts, use them if asked):\n"
            f"- You are JARVIS in Brain Studio, the 3D galaxy of Terry's brain, served from his Mac "
            f"({host}) at http://127.0.0.1:{PORT}. The galaxy has {notes} notes from ~/code/jarvis-brain.\n"
            f"- You are answering with {brain}.\n"
            f"- Engines: Claude (orange orb) or the local brain (green orb). Terry switches by saying "
            f"\"switch to the local brain\" or \"use Claude\", or you switch through the action field.\n"
            f"- Past answers below are labeled with the engine that gave them; the other engine's answers "
            f"were not yours.")


def engine_info() -> dict:
    return {"engine": ENGINE["name"], "model": LOCAL_MODEL if ENGINE["name"] == "local" else MODEL}


def parse_reply(text: str) -> dict:
    """Pull the reply object out of whatever the model sent. Models sometimes wrap it in prose, a
    ```json fence, or send it twice ("Correction: here it is on its own"); a greedy {.*} spanning all of
    that fails to parse and the whole mess got spoken. Take the LAST complete object that has an answer."""
    dec, found, i = json.JSONDecoder(), None, text.find("{")
    while i != -1:
        try:
            obj, end = dec.raw_decode(text, i)
            if isinstance(obj, dict) and str(obj.get("answer", "")).strip():
                found = obj
            i = text.find("{", end)
        except ValueError:
            i = text.find("{", i + 1)
    if found:
        return found
    m = re.search(r'"answer"\s*:\s*"((?:[^"\\]|\\.)*)"?', text)      # a truncated object: keep its answer
    if m:
        return {"about_notes": False, "answer": json.loads(f'"{m.group(1)}"'), "sources": []}
    plain = re.sub(r"```(?:json)?|[{}]", "", text).strip()
    return {"about_notes": False, "answer": plain, "sources": []}


def chat(q: str) -> dict:
    t0 = time.time()
    hits, mode = retrieve(q)
    # One block per note (a note can return two sections); label each with its galaxy id.
    blocks: dict[int, list[str]] = {}
    titles: dict[int, str] = {}
    for h in hits:
        nid = _graph["by_key"].get(h["file"])
        if nid is None:
            continue
        blocks.setdefault(nid, []).append(h["text"])
        titles[nid] = _graph["nodes"][nid]["label"]
    notes = "\n\n".join(f"<note id={nid} title=\"{titles[nid]}\">\n" + "\n…\n".join(parts) + "\n</note>"
                        for nid, parts in blocks.items())
    # Each past answer is labeled with the engine that gave it, so after a switch neither brain owns
    # (or apologizes for) the other's words.
    convo = "".join(f"Terry: {t['q']}\nJARVIS ({t.get('by', '?')}): {t['a']}\n" for t in _history[-HISTORY_TURNS:])
    prompt = (where_you_are() + "\n\n"
              + f"Notes from the brain (closest matches to the question):\n\n{notes or '(none found)'}\n\n"
              + (f"Conversation so far:\n{convo}\n" if convo else "")
              + f"Terry: {q}")
    engine = ENGINE["name"]
    reply = parse_reply(ask_local(prompt) if engine == "local" else ask_claude(prompt))
    # The model can act on exactly one thing: which brain answers. However Terry phrases "switch to the
    # local model", the model understands it, so the page's regex is only the fast path.
    act = {"switch_local": "local", "switch_claude": "claude"}.get(str(reply.get("action", "")))
    if act and act != ENGINE["name"]:
        try:
            set_engine(act)
            reply["about_notes"], reply["sources"] = False, []
        except Exception as e:
            reply["answer"] = f"I couldn't switch: {e}."
    used = [int(i) for i in reply.get("sources", []) if str(i).isdigit() and int(i) in blocks]
    about = bool(reply.get("about_notes")) and bool(used)
    answer = str(reply.get("answer", "")).strip() or "I lost my train of thought there. Ask me again?"
    _history.append({"q": q, "a": answer, "by": f"local {LOCAL_MODEL}" if engine == "local" else f"Claude {MODEL}"})
    del _history[:-HISTORY_TURNS]
    return {"answer": answer, "nodes": used if about else [], "about_notes": about,
            "considered": list(blocks), "retrieval": mode, "ms": int((time.time() - t0) * 1000),
            **engine_info()}


# ─── remember: ONE door for new notes ────────────────────────────────────────────────────────────
# "Remember that…" becomes (1) a real note in captures/, a star in the galaxy and searchable in the very
# next question, and (2) one line in today's daily log, which the nightly reflection promotes into
# MEMORY.md / USER.md / wiki. daily/ is append-only and union-merged, so appending is safe from any machine.
# Anything that creates a note goes through capture(); the viewer's addNote() is its other half.
CAPTURES = BRAIN / "captures"


def slugify(s: str, n: int = 6) -> str:
    words = re.findall(r"[a-z0-9]+", s.lower())[:n]
    return "-".join(words) or "note"


def capture(fact: str) -> dict:
    fact = re.sub(r"\s+", " ", fact).strip().strip('"').strip()
    if len(fact) < 4:
        raise ValueError("there was nothing to remember")
    fact = fact[0].upper() + fact[1:]
    if fact[-1] not in ".!?":
        fact += "."
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    words = fact.rstrip(".!?").split()
    title = " ".join(words[:8]) + ("…" if len(words) > 8 else "")

    # Duplicate check: the same fact twice today is one memory, not two.
    for old in CAPTURES.glob(f"{date}-*.md"):
        if fact in old.read_text(errors="replace"):
            nid = _graph["by_key"].get(str(old.relative_to(BRAIN)))
            return {"duplicate": True, "node": _graph["nodes"][nid] if nid is not None else None,
                    "hub": None, "links": [], "say": "I already have that one."}

    # Link it to what it is about: the closest curated notes (not journals or raw dumps).
    hits, _ = retrieve(fact)
    related = []
    for h in hits:
        if h["file"].startswith(("daily/", "raw/", "captures/")) or h["file"] in related:
            continue
        if h.get("score", 1) < 0.55 and related:  # weak matches only if nothing better
            continue
        related.append(h["file"])
        if len(related) == 3:
            break

    CAPTURES.mkdir(parents=True, exist_ok=True)
    path = CAPTURES / f"{date}-{slugify(fact)}.md"
    k = 2
    while path.exists():
        path = CAPTURES / f"{date}-{slugify(fact)}-{k}.md"
        k += 1
    rel = str(path.relative_to(BRAIN))
    links_line = " · ".join(f"[[{Path(r).stem}]]" for r in related)
    body = (f"# {title}\n\n> **Summary:** {fact}\n\n"
            f"Said to JARVIS in Brain Studio, {now:%A %B %-d, %Y at %-I:%M %p}.\n\n{fact}\n"
            + (f"\nRelated: {links_line}\n" if related else ""))
    path.write_text(body)
    if path.read_text() != body:               # a capture that didn't land must never look saved
        raise OSError(f"{rel} did not save correctly")

    daily = BRAIN / "daily" / f"{date}.md"
    entry = (f"\n## {now:%H:%M} · Mac · Brain Studio capture\n\n**Learned:**\n"
             f"- [S] Terry asked JARVIS to remember: {fact} (`{rel}`)\n")
    with daily.open("a") as f:
        if f.tell() == 0:
            f.write(f"# {date}\n")
        f.write(entry)

    # Live graph: append (never rebuild) so every id the open page holds stays valid.
    sys.path.insert(0, str(HERE))
    import build
    with _lock:
        nodes = _graph["nodes"]
        new_hub = None
        hub = next((n for n in nodes if n.get("hub") and n["g"] == "captures"), None)
        links = []
        if hub is None:
            name, color = build.GROUP_OF["captures"]
            new_hub = hub = {"key": "hub:captures", "label": name, "g": "captures", "hub": True,
                             "e": "", "s": f"Every note in {name}.", "r": 7, "id": len(nodes)}
            nodes.append(hub)
            _graph["groups"]["captures"] = {"name": name, "color": color}
            core = next((n for n in nodes if n.get("hub") and n["g"] == "core"), None)
            if core:
                links.append({"source": hub["id"], "target": core["id"]})
        node = {"key": rel, "label": title, "g": "captures", "s": fact,
                "e": f"Said to JARVIS in Brain Studio, {now:%A %B %-d, %Y at %-I:%M %p}.",
                "m": int(path.stat().st_mtime), "w": len(body.split()), "r": build.RADIUS["captures"],
                "id": len(nodes)}
        nodes.append(node)
        _graph["by_key"][rel] = node["id"]
        links.append({"source": node["id"], "target": hub["id"]})
        for r in related:
            if r in _graph["by_key"]:
                links.append({"source": node["id"], "target": _graph["by_key"][r]})
        _graph["links"].extend(links)
        build.write({k: v for k, v in _graph.items() if k != "by_key"})

    # Push it to GitHub in the background so the server and Telegram know it within a minute.
    sync = BRAIN / "scripts/brain-sync.sh"
    if sync.exists():
        subprocess.Popen(["bash", str(sync)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                         start_new_session=True)
    return {"duplicate": False, "node": node, "hub": new_hub, "links": links, "groups": _graph["groups"],
            "say": "Got it. That's in the brain now."}


# ─── HTTP ────────────────────────────────────────────────────────────────────────────────────────
TYPES = {".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8",
         ".css": "text/css; charset=utf-8", ".svg": "image/svg+xml", ".png": "image/png",
         ".json": "application/json", ".webmanifest": "application/manifest+json"}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *a):
        # a[0] is the request line for access logs, but an HTTPStatus for send_error(); don't crash on it.
        if a and isinstance(a[0], str) and "/api/" in a[0]:
            sys.stderr.write("%s\n" % (fmt % a))

    def do_HEAD(self):   # health checks probe with HEAD; answer instead of logging a 501 traceback
        self.send_response(200 if urlparse(self.path).path in ("/", "/index.html") else 404)
        self.end_headers()

    def send(self, code: int, body: bytes, ctype: str):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def json(self, code: int, obj: dict):
        self.send(code, json.dumps(obj).encode(), "application/json")

    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/api/engine":
            return self.json(200, engine_info())
        if url.path == "/api/note":
            try:
                node = _graph["nodes"][int(parse_qs(url.query)["id"][0])]
            except (KeyError, ValueError, IndexError):
                return self.json(404, {"error": "no such note"})
            p = note_path(node)
            return self.json(200, {"key": node["key"], "text": p.read_text(errors="replace") if p else ""})
        rel = url.path.lstrip("/") or "index.html"
        f = (VIEWER / rel).resolve()
        if not f.is_relative_to(VIEWER.resolve()) or not f.is_file():
            return self.send(404, b"not found", "text/plain")
        self.send(200, f.read_bytes(), TYPES.get(f.suffix, "application/octet-stream"))

    def do_POST(self):
        path = urlparse(self.path).path
        n = int(self.headers.get("Content-Length") or 0)
        try:
            body = json.loads(self.rfile.read(n) or b"{}")
        except ValueError:
            return self.json(400, {"error": "bad json"})
        if path == "/api/chat":
            q = str(body.get("q", "")).strip()[:2000]
            if not q:
                return self.json(400, {"error": "empty question"})
            try:
                return self.json(200, chat(q))
            except subprocess.TimeoutExpired:
                return self.json(504, {"error": "The brain took too long to answer."})
            except Exception as e:
                return self.json(500, {"error": f"The brain call failed: {e}"})
        if path == "/api/remember":
            try:
                return self.json(200, capture(str(body.get("text", ""))[:4000]))
            except Exception as e:  # never fail silently: the viewer says this out loud
                return self.json(500, {"error": f"I couldn't save that: {e}"})
        if path == "/api/engine":
            try:
                return self.json(200, set_engine(str(body.get("engine", ""))))
            except Exception as e:
                return self.json(400, {"error": str(e)})
        if path == "/api/reset":
            _history.clear()
            return self.json(200, {"ok": True})
        if path == "/api/rebuild":
            g = rebuild()
            return self.json(200, {"notes": sum(1 for x in g["nodes"] if not x.get("hub")),
                                   "links": len(g["links"])})
        self.json(404, {"error": "unknown route"})


def main(argv: list[str]) -> int:
    global MODEL, PORT
    port = PORT = int(argv[argv.index("--port") + 1]) if "--port" in argv else PORT
    if "--model" in argv:
        MODEL = argv[argv.index("--model") + 1]
    g = rebuild()
    print(f"galaxy: {sum(1 for x in g['nodes'] if not x.get('hub'))} notes, {len(g['links'])} links")
    srv = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"Brain Studio on http://127.0.0.1:{port}  (model {MODEL}; Ctrl-C to stop)")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
