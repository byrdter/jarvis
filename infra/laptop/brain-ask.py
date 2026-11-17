#!/usr/bin/env python3
"""Ask the brain, locally. A free, offline chat that answers from jarvis-brain and names its sources.

How it works:
  1. index: split the brain's markdown into sections and embed each with nomic-embed-text (Ollama).
     Only changed files are re-embedded. The index lives outside git at ~/.local/share/jarvis/.
  2. ask: find the sections closest to the question (meaning + shared words), hand them to the local
     model (qwen3.8:27b by default) with the rule "answer only from these, cite [n]".
  3. serve: the same thing as a chat page at http://localhost:8765, with sources you can open.
  4. search: just the matching sections, no answer. For Claude sessions (laptop, Telegram, server
     jobs) that want to search the brain by meaning; they write the answer themselves.

Usage: brain-ask.py index
       brain-ask.py ask "what time does the morning brief go out?"
       brain-ask.py serve [--port 8765]
       brain-ask.py search "who is Ray Fu?" [-k 8] [--full]   (runs on the server too)
Env:   BRAIN_ASK_MODEL (default qwen3.8:27b), JARVIS_BRAIN (default ~/code/jarvis-brain)

Stdlib only. Nothing leaves the machine: Ollama runs on localhost and the page binds to 127.0.0.1."""
import json
import math
import os
import re
import sys
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

BRAIN = Path(os.environ.get("JARVIS_BRAIN", Path.home() / "code/jarvis-brain"))
INDEX = Path(os.environ.get("BRAIN_ASK_INDEX", Path.home() / ".local/share/jarvis/brain-index.json"))
API = "http://localhost:11434/api"
EMBED = "nomic-embed-text"
MODEL = os.environ.get("BRAIN_ASK_MODEL", "qwen3.8:27b")
TOP_K = int(os.environ.get("BRAIN_ASK_K", 8))
MAX_CHARS = int(os.environ.get("BRAIN_ASK_CHARS", 900))  # per section; longer ones split at blank lines/bullets
KW = float(os.environ.get("BRAIN_ASK_KW", 0.25))         # weight of the shared-words bonus
# Curated pages beat raw material: daily logs and source dumps mention everything in passing, so they
# take a small penalty and only win when they are clearly the best match.
RAW_PENALTY = float(os.environ.get("BRAIN_ASK_RAW", 0.03))
RAW_PREFIXES = ("daily/", "raw/")

# What counts as the brain. drafts/ and evals/ are working files, CLAUDE.md is instructions.
INCLUDE_DIRS = ["wiki", "daily", "lab", "raw/sources", "raw/claude-memory", "raw/jarvis-private-context",
                "raw/reports", "audits", "proposals"]
INCLUDE_FILES = ["MEMORY.md", "USER.md", "SOUL.md", "HEARTBEAT.md", "CLAUDE.md"]

STOP = set("""a an and are as at be but by can could did do does for from had has have how i if in into is
it its me my no not of on or our so than that the their them then there these they this to us was we were
what when where which who why will with would you your about any all also been more most should""".split())


def post(path: str, body: dict, timeout: int = 600):
    req = urllib.request.Request(f"{API}/{path}", json.dumps(body).encode(),
                                 {"Content-Type": "application/json"})
    return urllib.request.urlopen(req, timeout=timeout)


def embed(texts: list[str]) -> list[list[float]]:
    out = []
    for i in range(0, len(texts), 32):
        r = json.loads(post("embed", {"model": EMBED, "input": texts[i:i + 32], "keep_alive": "30m"}).read())
        out += r["embeddings"]
    return out


def brain_files() -> list[Path]:
    files = [BRAIN / f for f in INCLUDE_FILES if (BRAIN / f).exists()]
    for d in INCLUDE_DIRS:
        files += sorted((BRAIN / d).rglob("*.md")) if (BRAIN / d).exists() else []
    return files


def chunks(path: Path) -> list[dict]:
    """Split one file into sections at headings; split long sections at blank lines."""
    rel = str(path.relative_to(BRAIN))
    text = path.read_text(errors="replace")
    title = next((l.lstrip("# ").strip() for l in text.splitlines() if l.startswith("# ")), rel)
    parts, head, buf = [], "", []
    for line in text.splitlines():
        if re.match(r"#{1,3} ", line) and buf:
            parts.append((head, "\n".join(buf)))
            buf = []
        if re.match(r"#{1,3} ", line):
            head = line.lstrip("# ").strip()
        buf.append(line)
    if buf:
        parts.append((head, "\n".join(buf)))
    out = []
    for head, body in parts:
        body = body.strip()
        if len(body) < 40:
            continue
        pieces, cur = [], ""
        for para in re.split(r"\n\s*\n|\n(?=- )", body):
            if cur and len(cur) + len(para) > MAX_CHARS:
                pieces.append(cur)
                cur = ""
            cur = (cur + "\n" + para).strip()[:MAX_CHARS * 2]
        if cur:
            pieces.append(cur)
        for p in pieces:
            label = f"{title} › {head}" if head and head != title else title
            out.append({"file": rel, "label": label, "text": p})
    return out


def load_index() -> dict:
    try:
        return json.loads(INDEX.read_text())
    except (OSError, ValueError):
        return {"files": {}, "chunks": []}


def update_index(quiet: bool = False) -> dict:
    """Re-embed only files whose modification time changed; drop files that are gone."""
    idx = load_index()
    params = {"chars": MAX_CHARS, "embed": EMBED}
    if idx.get("params") != params:
        idx = {"files": {}, "chunks": []}
    seen, changed = {}, []
    for f in brain_files():
        rel = str(f.relative_to(BRAIN))
        seen[rel] = f.stat().st_mtime
        if idx["files"].get(rel) != seen[rel]:
            changed.append(f)
    gone = set(idx["files"]) - set(seen)
    if not changed and not gone:
        return idx
    drop = gone | {str(f.relative_to(BRAIN)) for f in changed}
    keep = [c for c in idx["chunks"] if c["file"] not in drop]
    new = [c for f in changed for c in chunks(f)]
    if new:
        vecs = embed([f"search_document: {c['label']}\n{c['text']}" for c in new])
        for c, v in zip(new, vecs):
            c["vec"] = [round(x, 5) for x in v]
    idx = {"params": params, "files": seen, "chunks": keep + new}
    INDEX.parent.mkdir(parents=True, exist_ok=True)
    tmp = INDEX.with_suffix(f".tmp{os.getpid()}")  # two searches at once mustn't share a temp file
    tmp.write_text(json.dumps(idx))
    tmp.replace(INDEX)
    if not quiet:
        print(f"indexed {len(changed)} changed file(s), removed {len(gone)}; {len(idx['chunks'])} sections total")
    return idx


def words(s: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9][a-z0-9.\-]*[a-z0-9]|[a-z0-9]", s.lower()) if w not in STOP}


def search(idx: dict, question: str, k: int = TOP_K) -> list[dict]:
    """Hybrid score: meaning (cosine) plus a bonus for sharing the question's rarer words, so names,
    model numbers and dates still win when the embedding blurs them."""
    q = embed([f"search_query: {question}"])[0]
    qn = math.sqrt(sum(x * x for x in q))
    qw = words(question)
    n = len(idx["chunks"]) or 1
    cw = [words(c["label"] + " " + c["text"]) for c in idx["chunks"]]
    df = {w: sum(1 for s in cw if w in s) for w in qw}
    scored = []
    for c, ws in zip(idx["chunks"], cw):
        v = c["vec"]
        cos = sum(a * b for a, b in zip(q, v)) / (qn * math.sqrt(sum(x * x for x in v)) or 1)
        hit = sum(math.log(1 + n / df[w]) for w in qw if df[w] and w in ws)
        best = sum(math.log(1 + n / df[w]) for w in qw if df[w]) or 1
        pen = RAW_PENALTY if c["file"].startswith(RAW_PREFIXES) else 0
        scored.append((cos + KW * hit / best - pen, c))
    scored.sort(key=lambda t: -t[0])
    picked, per_file = [], {}
    for s, c in scored:                       # at most 2 sections from one file, so answers see breadth
        if per_file.get(c["file"], 0) >= 2:
            continue
        per_file[c["file"]] = per_file.get(c["file"], 0) + 1
        picked.append({"file": c["file"], "label": c["label"], "text": c["text"], "score": round(s, 3)})
        if len(picked) == k:
            break
    return picked


SYSTEM = """You are JARVIS, Terry Byrd's second brain, running on a local model on his laptop.
Answer ONLY from the numbered sources from his brain below, and cite every fact with its number, like [2].
If the sources answer part of the question, give that part and say what they don't cover.
If they don't answer it at all, reply exactly: The brain doesn't say.
Never use general knowledge to fill gaps. Give the answer only: no reasoning out loud, no notes about the
sources or these rules. Brief and plain, American English, speaking to Terry as "you"."""


def messages(question: str, hits: list[dict], history: list[dict]) -> list[dict]:
    src = "\n\n".join(f"[{i}] {h['file']} ({h['label']})\n{h['text']}" for i, h in enumerate(hits, 1))
    return ([{"role": "system", "content": SYSTEM}] + history[-4:] +
            [{"role": "user", "content": f"SOURCES:\n{src}\n\nQUESTION: {question}"}])


def stream_answer(msgs: list[dict]):
    body = {"model": MODEL, "messages": msgs, "stream": True, "think": False, "keep_alive": "30m",
            "options": {"temperature": 0.2, "num_ctx": 16384}}
    with post("chat", body) as r:
        for line in r:
            if line.strip():
                d = json.loads(line)
                yield d.get("message", {}).get("content", "")


def cmd_ask(question: str) -> int:
    idx = update_index(quiet=True)
    hits = search(idx, question)
    for piece in stream_answer(messages(question, hits, [])):
        print(piece, end="", flush=True)
    print("\n\nSources:")
    for i, h in enumerate(hits, 1):
        print(f"  [{i}] {h['file']}  ({h['label']})  score {h['score']}")
    return 0


def cmd_search(argv: list[str]) -> int:
    k = int(argv[argv.index("-k") + 1]) if "-k" in argv else TOP_K
    full = "--full" in argv
    skip = {"-k", "--full"} | ({argv[argv.index("-k") + 1]} if "-k" in argv else set())
    question = " ".join(a for a in argv if a not in skip).strip()
    if not question:
        print('usage: brain-ask.py search "question" [-k 8] [--full]')
        return 1
    idx = update_index(quiet=True)
    for i, h in enumerate(search(idx, question, k), 1):
        text = h["text"] if full else (h["text"][:600] + ("…" if len(h["text"]) > 600 else ""))
        print(f"[{i}] {h['file']} · {h['label']} · score {h['score']}\n{text}\n")
    return 0


PAGE = (Path(__file__).parent / "brain-ask.html")


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def send(self, code: int, body: bytes, ctype: str):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            return self.send(200, PAGE.read_bytes(), "text/html; charset=utf-8")
        if self.path == "/status":
            idx = load_index()
            return self.send(200, json.dumps({"model": MODEL, "files": len(idx["files"]),
                                              "sections": len(idx["chunks"])}).encode(), "application/json")
        self.send(404, b"not found", "text/plain")

    def do_POST(self):
        if self.path != "/ask":
            return self.send(404, b"not found", "text/plain")
        req = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
        question = (req.get("question") or "").strip()
        history = [m for m in req.get("history", []) if m.get("role") in ("user", "assistant")]
        # A follow-up ("and for images?") means little alone, so search with the previous question too.
        prev = next((m["content"] for m in reversed(history) if m["role"] == "user"), "")
        try:
            hits = search(update_index(quiet=True), f"{prev} {question}".strip())
        except Exception as e:
            return self.send(503, f"Ollama isn't answering ({e}). Is the Ollama app running?".encode(),
                             "text/plain")
        # Newline-delimited JSON: first the sources, then answer text as it's written.
        self.send_response(200)
        self.send_header("Content-Type", "application/x-ndjson")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write((json.dumps({"sources": hits}) + "\n").encode())
        self.wfile.flush()
        try:
            for piece in stream_answer(messages(question, hits, history)):
                self.wfile.write((json.dumps({"text": piece}) + "\n").encode())
                self.wfile.flush()
        except BrokenPipeError:
            pass
        except Exception as e:
            self.wfile.write((json.dumps({"text": f"\n\n(The model stopped: {e})"}) + "\n").encode())
        self.close_connection = True


def cmd_serve(port: int) -> int:
    try:
        update_index()
    except Exception as e:
        print(f"index not updated yet ({e}); will retry on the first question")
    print(f"brain chat on http://localhost:{port}  (model {MODEL})", flush=True)
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
    return 0


def main(argv: list[str]) -> int:
    if not argv or argv[0] not in ("index", "ask", "serve", "search"):
        print(__doc__)
        return 1
    if argv[0] == "index":
        update_index()
        return 0
    if argv[0] == "ask":
        return cmd_ask(" ".join(argv[1:]))
    if argv[0] == "search":
        return cmd_search(argv[1:])
    port = int(argv[argv.index("--port") + 1]) if "--port" in argv else 8765
    return cmd_serve(port)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
