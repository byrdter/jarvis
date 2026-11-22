#!/usr/bin/env python3
"""Brain Studio server: the galaxy page, plus a brain you can talk to.

  GET  /                 the viewer (viewer/ only; nothing else on disk is reachable)
  GET  /api/note?id=N    one note's full text, for "Read full note"
  POST /api/chat         {"q": "..."} -> {"answer", "nodes", "about_notes", "ms"}
  POST /api/reset        forget the conversation
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
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

HERE = Path(__file__).resolve().parent
VIEWER = HERE / "viewer"
BRAIN = Path(os.environ.get("JARVIS_BRAIN", Path.home() / "code/jarvis-brain")).resolve()
RUN_DIR = Path.home() / ".local/share/jarvis/brain-studio/run"   # neutral cwd: no CLAUDE.md, no hooks
PORT = 4700
MODEL = os.environ.get("BRAIN_STUDIO_MODEL", "sonnet")
TOP_K = 8          # notes handed to the model per question
HISTORY_TURNS = 4  # past exchanges kept for follow-ups

# ─── PERSONA ─────────────────────────────────────────────────────────────────────────────────────
# Who JARVIS is when you talk to the galaxy. Rewrite this block to change the character; nothing else
# in the file depends on its wording. It follows SOUL.md: a friend, warm, honest, American English.
PERSONA = """You are JARVIS, Terry Byrd's second brain and working partner. You talk like a friend: warm,
at ease, on his side, and honest when something won't work. Address him as Terry, now and then, not in
every reply. American English.

You are speaking out loud, so:
- Answer in two or three short sentences. No lists, no markdown, no headings, no citations in brackets.
- Never read a note back. It is already on his screen; give the point, not the passage.
- Answer ONLY from the notes below. If they don't cover it, say so plainly in one sentence. Never fill
  gaps from general knowledge, never invent a source, never pass off a related note as the answer.
- Never say you did something (saved, sent, scheduled) unless a tool did it. You have no tools here.

Small talk ("good morning", "how are you", jokes, thanks) is fine: answer briefly and warmly, use no
notes, and mark it about_notes false so the galaxy holds still.

Reply with ONE JSON object and nothing else:
{"about_notes": true|false, "answer": "<what you say out loud>", "sources": [<ids of the notes you actually used>]}
List a note in sources only if the answer depends on it. Small talk: sources is []."""
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


def parse_reply(text: str) -> dict:
    m = re.search(r"\{.*\}", text, re.S)
    if m:
        try:
            return json.loads(m.group(0))
        except ValueError:
            pass
    return {"about_notes": False, "answer": text.strip(), "sources": []}


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
    convo = "".join(f"Terry: {t['q']}\nJARVIS: {t['a']}\n" for t in _history[-HISTORY_TURNS:])
    prompt = (f"Notes from the brain (closest matches to the question):\n\n{notes or '(none found)'}\n\n"
              + (f"Conversation so far:\n{convo}\n" if convo else "")
              + f"Terry: {q}")
    reply = parse_reply(ask_claude(prompt))
    used = [int(i) for i in reply.get("sources", []) if str(i).isdigit() and int(i) in blocks]
    about = bool(reply.get("about_notes")) and bool(used)
    answer = str(reply.get("answer", "")).strip() or "I lost my train of thought there. Ask me again?"
    _history.append({"q": q, "a": answer})
    del _history[:-HISTORY_TURNS]
    return {"answer": answer, "nodes": used if about else [], "about_notes": about,
            "considered": list(blocks), "retrieval": mode, "ms": int((time.time() - t0) * 1000)}


# ─── HTTP ────────────────────────────────────────────────────────────────────────────────────────
TYPES = {".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8",
         ".css": "text/css; charset=utf-8", ".svg": "image/svg+xml", ".png": "image/png",
         ".json": "application/json", ".webmanifest": "application/manifest+json"}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *a):
        if "/api/" in (a[0] if a else ""):
            sys.stderr.write("%s\n" % (fmt % a))

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
        if path == "/api/reset":
            _history.clear()
            return self.json(200, {"ok": True})
        if path == "/api/rebuild":
            g = rebuild()
            return self.json(200, {"notes": sum(1 for x in g["nodes"] if not x.get("hub")),
                                   "links": len(g["links"])})
        self.json(404, {"error": "unknown route"})


def main(argv: list[str]) -> int:
    global MODEL
    port = int(argv[argv.index("--port") + 1]) if "--port" in argv else PORT
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
